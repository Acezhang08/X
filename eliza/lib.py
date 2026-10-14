# -*- coding: utf-8 -*-
"""Skia toolkit for the 'AI history' series: aged paper, brown-black ink line art, hatching,
one vermilion accent. Every frame is a pure function of t."""
import math, random, os
import re as _re
import numpy as np
import skia
from contextlib import contextmanager

W, H = 1920, 1080
HERE = os.path.dirname(os.path.abspath(__file__))
FD = os.path.join(HERE, "assets", "fonts")

# --- palette (colour meaning is fixed, see style_ai-history.md) ---------------------------
PAPER = 0xFFE9DCBC      # aged cream paper
PAPER2 = 0xFFF3EAD1     # cards / slips
PAPER3 = 0xFFDCCDA8     # darker scrap
INK = 0xFF2B2118        # brown-black ink
INK2 = 0xFF5A4733       # mid brown (secondary lines, past)
WASH = 0xFF8D7A5F       # faded ink / watercolour wash
LINEL = 0xFFB9A887      # faint guide lines
VERM = 0xFFC9301C       # vermilion: the ONE accent

MIN_FONT = 36           # px at 1080p
SAFE = (80, 80, 1840, 910)   # content safe box (x0,y0,x1,y1); subtitles live below y=910

# --- maths ---------------------------------------------------------------------------------
def clamp(x, a=0.0, b=1.0): return a if x < a else (b if x > b else x)
def prog(t, a, b):
    if b <= a: return 1.0 if t >= a else 0.0
    return clamp((t - a) / (b - a))
def e_out(x): x = clamp(x); return 1 - (1 - x) ** 3
def e_in(x): x = clamp(x); return x ** 3
def e_io(x): x = clamp(x); return 3*x*x - 2*x*x*x
def e_back(x):
    x = clamp(x); s = 1.4; x -= 1; return x*x*((s+1)*x + s) + 1
def lerp(a, b, x): return a + (b - a) * x
def with_alpha(color, a):
    a = clamp(a); return (int(255*a) << 24) | (color & 0xFFFFFF)
def mix(c1, c2, x):
    out = 0
    for sh in (24, 16, 8, 0):
        a = (c1 >> sh) & 255; b = (c2 >> sh) & 255
        out |= int(round(a + (b-a)*clamp(x))) << sh
    return out

# --- QA instrumentation: records every text draw in screen space --------------------------
QA = {"on": False, "log": []}

# --- fonts ----------------------------------------------------------------------------------
_tf = {}; _fc = {}
FONTS = {
    "serif": "FellEnglish.ttf", "serifi": "FellEnglishItalic.ttf", "sc": "FellEnglishSC.ttf",
    "type": "SpecialElite.ttf", "mono": "CourierPrimeBold.ttf", "monor": "CourierPrime.ttf",
    "hand": "CaveatBold.ttf", "kalam": "KalamBold.ttf",
}
def _typeface(kind):
    if kind in _tf: return _tf[kind]
    if kind == "sans": tf = skia.Typeface.MakeFromFile("/usr/share/fonts/opentype/inter/Inter-Bold.otf", 0)
    else: tf = skia.Typeface.MakeFromFile(os.path.join(FD, FONTS[kind]), 0)
    _tf[kind] = tf; return tf
def font(kind, size):
    k = (kind, size)
    if k not in _fc:
        f = skia.Font(_typeface(kind), size); f.setSubpixel(True); _fc[k] = f
    return _fc[k]
def tw(s, kind, size): return font(kind, size).measureText(s)

def P(color=INK, style="fill", w=1.0, alpha=1.0, cap="round", join="round", blur=0, dash=None, rough=None):
    p = skia.Paint(AntiAlias=True)
    p.setColor(with_alpha(color, alpha) if alpha < 1.0 else color)
    if style == "stroke":
        p.setStyle(skia.Paint.kStroke_Style); p.setStrokeWidth(w)
        p.setStrokeCap({"round": skia.Paint.kRound_Cap, "butt": skia.Paint.kButt_Cap, "square": skia.Paint.kSquare_Cap}[cap])
        p.setStrokeJoin(skia.Paint.kRound_Join if join == "round" else skia.Paint.kMiter_Join)
    if blur: p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, blur))
    if dash: p.setPathEffect(skia.DashPathEffect.Make(dash, 0))
    elif rough: p.setPathEffect(skia.DiscretePathEffect.Make(rough[0], rough[1], rough[2] if len(rough) > 2 else 0))
    return p

