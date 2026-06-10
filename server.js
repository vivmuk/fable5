// ──────────────────────────────────────────────────────────────
// FABLE — The Interactive Legend
// Tiny Express server for Railway. Serves the static app and proxies
// the Oracle chat to Venice. The Venice key lives ONLY here, in the
// VENICE_API_KEY env var, and is never sent to the browser.
// ──────────────────────────────────────────────────────────────
import express from 'express';
import rateLimit from 'express-rate-limit';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const app  = express();
const PORT = process.env.PORT || 3000;
const VENICE_KEY = process.env.VENICE_API_KEY;
const VENICE_URL = 'https://api.venice.ai/api/v1/chat/completions';

// Only these models may be requested through the proxy.
const ALLOWED_MODELS = new Set(['claude-fable-5', 'claude-opus-4-7', 'claude-opus-4-8']);

// The Oracle's persona is fixed server-side so the proxy can't be
// repurposed as a free general-purpose LLM with someone else's key.
const SYSTEM_PROMPT =
  "You are Claude Fable 5, Anthropic's most capable model released to the public on June 9, 2026. " +
  "You are inside an interactive experience called FABLE that lets people play with you live. " +
  "Be engaging, insightful, and show off deep reasoning and creativity. " +
  "IMPORTANT: Always finish your thought. Keep answers complete and self-contained — " +
  "aim for roughly 120-300 words so you never get cut off mid-sentence.";

const MAX_PROMPT_CHARS = 1200;
const MAX_TOKENS = 1024;

app.set('trust proxy', 1);                 // Railway sits behind a proxy (correct client IPs)
app.use(express.json({ limit: '16kb' }));

// Rate limit the API surface: generous enough for the 3-query game,
// strict enough to deter abuse of the shared key.
const limiter = rateLimit({
  windowMs: 10 * 60 * 1000,                // 10 minutes
  max: 40,                                 // 40 requests / IP / window
  standardHeaders: true,
  legacyHeaders: false,
  message: { error: { message: 'Too many requests — please wait a moment and try again.' } }
});
app.use('/api/', limiter);

// ── ORACLE CHAT PROXY ──────────────────────────────────────────
app.post('/api/chat', async (req, res) => {
  if (!VENICE_KEY) {
    return res.status(500).json({ error: { message: 'Server is not configured (missing VENICE_API_KEY).' } });
  }
  try {
    const { prompt, model } = req.body || {};
    if (typeof prompt !== 'string' || !prompt.trim()) {
      return res.status(400).json({ error: { message: 'Ask the Oracle a question first.' } });
    }
    const useModel = ALLOWED_MODELS.has(model) ? model : 'claude-fable-5';

    const upstream = await fetch(VENICE_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${VENICE_KEY}`
      },
      body: JSON.stringify({
        model: useModel,
        messages: [
          { role: 'system', content: SYSTEM_PROMPT },
          { role: 'user',   content: prompt.slice(0, MAX_PROMPT_CHARS) }
        ],
        max_tokens: MAX_TOKENS,
        stream: false
      })
    });

    const data = await upstream.json().catch(() => ({}));
    return res.status(upstream.status).json(data);
  } catch (e) {
    return res.status(502).json({ error: { message: 'The Oracle is unreachable: ' + (e.message || 'unknown error') } });
  }
});

// ── HEALTH CHECK ───────────────────────────────────────────────
app.get('/healthz', (_req, res) => res.json({ ok: true, keyConfigured: Boolean(VENICE_KEY) }));

// ── STATIC APP ─────────────────────────────────────────────────
app.use(express.static(__dirname, { extensions: ['html'] }));
app.get('*', (_req, res) => res.sendFile(path.join(__dirname, 'index.html')));

app.listen(PORT, () => {
  console.log(`FABLE running on port ${PORT}  (Venice key ${VENICE_KEY ? 'configured ✓' : 'MISSING ✗'})`);
});
