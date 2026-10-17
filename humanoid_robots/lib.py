# -*- coding: utf-8 -*-
"""Skia toolkit for 'The Future of AI' series: blueprint / engineering drawing.
Deep blue sheet, white linework, cyan = what is solved / data, amber = the key number (max 8 per video),
red only for stamps (max 4). Every frame is a pure function of t."""
import math, os
import numpy as np
import skia

W, H = 1920, 1080
HERE = os.path.dirname(os.path.abspath(__file__))
FD = os.path.join(HERE, "assets", "fonts")

BG = 0xFF0E2A47
LINE = 0xFFF4F1EA
CYAN = 0xFF6FD3F7
AMBER = 0xFFFFB547
RED = 0xFFE5484D
PANEL = 0xFF12365A          # slightly lighter blue for cards

MIN_FONT = 36
SAFE = (80, 80, 1840, 790)        # content box; title block lives at x1360-1840,y800-900
SUBZONE_Y = 910

# ---- maths ---------------------------------------------------------------------------------
def clamp(x, a=0.0, b=1.0): return a if x < a else (b if x > b else x)
def prog(t, a, b):
    if b <= a: return 1.0 if t >= a else 0.0
    return clamp((t - a) / (b - a))
def e_out(x): x = clamp(x); return 1 - (1 - x) ** 3
def e_in(x): x = clamp(x); return x ** 3
def e_io(x): x = clamp(x); return 4*x*x*x if x < .5 else 1 - (-2*x + 2) ** 3 / 2
def ap(t, t0, d=0.7): return e_out(prog(t, t0, t0 + d))
def lerp(a, b, x): return a + (b - a) * x
def with_alpha(color, a):
    a = clamp(a); return (int(255 * a) << 24) | (color & 0xFFFFFF)
def mix(c1, c2, x):
    out = 0
    for sh in (24, 16, 8, 0):
        a = (c1 >> sh) & 255; b = (c2 >> sh) & 255
        out |= int(round(a + (b - a) * clamp(x))) << sh
    return out

QA = {"on": False, "log": []}

# ---- fonts ----------------------------------------------------------------------------------
_tf = {}; _fc = {}
FONTS = {"mono": "JetBrainsMono.ttf", "monob": "JetBrainsMonoBold.ttf", "hand": "ArchitectsDaughter.ttf", "sans": "LiberationSans-Bold.ttf"}
def font(kind, size):
    k = (kind, size)
    if k not in _fc:
        if kind not in _tf: _tf[kind] = skia.Typeface.MakeFromFile(os.path.join(FD, FONTS[kind]), 0)
        f = skia.Font(_tf[kind], size); f.setSubpixel(True); _fc[k] = f
    return _fc[k]
def tw(s, kind, size): return font(kind, size).measureText(s)

def P(color=LINE, style="fill", w=1.0, alpha=1.0, cap="round", join="round", blur=0, dash=None):
    p = skia.Paint(AntiAlias=True)
    p.setColor(with_alpha(color, alpha) if alpha < 1.0 else color)
    if style == "stroke":
        p.setStyle(skia.Paint.kStroke_Style); p.setStrokeWidth(w)
        p.setStrokeCap({"round": skia.Paint.kRound_Cap, "butt": skia.Paint.kButt_Cap, "square": skia.Paint.kSquare_Cap}[cap])
        p.setStrokeJoin(skia.Paint.kRound_Join if join == "round" else skia.Paint.kMiter_Join)
    if blur: p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, blur))
    if dash: p.setPathEffect(skia.DashPathEffect.Make(dash, 0))
    return p

def _scale_of(c):
    m = c.getTotalMatrix()
    return math.sqrt(abs(m.getScaleX() * m.getScaleY() - m.getSkewX() * m.getSkewY()))

def text(c, s, x, y, kind="mono", size=36, color=LINE, align="c", alpha=1.0, p=1.0, vcenter=True, deco=False, tag=None, rot=0):
    """y = vertical centre if vcenter else baseline. p = typing progress 0..1 (characters revealed)."""
    if alpha <= 0.01 or p <= 0: return 0
    full = s
    f = font(kind, size); w = f.measureText(full)
    x0 = x - w/2 if align == "c" else (x if align == "l" else x - w)
    by = y + size * 0.34 if vcenter else y
    if QA["on"] and alpha > 0.05 and full.strip():
        m = c.getTotalMatrix()
        pts = [(x0, by - size*0.8), (x0 + w, by - size*0.8), (x0, by + size*0.2), (x0 + w, by + size*0.2)]
        xs, ys = [], []
        for (px, py) in pts:
            if rot:
                a_ = math.radians(rot); dx_, dy_ = px - x, py - y
                px, py = x + dx_ * math.cos(a_) - dy_ * math.sin(a_), y + dx_ * math.sin(a_) + dy_ * math.cos(a_)
            q = m.mapXY(px, py); xs.append(q.fX); ys.append(q.fY)
        QA["log"].append(dict(s=full, size=size * _scale_of(c), x0=min(xs), x1=max(xs), y0=min(ys), y1=max(ys), deco=deco, alpha=alpha, tag=tag))
    show = full if p >= 1 else full[:int(len(full) * p)]
    if rot:
        c.save(); c.rotate(rot, x, y)
    c.drawString(show, x0, by, f, P(color, alpha=alpha))
    if rot: c.restore()
    return w

