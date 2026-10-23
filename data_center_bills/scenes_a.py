# -*- coding: utf-8 -*-
"""Segments 0 (the opening) and 1 (your bill / how the auction works)."""
from common import *

def cam(t): return (960, 455, 1.0)

def ftext(c, s, x, y, t, a, kind="sans", size=40, color=INK, align="c", b=None, dur=0.3, rise=10, **k):
    if t < a or (b is not None and t > b + dur): return
    al = e_out(prog(t, a, a + dur))
    if b is not None and t > b: al *= 1 - prog(t, b, b + dur)
    text(c, s, x, y + rise*(1 - e_out(prog(t, a, a + dur))), kind, size, color, align, al, **k)

# ================================================================== SEGMENT 0 — the opening
R0, R1 = 3.3, 4.5            # $29 -> $329 roll (finishes inside the first 5 seconds)
TEN_X = 4.7

def seg0(c, t):
    s04 = S("0.4"); s05 = S("0.5"); s06 = S("0.6"); s07 = S("0.7")
    out_a = s04 - 0.55
    # ---- price board: complete on the very first frame (a < 0 so nothing fades in)
    with ph(c, t, None, out_a, 0.3):
        bx = 960 - 320*e_io(prog(t, 4.0, 4.8))
        with board(c, bx, 450, 1060, 600, t, -1.0, None, rot=-0.6, seed=9) as ok:
            if ok:
                text(c, "PJM CAPACITY PRICE", 0, -228, "sans", 48, CREAM, spacing=3)
                text(c, "dollars per megawatt, per day", 0, -172, "sansr", 40, 0xFFC9C2B2)
                v = roll(t, R0, R1 - R0, 28.92, 329.17)
                done = t >= R1
                col = CREAM if t < R0 else mix(CREAM, VERM, e_out(prog(t, R0, R1)))
                sc = 1.0 + (0.05*math.sin(math.pi*prog(t, R1, R1 + 0.5)) if t >= R1 else 0)
                c.save(); c.scale(sc, sc)
                text(c, money(round(v)), 0, 20, "mono", 300, col)
                c.restore()
                yr = "2024/25" if t < R1 - 0.2 else "2026/27"
                text(c, yr + " delivery year", 0, 222, "monom", 44, AMBER)
        # 10x, 1.5s+ hold is guaranteed (stays until out_a)
        if t >= TEN_X - 0.2:
            stamp(c, "MORE THAN", 1480, 215, t, TEN_X, INK, 2, 44, pad=(24, 14), alpha_max=1.0)
            q = prog(t, TEN_X, TEN_X + 0.25)
            if q > 0:
                sc = lerp(1.9, 1.0, e_out(q)); al = e_out(prog(t, TEN_X, TEN_X + 0.12))
                c.save(); c.translate(1480, 390); c.rotate(math.radians(-3)); c.scale(sc, sc)
                c.saveLayerAlpha(skia.Rect.MakeXYWH(-400, -200, 800, 400), int(255*al))
                text(c, "10×", 0, 0, "mono", 270, VERM)
                c.restore(); c.restore()
        a_ring = Wd("0.2", "This year") - 0.1
        if t >= a_ring:
            pen_ellipse(c, 640, 480, 450, 135, prog(t, a_ring, a_ring + 0.7), AMBER, 9, 3)
            tag(c, "THIS YEAR", 640, 800, t, a_ring + 0.4, INK, 40, "sans", fill=AMBER)
        a_u = Wd("0.3", "More than") + 0.2
        if t >= a_u:
            pen_line(c, 1250, 548, 1720, 544, prog(t, a_u, a_u + 0.5), INK, 11)
        # data-center stamp
        a_dc = Wd("0.3", "data centers") - 0.15
        if t >= a_dc - 0.05:
            q = prog(t, a_dc, a_dc + 0.22)
            if q > 0:
                sc = lerp(1.7, 1.0, e_out(q)); al = e_out(prog(t, a_dc, a_dc + 0.1))
                c.save(); c.translate(1480, 745); c.rotate(math.radians(4)); c.scale(sc, sc)
                c.saveLayerAlpha(skia.Rect.MakeXYWH(-330, -230, 660, 460), int(255*al))
                c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-250, -150, 500, 300), 14, 14), P(INK, "stroke", 8))
                sil_building(c, 0, 60, 1.0, INK)
                text(c, "DATA CENTERS", 0, 105, "mono", 46, INK)
                c.restore(); c.restore()
    # ---- 67 million people / map
    ma = s04 - 0.1; mb = s05 - 0.55
    with ph(c, t, ma, mb, 0.3):
        tile_map(c, 560, 485, t, Wd("0.4", "sixty-seven") + 0.2, step=0.1, size=140, gap=14)
        with board(c, 1380, 450, 700, 520, t, Wd("0.4", "sixty-seven"), None, rot=0.8, seed=4) as ok:
            if ok:
                v = roll(t, Wd("0.4", "sixty-seven"), 1.2, 0, 67)
                text(c, "%d" % round(v), 0, -40, "mono", 280, VERM)
                text(c, "MILLION PEOPLE", 0, 105, "sans", 64, CREAM)
                text(c, "13 states + DC", 0, 180, "sansr", 44, 0xFFC9C2B2)
        src(c, "Source: PJM", 960, 890, "c")
    # ---- cheaper
    ca = s05 - 0.15; cb = s06 - 0.55
    with ph(c, t, ca, cb, 0.3):
        with clip(c, 960, 450, 1300, 620, t, ca, None, rot=-0.8, seed=12) as ok:
            if ok:
                text(c, "DATA CENTERS WERE MAKING", 0, -235, "serif", 56)
                text(c, "BILLS CHEAPER", 0, -165, "serif", 72, GREEN)
                # falling line
                path = bez((-460, -40), (-120, -50), (80, 60), (460, 200))
                prg = e_io(prog(t, s05 + 1.0, Wd("0.5", "cheaper") + 0.8))
                arrow(c, path, prg, GREEN, 18, True, head_size=70)
                text(c, "electric rates", -330, 150, "sansr", 44, DKGRAY, alpha=e_out(prog(t, s05 + 0.8, s05 + 1.4)))
                ftext(c, "until recently", -60, -105, t, Wd("0.5", "until recently"), "sansr", 44, DKGRAY)
    # ---- both are true / what flipped
    ba = s06 - 0.1
    with ph(c, t, ba, None, 0.2):
        x_off = -50*e_io(prog(t, s07, s07 + 0.5))
        with clip(c, 500 + x_off, 450, 640, 600, t, ba, None, rot=-2, seed=21) as ok:
            if ok:
                text(c, "CAPACITY PRICE", 0, -215, "sans", 50)
                text(c, "↑ 10×", 0, -60, "mono", 150, VERM)
                text(c, "$29 → $329", 0, 70, "mono", 66)
                text(c, "per megawatt, per day", 0, 140, "sansr", 40, DKGRAY)
        with clip(c, 1420 - x_off, 450, 640, 600, t, ba + 0.35, None, rot=2, seed=22) as ok:
            if ok:
                text(c, "ELECTRIC RATES", 0, -215, "sans", 50)
                text(c, "↓ ~6%", 0, -60, "mono", 150, GREEN)
                text(c, "2019–2024 national", 0, 70, "sanss", 46)
                text(c, "average, EPRI estimate", 0, 135, "sansr", 40, DKGRAY)
        if t >= s07:
            q = prog(t, s07, s07 + 0.3)
            al = e_out(q)
            c.save(); c.translate(960, 440); c.scale(lerp(1.8, 1.0, e_out(q)), lerp(1.8, 1.0, e_out(q))); c.rotate(math.radians(-6*(1-e_out(q))))
            c.saveLayerAlpha(skia.Rect.MakeXYWH(-250, -330, 500, 660), int(255*al))
            text(c, "?", 0, 0, "mono", 520, VERM)
            c.restore(); c.restore()

