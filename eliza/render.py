# -*- coding: utf-8 -*-
import sys, os
import skia
from lib import *

SEGS = {}   # seg -> (cam, draw)
T_ = None
def load_scenes():
    global T_
    import scenes_a, scenes_b, scenes_c
    for m in (scenes_a, scenes_b, scenes_c): SEGS.update(m.REG)
    T_ = scenes_a.T
    return T_

def draw_world(c, k, t, ox, scraps_base):
    cam, draw = SEGS[k]
    cx, cy = cam(t)
    wall_scraps(c, scraps_base + (cx - 960), (cy - 540))
    c.save(); c.translate(W/2 + ox - cx, H/2 - cy); draw(c, t); c.restore()

def draw_frame(c, t, T):
    c.drawImage(paper_image(), 0, 0)
    seg = 0
    for k, st in T.seg_start.items():
        if t >= st - 0.15: seg = k
    nxt = seg + 1
    if nxt in T.seg_start:
        a = T.seg_start[nxt] - 0.95; b = T.seg_start[nxt] - 0.15
        if t >= a and t < b:
            p = e_io(prog(t, a, b))
            draw_world(c, seg, t, -p*W, seg*W + p*W)
            draw_world(c, nxt, t, (1-p)*W, seg*W + p*W)
            return
    draw_world(c, seg, t, 0, seg*W)

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
    im.save(f"build/prev/{name}.png"); print("saved", name, [round(float(x.split('@')[0]) if '@' not in x else 0,1) for x in sys.argv[2:]])