def wrap(s, kind, size, maxw):
    words = s.split(" "); lines = []; cur = ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if tw(trial, kind, size) <= maxw or not cur: cur = trial
        else: lines.append(cur); cur = w_
    if cur: lines.append(cur)
    return lines

# ---- sheet background -----------------------------------------------------------------------
_bg = None
def bg_image():
    global _bg
    if _bg is None:
        s = skia.Surface(W, H); c = s.getCanvas(); c.clear(BG)
        # soft vignette
        sh = skia.GradientShader.MakeRadial((W/2, H/2), 1250, [with_alpha(0xFFFFFF, 0.05), with_alpha(0x000000, 0.28)], [0.0, 1.0])
        pp = skia.Paint(); pp.setShader(sh); c.drawRect(skia.Rect.MakeWH(W, H), pp)
        for x in range(0, W + 1, 24): c.drawLine(x, 0, x, H, P(LINE, "stroke", 1, 0.05))
        for y in range(0, H + 1, 24): c.drawLine(0, y, W, y, P(LINE, "stroke", 1, 0.05))
        for x in range(0, W + 1, 120): c.drawLine(x, 0, x, H, P(LINE, "stroke", 1.5, 0.08))
        for y in range(0, H + 1, 120): c.drawLine(0, y, W, y, P(LINE, "stroke", 1.5, 0.08))
        # sheet border
        c.drawRect(skia.Rect.MakeXYWH(40, 40, W - 80, H - 80), P(LINE, "stroke", 2, 0.35))
        _bg = s.makeImageSnapshot()
    return _bg

# ---- line primitives -------------------------------------------------------------------------
def plen(pts): return sum(math.hypot(pts[i][0]-pts[i-1][0], pts[i][1]-pts[i-1][1]) for i in range(1, len(pts)))
def cut(pts, p):
    if p >= 1: return pts
    if p <= 0: return []
    target = plen(pts) * p; out = [pts[0]]; acc = 0
    for i in range(1, len(pts)):
        seg = math.hypot(pts[i][0]-pts[i-1][0], pts[i][1]-pts[i-1][1])
        if acc + seg >= target:
            k = (target - acc) / seg if seg else 0
            out.append((lerp(pts[i-1][0], pts[i][0], k), lerp(pts[i-1][1], pts[i][1], k))); return out
        out.append(pts[i]); acc += seg
    return out

def pts_path(pts, close=False):
    path = skia.Path(); path.moveTo(*pts[0])
    for q in pts[1:]: path.lineTo(*q)
    if close: path.close()
    return path

def draw_on(c, pts, p=1.0, w=3, color=LINE, alpha=1.0, close=False, dash=None, cap="round"):
    if close: pts = list(pts) + [pts[0]]
    q = cut(pts, clamp(p))
    if len(q) < 2: return
    c.drawPath(pts_path(q), P(color, "stroke", w, alpha, cap=cap, dash=dash))

def line(c, x0, y0, x1, y1, p=1.0, w=3, color=LINE, alpha=1.0, dash=None): draw_on(c, [(x0, y0), (x1, y1)], p, w, color, alpha, dash=dash)
def rect_pts(x, y, w, h): return [(x, y), (x+w, y), (x+w, y+h), (x, y+h)]
def rect(c, x, y, w, h, p=1.0, lw=3, color=LINE, alpha=1.0, fill=None, falpha=1.0, dash=None):
    if fill is not None and p > 0: c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), P(fill, alpha=falpha * clamp(p * 1.5)))
    draw_on(c, rect_pts(x, y, w, h), p, lw, color, alpha, close=True, dash=dash)
def circ_pts(cx, cy, r, n=64, a0=-math.pi/2, a1=None):
    a1 = a0 + 2*math.pi if a1 is None else a1
    return [(cx + r*math.cos(lerp(a0, a1, i/n)), cy + r*math.sin(lerp(a0, a1, i/n))) for i in range(n + 1)]
