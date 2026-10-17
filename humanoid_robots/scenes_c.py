# -*- coding: utf-8 -*-
"""Sheets 5-7: the data gap; reading a demo; when."""
import math, random
import skia
from lib import *
from props import *
from scenes_a import T, S, E, Wd, win, src, ground, flip_loop, check_mark
from scenes_b import tag
REG = {}
def reg_c(k):
    def deco(fn): REG[k] = fn; return fn
    return deco

def tabs(c, t, a, cur, alpha=1.0):
    names = ("1 TELEOPERATION", "2 SIMULATION", "3 HUMAN VIDEO")
    for i, nm in enumerate(names):
        x = 140 + i * 560
        hl = (cur == i)
        card(c, x, 110, 520, 74, e_out(prog(t, a + i * .2, a + i * .2 + .5)), CYAN if hl else LINE, alpha * (1 if hl else .55), 3.5 if hl else 2.5)
        tag(c, nm, x + 260, 147, ap(t, a + i * .2 + .2, .4) * alpha * (1 if hl else .6), 36, CYAN if hl else LINE, "c", "monob")

# ==================================================================================================
@reg_c(4)
def seg4(c, t):
    # ---- 4.1 motors vs data
    a0 = S("4.1") - .05; a1 = S("4.2") - .1
    A = win(t, a0, a1, .4, .3)
    if A > 0:
        for i, (nm, ok, ph) in enumerate((("MOTORS", True, "Not the motors"), ("DATA", False, "The data"))):
            ya = 300 + i * 230; tt_ = Wd("4.1", ph) if i else a0 + .3
            card(c, 400, ya - 85, 1120, 170, e_out(prog(t, tt_, tt_ + .5)), LINE, A)
            tag(c, nm, 520, ya, ap(t, tt_ + .2, .4) * A, 84, LINE, "l", "monob")
            if ok: check(c, 1380, ya, 46, ap(t, tt_ + .5, .3), 14, CYAN, A)
            else: cross(c, 1380, ya, 46, ap(t, tt_ + .5, .3), 14, RED, A)
        tag(c, "THE REAL BOTTLENECK", 960, 140, ap(t, a0, .5) * A, 56, CYAN, "c", "monob")
    # ---- 4.2 15 trillion tokens
    a0 = S("4.2") - .05; a1 = S("4.3") - .1
    B = win(t, a0, a1, .4, .3)
    if B > 0:
        tag(c, "CHATBOTS LEARNED FROM TEXT", 960, 140, ap(t, a0, .5) * B, 52, LINE, "c", "monob")
        for i in range(9):
            ia = ap(t, a0 + .3 + i * .22, .4)
            book_icon(c, 220 + i * 185, 380 + 24 * math.sin(i * 1.3), .85, LINE, ia * B)
        tt_ = Wd("4.2", "15 trillion")
        tr = prog(t, tt_, tt_ + 2.2)
        tag(c, roll(15_000_000_000_000, tr), 960, 600, ap(t, tt_ - .2, .4) * B, 92, LINE, "c", "monob")
        tag(c, "TOKENS · META'S LLAMA 3", 960, 700, ap(t, tt_, .5) * B, 44, CYAN, "c", "monob")
        src(c, "SRC: META, LLAMA 3 PAPER, 2024", t, a0 + 1.0, a1)
    # ---- 4.3 reading time
    a0 = S("4.3") - .05; a1 = S("4.4") - .1
    C = win(t, a0, a1, .4, .3)
    if C > 0:
        rows = [("15 TRILLION TOKENS", None), ("x 3/4 = ABOUT 11 TRILLION WORDS", "three-quarters"), ("/ 238 WORDS PER MINUTE", "238"), ("= NONSTOP READING:", "reading that much")]
        for i, (s_, ph) in enumerate(rows):
            tt_ = a0 + .1 if ph is None else Wd("4.3", ph, off=-.2)
            tag(c, s_, 150, 200 + i * 100, ap(t, tt_, .5) * C, 44, LINE if i < 3 else CYAN, "l", "monob")
        t9 = Wd("4.3", "90,000")
        pr = prog(t, t9 - .3, t9 + 1.8)
        tag(c, roll(90000, pr) + " YEARS", 960, 700, ap(t, t9 - .4, .4) * C, 130, AMBER, "c", "monob")
        person(c, 1600, 300, 1.2, alpha=ap(t, Wd("4.3", "reading"), .5) * C)
        rect(c, 1330, 470, 520, 36, ap(t, Wd("4.3", "reading"), .6), 3, LINE, C)
        c.drawRect(skia.Rect.MakeXYWH(1330, 470, 520 * e_out(prog(t, Wd("4.3", "reading"), E("4.3") - .3)), 36), P(CYAN, alpha=.7 * C))
        src(c, "SRC: OPENAI TOKENS, BRYSBAERT 2019 · OUR ARITHMETIC", t, a0 + 1.0, a1) if False else src(c, "SRC: OPENAI, BRYSBAERT 2019 · OUR ARITHMETIC", t, a0 + 1.0, a1)
    # ---- 4.4 Open X-Embodiment
    a0 = S("4.4") - .05; a1 = S("4.5") - .1
    Dd = win(t, a0, a1, .4, .3)
    if Dd > 0:
        tag(c, "OPEN X-EMBODIMENT", 960, 140, ap(t, a0, .5) * Dd, 52, LINE, "c", "monob")
        for i in range(22):
            r_, k_ = divmod(i, 6)
            ia = ap(t, a0 + .4 + i * .08, .3)
            x0 = 190 + k_ * 180; y0 = 270 + r_ * 135
            if ia > 0:
                if i % 2: quad(c, x0, y0 + 60, .9, (t * .5 + i * .11) % 1, LINE, ia * Dd)
                else: robot_side(c, x0, y0 + 5, s=.3, alpha=ia * Dd, ghost=True, **dict(b=0, a1=0, a2=0, u1=8, u2=18))
        t1 = Wd("4.4", "21 institutions"); t2 = Wd("4.4", "a million"); t3 = Wd("4.4", "22 kinds")
        tag(c, roll(21, prog(t, t1, t1 + .8)) + " INSTITUTIONS", 1340, 270, ap(t, t1 - .2, .4) * Dd, 44, LINE, "l", "monob")
        tag(c, roll(1_000_000, prog(t, t2, t2 + 1.4)) + "+", 1340, 420, ap(t, t2 - .2, .4) * Dd, 80, LINE, "l", "monob")
        tag(c, "ROBOT TRAJECTORIES", 1340, 500, ap(t, t2, .4) * Dd, 36, CYAN, "l", "monob")
        tag(c, roll(22, prog(t, t3, t3 + .8)) + " KINDS OF ROBOT", 1340, 620, ap(t, t3 - .2, .4) * Dd, 44, LINE, "l", "monob")
        src(c, "SRC: OPEN X-EMBODIMENT COLLAB., 2023", t, a0 + 1.0, a1)
    # ---- 4.5 DROID
    a0 = S("4.5") - .05; a1 = S("4.6") - .1
    F = win(t, a0, a1, .4, .3)
    if F > 0:
        tag(c, "ONE TRAJECTORY = ONE SHORT ATTEMPT", 640, 140, ap(t, Wd("4.5", "each trajectory"), .5) * F, 40, CYAN, "c", "monob")
        pts = [(180 + i * 12, 420 + 90 * math.sin(i * .17) * math.cos(i * .05) + 30 * math.sin(i * .5)) for i in range(80)]
        draw_on(c, pts, e_out(prog(t, a0 + .2, a0 + 2.2)), 4, LINE, F)
        circle(c, 180, pts[0][1], 12, ap(t, a0 + .2, .3), 3, CYAN, F, fill=CYAN)
        for j in range(3, 5):
            ph_ = j * 1.9 + 1.3; tj = a0 + 2.6 + j * .35
            pj = [(180 + i * 12, 210 + j * 0 + 40 * math.sin(i * .21 + ph_) * math.cos(i * .06 + j) + 16 * math.sin(i * .5 + j) + (j - 2) * 0) for i in range(80)]
            if j < 3: pj = [(x_, y_ - 95 + 0) for x_, y_ in pj]
            else: pj = [(x_, y_ + 255 + (j - 3) * 90) for x_, y_ in pj]
            draw_on(c, pj, e_out(prog(t, tj, tj + .9)), 3, LINE, F * .55)
        tt_ = Wd("4.5", "DROID dataset") if False else Wd("4.5", "The DROID")
        tag(c, "DROID", 640, 640, ap(t, tt_, .5) * F, 64, LINE, "c", "monob")
        t50 = Wd("4.5", "50 people")
        tag(c, "50 PEOPLE · 12 MONTHS", 640, 720, ap(t, t50, .5) * F, 40, CYAN, "c", "monob")
        t76 = Wd("4.5", "76,000")
        tag(c, roll(76000, prog(t, t76, t76 + 1.2)), 1400, 260, ap(t, t76 - .2, .4) * F, 100, LINE, "c", "monob")
        tag(c, "TRAJECTORIES", 1400, 340, ap(t, t76, .4) * F, 40, CYAN, "c", "monob")
        t3 = Wd("4.5", "350")
        poly_arrow(c, [(1400, 380), (1400, 450)], e_out(prog(t, t3 - .6, t3)), 4, CYAN, F)
        clock_icon(c, 1210, 580, 70, (t * .2) % 1, LINE, ap(t, t3 - .3, .4) * F)
        tag(c, "~" + roll(350, prog(t, t3, t3 + 1.2)) + " HOURS", 1520, 580, ap(t, t3 - .3, .4) * F, 64, LINE, "c", "monob")
        src(c, "SRC: KHAZATSKY ET AL., DROID, 2024", t, a0 + 1.0, a1)
    # ---- 4.6 AgiBot World -> 124 days
    a0 = S("4.6") - .05; a1 = S("4.7") - .1
    G = win(t, a0, a1, .4, .3)
    if G > 0:
        tag(c, "AGIBOT WORLD · 2025", 640, 150, ap(t, a0, .5) * G, 52, LINE, "c", "monob")
        t3 = Wd("4.6", "3,000")
        tag(c, "~" + roll(3000, prog(t, t3, t3 + 1.3)), 640, 330, ap(t, t3 - .3, .4) * G, 120, LINE, "c", "monob")
        tag(c, "HOURS OF RECORDINGS", 640, 430, ap(t, t3, .4) * G, 40, CYAN, "c", "monob")
        for j in range(12):
            ia = ap(t, a0 + .5 + j * .12, .3)
            if ia > 0: robot_side(c, 150 + j * 78, 720 - 20, s=.2, alpha=ia * G * .8, ghost=True, **dict(b=0, a1=0, a2=0, u1=8, u2=18)) if False else None
        t100 = Wd("4.6", "over a hundred")
        tag(c, "100+ ROBOTS", 640, 560, ap(t, t100, .5) * G, 56, LINE, "c", "monob")
        td = Wd("4.6", "124 days") if False else Wd("4.6", "That is")
        n = 124
        for i in range(n):
            r_, k_ = divmod(i, 16)
            ia = prog(t, td + i * .012, td + i * .012 + .2)
            if ia > 0: c.drawRect(skia.Rect.MakeXYWH(1150 + k_ * 40, 250 + r_ * 40, 30, 30), P(AMBER, alpha=.55 * ia * G))
        tag(c, roll(124, prog(t, td, td + 1.6)) + " DAYS", 1390, 640, ap(t, td, .4) * G, 72, AMBER, "c", "monob")
        src(c, "SRC: AGIBOT WORLD, ARXIV 2503.06669 / HF", t, a0 + 1.0, a1)
    # ---- 4.7 90,000 years vs 124 days
    a0 = S("4.7") - .05; a1 = S("4.8") - .1
    H_ = win(t, a0, a1, .4, .3)
    if H_ > 0:
        k1 = e_out(prog(t, a0 + .1, a0 + 1.3))
        c.drawRect(skia.Rect.MakeXYWH(150, 250, 1620 * k1, 90), P(AMBER, alpha=.35 * H_)); c.drawRect(skia.Rect.MakeXYWH(150, 250, 1620 * k1, 90), P(AMBER, "stroke", 4, H_))
        tag(c, "90,000 YEARS OF TEXT", 960, 190, ap(t, a0 + .1, .4) * H_, 56, AMBER, "c", "monob")
        tr_ = Wd("4.7", "four months")
        c.drawRect(skia.Rect.MakeXYWH(150, 480, 4, 90), P(CYAN, alpha=H_ * ap(t, tr_ - .4, .3)))
        tag(c, "4 MONTHS OF ROBOT", 520, 640, ap(t, tr_ - .3, .4) * H_, 52, CYAN, "l", "monob")
        mk = ap(t, tr_ + .3, .5) * H_
        c.drawCircle(150, 525, 70, P(BG, alpha=.9 * mk)); c.drawCircle(150, 525, 70, P(LINE, "stroke", 4, mk))
        c.drawRect(skia.Rect.MakeXYWH(146, 495, 8, 60), P(CYAN, alpha=mk))
    # ---- 4.8 200,000 : 1
    a0 = S("4.8") - .05; a1 = S("4.9") - .1
    I = win(t, a0, a1, .4, .3)
    if I > 0:
        tt_ = Wd("4.8", "200,000")
        book_icon(c, 560, 270, .75, LINE, ap(t, a0 + .1, .5) * I)
        tag(c, "A TOKEN", 560, 390, ap(t, a0 + .3, .4) * I, 40, LINE, "c", "monob")
        te = ap(t, Wd("4.8", "are not the same"), .4) * I
        line(c, 880, 255, 1040, 255, e_out(prog(t, Wd("4.8", "are not the same"), Wd("4.8", "are not the same") + .4)), 8, AMBER if False else LINE, I)
        line(c, 880, 295, 1040, 295, e_out(prog(t, Wd("4.8", "are not the same") + .1, Wd("4.8", "are not the same") + .5)), 8, LINE, I)
        line(c, 905, 320, 1015, 230, e_out(prog(t, Wd("4.8", "are not the same") + .3, Wd("4.8", "are not the same") + .7)), 8, RED, I)
        clock_icon(c, 1360, 270, 65, (t * .15) % 1, LINE, ap(t, a0 + .6, .5) * I)
        tag(c, "A ROBOT HOUR", 1360, 390, ap(t, a0 + .8, .4) * I, 40, LINE, "c", "monob")
        tag(c, "BUT IN TIME, THE GAP IS", 960, 520, ap(t, Wd("4.8", "in time"), .5) * I, 44, CYAN, "c", "monob")
        tag(c, "MORE THAN", 960, 590, ap(t, Wd("4.8", "more than"), .5) * I, 40, LINE)
        tag(c, roll(200000, prog(t, tt_ - .2, tt_ + 1.5)) + " : 1", 960, 720, ap(t, tt_ - .4, .4) * I, 150, AMBER, "c", "monob")
    # ---- 4.9 where does robot data come from
    a0 = S("4.9") - .05; a1 = S("4.10") - .1
    Jj = win(t, a0, a1, .4, .3)
    if Jj > 0:
        tag(c, "WHERE DOES ROBOT DATA COME FROM?", 960, 160, ap(t, a0, .5) * Jj, 52, LINE, "c", "monob")
        rect(c, 760, 560, 400, 160, ap(t, a0 + .4, .6), 4, LINE, Jj, fill=CYAN, falpha=.2)
        tag(c, "ROBOT DATA", 960, 640, ap(t, a0 + .8, .4) * Jj, 48, LINE, "c", "monob")
        for i, nm in enumerate(("1 TELEOPERATION", "2 SIMULATION", "3 HUMAN VIDEO")):
            tt_ = a0 + 1.4 + i * .8; x = 330 + i * 630
            card(c, x - 240, 280, 480, 90, e_out(prog(t, tt_, tt_ + .5)), LINE, Jj)
            tag(c, nm, x, 325, ap(t, tt_ + .2, .4) * Jj, 36, LINE, "c", "monob")
            poly_arrow(c, [(x, 370), (x, 440), (960, 540)] if i != 1 else [(x, 370), (x, 540)], e_out(prog(t, tt_ + .3, tt_ + 1.0)), 3.5, CYAN, Jj, 18, [12, 9])
    # ---- 4.10 teleoperation
    a0 = S("4.10") - .05; a1 = S("4.11") - .1
    K = win(t, a0, a1, .4, .3)
    if K > 0:
        tabs(c, t, a0 - 1, 0, K)
        person(c, 330, 440, 1.5, headset=True, alpha=ap(t, a0 + .2, .6) * K)
        tag(c, "OPERATOR", 330, 600, ap(t, a0 + .4, .4) * K, 36, CYAN)
        # hand controllers
        for sx in (-1, 1):
            c.drawCircle(330 + sx * 190, 520, 24, P(CYAN, "stroke", 4, ap(t, a0 + .8, .4) * K))
        tdv = Wd("4.10", "drives")
        for i, sx in enumerate((-1, 1)):
            draw_on(c, [(330 + sx * 190, 520), (780, 450 + i * 120), (1000, 430 + i * 120)], e_out(prog(t, tdv, tdv + 1.0)), 3, CYAN, K, dash=[12, 9])
        cyr, cxr = 560, 1040
        sw = math.sin(t * 2.5)
        robot_arms(c, cxr, 330, [(cxr - 160 + 40 * sw, 620 + 20 * sw), (cxr + 160 - 40 * sw, 620 - 20 * sw)], (.3, .3), s=.8, alpha=ap(t, tdv - .2, .6) * K)
        c.drawLine(cxr - 280, 700, cxr + 280, 700, P(LINE, "stroke", 3.5, K))
        trec = Wd("4.10", "records")
        if t > trec:
            on = (int((t - trec) * 2) % 2 == 0)
            c.drawCircle(1620, 270, 18, P(RED, alpha=(1.0 if on else .25) * K)); tag(c, "REC", 1700, 270, ap(t, trec, .3) * K, 44, LINE, "c", "monob")
        t50 = Wd("4.10", "50 demonstrations")
        tag(c, roll(50, prog(t, t50, t50 + .8)) + " DEMOS / TASK", 1610, 420, ap(t, t50 - .2, .4) * K, 40, LINE, "c", "monob")
        t90 = Wd("4.10", "90 percent")
        tag(c, "UP TO +" + roll(90, prog(t, t90, t90 + 1.0)) + "% SUCCESS", 1610, 520, ap(t, t90 - .2, .4) * K, 40, CYAN, "c", "monob")
        tsh = Wd("4.10", "shrimp")
        tag(c, "E.G. COOKING A SHRIMP", 1600, 620, ap(t, tsh - .3, .4) * K, 36, LINE)
        src(c, "SRC: MOBILE ALOHA, STANFORD, 2024", t, a0 + 1.0, a1)
    # ---- 4.11 slow by design
    a0 = S("4.11") - .05; a1 = S("4.12") - .1
    L_ = win(t, a0, a1, .4, .3)
    if L_ > 0:
        tabs(c, t, a0 - 1, 0, L_)
        clock_icon(c, 520, 450, 120, (t - a0) * .08, LINE, L_)
        tag(c, "1 HOUR OF DATA", 520, 640, ap(t, a0 + .3, .4) * L_, 44, LINE, "c", "monob")
        tag(c, "COSTS", 960, 450, ap(t, Wd("4.11", "costs"), .4) * L_, 56, CYAN, "c", "monob")
        person(c, 1400, 440, 1.5, alpha=ap(t, Wd("4.11", "an hour of data"), .5) * L_)
        tag(c, "AT LEAST 1 HOUR OF A HUMAN", 1400, 640, ap(t, Wd("4.11", "at least"), .4) * L_, 40, LINE, "c", "monob")
    # ---- 4.12 simulation
    a0 = S("4.12") - .05; a1 = S("4.13") - .1
    M = win(t, a0, a1, .4, .3)
    if M > 0:
        tabs(c, t, a0 - 1, 1, M)
        gy = 640
        ground(c, t, a0, gy, 150, 850, .6)
        flip_loop(c, t, a0 + .2, 4.0, gy, 500, .8, M)
        check(c, 500, 700, 36, ap(t, Wd("4.12", "backflips") - .3, .3), 12, CYAN, M)
        tag(c, "BACKFLIP", 500, 760, M, 36, LINE, "c", "monob")
        draw_shirt(c, 1300, 450, 1.2, 0, 0, 0, alpha=M, crumple=.5 + .2 * math.sin(t * 2), seed=t * .7)
        cross(c, 1300, 700, 36, ap(t, Wd("4.12", "badly for cloth"), .4), 12, RED, M)
        tag(c, "CLOTH", 1300, 760, M, 36, LINE, "c", "monob")
    # ---- 4.13 human video
    a0 = S("4.13") - .05
    N = ap(t, a0, .4)
    if N > 0:
        tabs(c, t, a0 - 1, 2, N)
        person(c, 330, 420, 1.3, alpha=N)
        camera_icon(c, 330, 300, .6, CYAN, ap(t, a0 + .4, .4) * N)
        tag(c, "FIRST-PERSON VIDEO", 330, 600, ap(t, a0 + .5, .4) * N, 36, LINE)
        rect(c, 620, 260, 520, 330, ap(t, a0 + .6, .6), 3.5, LINE, N)
        draw_shirt(c, 880, 430, .8, 0, 0, 0, alpha=ap(t, a0 + 1.0, .5) * N, crumple=.2, seed=2)
        hand_outline(c, 760, 520, .35, 1, LINE, ap(t, a0 + 1.4, .5) * N)
        # channels
        tv = Wd("4.13", "navigate")
        tag(c, "VISION", 1300, 300, ap(t, tv - .4, .4) * N, 44, LINE, "l", "monob")
        c.drawRect(skia.Rect.MakeXYWH(1300, 340, 440 * e_out(prog(t, tv - .2, tv + 1.0)), 40), P(CYAN, alpha=.5 * N))
        tn = Wd("4.13", "no touch")
        tag(c, "TOUCH", 1300, 470, ap(t, tn - .4, .4) * N, 44, LINE, "l", "monob")
        line(c, 1300, 540, 1740, 540, e_out(prog(t, tn - .2, tn + .8)), 4, LINE, N)
        tag(c, "NO SIGNAL", 1520, 600, ap(t, tn, .4) * N, 40, CYAN, "c", "monob")
        src(c, "SRC: FIGURE (COMPANY-REPORTED); R. BROOKS", t, a0 + 1.0, 1e9) if False else src(c, "SRC: FIGURE AI (COMPANY-REPORTED)", t, a0 + 1.0, 1e9)

