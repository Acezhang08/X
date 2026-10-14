# -*- coding: utf-8 -*-
"""Ink line-art props for the AI-history series. All drawn procedurally; no photos, no likenesses."""
import math, random
import skia
from lib import *

def person2(c, x, y, s=1.0, kind="man", color=INK, alpha=1.0, glasses=False, flip=False, child=False, face_hatch=True):
    """Ink bust silhouette. (x,y)=base centre of shoulders, height ~ 290*s. Never a likeness."""
    c.save(); c.translate(x, y); c.scale((-s if flip else s) * (0.62 if child else 1.0), s * (0.62 if child else 1.0))
    if alpha < 1: c.saveLayerAlpha(skia.Rect.MakeXYWH(-220, -360, 440, 380), int(255*alpha))
    body = skia.Path(); body.moveTo(-136, 0); body.cubicTo(-136, -62, -104, -92, -56, -104); body.lineTo(-24, -112)
    body.lineTo(24, -112); body.lineTo(56, -104); body.cubicTo(104, -92, 136, -62, 136, 0); body.close()
    c.drawPath(body, P(color))
    neck = skia.Path(); neck.moveTo(-24, -150); neck.lineTo(24, -150); neck.lineTo(30, -104); neck.lineTo(-30, -104); neck.close(); c.drawPath(neck, P(color))
    head = skia.Path(); head.moveTo(0, -254); head.cubicTo(42, -254, 54, -218, 49, -186); head.cubicTo(45, -152, 24, -128, 0, -126)
    head.cubicTo(-24, -128, -45, -152, -49, -186); head.cubicTo(-54, -218, -42, -254, 0, -254); head.close(); c.drawPath(head, P(color))
    if kind == "woman":
        hair = skia.Path(); hair.moveTo(-54, -160); hair.cubicTo(-72, -262, 72, -262, 54, -160); hair.cubicTo(56, -196, 46, -226, 0, -230); hair.cubicTo(-46, -226, -56, -196, -54, -160); hair.close()
        c.drawPath(hair, P(color)); c.drawCircle(30, -268, 25, P(color))
        c.drawPath(skia.Path().addCircle(30, -268, 25), P(color))
    else:
        hair = skia.Path(); hair.moveTo(-52, -190); hair.cubicTo(-58, -266, 58, -266, 52, -190); hair.cubicTo(40, -222, 6, -236, -14, -232); hair.cubicTo(-34, -228, -46, -212, -52, -190); hair.close()
        c.drawPath(hair, P(color))
    if kind == "man" and not child:   # collar V
        v = skia.Path(); v.moveTo(-26, -112); v.lineTo(0, -66); v.lineTo(26, -112); c.drawPath(v, P(PAPER2, "stroke", 3.2, 0.55))
    if glasses:
        c.drawCircle(-19, -190, 17, P(PAPER2, "stroke", 4.2, 0.9)); c.drawCircle(20, -190, 17, P(PAPER2, "stroke", 4.2, 0.9)); c.drawLine(-2, -192, 3, -192, P(PAPER2, "stroke", 4, 0.9))
    if face_hatch:
        c.save(); c.clipPath(body, doAntiAlias=True)
        for k in range(-6, 7):
            c.drawLine(k*20 - 46, -108, k*20 - 22, -4, P(PAPER2, "stroke", 1.8, 0.22))
        c.restore()
    if alpha < 1: c.restore()
    c.restore()

