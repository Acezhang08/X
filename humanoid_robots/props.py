# -*- coding: utf-8 -*-
"""Blueprint props: generic line-art humanoid (joints, links), shirt that folds, hand, silhouettes, small icons.
Nothing here resembles any real product."""
import math
import skia
from lib import *

D2R = math.pi / 180

# ---------------------------------------------------------------------------------------------
# generic humanoid, side view, facing +x.  angles in degrees, measured from "down", positive = toward +x
def _dir(a): return (math.sin(a * D2R), math.cos(a * D2R))

def limb(c, x0, y0, x1, y1, r, w=4, color=LINE, alpha=1.0, fill=True):
    L = math.hypot(x1 - x0, y1 - y0); ang = math.degrees(math.atan2(y1 - y0, x1 - x0)) - 90
    c.save(); c.translate(x0, y0); c.rotate(ang)
    rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-r, -r * .6, 2*r, L + r * 1.2), r, r)
    if fill: c.drawRRect(rr, P(BG, alpha=0.9 * alpha))
    c.drawRRect(rr, P(color, "stroke", w, alpha))
    c.drawLine(0, 2, 0, L - 2, P(color, "stroke", 1.5, alpha * .5, dash=[10, 8]))      # centre line
    c.restore()

def joint(c, x, y, r=9, color=CYAN, alpha=1.0, w=3):
    c.drawCircle(x, y, r, P(BG, alpha=alpha)); c.drawCircle(x, y, r, P(color, "stroke", w, alpha))
    c.drawLine(x - r - 5, y, x + r + 5, y, P(color, "stroke", 1.5, alpha)); c.drawLine(x, y - r - 5, x, y + r + 5, P(color, "stroke", 1.5, alpha))

def pose_stand():
    return dict(px=0, py=0, rot=0, b=0, a1=0, a2=0, a1f=4, a2f=4, u1=8, u2=18, u1f=-6, u2f=6, head=0)

def robot_side(c, px, py, rot=0, b=0, a1=0, a2=0, a1f=None, a2f=None, u1=8, u2=18, u1f=None, u2f=None,
               s=1.0, color=LINE, jcolor=CYAN, alpha=1.0, ghost=False):
    """pelvis at (px,py). a1/a2 thigh/shin (abs, from down), b torso lean from up, u1/u2 upper/fore arm (abs from down)."""
    a1f = a1 + 6 if a1f is None else a1f; a2f = a2 + 6 if a2f is None else a2f
    u1f = u1 - 10 if u1f is None else u1f; u2f = u2 - 6 if u2f is None else u2f
    c.save(); c.translate(px, py); c.rotate(rot); c.scale(s, s)
    wlw = 3.5 if not ghost else 2.5
    def leg(a1_, a2_, al):
        d1 = _dir(a1_); kx, ky = d1[0] * 100, d1[1] * 100
        d2 = _dir(a2_); fx, fy = kx + d2[0] * 100, ky + d2[1] * 100
        limb(c, 0, 0, kx, ky, 17, wlw, color, al); limb(c, kx, ky, fx, fy, 14, wlw, color, al)
        # foot
        ca = math.cos((a2_ - 90) * D2R * -1)
        fa = _dir(a2_ + 90)
        c.drawLine(fx, fy, fx + fa[0] * 44 * -1 * -1, fy + fa[1] * 44, P(color, "stroke", wlw + 2, al))
        if not ghost: joint(c, kx, ky, 8, jcolor, al)
        return (kx, ky, fx, fy)
    def arm(u1_, u2_, al):
        sx, sy = _dir(b + 180)[0] * 0, 0
        top = _dir(180 + b)                            # unit "up along torso" in screen coords
        shx, shy = top[0] * 118 * -1 * -1, top[1] * 118 * -1
        # torso up direction: (sin b, -cos b)
        shx, shy = math.sin(b * D2R) * 118, -math.cos(b * D2R) * 118
        d1 = _dir(u1_); ex, ey = shx + d1[0] * 80, shy + d1[1] * 80
        d2 = _dir(u2_); hx, hy = ex + d2[0] * 74, ey + d2[1] * 74
        limb(c, shx, shy, ex, ey, 12, wlw, color, al); limb(c, ex, ey, hx, hy, 10, wlw, color, al)
        c.drawCircle(hx, hy, 11, P(BG, alpha=al)); c.drawCircle(hx, hy, 11, P(color, "stroke", wlw, al))
        if not ghost: joint(c, ex, ey, 7, jcolor, al)
    # far limbs first (dimmer)
    leg(a1f, a2f, alpha * .55); arm(u1f, u2f, alpha * .55)
    # torso
    ux, uy = math.sin(b * D2R), -math.cos(b * D2R)
    nx, ny = -uy, ux
    top = (ux * 130, uy * 130); bw, tw_ = 26, 36
    pts = [(nx * -bw, ny * -bw), (nx * bw, ny * bw), (top[0] + nx * tw_, top[1] + ny * tw_), (top[0] - nx * tw_, top[1] - ny * tw_)]
    c.drawPath(pts_path(pts, True), P(BG, alpha=0.9 * alpha)); c.drawPath(pts_path(pts, True), P(color, "stroke", wlw, alpha))
    # chest panel line + head
    c.drawLine(ux * 60 - nx * 20, uy * 60 - ny * 20, ux * 60 + nx * 20, uy * 60 + ny * 20, P(color, "stroke", 1.8, alpha * .6))
    hx0, hy0 = top[0] + ux * 6, top[1] + uy * 6
    c.drawLine(top[0], top[1], hx0, hy0 - 2, P(color, "stroke", wlw + 3, alpha))
    c.save(); c.translate(hx0, hy0); c.rotate(b)
    rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-24, -54, 52, 50), 12, 12)
    c.drawRRect(rr, P(BG, alpha=0.9 * alpha)); c.drawRRect(rr, P(color, "stroke", wlw, alpha))
    c.drawLine(2, -34, 26, -34, P(jcolor, "stroke", 4, alpha))      # visor slit, no face
    c.restore()
    leg(a1, a2, alpha); arm(u1, u2, alpha)
    joint(c, 0, 0, 9, jcolor, alpha)
    c.restore()

