const JSON_HEADERS = { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store', Vary: 'Origin' };
const STUDIO_ORIGINS = new Set([
  'https://www.keydesign.studio', 'https://keydesign.studio',
  'https://keydesign-studio-xxxxx.web.app', 'https://keydesign-studio-xxxxx.firebaseapp.com',
]);

function clean(value, max) {
  if (typeof value !== 'string') return '';
  const trimmed = value.trim().replace(/<[^>]*>/g, '');
  if (!trimmed) return '';
  return [...trimmed].slice(0, max).join('');
}

async function sendTelegram(botToken, chatId, text) {
  const url = `https://api.telegram.org/bot${botToken}/sendMessage`;
  const response = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      chat_id: chatId,
      text,
      disable_web_page_preview: true,
    }),
  });

  if (!response.ok) return false;
  const result = await response.json();
  return Boolean(result && result.ok);
}

function jsonResponse(statusCode, body) {
  return {
    statusCode,
    headers: JSON_HEADERS,
    body: JSON.stringify(body),
  };
}

async function submitBrief(event) {
  if (event.httpMethod !== 'POST') {
    return jsonResponse(405, { ok: false, error: 'method' });
  }

  let data;
  try {
    data = JSON.parse(event.body || '');
  } catch {
    return jsonResponse(400, { ok: false, error: 'json' });
  }

  if (!data || typeof data !== 'object' || Array.isArray(data)) {
    return jsonResponse(400, { ok: false, error: 'json' });
  }

  if (data.company) {
    return jsonResponse(200, { ok: true });
  }

  const botToken = process.env.TELEGRAM_BOT_TOKEN || '';
  const chatIdsRaw = process.env.TELEGRAM_CHAT_ID || '';
  const chatIds = chatIdsRaw
    .split(',')
    .map((id) => id.trim())
    .filter(Boolean);

  if (!botToken || chatIds.length === 0) {
    return jsonResponse(500, { ok: false, error: 'config' });
  }

  const area = clean(data.area, 80);
  const timeline = clean(data.timeline, 80);
  const name = clean(data.name, 120);
  const phone = clean(data.phone, 40);
  const page = clean(data.page, 200);

  if (!name || !phone) {
    return jsonResponse(422, { ok: false, error: 'validation' });
  }

  const lines = [
    'Новая заявка с сайта Key Design Studio',
    '',
    `Метраж: ${area || '-'}`,
    `Сроки: ${timeline || '-'}`,
    `Имя: ${name}`,
    `Телефон: ${phone}`,
  ];

  if (page) {
    lines.push(`Страница: ${page}`);
  }

  const text = lines.join('\n');

  let sent = 0;
  for (const chatId of chatIds) {
    if (await sendTelegram(botToken, chatId, text)) {
      sent += 1;
    }
  }

  if (sent === 0) {
    return jsonResponse(502, { ok: false, error: 'telegram' });
  }

  return jsonResponse(200, { ok: true });
}

exports.handler = async (event) => {
  const origin = event.headers?.origin;
  const headers = { ...JSON_HEADERS };
  if (origin) {
    const sameOrigin = event.rawUrl && new URL(event.rawUrl).origin === origin;
    if (!sameOrigin && !STUDIO_ORIGINS.has(origin)) {
      return jsonResponse(403, { ok: false, error: 'origin' });
    }
    headers['Access-Control-Allow-Origin'] = origin;
  }
  if (event.httpMethod === 'OPTIONS') {
    headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS';
    headers['Access-Control-Allow-Headers'] = 'Content-Type';
    return { statusCode: 204, headers, body: '' };
  }
  const response = await submitBrief(event);
  return { ...response, headers };
};
