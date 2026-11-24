"""Draw the 24 November 2026 world news image (1024x1024 PNG).

All art is procedural, drawn with PIL from shapes and text. No network,
no third-party images, no photographs, no real people. Run it with
python3 draw.py; it writes entry.png next to this file. The drawing is
deterministic: the same script always writes the same bytes.

Stories, all in the news cycle of Tuesday 24 November 2026:
1. Kyiv region strikes kill at least 14 (Manila Times, 24 Nov 2026)
2. Drones hit homes and a UN building in Khartoum (AFP, 23-24 Nov 2026)
3. Virginia and Oregon sue Musk firms over Grok deepfakes (Reuters, 23 Nov 2026)
4. Nvidia reinstates Jensen Huang as chief executive (Manila Times, 24 Nov 2026)
5. Trump announces a Japan trade deal; Nikkei rallies (Access24, 24 Nov 2026)
6. Bangladesh starts typhoid jabs for 50 million children (Access24, 24 Nov 2026)
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

PAPER = (247, 243, 232)
INK = (17, 24, 39)
NAVY = (15, 42, 68)
GOLD = (212, 160, 45)
RED = (178, 34, 34)
TEAL = (13, 110, 110)
BLUE = (42, 92, 150)
GREEN = (34, 120, 60)
ORANGE = (220, 110, 20)
GREY = (90, 100, 110)
LIGHT = (255, 255, 255)
BROWN = (120, 72, 20)
DARKGREY = (60, 66, 74)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def bold(size):
    return ImageFont.truetype(BOLD, size)


def reg(size):
    return ImageFont.truetype(REG, size)


def wrap(d, text, fnt, max_w):
    """Split text into lines that fit max_w pixels."""
    lines = []
    cur = ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def panel(d, x0, y0, x1, y1):
    d.rounded_rectangle([x0, y0, x1, y1], radius=6, fill=LIGHT,
                        outline=INK, width=3)


def kicker(d, x, y, text, colour):
    """A coloured label chip with white bold text."""
    fnt = bold(18)
    w = int(d.textlength(text, font=fnt)) + 18
    d.rounded_rectangle([x, y, x + w, y + 26], radius=4, fill=colour)
    d.text((x + 9, y + 4), text, font=fnt, fill=LIGHT)


def draw_building(d, x, y):
    """A damaged block of flats with a blast above it."""
    d.rectangle([x, y + 80, x + 110, y + 260], fill=GREY)
    d.rectangle([x + 120, y + 120, x + 200, y + 260], fill=DARKGREY)
    for wy in (110, 150, 190):
        for wx in (20, 60):
            d.rectangle([x + wx, y + wy, x + wx + 18, y + wy + 18],
                        fill=NAVY)
    d.polygon([(x + 10, y + 80), (x + 55, y + 130), (x + 30, y + 130),
               (x + 70, y + 180), (x + 45, y + 180), (x + 80, y + 230)],
              fill=RED)
    d.ellipse([x + 70, y, x + 130, y + 60], fill=ORANGE)
    d.ellipse([x + 88, y + 18, x + 112, y + 42], fill=GOLD)
    d.polygon([(x, y + 260), (x + 40, y + 230), (x + 80, y + 260)],
              fill=DARKGREY)


def draw_drone(d, x, y):
    """A quadcopter drone above low city blocks."""
    d.rectangle([x, y + 110, x + 40, y + 130], fill=GREY)
    d.rectangle([x + 55, y + 95, x + 95, y + 130], fill=DARKGREY)
    d.rectangle([x + 110, y + 115, x + 145, y + 130], fill=GREY)
    d.ellipse([x + 55, y + 20, x + 95, y + 45], fill=INK)
    d.line([x + 60, y + 32, x + 20, y + 12], fill=INK, width=5)
    d.line([x + 90, y + 32, x + 115, y + 12], fill=INK, width=5)
    d.line([x + 60, y + 32, x + 20, y + 52], fill=INK, width=5)
    d.line([x + 90, y + 32, x + 115, y + 52], fill=INK, width=5)
    for cx, cy in [(20, 12), (115, 12), (20, 52), (115, 52)]:
        d.ellipse([x + cx - 14, y + cy - 4, x + cx + 14, y + cy + 4],
                  fill=GREY)
    d.ellipse([x + 105, y + 70, x + 125, y + 90], fill=ORANGE)


def draw_scales(d, x, y):
    """Scales of justice for the court story."""
    d.line([x + 45, y, x + 45, y + 110], fill=INK, width=5)
    d.line([x, y + 8, x + 90, y + 8], fill=INK, width=5)
    d.ellipse([x + 38, y - 8, x + 52, y + 6], fill=GOLD)
    for sx in (0, 90):
        d.line([x + sx, y + 8, x + sx - 18, y + 55], fill=INK, width=3)
        d.line([x + sx, y + 8, x + sx + 18, y + 55], fill=INK, width=3)
        d.pieslice([x + sx - 20, y + 48, x + sx + 20, y + 72], 0, 180,
                   fill=GOLD)
    d.rectangle([x + 10, y + 110, x + 80, y + 122], fill=NAVY)


def draw_chip(d, x, y):
    """A green computer chip."""
    d.rectangle([x, y, x + 44, y + 36], fill=GREEN)
    d.rectangle([x + 10, y + 8, x + 34, y + 28], fill=LIGHT)
    d.rectangle([x + 16, y + 14, x + 28, y + 22], fill=GREEN)
    for px in (6, 20, 34):
        d.rectangle([x + px, y - 8, x + px + 4, y], fill=INK)
        d.rectangle([x + px, y + 36, x + px + 4, y + 44], fill=INK)


def draw_bars(d, x, y):
    """Three rising bars with an upward arrow."""
    d.rectangle([x, y + 28, x + 12, y + 44], fill=TEAL)
    d.rectangle([x + 18, y + 16, x + 30, y + 44], fill=TEAL)
    d.rectangle([x + 36, y + 2, x + 48, y + 44], fill=TEAL)
    d.line([x, y + 34, x + 48, y - 4], fill=RED, width=4)
    d.polygon([(x + 48, y - 4), (x + 36, y - 2), (x + 46, y + 8)],
              fill=RED)


def draw_shield(d, x, y):
    """A white shield with a red cross for the health story."""
    d.polygon([(x, y), (x + 44, y), (x + 44, y + 26), (x + 22, y + 44),
               (x, y + 26)], fill=LIGHT, outline=RED)
    d.rectangle([x + 18, y + 8, x + 26, y + 30], fill=RED)
    d.rectangle([x + 10, y + 15, x + 34, y + 23], fill=RED)


def draw():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Masthead
    d.rectangle([0, 0, W, 118], fill=NAVY)
    d.rectangle([0, 112, W, 118], fill=GOLD)
    d.text((28, 16), "THE WORLD IN ONE PAGE", font=bold(50), fill=LIGHT)
    d.text((28, 72), "TUESDAY 24 NOVEMBER 2026", font=bold(30),
           fill=GOLD)
    d.text((560, 80), "SIX STORIES THAT SHAPED THE DAY", font=bold(20),
           fill=LIGHT)

    # Lead story: Kyiv region strikes
    panel(d, 24, 134, 1000, 460)
    kicker(d, 44, 152, "LEAD STORY - UKRAINE", RED)
    d.text((44, 192), "KYIV REGION STRIKES", font=bold(44), fill=INK)
    d.text((44, 240), "KILL AT LEAST 14", font=bold(44), fill=INK)
    sub = ("Rescuers search the rubble of a collapsed block of flats in "
           "Dymer, north of Kyiv, after Russian strikes kill at least 14 "
           "people across the region.")
    yy = 300
    for line in wrap(d, sub, reg(21), 560):
        d.text((44, yy), line, font=reg(21), fill=INK)
        yy += 28
    draw_building(d, 750, 170)

    # Row 2, panel 1: Sudan drones
    panel(d, 24, 476, 502, 712)
    kicker(d, 40, 492, "SUDAN", NAVY)
    d.text((40, 528), "DRONES HIT HOMES", font=bold(32), fill=INK)
    d.text((40, 564), "AND UN BUILDING", font=bold(32), fill=INK)
    sub = ("Drones strike Khartoum, wrecking homes and a UN building. "
           "Sudan blames launches from Ethiopia.")
    yy = 606
    for line in wrap(d, sub, reg(18), 300):
        d.text((40, yy), line, font=reg(18), fill=INK)
        yy += 24
    draw_drone(d, 368, 578)

    # Row 2, panel 2: Grok lawsuits
    panel(d, 522, 476, 1000, 712)
    kicker(d, 538, 492, "UNITED STATES", RED)
    d.text((538, 528), "STATES SUE MUSK", font=bold(32), fill=INK)
    d.text((538, 564), "OVER GROK IMAGES", font=bold(32), fill=INK)
    sub = ("Virginia and Oregon file the first state suits over sexual "
           "images made by the Grok chatbot.")
    yy = 606
    for line in wrap(d, sub, reg(18), 300):
        d.text((538, yy), line, font=reg(18), fill=INK)
        yy += 24
    draw_scales(d, 885, 590)

    # Row 3, panel 1: Nvidia
    panel(d, 24, 728, 336, 924)
    kicker(d, 36, 742, "BUSINESS", TEAL)
    draw_chip(d, 272, 742)
    d.text((36, 780), "HUANG IS BACK", font=bold(25), fill=INK)
    d.text((36, 808), "AT NVIDIA", font=bold(25), fill=INK)
    sub = ("Nvidia reinstates Jensen Huang as chief executive after "
           "President Trump intervenes.")
    yy = 840
    for line in wrap(d, sub, reg(17), 276):
        d.text((36, yy), line, font=reg(17), fill=INK)
        yy += 22

    # Row 3, panel 2: Japan trade deal
    panel(d, 356, 728, 668, 924)
    kicker(d, 368, 742, "TRADE", NAVY)
    draw_bars(d, 620, 740)
    d.text((368, 780), "JAPAN TRADE DEAL", font=bold(25), fill=INK)
    d.text((368, 808), "NIKKEI RALLIES", font=bold(25), fill=INK)
    sub = ("Trump announces a trade deal with Japan. Tokyo's Nikkei "
           "leads an Asian rally.")
    yy = 840
    for line in wrap(d, sub, reg(17), 276):
        d.text((368, yy), line, font=reg(17), fill=INK)
        yy += 22

    # Row 3, panel 3: Bangladesh typhoid drive
    panel(d, 688, 728, 1000, 924)
    kicker(d, 700, 742, "HEALTH", RED)
    draw_shield(d, 946, 734)
    d.text((700, 780), "TYPHOID JABS FOR", font=bold(25), fill=INK)
    d.text((700, 808), "50 MILLION KIDS", font=bold(25), fill=INK)
    sub = ("Bangladesh begins a month-long drive to vaccinate 50 "
           "million children.")
    yy = 840
    for line in wrap(d, sub, reg(17), 276):
        d.text((700, yy), line, font=reg(17), fill=INK)
        yy += 22

    # Footer ticker: two more verified stories from the same day
    d.rectangle([0, 940, W, H], fill=NAVY)
    d.text((24, 954), "ALSO TODAY: CHINA SENTENCES AN OFFICIAL TO DEATH "
           "FOR SPYING", font=bold(19), fill=LIGHT)
    d.text((24, 982), "TRUMP PAUSES PLANNED DETONATION OF DEGRADED "
           "EXPLOSIVES", font=bold(19), fill=GOLD)
    return img


if __name__ == "__main__":
    image = draw()
    image.save("entry.png", format="PNG")
    print("wrote entry.png", image.size)