def bubble(c, cx, cy, w, h, tail=(0, 1), color=INK, fill=PAPER2, alpha=1.0, thought=False):
    """Hand-inked speech/thought bubble; tail=(dx,dy) direction. Returns inner rect centre."""
    c.save(); c.translate(cx, cy)
    if alpha < 1: c.saveLayerAlpha(skia.Rect.MakeXYWH(-w/2-60, -h/2-60, w+120, h+160), int(255*alpha))
    rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-w/2, -h/2, w, h), h*0.35, h*0.35)
    p = skia.Path(); p.addRRect(rr)
    if not thought:
        tx, ty = tail; bx = tx * w*0.28; by = ty * h/2
        tp = skia.Path(); tp.moveTo(bx - 22, by - (4 if ty > 0 else -4)); tp.lineTo(tx*w*0.42, ty*(h/2 + 44)); tp.lineTo(bx + 22, by - (4 if ty > 0 else -4)); tp.close()
        c.drawPath(tp, P(fill)); c.drawPath(p, P(fill)); c.drawPath(tp, P(color, "stroke", 3.5, rough=(14, 1.0)))
        c.drawPath(p, P(color, "stroke", 3.5, rough=(14, 1.0)))
        c.drawPath(tp, P(fill)); c.drawPath(skia.Path().addRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-w/2+3, -h/2+3, w-6, h-6), h*0.33, h*0.33)), P(fill))
    else:
        c.drawPath(p, P(fill)); c.drawPath(p, P(color, "stroke", 3.5, rough=(14, 1.0)))
        tx, ty = tail
        for i, r_ in enumerate((14, 9, 5)):
            c.drawCircle(tx*w*0.3 + tx*i*30, ty*(h/2 + 24 + i*26), r_, P(fill)); c.drawCircle(tx*w*0.3 + tx*i*30, ty*(h/2 + 24 + i*26), r_, P(color, "stroke", 3))
    if alpha < 1: c.restore()
    c.restore()

def terminal(c, x, y, s=1.0, color=INK, alpha=1.0, key_t=None, paper_lines=None, paper_h=1.0):
    """Typewriter terminal; (x,y) = base centre. ~360x300 at s=1. key_t: time driving key bounce.
    paper_lines: list of (width_frac) to draw as typed line strokes on the sheet."""
    c.save(); c.translate(x, y); c.scale(s, s)
    if alpha < 1: c.saveLayerAlpha(skia.Rect.MakeXYWH(-260, -420, 520, 460), int(255*alpha))
    # paper sheet sticking up
    sh = 170 * paper_h
    c.drawRect(skia.Rect.MakeXYWH(-95, -190 - sh, 190, sh + 20), P(PAPER2)); c.drawRect(skia.Rect.MakeXYWH(-95, -190 - sh, 190, sh + 20), P(color, "stroke", 3, rough=(14, 1)))
    if paper_lines:
        for i, f in enumerate(paper_lines):
            yy = -190 - sh + 28 + i*26
            if yy < -200: c.drawLine(-76, yy, -76 + 152*f, yy, P(color, "stroke", 3.5, 0.75))
    # platen
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-130, -200, 260, 36), 16, 16), P(PAPER3)); c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-130, -200, 260, 36), 16, 16), P(color, "stroke", 4, rough=(14, 1)))
    for sx in (-1, 1): c.drawCircle(sx*140, -182, 14, P(color, "stroke", 4))
    # body
    body = skia.Path(); body.moveTo(-170, 0); body.lineTo(-140, -160); body.lineTo(140, -160); body.lineTo(170, 0); body.close()
    c.drawPath(body, P(PAPER2)); ink(c, body, 5, color)
    # keys
    r = random.Random(3)
    for row in range(3):
        n = 9 - row; yy = -128 + row*34
        for k in range(n):
            xx = -(n-1)*17.5 + k*35 + (0 if row % 2 == 0 else 0)
            bounce = 0
            if key_t is not None and (int(key_t*9) + row*3 + k) % 7 == 0: bounce = 4
            c.drawCircle(xx, yy + bounce, 11, P(PAPER)); c.drawCircle(xx, yy + bounce, 11, P(color, "stroke", 2.6))
    c.drawLine(-70, -26, 70, -26, P(color, "stroke", 4)); c.drawLine(-70, -26, -70, -10, P(color, "stroke", 3)); c.drawLine(70, -26, 70, -10, P(color, "stroke", 3))
    if alpha < 1: c.restore()
    c.restore()

