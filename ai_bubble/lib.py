# -*- coding: utf-8 -*-
"""Small skia toolkit for the newspaper-collage style ("AI money" series)."""
import math, random, json, os
import re as _re
import numpy as np
import skia
from contextlib import contextmanager

W, H = 1920, 1080
HERE = os.path.dirname(os.path.abspath(__file__))
FD = os.path.join(HERE, "assets", "fonts")

PAPER = 0xFFEFE9DD; PAPER2 = 0xFFF7F2E7
INK = 0xFF1C1C1C; GREEN = 0xFF2F7D4A; RED = 0xFFC23B22; AMBER = 0xFFD99A1E; GRAY = 0xFF8A857C
LGRAY = 0xFFB9B3A6

# ---------------------------------------------------------------- maths
def clamp(x, a=0.0, b=1.0): return a if x < a else (b if x > b else x)
def prog(t, a, b):
    if b <= a: return 1.0 if t >= a else 0.0
    return clamp((t - a) / (b - a))
def e_out(x): x = clamp(x); return 1 - (1 - x) ** 3
def e_in(x): x = clamp(x); return x ** 3
def e_io(x):
    x = clamp(x); return 3*x*x - 2*x*x*x
def e_back(x):
    x = clamp(x); s = 1.5; x -= 1; return x*x*((s+1)*x + s) + 1
def lerp(a, b, x): return a + (b - a) * x
def with_alpha(color, a):
    a = clamp(a); return (int(255*a) << 24) | (color & 0xFFFFFF)
def mix(c1, c2, x):
    out = 0
    for sh in (24, 16, 8, 0):
        a = (c1 >> sh) & 255; b = (c2 >> sh) & 255
        out |= int(round(a + (b-a)*clamp(x))) << sh
    return out

# ---------------------------------------------------------------- fonts
_fc = {}
_tf = {}
def _typeface(kind):
    if kind in _tf: return _tf[kind]
    path, idx = {
        "serif": (f"{FD}/Playfair.ttf", 0),
        "sans": ("/usr/share/fonts/opentype/inter/Inter-Bold.otf", 0),
        "sansr": ("/usr/share/fonts/opentype/inter/Inter-Regular.otf", 0),
        "sanss": ("/usr/share/fonts/opentype/inter/Inter-SemiBold.otf", 0),
        "mono": (f"{FD}/PlexMono-Bold.ttf", 0),
        "monom": (f"{FD}/PlexMono-Medium.ttf", 0),
        "zh": ("/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc", 0),
    }[kind]
    _tf[kind] = skia.Typeface.MakeFromFile(path, idx)
    return _tf[kind]
def font(kind, size):
    k = (kind, size)
    if k not in _fc:
        f = skia.Font(_typeface(kind), size)
        f.setSubpixel(True)
        if kind == "serif": f.setEmbolden(True)
        _fc[k] = f
    return _fc[k]

def P(color=INK, style="fill", w=1.0, alpha=1.0, cap="round", join="round", blur=0, dash=None):
    p = skia.Paint(AntiAlias=True)
    p.setColor(with_alpha(color, alpha) if alpha < 1.0 else color)
    if style == "stroke":
        p.setStyle(skia.Paint.kStroke_Style); p.setStrokeWidth(w)
        p.setStrokeCap({"round": skia.Paint.kRound_Cap, "butt": skia.Paint.kButt_Cap, "square": skia.Paint.kSquare_Cap}[cap])
        p.setStrokeJoin(skia.Paint.kRound_Join if join == "round" else skia.Paint.kMiter_Join)
    if blur: p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, blur))
    if dash: p.setPathEffect(skia.DashPathEffect.Make(dash, 0))
    return p

def tw(s, kind, size):
    if kind == "serif" and _re.search(r"\d", s):
        return sum(font("sans" if _NUM.fullmatch(p) else "serif", size).measureText(p) for p in _NUM.split(s) if p)
    return font(kind, size).measureText(s)

