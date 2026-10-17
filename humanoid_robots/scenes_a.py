# -*- coding: utf-8 -*-
"""Sheets 1-2: the stunt and the chore; Moravec's paradox."""
import math
import skia
from lib import *
from props import *
from timeline import Timeline

T = Timeline()
S, E = T.s, T.e
def Wd(lid, phrase, nth=0, after=False, off=0.0):
    try: return T.w(lid, phrase, nth, after) + off
    except ValueError: return S(lid) + off

def win(t, a, b, fi=.5, fo=.35):
    """alpha window with a quick fade-in at a and fade-out ending at b"""
    return ap(t, a, fi) * (1 - e_in(prog(t, b - fo, b)))

SRC_XY = (100, 850)
def src(c, s, t, a, b=1e9, alpha=1.0):
    source(c, s, SRC_XY[0], SRC_XY[1], win(t, a, b, .4, .3) * alpha)

REG = {}
def reg(k):
    def deco(fn): REG[k] = fn; return fn
    return deco

def ground(c, t, a, y=650, x0=100, x1=1820, d=.9):
    p = e_out(prog(t, a, a + d))
    line(c, x0, y, x0 + (x1 - x0) * p, y, 1, 3, LINE)
    if p > .3:
        for k in range(int((x1 - x0) / 36)):
            xx = x0 + 18 + k * 36
            if xx < x0 + (x1 - x0) * p: c.drawLine(xx, y + 4, xx - 14, y + 22, P(LINE, "stroke", 1.8, .45))

def flip_loop(c, t, a, period, gy, x0, s=1.0, alpha=1.0, once=False):
    """backflip replaying every `period` seconds, starting at a."""
    if t < a: return 0
    k = (t - a) / period
    u = k if (once and k < 1) else (1.0 if once else k % 1.0)
    ghosts = [i * .08 for i in range(1, 13)]
    draw_flip(c, clamp(u), gy, x0, s, True, ghosts, alpha=alpha)
    return u

def check_mark(c, t, a, x, y, s=44, w=10): check(c, x, y, s, e_out(prog(t, a, a + .35)), w, CYAN)

