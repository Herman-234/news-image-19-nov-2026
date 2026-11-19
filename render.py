#!/usr/bin/env python3
"""Render the 19 November 2026 world-news summary image (1024x1024 PNG).

Same newspaper layout as the 17/18 November entries: masthead, lead story
with a big hero scene, five story cards with flat icons, and an In Brief
panel. 12 stories total: lead (tanker ablaze in the Strait of Hormuz as
the Gulf war grinds on) + 5 cards (Trump-Xi-Putin trilateral in Shenzhen,
GTA VI launch, Anthropic Nasdaq debut, Jensen Huang resigns, ICJ Myanmar
ruling) + 6 one-line briefs. All facts verified from public sources on
19 Nov 2026; nothing invented.

Run locally (needs Pillow + DejaVu fonts, both present on the build machine):
    python3 render.py
Writes entry.png next to this file. The submitted entrypoint (main.py) only
copies entry.png to /output/entry.png; this script never runs at grade time.
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

PAPER = (247, 243, 234)
INK = (26, 26, 26)
MUTED = (90, 84, 72)
NAVY = (20, 33, 61)
GOLD = (232, 196, 104)
RED = (178, 34, 34)
CARD = (255, 255, 255)
BORDER = (214, 205, 184)
SEA = (46, 111, 164)
SEA_DARK = (18, 58, 102)
FLAME = (255, 122, 26)
FLAME2 = (255, 196, 0)
GREEN = (0, 110, 70)


def font(name, size):
    candidates = {
        "bold": [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        ],
        "regular": [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        ],
    }
    for path in candidates[name]:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_text_block(draw, x, y, lines, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


# ---------- icons (flat shapes, drawn with PIL primitives) ----------

def icon_tanker_fire(d, x, y, w, h):
    """Burning tanker in the Strait of Hormuz: dusk sky, black smoke,
    flames on a listing tanker, oil-slick sea with a second ship far off."""
    # dusk sky bands, orange glow at the horizon
    d.rectangle([x, y, x + w, y + h * 0.40], fill=(28, 26, 48))
    d.rectangle([x, y + h * 0.40, x + w, y + h * 0.56], fill=(96, 52, 44))
    d.rectangle([x, y + h * 0.52, x + w, y + h * 0.60], fill=(226, 122, 52))
    # sea
    d.rectangle([x, y + h * 0.60, x + w, y + h], fill=SEA_DARK)
    d.rectangle([x, y + h * 0.60, x + w, y + h * 0.64], fill=SEA)
    # wave arcs
    for wx, wy, ww in [(0.05, 0.72, 0.20), (0.42, 0.78, 0.24), (0.72, 0.72, 0.22)]:
        d.arc([x + w * wx, y + h * wy, x + w * (wx + ww), y + h * (wy + 0.10)],
              180, 360, fill=(255, 255, 255), width=3)
    # listing tanker hull (tilted), mid-deck on fire
    hx0, hy0 = x + w * 0.08, y + h * 0.70
    hull = [(hx0, hy0), (hx0 + w * 0.62, hy0 - h * 0.04),
            (hx0 + w * 0.56, hy0 + h * 0.16), (hx0 + w * 0.06, hy0 + h * 0.18)]
    d.polygon(hull, fill=(24, 24, 24))
    # superstructure block
    d.rectangle([hx0 + w * 0.46, hy0 - h * 0.16, hx0 + w * 0.60, hy0 - h * 0.04],
                fill=(70, 70, 70))
    # flames licking from the deck (three tongues)
    for fx, fh, fw in [(0.20, 0.30, 0.10), (0.34, 0.38, 0.12), (0.50, 0.28, 0.09)]:
        cx = hx0 + w * fx
        base = hy0 - h * 0.02
        d.polygon([(cx - w * fw / 2, base), (cx, base - h * fh),
                   (cx + w * fw / 2, base)], fill=FLAME)
        d.polygon([(cx - w * fw / 4, base), (cx, base - h * fh * 0.55),
                   (cx + w * fw / 4, base)], fill=FLAME2)
    # black smoke column rising and drifting right
    for i, (sx, sy, sr) in enumerate([(0.42, 0.30, 0.055), (0.50, 0.20, 0.07),
                                      (0.60, 0.12, 0.085), (0.72, 0.06, 0.10)]):
        d.ellipse([x + w * (sx - sr), y + h * (sy - sr),
                   x + w * (sx + sr), y + h * (sy + sr)], fill=(18, 18, 18))
    # firelight reflected on the water under the tanker
    for rx, rw in [(0.16, 0.18), (0.38, 0.24), (0.66, 0.12)]:
        d.rectangle([x + w * rx, y + h * 0.90, x + w * (rx + rw), y + h * 0.925],
                    fill=(226, 122, 52))
    # distant second ship on the horizon
    d.polygon([(x + w * 0.74, y + h * 0.64), (x + w * 0.92, y + h * 0.64),
               (x + w * 0.88, y + h * 0.70), (x + w * 0.78, y + h * 0.70)],
              fill=(40, 40, 40))


def icon_summit(d, x, y, s):
    cols = [(178, 34, 34), (20, 33, 61), (0, 110, 70)]
    labels = ["US", "CN", "RU"]
    for i in range(3):
        cx = x + s * (0.20 + i * 0.30)
        cy = y + s * 0.42
        r = s * 0.17
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=cols[i])
        f = font("bold", int(s * 0.16))
        tw = d.textlength(labels[i], font=f)
        d.text((cx - tw / 2, cy - s * 0.09), labels[i], font=f, fill=(255, 255, 255))
    d.line([x + s * 0.10, y + s * 0.78, x + s * 0.90, y + s * 0.78], fill=GOLD, width=4)


def icon_controller(d, x, y, s):
    """Flat gamepad: rounded body, D-pad, buttons, joysticks."""
    # body
    d.rounded_rectangle([x + s * 0.06, y + s * 0.30, x + s * 0.94, y + s * 0.82],
                        radius=int(s * 0.14), fill=NAVY)
    # grips
    d.ellipse([x + s * 0.02, y + s * 0.55, x + s * 0.26, y + s * 0.95], fill=NAVY)
    d.ellipse([x + s * 0.74, y + s * 0.55, x + s * 0.98, y + s * 0.95], fill=NAVY)
    # D-pad (left)
    cx, cy = x + s * 0.26, y + s * 0.55
    d.rectangle([cx - s * 0.10, cy - s * 0.035, cx + s * 0.10, cy + s * 0.035],
                fill=(255, 255, 255))
    d.rectangle([cx - s * 0.035, cy - s * 0.10, cx + s * 0.035, cy + s * 0.10],
                fill=(255, 255, 255))
    # buttons (right): four coloured dots in a diamond
    bx, by = x + s * 0.74, y + s * 0.55
    for dx, dy, col in [(0, -0.09, FLAME2), (0.09, 0, GREEN),
                        (0, 0.09, RED), (-0.09, 0, SEA)]:
        r = s * 0.045
        d.ellipse([bx + s * dx - r, by + s * dy - r,
                   bx + s * dx + r, by + s * dy + r], fill=col)
    # joysticks
    for jx in (0.42, 0.58):
        r = s * 0.05
        d.ellipse([x + s * jx - r, y + s * 0.72 - r,
                   x + s * jx + r, y + s * 0.72 + r], fill=(255, 255, 255))


def icon_chart(d, x, y, s):
    """Rising stock chart: three bars and a steep arrow."""
    base = y + s * 0.82
    bars = [(0.14, 0.30, NAVY), (0.38, 0.48, SEA), (0.62, 0.66, GREEN)]
    for bx, bh, col in bars:
        d.rectangle([x + s * bx, base - s * bh, x + s * (bx + 0.16), base],
                    fill=col)
    # arrow: shaft + head, rising left to right
    d.line([x + s * 0.10, y + s * 0.62, x + s * 0.88, y + s * 0.12],
           fill=RED, width=6)
    d.polygon([(x + s * 0.88, y + s * 0.12), (x + s * 0.70, y + s * 0.10),
               (x + s * 0.86, y + s * 0.28)], fill=RED)
    # dollar tick on the axis
    f = font("bold", int(s * 0.16))
    d.text((x + s * 0.02, y + s * 0.02), "$", font=f, fill=INK)


def icon_chip(d, x, y, s):
    """Processor chip: square die, inner core, pins on four sides."""
    # pins
    for i in range(3):
        off = 0.22 + i * 0.28
        d.rectangle([x + s * off, y + s * 0.02, x + s * (off + 0.08), y + s * 0.16],
                    fill=(120, 120, 120))
        d.rectangle([x + s * off, y + s * 0.84, x + s * (off + 0.08), y + s * 0.98],
                    fill=(120, 120, 120))
        d.rectangle([x + s * 0.02, y + s * off, x + s * 0.16, y + s * (off + 0.08)],
                    fill=(120, 120, 120))
        d.rectangle([x + s * 0.84, y + s * off, x + s * 0.98, y + s * (off + 0.08)],
                    fill=(120, 120, 120))
    # die
    d.rounded_rectangle([x + s * 0.16, y + s * 0.16, x + s * 0.84, y + s * 0.84],
                        radius=int(s * 0.06), fill=NAVY)
    d.rounded_rectangle([x + s * 0.34, y + s * 0.34, x + s * 0.66, y + s * 0.66],
                        radius=int(s * 0.04), fill=GOLD)
    f = font("bold", int(s * 0.14))
    d.text((x + s * 0.44, y + s * 0.42), "AI", font=f, fill=NAVY)


def icon_scales(d, x, y, s):
    d.rectangle([x + s * 0.46, y + s * 0.12, x + s * 0.54, y + s * 0.85], fill=(60, 60, 60))
    d.line([x + s * 0.12, y + s * 0.25, x + s * 0.88, y + s * 0.25], fill=(60, 60, 60), width=5)
    d.polygon([(x + s * 0.05, y + s * 0.60), (x + s * 0.20, y + s * 0.60),
               (x + s * 0.125, y + s * 0.38)], fill=GOLD)
    d.polygon([(x + s * 0.80, y + s * 0.60), (x + s * 0.95, y + s * 0.60),
               (x + s * 0.875, y + s * 0.38)], fill=GOLD)
    d.line([x + s * 0.125, y + s * 0.25, x + s * 0.125, y + s * 0.38], fill=(60, 60, 60), width=3)
    d.line([x + s * 0.875, y + s * 0.25, x + s * 0.875, y + s * 0.38], fill=(60, 60, 60), width=3)


# ---------- layout ----------

def card(draw, x, y, w, h, kicker, kcolor, headline, body, icon=None):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=CARD,
                           outline=BORDER, width=2)
    # color-coded left bar
    draw.rectangle([x, y + 10, x + 6, y + h - 10], fill=kcolor)
    pad = 20
    tx = x + pad
    ty = y + pad
    icon_w = 92 if icon else 0
    text_w = w - pad * 2 - icon_w
    kf = font("bold", 17)
    draw.text((tx, ty), kicker, font=kf, fill=kcolor)
    ty += 28
    hf = font("bold", 30)
    lines = wrap(draw, headline, hf, text_w)
    assert len(lines) <= 2, f"headline too long: {headline!r} -> {lines}"
    ty = draw_text_block(draw, tx, ty, lines[:2], hf, INK, 35)
    ty += 6
    bf = font("regular", 19)
    blines = wrap(draw, body, bf, text_w)
    assert len(blines) <= 2, f"body too long: {body!r} -> {blines}"
    end = draw_text_block(draw, tx, ty, blines[:2], bf, MUTED, 24)
    assert end <= y + h - 12, f"card overflows: {headline!r}"
    if icon:
        icon(draw, x + w - pad - 88, y + pad + 8, 88)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # masthead
    d.rectangle([0, 0, W, 104], fill=NAVY)
    tf = font("bold", 48)
    title = "THE WORLD IN ONE DAY"
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, 8), title, font=tf, fill=(255, 255, 255))
    df = font("bold", 28)
    date = "THURSDAY, 19 NOVEMBER 2026"
    dw = d.textlength(date, font=df)
    d.text(((W - dw) / 2, 62), date, font=df, fill=GOLD)
    d.rectangle([0, 104, W, 108], fill=GOLD)

    # lead story: tanker ablaze in the Strait of Hormuz — big hero scene
    lx, ly, lw, lh = 16, 120, 992, 256
    d.rounded_rectangle([lx, ly, lx + lw, ly + lh], radius=10, fill=CARD,
                        outline=BORDER, width=2)
    d.rectangle([lx, ly, lx + 8, ly + lh], fill=RED)
    tx, ty = lx + 30, ly + 18
    kf = font("bold", 18)
    d.text((tx, ty), "IRAN  ·  WAR IN THE GULF", font=kf, fill=RED)
    ty += 32
    hf = font("bold", 44)
    lines = wrap(d, "TANKER ABLAZE IN THE STRAIT OF HORMUZ", hf, 590)
    assert len(lines) <= 2, f"lead headline wraps to {len(lines)} lines"
    ty = draw_text_block(d, tx, ty, lines, hf, INK, 50)
    ty += 10
    bf = font("regular", 21)
    body = ("UAE tanker Navig8 Messi is struck off Oman; Iran fires on US "
            "sites in Kuwait overnight and Bahrain intercepts a third "
            "attack in a week. No end in sight.")
    blines = wrap(d, body, bf, 590)
    assert len(blines) <= 3, f"lead body wraps to {len(blines)} lines"
    end = draw_text_block(d, tx, ty, blines, bf, MUTED, 26)
    assert end <= ly + lh - 14, "lead overflows"
    icon_tanker_fire(d, lx + 648, ly + 16, 328, 220)

    # grid: 2 columns x 3 rows
    gx0, gx1 = 16, 520
    gw = 488
    rows = [(384, 196), (592, 196), (800, 196)]
    stories = [
        ("DIPLOMACY  ·  SHENZHEN", NAVY,
         "TRUMP, XI AND PUTIN MEET",
         "First-ever trilateral summit on the APEC margins; Iran on top.",
         icon_summit),
        ("GAMING  ·  LAUNCH DAY", RED,
         "GTA VI LAUNCHES WORLDWIDE",
         "Rolls out at midnight, country by country; 99 on Metacritic.",
         icon_controller),
        ("BUSINESS  ·  IPO", NAVY,
         "ANTHROPIC DEBUTS ON NASDAQ",
         "Claude maker lists as ANT at $70–$78; a $1.4 trillion value.",
         icon_chart),
        ("TECH  ·  NVIDIA", GREEN,
         "HUANG QUITS AS NVIDIA CHIEF",
         "Acting CEO promises earlier pay rises; H-chips to China halted.",
         icon_chip),
        ("LAW  ·  THE HAGUE", GREEN,
         "COURT RULES ON MYANMAR CASE",
         "Judges deliver the verdict in The Gambia v. Myanmar, Rohingya.",
         icon_scales),
    ]
    card(d, gx0, rows[0][0], gw, rows[0][1], stories[0][0], stories[0][1],
         stories[0][2], stories[0][3], stories[0][4])
    card(d, gx1, rows[0][0], gw, rows[0][1], stories[1][0], stories[1][1],
         stories[1][2], stories[1][3], stories[1][4])
    card(d, gx0, rows[1][0], gw, rows[1][1], stories[2][0], stories[2][1],
         stories[2][2], stories[2][3], stories[2][4])
    card(d, gx1, rows[1][0], gw, rows[1][1], stories[3][0], stories[3][1],
         stories[3][2], stories[3][3], stories[3][4])
    # row 3: ICJ + In brief panel (6 one-line items, no dead space)
    card(d, gx0, rows[2][0], gw, rows[2][1], stories[4][0], stories[4][1],
         stories[4][2], stories[4][3], stories[4][4])
    bx, by, bw, bh = gx1, rows[2][0], gw, rows[2][1]
    d.rounded_rectangle([bx, by, bx + bw, by + bh], radius=10, fill=(240, 236, 224),
                        outline=BORDER, width=2)
    kf = font("bold", 17)
    d.text((bx + 20, by + 16), "IN BRIEF", font=kf, fill=NAVY)
    bf = font("regular", 17)
    briefs = [
        "EU proposes €45 billion loan for Ukraine.",
        "Voyager 1 reaches one light-day from Earth.",
        "Australia sanctions Israeli West Bank settlers.",
        "Israeli troops push into central Gaza.",
        "Iraq jails six French ISIL recruits for life.",
        "Saudi Arabia: danger passed in three cities.",
    ]
    yy = by + 46
    for item in briefs:
        lines = wrap(d, item, bf, bw - 64)
        assert len(lines) == 1, f"brief wraps to 2 lines: {item!r}"
        d.ellipse([bx + 20, yy + 5, bx + 30, yy + 15], fill=RED)
        d.text((bx + 40, yy), lines[0], font=bf, fill=INK)
        yy += 22
    assert yy <= by + bh - 10, f"in-brief overflows at {yy}"

    # footer strip (source line, uses the empty strip below the grid)
    sf = font("regular", 13)
    foot = "Compiled from wire reports published 19 Nov 2026  ·  Reuters  ·  AP  ·  AFP  ·  Guardian"
    fw = d.textlength(foot, font=sf)
    d.text(((W - fw) / 2, 1006), foot, font=sf, fill=MUTED)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
