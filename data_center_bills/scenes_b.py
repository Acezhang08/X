# -*- coding: utf-8 -*-
"""Segments 2 (why data centers made bills cheaper) and 3 (the flip)."""
from common import *
from scenes_a import cam, ftext, auction

def quote_card(c, cx, cy, w, h, t, a, b, lines, who, size=54, seed=7, rot=-1.0):
    with clip(c, cx, cy, w, h, t, a, b, rot=rot, seed=seed) as ok:
        if ok:
            n = len(lines)
            text(c, "“", -w/2 + 90, -h/2 + 100, "serif", 190, RED)
            y0 = -((n-1)*size*1.15)/2 - 15
            for i, ln in enumerate(lines):
                text(c, ln, 0, y0 + i*size*1.15, "serif", size)
            text(c, who, 0, h/2 - 70, "sansr", 40, DKGRAY)

# ================================================================== SEGMENT 2
def seg2(c, t):
    s = S
    # ---- A0: "the opposite" (2.1)
    a0, b0 = s("2.1") - 0.1, s("2.2") - 0.5
    with ph(c, t, a0, b0, 0.35):
        flip = e_io(prog(t, Wd("2.1", "appear"), Wd("2.1", "appear") + 0.9))
        with clip(c, 960, 450, 980, 560, t, a0, None, rot=-1, seed=41) as ok:
            if ok:
                text(c, "THE EXPECTED STORY", 0, -210, "sans", 48, DKGRAY)
                text(c, "DATA CENTERS", -230, -90, "serif", 64)
                c.save(); c.translate(140, -90)
                text(c, "→", 0, 0, "mono", 90)
                c.restore()
                c.save(); c.translate(0, 85); c.rotate(math.radians(180*flip))
                text(c, "↑", 0, 0, "mono", 250, mix(RED, GREEN, flip))
                c.restore()
                text(c, "ELECTRIC RATES", 0, 215, "sans", 56, INK)
    # ---- A1: the paper (2.2)
    a1, b1 = s("2.2") - 0.05, s("2.3") - 0.5
    with ph(c, t, a1, b1, 0.35):
        with clip(c, 820, 450, 1260, 600, t, a1, None, rot=-0.8, seed=42) as ok:
            if ok:
                text(c, "WORKING PAPER · arXiv · JUNE 2026", 0, -245, "sansr", 40, DKGRAY)
                text(c, "Have Data Centers Raised", 0, -150, "serif", 74)
                text(c, "Your Electric Bill?", 0, -62, "serif", 74)
                c.drawLine(-440, 5, 440, 5, P(INK, "stroke", 3))
                text(c, "Causal Evidence from the United States", 0, 62, "sanss", 46)
                text(c, "Watten · Bistline · Blanford", 0, 135, "sansr", 44, DKGRAY)
        stamp(c, "EPRI", 1640, 235, t, Wd("2.2", "EPRI") - 0.1, INK, 4, 110, pad=(36, 22))
        ftext(c, "Electric Power", 1640, 350, t, Wd("2.2", "Electric Power"), "sans", 44, INK)
        ftext(c, "Research Institute", 1640, 400, t, Wd("2.2", "Electric Power"), "sans", 44, INK)
    # ---- A2: who is EPRI (2.3)
    a2, b2 = s("2.3") - 0.05, s("2.4") - 0.5
    with ph(c, t, a2, b2, 0.35):
        with clip(c, 880, 450, 1200, 620, t, a2, None, rot=1, seed=43) as ok:
            if ok:
                text(c, "WHO IS EPRI?", 0, -235, "serif", 70)
                items = [("The power industry's research institute", Wd("2.3", "who they are") - 0.2),
                         ("Funded by its members", Wd("2.3", "funded") - 0.2),
                         ("Members: mostly electric utilities", Wd("2.3", "mostly") - 0.2)]
                for i, (tx, ta) in enumerate(items):
                    y = -105 + i*105
                    pa = e_out(prog(t, ta - 0.1, ta + 0.3))
                    c.drawCircle(-520, y, 14, P(RED, alpha=pa))
                    text(c, tx, -480, y, "sans", 48, INK, "l", pa)
        stamp(c, "KNOW THE SOURCE", 1500, 800, t, Wd("2.3", "But you") - 0.1, RED, -4, 60, pad=(30, 18))
    # ---- B: +160% and -6% (2.4)
    a3, b3 = s("2.4") - 0.05, s("2.5") - 0.5
    with ph(c, t, a3, b3, 0.35):
        with board(c, 960, 450, 1640, 700, t, a3, None, rot=-0.4, seed=8) as ok:
            if ok:
                text(c, "AVERAGE US HOUSEHOLD'S STATE, 2019 → 2024", 0, -305, "sans", 42, 0xFFC9C2B2)
                # left: data center capacity
                p1 = e_out(prog(t, Wd("2.4", "a hundred and sixty") - 0.6, Wd("2.4", "a hundred and sixty") + 0.8))
                base = 220
                for x, h0, col, nm in ((-640, 100, 0xFF8A857C, "2019"), (-380, 260, AMBER, "2024")):
                    hh = h0*(1.0 if nm == "2019" else 1 + (h0/100 - 1)*p1 - 0.0)
                    hh = 100 if nm == "2019" else 100 + 160*p1
                    c.drawRect(skia.Rect.MakeXYWH(x - 85, base - hh, 170, hh), P(col)); c.drawRect(skia.Rect.MakeXYWH(x - 85, base - hh, 170, hh), P(CREAM, "stroke", 3))
                    text(c, nm, x, base + 38, "sans", 38, CREAM)
                text(c, "+%d%%" % round(160*p1), -510, -165, "mono", 120, AMBER) if p1 > 0.02 else None
                text(c, "data center capacity", -510, -80, "sansr", 40, CREAM)
                ia = e_out(prog(t, a3 + 0.5, a3 + 1.0)) * (1 - e_out(prog(t, Wd("2.4", "grew") - 0.5, Wd("2.4", "grew") - 0.1)))
                if ia > 0.01:
                    house(c, 0, 90, 1.0, CREAM, ia)
                    text(c, "the average household", 0, -105, "sans", 48, CREAM, alpha=ia)
                    text(c, "2019 → 2024", 0, 160, "mono", 52, AMBER, alpha=ia*e_out(prog(t, Wd("2.4", "From twenty nineteen") , Wd("2.4", "From twenty nineteen") + 0.6)))
                ga = Wd("2.4", "grew") - 0.2
                if t >= ga:
                    arrow(c, bez((-640, 100), (-560, -60), (-400, -20)), e_io(prog(t, ga, ga + 1.4)), AMBER, 9)
                    ftext(c, "×2.6", -640, 30, t, ga + 1.2, "mono", 56, AMBER) if False else None
                pen_ellipse(c, -510, -165, 250, 70, prog(t, Wd("2.4", "a hundred and sixty") + 0.9, Wd("2.4", "a hundred and sixty") + 1.5), AMBER, 8, 5)
                # right: rates
                p2 = e_out(prog(t, Wd("2.4", "They estimate"), Wd("2.4", "six percent") + 0.8))
                rx = 380
                c.drawRect(skia.Rect.MakeXYWH(rx - 85 - 150, base - 106, 170, 106), P(CREAM, alpha=0.12*p2))
                c.drawRect(skia.Rect.MakeXYWH(rx - 85 - 150, base - 106, 170, 106), P(CREAM, "stroke", 4, p2, dash=[14, 10]))
                c.drawRect(skia.Rect.MakeXYWH(rx - 85 + 150, base - 100, 170, 100), P(GREEN, alpha=p2)); c.drawRect(skia.Rect.MakeXYWH(rx - 85 + 150, base - 100, 170, 100), P(CREAM, "stroke", 3, p2))
                text(c, "WITHOUT", rx - 150, base + 38, "sans", 38, CREAM, alpha=p2)
                text(c, "ACTUAL", rx + 150, base + 38, "sans", 38, CREAM, alpha=p2)
                if p2 > 0.02:
                    text(c, "−%d%%" % round(6*p2), rx, -165, "mono", 120, 0xFF58C27D)
                    text(c, "residential rates", rx, -80, "sansr", 40, CREAM, alpha=p2)
                text(c, "→", -100, 30, "mono", 110, CREAM, alpha=p2)
    # ---- C: doubling -> -3.5% (2.5)
    a4, b4 = s("2.5") - 0.05, s("2.6") - 0.5
    with ph(c, t, a4, b4, 0.35):
        with board(c, 960, 380, 1500, 460, t, a4, None, rot=0.5, seed=10) as ok:
            if ok:
                text(c, "DATA CENTER CAPACITY", -300, -130, "sans", 44, 0xFFC9C2B2)
                text(c, "DOUBLES", -300, -60, "sans", 64, CREAM)
                text(c, "2×", -300, 70, "mono", 190, AMBER)
                text(c, "→", 40, 60, "mono", 150, CREAM)
                ra_ = Wd("2.5", "residential rates fell") - 0.2
                v = roll(t, ra_, 1.8, 0, 3.5)
                text(c, "−%.1f%%" % v if t >= ra_ else "−?%", 360, 40, "mono", 170, 0xFF58C27D if t >= ra_ else 0xFF6F6A60)
                text(c, "residential rates", 360, 150, "sansr", 44, CREAM)
                pen_ellipse(c, 360, 30, 300, 80, prog(t, Wd("2.5", "three and a half") + 0.8, Wd("2.5", "three and a half") + 1.4), 0xFF58C27D, 8, 6)
        # range
        ra = Wd("2.5", "estimate") - 0.1
        with ph(c, t, ra, None, 0.3):
            x0, x1 = 360, 1560   # scale 0 .. -13%
            sc_ = (x1 - x0)/13.0
            y = 790
            c.drawLine(x0, y, x1, y, P(INK, "stroke", 5))
            for v_ in (0, -3.5, -12):
                xx = x0 + abs(v_)*sc_
                c.drawLine(xx, y - 14, xx, y + 14, P(INK, "stroke", 4))
            text(c, "0%", x0, y + 50, "sans", 40)
            text(c, "−12%", x0 + 12*sc_, y + 50, "sans", 40)
            rr = skia.Rect.MakeXYWH(x0 + 1.4*sc_, y - 24, (12.1 - 1.4)*sc_, 48)
            pw = e_out(prog(t, ra, ra + 0.8))
            c.drawRect(skia.Rect.MakeXYWH(rr.x(), rr.y(), rr.width()*pw, rr.height()), P(GREEN, alpha=0.25))
            c.drawRect(skia.Rect.MakeXYWH(rr.x(), rr.y(), rr.width()*pw, rr.height()), P(GREEN, "stroke", 4))
            c.drawCircle(x0 + 3.5*sc_, y, 17, P(RED)); c.drawCircle(x0 + 3.5*sc_, y, 17, P(INK, "stroke", 4))
            text(c, "best estimate", x0 + 3.5*sc_, y - 62, "sans", 40, RED)
            text(c, "range: −1.5% to −12%", 960, y - 125, "sans", 44, INK) if False else None
            tag(c, "AN ESTIMATE, NOT A GUARANTEE", 960, 880, t, ra + 0.3, INK, 40, "sans")
    # ---- D: why — fixed costs (2.6)
    a5, b5 = s("2.6") - 0.05, s("2.7") - 0.5
    with ph(c, t, a5, b5, 0.35):
        text(c, "THE POWER LINES COST THE SAME", 960, 160, "sans", 52, INK)
        for gx, n, lab, ta in ((520, 4, "EACH HOUSEHOLD PAYS ¼", a5 + 0.4), (1400, 8, "EACH PAYS ⅛", Wd("2.6", "When more"))):
            pa = e_out(prog(t, ta, ta + 0.5))
            sp = 100
            wtot = n*sp
            x_l = gx - wtot/2
            # fixed-cost bar split in n
            for k in range(n):
                r = skia.Rect.MakeXYWH(x_l + k*sp + 4, 395, sp - 8, 90)
                c.drawRect(r, P(RED, alpha=0.22*pa)); c.drawRect(r, P(RED, "stroke", 4, pa))
                house(c, x_l + k*sp + sp/2, 640, 0.52, INK, pa)
            text(c, "FIXED COST", gx, 340, "sans", 44, RED, alpha=pa)
            text(c, lab, gx, 760, "sans", 44, INK, alpha=pa)
        # shared wire line
        c.drawLine(120, 590, 1800, 590, P(INK, "stroke", 5, 0.0))
        ftext(c, "NEW PLANTS CAN COST LESS THAN OLD ONES", 960, 860, t, Wd("2.6", "new power plants"), "sans", 50, GREEN)
    # ---- E: Columbia quote (2.7)
    a6, b6 = s("2.7") - 0.05, s("2.8") - 0.5
    with ph(c, t, a6, b6, 0.35):
        quote_card(c, 960, 430, 1500, 560, t, a6, None,
                   ["recent increases “cannot be attributed", "to any single factor”"],
                   "Columbia University, Center on Global Energy Policy · June 2026", 66, 44)
        w1 = tw("recent increases “cannot be attributed", "serif", 66)
        pen_line(c, 960 - w1/2, 417, 960 + w1/2, 417, prog(t, Wd("2.7", "recent price"), Wd("2.7", "recent price") + 1.2), AMBER, 9, 1.0, 6)
        w2 = tw("to any single factor”", "serif", 66)
        pen_line(c, 960 - w2/2, 497, 960 + w2/2, 497, prog(t, Wd("2.7", "any single") - 0.6, Wd("2.7", "any single") + 0.5), RED, 9, 1.0, 4)
        tag(c, "AND: BIG NEW LOADS ARE NOT A PRINCIPAL DRIVER", 960, 790, t, Wd("2.7", "big new loads") - 0.2, INK, 40, "sans", fill=AMBER)
    # ---- F: "room" quote (2.8)
    a7, b7 = s("2.8") - 0.05, s("2.9") - 0.5
    with ph(c, t, a7, b7, 0.35):
        quote_card(c, 960, 360, 1500, 380, t, a7, None,
                   ["states with falling prices “already had room", "on their power grid”"],
                   "Ryan Hledik, The Brattle Group · Marketplace, July 2026", 56, 45, 1.0)
        for gx, filled, newb, lab, colr in ((560, 0.55, 0.22, "ROOM", GREEN), (1400, 0.93, 0.22, "FULL", RED)):
            p = e_out(prog(t, a7 + 1.8, a7 + 2.6))
            wbar = 600
            r = skia.Rect.MakeXYWH(gx - wbar/2, 640, wbar, 90)
            c.drawRect(r, P(PAPER2, alpha=p)); c.drawRect(r, P(INK, "stroke", 5, p))
            c.drawRect(skia.Rect.MakeXYWH(gx - wbar/2, 640, wbar*filled*p, 90), P(0xFF8A857C, alpha=0.8*p))
            nb = skia.Rect.MakeXYWH(gx - wbar/2 + wbar*filled, 640, wbar*newb, 90)
            c.drawRect(nb, P(AMBER, alpha=p)); c.drawRect(nb, P(INK, "stroke", 4, p))
            text(c, lab, gx, 800, "mono", 70, colr, alpha=p)
            text(c, "new load" if lab == "ROOM" else "new load: won't fit", gx, 600, "sans", 40, INK, alpha=p)
    # ---- G: California (2.9)
    a8, b8 = s("2.9") - 0.05, s("2.10") - 0.5
    fa8 = Wd("2.9", "From twenty") - 0.1
    with ph(c, t, a8, fa8 - 0.4, 0.3):
        with clip(c, 960, 430, 1500, 420, t, a8, None, rot=-1, seed=58) as ok:
            if ok:
                text(c, "BLAME DATA CENTERS", 0, -80, "serif", 84)
                text(c, "FOR EVERY PRICE RISE?", 0, 40, "serif", 84)
        pen_line(c, 260, 560, 1660, 330, prog(t, Wd("2.9", "every price") + 0.3, Wd("2.9", "every price") + 1.1), RED, 14)
    with ph(c, t, fa8, b8, 0.35):
        with board(c, 960, 450, 1500, 560, t, fa8, None, rot=-0.5, seed=11) as ok:
            if ok:
                text(c, "CALIFORNIA · 2021 → 2024", -330, -190, "sans", 48, 0xFFC9C2B2)
                ra_ = Wd("2.9", "nearly forty") - 0.5
                v = roll(t, ra_, 1.0, 0, 40)
                if t >= ra_: text(c, "+%d%%" % round(v), -330, -30, "mono", 240, VERM)
                else: text(c, "+?%", -330, -30, "mono", 240, DKGRAY)
                text(c, "electricity prices", -330, 110, "sansr", 48, CREAM)
                flame(c, 440, 150, 2.1*(1 + 0.05*math.sin(t*9)), VERM)
        pen_ellipse(c, 630, 420, 360, 100, prog(t, Wd("2.9", "nearly forty") + 0.9, Wd("2.9", "nearly forty") + 1.5), AMBER, 9, 7)
        ftext(c, "largely wildfire costs", 1000, 800, t, Wd("2.9", "wildfire") - 0.1, "sans", 56, RED)
        src(c, "Source: EPRI paper", 960, 880, "c")
    # ---- H: the hook (2.10)
    a9 = s("2.10") - 0.05
    with ph(c, t, a9, None, 0.35):
        base = 800; k = 2.0
        baseline(c, 400, 1520, base)
        bar(c, 640, base, 240, 28.92*k, e_out(prog(t, a9, a9 + 0.5)), GREEN)
        p2 = e_out(prog(t, Wd("2.10", "jump") - 0.2, Wd("2.10", "jump") + 0.9))
        bar(c, 1280, base, 240, 269.92*k, p2, RED)
        text(c, "$28.92", 640, base - 28.92*k - 40, "mono", 60, INK)
        if p2 > 0.02: text(c, money(269.92*p2, 2), 1280, base - 269.92*k*p2 - 40, "mono", 60, RED)
        text(c, "2024/25", 640, base + 46, "sans", 40); text(c, "2025/26", 1280, base + 46, "sans", 40)
        stamp(c, "9×+", 840, 300, t, Wd("2.10", "nine") - 0.1, VERM, -3, 150, pad=(40, 24))