# ===================================================================================================
@reg(0)
def seg0(c, t):
    # ---- A: the two backflips (0.1, 0.2)
    A = win(t, 1.2, S("0.3") - .2, .3, .35)
    if A > 0:
        c.save()
        gy = 610
        ground(c, t, 1.2, gy)
        # 2017
        a17 = ap(t, 1.5, .5)
        text(c, "2017", 520, 690, "monob", 84, LINE, "c", a17 * A)
        text(c, "HUMANOID ROBOT", 520, 760, "mono", 36, CYAN, "c", ap(t, 2.0, .5) * A)
        flip_loop(c, t, 1.5, 4.6, gy, 520, .8, A)
        check_mark(c, t, 5.0, 720, 520)
        # 2024
        a24 = ap(t, S("0.2"), .5)
        text(c, "2024", 1300, 690, "monob", 84, LINE, "c", a24 * A)
        text(c, "UNITREE · ELECTRIC", 1300, 760, "mono", 36, CYAN, "c", ap(t, Wd("0.2", "electric"), .5) * A)
        flip_loop(c, t, S("0.2") + .3, 4.6, gy, 1300, .8, A * a24)
        check_mark(c, t, S("0.2") + 4.1, 1500, 520)
        c.restore()
    # ---- B/C: the shirt and the laundry robot (0.3, 0.4)
    a0 = S("0.3") - .1; a1 = S("0.5") - .15
    B = win(t, a0, a1, .5, .4)
    if B > 0:
        table_y = 712
        line(c, 200, table_y, 200 + 1520 * e_out(prog(t, a0, a0 + .8)), table_y, 1, 4, LINE, B)
        cx, cy, ss = 900, 590, 1.0
        ts = S("0.4"); t_stuck = Wd("0.4", "When it gets stuck"); t_res = t_stuck + 3.2
        f1 = e_io(prog(t, ts + .9, ts + 2.7)); f2 = e_io(prog(t, ts + 3.1, ts + 4.9))
        if t < t_res: f3 = .45 * e_io(prog(t, ts + 5.5, t_stuck - .1))
        else: f3 = .45 + .55 * e_io(prog(t, t_res, t_res + 2.0))
        stuck = prog(t, t_stuck, t_stuck + .3) * (1 - prog(t, t_res - .4, t_res))
        draw_shirt(c, cx, cy, ss, f1, f2, f3, alpha=ap(t, a0 + .2, .7) * B, falpha=.2)
        # grippers: sleeve tips first, then the hem corners
        ltip = (cx + ss * (-45 + (-147) * math.cos(f1 * math.pi)), cy + ss * -92)
        rtip = (cx + ss * (45 + 147 * math.cos(f2 * math.pi)), cy + ss * -92)
        hy = cy + ss * (40 + 90 * math.cos(f3 * math.pi))
        lhem = (cx - ss * 45, hy); rhem = (cx + ss * 45, hy)
        w3 = e_io(prog(t, ts + 5.0, ts + 5.5))
        L_ = (lerp(ltip[0], lhem[0], w3), lerp(ltip[1], lhem[1], w3)); R_ = (lerp(rtip[0], rhem[0], w3), lerp(rtip[1], rhem[1], w3))
        rb = ap(t, a0, .6)
        robot_arms(c, cx, 280 - 40 * (1 - rb), [L_, R_], (.5 * (1 - w3) * min(1, f1 * 3), .5 * (1 - w3) * min(1, f2 * 3)), s=.95, alpha=B)
        text(c, "FEB 2026", 330, 250, "monob", 44, LINE, "c", ap(t, ts + .2, .5) * B)
        text(c, "LAUNDRY ROBOT", 330, 305, "mono", 36, CYAN, "c", ap(t, ts + .5, .5) * B)
        pr = prog(t, Wd("0.4", "nearly eight"), Wd("0.4", "nearly eight") + 1.2)
        if pr > 0: text(c, "$" + roll(7999, pr), 330, 420, "monob", 72, LINE, "c", B)
        if stuck > 0:
            qmark(c, cx, cy - 10, 150 * (.6 + .4 * stuck), AMBER, stuck * B)
            hs = ap(t, t_stuck + .2, .6) * B
            person(c, 1560, 250, .8, headset=True, alpha=hs)
            text(c, "REMOTE SPECIALIST", 1560, 380, "mono", 36, CYAN, "c", hs)
            q = e_out(prog(t, t_stuck + .5, t_stuck + 1.5))
            draw_on(c, [(1480, 300), (1300, 360), (1040, 330)], q, 3, CYAN, hs, dash=[12, 9])
        if t > Wd("0.4", "for a few seconds") - .2:
            hs2 = ap(t, Wd("0.4", "for a few seconds") - .2, .5) * B
            text(c, "A FEW SECONDS AT A TIME", 1500, 480, "mono", 36, LINE, "c", hs2)
    # ---- D: stunt vs chore (0.5)
    a0 = S("0.5") - .1; a1 = S("0.6") - .1
    D = win(t, a0, a1, .45, .35)
    if D > 0:
        text(c, "BACKFLIP", 520, 130, "monob", 72, LINE, "c", D)
        text(c, "FOLD A SHIRT", 1360, 130, "monob", 72, LINE, "c", D)
        line(c, 960, 110, 960, 760, e_out(prog(t, a0, a0 + .6)), 3, LINE, D * .6, dash=[14, 10])
        # left: flip ghost strip (static poses) + check
        gy = 620
        for i, uu in enumerate([.08, .2, .34, .46, .58, .7, .84, .95]):
            q = flip_pose(uu, gy, 520 - 200 + i * 56)
            q["px"] = 330 + i * 78; q["py"] = gy - 330 * (4 * prog(uu, .27, .92) * (1 - prog(uu, .27, .92))) * .5 - (216 * .55) + (0 if True else 0)
            if ap(t, a0 + .3 + i * .1, .3) > 0:
                robot_side(c, s=.5, alpha=ap(t, a0 + .3 + i * .1, .3) * D * (1 if i == 7 else .75), **q)
        check_mark(c, t, a0 + 1.6, 520, 700, 50, 12)
        # right: shirt + child silhouette
        tr = Wd("0.5", "Folding laundry")
        ar = ap(t, tr, .5) * D
        draw_shirt(c, 1500, 450, .95, 0, 0, 0, alpha=ar, crumple=.25, seed=2)
        person(c, 1150, 520, .75, alpha=ar)
        text(c, "A CHILD", 1150, 640, "mono", 36, CYAN, "c", ar)
        if t > a1 - 1.4: stamp(c, "FAIL", 1500, 640, t, S("0.5") + 3.6, 54, -.1)
    # ---- E: why? (0.6)
    a0 = S("0.6") - .1; a1 = S("0.7") - .15
    Ew = win(t, a0, a1, .4, .3)
    if Ew > 0:
        text(c, "WHY?", 960, 330, "monob", 200 * (.9 + .1 * ap(t, a0, .5)), LINE, "c", Ew)
        for k in range(3):
            r = 120 + ((t - a0) * 160 + k * 100) % 250
            circle(c, 960, 330, r, 1, 2.5, CYAN, Ew * (1 - r / 520) * .7)
        text(c, "STUNT SOLVED", 520, 640, "mono", 36, CYAN, "c", ap(t, a0 + .5, .4) * Ew)
        text(c, "CHORE NOT", 1400, 640, "mono", 36, LINE, "c", ap(t, a0 + 1.0, .4) * Ew)
    # ---- F: 1988 (0.7)
    a0 = S("0.7") - .1
    F = ap(t, a0, .4)
    if F > 0:
        yr = prog(t, a0 + .2, a0 + 1.8)
        text(c, str(int(1900 + 88 * e_out(yr))), 960, 300, "monob", 240, LINE, "c", F)
        text(c, "THE BACKFLIP IS THE EASY PART", 960, 520, "monob", 60, CYAN, "c", 1, p=prog(t, Wd("0.7", "it says the backflip"), Wd("0.7", "easy part", after=True)))
        line(c, 240, 585, 240 + 1440 * e_out(prog(t, Wd("0.7", "easy part"), E("0.7") + .3)), 585, 1, 4, CYAN)

