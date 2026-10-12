# -*- coding: utf-8 -*-
import math, random
import skia
from lib import *
from scenes_a import T, S, E, Wd, TOP, BOT, GRAYDK

def tone5(t):
    a = S("5.2") + 0.1; b = S("5.6") - 0.1
    return e_io(prog(t, a, a + 1.0)) * (1 - e_io(prog(t, b, b + 0.8)))

def cam5(t):
    z = lerp(1.0, 0.9, e_io(prog(t, S("5.11"), E("5.11") + 1.5)))
    return (960, 455, z)

def fiber_bundle(c, x0, x1, y0, n, p, color=INK, spread=14, amp=26, w=5, alpha=1.0, seed=3):
    r = random.Random(seed)
    for i in range(n):
        ph = r.uniform(0, 6.28); am = amp * r.uniform(0.6, 1.2)
        pth = skia.Path(); y = y0 + i*spread
        pth.moveTo(x0, y)
        for k in range(1, 61):
            xx = x0 + (x1 - x0)*k/60
            pth.lineTo(xx, y + am*math.sin(k/60*6.28*2 + ph) * (1 - 0.35*abs(math.sin(i))))
        seg, _, _ = partial(pth, 0, clamp(p))
        c.drawPath(seg, P(color if i % 4 else AMBER, "stroke", w, alpha))

