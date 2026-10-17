# -*- coding: utf-8 -*-
import sys, os
import skia
from lib import *

SEGS = {}
NAMES = {0: "STUNT", 1: "MORAVEC", 2: "EASY FLIP", 3: "CLOTH", 4: "DATA GAP", 5: "DEMOS", 6: "WHEN"}
T_ = None
def load_scenes():
    global T_
    import scenes_a, scenes_b, scenes_c
    for m in (scenes_a, scenes_b, scenes_c): SEGS.update(m.REG)
    T_ = scenes_a.T
    return T_

def sheet(c, k, t, T):
    c.drawImage(bg_image(), 0, 0)
    SEGS[k](c, t)
    last = (k == 6 and t >= T.s("6.10") + .5)
    titleblock(c, k + 1, NAMES[k], final=last)

def draw_frame(c, t, T):
    seg = 0
    for k, st in T.seg_start.items():
        if t >= st - 0.15: seg = k
    nxt = seg + 1
    if nxt in T.seg_start:
        a = T.seg_start[nxt] - 0.95; b = T.seg_start[nxt] - 0.15
        if a <= t < b:
            p = e_io(prog(t, a, b)); sx = p * W
            c.save(); c.clipRect(skia.Rect.MakeLTRB(sx, 0, W, H)); sheet(c, seg, t, T); c.restore()
            c.save(); c.clipRect(skia.Rect.MakeLTRB(0, 0, sx, H)); sheet(c, nxt, t, T); c.restore()
            c.drawLine(sx, 0, sx, H, P(CYAN, "stroke", 10, .25, blur=8)); c.drawLine(sx, 0, sx, H, P(CYAN, "stroke", 4, .95))
            return
    sheet(c, seg, t, T)

_surf = None
def frame_surface(t, T):
    global _surf
    if _surf is None: _surf = skia.Surface(W, H)
    draw_frame(_surf.getCanvas(), t, T)
    return _surf

if __name__ == "__main__":
    # render.py name spec...  spec = seconds | lineid@offset ; writes build/prev/name.png contact sheet (2 columns)
    from PIL import Image
    import subs
    T = load_scenes(); cues = subs.build_cues(T)
    name = sys.argv[1]; files = []
    for ts in sys.argv[2:]:
        if "@" in ts:
            lid, off = ts.split("@"); t = T.s(lid) + float(off)
        else: t = float(ts)
        s = frame_surface(t, T); cv = s.getCanvas(); subs.draw_subs(cv, subs.cue_at(cues, t))
        fn = f"build/prev/{name}_{len(files)}.png"; s.makeImageSnapshot().save(fn); files.append(fn)
    cols = 2; w, h = 960, 540; rows = (len(files) + cols - 1) // cols
    im = Image.new("RGB", (cols*w, rows*h), "white")
    for i, f in enumerate(files): im.paste(Image.open(f).convert("RGB").resize((w, h)), ((i % cols)*w, (i//cols)*h))
    im.save(f"build/prev/{name}.png"); print("saved", name)
