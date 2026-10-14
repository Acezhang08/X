# -*- coding: utf-8 -*-
"""Segments 0-1: the hook, and how the ELIZA trick works."""
import math, random
import skia
from lib import *
from props import *
from timeline import Timeline

T = Timeline()
S, E, Wd = T.s, T.e, T.w
CAM = lambda t: (960, 540)

def lerp_pts(a, b, x): return (lerp(a[0], b[0], x), lerp(a[1], b[1], x))

def prefix_x(s, n, kind, size): return tw(s[:n], kind, size)

# ------------------------------------------------------------------------------------------------
# shared bits
def desk(c, t, a, x0=330, x1=1590, y=700, dur=1.0):
    p = prog(t, a, a + dur)
    if p <= 0: return
    path = skia.Path(); path.moveTo(x0, y); path.lineTo(x1, y)
    draw_on(c, path, e_out(p), 7)
    if p > 0.5:
        q = prog(t, a + 0.5, a + 1.3)
        c.save(); c.clipRect(skia.Rect.MakeXYWH(x0, y + 4, (x1 - x0) * e_out(q), 120))
        hatch(c, rect_path(x0, y + 4, x1 - x0, 110), -50, 14, 2.2, INK2, 0.45); c.restore()

def door(c, t, a, cx=1700, base=700, open_p=0.0):
    """Door frame at right; open_p opens the door leaf."""
    q = e_out(prog(t, a, a + 0.8))
    if q <= 0: return
    c.save(); c.translate(cx, base)
    frame = rect_path(-70, -330, 140, 330)
    c.drawPath(frame, P(PAPER3, alpha=0.8 * q)); ink(c, frame, 5, INK, q)
    c.drawRect(skia.Rect.MakeXYWH(-58, -318, 116, 318), P(0xFF2A1D10, alpha=0.78 * q))
    lw = 116 * (1 - 0.7 * e_io(open_p))
    leaf = poly_path([(-58, -318), (-58 + lw, -318 + 20 * open_p), (-58 + lw, -20 * open_p), (-58, 0)])
    c.drawPath(leaf, P(PAPER2, alpha=q)); ink(c, leaf, 4, INK, q)
    c.drawCircle(-58 + lw - 14, -150, 6, P(INK, alpha=q))
    c.restore()

def quote_slip(c, t, a, b, cx, cy, w, h, quote, source, size=44, rot=-1.2, hl=None, seed=3, hl_t=None, kind="serifi", hl_times=None, scan=None):
    """Quote card: vermilion opening mark, quote text (wrapped), source in typewriter. hl = list of phrases to underline."""
    with slip(c, cx, cy, w, h, rot, t, a, b, seed=seed, slide=(0, -110)) as v:
        if not v: return
        text(c, "“", -w/2 + 70, -h/2 + 78, "serif", 150, VERM, deco=True)
        lines = wrap(quote, kind, size, w - 170)
        n = len(lines); lh = size * 1.28
        y0 = -h/2 + 80 + (0)
        y0 = -(n - 1) * lh / 2 - 22
        ys = []
        for i, ln in enumerate(lines):
            text(c, ln, -w/2 + 120, y0 + i * lh, kind, size, INK, "l"); ys.append((ln, y0 + i * lh))
        if hl and (hl_t is not None or hl_times):
            for k, ph in enumerate(hl):
                t_k = hl_times[k] if hl_times else hl_t + k*0.5
                for ln, yy in ys:
                    if ph in ln:
                        i0 = ln.index(ph); x0 = -w/2 + 120 + tw(ln[:i0], kind, size); x1 = x0 + tw(ph, kind, size)
                        underline(c, x0, x1, yy + size*0.62, prog(t, t_k, t_k + 0.5), VERM, 5, seed=k + 3)
        if scan and scan[0] <= t <= scan[1]:
            allw = []
            for ln, yy in ys:
                off = 0
                for wd in ln.split(" "):
                    allw.append((ln, off, wd, yy)); off += len(wd) + 1
            f = prog(t, scan[0], scan[1]); idx = min(len(allw) - 1, int(f * len(allw)))
            ln, off, wd, yy = allw[idx]
            wx = -w/2 + 120 + tw(ln[:off], kind, size); ww = tw(wd, kind, size)
            c.drawRect(skia.Rect.MakeXYWH(wx - 5, yy - size*0.62, ww + 10, size*1.15), P(WASH, alpha=0.28))
        text(c, source, w/2 - 40, h/2 - 38, "type", 36, INK2, "r")

def crowd(c, t, a, cols, rows, x0, y0, dx, dy, s=1.0, seed=1, dur=2.2, color=INK, fadeout=None):
    r = random.Random(seed)
    for j in range(rows):
        for i in range(cols):
            k = (j * cols + i) / (cols * rows)
            ta = a + k * dur * 0.8
            q = e_out(prog(t, ta, ta + 0.35))
            if q <= 0: continue
            al = q * (1 - (e_io(prog(t, fadeout[0], fadeout[1])) * 0.82 if fadeout else 0))
            small_person(c, x0 + i * dx + (j % 2) * dx / 2, y0 + j * dy + 12 * (1 - q), s * (0.7 + 0.3 * q), color, al)