# ==================================================================================================
@reg_c(5)
def seg5(c, t):
    # ---- 5.1 player
    a0 = S("5.1") - .05; a1 = S("5.2") - .1
    A = win(t, a0, a1, .4, .3)
    if A > 0:
        rect(c, 360, 190, 1200, 560, e_out(prog(t, a0, a0 + .8)), 4, LINE, A)
        draw_on(c, [(960 - 40, 410), (960 - 40, 530), (960 + 60, 470)], ap(t, a0 + .6, .6), 6, CYAN, A, close=True)
        line(c, 400, 700, 1520, 700, e_out(prog(t, a0 + .5, a0 + 1.2)), 5, LINE, A * .7)
        c.drawCircle(400 + 1120 * prog(t, a0 + 1.0, a1), 700, 12, P(CYAN, alpha=A))
        person(c, 1700, 300, .9, alpha=ap(t, Wd("5.1", "hard to read"), .6) * A * .6)
        tag(c, "OFF-CAMERA?", 1700, 410, ap(t, Wd("5.1", "hard to read"), .6) * A, 36, CYAN)
    # ---- 5.2 Tesla event
    a0 = S("5.2") - .05; a1 = S("5.3") - .1
    B = win(t, a0, a1, .4, .3)
    if B > 0:
        tag(c, "OCT 2024 · WE, ROBOT EVENT", 700, 150, ap(t, a0, .5) * B, 48, LINE, "c", "monob")
        robot_arms(c, 520, 330, [(340, 560), (700, 540)], (.5, .5), s=.9, alpha=ap(t, a0 + .3, .6) * B)
        c.drawLine(180, 700, 880, 700, P(LINE, "stroke", 4, B))
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(690, 540, 44, 60), 8, 8), P(CYAN, "stroke", 4, ap(t, a0 + 1.0, .4) * B))
        tag(c, "SERVING DRINKS", 520, 760, ap(t, Wd("5.2", "serving"), .4) * B, 36, CYAN)
        tp = Wd("5.2", "people in another")
        for i in range(2):
            person(c, 1250 + i * 230, 340, .85, headset=False, alpha=ap(t, tp + i * .3, .5) * B * .8)
            draw_on(c, [(1250 + i * 230 - 70, 400), (1000, 460), (720, 420)], e_out(prog(t, tp + .6 + i * .3, tp + 1.4 + i * .3)), 3, CYAN, B, dash=[12, 9])
        tag(c, "ANOTHER LOCATION", 1365, 480, ap(t, tp + .2, .5) * B, 36, CYAN)
        tb = Wd("5.2", "Bloomberg")
        tag(c, "BLOOMBERG: MANY INTERACTIONS OVERSEEN", 1250, 600, ap(t, tb, .5) * B, 36, LINE)
        tt_ = Wd("5.2", "a Tesla official")
        tag(c, "TESLA OFFICIAL: SOME FUNCTIONS REMOTE", 1250, 670, ap(t, tt_, .5) * B, 36, LINE)
        src(c, "SRC: BLOOMBERG, 14 OCT 2024", t, a0 + 1.0, a1)
    # ---- 5.3 Neo test
    a0 = S("5.3") - .05; a1 = S("5.4") - .1
    C = win(t, a0, a1, .4, .3)
    if C > 0:
        tag(c, "OCT 2025 · WSJ HOME-ROBOT TEST", 700, 150, ap(t, a0, .5) * C, 48, LINE, "c", "monob")
        robot_side(c, 420, 480, s=1.3, alpha=ap(t, a0 + .3, .6) * C, **dict(b=0, a1=0, a2=0, u1=40 + 35 * math.sin(t * 1.6), u2=70 + 40 * math.sin(t * 1.6 + .6)))
        c.drawLine(180, 480 + 216 * 1.3 - 14, 700, 480 + 216 * 1.3 - 14, P(LINE, "stroke", 4, C))
        top = Wd("5.3", "remote human operator")
        person(c, 1250, 330, 1.2, headset=True, alpha=ap(t, top - .3, .6) * C)
        tag(c, "REMOTE OPERATOR · VR", 1250, 470, ap(t, top, .5) * C, 36, CYAN)
        draw_on(c, [(1150, 360), (900, 420), (600, 330)], e_out(prog(t, top + .3, top + 1.2)), 3, CYAN, C, dash=[12, 9])
        if t > top + 1.3: runner(c, t, [(1150, 360), (900, 420), (600, 330)], 1.8, CYAN, C, 8)
        tp = Wd("5.3", "20,000")
        tag(c, "$" + roll(20000, prog(t, tp, tp + 1.2)), 1250, 640, ap(t, tp - .3, .4) * C, 96, LINE, "c", "monob")
        src(c, "SRC: WSJ, OCT 2025 (VIA DARING FIREBALL, DRONEXL)", t, a0 + 1.0, a1) if False else src(c, "SRC: WSJ TEST, OCT 2025 (VIA DRONEXL)", t, a0 + 1.0, a1)
    # ---- 5.4 / 5.5 / 5.6 the human is part of the plan: a loop
    a0 = S("5.4") - .05; a1 = S("5.7") - .1
    Dd = win(t, a0, a1, .4, .3)
    if Dd > 0:
        nodes = [("HUMAN HELPS", 560, 280), ("DATA", 1360, 280), ("BETTER MODEL", 1360, 600), ("LESS HELP", 560, 600)]
        times = [a0 + .2, a0 + 1.4, a0 + 2.6, a0 + 3.8]
        for i, (nm, x, y) in enumerate(nodes):
            card(c, x - 220, y - 55, 440, 110, e_out(prog(t, times[i], times[i] + .5)), CYAN if i == 0 else LINE, Dd)
            tag(c, nm, x, y, ap(t, times[i] + .2, .4) * Dd, 44, LINE, "c", "monob")
        for i in range(4):
            x0, y0 = nodes[i][1], nodes[i][2]; x1, y1 = nodes[(i + 1) % 4][1], nodes[(i + 1) % 4][2]
            dx = (x1 - x0); dy = (y1 - y0); L = math.hypot(dx, dy); ux, uy = dx / L, dy / L
            sx = x0 + ux * 235 if abs(dx) > abs(dy) else x0; sy = y0 + uy * 70 if abs(dy) >= abs(dx) else y0
            ex = x1 - ux * 235 if abs(dx) > abs(dy) else x1; ey = y1 - uy * 70 if abs(dy) >= abs(dx) else y1
            poly_arrow(c, [(sx, sy), (ex, ey)], e_out(prog(t, times[i] + .5, times[i] + 1.1)), 4, CYAN, Dd)
        if t > a0 + 5.0:
            loop = [(nodes[0][1] + 235, nodes[0][2]), (nodes[1][1] - 235, nodes[1][2]), (nodes[1][1], nodes[1][2] + 70), (nodes[2][1], nodes[2][2] - 70), (nodes[2][1] - 235, nodes[2][2]), (nodes[3][1] + 235, nodes[3][2]), (nodes[3][1], nodes[3][2] - 70), (nodes[0][1], nodes[0][2] + 70)]
            runner(c, t, loop + [loop[0]], 4.0, CYAN, Dd, 9)
            kk = int((t - a0 - 5.0) / 1.0) % 4
            c.drawRect(skia.Rect.MakeXYWH(nodes[kk][1] - 220, nodes[kk][2] - 55, 440, 110), P(CYAN, alpha=.18 * Dd * (1 - ((t - a0 - 5.0) % 1.0))))
        tq = Wd("5.4", "1X\'s chief executive")
        tag(c, "1X CEO: NO CUSTOMER DATA, NO BETTER PRODUCT", 960, 730, ap(t, tq, .5) * Dd, 36, LINE)
        src(c, "SRC: WSJ, OCT 2025 (VIA ROAD TO VR)", t, a0 + 1.0, S("5.5") - .05)
        t5 = Wd("5.5", "corrections")
        tag(c, "CORRECTIONS FEED BACK", 960, 200, ap(t, t5 - .2, .5) * Dd, 40, CYAN, "c", "monob")
        src(c, "SRC: WEAVE ROBOTICS, 2026 (VIA EWEEK)", t, S("5.5") - .1, a1)
        t6 = Wd("5.6", "stopgap")
        tag(c, "STOPGAP", 200 + 130, 440 if False else 440, ap(t, t6, .4) * Dd, 44, AMBER if False else CYAN, "c", "monob") if False else None
        if t > t6 - .2:
            tag(c, "A STOPGAP", 340, 400, ap(t, t6, .4) * Dd, 40, LINE, "c", "monob")
            tag(c, "AND A DATA SOURCE", 340, 460, ap(t, Wd("5.6", "data comes from") - .5, .4) * Dd, 40, CYAN, "c", "monob")
    # ---- 5.7 / 5.8 three questions
    a0 = S("5.7") - .05; a1 = S("5.9") - .1
    Ee = win(t, a0, a1, .4, .3)
    if Ee > 0:
        tag(c, "READING A DEMO: THREE QUESTIONS", 960, 150, ap(t, a0, .5) * Ee, 52, LINE, "c", "monob")
        qs = [("1", "AUTONOMOUS,", "OR SOMEONE DRIVING?", "autonomous"), ("2", "REAL SPEED?", "", "real speed"), ("3", "HOW MANY", "TRIES?", "how many tries")]
        for i, (n, l1, l2, ph) in enumerate(qs):
            tt_ = a0 + .5 + i * .8; tq_ = Wd("5.8", ph, off=-.2); x = 330 + i * 630
            card(c, x - 280, 260, 560, 400, e_out(prog(t, tt_, tt_ + .6)), LINE, Ee)
            tag(c, n, x, 340, ap(t, tt_ + .3, .4) * Ee, 100, CYAN, "c", "monob")
            if t > tt_ + 1.0: pulse(c, t, x, 340, 50, 100, 2.0, CYAN, Ee * .6, 2, 3)
            tag(c, l1, x, 470, ap(t, tt_ + .4, .4) * Ee, 40, LINE, "c", "monob")
            if l2: tag(c, l2, x, 520, ap(t, tt_ + .4, .4) * Ee, 36, LINE, "c", "monob")
            rect(c, x - 28, 560, 56, 56, e_out(prog(t, tq_ + .2, tq_ + .6)), 4, CYAN, Ee)
    # ---- 5.9 one in ten
    a0 = S("5.9") - .05
    F = ap(t, a0, .4)
    if F > 0:
        for i in range(10):
            ia = ap(t, a0 + .2 + i * .12, .3)
            x = 330 + i * 130
            if i < 9: rect(c, x - 40, 300, 80, 80, ia, 4, CYAN, F, fill=CYAN, falpha=.4)
            else:
                rect(c, x - 40, 300, 80, 80, ia, 4, LINE, F); cross(c, x, 340, 28, ap(t, a0 + 1.6, .3), 10, RED, F)
        tag(c, "9 OF 10 WORK", 700, 450, ap(t, a0 + 1.4, .4) * F, 48, CYAN, "c", "monob")
        tag(c, "1 FAILS", 1500, 450, ap(t, a0 + 1.8, .4) * F, 48, LINE, "c", "monob")
        person(c, 600, 640, .9, alpha=ap(t, Wd("5.9", "needs someone watching"), .5) * F)
        tag(c, "SOMEONE STILL WATCHING", 760, 640, ap(t, Wd("5.9", "needs someone watching"), .5) * F, 40, LINE, "l", "monob")

