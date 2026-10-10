# -*- coding: utf-8 -*-
"""AI 原理系列固定画风 + 与配音时间轴同步的基础场景"""
import json, os, random
from manim import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = json.load(open(f"{HERE}/build/timeline.json"))

BG = "#16181D"
BLUE = "#58C4DD"
YELLOW = "#F5D547"
GREEN = "#83C167"
RED = "#FC6255"
WHITE = "#ECECEC"
GREY = "#6B7080"
DIM = "#3A3F4B"
SERIF, SANS, MONO = "CMU Serif", "Inter", "JetBrains Mono"

config.background_color = BG

# 内容区（字幕占底部约 1.5 个单位）
TOP, BOTTOM = 3.55, -2.45


def T(s, size=24, color=WHITE, font=SANS, weight=NORMAL, **kw):
    return Text(s, font=font, font_size=size, color=color, weight=weight, **kw)


def big(s, size=64, color=YELLOW):
    return Text(s, font=SERIF, font_size=size, color=color)


def tok(label, color=BLUE, w=None, h=0.7, size=22, fill=0.18, dashed=False):
    t = Text(label, font=MONO, font_size=size, color=color)
    w = w or max(t.width + 0.4, 0.8)
    box = RoundedRectangle(corner_radius=0.08, width=w, height=h, stroke_color=color,
                           stroke_width=3, fill_color=color, fill_opacity=fill)
    if dashed:
        box = DashedVMobject(box, num_dashes=24)
    t.move_to(box.get_center())
    return VGroup(box, t)


def sq(color=BLUE, s=0.34, fill=0.25, sw=2):
    return Square(side_length=s, stroke_color=color, stroke_width=sw, fill_color=color, fill_opacity=fill)


def person(color=WHITE, scale=1.0):
    head = Circle(radius=0.13, color=color, fill_color=color, fill_opacity=1, stroke_width=0)
    body = Sector(radius=0.28, angle=PI, start_angle=0, color=color, fill_opacity=1, stroke_width=0)
    head.move_to(UP * 0.3)
    body.move_to(DOWN * 0.04 + DOWN * 0.0)
    g = VGroup(head, body).scale(scale)
    return g


def illus(text="illustrative"):
    return T(text, 18, GREY).to_corner(DR, buff=0.2).shift(UP * 1.45)


def make_net(layers=(4, 6, 6, 4), width=7.0, height=3.2, center=ORIGIN, r=0.09):
    cols = []
    xs = np.linspace(-width / 2, width / 2, len(layers))
    for x, n in zip(xs, layers):
        ys = np.linspace(-height / 2, height / 2, n) if n > 1 else [0]
        cols.append([Dot(center + RIGHT * x + UP * y, radius=r, color=BLUE) for y in ys])
    edges = VGroup()
    for a, b in zip(cols[:-1], cols[1:]):
        for d1 in a:
            for d2 in b:
                edges.add(Line(d1.get_center(), d2.get_center(), stroke_width=1.2, stroke_color=BLUE, stroke_opacity=0.35))
    dots = VGroup(*[d for c in cols for d in c])
    return cols, dots, edges


def counter(fmt, start, end, pos, size=64, color=YELLOW, font=SERIF, edge=None, rate=None):
    """返回 (Text, 动画)。滚动靠 ValueTracker + updater，字符串不变时不重绘。"""
    tr = ValueTracker(start)

    def mk(v):
        m = Text(fmt(v), font=font, font_size=size, color=color)
        if edge is None:
            m.move_to(pos)
        else:
            m.move_to(pos, aligned_edge=edge)
        return m
    first = mk(start)
    first._last = fmt(start)

    def upd(m):
        v = tr.get_value()
        s = fmt(v)
        if s != m._last:
            m.become(mk(v))
            m._last = s
    first.add_updater(upd)
    return first, tr.animate(rate_func=rate or rate_functions.ease_out_cubic).set_value(end)


class Seg(Scene):
    SEG = "0"

    def setup(self):
        fps = config.frame_rate
        seg = [s for s in TL["segments"] if s["id"] == self.SEG][0]
        self.t0 = round(seg["begin"] * fps) / fps
        self.t1 = round(seg["end"] * fps) / fps
        self.dur = self.t1 - self.t0
        self.rows = {r["id"]: r for r in TL["rows"]}
        self.chunks = {}
        for c in TL["chunks"]:
            self.chunks.setdefault(c["row"], []).append(c)

    # ---- 时间 ----
    def now(self):
        return self.renderer.time

    def tr(self, rid, ci=None, f=0.0):
        """某行(或某块)内 f 比例处的本段局部时间"""
        if ci is None:
            r = self.rows[rid]
            a, b = r["start"], r["end"]
        else:
            c = self.chunks[rid][ci]
            a, b = c["start"], c["end"]
        return a + f * (b - a) - self.t0

    def go(self, t):
        dt = t - self.now()
        if dt > 1.5 / config.frame_rate:
            self.wait(dt)

    def act(self, t, *anims, d=1.0, **kw):
        """等到 t 秒再播放动画；若已落后则压缩时长"""
        self.go(t)
        late = self.now() - t
        d = max(0.12, d - max(0.0, late))
        if anims:
            self.play(*anims, run_time=d, **kw)

    def finish(self, fade=True):
        if fade:
            self.go(self.dur - 0.35)
            objs = list(self.mobjects)
            if objs:
                self.play(*[FadeOut(m) for m in objs], run_time=0.3)
        self.go(self.dur)


def prob_chart(items, vals, hi=0, left=-1.2, top=0.5, gap=0.6, scale=6.0, show_vals=True, size=24, color=BLUE):
    """横向柱状概率图。每行 = VGroup(label, bar, value)。hi 行用黄色。"""
    rows = VGroup()
    for i, (w, v) in enumerate(zip(items, vals)):
        y = top - i * gap
        lab = Text(w, font=MONO, font_size=size, color=WHITE).move_to(RIGHT * (left - 0.25) + UP * y, aligned_edge=RIGHT)
        c = YELLOW if i == hi else color
        bar = Rectangle(width=max(v * scale, 0.04), height=0.38, stroke_width=0, fill_color=c, fill_opacity=0.9)
        bar.move_to(RIGHT * left + UP * y, aligned_edge=LEFT)
        val = Text(f"{v:.2f}" if v >= 0.005 else "≈ 0", font=MONO, font_size=size - 4, color=c)
        val.next_to(bar, RIGHT, buff=0.2)
        if not show_vals:
            val.set_opacity(0)
        rows.add(VGroup(lab, bar, val))
    return rows


def check(pos, color=GREEN, s=1.0):
    m = VMobject(stroke_color=color, stroke_width=7)
    m.set_points_as_corners([LEFT * 0.14 * s + UP * 0.0, LEFT * 0.04 * s + DOWN * 0.11 * s, RIGHT * 0.18 * s + UP * 0.13 * s])
    return m.move_to(pos)