def _scale_of(c):
    m = c.getTotalMatrix()
    return math.sqrt(abs(m.getScaleX() * m.getScaleY() - m.getSkewX() * m.getSkewY()))

def text(c, s, x, y, kind="serif", size=44, color=INK, align="c", alpha=1.0, spacing=0, vcenter=True,
         stroke=None, deco=False, tag=None):
    """y = vertical centre (cap-height centre) if vcenter else baseline."""
    f = font(kind, size)
    if spacing: w = sum(f.measureText(ch) for ch in s) + spacing*(len(s)-1)
    else: w = f.measureText(s)
    x0 = x - w/2 if align == "c" else (x if align == "l" else x - w)
    by = y + size*0.34 if vcenter else y
    eff = size * _scale_of(c)
    if QA["on"] and alpha > 0.05 and s.strip():
        m = c.getTotalMatrix()
        pts = [(x0, by - size*0.8), (x0 + w, by - size*0.8), (x0, by + size*0.2), (x0 + w, by + size*0.2)]
        xs, ys = [], []
        for (px, py) in pts:
            q = m.mapXY(px, py); xs.append(q.fX); ys.append(q.fY)
        QA["log"].append(dict(s=s, size=eff, x0=min(xs), x1=max(xs), y0=min(ys), y1=max(ys), deco=deco, alpha=alpha, tag=tag))
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
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if tw(trial, kind, size) <= maxw or not cur: cur = trial
        else: lines.append(cur); cur = w_
    if cur: lines.append(cur)
    return lines

