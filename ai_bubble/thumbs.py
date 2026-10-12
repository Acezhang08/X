# -*- coding: utf-8 -*-
import math, skia
from lib import *
from scenes_c import fiber_bundle

def base(c):
    c.drawImage(paper_image(), 0, 0)

def ring_pt(cx, cy, r, deg): return cx + r*math.cos(math.radians(deg)), cy + r*math.sin(math.radians(deg))

def thumb_A(c):
    base(c)
    NV, OA, AM = (430, 330), (1330, 330), (1330, 730)
    # NVIDIA <-> OPENAI: top arc = $ investment, bottom arc = buys chips
    top = bez((NV[0] + 190, NV[1] - 30), ((NV[0] + OA[0]) / 2, 90), (OA[0] - 190, OA[1] - 30))
    bot = bez((OA[0] - 190, OA[1] + 40), ((NV[0] + OA[0]) / 2, 600), (NV[0] + 190, NV[1] + 40))
    arrow(c, top, 1.0, GREEN, 20, head_size=56)
    arrow(c, bot, 1.0, GREEN, 20, head_size=56)
    text(c, "$", 880, 205, "mono", 150, AMBER, stroke=(INK, 4))
    chip(c, 880, 505, 1.1, INK)
    bill(c, 700, 205, -8, 1.3); bill(c, 1080, 455, 190, 1.0)
    # OPENAI <-> AMD: smaller pair (chips down, shares up)
    d1 = bez((OA[0] - 60, OA[1] + 60), (OA[0] - 120, (OA[1] + AM[1]) / 2), (AM[0] - 60, AM[1] - 60))
    d2 = bez((AM[0] + 60, AM[1] - 60), (AM[0] + 120, (OA[1] + AM[1]) / 2), (OA[0] + 60, OA[1] + 60))
    arrow(c, d1, 1.0, GREEN, 13, head_size=38)
    arrow(c, d2, 1.0, AMBER, 13, head_size=38)
    stamp(c, "NVIDIA", NV[0], NV[1], 99, 0, INK, -2, 64, pad=(34, 22))
    stamp(c, "OPENAI", OA[0], OA[1], 99, 0, INK, 2, 64, pad=(34, 22))
    stamp(c, "AMD", AM[0], AM[1], 99, 0, INK, -1.5, 56, pad=(30, 20))
    text(c, "THE MONEY LOOP", 800, 925, "serif", 150, INK)

def thumb_B(c):
    base(c)
    text(c, "$800B", 590, 380, "mono", 330, AMBER, stroke=(INK, 5))
    text(c, "ONE YEAR · 5 COMPANIES", 590, 590, "sans", 56, INK) if False else None
    text(c, "?", 1520, 440, "serif", 820, INK)
    c.drawCircle(1490, 684, 82, P(0xFFEDE7DB))
    c.drawRect(skia.Rect.MakeXYWH(1395, 628, 190, 112), P(INK))
    c.drawRect(skia.Rect.MakeXYWH(1385, 618, 210, 14), P(INK))
    for r_ in range(3):
        for k in range(5):
            c.drawRect(skia.Rect.MakeXYWH(1408 + k*34, 648 + r_*28, 22, 14), P(AMBER if (r_ + k) % 4 == 0 else PAPER2))
    text(c, "WHERE'S IT GO?", 700, 855, "serif", 140, INK)

def thumb_C(c):
    base(c)
    c.save(); c.clipRect(skia.Rect.MakeXYWH(0, 0, 940, 1080))
    c.drawRect(skia.Rect.MakeWH(1920, 1080), P(0xFFEBD9A8))
    fiber_bundle(c, -20, 960, 220, 12, 1.0, GREEN, 26, 36, 11)
    c.drawCircle(560, 380, 230, P(AMBER, alpha=0.18, blur=40))
    c.restore()
    c.save(); c.clipRect(skia.Rect.MakeXYWH(980, 0, 940, 1080))
    c.drawRect(skia.Rect.MakeWH(1920, 1080), P(0xFFC9C5BC))
    for i in range(6):
        r_, k = divmod(i, 2)
        gpu(c, 1220 + k*330, 330 + r_*190, 2.0, GRAYDK_)
        c.drawLine(1090 + k*330, 180 + r_*210 + 0, 1350 + k*330, 360 + r_*210, P(GRAYDK_, "stroke", 0.01, 0))
    c.restore()
    # torn seam
    seam = skia.Path(); seam.moveTo(945, -10)
    import random; rr = random.Random(3)
    y = -10
    while y < 1100:
        y += 30; seam.lineTo(945 + rr.uniform(-16, 16) + (18 if int(y/30) % 2 else -18), y)
    seam.lineTo(1000, 1100); seam.lineTo(1000, -10); seam.close()
    c.drawPath(seam, P(0x2A2418, alpha=0.35, blur=14)); c.drawPath(seam, P(PAPER2))
    text(c, "2001", 470, 110, "mono", 130, INK, stroke=(PAPER2, 8)); text(c, "2026", 1450, 110, "mono", 130, GRAYDK_, stroke=(PAPER2, 8))
    text(c, "WHAT SURVIVES?", 780, 900, "serif", 150, INK, stroke=(PAPER2, 14))

GRAYDK_ = 0xFF6F6A60

if __name__ == "__main__":
    from PIL import Image
    for name, fn in (("A", thumb_A), ("B", thumb_B), ("C", thumb_C)):
        s = skia.Surface(W, H); fn(s.getCanvas())
        s.makeImageSnapshot().save(f"build/thumb_{name}_full.png")
        Image.open(f"build/thumb_{name}_full.png").convert("RGB").resize((1280, 720), Image.LANCZOS).save(f"thumbnail_{name}.png")
    ims = [Image.open(f"thumbnail_{n}.png") for n in "ABC"]
    sh = Image.new("RGB", (1280, 2160))
    for i, im in enumerate(ims): sh.paste(im, (0, i*720))
    sh.save("build/prev/thumbs.png")