import re as _re
_NUM = _re.compile(r"([\$≈><×~]?\d[\d.,]*[A-Za-z%]*|[×≈≠<>↔→])")
def text(c, s, x, y, kind="sans", size=40, color=INK, align="c", alpha=1.0, spacing=0, vcenter=True, stroke=None):
    """Draw text. y is the vertical centre (cap-height centre) when vcenter else the baseline.
    Playfair has old-style figures, so digit runs inside serif text are set in Inter Bold."""
    if kind == "serif" and not spacing and _re.search(r"\d", s):
        parts = [p for p in _NUM.split(s) if p != ""]
        fs = [(font("sans" if _NUM.fullmatch(p) else "serif", size), p) for p in parts]
        w = sum(f.measureText(p) for f, p in fs)
        x0 = x - w/2 if align == "c" else (x if align == "l" else x - w)
        by = y + size*0.36 if vcenter else y
        for f, p in fs:
            if stroke: c.drawString(p, x0, by, f, P(stroke[0], "stroke", stroke[1], alpha))
            c.drawString(p, x0, by, f, P(color, alpha=alpha)); x0 += f.measureText(p)
        return w
    f = font(kind, size)
    if spacing:
        w = sum(f.measureText(ch) for ch in s) + spacing*(len(s)-1)
    else:
        w = f.measureText(s)
    x0 = x - w/2 if align == "c" else (x if align == "l" else x - w)
    by = y + size*0.36 if vcenter else y
    paints = []
    if stroke: paints.append(P(stroke[0], "stroke", stroke[1], alpha))
    paints.append(P(color, alpha=alpha))
    for p in paints:
        if spacing:
            xx = x0
            for ch in s:
                c.drawString(ch, xx, by, f, p); xx += f.measureText(ch) + spacing
        else:
            c.drawString(s, x0, by, f, p)
    return w

def wrap(s, kind, size, maxw):
    words = s.split(" "); lines = []; cur = ""
    for w in words:
        trial = (cur + " " + w).strip()
        if tw(trial, kind, size) <= maxw or not cur: cur = trial
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

