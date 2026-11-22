# Circuitarium YouTube avatar (800x800) + banner (2560x1440, safe area 1546x423 centred).
# Mark = a transistor as a switch: two gold leads, blue gate dot between them (same as site favicon).
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
BG, PANEL, INK, DIM, GOLD, BLUE = (14, 17, 24), (21, 26, 36), (238, 241, 246), (154, 163, 178), (233, 196, 106), (74, 125, 255)
F = "C:/Windows/Fonts/"
bold = lambda s: ImageFont.truetype(F + "segoeuib.ttf", s)
reg = lambda s: ImageFont.truetype(F + "segoeui.ttf", s)


def glow(img, xy, r, col):
    g = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(g).ellipse([xy[0] - r, xy[1] - r, xy[0] + r, xy[1] + r], fill=col + (110,))
    img.alpha_composite(g.filter(ImageFilter.GaussianBlur(r * 0.6)))


def mark(img, cx, cy, s):
    """s = total width of the mark."""
    glow(img, (cx, cy), int(s * 0.22), BLUE)
    d = ImageDraw.Draw(img)
    lw, gap, r = int(s * 0.085), int(s * 0.17), int(s * 0.11)
    for x0, x1 in ((cx - s // 2, cx - gap), (cx + gap, cx + s // 2)):
        d.rounded_rectangle([x0, cy - lw // 2, x1, cy + lw // 2], radius=lw // 2, fill=GOLD)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=BLUE)


def grid(img, step, col):
    d = ImageDraw.Draw(img)
    for x in range(0, img.width, step): d.line([x, 0, x, img.height], fill=col, width=1)
    for y in range(0, img.height, step): d.line([0, y, img.width, y], fill=col, width=1)


# ---- avatar (YouTube crops to a circle)
a = Image.new("RGBA", (800, 800), BG + (255,))
grid(a, 50, (24, 29, 40))
mark(a, 400, 400, 520)
a.convert("RGB").save(os.path.join(HERE, "yt_avatar_800.png"))

# ---- banner
W, H = 2560, 1440
b = Image.new("RGBA", (W, H), BG + (255,))
grid(b, 64, (22, 27, 37))
d = ImageDraw.Draw(b)
# faint circuit traces across the full width (only TV shows the outside of the safe area)
for i, y in enumerate((480, 560, 880, 960)):
    d.line([0, y, W, y], fill=(30, 37, 52), width=4)
    for x in range(140 + i * 90, W, 420): d.ellipse([x - 9, y - 9, x + 9, y + 9], fill=(40, 50, 70))
# safe area 1546x423 centred -> x 507..2053, y 508..931
cx, cy = W // 2, H // 2
mark(b, 640 + 110, cy, 220)
d = ImageDraw.Draw(b)
d.text((900, cy - 20), "CIRCUITARIUM", font=bold(132), fill=INK, anchor="ls")
d.text((906, cy + 70), "How a chip works, one switch at a time.", font=reg(54), fill=DIM, anchor="ls")
d.text((906, cy + 140), "circuitarium.com", font=reg(42), fill=GOLD, anchor="ls")
b.convert("RGB").save(os.path.join(HERE, "yt_banner_2560.png"))
print("ok")
