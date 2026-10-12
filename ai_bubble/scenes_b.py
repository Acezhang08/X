# -*- coding: utf-8 -*-
import math, random
import skia
from lib import *
from scenes_a import T, S, E, Wd, TOP, BOT, GRAYDK, loop_pos, CLOSED

LA = [(0.05,0.0),(0.62,0.0),(0.62,0.12),(0.58,0.18),(0.66,0.28),(0.64,0.4),(0.7,0.52),(0.66,0.62),(0.88,0.62),(0.95,0.72),(0.9,0.82),(0.78,0.78),(0.7,0.86),(0.55,0.85),(0.47,0.78),(0.35,0.80),(0.20,0.72),(0.15,0.64),(0.10,0.55),(0.12,0.4),(0.06,0.3),(0.08,0.15)]

def cam3(t): return (960, 455, 1.0)

def bond_stack(c, x, y, n, t, a):
    for i in range(n):
        al = e_out(prog(t, a + 0.12*i, a + 0.12*i + 0.25))
        if al <= 0: continue
        c.save(); c.translate(x + (i % 2)*10 - 5, y - i*34 + (1-al)*-40); c.rotate((-2 if i % 2 else 2))
        r_ = skia.Rect.MakeXYWH(-150, -80, 300, 160)
        c.drawRect(r_, P(PAPER2, alpha=al)); c.drawRect(r_, P(INK, "stroke", 3.5, al))
        c.drawRect(skia.Rect.MakeXYWH(-138, -68, 276, 136), P(RED, "stroke", 1.8, al))
        c.drawCircle(-90, 0, 24, P(RED, "stroke", 3, al)); text(c, "$", -90, 0, "mono", 30, RED, alpha=al)
        for k in range(3): c.drawLine(-40, -30 + k*30, 110, -30 + k*30, P(INK, "stroke", 3, 0.5*al))
        c.restore()

