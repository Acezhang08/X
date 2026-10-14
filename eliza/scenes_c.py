# -*- coding: utf-8 -*-
"""Segments 4-6: the code is found, then today: Turing test, chatbots, surveys, laws, and the question."""
import math, random
import skia
from lib import *
from props import *
from lib import fx_ring
from scenes_a import T, S, E, Wd, CAM, quote_slip, tile, desk, crowd
from scenes_b import suitcase, machine_box

def folder2(c, cx, cy, w, h, t=0.0, open_p=0.0, tab="COMPUTER CONVERSATIONS (1965)"):
    c.save(); c.translate(cx, cy)
    c.save(); c.translate(8, 12); c.drawRect(skia.Rect.MakeXYWH(-w/2, -h/2, w, h), P(0x2A1D10, alpha=0.28, blur=9)); c.restore()
    tabw = w * 0.62
    back = skia.Path(); back.moveTo(-w/2, -h/2 + 56); back.lineTo(-w/2 + 30, -h/2); back.lineTo(-w/2 + tabw, -h/2); back.lineTo(-w/2 + tabw + 40, -h/2 + 56); back.lineTo(w/2, -h/2 + 56)
    back.lineTo(w/2, h/2); back.lineTo(-w/2, h/2); back.close()
    c.drawPath(back, P(0xFFD9BF86)); ink(c, back, 4.5)
    if tab: text(c, tab, -w/2 + tabw/2 + 6, -h/2 + 28, "type", 36, INK, "c")
    c.restore()