def seg5(c, t):
    t1 = S("5.1")
    # 5.1 cards blown away
    cards = [(380, 190, "$100B FOR OPENAI", -2), (1000, 150, "VENDOR FINANCING", 1.5), (1520, 230, "$170B IN BONDS", -1),
             (300, 520, "$27B OFF THE BOOKS", 2), (900, 520, "×20", -2), (1500, 600, "$600B QUESTION", 1.5),
             (620, 800, "$7B IN LOANS", -1.5), (1280, 830, "16-YEAR GUARANTEE", 2)]
    for i, (x, y, s, rot) in enumerate(cards):
        a = t1 + 0.35 + 0.12*i
        if t > a + 1.6: continue
        q = e_in(prog(t, a, a + 1.3))
        with card(c, x + 1400*q, y - 500*q, 520, 130, rot + 40*q, t, -9, None, seed=40 + i) as ok:
            if ok: text(c, s, 0, 0, "serif", 44)
    with card(c, 960, 450, 1250, 260, -1.2, t, Wd("5.1", "Sometimes"), S("5.2") - 0.1, seed=50) as ok:
        if ok:
            text(c, "SOMETIMES THEY BUILD", 0, 0, "serif", 88)
    # 5.2 fiber
    t2 = S("5.2")
    with fade(c, t, t2 + 0.2, S("5.3") - 0.1, 0.4):
        fiber_bundle(c, 80, 1840, 190, 14, e_io(prog(t, t2 + 0.3, t2 + 3.8)), INK, 18, 38, 5)
        fade_text(c, "100 MILLION MILES", 960, 560, t, Wd("5.2", "about 100"), "mono", 104, AMBER)
        fade_text(c, "of fiber optic cable", 960, 640, t, Wd("5.2", "about 100") + 0.3, "sans", 44, INK)
        text(c, "Source: New York Times, Jun 2001", 960, 710, "sansr", 32, GRAY)
    # 5.3/5.4 grid
    t3 = S("5.3"); t4 = S("5.4"); t5 = S("5.5")
    rr = random.Random(5); order = list(range(100)); rr.shuffle(order)
    lit_final = set(order[:5])
    dark_t = {}
    for rank, idx in enumerate(order[5:]):
        dark_t[idx] = lerp(Wd("5.3", "sitting dark"), Wd("5.3", "sitting dark") + 2.2, rank/95)
    relight = {idx: lerp(Wd("5.4", "switched"), Wd("5.4", "switched") + 3.0, rank/95) for rank, idx in enumerate(order[5:])}
    with fade(c, t, t3, t5 - 0.1, 0.4):
        for idx in range(100):
            r_, k = divmod(idx, 10)
            x = 170 + k*58; y = 190 + r_*58
            dark = idx in dark_t and t > dark_t[idx] and not (t > relight[idx])
            col = GREEN
            c.drawCircle(x, y, 22, P(GRAYDK if dark else mix(PAPER2, GREEN, 0.5)))
            c.drawCircle(x, y, 22, P(GRAYDK if dark else GREEN, "stroke", 3.5))
            c.drawCircle(x, y, 7, P(PAPER2 if dark else AMBER))
        with fade(c, t, Wd("5.3", "95 percent"), t4 + 0.3, 0.3):
            text(c, "95%", 1330, 330, "mono", 190, AMBER)
            text(c, "DARK", 1330, 460, "mono", 100, INK)
            text(c, "Source: New York Times, Jun 2001", 1330, 560, "sansr", 32, GRAY)
        with fade(c, t, t4 + 0.2, t5 - 0.1, 0.3):
            tag(c, "PRICE: $$$", 1330, 330, t, t4 + 0.2, INK, 60, "mono")
            cross_out(c, 1130, 345, 1530, 315, t, Wd("5.4", "cheaply") - 0.3, RED, 9, 0.35)
            tag(c, "PRICE: $", 1330, 480, t, Wd("5.4", "cheaply"), GREEN, 60, "mono")
    # 5.5 split
    with fade(c, t, t5, S("5.6") - 0.1, 0.4):
        c.drawRect(skia.Rect.MakeXYWH(0, 0, 940, 1080), P(RED, alpha=0.12)); c.drawRect(skia.Rect.MakeXYWH(980, 0, 940, 1080), P(GREEN, alpha=0.14))
        c.drawLine(960, 0, 960, 1080, P(INK, "stroke", 6, dash=[30, 14, 6, 14]))
        fade_text(c, "PAID FOR IT", 470, 380, t, Wd("5.5", "disaster"), "serif", 100, RED)
        fade_text(c, "CAME AFTER", 1450, 380, t, Wd("5.5", "bargain"), "serif", 100, GREEN)
        bill(c, 470, 580, -6, 1.5, e_out(prog(t, Wd("5.5", "disaster"), Wd("5.5", "disaster") + 0.4)), RED)
        bill(c, 1450, 580, 5, 1.5, e_out(prog(t, Wd("5.5", "bargain"), Wd("5.5", "bargain") + 0.4)), GREEN)
    # 5.6 fiber vs gpu
    t6 = S("5.6")
    with fade(c, t, t6, S("5.7") - 0.1, 0.4):
        fiber_bundle(c, 90, 800, 300, 8, 1.0, GREEN, 16, 24, 5)
        text(c, "2001: FIBER", 445, 560, "mono", 48, INK)
        for i in range(6):
            r_, k = divmod(i, 3)
            fade_text(c, "", 0, 0, t, 0)
            with fade(c, t, Wd("5.6", "AI bubble") + 0.15*i, None, 0.3):
                gpu(c, 1130 + k*210, 330 + r_*150, 1.2, INK)
        text(c, "NOW: CHIPS", 1340, 560, "mono", 48, INK)
        fade_text(c, "?", 960, 440, t, Wd("5.6", "AI bubble"), "mono", 200, AMBER)
    # 5.7 timelines
    t7 = S("5.7")
    with fade(c, t, t7, S("5.8") - 0.1, 0.4):
        text(c, "FIBER", 170, 300, "mono", 52, GREEN)
        arrow(c, bez((330, 300), (1000, 300), (1800, 300)), e_io(prog(t, Wd("5.7", "Fiber lasts"), Wd("5.7", "Fiber lasts") + 1.6)), GREEN, 14)
        fade_text(c, "DECADES", 1060, 225, t, Wd("5.7", "decades"), "mono", 64, GREEN)
        text(c, "CHIPS", 170, 620, "mono", 52, INK)
        t0 = Wd("5.7", "A new generation")
        for i in range(5):
            a = lerp(Wd("5.7", "AI chips"), E("5.7") - 0.3, i/5)
            if i > 0: pass
            nxt = lerp(Wd("5.7", "AI chips"), E("5.7") - 0.3, (i+1)/5)
            old = t > nxt
            x = 330 + i*290
            with fade(c, t, a, None, 0.25):
                r_ = skia.Rect.MakeXYWH(x, 565, 260, 110)
                c.drawRect(r_, P(mix(PAPER2, GRAYDK, 0.5) if old else mix(PAPER2, AMBER, 0.45)))
                c.drawRect(r_, P(GRAYDK if old else INK, "stroke", 4))
                text(c, "GEN %d" % (i+1), x + 130, 620, "mono", 44, GRAYDK if old else INK)
        fade_text(c, "A NEW GENERATION EVERY 1–2 YEARS", 960, 760, t, t0, "sanss", 40, RED)
    # 5.8 ruler
    t8 = S("5.8"); t10 = S("5.10")
    with fade(c, t, t8, t10 - 0.1, 0.4):
        server(c, 520, 450, 1.8, INK)
        baseline(c, 800, 1800, 560, INK)
        for k in range(7):
            x = 800 + k*1000/6
            c.drawLine(x, 560, x, 590, P(INK, "stroke", 4)); text(c, str(k), x, 625, "mono", 34, INK)
        text(c, "YEARS", 1810, 625, "mono", 34, GRAYDK, "l") if False else None
        bar(c, 800 + 0, 560, 0, 0, 0)
        w = 917*e_out(prog(t, Wd("5.8", "five or six") - 0.2, Wd("5.8", "five or six") + 1.0))
        c.drawRect(skia.Rect.MakeXYWH(800, 500, w, 44), P(AMBER)); c.drawRect(skia.Rect.MakeXYWH(800, 500, w, 44), P(INK, "stroke", 3))
        fade_text(c, "5–6 YEARS", 1300, 400, t, Wd("5.8", "five or six"), "mono", 84, AMBER)
        fade_text(c, "cost spread over", 1300, 330, t, Wd("5.8", "spread"), "sanss", 40, INK)
    silhouette(c, 170, 560, 0.8, t, S("5.9") + 0.15, "MICHAEL BURRY", 34, b=t10 - 0.1)
    with fade(c, t, Wd("5.9", "too long"), t10 - 0.1, 0.4):
        c.drawRect(skia.Rect.MakeXYWH(800, 700, 417*e_out(prog(t, Wd("5.9", "too long"), Wd("5.9", "too long") + 0.8)), 44), P(RED))
        fade_text(c, "2–3 YR PRODUCT CYCLE", 1020, 790, t, Wd("5.9", "too long") + 0.3, "mono", 44, RED, "l" if False else "c")
        pen_ellipse(c, 1010, 760, 300, 90, prog(t, Wd("5.9", "too long") + 0.8, Wd("5.9", "too long") + 1.5), RED, 6, 12)
    # 5.10 number
    with card(c, 960, 430, 1260, 480, -1.0, t, t10 + 0.1, None, seed=60) as ok:
        if ok:
            v = roll(t, Wd("5.10", "176"), 1.6, 0, 176)
            text(c, "≈ $%.0fB" % v, 0, -110, "mono", 180, RED)
            text(c, "OVERSTATED PROFITS", 0, 20, "sans", 56)
            text(c, "THROUGH 2028", 0, 90, "sans", 56)
            text(c, "Burry's estimate, Nov 2025", 0, 180, "sansr", 32, GRAY)
    stamp(c, "ONE INVESTOR'S VIEW", 960, 460, t, S("5.11") + 0.3, GRAYDK, -8, 70, slam=2.2, alpha_max=0.92, fill=0xE6EFE9DD)

