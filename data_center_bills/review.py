# -*- coding: utf-8 -*-
"""Automated review pass on the scene code (draws every segment onto a transparent canvas):
 - edge margin: no ink within 80 px of the frame edge (and nothing below y=925, the subtitle band)
 - empty screens: runs where almost nothing is drawn
 - stale screens: runs with no visible change (rhythm)
usage: review.py edges|empty|stale|all"""
import sys, numpy as np, skia
import render
from lib import W, H
T = render.load_scenes()
FPS = 30
MARGIN = 80

def seg_at(t):
    seg = 0
    for k, st in T.seg_start.items():
        if t >= st - 0.15: seg = k
    return seg

def in_pan(t):
    for k, st in T.seg_start.items():
        if k == 0: continue
        if st - 0.95 <= t < st - 0.15 + 0.01: return True
    return False

_s = skia.Surface(W, H)
def content(t, seg=None):
    c = _s.getCanvas(); c.clear(0x00000000)
    k = seg_at(t) if seg is None else seg
    render.SEGS[k][1](c, t)
    a = _s.makeImageSnapshot().toarray(colorType=skia.kBGRA_8888_ColorType)
    return a

def edges(step=0.5):
    bad = []
    t = 0.0
    while t < T.duration:
        if not in_pan(t):
            a = content(t)[..., 3]
            m = a > 110
            if m.any():
                ys, xs = np.where(m)
                l, r, tp, b = xs.min(), xs.max(), ys.min(), ys.max()
                v = []
                if l < MARGIN: v.append(f"left {l}")
                if r > W - MARGIN: v.append(f"right {W - r}")
                if tp < MARGIN: v.append(f"top {tp}")
                if b > 925: v.append(f"bottom y={b}")
                if v: bad.append((round(t, 2), v))
        t += step
    return bad

def empty(step=0.25, thr=0.004):
    runs = []; start = None; t = 0.0
    while t < T.duration:
        a = content(t)[..., 3] if not in_pan(t) else np.ones((4, 4))
        frac = (a > 40).mean()
        if frac < thr and t > 0.0:
            if start is None: start = t
        else:
            if start is not None and t - start > 1.0: runs.append((round(start, 2), round(t, 2)))
            start = None
        t += step
    return runs

def stale(step=0.5, thr=0.0006, minrun=8.0):
    prev = None; last = 0.0; runs = []; t = 0.0
    while t < T.duration:
        a = content(t)[::8, ::8].astype(np.float32)
        if prev is not None:
            d = np.abs(a - prev).mean() / 255
            if d > thr: last = t
            elif t - last >= minrun and (not runs or runs[-1][0] != round(last, 1)):
                runs.append((round(last, 1), round(t, 1)))
            elif runs and runs[-1][0] == round(last, 1): runs[-1] = (runs[-1][0], round(t, 1))
        prev = a; t += step
    return runs

if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    if what in ("edges", "all"):
        b = edges(); print("EDGE VIOLATIONS", len(b))
        for x in b: print(" ", x)
    if what in ("empty", "all"):
        print("EMPTY RUNS >1s", empty())
    if what in ("stale", "all"):
        print("STALE RUNS", stale())