# ---------------------------------------------------------------- paper
def make_paper(seed=7):
    rng = np.random.default_rng(seed)
    base = np.array([0xEF, 0xE9, 0xDD], dtype=np.float32)
    img = np.ones((H, W, 3), dtype=np.float32) * base
    # low-frequency mottling
    lo = rng.normal(0, 1, (H//90+2, W//90+2)).astype(np.float32)
    lo = np.kron(lo, np.ones((90, 90), dtype=np.float32))[:H, :W]
    from scipy.ndimage import gaussian_filter
    lo = gaussian_filter(lo, 45)
    img += (lo[..., None] * 5.5)
    # medium blotches
    md = gaussian_filter(rng.normal(0, 1, (H, W)).astype(np.float32), 6)
    img += md[..., None] * 9
    # fine grain
    img += rng.normal(0, 2.2, (H, W, 1)).astype(np.float32)
    # fibres: short thin curved strokes
    surf = skia.Surface(W, H); cv = surf.getCanvas(); cv.clear(0x00000000)
    r = random.Random(seed)
    for i in range(2600):
        x, y = r.uniform(0, W), r.uniform(0, H); L = r.uniform(8, 38); a = r.uniform(0, math.pi)
        path = skia.Path(); path.moveTo(x, y)
        path.quadTo(x + math.cos(a)*L*0.5 + r.uniform(-4, 4), y + math.sin(a)*L*0.5 + r.uniform(-4, 4),
                    x + math.cos(a)*L, y + math.sin(a)*L)
        dark = r.random() < 0.55
        p = P(0x6B5E48 if dark else 0xFFFFFF, "stroke", r.uniform(0.5, 1.1), r.uniform(0.05, 0.16) if dark else r.uniform(0.12, 0.3))
        cv.drawPath(path, p)
    fib = surf.makeImageSnapshot().toarray()  # BGRA premul
    fa = fib[..., 3:4].astype(np.float32) / 255
    fc = fib[..., [2, 1, 0]].astype(np.float32)
    img = img * (1 - fa) + fc * fa
    # vignette
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.sqrt(((xx - W/2)/(W/2))**2 + ((yy - H/2)/(H/2))**2)
    img *= (1 - 0.06 * np.clip(d - 0.55, 0, 1.2) ** 1.5)[..., None]
    img = np.clip(img, 0, 255).astype(np.uint8)
    rgba = np.dstack([img, np.full((H, W), 255, np.uint8)])
    return skia.Image.fromarray(np.ascontiguousarray(rgba), colorType=skia.kRGBA_8888_ColorType)

_paper = None
def paper_image():
    global _paper
    if _paper is None: _paper = make_paper()
    return _paper

# faint world-attached scraps so camera pans read as movement
_scraps = None
def wall_scraps(c, ox=0.0, oy=0.0, tone=0.0):
    """Periodic (in x, every 1920) set of faint old paste-up scraps. ox/oy = camera offset."""
    global _scraps
    if _scraps is None:
        r = random.Random(11); _scraps = []
        for i in range(18):
            _scraps.append((r.uniform(0, W), r.uniform(-300, 1400), r.uniform(90, 260), r.uniform(60, 170), r.uniform(-4, 4), r.random()))
    for (x, y, w, h, rot, k) in _scraps:
        for rep in (-1, 0, 1):
            xx = (x - ox) % W + rep*W; yy = y - oy*1.0
            if xx < -300 or xx > W+300 or yy < -200 or yy > H+200: continue
            c.save(); c.translate(xx, yy); c.rotate(rot)
            c.drawRect(skia.Rect.MakeXYWH(-w/2, -h/2, w, h), P(0xD9D2C2, alpha=0.35))
            c.drawRect(skia.Rect.MakeXYWH(-w/2, -h/2, w, h), P(0xB5AE9E, "stroke", 1.5, 0.35))
            if k > 0.5:
                for j in range(3): c.drawLine(-w/2+14, -h/2+22+j*18, w/2-14-j*30, -h/2+22+j*18, P(0xB5AE9E, "stroke", 3, 0.35))
            c.restore()

# ---------------------------------------------------------------- torn paper
_torn = {}
def torn_path(w, h, seed=1, amp=3.2, step=15):
    k = (int(w), int(h), seed)
    if k in _torn: return _torn[k]
    r = random.Random(seed)
    p = skia.Path()
    x0, y0, x1, y1 = -w/2, -h/2, w/2, h/2
    pts = []
    def edge(ax, ay, bx, by):
        n = max(2, int(math.hypot(bx-ax, by-ay)/step))
        for i in range(n):
            f = i/n
            nx, ny = -(by-ay), (bx-ax); L = math.hypot(nx, ny) or 1
            j = r.uniform(-amp, amp)
            pts.append((ax+(bx-ax)*f + nx/L*j, ay+(by-ay)*f + ny/L*j))
    edge(x0, y0, x1, y0); edge(x1, y0, x1, y1); edge(x1, y1, x0, y1); edge(x0, y1, x0, y0)
    p.moveTo(*pts[0])
    for q in pts[1:]: p.lineTo(*q)
    p.close()
    _torn[k] = p
    return p

@contextmanager
def card(c, cx, cy, w, h, rot, t, a, b=None, seed=1, fill=PAPER2, tape=True, tint=None, pulse=None, slide=None):
    """Torn newspaper-style clipping that is 'pasted' at time a and 'peeled' at time b.
    Yields True when visible (local coords: origin at the card centre)."""
    if t < a or (b is not None and t > b + 0.6):
        c.save(); c.clipRect(skia.Rect.MakeWH(0, 0))
        try: yield False
        finally: c.restore()
        return
    pin = e_back(prog(t, a, a + 0.38))
    alpha = e_out(prog(t, a, a + 0.22))
    sc = 1 + 0.14 * (1 - pin)
    dy = 0.0; dx = 0.0; rr = rot
    if b is not None and t > b:
        q = e_in(prog(t, b, b + 0.55))
        alpha *= (1 - q); dy = -110*q; dx = 40*q; rr = rot + 7*q; sc *= 1 + 0.05*q
    if pulse:
        pa, pb, ps = pulse
        if pa <= t <= pb:
            sc *= 1 + ps * math.sin(math.pi * prog(t, pa, pb))
    if slide:
        s_a, s_b, ox, oy = slide
        q = e_io(prog(t, s_a, s_b)); dx += ox*q; dy += oy*q
    c.save()
    c.translate(cx + dx, cy + dy); c.rotate(rr); c.scale(sc, sc)
    layered = alpha < 0.995
    if layered:
        c.saveLayerAlpha(skia.Rect.MakeXYWH(-w/2-60, -h/2-60, w+120, h+120), int(255*alpha))
    sh = 6 + 14 * (1 - pin)
    path = torn_path(w, h, seed)
    c.save(); c.translate(sh*0.5, sh)
    c.drawPath(path, P(0x2A2418, alpha=0.30, blur=sh*0.8)); c.restore()
    c.drawPath(path, P(fill))
    c.drawPath(path, P(0x9A9282, "stroke", 1.6, 0.8))
    if tint: c.drawPath(path, P(tint, alpha=0.12))
    if tape:
        for sx in (-1, 1):
            c.save(); c.translate(sx*(w/2 - 38), -h/2 + 8); c.rotate(sx*-0.55)
            c.drawRect(skia.Rect.MakeXYWH(-34, -13, 68, 26), P(0xE6D79A, alpha=0.78))
            c.drawRect(skia.Rect.MakeXYWH(-34, -13, 68, 26), P(0xB8A860, "stroke", 1, 0.6))
            c.restore()
    try:
        yield True
    finally:
        if layered: c.restore()
        c.restore()

def source_line(c, s, x, y, w=None, color=GRAY, align="l"):
    text(c, s, x, y, "sansr", 32, color, align)

def headline(c, s, x, y, size=46, color=INK, maxw=None, lh=1.12):
    lines = wrap(s, "serif", size, maxw) if maxw else [s]
    y0 = y - (len(lines)-1)*size*lh/2
    for i, ln in enumerate(lines):
        text(c, ln, x, y0 + i*size*lh, "serif", size, color)
    return len(lines)

# ---------------------------------------------------------------- stamps / labels
def stamp(c, s, cx, cy, t, a, color=INK, rot=-2.0, size=44, b=None, fill=None, spacing=3, pad=(34, 20), alpha_max=0.95, slam=1.7, font_kind="mono", sub=None):
    """Rubber-stamp style label. Returns (w,h) so callers can attach arrows."""
    f = font(font_kind, size)
    tw_ = sum(f.measureText(ch) for ch in s) + spacing*(len(s)-1)
    w = tw_ + pad[0]*2; h = size + pad[1]*2
    if t < a or (b is not None and t > b + 0.4): return (w, h)
    q = prog(t, a, a + 0.2)
    sc = lerp(slam, 1.0, e_out(q)) if q < 1 else 1.0
    al = e_out(prog(t, a, a + 0.12)) * alpha_max
    if b is not None and t > b: al *= 1 - prog(t, b, b + 0.4)
    c.save(); c.translate(cx, cy); c.rotate(rot); c.scale(sc, sc)
    c.saveLayerAlpha(skia.Rect.MakeXYWH(-w/2-20, -h/2-20, w+40, h+40), int(255*al))
    if fill is not None:
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-w/2, -h/2, w, h), 10, 10), P(fill))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-w/2, -h/2, w, h), 10, 10), P(color, "stroke", 5))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-w/2+8, -h/2+8, w-16, h-16), 6, 6), P(color, "stroke", 1.8))
    tc = color if fill is None else PAPER2
    text(c, s, 0, 0, font_kind, size, tc, "c", 1.0, spacing)
    c.restore(); c.restore()
    return (w, h)