def mainframe(c, x, y, s=1.0, t=0.0, color=INK, alpha=1.0, lights=True):
    """Row of cabinets + a tape-reel pair. (x,y)=base centre, ~760x300 at s=1."""
    c.save(); c.translate(x, y); c.scale(s, s)
    if alpha < 1: c.saveLayerAlpha(skia.Rect.MakeXYWH(-460, -420, 920, 460), int(255*alpha))
    # three cabinets
    for i, (cx_, w_, h_) in enumerate(((-250, 210, 300), (0, 250, 330), (250, 210, 300))):
        r = skia.Rect.MakeXYWH(cx_ - w_/2, -h_, w_, h_)
        c.drawRect(r, P(PAPER2)); ink(c, rect_path(cx_ - w_/2, -h_, w_, h_), 5, color)
        c.drawLine(cx_ - w_/2, -h_ + 36, cx_ + w_/2, -h_ + 36, P(color, "stroke", 3.5))
        hatch(c, rect_path(cx_ + w_/2 - 30, -h_, 30, h_), 70, 9, 1.8, color, 0.45)
        if i != 1 and lights:
            for k in range(5):
                on = (int(t*3) + k + i) % 4 == 0
                c.drawCircle(cx_ - w_/2 + 30 + k*28, -h_ + 18, 8, P(VERM if on else PAPER3)); c.drawCircle(cx_ - w_/2 + 30 + k*28, -h_ + 18, 8, P(color, "stroke", 2))
    # reels on centre cabinet
    for sx in (-1, 1):
        rx, ry = sx*64, -246
        c.drawCircle(rx, ry, 52, P(PAPER3)); c.drawCircle(rx, ry, 52, P(color, "stroke", 4.5, rough=(12, 1)))
        c.drawCircle(rx, ry, 11, P(color))
        a0 = t * 2.2 * (1 if sx > 0 else -1)
        for k in range(3):
            a = a0 + k*2*math.pi/3
            c.drawLine(rx + 14*math.cos(a), ry + 14*math.sin(a), rx + 44*math.cos(a), ry + 44*math.sin(a), P(color, "stroke", 4))
    # panel with dials on the centre cabinet (keeps the reels from reading as a face)
    c.drawRect(skia.Rect.MakeXYWH(-96, -138, 192, 74), P(PAPER)); ink(c, rect_path(-96, -138, 192, 74), 3.5, color)
    for k in range(5):
        c.drawCircle(-68 + k*34, -112, 11, P(PAPER2)); c.drawCircle(-68 + k*34, -112, 11, P(color, "stroke", 2.6)); c.drawLine(-68 + k*34, -112, -68 + k*34 + 6, -118, P(color, "stroke", 2.4))
    c.drawLine(-80, -80, 80, -80, P(color, "stroke", 3))
    if alpha < 1: c.restore()
    c.restore()

def small_person(c, x, y, s=1.0, color=INK, alpha=1.0, fill=True):
    """Pictogram person (head + shoulders), ~ 40x60 at s=1, (x,y)=bottom centre."""
    c.save(); c.translate(x, y); c.scale(s, s)
    body = skia.Path(); body.moveTo(-16, 0); body.cubicTo(-16, -22, -8, -28, 0, -28); body.cubicTo(8, -28, 16, -22, 16, 0); body.close()
    if fill: c.drawPath(body, P(color, alpha=alpha)); c.drawCircle(0, -42, 11, P(color, alpha=alpha))
    else: c.drawPath(body, P(color, "stroke", 2.6, alpha)); c.drawCircle(0, -42, 11, P(color, "stroke", 2.6, alpha))
    c.restore()