# ================================================================== SEGMENT 3
def seg3(c, t):
    s = S
    # ---- A: room (3.1 - 3.2)
    a0, b0 = s("3.1") - 0.05, s("3.2") - 0.5
    with ph(c, t, a0, b0, 0.35):
        with clip(c, 960, 430, 1100, 480, t, a0, None, rot=-1.2, seed=51) as ok:
            if ok:
                text(c, "THE ANSWER IN ONE WORD", 0, -150, "sansr", 44, DKGRAY)
                text(c, "ROOM", 0, 30, "serif", 230)
        pen_line(c, 560, 640, 1360, 640, prog(t, Wd("3.1", "room") - 0.3, Wd("3.1", "room") + 0.5), RED, 12)
    a1, b1 = s("3.2") - 0.05, s("3.3") - 0.5
    with ph(c, t, a1, b1, 0.35):
        wbar = 1100
        for yy, filled, lab, fits in ((330, 0.5, "SPARE CAPACITY", True), (640, 0.95, "FULL GRID", False)):
            ta = a1 + (0.0 if fits else Wd("3.2", "When it's full") - a1 - 0.2)
            p = e_out(prog(t, ta, ta + 0.5))
            x0 = 960 - wbar/2
            r = skia.Rect.MakeXYWH(x0, yy - 55, wbar, 110)
            c.drawRect(r, P(PAPER2, alpha=p)); c.drawRect(r, P(INK, "stroke", 6, p))
            c.drawRect(skia.Rect.MakeXYWH(x0, yy - 55, wbar*filled*p, 110), P(0xFF8A857C, alpha=0.85*p))
            text(c, lab, x0, yy - 100, "sans", 44, INK, "l", p)
            mv = e_io(prog(t, ta + 0.8, ta + 1.8))
            nx = lerp(1600, x0 + wbar*filled + 100, mv) if fits else lerp(1600, x0 + wbar*filled + 100, mv)
            if p > 0.5:
                c.save(); c.translate(nx + (0 if fits else 0), yy)
                sil_building(c, 0, 55, 0.7, VERM if not fits else GREEN)
                c.restore()
            if fits:
                ftext(c, "SHARES THE FIXED COSTS", 960, yy + 100, t, ta + 1.8, "sans", 44, GREEN)
            else:
                ftext(c, "NEEDS NEW LINES AND NEW PLANTS", 960, yy + 100, t, ta + 1.8, "sans", 44, RED)
    # ---- B1: forecast (3.3)
    a2, b2 = s("3.3") - 0.05, s("3.4") - 0.5
    pa_ = Wd("3.3", "its forecast") - 0.1
    with ph(c, t, a2, pa_ - 0.4, 0.3):
        with clip(c, 960, 430, 1500, 500, t, a2, None, rot=-0.8, seed=57) as ok:
            if ok:
                text(c, "WHERE IS PJM'S GROWTH COMING FROM?", 0, -190, "serif", 60)
        for i in range(6):
            ta = a2 + 0.8 + i*0.9
            building(c, 330 + i*252, 620, 0.62, INK if i < 2 else RED, e_out(prog(t, ta, ta + 0.4)))
        tag(c, "THE 2027/28 AUCTION", 960, 760, t, Wd("3.3", "twenty twenty-seven") - 0.2, INK, 44, "sans", fill=AMBER)
    with ph(c, t, pa_, b2, 0.35):
        with board(c, 960, 420, 1560, 640, t, a2, None, rot=0.4, seed=12) as ok:
            if ok:
                text(c, "PJM FORECAST PEAK DEMAND, 2027/28 AUCTION", 0, -260, "sans", 44, 0xFFC9C2B2)
                p1 = e_out(prog(t, Wd("3.3", "fifty-two") - 0.5, Wd("3.3", "fifty-two") + 0.9))
                text(c, "+%s MW" % format(round(5250*p1), ","), 0, -135, "mono", 150, CREAM if p1 > 0 else DKGRAY) if p1 > 0 else text(c, "+? MW", 0, -135, "mono", 150, DKGRAY)
                wb = 1300
                p2 = e_out(prog(t, Wd("3.3", "fifty-one") - 0.4, Wd("3.3", "fifty-one") + 0.9))
                if p1 > 0.01:
                    c.drawRect(skia.Rect.MakeXYWH(-wb/2, 10, wb*p1, 100), P(0xFF8A857C))
                    c.drawRect(skia.Rect.MakeXYWH(-wb/2, 10, wb*p1*5100/5250*p2, 100), P(VERM))
                    c.drawRect(skia.Rect.MakeXYWH(-wb/2, 10, wb*p1, 100), P(CREAM, "stroke", 4))
                if p2 > 0.02:
                    text(c, "nearly %s MW = DATA CENTERS" % format(round(5100*p2), ","), 0, 175, "sans", 56, VERM)
                text(c, "than the year before", 0, 245, "sansr", 40, 0xFFC9C2B2)
        src(c, "Source: PJM, Dec. 17, 2025", 960, 880, "c")
    # ---- B2: supply (3.4)
    a3, b3 = s("3.4") - 0.05, s("3.5") - 0.5
    with ph(c, t, a3, b3, 0.35):
        baseline(c, 260, 1660, 780)
        bar(c, 600, 780, 300, 560, e_out(prog(t, a3 + 0.2, a3 + 1.0)), VERM)
        bp = e_out(prog(t, Wd("3.4", "seven hundred") - 0.5, Wd("3.4", "seven hundred") + 0.8))
        bar(c, 1320, 780, 300, 560*774/5250, bp, GREEN)
        text(c, "+5,250", 600, 780 - 560 - 50, "mono", 64, VERM)
        text(c, "DEMAND", 600, 830, "sans", 44)
        text(c, "+774", 1320, 780 - 560*774/5250*bp - 50, "mono", 64, GREEN) if bp > 0.02 else None
        text(c, "NEW SUPPLY", 1320, 830, "sans", 44)
        text(c, "MW, new generation + upgrades", 1320, 250, "sansr", 40, DKGRAY, alpha=e_out(prog(t, a3 + 1.5, a3 + 2)))
    # ---- B3: shortfall (3.5)
    a4, b4 = s("3.5") - 0.05, s("3.6") - 0.5
    with ph(c, t, a4, b4, 0.35):
        wbar = 1300; x0 = 960 - wbar/2
        r = skia.Rect.MakeXYWH(x0, 340, wbar, 110)
        pp = e_out(prog(t, a4 + 0.2, a4 + 1.0))
        c.drawRect(skia.Rect.MakeXYWH(x0, 340, wbar*0.955*pp, 110), P(0xFF8A857C)); c.drawRect(r, P(INK, "stroke", 6))
        c.drawLine(x0 + wbar, 300, x0 + wbar, 490, P(RED, "stroke", 8))
        text(c, "WHAT RELIABILITY REQUIRES", x0 + wbar, 270, "sans", 40, RED, "r")
        sa = Wd("3.5", "short") - 0.2
        gap = skia.Rect.MakeXYWH(x0 + wbar*0.955, 340, wbar*0.045, 110)
        if t >= sa:
            al = e_out(prog(t, sa, sa + 0.5))
            c.drawRect(gap, P(VERM, alpha=al)); c.drawRect(gap, P(VERM, "stroke", 5, al, dash=[10, 8]))
            v = roll(t, sa, 1.0, 0, 6623)
            text(c, "−%s MW" % format(round(v), ","), 960, 600, "mono", 140, VERM)
            text(c, "short of the target", 960, 725, "sans", 48, INK)
        text(c, "WHAT PJM LINED UP", x0, 510, "sans", 40, INK, "l")
        tg = Wd("3.5", "doesn't mean")
        if t >= tg - 0.1:
            tag(c, "PJM: NOT A BLACKOUT FORECAST — THINNER RESERVES", 960, 800, t, tg, INK, 38, "sans")
        src(c, "Source: PJM, Dec. 17, 2025", 960, 890, "c")
    # ---- B4: the jump again (3.6)
    a5, b5 = s("3.6") - 0.05, s("3.7") - 0.5
    with ph(c, t, a5, b5, 0.35):
        tm = dict(bids=-100, bid_dt=0.0, sort0=-100, sort1=-99, dem=-100, price=-100, shift0=Wd("3.6", "More demand"), shift1=Wd("3.6", "More demand") + 1.6, d0=51, d1=66)
        auction(c, t, tm)
        illustrative(c, 1840, 890)
        ftext(c, "LAST PLANT SETS THE PRICE FOR EVERYONE", 960, 118, t, a5 + 0.5, "sans", 52, INK)
    # ---- C: the watchdog quote (3.7)
    a6, b6 = s("3.7") - 0.05, s("3.8") - 0.5
    qa = Wd("3.7", "In June") - 0.3
    with ph(c, t, a6, b6, 0.35):
        quote_card(c, 1130, 440, 1260, 560, t, qa, None,
                   ["data center load growth is “the", "primary reason for recent and expected", "capacity market conditions”"],
                   "PJM's independent market monitor · June 25, 2025", 58, 52)
        silhouette(c, 300, 420, 1.0, t, a6 + 0.3, "MARKET MONITOR", 36)
        w2 = tw("primary reason for recent and expected", "serif", 58); w3 = tw("capacity market conditions”", "serif", 58)
        pen_line(c, 1130 - w2/2, 458, 1130 + w2/2, 458, prog(t, Wd("3.7", "primary reason") - 0.3, Wd("3.7", "primary reason") + 0.8), RED, 9, 1.0, 3)
        pen_line(c, 1130 - w3/2, 525, 1130 + w3/2, 525, prog(t, Wd("3.7", "conditions") - 1.0, Wd("3.7", "conditions") + 0.2), RED, 9, 1.0, 5)
    # ---- D1: 9.3B (3.8)
    a7, b7 = s("3.8") - 0.05, s("3.9") - 0.5
    with ph(c, t, a7, b7, 0.35):
        with board(c, 960, 430, 1500, 640, t, a7, None, rot=-0.5, seed=13) as ok:
            if ok:
                text(c, "2025/26 AUCTION · DATA CENTER LOAD ALONE", 0, -260, "sans", 44, 0xFFC9C2B2)
                t1 = Wd("3.8", "nine point three") - 0.3; t2 = Wd("3.8", "a hundred") - 0.3
                v = roll(t, t1, 1.1, 0, 9.3)
                text(c, "+$%.1fB" % v if t >= t1 else "+$?B", -330, -85, "mono", 170, VERM if t >= t1 else DKGRAY)
                v2 = roll(t, t2, 1.0, 0, 174)
                text(c, "+%d%%" % round(v2) if t >= t2 else "+?%", 400, -85, "mono", 170, AMBER if t >= t2 else DKGRAY)
                text(c, "added to the auction's total", 0, 100, "sansr", 52, CREAM)
                text(c, "the monitor's estimate", 0, 175, "sansr", 44, 0xFFC9C2B2)
        pen_ellipse(c, 630, 345, 360, 115, prog(t, Wd("3.8", "nine point three") + 1.3, Wd("3.8", "nine point three") + 1.9), AMBER, 9, 3)
        pen_ellipse(c, 1360, 345, 300, 115, prog(t, Wd("3.8", "a hundred") + 1.2, Wd("3.8", "a hundred") + 1.8), VERM, 9, 4)
        stamp(c, "THE MONITOR'S ESTIMATE", 960, 825, t, a7 + 0.4, INK, -2, 44, pad=(28, 14))
        src(c, "Source: IMM, June 25, 2025", 960, 905, "c")
    # ---- D2: 29.4B / 46% (3.9)
    a8, b8 = s("3.9") - 0.05, s("3.10") - 0.5
    with ph(c, t, a8, b8, 0.35):
        with board(c, 960, 430, 1500, 640, t, a8, None, rot=0.5, seed=14) as ok:
            if ok:
                text(c, "LAST FOUR AUCTIONS · TIED TO DATA CENTER LOAD", 0, -260, "sans", 42, 0xFFC9C2B2)
                t1 = Wd("3.9", "twenty-nine") - 0.4
                v = roll(t, t1, 1.2, 0, 29.4)
                text(c, "$%.1fB" % v if t >= t1 else "$?B", -380, -60, "mono", 190, VERM if t >= t1 else DKGRAY)
                p = e_out(prog(t, Wd("3.9", "Forty-six") - 0.6, Wd("3.9", "Forty-six") + 1.0))
                c.save(); c.translate(430, -10)
                c.drawCircle(0, 0, 150, P(CREAM, alpha=0.15)); c.drawCircle(0, 0, 150, P(CREAM, "stroke", 5))
                path = skia.Path(); path.moveTo(0, 0)
                path.arcTo(skia.Rect.MakeXYWH(-150, -150, 300, 300), -90, 360*0.462*p, False); path.close()
                c.drawPath(path, P(VERM))
                c.restore()
                text(c, "%d%%" % round(46*p), 430, -10, "mono", 100, CREAM) if p > 0.3 else None
                text(c, "of all capacity charges", 430, 195, "sansr", 44, CREAM)
        pen_ellipse(c, 580, 370, 420, 140, prog(t, Wd("3.9", "twenty-nine") + 1.4, Wd("3.9", "twenty-nine") + 2.0), AMBER, 9, 5)
        src(c, "Source: IMM, July 27, 2026", 960, 880, "c")
    # ---- D3: summary (3.10)
    a9, b9 = s("3.10") - 0.05, s("3.11") - 0.5
    with ph(c, t, a9, b9, 0.35):
        xs = (400, 960, 1520)
        vals = ("$9B", "$29B", "46%"); subs = ("2025/26", "last 4 auctions", "of capacity charges")
        for i in range(3):
            ta = Wd("3.10", ("Nine", "Twenty-nine", "Forty-six")[i]) - 0.1
            with clip(c, xs[i], 380, 460, 360, t, ta, None, rot=(-2, 1, -1)[i], seed=60 + i) as ok:
                if ok:
                    text(c, vals[i], 0, -30, "mono", 130, RED)
                    text(c, subs[i], 0, 80, "sans", 40, INK)
        stamp(c, "ESTIMATES", 960, 700, t, Wd("3.10", "estimates") - 0.1, INK, -2, 70)
        ftext(c, "charges in the auction  ≠  your bill", 960, 810, t, Wd("3.10", "not what") - 0.2, "sans", 52, DKGRAY)
    # ---- E1: skyline (3.11)
    a10, b10 = s("3.11") - 0.05, s("3.12") - 0.5
    with ph(c, t, a10, b10, 0.35):
        for i in range(6):
            x = 250 + i*285
            built = i < 2
            ta = a10 + 0.3 + i*0.25
            al = e_out(prog(t, ta, ta + 0.4))
            if built:
                building(c, x, 640, 0.85, INK, al)
            else:
                building(c, x, 640, 0.85, GRAY, al*0.9)
                c.drawRect(skia.Rect.MakeXYWH(x - 130, 640 - 112, 260, 112), P(PAPER, alpha=0.0))
        ftext(c, "BUILT", 535, 740, t, a10 + 0.8, "sans", 52, INK) if False else None
        ftext(c, "BUILT", 395, 760, t, a10 + 0.9, "mono", 56, INK)
        ftext(c, "NOT BUILT YET", 1250, 760, t, Wd("3.11", "isn't here yet") - 0.1, "mono", 56, RED)
        pen_line(c, 760, 790, 1730, 790, prog(t, Wd("3.11", "isn't here yet"), Wd("3.11", "isn't here yet") + 0.6), RED, 8)
    # ---- E2: 6.2 of 6.5 (3.12)
    a11, b11 = s("3.12") - 0.05, s("3.13") - 0.5
    with ph(c, t, a11, b11, 0.35):
        wbar = 1300; x0 = 960 - wbar/2
        text(c, "DECEMBER 2025 AUCTION · TIED TO DATA CENTERS", 960, 190, "sans", 44, INK)
        ftext(c, "NOT TODAY'S POWER USE", 960, 118, t, a11 + 0.2, "sans", 52, INK, b=Wd("3.12", "forecast") - 0.5)
        ftext(c, "THE AUCTION RUNS ON A FORECAST", 960, 118, t, Wd("3.12", "forecast"), "sans", 52, RED)
        p = e_out(prog(t, a11 + 0.3, a11 + 1.2))
        r = skia.Rect.MakeXYWH(x0, 300, wbar*p, 130)
        c.drawRect(r, P(RED, alpha=0.9)); c.drawRect(skia.Rect.MakeXYWH(x0, 300, wbar, 130), P(INK, "stroke", 6))
        text(c, "$6.5B", 960, 505, "mono", 110, RED) if p > 0.9 else None
        hp = e_out(prog(t, Wd("3.12", "six point two") - 0.4, Wd("3.12", "six point two") + 1.0))
        if hp > 0.01:
            hr = skia.Rect.MakeXYWH(x0, 300, wbar*6.2/6.5*hp, 130)
            c.save(); c.clipRect(hr)
            hatch_rect(c, hr.x(), hr.y(), hr.width(), hr.height(), PAPER2, 30, 9, 0.85)
            c.restore()
            c.drawRect(hr, P(INK, "stroke", 5))
            text(c, "$6.2B of it: NOT BUILT YET", 960, 640, "mono", 70, INK)
        pen_line(c, 560, 690, 1360, 690, prog(t, Wd("3.12", "not yet built") - 0.2, Wd("3.12", "not yet built") + 0.8), RED, 10, 1.0, 3)
        stamp(c, "IMM REPORT · JAN. 2026", 960, 790, t, Wd("3.12", "In January") - 0.1, INK, -2, 44, pad=(28, 14))
        src(c, "Source: IMM, Jan. 5, 2026 (via Utility Dive)", 960, 880, "c")
    # ---- E3: unique and unprecedented (3.13)
    a12, b12 = s("3.13") - 0.05, s("3.14") - 0.5
    with ph(c, t, a12, b12, 0.35):
        quote_card(c, 960, 440, 1300, 420, t, a12, None,
                   ["forecast uncertainty:", "“unique and unprecedented”"],
                   "PJM's market monitor · Jan. 2026 (via Utility Dive)", 76, 56, -1.2)
    # ---- E4: double counting (3.14)
    a13, b13 = s("3.14") - 0.05, s("3.15") - 0.5
    with ph(c, t, a13, b13, 0.35):
        building(c, 420, 620, 1.0, GRAY)
        text(c, "ONE PROJECT", 420, 700, "sans", 48, INK)
        for i, (nm, yy) in enumerate((("UTILITY A", 300), ("UTILITY B", 450), ("UTILITY C", 600))):
            ta = Wd("3.14", "developers") + 0.3 + i*1.3
            path = bez((580, 560), (800, 560 - (i-1)*60), (1180, yy))
            arrow(c, path, e_out(prog(t, ta, ta + 0.5)), RED, 8)
            tag(c, nm + " FORECAST", 1450, yy, t, ta + 0.3, INK, 40, "sans")
        stamp(c, "COUNTED 3×", 1150, 780, t, Wd("3.14", "inflate") - 0.1, RED, -3, 66)
        illustrative(c, 1840, 890)
    # ---- E5: buildings that don't exist (3.15)
    a14 = s("3.15") - 0.05
    with ph(c, t, a14, None, 0.35):
        building(c, 700, 600, 1.15, GRAY)
        c.drawRect(skia.Rect.MakeXYWH(500, 600 - 150, 400, 150), P(PAPER, alpha=0.0))
        tag(c, "PART OF TODAY'S PRICE", 1280, 380, t, a14 + 0.3, RED, 52, "sans")
        path = bez((1100, 420), (1000, 480), (880, 480 + 20))
        arrow(c, path, e_out(prog(t, a14 + 0.6, a14 + 1.3)), RED, 9)
        ftext(c, "a building that doesn't exist yet", 960, 760, t, a14 + 1.0, "sans", 56, INK)

REG = {2: (cam, seg2, None), 3: (cam, seg3, None)}