# ===================================================================================================
@reg(1)
def seg1(c, t):
    # ---- 1.1 Moravec, 1988, the book
    a0 = S("1.1"); a1 = S("1.2") - .05
    A = win(t, a0, a1, .4, .3)
    if A > 0:
        text(c, "1988", 960, 150, "monb" if False else "monob", 130, LINE, "c", A)
        person(c, 560, 470, 1.9, alpha=ap(t, a0 + .3, .7) * A)
        text(c, "HANS MORAVEC", 560, 700, "monob", 44, LINE, "c", ap(t, a0 + 1.2, .5) * A)
        text(c, "ROBOTICIST", 560, 752, "mono", 36, CYAN, "c", ap(t, a0 + 1.6, .5) * A)
        book_icon(c, 1330, 450, 2.2, alpha=ap(t, a0 + 2.6, .7) * A)
        text(c, "MIND CHILDREN", 1330, 705, "monob", 44, LINE, "c", ap(t, a0 + 3.0, .5) * A)
        text(c, "NOTICED SOMETHING STRANGE", 960, 770, "mono", 36, CYAN, "c", ap(t, Wd("1.1", "strange"), .5) * A * 0)
    # ---- 1.2 difficulty bars
    a0 = S("1.2") - .05; a1 = S("1.3") - .1
    B = win(t, a0, a1, .45, .35)
    if B > 0:
        base = 700
        line(c, 360, base, 1560, base, e_out(prog(t, a0, a0 + .7)), 4, LINE, B)
        line(c, 360, base, 360, 150, e_out(prog(t, a0, a0 + .8)), 4, LINE, B)
        text(c, "HOW HARD FOR A COMPUTER", 120, 430, "mono", 36, CYAN, "c", ap(t, a0 + .4, .5) * B, rot=-90)
        # checkers bar
        kh = 140 * e_out(prog(t, Wd("1.2", "checkers"), Wd("1.2", "checkers") + 1.0))
        rect(c, 520, base - kh, 280, kh, 1, 3.5, LINE, B, fill=CYAN, falpha=.25)
        chessboard(c, 560, base - 330, 25, ap(t, Wd("1.2", "checkers"), .8), B, 8) if False else None
        text(c, "CHECKERS", 660, base + 40, "monob", 36, LINE, "c", ap(t, Wd("1.2", "checkers"), .4) * B)
        text(c, "ADULT LEVEL", 660, base + 82, "mono", 36, CYAN, "c", ap(t, Wd("1.2", "adult"), .4) * B)
        chessboard(c, 590, base - 140 - 150, 20, ap(t, Wd("1.2", "play checkers"), .8), B, 8)
        # toddler bar
        tt = Wd("1.2", "perception")
        th = 470 * e_out(prog(t, tt, tt + 1.8))
        rect(c, 1000, base - th, 280, th, 1, 3.5, LINE, B, fill=CYAN, falpha=.25)
        hatch(c, rect_pts(1000, base - th, 280, th), 20, -math.pi / 4, CYAN, .5, 2, 1) if th > 4 else None
        eye_icon(c, 1140, base - 540 if th > 20 else -100, 1.0, LINE, ap(t, tt + 1.5, .5) * B)
        text(c, "PERCEPTION + MOBILITY", 1140, base + 40, "monob", 36, LINE, "c", ap(t, tt, .4) * B)
        text(c, "ONE-YEAR-OLD", 1140, base + 82, "mono", 36, CYAN, "c", ap(t, Wd("1.2", "one-year-old"), .4) * B)
    # ---- 1.3 Deep Blue 1997
    a0 = S("1.3") - .05; a1 = S("1.4") - .1
    C = win(t, a0, a1, .45, .35)
    if C > 0:
        ax = 300; bx = 1620; ay = 190
        line(c, ax, ay, bx, ay, e_out(prog(t, a0, a0 + 1.0)), 4, LINE, C)
        text(c, "1988", ax, ay - 50, "monob", 52, LINE, "c", C); text(c, "1997", bx, ay - 50, "monob", 52, LINE, "c", ap(t, a0 + .9, .4) * C)
        dim(c, ax + 30, ay + 55, bx - 30, ay + 55, "9 YEARS LATER", e_out(prog(t, a0 + .5, a0 + 1.6)), CYAN, 2.5, size=40, alpha=C)
        tb = Wd("1.3", "IBM")
        chessboard(c, 750, 300, 52, ap(t, tb, 1.2), C, 8)
        lk = ap(t, Wd("1.3", "Garry"), .5) * C
        text(c, "KASPAROV", 400, 450, "monob", 44, LINE, "c", lk); text(c, "WORLD CHAMPION", 400, 502, "mono", 36, CYAN, "c", lk)
        person(c, 400, 640, .9, alpha=lk)
        dk = ap(t, Wd("1.3", "Deep Blue"), .5) * C
        text(c, "DEEP BLUE", 1480, 450, "monob", 44, LINE, "c", dk); text(c, "IBM", 1480, 502, "mono", 36, CYAN, "c", dk)
        rect(c, 1380, 560, 200, 150, dk, 3.5, LINE, C, fill=BG, falpha=.9)
        for k in range(4): line(c, 1400, 590 + k * 30, 1560, 590 + k * 30, dk, 3, CYAN, C)
        sc = ap(t, Wd("1.3", "beat"), .5) * C
        text(c, "3½ – 2½", 960, 770, "monob", 56, LINE, "c", sc) if False else text(c, "3.5 - 2.5", 960, 760, "monob", 56, LINE, "c", sc)
        src(c, "SRC: IBM / HISTORY.COM, MAY 1997", t, a0 + 1.5, a1)
    # ---- 1.4 the paradox table
    a0 = S("1.4") - .05; a1 = S("1.5") - .1
    Dd = win(t, a0, a1, .45, .35)
    if Dd > 0:
        text(c, "MORAVEC'S PARADOX", 960, 135, "monob", 60, LINE, "c", Dd)
        t1 = min(Wd("1.4", "what is hard for people"), a0 + 1.0); t2 = Wd("1.4", "and what is easy")
        # row 1
        y1 = 330; y2 = 590
        a_ = ap(t, t1, .5) * Dd
        card(c, 130, y1 - 90, 640, 180, e_out(prog(t, t1, t1 + .6)), LINE, Dd)
        text(c, "HARD FOR PEOPLE", 450, y1 - 40, "monob", 40, LINE, "c", a_); text(c, "chess · arithmetic", 450, y1 + 25, "hand", 40, CYAN, "c", a_)
        poly_arrow(c, [(790, y1), (1130, y1)], e_out(prog(t, t1 + .8, t1 + 1.6)), 4, CYAN, Dd)
        card(c, 1150, y1 - 90, 640, 180, e_out(prog(t, t1 + 1.4, t1 + 2.0)), LINE, Dd)
        b_ = ap(t, t1 + 1.8, .5) * Dd
        text(c, "EASY FOR MACHINES", 1470, y1 - 40, "monob", 40, CYAN, "c", b_); check(c, 1470, y1 + 35, 28, b_, 8, CYAN, Dd)
        a2_ = ap(t, t2, .5) * Dd
        card(c, 130, y2 - 90, 640, 180, e_out(prog(t, t2, t2 + .6)), LINE, Dd)
        text(c, "EASY FOR PEOPLE", 450, y2 - 40, "monob", 40, LINE, "c", a2_); text(c, "walking · grasping · folding", 450, y2 + 25, "hand", 38, CYAN, "c", a2_)
        poly_arrow(c, [(790, y2), (1130, y2)], e_out(prog(t, t2 + .8, t2 + 1.6)), 4, CYAN, Dd)
        card(c, 1150, y2 - 90, 640, 180, e_out(prog(t, t2 + 1.4, t2 + 2.0)), LINE, Dd)
        b2 = ap(t, t2 + 1.8, .5) * Dd
        text(c, "HARD FOR MACHINES", 1470, y2 - 40, "monob", 40, LINE, "c", b2); cross(c, 1470, y2 + 35, 28, b2, 8, RED, Dd)
    # ---- 1.5-1.8 evolution axis
    a0 = S("1.5") - .05; a1 = S("1.9") - .15
    Ev = win(t, a0, a1, .45, .35)
    if Ev > 0:
        ax0, ax1, ay = 240, 1680, 400
        text(c, "WHY? EVOLUTION", 960, 140, "monob", 60, LINE, "c", Ev, p=prog(t, a0, a0 + 1.2))
        line(c, ax0, ay, ax0 + (ax1 - ax0) * e_out(prog(t, a0 + .3, a0 + 2.0)), ay, 1, 5, LINE, Ev)
        text(c, "NOW", ax1, ay + 60, "monob", 40, LINE, "c", ap(t, a0 + 1.8, .4) * Ev)
        c.drawLine(ax1, ay - 24, ax1, ay + 24, P(LINE, "stroke", 4, Ev))
        c.drawLine(ax0, ay - 24, ax0, ay + 24, P(LINE, "stroke", 4, Ev))
        te = Wd("1.6", "fossil eyes")
        eye_icon(c, ax0 + 10, ay - 110, 1.0, LINE, ap(t, te, .6) * Ev)
        text(c, "FOSSIL EYES", ax0 + 100, ay - 110, "mono", 36, LINE, "l", ap(t, te, .5) * Ev)
        sp = e_out(prog(t, Wd("1.6", "refined"), Wd("1.6", "refined") + 2.4))
        if sp > 0:
            band = rect_pts(ax0, ay - 70, (ax1 - ax0) * sp, 36)
            fillpoly(c, band, CYAN, .18 * Ev); hatch(c, band, 14, -math.pi / 4, CYAN, .5 * Ev, 2, 1)
            text(c, "POLISHED THE WHOLE TIME", ax1, ay - 150, "mono", 36, CYAN, "r", ap(t, Wd("1.6", "refined"), .6) * Ev)
        pr = prog(t, Wd("1.6", "500"), Wd("1.6", "500") + 1.6)
        if pr > 0:
            dim(c, ax0, ay + 150, ax1, ay + 150, "500+ MILLION YEARS", min(1, pr * 1.6), LINE, 2.5, size=44, ly=-36, alpha=Ev)
        tw_ = ap(t, S("1.7"), .5) * Ev
        if tw_ > 0:
            c.drawLine(ax1 - 3, ay - 24, ax1 - 3, ay + 24, P(CYAN, "stroke", 5, tw_))
            mx, my, mr = 1560, 690, 90
            c.drawCircle(mx, my, mr, P(BG, alpha=.95 * tw_)); c.drawCircle(mx, my, mr, P(LINE, "stroke", 4, tw_))
            c.drawLine(mx + 60, my - 70, ax1 - 3, ay + 30, P(LINE, "stroke", 2.5, tw_ * .8, dash=[8, 8]))
            c.drawLine(mx - 15, my - 50, mx - 15, my + 50, P(CYAN, "stroke", 5, tw_)); c.drawLine(mx + 30, my - 50, mx + 30, my + 50, P(LINE, "stroke", 5, tw_))
            text(c, "WRITING: ABOUT 5,000 YEARS", 1440, my, "monob", 36, LINE, "r", tw_)
        t8 = S("1.8") - .1
        if ap(t, t8, .5) > 0:
            text(c, "REASONING FEELS HARD: IT IS NEW", 240, 620, "mono", 36, LINE, "l", ap(t, Wd("1.8", "Reasoning"), .5) * Ev)
            text(c, "SEEING + MOVING FEEL EASY: THEY ARE OLD", 240, 745, "mono", 36, CYAN, "l", ap(t, Wd("1.8", "Seeing and moving feel"), .5) * Ev)
    # ---- 1.9 no head start
    a0 = S("1.9") - .05
    G = ap(t, a0, .5)
    if G > 0:
        robot_side(c, 560, 380, s=1.5, alpha=G, **dict(b=0, a1=0, a2=0, u1=8, u2=18))
        line(c, 360, 380 + 216 * 1.5 + 0, 760, 380 + 216 * 1.5, 1, 4, LINE, G)
        gx, gy_ = 1020, 360
        text(c, "HEAD START", 1360, 250, "monob", 48, LINE, "c", ap(t, a0 + .6, .5))
        rect(c, 1060, 300, 600, 60, ap(t, a0 + .8, .6), 3.5, LINE, 1)
        text(c, "0", 1360, 410, "monob", 72, CYAN, "c", ap(t, a0 + 1.4, .5))
        tq = Wd("1.9", "So the real question")
        text(c, "NOT: WHY BAD AT LAUNDRY?", 1360, 560, "mono", 36, LINE, "c", ap(t, tq, .5))
        text(c, "WHY GOOD AT BACKFLIPS?", 1360, 620, "monob", 40, CYAN, "c", ap(t, Wd("1.9", "It is why"), .5))
