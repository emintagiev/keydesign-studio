<?php
declare(strict_types=1);
if (($_SERVER['HTTP_HOST'] ?? '') !== 'keydesign-contact.tw1.ru') {
    http_response_code(404);
    exit;
}
header('Cache-Control: no-store');
require dirname(__DIR__,2).'/Keydesign.studio/public_html/api/brief.php';