def _smooth(x): return x * x * (3 - 2 * x)
def _kf(u, keys):
    """keys: [(u, value)] -> piecewise smooth interpolation"""
    if u <= keys[0][0]: return keys[0][1]
    for (u0, v0), (u1, v1) in zip(keys, keys[1:]):
        if u <= u1: return lerp(v0, v1, _smooth((u - u0) / (u1 - u0)))
    return keys[-1][1]

FLOOR_CLR = 16
def flip_pose(u, ground_y, x0, s=1.0):
    """Backflip, u in [0,1] -> pose kwargs. rotation is backward (counter-clockwise on screen)."""
    crouch = _kf(u, [(0, 0), (.16, 1), (.27, 0), (.34, 0), (.9, 0), (.95, 1), (1, 0)])        # 1 = deep crouch
    tuck = _kf(u, [(0, 0), (.30, 0), (.42, 1), (.62, 1), (.76, 0), (1, 0)])
    a1 = lerp(0, 70, crouch) + lerp(0, 95, tuck); a2 = lerp(0, -45, crouch) + lerp(0, -75, tuck)
    b = lerp(0, 25, crouch) + lerp(0, 5, tuck)
    u1 = _kf(u, [(0, 8), (.16, 40), (.28, 170), (.4, 90), (.62, 60), (.78, 120), (.95, 50), (1, 8)])
    u2 = u1 + 20
    rot = -360 * _kf(u, [(0, 0), (.3, 0), (.78, 1), (1, 1)])
    stand_h = 216
    pelvis_contact = lambda a1_, a2_: ground_y - s * (FLOOR_CLR + 100 * math.cos(a1_ * D2R) + 100 * math.cos(a2_ * D2R))
    ground_py = pelvis_contact(a1, a2)
    fl = prog(u, .27, .92)
    air = 4 * fl * (1 - fl) * 300 * s if 0 < fl < 1 else 0
    py = ground_py - air
    px = x0 - 40 * _kf(u, [(0, 0), (.3, 0), (.9, 1), (1, 1)])
    return dict(px=px, py=py, rot=rot, b=b, a1=a1, a2=a2, a1f=a1 + 5, a2f=a2 + 5, u1=u1, u2=u2, u1f=u1 - 12, u2f=u2 - 12)

