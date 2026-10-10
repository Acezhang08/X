# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from common import *


class Seg6(Seg):
    SEG = "6"

    def construct(self):
        base = Text("The cat sat on the", font=SERIF, font_size=72, color=WHITE)
        mat = Text("mat", font=SERIF, font_size=72, color=YELLOW)
        grp = VGroup(base, mat).arrange(RIGHT, buff=0.3, aligned_edge=DOWN).move_to(UP * 0.9)
        blank = Line(ORIGIN, RIGHT * 1.6, color=WHITE, stroke_width=4).move_to(mat).align_to(base, DOWN).shift(DOWN * 0.05)
        self.act(self.tr("6.1", f=0.1), FadeIn(base), Create(blank), d=1.0)
        self.act(self.tr("6.2", 0, 0.45), FadeOut(blank), FadeIn(mat, shift=UP * 0.2), d=0.5)
        # 6.3
        lab1 = T("not what someone on the internet would write next", 30, GREY).move_to(DOWN * 1.2)
        self.act(self.tr("6.3", 0, 0.1), mat.animate.scale(1.0), d=0.2)
        self.act(self.tr("6.3", 1, 0.0), FadeIn(lab1), d=0.6)
        steps = VGroup(*[sq(BLUE, 0.4, 0.25, 2).move_to(RIGHT * i * 0.5) for i in range(9)]).move_to(RIGHT * -0.8 + UP * 0.9)
        answer = VGroup(RoundedRectangle(corner_radius=0.12, width=2.2, height=1.1, stroke_color=GREEN, stroke_width=4, fill_color=GREEN, fill_opacity=0.2),
                        T("answer", 30, GREEN)).move_to(RIGHT * 4.9 + UP * 0.9)
        answer[1].move_to(answer[0])
        lab2 = T("the steps that lead to a right answer", 30, BLUE).move_to(DOWN * 1.2)
        self.act(self.tr("6.3", 2, 0.0), FadeOut(base), FadeOut(lab1), ReplacementTransform(mat, steps), FadeIn(answer), FadeIn(lab2), d=1.4)
        # 6.4
        arr = Arrow(steps.get_left() + LEFT * 0.3, answer.get_left() + LEFT * 0.15, buff=0.0, color=YELLOW, stroke_width=8)
        arr.shift(DOWN * 0.5)
        cap = T("next-word prediction, pointed at a goal", 34, YELLOW).move_to(DOWN * 2.0)
        self.act(self.tr("6.4", 0, 0.5), FadeOut(lab2), d=0.4)
        self.act(self.tr("6.4", 1, 0.0), GrowArrow(arr), FadeIn(cap), answer[0].animate.set_fill(GREEN, 0.4), d=1.2)
        # 6.5 三级台阶
        specs = [("PREDICT", BLUE, 1.3, "15T tokens", -4.6), ("POLISH", WHITE, 2.3, "1.3B > 175B", 0.0), ("REWARD", GREEN, 3.3, "15.6% → 71%", 4.6)]
        base_y = -2.0
        steps_g = []
        for nm, col, h, num, x in specs:
            r = Rectangle(width=4.1, height=h, stroke_color=col, stroke_width=4, fill_color=col, fill_opacity=0.15).move_to(RIGHT * x + UP * (base_y + h / 2))
            t = Text(nm, font=SERIF, font_size=48, color=col).move_to(r.get_top() + DOWN * 0.55)
            n = Text(num, font=SERIF, font_size=44, color=YELLOW).move_to(r.get_center() + DOWN * 0.1 + (DOWN * 0.15 if h > 2 else DOWN * 0.0))
            if h < 2:
                n.move_to(r.get_center() + DOWN * 0.1)
                t.move_to(r.get_top() + UP * 0.45)
            steps_g.append(VGroup(r, t, n))
        # 第一个台阶随旁白一开始就画出；数字在对应那句话里出现
        self.act_mark("PREDICT step (6.5)", self.tr("6.5", 0, 0.0), *[FadeOut(m) for m in list(self.mobjects)],
                      FadeIn(steps_g[0][0], shift=UP * 0.3), FadeIn(steps_g[0][1]), d=0.5)
        self.act(self.wt("6.5", 1, "trillions"), FadeIn(steps_g[0][2], scale=0.8), d=0.4)
        self.act(self.wt("6.5", 2, "second"), FadeIn(steps_g[1][0], shift=UP * 0.3), FadeIn(steps_g[1][1]), d=0.6)
        self.act(self.wt("6.5", 2, "preferences"), FadeIn(steps_g[1][2], scale=0.8), d=0.4)
        self.act(self.wt("6.5", 3, "third"), FadeIn(steps_g[2][0], shift=UP * 0.3), FadeIn(steps_g[2][1]), d=0.6)
        self.act(self.wt("6.5", 3, "rewarded"), FadeIn(steps_g[2][2], scale=0.8), d=0.4)
        # 6.6
        self.act(self.tr("6.6", 1, 0.0), steps_g[0].animate.set_opacity(0.25), steps_g[1].animate.set_opacity(0.25),
                 steps_g[2][0].animate.set_fill(GREEN, 0.4).set_stroke(GREEN, 7), d=0.9)
        self.finish()