def seg3(c, t):
    # 3.1 + 3.2 bar and bonds
    t1 = S("3.1"); gone = S("3.3") - 0.1
    with fade(c, t, t1, gone, 0.4):
        base = 820; h = 440; bx = 330
        baseline(c, bx - 190, bx + 190, base)
        bar(c, bx, base, 280, h * 0.78, e_out(prog(t, t1 + 0.3, Wd("3.1", "But not") )), GREEN)
        if t > Wd("3.1", "But not"):
            q = e_out(prog(t, Wd("3.1", "But not"), Wd("3.1", "But not") + 0.8))
            r_ = skia.Rect.MakeXYWH(bx - 140, base - h, 280, h * 0.22 * q)
            c.save(); c.translate(0, 0)
            hatch_rect(c, bx - 140, base - h, 280, h * 0.22 * q, RED)
            c.restore()
            c.drawRect(skia.Rect.MakeXYWH(bx - 140, base - h, 280, h * 0.22 * q), P(INK, "stroke", 3, 0.8))
        text(c, "$800B", bx, base - h - 55, "mono", 84, AMBER)
        fade_text(c, "CASH THEY EARN", bx + 190, 640, t, t1 + 1.0, "sans", 40, GREEN, "l")
        fade_text(c, "BORROWED", bx + 190, 420, t, Wd("3.1", "But not"), "sans", 40, RED, "l")
        text(c, "illustrative", bx, 880, "sansr", 32, GRAYDK)
    t2 = Wd("3.2", "By the end")
    with fade(c, t, t2, gone, 0.4):
        bond_stack(c, 1250, 730, 7, t, Wd("3.2", "170") - 0.5)
        v = roll(t, Wd("3.2", "170"), 1.5, 0, 170)
        text(c, "$%.0fB" % v, 1350, 215, "mono", 150, RED)
        text(c, "IN BONDS · 2026 (TO JUNE)", 1350, 322, "sans", 44)
        text(c, "Source: Aviva Investors, Jul 2026", 1350, 378, "sansr", 32, GRAY)
        fade_text(c, "That's borrowed money.", 1350, 868, t, Wd("3.2", "That's"), "sanss", 40, RED)
    # 3.3 ledger search
    t3 = S("3.3"); g3 = S("3.4") - 0.1
    with fade(c, t, t3, g3, 0.4):
        ledger(c, 960, 450, 1.9, INK)
        text(c, "ASSETS", 790, 315, "sans", 38, INK); text(c, "DEBT", 1130, 315, "sans", 38, INK)
        q = prog(t, t3 + 0.4, E("3.3") - 0.3)
        cx_ = 960 + 260*math.sin(q*math.pi*3.2) ; cy_ = 400 + 190*q + 40*math.sin(q*9)
        pen_ellipse(c, cx_, cy_, 80, 55, 1.0, RED, 7, 8) if 0 < q < 1 else None
        if q >= 1:
            fade_text(c, "?", 1130, 480, t, E("3.3") - 0.3, "mono", 170, RED)
    # 3.4 Louisiana
    t4 = S("3.4"); g4 = S("3.5") - 0.15
    with card(c, 760, 450, 760, 700, -1.2, t, t4 + 0.1, g4, seed=21) as ok:
        if ok:
            pth = skia.Path()
            for i, (x, y) in enumerate(LA):
                px, py = -270 + x*540, -230 + y*470
                pth.moveTo(px, py) if i == 0 else pth.lineTo(px, py)
            pth.close()
            c.drawPath(pth, P(mix(PAPER2, GREEN, 0.15))); c.drawPath(pth, P(INK, "stroke", 5))
            text(c, "LOUISIANA", -80, 20, "serif", 52, INK)
            text(c, "illustrative map", 0, 300, "sansr", 32, GRAYDK)
            q = e_back(prog(t, t4 + 1.0, t4 + 1.5))
            bx_, by_ = -270 + 0.66*540, -230 + 0.2*470
            if q > 0:
                building(c, bx_, by_ + 35, 0.45*q, INK, 1.0)
                pen_ellipse(c, bx_, by_ - 10, 90, 62, prog(t, t4 + 1.5, t4 + 2.1), RED, 5, 3)
                fade_text(c, "HYPERION", bx_ - 40, by_ - 100, t, t4 + 1.6, "mono", 44, RED)
    # 3.5-3.9 Meta + JV
    t5 = S("3.5"); g10 = S("3.10") - 0.1
    with fade(c, t, t5, g10, 0.4):
        stamp(c, "META", 330, 300, t, t5 + 0.1, INK, -2, 52)
        ledger(c, 330, 570, 0.9, INK)
        text(c, "DEBT", 330, 720, "mono", 40, INK)
        c.drawRect(skia.Rect.MakeXYWH(398, 703, 36, 34), P(GRAY, "stroke", 3, dash=[7, 6]))
        # $27B tag
        tag_a = Wd("3.5", "27")
        if t >= tag_a:
            q1 = e_io(prog(t, t5 + 1.0, t5 + 2.6))
            q2 = e_io(prog(t, Wd("3.7", "borrowed") if False else S("3.7") + 0.2, S("3.7") + 1.3))
            x = lerp(520, 800, q1); y = lerp(600, 430, q1) + 8*math.sin(t*3)*(1-q2)
            x = lerp(x, 1480, q2); y = lerp(y, 600, q2)
            tag(c, "$27B DEBT", x, y, t, tag_a, RED, 44, "mono")
            if t5 + 1.0 < t < S("3.7"):
                fade_text(c, "OFF THE BOOKS", 800, 360, t, t5 + 1.8, "sanss", 36, RED)
    t6 = S("3.6")
    with fade(c, t, t6, g10, 0.4):
        r_ = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(1020, 210, 760, 520), 22, 22)
        c.drawRRect(r_, P(INK, "stroke", 4.5, dash=[22, 12]))
        text(c, "JOINT VENTURE", 1400, 262, "sans", 40, INK, spacing=4)
        w80 = 640*0.8*e_out(prog(t, Wd("3.6", "Blue Owl"), Wd("3.6", "Blue Owl") + 0.7))
        w20 = 640*0.2*e_out(prog(t, Wd("3.6", "Meta owns"), Wd("3.6", "Meta owns") + 0.5))
        c.drawRect(skia.Rect.MakeXYWH(1080, 395, w80, 60), P(INK)); c.drawRect(skia.Rect.MakeXYWH(1080+512, 395, w20, 60), P(AMBER))
        c.drawRect(skia.Rect.MakeXYWH(1080, 395, 640, 60), P(INK, "stroke", 3))
        fade_text(c, "80%", 1080+256, 345, t, Wd("3.6", "Blue Owl") + 0.2, "mono", 56, INK)
        fade_text(c, "20%", 1080+576, 345, t, Wd("3.6", "Meta owns") + 0.1, "mono", 56, AMBER)
        fade_text(c, "BLUE OWL", 1080+256, 500, t, Wd("3.6", "Blue Owl"), "sans", 38, INK)
        fade_text(c, "META", 1080+576, 500, t, Wd("3.6", "Meta owns"), "sans", 38, INK)
        text(c, "Source: Bisnow, Oct 2025", 1400, 695, "sansr", 32, GRAY)
    t7 = S("3.7")
    with fade(c, t, t7 + 0.9, g10, 0.4):
        building(c, 1170, 650, 0.5, INK)
        fade_text(c, "data center", 1170, 590, t, t7 + 1.2, "sanss", 32, GRAYDK) if False else None
    with fade(c, t, Wd("3.7", "Meta rents"), g10, 0.4):
        pth = bez((520, 520), (770, 470), (1020, 520))
        arrow(c, pth, e_io(prog(t, Wd("3.7", "Meta rents"), Wd("3.7", "Meta rents") + 0.8)), GREEN, 8, dashed=[18, 12])
        fade_text(c, "RENT", 770, 440, t, Wd("3.7", "Meta rents") + 0.3, "mono", 44, GREEN)
    # contract 3.8
    t8 = S("3.8")
    with card(c, 690, 125, 680, 230, -1.5, t, Wd("3.8", "here's the catch"), g10, seed=23) as ok:
        if ok:
            text(c, "VALUE GUARANTEE", 0, -62, "serif", 50)
            text(c, "16 YEARS", 0, 20, "mono", 76, AMBER)
            sg = skia.Path(); sg.moveTo(150, 80)
            for k in range(1, 8): sg.lineTo(150 + k*18, 80 + (-14 if k % 2 else 14))
            c.drawPath(sg, P(INK, "stroke", 3))
            pen_ellipse(c, 0, 20, 175, 62, prog(t, Wd("3.8", "first 16"), Wd("3.8", "first 16") + 0.8), RED, 6, 9)
    t9 = S("3.9")
    with fade(c, t, t9 + 0.1, g10, 0.4):
        pth = bez((1500, 700), (900, 880), (450, 690))
        arrow(c, pth, e_io(prog(t, t9 + 0.2, t9 + 1.5)), RED, 10)
        fade_text(c, "RISK", 900, 735, t, t9 + 0.9, "mono", 64, RED)
    # 3.10 oracle + 3.11/3.12
    t10 = S("3.10")
    stamp(c, "ORACLE", 380, 160, t, t10 + 0.1, INK, -2, 52)
    stamp(c, "OPENAI", 1540, 160, t, Wd("3.10", "OpenAI"), INK, 2, 52)
    arrow(c, bez((580, 150), (960, 70), (1330, 150)), e_io(prog(t, t10 + 0.5, t10 + 1.6)), GREEN, 10)
    fade_text(c, "builds computing capacity", 960, 215, t, t10 + 1.0, "sanss", 40, GREEN)
    items = [(320, "$25B", "BONDS", RED, "bonds"), (960, "$5B", "PREFERRED", AMBER, "preferred"), (1600, "UP TO $20B", "NEW SHARES", AMBER, "new shares")]
    for i, (x, big, lab, col, w) in enumerate(items):
        with card(c, x, 560, 600, 330, (-1.5, 1.0, -0.8)[i], t, Wd("3.11", w) - 0.5, None, seed=30 + i) as ok:
            if ok:
                text(c, big, 0, -60, "mono", 100 if len(big) < 6 else 66, col)
                text(c, lab, 0, 30, "sans", 48)
                text(c, "Source: Aviva Investors, Jul 2026", 0, 120, "sansr", 32, GRAY)
    t12 = S("3.12")
    with fade(c, t, t12 + 0.2, None, 0.4):
        c.drawRoundRect(skia.Rect.MakeXYWH(120, 372, 1680, 30), 15, 15, P(INK))
        for x in (320, 960, 1600):
            c.drawRoundRect(skia.Rect.MakeXYWH(x - 60, 346, 120, 60), 14, 14, P(INK, "stroke", 8))
        stamp(c, "3 WAYS · 1 YEAR", 960, 810, t, t12 + 0.6, AMBER, -2, 60)