def chat_bubbles_pop(c, t, a, pts, size=1.0):
    r = random.Random(7)
    for i, (x, y) in enumerate(pts):
        ta = a + i * 0.28
        q = prog(t, ta, ta + 0.9)
        if q <= 0 or q >= 1: continue
        al = math.sin(math.pi * q)
        c.save(); c.translate(x, y - 40 * q); c.scale(size, size)
        rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-34, -22, 68, 44), 16, 16)
        c.drawRRect(rr, P(PAPER2, alpha=al)); c.drawRRect(rr, P(INK, "stroke", 3, al))
        for k in range(3): c.drawCircle(-14 + k*14, 0, 4, P(INK, alpha=al))
        c.restore()

# ================================================================================================
# SEGMENT 0 : hook
# ================================================================================================
def draw0(c, t):
    t_office_end = S("0.5") - 0.35
    # ---- office scene (0.1 - 0.4) ----
    with fade(c, t, 1.2, t_office_end, 0.5) as v:
        if v:
            fade_text(c, "MIT, mid-1960s", 960, 136, t, 1.5, "hand", 64, INK2, "c", dur=0.9, b=S("0.4") - 0.3)
            desk(c, t, 1.5)
            # man (left? right) - woman left, man right
            if t > 2.1:
                q = e_out(prog(t, 2.1, 2.9))
                person2(c, 640, 700, 1.0, "woman", alpha=q)
            # woman moves aside when quote appears? (stays)
            manx = 1330
            if t > 2.6:
                q = e_out(prog(t, 2.6, 3.3))
                leave = e_io(prog(t, Wd("0.3", "leave") + 0.2, Wd("0.3", "leave") + 2.2))
                mx = lerp(manx, 1700, leave)
                person2(c, mx, 700, 1.0, "man", glasses=True, alpha=q * (1 - 0.0))
            # terminal in front of woman
            if t > 3.0:
                q = e_out(prog(t, 3.0, 3.8))
                typing = prog(t, Wd("0.3", "Then") - 0.1, E("0.3"))
                lines = [0.9, 0.6, 0.8, 0.5, 0.75, 0.4]
                nl = int(typing * len(lines) * 1.0) if t > Wd("0.3", "Then") - 0.1 else 0
                terminal(c, 900, 700, 0.95, alpha=q, key_t=(t if Wd("0.3", "Then") - 0.1 < t < E("0.3") else None), paper_lines=lines[:nl], paper_h=0.9)
            # printouts stack (the program) on the desk, grows while 'build'
            if t > 3.4:
                n = 1 + int(prog(t, 3.6, 8.6) * 5)
                for i in range(n):
                    c.save(); c.translate(1180 + i * 3, 686 - i * 13); c.rotate(-2 + i * 0.7)
                    c.drawRect(skia.Rect.MakeXYWH(-80, -10, 160, 14), P(PAPER2)); c.drawRect(skia.Rect.MakeXYWH(-80, -10, 160, 14), P(INK, "stroke", 2.4))
                    c.restore()
                pass
            # calendar flips for "months"
            tm = Wd("0.1", "months") - 1.2
            if t > tm:
                months = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN"]
                k = min(len(months) - 1, int((t - tm) / 0.38))
                al = e_out(prog(t, tm, tm + 0.3)) * (1 - e_in(prog(t, S("0.2") + 1.0, S("0.2") + 1.5)))
                if al > 0.01:
                    c.save(); c.saveLayerAlpha(skia.Rect.MakeXYWH(1420, 100, 440, 400), int(255 * al))
                    calendar_page(c, 1610, 290, months[k], "", 0.9, rot=3)
                    c.restore()
            # 0.2 thought bubble: she knew it was just a program
            ta, tb = S("0.2"), E("0.2") + 1.6
            if ta <= t <= tb + 0.5:
                al = e_out(prog(t, ta, ta + 0.4)) * (1 - e_in(prog(t, tb, tb + 0.4)))
                bubble(c, 460, 360, 560, 120, tail=(1, 1), alpha=al, thought=True)
                if al > 0.05: text(c, "just a program", 460, 360, "type", 44, INK, alpha=al)
            # door + man leaves
            door(c, t, Wd("0.3", "asked") - 0.5, 1700, 700, open_p=prog(t, Wd("0.3", "leave"), Wd("0.3", "leave") + 1.0))
            # quote slip
            quote_slip(c, t, Wd("0.3", "After") + 0.1, S("0.4") - 0.3, 960, 330, 1360, 250,
                       "After only a few interchanges with it, she asked me to leave the room.",
                       "J. Weizenbaum, Computer Power and Human Reason (1976), p. 6", 46, hl=["asked me to leave the room"], hl_t=Wd("0.3", "asked") + 0.3)
            # 0.4 privacy stamp
            ta = S("0.4") + 0.15
            stamp(c, "PRIVACY", 900, 240, t, ta, VERM, -5, 96, pad=(40, 22))
            fade_text(c, "with a computer program", 900, 335, t, S("0.4") + 1.55, "type", 44, INK, "c")
    # ---- ELIZA title (0.5) ----
    ta = S("0.5") + 0.1
    with fade(c, t, ta, S("0.6") - 0.2, 0.5, bleed=True) as v:
        if v:
            fade_text(c, "ELIZA", 960, 300, t, ta + 0.1, "serif", 260, INK, "c", dur=0.9, rise=0)
            underline(c, 560, 1360, 422, prog(t, ta + 0.7, ta + 1.4), VERM, 8)
            stamp(c, "UNDERSTOOD: NOTHING", 960, 540, t, Wd("0.5", "understood") + 0.1, VERM, -3, 54, pad=(34, 18))
            # words -> rules -> question
            tw0 = Wd("0.5", "rules") - 0.9
            y = 760
            boxes = [(430, "your words", "serif"), (960, "RULES", "mono"), (1490, "a question", "serif")]
            for i, (x, s_, kd) in enumerate(boxes):
                ba = tw0 + i * 0.7
                q = e_out(prog(t, ba, ba + 0.45))
                if q > 0:
                    w_ = 420 if kd == "serif" else 300
                    c.save(); c.translate(x, y); c.scale(0.9 + 0.1 * q, 0.9 + 0.1 * q)
                    c.saveLayerAlpha(skia.Rect.MakeXYWH(-250, -80, 500, 160), int(255 * q))
                    c.drawPath(rect_path(-w_/2, -52, w_, 104, 10), P(PAPER2)); ink(c, rect_path(-w_/2, -52, w_, 104, 10), 4.5)
                    text(c, s_, 0, 0, kd, 54 if kd == "serif" else 48, VERM if kd == "mono" else INK)
                    c.restore(); c.restore()
            for i, (x0, x1) in enumerate(((650, 800), (1125, 1280))):
                pa = tw0 + 0.45 + i * 0.7
                a_ = bez((x0, y), ((x0 + x1) / 2, y - 8), (x1, y))
                draw_on(c, a_, e_out(prog(t, pa, pa + 0.5)), 6, INK, 1.0, True, True, 28)
    # ---- Weizenbaum + decades (0.6) ----
    ta = S("0.6") + 0.1
    with fade(c, t, ta, S("0.7") - 0.25, 0.5, bleed=True) as v:
        if v:
            person2(c, 470, 700, 1.05, "man", glasses=True)
            label(c, "JOSEPH WEIZENBAUM", 470, 790, t, ta + 0.5, INK, 40, "type")
            fade_text(c, "1966", 940, 440, t, ta + 0.6, "type", 70, INK, "c")
            path = skia.Path(); path.moveTo(1040, 470); path.lineTo(1660, 470)
            draw_on(c, path, e_out(prog(t, ta + 1.0, ta + 3.8)), 7, INK, 1.0, True, True, 40)
            fade_text(c, "decades of warning", 1360, 400, t, Wd("0.6", "decades") - 0.1, "hand", 74, VERM, "c")
            for i in range(9):
                tx = 1080 + i * 66
                if t > ta + 1.4 + i * 0.26: c.drawLine(tx, 454, tx, 486, P(INK, "stroke", 4))
    # ---- crowd (0.7) ----
    ta = S("0.7") + 0.1
    with fade(c, t, ta - 0.1, S("0.8") + 0.2, 0.5) as v:
        if v:
            fade_text(c, "hundreds of millions · every week", 960, 140, t, ta + 0.2, "type", 50, INK2, "c")
            crowd(c, t, ta, 18, 6, 130, 290, 96, 96, 1.0, 1, 2.4, INK, fadeout=(S("0.8") + 0.1, S("0.8") + 1.0))
            chat_bubbles_pop(c, t, ta + 0.6, [(300, 250), (700, 270), (1100, 250), (1500, 270), (1760, 260), (520, 250), (900, 245), (1300, 262)], 1.1)
    # ---- title (0.8) ----
    ta = S("0.8") + 0.2
    with fade(c, t, ta, None, 0.7, bleed=True) as v:
        if v:
            fade_text(c, "the first chatbot", 960, 470, t, ta + 0.1, "serif", 150, INK, "c", dur=0.9, rise=0)
            underline(c, 380, 1540, 556, prog(t, ta + 0.8, ta + 1.5), VERM, 8)
            fade_text(c, "and the warning that came with it", 960, 690, t, S("0.8") + Wd("0.8", "warning") - S("0.8"), "hand", 90, INK2, "c")

