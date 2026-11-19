#!/usr/bin/env python3
"""Draw the 19 November 2026 world-news front page as a 1024x1024 PNG.

Hand-written renderer for the make.fun news-image-20261119 entry. It draws
a newspaper front page: a navy masthead, one lead story (a tanker ablaze in
the Strait of Hormuz) with a large painted hero scene, five story cards with
small flat icons, and an "In Brief" panel. Twelve stories in total, every
fact checked against public sources on 19 Nov 2026; nothing invented.

    python3 render.py        # writes entry.png next to this file

The submitted entrypoint (main.py) only copies entry.png into /output; this
script never runs at grade time. Rendering is fully deterministic: no
randomness, no clock, no network, so two runs produce byte-identical files.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W = H = 1024

# Palette: warm newsprint paper, navy masthead, gold date line, red for
# breaking news, and a small set of flat accent colours for the icons.
PAL = {
    "paper": (247, 243, 234),
    "ink": (26, 26, 26),
    "muted": (90, 84, 72),
    "navy": (20, 33, 61),
    "gold": (232, 196, 104),
    "red": (178, 34, 34),
    "card": (255, 255, 255),
    "border": (214, 205, 184),
    "panel": (240, 236, 224),
    "sea": (46, 111, 164),
    "deep_sea": (18, 58, 102),
    "flame": (255, 122, 26),
    "flame_core": (255, 196, 0),
    "green": (0, 110, 70),
    "white": (255, 255, 255),
    "charcoal": (24, 24, 24),
    "grey": (120, 120, 120),
    "dark_grey": (60, 60, 60),
    "black": (18, 18, 18),
}

FONT_PATHS = {
    "bold": [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    ],
    "regular": [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ],
}


def get_font(weight, size):
    """First usable font file for the weight, else Pillow's default."""
    for path in FONT_PATHS[weight]:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def wrap_text(draw, text, fnt, max_width):
    """Greedy word wrap; returns a list of lines that fit max_width."""
    lines = []
    current = ""
    for word in text.split():
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def text_block(draw, x, y, lines, fnt, fill, leading):
    """Draw lines top to bottom; return the y just below the last line."""
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def card_frame(draw, x, y, w, h, accent):
    """White rounded card with a coloured bar down its left edge."""
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10,
                           fill=PAL["card"], outline=PAL["border"], width=2)
    draw.rectangle([x, y + 10, x + 6, y + h - 10], fill=accent)

# ---------------------------------------------------------------------------
# Icons — all flat shapes drawn with Pillow primitives, no image assets.
# ---------------------------------------------------------------------------

def hero_tanker(d, x, y, w, h):
    """Burning tanker at dusk in the Strait of Hormuz.

    Improvement over the first draft: a brighter, crisper horizon glow band
    (a hot orange strip right above the sea line), a fourth flame tongue so
    the fire reads wider, one extra smoke puff drifting further right, and
    four firelight streaks on the water instead of three.
    """
    # Dusk sky: dark top, warm middle, hot glow hugging the horizon.
    d.rectangle([x, y, x + w, y + h * 0.38], fill=(28, 26, 48))
    d.rectangle([x, y + h * 0.38, x + w, y + h * 0.52], fill=(110, 58, 48))
    d.rectangle([x, y + h * 0.50, x + w, y + h * 0.60], fill=(238, 134, 58))
    # Sea with a lighter strip at the top.
    d.rectangle([x, y + h * 0.60, x + w, y + h], fill=PAL["deep_sea"])
    d.rectangle([x, y + h * 0.60, x + w, y + h * 0.64], fill=PAL["sea"])
    # White wave arcs.
    for wx, wy, ww in [(0.05, 0.72, 0.20), (0.42, 0.78, 0.24),
                       (0.72, 0.72, 0.22)]:
        d.arc([x + w * wx, y + h * wy, x + w * (wx + ww),
               y + h * (wy + 0.10)], 180, 360, fill=PAL["white"], width=3)
    # Listing tanker hull, bow slightly down.
    hx, hy = x + w * 0.08, y + h * 0.70
    hull = [(hx, hy), (hx + w * 0.62, hy - h * 0.04),
            (hx + w * 0.56, hy + h * 0.16), (hx + w * 0.06, hy + h * 0.18)]
    d.polygon(hull, fill=PAL["charcoal"])
    # Grey superstructure block at the stern.
    d.rectangle([hx + w * 0.46, hy - h * 0.16, hx + w * 0.60, hy - h * 0.04],
                fill=(70, 70, 70))
    # Four flame tongues on the deck, each with a yellow core.
    for fx, fh, fw in [(0.18, 0.28, 0.09), (0.32, 0.38, 0.12),
                       (0.48, 0.30, 0.10), (0.62, 0.22, 0.08)]:
        cx = hx + w * fx
        base = hy - h * 0.02
        d.polygon([(cx - w * fw / 2, base), (cx, base - h * fh),
                   (cx + w * fw / 2, base)], fill=PAL["flame"])
        d.polygon([(cx - w * fw / 4, base), (cx, base - h * fh * 0.55),
                   (cx + w * fw / 4, base)], fill=PAL["flame_core"])
    # Black smoke column rising and drifting right, five puffs.
    for sx, sy, sr in [(0.42, 0.30, 0.055), (0.50, 0.20, 0.07),
                       (0.60, 0.12, 0.085), (0.72, 0.06, 0.10),
                       (0.84, 0.03, 0.11)]:
        d.ellipse([x + w * (sx - sr), y + h * (sy - sr),
                   x + w * (sx + sr), y + h * (sy + sr)], fill=PAL["black"])
    # Firelight reflected on the water beneath the tanker.
    for rx, rw in [(0.14, 0.16), (0.34, 0.22), (0.58, 0.14), (0.76, 0.10)]:
        d.rectangle([x + w * rx, y + h * 0.90,
                     x + w * (rx + rw), y + h * 0.925],
                    fill=(238, 134, 58))
    # A distant second ship on the horizon, with a thin mast.
    d.polygon([(x + w * 0.74, y + h * 0.64), (x + w * 0.92, y + h * 0.64),
               (x + w * 0.88, y + h * 0.70), (x + w * 0.78, y + h * 0.70)],
              fill=(40, 40, 40))
    d.line([x + w * 0.83, y + h * 0.64, x + w * 0.83, y + h * 0.57],
           fill=(40, 40, 40), width=3)