# --- paper ----------------------------------------------------------------------------------
def make_paper(seed=5):
    from scipy.ndimage import gaussian_filter
    rng = np.random.default_rng(seed)
    base = np.array([(PAPER >> 16) & 255, (PAPER >> 8) & 255, PAPER & 255], dtype=np.float32)
    img = np.ones((H, W, 3), dtype=np.float32) * base
    lo = rng.normal(0, 1, (H//110+2, W//110+2)).astype(np.float32)
    lo = gaussian_filter(np.kron(lo, np.ones((110, 110), dtype=np.float32))[:H, :W], 55)
    img += lo[..., None] * np.array([7.5, 7.0, 6.0], dtype=np.float32)
    md = gaussian_filter(rng.normal(0, 1, (H, W)).astype(np.float32), 5)
    img += md[..., None] * 9
    img += rng.normal(0, 2.4, (H, W, 1)).astype(np.float32)
    # foxing: small brown age spots
    surf = skia.Surface(W, H); cv = surf.getCanvas(); cv.clear(0)
    r = random.Random(seed)
    for i in range(70):
        x, y, rad = r.uniform(0, W), r.uniform(0, H), r.uniform(3, 15)
        cv.drawCircle(x, y, rad, P(0x8A6A3A, alpha=r.uniform(0.04, 0.12), blur=rad*0.6))
    for i in range(3):   # faint tea-ring stains
        x, y, rad = r.uniform(200, W-200), r.uniform(150, H-150), r.uniform(60, 120)
        cv.drawCircle(x, y, rad, P(0x8A6A3A, "stroke", r.uniform(3, 6), 0.05, blur=3))
    for i in range(2200):  # fibres
        x, y = r.uniform(0, W), r.uniform(0, H); L = r.uniform(8, 36); a = r.uniform(0, math.pi)
        path = skia.Path(); path.moveTo(x, y)
        path.quadTo(x + math.cos(a)*L*0.5 + r.uniform(-4, 4), y + math.sin(a)*L*0.5 + r.uniform(-4, 4), x + math.cos(a)*L, y + math.sin(a)*L)
        dark = r.random() < 0.6
        cv.drawPath(path, P(0x6B5638 if dark else 0xFFFFFF, "stroke", r.uniform(0.5, 1.1), r.uniform(0.05, 0.16) if dark else r.uniform(0.1, 0.25)))
    ov = surf.makeImageSnapshot().toarray()
    fa = ov[..., 3:4].astype(np.float32) / 255
    fc = ov[..., [2, 1, 0]].astype(np.float32)
    img = img * (1 - fa) + fc * fa
    # vignette (stronger, warm-dark corners)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.sqrt(((xx - W/2)/(W/2))**2 + ((yy - H/2)/(H/2))**2)
    v = np.clip(d - 0.5, 0, 1.3) ** 1.6
    img *= (1 - 0.20 * v)[..., None]
    img[..., 2] *= (1 - 0.06 * v)
    img = np.clip(img, 0, 255).astype(np.uint8)
    rgba = np.dstack([img, np.full((H, W), 255, np.uint8)])
    return skia.Image.fromarray(np.ascontiguousarray(rgba), colorType=skia.kRGBA_8888_ColorType)

_paper = None
def paper_image():
    global _paper
    if _paper is None: _paper = make_paper()
    return _paper

_scraps = None
def wall_scraps(c, ox=0.0, oy=0.0, tone=1.0):
    """Faint world-attached old paper scraps / ruled sheets so pans read as movement."""
    global _scraps
    if _scraps is None:
        r = random.Random(21); _scraps = []
        for i in range(20): _scraps.append((r.uniform(0, W), r.uniform(-300, 1400), r.uniform(110, 280), r.uniform(80, 200), r.uniform(-4, 4), r.random()))
    for (x, y, w, h, rot, k) in _scraps:
        for rep in (-1, 0, 1):
            xx = (x - ox) % W + rep*W; yy = y - oy
            if xx < -300 or xx > W+300 or yy < -200 or yy > H+200: continue
            c.save(); c.translate(xx, yy); c.rotate(rot)
            c.drawRect(skia.Rect.MakeXYWH(-w/2, -h/2, w, h), P(PAPER3, alpha=0.28*tone))
            c.drawRect(skia.Rect.MakeXYWH(-w/2, -h/2, w, h), P(LINEL, "stroke", 1.5, 0.35*tone))
            if k > 0.45:
                for j in range(4): c.drawLine(-w/2+14, -h/2+24+j*20, w/2-14-(j % 2)*34, -h/2+24+j*20, P(LINEL, "stroke", 2.5, 0.35*tone))
            c.restore()

# --- ink line toolkit --------------------------------------------------------------------------
def wob(w=3.4, seg=16, dev=1.1): return (seg, dev)

def ink(c, path, w=4.0, color=INK, alpha=1.0, rough=True, fill=None, falpha=1.0):
    """Hand-inked path: slightly wobbly main stroke plus a faint second pass."""
    if fill is not None: c.drawPath(path, P(fill, alpha=falpha))
    c.drawPath(path, P(color, "stroke", w, alpha, rough=(14, 1.3, 7) if rough else None))
    if rough and w >= 3: c.drawPath(path, P(color, "stroke", max(1.2, w*0.35), alpha*0.55, rough=(9, 1.6, 21)))

def line(c, x0, y0, x1, y1, w=4, color=INK, alpha=1.0, rough=True):
    p = skia.Path(); p.moveTo(x0, y0); p.lineTo(x1, y1); ink(c, p, w, color, alpha, rough)

def rect_path(x, y, w, h, r=0):
    p = skia.Path()
    if r: p.addRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w, h), r, r))
    else: p.addRect(skia.Rect.MakeXYWH(x, y, w, h))
    return p

def poly_path(pts, close=True):
    p = skia.Path(); p.moveTo(*pts[0])
    for q in pts[1:]: p.lineTo(*q)
    if close: p.close()
    return p

def hatch(c, clip_path, angle=-45, gap=11, w=2.4, color=INK, alpha=0.7, bounds=None, cross=False, rough=True):
    """Parallel hatching clipped to a path (engraving-style shadow)."""
    c.save(); c.clipPath(clip_path, doAntiAlias=True)
    b = clip_path.getBounds()
    cx, cy = b.centerX(), b.centerY(); R = math.hypot(b.width(), b.height())/2 + 6
    for ang in ([angle, angle + 90] if cross else [angle]):
        c.save(); c.translate(cx, cy); c.rotate(ang)
        k = -R
        while k <= R:
            c.drawLine(-R, k, R, k, P(color, "stroke", w, alpha, rough=(12, 0.9) if rough else None)); k += gap
        c.restore()
    c.restore()