# ================================================================================================
# SEGMENT 1 : how the trick works
# ================================================================================================
TR = [  # (text, who)
    ("HOW DO YOU DO. PLEASE TELL ME YOUR PROBLEM", "E"),
    ("Men are all alike.", "H"), ("IN WHAT WAY", "E"),
    ("They're always bugging us about", "H"), ("something or other.", "h"), ("CAN YOU THINK OF A SPECIFIC EXAMPLE", "E"),
    ("Well, my boyfriend made me come here.", "H"), ("YOUR BOYFRIEND MADE YOU COME HERE", "E"),
    ("He says I'm depressed much of the time.", "H"), ("I AM SORRY TO HEAR YOU ARE DEPRESSED", "E"),
]
TR_TIMES = None
def tr_times():
    """when each transcript row starts typing"""
    a = {}
    a[0] = S("1.3") + 0.5
    a[1] = S("1.3") + 3.6        # Men are all alike. (typed during 1.3)
    a[2] = a[1] + 1.5
    a[3] = S("1.4") + 2.6
    a[4] = a[3] + 1.5
    a[5] = a[4] + 1.0
    a[6] = S("1.5") + 0.2
    a[7] = Wd("1.5", "replies") + 0.1
    a[8] = S("1.6") + 0.2
    a[9] = Wd("1.6", "ELIZA") + 0.2
    return a

