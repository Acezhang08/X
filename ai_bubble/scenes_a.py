# -*- coding: utf-8 -*-
import math, random
import skia
from lib import *
from timeline import Timeline
T = Timeline()
S = T.s; E = T.e; Wd = T.w
GRAYDK = 0xFF6F6A60

# ------------------------------------------------------------------ shared pieces
def loop_paths_():
    return (bez((650, 420), (960, 215), (1270, 420)), bez((1270, 525), (960, 770), (650, 525)))

def closed_loop():
    p = skia.Path()
    p.moveTo(650, 420); p.quadTo(960, 215, 1270, 420); p.lineTo(1270, 525)
    p.quadTo(960, 735, 650, 525); p.close()
    return p

def loop_pos(f):
    pm = skia.PathMeasure(CLOSED, True); L = pm.getLength()
    pos, tan = pm.getPosTan((f % 1.0) * L)
    return pos.fX, pos.fY, math.degrees(math.atan2(tan.fY, tan.fX))
CLOSED = closed_loop()
TOP, BOT = loop_paths_()

# ================================================================== SEGMENT 0
def cam0(t): return (960, 455, 1.0)

def seg0(c, t):
    s1 = S("0.1")
    # title card
    with card(c, 960, 430, 1300, 400, -1.2, t, 0.15, s1 + 0.7, seed=3) as ok:
        if ok:
            text(c, "AI MONEY  ·  EPISODE 1", 0, -135, "sans", 38, GRAY, spacing=5)
            text(c, "THE AI BUBBLE,", 0, -50, "serif", 96)
            text(c, "EXPLAINED", 0, 50, "serif", 96)
            text(c, "FOLLOW THE MONEY", 0, 140, "sanss", 46, GREEN, spacing=8)
    # 0.1 companies + bars
    names = ["ALPHABET", "AMAZON", "META", "MICROSOFT", "ORACLE"]
    xs = [190, 575, 960, 1345, 1730]
    t0 = Wd("0.1", "five")
    with fade(c, t, S("0.3") + 0.1, None, 0.01):
        pass
    gone = S("0.3") + 0.15
    with fade(c, t, None, gone, 0.4):
        for i, (nm, x) in enumerate(zip(names, xs)):
            stamp(c, nm, x, 150, t, t0 + 0.25 * i + 0.1, INK, (-2, 1.5, -1, 2, -1.5)[i], 44)
        base = 860; sc_ = 0.62
        p1 = e_out(prog(t, Wd("0.1", "four hundred"), E("0.1") - 0.5))
        baseline(c, 400, 1520, base)
        bar(c, 700, base, 300, 400*sc_, p1, GREEN)
        if p1 > 0.02:
            text(c, "$%dB" % round(400*p1), 700, base - 400*sc_*p1 - 52, "mono", 84, GREEN)
        text(c, "2025", 700, base + 38, "mono", 40, INK)
        p2 = e_out(prog(t, Wd("0.2", "around eight"), Wd("0.2", "Double") + 0.3))
        bar(c, 1220, base, 300, 800*sc_, p2, AMBER)
        if p2 > 0.02:
            text(c, "$%dB" % round(800*p2), 1220, base - 800*sc_*p2 - 52, "mono", 84, AMBER)
        text(c, "2026", 1220, base + 38, "mono", 40, INK)
        td = Wd("0.2", "Double")
        if t > td:
            q = prog(t, td, td + 0.6)
            path = bez((760, 590), (960, 430), (1150, 560))
            arrow(c, path, q, RED, 8, pen=True)
            if t > td + 0.5:
                text(c, "×2", 960, 468, "mono", 78, RED, alpha=e_out(prog(t, td + 0.5, td + 0.8)))
                pen_ellipse(c, 960, 468, 78, 52, prog(t, td + 0.6, td + 1.2), RED, 6, 4)
    # 0.3 search
    a3 = S("0.3") + 0.35
    typed = typed_str("is ai a bubble", t, S("0.3") + 1.9, 1.5)
    search_box(c, 960, 450, 1320, 140, typed, t, a3, S("0.4") + 0.9, cursor_t=a3)
    # 0.4 clipping
    a4 = S("0.4") + 0.35
    with card(c, 960, 440, 1240, 380, -1.5, t, a4, S("0.5") - 0.1, seed=5, pulse=None) as ok:
        if ok:
            fade_text(c, "WHERE DOES IT GO?", 0, -62, t, Wd("0.4", "where is"), "serif", 92, INK)
            fade_text(c, "WHAT'S LEFT?", 0, 70, t, Wd("0.4", "what's left"), "serif", 92, RED)
    # 0.5 dollar loops
    a5 = S("0.5") + 0.1
    tc = Wd("0.5", "It goes")
    if t >= a5:
        L1 = 580.0; Ltot = L1 + 1.45 * 2 * math.pi * 190
        if t < tc:
            u = L1 * e_io(prog(t, a5, tc + 0.1))
        else:
            u = L1 + (Ltot - L1) * prog(t, tc, E("0.5") + 1.0) ** 0.9
        # trail
        trail = skia.Path(); trail.moveTo(380, 600)
        n = 90
        for i in range(1, n + 1):
            uu = u * i / n
            x, y, _ = bill_route2(uu)
            trail.lineTo(x, y)
        c.drawPath(trail, P(GREEN, "stroke", 8, 0.55, dash=[22, 16]))
        x, y, ang = bill_route2(u)
        bill(c, x, y, ang * 0.4, 1.0, e_out(prog(t, a5, a5 + 0.3)))