def partial(path, f0, f1):
    pm = skia.PathMeasure(path, False); L = pm.getLength()
    out = skia.Path(); pm.getSegment(L*f0, L*f1, out, True)
    return out, pm, L

def draw_on(c, path, p, w=4.0, color=INK, alpha=1.0, rough=True, head=False, head_size=None):
    """Progressively 'draw' a path (0..1); optional arrow head at the leading end."""
    p = clamp(p)
    if p <= 0.001: return
    seg, pm, L = partial(path, 0.0, max(0.0001, p))
    ink(c, seg, w, color, alpha, rough)
    if head and p > 0.04:
        hs = head_size or w*3.2
        ok = pm.getPosTan(L*p)
        if ok:
            pos, tan = ok; ang = math.atan2(tan.fY, tan.fX)
            hp = skia.Path(); hp.moveTo(pos.fX, pos.fY)
            hp.lineTo(pos.fX - hs*math.cos(ang - 0.42), pos.fY - hs*math.sin(ang - 0.42))
            hp.lineTo(pos.fX - hs*0.7*math.cos(ang), pos.fY - hs*0.7*math.sin(ang))
            hp.lineTo(pos.fX - hs*math.cos(ang + 0.42), pos.fY - hs*math.sin(ang + 0.42)); hp.close()
            c.drawPath(hp, P(color, alpha=alpha))

def bez(p0, p1, p2, p3=None):
    path = skia.Path(); path.moveTo(*p0)
    if p3 is None: path.quadTo(*p1, *p2)
    else: path.cubicTo(*p1, *p2, *p3)
    return path

def pos_on(path, f):
    pm = skia.PathMeasure(path, False); L = pm.getLength()
    pos, tan = pm.getPosTan(L*clamp(f, 0, 1))
    return pos.fX, pos.fY, math.degrees(math.atan2(tan.fY, tan.fX))

# --- visibility wrappers ---------------------------------------------------------------------
@contextmanager
def fade(c, t, a=None, b=None, dur=0.4, dy=0.0, bounds=None, bleed=False):
    """Alpha fade in at a / out at b. bleed=True: 'ink bleeds in' (blurred -> sharp) while fading in."""
    hidden = (a is not None and t < a) or (b is not None and t > b + dur)
    if hidden:
        c.save(); c.clipRect(skia.Rect.MakeWH(0, 0))
        try: yield False
        finally: c.restore()
        return
    al = 1.0; blur = 0.0
    if a is not None:
        q = prog(t, a, a + dur); al *= e_out(q)
        if bleed: blur = max(blur, 14 * (1 - e_out(q)))
    if b is not None:
        al *= 1 - e_in(prog(t, b, b + dur))
    off = 0.0
    if dy:
        if a is not None: off += dy * (1 - e_out(prog(t, a, a + dur)))
        if b is not None: off += -dy * e_in(prog(t, b, b + dur))
    bounds = bounds or skia.Rect.MakeXYWH(-200, -200, W + 400, H + 400)
    c.save(); c.translate(0, off)
    layer = al < 0.995 or blur > 0.3
    if layer:
        paint = skia.Paint(); paint.setAlphaf(clamp(al))
        if blur > 0.3: paint.setImageFilter(skia.ImageFilters.Blur(blur, blur))
        c.saveLayer(bounds, paint)
    try: yield True
    finally:
        if layer: c.restore()
        c.restore()