def calendar_page(c, cx, cy, month, year, s=1.0, rot=0.0, color=INK, accent=VERM):
    c.save(); c.translate(cx, cy); c.rotate(rot); c.scale(s, s)
    c.drawRect(skia.Rect.MakeXYWH(-150, -130, 300, 260), P(0x552A1D10, blur=0)) if False else None
    c.save(); c.translate(5, 9); c.drawRect(skia.Rect.MakeXYWH(-150, -130, 300, 260), P(0x2A1D10, alpha=0.28, blur=7)); c.restore()
    c.drawRect(skia.Rect.MakeXYWH(-150, -130, 300, 260), P(PAPER2)); ink(c, rect_path(-150, -130, 300, 260), 4, color)
    c.drawRect(skia.Rect.MakeXYWH(-150, -130, 300, 74), P(accent));
    for sx in (-80, 80): c.drawCircle(sx, -130, 11, P(PAPER)); c.drawCircle(sx, -130, 11, P(color, "stroke", 3))
    text(c, month, 0, -93, "sc", 46, PAPER2)
    if year: text(c, str(year), 0, 20, "type", 76, color)
    else:
        for r_ in range(4):
            for k_ in range(6): c.drawRect(skia.Rect.MakeXYWH(-112 + k_*38, -34 + r_*34, 24, 18), P(LINEL, "stroke", 2, 0.9))
    c.restore()

def book(c, cx, cy, w, h, title_lines, s=1.0, rot=0.0, color=INK, spine=VERM, sub=None):
    c.save(); c.translate(cx, cy); c.rotate(rot); c.scale(s, s)
    c.save(); c.translate(10, 14); c.drawRect(skia.Rect.MakeXYWH(-w/2, -h/2, w, h), P(0x2A1D10, alpha=0.3, blur=10)); c.restore()
    c.drawRect(skia.Rect.MakeXYWH(-w/2, -h/2, w, h), P(PAPER3)); ink(c, rect_path(-w/2, -h/2, w, h), 5, color)
    c.drawRect(skia.Rect.MakeXYWH(-w/2, -h/2, 34, h), P(spine)); c.drawLine(-w/2 + 34, -h/2, -w/2 + 34, h/2, P(color, "stroke", 3))
    y0 = -h/2 + 80
    for i, ln in enumerate(title_lines): text(c, ln, 17, y0 + i*58, "sc", 40, color)
    c.drawLine(-w/2 + 80, y0 + len(title_lines)*58 - 10, w/2 - 40, y0 + len(title_lines)*58 - 10, P(color, "stroke", 3))
    if sub: text(c, sub, 17, h/2 - 52, "type", 38, color)
    c.restore()

def folder(c, cx, cy, w, h, tab_text, s=1.0, rot=0.0, color=INK, open_p=0.0):
    c.save(); c.translate(cx, cy); c.rotate(rot); c.scale(s, s)
    c.save(); c.translate(8, 12); c.drawRect(skia.Rect.MakeXYWH(-w/2, -h/2, w, h), P(0x2A1D10, alpha=0.28, blur=9)); c.restore()
    back = skia.Path(); back.moveTo(-w/2, -h/2 + 36); back.lineTo(-w/2, h/2); back.lineTo(w/2, h/2); back.lineTo(w/2, -h/2 + 36); back.lineTo(-w/2 + 330, -h/2 + 36); back.lineTo(-w/2 + 300, -h/2); back.lineTo(-w/2 + 30, -h/2); back.lineTo(-w/2 + 0, -h/2 + 36); back.close()
    c.drawPath(back, P(0xFFD8C08A)); ink(c, back, 4.5, color)
    text(c, tab_text, -w/2 + 168, -h/2 + 16, "type", 36, color, "c") if False else None
    c.restore()

def window(c, cx, cy, w, h, title="", color=INK, fill=PAPER2):
    """Hand-inked chat window frame."""
    c.save(); c.translate(cx, cy)
    c.save(); c.translate(6, 10); c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-w/2, -h/2, w, h), 14, 14), P(0x2A1D10, alpha=0.28, blur=9)); c.restore()
    rr = rect_path(-w/2, -h/2, w, h, 14); c.drawPath(rr, P(fill)); ink(c, rr, 4.5, color)
    c.drawLine(-w/2, -h/2 + 52, w/2, -h/2 + 52, P(color, "stroke", 3.5))
    for i in range(3): c.drawCircle(-w/2 + 30 + i*28, -h/2 + 26, 8, P(color, "stroke", 3))
    if title: text(c, title, 0, -h/2 + 27, "type", 36, color)
    c.restore()