def draw_flip(c, u, ground_y, x0, s=1.0, trail=True, ghosts=(), color=LINE, alpha=1.0, trail_alpha=1.0):
    """whole backflip figure: ground line, ballistic trail, ghost poses, current pose."""
    if trail:
        pts = []
        for i in range(0, 41):
            uu = .27 + (.92 - .27) * i / 40
            q = flip_pose(uu, ground_y, x0, s); pts.append((q["px"], q["py"]))
        vis = [p_ for i, p_ in enumerate(pts) if (.27 + (.92 - .27) * i / 40) <= u]
        if len(vis) > 1: c.drawPath(pts_path(vis), P(AMBER if False else CYAN, "stroke", 3, .8 * trail_alpha * alpha, dash=[14, 10]))
    for gu in ghosts:
        if gu < u - 0.02:
            q = flip_pose(gu, ground_y, x0, s); robot_side(c, s=s, color=color, alpha=.22 * alpha, ghost=True, **q)
    q = flip_pose(u, ground_y, x0, s); robot_side(c, s=s, color=color, alpha=alpha, **q)

# ---------------------------------------------------------------------------------------------
# bimanual robot (front/top style) for the laundry table: torso block + two 2-link arms by IK
def ik2(sx, sy, tx, ty, l1, l2, bend=1):
    d = min(math.hypot(tx - sx, ty - sy), l1 + l2 - 1); a = math.atan2(ty - sy, tx - sx)
    cosb = clamp((l1*l1 + d*d - l2*l2) / (2 * l1 * d), -1, 1); b = math.acos(cosb) * bend
    ex, ey = sx + l1 * math.cos(a + b), sy + l1 * math.sin(a + b)
    hx, hy = sx + d * math.cos(a), sy + d * math.sin(a)
    return (ex, ey), (hx, hy)

def gripper(c, x, y, ang, openp=0.0, color=LINE, alpha=1.0, w=3.5):
    c.save(); c.translate(x, y); c.rotate(math.degrees(ang) - 90)
    o = 6 + 12 * openp
    for sgn in (-1, 1):
        pts = [(sgn * o, 0), (sgn * (o + 4), 26), (sgn * o * .6, 40)]
        c.drawPath(pts_path(pts), P(color, "stroke", w, alpha))
    c.restore()

def robot_arms(c, cx, cy, targets, grips=(0.0, 0.0), s=1.0, color=LINE, alpha=1.0, torso=True, head=True):
    """Robot body seen from the front, camera-side up; arms reach the two target points (absolute coords)."""
    if torso:
        c.save(); c.translate(cx, cy); c.scale(s, s)
        body = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-90, -30, 180, 170), 26, 26)
        c.drawRRect(body, P(BG, alpha=.92 * alpha)); c.drawRRect(body, P(color, "stroke", 3.5, alpha))
        if head:
            hd = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-44, -110, 88, 66), 16, 16)
            c.drawRRect(hd, P(BG, alpha=.92 * alpha)); c.drawRRect(hd, P(color, "stroke", 3.5, alpha))
            c.drawLine(-28, -77, 28, -77, P(CYAN, "stroke", 5, alpha))
        c.drawLine(-60, 40, 60, 40, P(color, "stroke", 1.8, alpha * .6)); c.drawLine(-60, 70, 60, 70, P(color, "stroke", 1.8, alpha * .6))
        c.restore()
    for side, (tx, ty), gp in zip((-1, 1), targets, grips):
        sx, sy = cx + side * 96 * s, cy + 6 * s
        (ex, ey), (hx, hy) = ik2(sx, sy, tx, ty, 215 * s, 195 * s, bend=-side)
        limb(c, sx, sy, ex, ey, 15 * s, 3.5, color, alpha); limb(c, ex, ey, hx, hy, 12 * s, 3.5, color, alpha)
        joint(c, sx, sy, 10, CYAN, alpha); joint(c, ex, ey, 9, CYAN, alpha)
        gripper(c, hx, hy, math.atan2(hy - ey, hx - ex), gp, color, alpha)

# ---------------------------------------------------------------------------------------------
# shirt that folds
def clip_poly(poly, nx, ny, d0, keep_pos=True):
    """Sutherland-Hodgman against half-plane  nx*x+ny*y >= d0 (keep_pos) or <= d0."""
    def side(p_): v = nx * p_[0] + ny * p_[1] - d0; return v if keep_pos else -v
    out = []
    for i in range(len(poly)):
        a = poly[i]; b = poly[(i + 1) % len(poly)]; sa, sb = side(a), side(b)
        if sa >= 0: out.append(a)
        if (sa >= 0) != (sb >= 0):
            k = sa / (sa - sb); out.append((a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k))
    return out

SHIRT = [(-40, -130), (-22, -112), (22, -112), (40, -130), (100, -130), (192, -92), (160, -28), (100, -52), (100, 130), (-100, 130), (-100, -52), (-160, -28), (-192, -92), (-100, -130)]