def tag(c, s, cx, cy, t, a, color=INK, size=36, kind="sans", b=None, fill=PAPER2, alpha=1.0, rot=0):
    f = font(kind, size); w = f.measureText(s) + 36; h = size + 22
    if t < a or (b is not None and t > b): return (w, h)
    al = e_out(prog(t, a, a + 0.25)) * alpha
    c.save(); c.translate(cx, cy); c.rotate(rot)
    c.saveLayerAlpha(skia.Rect.MakeXYWH(-w/2-10, -h/2-10, w+20, h+20), int(255*al))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-w/2, -h/2, w, h), 9, 9), P(fill))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-w/2, -h/2, w, h), 9, 9), P(color, "stroke", 2.5))
    text(c, s, 0, 0, kind, size, color)
    c.restore(); c.restore()
    return (w, h)

def fade_text(c, s, x, y, t, a, kind="sans", size=40, color=INK, align="c", b=None, dur=0.3, spacing=0, rise=10, stroke=None):
    if t < a or (b is not None and t > b + dur): return
    al = e_out(prog(t, a, a + dur))
    if b is not None and t > b: al *= 1 - prog(t, b, b + dur)
    text(c, s, x, y + rise*(1 - e_out(prog(t, a, a + dur))), kind, size, color, align, al, spacing, stroke=stroke)