TCX, TCY, TW_, TH_, TSZ, TLH = 740, 490, 1280, 760, 44, 56
def transcript(c, t, a_slip, b_slip):
    """The famous 1966 exchange on a typed sheet (left)."""
    cx, cy, w, h = TCX, TCY, TW_, TH_
    with slip(c, cx, cy, w, h, -0.6, t, a_slip, b_slip, seed=8, slide=(-200, 0), lined=False) as v:
        if not v: return
        text(c, "ELIZA \u00B7 Weizenbaum, CACM, Jan. 1966", 0, -h/2 + 54, "type", 40, INK2, deco=False)
        c.drawLine(-w/2 + 40, -h/2 + 92, w/2 - 40, -h/2 + 92, P(INK2, "stroke", 2.4))
        tt = tr_times()
        y = -h/2 + 160
        for i, (s_, who) in enumerate(TR):
            kind = "mono" if who == "E" else "monor"
            col = INK if who == "E" else INK2
            x0 = -w/2 + 60 + (34 if who == "h" else 0)
            ty = y + i * TLH
            if t >= tt[i]:
                typed(c, s_, x0, ty, t, tt[i], cps=34, kind=kind, size=TSZ, color=col, align="l", cursor=True, cursor_color=VERM)

ROW = {}

def hl_word(c, t, a, row_idx, phrase, color=VERM, p_dur=0.5, w=5):
    """underline a phrase within a transcript row (call inside the slip's local coords)"""
    s_, who = TR[row_idx]
    if phrase not in s_ or row_idx not in ROW: return
    i0 = s_.index(phrase); kind = "mono" if who == "E" else "monor"
    x0, ty = ROW[row_idx]
    xa = x0 + tw(s_[:i0], kind, TSZ); xb = xa + tw(phrase, kind, TSZ)
    underline(c, xa, xb, ty + 28, prog(t, a, a + p_dur), color, w, seed=row_idx)

def tile(c, x, y, s_, kind="mono", size=40, color=INK, fill=PAPER2, alpha=1.0, w=None, rot=0.0, ring=None):
    w = w or (tw(s_, kind, size) + 36); h = size + 30
    c.save(); c.translate(x, y); c.rotate(rot)
    if alpha < 1: c.saveLayerAlpha(skia.Rect.MakeXYWH(-w/2-30, -h/2-30, w+60, h+60), int(255*alpha))
    c.save(); c.translate(3, 5); c.drawPath(rect_path(-w/2, -h/2, w, h, 6), P(0x2A1D10, alpha=0.25, blur=4)); c.restore()
    c.drawPath(rect_path(-w/2, -h/2, w, h, 6), P(fill)); ink(c, rect_path(-w/2, -h/2, w, h, 6), 3.4, ring or INK)
    text(c, s_, 0, 0, kind, size, color)
    if alpha < 1: c.restore()
    c.restore()
    return w

