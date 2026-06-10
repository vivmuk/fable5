# 🦋 FABLE — An Interactive Tale of Claude Fable 5

A short, story-driven web game that teaches people about **Claude Fable 5**, Anthropic's most capable publicly released model (June 9, 2026). Built around the model's name — *Fable*, from the Latin *fabula*, "a tale" — it turns a product launch into an interactive legend you walk through.

## How it works

A single self-contained front end (`index.html`) plus a tiny backend proxy (`server.js`). The tale is told in **two trials**, and finishing them unseals **three illustrated treasure scrolls**.

1. **Trial I — The Weaver of Worlds.** A fable about Fable 5's real powers (vision, software engineering, memory, reasoning), told as myth and grounded with fact "glints." Then you **play live with the actual Fable 5 model** — give the Weaver a real task (code, reasoning, science, creativity) and watch it answer, with a live generating progress bar and a real-time token-cost meter. Asking once breaks the first seal.
2. **Trial II — The Two Masks.** The story of Fable and Mythos as one mind behind two veils. An interactive "lift the veil" toggle shows exactly what each model exposes (safeguards, access, the shared price). Turning the mask breaks the final seals.
3. **The Treasures Unsealed.** The three scrolls are revealed — view full-size or download each.

The home screen lists the treasures as a **minimalist sealed manifest** (no spoilers), so players know what awaits without seeing it.

## The Venice proxy (why there's a server)

The live model is called through the [Venice API](https://venice.ai). The API key **must never live in the browser** — anyone could read it and run up charges. So `server.js` is a small Express app that:

- holds the key in the `VENICE_API_KEY` environment variable (server-side only),
- exposes `POST /api/chat`, building the system prompt itself and accepting only the user's question (so it can't be repurposed as a free general-purpose LLM),
- rate-limits the API, caps tokens, and serves the static front end.

### Deploy on Railway

1. Push this repo to GitHub and create a Railway project from it.
2. Set one environment variable: **`VENICE_API_KEY`** = your Venice key.
3. Railway runs `npm start` (`node server.js`) automatically. Done — visitors play with no key of their own.

Local dev:

```bash
npm install
VENICE_API_KEY=your-key npm start   # http://localhost:3000
```

## Design

- **Light theme** using Anthropic's brand palette: terracotta orange `#d97757`, steel blue `#6a9bcc`, cream `#faf9f5`.
- Typography: Poppins (headings) + Lora (body), per Anthropic brand guidelines.
- Storybook prose with drop caps, material-design cards, floating butterfly particles, warm ambient canvas.

## Assets

- `images/banner-*.png` — AI-generated chapter art (Venice `gpt-image-2`).
- `images/treasure*.png` — the three illustrated reward scrolls.
- `make_infographics.py` — a Pillow renderer kept around for data-accurate infographics (AI image models garble exact numbers, so stats/pricing can be drawn programmatically).

## Tech

Express proxy · Venice AI API (chat + image generation) · vanilla HTML/CSS/JS front end.

---

*Built as a fun, non-technical-friendly way to actually experience what Fable 5 can do.*
