// Vercel Serverless Function: ИИ-консультант __BRAND__. Файл собирается из src/gen_chat.py — правьте данные там.
// Нужна переменная окружения ANTHROPIC_API_KEY (Vercel → Settings → Environment Variables).
// Без ключа функция отвечает 503, и сайт сам переключается на встроенный автоответчик.

const MODEL = process.env.ANTHROPIC_MODEL || "claude-haiku-5-5";
const PHONE = "__PHONE__";

const SYSTEM = `__PROMPT__`;

const hits = new Map();
function limited(ip) {
  const now = Date.now(), win = 10 * 60 * 1000, max = 25;
  const arr = (hits.get(ip) || []).filter((t) => now - t < win);
  arr.push(now); hits.set(ip, arr);
  if (hits.size > 5000) hits.clear();
  return arr.length > max;
}

module.exports = async (req, res) => {
  res.setHeader("Cache-Control", "no-store");
  if (req.method !== "POST") { res.status(405).json({ error: "method" }); return; }
  const key = process.env.ANTHROPIC_API_KEY;
  if (!key) { res.status(503).json({ error: "not_configured" }); return; }
  const ip = (req.headers["x-forwarded-for"] || "").split(",")[0].trim() || "x";
  if (limited(ip)) { res.status(429).json({ error: "rate" }); return; }
  let body = req.body;
  if (typeof body === "string") { try { body = JSON.parse(body); } catch (e) { body = {}; } }
  const msgs = Array.isArray(body && body.messages) ? body.messages.slice(-12) : [];
  const clean = msgs.filter((m) => m && (m.role === "user" || m.role === "assistant") && typeof m.content === "string")
    .map((m) => ({ role: m.role, content: m.content.slice(0, 1500) }));
  while (clean.length && clean[0].role !== "user") clean.shift();
  if (!clean.length) { res.status(400).json({ error: "empty" }); return; }
  try {
    const r = await fetch("https://api.anthropic.com/v1/messages", {
      method: "POST",
      headers: { "x-api-key": key, "anthropic-version": "2023-06-01", "content-type": "application/json" },
      body: JSON.stringify({ model: MODEL, max_tokens: 500, system: SYSTEM + "\nСтраница: " + String((body && body.page) || "/").slice(0, 120), messages: clean }),
    });
    if (!r.ok) { res.status(502).json({ error: "upstream" }); return; }
    const d = await r.json();
    const text = (d.content || []).filter((c) => c.type === "text").map((c) => c.text).join("").trim();
    res.status(200).json({ text: text || "Уточню у менеджера. Позвоните " + PHONE + " или напишите в WhatsApp." });
  } catch (e) { res.status(502).json({ error: "fail" }); }
};