# ================================================================== SEGMENT 1 — the bill and the auction
# supply stack: (width in MW-units, relative price height), sorted cheapest -> dearest
STEPS = [(14, .10), (12, .16), (10, .22), (10, .30), (9, .40), (8, .55), (7, .74), (6, 1.0)]
PERM = [5, 1, 7, 3, 0, 6, 2, 4]          # how the bids first arrive (unsorted)
CX0, UNIT, CBASE, CH = 300, 15.0, 800, 520
def _cum(order):
    xs = {}; x = 0
    for i in order:
        xs[i] = x; x += STEPS[i][0]
    return xs
SORTED_X = _cum(range(len(STEPS))); UNS_X = _cum(PERM)

def price_at(units):
    cum = 0
    for i, (w, h) in enumerate(STEPS):
        cum += w
        if units <= cum: return i, h
    return len(STEPS) - 1, STEPS[-1][1]

def auction(c, t, tm):
    """tm: bids (start of bids), sort0, sort1, dem (demand line appears), shift0, shift1, d0, d1 (demand units)."""
    n = len(STEPS)
    # axes
    ax = P(INK, "stroke", 6)
    c.drawLine(CX0 - 12, CBASE, CX0 + 76*UNIT + 12, CBASE, ax)
    c.drawLine(CX0 - 12, CBASE, CX0 - 12, CBASE - CH - 40, ax)
    text(c, "PRICE ↑", CX0 - 12, CBASE - CH - 78, "sans", 40, INK, "l")
    text(c, "MEGAWATTS OFFERED →", CX0 + 38*UNIT, CBASE + 56, "sans", 40, INK)
    sp = e_io(prog(t, tm["sort0"], tm["sort1"]))
    # demand
    dsh = e_io(prog(t, tm["shift0"], tm["shift1"]))
    d_units = lerp(tm["d0"], tm["d1"], dsh)
    win_i, win_h = price_at(d_units)
    show_dem = t >= tm["dem"]
    for i in range(n):
        w, h = STEPS[i]
        a_i = tm["bids"] + i*tm.get("bid_dt", 0.55)
        if t < a_i: continue
        grow = e_back(prog(t, a_i, a_i + 0.35))
        x = lerp(UNS_X[i], SORTED_X[i], sp)*UNIT + CX0
        bw = w*UNIT
        won = show_dem and sp >= 0.99 and (SORTED_X[i] + w <= d_units + 1e-6 or i == win_i)
        # a plant is "in" if the demand line lies beyond its start
        won = show_dem and sp >= 0.99 and (SORTED_X[i] < d_units)
        col = GREEN if won else LGRAY
        hh = h*CH*grow
        r = skia.Rect.MakeXYWH(x + 3, CBASE - hh, bw - 6, hh)
        c.drawRect(r, P(col, alpha=0.9)); c.drawRect(r, P(INK, "stroke", 4))
    if t >= tm["bids"] and t < tm["sort0"]:
        pass
    # demand line
    if show_dem:
        dx = CX0 + d_units*UNIT
        al = e_out(prog(t, tm["dem"], tm["dem"] + 0.3))
        c.drawLine(dx, CBASE + 4, dx, CBASE - CH - 20, P(INK, "stroke", 9, al, dash=[22, 14]))
        tag(c, "WHAT PJM NEEDS", dx, CBASE - CH - 50, t, tm["dem"], INK, 36, "sans", fill=AMBER)
        if t >= tm["price"]:
            yy = CBASE - win_h*CH
            pa = e_out(prog(t, tm["price"], tm["price"] + 0.4))
            c.drawLine(CX0 - 12, yy, CX0 + 76*UNIT + 12, yy, P(RED, "stroke", 9, pa))
            tag(c, "CLEARING PRICE", CX0 + 76*UNIT + 190, yy, t, tm["price"], RED, 36, "sans")
            ftext(c, "EVERYONE WHO WINS GETS THIS", CX0 + 330, yy - 40, t, tm["price"] + 0.2, "sans", 40, RED)
    return win_h

