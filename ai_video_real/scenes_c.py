# -*- coding: utf-8 -*-
"""Segments 4-5: what still works (provenance, watermarks, who posted first) and the closing question."""
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

BOX = [(250, 380), (770, 380), (1290, 380)]   # three panels, 380 px wide, 300 px tall

@reg(4)
def seg4(c, t):
    wb = win(t, S("4.1") - .2, S("5.1") - .2, .4, .3)
    if wb > 0:
        text(c, "THREE THINGS THAT STILL WORK", 960, 260, "mono", 44, LINE, "c", wb)
        for k, (x, y) in enumerate(BOX):
            rect(c, x, y, 380, 300, 1, 2, GREY, alpha=wb * .8, fill=PANEL, falpha=wb)
            text(c, str(k + 1), x + 340, y + 46, "serif", 60, GREY, "r", wb)
    # 1: provenance (4.2 - 4.3)
    x, y = BOX[0]
    w1 = win(t, S("4.2") - .2, S("4.4") - .2, .4, .3)
    if w1 > 0:
        text(c, "PROVENANCE", x + 40, y + 46, "mono", 40, CYAN, "l", w1)
        for r_, s_ in enumerate(["WHO MADE IT", "WHICH TOOL", "SIGNED"]):
            yy = y + 110 + r_ * 56
            a = ap(t, S("4.2") + .3 + r_ * .35, .4) * w1
            check(c, x + 56, yy, 34, prog(t, S("4.2") + .3 + r_ * .35, S("4.2") + .6 + r_ * .35), 7, GREEN, a)
            text(c, s_, x + 100, yy, "mono", 36, LINE, "l", a)
        text(c, "C2PA", x + 40, y + 270, "mono", 36, CYAN, "l", ap(t, S("4.2") + 1.5, .4) * win(t, S("4.2") - .2, S("4.3") - .2, .4, .3))
    w1b = win(t, S("4.3") - .2, S("4.4") - .2, .4, .3)
    if w1b > 0:
        for r_ in range(3):
            yy = y + 110 + r_ * 56
            line(c, x + 100, yy, x + 100 + tw(["WHO MADE IT", "WHICH TOOL", "SIGNED"][r_], "mono", 36), yy, prog(t, S("4.3") + .6 + r_ * .3, S("4.3") + 1.0 + r_ * .3), 5, RED, alpha=w1b)
        text(c, "UPLOAD STRIPS", x + 40, y + 270, "mono", 36, RED, "l", ap(t, S("4.3") + 1.6, .4) * w1b)
    # 2: watermark (4.4 - 4.6)
    x, y = BOX[1]
    w2 = win(t, S("4.4") - .2, S("4.6") - .2, .4, .3)
    if w2 > 0:
        text(c, "WATERMARK", x + 40, y + 46, "mono", 40, CYAN, "l", w2)
        cols_, rows_, cw_, ch_ = 10, 6, 30, 30
        ox, oy = x + 40, y + 100
        sweep = prog(t, S("4.4") + .3, S("4.4") + 2.8)
        for r_ in range(rows_):
            for k_ in range(cols_):
                shade = mix(0xFF2D4E5C, 0xFF58C4DD, ((k_ + r_ * 3) % 7) / 7.0)
                c.drawRect(skia.Rect.MakeXYWH(ox + k_ * cw_, oy + r_ * ch_, cw_ - 2, ch_ - 2), P(shade, alpha=w2))
        # invisible lattice: visible only where the detector sweep has passed
        for r_ in range(rows_ + 1):
            for k_ in range(cols_ + 1):
                px = ox + k_ * cw_ * 1.0; py = oy + r_ * ch_ * 1.0
                near = clamp(1 - abs((px - x) / 380 - sweep) * 4)
                c.drawCircle(px, py, 3, P(AMBER, alpha=w2 * near * .9))
        sx = ox + sweep * (cols_ * cw_)
        line(c, sx, oy - 10, sx, oy + rows_ * ch_, 1, 3, AMBER, alpha=w2 * (1 if 0 < sweep < 1 else 0))
    w2b = win(t, S("4.5") - .2, S("4.6") - .2, .4, .3)
    if w2b > 0:
        text(c, "OCT 7, 2026  ·  OPEN TO ANYONE, IN ENGLISH", 960, 760, "mono", 40, LINE, "c", w2b)
        for k, (s_, cx_) in enumerate([("OPENAI", 560), ("NVIDIA", 880), ("KAKAO", 1160)]):
            chip(c, s_, cx_, 860, CYAN, w2b * ap(t, S("4.5") + 1.2 + k * .3, .4), size=36)
    w2c = win(t, S("4.6") - .2, S("4.7") - .2, .4, .3)
    if w2c > 0:
        text(c, "MATCH: MARK FOUND", 960, 760, "mono", 44, GREEN, "c", ap(t, S("4.6") + .3, .4) * w2c)
        text(c, "NO MATCH: NO ANSWER, NOT PROOF", 960, 830, "mono", 44, GREY, "c", ap(t, S("4.6") + 1.0, .4) * w2c)
    w2d = win(t, S("4.7") - .2, S("4.8") - .2, .4, .3)
    if w2d > 0:
        text(c, "BOTH TOOLS HAVE HOLES", 960, 800, "mono", 48, AMBER, "c", ap(t, S("4.7") + .2, .4) * w2d)
    w2e = win(t, S("4.8") - .2, S("5.1") - .2, .4, .3)
    if w2e > 0:
        text(c, "NEITHER ANSWERS: IS THIS CLIP REAL?", 960, 800, "mono", 40, LINE, "c", ap(t, S("4.8") + .2, .4) * w2e)
        text(c, "THEY ANSWER NARROWER QUESTIONS", 960, 860, "mono", 36, CYAN, "c", ap(t, S("4.8") + 1.2, .4) * w2e)
    illus(c, wb)

