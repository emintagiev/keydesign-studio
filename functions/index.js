const { onRequest } = require("firebase-functions/v2/https");
const { defineSecret } = require("firebase-functions/params");

const TELEGRAM_BOT_TOKEN = defineSecret("TELEGRAM_BOT_TOKEN");
const TELEGRAM_CHAT_ID = defineSecret("TELEGRAM_CHAT_ID");

function clean(value, max) {
  if (typeof value !== "string") return "";
  const trimmed = value.trim().replace(/<[^>]*>/g, "");
  if (!trimmed) return "";
  return [...trimmed].slice(0, max).join("");
}

async function sendTelegram(botToken, chatId, text) {
  const url = `https://api.telegram.org/bot${botToken}/sendMessage`;
  const response = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
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

exports.brief = onRequest(
  {
    region: "us-central1",
    secrets: [TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID],
    cors: true,
  },
  async (req, res) => {
    if (req.method === "OPTIONS") {
      res.set("Access-Control-Allow-Methods", "POST, OPTIONS");
      res.set("Access-Control-Allow-Headers", "Content-Type");
      res.status(204).send("");
      return;
    }

    if (req.method !== "POST") {
      res.status(405).json({ ok: false, error: "method" });
      return;
    }

    const data = req.body;
    if (!data || typeof data !== "object" || Array.isArray(data)) {
      res.status(400).json({ ok: false, error: "json" });
      return;
    }

    if (data.company) {
      res.status(200).json({ ok: true });
      return;
    }

    const botToken = TELEGRAM_BOT_TOKEN.value() || "";
    const chatIds = (TELEGRAM_CHAT_ID.value() || "")
      .split(",")
      .map((id) => id.trim())
      .filter(Boolean);

    if (!botToken || chatIds.length === 0) {
      res.status(500).json({ ok: false, error: "config" });
      return;
    }

    const area = clean(data.area, 80);
    const timeline = clean(data.timeline, 80);
    const name = clean(data.name, 120);
    const phone = clean(data.phone, 40);
    const page = clean(data.page, 200);

    if (!name || !phone) {
      res.status(422).json({ ok: false, error: "validation" });
      return;
    }

    const lines = [
      "Новая заявка с сайта Key Design Studio",
      "",
      `Метраж: ${area || "-"}`,
      `Сроки: ${timeline || "-"}`,
      `Имя: ${name}`,
      `Телефон: ${phone}`,
    ];

    if (page) {
      lines.push(`Страница: ${page}`);
    }

    const text = lines.join("\n");

    let sent = 0;
    for (const chatId of chatIds) {
      if (await sendTelegram(botToken, chatId, text)) {
        sent += 1;
      }
    }

    if (sent === 0) {
      res.status(502).json({ ok: false, error: "telegram" });
      return;
    }

    res.status(200).json({ ok: true });
  }
);