def gear(c, x, y, r, rot, color=INK, alpha=1.0, teeth=10):
    p = skia.Path()
    for i in range(teeth*2):
        a0 = rot + i*math.pi/teeth; rr = r if i % 2 == 0 else r*0.78
        a1 = rot + (i+1)*math.pi/teeth
        if i == 0: p.moveTo(x + rr*math.cos(a0), y + rr*math.sin(a0))
        p.lineTo(x + rr*math.cos(a0), y + rr*math.sin(a0)); p.lineTo(x + rr*math.cos(a0 + math.pi/teeth*0.6), y + rr*math.sin(a0 + math.pi/teeth*0.6))
    p.close(); c.drawPath(p, P(PAPER3, alpha=alpha)); c.drawPath(p, P(color, "stroke", 3.6, alpha, rough=(10, 0.8)))
    c.drawCircle(x, y, r*0.3, P(color, "stroke", 3.4, alpha))

def scales(c, x, y, s=1.0, tilt=0.0, color=INK, alpha=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawLine(0, 120, 0, -70, P(color, "stroke", 6, alpha)); c.drawLine(-60, 120, 60, 120, P(color, "stroke", 6, alpha))
    c.save(); c.translate(0, -70); c.rotate(tilt)
    c.drawLine(-120, 0, 120, 0, P(color, "stroke", 6, alpha))
    for sx in (-1, 1):
        c.drawLine(sx*120, 0, sx*120 - 40, 90, P(color, "stroke", 3, alpha)); c.drawLine(sx*120, 0, sx*120 + 40, 90, P(color, "stroke", 3, alpha))
        pan = skia.Path(); pan.moveTo(sx*120 - 54, 90); pan.cubicTo(sx*120 - 40, 124, sx*120 + 40, 124, sx*120 + 54, 90); pan.close()
        c.drawPath(pan, P(PAPER3, alpha=alpha)); c.drawPath(pan, P(color, "stroke", 4, alpha))
    c.restore(); c.restore()

def heart(c, x, y, s=1.0, color=VERM, alpha=1.0, stroke=True):
    p = skia.Path(); p.moveTo(0, 30); p.cubicTo(-60, -10, -40, -50, 0, -22); p.cubicTo(40, -50, 60, -10, 0, 30)
    c.save(); c.translate(x, y); c.scale(s, s)
    if stroke: c.drawPath(p, P(color, "stroke", 5, alpha, rough=(10, 1)));
    else: c.drawPath(p, P(color, alpha=alpha))
    c.restore()

def padlock(c, x, y, s=1.0, color=INK, alpha=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    sh = skia.Path(); sh.moveTo(-26, -40); sh.cubicTo(-26, -90, 26, -90, 26, -40); c.drawPath(sh, P(color, "stroke", 9, alpha))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-44, -44, 88, 70), 10, 10), P(PAPER3, alpha=alpha)); c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-44, -44, 88, 70), 10, 10), P(color, "stroke", 5, alpha))
    c.drawCircle(0, -14, 8, P(color, alpha=alpha)); c.drawLine(0, -14, 0, 6, P(color, "stroke", 5, alpha))
    c.restore()

def sparkle(c, x, y, r, rot=0, color=INK, alpha=1.0, w=4):
    c.save(); c.translate(x, y); c.rotate(rot)
    p = skia.Path(); p.moveTo(0, -r); p.quadTo(0, 0, r, 0); p.quadTo(0, 0, 0, r); p.quadTo(0, 0, -r, 0); p.quadTo(0, 0, 0, -r); p.close()
    c.drawPath(p, P(color, "stroke", w, alpha)); c.restore()

