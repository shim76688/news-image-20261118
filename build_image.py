"""Build-time renderer for the 18 November 2026 news poster.

Draws a 1024x1024 front-page style poster with PIL and writes entry.png
next to this file. Deterministic: no randomness, no timestamps, fixed
layout constants, so two runs produce byte-identical output.
PIL is used here only; main.py never imports it.
"""

import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W = 1024
H = 1024
PAPER = (247, 243, 234)
BLACK = (18, 18, 18)
WHITE = (255, 255, 255)
RED = (192, 57, 43)
GREY = (90, 90, 90)
LIGHT_LINE = (205, 198, 182)
NAVY = (46, 74, 98)
GOLD = (176, 141, 32)
GREEN = (70, 110, 74)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
REG = os.path.join(FONT_DIR, "DejaVuSans.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap using measured text widths."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=fnt) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def fit_font(draw, text, path, start_size, max_width, max_lines, min_size=20):
    """Shrink a font until the wrapped text fits the line budget."""
    size = start_size
    while size > min_size:
        fnt = font(path, size)
        if len(wrap(draw, text, fnt, max_width)) <= max_lines:
            return fnt, size
        size -= 2
    fnt = font(path, min_size)
    return fnt, min_size


def centered(draw, cx, y, text, fnt, fill):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)
    return w


# ---------------------------------------------------------------- icons
# Each icon draws inside the box (x, y, w, h) at the top of a panel.

def icon_skyline(draw, x, y, w, h):
    base = y + h - 6
    draw.arc([x + w - 120, y - 6, x + w + 30, y + 74], 180, 330, fill=RED, width=4)
    buildings = [(0, 34, 26), (32, 52, 30), (68, 40, 24), (98, 60, 30), (134, 44, 26)]
    for bx, bh, bw in buildings:
        draw.rectangle([x + bx, base - bh, x + bx + bw, base], fill=BLACK)
        for wy in range(base - bh + 7, base - 8, 11):
            draw.rectangle([x + bx + 6, wy, x + bx + 11, wy + 5], fill=PAPER)
            draw.rectangle([x + bx + 15, wy, x + bx + 20, wy + 5], fill=PAPER)
    draw.line([x, base, x + w - 90, base], fill=BLACK, width=3)


def icon_pennants(draw, x, y, w, h):
    colors = [RED, NAVY, GOLD, GREEN]
    top = y + 4
    for i, color in enumerate(colors):
        px = x + 18 + i * 52
        draw.line([px, top, px, top + h - 12], fill=BLACK, width=4)
        draw.polygon(
            [(px, top), (px + 36, top + 11), (px, top + 22)], fill=color
        )
    draw.line([x + 6, y + h - 6, x + 220, y + h - 6], fill=BLACK, width=3)


def icon_bridge(draw, x, y, w, h):
    deck = y + h - 22
    for tx in (x + 26, x + 150):
        draw.rectangle([tx, y + 8, tx + 12, deck], fill=BLACK)
    draw.line([x + 6, y + 10, x + 226, y + 10], fill=BLACK, width=3)
    draw.line([x + 6, deck - 16, x + 96, deck - 16], fill=BLACK, width=5)
    draw.line([x + 140, deck - 26, x + 226, deck - 16], fill=BLACK, width=5)
    draw.polygon(
        [(x + 100, deck - 16), (x + 136, deck - 27), (x + 132, deck - 8)],
        fill=RED,
    )
    for wx in range(x + 8, x + 220, 36):
        draw.arc([wx, deck + 2, wx + 22, deck + 13], 0, 180, fill=NAVY, width=3)


def icon_drone(draw, x, y, w, h):
    cx, cy = x + 62, y + 28
    for dx, dy in ((-30, -14), (30, -14), (-30, 14), (30, 14)):
        draw.line([cx, cy, cx + dx, cy + dy], fill=BLACK, width=4)
        draw.ellipse([cx + dx - 11, cy + dy - 5, cx + dx + 11, cy + dy + 5],
                     outline=BLACK, width=3)
    draw.rectangle([cx - 15, cy - 9, cx + 15, cy + 9], fill=RED)
    draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=WHITE)
    rx, ry = x + 168, y + h - 14
    for r in (16, 32, 48):
        draw.arc([rx - r, ry - r, rx + r, ry + r], 200, 320, fill=NAVY, width=4)
    draw.ellipse([rx - 4, ry - 4, rx + 4, ry + 4], fill=RED)


