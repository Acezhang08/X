# -*- coding: utf-8 -*-
"""Shared helpers for the data-center-bills scenes (newspaper collage, 'AI money' series)."""
import math, random
import skia
from lib import *
from timeline import Timeline

T = Timeline()
S = T.s; E = T.e; Wd = T.w

VERM = 0xFFD9341F          # vermilion: the key number colour on dark boards
DARK = 0xFF1F1D1A          # deep ink board for big numbers
CREAM = 0xFFF7F2E7
DKGRAY = 0xFF6F6A60
FULL = skia.Rect.MakeXYWH(-300, -300, W + 600, H + 600)

# --- keep every glyph at >= 36 px (1080p) -------------------------------------
_text = text
def text(c, s, x, y, kind="sans", size=40, *a, **k):
    return _text(c, s, x, y, kind, max(size, 36), *a, **k)

def ph(c, t, a, b=None, dur=0.35, dy=0.0):
    """Scene phase: fades in at a, fades out at b."""
    return fade(c, t, a, b, dur, dy=dy, bounds=FULL)

def board(c, cx, cy, w, h, t, a, b=None, rot=-0.8, seed=5, **k):
    """Dark ink board (for big numbers); torn edge, no tape."""
    return card(c, cx, cy, w, h, rot, t, a, b, seed=seed, fill=DARK, tape=False, **k)

def clip(c, cx, cy, w, h, t, a, b=None, rot=-1.2, seed=3, **k):
    return card(c, cx, cy, w, h, rot, t, a, b, seed=seed, **k)

def src(c, s, x, y, align="l", color=DKGRAY):
    text(c, s, x, y, "sansr", 36, color, align)

def money(v, d=0):
    return ("${:,.%df}" % d).format(v)

def hold_roll(t, a, dur, v0, v1):
    return roll(t, a, dur, v0, v1)

def illustrative(c, x, y, align="r", color=DKGRAY):
    text(c, "illustrative", x, y, "sansr", 36, color, align)

def sil_building(c, x, y, s=1.0, color=INK, alpha=1.0, dashed=False):
    """Data-center silhouette (solid fill) for stamps; (x,y)=bottom centre."""
    c.save(); c.translate(x, y); c.scale(s, s)
    p = P(color, alpha=alpha)
    c.drawRect(skia.Rect.MakeXYWH(-150, -130, 300, 130), p)
    for sx in (-1, 1):
        c.drawCircle(sx*110, -150, 20, P(color, "stroke", 8, alpha))
    for r_ in range(3):
        for k in range(6):
            c.drawRect(skia.Rect.MakeXYWH(-126 + k*42, -112 + r_*30, 26, 14), P(PAPER2, alpha=alpha))
    c.drawRect(skia.Rect.MakeXYWH(-22, -50, 44, 50), P(PAPER2, alpha=alpha))
    c.restore()

def house(c, x, y, s=1.0, color=INK, alpha=1.0, fill=None):
    """Plain house line art; (x,y)=bottom centre."""
    c.save(); c.translate(x, y); c.scale(s, s)
    body = skia.Rect.MakeXYWH(-60, -90, 120, 90)
    if fill is not None: c.drawRect(body, P(fill, alpha=alpha))
    c.drawRect(body, P(color, "stroke", 6, alpha))
    roof = skia.Path(); roof.moveTo(-76, -88); roof.lineTo(0, -156); roof.lineTo(76, -88)
    c.drawPath(roof, P(color, "stroke", 6, alpha))
    c.drawRect(skia.Rect.MakeXYWH(-14, -52, 28, 52), P(color, "stroke", 5, alpha))
    c.restore()

def person(c, x, y, s=1.0, color=INK, alpha=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawCircle(0, -52, 17, P(color, alpha=alpha))
    pth = skia.Path(); pth.moveTo(-26, 0); pth.cubicTo(-26, -30, -14, -36, 0, -36); pth.cubicTo(14, -36, 26, -30, 26, 0); pth.close()
    c.drawPath(pth, P(color, alpha=alpha))
    c.restore()

def flame(c, x, y, s=1.0, color=RED, alpha=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    p = skia.Path(); p.moveTo(0, 0); p.cubicTo(-60, 0, -70, -60, -30, -110); p.cubicTo(-30, -70, -10, -70, 0, -150)
    p.cubicTo(30, -110, 70, -70, 60, -30); p.cubicTo(55, -8, 30, 0, 0, 0); p.close()
    c.drawPath(p, P(color, alpha=0.25*alpha)); c.drawPath(p, P(color, "stroke", 7, alpha))
    c.restore()

# --- 13 states + DC as a tile map (PJM footprint) -----------------------------
TILES = {  # abbreviation: (col, row)
    "MI": (2, 0), "IL": (0, 1), "IN": (1, 1), "OH": (2, 1), "PA": (3, 1), "NJ": (4, 1),
    "KY": (1, 2), "WV": (2, 2), "MD": (3, 2), "DE": (4, 2),
    "VA": (2, 3), "DC": (3, 3), "TN": (1, 4), "NC": (2, 4),
}
def tile_map(c, cx, cy, t, a, step=0.12, size=150, gap=14, lit_color=RED, dur=0.3, order=None):
    """Tile-grid map of the 13 PJM states + DC; tiles light up one after another from time a."""
    cols, rows = 5, 5
    x0 = cx - (cols*size + (cols-1)*gap)/2; y0 = cy - (rows*size + (rows-1)*gap)/2
    keys = order or list(TILES.keys())
    for i, k in enumerate(keys):
        col, row = TILES[k]
        x = x0 + col*(size+gap); y = y0 + row*(size+gap)
        p = e_out(prog(t, a + i*step, a + i*step + dur))
        r = skia.Rect.MakeXYWH(x, y, size, size)
        rr = skia.RRect.MakeRectXY(r, 12, 12)
        c.drawRRect(rr, P(0xD9D2C2, alpha=0.7))
        c.drawRRect(rr, P(LGRAY, "stroke", 3))
        if p > 0:
            c.save(); c.translate(x + size/2, y + size/2); c.scale(0.8 + 0.2*p, 0.8 + 0.2*p); c.translate(-size/2, -size/2)
            rr2 = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(0, 0, size, size), 12, 12)
            c.drawRRect(rr2, P(lit_color, alpha=p))
            c.drawRRect(rr2, P(INK, "stroke", 4, p))
            text(c, k, size/2, size/2, "mono", 56, CREAM, alpha=p)
            c.restore()
        else:
            text(c, k, x + size/2, y + size/2, "mono", 44, LGRAY)
    return x0, y0