def shirt_layers(f1, f2, f3):
    """Return list of polygons (back to front) for fold progresses: f1 = left side in, f2 = right side in, f3 = bottom up."""
    if f1 <= 0 and f2 <= 0 and f3 <= 0: return [SHIRT]
    layers = []
    base = clip_poly(clip_poly(SHIRT, 1, 0, -45, True), 1, 0, 45, False)      # centre strip x in [-45,45]
    left = clip_poly(SHIRT, 1, 0, -45, False); right = clip_poly(SHIRT, 1, 0, 45, True)
    def fx(poly, xa, p_): return [(xa + (x - xa) * math.cos(p_ * math.pi), y) for x, y in poly]
    stack = [base, fx(left, -45, f1), fx(right, 45, f2)]
    for i, poly in enumerate(stack):
        if len(poly) < 3: continue
        top = clip_poly(poly, 0, 1, 40, False); bot = clip_poly(poly, 0, 1, 40, True)
        if len(top) >= 3: layers.append((i, top))
        if len(bot) >= 3: layers.append((i + 3, [(x, 40 + (y - 40) * math.cos(f3 * math.pi)) for x, y in bot]))
    layers.sort(key=lambda t: (1 if t[0] >= 3 and f3 > .5 else 0, t[0] % 3 if t[0] < 3 else (t[0] % 3) + 0.5))
    return [p_ for _, p_ in layers]

def draw_shirt(c, cx, cy, s=1.0, f1=0, f2=0, f3=0, color=LINE, alpha=1.0, fill=CYAN, falpha=.16, rot=0, crumple=0.0, seed=0):
    c.save(); c.translate(cx, cy); c.rotate(rot); c.scale(s, s)
    for poly in shirt_layers(f1, f2, f3):
        if crumple:
            poly = [(x + crumple * 22 * math.sin(y * .05 + seed * 3 + x * .03), y + crumple * 18 * math.cos(x * .04 + seed)) for x, y in poly]
        path = pts_path(poly, True)
        c.drawPath(path, P(BG, alpha=.94 * alpha)); c.drawPath(path, P(fill, alpha=falpha * alpha)); c.drawPath(path, P(color, "stroke", 3.2, alpha))
    c.restore()

# ---------------------------------------------------------------------------------------------
# human silhouettes (no faces) and small icons
def person(c, x, y, s=1.0, color=LINE, alpha=1.0, headset=False, arms_up=0.0, bust=True):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawCircle(0, -70, 34, P(BG, alpha=.95 * alpha)); c.drawCircle(0, -70, 34, P(color, "stroke", 3.5, alpha))
    body = skia.Path(); body.moveTo(-86, 40); body.cubicTo(-86, -10, -50, -28, 0, -28); body.cubicTo(50, -28, 86, -10, 86, 40); body.close()
    c.drawPath(body, P(BG, alpha=.95 * alpha)); c.drawPath(body, P(color, "stroke", 3.5, alpha))
    if headset:
        arc(c, 0, -74, 40, math.pi * 1.05, math.pi * 1.95, 1, 5, CYAN, alpha)
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-38, -80, 76, 28), 8, 8), P(CYAN, "stroke", 4, alpha))
    c.restore()

def eye_icon(c, x, y, s=1.0, color=LINE, alpha=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    pth = skia.Path(); pth.moveTo(-60, 0); pth.quadTo(0, -52, 60, 0); pth.quadTo(0, 52, -60, 0)
    c.drawPath(pth, P(color, "stroke", 4, alpha)); c.drawCircle(0, 0, 17, P(CYAN, "stroke", 4, alpha)); c.drawCircle(0, 0, 6, P(CYAN, alpha=alpha))
    c.restore()

def camera_icon(c, x, y, s=1.0, color=LINE, alpha=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-45, -28, 90, 56), 8, 8), P(color, "stroke", 4, alpha))
    c.drawCircle(0, 0, 16, P(CYAN, "stroke", 4, alpha)); c.drawRect(skia.Rect.MakeXYWH(-20, -40, 24, 12), P(color, "stroke", 3, alpha))
    c.restore()