def draw1(c, t):
    # ---- 1.1 mainframe + terminal (48.7 - 57) ----
    a1 = S("1.1") - 0.8; b1 = S("1.2") - 0.1
    with fade(c, t, a1, b1, 0.5, bleed=True) as v:
        if v:
            mainframe(c, 560, 850, 1.3, t=t)
            fade_text(c, "IBM 7094 · MIT", 520, 390, t, a1 + 0.9, "type", 46, INK, "c")
            ty = Wd("1.1", "typed back")
            lines = [0.9, 0.7, 0.85, 0.5, 0.8, 0.6]
            nl = int(prog(t, ty - 0.2, E("1.1") + 0.2) * 6)
            terminal(c, 1400, 850, 1.3, key_t=t if t > Wd("1.1", "sat") else None, paper_lines=lines[:nl], paper_h=0.9)
            fade_text(c, "typewriter terminal", 1400, 270, t, Wd("1.1", "typewriter") - 0.1, "type", 46, INK, "c")
            # cable with travelling pulses
            cab = bez((880, 760), (1060, 900), (1180, 790))
            draw_on(c, cab, e_out(prog(t, a1 + 1.2, a1 + 2.2)), 5, INK2, 1.0)
            if t > a1 + 2.2:
                for k in range(3):
                    f = ((t * 0.5) + k / 3.0) % 1.0
                    px, py, _ = pos_on(cab, f if (int(t) % 2 == 0) else 1 - f)
                    c.drawCircle(px, py, 9, P(VERM))
            fade_text(c, "you typed. it typed back.", 960, 160, t, Wd("1.1", "You sat") - 0.1, "hand", 70, INK2, "c")
    # ---- 1.2 first line on a big slip ----
    a2, b2 = S("1.2") + 0.1, S("1.3") + 0.2
    with slip(c, 960, 470, 1280, 330, -0.8, t, a2, b2, seed=9, slide=(0, -130)) as v:
        if v:
            text(c, "its first line", 0, -110, "hand", 56, INK2)
            typed(c, "HOW DO YOU DO. PLEASE TELL ME", -590, -20, t, a2 + 0.5, 18, "mono", 50, INK, "l", True, VERM)
            typed(c, "YOUR PROBLEM", -590, 62, t, a2 + 0.5 + 29 / 18, 18, "mono", 50, INK, "l", True, VERM)
    # ---- 1.3-1.7 transcript ----
    ROW.clear()
    ta, tb = S("1.3") + 0.15, S("1.8") - 0.2
    transcript(c, t, ta, tb)
    # (annotations drawn in screen space over the slip - transcript is at (600,490), rot -0.6)
    if ta < t < tb + 0.6:
        c.save(); c.translate(TCX, TCY); c.rotate(math.radians(-0.6))
        # row positions are relative to slip centre; underline highlights
        w_, h_ = TW_, TH_
        c.save(); c.translate(0, 0)
        # recompute ROW inside local coords by replicating transcript layout
        y = -h_/2 + 160
        for i, (s_, who) in enumerate(TR):
            x0 = -w_/2 + 60 + (34 if who == "h" else 0); ROW[i] = (x0, y + i * TLH)
        # 1.4: underline Men are all alike / IN WHAT WAY
        hl_word(c, t, Wd("1.4", "men"), 1, "Men are all alike.")
        hl_word(c, t, Wd("1.4", "in what way"), 2, "IN WHAT WAY")
        hl_word(c, t, Wd("1.5", "boyfriend") - 0.1, 6, "my boyfriend made me come here", p_dur=0.7)
        hl_word(c, t, Wd("1.5", "your boyfriend") + 0.1, 7, "YOUR BOYFRIEND MADE YOU COME HERE", p_dur=0.8)
        hl_word(c, t, Wd("1.6", "depressed"), 8, "depressed")
        hl_word(c, t, Wd("1.6", "sorry"), 9, "SORRY TO HEAR")
        c.restore(); c.restore()
        # lowercase/capitals tags
        if ta + 4 < t < S("1.4"):
            fade_text(c, "person: lowercase", 1590, 330, t, Wd("1.3", "lowercase") - 0.2, "hand", 62, INK2, "c", b=S("1.4") - 0.2)
            fade_text(c, "ELIZA: CAPITALS", 1590, 440, t, Wd("1.3", "capital") - 0.4, "hand", 62, VERM, "c", b=S("1.4") - 0.2)
    # right-hand side: pairs (1.4-1.6) as hand notes
    for lid, txt, yy in (("1.4", "echoes “men”", 360), ("1.5", "my becomes your", 520), ("1.6", "“depressed” back", 680)):
        if S(lid) + 1.0 < t < S("1.8") - 0.3:
            fade_text(c, txt, 1590, yy, t, S(lid) + 1.4, "hand", 60, INK2, "c", b=S("1.7") - 0.1)
    # 1.7 echo arrows between human and ELIZA rows (screen space)
    if S("1.7") - 0.1 < t < S("1.8") - 0.2:
        q = prog(t, S("1.7") + 0.2, S("1.7") + 1.2)
        # arrows on right edge of the sheet from human row to ELIZA row
        ys = [(1, 2), (6, 7), (8, 9)]
        for k, (r1, r2) in enumerate(ys):
            y1 = TCY - TH_/2 + 160 + r1 * TLH + 4; y2 = TCY - TH_/2 + 160 + r2 * TLH + 4
            xe = 1250 + k * 20
            path = bez((1190, y1), (xe + 80, (y1 + y2) / 2), (1190, y2))
            draw_on(c, path, e_out(prog(t, S("1.7") + 0.3 + k * 0.5, S("1.7") + 1.0 + k * 0.5)), 5, VERM, 1.0, True, True, 26)
        fade_text(c, "her words,", 1580, 400, t, S("1.7") + 0.4, "hand", 68, VERM, "c")
        fade_text(c, "turned around", 1580, 490, t, S("1.7") + 1.6, "hand", 68, VERM, "c")
    # ---- 1.8 step 1 : keyword ----
    a8, b8 = S("1.8") + 0.05, S("1.9") - 0.0
    with fade(c, t, a8, S("1.10") - 0.1, 0.5) as v:
        if v:
            # step badge
            if t < S("1.10") - 0.2:
                pass
    # step badge persistent for 1.8-1.12 handled per step below
    step1(c, t); step2(c, t); step3(c, t); step4(c, t); step5(c, t); step6(c, t)

