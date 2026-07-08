#!/usr/bin/env php
<?php
/**
 * Writes api/brief-secrets.php from env vars or deploy.env.
 * Usage:
 *   php scripts/write-brief-secrets.php [output-path]
 * Env: TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID (one id or comma-separated list)
 */

declare(strict_types=1);

$root = dirname(__DIR__);
$out = $argv[1] ?? ($root . '/api/brief-secrets.php');

$token = getenv('TELEGRAM_BOT_TOKEN') ?: '';
$chatRaw = getenv('TELEGRAM_CHAT_ID') ?: '';

if ($token === '' || $chatRaw === '') {
    $envFile = getenv('DEPLOY_ENV') ?: ($root . '/deploy.env');
    if (is_file($envFile)) {
        foreach (file($envFile, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES) as $line) {
            $line = trim($line);
            if ($line === '' || str_starts_with($line, '#')) {
                continue;
            }
            if (!str_contains($line, '=')) {
                continue;
            }
            [$key, $value] = explode('=', $line, 2);
            $key = trim($key);
            $value = trim($value);
            if ($key === 'TELEGRAM_BOT_TOKEN' && $token === '') {
                $token = $value;
            }
            if ($key === 'TELEGRAM_CHAT_ID' && $chatRaw === '') {
                $chatRaw = $value;
            }
        }
    }
}

$chatIds = briefParseChatIds($chatRaw);

if ($token === '' || $chatIds === []) {
    fwrite(STDERR, "TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID required\n");
    exit(1);
}

$dir = dirname($out);
if (!is_dir($dir)) {
    mkdir($dir, 0755, true);
}

$content = "<?php\n\nreturn " . var_export([
    'bot_token' => $token,
    'chat_ids' => $chatIds,
], true) . ";\n";

file_put_contents($out, $content);
fwrite(STDOUT, "Wrote {$out}\n");

function briefParseChatIds(string $raw): array
{
    $parts = preg_split('/\s*,\s*/', trim($raw)) ?: [];
    $ids = [];
    foreach ($parts as $part) {
        $part = trim($part);
        if ($part !== '') {
            $ids[] = $part;
        }
    }

    return array_values(array_unique($ids));
}
