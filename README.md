# 🦋 FABLE — The Interactive Legend

A creative, three-chapter web game that teaches people about **Claude Fable 5**, Anthropic's most capable publicly released model (June 9, 2026). Built around the model's name — *Fable* — it turns a product announcement into an interactive tale.

## How it works

A single self-contained `index.html`. Players progress through three chapters:

1. **Chapter I — The Scrolls of Knowledge** — a short quiz on Fable 5's real capabilities (Stripe migration, Pokémon FireRed vision run, the Fable-vs-Mythos relationship).
2. **Chapter II — Speak with the Oracle** — a live chat with Fable 5 via the [Venice API](https://venice.ai), complete with a **real-time token cost tracker** (at the model's actual $10 / $50 per-million-token rates).
3. **Chapter III — The Prophecy Revealed** — confetti, a wisdom score, and three unlocked **treasure scrolls** (illustrated infographics) you can view full-size and download, plus a generated comparison PDF.

The home screen shows hazy, locked previews of the treasure scrolls to entice players to finish.

## Design

- **Light theme** using Anthropic's brand palette: terracotta orange `#d97757`, steel blue `#6a9bcc`, cream `#faf9f5`.
- Typography: Poppins (headings) + Lora (body), per Anthropic brand guidelines.
- Material-design cards, floating butterfly particles, warm ambient canvas.

## Setup

1. Open `index.html` in any modern browser.
2. Enter your **Venice API key** (get one at [venice.ai](https://venice.ai)).
3. Model ID defaults to `claude-fable-5` (fallback: `claude-opus-4-7`).

## Assets

- `images/banner-*.png` — AI-generated chapter art (Venice `gpt-image-2`).
- `images/treasure*.png` — the three illustrated reward scrolls.
- `make_infographics.py` — deterministic Pillow renderer for data-accurate infographics (AI image models garble exact numbers, so pricing/stats are drawn programmatically).

## Tech

Pure HTML/CSS/JS · jsPDF for the comparison PDF · Venice AI API for chat + image generation.

---

*Built as a fun, non-technical-friendly way to explore what Fable 5 can do.*
