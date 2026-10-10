# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from common import *


def card(label, icon, color=WHITE):
    r = RoundedRectangle(corner_radius=0.15, width=3.9, height=1.9, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.06)
    t = T(label, 26, color).move_to(r.get_bottom() + UP * 0.38)
    icon.move_to(r.get_center() + UP * 0.28)
    return VGroup(r, icon, t)


class Seg7(Seg):
    SEG = "7"

    def construct(self):
        # 7.1 总图
        mini_tok = VGroup(*[tok(w, BLUE, size=18, h=0.45, w=0.8) for w in ["The", "cat", "sat"]]).arrange(RIGHT, buff=0.1)
        mini_bars = prob_chart(["a", "b", "c"], [0.6, 0.25, 0.1], hi=0, left=0, top=0.3, gap=0.3, scale=1.6, show_vals=False, size=18)
        mini_bars = VGroup(*[r[1] for r in mini_bars]).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        _, d_, e_ = make_net((3, 4, 3), 1.6, 0.8)
        mini_net = VGroup(e_, d_)
        mini_att = VGroup(*[Arc(radius=0.3 + 0.12 * i, start_angle=PI, angle=-PI, stroke_color=YELLOW if i == 2 else BLUE, stroke_width=3 + i) for i in range(3)])
        mini_ppl = person(WHITE, 1.0)
        mini_think = VGroup(*[sq(BLUE, 0.2, 0.3, 2) for _ in range(8)]).arrange(RIGHT, buff=0.06)
        cards = VGroup(card("tokens", mini_tok, BLUE), card("probabilities", mini_bars), card("parameters", mini_net, BLUE),
                       card("attention", mini_att, YELLOW), card("human feedback", mini_ppl), card("thinking", mini_think, GREEN))
        cards.arrange_in_grid(2, 3, buff=0.3).move_to(UP * 0.6)
        self.act(self.tr("7.1", f=0.0), LaggedStart(*[FadeIn(c, scale=0.85) for c in cards], lag_ratio=0.15), d=1.6)
        # 7.2 开关
        self.act(self.tr("7.2", 0, 0.0), *[FadeOut(m) for m in list(self.mobjects)], d=0.6)
        chips = VGroup(*[VGroup(RoundedRectangle(corner_radius=0.3, width=2.2, height=0.7, stroke_color=WHITE, stroke_width=3), T(w, 28)) for w in ["math", "code", "planning"]])
        for c in chips:
            c[1].move_to(c[0])
        chips.arrange(RIGHT, buff=0.4).move_to(UP * 3.2)
        self.act(self.tr("7.2", 0, 0.2), LaggedStart(*[FadeIn(c, shift=UP * 0.15) for c in chips], lag_ratio=0.3), d=1.4)
        track = RoundedRectangle(corner_radius=0.5, width=2.4, height=1.0, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.2).move_to(LEFT * 3.0 + UP * 0.9)
        knob = Circle(radius=0.4, stroke_width=0, fill_color=WHITE, fill_opacity=1).move_to(track.get_left() + RIGHT * 0.55)
        off = T("OFF", 30, GREY).next_to(track, DOWN, buff=0.3)
        ml = T("thinking mode", 32, WHITE).next_to(track, UP, buff=0.35)
        self.act(self.tr("7.2", 1, 0.0), FadeIn(track), FadeIn(knob), FadeIn(off), FadeIn(ml), d=0.6)
        on = T("ON", 30, GREEN).move_to(off)
        self.act(self.tr("7.2", 1, 0.6), knob.animate.move_to(track.get_right() + LEFT * 0.55), track.animate.set_stroke(GREEN).set_fill(GREEN, 0.3),
                 FadeOut(off), FadeIn(on), d=0.5)
        st = VGroup(*[sq(BLUE, 0.3, 0.3, 2) for _ in range(16)]).arrange(RIGHT, buff=0.08).move_to(RIGHT * 2.6 + UP * 0.9)
        self.act(self.tr("7.2", 2, 0.0), LaggedStart(*[FadeIn(s, scale=0.4) for s in st], lag_ratio=0.15), d=2.4)
        cap = T("the same kind of machine, given time to think", 32, BLUE).move_to(DOWN * 1.0)
        self.act(self.tr("7.2", 2, 0.3), FadeIn(cap), d=0.6)
        # 7.3 会思考不等于知道
        self.act(self.tr("7.3", 0, 0.0), *[FadeOut(m) for m in list(self.mobjects)], d=0.6)
        st2 = VGroup(*[sq(BLUE, 0.34, 0.3, 2) for _ in range(14)]).arrange(RIGHT, buff=0.1).move_to(LEFT * 1.5 + UP * 1.2)
        ans = VGroup(RoundedRectangle(corner_radius=0.12, width=2.4, height=1.1, stroke_color=RED, stroke_width=4, fill_color=RED, fill_opacity=0.22),
                     T("answer", 30, RED)).move_to(RIGHT * 5.0 + UP * 1.2)
        ans[1].move_to(ans[0])
        l1 = T("careful reasoning", 28, BLUE).next_to(st2, UP, buff=0.4)
        self.act(self.tr("7.3", 0, 0.3), LaggedStart(*[FadeIn(s, scale=0.5) for s in st2], lag_ratio=0.08), FadeIn(l1), d=1.6)
        self.act(self.tr("7.3", 2, 0.0), FadeIn(ans, scale=0.8), d=0.7)
        l2 = T("can still be wrong", 30, RED).next_to(ans, DOWN, buff=0.3)
        self.act(self.tr("7.3", 2, 0.4), FadeIn(l2), d=0.5)
        ck = T("check anything that matters", 36, YELLOW).move_to(DOWN * 1.4)
        self.act(self.tr("7.3", 3, 0.0), FadeIn(ck, shift=UP * 0.15), d=0.7)
        # 7.4 问题
        self.act(self.tr("7.4", 0, 0.0), *[FadeOut(m) for m in list(self.mobjects)], d=0.6)
        q = Text("\"wait, let me check that\"", font=MONO, font_size=34, color=BLUE).move_to(UP * 2.6)
        self.act(self.tr("7.4", 1, 0.0), FadeIn(q), d=0.8)
        b1 = VGroup(RoundedRectangle(corner_radius=0.15, width=5.6, height=1.5, stroke_color=WHITE, stroke_width=4, fill_color=WHITE, fill_opacity=0.08),
                    Text("THINKING", font=SERIF, font_size=50, color=WHITE)).move_to(LEFT * 3.4 + UP * 0.6)
        b2 = VGroup(RoundedRectangle(corner_radius=0.15, width=5.6, height=1.5, stroke_color=WHITE, stroke_width=4, fill_color=WHITE, fill_opacity=0.08),
                    Text("PREDICTING", font=SERIF, font_size=50, color=WHITE)).move_to(RIGHT * 3.4 + UP * 0.6)
        b1[1].move_to(b1[0]); b2[1].move_to(b2[0])
        self.act(self.tr("7.4", 2, 0.0), FadeIn(b1, shift=RIGHT * 0.2), FadeIn(b2, shift=LEFT * 0.2), d=0.9)
        cur = Rectangle(width=0.07, height=1.1, stroke_width=0, fill_color=WHITE, fill_opacity=1).move_to(UP * 0.6)
        cur.add_updater(lambda m: m.set_opacity(1 if int(self.now() * 2) % 2 == 0 else 0.1))
        self.add(cur)
        cm = T("tell me in the comments", 34, GREY).move_to(DOWN * 1.6)
        self.act(self.tr("7.4", 3, 0.0), FadeIn(cm), d=0.7)
        # 片尾慢收
        self.dump_marks()
        self.go(self.dur - 1.3)
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=1.0)
        self.go(self.dur)