# --- paper slips -----------------------------------------------------------------------------
_torn = {}
def deckle_path(w, h, seed=1, amp=2.6, step=14):
    k = (int(w), int(h), seed)
    if k in _torn: return _torn[k]
    r = random.Random(seed); pts = []
    x0, y0, x1, y1 = -w/2, -h/2, w/2, h/2
    def edge(ax, ay, bx, by):
        n = max(2, int(math.hypot(bx-ax, by-ay)/step))
        for i in range(n):
            f = i/n; nx, ny = -(by-ay), (bx-ax); L = math.hypot(nx, ny) or 1; j = r.uniform(-amp, amp)
            pts.append((ax+(bx-ax)*f + nx/L*j, ay+(by-ay)*f + ny/L*j))
    edge(x0, y0, x1, y0); edge(x1, y0, x1, y1); edge(x1, y1, x0, y1); edge(x0, y1, x0, y0)
    p = skia.Path(); p.moveTo(*pts[0])
    for q in pts[1:]: p.lineTo(*q)
    p.close(); _torn[k] = p; return p

@contextmanager
def slip(c, cx, cy, w, h, rot, t, a, b=None, seed=1, fill=PAPER2, tape=True, slide=(0, -90), pulse=None, dur=0.55, edge=INK2, lined=False):
    """A paper slip that slides in at a (from offset `slide`) and lifts away at b. Yields True when visible;
    local origin is the slip centre."""
    if t < a or (b is not None and t > b + 0.6):
        c.save(); c.clipRect(skia.Rect.MakeWH(0, 0))
        try: yield False
        finally: c.restore()
        return
    q = prog(t, a, a + dur); pin = e_out(q)
    alpha = e_out(prog(t, a, a + 0.25))
    dx = slide[0] * (1 - pin); dy = slide[1] * (1 - pin); rr = rot + (-3.5 * (1 - pin) if slide != (0, 0) else 0)
    sc = 1.0
    if b is not None and t > b:
        z = e_in(prog(t, b, b + 0.55)); alpha *= (1 - z); dy += -70*z; dx += 30*z; rr += 4*z
    if pulse:
        pa, pb, ps = pulse
        if pa <= t <= pb: sc *= 1 + ps * math.sin(math.pi * prog(t, pa, pb))
    c.save(); c.translate(cx + dx, cy + dy); c.rotate(rr); c.scale(sc, sc)
    layered = alpha < 0.995
    if layered: c.saveLayerAlpha(skia.Rect.MakeXYWH(-w/2-70, -h/2-70, w+140, h+160), int(255*alpha))
    sh = 5 + 12 * (1 - pin)
    path = deckle_path(w, h, seed)
    c.save(); c.translate(sh*0.4, sh); c.drawPath(path, P(0x2A1D10, alpha=0.30, blur=sh*0.8)); c.restore()
    c.drawPath(path, P(fill)); c.drawPath(path, P(edge, "stroke", 1.8, 0.85))
    if lined:
        for yy in range(int(-h/2 + 70), int(h/2 - 20), 44):
            c.drawLine(-w/2 + 24, yy, w/2 - 24, yy, P(LINEL, "stroke", 1.6, 0.55))
    if tape:
        for sx in (-1, 1):
            c.save(); c.translate(sx*(w/2 - 36), -h/2 + 6); c.rotate(sx*-0.5)
            c.drawRect(skia.Rect.MakeXYWH(-32, -12, 64, 24), P(0xFFE0CC8E, alpha=0.7))
            c.drawRect(skia.Rect.MakeXYWH(-32, -12, 64, 24), P(0xFFAE9855, "stroke", 1, 0.55)); c.restore()
    try: yield True
    finally:
        if layered: c.restore()
        c.restore()

def stamp(c, s, cx, cy, t, a, color=VERM, rot=-4, size=48, b=None, spacing=4, pad=(30, 16), alpha_max=0.92, kind="type"):
    """Rubber stamp that slams in (1.6x -> 1x)."""
    f = font(kind, size)
    w = sum(f.measureText(ch) for ch in s) + spacing*(len(s)-1) + pad[0]*2; h = size + pad[1]*2
    if t < a or (b is not None and t > b + 0.4): return (w, h)
    q = prog(t, a, a + 0.18); sc = lerp(1.6, 1.0, e_out(q))
    al = e_out(prog(t, a, a + 0.1)) * alpha_max
    if b is not None and t > b: al *= 1 - prog(t, b, b + 0.4)
    c.save(); c.translate(cx, cy); c.rotate(rot); c.scale(sc, sc)
    c.saveLayerAlpha(skia.Rect.MakeXYWH(-w/2-20, -h/2-20, w+40, h+40), int(255*al))
    rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-w/2, -h/2, w, h), 8, 8)
    c.drawRRect(rr, P(color, "stroke", 5, rough=(10, 1.2)))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-w/2+8, -h/2+8, w-16, h-16), 5, 5), P(color, "stroke", 1.8))
    text(c, s, 0, 0, kind, size, color, "c", 1.0, spacing)
    c.restore(); c.restore()
    return (w, h)

