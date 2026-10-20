# -*- coding: utf-8 -*-
"""Segments 2-3: why the old tells expire, and the Berkeley viewing-time study (the reversal)."""
import math
import skia
from lib import *
from scene_util import *

REG = {}
def reg(k):
    def deco(fn): REG[k] = fn; return fn
    return deco

def illus(c, alpha=1.0):
    text(c, "illustrative", 1800, 880, "mono", 36, GREY, "r", alpha, tag="illus")

def hand(c, cx, cy, angles, col, p=1.0, alpha=1.0, palm=70, flen=130, fw=26):
    """schematic hand: palm disc with one rounded stroke per finger (geometry, not a picture)"""
    c.drawCircle(cx, cy, palm, P(col, alpha=.22 * alpha))
    c.drawCircle(cx, cy, palm, P(col, "stroke", 3, alpha))
    for k, a in enumerate(angles):
        q = clamp(p * (1.0 if k < len(angles) else 0) - 0.0)
        ax = math.radians(a)
        x0 = cx + palm * .75 * math.cos(ax); y0 = cy + palm * .75 * math.sin(ax)
        x1 = cx + (palm + flen) * math.cos(ax); y1 = cy + (palm + flen) * math.sin(ax)
        draw_on(c, [(x0, y0), (x1, y1)], q, fw, col, alpha)

@reg(2)
def seg2(c, t):
    # 2.1 - 2.4: hands, small training photos, data vs errors, text
    w1 = win(t, S("2.1") - .2, S("2.2") - .2, .4, .3)
    if w1 > 0:
        pr = ap(t, S("2.1") + .3, .6)
        hand(c, 520, 520, [-150, -120, -90, -60, -30], CYAN, pr, w1)
        text(c, "5 FINGERS", 520, 790, "mono", 44, CYAN, "c", w1)
        wr = ap(t, S("2.1") + 1.2, .5)
        hand(c, 1300, 520, [-165, -140, -115, -90, -65, -40], RED, wr, w1)
        text(c, "6 FINGERS", 1300, 790, "mono", 44, RED, "c", wr * w1)
        illus(c, w1)
    w2 = win(t, S("2.2") - .2, S("2.3") - .2, .4, .3)
    if w2 > 0:
        text(c, "TRAINING PHOTOS", 1380, 300, "mono", 44, LINE, "c", w2)
        for k in range(3):
            x = 1000 + k * 280; y = 380
            rect(c, x, y, 240, 180, 1, 2, GREY, alpha=w2, fill=PANEL, falpha=w2)
            hand(c, x + 120, y + 110, [-150, -120, -90, -60, -30], CYAN, ap(t, S("2.2") + .3 + k * .2, .4), w2 * .9, palm=14, flen=24, fw=5)
            rect(c, x + 60 + k * 30, y + 70, 70, 80, 1, 1, PANEL, alpha=w2, fill=0xFF3A4150, falpha=w2)   # occluder
        text(c, "SMALL, AND OFTEN HIDDEN", 1380, 640, "mono", 40, AMBER, "c", w2)
        illus(c, w2)
    w3 = win(t, S("2.3") - .2, S("2.4") - .2, .4, .3)
    if w3 > 0:
        base = 680
        text(c, "MORE DATA, BIGGER MODEL", 1380, 240, "mono", 40, CYAN, "c", w3)
        for k, (d, e) in enumerate([(80, 300), (140, 220), (210, 150), (290, 90), (380, 50)]):
            x = 1040 + k * 150
            p = ap(t, S("2.3") + .3 + k * .25, .4)
            c.drawRect(skia.Rect.MakeXYWH(x, base - d * p, 60, d * p), P(CYAN, alpha=w3))
            c.drawRect(skia.Rect.MakeXYWH(x + 74, base - e * p, 60, e * p), P(RED, alpha=w3))
        line(c, 1000, base, 1800, base, 1, 2.5, GREY, alpha=w3)
        text(c, "DATA", 1100, 712, "mono", 36, CYAN, "c", w3)
        text(c, "HAND ERRORS", 1320, 712, "mono", 36, RED, "c", w3)
        illus(c, w3)
    w4 = win(t, S("2.4") - .2, S("2.6") - .2, .4, .3)
    if w4 > 0:
        text(c, "FROM FAR", 560, 300, "mono", 40, GREY, "c", w4)
        text(c, "OPEN", 560, 480, "serif", 150, LINE, "c", w4)
        text(c, "UP CLOSE", 1300, 300, "mono", 40, GREY, "c", w4)
        jit = int(t * 6) % 3
        text(c, ["0PEN", "OP3N", "0P-N"][jit], 1300, 480, "serif", 150, AMBER, "c", w4)
        illus(c, w4)
    # 2.6 - 2.8: the checklist goes stale, one item at a time
    w5 = win(t, S("2.6") - .2, E("2.8") + 1.2, .4, .4)
    if w5 > 0:
        text(c, "SPOT THE FAKE: THE LIST", 400, 300, "mono", 44, LINE, "l", ap(t, S("2.6") - .1, .4) * w5)
        items = ["EXTRA FINGERS", "GARBLED TEXT", "WRONG BLINKS", "ODD REFLECTIONS"]
        for k, s_ in enumerate(items):
            y = 400 + k * 90
            a = ap(t, S("2.6") + .2 + k * .15, .4) * w5
            rect(c, 400, y - 22, 44, 44, 1, 2.5, LINE, alpha=a)
            text(c, s_, 470, y, "mono", 44, LINE, "l", a)
            wd = tw(s_, "mono", 44)
            line(c, 470, y, 470 + wd, y, prog(t, S("2.6") + .8 + k * .55, S("2.6") + 1.1 + k * .55), 7, RED, alpha=w5)
        text(c, "A GUESS ABOUT NEXT YEAR'S MODELS", 400, 800, "mono", 40, AMBER, "l", ap(t, S("2.7") + .3, .5) * w5)
        text(c, "NEW ROUND OF TRAINING, NEW TELLS", 400, 860, "mono", 36, CYAN, "l", ap(t, S("2.8") + .4, .5) * w5)

