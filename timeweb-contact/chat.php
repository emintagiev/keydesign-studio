<?php
declare(strict_types=1);
require_once __DIR__.'/chat-core.php';

header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store');
header('X-Robots-Tag: noindex');
function finishChat(int $code, array $body=[]): void {
    http_response_code($code);
    echo json_encode(['ok'=>$code===200]+$body,JSON_UNESCAPED_UNICODE);
    exit;
}

if (($_SERVER['HTTP_HOST'] ?? '') !== 'keydesign-contact.tw1.ru') finishChat(404);
$origin = $_SERVER['HTTP_ORIGIN'] ?? '';
$sites = ['https://www.keydesign.studio','https://keydesign.studio'];
if ($origin !== '' && !in_array($origin,$sites,true)) finishChat(403);
if ($origin) {
    header('Access-Control-Allow-Origin: '.$origin);
    header('Vary: Origin');
}
$method = $_SERVER['REQUEST_METHOD'] ?? '';
if ($method==='OPTIONS') {
    header('Access-Control-Allow-Methods: POST, OPTIONS');
    header('Access-Control-Allow-Headers: Content-Type');
    http_response_code(204);
    exit;
}
if ($method!=='POST') finishChat(405);
if (stripos($_SERVER['CONTENT_TYPE'] ?? '','application/json')!==0) finishChat(415);
try {
    $dir = dirname(__DIR__,2).'/studio-chat-private';
    $config = require dirname(__DIR__,2).'/Keydesign.studio/public_html/api/brief-secrets.php';
    $destinations = $config['chat_ids'] ?? ($config['chat_id'] ?? []);
    if (!is_array($destinations)) $destinations = explode(',', (string)$destinations);
    $destinations = array_values(array_filter(array_map('trim',array_map('strval',$destinations))));
    if (!$destinations || empty($config['bot_token'])) finishChat(503);
    $token = $config['bot_token'];
    $webhook = isset($_GET['webhook']);
    if ($webhook && !hash_equals(hash_hmac('sha256','studio-chat-webhook-v1',$token),$_SERVER['HTTP_X_TELEGRAM_BOT_API_SECRET_TOKEN'] ?? '')) finishChat(403);
    if (!$webhook && !$origin) finishChat(403);
    $raw = file_get_contents('php://input', false, null, 0, 65537);
    if (strlen($raw)>65536) finishChat(413);
    $data = json_decode($raw,true);
    if (!is_array($data)) finishChat(400);
    $dispatch = function ($dest,$text) use ($token) {
        $ch = curl_init('https://api.telegram.org/bot'.$token.'/sendMessage');
        curl_setopt_array($ch,[CURLOPT_POST=>true,CURLOPT_RETURNTRANSFER=>true,CURLOPT_CONNECTTIMEOUT=>4,CURLOPT_TIMEOUT=>8,
            CURLOPT_POSTFIELDS=>['chat_id'=>$dest,'text'=>$text,'disable_web_page_preview'=>'true']]);
        $reply = json_decode((string)curl_exec($ch),true);
        return isset($reply['ok']) ? $reply['ok']===true : null;
    };
    umask(0077);
    if (!is_dir($dir) && !mkdir($dir,0700) && !is_dir($dir)) finishChat(503);
    $chat = new StudioChat(new PDO('sqlite:'.$dir.'/messages.sqlite'),$token,$destinations,$dispatch);
    $chat->prune();
    if ($webhook) { $chat->reply($data); finishChat(200); }
    [$status,$result] = $chat->visitor($data,$_SERVER['REMOTE_ADDR'] ?? '');
    finishChat($status,$result);
} catch (Throwable $e) {
    finishChat(503);
}