# ====================================================================== SEGMENT 6
def cam6(t):
    a = S("6.4") - 0.1; b = S("6.5") - 0.5
    if a <= t < b + 0.8:
        q = e_io(prog(t, a, a + 0.9)) * (1 - e_io(prog(t, b, b + 0.8)))
        return (lerp(960, 1400, q), 455, lerp(1.0, 1.65, q))
    return (960, 455, 1.0)

def circle_draw(c, cx, cy, r, p, color=INK, w=7, alpha=1.0):
    pth = skia.Path(); pth.addOval(skia.Rect.MakeXYWH(cx - r, cy - r, 2*r, 2*r))
    seg, _, _ = partial(pth, 0, clamp(p)); c.drawPath(seg, P(color, "stroke", w, alpha))

def crack(c, cx, cy, p):
    r = random.Random(4)
    for k in range(3):
        ang = math.radians(-40 + k*30)
        x, y = cx + 300*math.cos(ang), cy + 300*math.sin(ang)
        pth = skia.Path(); pth.moveTo(x, y)
        for j in range(1, 6): pth.lineTo(x - j*math.cos(ang)*22 + r.uniform(-14, 14), y - j*math.sin(ang)*22 + r.uniform(-14, 14))
        seg, _, _ = partial(pth, 0, p); c.drawPath(seg, P(RED, "stroke", 8))