@reg(3)
def seg3(c, t):
    # 3.1 headline numbers
    w1 = win(t, S("3.1") - .2, S("3.2") - .2, .4, .3)
    if w1 > 0:
        text(c, "376", 1380, 380, "serif", 150, LINE, "c", w1)
        text(c, "PEOPLE, 3 AI VIDEO MODELS", 1380, 520, "mono", 40, CYAN, "c", w1)
        text(c, "PLUS REAL FOOTAGE", 1380, 580, "mono", 40, LINE, "c", w1)
        source(c, "SOURCE: UC BERKELEY, PERCEPTUAL STUDY", 100, 850, alpha=w1)
    # 3.2 - 3.4: viewing time vs accuracy (only the two measured endpoints are placed; the line between is illustrative)
    w2 = win(t, S("3.2") - .2, S("3.6") - .2, .4, .3)
    if w2 > 0:
        def X(i): return 380 if i == 0 else 1560
        def Y(v): return 740 - (v - 40) / 50 * 440
        line(c, 300, 740, 1640, 740, 1, 2.5, GREY, alpha=w2)
        line(c, 300, 300, 300, 740, 1, 2.5, GREY, alpha=w2)
        for v in (50, 60, 70, 80):
            text(c, str(v) + "%", 250, Y(v), "mono", 36, GREY, "r", w2)
        line(c, 300, Y(50), 1640, Y(50), 1, 2, LINE, alpha=w2 * .5, dash=[10, 8])
        text(c, "CHANCE", 1640, Y(50) - 30, "mono", 36, LINE, "r", w2)
        text(c, "1 FRAME", X(0), 790, "mono", 40, LINE, "c", w2)
        text(c, "8 SECONDS", X(1), 790, "mono", 40, LINE, "c", w2)
        # real footage: flat, near 60
        pr = prog(t, S("3.4") - .3, S("3.4") + 1.2)
        line(c, X(0), Y(60), X(0) + (X(1) - X(0)) * pr, Y(60), 1, 6, CYAN, alpha=w2)
        circle(c, X(0), Y(60), 12, 1, 3, CYAN, w2, fill=CYAN, falpha=w2)
        circle(c, X(1), Y(60), 12, pr, 3, CYAN, w2, fill=CYAN, falpha=w2 * pr)
        text(c, "REAL: STAYS NEAR 60%", 1100, Y(60) + 50, "mono", 40, CYAN, "c", ap(t, S("3.4") + .5, .5) * w2)
        # fake clips: the two endpoints, measured
        pf = prog(t, S("3.3") + .2, S("3.3") + 2.0)
        line(c, X(0), Y(57.7), X(0) + (X(1) - X(0)) * pf, Y(57.7) + (Y(74.6) - Y(57.7)) * pf, 1, 6, AMBER, alpha=w2)
        circle(c, X(0), Y(57.7), 14, 1, 3, AMBER, w2, fill=AMBER, falpha=w2)
        circle(c, X(1), Y(74.6), 14, pf, 3, AMBER, w2, fill=AMBER, falpha=w2 * pf)
        text(c, roll_str(t, S("3.3") + .2, S("3.3") + 1.4, 57.7, 1) + "%", X(0) + 40, Y(57.7) - 60, "serif", 60, AMBER, "l", w2)
        text(c, roll_str(t, S("3.3") + 1.0, S("3.3") + 2.2, 74.6, 1) + "%", X(1) - 40, Y(74.6) - 60, "serif", 60, AMBER, "r", w2)
        text(c, "FAKE CLIPS: MORE TIME, MORE CAUGHT", 960, 300, "mono", 40, AMBER, "c", ap(t, S("3.3") + .5, .5) * w2)
        text(c, "LINE BETWEEN IS ILLUSTRATIVE", 960, 350, "mono", 36, GREY, "c", w2)
        illus(c, w2)
    # 3.6: the reversal (looking longer helps with fakes, not with real clips)
    w3 = win(t, S("3.6") - .2, S("3.7") - .2, .4, .3)
    if w3 > 0:
        text(c, "LOOK LONGER", 480, 460, "monob", 64, LINE, "c", ap(t, S("3.6"), .4) * w3)
        arrow(c, 760, 460, 1020, 460, prog(t, S("3.6") + .3, S("3.6") + .9), 6, LINE, alpha=w3)
        text(c, "FAKES: CAUGHT MORE", 1400, 460, "monob", 60, AMBER, "c", ap(t, S("3.6") + 1.0, .4) * w3)
        text(c, "REAL: NO GAIN", 1400, 620, "monob", 60, LINE, "c", ap(t, S("3.6") + 1.8, .4) * w3)
        line(c, 1000, 620, 1800, 620, prog(t, S("3.6") + 2.6, S("3.6") + 3.1), 9, RED, alpha=w3)
    # 3.7: viewers look for broken motion
    w4 = win(t, S("3.7") - .2, S("3.8") + .1, .4, .3)
    if w4 > 0:
        pts_e = [(500 + i * 40, 560 - 90 * math.sin(i / 3.0)) for i in range(26)]
        pts_a = [(500 + i * 40, 560 - 90 * math.sin(i / 3.0) + (60 if 12 <= i <= 14 else 0)) for i in range(26)]
        draw_on(c, pts_e, prog(t, S("3.7") + .2, S("3.7") + 1.2), 4, CYAN, w4, dash=[12, 10])
        draw_on(c, pts_a, prog(t, S("3.7") + 1.2, S("3.7") + 2.4), 5, AMBER, w4)
        text(c, "EXPECTED MOTION", 800, 260, "mono", 40, CYAN, "l", ap(t, S("3.7") + .3, .4) * w4)
        text(c, "BROKEN MOTION", 1060, 790, "mono", 40, AMBER, "l", ap(t, S("3.7") + 1.4, .4) * w4)
        illus(c, w4)
    # 3.8: doubt grows
    w5 = win(t, S("3.8") - .2, S("3.9") - .2, .4, .3)
    if w5 > 0:
        for k in range(3):
            text(c, "?", 600 + k * 380, 470, "serif", 120 + k * 50, LINE, "c", ap(t, S("3.8") - .1 + k * .25, .4) * w5)
        text(c, "NO CREDIT FOR REAL", 960, 680, "mono", 44, AMBER, "c", ap(t, S("3.8") + 1.4, .4) * w5)
    # 3.9: real video stops being believed
    w6 = win(t, S("3.9") - .2, E("3.95") + 1.0, .4, .4)
    if w6 > 0:
        rect(c, 1000, 330, 400, 260, 1, 4, GREEN, alpha=w6, fill=PANEL, falpha=w6)
        text(c, "REAL", 1200, 460, "monob", 56, GREEN, "c", w6)
        text(c, "?", 1200, 600, "serif", 110, LINE, "c", ap(t, S("3.9") + .5, .4) * w6 * .6)
        text(c, "NOT BELIEVED", 1200, 680, "mono", 48, RED, "c", ap(t, S("3.9") + 1.0, .4) * w6)
