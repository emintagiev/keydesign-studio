<?php
/**
 * Decap CMS GitHub OAuth proxy for Key Design Studio.
 * Deploy to /oauth/ on Timeweb. Secrets in oauth-secrets.php (not in git).
 */

declare(strict_types=1);

$configFile = __DIR__ . '/oauth-secrets.php';
if (!is_file($configFile)) {
    http_response_code(500);
    header('Content-Type: text/plain; charset=utf-8');
    echo 'OAuth secrets missing. Create oauth/oauth-secrets.php on server.';
    exit;
}

$config = require $configFile;
$clientId = $config['client_id'] ?? '';
$clientSecret = $config['client_secret'] ?? '';
$baseUrl = rtrim($config['base_url'] ?? 'https://www.keydesign.studio/oauth', '/');

if ($clientId === '' || $clientSecret === '') {
    http_response_code(500);
    header('Content-Type: text/plain; charset=utf-8');
    echo 'OAuth client_id / client_secret not configured.';
    exit;
}

$path = parse_url($_SERVER['REQUEST_URI'] ?? '/', PHP_URL_PATH) ?: '/';
$path = rtrim($path, '/');
$basename = basename($path);

if ($basename === 'auth' || str_ends_with($path, '/auth')) {
    $state = bin2hex(random_bytes(8));
    $redirectUri = $baseUrl . '/callback?provider=github';
    $params = http_build_query([
        'client_id' => $clientId,
        'redirect_uri' => $redirectUri,
        'scope' => 'repo user',
        'state' => $state,
        'response_type' => 'code',
    ]);
    header('Location: https://github.com/login/oauth/authorize?' . $params, true, 302);
    exit;
}

if ($basename === 'callback' || str_ends_with($path, '/callback')) {
    $provider = $_GET['provider'] ?? 'github';
    if ($provider !== 'github') {
        http_response_code(400);
        echo 'Invalid provider';
        exit;
    }

    $code = $_GET['code'] ?? '';
    if ($code === '') {
        http_response_code(400);
        echo 'Missing code';
        exit;
    }

    $redirectUri = $baseUrl . '/callback?provider=github';
    $payload = json_encode([
        'client_id' => $clientId,
        'client_secret' => $clientSecret,
        'code' => $code,
        'redirect_uri' => $redirectUri,
    ]);

    $ch = curl_init('https://github.com/login/oauth/access_token');
    curl_setopt_array($ch, [
        CURLOPT_POST => true,
        CURLOPT_POSTFIELDS => $payload,
        CURLOPT_HTTPHEADER => ['Accept: application/json', 'Content-Type: application/json'],
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_TIMEOUT => 30,
    ]);
    $response = curl_exec($ch);
    $httpCode = (int) curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);

    $data = json_decode($response ?: '', true);
    if ($httpCode >= 400 || empty($data['access_token'])) {
        $error = $data['error'] ?? 'token exchange failed';
        renderCallback('error', (string) $error);
        exit;
    }

    renderCallback('success', (string) $data['access_token']);
    exit;
}

header('Content-Type: text/plain; charset=utf-8');
echo 'Key Design Decap OAuth proxy';

function renderCallback(string $status, string $token): void
{
    $safeStatus = htmlspecialchars($status, ENT_QUOTES, 'UTF-8');
    $safeToken = json_encode($token, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);

    header('Content-Type: text/html; charset=utf-8');
    echo <<<HTML
<!DOCTYPE html>
<html lang="ru">
  <head><meta charset="utf-8"><title>Авторизация</title></head>
  <body>
    <script>
      const receiveMessage = (message) => {
        window.opener.postMessage(
          'authorization:github:{$safeStatus}:' + JSON.stringify({ token: {$safeToken} }),
          '*'
        );
        window.removeEventListener('message', receiveMessage, false);
      };
      window.addEventListener('message', receiveMessage, false);
      window.opener.postMessage('authorizing:github', '*');
    </script>
    <p>Авторизация Decap...</p>
  </body>
</html>
HTML;
}