def icon_flags(d, x, y, s):
    """Three roundel flags (US / CN / RU) over a gold rule — the summit."""
    colours = [PAL["red"], PAL["navy"], PAL["green"]]
    labels = ["US", "CN", "RU"]
    fnt = get_font("bold", int(s * 0.16))
    for i in range(3):
        cx = x + s * (0.20 + i * 0.30)
        cy = y + s * 0.42
        r = s * 0.17
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=colours[i])
        tw = d.textlength(labels[i], font=fnt)
        d.text((cx - tw / 2, cy - s * 0.09), labels[i], font=fnt,
               fill=PAL["white"])
    d.line([x + s * 0.10, y + s * 0.78, x + s * 0.90, y + s * 0.78],
           fill=PAL["gold"], width=4)


def icon_gamepad(d, x, y, s):
    """Flat gamepad: navy body, white D-pad, four coloured buttons."""
    d.rounded_rectangle([x + s * 0.06, y + s * 0.30, x + s * 0.94,
                         y + s * 0.82], radius=int(s * 0.14), fill=PAL["navy"])
    d.ellipse([x + s * 0.02, y + s * 0.55, x + s * 0.26, y + s * 0.95],
              fill=PAL["navy"])
    d.ellipse([x + s * 0.74, y + s * 0.55, x + s * 0.98, y + s * 0.95],
              fill=PAL["navy"])
    # D-pad on the left.
    cx, cy = x + s * 0.26, y + s * 0.55
    d.rectangle([cx - s * 0.10, cy - s * 0.035, cx + s * 0.10, cy + s * 0.035],
                fill=PAL["white"])
    d.rectangle([cx - s * 0.035, cy - s * 0.10, cx + s * 0.035, cy + s * 0.10],
                fill=PAL["white"])
    # Four buttons in a diamond on the right.
    bx, by = x + s * 0.74, y + s * 0.55
    for dx, dy, col in [(0, -0.09, PAL["flame_core"]), (0.09, 0, PAL["green"]),
                        (0, 0.09, PAL["red"]), (-0.09, 0, PAL["sea"])]:
        r = s * 0.045
        d.ellipse([bx + s * dx - r, by + s * dy - r,
                   bx + s * dx + r, by + s * dy + r], fill=col)
    # Two thumbsticks.
    for jx in (0.42, 0.58):
        r = s * 0.05
        d.ellipse([x + s * jx - r, y + s * 0.72 - r,
                   x + s * jx + r, y + s * 0.72 + r], fill=PAL["white"])


def icon_stocks(d, x, y, s):
    """Rising stock chart: three bars, a steep red arrow, a dollar sign."""
    base = y + s * 0.82
    for bx, bh, col in [(0.14, 0.30, PAL["navy"]), (0.38, 0.48, PAL["sea"]),
                        (0.62, 0.66, PAL["green"])]:
        d.rectangle([x + s * bx, base - s * bh, x + s * (bx + 0.16), base],
                    fill=col)
    d.line([x + s * 0.10, y + s * 0.62, x + s * 0.88, y + s * 0.12],
           fill=PAL["red"], width=6)
    d.polygon([(x + s * 0.88, y + s * 0.12), (x + s * 0.70, y + s * 0.10),
               (x + s * 0.86, y + s * 0.28)], fill=PAL["red"])
    d.text((x + s * 0.02, y + s * 0.02), "$",
           font=get_font("bold", int(s * 0.16)), fill=PAL["ink"])


