"""
Generate the three Fable 5 reward infographics with pixel-perfect text.
AI image models garble numbers, so these are rendered deterministically.
Data sourced from the official Anthropic announcement (June 9, 2026).
"""
from PIL import Image, ImageDraw, ImageFont
import os

OUT = os.path.join(os.path.dirname(__file__), "images")
os.makedirs(OUT, exist_ok=True)

# ── BRAND COLORS ──
CREAM     = (250, 249, 245)
WHITE     = (255, 255, 255)
DARK      = (20, 20, 19)
GRAY_M    = (120, 118, 110)
GRAY_L    = (232, 230, 220)
ORANGE    = (217, 119, 87)
ORANGE_D  = (184, 94, 62)
ORANGE_L  = (248, 232, 223)
BLUE      = (106, 155, 204)
BLUE_D    = (72, 120, 168)
BLUE_L    = (221, 234, 247)
GREEN     = (120, 140, 93)
GREEN_L   = (228, 232, 218)
GOLD      = (201, 150, 60)
GOLD_L    = (248, 238, 218)

W, H = 900, 1200

# ── FONTS (Windows) ──
FONTDIR = r"C:\Windows\Fonts"
def font(name, size):
    for cand in (name, name.lower()):
        p = os.path.join(FONTDIR, cand)
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.truetype(os.path.join(FONTDIR, "segoeui.ttf"), size)

F_BLACK  = lambda s: font("seguibl.ttf", s)   # Segoe UI Black
F_BOLD   = lambda s: font("segoeuib.ttf", s)  # Segoe UI Bold
F_SEMI   = lambda s: font("seguisb.ttf", s)   # Segoe UI Semibold
F_REG    = lambda s: font("segoeui.ttf", s)   # Segoe UI
F_MONO   = lambda s: font("consola.ttf", s)   # Consolas

# ── HELPERS ──
def rrect(d, box, r, fill=None, outline=None, width=1):
    d.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)

def text_w(d, s, f):
    return d.textbbox((0, 0), s, font=f)[2]

def center(d, cx, y, s, f, fill):
    d.text((cx - text_w(d, s, f) / 2, y), s, font=f, fill=fill)