def crescent(c, x, y, r, color=INK, alpha=1.0):
    p = skia.Path(); p.addCircle(x, y, r); q = skia.Path(); q.addCircle(x + r*0.45, y - r*0.2, r*0.85)
    res = skia.Op(p, q, skia.PathOp.kDifference_PathOp)
    c.drawPath(res, P(PAPER2, alpha=alpha)); c.drawPath(res, P(color, "stroke", 4, alpha, rough=(10, 1)))

def clock(c, x, y, r, t_hand=0.0, color=INK, alpha=1.0):
    c.drawCircle(x, y, r, P(PAPER2, alpha=alpha)); c.drawCircle(x, y, r, P(color, "stroke", 5, alpha, rough=(12, 1)))
    for i in range(12):
        a = i*math.pi/6; c.drawLine(x + (r-4)*math.cos(a), y + (r-4)*math.sin(a), x + (r-14)*math.cos(a), y + (r-14)*math.sin(a), P(color, "stroke", 3, alpha))
    a = t_hand*2*math.pi - math.pi/2; c.drawLine(x, y, x + r*0.72*math.cos(a), y + r*0.72*math.sin(a), P(color, "stroke", 4.5, alpha))
    a2 = a/12 - math.pi/2*0 ; c.drawLine(x, y, x + r*0.45*math.cos(a/12), y + r*0.45*math.sin(a/12), P(color, "stroke", 6, alpha))

def sparkles_burst(c, x, y, p, n=9, r0=30, r1=120, color=VERM, w=5):
    if p <= 0 or p >= 1: return
    for i in range(n):
        a = i*2*math.pi/n + 0.3; rr0 = lerp(r0, r1*0.6, e_out(p)); rr1 = lerp(r0 + 10, r1, e_out(p))
        c.drawLine(x + rr0*math.cos(a), y + rr0*math.sin(a), x + rr1*math.cos(a), y + rr1*math.sin(a), P(color, "stroke", w*(1 - p), 1 - p*0.6))

def curtain(c, cx, cy, w, h, open_p, color=INK, fill=VERM, back=True):
    """Stage proscenium: two curtains that part. (cx,cy)=centre."""
    c.save(); c.translate(cx, cy)
    if back: c.drawRect(skia.Rect.MakeXYWH(-w/2, -h/2, w, h), P(PAPER3)); ink(c, rect_path(-w/2, -h/2, w, h), 5, color)
    cw = w/2 * (1 - 0.85*e_io(open_p))
    for sx in (-1, 1):
        x0 = -w/2 if sx < 0 else w/2 - cw
        c.drawRect(skia.Rect.MakeXYWH(x0, -h/2, cw, h), P(fill, alpha=0.92))
        for k in range(1, 6):
            xx = x0 + cw*k/6; c.drawLine(xx, -h/2, xx, h/2, P(0x7A1A0C, "stroke", 3, 0.5))
        ink(c, rect_path(x0, -h/2, cw, h), 4, color)
    c.drawLine(-w/2 - 20, -h/2, w/2 + 20, -h/2, P(color, "stroke", 9))
    c.restore()

def ticket(c, cx, cy, w, h, lines, rot=0.0, color=INK, kind="type", size=36, fill=PAPER2):
    c.save(); c.translate(cx, cy); c.rotate(rot)
    c.save(); c.translate(5, 8); c.drawRect(skia.Rect.MakeXYWH(-w/2, -h/2, w, h), P(0x2A1D10, alpha=0.28, blur=7)); c.restore()
    c.drawPath(deckle_path(w, h, 5), P(fill)); c.drawPath(deckle_path(w, h, 5), P(INK2, "stroke", 1.8, 0.85))
    n = len(lines); y0 = -(n-1)*size*0.62
    for i, (s_, k_, sz_, col_) in enumerate(lines):
        text(c, s_, 0, y0 + i*size*1.25, k_ or kind, sz_ or size, col_ or color)
    c.restore()