def label(c, s, cx, cy, t, a, color=INK, size=40, kind="type", b=None, fill=PAPER2, rot=0, dur=0.3):
    f = font(kind, size); w = f.measureText(s) + 40; h = size + 24
    if t < a or (b is not None and t > b + dur): return (w, h)
    al = e_out(prog(t, a, a + dur))
    if b is not None and t > b: al *= 1 - prog(t, b, b + dur)
    c.save(); c.translate(cx, cy); c.rotate(rot)
    c.saveLayerAlpha(skia.Rect.MakeXYWH(-w/2-10, -h/2-10, w+20, h+20), int(255*al))
    c.drawRect(skia.Rect.MakeXYWH(-w/2, -h/2, w, h), P(fill)); c.drawRect(skia.Rect.MakeXYWH(-w/2, -h/2, w, h), P(color, "stroke", 2.2, rough=(12, 0.8)))
    text(c, s, 0, 0, kind, size, color)
    c.restore(); c.restore()
    return (w, h)

def fade_text(c, s, x, y, t, a, kind="serif", size=48, color=INK, align="c", b=None, dur=0.35, spacing=0, rise=10, stroke=None, bleed=True):
    if t < a or (b is not None and t > b + dur): return
    q = prog(t, a, a + dur); al = e_out(q)
    if b is not None and t > b: al *= 1 - prog(t, b, b + dur)
    blur = 7 * (1 - e_out(q)) if bleed else 0
    w = tw(s, kind, size)
    if blur > 0.4:
        c.save(); c.translate(0, rise*(1 - e_out(q)))
        pp = skia.Paint(); pp.setAlphaf(al); pp.setImageFilter(skia.ImageFilters.Blur(blur, blur))
        c.saveLayer(skia.Rect.MakeXYWH(x - w/2 - 40 if align == "c" else x - 40, y - size, w + 80, size*2), pp)
        text(c, s, x, y, kind, size, color, align, 1.0, spacing, stroke=stroke)
        c.restore(); c.restore()
    else:
        text(c, s, x, y + rise*(1 - e_out(q)), kind, size, color, align, al, spacing, stroke=stroke)
    return w

def typed(c, s, x, y, t, a, cps=22, kind="mono", size=40, color=INK, align="l", cursor=True, cursor_color=None, b=None):
    """Typewriter: reveals chars at cps from time a. Returns (n_chars, width_of_typed)."""
    if t < a: return 0, 0
    n = min(len(s), int((t - a) * cps) + 1) if t >= a else 0
    sub = s[:n]
    w = text(c, sub, x, y, kind, size, color, align) if sub else 0
    if cursor and n < len(s) and int((t - a) * 3) % 2 == 0:
        cx_ = (x + w) if align == "l" else x
        c.drawRect(skia.Rect.MakeXYWH(cx_ + 3, y - size*0.45, size*0.5, size*0.9), P(cursor_color or color, alpha=0.8))
    return n, w

def ink_circle(c, cx, cy, rx, ry, p, color=VERM, w=6, seed=2, rot=-5):
    """Hand-drawn pen loop that draws itself around something."""
    if p <= 0: return
    r = random.Random(seed); n = 70; start = r.uniform(-2.7, -2.2); pts = []
    for i in range(n+1):
        th = start + i/n * (math.pi*2*1.1); k = 1 + 0.03*math.sin(th*3 + seed) + (i/n)*0.08
        pts.append((rx*k*math.cos(th), ry*k*math.sin(th)))
    path = skia.Path(); path.moveTo(*pts[0])
    for q in pts[1:]: path.lineTo(*q)
    seg, _, _ = partial(path, 0, clamp(p))
    c.save(); c.translate(cx, cy); c.rotate(rot); c.drawPath(seg, P(color, "stroke", w, rough=(16, 1.4))); c.restore()

