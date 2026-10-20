# -*- coding: utf-8 -*-
"""Segments 0-1: the quiz numbers, and how a diffusion model turns noise into a picture."""
import math, random
import skia
from lib import *
from scene_util import *

REG = {}
def reg(k):
    def deco(fn): REG[k] = fn; return fn
    return deco

def illus(c, alpha=1.0):
    text(c, "illustrative", 1800, 880, "mono", 36, GREY, "r", alpha, tag="illus")

# ===================================================================================================
@reg(0)
def seg0(c, t):
    # A: 20 tiles, 10 real and 10 AI, all shown as "?" (the quiz)
    tiles = win(t, .2, S("0.6") - .2, .4, .4)
    if tiles > 0:
        text(c, "10 REAL  ·  10 AI", 480, 252, "mono", 40, LINE, "c", ap(t, .8, .5) * tiles)
        for k in range(20):
            r_, co = divmod(k, 5)
            x = 140 + co * 140; y = 300 + r_ * 140
            p = ap(t, .4 + k * .07, .4)
            rect(c, x, y, 120, 120, 1, 2.5, LINE, alpha=p * tiles, fill=PANEL, falpha=tiles)
            text(c, "?", x + 60, y + 62, "serif", 72, LINE, "c", p * tiles)
    # B: 1,043 people, rolled and held
    w2 = win(t, S("0.2") - .2, S("0.3") - .2, .4, .3)
    if w2 > 0:
        text(c, roll_str(t, S("0.2") + .4, S("0.2") + 2.2, 1043), 1380, 360, "serif", 150, LINE, "c", w2)
        text(c, "PEOPLE", 1380, 470, "mono", 40, CYAN, "c", w2)
        text(c, "20 CLIPS EACH", 1380, 530, "mono", 40, LINE, "c", w2)
    # C: 57.1 percent, against a coin flip at 50
    w3 = win(t, S("0.3") - .2, S("0.5") - .2, .4, .3)
    if w3 > 0:
        text(c, roll_str(t, S("0.3") + .3, S("0.3") + 1.6, 57.1, 1) + "%", 1380, 360, "serif", 150, AMBER, "c", w3)
        rect(c, 1000, 520, 760, 34, 1, 2, GREY, alpha=w3)
        bar(c, 1000, 520, 760, 34, .571, AMBER, alpha=w3, p=prog(t, S("0.3") + .3, S("0.3") + 1.6))
        line(c, 1380, 490, 1380, 570, 1, 3, LINE, alpha=w3 * .8, dash=[10, 8])
        text(c, "COIN FLIP: 50%", 1380, 610, "mono", 40, LINE, "c", w3)
        text(c, "0", 1000, 585, "mono", 36, GREY, "c", w3)
        text(c, "100", 1760, 585, "mono", 36, GREY, "c", w3)
    # D: 99 of 1,043 light up
    w4 = win(t, S("0.5") - .2, S("0.52") - .2, .4, .3)
    if w4 > 0:
        r = random.Random(11); order = list(range(1043)); r.shuffle(order); hi = set(order[:99]); rank = {v: k for k, v in enumerate(order[:99])}
        for i in range(1043):
            col_, row_ = i % 41, i // 41
            x = 1010 + col_ * 18.5; y = 340 + row_ * 14.6
            a = ap(t, S("0.5") + (i / 1043) * .8, .25)
            if i in hi:
                q = prog(t, S("0.5") + 1.3 + rank[i] / 99 * 1.1, S("0.5") + 1.3 + rank[i] / 99 * 1.1 + .15)
                c.drawCircle(x, y, 5, P(mix(0xFF3A4150, AMBER, q), alpha=a * w4))
            else:
                c.drawCircle(x, y, 4, P(0xFF3A4150, alpha=a * w4))
        text(c, roll_str(t, S("0.5") + 1.2, S("0.5") + 2.6, 99) + " OF 1,043  ·  9.5%", 1400, 262, "mono", 46, AMBER, "c", w4)
    # E: real vs fake, correct rates
    w5 = win(t, S("0.52") - .2, S("0.53") - .2, .4, .3)
    if w5 > 0:
        text(c, "REAL CLIPS JUDGED RIGHT", 1000, 330, "mono", 40, LINE, "l", w5)
        bar(c, 1000, 370, 760, 40, .580, CYAN, alpha=w5, p=prog(t, S("0.52") + .2, S("0.52") + 1.2))
        text(c, roll_str(t, S("0.52") + .2, S("0.52") + 1.2, 58.0, 1) + "%", 1000, 520, "serif", 80, AMBER, "l", w5)
        text(c, "FAKE CLIPS JUDGED RIGHT", 1000, 600, "mono", 40, LINE, "l", w5)
        bar(c, 1000, 640, 760, 40, .561, CYAN, alpha=w5, p=prog(t, S("0.52") + .2, S("0.52") + 1.2))
        text(c, roll_str(t, S("0.52") + .2, S("0.52") + 1.2, 56.1, 1) + "%", 1000, 790, "serif", 80, AMBER, "l", w5)
    # F: by category, against 50%
    w6 = win(t, S("0.53") - .2, S("0.55") - .2, .4, .3)
    if w6 > 0:
        def X(v): return 1000 + (v - 40) / 30 * 760
        text(c, "ANIMALS, BUILDINGS: 45–47%", 1000, 320, "mono", 40, RED, "l", w6)
        rect(c, X(45), 350, X(47) - X(45), 36, 1, 2, RED, alpha=w6, fill=RED, falpha=w6 * .9)
        text(c, "PEOPLE, HANDS, ACTIONS: 58–65%", 1000, 440, "mono", 40, CYAN, "l", w6)
        rect(c, X(58), 470, X(65) - X(58), 36, 1, 2, CYAN, alpha=w6, fill=CYAN, falpha=w6 * .9)
        line(c, 1000, 560, 1760, 560, 1, 3, GREY, alpha=w6)
        for v in (40, 50, 60, 70):
            line(c, X(v), 548, X(v), 572, 1, 2.5, GREY, alpha=w6)
            text(c, str(v) + "%", X(v), 606, "mono", 36, GREY, "c", w6)
        line(c, X(50), 300, X(50), 572, 1, 2.5, LINE, alpha=w6 * .8, dash=[10, 8])
        text(c, "CHANCE", X(50), 280, "mono", 36, LINE, "c", w6)
    # G: a small group, a guess
    w7 = win(t, S("0.55") - .2, S("0.6") - .2, .4, .3)
    if w7 > 0:
        text(c, "FOR MOST VIEWERS, A GUESS", 1400, 720, "mono", 44, AMBER, "c", w7)
    # 0.7: the open question
    wq = win(t, S("0.7") - .2, S("0.8") - .2, .4, .3)
    if wq > 0:
        text(c, "WHY CAN'T WE TELL?", 960, 500, "serif", 88, AMBER, "c", ap(t, S("0.7"), .4) * wq)
    # H: who ran it
    w8 = win(t, S("0.6") - .2, S("0.7") - .2, .4, .3)
    if w8 > 0:
        card(c, 1000, 330, 800, 240, ap(t, S("0.6"), .5) * w8, LINE)
        text(c, "RUNWAY", 1400, 400, "serif", 72, AMBER, "c", w8)
        text(c, "MAKES AI VIDEO MODELS", 1400, 480, "mono", 40, LINE, "c", w8)
        text(c, "THE STUDY IS THE COMPANY'S OWN", 1400, 530, "mono", 36, GREY, "c", w8)
        source(c, "SOURCE: RUNWAY, THE TURING REEL", 100, 850, alpha=w8)
    # I: the checklists
    w9 = win(t, S("0.8") - .2, E("0.8") + 1.2, .4, .4)
    if w9 > 0:
        text(c, "EVERY 'SPOT THE FAKE' LIST", 1000, 300, "mono", 40, LINE, "l", ap(t, S("0.8") - .1, .4) * w9)
        items = ["EXTRA FINGERS", "GARBLED TEXT", "WRONG BLINKS", "ODD REFLECTIONS"]
        for k, s_ in enumerate(items):
            y = 390 + k * 80
            a = ap(t, S("0.8") + .2 + k * .15, .4) * w9
            rect(c, 1000, y - 20, 40, 40, 1, 2.5, LINE, alpha=a)
            text(c, s_, 1070, y, "mono", 40, LINE, "l", a)
            wd = tw(s_, "mono", 40)
            line(c, 1070, y, 1070 + wd, y, prog(t, S("0.8") + 1.0 + k * .45, S("0.8") + 1.35 + k * .45), 6, RED, alpha=w9)
        text(c, "THE LIST IS ALREADY OUT OF DATE", 1400, 760, "mono", 40, AMBER, "c", ap(t, S("0.8") + 3.0, .5) * w9)