def bill_route2(u):
    L1 = 580.0; R = 190.0
    if u <= L1: return 380 + u, 600, 0.0
    th = (u - L1) / R
    x = 960 + R * math.sin(th)
    y = 410 + R * math.cos(th)
    # moving direction (derivative): (cos th, -sin th)
    ang = math.degrees(math.atan2(-math.sin(th), math.cos(th)))
    return x, y, ang

# ================================================================== SEGMENT 1
def cam1(t):
    return (960, 455, 1.0)

def seg1(c, t):
    S12, S13 = S("1.2"), S("1.3")
    t_nv = S("1.1") + 0.1
    t_oa = Wd("1.2", "OpenAI")
    t_19 = S("1.9")
    # --- NVIDIA + chip
    stamp(c, "NVIDIA", 430, 470, t, t_nv, INK, -2, 52)
    with fade(c, t, S("1.1") + 1.5, None, 0.4):
        chip(c, 430, 350, 0.85, INK)
    stamp(c, "OPENAI", 1490, 470, t, t_oa, INK, 2, 52)
    # --- card 1
    with card(c, 500, 150, 900, 235, -1.4, t, Wd("1.2", "Nvidia announced") , t_19 - 0.1, seed=2) as ok:
        if ok:
            text(c, "NVIDIA: UP TO $100B FOR OPENAI", 0, -58, "serif", 46)
            if t > S("1.3"):
                al = e_out(prog(t, Wd("1.3", "Read the"), Wd("1.3", "the money")))
                text(c, "paid as each gigawatt is deployed", 0, 6, "sanss", 36, INK, alpha=al)
                pen_line(c, -283, 30, 283, 30, prog(t, Wd("1.3", "fine print"), Wd("1.3", "as each")), RED, 6)
            source_line(c, "Source: NVIDIA press release, Sep 2025", -410, 84)
            if t > S("1.7") - 0.0:
                pass
    # stamp NEVER FINALIZED over card1 (screen coords approx card centre)
    stamp(c, "NEVER FINALIZED", 640, 205, t, S("1.7") + 0.15, GRAYDK, -8, 44, b=t_19 - 0.1, slam=2.2)
    # --- card 2 (AMD)
    t_amd = Wd("1.5", "AMD")
    with card(c, 1420, 150, 900, 235, 1.3, t, t_amd + 0.2, S("1.8") + 0.4, seed=4) as ok:
        if ok:
            text(c, "OPENAI ↔ AMD: 6 GW", 0, -34, "serif", 50)
            source_line(c, "Source: AMD press release, Oct 2025", -410, 74)
    with card(c, 1420, 150, 900, 235, 1.3, t, Wd("1.8", "122 billion") - 0.2 if False else Wd("1.8", "closed"), t_19 - 0.1, seed=6) as ok:
        if ok:
            text(c, "OPENAI RAISES $122B", 0, -34, "serif", 50)
            source_line(c, "Source: Bloomberg, Apr 2026", -410, 74)
    # --- top arrow NV -> OA
    top_p = e_io(prog(t, Wd("1.2", "invest"), Wd("1.2", "dollars in")))
    never = t >= S("1.7") + 0.1 and t < t_19
    col_top = GRAYDK if never else GREEN
    if t >= t_19:
        top_p = 1.0
    if never:
        arrow(c, TOP, 1.0, GRAYDK, 9, dashed=[22, 14])
    else:
        # at 1.3: split into ten steps (dashed look)
        steps = prog(t, Wd("1.3", "in stages"), Wd("1.3", "in stages") + 0.6)
        if S("1.3") <= t < S("1.7") and steps > 0:
            arrow(c, TOP, 1.0, GREEN, 11, dashed=[44 - 14*steps, 6 + 14*steps]) if False else None
        arrow(c, TOP, top_p, col_top, 11)
        if S("1.3") <= t < S("1.7"):
            # ten ticks across the arrow
            pm = skia.PathMeasure(TOP, False); Lp = pm.getLength()
            for i in range(1, 10):
                f = i / 10 * steps
                pos, tan = pm.getPosTan(Lp * i / 10)
                nx, ny = -tan.fY, tan.fX
                al = steps
                c.drawLine(pos.fX - nx*22, pos.fY - ny*22, pos.fX + nx*22, pos.fY + ny*22, P(PAPER, "stroke", 9, 1.0*al))
    if t >= Wd("1.2", "up to") and t < S("1.7"):
        fade_text(c, "$100B", 960, 378, t, Wd("1.2", "up to"), "mono", 66, AMBER)
    if t >= S("1.7") and t < t_19:
        fade_text(c, "$100B", 960, 378, t, S("1.7"), "mono", 66, GRAYDK)
    # --- bottom arrow OA -> NV
    t_b = Wd("1.4", "Nvidia systems") - 0.4
    bot_p = e_io(prog(t, S("1.4") + 0.5, S("1.4") + 1.6))
    if t_b > 0 and t >= S("1.4"):
        glow = 0.0
        if S("1.10") <= t < S("1.10") + 2.2:
            glow = 0.5 + 0.5 * math.sin((t - S("1.10")) * 6)
        arrow(c, BOT, bot_p, GREEN, 11 + 4 * glow)
        fade_text(c, "buys NVIDIA systems", 960, 556, t, S("1.4") + 1.0, "sanss", 40, GREEN)
    # circle closes pulse at 1.4
    # --- AMD side
    amd_alpha_end = t_19
    with fade(c, t, None, amd_alpha_end, 0.5, bounds=None):
        stamp(c, "AMD", 960, 800, t, t_amd + 0.1, INK, -1.5, 52)
        p_f = e_io(prog(t, Wd("1.5", "OpenAI would"), Wd("1.5", "of AMD")))
        f_path = bez((1450, 528), (1420, 790), (1140, 790))
        arrow(c, f_path, p_f, GREEN, 10)
        fade_text(c, "6 GW of chips", 1280, 700, t, Wd("1.5", "six"), "mono", 42, GREEN)
        p_r = e_io(prog(t, Wd("1.6", "right to buy"), Wd("1.6", "AMD shares")))
        r_path = bez((1140, 840), (1560, 880), (1530, 530))
        arrow(c, r_path, p_r, AMBER, 10)
        fade_text(c, "up to 160M shares", 1720, 740, t, Wd("1.6", "up to"), "mono", 36, AMBER)
        # unlocking bar
        if t >= Wd("1.6", "unlocked") - 0.4:
            nseg = 8
            unl = prog(t, Wd("1.6", "unlocked"), E("1.6") + 0.2)
            bx = 330
            for i in range(nseg):
                on = unl * nseg > i + 0.3
                r_ = skia.Rect.MakeXYWH(bx + i*54, 780, 46, 40)
                c.drawRect(r_, P(AMBER if on else PAPER2, alpha=1.0))
                c.drawRect(r_, P(INK, "stroke", 3, 0.9))
            text(c, "unlocks as OpenAI buys", bx + 211, 740, "sansr", 34, GRAYDK)
    # --- check 30B
    if t >= Wd("1.8", "Nvidia") - 0.6 and t < t_19 + 0.4:
        q = e_io(prog(t, Wd("1.8", "One of"), Wd("1.8", "came from")))
        if q > 0:
            x, y, ang = pos_on(TOP, q)
            c.save(); c.translate(x, y - 30); c.rotate(ang * 0.5)
            r_ = skia.Rect.MakeXYWH(-110, -42, 220, 84)
            c.drawRect(r_, P(PAPER2)); c.drawRect(r_, P(INK, "stroke", 4))
            c.drawLine(-92, 16, -10, 16, P(INK, "stroke", 3)); c.drawLine(-92, -6, 20, -6, P(INK, "stroke", 2))
            text(c, "$30B", 52, -4, "mono", 40, AMBER)
            c.restore()
    # --- 1.9 labels
    if t >= t_19:
        fade_text(c, "SELLER → BUYER", 960, 268, t, t_19 + 0.1, "mono", 44, GREEN)
        arrow(c, TOP, 1.0, GREEN, 11)
    # --- bill laps (1.10-1.11)
    a10 = S("1.10") + 0.3
    if t >= a10:
        tau = prog(t, a10, E("1.11") + 0.6)
        f = 4.0 * tau ** 1.6
        x, y, ang = loop_pos(f)
        bill(c, x, y, ang * 0.35, 0.8, 1.0)
    # ledger REVENUE
    ta = Wd("1.11", "books")
    with fade(c, t, ta, None, 0.4):
        ledger(c, 360, 790, 0.78, INK)
        text(c, "REVENUE", 360, 650, "mono", 44, GREEN, spacing=3)
        n = int(((t - ta) * 3.5)) % 5
        for i in range(4):
            if i <= n and t > ta + 0.4:
                text(c, "+", 250, 745 + i*28 - 0, "mono", 30, GREEN, "l")