def clock_icon(c, x, y, r=60, t=0.0, color=LINE, alpha=1.0):
    c.drawCircle(x, y, r, P(color, "stroke", 4, alpha))
    for k in range(12):
        a = k * math.pi / 6; c.drawLine(x + math.sin(a) * (r - 10), y - math.cos(a) * (r - 10), x + math.sin(a) * r, y - math.cos(a) * r, P(color, "stroke", 3, alpha))
    c.drawLine(x, y, x + math.sin(t * 2 * math.pi) * (r - 14), y - math.cos(t * 2 * math.pi) * (r - 14), P(AMBER if False else CYAN, "stroke", 5, alpha))
    c.drawLine(x, y, x + math.sin(t * 24 * math.pi) * (r * .5), y - math.cos(t * 24 * math.pi) * (r * .5), P(color, "stroke", 4, alpha))

def gpu_icon(c, x, y, s=1.0, color=LINE, alpha=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-80, -36, 160, 72), 8, 8), P(color, "stroke", 4, alpha))
    for dx in (-36, 36): c.drawCircle(dx, 0, 22, P(CYAN, "stroke", 3.5, alpha))
    for k in range(6): c.drawLine(-70 + k * 28, 36, -70 + k * 28, 52, P(color, "stroke", 3, alpha))
    c.restore()

def book_icon(c, x, y, s=1.0, color=LINE, alpha=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRect(skia.Rect.MakeXYWH(-70, -95, 140, 190), P(BG, alpha=.95 * alpha)); c.drawRect(skia.Rect.MakeXYWH(-70, -95, 140, 190), P(color, "stroke", 4, alpha))
    c.drawLine(-52, -95, -52, 95, P(color, "stroke", 3, alpha))
    for k in range(4): c.drawLine(-30, -50 + k * 22, 50, -50 + k * 22, P(color, "stroke", 2.5, alpha * .7))
    c.restore()

def chessboard(c, x, y, cell=44, p=1.0, alpha=1.0, n=8):
    for i in range(n):
        for j in range(n):
            if (i + j) % 2 == 0 and p * n * n > i * n + j: c.drawRect(skia.Rect.MakeXYWH(x + i * cell, y + j * cell, cell, cell), P(LINE, alpha=.25 * alpha))
    draw_on(c, rect_pts(x, y, cell * n, cell * n), p, 3, LINE, alpha, close=True)

def hand_outline(c, x, y, s=1.0, p=1.0, color=LINE, alpha=1.0, dots=0.0, seed=1):
    """Open hand (palm to viewer): capsule fingers with joints; optional touch-receptor dots inside the outline."""
    import random
    c.save(); c.translate(x, y); c.scale(s, s)
    segs = []     # (x0,y0,x1,y1,r)
    fing = [(-52, -90, 98, 4.5), (-18, -92, 122, 1.5), (16, -92, 128, -1), (50, -90, 108, -4)]
    for bx, a0, L, ang in fing:
        a = ang * D2R; mx, my = bx + math.sin(a) * L * .58, -10 - math.cos(a) * L * .58
        ex, ey = bx + math.sin(a) * L, -10 - math.cos(a) * L
        segs.append((bx, -10, mx, my, 13)); segs.append((mx, my, ex, ey, 12))
    segs.append((66, 56, 118, 4, 14)); segs.append((118, 4, 150, -34, 12))     # thumb
    palm = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-72, -10, 144, 124), 34, 34)
    n = len(segs)
    for i, (x0, y0, x1, y1, r) in enumerate(segs):
        k = prog(p, i / (n + 2), (i + 3) / (n + 2))
        if k > 0: limb(c, x0, y0, x0 + (x1 - x0) * k, y0 + (y1 - y0) * k, r, 4, color, alpha)
    if p > .25:
        c.drawRRect(palm, P(BG, alpha=.95 * alpha * clamp(p * 2))); c.drawRRect(palm, P(color, "stroke", 4, alpha * clamp(p * 2)))
    if p > .8:
        for (x0, y0, x1, y1, r) in segs[::2]: c.drawCircle(x1 * .0 + (x0 + x1) / 2, (y0 + y1) / 2, 5, P(CYAN, "stroke", 2.5, alpha))
    if dots > 0:
        r_ = random.Random(seed); pts = []
        for i in range(260):
            if r_.random() < .45: pts.append((r_.uniform(-60, 60), r_.uniform(0, 104)))
            else:
                x0, y0, x1, y1, rr = segs[r_.randrange(len(segs))]; t_ = r_.random() ** .6
                pts.append((x0 + (x1 - x0) * t_ + r_.uniform(-6, 6), y0 + (y1 - y0) * t_ + r_.uniform(-6, 6)))
        for q in pts[:int(dots * len(pts))]: c.drawCircle(q[0], q[1], 3.6, P(CYAN, alpha=.95 * alpha))
    c.restore()

