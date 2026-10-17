# -*- coding: utf-8 -*-
"""Sheets 3-4: why the backflip is easy; why laundry is hard."""
import math, random
import skia
from lib import *
from props import *
from scenes_a import T, S, E, Wd, win, src, reg, ground, flip_loop, check_mark
import scenes_a
REG = {}
def reg_b(k):
    def deco(fn): REG[k] = fn; return fn
    return deco

def tag(c, s, x, y, a, size=36, color=LINE, align="c", kind="mono"):
    text(c, s, x, y, kind, size, color, align, a)

def mini_fall(c, x, gy, ph, t, s=.3, alpha=1.0):
    """tiny robot repeatedly standing, tipping over, lying; ph = phase offset"""
    k = ((t * .45) + ph) % 1.0
    rot = 88 * e_in(prog(k, .15, .55))
    c.save(); c.translate(x, gy);
    robot_side(c, 0, -216 * s * math.cos(rot * D2R) - 8 * s, rot=rot, b=0, a1=0, a2=0, u1=8, u2=18, s=s, alpha=alpha, ghost=True)
    c.restore()

# ==================================================================================================
@reg_b(2)
def seg2(c, t):
    # ---- 2.1 chess and flip
    a0 = S("2.1") - .05; a1 = S("2.2") - .1
    A = win(t, a0, a1, .4, .35)
    if A > 0:
        chessboard(c, 150, 190, 62, ap(t, a0, 1.2), A, 8)
        tag(c, "CHESS", 398, 740, ap(t, a0 + .4, .4) * A, 48, LINE, "c", "monob")
        text(c, "=", 960, 450, "monob", 150, CYAN, "c", ap(t, Wd("2.1", "in the same way"), .5) * A)
        gy = 640
        ground(c, t, a0, gy, 1100, 1800, .8)
        flip_loop(c, t, a0 + .5, 4.0, gy, 1450, .8, A)
        tag(c, "BACKFLIP", 1450, 740, ap(t, a0 + .8, .4) * A, 48, LINE, "c", "monob")
        tag(c, "KNOWN RULES", 960, 150, ap(t, Wd("2.1", "easy"), .5) * A, 52, CYAN, "c", "monob")
    # ---- 2.2 rigid links + simulator
    a0 = S("2.2") - .05; a1 = S("2.3") - .1
    B = win(t, a0, a1, .4, .35)
    if B > 0:
        gy = 740
        line(c, 150, gy, 150 + 700 * e_out(prog(t, a0, a0 + .7)), gy, 1, 4, LINE, B)
        rb = ap(t, a0 + .2, .7)
        robot_side(c, 480, gy - 16 * 1.5 - 200 * 1.5, b=0, a1=0, a2=0, u1=8, u2=18, s=1.5, alpha=rb * B)
        t1 = Wd("2.2", "rigid metal links")
        ca = ap(t, t1, .5) * B
        poly_arrow(c, [(250, 330), (330, 330), (440, 475)], e_out(prog(t, t1, t1 + .8)), 3, CYAN, B)
        tag(c, "RIGID LINK", 230, 290, ca, 40, LINE, "c", "monob")
        t2 = Wd("2.2", "joined at motors")
        cb = ap(t, t2, .5) * B
        poly_arrow(c, [(250, 560), (330, 560), (430, 622)], e_out(prog(t, t2, t2 + .8)), 3, CYAN, B)
        tag(c, "MOTOR JOINT", 250, 520, cb, 40, LINE, "c", "monob")
        t3 = Wd("2.2", "Physics engines")
        sa = ap(t, t3, .6) * B
        card(c, 1000, 190, 780, 540, e_out(prog(t, t3, t3 + .7)), LINE, B)
        tag(c, "SIMULATOR", 1390, 250, sa, 48, LINE, "c", "monob")
        line(c, 1060, 640, 1720, 640, sa, 3, LINE, B)
        robot_side(c, 1250, 640 - 16 * .8 - 200 * .8, b=0, a1=0, a2=0, u1=8, u2=18, s=.8, alpha=sa)
        arrow(c, 1600, 330, 1600, 480, ap(t, t3 + .8, .8), 4, CYAN, B)
        tag(c, "GRAVITY", 1600, 300, ap(t, t3 + 1.0, .5) * B, 36, CYAN)
        tag(c, "RIGID BODIES + CONTACTS", 1390, 700, ap(t, Wd("2.2", "simulate"), .5) * B, 36, LINE)
    # ---- 2.3 train in the simulator: falls are free
    a0 = S("2.3") - .05; a1 = S("2.4") - .1
    C = win(t, a0, a1, .4, .35)
    if C > 0:
        tag(c, "SIMULATOR", 960, 140, ap(t, a0, .4) * C, 56, LINE, "c", "monob")
        n = 0
        for r in range(3):
            line(c, 140, 330 + r * 190, 140 + 1300 * e_out(prog(t, a0 + .2 + r * .15, a0 + 1.0 + r * .15)), 330 + r * 190, 1, 3, LINE, C * .8)
            for cidx in range(6):
                ia = ap(t, a0 + .5 + (r * 6 + cidx) * .06, .4)
                if ia > 0: mini_fall(c, 230 + cidx * 220, 330 + r * 190, (r * 6 + cidx) * .137, t, .5, ia * C)
        tc = ap(t, Wd("2.3", "fall as many times"), .5) * C
        tag(c, "ATTEMPTS", 1660, 300, tc, 40, CYAN, "c", "monob")
        tag(c, f"{int(max(0, t - a0 - 2.0) ** 2 * 3300):,}", 1660, 380, tc, 52, LINE, "c", "monob")
        tag(c, "ILLUSTRATIVE", 1660, 450, tc, 36, LINE)
        tag(c, "NOTHING BREAKS", 1660, 600, ap(t, Wd("2.3", "without breaking"), .5) * C, 36, CYAN)
    # ---- 2.4 ETH Zurich + NVIDIA
    a0 = S("2.4") - .05; a1 = S("2.5") - .1
    Dd = win(t, a0, a1, .4, .35)
    if Dd > 0:
        tag(c, "2021 · ETH ZURICH + NVIDIA", 700, 140, ap(t, a0, .5) * Dd, 44, LINE, "c", "monob")
        for r in range(3):
            for k in range(4):
                x0 = 230 + k * 290; y0 = 330 + r * 190
                ia = ap(t, a0 + .4 + (r * 4 + k) * .09, .4)
                pts = [(x0 - 120 + i * 24, y0 + 6 + 10 * math.sin(i * .8 + r * 2 + k)) for i in range(11)]
                draw_on(c, pts, ia, 3, LINE, Dd * .8)
                if ia > 0.1: quad(c, x0, y0 - 4, 1.0, (t * .9 + r * .2 + k * .13) % 1.0, LINE, ia * Dd)
        tag(c, "THOUSANDS AT ONCE", 700, 720, ap(t, Wd("2.4", "thousands of simulated"), .5) * Dd, 40, CYAN, "c", "monob")
        t1 = Wd("2.4", "20 minutes") if False else Wd("2.4", "about 20")
        tm = prog(t, t1, t1 + 1.6)
        clock_icon(c, 1560, 300, 90, tm * .33, LINE, ap(t, t1, .5) * Dd)
        tag(c, roll(20, tm) + " MIN", 1560, 440, ap(t, t1, .5) * Dd, 52, LINE, "c", "monob")
        t2 = Wd("2.4", "single graphics card")
        gpu_icon(c, 1560, 570, 1.3, LINE, ap(t, t2, .6) * Dd)
        tag(c, "1 GPU", 1560, 690, ap(t, t2, .5) * Dd, 52, LINE, "c", "monob")
        src(c, "SRC: RUDIN ET AL., ETH + NVIDIA, 2021", t, a0 + 1.0, a1)
    # ---- 2.5 copy to the real robot
    a0 = S("2.5") - .05; a1 = S("2.6") - .1
    Ee = win(t, a0, a1, .4, .35)
    if Ee > 0:
        card(c, 120, 200, 640, 520, e_out(prog(t, a0, a0 + .7)), LINE, Ee)
        tag(c, "SIMULATOR", 440, 255, ap(t, a0 + .3, .5) * Ee, 44, LINE, "c", "monob")
        gy = 660
        line(c, 160, gy, 720, gy, ap(t, a0 + .3, .5), 3, LINE, Ee)
        flip_loop(c, t, a0 + .3, 3.6, gy, 440, .55, Ee)
        tc = Wd("2.5", "copied")
        poly_arrow(c, [(800, 450), (1060, 450)], e_out(prog(t, tc - .2, tc + .8)), 6, CYAN, Ee, 26)
        tag(c, "COPY", 930, 400, ap(t, tc - .2, .4) * Ee, 48, CYAN, "c", "monob")
        tu = Wd("2.5", "Unitree")
        gy2 = 660
        ground(c, t, tu, gy2, 1100, 1800, .6)
        flip_loop(c, t, tu + .3, 4.0, gy2, 1450, .8, Ee * ap(t, tu, .4))
        tag(c, "UNITREE 2024", 1450, 735, ap(t, tu, .5) * Ee, 44, LINE, "c", "monob")
        tag(c, "TRAINED THIS WAY (REPORTS)", 1450, 190, ap(t, Wd("2.5", "trained that way"), .5) * Ee, 36, CYAN)
        src(c, "SRC: INTERESTING ENGINEERING, MAR 2024", t, a0 + 1.5, a1)
    # ---- 2.6 short, rehearsed, flat
    a0 = S("2.6") - .05; a1 = S("2.7") - .1
    F = win(t, a0, a1, .4, .35)
    if F > 0:
        gy = 600
        ground(c, t, a0, gy, 120, 1000, .6)
        u = flip_loop(c, t, a0 + .2, 4.2, gy, 560, .6, F)
        tf = Wd("2.6", "flat")
        line(c, 120, gy + 12, 1000, gy + 12, ap(t, tf - 1.0, .6), 5, CYAN, F)
        tag(c, "KNOWN FLOOR", 560, 690, ap(t, tf - 1.0, .5) * F, 40, CYAN, "c", "monob")
        tb = Wd("2.6", "body is known")
        rect(c, 400, 250, 320, 340, ap(t, tb, .7), 3, CYAN, F, dash=[12, 9])
        tag(c, "KNOWN BODY", 560, 745, ap(t, tb, .5) * F, 40, CYAN, "c", "monob")
        ts = Wd("2.6", "short")
        dim(c, 150, 145, 970, 145, "SHORT", e_out(prog(t, ts - 2.2, ts - 1.0)), LINE, 2.5, size=40, alpha=F)
        tr = Wd("2.6", "rehearsed")
        tag(c, "REHEARSED", 1450, 230, ap(t, tr, .5) * F, 44, LINE, "c", "monob")
        for i in range(3): check(c, 1160, 330 + i * 70, 24, ap(t, tr + .4 + i * .35, .3), 7, CYAN, F)
        for i, s_ in enumerate(("TRY 1", "TRY 2", "TRY 3")): tag(c, s_, 1300, 330 + i * 70, ap(t, tr + .4 + i * .35, .3) * F, 40, LINE, "l")
        tn = Wd("2.6", "nothing in the scene")
        rect(c, 1130, 520, 640, 220, ap(t, tn, .8), 3, LINE, F, dash=[12, 9])
        tag(c, "NOTHING ELSE MOVES", 1450, 630, ap(t, tn + .5, .5) * F, 40, LINE, "c", "monob")
    # ---- 2.7 exam with the questions in advance
    a0 = S("2.7") - .05; a1 = S("2.8") - .1
    G = win(t, a0, a1, .4, .35)
    if G > 0:
        card(c, 520, 150, 880, 600, e_out(prog(t, a0, a0 + .7)), LINE, G)
        tag(c, "EXAM", 960, 225, ap(t, a0 + .3, .4) * G, 72, LINE, "c", "monob")
        for i in range(4):
            ya = 330 + i * 80
            tag(c, f"Q{i+1}", 640, ya, ap(t, a0 + .5 + i * .25, .3) * G, 44, LINE, "l", "monob")
            line(c, 740, ya + 22, 1220, ya + 22, e_out(prog(t, a0 + .5 + i * .25, a0 + 1.0 + i * .25)), 3, LINE, G * .7)
            check(c, 1300, ya, 22, ap(t, a0 + 1.6 + i * .25, .3), 7, CYAN, G)
        tp = Wd("2.7", "published in advance")
        tag(c, "QUESTIONS PUBLISHED IN ADVANCE", 960, 690, ap(t, tp, .5) * G, 40, CYAN, "c", "monob")
    # ---- 2.8 / 2.9 the twist: nesting inverted
    a0 = S("2.8") - .05
    H_ = ap(t, a0, .4)
    if H_ > 0:
        # left: big stunt box, small easy problem
        rect(c, 130, 180, 800, 540, e_out(prog(t, a0 + .1, a0 + 1.2)), 4, LINE, H_)
        tag(c, "HARD STUNT", 530, 235, ap(t, Wd("2.8", "hard stunt"), .5) * H_, 48, LINE, "c", "monob")
        te = Wd("2.8", "easy problem")
        circle(c, 530, 470, 120, e_out(prog(t, te, te + .8)), 4, CYAN, H_, fill=CYAN, falpha=.2)
        tag(c, "EASY", 530, 455, ap(t, te + .4, .4) * H_, 44, CYAN, "c", "monob"); tag(c, "PROBLEM", 530, 505, ap(t, te + .4, .4) * H_, 44, CYAN, "c", "monob")
        for i, (s_, ph) in enumerate((("KNOWN BODY", "a known body"), ("KNOWN FLOOR", "a known floor"), ("KNOWN GOAL", "a known goal"))):
            tt_ = Wd("2.8", ph); aa = ap(t, tt_, .4)
            if S("2.9") - .0 > t or True:
                fade = 1 - e_in(prog(t, S("2.9") - .35, S("2.9") - .05))
                tag(c, s_, 1360, 300 + i * 80, aa * H_ * fade, 44, LINE, "l", "monob"); check(c, 1300, 300 + i * 80, 20, aa, 7, CYAN, H_ * fade)
    a0 = S("2.9") - .05
    I = ap(t, a0, .4)
    if I > 0:
        rect(c, 1060, 300, 720, 330, e_out(prog(t, a0 + .1, a0 + 1.0)), 4, LINE, I)
        tag(c, "EASY-LOOKING JOB", 1420, 355, ap(t, Wd("2.9", "easy-looking job"), .5) * I, 44, LINE, "c", "monob")
        th_ = Wd("2.9", "hard problem")
        pts = [(1100, 420), (1300, 395), (1500, 430), (1740, 410), (1745, 600), (1500, 612), (1280, 590), (1100, 605)]
        fillpoly(c, pts, AMBER, .22 * ap(t, th_, .6) * I)
        hatch(c, pts, 16, -math.pi / 4, AMBER, .7 * I, 2, ap(t, th_, 1.0))
        draw_on(c, pts, e_out(prog(t, th_, th_ + .9)), 4, AMBER, I, close=True)
        tag(c, "HARD PROBLEM", 1420, 510, ap(t, th_ + .4, .5) * I, 48, AMBER, "c", "monob")