def icon_chip(draw, x, y, w, h):
    sx, sy = x + 78, y + 2
    size = 58
    for i in range(4):
        off = 10 + i * 13
        draw.line([sx - 14, sy + off, sx, sy + off], fill=BLACK, width=4)
        draw.line([sx + size, sy + off, sx + size + 14, sy + off], fill=BLACK, width=4)
        draw.line([sx + off, sy - 14, sx + off, sy], fill=BLACK, width=4)
        draw.line([sx + off, sy + size, sx + off, sy + size + 14], fill=BLACK, width=4)
    draw.rectangle([sx, sy, sx + size, sy + size], outline=BLACK, width=5)
    draw.rectangle([sx + 15, sy + 15, sx + size - 15, sy + size - 15],
                   outline=RED, width=4)


def icon_cyclone(draw, x, y, w, h):
    cx, cy = x + 116, y + h // 2
    for r, start in ((52, 20), (40, 140), (28, 260), (16, 60)):
        draw.arc([cx - r, cy - r, cx + r, cy + r], start, start + 250,
                 fill=NAVY, width=6)
    draw.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=RED)


ICONS = [icon_skyline, icon_pennants, icon_bridge, icon_drone, icon_chip,
         icon_cyclone]

STORIES = [
    ("APEC SUMMIT OPENS IN SHENZHEN",
     "Asia-Pacific leaders meet in China"),
    ("TRUMP IN MANILA FOR QUAD TALKS",
     "US-China-Russia summit follows tomorrow"),
    ("UKRAINE HITS CRIMEAN BRIDGE",
     "Drone exchanges as Abu Dhabi peace talks go on"),
    ("IRAN DRONES TARGET BAHRAIN RADAR",
     "Kuwait intercepts drones; Gaza truce at risk"),
    ("NVIDIA REVENUE DOUBLES TO $115.8BN",
     "Board rules out return of ousted CEO Huang"),
    ("CYCLONE AKVAN NEARS INDIA COAST",
     "Andhra landfall due Nov 20; Dhoni retires from IPL"),
]

TICKER = ("NORTH KOREA FIRES BALLISTIC MISSILE INTO SEA OF JAPAN  \u2022  "
          "PRAGUE MARCHES FOR A FREE PRESS  \u2022  "
          "GTA VI LAUNCHES TOMORROW, NOV 19")


def draw_panel(draw, x, y, w, h, icon, headline, sub):
    draw.rectangle([x, y, x + w, y + h], fill=WHITE, outline=BLACK, width=2)
    draw.rectangle([x, y, x + w, y + 7], fill=RED)
    icon(draw, x + (w - 232) // 2, y + 16, 232, 62)
    inner = w - 32
    hf, _ = fit_font(draw, headline, BOLD, 38, inner, 2)
    hy = y + 90
    for line in wrap(draw, headline, hf, inner):
        draw.text((x + 16, hy), line, font=hf, fill=BLACK)
        hy += 42
    sf, _ = fit_font(draw, sub, REG, 23, inner, 2)
    sy = y + h - 58
    for line in wrap(draw, sub, sf, inner):
        draw.text((x + 16, sy), line, font=sf, fill=GREY)
        sy += 27


def build():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # Masthead: black band, small line, then the date as the biggest text.
    draw.rectangle([0, 0, W, 176], fill=BLACK)
    centered(draw, W // 2, 16, "THE WORLD IN ONE DAY", font(BOLD, 27), RED)
    date_font, _ = fit_font(draw, "18 NOVEMBER 2026", BOLD, 88, W - 32, 1)
    centered(draw, W // 2, 52, "18 NOVEMBER 2026", date_font, WHITE)
    draw.line([40, 196, 380, 196], fill=BLACK, width=3)
    draw.line([644, 196, 984, 196], fill=BLACK, width=3)
    centered(draw, W // 2, 178, "WEDNESDAY", font(BOLD, 32), RED)

    # Six story panels in a 2 x 3 grid.
    gx, gy = 24, 226
    gap = 14
    col_w = (W - 2 * gx - gap) // 2
    row_h = 230
    for i, (headline, sub) in enumerate(STORIES):
        col, row = i % 2, i // 2
        px = gx + col * (col_w + gap)
        py = gy + row * (row_h + gap)
        draw_panel(draw, px, py, col_w, row_h, ICONS[i], headline, sub)

    # Footer ticker band.
    fy = H - 78
    draw.rectangle([0, fy, W, H], fill=BLACK)
    tf, _ = fit_font(draw, TICKER, BOLD, 24, W - 48, 2)
    lines = wrap(draw, TICKER, tf, W - 48)
    ty = fy + (78 - len(lines) * 30) // 2
    for line in lines:
        centered(draw, W // 2, ty, line, tf, WHITE)
        ty += 30

    img.save(OUT, format="PNG", optimize=True)
    print("wrote", OUT)


if __name__ == "__main__":
    build()
