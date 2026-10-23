# -*- coding: utf-8 -*-
"""Three 1280x720 thumbnails + 168x94 previews, built to the sketches in the brief."""
import math, skia
from PIL import Image
import lib
from lib import P, torn_path, INK, PAPER2, GREEN, RED, GRAY, bez
import common

TW, TH = 1280, 720
BLACK = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
_f = {}
def bfont(size):
    if size not in _f: _f[size] = skia.Font(skia.Typeface.MakeFromFile(BLACK, 0), size)
    return _f[size]

def btext(c, s, x, y, size, color, align="c", stroke=None, maxw=None):
    while maxw and bfont(size).measureText(s) > maxw: size -= 4
    f = bfont(size); w = f.measureText(s)
    x0 = x - w/2 if align == "c" else (x if align == "l" else x - w)
    if stroke: c.drawString(s, x0, y, f, P(stroke[0], "stroke", stroke[1]))
    c.drawString(s, x0, y, f, P(color))

def surf(bg):
    s = skia.Surface(TW, TH); c = s.getCanvas(); c.clear(bg); return s, c

def vignette(c, a=0.45):
    sh = skia.GradientShader.MakeRadial((TW/2, TH/2), TW*0.7, [0x00000000, int(255*a) << 24], [0.55, 1.0])
    p = skia.Paint(); p.setShader(sh); c.drawRect(skia.Rect.MakeWH(TW, TH), p)

def vermilion_glow(c, cx, cy, r=420, a=0.28):
    sh = skia.GradientShader.MakeRadial((cx, cy), r, [int(255*a) << 24 | 0xE0341E, 0x00E0341E], [0, 1])
    p = skia.Paint(); p.setShader(sh); c.drawRect(skia.Rect.MakeWH(TW, TH), p)

def bill(c, cx, cy, w, h, rot):
    c.save(); c.translate(cx, cy); c.rotate(rot)
    path = torn_path(w, h, 4, 5, 16)
    c.save(); c.translate(12, 18); c.drawPath(path, P(0x000000, alpha=0.5, blur=18)); c.restore()
    c.drawPath(path, P(0xFFF7F2E7)); c.drawPath(path, P(0xFF9A9282, "stroke", 3))
    for sx in (-1, 1):
        c.save(); c.translate(sx*(w/2 - 60), -h/2 + 14); c.rotate(sx*-0.5)
        c.drawRect(skia.Rect.MakeXYWH(-52, -20, 104, 40), P(0xFFE6D79A, alpha=0.85)); c.restore()
    # header + rows (no readable small print: it must read as "a bill" at thumbnail size)
    f = common.font("serif", 46); c.drawString("ELECTRIC BILL", -w/2 + 44, -h/2 + 118, f, P(INK))
    c.drawLine(-w/2 + 40, -h/2 + 150, w/2 - 40, -h/2 + 150, P(INK, "stroke", 6))
    for i in range(3):
        y = -h/2 + 215 + i*90
        c.drawRect(skia.Rect.MakeXYWH(-w/2 + 44, y - 30, 190 + i*30, 36), P(INK, alpha=0.85))
        c.drawRect(skia.Rect.MakeXYWH(w/2 - 190, y - 30, 146, 36), P(INK, alpha=0.35))
        if i == 2:
            c.drawRect(skia.Rect.MakeXYWH(-w/2 + 24, y - 50, w - 48, 90), P(RED, "stroke", 8))
            c.drawRect(skia.Rect.MakeXYWH(w/2 - 190, y - 30, 146, 36), P(RED, alpha=0.9))
    c.drawLine(-w/2 + 40, h/2 - 85, w/2 - 40, h/2 - 85, P(INK, "stroke", 6))
    c.drawRect(skia.Rect.MakeXYWH(w/2 - 250, h/2 - 62, 206, 36), P(INK))
    c.restore()

def thumb_A():
    s, c = surf(0xFF17171A)
    vermilion_glow(c, 930, 300)
    bill(c, 300, 292, 440, 560, math.radians(-5))
    btext(c, "10×", 930, 470, 400, 0xFFE8331C, maxw=620)
    btext(c, "DATA CENTERS", 640, 694, 96, 0xFFFFFFFF, maxw=1100)
    vignette(c, 0.35)
    return s