def seg6(c, t):
    t1 = S("6.1"); t2 = S("6.2"); t3 = S("6.3"); t4 = S("6.4"); t5 = S("6.5")
    gone = t5 - 0.4
    with fade(c, t, t1, gone, 0.4):
        circle_draw(c, 520, 450, 300, e_io(prog(t, t1 + 0.2, t1 + 1.2)))
        circle_draw(c, 1400, 450, 300, e_io(prog(t, t1 + 0.6, t1 + 1.6)))
    # left: prices
    with fade(c, t, Wd("6.2", "prices"), gone, 0.4):
        text(c, "PRICES", 520, 255, "mono", 56, INK, spacing=4)
        c.save(); c.translate(520, 410); c.scale(0.34, 0.34); c.translate(-960, -470)
        arrow(c, TOP, 1, GREEN, 30); arrow(c, BOT, 1, GREEN, 30)
        c.drawCircle(430, 470, 70, P(INK)); c.drawCircle(1490, 470, 70, P(INK))
        c.restore()
        pts = [(380, 640), (420, 610), (450, 625), (500, 570), (540, 590), (590, 530), (640, 545)]
        pth = skia.Path(); pth.moveTo(*pts[0])
        for q in pts[1:]: pth.lineTo(*q)
        c.drawPath(pth, P(GREEN, "stroke", 7))
        td = Wd("6.2", "pop fast")
        if t > td:
            q2 = prog(t, td, td + 0.4)
            c.drawLine(640, 545, lerp(640, 690, q2), lerp(545, 660, q2), P(RED, "stroke", 8))
            crack(c, 520, 450, e_out(prog(t, td, td + 0.6)))
    # right: things
    ta = Wd("6.3", "buildings")
    chip_old = t > Wd("6.3", "obsolete")
    with fade(c, t, ta - 0.3, t4 + 0.01 if False else gone, 0.4):
        text(c, "THINGS", 1400, 255, "mono", 56, INK, spacing=4)
        with fade(c, t, ta, None, 0.3): building(c, 1300, 590, 0.5, INK)
        with fade(c, t, Wd("6.3", "power lines"), None, 0.3): pylon(c, 1470, 590, 0.62, INK)
        with fade(c, t, Wd("6.3", "grid"), None, 0.3):
            amb = prog(t, t4 - 0.05, t4 + 0.4)
            if amb > 0: c.drawCircle(1535, 420, 70*amb, P(AMBER, alpha=0.4))
            plug(c, 1535, 420, 0.8, INK, 1.0, 0, False)
        with fade(c, t, Wd("6.3", "chips"), None, 0.3):
            chip(c, 1330, 410, 0.9, GRAYDK if chip_old else INK)
            if chip_old: cross_out(c, 1270, 350, 1390, 470, t, Wd("6.3", "obsolete"), RED, 8)
        fade_text(c, "DECADES", 1385, 640, t, Wd("6.3", "last decades"), "mono", 36, GREEN, b=t4 - 0.1)
        fade_text(c, "3 YEARS", 1330, 490, t, Wd("6.3", "obsolete"), "mono", 34, RED)
    fade_text(c, "ELECTRICITY", 1400, 650, t, t4 + 0.3, "mono", 56, AMBER, b=t5 - 0.3)
    # 6.5 warehouse
    with fade(c, t, t5, S("6.6") - 0.1, 0.4):
        building(c, 640, 740, 2.0, INK)
        for i in range(6):
            r_, k = divmod(i, 3)
            chip(c, 520 + k*120, 640 + r_*0 + (i//3)*0, 0.38, INK) if False else None
        for i in range(6):
            r_, k = divmod(i, 3); chip(c, 490 + k*150, 560 + r_*100, 0.5, INK)
        plug(c, 1250, 600, 1.5, INK, 1.0, -0.4, True)
        c.drawRect(skia.Rect.MakeXYWH(1560, 560, 90, 120), P(PAPER2)); c.drawRect(skia.Rect.MakeXYWH(1560, 560, 90, 120), P(INK, "stroke", 5))
        for yy in (590, 640): c.drawLine(1590, yy, 1620, yy, P(INK, "stroke", 6))
        fade_text(c, "NO POWER TO PLUG IN", 1400, 430, t, Wd("6.5", "power to plug"), "mono", 44, AMBER)
        text(c, "Source: Satya Nadella, BG2 Pod, Nov 2025", 960, 850, "sansr", 32, GRAY)
    # 6.6 queue
    t6 = S("6.6")
    with fade(c, t, t6, S("6.7") - 0.1, 0.4):
        stamp(c, "APPLY", 280, 470, t, t6 + 0.1, INK, -2, 48)
        x0 = 440; ppy = 200
        wq = e_io(prog(t, Wd("6.6", "waited") - 0.5, E("6.6") - 0.3))
        c.drawLine(x0, 470, x0 + 1050, 470, P(GRAY, "stroke", 6, dash=[14, 10]))
        c.drawLine(x0, 470, x0 + 1050*wq, 470, P(RED, "stroke", 16))
        for k in range(1, 6):
            x = x0 + k*ppy*0.95 * 1.0
            c.drawLine(x, 450, x, 490, P(INK, "stroke", 4)); text(c, str(k), x, 530, "mono", 34, INK)
        fade_text(c, "> 5 YRS (median)", 960, 300, t, Wd("6.6", "more than"), "mono", 84, AMBER)
        stamp(c, "CONNECTED", 1670, 470, t, E("6.6") - 0.3, GREEN, 2, 44)
        text(c, "Source: Berkeley Lab, Queued Up 2026", 960, 640, "sansr", 32, GRAY)
    # 6.7 chips scrap, building stays
    t7 = S("6.7")
    with fade(c, t, t7, S("6.8") - 0.1, 0.4):
        building(c, 640, 740, 2.0, INK, 1.0, win_color=GREEN)
        pylon(c, 1250, 740, 1.5, INK)
        pth = bez((1180, 610), (900, 650), (900, 560)); c.drawPath(pth, P(AMBER, "stroke", 8))
        c.drawLine(1180, 610, 1180, 580, P(AMBER, "stroke", 8))
        q = e_io(prog(t, Wd("6.7", "scrap") - 0.3, Wd("6.7", "scrap") + 1.2))
        gq = prog(t, Wd("6.7", "after"), Wd("6.7", "scrap"))
        for i in range(6):
            r_, k = divmod(i, 3)
            col = mix(INK, GRAYDK, gq)
            chip(c, 490 + k*150 + 900*q, 560 + r_*100 + 80*q*0, 0.5, col, 1 - 0.7*q)
        fade_text(c, "STILL WORTH SOMETHING", 960, 260, t, Wd("6.7", "still worth"), "serif", 70, GREEN)
    # 6.8 fiber vs power
    t8 = S("6.8")
    with fade(c, t, t8, S("6.9") - 0.1, 0.4):
        fiber_bundle(c, 90, 800, 330, 9, 1.0, GREEN, 16, 24, 6)
        building(c, 1150, 560, 1.0, INK); pylon(c, 1530, 560, 1.0, INK)
        c.drawPath(bez((1470, 420), (1330, 480), (1250, 470)), P(AMBER, "stroke", 7))
        fade_text(c, "2001: FIBER", 445, 680, t, t8 + 0.5, "mono", 52, GREEN)
        fade_text(c, "2026: POWER?", 1340, 680, t, Wd("6.8", "concrete") - 0.4, "mono", 52, AMBER)
        fade_text(c, "the concrete and the copper", 1340, 760, t, Wd("6.8", "concrete"), "sanss", 40, INK)
    # 6.9 search box
    t9 = S("6.9")
    search_box(c, 960, 330, 1300, 140, "is ai a bubble", t, t9 - 0.0, S("6.10") - 0.1, strike=Wd("6.9", "is A I") if False else Wd("6.9", "instead"))
    with fade(c, t, Wd("6.9", "ask"), S("6.10") - 0.1, 0.3):
        search_box(c, 960, 560, 1300, 140, typed_str("which parts last?", t, Wd("6.9", "ask"), 1.4), t, Wd("6.9", "ask") - 0.05, None, cursor_t=Wd("6.9", "ask"), text_color=GREEN)
    # 6.10 index fund
    t10 = S("6.10")
    with fade(c, t, t10, S("6.11") - 0.1, 0.4):
        names = ["NVIDIA", "MICROSOFT", "ALPHABET", "AMAZON", "META", "ORACLE"]
        cols = [GREEN, GRAY, LGRAY, mix(GREEN, PAPER2, 0.5), mix(AMBER, PAPER2, 0.3), mix(GRAY, PAPER2, 0.4)]
        pc = (560, 470); R = 240
        fr = [0.17, 0.15, 0.12, 0.10, 0.08, 0.05]; rest = 1 - sum(fr)
        a0 = -90.0
        mids = []
        sweep_t = e_out(prog(t, t10 + 0.2, t10 + 1.2))
        for i, f in enumerate(fr + [rest]):
            sw = f*360*sweep_t
            col = cols[i] if i < 6 else mix(PAPER2, INK, 0.12)
            c.drawArc(skia.Rect.MakeXYWH(pc[0]-R, pc[1]-R, 2*R, 2*R), a0, sw, True, P(col))
            c.drawArc(skia.Rect.MakeXYWH(pc[0]-R, pc[1]-R, 2*R, 2*R), a0, sw, True, P(INK, "stroke", 3))
            mids.append(math.radians(a0 + f*360/2))
            a0 += sw
        text(c, "INDEX FUND", 560, 200, "mono", 48, INK, spacing=4)
        text(c, "illustrative", 560, 750, "sansr", 32, GRAYDK)
        for i, nm in enumerate(names):
            ty = 270 + i*88
            ta_ = Wd("6.10", "you already") - 0.2 + 0.18*i
            with fade(c, t, ta_, None, 0.3):
                c.drawLine(pc[0] + R*0.7*math.cos(mids[i]), pc[1] + R*0.7*math.sin(mids[i]), 990, ty, P(INK, "stroke", 3, alpha=0.6))
                tag(c, nm, 1130, ty, t, -9, INK, 38, "mono")
        with fade(c, t, Wd("6.10", "piece"), None, 0.4):
            c.drawLine(1350, 270, 1350, 710, P(INK, "stroke", 6)); c.drawLine(1350, 490, 1440, 490, P(GREEN, "stroke", 7))
            c.save(); c.translate(1660, 490); c.scale(0.3, 0.3); c.translate(-960, -470)
            arrow(c, TOP, 1, GREEN, 36); arrow(c, BOT, 1, GREEN, 36)
            c.drawCircle(430, 470, 80, P(INK)); c.drawCircle(1490, 470, 80, P(INK))
            c.restore()
    # 6.11 options
    t11 = S("6.11"); t12_ = S("6.12")
    with fade(c, t, t11, t12_ - 0.1, 0.4):
        for x, lab in ((520, "BUILDINGS & POWER"), (1400, "CHIPS")):
            rr_ = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x - 330, 300, 660, 300), 22, 22)
            c.drawRRect(rr_, P(PAPER2)); c.drawRRect(rr_, P(INK, "stroke", 5))
            text(c, lab, x, 540, "sans", 54, INK)
        building(c, 400, 480, 0.5, INK); pylon(c, 620, 480, 0.6, INK)
        chip(c, 1400, 430, 1.3, INK)
        gq = prog(t, Wd("6.11", "buildings"), Wd("6.11", "buildings") + 0.5)
        if gq > 0:
            ck = skia.Path(); ck.moveTo(780, 330); ck.lineTo(810, 362); ck.lineTo(860, 300)
            c.drawPath(ck, P(GREEN, "stroke", 14*gq))
        if t > Wd("6.11", "Tell me") and int((t - t11) * 2) % 2 == 0:
            c.drawRect(skia.Rect.MakeXYWH(955, 380, 8, 140), P(INK))
        fade_text(c, "Tell me in the comments", 960, 700, t, Wd("6.11", "Tell me"), "sanss", 48, INK)
    # 6.12 end
    t12 = S("6.12")
    with fade(c, t, t12 + 0.2, None, 0.4):
        text(c, "Not investment advice.", 960, 300, "sanss", 56, INK)
    with fade(c, t, t12 + 0.2, None, 0.4):
        pass
    if t >= t12 - 0.4 and t < E("6.12") + 2.4:
        tt = t - (t12 - 0.4)
        tot = (E("6.12") + 1.4) - (t12 - 0.4)
        f = prog(tt, 0, tot)
        ang = -math.pi/2 + 2*math.pi*2*e_out(f)
        r_ = 150*(1 - e_in(prog(f, 0.75, 1.0)))
        x = 960 + r_*math.cos(ang); y = 560 + r_*math.sin(ang)*0.6
        al = 1 - e_io(prog(t, E("6.12") + 0.6, E("6.12") + 2.2))
        if al > 0: bill(c, x, y, math.degrees(ang) * 0.1, 1.2, al)

REG = {5: (cam5, seg5, tone5), 6: (cam6, seg6, None)}