# ---------------------------------------------------------------- arrows
def bez(p0, p1, p2, p3=None):
    path = skia.Path(); path.moveTo(*p0)
    if p3 is None: path.quadTo(*p1, *p2)
    else: path.cubicTo(*p1, *p2, *p3)
    return path

def partial(path, f0, f1):
    pm = skia.PathMeasure(path, False); L = pm.getLength()
    out = skia.Path(); pm.getSegment(L*f0, L*f1, out, True)
    return out, pm, L

def arrow(c, path, p, color=GREEN, w=11, head=True, dashed=None, alpha=1.0, head_size=None, f0=0.0, pen=False):
    """Draw path progressively (0..1) with an arrow head at the leading end."""
    p = clamp(p)
    if p <= 0.001: return
    seg, pm, L = partial(path, f0, max(f0+0.0001, p))
    pp = P(color, "stroke", w, alpha, dash=dashed)
    if pen: pp.setPathEffect(skia.DiscretePathEffect.Make(18, 1.6, 3))
    c.drawPath(seg, pp)
    if head and p > 0.04:
        hs = head_size or w*2.6
        ok = pm.getPosTan(L*p)
        if ok:
            pos, tan = ok
            ang = math.atan2(tan.fY, tan.fX)
            hp = skia.Path()
            hp.moveTo(pos.fX, pos.fY)
            hp.lineTo(pos.fX - hs*math.cos(ang - 0.45), pos.fY - hs*math.sin(ang - 0.45))
            hp.lineTo(pos.fX - hs*0.72*math.cos(ang), pos.fY - hs*0.72*math.sin(ang))
            hp.lineTo(pos.fX - hs*math.cos(ang + 0.45), pos.fY - hs*math.sin(ang + 0.45))
            hp.close()
            c.drawPath(hp, P(color, alpha=alpha))

def pos_on(path, f):
    pm = skia.PathMeasure(path, False); L = pm.getLength()
    ok = pm.getPosTan(L*clamp(f, 0, 1))
    pos, tan = ok
    return pos.fX, pos.fY, math.degrees(math.atan2(tan.fY, tan.fX))

def pen_ellipse(c, cx, cy, rx, ry, p, color=RED, w=7, seed=2, alpha=1.0, rot=-6):
    """Hand-drawn red-pen loop around something."""
    if p <= 0: return
    r = random.Random(seed)
    pts = []
    n = 60
    start = r.uniform(-2.7, -2.2)
    for i in range(n+1):
        th = start + i/n * (math.pi*2*1.08)
        k = 1 + 0.03*math.sin(th*3+seed) + (i/n)*0.07
        pts.append((rx*k*math.cos(th), ry*k*math.sin(th)))
    path = skia.Path(); path.moveTo(*pts[0])
    for q in pts[1:]: path.lineTo(*q)
    seg, pm, L = partial(path, 0, clamp(p))
    c.save(); c.translate(cx, cy); c.rotate(rot)
    c.drawPath(seg, P(color, "stroke", w, alpha))
    c.restore()

def pen_line(c, x0, y0, x1, y1, p, color=RED, w=7, alpha=1.0, wob=3.0, seed=1):
    if p <= 0: return
    path = skia.Path(); path.moveTo(x0, y0)
    n = 10
    r = random.Random(seed)
    for i in range(1, n+1):
        f = i/n
        path.lineTo(lerp(x0, x1, f) + r.uniform(-1, 1)*wob*(i < n), lerp(y0, y1, f) + r.uniform(-1, 1)*wob*(i < n))
    seg, _, _ = partial(path, 0, clamp(p))
    c.drawPath(seg, P(color, "stroke", w, alpha))

def cross_out(c, x0, y0, x1, y1, t, a, color=RED, w=8, dur=0.3):
    pen_line(c, x0, y0, x1, y1, prog(t, a, a + dur), color, w)