# ================================================================== SEGMENT 2
TONE2 = (S("2.2") + 0.1, S("2.10") - 0.1)
def tone2(t):
    a, b = TONE2
    return e_io(prog(t, a, a + 1.2)) * (1 - e_io(prog(t, b, b + 0.8)))
def cam2(t):
    if t >= S("2.12") - 0.2:
        q = e_io(prog(t, Wd("2.12", "whether its customers"), E("2.12")))
        return (lerp(560, 1160, q), 455, 1.0)
    return (960, 455, 1.0)

def loop_static(c, t, alpha=1.0, gray=False, left="NVIDIA", right="OPENAI", tl="SELLER → BUYER", bl="buys NVIDIA systems", top_p=1.0, bot_p=1.0, a_l=-9, bot_col=None, top_col=None, label=True):
    col = GRAYDK if gray else GREEN
    stamp(c, left, 430, 470, t, a_l, INK, -2, 52)
    stamp(c, right, 1490, 470, t, a_l, INK, 2, 52)
    arrow(c, TOP, top_p, top_col or col, 11)
    arrow(c, BOT, bot_p, bot_col or col, 11)
    if label:
        text(c, tl, 960, 268, "mono", 44, top_col or col) if False else None
        text(c, tl, 960, 384, "mono", 40, top_col or col)
        text(c, bl, 960, 566, "sanss", 40, bot_col or col)

