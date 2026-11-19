#!/usr/bin/env python3
"""Draw entry.png: a newspaper front page summing up Wednesday,
18 November 2026, for make.fun competition news-image-20261118.

Stories and their sources live in SOURCES.md; to refresh the page, edit
STORIES below and re-run:  python3 draw.py
Output: entry.png, 1024x1024, well under the 1 MiB gate limit.
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (246, 241, 231)
PANEL_BG = (255, 253, 247)
INK = (26, 25, 23)
GREY = (96, 90, 80)
RED = (163, 22, 33)

FONT_DIR = "/usr/share/fonts/truetype/noto"
SERIF_BLACK = f"{FONT_DIR}/NotoSerifDisplay-Black.ttf"
SERIF_BOLD = f"{FONT_DIR}/NotoSerif-Bold.ttf"
SANS_BOLD = f"{FONT_DIR}/NotoSans-Bold.ttf"
SANS = f"{FONT_DIR}/NotoSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = word if not cur else f"{cur} {word}"
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def centered(draw, cx, y, text, fnt, fill):
    draw.text((cx - draw.textlength(text, font=fnt) / 2, y), text, font=fnt, fill=fill)


# ---------------------------------------------------------------- icons
# Each icon draws inside the box (x, y, s, s) in its accent colour.

def icon_bridge(d, x, y, s, c):
    deck = y + s * 0.34
    for px in (x + s * 0.16, x + s * 0.84):
        d.line([px, deck, px, y + s * 0.78], fill=c, width=6)
    d.line([x + s * 0.04, deck, x + s * 0.40, deck], fill=c, width=6)
    d.line([x + s * 0.60, deck, x + s * 0.96, deck], fill=c, width=6)
    d.line([x + s * 0.40, deck, x + s * 0.52, y + s * 0.66], fill=c, width=5)
    d.line([x + s * 0.60, deck, x + s * 0.55, y + s * 0.52], fill=c, width=4)
    for i in range(3):
        wy = y + s * 0.84 + i * 5
        d.arc([x + s * 0.10 + i * 7, wy, x + s * 0.34 + i * 7, wy + 7], 180, 360, fill=c, width=3)
        d.arc([x + s * 0.58 + i * 7, wy, x + s * 0.82 + i * 7, wy + 7], 180, 360, fill=c, width=3)


def icon_quad(d, x, y, s, c):
    r = s * 0.21
    for cx, cy in ((0.30, 0.30), (0.70, 0.30), (0.30, 0.70), (0.70, 0.70)):
        d.ellipse([x + s * cx - r, y + s * cy - r, x + s * cx + r, y + s * cy + r], outline=c, width=5)
    d.ellipse([x + s * 0.5 - 5, y + s * 0.5 - 5, x + s * 0.5 + 5, y + s * 0.5 + 5], fill=c)


def icon_drone(d, x, y, s, c):
    cx, cy = x + s * 0.5, y + s * 0.46
    for dx, dy in ((-0.28, -0.20), (0.28, -0.20), (-0.28, 0.20), (0.28, 0.20)):
        d.line([cx, cy, cx + s * dx, cy + s * dy], fill=c, width=4)
        px, py = cx + s * dx, cy + s * dy
        d.ellipse([px - 9, py - 5, px + 9, py + 5], outline=c, width=3)
    d.rectangle([cx - 13, cy - 9, cx + 13, cy + 9], outline=c, width=4)
    for r in (0.18, 0.30):
        d.arc([x + s * 0.62, y + s * 0.62, x + s * (0.62 + r), y + s * (0.62 + r)], 270, 360, fill=c, width=3)


def icon_chart(d, x, y, s, c):
    base = y + s * 0.85
    d.line([x + s * 0.08, base, x + s * 0.95, base], fill=c, width=4)
    for i, h in enumerate((0.25, 0.45, 0.62, 0.82)):
        bx = x + s * (0.14 + i * 0.21)
        d.rectangle([bx, base - s * h, bx + s * 0.13, base], fill=c)
    d.line([x + s * 0.10, y + s * 0.55, x + s * 0.88, y + s * 0.12], fill=RED, width=5)
    d.polygon([(x + s * 0.88, y + s * 0.12), (x + s * 0.74, y + s * 0.14), (x + s * 0.86, y + s * 0.26)], fill=RED)


def icon_virus(d, x, y, s, c):
    cx, cy, r = x + s * 0.5, y + s * 0.48, s * 0.24
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=c, width=5)
    import math
    for k in range(8):
        a = math.radians(k * 45)
        x1, y1 = cx + r * math.cos(a), cy + r * math.sin(a)
        x2, y2 = cx + (r + 11) * math.cos(a), cy + (r + 11) * math.sin(a)
        d.line([x1, y1, x2, y2], fill=c, width=4)
        d.ellipse([x2 - 4, y2 - 4, x2 + 4, y2 + 4], fill=c)
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=c)


def icon_cyclone(d, x, y, s, c):
    import math
    pts = []
    for t in range(0, 340, 4):
        rad = math.radians(t)
        rr = 3 + t / 340 * s * 0.40
        pts.append((x + s * 0.5 + rr * math.cos(rad), y + s * 0.5 + rr * math.sin(rad)))
    d.line(pts, fill=c, width=5)
    pts2 = [(px, py) for (px, py) in [(x + s - (px - x), y + s - (py - y)) for (px, py) in pts[::2]]]
    d.line(pts2, fill=c, width=3)


def icon_cricket(d, x, y, s, c):
    d.polygon([(x + s * 0.30, y + s * 0.90), (x + s * 0.50, y + s * 0.92),
               (x + s * 0.72, y + s * 0.28), (x + s * 0.58, y + s * 0.20)], fill=c)
    d.line([x + s * 0.60, y + s * 0.28, x + s * 0.70, y + s * 0.12], fill=c, width=6)
    d.ellipse([x + s * 0.62, y + s * 0.60, x + s * 0.90, y + s * 0.88], outline=RED, width=5)
    d.arc([x + s * 0.67, y + s * 0.65, x + s * 0.85, y + s * 0.83], 90, 270, fill=RED, width=3)
    d.text((x + s * 0.06, y + s * 0.06), "7", font=font(SANS_BOLD, 30), fill=c)


def icon_summit(d, x, y, s, c):
    pts = [(x + s * 0.50, y + s * 0.24), (x + s * 0.24, y + s * 0.72),
           (x + s * 0.76, y + s * 0.72)]
    for (ax, ay), (bx, by) in ((pts[0], pts[1]), (pts[0], pts[2]), (pts[1], pts[2])):
        d.line([ax, ay, bx, by], fill=c, width=4)
    for (cx, cy) in pts:
        r = s * 0.13
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=c, width=5)


def icon_capitol(d, x, y, s, c):
    cx = x + s * 0.5
    d.line([cx, y + s * 0.08, cx, y + s * 0.26], fill=c, width=4)
    d.ellipse([cx - 6, y + s * 0.05, cx + 6, y + s * 0.17], fill=c)
    d.arc([x + s * 0.28, y + s * 0.26, x + s * 0.72, y + s * 0.62], 180, 360, fill=c, width=5)
    d.line([x + s * 0.28, y + s * 0.62, x + s * 0.72, y + s * 0.62], fill=c, width=5)
    d.line([x + s * 0.18, y + s * 0.72, x + s * 0.82, y + s * 0.72], fill=c, width=5)
    d.line([x + s * 0.14, y + s * 0.82, x + s * 0.86, y + s * 0.82], fill=c, width=5)


ICONS = {
    "bridge": icon_bridge, "quad": icon_quad, "drone": icon_drone,
    "chart": icon_chart, "virus": icon_virus, "cyclone": icon_cyclone,
    "cricket": icon_cricket, "summit": icon_summit, "capitol": icon_capitol,
}

# ---------------------------------------------------------------- stories
# (tag, accent, icon, headline, body) — facts per SOURCES.md.
# v2 (final, 19 Nov evening): refreshed to the full day of 18 Nov 2026.
# The Quad summit (17 Nov) and the measles announcement (17 Nov) make way
# for the two biggest genuine 18 Nov developments: the Shenzhen summit and
# the Alaska Senate call. The bridge, Gulf, Nvidia, Akvan and Dhoni stories
# are updated with what happened during 18 Nov.

LEAD = ("UKRAINE WAR — EUROPE", RED, "bridge",
        "Ukraine collapses Crimean Bridge span",
        "Missiles and drones destroyed the road arch of the 19-km Kerch Bridge "
        "and halted traffic, Kyiv says. The Kremlin vows to rebuild it; "
        "analysts say the road span will not be fixed during the war.")

ROW2 = [
    ("SUMMIT — SHENZHEN", (31, 58, 95), "summit",
     "Xi and Putin meet before Trump trilateral",
     "Fifth Xi-Putin talks this year in Shenzhen; Trump lands for Thursday's "
     "first three-way summit."),
    ("GULF — KUWAIT & BAHRAIN", (146, 64, 14), "drone",
     "Iran widens Gulf attacks to Kuwait",
     "Drones target US kit at Ali Al Salem; Bahrain hit again. ADNOC ship "
     "struck in Hormuz: 1 missing, 11 hurt."),
]

ROW3 = [
    ("MARKETS — AI CHIPS", (21, 101, 80), "chart",
     "Nvidia beats, then falls 2.9%",
     "Record Q3 revenue $115.8B, up 103%; Q4 guided to $130B. Shares still "
     "fell 2.9% to $150.96."),
    ("POLITICS — US SENATE", (122, 31, 62), "capitol",
     "Peltola flips Alaska; Democrats 56-44",
     "AP calls the last Senate race: Peltola beats Sullivan. Nine flips — "
     "the biggest midterm gain since 1958."),
]

ROW4 = [
    ("CLIMATE — BAY OF BENGAL", (14, 92, 134), "cyclone",
     "Cyclone Akvan shifts track north",
     "Due ashore 20 Nov between Narsapur and Puri: 90-100 km/h, gusting "
     "110. Evacuations under way."),
]

SPORT = ("SPORT — CRICKET", (146, 104, 10), "cricket",
         "Dhoni calls time on his IPL career",
         "Dhoni, 45, retires as a player: 272 CSK matches, five titles. "
         "He stays on as mentor for 2027.")


def panel(d, x, y, w, h, story):
    tag, accent, icon, headline, body = story
    d.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=PANEL_BG, outline=INK, width=2)
    d.rectangle([x, y, x + 8, y + h], fill=accent)
    # icon column
    ix = x + 18
    ICONS[icon](d, ix, y + h / 2 - 34, 68, accent)
    tx = x + 100
    tw = x + w - tx - 14
    cy = y + 13
    d.text((tx, cy), tag, font=font(SANS_BOLD, 17), fill=accent)
    cy += 25
    for line in wrap(d, headline, font(SERIF_BOLD, 27), tw):
        d.text((tx, cy), line, font=font(SERIF_BOLD, 27), fill=INK)
        cy += 33
    cy += 3
    for line in wrap(d, body, font(SANS, 19), tw):
        d.text((tx, cy), line, font=font(SANS, 19), fill=(45, 42, 38))
        cy += 24
    return cy


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead
    d.line([34, 26, W - 34, 26], fill=INK, width=3)
    centered(d, W / 2, 36, "THE  DAILY  WORLD", font(SERIF_BLACK, 66), INK)
    d.line([34, 118, W - 34, 118], fill=INK, width=2)
    centered(d, W / 2, 126, "Wednesday, 18 November 2026", font(SERIF_BOLD, 43), RED)
    centered(d, W / 2, 182, "THE DAY'S BIGGEST STORIES — WAR • DIPLOMACY • GULF • MARKETS • POLITICS • CLIMATE • SPORT",
             font(SANS_BOLD, 16), GREY)
    d.line([34, 208, W - 34, 208], fill=INK, width=3)

    # ---- panels
    px, pw = 34, W - 68
    half = (pw - 12) // 2
    y = 222
    panel(d, px, y, pw, 168, LEAD)
    y += 180
    panel(d, px, y, half, 184, ROW2[0])
    panel(d, px + half + 12, y, half, 184, ROW2[1])
    y += 196
    panel(d, px, y, half, 184, ROW3[0])
    panel(d, px + half + 12, y, half, 184, ROW3[1])
    y += 196
    panel(d, px, y, half, 184, ROW4[0])
    panel(d, px + half + 12, y, half, 184, SPORT)

    # ---- footer
    d.line([34, 988, W - 34, 988], fill=INK, width=2)
    centered(d, W / 2, 994,
             "From reports by Reuters, Al Jazeera, Dawn, Gulf News, The National, AP, the IMD and The Hindu",
             font(SANS, 15), GREY)

    img.save("entry.png", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