# ---------------------------------------------------------------- icons (line art)
def bill(c, x, y, rot=0, s=1.0, alpha=1.0, color=GREEN):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    if alpha < 1: c.saveLayerAlpha(skia.Rect.MakeXYWH(-120, -70, 240, 140), int(255*alpha))
    c.save(); c.translate(3, 6); c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-80, -40, 160, 80), 8, 8), P(0x2A2418, alpha=0.25, blur=4)); c.restore()
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-80, -40, 160, 80), 8, 8), P(mix(PAPER2, color, 0.18)))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-80, -40, 160, 80), 8, 8), P(color, "stroke", 4))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-68, -28, 136, 56), 5, 5), P(color, "stroke", 1.6))
    c.drawCircle(0, 0, 21, P(color, "stroke", 3))
    text(c, "$", 0, 0, "mono", 32, color)
    for sx in (-1, 1):
        c.drawCircle(sx*50, 0, 5, P(color, "stroke", 2))
    if alpha < 1: c.restore()
    c.restore()

def chip(c, x, y, s=1.0, color=INK, alpha=1.0, pins=5):
    c.save(); c.translate(x, y); c.scale(s, s)
    a = alpha
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-50, -50, 100, 100), 10, 10), P(PAPER2, alpha=a))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-50, -50, 100, 100), 10, 10), P(color, "stroke", 5, a))
    c.drawRect(skia.Rect.MakeXYWH(-24, -24, 48, 48), P(color, "stroke", 3.5, a))
    for i in range(pins):
        o = -36 + i*72/(pins-1)
        for (x0, y0, x1, y1) in ((o, -50, o, -68), (o, 50, o, 68), (-50, o, -68, o), (50, o, 68, o)):
            c.drawLine(x0, y0, x1, y1, P(color, "stroke", 4, a))
    c.restore()

def building(c, x, y, s=1.0, color=INK, alpha=1.0, wires=False, win_color=None, rows=3, cols=6):
    """Low data-center shed. (x,y) = bottom centre."""
    c.save(); c.translate(x, y); c.scale(s, s)
    w, h = 300, 130
    c.drawRect(skia.Rect.MakeXYWH(-w/2, -h, w, h), P(PAPER2, alpha=alpha))
    c.drawRect(skia.Rect.MakeXYWH(-w/2, -h, w, h), P(color, "stroke", 5, alpha))
    c.drawLine(-w/2-8, -h, w/2+8, -h, P(color, "stroke", 7, alpha))
    for r_ in range(rows):
        for k in range(cols):
            wx = -w/2 + 24 + k*(w-48)/(cols-1) - 14
            wy = -h + 18 + r_*30
            c.drawRect(skia.Rect.MakeXYWH(wx, wy, 28, 16), P(win_color or color, "stroke", 2.5, alpha))
    c.drawRect(skia.Rect.MakeXYWH(-24, -44, 48, 44), P(color, "stroke", 4, alpha))
    # cooling units
    for sx in (-1, 1):
        c.drawCircle(sx*(w/2-40), -h-18, 18, P(color, "stroke", 4, alpha))
        c.drawLine(sx*(w/2-40)-12, -h-18, sx*(w/2-40)+12, -h-18, P(color, "stroke", 3, alpha))
    c.restore()

def pylon(c, x, y, s=1.0, color=INK, alpha=1.0):
    """Transmission tower; (x,y) = bottom centre."""
    c.save(); c.translate(x, y); c.scale(s, s)
    p = P(color, "stroke", 5, alpha)
    c.drawLine(-50, 0, -10, -200, p); c.drawLine(50, 0, 10, -200, p)
    c.drawLine(-10, -200, 0, -230, p); c.drawLine(10, -200, 0, -230, p)
    for yy, ww in ((-40, 42), (-100, 30), (-160, 18)):
        c.drawLine(-ww, yy, ww, yy, p)
    c.drawLine(-42, -40, 30, -100, P(color, "stroke", 3, alpha)); c.drawLine(42, -40, -30, -100, P(color, "stroke", 3, alpha))
    c.drawLine(-30, -100, 18, -160, P(color, "stroke", 3, alpha)); c.drawLine(30, -100, -18, -160, P(color, "stroke", 3, alpha))
    for yy, ww in ((-180, 80), (-130, 66)):
        c.drawLine(-ww, yy, ww, yy, p)
        for sx in (-1, 1): c.drawLine(sx*ww, yy, sx*ww, yy+20, P(color, "stroke", 3.5, alpha))
    c.restore()