def customers_row(c, t, a, y, bust_times=None, size=1.0, labels=True):
    xs = [330, 590, 850, 1110, 1370, 1630]
    for i, x in enumerate(xs):
        al = e_out(prog(t, a + 0.1*i, a + 0.1*i + 0.3))
        if al <= 0: continue
        c.save(); c.translate(x, y); c.saveLayerAlpha(skia.Rect.MakeXYWH(-80, -90, 160, 180), int(255*al))
        r_ = skia.Rect.MakeXYWH(-56, -56, 112, 112)
        c.drawRect(r_, P(PAPER2)); c.drawRect(r_, P(INK, "stroke", 4))
        # empty coin
        c.drawCircle(0, 0, 26, P(GRAY, "stroke", 4, dash=[8, 8]))
        c.drawLine(-56, -56, 56, -56, P(INK, "stroke", 8))
        c.restore(); c.restore()

def seg2(c, t):
    t1 = S("2.1"); g = tone2(t)
    # 2.1 loop + tag; 2.2 flashback
    loop_gone = S("2.3") - 0.1
    with fade(c, t, None, loop_gone, 0.4):
        loop_static(c, t, top_col=GREEN, bot_col=GREEN)
        # vendor financing tag
        with card(c, 960, 470, 440, 190, -2.0, t, Wd("2.1", "vendor"), None, seed=7, tape=True) as ok:
            if ok:
                text(c, "VENDOR", 0, -34, "serif", 66)
                text(c, "FINANCING", 0, 38, "serif", 66, RED)
    # calendar flip
    ta = S("2.2") + 0.6
    with card(c, 960, 430, 520, 400, 1.5, t, ta, S("2.3") + 0.1, seed=9) as ok:
        if ok:
            c.drawRect(skia.Rect.MakeXYWH(-260, -200, 520, 74), P(RED, alpha=0.9))
            text(c, "YEAR", 0, -163, "sans", 46, PAPER2, spacing=10)
            yr = int(round(roll(t, ta + 0.2, 1.1, 2026, 1999)))
            text(c, str(yr), 0, 20, "mono", 150, AMBER if yr == 1999 else INK)
    # 2.3 Lucent clipping
    ta = S("2.3")
    with card(c, 620, 300, 860, 300, -1.8, t, ta + 0.2, S("2.5") - 0.1, seed=11, tint=0xFFB59B60) as ok:
        if ok:
            text(c, "LUCENT · 1999", 0, -60, "serif", 72)
            text(c, "the internet boom", 0, 14, "sanss", 40, GRAYDK)
            source_line(c, "Source: Fortune, Oct 2010", -400, 100)
    with fade(c, t, ta + 0.8, S("2.5") - 0.1, 0.4):
        # telecom equipment: rack + dish
        c.drawRect(skia.Rect.MakeXYWH(1180, 190, 150, 230), P(PAPER2)); c.drawRect(skia.Rect.MakeXYWH(1180, 190, 150, 230), P(GRAYDK, "stroke", 5))
        for i in range(4):
            c.drawLine(1196, 220 + i*50, 1314, 220 + i*50, P(GRAYDK, "stroke", 4)); c.drawCircle(1296, 238 + i*50 - 0, 5, P(GRAYDK))
        dish = skia.Path(); dish.moveTo(1420, 170); dish.cubicTo(1480, 210, 1480, 280, 1420, 320); dish.cubicTo(1400, 250, 1400, 240, 1420, 170)
        c.drawPath(dish, P(GRAYDK, "stroke", 5)); c.drawLine(1450, 245, 1530, 300, P(GRAYDK, "stroke", 5))
        c.drawLine(1530, 300, 1530, 400, P(GRAYDK, "stroke", 5))
    # 2.4 customers row (empty pockets)
    ta = S("2.4") + 0.2
    with fade(c, t, ta, S("2.5") - 0.1, 0.4):
        customers_row(c, t, ta, 640)
        text(c, "NEW INTERNET COMPANIES · NO CASH", 960, 790, "sans", 40, GRAYDK, spacing=2)
    # 2.5 loop in gray
    t5 = S("2.5")
    with fade(c, t, t5 + 0.1, S("2.7") - 0.1, 0.4):
        stamp(c, "LUCENT", 430, 470, t, t5 + 0.1, INK, -2, 52)
        stamp(c, "CUSTOMERS", 1490, 470, t, t5 + 0.3, INK, 2, 52)
        arrow(c, TOP, e_io(prog(t, t5 + 0.5, t5 + 1.6)), GRAYDK, 11)
        arrow(c, BOT, e_io(prog(t, t5 + 1.6, t5 + 2.6)), GRAYDK, 11)
        fade_text(c, "lends them cash", 960, 384, t, t5 + 0.9, "sanss", 40, GRAYDK)
        fade_text(c, "buys Lucent equipment", 960, 566, t, t5 + 2.0, "sanss", 40, GRAYDK)
        # 2.6 >100% bar
        t6 = S("2.6")
        if t >= t6 + 0.3:
            fill = e_out(prog(t, Wd("2.6", "more than"), Wd("2.6", "percent") + 0.5))
            bx, bw = 560, 760
            c.drawRect(skia.Rect.MakeXYWH(bx, 790, bw, 46), P(PAPER2)); c.drawRect(skia.Rect.MakeXYWH(bx, 790, bw, 46), P(INK, "stroke", 4))
            fw = (bw + 190) * fill
            c.drawRect(skia.Rect.MakeXYWH(bx, 790, fw, 46), P(AMBER, alpha=0.95))
            c.drawRect(skia.Rect.MakeXYWH(bx, 790, min(fw, bw), 46), P(INK, "stroke", 3, 0.5))
            c.drawLine(bx + bw, 770, bx + bw, 858, P(INK, "stroke", 5, dash=[10, 7]))
            text(c, ">100%", bx + bw + 330, 813, "mono", 70, AMBER, alpha=fill)
            text(c, "of a small carrier's equipment", bx + 380, 742, "sansr", 36, GRAYDK, alpha=prog(t, t6 + 0.3, t6 + 0.8))
    # 2.7 $7B
    t7 = S("2.7")
    with card(c, 960, 440, 1180, 440, -1.2, t, t7 + 0.1, S("2.8") - 0.1, seed=13, tint=0xFFB59B60) as ok:
        if ok:
            v = roll(t, t7 + 0.5, 1.8, 0, 7)
            text(c, "$%.0fB" % v, 0, -70, "mono", 190, AMBER)
            text(c, "IN LOANS TO CUSTOMERS", 0, 62, "sans", 60, INK)
            source_line(c, "Source: Fortune, citing SEC filing", -540, 160)
    # 2.8 bankrupt
    t8 = S("2.8")
    with fade(c, t, t8 + 0.1, S("2.9") - 0.1, 0.4):
        stamp(c, "LUCENT", 960, 190, t, t8 + 0.1, INK, 0, 50)
        customers_row(c, t, t8 + 0.2, 470)
        xs = [330, 590, 850, 1110, 1370, 1630]
        tb = Wd("2.8", "bankrupt")
        for i, x in enumerate(xs):
            q = prog(t, t8 + 0.3, t8 + 0.9)
            pth = bez((960, 240), (x, 300), (x, 396))
            arrow(c, pth, q, GRAYDK, 6, head=True)
            if i not in (0, 1, 3, 4): continue   # four go bankrupt, two survive
            ts = tb + 0.22 * (0, 1, 1.6, 2.2, 3.0, 3.6)[i]
            stamp(c, "BANKRUPT", x, 478, t, ts, RED, (-12, 9, -8, 12, -10, 7)[i], 32, spacing=0, pad=(12, 10), slam=2.0)
            if t > ts + 0.2:  # severed arrow
                c.drawLine(x - 24, 336, x + 24, 366, P(RED, "stroke", 8))
        stamp(c, "FILED · 2001", 960, 700, t, Wd("2.8", "filed"), RED, -2, 56)
    # 2.9 stock chart
    t9 = S("2.9")
    with card(c, 960, 440, 1300, 560, 1.0, t, t9 + 0.1, S("2.10") - 0.1, seed=15, tint=0xFFB59B60) as ok:
        if ok:
            text(c, "LUCENT STOCK", -330, -230, "sans", 42, INK, "l")
            text(c, "illustrative", 400, -232, "sansr", 32, GRAYDK, "r")
            c.drawLine(-560, 210, 560, 210, P(INK, "stroke", 4)); c.drawLine(-560, -190, -560, 210, P(INK, "stroke", 4))
            pth = skia.Path(); pth.moveTo(-540, -150)
            pts = [(-540, -150), (-440, -170), (-340, -120), (-250, -175), (-150, -90), (-60, 20), (40, 95), (140, 140), (250, 175), (360, 190), (470, 198)]
            pth = skia.Path(); pth.moveTo(*pts[0])
            for q in pts[1:]: pth.lineTo(*q)
            seg, _, _ = partial(pth, 0, prog(t, t9 + 0.4, E("2.9") + 0.3))
            c.drawPath(seg, P(RED, "stroke", 9))
            if t > E("2.9") - 0.5:
                pen_ellipse(c, 470, 160, 140, 80, prog(t, E("2.9") - 0.5, E("2.9") + 0.2), RED, 6, 5)
                text(c, "< $1", 330, 80, "mono", 72, RED, alpha=prog(t, E("2.9") - 0.2, E("2.9") + 0.3))
    # 2.10 NVIDIA != LUCENT
    t10 = S("2.10")
    with fade(c, t, t10 + 0.1, S("2.11") - 0.1, 0.4):
        stamp(c, "NVIDIA", 520, 450, t, t10 + 0.1, GREEN, -2, 62)
        stamp(c, "LUCENT", 1400, 450, t, t10 + 0.1, GRAYDK, 2, 62)
        text(c, "≠", 960, 450, "sans", 190, AMBER, alpha=e_back(prog(t, t10 + 0.3, t10 + 0.7)))
        fade_text(c, "enormously profitable", 520, 590, t, Wd("2.10", "enormously"), "sanss", 44, GREEN)
    # 2.11 numbers
    t11 = S("2.11")
    with card(c, 500, 440, 800, 470, -1.0, t, t11 + 0.1, S("2.12") - 0.1, seed=17) as ok:
        if ok:
            v = roll(t, Wd("2.11", "89"), 1.4, 0, 89)
            text(c, "$%.0fB" % v, 0, -80, "mono", 170, GREEN)
            text(c, "DATA CENTER,", 0, 50, "sans", 50)
            text(c, "ONE QUARTER", 0, 108, "sans", 50)
            source_line(c, "Source: NVIDIA Q2 FY2027", -370, 190)
    with card(c, 1420, 440, 800, 470, 1.2, t, Wd("2.11", "holds") - 0.2, S("2.12") - 0.1, seed=19) as ok:
        if ok:
            v = roll(t, Wd("2.11", "50 billion") if False else Wd("2.11", "holds"), 1.2, 0, 50)
            text(c, "$%.0fB+" % v, 0, -80, "mono", 170, GREEN)
            text(c, "CASH & BONDS", 0, 62, "sans", 50)
            source_line(c, "Source: NVIDIA Q2 FY2027", -370, 190)
    # 2.12 camera moves from NVIDIA to its customers; 2.13 the $800B bar returns
    t12 = S("2.12"); cx_ = cam2(t)[0]
    if t >= t12 - 0.2:
        with fade(c, t, t12 - 0.2, S("2.13") - 0.1, 0.4):
            stamp(c, "NVIDIA", 340, 440, t, t12 - 0.1, GREEN, -2, 52)
            cust = [("OPENAI", 1180, 270), ("ORACLE", 1180, 450), ("META", 1180, 630), ("MICROSOFT", 1640, 270), ("ALPHABET", 1640, 450), ("AMAZON", 1640, 630)]
            for i, (nm, x, y) in enumerate(cust):
                ts = Wd("2.12", "customers") + 0.12 * i
                stamp(c, nm, x, y, t, ts, INK, (-2, 1.5, -1, 2, -1.5, 1)[i], 44)
                fade_text(c, "?", x + (215 if nm not in ("MICROSOFT", "ALPHABET") else 235), y, t, ts + 0.3, "mono", 90, AMBER)
    t13 = S("2.13")
    if t >= t13 - 0.1:
        with fade(c, t, t13 - 0.05, None, 0.4):
            base = 840; hh = 800 * 0.5
            bx = cx_ - 330
            bar(c, bx, base, 300, hh, e_out(prog(t, t13, t13 + 1.0)), AMBER)
            baseline(c, bx - 220, bx + 220, base)
            text(c, "$800B", bx, base - hh - 60, "mono", 96, AMBER)
            text(c, "2026", bx, base + 36, "mono", 40, INK)
            fade_text(c, "WHO PAYS?", cx_ + 330, 420, t, Wd("2.13", "who's paying"), "serif", 120, RED)