# ==================================================================================================
@reg_b(3)
def seg3(c, t):
    # ---- 3.1 one shape vs no fixed shape
    a0 = S("3.1") - .05; a1 = S("3.2") - .1
    A = win(t, a0, a1, .4, .3)
    if A > 0:
        limb(c, 420, 230, 420, 590, 40, 5, LINE, A)
        joint(c, 420, 230, 11, CYAN, A); joint(c, 420, 590, 11, CYAN, A)
        tag(c, "A METAL LINK: ONE SHAPE", 420, 700, ap(t, a0 + .4, .5) * A, 36, LINE)
        draw_shirt(c, 1330, 400, 1.35, 0, 0, 0, alpha=ap(t, Wd("3.1", "shirt"), .6) * A, crumple=.55 + .25 * math.sin(t * 2.2), seed=t * .9)
        tag(c, "A SHIRT: NO FIXED SHAPE", 1330, 700, ap(t, Wd("3.1", "no fixed"), .5) * A, 36, LINE)
    # ---- 3.2 infinite degrees of freedom
    a0 = S("3.2") - .05; a1 = S("3.3") - .1
    B = win(t, a0, a1, .4, .3)
    if B > 0:
        tag(c, "DEGREES OF FREEDOM", 960, 140, ap(t, a0, .5) * B, 56, LINE, "c", "monob")
        limb(c, 420, 280, 420, 560, 34, 5, LINE, B); joint(c, 420, 280, 11, CYAN, B)
        arc(c, 420, 280, 110, math.pi * .1, math.pi * .6, ap(t, a0 + .4, .8), 4, CYAN, B)
        tag(c, "ONE JOINT ANGLE", 420, 660, ap(t, a0 + .5, .5) * B, 36, LINE)
        # shirt with control-point grid
        draw_shirt(c, 1330, 410, 1.3, 0, 0, 0, alpha=B, crumple=.3 + .15 * math.sin(t * 2), seed=t * .7, falpha=.1)
        r_ = random.Random(3)
        nn = int(110 * ap(t, a0 + .8, 2.4))
        for i in range(nn):
            q = (r_.uniform(1080, 1580), r_.uniform(250, 560)); c.drawCircle(q[0], q[1], 5, P(CYAN, alpha=.9 * B))
        ti = Wd("3.2", "infinite")
        infinity(c, 1330, 650, 70 * ap(t, ti, .6), ap(t, ti, .8), 7, CYAN, B)
        src(c, "SRC: SOFTGYM BENCHMARK, CORL 2020", t, a0 + 1.0, a1)
    # ---- 3.3 occlusion
    a0 = S("3.3") - .05; a1 = S("3.4") - .1
    C = win(t, a0, a1, .4, .3)
    if C > 0:
        camera_icon(c, 960, 190, 1.6, LINE, ap(t, a0, .5) * C)
        draw_shirt(c, 960, 520, 1.25, 0, 0, 0, alpha=C, crumple=.12, seed=1.0)
        tf = Wd("3.3", "A fold covers")
        # folded flap covering a sleeve (draws over the left sleeve)
        flap = [(700, 470), (900, 450), (930, 590), (720, 620)]
        k = e_out(prog(t, tf, tf + .8))
        fillpoly(c, flap, LINE, .25 * k * C); draw_on(c, flap, k, 4, LINE, C, close=True)
        for ang in (-.3, -.12, .06):
            line(c, 960, 245, 960 + math.tan(ang) * 340 * 1.0 - 120 * ang / abs(ang or 1) * 0, 560, ap(t, a0 + .4, .6), 2, CYAN, C * .6, dash=[10, 8])
        th = Wd("3.3", "cannot see")
        hid = [(640, 500), (710, 470), (720, 600), (650, 610)]
        hatch(c, hid, 12, -math.pi / 4, CYAN, .9 * C, 2, ap(t, th, .8)); qmark(c, 600, 540, 90, AMBER if False else CYAN, ap(t, th, .5) * C)
        tag(c, "HIDDEN FROM THE CAMERA", 1400, 520, ap(t, th, .5) * C, 40, CYAN, "c", "monob")
        poly_arrow(c, [(1150, 520), (800, 540), (700, 540)], e_out(prog(t, th + .2, th + 1.0)), 3, CYAN, C * .8) if False else None
        src(c, "SRC: KADI & TERZIC, SENSORS, 2023", t, a0 + 1.0, a1)
    # ---- 3.4 cloth simulation artifacts
    a0 = S("3.4") - .05; a1 = S("3.5") - .1
    Dd = win(t, a0, a1, .4, .3)
    if Dd > 0:
        tag(c, "SIMULATED CLOTH", 700, 130, ap(t, a0, .5) * Dd, 52, LINE, "c", "monob")
        gx0, gy0, nx, ny, cs = 260, 250, 10, 7, 76
        tst = Wd("3.4", "stretch"); tpt = Wd("3.4", "pass through"); tsl = Wd("3.4", "too slow")
        stretch = e_out(prog(t, tst, tst + 1.2))
        def node(i, j):
            x = gx0 + i * cs; y = gy0 + j * cs
            x += stretch * (math.sin(i * 1.3 + j) * 24 + (i > 6) * 60 * (j % 2)); y += stretch * math.cos(i + j * 1.7) * 18
            return (x, y)
        gp = ap(t, a0 + .3, 1.0)
        for j in range(ny):
            draw_on(c, [node(i, j) for i in range(nx)], gp, 2.5, LINE, Dd * .85)
        for i in range(nx):
            draw_on(c, [node(i, j) for j in range(ny)], gp, 2.5, LINE, Dd * .85)
        if t > tpt - .2:
            kk = ap(t, tpt, .6)
            for (a_, b_, c_, d_) in ((2, 1, 3, 3), (6, 3, 7, 5), (4, 4, 5, 6)):
                p0 = node(a_, b_); p1 = node(c_, d_)
                line(c, p0[0], p0[1], p0[0] + (p1[0] - p0[0]) * 1.8, p0[1] + (p1[1] - p0[1]) * -1.0, kk, 4, CYAN, Dd)
                circle(c, (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2 + 30, 34, kk, 3, CYAN, Dd)
        tag(c, "STRETCH · DISTORT · SELF-PENETRATION", 700, 760, ap(t, tst, .5) * Dd, 36, CYAN)
        # speed gauge
        if t > tsl - .5:
            ga = ap(t, tsl - .5, .5) * Dd
            tag(c, "SIMULATION SPEED", 1500, 270, ga, 40, LINE, "c", "monob")
            rect(c, 1250, 320, 500, 54, 1, 3.5, LINE, Dd * ga)
            fw = 500 * .12 * e_out(prog(t, tsl, tsl + 1.2)) + 4
            c.drawRect(skia.Rect.MakeXYWH(1250, 320, fw, 54), P(CYAN, alpha=.7 * Dd * ga))
            tag(c, "LARGE-SCALE TRAINING NEEDS MORE", 1500, 430, ga, 36, LINE)
            tag(c, "TOO SLOW", 1500, 520, ap(t, tsl + 1.0, .5) * Dd, 60, RED, "c", "monob")
        src(c, "SRC: CLOTH-SIM BENCHMARKS (AAAI, SOFTGYM)", t, a0 + 1.5, a1)
    # ---- 3.5 the trick works less well
    a0 = S("3.5") - .05; a1 = S("3.6") - .1
    Ee = win(t, a0, a1, .4, .3)
    if Ee > 0:
        base = 700
        line(c, 360, base, 1560, base, e_out(prog(t, a0, a0 + .6)), 4, LINE, Ee)
        h1 = 430 * e_out(prog(t, a0 + .3, a0 + 1.3)); h2 = 150 * e_out(prog(t, Wd("3.5", "much less"), Wd("3.5", "much less") + 1.0))
        rect(c, 520, base - h1, 280, h1, 1, 3.5, LINE, Ee, fill=CYAN, falpha=.25)
        rect(c, 1120, base - h2, 280, h2, 1, 3.5, LINE, Ee, fill=CYAN, falpha=.25)
        tag(c, "BACKFLIP", 660, base + 46, ap(t, a0 + .4, .4) * Ee, 40, LINE, "c", "monob")
        tag(c, "SHIRT", 1260, base + 46, ap(t, a0 + 1.2, .4) * Ee, 40, LINE, "c", "monob")
        tag(c, "SIMULATION WORKS", 660, 190, ap(t, a0 + 1.0, .5) * Ee, 40, CYAN, "c", "monob")
        tag(c, "WORKS MUCH LESS WELL", 1260, 480, ap(t, Wd("3.5", "much less"), .5) * Ee, 36, CYAN)
    # ---- 3.6 every home is different
    a0 = S("3.6") - .05; a1 = S("3.7") - .1
    F = win(t, a0, a1, .4, .3)
    if F > 0:
        tag(c, "EVERY HOME IS DIFFERENT", 960, 140, ap(t, a0, .5) * F, 52, LINE, "c", "monob")
        for i, (x0, nm) in enumerate(((140, "KITCHEN"), (560, "CLOSET"), (980, "BASKET"), (1400, "HOME 4"))):
            tt_ = a0 + .4 + i * .7
            house_plan(c, x0, 260, 380, 380, i, e_out(prog(t, tt_, tt_ + .8)), LINE, F)
    # ---- 3.7 hands: touch receptors
    a0 = S("3.7") - .05; a1 = S("3.8") - .1
    G = win(t, a0, a1, .4, .3)
    if G > 0:
        hand_outline(c, 640, 480, 2.3, ap(t, a0, 1.2), LINE, G, prog(t, Wd("3.7", "17,000"), Wd("3.7", "17,000") + 2.2))
        tr = prog(t, Wd("3.7", "17,000"), Wd("3.7", "17,000") + 2.0)
        tag(c, roll(17000, tr), 1380, 330, ap(t, Wd("3.7", "17,000") - .3, .4) * G, 120, LINE, "c", "monob")
        tag(c, "RECEPTORS FOR LIGHT TOUCH", 1380, 430, ap(t, Wd("3.7", "17,000"), .5) * G, 40, CYAN, "c", "monob")
        tag(c, "IN ONE HUMAN HAND", 1380, 490, ap(t, Wd("3.7", "17,000"), .5) * G, 36, LINE)
        src(c, "SRC: R. BROOKS ESSAY, SEP 2025 (VIA FORTUNE)", t, a0 + 1.0, a1)
    # ---- 3.8 Brooks: no touch data
    a0 = S("3.8") - .05; a1 = S("3.9") - .1
    Hh = win(t, a0, a1, .4, .3)
    if Hh > 0:
        person(c, 330, 380, 1.5, alpha=Hh)
        tag(c, "RODNEY BROOKS", 330, 560, ap(t, a0 + .3, .5) * Hh, 44, LINE, "c", "monob")
        tag(c, "IROBOT CO-FOUNDER", 330, 615, ap(t, a0 + .5, .5) * Hh, 36, CYAN)
        # two channels into buckets
        camera_icon(c, 800, 250, 1.1, LINE, Hh)
        tag(c, "VIDEO + TEXT", 800, 330, Hh, 36, LINE)
        poly_arrow(c, [(930, 250), (1270, 250)], e_out(prog(t, a0 + .8, a0 + 1.6)), 4, CYAN, Hh)
        rect(c, 1290, 170, 450, 160, ap(t, a0 + 1.2, .5), 4, LINE, Hh, fill=CYAN, falpha=.3)
        tag(c, "LOTS OF DATA", 1515, 250, ap(t, a0 + 1.6, .4) * Hh, 40, LINE, "c", "monob")
        hand_outline(c, 800, 590, .6, 1, LINE, Hh)
        tag(c, "TOUCH", 800, 720, Hh, 36, LINE)
        tt_ = Wd("3.8", "nobody is collecting")
        poly_arrow(c, [(930, 590), (1270, 590)], e_out(prog(t, a0 + 2.2, a0 + 3.0)), 4, CYAN, Hh, 18, [12, 9])
        rect(c, 1290, 510, 450, 160, ap(t, a0 + 2.8, .5), 4, LINE, Hh, dash=[12, 9])
        tag(c, "NOT COLLECTED", 1515, 590, ap(t, tt_, .5) * Hh, 40, LINE, "c", "monob")
        cross(c, 1515, 710, 26, ap(t, tt_ + .3, .4), 9, RED, Hh)
        src(c, "SRC: RODNEY BROOKS, 2025", t, a0 + 1.0, a1)
    # ---- 3.9 Rubik's cube, 13,000 years of simulation
    a0 = S("3.9") - .05; a1 = S("3.10") - .1
    I = win(t, a0, a1, .4, .3)
    if I > 0:
        rubik(c, 560, 430, 2.3, 0, LINE, ap(t, a0, .7) * I)
        hand_outline(c, 1080, 600, .9, ap(t, a0 + .4, 1.0), LINE, ap(t, a0 + .4, .5) * I)
        tag(c, "SIMULATION ONLY", 560, 800, ap(t, Wd("3.9", "in simulation"), .5) * I, 40, CYAN, "c", "monob")
        tr = prog(t, Wd("3.9", "13,000"), Wd("3.9", "13,000") + 2.4)
        tag(c, roll(13000, tr), 1500, 330, ap(t, Wd("3.9", "13,000") - .3, .4) * I, 120, LINE, "c", "monob")
        tag(c, "YEARS OF EXPERIENCE", 1500, 430, ap(t, Wd("3.9", "13,000") - .3, .4) * I, 44, CYAN, "c", "monob")
        tag(c, "OPENAI · 2019", 1500, 160, ap(t, a0 + .3, .5) * I, 44, LINE, "c", "monob")
        src(c, "SRC: OPENAI, 2019 (SYNCED REVIEW)", t, a0 + 1.0, a1)
    # ---- 3.10 60% / 20%
    a0 = S("3.10") - .05; a1 = S("3.11") - .1
    J = win(t, a0, a1, .4, .3)
    if J > 0:
        rect(c, 100, 190, 660, 120, ap(t, a0, .6), 3.5, LINE, J)
        tag(c, "SEPARATE PROGRAM: THE MOVES", 430, 250, ap(t, a0 + .3, .5) * J, 36, LINE)
        poly_arrow(c, [(430, 310), (430, 420)], e_out(prog(t, a0 + .6, a0 + 1.2)), 4, CYAN, J)
        if t > a0 + 1.4: runner(c, t, [(430, 310), (430, 420)], 1.2, CYAN, J, 7)
        c.save(); c.rotate(10 * math.sin(t * 2.4), 430, 650)
        hand_outline(c, 430, 640, 1.2, 1, LINE, ap(t, a0 + .5, .5) * J)
        c.restore()
        tag(c, "THE HAND: CARRIES THEM OUT", 430, 770, ap(t, Wd("3.10", "The hand"), .5) * J, 36, LINE) if False else None
        base = 690
        line(c, 880, base, 1780, base, 1, 4, LINE, J)
        t6 = Wd("3.10", "60 percent"); t2 = Wd("3.10", "20 percent")
        h1 = 440 * .6 * e_out(prog(t, t6, t6 + 1.2)); h2 = 440 * .2 * e_out(prog(t, t2, t2 + 1.2))
        rect(c, 960, base - h1, 260, h1, 1, 3.5, LINE, J, fill=CYAN, falpha=.3)
        rect(c, 1440, base - h2, 260, h2, 1, 3.5, LINE, J, fill=CYAN, falpha=.3)
        tag(c, roll(60, prog(t, t6, t6 + 1.2)) + "%", 1090, base - h1 - 50, ap(t, t6, .3) * J, 72, LINE, "c", "monob")
        tag(c, roll(20, prog(t, t2, t2 + 1.2)) + "%", 1570, base - h2 - 50, ap(t, t2, .3) * J, 72, LINE, "c", "monob")
        tag(c, "SOLVED", 1090, base + 46, ap(t, t6, .4) * J, 40, CYAN, "c", "monob")
        tag(c, "HARDEST SCRAMBLES", 1570, base + 46, ap(t, t2, .4) * J, 36, CYAN, "c", "monob")
    # ---- 3.11 towel vs shirt
    a0 = S("3.11") - .05; a1 = S("3.12") - .1
    K = win(t, a0, a1, .4, .3)
    if K > 0:
        # towel: rectangle with 4 corner grips, folds in half twice
        tx, ty = 480, 470
        k1 = e_io(prog(t, a0 + 1.4, a0 + 2.6)); k2 = e_io(prog(t, a0 + 3.0, a0 + 4.2))
        w_ = 380; h_ = 260
        wi = w_ * (1 - .5 * k1); hi = h_ * (1 - .5 * k2)
        rect(c, tx - wi / 2, ty - hi / 2, wi, hi, ap(t, a0, .6), 4, LINE, K, fill=CYAN, falpha=.25)
        for sx_, sy_ in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
            cc = ap(t, a0 + .8 + (sx_ + 1) * .15 + (sy_ + 1) * .1, .3)
            circle(c, tx + sx_ * wi / 2, ty + sy_ * hi / 2, 12, cc, 3, CYAN, K, fill=CYAN, falpha=.9)
        tag(c, "TOWEL: 4 CORNERS", 480, 700, ap(t, a0 + .4, .5) * K, 36, LINE)
        tr = prog(t, Wd("3.11", "50 times"), Wd("3.11", "50 times") + 1.4)
        tag(c, roll(50, tr) + " / 50", 480, 190, ap(t, Wd("3.11", "50 times") - .2, .4) * K, 84, LINE, "c", "monob")
        tag(c, "UC BERKELEY · 2010", 480, 270, ap(t, a0 + .3, .5) * K, 36, CYAN)
        ts_ = Wd("3.11", "A shirt is not")
        draw_shirt(c, 1330, 430, 1.4, 0, 0, 0, alpha=ap(t, ts_ - 1.0, .6) * K, crumple=.4 + .15 * math.sin(t * 2), seed=t * .8)
        for i, (qx, qy) in enumerate(((1120, 300), (1560, 300), (1330, 560), (1190, 420), (1470, 470))):
            qmark(c, qx, qy, 70, CYAN, ap(t, ts_ + .1 * i, .4) * K * .9)
        tag(c, "SHIRT: WHERE ARE THE CORNERS?", 1330, 700, ap(t, ts_, .5) * K, 36, LINE)
        src(c, "SRC: MAITIN-SHEPARD ET AL., ICRA 2010", t, a0 + 1.0, a1)
    # ---- 3.12 sheets and inside-out garments
    a0 = S("3.12") - .05; a1 = S("3.13") - .1
    L_ = win(t, a0, a1, .4, .3)
    if L_ > 0:
        tag(c, "2026 · A LAUNDRY ROBOT ON SALE", 960, 140, ap(t, a0, .5) * L_, 48, LINE, "c", "monob")
        # bed sheet
        sh = [(210, 300), (700, 280), (730, 560), (180, 580)]
        tb_ = S("3.12") + 1.2
        fillpoly(c, sh, CYAN, .15 * ap(t, tb_ - .4, .6) * L_); draw_on(c, sh, e_out(prog(t, tb_ - .4, tb_ + .6)), 4, LINE, L_, close=True)
        for k in range(1, 4): draw_on(c, [(200 + k * 20, 330 + k * 60), (460, 320 + k * 60 + 20 * math.sin(k)), (720, 320 + k * 60)], ap(t, tb_, .8), 2, LINE, L_ * .5)
        tag(c, "BED SHEET", 460, 640, ap(t, tb_, .5) * L_, 40, LINE, "c", "monob")
        cross(c, 460, 440, 80, ap(t, tb_ + .5, .4), 12, RED, L_)
        ti_ = Wd("3.12", "inside-out")
        draw_shirt(c, 1330, 450, 1.1, 0, 0, 0, alpha=ap(t, ti_ - .4, .6) * L_, falpha=.1)
        for sx in (-100, 100): draw_on(c, [(1330 + sx * 1.1, 330), (1330 + sx * 1.1, 590)], ap(t, ti_, .8), 3, CYAN, L_, dash=[10, 8])
        draw_on(c, [(1330 - 160, 440), (1330 - 110, 460)], ap(t, ti_, .8), 3, CYAN, L_, dash=[10, 8])
        tag(c, "INSIDE-OUT GARMENT", 1330, 640, ap(t, ti_, .5) * L_, 40, LINE, "c", "monob")
        cross(c, 1330, 450, 80, ap(t, ti_ + .5, .4), 12, RED, L_)
        src(c, "SRC: EWEEK / INTERESTING ENGINEERING, FEB 2026", t, a0 + 1.0, a1)
    # ---- 3.13 summary checklist
    a0 = S("3.13") - .05
    M = ap(t, a0, .4)
    if M > 0:
        rows = (("PHYSICS", "NOT THE PROBLEM", True), ("VARIETY", "THE PROBLEM", False), ("PRACTICE", "THE PROBLEM", False))
        for i, (nm, sub, ok) in enumerate(rows):
            ya = 250 + i * 170
            tt_ = a0 + .3 + i * .9 if i else a0 + .2
            aa = ap(t, tt_, .4) * M
            card(c, 300, ya - 65, 1320, 130, e_out(prog(t, tt_, tt_ + .5)), LINE, M)
            tag(c, nm, 380, ya, aa, 60, LINE, "l", "monob")
            tag(c, sub, 1200, ya, aa, 40, CYAN if ok else LINE, "c", "monob")
            if ok: check(c, 1540, ya, 30, ap(t, tt_ + .4, .3), 10, CYAN, M)
            else: cross(c, 1540, ya, 30, ap(t, tt_ + .4, .3), 10, RED, M)
