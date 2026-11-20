#!/usr/bin/env python3
"""Draw the 20 November 2026 world-news summary image (1024x1024 PNG).

Stories verified from 20 Nov 2026 reporting (Dawn, BBC, Bangkok Post,
Scoop, The Standard, AppiSToS). Typography only: no AI-generated art,
so every word is crisp and legible.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (255, 255, 255)
INK = (17, 17, 17)
GREY = (110, 110, 110)
RED = (192, 32, 32)
BLUE = (31, 56, 100)
TEAL = (14, 110, 90)
GOLD = (146, 102, 0)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)

F_DATE = font("DejaVuSans-Bold.ttf", 68)
F_SUB = font("DejaVuSans.ttf", 24)
F_KICK = font("DejaVuSans-Bold.ttf", 22)
F_HEAD = font("DejaVuSans-Bold.ttf", 40)
F_HEAD2 = font("DejaVuSans-Bold.ttf", 30)
F_BODY = font("DejaVuSans.ttf", 24)
F_BODY2 = font("DejaVuSans.ttf", 21)
F_TICK = font("DejaVuSans.ttf", 20)
F_FOOT = font("DejaVuSans.ttf", 18)

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

def wrap(text, fnt, width):
    lines = []
    for para in text.split("\n"):
        lines += textwrap.wrap(para, width=width, break_long_words=False) or [""]
    return lines

def text_block(x, y, lines, fnt, fill=INK, leading=None):
    if leading is None:
        leading = int(fnt.size * 1.25)
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y

def text_w(text, fnt):
    return d.textlength(text, font=fnt)

MX = 30  # margin
# ---------- masthead ----------
y = 30
d.text((MX, y), "THE WORLD IN ONE IMAGE", font=F_SUB, fill=GREY)
y += 34
date = "20 NOVEMBER 2026"
d.text((MX, y), date, font=F_DATE, fill=INK)
y += 84
d.text((MX, y), "FRIDAY  ·  THE DAY'S NEWS, SUMMED UP", font=F_SUB, fill=INK)
y += 40
d.rectangle([MX, y, W - MX, y + 6], fill=RED)
y += 22

# ---------- lead story (full width) ----------
lead_kicker = "DIPLOMACY  ·  BEIJING"
d.text((MX, y), lead_kicker, font=F_KICK, fill=RED)
y += 32
lead_head = "Trump, Putin and Xi release a\n\u2018peace declaration\u2019"
y = text_block(MX, y, lead_head.split("\n"), F_HEAD, leading=48)
y += 6
lead_body = ("Trilateral talks open on Ukraine, Iran, trade and nuclear arms "
             "as the APEC summit wraps up in Shenzhen.")
y = text_block(MX, y, wrap(lead_body, F_BODY, 62), F_BODY, leading=30)
y += 14
d.line([MX, y, W - MX, y], fill=(200, 200, 200), width=2)
y += 16

# ---------- 2x2 grid ----------
col_w = (W - 2 * MX - 24) // 2
row_h = 218
stories = [
    ("CLIMATE", RED, "Fossil fuels cut from draft UN climate deal",
     "COP31 talks enter crunch time with no deal in sight as the fossil-fuel phase-out is dropped."),
    ("TECH", BLUE, "Anthropic lists in a landmark AI IPO",
     "The first pure-AI company goes public; shares spike, then fade as AI-bubble fears hit markets."),
    ("EUROPE", TEAL, "UK pledges 1,000 drones for Ukraine",
     "\u00a3260m long-range drone package unveiled in Berlin as Europe readies talks with Russia."),
    ("USA", GOLD, "Trump pardons baseball legend Pete Rose",
     "The late hits king is cleared posthumously, 37 years after his lifetime ban."),
]
gx0, gy0 = MX, y
for i, (kick, color, head, body) in enumerate(stories):
    cx = gx0 + (i % 2) * (col_w + 24)
    cy = gy0 + (i // 2) * row_h
    d.rectangle([cx, cy, cx + 8, cy + 26], fill=color)
    d.text((cx + 18, cy), kick, font=F_KICK, fill=color)
    hy = cy + 34
    hl = wrap(head, F_HEAD2, 24)
    hy = text_block(cx, hy, hl, F_HEAD2, leading=36)
    by = hy + 6
    bl = wrap(body, F_BODY2, 34)
    text_block(cx, by, bl, F_BODY2, leading=26)

# ---------- ticker + footer ----------
ty = gy0 + 2 * row_h + 10
d.rectangle([MX, ty, W - MX, ty + 2], fill=(200, 200, 200))
ty += 14
ticker = "ALSO: Van Gogh sells for a record $190.4m  ·  Scientists grow potatoes in moon soil"
d.text((MX, ty), ticker, font=F_TICK, fill=INK)
ty += 34
d.rectangle([MX, ty, W - MX, ty + 2], fill=(200, 200, 200))
ty += 12
d.text((MX, ty), "20 NOVEMBER 2026", font=F_FOOT, fill=GREY)
foot_r = "Summed up from the day's reporting"
d.text((W - MX - text_w(foot_r, F_FOOT), ty), foot_r, font=F_FOOT, fill=GREY)

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
import os
print("bytes:", os.path.getsize("entry.png"))