@reg(5)
def seg5(c, t):
    # 3: who posted first (5.1 - 5.2)
    w1 = win(t, S("5.1") - .2, S("5.25") - .2, .4, .3)
    if w1 > 0:
        text(c, "3  ASK WHO POSTED FIRST", 120, 240, "mono", 48, LINE, "l", ap(t, S("5.1") - .1, .4) * w1)
        line(c, 200, 520, 1720, 520, 1, 3, GREY, alpha=w1)
        for k in range(5):
            x = 300 + k * 350
            a = ap(t, S("5.1") + .3 + k * .25, .4) * w1
            if k == 0:
                c.drawCircle(x, 520, 22, P(AMBER, alpha=a))
                text(c, "FIRST POST", x, 600, "mono", 40, AMBER, "c", a)
            else:
                c.drawCircle(x, 520, 18, P(GREY, alpha=a))
                text(c, "REPOST", x, 600, "mono", 36, GREY, "c", a)
                cross(c, x, 440, 40, prog(t, S("5.2") + k * .2, S("5.2") + .4 + k * .2), 8, RED, w1)
        text(c, "A REPOST IS NOT A SOURCE", 960, 700, "mono", 44, LINE, "c", ap(t, S("5.2") + .6, .4) * w1)
        illus(c, w1)
    # caution (5.25)
    w2 = win(t, S("5.25") - .2, S("5.3") - .2, .4, .3)
    if w2 > 0:
        rect(c, 200, 330, 800, 110, 1, 3, GREY, alpha=w2, fill=PANEL, falpha=w2)
        text(c, "BREAKING!!!  WATCH THIS NOW", 240, 385, "mono", 40, LINE, "l", ap(t, S("5.25") + .2, .4) * w2)
        text(c, "NO SOURCE", 200, 480, "mono", 40, RED, "l", ap(t, S("5.25") + .5, .4) * w2)
        text(c, "THE ORIGIN MATTERS MORE THAN THE LOOK", 200, 560, "mono", 40, AMBER, "l", ap(t, S("5.25") + 1.0, .4) * w2)
    # second, independent source (5.3 - 5.4)
    w3 = win(t, S("5.3") - .2, S("5.45") - .2, .4, .3)
    if w3 > 0:
        c.drawCircle(1400, 380, 22, P(CYAN, alpha=w3))
        text(c, "SECOND SOURCE", 1400, 330 - 40, "mono", 40, CYAN, "c", ap(t, S("5.3") + .2, .4) * w3)
        text(c, "INDEPENDENT", 1400, 440, "mono", 36, CYAN, "c", ap(t, S("5.3") + .4, .4) * w3)
        draw_on(c, [(300, 520), (1400, 380)], prog(t, S("5.3") + .2, S("5.3") + 1.2), 3, CYAN, w3, dash=[12, 10])
        for k, s_ in enumerate(["PLACE", "TIME", "DETAILS"]):
            yy = 690 + k * 70
            a = ap(t, S("5.4") + .2 + k * .4, .4) * w3
            check(c, 260, yy, 36, prog(t, S("5.4") + .2 + k * .4, S("5.4") + .6 + k * .4), 8, GREEN, a)
            text(c, s_ + " LINES UP", 330, yy, "mono", 40, LINE, "l", a)
    # 5.45 - 5.5: checks that do not need pixels
    w4 = win(t, S("5.45") - .2, S("5.5") - .2, .4, .3)
    if w4 > 0:
        text(c, "REVERSE IMAGE SEARCH  ·  ORIGINAL POST", 960, 560, "mono", 44, CYAN, "c", ap(t, S("5.45"), .4) * w4)
    w5 = win(t, S("5.5") - .2, S("5.6") - .2, .4, .3)
    if w5 > 0:
        text(c, "PIXEL HUNT", 960, 520, "mono", 80, LINE, "c", ap(t, S("5.5"), .4) * w5)
        cross(c, 960, 520, 300, prog(t, S("5.5") + .4, S("5.5") + 1.0), 12, RED, w5)
    # 5.6 - 5.7: the real question
    w6 = win(t, S("5.6") - .2, S("5.7") - .2, .4, .3)
    if w6 > 0:
        text(c, "MOST PEOPLE CANNOT", 960, 440, "mono", 60, LINE, "c", ap(t, S("5.6") + .2, .4) * w6)
        text(c, "THAT IS NOT A PERSONAL FAILING", 960, 520, "mono", 40, GREY, "c", ap(t, S("5.6") + 1.2, .4) * w6)
    w7 = win(t, S("5.7") - .2, E("5.8") + 10.0, .4, .0)
    if w7 > 0:
        text(c, "WHAT WILL YOU STILL TRUST?", 960, 470, "serif", 84, AMBER, "c", ap(t, S("5.7"), .5) * w7)
        text(c, "TELL US IN THE COMMENTS", 960, 640, "mono", 52, LINE, "c", ap(t, S("5.8") + .3, .5) * w7)
