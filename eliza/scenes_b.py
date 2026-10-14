# -*- coding: utf-8 -*-
"""Segments 2-3: how people reacted, and who Weizenbaum was."""
import math, random
import skia
from lib import *
from props import *
from scenes_a import T, S, E, Wd, CAM, quote_slip, tile, desk

def suitcase(c, x, y, s=1.0, rot=0.0, alpha=1.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    if alpha < 1: c.saveLayerAlpha(skia.Rect.MakeXYWH(-90, -90, 180, 160), int(255*alpha))
    hnd = skia.Path(); hnd.moveTo(-26, -40); hnd.lineTo(-26, -62); hnd.lineTo(26, -62); hnd.lineTo(26, -40); c.drawPath(hnd, P(INK, "stroke", 6))
    c.drawPath(rect_path(-72, -42, 144, 96, 10), P(PAPER3)); ink(c, rect_path(-72, -42, 144, 96, 10), 5)
    c.drawLine(-72, -4, 72, -4, P(INK, "stroke", 3.5)); c.drawRect(skia.Rect.MakeXYWH(-10, -12, 20, 16), P(INK))
    if alpha < 1: c.restore()
    c.restore()

def machine_box(c, x, y, s=1.0, t=0.0, alpha=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    if alpha < 1: c.saveLayerAlpha(skia.Rect.MakeXYWH(-200, -300, 400, 330), int(255*alpha))
    c.drawPath(rect_path(-130, -230, 260, 230, 12), P(PAPER2)); ink(c, rect_path(-130, -230, 260, 230, 12), 5)
    c.drawPath(rect_path(-90, -200, 180, 70, 8), P(PAPER)); ink(c, rect_path(-90, -200, 180, 70, 8), 3.4)
    for k in range(3): c.drawLine(-70, -182 + k*18, 40 - k*20, -182 + k*18, P(INK2, "stroke", 3))
    gear(c, -50, -70, 40, t*0.8, INK); gear(c, 40, -60, 30, -t*1.0 + 0.3, INK, teeth=8)
    c.drawLine(0, -230, 0, -270, P(INK, "stroke", 5)); c.drawCircle(0, -278, 12, P(VERM))
    if alpha < 1: c.restore()
    c.restore()

def basket(c, x, y, s=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    p = skia.Path(); p.moveTo(-60, -20); p.lineTo(-44, 40); p.lineTo(44, 40); p.lineTo(60, -20); p.close()
    c.drawPath(p, P(PAPER3)); ink(c, p, 4.5)
    hatch(c, p, 45, 12, 2, INK2, 0.5, cross=True)
    for i, (fx, fy) in enumerate(((-34, -44), (-6, -62), (24, -48), (46, -34))):
        c.drawLine(fx, fy + 20, fx*0.7, -18, P(INK, "stroke", 3.5)); c.drawCircle(fx, fy, 14, P(VERM if i % 2 == 0 else PAPER2)); c.drawCircle(fx, fy, 14, P(INK, "stroke", 3))
    c.restore()

def diary(c, x, y, s=1.0, alpha=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawPath(rect_path(-110, -150, 220, 300, 8), P(PAPER3)); ink(c, rect_path(-110, -150, 220, 300, 8), 5)
    c.drawRect(skia.Rect.MakeXYWH(-110, -150, 26, 300), P(INK2));
    c.drawLine(-60, -60, 80, -60, P(INK2, "stroke", 3)); c.drawLine(-60, -30, 60, -30, P(INK2, "stroke", 3)); c.drawLine(-60, 0, 70, 0, P(INK2, "stroke", 3))
    padlock(c, 110, 40, 0.8)
    c.restore()

# ===================================================================================================
def draw2(c, t):
    # ---- 2.1 surprise ----
    a, b = S("2.1") - 0.8, S("2.2") - 0.55
    with fade(c, t, a, b, 0.4, bleed=True) as v:
        if v:
            person2(c, 600, 800, 1.25, "man", glasses=True)
            q = prog(t, a + 1.3, a + 2.1)
            sparkles_burst(c, 600, 430, q, 11, 60, 190, VERM, 8)
            fade_text(c, "!", 600, 380, t, a + 1.3, "type", 190, VERM, "c", dur=0.3, rise=0)
            fade_text(c, "the part he", 1300, 380, t, Wd("2.1", "Now the") + 0.4, "hand", 100, INK2, "c")
            fade_text(c, "did not expect", 1300, 500, t, Wd("2.1", "did not") - 0.1, "hand", 100, VERM, "c")
    # ---- 2.2 quote: startled ----
    a, b = S("2.2") + 0.1, S("2.3") - 0.2
    quote_slip(c, t, a, b, 960, 330, 1560, 400,
               "I was startled to see how quickly and how very deeply people conversing with DOCTOR became emotionally involved with the computer and how unequivocally they anthropomorphized it.",
               "J. Weizenbaum, Computer Power and Human Reason (1976), p. 6", 46, rot=-0.8,
               hl=["how quickly", "how very deeply", "emotionally involved with the computer"],
               hl_times=[Wd("2.2", "quickly") - 0.2, Wd("2.2", "deeply") - 0.3, Wd("2.2", "emotionally") - 0.2], seed=21)
    with fade(c, t, S("2.2") + 0.9, b, 0.4) as v:
        if v:
            for i in range(6):
                xx = 400 + i * 224; ta = S("2.2") + 1.2 + i * 0.35
                q = e_out(prog(t, ta, ta + 0.4))
                small_person(c, xx, 840, 1.7, INK, q)
                th = Wd("2.2", "emotionally") - 0.2 + i * 0.18
                qh = e_out(prog(t, th, th + 0.4))
                if qh > 0: heart(c, xx, 700 - 8 * math.sin(t * 3 + i), 0.95 * qh, VERM, qh)
    # ---- 2.3 overnight ----
    a, b = S("2.3") + 0.25, S("2.4") - 0.15
    with fade(c, t, a, b, 0.4, bleed=True) as v:
        if v:
            person2(c, 440, 820, 1.2, "man", glasses=True)
            desk(c, t, a, 700, 1560, 830, 0.8)
            terminal(c, 1400, 830, 1.05, key_t=t, paper_lines=[0.8, 0.6, 0.9, 0.5], paper_h=0.8)
            fade_text(c, "every conversation", 1400, 330, t, Wd("2.3", "every") - 0.2, "hand", 70, INK2, "c")
            # sheets sliding from terminal to the man's desk
            for i in range(7):
                ta = Wd("2.3", "read") - 0.3 + i * 0.35
                q = prog(t, ta, ta + 1.4)
                if 0 < q < 1.0 or q >= 1.0:
                    x = lerp(1400, 820 + i * 6, e_io(min(1, q))); y = lerp(660, 780 - min(i, 6) * 12, e_io(min(1, q))) - 70 * math.sin(math.pi * min(1, q))
                    c.save(); c.translate(x, y); c.rotate(-6 + i * 2)
                    c.drawRect(skia.Rect.MakeXYWH(-52, -36, 104, 72), P(PAPER2)); c.drawRect(skia.Rect.MakeXYWH(-52, -36, 104, 72), P(INK, "stroke", 3))
                    for l in range(3): c.drawLine(-38, -18 + l*16, 36 - l*10, -18 + l*16, P(INK2, "stroke", 2.4))
                    c.restore()
            # moon + clock = overnight
            if t > Wd("2.3", "overnight") - 0.6:
                q = e_out(prog(t, Wd("2.3", "overnight") - 0.6, Wd("2.3", "overnight")))
                crescent(c, 1700, 190, 70 * q, INK, q)
                clock(c, 1480, 200, 66 * q, ((t - Wd("2.3", "overnight")) * 0.5) % 1.0, INK, q)
                fade_text(c, "overnight", 1590, 400, t, Wd("2.3", "overnight") - 0.2, "hand", 66, VERM, "c")
    # ---- 2.4 accused of spying ----
    a, b = S("2.4") + 0.25, S("2.5") - 0.15
    with fade(c, t, a, b, 0.4, bleed=True) as v:
        if v:
            person2(c, 960, 840, 1.2, "man", glasses=True)
            spots = [(330, 800, "man", False), (590, 840, "woman", False), (1330, 840, "man", True), (1590, 800, "woman", True)]
            for i, (x, y, k, fl) in enumerate(spots):
                ta = a + 0.5 + i * 0.35
                q = e_out(prog(t, ta, ta + 0.4))
                person2(c, x, y, 0.62, k, flip=fl, alpha=q)
                bx = x + (80 if not fl else -80)
                if q > 0.3:
                    bubble(c, bx, y - 230 - (i % 2) * 40, 120, 110, tail=(-0.5 if not fl else 0.5, 1), alpha=q)
                    text(c, "!", bx, y - 230 - (i % 2) * 40, "type", 80, VERM, alpha=q)
            label(c, "“spying on people's most intimate thoughts”", 960, 190, t, Wd("2.4", "spying") - 0.3, INK, 44, "type")
            fade_text(c, "J. Weizenbaum, 1976, p. 6", 960, 280, t, Wd("2.4", "spying") + 0.3, "type", 36, INK2, "c")
    # ---- 2.5 not a diary ----
    a, b = S("2.5") + 0.25, S("2.6") - 0.15
    with fade(c, t, a, b, 0.4, bleed=True) as v:
        if v:
            diary(c, 560, 520, 1.15)
            fade_text(c, "a diary", 560, 760, t, Wd("2.5", "diary") - 0.1, "hand", 80, INK2, "c")
            strike(c, 390, 740, 740, prog(t, Wd("2.5", "not") , Wd("2.5", "not") + 0.5), VERM, 9) if False else None
            if t > Wd("2.5", "not") - 0.1:
                p = prog(t, Wd("2.5", "not") - 0.1, Wd("2.5", "not") + 0.5)
                strike(c, 380, 740, 764, p, VERM, 10)
            terminal(c, 1330, 760, 1.2, key_t=t, paper_lines=[0.8, 0.6, 0.9, 0.5], paper_h=0.9)
            qpad = e_back(prog(t, Wd("2.5", "protecting a chat") - 0.2, Wd("2.5", "protecting a chat") + 0.4))
            if qpad > 0: padlock(c, 1330, 360, 1.7 * qpad, INK, min(1, qpad))
            fade_text(c, "a chat with a machine", 1330, 820 + 40, t, Wd("2.5", "chat with") , "hand", 80, VERM, "c")
    # ---- 2.6 magic crumbles ----
    a, b = S("2.6") + 0.1, S("2.7") - 0.2
    with fade(c, t, a, b, 0.4) as v:
        if v:
            tc = Wd("2.6", "crumbles")
            # star that crumbles into falling fragments
            if t < tc:
                q = e_out(prog(t, a + 0.2, a + 0.9))
                c.save(); c.translate(960, 190); c.rotate(t * 0.4)
                for k in range(8):
                    ang = k * math.pi / 4; c.drawLine(0, 0, 80 * q * math.cos(ang), 80 * q * math.sin(ang), P(INK, "stroke", 5 if k % 2 == 0 else 3))
                c.drawCircle(0, 0, 16 * q, P(VERM))
                c.restore()
            else:
                rr = random.Random(5)
                for k in range(26):
                    ang = rr.uniform(0, 2 * math.pi); r0 = rr.uniform(10, 80); v0 = rr.uniform(20, 90)
                    q = t - tc
                    x = 960 + r0 * math.cos(ang) + v0 * math.cos(ang) * q * 0.6
                    y = 190 + r0 * math.sin(ang) + v0 * math.sin(ang) * q * 0.6 + 260 * q * q
                    al = max(0.0, 1 - q / 1.8)
                    if al > 0 and y < 900:
                        c.save(); c.translate(x, y); c.rotate(q * rr.uniform(-5, 5))
                        c.drawLine(-10, 0, 10, 0, P(VERM if k % 3 == 0 else INK, "stroke", 5, al)); c.restore()
            quote_slip(c, t, a + 0.3, b - 0.1, 960, 600, 1560, 360,
                       "…its magic crumbles away; it stands revealed as a mere collection of procedures…",
                       "J. Weizenbaum, CACM, January 1966", 54, rot=-0.6, hl=["magic crumbles away"], hl_t=tc - 0.2, seed=24)
    # ---- 2.7 she knew ----
    a, b = S("2.7") + 0.3, S("2.9") - 0.15
    with fade(c, t, a, b, 0.4, bleed=True) as v:
        if v:
            person2(c, 640, 810, 1.2, "woman")
            terminal(c, 1040, 810, 1.15, key_t=None, paper_lines=[0.8, 0.5, 0.7], paper_h=0.8)
            desk(c, t, a - 0.1, 380, 1380, 810, 0.6)
            bub_a = e_out(prog(t, S("2.7") + 1.4, S("2.7") + 1.8)) * (1 - e_in(prog(t, S("2.8"), S("2.8") + 0.4)))
            bubble(c, 420, 330, 440, 120, tail=(1, 1), thought=True, alpha=bub_a)
            if t > S("2.7") + 1.6: text(c, "she knew", 420, 330, "hand", 66, INK, alpha=bub_a)
            tm = S("2.7") + 0.2
            months = ["JAN", "MAR", "MAY", "JUL", "SEP", "NOV"]
            k = min(5, int(max(0, t - tm) / 0.5))
            if t < S("2.8") - 0.1:
                calendar_page(c, 1620, 330, months[k], "", 0.9, rot=3)
                fade_text(c, "for months", 1620, 520, t, tm + 0.3, "hand", 60, INK2, "c", b=S("2.8") - 0.4)
    # ---- 2.8 spell unbroken ----
    a = S("2.8") + 0.0
    with fade(c, t, a, S("2.9") - 0.15, 0.4) as v:
        if v:
            p = prog(t, a, a + 0.8)
            ink_circle(c, 640, 610, 300, 290, p, VERM, 8, seed=4, rot=0)
            for k in range(5):
                ang = k * 2 * math.pi / 5 + t * 0.3
                x_, y_ = 640 + 300 * math.cos(ang), 610 + 290 * math.sin(ang)
                if p > 0.9: sparkle(c, x_, y_, 20, t, VERM, 0.9, 4)
            stamp(c, "SPELL UNBROKEN", 1530, 330, t, a + 0.3, VERM, -5, 62, pad=(34, 20))
            fade_text(c, "knowing did not", 1560, 470, t, Wd("2.8", "Knowing") - 0.1, "hand", 70, INK2, "c")
            fade_text(c, "break it", 1560, 555, t, Wd("2.8", "break") - 0.3, "hand", 70, INK2, "c")
    # ---- 2.9 psychiatrists ----
    a, b = S("2.9") + 0.3, S("2.10") - 0.15
    with fade(c, t, a, b, 0.4, bleed=True) as v:
        if v:
            for i, (x, k) in enumerate(((300, "man"), (660, "man"), (1020, "woman"))):
                ta = a + 0.3 + i * 0.3; q = e_out(prog(t, ta, ta + 0.4))
                person2(c, x, 760, 1.0, k, glasses=(i == 0), alpha=q)
                # clipboard
                c.save(); c.translate(x + 120, 640); c.rotate(0.15)
                c.saveLayerAlpha(skia.Rect.MakeXYWH(-60, -80, 120, 160), int(255*q))
                c.drawRect(skia.Rect.MakeXYWH(-46, -64, 92, 124), P(PAPER2)); c.drawRect(skia.Rect.MakeXYWH(-46, -64, 92, 124), P(INK, "stroke", 3.4))
                c.drawRect(skia.Rect.MakeXYWH(-22, -74, 44, 18), P(INK))
                for l in range(4): c.drawLine(-32, -30 + l*22, 30 - (l % 2)*10, -30 + l*22, P(INK2, "stroke", 2.6))
                c.restore(); c.restore()
            label(c, "practicing psychiatrists", 740, 190, t, S("2.9") + Wd("2.9", "psychiatrists") - S("2.9") - 0.2 if False else Wd("2.9", "practicing"), INK, 46, "type")
            tt = Wd("2.9", "automatic")
            with slip(c, 1490, 440, 640, 330, 2.0, t, tt - 0.5, None, seed=26, slide=(160, 0)) as v2:
                if v2:
                    text(c, "AUTOMATIC", 0, -64, "mono", 56, VERM)
                    text(c, "PSYCHOTHERAPY?", 0, 8, "mono", 56, VERM)
                    text(c, "per Weizenbaum, 1976", 0, 98, "type", 36, INK2)
    # ---- 2.10 PARRY ----
    a, b = S("2.10") + 0.3, None
    with fade(c, t, a, b, 0.4, bleed=True) as v:
        if v:
            terminal(c, 420, 830, 1.15, key_t=t, paper_lines=[0.8, 0.5, 0.9, 0.6], paper_h=0.9)
            terminal(c, 1500, 830, 1.15, key_t=t + 1, paper_lines=[0.5, 0.9, 0.6, 0.8], paper_h=0.9)
            label(c, "ELIZA", 420, 300, t, a + 0.4, INK, 50, "type")
            label(c, "PARRY", 1500, 300, t, Wd("2.10", "PARRY") if False else Wd("2.10", "another") , INK, 50, "type")
            fade_text(c, "1972", 960, 190, t, a + 0.3, "type", 80, INK, "c")
            # network nodes
            nodes = [(640, 560), (800, 470), (960, 590), (1120, 480), (1290, 570)]
            for i, (x, y) in enumerate(nodes):
                q = e_out(prog(t, a + 1.0 + i * 0.25, a + 1.4 + i * 0.25))
                if q > 0:
                    c.drawCircle(x, y, 22 * q, P(PAPER2)); c.drawCircle(x, y, 22 * q, P(INK, "stroke", 4))
            pts = [(560, 620)] + nodes + [(1400, 620)]
            path = skia.Path(); path.moveTo(*pts[0])
            for p_ in pts[1:]: path.lineTo(*p_)
            draw_on(c, path, e_out(prog(t, a + 1.0, a + 2.8)), 4.5, INK2, 1.0)
            if t > a + 3.0:
                for k in range(3):
                    f = (t * 0.35 + k / 3) % 1.0
                    px, py, _ = pos_on(path, f); c.drawCircle(px, py, 10, P(VERM))
                    px, py, _ = pos_on(path, 1 - f); c.drawCircle(px, py, 10, P(INK))
            fade_text(c, "ARPANET", 960, 720, t, Wd("2.10", "ARPANET") - 0.2, "hand", 80, VERM, "c")
            fade_text(c, "a forerunner of the internet", 960, 810, t, Wd("2.10", "forerunner"), "hand", 66, INK2, "c")
            fade_text(c, "a program that imitated a patient with paranoia", 1500, 180, t, Wd("2.10", "imitated") - 0.2, "hand", 40, INK2, "c", b=Wd("2.10", "ARPANET") - 0.5) if False else None

# ===================================================================================================
def draw3(c, t):
    # ---- 3.1 Berlin 1923 / 1936 ----
    a, b = S("3.1") - 0.8, S("3.2") - 0.1
    with fade(c, t, a, b, 0.4, bleed=True) as v:
        if v:
            with slip(c, 520, 420, 640, 300, -2.2, t, a + 0.6, None, seed=31, slide=(-120, 0)) as v2:
                if v2:
                    text(c, "BERLIN", 0, -50, "serif", 100, INK); text(c, "born 1923", 0, 60, "type", 48, INK2)
            with slip(c, 1400, 420, 700, 300, 1.8, t, Wd("3.1", "His") , None, seed=32, slide=(120, 0)) as v2:
                if v2:
                    text(c, "1936", 0, -50, "serif", 100, INK); text(c, "fled Nazi Germany", 0, 62, "type", 46, INK2)
            path = bez((680, 210), (960, 90), (1250, 210))
            if t > Wd("3.1", "fled") - 0.2:
                draw_on(c, path, e_out(prog(t, Wd("3.1", "fled") - 0.2, Wd("3.1", "fled") + 1.4)), 6, INK2, 1.0, True, True, 34)
                f = e_io(prog(t, Wd("3.1", "fled") - 0.2, Wd("3.1", "fled") + 1.4))
                x_, y_, _ = pos_on(path, f); suitcase(c, x_, y_ - 50, 0.8, math.sin(f * 14) * 5)
            ta = Wd("3.1", "thirteen") - 0.3
            person2(c, 960, 860, 1.0, "man", child=True, alpha=e_out(prog(t, ta, ta + 0.5)))
            fade_text(c, "age thirteen", 1200, 790, t, ta + 0.2, "hand", 76, VERM, "c")
    # ---- 3.2 the book ----
    a, b = S("3.2") - 0.05, S("3.3") - 0.1
    with fade(c, t, a, b, 0.4) as v:
        if v:
            q = e_out(prog(t, a, a + 0.9))
            book(c, 700, 500 + 120 * (1 - q), 330, 460, ["COMPUTER", "POWER &", "HUMAN", "REASON"], 1.35, rot=-3 + 4 * (1 - q), sub="")
            stamp(c, "1976", 1180, 270, t, a + 0.8, VERM, -6, 96, pad=(34, 20))
            fade_text(c, "its argument", 1400, 470, t, Wd("3.2", "argument") - 0.1, "hand", 84, INK2, "c")
            fade_text(c, "is blunt", 1400, 580, t, Wd("3.2", "blunt") - 0.1, "hand", 110, VERM, "c")
    # ---- 3.3 some jobs ----
    a, b = S("3.3") + 0.15, S("3.4") - 0.1
    with fade(c, t, a, b, 0.4, bleed=True) as v:
        if v:
            person2(c, 420, 830, 1.15, "woman")
            machine_box(c, 1450, 830, 1.2, t)
            ta = Wd("3.3", "handed") - 0.4
            q = prog(t, ta, ta + 1.4)
            path = bez((640, 420), (950, 250), (1250, 420))
            fade_text(c, "some jobs", 430, 330, t, Wd("3.3", "jobs") - 0.5, "hand", 76, INK2, "c")
            if q > 0:
                x_, y_, _ = pos_on(path, e_io(min(q, 1)))
                heart(c, x_, y_, 1.5, VERM)
                draw_on(c, path, e_out(min(q, 1)), 5, INK2, 1.0, True, True, 30)
            tx = Wd("3.3", "never") - 0.2
            p = prog(t, tx, tx + 0.5)
            if p > 0:
                pen = P(VERM, "stroke", 16, rough=(14, 1.4)); pa_ = skia.Path(); pa_.moveTo(830, 300); pa_.lineTo(830 + 220 * p, 300 + 220 * p); c.drawPath(pa_, pen)
                pb_ = skia.Path(); pb_.moveTo(1050, 300); pb_.lineTo(1050 - 220 * p, 300 + 220 * p); c.drawPath(pb_, pen)
    # ---- 3.4 objectives quote ----
    a, b = S("3.4") + 0.5, S("3.5") - 0.15
    quote_slip(c, t, a, b, 960, 440, 1560, 380,
               "…there are objectives that are not appropriately assignable to machines.",
               "J. Weizenbaum, Computer Power and Human Reason (1976), p. 210", 58, rot=0.8,
               hl=["not appropriately assignable"], hl_t=Wd("3.4", "not appropriately") - 0.1, seed=33)
    # ---- 3.5 deciding vs choosing ----
    a, b = S("3.5") + 0.3, S("3.6") - 0.15
    with fade(c, t, a, b, 0.4, bleed=True) as v:
        if v:
            line(c, 960, 200, 960, 840, 5, INK2, 0.8)
            fade_text(c, "DECIDING", 520, 210, t, Wd("3.5", "deciding") - 0.2, "sc", 84, INK, "c")
            gear(c, 520, 470, 120, t * 0.6, INK)
            gear(c, 650, 370, 70, -t * 1.0 + 0.2, INK, teeth=8)
            fade_text(c, "computation", 520, 700, t, Wd("3.5", "computation") - 0.2, "hand", 76, INK2, "c")
            fade_text(c, "a computer can do it", 520, 800, t, Wd("3.5", "computer can") - 0.2, "hand", 64, INK2, "c")
            tc_ = Wd("3.5", "Choosing") - 0.2
            fade_text(c, "CHOOSING", 1400, 210, t, tc_, "sc", 84, INK, "c")
            scales(c, 1400, 440, 1.5, 0.12 * math.sin(t * 1.5), INK, e_out(prog(t, tc_, tc_ + 0.5)))
            fade_text(c, "judgment", 1400, 700, t, Wd("3.5", "judgment") - 0.1, "hand", 80, VERM, "c")
            fade_text(c, "is not calculation", 1400, 800, t, Wd("3.5", "not calculation") - 0.2, "hand", 66, INK2, "c")
    # ---- 3.6 Eliza Doolittle ----
    a, b = S("3.6") + 0.3, S("3.7") - 0.15
    with fade(c, t, a, b, 0.4, bleed=True) as v:
        if v:
            person2(c, 560, 830, 1.2, "woman")
            basket(c, 790, 790, 1.4)
            label(c, "ELIZA DOOLITTLE", 640, 190, t, Wd("3.6", "Doolittle") - 0.4, INK, 50, "type")
            with slip(c, 1400, 470, 640, 420, 2.5, t, Wd("3.6", "Pygmalion") - 0.3, None, seed=36, slide=(140, 0)) as v2:
                if v2:
                    text(c, "PYGMALION", 0, -80, "serif", 90, INK); text(c, "a play", 0, 10, "hand", 64, INK2)
                    c.drawLine(-200, -30, 200, -30, P(INK2, "stroke", 3))
            fade_text(c, "taught to speak like a lady", 1400, 780, t, Wd("3.6", "taught") - 0.2, "hand", 66, VERM, "c")
    # ---- 3.7 civilized quote ----
    a, b = S("3.7") + 0.25, S("3.8") - 0.15
    quote_slip(c, t, a, b, 960, 450, 1640, 520,
               "Like the Eliza of Pygmalion fame, it can be made to appear even more civilized, the relation of appearance to reality, however, remaining in the domain of the playwright.",
               "J. Weizenbaum, CACM, January 1966", 48, rot=-0.7,
               hl=["civilized", "appearance to reality", "playwright."], hl_times=[Wd("3.7", "civilized") - 0.2, Wd("3.7", "appearance") - 0.2, Wd("3.7", "playwright") - 0.3], seed=37, scan=(S("3.7") + 0.6, E("3.7")))
    # ---- 3.8 theater ----
    a = S("3.8") + 0.15
    with fade(c, t, a, None, 0.5, bleed=True) as v:
        if v:
            # stage floor + terminal behind the curtain
            c.drawRect(skia.Rect.MakeXYWH(510, 170, 900, 620), P(PAPER3)); ink(c, rect_path(510, 170, 900, 620), 5)
            c.drawRect(skia.Rect.MakeXYWH(510, 760, 900, 40), P(INK2, alpha=0.85)); ink(c, rect_path(510, 760, 900, 40), 4)
            terminal(c, 960, 750, 1.0, key_t=t, paper_lines=[0.8, 0.5, 0.9], paper_h=0.7)
            curtain(c, 960, 480, 900, 620, e_out(prog(t, a + 0.2, a + 1.6)), back=False)
            stamp(c, "THEATER", 960, 880 if False else 850, t, a + 1.3, VERM, -3, 70, pad=(34, 18))

REG = {2: (CAM, draw2), 3: (CAM, draw3)}