def circle(c, cx, cy, r, p=1.0, w=3, color=LINE, alpha=1.0, fill=None, falpha=1.0, dash=None):
    if fill is not None and p > 0: c.drawCircle(cx, cy, r, P(fill, alpha=falpha * clamp(p * 1.5)))
    draw_on(c, circ_pts(cx, cy, r), p, w, color, alpha, dash=dash)
def arc(c, cx, cy, r, a0, a1, p=1.0, w=3, color=LINE, alpha=1.0, dash=None):
    draw_on(c, circ_pts(cx, cy, r, 48, a0, a1), p, w, color, alpha, dash=dash)
def fillpoly(c, pts, color=CYAN, alpha=0.2):
    c.drawPath(pts_path(pts, True), P(color, alpha=alpha))

def hatch(c, pts, spacing=18, ang=-math.pi/4, color=CYAN, alpha=0.8, w=2, p=1.0):
    if p <= 0: return
    c.save(); c.clipPath(pts_path(pts, True), skia.ClipOp.kIntersect, True)
    xs = [q[0] for q in pts]; ys = [q[1] for q in pts]
    R = math.hypot(max(xs) - min(xs), max(ys) - min(ys)); cx = (max(xs) + min(xs)) / 2; cy = (max(ys) + min(ys)) / 2
    ca, sa = math.cos(ang), math.sin(ang); paint = P(color, "stroke", w, alpha * clamp(p)); d = -R
    while d <= R:
        c.drawLine(cx + d*-sa - R*ca, cy + d*ca - R*sa, cx + d*-sa + R*ca, cy + d*ca + R*sa, paint); d += spacing
    c.restore()

def arrowhead(c, x, y, ang, sz=18, w=3, color=LINE, alpha=1.0):
    pts = [(x - sz*math.cos(ang - .45), y - sz*math.sin(ang - .45)), (x, y), (x - sz*math.cos(ang + .45), y - sz*math.sin(ang + .45))]
    c.drawPath(pts_path(pts), P(color, "stroke", w, alpha))
def arrow(c, x0, y0, x1, y1, p=1.0, w=3, color=LINE, alpha=1.0, sz=18, dash=None):
    line(c, x0, y0, x0 + (x1 - x0) * clamp(p), y0 + (y1 - y0) * clamp(p), 1.0, w, color, alpha, dash=dash)
    if p >= 1: arrowhead(c, x1, y1, math.atan2(y1 - y0, x1 - x0), sz, w, color, alpha)
def poly_arrow(c, pts, p=1.0, w=3, color=LINE, alpha=1.0, sz=18, dash=None):
    draw_on(c, pts, p, w, color, alpha, dash=dash)
    if p >= 1: arrowhead(c, pts[-1][0], pts[-1][1], math.atan2(pts[-1][1]-pts[-2][1], pts[-1][0]-pts[-2][0]), sz, w, color, alpha)

def dim(c, x0, y0, x1, y1, label=None, p=1.0, color=LINE, lw=2.5, off=0, size=36, lx=0, ly=-34, alpha=1.0):
    """Engineering dimension line with end ticks and arrowheads."""
    a = math.atan2(y1 - y0, x1 - x0); nx, ny = -math.sin(a), math.cos(a)
    line(c, x0, y0, x1, y1, p, lw, color, alpha)
    if p > 0.05:
        line(c, x0 + nx*16, y0 + ny*16, x0 - nx*16, y0 - ny*16, 1, lw, color, alpha)
        arrowhead(c, x0, y0, a + math.pi, 15, lw, color, alpha)
    if p >= 1:
        line(c, x1 + nx*16, y1 + ny*16, x1 - nx*16, y1 - ny*16, 1, lw, color, alpha)
        arrowhead(c, x1, y1, a, 15, lw, color, alpha)
        if label: text(c, label, (x0+x1)/2 + lx, (y0+y1)/2 + ly, "mono", size, color, "c", alpha)

def check(c, cx, cy, s=40, p=1.0, w=9, color=CYAN, alpha=1.0):
    draw_on(c, [(cx - s*.6, cy), (cx - s*.15, cy + s*.5), (cx + s*.7, cy - s*.55)], p, w, color, alpha)
def cross(c, cx, cy, s=40, p=1.0, w=9, color=RED, alpha=1.0):
    draw_on(c, [(cx - s*.55, cy - s*.55), (cx + s*.55, cy + s*.55)], clamp(p * 2), w, color, alpha)
    if p > .5: draw_on(c, [(cx + s*.55, cy - s*.55), (cx - s*.55, cy + s*.55)], clamp(p * 2 - 1), w, color, alpha)