def badge(c, t, a, b, n, title):
    with fade(c, t, a, b, 0.4) as v:
        if v:
            stamp(c, f"STEP {n}", 330, 150, t, a + 0.1, VERM, -3, 56, pad=(26, 14))
            fade_text(c, title, 800, 150, t, a + 0.3, "serif", 70, INK, "l")

def step1(c, t):
    a, b = S("1.8") + 0.1, S("1.9") - 0.15
    badge(c, t, a, b, 1, "find a keyword")
    with fade(c, t, a, b, 0.4, bleed=True) as v:
        if not v: return
        sent = "They're always bugging us about something or other."
        sz = 50
        sx = 960 - tw(sent, "serif", sz) / 2
        with slip(c, 960, 360, 1500, 150, -0.5, t, a + 0.1, b - 0.2, seed=12, slide=(0, -90), tape=True) as v2:
            if v2:
                text(c, sent, 0, 0, "serif", sz, INK)
                # scanning highlight (moves word by word)
                words = sent.split(" ")
                pos = []
                off = 0
                for wd in words:
                    pos.append((off, wd)); off += len(wd) + 1
                tscan0, tscan1 = a + 0.6, a + 3.2
                if t > tscan0:
                    f = prog(t, tscan0, tscan1)
                    idx = min(len(words) - 1, int(f * len(words)))
                    i0, wd = pos[idx]
                    wx0 = -tw(sent, "serif", sz) / 2 + tw(sent[:i0], "serif", sz)
                    ww = tw(wd, "serif", sz)
                    if f < 1: c.drawRect(skia.Rect.MakeXYWH(wx0 - 6, -34, ww + 12, 66), P(WASH, alpha=0.30))
                # ring "always"
                i0 = sent.index("always"); wx0 = -tw(sent, "serif", sz) / 2 + tw(sent[:i0], "serif", sz); ww = tw("always", "serif", sz)
                ink_circle(c, wx0 + ww / 2, 2, ww / 2 + 36, 46, prog(t, a + 3.3, a + 4.0), VERM, 6)
        # keyword chips appear when the words are spoken
        chips = [("MOTHER", Wd("1.8", "Mother")), ("DREAM", Wd("1.8", "Dream")), ("ALIKE", Wd("1.8", "Alike")), ("ALWAYS", Wd("1.8", "Always"))]
        for i, (s_, ta) in enumerate(chips):
            q = e_back(prog(t, ta - 0.05, ta + 0.4))
            if q > 0:
                xx = 330 + i * 420; yy = 640
                if t >= S("1.9") - 0.0: pass
                tile(c, xx, yy, s_, "mono", 52, VERM if s_ == "ALWAYS" and t > Wd("1.8", "Always") else INK, w=330, alpha=min(1, q * 1.2))
        fade_text(c, "words the script knows", 960, 760, t, a + 0.8, "hand", 60, INK2, "c")
        if t > Wd("1.8", "Always") + 0.5:
            p = e_out(prog(t, Wd("1.8", "Always") + 0.5, Wd("1.8", "Always") + 1.3))
            arr = bez((1560 if False else 1280, 690), (1280, 760), (1280, 800))
            fade_text(c, "ELIZA: CAN YOU THINK OF A SPECIFIC EXAMPLE", 960, 850, t, Wd("1.8", "Always") + 0.6, "mono", 38, INK, "c")

def step2(c, t):
    a, b = S("1.9") + 0.3, S("1.10") - 0.15
    badge(c, t, a, b, 1, "every keyword has a rank")
    with fade(c, t, a, b, 0.4, bleed=True) as v:
        if not v: return
        items = [("ALIKE", 10), ("DREAM", 3), ("ALWAYS", 1), ("MOTHER", 0)]
        y0 = 330
        for i, (k, r) in enumerate(items):
            ya = a + 0.4 + i * 0.55
            q = e_out(prog(t, ya, ya + 0.5))
            if q <= 0: continue
            yy = y0 + i * 125
            tile(c, 440, yy, k, "mono", 52, INK, w=330, alpha=q)
            bw = 900 * r / 10.0 * q
            if bw > 2:
                c.drawRect(skia.Rect.MakeXYWH(660, yy - 36, bw, 72), P(VERM if k == "ALIKE" else INK2, alpha=0.85 if k == "ALIKE" else 0.55))
                ink(c, rect_path(660, yy - 36, bw, 72), 3.4)
            text(c, str(r), 660 + max(bw, 0) + 40, yy, "mono", 56, INK, "l", alpha=q)
        fade_text(c, "highest rank wins", 1300, 790, t, Wd("1.9", "highest") - 0.1, "hand", 80, VERM, "c")
        underline(c, 1030, 1570, 832, prog(t, Wd("1.9", "highest"), Wd("1.9", "highest") + 0.8), VERM, 6)

