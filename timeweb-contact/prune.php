<?php
declare(strict_types=1);
if (PHP_SAPI !== 'cli') { http_response_code(404); exit; }
require __DIR__.'/chat-core.php';
$file = dirname(__DIR__,2).'/studio-chat-private/messages.sqlite';
if (is_file($file)) (new StudioChat(new PDO('sqlite:'.$file),'',[],function () {}))->prune();