def wrap(d, s, f, maxw):
    words = s.split()
    lines, cur = [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if text_w(d, t, f) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines

def bullets(d, x, y, items, f, color, maxw, lh=30, gap=6, dot=ORANGE):
    for it in items:
        ls = wrap(d, it, f, maxw - 18)
        d.ellipse([x, y + 9, x + 6, y + 15], fill=dot)
        for i, ln in enumerate(ls):
            d.text((x + 16, y), ln, font=f, fill=color)
            y += lh
        y += gap
    return y

def card(d, box, fill, accent=None, accent_w=6, radius=16):
    rrect(d, box, radius, fill=fill)
    if accent:
        x0, y0, x1, y1 = box
        # left accent stripe with rounded left
        d.rounded_rectangle([x0, y0, x0 + accent_w + radius, y1], radius=radius, fill=accent)
        d.rectangle([x0 + accent_w, y0, x0 + accent_w + radius, y1], fill=fill)

def header_band(d):
    # top gradient bar
    for x in range(W):
        t = x / W
        r = int(ORANGE[0] + t * (BLUE[0] - ORANGE[0]))
        g = int(ORANGE[1] + t * (BLUE[1] - ORANGE[1]))
        b = int(ORANGE[2] + t * (BLUE[2] - ORANGE[2]))
        d.line([(x, 0), (x, 6)], fill=(r, g, b))

def footer_band(d, txt):
    for x in range(W):
        t = x / W
        r = int(ORANGE[0] + t * (BLUE[0] - ORANGE[0]))
        g = int(ORANGE[1] + t * (BLUE[1] - ORANGE[1]))
        b = int(ORANGE[2] + t * (BLUE[2] - ORANGE[2]))
        d.line([(x, H - 6), (x, H)], fill=(r, g, b))
    center(d, W / 2, H - 32, txt, F_MONO(14), GRAY_M)

def new_canvas():
    img = Image.new("RGB", (W, H), CREAM)
    return img, ImageDraw.Draw(img)

# ════════════════════════════════════════════════════════
# INFOGRAPHIC 1 — CAPABILITIES
# ════════════════════════════════════════════════════════
def make_info1():
    img, d = new_canvas()
    header_band(d)

    center(d, W/2, 34, "CLAUDE FABLE 5", F_BLACK(54), ORANGE)
    center(d, W/2, 96, "KEY CAPABILITIES", F_BOLD(30), DARK)
    center(d, W/2, 138, "Anthropic  ·  Launched June 9, 2026", F_REG(18), GRAY_M)

    M = 50
    cw = W - 2*M
    y = 178

    def cap_card(title, accent, accent_l, items, height, icon):
        nonlocal y
        card(d, [M, y, W-M, y+height], WHITE, accent=accent)
        # icon chip
        rrect(d, [M+22, y+18, M+62, y+58], 10, fill=accent_l)
        center(d, M+42, y+26, icon, F_BOLD(22), accent)
        d.text((M+78, y+20), title, font=F_BOLD(23), fill=accent if accent!=GOLD else ORANGE_D)
        by = bullets(d, M+80, y+56, items, F_REG(18), DARK, cw-110, lh=27, gap=5, dot=accent)
        y += height + 16

    cap_card("SOFTWARE ENGINEERING", ORANGE, ORANGE_L, [
        "Stripe: a 50-million-line Ruby codebase migration in ONE DAY — a task that would take a full team over two months",
        "Highest score among frontier models on Cognition’s FrontierCode evaluation, even at medium effort",
    ], 150, "</>")

    cap_card("KNOWLEDGE WORK", BLUE, BLUE_L, [
        "#1 on Hebbia’s Finance Benchmark for senior-level reasoning",
        "IMC: aced trading-analysis evals — factual lookup, conceptual reasoning, root-cause & expected-value analysis",
    ], 145, "$")

    cap_card("VISION", ORANGE, ORANGE_L, [
        "New state-of-the-art vision model; rebuilt a web app’s source code from screenshots alone",
        "Beat Pokémon FireRed using ONLY raw screenshots — no maps, no helper tools",
    ], 145, "[o]")

    cap_card("MEMORY & LONG CONTEXT", BLUE, BLUE_L, [
        "Persistent memory boosted performance 3× more than for Opus 4.8",
        "Reached Slay the Spire’s final act 3× more often; stays focused across millions of tokens",
    ], 145, "~")

    # PRICING — gold highlight
    ph = 190
    card(d, [M, y, W-M, y+ph], GOLD_L, accent=GOLD)
    d.text((M+30, y+18), "PRICING", font=F_BOLD(23), fill=ORANGE_D)
    # two big price boxes
    bx = M + 30
    bw = (cw - 60 - 30) / 2
    bt, bb = y+56, y+168          # box top / bottom (height 112)
    rrect(d, [bx, bt, bx+bw, bb], 12, fill=WHITE)
    center(d, bx+bw/2, bt+12, "INPUT", F_SEMI(16), GRAY_M)
    center(d, bx+bw/2, bt+34, "$10", F_BLACK(44), ORANGE_D)
    center(d, bx+bw/2, bb-26, "per 1M tokens", F_REG(14), GRAY_M)
    bx2 = bx + bw + 30
    rrect(d, [bx2, bt, bx2+bw, bb], 12, fill=WHITE)
    center(d, bx2+bw/2, bt+12, "OUTPUT", F_SEMI(16), GRAY_M)
    center(d, bx2+bw/2, bt+34, "$50", F_BLACK(44), BLUE_D)
    center(d, bx2+bw/2, bb-26, "per 1M tokens", F_REG(14), GRAY_M)
    y += ph + 14

    center(d, W/2, y, "Less than half the price of Mythos Preview   ·   API: claude-fable-5",
           F_SEMI(17), DARK)

    footer_band(d, "DATA FROM ANTHROPIC ANNOUNCEMENT  ·  JUNE 9, 2026")
    img.save(os.path.join(OUT, "info1-fable5.png"))
    print("Saved info1-fable5.png")

# ════════════════════════════════════════════════════════
# INFOGRAPHIC 2 — COMPARISON
# ════════════════════════════════════════════════════════
def make_info2():
    img, d = new_canvas()
    header_band(d)

    center(d, W/2, 34, "FABLE 5  vs  MYTHOS 5", F_BLACK(46), DARK)
    center(d, W/2, 92, "Same Model. Different Safeguards.", F_SEMI(24), GRAY_M)

    M = 40
    # core-truth gold banner
    by0 = 134
    card(d, [M, by0, W-M, by0+52], GOLD_L, accent=GOLD)
    cl = wrap(d, "Both share the EXACT SAME underlying AI model — only the safeguards differ.",
              F_SEMI(19), W-2*M-60)
    yy = by0 + (52 - len(cl)*24)/2
    for ln in cl:
        center(d, W/2+8, yy, ln, F_SEMI(19), ORANGE_D)
        yy += 24

    # two columns
    colY = by0 + 70
    colH = 560
    gap = 20
    colW = (W - 2*M - gap) / 2
    fx, mx = M, M + colW + gap

    # FABLE column
    card(d, [fx, colY, fx+colW, colY+colH], WHITE)
    rrect(d, [fx, colY, fx+colW, colY+56], 16, fill=ORANGE)
    d.rectangle([fx, colY+30, fx+colW, colY+56], fill=ORANGE)
    center(d, fx+colW/2, colY+12, "FABLE 5", F_BLACK(30), WHITE)
    center(d, fx+colW/2, colY+64, "GENERAL PUBLIC ACCESS", F_SEMI(14), ORANGE_D)
    bullets(d, fx+22, colY+96, [
        "Available to everyone",
        "Cyber safeguards ACTIVE — sensitive queries fall back to Opus 4.8",
        "Triggers in less than 5% of sessions",
        "Biology & chemistry classifiers active",
        "Distillation protection active",
        "API ID: claude-fable-5 (public)",
        "On Pro, Max, Team & Enterprise plans",
    ], F_REG(18), DARK, colW-40, lh=26, gap=10, dot=ORANGE)

    # MYTHOS column
    card(d, [mx, colY, mx+colW, colY+colH], WHITE)
    rrect(d, [mx, colY, mx+colW, colY+56], 16, fill=BLUE)
    d.rectangle([mx, colY+30, mx+colW, colY+56], fill=BLUE)
    center(d, mx+colW/2, colY+12, "MYTHOS 5", F_BLACK(30), WHITE)
    center(d, mx+colW/2, colY+64, "RESTRICTED TRUSTED ACCESS", F_SEMI(14), BLUE_D)
    bullets(d, mx+22, colY+96, [
        "Glasswing partners & trusted researchers only",
        "Cyber safeguards LIFTED — strongest cyber AI in the world",
        "Bio & chemistry safeguards can be lifted for researchers",
        "Project Glasswing — US government cyber defense",
        "API not publicly available",
        "Upgrade from Mythos Preview",
    ], F_REG(18), DARK, colW-40, lh=26, gap=10, dot=BLUE)

    # SHARED green strip
    sy = colY + colH + 18
    sh = 158
    card(d, [M, sy, W-M, sy+sh], GREEN_L, accent=GREEN)
    d.text((M+30, sy+18), "SHARED BY BOTH MODELS", font=F_BOLD(22), fill=GREEN)
    bullets(d, M+34, sy+56, [
        "Identical price: $10 input / $50 output per 1M tokens — less than half of Mythos Preview",
        "Same underlying model, same performance  ·  30-day data retention  ·  Launched June 9, 2026",
        "Both show low misaligned behavior — similar to Opus 4.8",
    ], F_REG(18), DARK, W-2*M-70, lh=26, gap=6, dot=GREEN)

    footer_band(d, "DATA FROM ANTHROPIC ANNOUNCEMENT  ·  JUNE 9, 2026")
    img.save(os.path.join(OUT, "info2-comparison.png"))
    print("Saved info2-comparison.png")

# ════════════════════════════════════════════════════════
# INFOGRAPHIC 3 — PRICING
# ════════════════════════════════════════════════════════
def make_info3():
    img, d = new_canvas()
    header_band(d)

    center(d, W/2, 34, "FABLE 5 PRICING GUIDE", F_BLACK(46), ORANGE)
    center(d, W/2, 92, "What the most powerful public AI model costs", F_SEMI(20), GRAY_M)

    M = 50
    cw = W - 2*M
    y = 146

    # HEADLINE RATES
    rh = 240
    card(d, [M, y, W-M, y+rh], WHITE, accent=ORANGE)
    center(d, W/2+6, y+18, "HEADLINE RATES", F_BOLD(22), ORANGE_D)
    bx = M + 40
    bw = (cw - 80 - 30) / 2
    bt, bb = y+56, y+180          # box top / bottom (height 124)
    rrect(d, [bx, bt, bx+bw, bb], 14, fill=ORANGE_L)
    center(d, bx+bw/2, bt+14, "INPUT TOKENS", F_SEMI(17), GRAY_M)
    center(d, bx+bw/2, bt+40, "$10", F_BLACK(56), ORANGE_D)
    center(d, bx+bw/2, bb-28, "per 1 million tokens", F_REG(15), GRAY_M)
    bx2 = bx + bw + 30
    rrect(d, [bx2, bt, bx2+bw, bb], 14, fill=BLUE_L)
    center(d, bx2+bw/2, bt+14, "OUTPUT TOKENS", F_SEMI(17), GRAY_M)
    center(d, bx2+bw/2, bt+40, "$50", F_BLACK(56), BLUE_D)
    center(d, bx2+bw/2, bb-28, "per 1 million tokens", F_REG(15), GRAY_M)
    center(d, W/2, bb+12, "Less than HALF the price of Claude Mythos Preview", F_SEMI(17), DARK)
    y += rh + 18

    # EXAMPLE COSTS table
    th = 250
    card(d, [M, y, W-M, y+th], WHITE, accent=BLUE)
    d.text((M+30, y+18), "WHAT IT COSTS IN PRACTICE", font=F_BOLD(22), fill=BLUE_D)
    rows = [
        ("One short Q&A  (~500 tokens total)", "$0.003"),
        ("100 conversations / day  (~1K tokens each)", "~$5 / day"),
        ("Process 1 million input tokens", "$10.00"),
        ("Generate 1 million output tokens", "$50.00"),
        ("Heavy dev use  (10M output / month)", "$500 / mo"),
    ]
    ry = y + 60
    for i, (lab, val) in enumerate(rows):
        if i % 2 == 0:
            rrect(d, [M+20, ry-4, W-M-20, ry+32], 8, fill=CREAM)
        d.text((M+36, ry), lab, font=F_REG(19), fill=DARK)
        vw = text_w(d, val, F_BOLD(20))
        d.text((W-M-36-vw, ry), val, font=F_BOLD(20), fill=ORANGE_D)
        ry += 38
    y += th + 18

    # SUBSCRIPTION + API row (two cards)
    sh = 210
    gap = 20
    half = (cw - gap) / 2
    # subscription
    card(d, [M, y, M+half, y+sh], GREEN_L, accent=GREEN)
    d.text((M+26, y+18), "ON SUBSCRIPTION PLANS", font=F_BOLD(19), fill=GREEN)
    bullets(d, M+28, y+54, [
        "FREE on Pro, Max, Team & Enterprise until June 22, 2026",
        "After June 22: requires usage credits",
        "Claude API: pay-as-you-go, available now",
    ], F_REG(17), DARK, half-50, lh=24, gap=8, dot=GREEN)
    # api access
    ax = M + half + gap
    card(d, [ax, y, ax+half, y+sh], WHITE, accent=ORANGE)
    d.text((ax+26, y+18), "API ACCESS", font=F_BOLD(19), fill=ORANGE_D)
    bullets(d, ax+28, y+54, [
        "Model ID: claude-fable-5",
        "Available via Claude API immediately",
        "30-day data retention; never used for training",
    ], F_REG(17), DARK, half-50, lh=24, gap=8, dot=ORANGE)

    footer_band(d, "DATA FROM ANTHROPIC ANNOUNCEMENT  ·  JUNE 9, 2026")
    img.save(os.path.join(OUT, "info3-pricing.png"))
    print("Saved info3-pricing.png")


if __name__ == "__main__":
    make_info1()
    make_info2()
    make_info3()
    print("All infographics generated with accurate pricing.")