def seg1(c, t):
    s = lambda k: S(k)
    # ---- A: the bill splits (1.1 – 1.2)
    A_a, A_b = s("1.1") - 0.1, Wd("1.3", "A grid") - 0.5
    with ph(c, t, A_a, A_b, 0.35):
        pull = e_io(prog(t, Wd("1.2", "one slice"), Wd("1.2", "one slice") + 0.9))
        with clip(c, 600, 470, 760, 700, 1.0 and t, A_a, None, rot=-1.5, seed=31) as ok:
            if ok:
                text(c, "ELECTRIC BILL", 0, -290, "serif", 58)
                c.drawLine(-320, -245, 320, -245, P(INK, "stroke", 4))
                rows = [("ENERGY", "the power itself", Wd("1.2", "Some of it"), AMBER),
                        ("DELIVERY", "wires and poles", Wd("1.2", "Some pays"), AMBER),
                        ("CAPACITY", "being ready", Wd("1.2", "capacity"), RED)]
                for i, (nm, sub, ta, colr) in enumerate(rows):
                    y = -150 + i*130
                    hl = e_out(prog(t, ta, ta + 0.35))
                    if i == 2 and pull > 0:
                        c.drawRect(skia.Rect.MakeXYWH(-330, y - 52, 660, 104), P(INK, "stroke", 3.5, 0.5, dash=[14, 10]))
                    else:
                        c.drawRect(skia.Rect.MakeXYWH(-330, y - 52, 660, 104), P(colr, alpha=0.28*hl))
                        text(c, nm, -310, y - 14, "sans", 46, INK, "l")
                        text(c, sub, -310, y + 30, "sansr", 36, DKGRAY, "l")
                        c.drawLine(110, y + 34, 300, y + 34, P(INK, "stroke", 3, 0.4))
                c.drawLine(-320, 255, 320, 255, P(INK, "stroke", 4))
                tot_a = max(0.0, 1 - pull)
                text(c, "TOTAL", -310, 305, "sans", 50, INK, "l")
                text(c, "one number", 310, 305, "sansr", 44, DKGRAY, "r")
        if pull > 0:
            cx = lerp(600, 1330, pull); cy = lerp(470 - 20 + 0 , 470, pull)
            sc = lerp(1.0, 1.45, pull)
            c.save(); c.translate(cx, lerp(470 + 110, 450, pull)); c.scale(sc, sc)
            r = skia.Rect.MakeXYWH(-330, -104, 660, 208)
            c.drawRect(r, P(PAPER2)); c.drawRect(r, P(RED, "stroke", 7))
            text(c, "CAPACITY", 0, -35, "mono", 76, RED)
            text(c, "the price of being ready", 0, 52, "sans", 40, INK)
            c.restore()
    # ---- B: hottest afternoon, bought in advance (1.3 – 1.4)
    B_a, B_b = Wd("1.3", "A grid") - 0.1, s("1.5") - 0.5
    with ph(c, t, B_a, B_b, 0.35):
        base = 800
        ftext(c, "A GRID MUST HAVE ENOUGH POWER FOR…", 960, 160, t, B_a + 0.1, "sans", 54, INK)
        p1 = e_out(prog(t, Wd("1.3", "average") - 0.4, Wd("1.3", "average") + 0.6))
        p2 = e_out(prog(t, Wd("1.3", "hottest") - 0.4, Wd("1.3", "hottest") + 0.6))
        p3 = e_out(prog(t, Wd("1.3", "cushion") - 0.3, Wd("1.3", "cushion") + 0.5))
        baseline(c, 330, 1290, base) if p1 > 0 else None
        bar(c, 600, base, 260, 330, p1, GRAY)
        bar(c, 1060, base, 260, 480, p2, AMBER)
        bar(c, 1060, base - 480*p2, 260, 90, p3, GREEN, hatch=True)
        ftext(c, "AVERAGE DAY", 600, base + 50, t, Wd("1.3", "average") - 0.4, "sans", 40)
        ftext(c, "HOTTEST AFTERNOON", 1060, base + 50, t, Wd("1.3", "hottest") - 0.4, "sans", 40)
        ftext(c, "+ CUSHION", 1210, base - 480 - 45, t, Wd("1.3", "cushion"), "sans", 44, GREEN, "l")
        if p2 > 0:
            sx, sy = 1650, 300
            c.drawCircle(sx, sy, 48, P(AMBER, alpha=p2)); c.drawCircle(sx, sy, 48, P(INK, "stroke", 5, p2))
            for k in range(10):
                a_ = k*math.pi/5
                c.drawLine(sx + 66*math.cos(a_), sy + 66*math.sin(a_), sx + 92*math.cos(a_), sy + 92*math.sin(a_), P(INK, "stroke", 6, p2))
        stamp(c, "AUCTION", 1560, 640, t, Wd("1.4", "auction") - 0.2, INK, -3, 68)
        ftext(c, "IN ADVANCE", 1560, 750, t, Wd("1.4", "advance"), "sans", 52, RED)
    # ---- C: PJM (1.5)
    C_a, C_b = s("1.5") - 0.05, s("1.6") - 0.5
    with ph(c, t, C_a, C_b, 0.35):
        tile_map(c, 560, 485, t, C_a + 0.1, step=0.05, size=140, gap=14)
        stamp(c, "PJM", 1370, 380, t, Wd("1.5", "PJM") - 0.1, INK, -2, 160, pad=(50, 30))
        ftext(c, "13 states + DC", 1370, 530, t, C_a + 1.0, "sans", 54, INK)
        ftext(c, "67 million people", 1370, 600, t, C_a + 1.3, "sansr", 50, DKGRAY)
    # ---- D: the auction (1.6 – 1.11)
    D_a, D_b = s("1.6") - 0.05, s("1.11") - 0.5
    with ph(c, t, D_a, D_b, 0.35):
        tm = dict(bids=Wd("1.7", "bid"), bid_dt=0.28, sort0=Wd("1.8", "lines"), sort1=Wd("1.8", "lines") + 1.4,
                  dem=Wd("1.6", "calculates"), price=Wd("1.9", "paid"), shift0=Wd("1.10", "demand"), shift1=Wd("1.10", "demand") + 1.6,
                  d0=51, d1=66)
        auction(c, t, tm)
        illustrative(c, 1840, 890)
        a8 = Wd("1.8", "buys"); b8 = Wd("1.9", "paid") - 0.2
        if a8 <= t <= b8 + 0.4:
            al = 1 - prog(t, b8, b8 + 0.3)
            path = bez((CX0 + 20, 470), (CX0 + 300, 440), (CX0 + 51*UNIT, 470))
            arrow(c, path, e_io(prog(t, a8, a8 + 2.6)), GREEN, 12, True, alpha=al)
            text(c, "BUYS FROM THE BOTTOM UP", CX0 + 330, 415, "sans", 44, GREEN, alpha=al)
        ftext(c, "HOW THE AUCTION WORKS", 960, 118, t, D_a + 0.1, "sans", 56, INK, b=Wd("1.6", "PJM first") - 0.2)
        ftext(c, "ONE PRICE FOR EVERYONE", 960, 118, t, Wd("1.9", "One price"), "sans", 56, INK, b=s("1.10") - 0.1)
        ftext(c, "DEMAND UP  →  PRICE JUMPS", 960, 118, t, Wd("1.10", "demand") + 0.8, "sans", 56, RED)
    # ---- D2: utilities pay it, it lands in the bill (1.11)
    with ph(c, t, s("1.11") - 0.05, s("1.12") - 0.5, 0.35):
        pylon(c, 330, 700, 1.1, INK)
        text(c, "UTILITIES", 330, 770, "sans", 48, INK)
        pa = e_io(prog(t, Wd("1.11", "pay"), Wd("1.11", "pay") + 1.2))
        arrow(c, bez((540, 560), (760, 480), (1000, 560)), pa, GREEN, 14)
        tag(c, "PAY THE CLEARING PRICE", 770, 420, t, Wd("1.11", "pay"), INK, 40, "sans", fill=AMBER)
        with clip(c, 1400, 470, 560, 560, t, Wd("1.11", "ends up"), None, rot=2, seed=33) as ok:
            if ok:
                text(c, "YOUR BILL", 0, -215, "serif", 56)
                for i, nm in enumerate(("ENERGY", "DELIVERY", "CAPACITY")):
                    y = -100 + i*105
                    if i == 2:
                        c.drawRect(skia.Rect.MakeXYWH(-235, y - 40, 470, 80), P(RED, alpha=0.25)); c.drawRect(skia.Rect.MakeXYWH(-235, y - 40, 470, 80), P(RED, "stroke", 6))
                    text(c, nm, -215, y, "sans", 44, INK if i < 2 else RED, "l")
    # ---- E: the price history (1.12 – 1.15)
    E_a, E_b = s("1.12") - 0.05, s("1.16") - 0.5
    with ph(c, t, E_a, E_b, 0.35):
        base = 790; k = 590/560
        years = ["2024/25", "2025/26", "2026/27", "2027/28", "2028/29"]
        vals = [28.92, 269.92, 329.17, 333.44, 325.00]
        cols = [GREEN, RED, RED, RED, RED]
        xs = [320, 620, 920, 1220, 1520]
        times = [Wd("1.12", "twenty-nine"), Wd("1.12", "two hundred and seventy"), Wd("1.12", "three hundred and twenty-nine"),
                 Wd("1.12", "three hundred and thirty-three"), Wd("1.13", "three hundred and twenty-five")]
        if t >= times[0] - 0.4: baseline(c, 200, 1650, base)
        text(c, "CAPACITY PRICE · $ per megawatt-day", 210, 130, "sans", 44, INK, "l")
        for i in range(5):
            p = e_out(prog(t, times[i] - 0.15, times[i] + 0.7))
            bar(c, xs[i], base, 200, vals[i]*k, p, cols[i])
            if p > 0.02:
                text(c, money(vals[i]*p, 2), xs[i], base - max(vals[i], 333.44 if i >= 2 else 0)*k*p - (56 if i >= 2 else 40), "mono", 52, INK if i == 0 else RED)
            ftext(c, years[i], xs[i], base + 46, t, times[i] - 0.3, "sans", 40)
        # cap line + ghost
        ca = Wd("1.14", "price cap") - 0.2
        if t >= ca:
            pa = e_out(prog(t, ca, ca + 0.5))
            y = base - 333.44*k
            c.drawLine(220, y, 1650, y, P(INK, "stroke", 6, pa, dash=[22, 14]))
            ftext(c, "PRICE CAP", 330, y - 30, t, ca, "sans", 50, INK)
            c.drawLine(640, y - 25, 760, y - 25, P(INK, "stroke", 5, pa)) if False else None
            g = e_out(prog(t, Wd("1.14", "without"), Wd("1.14", "without") + 1.0))
            ymax = 554.72*k*g
            r = skia.Rect.MakeXYWH(xs[4] - 100, base - ymax, 200, ymax - 325*k)
            if g > 0.02:
                c.drawRect(skia.Rect.MakeXYWH(xs[4] - 100, base - ymax, 200, max(0, ymax - 325*k)), P(RED, alpha=0.12))
                c.drawRect(skia.Rect.MakeXYWH(xs[4] - 100, base - ymax, 200, max(0, ymax - 325*k)), P(RED, "stroke", 5, 1.0, dash=[16, 10]))
                text(c, "$554 without the cap", xs[4], base - ymax - 38, "monom", 40, RED) if False else None
            ftext(c, "$554 uncapped", 1520, 160, t, Wd("1.14", "without") + 0.8, "mono", 44, RED, "c")
        stamp(c, "11× IN TWO YEARS", 640, 250, t, Wd("1.15", "eleven"), VERM, -3, 56, pad=(30, 18))
        if t >= Wd("1.14", "without"): src(c, "Source: PJM auction results · dashed bar: PJM's simulation without the cap", 960, 895, "c")
        else: src(c, "Source: PJM auction results", 960, 895, "c")
    # ---- F: capacity in proportion (1.16)
    F_a = s("1.16") - 0.05
    with ph(c, t, F_a, None, 0.35):
        x0, bw = 280, 1320
        shares = {"2025": [64.6, 24.7, 8.4, 2.3], "2026": [63.5, 17.4, 17.1, 2.0]}
        cols_ = [0xFF8A857C, 0xFFB9B3A6, RED, 0xFFE3DDCF]
        names = ["Energy", "Transmission", "Capacity", "Other"]
        # legend
        lx = 280
        for nm, col in zip(names, cols_):
            c.drawRect(skia.Rect.MakeXYWH(lx, 168, 40, 40), P(col)); c.drawRect(skia.Rect.MakeXYWH(lx, 168, 40, 40), P(INK, "stroke", 3))
            lx += 62 + tw(nm, "sans", 40) + 40
            text(c, nm, lx - tw(nm, "sans", 40) - 40, 188, "sans", 40, INK, "l")
        ftext(c, "CAPACITY: ONE SLICE OF WHOLESALE COST", 960, 118, t, F_a + 0.1, "sans", 52, INK)
        for row, (yr, yy, lab_t) in enumerate((("2025", 400, Wd("1.16", "eight percent") - 0.5), ("2026", 660, Wd("1.16", "seventeen") - 0.5))):
            p = e_out(prog(t, lab_t, lab_t + 0.9))
            text(c, "JAN–JUN " + yr, x0, yy - 100, "sans", 44, INK, "l", alpha=p)
            x = x0
            for sh, col, nm in zip(shares[yr], cols_, names):
                w = bw*sh/100*p
                if w < 1:
                    continue
                r = skia.Rect.MakeXYWH(x, yy - 55, w, 110)
                c.drawRect(r, P(col)); c.drawRect(r, P(INK, "stroke", 4))
                if nm == "Capacity" and p > 0.95:
                    text(c, "%d%%" % round(sh), x + w/2, yy - 105, "mono", 70, RED)
                x += w
        src(c, "Source: PJM Independent Market Monitor, wholesale cost of power", 960, 880, "c")

REG = {0: (cam, seg0, None), 1: (cam, seg1, None)}
