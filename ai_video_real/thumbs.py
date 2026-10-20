# -*- coding: utf-8 -*-
"""Three thumbnails, 1280x720 PNG, same style as the video. Geometry only, no photos or footage."""
import skia
from lib import *
from scene_util import noise_grid, bar, TGT

def canvas():
    s = skia.Surface(1280, 720); c = s.getCanvas(); c.clear(BG); return s, c

def save(s, name):
    s.makeImageSnapshot().save(name, skia.kPNG); print("saved", name)

def A():
    """REAL OR AI?  two identical tiles, one big question mark"""
    s, c = canvas()
    noise_grid(c, 1.0, 140, 200, 20, 20, 15, 12, sx=0.0, seed=4)
    noise_grid(c, 1.0, 780, 200, 20, 20, 15, 12, sx=0.0, seed=4)
    rect(c, 140, 200, 300, 240, 1, 5, LINE)
    rect(c, 780, 200, 300, 240, 1, 5, LINE)
    text(c, "?", 640, 320, "serif", 220, AMBER, "c")
    text(c, "REAL OR AI?", 640, 600, "monob", 96, LINE, "c")
    save(s, "thumbnail_A.png")

def B():
    """ALMOST A COIN FLIP  57% against a 50% line"""
    s, c = canvas()
    text(c, "57%", 420, 340, "serif", 300, AMBER, "c")
    line(c, 140, 480, 1140, 480, 1, 4, GREY)
    line(c, 140, 480 + 1, 140, 480 + 1, 1, 4, GREY)
    bar(c, 140, 520, 1000, 56, .571, AMBER)
    rect(c, 140, 520, 1000, 56, 1, 3, GREY)
    line(c, 640, 490, 640, 590, 1, 5, LINE, dash=[14, 10])
    text(c, "COIN FLIP 50%", 640, 630, "mono", 48, LINE, "c")
    text(c, "ALMOST A COIN FLIP", 640, 110, "monob", 84, LINE, "c")
    save(s, "thumbnail_B.png")

def C():
    """NO MORE TELLS  a checklist, every item crossed out"""
    s, c = canvas()
    items = ["EXTRA FINGERS", "GARBLED TEXT", "WRONG BLINKS"]
    for k, it in enumerate(items):
        y = 260 + k * 110
        rect(c, 200, y - 34, 56, 56, 1, 4, LINE)
        text(c, it, 300, y, "mono", 60, LINE, "l")
        wd = tw(it, "mono", 60)
        line(c, 300, y, 300 + wd, y, 1, 10, RED)
    text(c, "NO MORE TELLS", 640, 610, "monob", 100, AMBER, "c")
    save(s, "thumbnail_C.png")

if __name__ == "__main__":
    A(); B(); C()