def plug(c, x, y, s=1.0, color=INK, alpha=1.0, rot=0, cord=True):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-34, -30, 68, 60), 12, 12), P(PAPER2, alpha=alpha))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-34, -30, 68, 60), 12, 12), P(color, "stroke", 5, alpha))
    c.drawLine(-14, -30, -14, -56, P(color, "stroke", 8, alpha)); c.drawLine(14, -30, 14, -56, P(color, "stroke", 8, alpha))
    if cord:
        pth = skia.Path(); pth.moveTo(0, 30); pth.cubicTo(0, 80, 40, 70, 40, 120)
        c.drawPath(pth, P(color, "stroke", 6, alpha))
    c.restore()

def gpu(c, x, y, s=1.0, color=INK, alpha=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-70, -34, 140, 68), 6, 6), P(PAPER2, alpha=alpha))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-70, -34, 140, 68), 6, 6), P(color, "stroke", 4.5, alpha))
    for sx in (-28, 28):
        c.drawCircle(sx, 0, 22, P(color, "stroke", 3.5, alpha))
        for k in range(3):
            a = k*math.pi/3
            c.drawLine(sx-18*math.cos(a), -18*math.sin(a), sx+18*math.cos(a), 18*math.sin(a), P(color, "stroke", 2.5, alpha))
    for i in range(7):
        c.drawLine(-56+i*18, 34, -56+i*18, 46, P(color, "stroke", 3, alpha))
    c.restore()

def server(c, x, y, s=1.0, color=INK, alpha=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    for i in range(3):
        yy = -60 + i*42
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-60, yy, 120, 36), 5, 5), P(PAPER2, alpha=alpha))
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-60, yy, 120, 36), 5, 5), P(color, "stroke", 4.5, alpha))
        c.drawCircle(-40, yy+18, 5, P(color, alpha=alpha))
        c.drawLine(-20, yy+18, 40, yy+18, P(color, "stroke", 3, alpha))
    c.restore()

def ledger(c, x, y, s=1.0, color=INK, alpha=1.0, title=None, cols=("ASSETS", "DEBT"), rows=5, hl_col=None):
    """Open account book. Centre (x,y), 360x240 at s=1."""
    c.save(); c.translate(x, y); c.scale(s, s)
    for sx in (-1, 1):
        pth = skia.Path(); pth.moveTo(0, -110)
        pth.lineTo(sx*175, -100); pth.lineTo(sx*175, 105); pth.lineTo(0, 115); pth.close()
        c.drawPath(pth, P(PAPER2, alpha=alpha)); c.drawPath(pth, P(color, "stroke", 4.5, alpha))
    c.drawLine(0, -110, 0, 115, P(color, "stroke", 4.5, alpha))
    for i in range(rows):
        yy = -50 + i*30
        for sx in (-1, 1):
            c.drawLine(sx*14, yy, sx*160, yy+ (2 if sx > 0 else 0)*0, P(color, "stroke", 1.8, 0.45*alpha))
    c.restore()

def silhouette(c, cx, cy, s, t, a, name, name_size=34, b=None, color=INK):
    if t < a or (b is not None and t > b + 0.4): return
    al = e_out(prog(t, a, a + 0.4))
    if b is not None and t > b: al *= 1 - prog(t, b, b + 0.4)
    c.save(); c.translate(cx, cy + 16*(1-al)); c.scale(s, s)
    c.saveLayerAlpha(skia.Rect.MakeXYWH(-200, -230, 400, 400), int(255*al))
    c.drawCircle(0, -90, 52, P(color))
    pth = skia.Path(); pth.moveTo(-120, 90); pth.cubicTo(-120, 0, -70, -20, -30, -25); pth.lineTo(30, -25)
    pth.cubicTo(70, -20, 120, 0, 120, 90); pth.close()
    c.drawPath(pth, P(color))
    c.restore(); c.restore()
    tag(c, name, cx, cy + 90*s + 56, t, a + 0.15, color, name_size, "sans")

