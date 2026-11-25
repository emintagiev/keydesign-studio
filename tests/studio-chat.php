<?php
declare(strict_types=1);
if (PHP_SAPI!=='cli') exit;
require ($argv[1] ?? dirname(__DIR__).'/timeweb-contact/chat-core.php');
function check($value) { if (!$value) throw new RuntimeException('Chat assertion failed at line '.debug_backtrace()[0]['line']); }
$token = '1234:test';
$deliveries = [];
$chat = new StudioChat(new PDO('sqlite::memory:'),$token,['52'],function($id,$text) use (&$deliveries) {
    $deliveries[] = $text;
    return true;
});
$a = ['action'=>'send','session'=>bin2hex(random_bytes(32)),'id'=>bin2hex(random_bytes(16)),'name'=>'Test','text'=>'Sample question','consent'=>true];
check($chat->visitor($a,'test')[0]===200);
check($chat->visitor($a,'test')[0]===200 && count($deliveries)===1);
$event = ['message'=>['chat'=>['id'=>52],'message_id'=>8,'from'=>['is_bot'=>false],'text'=>'Sample reply',
    'reply_to_message'=>['from'=>['id'=>1234,'is_bot'=>true],'text'=>$deliveries[0]]]];
$wrong = $event; $wrong['message']['chat']['id'] = 99;
$chat->reply($wrong);
$read = ['action'=>'read','session'=>$a['session']];
check(count($chat->visitor($read,'test')[1]['messages'])===1);
$wrong = $event; $wrong['message']['reply_to_message']['from']['id']=777; $chat->reply($wrong);
check(count($chat->visitor($read,'test')[1]['messages'])===1);
$chat->reply($event); $chat->reply($event);
check(array_column($chat->visitor($read,'test')[1]['messages'],'text')===['Sample question','Sample reply']);
$read['session'] = bin2hex(random_bytes(32));
check($chat->visitor($read,'test')[1]['messages']===[]);
$a['consent']=false; check($chat->visitor($a,'test')[0]===422);
$chat->prune();
echo "KDS_ISOLATION_REPLY_RETRY_OK\n";