def step3(c, t):
    a, b = S("1.10") + 0.3, S("1.11") - 0.15
    badge(c, t, a, b, 2, "rebuild it from a template")
    with fade(c, t, a, b, 0.4, bleed=True) as v:
        if not v: return
        words = ["my", "boyfriend", "made", "me", "come", "here"]
        outw = ["YOUR", "BOYFRIEND", "MADE", "YOU", "COME", "HERE"]
        ws = [tw(x, "mono", 46) + 36 for x in words]; gap = 18
        total = sum(ws) + gap * 5; x = 960 - total / 2
        ty = 380; oy = 700
        pos = []
        for i, wd in enumerate(words):
            xc = x + ws[i] / 2; pos.append(xc); x += ws[i] + gap
            ta = a + 0.4 + i * 0.22
            tile(c, xc, ty, wd, "mono", 46, INK, w=ws[i], alpha=e_out(prog(t, ta, ta + 0.35)))
        fade_text(c, "cut apart", 960, 250, t, a + 0.3, "hand", 64, INK2, "c")
        # swap I/you words flips
        tsw = Wd("1.10", "swapping")
        for i, (wd, ow) in enumerate(zip(words, outw)):
            ta = a + 3.2 + i * 0.35
            q = e_io(prog(t, ta, ta + 0.6))
            swapped = wd in ("my", "me")
            if q <= 0: continue
            yy = lerp(ty, oy, q)
            # arrow path
            alp = 1.0
            ws2 = [tw(x_, "mono", 46) + 36 for x_ in outw]
            tot2 = sum(ws2) + gap * 5; xo = 960 - tot2 / 2 + sum(ws2[:i]) + gap * i + ws2[i] / 2
            xx = lerp(pos[i], xo, q)
            tile(c, xx, yy, ow if q > 0.55 else wd, "mono", 46, VERM if swapped else INK, w=lerp(ws[i], ws2[i], q), ring=VERM if swapped else None)
        fade_text(c, "swap  I for you,  my for your", 960, 860, t, tsw - 0.1, "hand", 70, VERM, "c")

def step4(c, t):
    a, b = S("1.11") + 0.3, S("1.12") - 0.15
    badge(c, t, a, b, 3, "no keyword? say anything")
    with fade(c, t, a, b, 0.4, bleed=True) as v:
        if not v: return
        stock = ["I AM NOT SURE I UNDERSTAND YOU FULLY", "PLEASE GO ON", "WHAT DOES THAT SUGGEST TO YOU", "DO YOU FEEL STRONGLY ABOUT DISCUSSING SUCH THINGS"]
        fade_text(c, "(no keyword found)", 960, 270, t, a + 0.3, "hand", 66, INK2, "c")
        for i, s_ in enumerate(stock):
            ta = a + 0.9 + i * 0.5
            q = e_out(prog(t, ta, ta + 0.4))
            if q <= 0: continue
            hit = (i == 1) and t > Wd("1.11", "Please go on") - 0.1
            tile(c, 960, 380 + i * 118, s_, "mono", 38, VERM if hit else INK, w=1180, alpha=q, ring=VERM if hit else None)
        if t > Wd("1.11", "Please go on") - 0.1:
            fade_text(c, "fits anywhere", 960, 850, t, Wd("1.11", "Please go on"), "hand", 70, VERM, "c", dur=0.4)

def step5(c, t):
    a, b = S("1.12") + 0.3, S("1.13") - 0.1
    badge(c, t, a, b, 4, "a trick of memory")
    with fade(c, t, a, b, 0.4, bleed=True) as v:
        if not v: return
        # drawer
        c.save(); c.translate(960, 640)
        c.drawPath(rect_path(-240, -60, 480, 150, 8), P(PAPER3)); ink(c, rect_path(-240, -60, 480, 150, 8), 5)
        c.drawPath(rect_path(-70, 20, 140, 40, 6), P(PAPER2)); ink(c, rect_path(-70, 20, 140, 40, 6), 3.4)
        text(c, "MEMORY", 0, -22, "mono", 44, INK)
        c.restore()
        ts = Wd("1.12", "saves")
        # slip 'my ...' goes into drawer
        q = e_io(prog(t, ts - 0.4, ts + 0.9))
        if prog(t, a + 0.3, ts + 0.9) > 0 and q < 1:
            sx, sy = lerp(520, 960, q), lerp(330, 600, q)
            tile(c, sx, sy, "my …", "mono", 52, INK, w=220, alpha=1 - 0.7 * q, rot=-4)
            fade_text(c, "you say: my …", 520, 230, t, a + 0.4, "hand", 60, INK2, "c", b=ts + 0.8)
        tb = Wd("1.12", "brings") - 0.1
        fade_text(c, "…a few turns later", 1330, 330, t, Wd("1.12", "later") - 0.3, "hand", 64, INK2, "c")
        for i in range(3):
            if t > Wd("1.12", "later") - 0.1 + i * 0.3: c.drawCircle(1210 + i * 60, 420, 9, P(INK2))
        q2 = e_io(prog(t, tb + 0.4, tb + 1.4))
        if q2 > 0:
            sx, sy = lerp(960, 1330, q2), lerp(600, 560, q2) - 40 * math.sin(math.pi * q2)
            tile(c, sx, sy, "EARLIER YOU SAID YOUR …", "mono", 40, VERM, w=760, alpha=min(1, q2 * 1.5), rot=2, ring=VERM)
        fade_text(c, "as if it remembered", 960, 800, t, Wd("1.12", "remembered") - 0.3, "hand", 70, INK, "c")