# ==================================================================================================
def tline(c, t, a, y=420, x0=200, x1=1720, alpha=1.0, labels=True):
    """2026 -> 2040 timeline"""
    p = e_out(prog(t, a, a + 1.0))
    line(c, x0, y, x0 + (x1 - x0) * p, y, 1, 5, LINE, alpha)
    if p > .9:
        for yr in range(2026, 2041, 2):
            xx = x0 + (x1 - x0) * (yr - 2026) / 14
            c.drawLine(xx, y - 14, xx, y + 14, P(LINE, "stroke", 3, alpha))
            if yr in (2026, 2030, 2036, 2040): text(c, str(yr), xx, y + 62, "mono", 36, LINE, "c", alpha)
def xyr(yr, x0=200, x1=1720): return x0 + (x1 - x0) * (yr - 2026) / 14

@reg_c(6)
def seg6(c, t):
    # ---- 6.1 the question on a timeline
    a0 = S("6.1") - .05; a1 = S("6.2") - .1
    A = win(t, a0, a1, .4, .3)
    if A > 0:
        tline(c, t, a0 + .2, 460, alpha=A)
        tag(c, "NOW", xyr(2026), 380, ap(t, a0 + .8, .4) * A, 40, CYAN, "c", "monob")
        qmark(c, xyr(2033), 330, 160, CYAN, ap(t, a0 + 1.2, .5) * A)
        draw_shirt(c, 960, 640 if False else 640, .45, 0, 0, 0, alpha=ap(t, Wd("6.1", "fold your laundry"), .5) * A)
        tag(c, "AT HOME · ON ITS OWN", 960, 190, ap(t, Wd("6.1", "at home"), .5) * A, 52, LINE, "c", "monob")
    # ---- 6.2 / 6.3 / 6.4 two pillars
    a0 = S("6.2") - .05; a1 = S("6.5") - .1
    B = win(t, a0, a1, .4, .3)
    if B > 0:
        # roof + two pillars
        t1 = a0 + .2
        draw_on(c, [(300, 250), (1620, 250)], e_out(prog(t, t1 + .8, t1 + 1.6)), 6, LINE, B)
        tag(c, "A ROBOT THAT FOLDS YOUR LAUNDRY", 960, 200, ap(t, t1 + 1.2, .5) * B, 44, LINE, "c", "monob")
        for i, nm in enumerate(("1 DATA FROM REAL HOMES", "2 RELIABILITY")):
            xc = 560 + i * 800
            rect(c, xc - 280, 250, 560, 520, e_out(prog(t, t1 + i * .5, t1 + .8 + i * .5)), 4, CYAN if (i == 0 and t < S("6.4") - .1) or (i == 1 and t >= S("6.4") - .1) else LINE, B)
            tag(c, nm, xc, 300, ap(t, t1 + .4 + i * .5, .4) * B, 36, LINE, "c", "monob")
        # data pillar content (6.3)
        t3 = Wd("6.3", "Not thousands")
        base = 740
        h = lambda hours: 330 * math.log10(hours) / 6.6
        for j, (nm, hrs, col) in enumerate((("350 H", 350, LINE), ("3,000 H", 3000, LINE), ("MILLIONS", 3_000_000, CYAN))):
            tt_ = t3 + j * .9 if j < 2 else Wd("6.3", "Millions")
            hh = h(hrs) * e_out(prog(t, tt_, tt_ + 1.0))
            x = 380 + j * 170
            rect(c, x - 55, base - hh, 110, hh, 1, 3.5, col, B, fill=col, falpha=.25)
            tag(c, nm, x, base - hh - 34, ap(t, tt_, .4) * B, 36, col, "c", "monob")
        tag(c, "DROID", 380, base + 0, 0, 36)  # (kept silent)
        tag(c, "TODAY", 465, 795, ap(t, t3, .4) * B, 36, CYAN, "c", "monob")
        # reliability pillar content (6.4)
        t4 = S("6.4")
        for i in range(10):
            ia = ap(t, t4 + .2 + i * .08, .3)
            x = 1180 + (i % 5) * 100; y = 380 + (i // 5) * 100
            ok = i < 9
            if ia > 0:
                rect(c, x - 32, y - 32, 64, 64, 1, 3.5, CYAN if ok else LINE, B * ia, fill=CYAN if ok else None, falpha=.35)
        tag(c, "9 OUT OF 10", 1380, 620, ap(t, t4 + 1.0, .4) * B, 44, LINE, "c", "monob")
        t99 = Wd("6.4", "ninety-nine") if False else Wd("6.4", "99 times")
        tag(c, "99 OUT OF 100", 1380, 700, ap(t, t99, .4) * B, 52, AMBER, "c", "monob")
    # ---- 6.5 now vs Brooks
    a0 = S("6.5") - .05; a1 = S("6.6") - .1
    C = win(t, a0, a1, .4, .3)
    if C > 0:
        tline(c, t, a0, 450, alpha=C)
        tn = Wd("6.5", "already for sale")
        c.drawCircle(xyr(2026), 450, 16, P(CYAN, alpha=C * ap(t, tn - .3, .3)))
        tag(c, "NOW: SOME CLOTHES,", xyr(2026) + 20, 250, ap(t, tn - .3, .4) * C, 36, CYAN, "l", "monob")
        tag(c, "HUMAN ON CALL", xyr(2026) + 20, 296, ap(t, tn - .3, .4) * C, 36, CYAN, "l", "monob")
        tb = Wd("6.5", "Rodney Brooks")
        band = [(xyr(2036), 330), (1720, 330), (1720, 410), (xyr(2036), 410)]
        hatch(c, band, 16, -math.pi / 4, LINE, .5 * C, 2, ap(t, tb + 1.0, 1.0)); draw_on(c, band, e_out(prog(t, tb + 1.0, tb + 1.8)), 3, LINE, C, close=True)
        tag(c, "BROOKS: DEXTERITY STILL", xyr(2036) - 20, 600, ap(t, tb + 1.4, .5) * C, 36, LINE, "r", "monob")
        tag(c, "FAR BEHIND HUMAN HANDS", xyr(2036) - 20, 650, ap(t, tb + 1.4, .5) * C, 36, LINE, "r", "monob")
        tag(c, "PAST 2036", xyr(2036) + 160, 285, ap(t, Wd("6.5", "past 2036"), .5) * C, 44, LINE, "c", "monob")
        src(c, "SRC: RODNEY BROOKS, 2025-26 PREDICTIONS", t, a0 + 1.0, a1)
    # ---- 6.6 our bet
    a0 = S("6.6") - .05; a1 = S("6.7") - .1
    Dd = win(t, a0, a1, .4, .3)
    if Dd > 0:
        tline(c, t, a0 - 1, 450, alpha=Dd)
        t1 = Wd("6.6", "A supervised"); t2 = Wd("6.6", "nobody watching")
        x1 = xyr(2030); x2 = xyr(2035)
        for (x, tt_, l1, l2) in ((x1, t1, "BY END OF DECADE:", "SUPERVISED"), (x2, t2, "NOT BEFORE MID-2030s:", "NOBODY WATCHING")):
            k = ap(t, tt_, .5) * Dd
            c.drawCircle(x, 450, 20, P(AMBER, alpha=k)); pulse(c, t, x, 450, 20, 70, 1.8, AMBER, k * Dd, 2, 3); line(c, x, 430, x, 290, e_out(prog(t, tt_, tt_ + .6)), 4, AMBER, Dd)
            tag(c, l1, x, 190, k, 36, AMBER, "c", "monob"); tag(c, l2, x, 240, k, 36, AMBER, "c", "monob")
        tag(c, "OUR BET (OPINION)", 960, 640, ap(t, Wd("6.6", "My bet"), .5) * Dd, 56, LINE, "c", "monob")
        tag(c, "BETWEEN BROOKS AND TODAY'S HYPE", 960, 710, ap(t, Wd("6.6", "sits in between"), .5) * Dd, 36, CYAN)
    # ---- 6.7 signal: fine print
    a0 = S("6.7") - .05; a1 = S("6.8") - .1
    Ee = win(t, a0, a1, .4, .3)
    if Ee > 0:
        tag(c, "A SIGNAL TO WATCH", 960, 160, ap(t, a0, .5) * Ee, 56, LINE, "c", "monob")
        card(c, 360, 270, 1200, 300, e_out(prog(t, a0 + .3, a0 + 1.0)), LINE, Ee)
        for i, ln in enumerate(("* ROBOT PERFORMS CHORES.", "* IMAGES SHOWN ARE ILLUSTRATIVE.")):
            tag(c, ln, 420, 340 + i * 60, ap(t, a0 + .8 + i * .3, .4) * Ee, 36, LINE, "l")
        tr_ = Wd("6.7", "remote operator")
        tag(c, "* REMOTE OPERATOR MAY ASSIST.", 420, 460, ap(t, tr_ - .3, .4) * Ee, 36, CYAN, "l", "monob")
        rect(c, 410, 425, 740, 70, e_out(prog(t, tr_, tr_ + .8)), 3.5, CYAN, Ee)
        tag(c, "THE DAY THIS LINE DISAPPEARS", 960, 670, ap(t, Wd("6.7", "stops saying"), .5) * Ee, 48, CYAN, "c", "monob")
    # ---- 6.8 lesson
    a0 = S("6.8") - .05; a1 = S("6.9") - .1
    F = win(t, a0, a1, .4, .3)
    if F > 0:
        line(c, 240, 420, 240 + 1440 * e_out(prog(t, a0 + .2, a0 + 1.4)), 420, 1, 5, LINE, F)
        band = [(240, 380), (1680, 380), (1680, 400), (240, 400)]
        fillpoly(c, [(240, 360), (1680, 360), (1680, 480), (240, 480)], CYAN, .12 * ap(t, a0 + .8, 1.0) * F)
        tag(c, "WHAT LOOKS EASY TO US", 960, 190, ap(t, Wd("6.8", "What looks easy"), .5) * F, 52, LINE, "c", "monob")
        tag(c, "EVOLUTION DID THE WORK", 960, 300, ap(t, Wd("6.8", "evolution"), .5) * F, 52, CYAN, "c", "monob")
        tag(c, "NOBODY WROTE IT DOWN AS DATA", 960, 620, ap(t, Wd("6.8", "nobody wrote"), .5) * F, 52, LINE, "c", "monob")
        for i in range(8):
            if ap(t, Wd("6.8", "nobody wrote") + i * .15, .3) > 0:
                rect(c, 340 + i * 160, 520, 100, 40, 1, 3, LINE, F * .6, dash=[8, 8])
    # ---- 6.9 backflip, what was it never asked to do
    a0 = S("6.9") - .05; a1 = S("6.10") - .1
    G = win(t, a0, a1, .4, .3)
    if G > 0:
        gy = 650
        ground(c, t, a0, gy, 120, 820, .6)
        flip_loop(c, t, a0 + .2, 4.4, gy, 470, .85, G)
        tag(c, "DON'T ASK:", 1330, 250, ap(t, Wd("6.9", "don't ask"), .5) * G, 48, LINE, "c", "monob")
        tag(c, "HOW IT GOT SO GOOD", 1330, 320, ap(t, Wd("6.9", "how it got"), .5) * G, 44, LINE, "c", "monob")
        tag(c, "ASK:", 1330, 470, ap(t, Wd("6.9", "Ask what"), .5) * G, 48, CYAN, "c", "monob")
        tag(c, "WHAT WAS IT NEVER", 1330, 540, ap(t, Wd("6.9", "never asked") - .6, .5) * G, 44, CYAN, "c", "monob")
        tag(c, "ASKED TO DO?", 1330, 600, ap(t, Wd("6.9", "never asked") - .2, .5) * G, 44, CYAN, "c", "monob")
    # ---- 6.10 comment prompt
    a0 = S("6.10") - .05
    H_ = ap(t, a0, .4)
    if H_ > 0:
        tag(c, "WHICH CHORE FIRST?", 960, 190, H_, 84, LINE, "c", "monob")
        for i, nm in enumerate(("LAUNDRY", "DISHES", "FLOORS")):
            tt_ = a0 + .8 + i * .5; x = 420 + i * 540
            card(c, x - 220, 300, 440, 150, e_out(prog(t, tt_, tt_ + .5)), LINE, H_)
            tag(c, nm, x, 375, ap(t, tt_ + .2, .4) * H_, 52, LINE, "c", "monob")
        tq = Wd("6.10", "stranger")
        person(c, 960, 660, .8, headset=True, alpha=ap(t, tq - .3, .5) * H_)
        tag(c, "A STRANGER DRIVING IT, WHILE YOU ARE OUT?", 960, 760, ap(t, tq, .5) * H_, 36, CYAN, "c", "monob")
        tag(c, "TELL ME IN THE COMMENTS", 960, 560, ap(t, Wd("6.10", "comments") - .8, .5) * H_, 48, LINE, "c", "monob")
