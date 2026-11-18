#!/usr/bin/env python3
"""The World in One Day -- Tuesday 17 November 2026.

Deterministic generative entry for the make.fun bounty
"Sum up 17 November's world news in one image" (news-image-20261117).

A dense newspaper front page, drawn entirely with Pillow from
procedural vector shapes (no external assets, no network, no
randomness): 37 real stories from Tuesday 17 November 2026 --
a masthead, a hero story, 12 illustrated panels, a numbered
world map and a 24-item "also on" list.

Every story is one first reported on 17 November 2026, checked
against that day's reporting (BBC, AP, AFP, Reuters, Al Jazeera,
CNBC, ABC News, NPR, Spaceflight Now and others). Disputed claims
stay attributed ("Iran says ...", "Bahrain says ...", "bank says ...").
Nothing is invented beyond the reporting and no other day's news
is in the picture.

Layout (1024 x 1024):
  * navy masthead: THE DAY IN WORLD NEWS / Tuesday 17 November 2026
  * HERO, full width: Kerch Bridge span collapses after the
    Ukrainian strike -- text left, bridge illustration right
  * 12 illustrated panels in a 4 x 3 grid, one story each
  * WHERE IT HAPPENED: a world map with numbered pins for the
    13 lead stories, beside ALSO ON TUESDAY 17 NOVEMBER, 24 more
  * navy footer strip: date + source credit

Run:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
The program writes exactly one file, entry.png, 1024x1024, and
two runs write byte-identical files.
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

# ---------------------------------------------------------------- palette
PAPER = (247, 242, 231)      # warm newsprint cream
PANEL_BG = (252, 249, 242)   # panel background, a touch lighter
INK = (20, 20, 20)           # near-black text
NAVY = (16, 30, 51)          # masthead / footer band
CREAM = (247, 242, 231)      # masthead text
GOLD = (201, 162, 39)        # masthead rule / eyebrow accent
RED = (176, 30, 36)          # kickers, pins, alerts
BLUE = (31, 78, 121)         # secondary accents
GREY = (110, 106, 96)        # source tags, small print
RULE = (180, 172, 152)       # hairlines
LAND = (214, 202, 172)       # map land
LANDLINE = (168, 154, 118)   # map coast outline
SKY = (198, 217, 229)        # illustration sky
SEA = (158, 190, 212)        # illustration water

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def f_serif(size):
    return font("DejaVuSerif-Bold.ttf", size)


def f_serif_r(size):
    return font("DejaVuSerif.ttf", size)


def f_sans(size):
    return font("DejaVuSans.ttf", size)


def f_sans_b(size):
    return font("DejaVuSans-Bold.ttf", size)


# ---------------------------------------------------------------- helpers
def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines fitting max_w pixels."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def hline(draw, x0, x1, y, fill=RULE, width=1):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def flag_stripes(draw, x, y, w, h, colors):
    """Horizontal-stripe flag (colors top to bottom)."""
    n = len(colors)
    for i, c in enumerate(colors):
        y0 = y + h * i // n
        y1 = y + h * (i + 1) // n
        draw.rectangle([x, y0, x + w, y1], fill=c)


def star(draw, cx, cy, r, fill, phase=-math.pi / 2):
    pts = []
    for i in range(10):
        ang = phase + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.42
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    draw.polygon(pts, fill=fill)


def burst(draw, cx, cy, r, fill):
    """Explosion starburst: alternating long/short spikes."""
    pts = []
    for i in range(24):
        ang = i * math.pi / 12
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    draw.polygon(pts, fill=fill)


def pin(draw, x, y, num, r=7):
    draw.ellipse([x - r, y - r, x + r, y + r], fill=RED,
                 outline=(255, 255, 255), width=2)
    fnt = f_sans_b(9)
    tw = draw.textlength(str(num), font=fnt)
    draw.text((x - tw / 2, y - 6.5), str(num), font=fnt, fill=(255, 255, 255))


# ---------------------------------------------------------------- stories
# (number, kicker, headline, deck, source, pin lon/lat, illustration)
PANELS = [
    (2, "STRAIT OF HORMUZ \u00b7 IRAN WAR",
     "Tankers ablaze after mine strikes in Strait",
     "Two tankers catch fire; a third is immobilised. A US carrier arrives.",
     "AL JAZEERA \u00b7 REUTERS", (56.5, 26.5), "tanker"),
    (3, "ASIA \u00b7 DIPLOMACY",
     "Trump lands in Manila; Xi and Putin next",
     "ASEAN summit opens; three-way talks set for Thursday in Shenzhen.",
     "AP \u00b7 AFP", (121.0, 14.6), "flags"),
    (4, "GULF \u00b7 IRAN WAR",
     "Iran's drones fired at US radar base",
     "Bahrain says it intercepted the drones aimed at Sheikh Isa base.",
     "REUTERS", (50.5, 26.2), "radar"),
    (5, "ASIA \u00b7 DEFENCE",
     "Japan scrambles jets at Russian incursion",
     "Two planes enter airspace; Tokyo protests, first such case since 2024.",
     "AP", (139.0, 36.0), "jets"),
    (6, "EUROPE \u00b7 MIGRATION",
     "Five EU states plan Rwanda return hub",
     "Germany, Denmark, Austria, Greece and the Netherlands sign up.",
     "AP", (30.0, -2.0), "rwanda"),
    (7, "US \u00b7 BANKING",
     "JPMorgan bug cuts off Zelle for hours",
     "Software bug, not a cyberattack, bank says; 5,000 outage reports.",
     "ABC \u00b7 CNBC", (-74.0, 40.7), "bank"),
    (8, "US \u00b7 TECH",
     "Nvidia reports after the bell",
     "First results since Jensen Huang quit; $109.1bn revenue expected.",
     "CNBC", (-121.0, 37.4), "chip"),
    (9, "US \u00b7 SPACE",
     "Vulcan fails; 40 Amazon satellites lost",
     "First outright failure for ULA; payload never reaches orbit.",
     "SPACEFLIGHT NOW", (-80.5, 28.4), "rocket"),
    (10, "EUROPE \u00b7 SECURITY",
     "Estonia to shut Russia border crossings",
     "From 1 Dec, after a foiled plot to bomb a drone plant.",
     "NPR", (24.7, 59.4), "border"),
    (11, "AMERICAS \u00b7 HEALTH",
     "US loses measles-free status",
     "First loss in nearly 30 years; Mexico and Bolivia lose it too.",
     "PAHO", (-98.0, 39.0), "virus"),
    (12, "MIDDLE EAST \u00b7 WAR",
     "Houthis advance as Yemen army pulls back",
     "Government forces withdraw from the Red Sea coast to defend Aden.",
     "AP", (45.0, -12.8), "yemen"),
    (13, "MIDDLE EAST \u00b7 AID",
     "West urges Israel: open Gaza crossings",
     "UK, Australia, Canada and Italy call the situation catastrophic.",
     "AP", (34.5, 31.5), "gaza"),
]

# (number, one-line story) -- also on Tuesday 17 November
ALSO = [
    (14, "House Democrats set their agenda"),
    (15, "Microsoft explains global outage"),
    (16, "Depardieu pleads guilty in Paris"),
    (17, "Expert doubts Epstein suicide ruling"),
    (18, "Britain sanctions settlement firms"),
    (19, "EU charges Temu over illegal goods"),
    (20, "Oil torn by Mideast tanker attacks"),
    (21, "Stocks fall; Nvidia in focus"),
    (22, "Le Pen pledges earlier retirement"),
    (23, "Bus crash in Uttarakhand kills 6"),
    (24, "Washington faces $4bn budget gap"),
    (25, "Seattle I-5 lanes shut for repairs"),
    (26, "Colorado: a third cost-burdened"),
    (27, "Young voters drove Colorado taxes"),
    (28, "Broncos 10-point favourites"),
    (29, "Singapore seeks trusted AI chips"),
    (30, "Crypto malware hits top websites"),
    (31, "Britain sets out EU summit plan"),
    (32, "Sterling ends five-day slide"),
    (33, "Mongolia president to resign"),
    (34, "COP31 in final days, split on fuel"),
    (35, "Drone alert at Iraqi gas field"),
    (36, "US curbs chip sales to SE Asia"),
    (37, "Thailand signs $2.6bn farm deal"),
]

HERO = (
    "EUROPE \u00b7 UKRAINE WAR",
    "Kerch Bridge span falls into the strait",
    "Ukraine calls it an \u2018unprecedented operation\u2019 weeks in the "
    "making; the Kremlin vows to rebuild. Rail traffic resumes on one track.",
    "BBC \u00b7 AP",
)


# ------------------------------------------------------- illustrations
def illo_hero(draw, x, y, w, h):
    """Kerch Strait: bridge, collapsed span, smoke, sea, small ship."""
    draw.rectangle([x, y, x + w, y + h], fill=SKY)
    # distant shore
    draw.rectangle([x, y + h * 0.52, x + w, y + h * 0.58], fill=(150, 168, 140))
    # sea
    draw.rectangle([x, y + h * 0.58, x + w, y + h], fill=SEA)
    for i, wy in enumerate((0.66, 0.74, 0.82, 0.90)):
        yy = y + h * wy
        draw.line([(x + 8, yy), (x + w - 8, yy)], fill=(120, 160, 190), width=2)
    # bridge deck
    dy = y + h * 0.52
    draw.rectangle([x, dy, x + w, dy + 7], fill=(70, 70, 72))
    # arch
    cx = x + w * 0.52
    for t in range(0, 41):
        ax = cx - 90 + t * 4.5
        ay = dy - 52 * math.sin(math.pi * t / 40)
        draw.ellipse([ax - 2, ay - 2, ax + 2, ay + 2], fill=(50, 50, 52))
    # towers
    for tx in (x + w * 0.16, x + w * 0.86):
        draw.rectangle([tx - 3, dy - 62, tx + 3, dy], fill=(50, 50, 52))
    # collapsed span: tilted deck piece falling into the water
    draw.polygon([(cx + 30, dy + 2), (cx + 118, dy + 34),
                  (cx + 112, dy + 42), (cx + 26, dy + 10)], fill=(70, 70, 72))
    # blast + smoke at the break
    burst(draw, cx + 18, dy - 8, 26, (255, 176, 32))
    burst(draw, cx + 18, dy - 8, 15, (255, 90, 32))
    for sx, sy, sr in ((cx - 6, dy - 48, 15), (cx + 22, dy - 62, 19),
                       (cx + 48, dy - 44, 12)):
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(120, 120, 118))
    # small red ship
    sx = x + w * 0.10
    sy = y + h * 0.78
    draw.polygon([(sx, sy), (sx + 52, sy), (sx + 44, sy + 12), (sx + 8, sy + 12)],
                 fill=(150, 40, 36))
    draw.rectangle([sx + 18, sy - 10, sx + 30, sy], fill=(150, 40, 36))


def illo_tanker(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=SKY)
    draw.rectangle([x, y + h * 0.62, x + w, y + h], fill=SEA)
    # tanker hull + tanks
    hy = y + h * 0.58
    draw.polygon([(x + 12, hy), (x + w - 12, hy), (x + w - 26, hy + 20),
                  (x + 26, hy + 20)], fill=(150, 40, 36))
    for i in range(3):
        tx = x + 34 + i * 52
        draw.ellipse([tx, hy - 16, tx + 40, hy], fill=(226, 220, 205),
                     outline=(120, 116, 100))
    draw.rectangle([x + w - 52, hy - 22, x + w - 30, hy], fill=(90, 90, 90))
    # fire + smoke from the mid tank
    burst(draw, x + w * 0.52, hy - 14, 14, (255, 176, 32))
    burst(draw, x + w * 0.52, hy - 14, 8, (255, 90, 32))
    draw.ellipse([x + w * 0.60, y + 4, x + w * 0.60 + 16, y + 20],
                 fill=(120, 120, 118))
    # mine in the water
    mx, my = x + w * 0.80, y + h * 0.82
    draw.ellipse([mx - 6, my - 6, mx + 6, my + 6], fill=(40, 40, 40))
    for ang in range(0, 360, 45):
        rad = math.radians(ang)
        draw.line([(mx, my), (mx + 10 * math.cos(rad), my + 10 * math.sin(rad))],
                  fill=(40, 40, 40), width=2)


def illo_flags(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(232, 226, 208))
    # three flags on poles: US, China, Russia
    specs = [
        ([(176, 30, 36), (247, 247, 247), (176, 30, 36)], (31, 78, 121)),
        ([(222, 41, 16)], (255, 222, 0)),
        ([(247, 247, 247), (31, 78, 121), (176, 30, 36)], None),
    ]
    fw, fh = 52, 30
    for i, (stripes, canton) in enumerate(specs):
        fx = x + 18 + i * 72
        fy = y + 10
        flag_stripes(draw, fx, fy, fw, fh, stripes)
        if canton:
            draw.rectangle([fx, fy, fx + 20, fy + 16], fill=canton)
            for sx in (fx + 5, fx + 12):
                for sy in (fy + 4, fy + 10):
                    draw.ellipse([sx, sy, sx + 2, sy + 2], fill=(255, 255, 255))
        if i == 1:
            star(draw, fx + 12, fy + 12, 7, (255, 222, 0))
        draw.line([(fx + fw / 2, fy + fh), (fx + fw / 2, y + h - 4)],
                  fill=(90, 84, 70), width=2)
    # table line
    draw.rectangle([x, y + h - 6, x + w, y + h], fill=(120, 90, 60))


def illo_radar(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(24, 34, 52))
    # radar dish
    cx, cy = x + w * 0.30, y + h * 0.55
    draw.pieslice([cx - 26, cy - 26, cx + 26, cy + 26], 180, 360,
                  fill=(226, 220, 205))
    draw.line([(cx, cy), (cx, cy + 22)], fill=(140, 140, 135), width=4)
    draw.rectangle([cx - 14, cy + 20, cx + 14, y + h], fill=(90, 90, 88))
    # sweeping beam
    draw.line([(cx, cy - 10), (cx + 74, cy - 30)], fill=(255, 222, 0), width=2)
    # drones
    for dx, dy in ((0.62, 0.30), (0.78, 0.48), (0.68, 0.62)):
        px, py = x + w * dx, y + h * dy
        draw.ellipse([px - 8, py - 3, px + 8, py + 3], fill=(200, 200, 195))
        draw.line([(px - 12, py), (px + 12, py)], fill=(200, 200, 195), width=2)
    # intercept burst
    burst(draw, x + w * 0.86, y + h * 0.28, 11, (255, 176, 32))


def illo_jets(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=SKY)
    # red sun
    draw.ellipse([x + w - 34, y + 6, x + w - 8, y + 32], fill=(176, 30, 36))
    # two jets + contrails
    for jx, jy, s in ((0.16, 0.34, 1.0), (0.52, 0.62, 0.85)):
        px, py = x + w * jx, y + h * jy
        draw.line([(x + 6, py + 6), (px - 16, py)], fill=(255, 255, 255), width=2)
        draw.polygon([(px, py - 5 * s), (px + 34 * s, py),
                      (px, py + 5 * s), (px + 8 * s, py)],
                     fill=(70, 74, 80))
        draw.polygon([(px + 8 * s, py - 10 * s), (px + 18 * s, py),
                      (px + 8 * s, py + 2 * s)], fill=(70, 74, 80))
    # clouds
    for cx, cy in ((0.30, 0.18), (0.70, 0.80)):
        px, py = x + w * cx, y + h * cy
        draw.ellipse([px - 16, py - 6, px + 16, py + 6], fill=(255, 255, 255))


def illo_rwanda(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(226, 232, 214))
    # five small flags in a row
    flags = [
        [(0, 0, 0), (176, 30, 36), (201, 162, 39)],
        [(176, 30, 36), (247, 247, 247)],
        [(176, 30, 36), (247, 247, 247), (176, 30, 36)],
        [(31, 78, 121), (247, 247, 247)],
        [(0, 120, 80), (247, 247, 247)],
    ]
    for i, cols in enumerate(flags):
        fx = x + 12 + i * 44
        flag_stripes(draw, fx, y + 8, 36, 20, cols)
        draw.line([(fx + 18, y + 28), (fx + 18, y + 38)], fill=(90, 84, 70), width=2)
    # arrow down to a Rwanda dot on a mini map
    draw.polygon([(x + w * 0.5, y + 40), (x + w * 0.5 - 5, y + 34),
                  (x + w * 0.5 + 5, y + 34)], fill=RED)
    draw.line([(x + w * 0.5, y + 34), (x + w * 0.5, y + 44)], fill=RED, width=2)
    draw.ellipse([x + w * 0.5 - 5, y + 44, x + w * 0.5 + 5, y + 54], fill=RED)


def illo_bank(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(232, 226, 208))
    # bank building
    bx, by = x + 16, y + 8
    draw.polygon([(bx, by + 12), (bx + 46, by), (bx + 92, by + 12)],
                 fill=(120, 116, 100))
    draw.rectangle([bx, by + 12, bx + 92, by + 16], fill=(90, 86, 76))
    for i in range(4):
        cx = bx + 10 + i * 24
        draw.rectangle([cx, by + 16, cx + 8, y + h - 8], fill=(150, 144, 126))
    draw.rectangle([bx, y + h - 8, bx + 92, y + h - 4], fill=(90, 86, 76))
    # red bug with legs, over the door
    cx, cy = x + w - 34, y + h * 0.55
    draw.ellipse([cx - 9, cy - 7, cx + 9, cy + 7], fill=RED)
    for k in range(3):
        ly = cy - 5 + k * 5
        draw.line([(cx - 9, ly), (cx - 18, ly - 4)], fill=RED, width=2)
        draw.line([(cx + 9, ly), (cx + 18, ly - 4)], fill=RED, width=2)


def illo_chip(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(232, 240, 226))
    # chip
    cx, cy = x + 46, y + h / 2
    draw.rectangle([cx - 22, cy - 22, cx + 22, cy + 22], fill=(24, 44, 34),
                   outline=(201, 162, 39), width=2)
    draw.rectangle([cx - 10, cy - 10, cx + 10, cy + 10], fill=(201, 162, 39))
    for i in range(4):
        px = cx - 15 + i * 10
        draw.line([(px, cy - 28), (px, cy - 22)], fill=(120, 120, 115), width=2)
        draw.line([(px, cy + 22), (px, cy + 28)], fill=(120, 120, 115), width=2)
    # rising chart arrow
    pts = [(x + 84, y + h - 12), (x + 116, y + h - 26), (x + 138, y + h - 18),
           (x + 168, y + h - 36), (x + 210, y + 12)]
    draw.line(pts, fill=(0, 120, 80), width=3)
    draw.polygon([(x + 210, y + 12), (x + 196, y + 12), (x + 210, y + 26)],
                 fill=(0, 120, 80))
    draw.text((x + 168, y + 2), "$109bn", font=f_sans_b(13), fill=(0, 120, 80))


def illo_rocket(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(24, 34, 52))
    # stars
    for sx, sy in ((0.12, 0.2), (0.85, 0.16), (0.70, 0.34), (0.25, 0.78),
                   (0.90, 0.72)):
        star(draw, x + w * sx, y + h * sy, 3, (255, 255, 255))
    # rocket body, tilted, breaking up
    cx, cy = x + w * 0.42, y + h * 0.52
    draw.polygon([(cx - 8, cy + 18), (cx - 6, cy - 14), (cx, cy - 26),
                  (cx + 6, cy - 14), (cx + 8, cy + 18)], fill=(226, 220, 205))
    draw.rectangle([cx - 8, cy + 2, cx + 8, cy + 12], fill=(176, 30, 36))
    # flame + debris
    burst(draw, cx, cy + 26, 12, (255, 176, 32))
    for dx, dy in ((0.68, 0.30), (0.80, 0.52), (0.62, 0.72)):
        px, py = x + w * dx, y + h * dy
        draw.rectangle([px - 4, py - 4, px + 4, py + 4], fill=(200, 200, 195))
        draw.line([(px - 10, py), (px + 10, py)], fill=(200, 200, 195), width=1)


def illo_border(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(226, 230, 232))
    # fence posts + wire
    for i in range(6):
        px = x + 14 + i * 38
        draw.rectangle([px, y + 10, px + 4, y + h - 10], fill=(90, 90, 88))
    for wy in (y + 16, y + 28, y + 40):
        draw.line([(x + 8, wy), (x + w - 8, wy)], fill=(120, 120, 115), width=1)
    # closed sign
    sx, sy = x + w - 74, y + 8
    draw.rectangle([sx, sy, sx + 62, sy + 22], fill=RED)
    draw.text((sx + 6, sy + 4), "CLOSED", font=f_sans_b(12), fill=(255, 255, 255))
    # small Estonian flag
    flag_stripes(draw, x + 14, y + h - 22, 34, 14,
                 [(31, 78, 121), (20, 20, 20), (247, 247, 247)])


def illo_virus(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(238, 228, 228))
    # spiky virus balls
    for cx, cy, r in ((0.30, 0.42, 15), (0.62, 0.58, 12), (0.82, 0.32, 9)):
        px, py = x + w * cx, y + h * cy
        for ang in range(0, 360, 30):
            rad = math.radians(ang)
            draw.line([(px, py), (px + (r + 7) * math.cos(rad),
                                  py + (r + 7) * math.sin(rad))],
                      fill=(150, 40, 60), width=2)
        draw.ellipse([px - r, py - r, px + r, py + r], fill=(176, 50, 70))
        draw.ellipse([px - r / 2, py - r / 2, px, py], fill=(220, 120, 130))
    # small US flag corner
    flag_stripes(draw, x + w - 44, y + 6, 34, 20,
                 [(176, 30, 36), (247, 247, 247), (176, 30, 36)])
    draw.rectangle([x + w - 44, y + 6, x + w - 30, y + 13], fill=(31, 78, 121))


def illo_yemen(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(238, 226, 200))
    # desert dunes
    draw.polygon([(x, y + h * 0.62), (x + w * 0.35, y + h * 0.42),
                  (x + w * 0.70, y + h * 0.62), (x + w, y + h * 0.48),
                  (x + w, y + h), (x, y + h)], fill=(214, 186, 130))
    draw.polygon([(x, y + h * 0.78), (x + w * 0.45, y + h * 0.60),
                  (x + w, y + h * 0.78), (x + w, y + h), (x, y + h)],
                 fill=(190, 158, 100))
    # flag on a pole + retreat arrow
    fx, fy = x + 22, y + 10
    flag_stripes(draw, fx, fy, 34, 20,
                 [(176, 30, 36), (247, 247, 247), (20, 20, 20)])
    draw.line([(fx, fy + 20), (fx, y + h - 12)], fill=(90, 84, 70), width=2)
    draw.line([(x + w - 90, y + 22), (x + w - 30, y + 22)], fill=RED, width=3)
    draw.polygon([(x + w - 30, y + 22), (x + w - 44, y + 14),
                  (x + w - 44, y + 30)], fill=RED)


def illo_gaza(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(228, 230, 226))
    # border gate + fence
    draw.rectangle([x, y + 8, x + w, y + 12], fill=(90, 90, 88))
    for i in range(7):
        px = x + 12 + i * 30
        draw.line([(px, y + 12), (px, y + h - 14)], fill=(120, 120, 115), width=2)
    # aid trucks
    for tx in (0.14, 0.52):
        px, py = x + w * tx, y + h * 0.58
        draw.rectangle([px, py, px + 52, py + 20], fill=(247, 247, 247),
                       outline=(90, 90, 88))
        draw.rectangle([px + 52, py + 6, px + 68, py + 20], fill=(176, 30, 36))
        draw.ellipse([px + 8, py + 20, px + 18, py + 30], fill=(40, 40, 40))
        draw.ellipse([px + 52, py + 20, px + 62, py + 30], fill=(40, 40, 40))
        draw.text((px + 8, py + 5), "AID", font=f_sans_b(11), fill=RED)


ILLOS = {
    "tanker": illo_tanker, "flags": illo_flags, "radar": illo_radar,
    "jets": illo_jets, "rwanda": illo_rwanda, "bank": illo_bank,
    "chip": illo_chip, "rocket": illo_rocket, "border": illo_border,
    "virus": illo_virus, "yemen": illo_yemen, "gaza": illo_gaza,
}


# ------------------------------------------------------- world map
# Simplified continent outlines as (lon, lat) polygons.
N_AMERICA = [(-168, 65), (-158, 58), (-152, 60), (-140, 60), (-135, 58),
             (-130, 54), (-125, 49), (-124, 42), (-120, 34), (-114, 29),
             (-110, 24), (-105, 20), (-97, 16), (-92, 14), (-86, 12),
             (-83, 9), (-79, 8), (-81, 13), (-86, 16), (-88, 18), (-90, 21),
             (-87, 21), (-84, 30), (-81, 26), (-80, 32), (-76, 35),
             (-74, 40), (-70, 42), (-66, 45), (-60, 47), (-65, 50),
             (-55, 52), (-60, 55), (-65, 60), (-68, 58), (-75, 62),
             (-78, 62), (-85, 66), (-92, 66), (-95, 69), (-110, 68),
             (-125, 70), (-140, 70), (-155, 71), (-165, 68)]
GREENLAND = [(-58, 64), (-52, 60), (-44, 60), (-40, 64), (-32, 68),
             (-22, 70), (-20, 74), (-30, 76), (-45, 76), (-58, 74)]
S_AMERICA = [(-79, 9), (-77, 4), (-80, -3), (-81, -6), (-77, -12),
             (-72, -18), (-70, -23), (-70, -30), (-73, -37), (-73, -44),
             (-74, -50), (-70, -54), (-66, -55), (-65, -45), (-62, -41),
             (-58, -34), (-52, -32), (-48, -28), (-41, -23), (-39, -17),
             (-35, -9), (-35, -6), (-40, -3), (-44, -2), (-50, 0), (-53, 4),
             (-58, 6), (-62, 9), (-68, 11), (-72, 12), (-77, 8)]
AFRICA = [(-17, 15), (-17, 21), (-15, 27), (-10, 31), (-5, 35), (0, 36),
          (10, 37), (11, 34), (20, 32), (30, 31), (32, 31), (34, 28),
          (37, 22), (39, 18), (43, 12), (48, 11), (51, 12), (46, 5),
          (42, 0), (40, -5), (40, -10), (36, -18), (33, -26), (28, -33),
          (20, -35), (17, -32), (15, -27), (13, -18), (12, -10), (13, -5),
          (9, 0), (9, 4), (4, 6), (-8, 5), (-13, 8), (-17, 12)]
EUROPE = [(-10, 36), (-9, 38), (-9, 43), (-2, 44), (-1, 46), (-4, 48),
          (-2, 50), (0, 51), (3, 53), (8, 55), (8, 57), (10, 59), (5, 60),
          (5, 62), (10, 64), (13, 66), (18, 69), (25, 71), (30, 70),
          (32, 68), (35, 66), (40, 64), (42, 60), (40, 58), (35, 55),
          (30, 55), (28, 54), (24, 58), (21, 55), (18, 54), (15, 54),
          (12, 54), (8, 54), (7, 53), (3, 51), (-2, 50), (-5, 48),
          (-2, 47), (-1, 44), (-1, 38), (-6, 36), (-9, 37)]
ASIA = [(28, 41), (30, 42), (33, 42), (36, 41), (39, 41), (41, 42),
        (43, 43), (46, 44), (49, 45), (51, 46), (54, 47), (56, 50),
        (58, 53), (60, 55), (63, 58), (66, 61), (68, 65), (71, 68),
        (74, 70), (78, 72), (84, 74), (90, 75), (96, 76), (102, 77),
        (108, 75), (114, 74), (120, 73), (127, 72), (134, 72), (141, 72),
        (148, 71), (155, 70), (162, 69), (169, 66), (178, 65), (173, 62),
        (168, 60), (162, 58), (158, 53), (156, 51), (150, 59), (144, 57),
        (142, 52), (141, 47), (139, 42), (137, 39), (134, 36), (131, 34),
        (128, 34), (126, 38), (124, 39), (121, 37), (120, 34), (122, 31),
        (120, 27), (117, 24), (113, 22), (110, 20), (108, 18), (106, 10),
        (105, 9), (103, 8), (101, 7), (100, 6), (98, 9), (96, 12),
        (94, 16), (92, 20), (89, 22), (86, 20), (83, 18), (80, 15),
        (77, 8), (76, 10), (74, 14), (72, 19), (70, 21), (68, 23),
        (66, 25), (63, 25), (60, 25), (57, 26), (54, 26), (52, 27),
        (50, 29), (48, 30), (46, 29), (44, 29), (42, 28), (40, 25),
        (39, 22), (38, 20), (36, 18), (35, 16), (34, 14), (33, 12),
        (35, 12), (39, 13), (43, 12), (46, 12), (49, 14), (52, 15),
        (55, 17), (58, 20), (59, 22), (57, 25), (55, 26), (52, 26),
        (50, 26), (48, 28), (48, 30), (47, 31), (44, 31), (42, 32),
        (39, 32), (36, 36), (33, 36), (30, 36), (28, 38)]
JAPAN = [(130, 31), (132, 33), (134, 34), (136, 35), (138, 35), (140, 36),
         (141, 38), (141, 41), (143, 42), (145, 44), (142, 45), (140, 44),
         (138, 40), (136, 38), (134, 36), (132, 34), (130, 32)]
INDONESIA = [(95, 5), (98, 3), (100, 0), (103, -2), (106, -6), (105, -7),
             (100, -2), (97, 3)]
BORNEO = [(109, 1), (113, 4), (117, 6), (119, 1), (117, -2), (113, -4),
          (110, -3), (109, 0)]
NEW_GUINEA = [(131, -1), (136, -2), (141, -3), (146, -6), (150, -9),
              (147, -9), (143, -8), (138, -7), (134, -4)]
AUSTRALIA = [(113, -22), (114, -28), (115, -33), (118, -35), (124, -33),
             (129, -32), (132, -32), (135, -35), (138, -35), (140, -38),
             (145, -38), (150, -37), (153, -32), (153, -27), (150, -23),
             (146, -19), (143, -15), (142, -11), (140, -17), (136, -15),
             (135, -12), (132, -11), (130, -13), (126, -14), (122, -17),
             (118, -20)]
UK = [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (1, 51),
      (-2, 50)]

CONTINENTS = [N_AMERICA, GREENLAND, S_AMERICA, AFRICA, EUROPE, ASIA,
              JAPAN, INDONESIA, BORNEO, NEW_GUINEA, AUSTRALIA, UK]

# pins: (story number, lon, lat, dx, dy) for the hero + 12 panels.
# dx/dy shift a pin (with a leader line) where true spots collide.
PINS = [(1, 33.5, 45.3, 0, 0),
        (2, 56.5, 26.5, 0, 0),
        (3, 121.0, 14.6, 0, 0),
        (4, 50.5, 26.2, 0, 18),
        (5, 139.0, 36.0, 0, 0),
        (6, 30.0, -2.0, 0, 0),
        (7, -74.0, 40.7, 0, 0),
        (8, -121.0, 37.4, 0, 0),
        (9, -80.5, 28.4, 0, 15),
        (10, 24.7, 59.4, 0, 0),
        (11, -98.0, 39.0, 0, 0),
        (12, 45.0, -12.8, 0, 0),
        (13, 34.5, 31.5, 0, 0)]


def draw_map(draw, x0, y0, w, h):
    """Equirectangular world map, lon -180..180, lat 75..-60."""
    draw.rectangle([x0, y0, x0 + w, y0 + h], fill=(233, 228, 212))

    def proj(lon, lat):
        return (x0 + (lon + 180.0) / 360.0 * w,
                y0 + (75.0 - lat) / 135.0 * h)

    for poly in CONTINENTS:
        pts = [proj(lon, lat) for lon, lat in poly]
        draw.polygon(pts, fill=LAND, outline=LANDLINE)
    # ocean labels
    lf = f_sans_b(10)
    draw.text((x0 + 8, y0 + h - 18), "PACIFIC", font=lf, fill=(150, 148, 130))
    draw.text((x0 + w * 0.42, y0 + h - 18), "ATLANTIC", font=lf,
              fill=(150, 148, 130))
    draw.text((x0 + w * 0.74, y0 + h - 18), "INDIAN OCEAN", font=lf,
              fill=(150, 148, 130))
    # continent labels
    draw.text(proj(-105, 62), "NORTH", font=lf, fill=(140, 132, 108))
    draw.text(proj(-105, 56), "AMERICA", font=lf, fill=(140, 132, 108))
    draw.text(proj(-60, -14), "SOUTH AMERICA", font=lf, fill=(140, 132, 108))
    draw.text(proj(2, 18), "AFRICA", font=lf, fill=(140, 132, 108))
    draw.text(proj(78, 52), "ASIA", font=lf, fill=(140, 132, 108))
    draw.text(proj(134, -26), "AUSTRALIA", font=lf, fill=(140, 132, 108))
    # numbered pins (leader line when the pin is shifted)
    for num, lon, lat, dx, dy in PINS:
        px, py = proj(lon, lat)
        if dx or dy:
            draw.line([(px, py), (px + dx, py + dy)], fill=RED, width=1)
            draw.ellipse([px - 2, py - 2, px + 2, py + 2], fill=RED)
            px, py = px + dx, py + dy
        pin(draw, px, py, num)


# ------------------------------------------------------- page assembly
def draw_masthead(draw):
    draw.rectangle([0, 0, W, 104], fill=NAVY)
    draw.text((16, 12), "THE DAY IN WORLD NEWS", font=f_sans_b(13),
              fill=GOLD)
    right = "37 STORIES \u00b7 6 CONTINENTS \u00b7 ONE DAY"
    tw = draw.textlength(right, font=f_sans_b(13))
    draw.text((W - 16 - tw, 12), right, font=f_sans_b(13), fill=GOLD)
    draw.text((16, 34), "Tuesday 17 November 2026", font=f_serif(56),
              fill=CREAM)
    draw.rectangle([0, 100, W, 104], fill=GOLD)


def draw_hero(draw):
    kicker, headline, deck, source = HERO
    y0, y1 = 112, 302
    tx, tw = 16, 584
    draw.text((tx, y0), "1  " + kicker, font=f_sans_b(13), fill=RED)
    y = y0 + 24
    y = text_block(draw, tx, y, wrap(draw, headline, f_serif(34), tw),
                   f_serif(34), INK, 40)
    y += 6
    y = text_block(draw, tx, y, wrap(draw, deck, f_sans(15), tw),
                   f_sans(15), (60, 58, 52), 20)
    draw.text((tx, y1 - 18), source, font=f_sans_b(10), fill=GREY)
    illo_hero(draw, 612, y0, 396, y1 - y0)
    hline(draw, 16, W - 16, y1 + 8, fill=INK, width=2)


def draw_panels(draw):
    x0, y0 = 16, 318
    pw, ph, gx, gy = 240, 152, 10, 8
    for idx, (num, kicker, headline, deck, source, _pin, key) in enumerate(PANELS):
        col, row = idx % 4, idx // 4
        px = x0 + col * (pw + gx)
        py = y0 + row * (ph + gy)
        draw.rectangle([px, py, px + pw, py + ph], fill=PANEL_BG,
                       outline=RULE)
        ILLOS[key](draw, px + 1, py + 1, pw - 2, 52)
        draw.rectangle([px, py + 53, px + pw, py + 56], fill=RED)
        draw.text((px + 8, py + 61), "%d  %s" % (num, kicker),
                  font=f_sans_b(10), fill=RED)
        y = py + 77
        y = text_block(draw, px + 8, y,
                       wrap(draw, headline, f_serif(16), pw - 16)[:2],
                       f_serif(16), INK, 19)
        text_block(draw, px + 8, py + 118,
                   wrap(draw, deck, f_sans(11), pw - 16)[:2],
                   f_sans(11), (60, 58, 52), 13)


def draw_map_band(draw):
    y0 = 798
    draw.text((16, y0), "WHERE IT HAPPENED", font=f_sans_b(13), fill=INK)
    draw.text((16, y0 + 16), "Numbers match stories", font=f_sans(10),
              fill=GREY)
    draw_map(draw, 16, y0 + 34, 560, 152)
    ax = 592
    draw.text((ax, y0), "ALSO ON TUESDAY 17 NOVEMBER",
              font=f_sans_b(13), fill=INK)
    hline(draw, ax, W - 16, y0 + 20, fill=INK, width=2)
    col_w = 202
    fnt = f_sans(10)
    for i, (num, line) in enumerate(ALSO):
        col = i // 12
        row = i % 12
        lx = ax + col * (col_w + 12)
        ly = y0 + 30 + row * 13
        draw.text((lx, ly), "%d" % num, font=f_sans_b(10), fill=RED)
        draw.text((lx + 22, ly), line, font=fnt, fill=INK)


def draw_footer(draw):
    draw.rectangle([0, 992, W, H], fill=NAVY)
    msg = ("Every story was reported on Tuesday 17 November 2026. "
           "Sources: Reuters, AP, AFP, BBC, Al Jazeera, CNBC, ABC News, "
           "NPR and others.")
    draw.text((16, 1001), msg, font=f_sans(11), fill=CREAM)


def build():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    draw_masthead(draw)
    draw_hero(draw)
    draw_panels(draw)
    draw_map_band(draw)
    draw_footer(draw)
    return img


def main():
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(outdir, exist_ok=True)
    img = build()
    img.save(os.path.join(outdir, "entry.png"), format="PNG")


if __name__ == "__main__":
    main()