def step6(c, t):
    # 1.13 : fewer than 70 entries ; 1.14 therapist ; 1.15 hidden
    a, b = S("1.13") + 0.05, S("1.14") - 0.15
    with fade(c, t, a, b, 0.4) as v:
        if v:
            cols, rows = 10, 7; n = 69
            for k in range(n):
                i, j = k % cols, k // cols
                ta = a + 0.2 + k * 0.045
                q = e_back(prog(t, ta, ta + 0.25))
                if q <= 0: continue
                xx = 280 + i * 84; yy = 240 + j * 84
                c.save(); c.translate(xx, yy); c.scale(q, q)
                c.drawPath(rect_path(-30, -30, 60, 60, 5), P(PAPER2)); ink(c, rect_path(-30, -30, 60, 60, 5), 3.2)
                for l in range(3): c.drawLine(-18, -12 + l * 12, 18 - (l % 2) * 8, -12 + l * 12, P(INK2, "stroke", 2.4, 0.7))
                c.restore()
            fade_text(c, "< 70", 1400, 400, t, a + 1.6, "type", 220, VERM, "c", dur=0.6, rise=0)
            fade_text(c, "entries in the printed script", 1420, 560, t, a + 2.1, "hand", 64, INK2, "c")
    a, b = S("1.14") + 0.1, S("1.15") - 0.1
    with fade(c, t, a, None, 0.5, bleed=True) as v:
        if v:
            hollow = t > S("1.15") + 0.1
            person2(c, 560, 740, 1.15, "man", alpha=0.0 if hollow else 1.0, glasses=True)
            if hollow:   # hollow dashed outline: nothing inside
                c.save(); c.translate(560, 740); c.scale(1.15, 1.15)
                head = skia.Path(); head.addOval(skia.Rect.MakeXYWH(-50, -254, 100, 128)); body = skia.Path(); body.moveTo(-136, 0); body.cubicTo(-136, -62, -104, -92, -56, -104); body.lineTo(56, -104); body.cubicTo(104, -92, 136, -62, 136, 0); body.close()
                for pth in (head, body): c.drawPath(pth, P(INK, "stroke", 4.5, dash=[16, 12]))
                text(c, "?", 0, -190, "type", 90, VERM)
                c.restore()
            person2(c, 1380, 740, 1.15, "woman", flip=True)
            bubble(c, 1130, 340, 640, 150, tail=(1, 1), thought=False, alpha=1.0) if False else None
            label(c, "DOCTOR script · a psychotherapist", 960, 150, t, a + 0.3, INK, 46, "type")
            tp = Wd("1.14", "pretend")
            if t > a + 0.8:
                # patient talks a lot (scribble lines), therapist says little
                bubble(c, 1250, 400, 520, 200, tail=(0.7, 1), alpha=e_out(prog(t, a + 0.8, a + 1.2)))
                for k in range(4):
                    ln = 420 - (k % 2) * 90
                    p_ = prog(t, a + 1.0 + k * 0.4, a + 1.5 + k * 0.4)
                    c.drawLine(1250 - ln / 2, 340 + k * 38, 1250 - ln / 2 + ln * p_, 340 + k * 38, P(INK2, "stroke", 4))
                bubble(c, 640, 410, 340, 110, tail=(-0.7, 1), alpha=e_out(prog(t, tp - 0.2, tp + 0.2)))
                if t > tp: text(c, "…", 640, 410, "type", 60, INK, alpha=e_out(prog(t, tp - 0.2, tp + 0.2)))
                fade_text(c, "pretends to know almost nothing", 960, 840, t, tp, "hand", 72, VERM, "c", b=S("1.15") + 0.0)
            stamp(c, "NOTHING INSIDE", 960, 830, t, S("1.15") + 0.45, VERM, -3, 64, pad=(36, 20))

REG = {0: (CAM, draw0), 1: (CAM, draw1)}
