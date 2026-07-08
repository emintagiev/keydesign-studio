<?php
/**
 * Brief quiz form -> Telegram notification.
 * Secrets in brief-secrets.php (not in git).
 */

declare(strict_types=1);

header('Content-Type: application/json; charset=utf-8');

$configFile = __DIR__ . '/brief-secrets.php';
if (!is_file($configFile)) {
    http_response_code(500);
    echo json_encode(['ok' => false, 'error' => 'config'], JSON_UNESCAPED_UNICODE);
    exit;
}

$config = require $configFile;
$botToken = (string) ($config['bot_token'] ?? '');
$chatIds = briefChatIds($config);

if ($botToken === '' || $chatIds === []) {
    http_response_code(500);
    echo json_encode(['ok' => false, 'error' => 'config'], JSON_UNESCAPED_UNICODE);
    exit;
}

$allowedOrigins = [
    'https://www.keydesign.studio',
    'https://keydesign.studio',
];

$origin = $_SERVER['HTTP_ORIGIN'] ?? '';
if ($origin !== '' && in_array($origin, $allowedOrigins, true)) {
    header('Access-Control-Allow-Origin: ' . $origin);
    header('Vary: Origin');
}

if (($_SERVER['REQUEST_METHOD'] ?? '') === 'OPTIONS') {
    header('Access-Control-Allow-Methods: POST, OPTIONS');
    header('Access-Control-Allow-Headers: Content-Type');
    http_response_code(204);
    exit;
}

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    http_response_code(405);
    echo json_encode(['ok' => false, 'error' => 'method'], JSON_UNESCAPED_UNICODE);
    exit;
}

$raw = file_get_contents('php://input');
$data = json_decode($raw ?: '', true);
if (!is_array($data)) {
    http_response_code(400);
    echo json_encode(['ok' => false, 'error' => 'json'], JSON_UNESCAPED_UNICODE);
    exit;
}

if (!empty($data['company'])) {
    echo json_encode(['ok' => true], JSON_UNESCAPED_UNICODE);
    exit;
}

if (!briefRateLimitOk()) {
    http_response_code(429);
    echo json_encode(['ok' => false, 'error' => 'rate'], JSON_UNESCAPED_UNICODE);
    exit;
}

$area = briefClean($data['area'] ?? '', 80);
$style = briefClean($data['style'] ?? '', 80);
$timeline = briefClean($data['timeline'] ?? '', 80);
$name = briefClean($data['name'] ?? '', 120);
$phone = briefClean($data['phone'] ?? '', 40);
$page = briefClean($data['page'] ?? '', 200);

if ($name === '' || $phone === '') {
    http_response_code(422);
    echo json_encode(['ok' => false, 'error' => 'validation'], JSON_UNESCAPED_UNICODE);
    exit;
}

$lines = [
    'Новая заявка с сайта Key Design Studio',
    '',
    'Метраж: ' . ($area !== '' ? $area : '-'),
    'Направление: ' . ($style !== '' ? $style : '-'),
    'Сроки: ' . ($timeline !== '' ? $timeline : '-'),
    'Имя: ' . $name,
    'Телефон: ' . $phone,
];

if ($page !== '') {
    $lines[] = 'Страница: ' . $page;
}

$text = implode("\n", $lines);

$sent = 0;
foreach ($chatIds as $chatId) {
    if (briefSendTelegram($botToken, $chatId, $text)) {
        $sent++;
    }
}

if ($sent === 0) {
    http_response_code(502);
    echo json_encode(['ok' => false, 'error' => 'telegram'], JSON_UNESCAPED_UNICODE);
    exit;
}

echo json_encode(['ok' => true], JSON_UNESCAPED_UNICODE);

function briefChatIds(array $config): array
{
    $raw = $config['chat_ids'] ?? null;
    if (is_array($raw)) {
        $ids = [];
        foreach ($raw as $id) {
            $id = trim((string) $id);
            if ($id !== '') {
                $ids[] = $id;
            }
        }
        return array_values(array_unique($ids));
    }

    $legacy = trim((string) ($config['chat_id'] ?? ''));
    if ($legacy === '') {
        return [];
    }

    $parts = preg_split('/\s*,\s*/', $legacy) ?: [];
    $ids = [];
    foreach ($parts as $part) {
        $part = trim($part);
        if ($part !== '') {
            $ids[] = $part;
        }
    }

    return array_values(array_unique($ids));
}

function briefSendTelegram(string $botToken, string $chatId, string $text): bool
{
    $telegramUrl = 'https://api.telegram.org/bot' . $botToken . '/sendMessage';
    $payload = json_encode([
        'chat_id' => $chatId,
        'text' => $text,
        'disable_web_page_preview' => true,
    ], JSON_UNESCAPED_UNICODE);

    $ch = curl_init($telegramUrl);
    curl_setopt_array($ch, [
        CURLOPT_POST => true,
        CURLOPT_POSTFIELDS => $payload,
        CURLOPT_HTTPHEADER => ['Content-Type: application/json'],
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_TIMEOUT => 15,
    ]);
    $response = curl_exec($ch);
    $httpCode = (int) curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);

    $result = json_decode($response ?: '', true);
    return $httpCode === 200 && is_array($result) && ($result['ok'] ?? false);
}

function briefClean(string $value, int $max): string
{
    $value = trim(strip_tags($value));
    if ($value === '') {
        return '';
    }
    if (function_exists('mb_substr')) {
        return mb_substr($value, 0, $max);
    }
    return substr($value, 0, $max);
}

function briefRateLimitOk(): bool
{
    $ip = $_SERVER['REMOTE_ADDR'] ?? 'unknown';
    $file = sys_get_temp_dir() . '/kds-brief-' . md5($ip) . '.json';
    $now = time();
    $window = 3600;
    $maxHits = 8;
    $hits = [];

    if (is_file($file)) {
        $raw = file_get_contents($file);
        $decoded = json_decode($raw ?: '[]', true);
        if (is_array($decoded)) {
            $hits = $decoded;
        }
    }

    $hits = array_values(array_filter($hits, static function ($ts) use ($now, $window) {
        return is_int($ts) && ($now - $ts) < $window;
    }));

    if (count($hits) >= $maxHits) {
        return false;
    }

    $hits[] = $now;
    file_put_contents($file, json_encode($hits));

    return true;
}