def icon_processor(d, x, y, s):
    """Processor chip: pins on four sides, navy die, gold core, 'AI'."""
    for i in range(3):
        off = 0.22 + i * 0.28
        d.rectangle([x + s * off, y + s * 0.02,
                     x + s * (off + 0.08), y + s * 0.16], fill=PAL["grey"])
        d.rectangle([x + s * off, y + s * 0.84,
                     x + s * (off + 0.08), y + s * 0.98], fill=PAL["grey"])
        d.rectangle([x + s * 0.02, y + s * off,
                     x + s * 0.16, y + s * (off + 0.08)], fill=PAL["grey"])
        d.rectangle([x + s * 0.84, y + s * off,
                     x + s * 0.98, y + s * (off + 0.08)], fill=PAL["grey"])
    d.rounded_rectangle([x + s * 0.16, y + s * 0.16, x + s * 0.84,
                         y + s * 0.84], radius=int(s * 0.06), fill=PAL["navy"])
    d.rounded_rectangle([x + s * 0.34, y + s * 0.34, x + s * 0.66,
                         y + s * 0.66], radius=int(s * 0.04), fill=PAL["gold"])
    d.text((x + s * 0.44, y + s * 0.42), "AI",
           font=get_font("bold", int(s * 0.14)), fill=PAL["navy"])


def icon_justice(d, x, y, s):
    """Scales of justice: centre post, beam, two hanging pans."""
    d.rectangle([x + s * 0.46, y + s * 0.12, x + s * 0.54, y + s * 0.85],
                fill=PAL["dark_grey"])
    d.line([x + s * 0.12, y + s * 0.25, x + s * 0.88, y + s * 0.25],
           fill=PAL["dark_grey"], width=5)
    for px in (0.125, 0.875):
        d.line([x + s * px, y + s * 0.25, x + s * px, y + s * 0.38],
               fill=PAL["dark_grey"], width=3)
    d.polygon([(x + s * 0.05, y + s * 0.60), (x + s * 0.20, y + s * 0.60),
               (x + s * 0.125, y + s * 0.38)], fill=PAL["gold"])
    d.polygon([(x + s * 0.80, y + s * 0.60), (x + s * 0.95, y + s * 0.60),
               (x + s * 0.875, y + s * 0.38)], fill=PAL["gold"])

# ---------------------------------------------------------------------------
# Layout — masthead, lead story, 2x3 grid, footer.
# ---------------------------------------------------------------------------

def story_card(draw, x, y, w, h, kicker, accent, headline, body, icon=None):
    """One story card: kicker, two-line headline, two-line body, icon right."""
    card_frame(draw, x, y, w, h, accent)
    pad = 20
    tx = x + pad
    ty = y + pad
    icon_w = 92 if icon else 0
    text_w = w - pad * 2 - icon_w
    kf = get_font("bold", 17)
    draw.text((tx, ty), kicker, font=kf, fill=accent)
    ty += 28
    hf = get_font("bold", 30)
    lines = wrap_text(draw, headline, hf, text_w)
    assert len(lines) <= 2, f"headline too long: {headline!r} -> {lines}"
    ty = text_block(draw, tx, ty, lines[:2], hf, PAL["ink"], 35)
    ty += 6
    bf = get_font("regular", 19)
    blines = wrap_text(draw, body, bf, text_w)
    assert len(blines) <= 2, f"body too long: {body!r} -> {blines}"
    end = text_block(draw, tx, ty, blines[:2], bf, PAL["muted"], 24)
    assert end <= y + h - 12, f"card overflows: {headline!r}"
    if icon:
        icon(draw, x + w - pad - 88, y + pad + 8, 88)


# The five grid cards: (kicker, accent, headline, body, icon).
GRID_STORIES = [
    ("DIPLOMACY  ·  SHENZHEN", PAL["navy"],
     "TRUMP, XI AND PUTIN MEET",
     "First-ever trilateral summit on the APEC margins; Iran on top.",
     icon_flags),
    ("GAMING  ·  LAUNCH DAY", PAL["red"],
     "GTA VI LAUNCHES WORLDWIDE",
     "Rolls out at midnight, country by country; 99 on Metacritic.",
     icon_gamepad),
    ("BUSINESS  ·  IPO", PAL["navy"],
     "ANTHROPIC DEBUTS ON NASDAQ",
     "Claude maker lists as ANT at $70–$78; a $1.4 trillion value.",
     icon_stocks),
    ("TECH  ·  NVIDIA", PAL["green"],
     "HUANG QUITS AS NVIDIA CHIEF",
     "Acting CEO promises earlier pay rises; H-chips to China halted.",
     icon_processor),
    ("LAW  ·  THE HAGUE", PAL["green"],
     "COURT RULES ON MYANMAR CASE",
     "Judges deliver the verdict in The Gambia v. Myanmar, Rohingya.",
     icon_justice),
]

