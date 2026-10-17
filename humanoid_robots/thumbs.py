# -*- coding: utf-8 -*-
"""Three 1280x720 thumbnails, blueprint style. Max 3 words, one visual focus (a contradiction), high contrast."""
import math, skia
from lib import *
from props import *
from PIL import Image

def base(c):
    c.drawImage(bg_image(), 0, 0)
    c.drawRect(skia.Rect.MakeWH(W, H), P(0x000000, alpha=0.12))

def big(c, s, x, y, size, color=LINE, align="c", kind="monob"):
    text(c, s, x, y, kind, size, color, align, 1, deco=True)

def chk(c, x, y, s): check(c, x, y, s, 1, s * .28, CYAN)
def crs(c, x, y, s): cross(c, x, y, s, 1, s * .3, RED)

def thumb_A(c):      # FLIP ✓ | FOLD ✗
    base(c)
    c.drawLine(960, 120, 960, 960, P(LINE, "stroke", 6, .6, dash=[22, 16]))
    big(c, "FLIP", 480, 190, 230)
    big(c, "FOLD", 1440, 190, 230)
    # left: one big robot mid-flip + rotation arc
    q = flip_pose(.5, 800, 0, 1.0); q["px"] = 480; q["py"] = 620
    arc(c, 480, 620, 250, math.pi * .15, math.pi * 1.55, 1, 7, CYAN, .9, dash=[26, 16])
    arrowhead(c, 480 + 250 * math.cos(math.pi * 1.55), 620 + 250 * math.sin(math.pi * 1.55), math.pi * 1.55 + math.pi / 2, 40, 7, CYAN)
    robot_side(c, s=1.9, alpha=1, **q)
    chk(c, 800, 330, 130)
    # right: crumpled shirt
    draw_shirt(c, 1440, 720, 1.9, 0, 0, 0, alpha=1, crumple=.55, seed=1.7, falpha=.3)
    crs(c, 1440, 720, 190)

def thumb_B(c):      # BACKFLIP ✓ / LAUNDRY ✗  (pure type)
    base(c)
    big(c, "BACKFLIP", 800, 270, 260, LINE)
    chk(c, 1720, 270, 170)
    big(c, "LAUNDRY", 800, 700, 260, LINE)
    crs(c, 1720, 700, 170)
    line(c, 120, 485, 1800, 485, 1, 6, CYAN, .7)
    robot_side(c, 160, 960, s=.0001) if False else None

def thumb_C(c):      # FOLD THIS?  robot arms + shirt + amber ?
    base(c)
    big(c, "FOLD", 560, 200, 250)
    big(c, "THIS?", 560, 470, 250, AMBER)
    draw_shirt(c, 1400, 700, 2.0, 0, 0, 0, alpha=1, crumple=.5, seed=3.1, falpha=.3)
    robot_arms(c, 1400, 330, [(1180, 640), (1620, 640)], (.8, .8), s=1.35)
    qmark(c, 1400, 700, 220, AMBER, 1)

if __name__ == "__main__":
    import os; os.makedirs("build/prev", exist_ok=True)
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