# ======================================================================= SEGMENT 4
def col_h(t):
    a = Wd("4.7", "1.4") - 0.9
    h = 1700 * e_io(prog(t, a, E("4.7") + 0.2))
    if t >= Wd("4.8", "scaled"):
        h = lerp(1700, 729, e_io(prog(t, Wd("4.8", "scaled"), Wd("4.8", "scaled") + 1.4)))
    if t >= S("4.9"): h = lerp(729, 0, prog(t, S("4.9"), S("4.9") + 0.5))
    return h

def cam4(t):
    cx = 960; cy = 455
    t3 = Wd("4.4", "His answer"); t5 = S("4.5") - 0.3
    if t3 <= t < t5 + 0.9:
        cx = lerp(960, 1380, e_io(prog(t, t3, t3 + 0.9)))
        cx = lerp(cx, 960, e_io(prog(t, t5, t5 + 0.9)))
    if t >= S("4.7") - 0.5 and t < S("4.9"):
        top = 840 - col_h(t)
        cy = min(455, top + 330)
    return (cx, cy, 1.0)

def seg4(c, t):
    cx_ = cam4(t)[0]
    # 4.1 loop with doubt
    with fade(c, t, -9, S("4.2") - 0.1, 0.4):
        stamp(c, "NVIDIA", 430, 470, t, -9, INK, -2, 52); stamp(c, "OPENAI", 1490, 470, t, -9, INK, 2, 52)
        arrow(c, TOP, 1, GREEN, 11)
        text(c, "SELLER → BUYER", 960, 384, "mono", 40, GREEN)
        q = prog(t, S("4.1") + 0.2, S("4.1") + 1.0)
        arrow(c, BOT, 1, GREEN, 11, dashed=[22, 14] if t > S("4.1") + 0.3 else None)
        fade_text(c, "revenue?", 960, 556, t, S("4.1") + 0.6, "sanss", 40, GREEN)
        fade_text(c, "?", 960, 650, t, Wd("4.1", "So does"), "mono", 150, AMBER)
    # 4.2 silhouette
    silhouette(c, 330, 420, 1.3, t, S("4.2") + 0.1, "DAVID CAHN · SEQUOIA · 2024", 32, b=S("4.5") - 0.2)
    # 4.3 bars
    t3 = S("4.3")
    xs = [800, 1250, 1700]; hs = [90, 180, 360]; labs = ["CHIP SPEND", "+ BUILDINGS & POWER", "+ CUSTOMER PROFIT"]
    ts_ = [Wd("4.3", "Take"), Wd("4.3", "double it for"), Wd("4.3", "again")]
    fin_b = Wd("4.4", "His answer") + 0.3
    for i in range(3):
        vis_b = fin_b if i < 2 else S("4.5") - 0.2
        with fade(c, t, ts_[i], vis_b, 0.35):
            baseline(c, xs[i] - 150, xs[i] + 150, 820)
            bar(c, xs[i], 820, 280, hs[i], e_out(prog(t, ts_[i], ts_[i] + 0.7)), [INK, GRAY, GREEN][i] if i < 2 else GREEN, 1.0)
            text(c, labs[i], xs[i], 868, "sans", 34, INK)
    for i in range(2):
        with fade(c, t, ts_[i+1] + 0.2, fin_b if i == 0 else Wd("4.4", "His answer") + 0.6, 0.3):
            pth = bez((xs[i] + 40, 820 - hs[i] - 40), (xs[i] + 225, 820 - hs[i+1] - 150), (xs[i+1] - 40, 820 - hs[i+1] - 30))
            arrow(c, pth, e_io(prog(t, ts_[i+1] + 0.2, ts_[i+1] + 0.8)), RED, 8, pen=True)
            fade_text(c, "×2", xs[i] + 225, 820 - hs[i+1] - 190, t, ts_[i+1] + 0.7, "mono", 70, RED)
    # 4.4
    t4 = Wd("4.4", "His answer")
    with fade(c, t, t4 + 0.4, S("4.5") - 0.2, 0.4):
        fade_text(c, "$600B", 1700, 330, t, t4 + 0.6, "mono", 90, AMBER)
        fade_text(c, "A YEAR NEEDED", 1700, 408, t, t4 + 0.7, "sans", 38, INK)
        baseline(c, 2000, 2300, 820)
        bar(c, 2150, 820, 200, 44, e_out(prog(t, Wd("4.4", "earning"), Wd("4.4", "earning") + 0.6)), GREEN)
        fade_text(c, "ACTUAL", 2150, 868, t, Wd("4.4", "earning"), "sans", 38, INK)
        fade_text(c, "illustrative", 2150, 745, t, Wd("4.4", "earning"), "sansr", 32, GRAYDK)
        text(c, "Source: Sequoia, 'AI's $600B Question', Jun 2024", cx_ + 180, 120, "sansr", 32, GRAY)
    # 4.5 OPENAI
    stamp(c, "OPENAI", 960, 300, t, S("4.5") + 0.1, INK, -2, 96, b=S("4.6") + 0.2) if True else None
    # 4.6 green bar
    t6 = S("4.6")
    with fade(c, t, t6 + 0.2, S("4.10") - 0.1, 0.4):
        xg = lerp(420, 700, e_io(prog(t, S("4.9"), S("4.9") + 0.8)))
        base = 840
        baseline(c, xg - 140, xg + 140, base)
        bar(c, xg, base, 160, 16, e_out(prog(t, t6 + 0.3, t6 + 0.9)), GREEN)
        text(c, "$13B", xg, 740, "mono", 80, GREEN)
        text(c, "2025 REVENUE", xg, 790, "sans", 36, INK)
        text(c, "Source: Reuters, Feb 2026", xg, 886, "sansr", 32, GRAY)
    # 4.7 / 4.8 red column
    t7 = S("4.7")
    h = col_h(t)
    if h > 1:
        top = 840 - h
        with fade(c, t, None, None):
            baseline(c, 700, 900, 840)
            bar(c, 800, 840, 180, h, 1.0, RED)
            if h < 1700 and h > 800:
                for k in range(3):
                    c.drawLine(700, 700 - k*40 - 0, 900, 680 - k*40, P(PAPER, "stroke", 0.1, 0))
            lab = "$1.4T" if t < Wd("4.8", "scaled") + 0.6 else "$600B"
            sub = "OVER 8 YEARS" if t < Wd("4.8", "scaled") + 0.6 else "THROUGH 2030"
            text(c, lab, 910, top + 60, "mono", 80, RED, "l")
            text(c, sub, 910, top + 125, "sans", 38, INK, "l")
    silhouette(c, 1450, 600, 1.0, t, S("4.7") + 0.2, "SAM ALTMAN", 34, b=S("4.8"))
    with fade(c, t, Wd("4.7", "Its CEO") + 0.3, S("4.8"), 0.3):
        text(c, "Source: Altman on X, Nov 2025", 1450, 840, "sansr", 32, GRAY)
    # 4.8 projected bar
    t8 = Wd("4.8", "projects")
    with fade(c, t, t8, S("4.10") - 0.1, 0.4):
        xp = lerp(1300, 1250, e_io(prog(t, S("4.9"), S("4.9") + 0.8)))
        baseline(c, xp - 140, xp + 140, 840)
        bar(c, xp, 840, 180, 340, e_out(prog(t, t8 + 0.1, t8 + 1.0)), GREEN, dashed=True)
        text(c, "$280B+", xp, 440, "mono", 80, GREEN)
        text(c, "2030 REVENUE", xp, 890, "sans", 36, INK)
        text(c, "(PROJECTED)", xp, 380, "sans", 36, GREEN) if False else None
        fade_text(c, "(projected)", xp, 385, t, t8 + 0.4, "sanss", 36, GREEN)
    # 4.9 x20 arrow
    t9 = S("4.9")
    with fade(c, t, Wd("4.9", "That's"), S("4.10") + 0.0, 0.3):
        pth = bez((760, 780), (860, 270), (1170, 470))
        arrow(c, pth, e_io(prog(t, Wd("4.9", "That's"), Wd("4.9", "That's") + 0.9)), AMBER, 16, head_size=44)
        fade_text(c, "×20", 960, 300, t, Wd("4.9", "That's") + 0.5, "mono", 170, AMBER)
    # 4.10 back to the loop
    t10 = S("4.10")
    with fade(c, t, t10 + 0.2, None, 0.5):
        stamp(c, "NVIDIA", 430, 470, t, -9, INK, -2, 52); stamp(c, "OPENAI", 1490, 470, t, -9, INK, 2, 52)
        arrow(c, TOP, 1, GREEN, 11)
        arrow(c, BOT, 1, AMBER, 20, head_size=46)
        fade_text(c, "×20", 960, 560, t, t10 + 0.4, "mono", 90, AMBER)
        fade_text(c, "the whole loop depends on it", 960, 840, t, Wd("4.10", "But the"), "sanss", 44, INK)

REG = {3: (cam3, seg3, None), 4: (cam4, seg4, None)}
