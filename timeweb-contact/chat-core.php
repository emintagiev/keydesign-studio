<?php
declare(strict_types=1);

// The database and credentials live outside the public directory.
final class StudioChat {
    private $db;
    private $token;
    private $destinations;
    private $send;

    public function __construct(PDO $db, string $token, array $destinations, callable $send) {
        $this->db = $db;
        $this->token = $token;
        $this->destinations = $destinations;
        $this->send = $send;
        $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        $db->exec("PRAGMA busy_timeout=5000");
        $db->exec("CREATE TABLE IF NOT EXISTS messages (
            seq INTEGER PRIMARY KEY, room TEXT NOT NULL, event TEXT NOT NULL,
            side TEXT NOT NULL, body TEXT NOT NULL, state TEXT NOT NULL,
            created INTEGER NOT NULL, UNIQUE(room,event))");
        $db->exec("CREATE INDEX IF NOT EXISTS chat_time ON messages(created)");
        $db->exec("CREATE TABLE IF NOT EXISTS limits (scope TEXT PRIMARY KEY, total INTEGER, expires INTEGER)");
    }

    private function query(string $sql, array $params) {
        $q = $this->db->prepare($sql);
        $q->execute($params);
        return $q;
    }

    public function prune(): void {
        $this->query("DELETE FROM messages WHERE created < ?", [time()-7*86400]);
        $this->query("DELETE FROM limits WHERE expires < ?", [time()]);
    }

    private function quota(string $key, int $period, int $max): bool {
        $slot = intdiv(time(), $period);
        $scope = hash_hmac('sha256', $key . ':' . $slot, $this->token);
        $this->query("INSERT INTO limits(scope,total,expires) VALUES (?,1,?)
            ON CONFLICT(scope) DO UPDATE SET total=total+1 WHERE total < ?", [$scope, ($slot+1)*$period, $max]);
        return (bool)$this->db->query("SELECT changes()")->fetchColumn();
    }

    public function visitor(array $data, string $ip): array {
        $secret = $data['session'] ?? null;
        if (!is_string($secret) || !preg_match('/^[0-9a-f]{64}$/D', $secret)) return [422, []];
        $room = hash_hmac('sha256', $secret, $this->token);
        if (($data['action'] ?? '') === 'read') {
            $rows = $this->query("SELECT side,body AS text,seq FROM messages WHERE room=? AND state='sent' AND created>=? ORDER BY seq DESC LIMIT 120",
                [$room,time()-7*86400])->fetchAll(PDO::FETCH_ASSOC);
            return [200, ['messages'=>array_reverse($rows)]];
        }
        if (($data['action'] ?? '') !== 'send') return [400, []];
        $id = $data['id'] ?? null;
        $name = is_string($data['name'] ?? null) ? trim($data['name']) : '';
        $text = is_string($data['text'] ?? null) ? trim($data['text']) : '';
        if (!is_string($id) || !preg_match('/^[a-f0-9]{32}$/D',$id) || !$name || mb_strlen($name)>100 ||
            $text === '' || mb_strlen($text)>1500 || ($data['consent'] ?? false)!==true || !empty($data['company'])) return [422, []];
        $this->db->exec('BEGIN IMMEDIATE');
        try {
            $existing = $this->query("SELECT state FROM messages WHERE room=? AND event=?",[$room,$id])->fetchColumn();
            if ($existing) {
                $this->db->exec('COMMIT');
                return [$existing==='sent' ? 200 : 409, ['delivery'=>$existing]];
            }
            if (!$this->quota('ip:'.$ip,600,12) || !$this->quota('site',3600,100)) {
                $this->db->exec('COMMIT');
                return [429, []];
            }
            $this->query("INSERT INTO messages(room,event,side,body,state,created) VALUES (?,?,'visitor',?,'pending',?)",[$room,$id,$text,time()]);
            $this->db->exec('COMMIT');
        } catch (Throwable $e) {
            $this->db->exec('ROLLBACK');
            throw $e;
        }
        $notice = "Вопрос с сайта #".$room."\n".$name."\n\n".$text."\n\nЧтобы ответ появился у посетителя, нажмите «Ответить» на это сообщение.";
        $confirmed = false;
        $uncertain = false;
        foreach ($this->destinations as $dest) {
            try {
                $result = ($this->send)($dest, $notice);
                $confirmed = $confirmed || $result === true;
                $uncertain = $uncertain || $result === null;
            } catch (Throwable $e) { $uncertain = true; }
        }
        if (!$confirmed && !$uncertain) {
            $this->query("DELETE FROM messages WHERE room=? AND event=? AND state='pending'",[$room,$id]);
            return [502, []];
        }
        $this->query("UPDATE messages SET state=? WHERE room=? AND event=?",[$confirmed?'sent':'unknown',$room,$id]);
        return [$confirmed?200:409,['delivery'=>$confirmed?'sent':'unknown']];
    }

    public function reply(array $update): void {
        $m = $update['message'] ?? [];
        $parent = $m['reply_to_message'] ?? [];
        $id = (string)($m['chat']['id'] ?? '');
        if (!in_array($id,$this->destinations,true) || empty($m['message_id']) || !empty($m['from']['is_bot']) ||
            empty($parent['from']['is_bot']) || (string)($parent['from']['id'] ?? '')!==explode(':',$this->token,2)[0] ||
            !is_string($m['text'] ?? null) || trim($m['text'])==='' ||
            !preg_match('/^Вопрос с сайта #([a-f0-9]{64})\n/u',$parent['text'] ?? '',$match)) return;
        $this->query("INSERT OR IGNORE INTO messages(room,event,side,body,state,created)
            SELECT ?,?,'studio',?,'sent',? WHERE EXISTS (SELECT 1 FROM messages WHERE room=? AND side='visitor' AND created>=?)",
            [$match[1],'reply:'.$id.':'.$m['message_id'],mb_substr($m['text'],0,4096),time(),$match[1],time()-7*86400]);
    }
}
