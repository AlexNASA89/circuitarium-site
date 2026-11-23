# Circuitarium avatar options, red / blue / white only (Alex 39870/39872: no yellow+blue anywhere).
# Writes brand/avatar_opts/av_1..5.png (800x800) + sheet.jpg (circle-cropped preview like IG/YT).
import os, math
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "avatar_opts"); os.makedirs(OUT, exist_ok=True)
S = 800; C = S // 2
BG = (12, 14, 20); INK = (240, 242, 246); RED = (255, 72, 66); BLUE = (64, 118, 255); STEEL = (70, 84, 112)


def canvas(grid=True):
    im = Image.new("RGBA", (S, S), BG + (255,))
    if grid:
        d = ImageDraw.Draw(im)
        for i in range(0, S, 40): d.line([i, 0, i, S], fill=(22, 26, 36)); d.line([0, i, S, i], fill=(22, 26, 36))
    return im


def glow(im, box, col, a=120, blur=60, ellipse=True):
    g = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(g)
    (d.ellipse if ellipse else d.rectangle)(box, fill=col + (a,))
    im.alpha_composite(g.filter(ImageFilter.GaussianBlur(blur)))


def av1():  # transistor switch: red leads, white gate dot, blue halo
    im = canvas(); glow(im, [C - 150, C - 150, C + 150, C + 150], BLUE, 130, 70)
    d = ImageDraw.Draw(im); lw = 44
    d.rounded_rectangle([C - 260, C - lw // 2, C - 90, C + lw // 2], radius=lw // 2, fill=RED)
    d.rounded_rectangle([C + 90, C - lw // 2, C + 260, C + lw // 2], radius=lw // 2, fill=RED)
    d.ellipse([C - 58, C - 58, C + 58, C + 58], fill=INK)
    return im


def av2():  # chip: white package with pins, red die, blue traces
    im = canvas(); d = ImageDraw.Draw(im)
    for k in range(-2, 3):
        y = C + k * 52
        d.line([60, y, C - 200, y], fill=BLUE, width=8); d.line([C + 200, y, S - 60, y], fill=BLUE, width=8)
        d.line([C + k * 52, 60, C + k * 52, C - 200], fill=BLUE, width=8); d.line([C + k * 52, C + 200, C + k * 52, S - 60], fill=BLUE, width=8)
    glow(im, [C - 170, C - 170, C + 170, C + 170], RED, 120, 50, False); d = ImageDraw.Draw(im)
    d.rounded_rectangle([C - 170, C - 170, C + 170, C + 170], radius=26, fill=(26, 30, 40), outline=INK, width=12)
    d.rounded_rectangle([C - 80, C - 80, C + 80, C + 80], radius=12, fill=RED)
    for i in range(-60, 61, 40): d.line([C + i, C - 80, C + i, C + 80], fill=(200, 50, 50), width=3)
    return im


def av3():  # wafer: steel disc, die grid, one red die
    im = canvas(False); r = 320
    disc = Image.new("RGB", (2 * r, 2 * r), STEEL); dd = ImageDraw.Draw(disc)
    dd.ellipse([-120, -80, r * 1.3, r * 1.2], fill=(84, 112, 190)); disc = disc.filter(ImageFilter.GaussianBlur(90)); dd = ImageDraw.Draw(disc)
    st = 2 * r // 12
    for i in range(0, 2 * r, st): dd.line([i, 0, i, 2 * r], fill=(34, 40, 56), width=3); dd.line([0, i, 2 * r, i], fill=(34, 40, 56), width=3)
    dd.rectangle([st * 7 + 3, st * 4 + 3, st * 8 - 2, st * 5 - 2], fill=RED)
    m = Image.new("L", disc.size, 0); md = ImageDraw.Draw(m); md.ellipse([0, 0, 2 * r - 1, 2 * r - 1], fill=255)
    md.rectangle([r - 40, 2 * r - 24, r + 40, 2 * r], fill=0)  # wafer notch
    im.paste(disc, (C - r, C - r), m); ImageDraw.Draw(im).arc([C - r, C - r, C + r, C + r], 0, 360, fill=INK, width=8)
    return im


def av4():  # "C" monogram drawn as a circuit trace with nodes
    im = canvas(); glow(im, [C - 220, C - 220, C + 220, C + 220], BLUE, 70, 90); d = ImageDraw.Draw(im)
    r = 230; d.arc([C - r, C - r, C + r, C + r], 40, 320, fill=INK, width=46)
    for ang in (40, 320):
        x = C + r * math.cos(math.radians(ang)); y = C + r * math.sin(math.radians(ang))
        d.ellipse([x - 44, y - 44, x + 44, y + 44], fill=RED)
        d.ellipse([x - 18, y - 18, x + 18, y + 18], fill=BG)
    d.line([C - 60, C, C + 120, C], fill=BLUE, width=30); d.ellipse([C + 90, C - 34, C + 158, C + 34], fill=RED)
    return im


def av5(bg=True):  # MOSFET cross-section icon: blue substrate, red wells, white gate  (CHOSEN, Alex 39878)
    im = canvas() if bg else Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([C - 270, C - 30, C + 270, C + 190], radius=24, fill=BLUE)
    d.rounded_rectangle([C - 240, C - 30, C - 70, C + 70], radius=20, fill=RED)
    d.rounded_rectangle([C + 70, C - 30, C + 240, C + 70], radius=20, fill=RED)
    d.rounded_rectangle([C - 110, C - 90, C + 110, C - 46], radius=10, fill=INK)
    for x in (C - 155, C, C + 155):
        top = C - 230 if x == C else C - 190
        d.line([x, top, x, C - 90 if x == C else C - 30], fill=INK, width=16)
        d.ellipse([x - 30, top - 30, x + 30, top + 30], outline=INK, width=14)
    return im


def preview(im):
    p = im.convert("RGB").resize((300, 300), Image.LANCZOS); m = Image.new("L", (300, 300), 0)
    ImageDraw.Draw(m).ellipse([0, 0, 299, 299], fill=255); o = Image.new("RGB", (300, 300), (255, 255, 255)); o.paste(p, (0, 0), m); return o


if __name__ == "__main__":
    ims = [f() for f in (av1, av2, av3, av4, av5)]
    sheet = Image.new("RGB", (5 * 320 + 20, 380), (255, 255, 255)); sd = ImageDraw.Draw(sheet)
    fnt = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 40)
    for i, im in enumerate(ims, 1):
        im.convert("RGB").save(os.path.join(OUT, f"av_{i}.png"))
        sheet.paste(preview(im), (20 + (i - 1) * 320, 20)); sd.text((170 + (i - 1) * 320, 350), str(i), font=fnt, fill=(0, 0, 0), anchor="mm")
    sheet.save(os.path.join(OUT, "sheet.jpg"), quality=90)
    # chosen = 5: final avatar + transparent icon for watermark / banner / site
    av5().convert("RGB").save(os.path.join(HERE, "avatar_800.png"))
    ic = av5(bg=False); ic = ic.crop(ic.getbbox()); ic.save(os.path.join(HERE, "icon.png"))
    ic.resize((64, round(64 * ic.height / ic.width)), Image.LANCZOS).save(os.path.join(HERE, "icon_64.png")); print("ok")