BRIEFS = [
    "EU proposes €45 billion loan for Ukraine.",
    "Voyager 1 reaches one light-day from Earth.",
    "Australia sanctions Israeli West Bank settlers.",
    "Israeli troops push into central Gaza.",
    "Iraq jails six French ISIL recruits for life.",
    "Saudi Arabia: danger passed in three cities.",
]

LEAD_BODY = ("UAE tanker Navig8 Messi is struck off Oman; Iran fires on US "
             "sites in Kuwait overnight and Bahrain intercepts a third "
             "attack in a week. No end in sight.")


def build():
    img = Image.new("RGB", (W, H), PAL["paper"])
    d = ImageDraw.Draw(img)

    # Masthead: navy band, white title, gold date, gold rule.
    d.rectangle([0, 0, W, 104], fill=PAL["navy"])
    tf = get_font("bold", 48)
    title = "THE WORLD IN ONE DAY"
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, 8), title, font=tf, fill=PAL["white"])
    df = get_font("bold", 28)
    date = "THURSDAY, 19 NOVEMBER 2026"
    dw = d.textlength(date, font=df)
    d.text(((W - dw) / 2, 62), date, font=df, fill=PAL["gold"])
    d.rectangle([0, 104, W, 108], fill=PAL["gold"])

    # Lead story: tanker ablaze in the Strait of Hormuz.
    lx, ly, lw, lh = 16, 120, 992, 256
    card_frame(d, lx, ly, lw, lh, PAL["red"])
    tx, ty = lx + 30, ly + 18
    d.text((tx, ty), "IRAN  ·  WAR IN THE GULF",
           font=get_font("bold", 18), fill=PAL["red"])
    ty += 32
    hf = get_font("bold", 44)
    lines = wrap_text(d, "TANKER ABLAZE IN THE STRAIT OF HORMUZ", hf, 590)
    assert len(lines) <= 2, f"lead headline wraps to {len(lines)} lines"
    ty = text_block(d, tx, ty, lines, hf, PAL["ink"], 50)
    ty += 10
    bf = get_font("regular", 21)
    blines = wrap_text(d, LEAD_BODY, bf, 590)
    assert len(blines) <= 3, f"lead body wraps to {len(blines)} lines"
    end = text_block(d, tx, ty, blines, bf, PAL["muted"], 26)
    assert end <= ly + lh - 14, "lead overflows"
    hero_tanker(d, lx + 648, ly + 16, 328, 220)

    # Grid: two columns, three rows; the last cell is the In Brief panel.
    gx0, gx1 = 16, 520
    gw = 488
    row_y = [384, 592, 800]
    row_h = 196
    story_card(d, gx0, row_y[0], gw, row_h, *GRID_STORIES[0])
    story_card(d, gx1, row_y[0], gw, row_h, *GRID_STORIES[1])
    story_card(d, gx0, row_y[1], gw, row_h, *GRID_STORIES[2])
    story_card(d, gx1, row_y[1], gw, row_h, *GRID_STORIES[3])
    story_card(d, gx0, row_y[2], gw, row_h, *GRID_STORIES[4])

    bx, by, bw, bh = gx1, row_y[2], gw, row_h
    d.rounded_rectangle([bx, by, bx + bw, by + bh], radius=10,
                        fill=PAL["panel"], outline=PAL["border"], width=2)
    d.text((bx + 20, by + 16), "IN BRIEF",
           font=get_font("bold", 17), fill=PAL["navy"])
    bf = get_font("regular", 17)
    yy = by + 46
    for item in BRIEFS:
        lines = wrap_text(d, item, bf, bw - 64)
        assert len(lines) == 1, f"brief wraps to 2 lines: {item!r}"
        d.ellipse([bx + 20, yy + 5, bx + 30, yy + 15], fill=PAL["red"])
        d.text((bx + 40, yy), lines[0], font=bf, fill=PAL["ink"])
        yy += 22
    assert yy <= by + bh - 10, f"in-brief overflows at {yy}"

    # Footer: source line centred in the strip below the grid.
    sf = get_font("regular", 13)
    foot = ("Compiled from wire reports published 19 Nov 2026  ·  Reuters"
            "  ·  AP  ·  AFP  ·  Guardian")
    fw = d.textlength(foot, font=sf)
    d.text(((W - fw) / 2, 1006), foot, font=sf, fill=PAL["muted"])
    return img


def main():
    img = build()
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