def quad(c, x, y, s=1.0, ph=0.0, color=LINE, alpha=1.0):
    """tiny four-legged walker, side view; (x,y) = foot level centre"""
    c.save(); c.translate(x, y); c.scale(s, s)
    top = -74
    body = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-62, top, 124, 38), 10, 10)
    c.drawRRect(body, P(BG, alpha=.92 * alpha)); c.drawRRect(body, P(color, "stroke", 3.5, alpha))
    c.drawCircle(70, top + 8, 11, P(BG, alpha=alpha)); c.drawCircle(70, top + 8, 11, P(color, "stroke", 3, alpha))
    for lx, off in ((-46, 0), (-18, .5), (18, .25), (46, .75)):
        th = 26 * math.sin((ph + off) * 2 * math.pi)
        hx, hy = lx, top + 38
        kx, ky = hx + math.sin(th * D2R) * 34, hy + math.cos(th * D2R) * 34
        a2 = -th * .6 + (18 if lx > 0 else -18) * 0
        fx, fy = kx + math.sin(a2 * D2R) * 34, ky + math.cos(a2 * D2R) * 34
        c.drawPath(pts_path([(hx, hy), (kx, ky), (fx, min(fy, 0))]), P(color, "stroke", 4, alpha))
        c.drawCircle(kx, ky, 4.5, P(CYAN, "stroke", 2.5, alpha))
    c.restore()

def rubik(c, x, y, s=1.0, twist=0.0, color=LINE, alpha=1.0):
    """isometric 3x3 cube"""
    c.save(); c.translate(x, y); c.scale(s, s)
    k = 46
    def iso(i, j, kk): return ((i - j) * k * .87, (i + j) * k * .5 - kk * k)
    faces = {"top": [], "left": [], "right": []}
    cols = [CYAN, LINE, AMBER, 0xFF5BC27F, RED, 0xFF4F7BD8]
    for i in range(3):
        for j in range(3):
            pts = [iso(i, j, 3), iso(i + 1, j, 3), iso(i + 1, j + 1, 3), iso(i, j + 1, 3)]
            c.drawPath(pts_path(pts, True), P(cols[(i + j) % 6] if False else CYAN, alpha=.12 * alpha)); c.drawPath(pts_path(pts, True), P(color, "stroke", 2.5, alpha))
            pts = [iso(i, 3, 3 - j), iso(i + 1, 3, 3 - j), iso(i + 1, 3, 2 - j), iso(i, 3, 2 - j)]
            c.drawPath(pts_path(pts, True), P(color, "stroke", 2.5, alpha))
            pts = [iso(3, i, 3 - j), iso(3, i + 1, 3 - j), iso(3, i + 1, 2 - j), iso(3, i, 2 - j)]
            c.drawPath(pts_path(pts, True), P(color, "stroke", 2.5, alpha))
    c.restore()

def house_plan(c, x, y, w, h, kind=0, p=1.0, color=LINE, alpha=1.0):
    """architectural floor plan thumbnail with a basket"""
    rect(c, x, y, w, h, p, 3.5, color, alpha)
    if kind == 0: line(c, x + w * .55, y, x + w * .55, y + h * .6, p, 3, color, alpha); line(c, x, y + h * .6, x + w * .55, y + h * .6, p, 3, color, alpha)
    if kind == 1: line(c, x + w * .35, y, x + w * .35, y + h, p, 3, color, alpha); line(c, x + w * .35, y + h * .45, x + w, y + h * .45, p, 3, color, alpha)
    if kind == 2: line(c, x, y + h * .4, x + w * .7, y + h * .4, p, 3, color, alpha); line(c, x + w * .7, y + h * .4, x + w * .7, y + h, p, 3, color, alpha)
    if kind == 3: line(c, x + w * .5, y, x + w * .5, y + h, p, 3, color, alpha); line(c, x + w * .5, y + h * .7, x + w, y + h * .7, p, 3, color, alpha)
    if p >= 1:
        bx, by = [(x + w * .2, y + h * .75), (x + w * .78, y + h * .2), (x + w * .15, y + h * .2), (x + w * .75, y + h * .85)][kind]
        shapes = [0, 1, 2, 1]
        if kind in (0, 3): circle(c, bx, by, 18, 1, 3, CYAN, alpha)
        else: rect(c, bx - 20, by - 14, 40, 28, 1, 3, CYAN, alpha)
