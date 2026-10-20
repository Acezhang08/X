# -*- coding: utf-8 -*-
"""Programmatic frame QA: font size >= 36, 80px margins, subtitle zone, text-text overlaps."""
import sys, json, itertools
import skia
import lib, render, subs
from lib import *
T = render.load_scenes(); cues = subs.build_cues(T)
surf = skia.Surface(W, H)

def in_transition(t):
    for k, st in T.seg_start.items():
        if k > 0 and st - 0.95 <= t < st - 0.15: return True
    return False

def check(t):
    lib.QA["on"] = True; lib.QA["log"] = []
    render.draw_frame(surf.getCanvas(), t, T)
    subs.draw_subs(surf.getCanvas(), subs.cue_at(cues, t))
    items = [i for i in lib.QA["log"] if i["alpha"] > 0.35]
    probs = []
    trans = in_transition(t)
    for it in items:
        if it["tag"] == "sub":
            continue
        if not it["deco"] and it["size"] < 35.5: probs.append(("SMALL", round(it["size"]), it["s"][:40]))
        if trans: continue
        if it["x0"] < 78 or it["x1"] > 1842: probs.append(("MARGIN-X", round(it["x0"]), round(it["x1"]), it["s"][:40]))
        if it["y0"] < 78: probs.append(("MARGIN-TOP", round(it["y0"]), it["s"][:40]))
        if it["y1"] > 925: probs.append(("SUBZONE", round(it["y1"]), it["s"][:40]))
    if not trans:
        for a, b in itertools.combinations(items, 2):
            if a["tag"] == "sub" or b["tag"] == "sub": continue
            ox = min(a["x1"], b["x1"]) - max(a["x0"], b["x0"]); oy = min(a["y1"], b["y1"]) - max(a["y0"], b["y0"])
            if ox > 12 and oy > 12 and a["s"] != b["s"]:
                probs.append(("OVERLAP", a["s"][:30], b["s"][:30], round(ox), round(oy)))
    lib.QA["on"] = False
    return probs

if __name__ == "__main__":
    step = float(sys.argv[1]) if len(sys.argv) > 1 else 2.0
    t0 = float(sys.argv[2]) if len(sys.argv) > 2 else 0.0
    t1 = float(sys.argv[3]) if len(sys.argv) > 3 else T.duration
    ts = []
    t = t0
    while t < t1: ts.append(round(t, 2)); t += step
    # also scene-change points: each line start + 0.4
    out = {}
    for t in ts:
        p = check(t)
        if p: out[t] = p
    for t, p in out.items():
        print(t, p)
    print("frames checked", len(ts), "with problems", len(out))