def underline(c, x0, x1, y, p, color=VERM, w=6, seed=1):
    if p <= 0: return
    r = random.Random(seed); path = skia.Path(); path.moveTo(x0, y)
    n = 12
    for i in range(1, n+1):
        f = i/n; path.lineTo(lerp(x0, x1, f), y + r.uniform(-2.2, 2.2))
    seg, _, _ = partial(path, 0, clamp(p)); c.drawPath(seg, P(color, "stroke", w, rough=(14, 1.0)))

def strike(c, x0, x1, y, p, color=VERM, w=7):
    if p <= 0: return
    path = skia.Path(); path.moveTo(x0, y + 4); path.lineTo(x1, y - 4)
    seg, _, _ = partial(path, 0, clamp(p)); c.drawPath(seg, P(color, "stroke", w, rough=(14, 1.2)))

def headline(c, s, x, y, size=64, color=INK, maxw=None, lh=1.12, kind="serif", align="c"):
    lines = wrap(s, kind, size, maxw) if maxw else [s]
    y0 = y - (len(lines)-1)*size*lh/2
    for i, ln in enumerate(lines): text(c, ln, x, y0 + i*size*lh, kind, size, color, align)
    return len(lines)

# --- figures (ink silhouettes, never real likenesses) -----------------------------------------
def person(c, x, y, s=1.0, kind="man", color=INK, alpha=1.0, glasses=False, flip=False, hatch_on=True):
    """Bust silhouette. (x,y) = base centre of the shoulders. height ~ 300*s."""
    c.save(); c.translate(x, y); c.scale(-s if flip else s, s)
    if alpha < 1: c.saveLayerAlpha(skia.Rect.MakeXYWH(-200, -340, 400, 360), int(255*alpha))
    body = skia.Path(); body.moveTo(-130, 0); body.cubicTo(-130, -70, -96, -100, -48, -112); body.lineTo(48, -112)
    body.cubicTo(96, -100, 130, -70, 130, 0); body.close()
    neck = rect_path(-22, -150, 44, 50)
    head = skia.Path()
    if kind == "man":
        head.addOval(skia.Rect.MakeXYWH(-50, -245, 100, 112))
    else:
        head.addOval(skia.Rect.MakeXYWH(-46, -243, 92, 108))
    c.drawPath(body, P(color)); c.drawPath(neck, P(color)); c.drawPath(head, P(color))
    if kind == "woman":
        hair = skia.Path(); hair.moveTo(-58, -170); hair.cubicTo(-70, -270, 70, -270, 58, -170); hair.cubicTo(60, -200, 40, -222, 0, -222); hair.cubicTo(-40, -222, -60, -200, -58, -170)
        c.drawPath(hair, P(color)); c.drawCircle(34, -262, 24, P(color))   # bun
        c.drawPath(skia.Path().addCircle(34, -262, 24), P(PAPER2, "stroke", 1.5, 0.0))
    if kind == "man":
        hair = skia.Path(); hair.moveTo(-52, -190); hair.cubicTo(-54, -262, 54, -262, 52, -190); hair.cubicTo(36, -222, -36, -222, -52, -190)
        c.drawPath(hair, P(color))
    if glasses:
        c.drawCircle(-18, -188, 17, P(PAPER, "stroke", 4)); c.drawCircle(20, -188, 17, P(PAPER, "stroke", 4)); c.drawLine(-1, -190, 3, -190, P(PAPER, "stroke", 4))
    if hatch_on:   # engraving-style highlight strokes on the shoulder
        c.save(); c.clipPath(body, doAntiAlias=True)
        for k in range(-5, 6):
            c.drawLine(k*22 - 40, -112, k*22 - 10, -8, P(PAPER2, "stroke", 2, 0.28))
        c.restore()
    if alpha < 1: c.restore()
    c.restore()

def fx_ring(c, x, y, p, r0=20, r1=90, color=VERM, w=4):
    if p <= 0 or p >= 1: return
    c.drawCircle(x, y, lerp(r0, r1, e_out(p)), P(color, "stroke", w*(1 - p), 1 - p))