# search box ----------------------------------------------------------
def search_box(c, cx, cy, w, h, typed, t, a, b=None, cursor_t=0.0, text_color=INK, size=56, strike=None):
    if t < a or (b is not None and t > b + 0.5): return
    al = e_out(prog(t, a, a + 0.3))
    if b is not None and t > b: al *= 1 - prog(t, b, b + 0.5)
    c.save(); c.translate(cx, cy)
    c.saveLayerAlpha(skia.Rect.MakeXYWH(-w/2-30, -h/2-30, w+60, h+60), int(255*al))
    c.save(); c.translate(0, 8); c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-w/2, -h/2, w, h), h/2, h/2), P(0x2A2418, alpha=0.25, blur=10)); c.restore()
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-w/2, -h/2, w, h), h/2, h/2), P(0xFFFFFCF5))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-w/2, -h/2, w, h), h/2, h/2), P(INK, "stroke", 3.5))
    mx = -w/2 + 62
    c.drawCircle(mx, -4, 17, P(INK, "stroke", 5)); c.drawLine(mx+12, 8, mx+28, 24, P(INK, "stroke", 6))
    tx = -w/2 + 120
    wdt = text(c, typed, tx, 0, "sanss", size, text_color, "l")
    if strike:
        cross_out(c, tx - 6, 2, tx + wdt + 6, -2, t, strike, RED, 8, 0.35)
    if int((t - cursor_t) * 2) % 2 == 0:
        c.drawRect(skia.Rect.MakeXYWH(tx + wdt + 6, -h/2 + 20, 5, h - 40), P(INK))
    c.restore(); c.restore()

def typed_str(s, t, a, dur):
    n = int(len(s) * e_io(prog(t, a, a + dur)) + 0.0001)
    return s[:n]

def roll(t, a, dur, v0, v1):
    return lerp(v0, v1, e_out(prog(t, a, a + dur)))

# bars ------------------------------------------------------------------
def bar(c, cx, base, w, hfull, p, color=GREEN, alpha=1.0, hatch=False, dashed=False):
    h = hfull * p
    if h < 1: return
    r = skia.Rect.MakeXYWH(cx - w/2, base - h, w, h)
    if dashed:
        c.drawRect(r, P(color, alpha=0.18*alpha)); c.drawRect(r, P(color, "stroke", 5, alpha, dash=[18, 12]))
    else:
        c.drawRect(r, P(color, alpha=alpha))
        c.drawRect(r, P(INK, "stroke", 3, 0.8*alpha))
    if hatch:
        c.save(); c.clipRect(r)
        for k in range(-int(h), int(w) + 40, 26):
            c.drawLine(cx - w/2 + k, base, cx - w/2 + k + h, base - h, P(PAPER2, "stroke", 6, 0.9))
        c.restore()

def baseline(c, x0, x1, y, color=INK, alpha=0.8):
    c.drawLine(x0, y, x1, y, P(color, "stroke", 4, alpha))

# loop diagram -----------------------------------------------------------
LOOP_NV = (430, 470); LOOP_OA = (1490, 470)
def loop_paths():
    top = bez((650, 420), (960, 215), (1270, 420))
    bot = bez((1270, 525), (960, 770), (650, 525))
    return top, bot


@contextmanager
def fade(c, t, a=None, b=None, dur=0.35, dy=0.0, bounds=None):
    """Alpha-fade wrapper: visible from a (fade in) to b (fade out). Yields alpha>0 flag."""
    al = 1.0
    hidden = (a is not None and t < a) or (b is not None and t > b + dur)
    if hidden:
        c.save(); c.clipRect(skia.Rect.MakeWH(0, 0))
        try: yield False
        finally: c.restore()
        return
    if a is not None:
        al *= e_out(prog(t, a, a + dur))
    if b is not None:
        al *= 1 - e_in(prog(t, b, b + dur))
    off = 0.0
    if dy:
        if a is not None: off += dy * (1 - e_out(prog(t, a, a + dur)))
        if b is not None: off += -dy * e_in(prog(t, b, b + dur))
    c.save(); c.translate(0, off)
    layer = al < 0.995
    if layer: c.saveLayerAlpha(bounds, int(255*clamp(al)))
    try: yield True
    finally:
        if layer: c.restore()
        c.restore()

def vignette_tone(c, amount, color=0xFFC9B07A):
    if amount <= 0.001: return
    c.drawRect(skia.Rect.MakeWH(W, H), P(color, alpha=0.30*amount))

def hatch_rect(c, x, y, w, h, color=RED, gap=22, lw=5, alpha=1.0):
    c.save(); c.clipRect(skia.Rect.MakeXYWH(x, y, w, h))
    k = -h
    while k < w + h:
        c.drawLine(x + k, y + h, x + k + h, y, P(color, "stroke", lw, alpha)); k += gap
    c.restore()
