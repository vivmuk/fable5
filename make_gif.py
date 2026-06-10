"""Assemble captured frames into a LinkedIn-ready walkthrough GIF."""
import json, os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(__file__)
FR = os.path.join(HERE, "frames")
OUT = os.path.join(HERE, "fable-walkthrough.gif")

TARGET_W = 720                      # final GIF width (square input -> square output)
BAR_H = 84                          # caption bar height (on scaled frame)
ORANGE = (217, 119, 87)
DARK = (20, 20, 19)

FONTDIR = r"C:\Windows\Fonts"
def font(name, size):
    p = os.path.join(FONTDIR, name)
    return ImageFont.truetype(p, size) if os.path.exists(p) else ImageFont.truetype(os.path.join(FONTDIR, "segoeui.ttf"), size)
F_CAP = font("segoeuib.ttf", 26)
F_NUM = font("seguibl.ttf", 30)

# caption + hold-time (ms) per frame name
PLAN = {
    "01_intro":      ("Meet FABLE — an interactive tale of Claude Fable 5", 3000),
    "02_trial1":     ("Trial I — discover Fable 5's powers", 2400),
    "03_console":    ("Play LIVE with the real Fable 5 model", 2700),
    "04_generating": ("Ask it anything — answered live", 1600),
    "05_answer":     ("Watch Fable 5 respond", 3000),
    "06_treasure1":  ("Break the seal → unlock Treasure I", 2800),
    "07_trial2":     ("Trial II — Fable vs Mythos", 2400),
    "08_mythos":     ("Lift the veil: same model, different guardrails", 2900),
    "09_finale":     ("Complete the tale…", 1900),
    "10_treasures":  ("Three treasures, unsealed", 2800),
    "11_treasures2": ("Go find the treasures yourself!", 3600),
}

def caption(img, idx, text, last=False):
    """Draw a caption bar at the bottom of a scaled frame."""
    d = ImageDraw.Draw(img, "RGBA")
    w, h = img.size
    y0 = h - BAR_H
    # translucent dark bar + orange top accent
    d.rectangle([0, y0, w, h], fill=(20, 20, 19, 215))
    d.rectangle([0, y0, w, y0 + 4], fill=ORANGE)
    # number chip
    cx = 30
    d.ellipse([cx, y0 + BAR_H/2 - 19, cx + 38, y0 + BAR_H/2 + 19], fill=ORANGE)
    n = str(idx)
    nb = d.textbbox((0, 0), n, font=F_NUM)
    d.text((cx + 19 - (nb[2]-nb[0])/2, y0 + BAR_H/2 - (nb[3]-nb[1])/2 - nb[1]), n, font=F_NUM, fill=(255, 255, 255))
    # caption text (wrap to 2 lines if needed)
    tx = cx + 58
    maxw = w - tx - 24
    words, lines, cur = text.split(), [], ""
    for word in words:
        t = (cur + " " + word).strip()
        if d.textlength(t, font=F_CAP) <= maxw:
            cur = t
        else:
            lines.append(cur); cur = word
    if cur: lines.append(cur)
    lines = lines[:2]
    lh = 30
    ty = y0 + BAR_H/2 - (len(lines)*lh)/2
    for ln in lines:
        col = (251, 215, 130) if last else (255, 255, 255)
        d.text((tx, ty), ln, font=F_CAP, fill=col)
        ty += lh
    return img

order = json.load(open(os.path.join(FR, "order.json")))
frames, durations = [], []
for i, name in enumerate(order, 1):
    im = Image.open(os.path.join(FR, name + ".png")).convert("RGB")
    w, h = im.size
    nh = round(h * TARGET_W / w)
    im = im.resize((TARGET_W, nh), Image.LANCZOS)
    cap, dur = PLAN.get(name, ("", 2500))
    caption(im, i, cap, last=(name == order[-1]))
    frames.append(im)
    durations.append(dur)

# uniform canvas height (max) so the GIF doesn't jitter
maxh = max(f.height for f in frames)
norm = []
for f in frames:
    if f.height != maxh:
        c = Image.new("RGB", (TARGET_W, maxh), (250, 249, 245))
        c.paste(f, (0, 0))
        f = c
    norm.append(f.convert("P", palette=Image.ADAPTIVE, colors=200))

norm[0].save(OUT, save_all=True, append_images=norm[1:], duration=durations,
             loop=0, optimize=True, disposal=2)
print("Saved", OUT, "(", round(os.path.getsize(OUT)/1024), "KB,", len(norm), "frames )")