def infinity(c, cx, cy, s=60, p=1.0, w=6, color=AMBER, alpha=1.0):
    pts = [(cx + s*math.cos(t)/(1 + math.sin(t)**2), cy + s*math.sin(t)*math.cos(t)/(1 + math.sin(t)**2)*1.2) for t in [i/60*2*math.pi for i in range(61)]]
    draw_on(c, pts, p, w, color, alpha)
def qmark(c, cx, cy, size=80, color=AMBER, alpha=1.0): text(c, "?", cx, cy, "monob", size, color, "c", alpha, deco=True)

def fmt(v, dec=0):
    return f"{v:,.{dec}f}"
def roll(v, p, dec=0): return fmt(v * e_out(clamp(p)), dec)

# ---- cards / labels -----------------------------------------------------------------------------
def card(c, x, y, w, h, p=1.0, color=LINE, alpha=1.0, lw=3):
    if p <= 0: return
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), P(PANEL, alpha=0.92 * alpha * clamp(p * 1.4)))
    draw_on(c, rect_pts(x, y, w, h), p, lw, color, alpha, close=True)
    if p >= 1: draw_on(c, rect_pts(x + 9, y + 9, w - 18, h - 18), 1, 1.5, color, alpha * 0.5, close=True)

def label(c, s, x, y, size=36, color=LINE, align="c", alpha=1.0, kind="mono", p=1.0): return text(c, s, x, y, kind, size, color, align, alpha, p)

def source(c, s, x, y, alpha=1.0, align="l", w=None):
    """Source tag: small, but never below 36px so it stays legible on a phone."""
    if alpha <= 0.02: return
    f = font("mono", 36); tw_ = f.measureText(s); x0 = x if align == "l" else (x - tw_ if align == "r" else x - tw_/2)
    c.drawRect(skia.Rect.MakeXYWH(x0 - 14, y - 26, tw_ + 28, 52), P(BG, alpha=0.88 * alpha))
    c.drawLine(x0 - 14, y - 26, x0 - 14, y + 26, P(CYAN, "stroke", 4, alpha))
    text(c, s, x0, y, "mono", 36, CYAN, "l", alpha, tag="src")

def stamp(c, s, cx, cy, t, t0, size=48, rot=-0.12, color=RED):
    k = clamp((t - t0) / 0.28)
    if k <= 0: return
    sc = lerp(2.2, 1, e_out(k)); al = clamp(k * 1.6)
    f = font("monob", size); w = f.measureText(s) + 64; h = size + 44
    c.save(); c.translate(cx, cy); c.rotate(math.degrees(rot)); c.scale(sc, sc)
    c.drawRect(skia.Rect.MakeXYWH(-w/2, -h/2, w, h), P(BG, alpha=0.6 * al))
    c.drawRect(skia.Rect.MakeXYWH(-w/2, -h/2, w, h), P(color, "stroke", 6, al))
    c.drawRect(skia.Rect.MakeXYWH(-w/2 + 12, -h/2 + 12, w - 24, h - 24), P(color, "stroke", 2, al))
    text(c, s, 0, 0, "monob", size, color, "c", al, tag="stamp")
    c.restore()

def titleblock(c, sheet, name, alpha=1.0, final=False):
    x, y, w, h = 1360, 800, 480, 100
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), P(BG, alpha=0.92 * alpha))
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), P(LINE, "stroke", 2.5, alpha))
    c.drawLine(x, y + 50, x + w, y + 50, P(LINE, "stroke", 1.5, alpha * 0.6))
    text(c, "DWG-09 / HUMANOID", x + 16, y + 25, "mono", 36, LINE, "l", alpha, deco=True, tag="tb")
    text(c, "END OF DRAWING" if final else f"SHEET {sheet} — {name}", x + 16, y + 75, "mono", 36, CYAN, "l", alpha, deco=True, tag="tb")

def pulse(c, t, x, y, r0=14, r1=60, period=1.6, color=CYAN, alpha=1.0, n=2, w=3):
    """expanding rings: keeps a settled diagram alive"""
    for k in range(n):
        ph = ((t / period) + k / n) % 1.0
        c.drawCircle(x, y, lerp(r0, r1, ph), P(color, "stroke", w, alpha * (1 - ph) * .8))

def runner(c, t, pts, period=2.4, color=CYAN, alpha=1.0, r=7, trail=3):
    """a dot travelling along a polyline, repeating"""
    L = plen(pts)
    for k in range(trail):
        ph = ((t / period) - k * .035) % 1.0
        q = cut(pts, ph)
        if len(q) >= 2: c.drawCircle(q[-1][0], q[-1][1], r * (1 - k * .25), P(color, alpha=alpha * (1 - k * .3)))
