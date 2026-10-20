# -*- coding: utf-8 -*-
import sys, os
import skia
from lib import *

SEGS = {}
NAMES = {0: "THE QUIZ", 1: "HOW IT IS MADE", 2: "THE OLD TELLS", 3: "THE SECOND STUDY", 4: "WHAT STILL WORKS", 5: "WHAT TO DO"}
FADE_OUT, FADE_IN = .9, .35   # cross-fade sits in the pause before each segment (1.0 s gap in the voice track)

def load_scenes():
    import scenes_a, scenes_b, scenes_c
    for m in (scenes_a, scenes_b, scenes_c): SEGS.update(m.REG)
    return scenes_a.T

def draw_seg(c, k, t):
    c.drawImage(bg_image(), 0, 0)
    SEGS[k](c, t)

def draw_frame(c, t, T):
    seg = 0
    for k, st in T.seg_start.items():
        if t >= st - FADE_IN: seg = max(seg, k)
    nxt = seg + 1
    if nxt in T.seg_start and t >= T.seg_start[nxt] - FADE_OUT and seg in T.seg_start and t < T.seg_start[nxt] + FADE_IN:
        st = T.seg_start[nxt]
        a = prog(t, st - FADE_OUT, st - FADE_IN)     # previous fades out
        b = prog(t, st - FADE_IN, st + FADE_IN)      # next fades in
        c.drawImage(bg_image(), 0, 0)
        c.saveLayerAlpha(None, int(255 * (1 - a))); SEGS[seg](c, t); c.restore()
        c.saveLayerAlpha(None, int(255 * b)); SEGS[nxt](c, t); c.restore()
        return
    draw_seg(c, seg, t)

if __name__ == "__main__":
    # python3 render.py name t1 t2 ...  -> build/prev/name.png (2-column contact sheet), subtitles included
    from PIL import Image
    import subs
    T = load_scenes(); cues = subs.build_cues(T)
    name = sys.argv[1]; files = []
    os.makedirs("build/prev", exist_ok=True)
    for ts in sys.argv[2:]:
        t = T.s(ts.split("@")[0]) + float(ts.split("@")[1]) if "@" in ts else float(ts)
        s = skia.Surface(W, H); cv = s.getCanvas(); draw_frame(cv, t, T); subs.draw_subs(cv, subs.cue_at(cues, t))
        fn = f"build/prev/{name}_{len(files)}.png"; s.makeImageSnapshot().save(fn); files.append(fn)
    cols = 2; w, h = 960, 540; rows = (len(files) + cols - 1) // cols
    im = Image.new("RGB", (cols * w, rows * h), "white")
    for i, f in enumerate(files): im.paste(Image.open(f).convert("RGB").resize((w, h)), ((i % cols) * w, (i // cols) * h))
    im.save(f"build/prev/{name}.png"); print("saved", f"build/prev/{name}.png")