# ===================================================================================================
GRID = dict(x0=120, y0=300, cw=22, ch=22, cols=36, rows=20)

def s_main(t):
    """denoising schedule for the main grid: noise, then denoise, add noise (training), undo again"""
    a1 = S("1.4") + .2; b1 = S("1.5") + .2
    if t < a1: return 0.0
    if t < b1: return denoise_s(t, a1, b1)
    if t < S("1.5") + .6: return 1.0
    if t < S("1.5") + 2.6: return 1 - denoise_s(t, S("1.5") + .6, S("1.5") + 2.6)
    if t < S("1.7") + .2: return 0.0
    return denoise_s(t, S("1.7") + .2, S("1.7") + 4.5)

@reg(1)
def seg1(c, t):
    g = GRID
    # 1.1-1.2: the lists of flaws the guides are made of (fills the opening of the segment)
    tl = win(t, S("1.1") - .2, S("1.3") - .2, .4, .3)
    if tl > 0:
        for k, s_ in enumerate(["EXTRA FINGERS", "GARBLED SIGNS", "WRONG BLINKS"]):
            a_ = ap(t, S("1.1") + .2 + k * .35, .4) * tl
            chip(c, s_, 960, 440 + k * 110, GREY, a_, size=44, w=520)
    # left: the main denoising grid
    gw = win(t, S("1.3") - .2, S("1.9") + 4.0, .4, .5)
    if gw > 0:
        text(c, "HOW A VIDEO IS MADE", 120, 230, "mono", 44, CYAN, "l", gw)
        sv = s_main(t)
        noise_grid(c, sv, g["x0"], g["y0"], g["cw"], g["ch"], g["cols"], g["rows"], seed=5, alpha=gw)
        rect(c, g["x0"], g["y0"], g["cols"] * g["cw"], g["rows"] * g["ch"], 1, 2, LINE, alpha=gw * .5)
        illus(c, gw)
    # right column: captions per beat
    tn = win(t, S("1.3") - .2, S("1.4") - .2, .3, .3)
    if tn > 0: text(c, "PURE NOISE", 1000, 340, "monob", 56, LINE, "l", tn)
    sv_step = int(round(s_main(t) * 50))
    ts = win(t, S("1.4") + .2, S("1.5") + .4, .3, .3)
    if ts > 0: text(c, "STEP  " + str(sv_step).rjust(2, " "), 1000, 340, "monob", 56, AMBER, "l", ts)
    tf = win(t, S("1.5") + .6, S("1.5") + 2.6, .3, .3)
    if tf > 0: text(c, "TRAINING: ADD NOISE", 1000, 340, "monob", 56, RED, "l", tf)
    tu = win(t, S("1.7") + .2, S("1.8") - .2, .3, .3)
    if tu > 0: text(c, "UNDO ONE STEP", 1000, 340, "monob", 56, AMBER, "l", tu)
    # 1.6: the 2020 paper, as a source line
    t6 = win(t, S("1.6") - .2, S("1.7") - .2, .4, .3)
    if t6 > 0:
        card(c, 1000, 430, 800, 150, ap(t, S("1.6"), .4) * t6, CYAN)
        text(c, "DENOISING DIFFUSION", 1400, 485, "mono", 40, CYAN, "c", t6)
        text(c, "2020  ·  UC BERKELEY", 1400, 540, "mono", 40, LINE, "c", t6)
    # 1.7: the prompt steers every step
    t7 = win(t, S("1.7") - .2, S("1.8") - .2, .4, .3)
    if t7 > 0:
        text(c, "PROMPT", 1000, 430, "mono", 36, GREY, "l", t7)
        text(c, "a sun over a calm sea", 1000, 480, "mono", 44, LINE, "l", ap(t, S("1.7") + .4, .6) * t7)
        text(c, "EVERY STEP IS NUDGED TOWARD IT", 1000, 540, "mono", 40, AMBER, "l", ap(t, S("1.7") + 1.4, .5) * t7)
    # 1.8: three frames denoised together, so they must agree
    t8 = win(t, S("1.8") - .2, S("1.9") - .2, .4, .3)
    if t8 > 0:
        s8 = denoise_s(t, S("1.8") + .2, S("1.8") + 4.0)
        for k, (x, sx) in enumerate([(1000, 0.0), (1280, 1.2), (1560, 2.4)]):
            noise_grid(c, s8, x, 440, 15, 15, 16, 10, sx=sx, seed=9, alpha=t8)
            rect(c, x, 440, 240, 150, 1, 2, LINE, alpha=t8 * .6)
        text(c, "FRAMES DENOISED TOGETHER", 1400, 640, "mono", 40, CYAN, "c", t8)
        line(c, 1120, 515, 1280, 515, 1, 2, CYAN, alpha=t8 * .6, dash=[8, 8])
        line(c, 1400, 515, 1560, 515, 1, 2, CYAN, alpha=t8 * .6, dash=[8, 8])
    # 1.9 onward: the model learns patterns, not a copy
    t9 = win(t, S("1.9") - .2, E("1.11") + .4, .4, .5)
    if t9 > 0:
        text(c, "LEARNS PATTERNS,", 1000, 460, "monob", 60, LINE, "l", ap(t, S("1.9") + .2, .5) * t9)
        text(c, "NOT A CHECKLIST", 1000, 540, "monob", 60, AMBER, "l", ap(t, S("1.9") + 1.0, .5) * t9)
        text(c, "SAME PROMPT, NEW STATIC, NEW PICTURE", 1000, 620, "mono", 36, CYAN, "l", ap(t, S("1.11") - .5, .5) * t9)