def thumb_B():
    s, c = surf(0xFF0A0E1C)
    # faint grid
    for x in range(0, TW, 80): c.drawLine(x, 0, x, TH, P(0xFFFFFF, "stroke", 1, 0.05))
    for y in range(0, TH, 80): c.drawLine(0, y, TW, y, P(0xFFFFFF, "stroke", 1, 0.05))
    pts = [(80, 300), (300, 350), (560, 470)]
    g = skia.Path(); g.moveTo(*pts[0]); g.quadTo(300, 380, 560, 470)
    c.drawPath(g, P(0xFF2FCB6B, "stroke", 28, cap="round"))
    r = skia.Path(); r.moveTo(560, 470); r.quadTo(760, 450, 880, 170); r.lineTo(1020, 60)
    c.drawPath(r, P(0xFFE8331C, "stroke", 28, cap="round"))
    for p_, col in (((560, 470), 0xFFFFFFFF),):
        c.drawCircle(p_[0], p_[1], 24, P(col)); c.drawCircle(p_[0], p_[1], 24, P(0xFF0A0E1C, "stroke", 8))
    common.sil_building(c, 560, 380, 0.9, 0xFFF2EEE4)
    btext(c, "−6%", 250, 580, 170, 0xFF2FCB6B, maxw=400)
    btext(c, "10×", 1050, 400, 190, 0xFFE8331C, maxw=340)
    vignette(c, 0.4)
    return s

def thumb_C():
    s, c = surf(0xFF14161D)
    vermilion_glow(c, 270, 520, 520, 0.12)
    common.sil_building(c, 270, 620, 1.5, 0xFFF2EEE4)
    pole = P(0xFFC9C2B2, "stroke", 10)
    c.drawLine(560, 650, 560, 430, pole); c.drawLine(520, 450, 600, 450, pole)
    w = skia.Path(); w.moveTo(600, 450); w.quadTo(720, 600, 830, 520)
    c.drawPath(w, P(0xFFE8331C, "stroke", 12))
    c.save(); c.translate(930, 640); c.scale(2.4, 2.4)
    c.drawRect(skia.Rect.MakeXYWH(-60, -90, 120, 90), P(0xFFF2EEE4))
    roof = skia.Path(); roof.moveTo(-78, -88); roof.lineTo(0, -160); roof.lineTo(78, -88); roof.close()
    c.drawPath(roof, P(0xFFE8331C))
    c.drawRect(skia.Rect.MakeXYWH(-14, -52, 28, 52), P(0xFF14161D))
    c.drawRect(skia.Rect.MakeXYWH(26, -72, 24, 24), P(0xFF14161D))
    c.restore()
    btext(c, "WHO PAYS?", 930, 150, 120, 0xFFFFFFFF, maxw=640)
    vignette(c, 0.35)
    return s

if __name__ == "__main__":
    import os
    os.makedirs("thumbs_preview", exist_ok=True)
    for k, fn in (("A", thumb_A), ("B", thumb_B), ("C", thumb_C)):
        s = fn(); s.makeImageSnapshot().save(f"thumbnail_{k}.png")
        Image.open(f"thumbnail_{k}.png").convert("RGB").resize((168, 94), Image.LANCZOS).save(f"thumbs_preview/thumbnail_{k}_168x94.png")
    # one contact sheet for quick review: three full-size + three small previews
    sheet = Image.new("RGB", (1280, 720*3//2 + 140), (40, 40, 40))
    for i, k in enumerate("ABC"):
        im = Image.open(f"thumbnail_{k}.png").convert("RGB").resize((640, 360)); sheet.paste(im, ((i % 2)*640, (i//2)*360))
    for i, k in enumerate("ABC"):
        im = Image.open(f"thumbs_preview/thumbnail_{k}_168x94.png"); sheet.paste(im, (20 + i*200, 740))
    sheet.save("build/prev/thumbs_sheet.png")
