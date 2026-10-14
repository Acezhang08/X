# -*- coding: utf-8 -*-
"""Three 1280x720 thumbnails in the aged-paper ink style. Max 3 words, one visual focus, high contrast."""
import math, skia
from lib import *
from props import *
from PIL import Image

def base(c):
    c.drawImage(paper_image(), 0, 0)
    c.drawRect(skia.Rect.MakeWH(W, H), P(0xFFF6EBCB, alpha=0.35))      # slightly brighter, higher contrast

def big(c, s, x, y, size, color=INK, kind="serif", align="l", stroke=True):
    text(c, s, x, y, kind, size, color, align, stroke=(PAPER2, 14) if stroke else None, deco=True)

def thumb_A(c):   # LEAVE THE ROOM
    base(c)
    big(c, "LEAVE", 90, 230, 240, INK, "serif")
    big(c, "THE", 90, 440, 240, INK, "serif")
    big(c, "ROOM", 90, 670, 270, VERM, "serif")
    # open door, dark inside (right)
    c.save(); c.translate(1660, 960)
    c.drawRect(skia.Rect.MakeXYWH(-210, -820, 420, 820), P(0xFF2A1D10)); ink(c, rect_path(-210, -820, 420, 820), 9)
    leaf = poly_path([(-210, -820), (-70, -780), (-70, -40), (-210, 0)])
    c.drawPath(leaf, P(PAPER2)); ink(c, leaf, 7)
    c.drawCircle(-100, -400, 10, P(INK))
    c.restore()
    # secretary behind her typewriter
    person2(c, 1230, 1000, 1.7, "woman", color=INK)
    terminal(c, 1420, 1040, 0.95)

def thumb_B(c):   # 1966 CHATBOT
    base(c)
    text(c, "1966", 960, 330, "type", 470, VERM, "c", stroke=(PAPER2, 16), deco=True)
    big(c, "CHATBOT", 960, 690, 250, INK, "serif", "c")
    underline(c, 260, 1660, 800, 1.0, VERM, 12)

def thumb_C(c):   # NOTHING INSIDE
    base(c)
    big(c, "NOTHING", 90, 300, 250, INK, "serif")
    big(c, "INSIDE", 90, 590, 250, VERM, "serif")
    # hollow dashed bust with a big question mark
    c.save(); c.translate(1480, 1000); c.scale(2.45, 2.45)
    head = skia.Path(); head.addOval(skia.Rect.MakeXYWH(-50, -254, 100, 128))
    body = skia.Path(); body.moveTo(-136, 0); body.cubicTo(-136, -62, -104, -92, -56, -104); body.lineTo(56, -104); body.cubicTo(104, -92, 136, -62, 136, 0); body.close()
    for pth in (head, body):
        c.drawPath(pth, P(PAPER2, alpha=0.6)); c.drawPath(pth, P(INK, "stroke", 5, dash=[18, 12]))
    text(c, "?", 0, -190, "type", 110, VERM, deco=True)
    c.restore()
    bubble(c, 1560, 190, 340, 190, tail=(-0.5, 1))
    text(c, "…", 1560, 190, "type", 110, INK, deco=True)

if __name__ == "__main__":
    for name, fn in (("A", thumb_A), ("B", thumb_B), ("C", thumb_C)):
        s = skia.Surface(W, H); fn(s.getCanvas())
        s.makeImageSnapshot().save(f"build/thumb_{name}_full.png")
        Image.open(f"build/thumb_{name}_full.png").convert("RGB").resize((1280, 720), Image.LANCZOS).save(f"thumbnail_{name}.png")
    sm = Image.new("RGB", (960 + 20, 180 * 3 + 20), "white")
    for i, n in enumerate("ABC"): sm.paste(Image.open(f"thumbnail_{n}.png").resize((320, 180)), (0, i * 190))
    sm.save("build/prev/thumbs_small.png")
    big_ = Image.new("RGB", (1280, 2160))
    for i, n in enumerate("ABC"): big_.paste(Image.open(f"thumbnail_{n}.png"), (0, i * 720))
    big_.save("build/prev/thumbs.png")