def printout(c, x, y, w=420, h=300, rot=0.0, lines=9, alpha=1.0):
    c.save(); c.translate(x, y); c.rotate(rot)
    if alpha < 1: c.saveLayerAlpha(skia.Rect.MakeXYWH(-w/2-30, -h/2-30, w+60, h+60), int(255*alpha))
    c.drawRect(skia.Rect.MakeXYWH(-w/2, -h/2, w, h), P(PAPER2)); ink(c, rect_path(-w/2, -h/2, w, h), 3.4)
    for sx in (-w/2 + 16, w/2 - 16):
        for k in range(int(h // 30)): c.drawCircle(sx, -h/2 + 16 + k*30, 4, P(INK2))
    for i in range(lines):
        ln = w - 90 - ((i * 37) % 120)
        c.drawLine(-w/2 + 40, -h/2 + 30 + i * (h - 50) / lines, -w/2 + 40 + ln, -h/2 + 30 + i * (h - 50) / lines, P(INK2, "stroke", 3.2, 0.8))
    if alpha < 1: c.restore()
    c.restore()

# ===================================================================================================
def draw4(c, t):
    # ---- 4.1 method published, program not ----
    a, b = S("4.1") - 0.8, S("4.2") - 0.1
    with fade(c, t, a, b, 0.4, bleed=True) as v:
        if v:
            with slip(c, 620, 470, 960, 600, -1.2, t, a + 0.4, None, seed=41, slide=(-160, 0)) as v2:
                if v2:
                    text(c, "ELIZA — A Computer Program", 0, -170, "serif", 54, INK)
                    text(c, "For the Study of Natural Language", 0, -100, "serif", 54, INK)
                    text(c, "Communication Between Man", 0, -30, "serif", 54, INK)
                    text(c, "and Machine", 0, 40, "serif", 54, INK)
                    c.drawLine(-380, 100, 380, 100, P(INK2, "stroke", 2.5))
                    text(c, "J. Weizenbaum · CACM · January 1966", 0, 160, "type", 38, INK2)
                    stamp(c, "THE METHOD", 230, 235, t, a + 1.9, VERM, -4, 46, pad=(24, 12))
            tp = Wd("4.1", "never") - 0.3
            with slip(c, 1480, 470, 560, 520, 2.2, t, tp, None, seed=42, slide=(160, 0), fill=PAPER) as v2:
                if v2:
                    rr = rect_path(-240, -220, 480, 440, 6); c.drawPath(rr, P(INK, "stroke", 4, dash=[18, 12]))
                    text(c, "?", 0, -20, "type", 240, VERM)
                    stamp(c, "THE CODE", 0, 170, t, tp + 0.7, VERM, -3, 46, pad=(24, 12))
    # ---- 4.2 more than fifty years ----
    a, b = S("4.2") + 0.2, S("4.3") - 0.1
    with fade(c, t, a, b, 0.4) as v:
        if v:
            path = skia.Path(); path.moveTo(250, 520); path.lineTo(1670, 520)
            draw_on(c, path, e_out(prog(t, a, a + 2.6)), 7, INK, 1.0, True, True, 40)
            for i in range(12):
                x = 250 + i * 118
                if t > a + 0.2 + i * 0.2: c.drawLine(x, 500, x, 540, P(INK, "stroke", 4))
            fade_text(c, "1966", 250, 440, t, a + 0.2, "type", 80, INK, "c")
            fade_text(c, "2021", 1590, 440, t, a + 2.2, "type", 80, INK, "c")
            q = prog(t, a + 1.0, a + 3.0)
            if q > 0:
                br = skia.Path(); br.moveTo(250, 600); br.lineTo(250, 630); br.lineTo(250 + 1340 * e_out(q), 630); br.lineTo(250 + 1340 * e_out(q), 600)
                c.drawPath(br, P(VERM, "stroke", 7, rough=(14, 1.2)))
            fade_text(c, "55 years", 920, 730, t, Wd("4.2", "fifty") - 0.1, "hand", 130, VERM, "c")
    # ---- 4.3 / 4.4 found in a folder ----
    a, b = S("4.3") + 0.15, S("4.5") - 0.1
    with fade(c, t, a, b, 0.4, bleed=True) as v:
        if v:
            fx, fy = 1220, 520
            folder2(c, fx, fy, 1020, 520, t, tab="COMPUTER CONVERSATIONS (1965)" if t > S("4.4") - 0.2 else "")
            q = e_io(prog(t, Wd("4.3", "printout") - 0.6, Wd("4.3", "printout") + 0.8))
            printout(c, fx + 350, lerp(fy + 40, fy - 120, q), 400, 340, 3 * q, 10, 1.0) if q > 0 else None
            # re-draw the folder front over the printout bottom
            c.save(); c.clipRect(skia.Rect.MakeXYWH(fx - 520, fy + 40, 1040, 300))
            c.drawRect(skia.Rect.MakeXYWH(fx - 510, fy - 260 + 56, 1020, 470), P(0xFFD9BF86)); ink(c, rect_path(fx - 510, fy - 260 + 56, 1020, 470), 4.5)
            c.restore()
            person2(c, 250, 840, 0.9, "man", alpha=e_out(prog(t, a + 0.3, a + 0.8)))
            person2(c, 520, 840, 0.9, "woman", alpha=e_out(prog(t, a + 0.6, a + 1.1)))
            fade_text(c, "Jeff Shrager", 300, 210, t, Wd("4.3", "Jeff"), "type", 40, INK, "c") if False else None
            label(c, "Jeff Shrager", 250, 540, t, Wd("4.3", "Jeff"), INK, 40, "type")
            label(c, "MIT archivist", 520, 600, t, Wd("4.3", "archivist"), INK, 40, "type")
            stamp(c, "2021", 1500, 170, t, Wd("4.3", "2021"), VERM, 5, 90, pad=(34, 18))
            if t > S("4.4") + 0.8:
                ink_circle(c, fx - 190, fy - 232, 360, 50, prog(t, S("4.4") + 0.8, S("4.4") + 1.6), VERM, 7, seed=3, rot=0)
    # ---- 4.5 ran again ----
    a, b = S("4.5") + 0.2, S("4.6") - 0.15
    with fade(c, t, a, b, 0.4, bleed=True) as v:
        if v:
            mainframe(c, 540, 850, 1.3, t=t)
            c.save(); c.translate(540, 850); c.scale(1.3, 1.3)
            for (x0, w_, h_) in ((-355, 210, 300), (-125, 250, 330), (105, 210, 300)):
                pass
            c.restore()
            terminal(c, 1400, 850, 1.3, key_t=t, paper_lines=[0.8, 0.6, 0.9, 0.5, 0.7, 0.4], paper_h=0.9)
            fade_text(c, "rebuilt 1960s system", 540, 330, t, Wd("4.5", "rebuilt") - 0.2, "type", 46, INK, "c")
            stamp(c, "2025", 1400, 250, t, Wd("4.5", "2025") - 0.1 if False else S("4.5") + 0.3, VERM, -5, 96, pad=(36, 20))
            fade_text(c, "the code runs again", 960, 160, t, Wd("4.5", "ran that code") - 0.2, "hand", 76, INK2, "c")
    # ---- 4.6 / 4.7 ELIZA effect ----
    a, b = S("4.6") + 0.2, S("4.8") - 0.2
    with fade(c, t, a, b, 0.4, bleed=True) as v:
        if v:
            fade_text(c, "THE ELIZA EFFECT", 960, 300, t, a + 0.1, "serif", 160, INK, "c", dur=0.8, rise=0)
            underline(c, 230, 1690, 400, prog(t, a + 0.8, a + 1.6), VERM, 8)
            tdef = S("4.7") + 0.2
            with slip(c, 960, 640, 1380, 300, 0.8, t, tdef, None, seed=44, slide=(0, 120)) as v2:
                if v2:
                    text(c, "reading far more understanding into", 0, -52, "serifi", 62, INK)
                    text(c, "a computer's words than is really there", 0, 36, "serifi", 62, INK)
                    underline(c, -560, 560, 76, prog(t, tdef + 1.5, tdef + 2.3), VERM, 6)
    # ---- 4.8 Hofstadter ----
    a = S("4.8") + 0.2
    with fade(c, t, a, None, 0.5, bleed=True) as v:
        if v:
            q = e_out(prog(t, a, a + 0.8))
            book(c, 380, 520 + 100 * (1 - q), 330, 470, ["FLUID", "CONCEPTS", "& CREATIVE", "ANALOGIES"], 1.15, rot=-4, sub="1995")
            with slip(c, 1170, 440, 1100, 360, 1.2, t, S("4.8") + 1.6, None, seed=48, slide=(140, 0)) as v2:
                if v2:
                    text(c, "The Ineradicable", 0, -92, "serif", 76, INK)
                    text(c, "ELIZA Effect and Its Dangers", 0, -8, "serif", 76, INK)
                    c.drawLine(-440, 50, 440, 50, P(INK2, "stroke", 2.5))
                    text(c, "chapter title · Douglas Hofstadter · 1995", 0, 110, "type", 38, INK2)
            fade_text(c, "still fits", 1170, 790, t, Wd("4.8", "still fits"), "hand", 110, VERM, "c")

# ===================================================================================================
def chat_window_lines(c, t, cx, cy, w, h, a, n=4, title="", seed=0, who_left=True):
    window(c, cx, cy, w, h, title)
    r = random.Random(seed)
    for i in range(n):
        ta = a + i * 0.9
        q = e_out(prog(t, ta, ta + 0.6))
        if q <= 0: continue
        left = (i % 2 == 0) == who_left
        bw = r.uniform(0.35, 0.6) * (w - 100)
        yy = cy - h/2 + 110 + i * (h - 170) / max(1, n)
        xx = cx - w/2 + 36 if left else cx + w/2 - 36 - bw
        rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(xx, yy - 26, bw * q, 54), 20, 20)
        c.drawRRect(rr, P(PAPER if left else PAPER3)); c.drawRRect(rr, P(INK, "stroke", 3.2))
        for k in range(2): c.drawLine(xx + 20, yy - 6 + k * 18, xx + 20 + (bw - 50) * q * (1 - 0.3 * k), yy - 6 + k * 18, P(INK2, "stroke", 3))

def draw5(c, t):
    # ---- 5.1 today ----
    a, b = S("5.1") - 0.8, S("5.2") - 0.1
    with fade(c, t, a, b, 0.4, bleed=True) as v:
        if v:
            fade_text(c, "TODAY", 960, 190, t, a + 0.1, "serif", 170, INK, "c", dur=0.6, rise=0)
            window(c, 960, 590, 1000, 520, "")
            for i in range(3):
                if int(t * 2.2) % 4 > i: c.drawCircle(900 + i * 60, 600, 14, P(INK))
    # ---- 5.2 Turing test setup ----
    a, b = S("5.2") + 0.3, S("5.3") - 0.2
    with fade(c, t, a, b, 0.4, bleed=True) as v:
        if v:
            fade_text(c, "UC San Diego · 2025", 960, 135, t, a + 0.1, "type", 50, INK, "c")
            chat_window_lines(c, t, 480, 480, 700, 520, a + 1.2, 4, "", 1, True)
            chat_window_lines(c, t, 1440, 480, 700, 520, a + 1.7, 4, "", 2, False)
            label(c, "A", 480, 200 + 80 if False else 250, t, a + 0.6, INK, 56, "serif") if False else None
            fade_text(c, "A", 480, 175, t, a + 0.6, "serif", 90, INK, "c")
            fade_text(c, "B", 1440, 175, t, a + 0.6, "serif", 90, INK, "c")
            person2(c, 960, 880, 0.8, "man", glasses=True, alpha=e_out(prog(t, a + 0.5, a + 1.0)))
            fade_text(c, "judge", 960, 820 - 0 if False else 590, t, a + 0.9, "hand", 70, INK2, "c")
            tw_ = Wd("5.2", "five-minute")
            fade_text(c, "5 min", 960, 335, t, tw_ - 0.2, "hand", 66, INK2, "c")
            clock(c, 960, 440, 70 * e_out(prog(t, tw_, tw_ + 0.5)), ((t - tw_) * 0.12) % 1.0, INK, 1.0)
            tq = Wd("5.2", "picked")
            if t > tq - 0.1:
                al = e_out(prog(t, tq - 0.1, tq + 0.4))
                text(c, "which one is human?", 1420, 830, "hand", 72, VERM, alpha=al)
    # ---- 5.3 - 5.5 bar chart ----
    a, b = S("5.3") + 0.2, S("5.6") - 0.15
    with fade(c, t, a, b, 0.4, bleed=True) as v:
        if v:
            base = 720; sc = 5.0   # px per percent
            line(c, 260, base, 1660, base, 6, INK)
            fade_text(c, "judged to be the human", 960, 150, t, a + 0.1, "hand", 80, INK2, "c")
            # chance line
            q = prog(t, a + 0.3, a + 1.2)
            if q > 0:
                yy = base - 50 * sc
                c.drawLine(260, yy, 260 + 1400 * q, yy, P(INK2, "stroke", 3.5, dash=[16, 12]))
                fade_text(c, "chance: 50%", 1710, yy + 32, t, a + 1.0, "type", 36, INK2, "c")
            bars = [
                (520, 73, "GPT-4.5", "told to play a persona", Wd("5.3", "best AI"), Wd("5.3", "best AI") - 0.2, INK2, False),
                (960, 23, "ELIZA", "the 1960s program", Wd("5.4", "ELIZA"), Wd("5.4", "ELIZA") - 0.2, VERM, True),
                (1400, 21, "GPT-4o", "no persona", Wd("5.4", "GPT-4o"), Wd("5.4", "GPT-4o") - 0.2, INK2, False),
            ]
            for x, val, nm, sub, tn, tv, col, hot in bars:
                tend = {73: Wd("5.3", "73") + 0.6, 23: Wd("5.4", "23") + 0.5, 21: Wd("5.4", "got 21") + 0.6}[val]
                p = e_io(prog(t, tv, tend))
                h = val * sc * p
                if h > 1:
                    r_ = skia.Rect.MakeXYWH(x - 130, base - h, 260, h)
                    c.drawRect(r_, P(col, alpha=0.88 if hot else 0.34)); ink(c, rect_path(x - 130, base - h, 260, h), 4.5)
                    if not hot: hatch(c, rect_path(x - 130, base - h, 260, h), -45, 16, 2.4, INK, 0.5)
                    text(c, f"{round(val * p)}%", x, base - h - 52, "type", 96, VERM if hot else INK)
                fade_text(c, nm, x, base + 52, t, tn - 0.1, "serif", 60, INK, "c")
                fade_text(c, sub, x, base + 106, t, tn + 0.1, "hand", 52, INK2, "c")
            # 5.5 callouts
            tq = Wd("5.5", "how the chat")
            qb = prog(t, S("5.5") + 0.3, S("5.5") + 1.1)
            if qb > 0:
                pb = skia.Path(); pb.moveTo(830, 520); pb.lineTo(830, 495); pb.lineTo(1530, 495); pb.lineTo(1530, 520)
                seg_, _, _ = partial(pb, 0, qb); c.drawPath(seg_, P(VERM, "stroke", 6, rough=(14, 1.2)))
                fade_text(c, "23 vs 21", 1180, 425, t, S("5.5") + 0.9, "hand", 64, VERM, "c")
            fade_text(c, "not only intelligence", 960, 240, t, Wd("5.5", "never") - 0.1, "hand", 82, VERM, "c")
            fade_text(c, "how the chat is set up", 1010, 345, t, tq - 0.2, "hand", 58, INK2, "c")
            fade_text(c, "who is judging", 1500, 345, t, Wd("5.5", "who is") - 0.2, "hand", 58, INK2, "c")
            fade_text(c, "Jones & Bergen · UC San Diego · 2025", 960, 892, t, a + 1.0, "type", 36, INK2, "c")
    # ---- 5.6 echo vs flatter ----
    a, b = S("5.6") + 0.15, S("5.7") - 0.15
    with fade(c, t, a, b, 0.4, bleed=True) as v:
        if v:
            # mirror
            c.save(); c.translate(500, 460)
            c.drawOval(skia.Rect.MakeXYWH(-130, -190, 260, 340), P(PAPER2)); ink(c, skia.Path().addOval(skia.Rect.MakeXYWH(-130, -190, 260, 340)), 6)
            c.drawLine(0, 150, 0, 260, P(INK, "stroke", 14)); c.drawLine(-60, 262, 60, 262, P(INK, "stroke", 10))
            for k in range(3): c.drawLine(-60 + k*20, -110 + k*10, 20 + k*20, -150 + k*10, P(WASH, "stroke", 5, 0.6))
            c.restore()
            fade_text(c, "echo", 500, 790, t, Wd("5.6", "echo") - 0.1, "hand", 130, INK, "c")
            tf = Wd("5.6", "flatter")
            for k in range(7):
                ang = k * 2 * math.pi / 7 + t * 0.4
                x_, y_ = 1380 + 250 * math.cos(ang) * 0.9, 440 + 190 * math.sin(ang)
                if t > tf: sparkle(c, x_, y_, 26 + 8 * math.sin(t * 3 + k), t * 0.6 + k, VERM, e_out(prog(t, tf, tf + 0.5)), 5)
            person2(c, 1380, 560, 0.95, "woman", alpha=e_out(prog(t, tf - 0.2, tf + 0.3)))
            if t > tf: heart(c, 1380, 230, 1.6 * e_out(prog(t, tf, tf + 0.4)), VERM, 1.0)
            fade_text(c, "flatter", 1380, 790, t, tf - 0.1, "hand", 130, VERM, "c")
    # ---- 5.7 April 2025 rollback ----
    a, b = S("5.7") + 0.2, S("5.8") - 0.15
    with fade(c, t, a, b, 0.4, bleed=True) as v:
        if v:
            q = e_out(prog(t, a, a + 0.6))
            calendar_page(c, 430, 430 + 80 * (1 - q), "APRIL", 2025, 1.4, rot=-3)
            stamp(c, "ROLLED BACK", 430, 770, t, Wd("5.7", "rolled") + 0.2, VERM, -5, 62, pad=(30, 18))
            quote_slip(c, t, Wd("5.7", "overly") - 0.4, None, 1240, 440, 1100, 430,
                       "…overly flattering or agreeable – often described as sycophantic.",
                       "OpenAI, April 29, 2025", 56, rot=1.0, hl=["overly flattering or agreeable"], hl_t=Wd("5.7", "overly") + 0.3, seed=57)
    # ---- 5.8 August 2025 4o retired ----
    a, b = S("5.8") + 0.15, S("5.8b") - 0.15
    with fade(c, t, a, b, 0.4, bleed=True) as v:
        if v:
            calendar_page(c, 430, 400, "AUGUST", 2025, 1.4, rot=3)
            ta = Wd("5.8", "retired")
            tile(c, 1280, 360, "GPT-4o", "mono", 84, INK, w=480, rot=-2)
            stamp(c, "RETIRED", 1380, 500, t, ta, VERM, -6, 80, pad=(34, 20))
            tl = Wd("5.8", "losing")
            person2(c, 640 if False else 1040, 840, 0.8, "man", flip=True, alpha=e_out(prog(t, tl - 0.4, tl + 0.2)))
            if t > tl - 0.1:
                al = e_out(prog(t, tl - 0.1, tl + 0.3))
                heart(c, 1040, 560, 1.7, VERM, al)
                pa = prog(t, tl + 0.3, tl + 0.8)
                if pa > 0: c.drawPath(partial(poly_path([(1020, 520), (1048, 548), (1028, 572), (1052, 600)], False), 0, pa)[0], P(INK, "stroke", 6, rough=(10, 1)))
            tb_ = Wd("5.8", "brought")
            stamp(c, "BACK AS AN OPTION", 1480, 700, t, tb_, INK, 3, 58, pad=(30, 16))
    # ---- 5.8b 800 million ----
    a, b = S("5.8b") + 0.15, S("5.9") - 0.15
    with fade(c, t, a, b, 0.4, bleed=True) as v:
        if v:
            crowd(c, t, a, 18, 6, 130, 250, 96, 96, 1.0, 3, 2.0, INK2, fadeout=None)
            with slip(c, 960, 520, 1180, 360, -0.8, t, a + 0.4, None, seed=58, slide=(0, 110)) as v2:
                if v2:
                    n = 800 * e_out(prog(t, a + 0.7, a + 2.2))
                    text(c, f"{int(n)} million+", 0, -50, "type", 140, VERM)
                    text(c, "ChatGPT weekly users · Oct. 2025", 0, 90, "type", 44, INK)
    # ---- 5.9 Pew ----
    a, b = S("5.9") + 0.25, S("5.10") + 0.1
    with fade(c, t, a, b, 0.4, bleed=True) as v:
        if v:
            fade_text(c, "emotional support or advice", 960, 150, t, a + 0.1, "serif", 70, INK, "c")
            for i in range(10):
                ta = Wd("5.9", "one in ten") - 0.9 + i * 0.07
                q = e_out(prog(t, ta, ta + 0.3))
                small_person(c, 360 + i * 130, 480, 2.6 * (0.6 + 0.4 * q), VERM if i == 0 else INK, q)
            fx_ring(c, 360, 450, ((t - S("5.9")) * 0.6) % 1.0, 30, 95, VERM, 6) if t > Wd("5.9", "one in ten") else None
            if t > Wd("5.9", "aged 18") + 0.8: fx_ring(c, 560, 750, ((t - S("5.9")) * 0.6) % 1.0, 30, 95, VERM, 6)
            fade_text(c, "1 in 10 U.S. adults", 960, 560, t, Wd("5.9", "one in ten") - 0.4, "hand", 84, INK, "c")
            for i in range(5):
                ta = Wd("5.9", "aged 18") + i * 0.1 - 0.2
                q = e_out(prog(t, ta, ta + 0.3))
                small_person(c, 560 + i * 200, 780, 2.6 * (0.6 + 0.4 * q), VERM if i == 0 else INK, q)
            fade_text(c, "1 in 5 adults aged 18 to 29", 960, 850, t, Wd("5.9", "one in five") - 0.3, "hand", 70, VERM, "c")
            fade_text(c, "Pew Research Center · Feb. 2026", 960, 892, t, a + 0.6, "type", 36, INK2, "c") if False else None
    # ---- 5.10 teens ----
    a, b = S("5.10") + 0.05, S("5.11") - 0.15
    with fade(c, t, a, b, 0.4, bleed=True) as v:
        if v:
            t72 = Wd("5.10", "72"); t52 = Wd("5.10", "52")
            for k in range(100):
                i, j = k % 10, k // 10
                ta = a + 0.2 + k * 0.012
                q = e_out(prog(t, ta, ta + 0.3))
                if q <= 0: continue
                f72 = k < 72 and t > t72 - 0.2
                f52 = k < 52 and t > t52 - 0.2
                col = VERM if f52 else (INK if f72 else LINEL)
                small_person(c, 220 + i * 62, 200 + j * 62 + 30, 1.45 * q, col, q, fill=(f72 or f52))
            fade_text(c, "72%", 1290, 330, t, t72 - 0.1, "type", 180, INK, "c")
            fade_text(c, "of U.S. teens tried an AI companion", 1290, 450, t, t72, "hand", 58, INK2, "c") if False else None
            fade_text(c, "tried one", 1290, 460, t, t72, "hand", 76, INK2, "c")
            fade_text(c, "52%", 1290, 620, t, t52 - 0.1, "type", 180, VERM, "c")
            fade_text(c, "a few times a month+", 1290, 750, t, t52, "hand", 76, VERM, "c")
            fade_text(c, "Common Sense Media · 2025", 960, 892, t, a + 0.6, "type", 36, INK2, "c")
    # ---- 5.11 she is a survey result ----
    a, b = S("5.11") + 0.25, S("5.12") - 0.15
    with fade(c, t, a, b, 0.4, bleed=True) as v:
        if v:
            person2(c, 480, 830, 1.35, "woman")
            fade_text(c, "1966", 480, 190, t, a + 0.3, "type", 90, INK, "c")
            ts = Wd("5.11", "survey")
            for k in range(30):
                i, j = k % 10, k // 10
                x_, y_ = 880 + i * 92, 450 + j * 120
                ta = a + 0.4 + k * 0.03
                q = e_out(prog(t, ta, ta + 0.3))
                small_person(c, x_, y_, 2.0 * q, VERM if k == 14 else INK, q)
            ink_circle(c, 880 + 4 * 92, 450 + 120 - 40, 80, 110, prog(t, ts - 0.2, ts + 0.6), VERM, 7, seed=7)
            stamp(c, "A SURVEY RESULT", 1300, 205, t, ts, VERM, -3, 70, pad=(34, 18))
    # ---- 5.12 Illinois ----
    a, b = S("5.12") + 0.25, S("5.13") - 0.15
    with fade(c, t, a, b, 0.4, bleed=True) as v:
        if v:
            with slip(c, 700, 500, 1100, 600, -1.2, t, a + 0.1, None, seed=60, slide=(-140, 0)) as v2:
                if v2:
                    text(c, "ILLINOIS", 0, -210, "serif", 100, INK)
                    text(c, "Wellness and Oversight for", 0, -122, "serif", 54, INK)
                    text(c, "Psychological Resources Act", 0, -50, "serif", 54, INK)
                    c.drawLine(-440, 5, 440, 5, P(INK2, "stroke", 2.5))
                    for k in range(4): c.drawLine(-440, 60 + k*44, 440 - (k % 2)*120, 60 + k*44, P(LINEL, "stroke", 3))
                    text(c, "AUGUST 2025", 0, 250, "type", 44, INK2)
            stamp(c, "FIRST STATE", 1560, 300, t, Wd("5.12", "first") - 0.1, VERM, 4, 66, pad=(30, 18))
            fade_text(c, "no AI therapy", 1560, 470, t, Wd("5.12", "bar") , "hand", 90, INK, "c")
            fade_text(c, "without a licensed", 1560, 560, t, Wd("5.12", "without"), "hand", 70, INK2, "c")
            fade_text(c, "professional involved", 1560, 640, t, Wd("5.12", "professional") - 0.3, "hand", 70, INK2, "c")
            fade_text(c, "fines up to $10,000", 1560, 790, t, Wd("5.12", "fines"), "hand", 82, VERM, "c")
    # ---- 5.13 FTC ----
    a, b = S("5.13") + 0.25, S("5.14") - 0.15
    with fade(c, t, a, b, 0.4, bleed=True) as v:
        if v:
            label(c, "FEDERAL TRADE COMMISSION · SEPT. 2025", 960, 170, t, a + 0.1, INK, 46, "type")
            names = ["Alphabet", "Character.AI", "Instagram", "Meta", "OpenAI", "Snap", "xAI"]
            pos = [(380, 380), (960, 380), (1540, 380), (380, 540), (960, 540), (1540, 540), (960, 700)]
            for i, (nm, (x, y)) in enumerate(zip(names, pos)):
                ta = S("5.13") + 0.9 + i * 0.7
                q = e_back(prog(t, ta, ta + 0.4))
                if q > 0:
                    c.save(); c.translate(x, y); c.scale(q, q)
                    hot = nm in ("OpenAI", "Meta", "Character.AI") and t > Wd("5.13", nm if nm != "Character.AI" else "Character") - 0.1
                    tile(c, 0, 0, nm, "type", 54, VERM if hot else INK, w=470, ring=VERM if hot else None)
                    c.restore()
            fade_text(c, "how companion chatbots affect children and teens", 960, 830, t, Wd("5.13", "explain"), "hand", 62, VERM, "c")
    # ---- 5.14 human in charge ----
    a, b = S("5.14") + 0.25, None
    with fade(c, t, a, b, 0.4, bleed=True) as v:
        if v:
            person2(c, 620, 830, 1.45, "man", glasses=True)
            machine_box(c, 1380, 830, 1.2, t)
            path = bez((780, 520), (1000, 420), (1200, 560))
            draw_on(c, path, e_out(prog(t, a + 0.8, a + 1.8)), 7, INK, 1.0, True, True, 34)
            stamp(c, "A HUMAN IN CHARGE", 960, 230, t, Wd("5.14", "human in charge") - 0.1, VERM, -3, 78, pad=(36, 20))
            fade_text(c, "of the human parts", 960, 360, t, Wd("5.14", "human parts") - 0.1, "hand", 90, INK2, "c")

# ===================================================================================================
def draw6(c, t):
    # ---- 6.1 ----
    a, b = S("6.1") - 0.8, S("6.2") - 0.15
    with fade(c, t, a, b, 0.4, bleed=True) as v:
        if v:
            person2(c, 960, 770, 1.5, "man", glasses=True)
            with slip(c, 960, 825, 520, 110, 0, t, a + 0.5, None, seed=61, slide=(0, 80), tape=False) as v2:
                if v2: text(c, "1923 – 2008", 0, 0, "type", 62, INK)
            fade_text(c, "Joseph Weizenbaum", 960, 150, t, a + 0.2, "serif", 96, INK, "c")
    # ---- 6.2 warning quote ----
    a, b = S("6.2") + 0.25, S("6.3") - 0.15
    quote_slip(c, t, a, b, 960, 470, 1640, 560,
               "…how easy it is to create and maintain the illusion of understanding… A certain danger lurks there.",
               "J. Weizenbaum, CACM, January 1966", 62, rot=-0.6,
               hl=["illusion of understanding", "A certain danger lurks there."], hl_t=Wd("6.2", "takes") - 0.3, seed=62)
    # ---- 6.3 fewer than 70 and a typewriter ----
    a, b = S("6.3") + 0.25, S("6.4") - 0.15
    with fade(c, t, a, b, 0.4, bleed=True) as v:
        if v:
            terminal(c, 520, 850, 1.45, key_t=t, paper_lines=[0.8, 0.6, 0.9, 0.5, 0.7], paper_h=0.9)
            fade_text(c, "1966", 520, 190, t, a + 0.2, "type", 100, INK, "c")
            fade_text(c, "< 70", 1330, 440, t, Wd("6.3", "70") - 0.2, "type", 260, VERM, "c", dur=0.5, rise=0)
            fade_text(c, "entries", 1330, 620, t, Wd("6.3", "entries"), "hand", 100, INK2, "c")
            fade_text(c, "+ a typewriter", 1330, 740, t, Wd("6.3", "typewriter") - 0.2, "hand", 90, INK2, "c")
    # ---- 6.4 / 6.5 question ----
    a = S("6.4") + 0.2
    with fade(c, t, a, None, 0.5, bleed=True) as v:
        if v:
            window(c, 960, 430, 1560, 640, "you")
            q1 = "Have you ever told a chatbot"
            q2 = "something you would not tell a person?"
            n1, _ = typed(c, q1, 260, 330, t, a + 0.3, 20, "type", 66, INK, "l", True, VERM)
            n2, _ = typed(c, q2, 260, 430, t, a + 0.3 + len(q1) / 20 + 0.2, 20, "type", 66, INK, "l", True, VERM)
            ta = S("6.5") + 0.1
            fade_text(c, "easier because it was a machine,", 960, 580, t, ta, "hand", 84, VERM, "c")
            fade_text(c, "or in spite of it?", 960, 670, t, Wd("6.5", "or in spite"), "hand", 84, VERM, "c")
            tc = Wd("6.5", "Tell me")
            fade_text(c, "tell me in the comments", 960, 850, t, tc, "serif", 74, INK, "c")
            ar = bez((1500, 800), (1560, 850), (1500, 900))
            if t > tc: draw_on(c, bez((1560, 790), (1600, 830), (1560, 890)), e_out(prog(t, tc, tc + 0.6)), 6, VERM, 1.0, True, True, 30)

REG = {4: (CAM, draw4), 5: (CAM, draw5), 6: (CAM, draw6)}
