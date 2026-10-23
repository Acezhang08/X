# -*- coding: utf-8 -*-
import sys, os, math, importlib
import numpy as np, skia
from lib import *

SEGS = {}
def load_scenes():
    import scenes_a, scenes_b, scenes_c
    for m in (scenes_a, scenes_b, scenes_c):
        SEGS.update(m.REG)
    from common import T
    return T

CY = 455
def draw_world(c, k, t, ox, scraps_base):
    cam, draw, tone = SEGS[k]
    cx, cy, z = cam(t)
    if tone: vignette_tone(c, tone(t))
    wall_scraps(c, scraps_base + (cx - 960), (cy - 455))
    c.save()
    c.translate(W/2 + ox, CY); c.scale(z, z); c.translate(-cx, -cy)
    draw(c, t)
    c.restore()

def draw_frame(c, t, T):
    c.drawImage(paper_image(), 0, 0)
    seg = 0
    for k, st in T.seg_start.items():
        if t >= st - 0.15: seg = k
    nxt = seg + 1
    pan_a = None
    if nxt in T.seg_start:
        a = T.seg_start[nxt] - 0.95; b = T.seg_start[nxt] - 0.15
        if t >= a:
            p = e_io(prog(t, a, b))
            # draw both segments sliding
            if t < b:
                if p > 0.5 and SEGS[nxt][2]: pass
                draw_world(c, seg, t, -p*W, seg*W + p*W)
                draw_world(c, nxt, t, (1-p)*W, seg*W + p*W)
                return
    draw_world(c, seg, t, 0, seg*W)

_surf = None
def frame_surface(t, T):
    global _surf
    if _surf is None: _surf = skia.Surface(W, H)
    c = _surf.getCanvas()
    draw_frame(c, t, T)
    return _surf

if __name__ == "__main__":
    # usage: render.py name spec...   spec = seconds | lineid@offset ; writes build/prev/name.png contact sheet
    from PIL import Image
    T = load_scenes()
    name = sys.argv[1]; files = []
    for ts in sys.argv[2:]:
        if "@" in ts:
            lid, off = ts.split("@"); t = T.s(lid) + float(off)
        else: t = float(ts)
        s = frame_surface(t, T)
        fn = f"build/prev/{name}_{len(files)}.png"; s.makeImageSnapshot().save(fn); files.append(fn)
    cols = 2; w, h = 960, 540
    rows = (len(files) + cols - 1) // cols
    im = Image.new("RGB", (cols*w, rows*h), "white")
    for i, f in enumerate(files):
        im.paste(Image.open(f).convert("RGB").resize((w, h)), ((i % cols)*w, (i//cols)*h))
    im.save(f"build/prev/{name}.png")
