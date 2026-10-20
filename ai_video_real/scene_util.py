# -*- coding: utf-8 -*-
"""Shared helpers for the AI-video scenes: timing, alpha windows, pixel grids, bar charts.
All visuals are geometric illustrations. No real or AI-generated photos or footage."""
import math, random
import skia
from lib import *
from timeline import Timeline

T = Timeline()

def S(lid): return T.s(lid)
def E(lid): return T.e(lid)

def Ws(lid, phrase, nth=0, after=False):
    """time at which a phrase is spoken inside a line; falls back to the line start"""
    try: return T.w(lid, phrase, nth, after)
    except ValueError: return T.s(lid)

def win(t, a, b, fi=.4, fo=.3):
    """alpha window: fade in from a, fade out ending at b"""
    return ap(t, a, fi) * (1 - e_in(prog(t, b - fo, b)))

def roll_str(t, a, b, end, dec=0):
    """counter that rolls from 0 to end between a and b, then holds the exact final value"""
    return fmt(end * e_out(prog(t, a, b)), dec)

def bar(c, x, y, w, h, frac, color=CYAN, alpha=1.0, p=1.0):
    c.drawRect(skia.Rect.MakeXYWH(x, y, w * clamp(frac) * e_out(clamp(p)), h), P(color, alpha=alpha))

def chip(c, s, x, y, color=CYAN, alpha=1.0, size=36, w=None):
    """rounded label chip (no fill-heavy box, outline + text)"""
    if alpha <= 0.01: return 0
    f = font("mono", size); tw_ = f.measureText(s)
    w = w or tw_ + 36
    c.drawRoundRect(skia.Rect.MakeXYWH(x - w / 2, y - size * .7, w, size * 1.4), 10, 10, P(PANEL, alpha=0.9 * alpha))
    c.drawRoundRect(skia.Rect.MakeXYWH(x - w / 2, y - size * .7, w, size * 1.4), 10, 10, P(color, "stroke", 2.5, alpha))
    text(c, s, x, y, "mono", size, color, "c", alpha)
    return w

# ---- pixel grid used for the denoising and thumbnail illustrations -------------------------------
NOISE_COLS = [0xFF2A2F3A, 0xFF3A4150, 0xFF4A5566, 0xFF6B7080, 0xFF2D4E5C, 0xFF3C6F80]
TGT = {0: 0xFF1F232B, 1: 0xFF58C4DD, 2: 0xFFF5D547, 3: 0xFF2B4F5C}
_arr = {}

def _arrays(cols, rows, seed):
    k = (cols, rows, seed)
    if k not in _arr:
        r = random.Random(seed)
        _arr[k] = ([r.choice(NOISE_COLS) for _ in range(cols * rows)], [r.random() * 0.45 for _ in range(cols * rows)])
    return _arr[k]

def sun_class(col, row, cols, rows, sx=0.0):
    """class map of a simple illustrative scene: sun disc on a dark horizon (not a photo)"""
    cx = cols * 0.5 + sx; cy = rows * 0.42
    d = math.hypot(col + .5 - cx, row + .5 - cy)
    m = min(cols, rows)
    if d < m * 0.10: return 2
    if d < m * 0.32: return 1
    if row > rows * 0.72: return 3
    return 0

def avg_col(cols_):
    r = sum((c >> 16) & 255 for c in cols_) / len(cols_)
    g = sum((c >> 8) & 255 for c in cols_) / len(cols_)
    b = sum(c & 255 for c in cols_) / len(cols_)
    return 0xFF000000 | (int(r) << 16) | (int(g) << 8) | int(b)

def noise_grid(c, s, x0, y0, cw, ch, cols, rows, sx=0.0, seed=3, alpha=1.0, blur=True):
    """denoising illustration: s in [0,1] (0 = pure noise, 1 = clean). Cells settle in random order;
    early on the target is blurred by blending it with its neighbours."""
    nc, dl = _arrays(cols, rows, seed)
    pt = skia.Paint(AntiAlias=False)
    cls = [[sun_class(col, row, cols, rows, sx) for col in range(cols)] for row in range(rows)]
    for row in range(rows):
        for col in range(cols):
            i = row * cols + col
            tgt = TGT[cls[row][col]]
            if blur and s < 0.7:
                nb = []
                for dr in (-1, 0, 1):
                    for dc in (-1, 0, 1):
                        rr, cc = row + dr, col + dc
                        if 0 <= rr < rows and 0 <= cc < cols: nb.append(TGT[cls[rr][cc]])
                tgt = mix(tgt, avg_col(nb), (1 - s / 0.7) * 0.6)
            a = e_out(clamp((s - dl[i]) / 0.55))
            col_ = mix(nc[i], tgt, a)
            pt.setColor(with_alpha(col_, alpha) if alpha < 1 else col_)
            c.drawRect(skia.Rect.MakeXYWH(x0 + col * cw, y0 + row * ch, cw - 1, ch - 1), pt)

def denoise_s(t, a, b):
    """0 before a, ramps with easing to 1 at b"""
    return e_io(prog(t, a, b))
