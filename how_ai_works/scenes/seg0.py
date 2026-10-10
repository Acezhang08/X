# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from common import *


class Seg0(Seg):
    SEG = "0"

    def construct(self):
        # 0.1 打字 + 光标 + mat
        base = Text("The cat sat on the", font=SERIF, font_size=72, color=WHITE)
        blank = Line(ORIGIN, RIGHT * 1.6, color=WHITE, stroke_width=4)
        sent = VGroup(base, blank).arrange(RIGHT, buff=0.3, aligned_edge=DOWN)
        sent.move_to(UP * 0.6)
        blank.align_to(base, DOWN).shift(DOWN * 0.05)
        cursor = Rectangle(width=0.06, height=0.9, color=WHITE, fill_color=WHITE, fill_opacity=1, stroke_width=0)
        cursor.move_to(blank.get_left() + RIGHT * 0.1 + UP * 0.45)
        cursor.add_updater(lambda m: m.set_opacity(1 if int(self.now() * 2) % 2 == 0 else 0))
        self.act(0.35, Write(base), Create(blank), d=1.6)
        self.add(cursor)
        mat = Text("mat", font=SERIF, font_size=72, color=YELLOW).next_to(base, RIGHT, buff=0.3)
        mat.align_to(base, DOWN)
        self.go(self.tr("0.1", f=0.78))
        cursor.clear_updaters()
        self.play(FadeOut(cursor), FadeOut(blank), FadeIn(mat, shift=UP * 0.2), run_time=0.4)

        # 0.2 句子留在画面中央：白色 60% 透明度，句末一条短竖线表示"讲到这里就停了"
        full = VGroup(base, mat)
        stop = Line(DOWN * 0.5, UP * 0.5, color=WHITE, stroke_width=7).move_to(mat.get_right() + RIGHT * 0.4)
        stop.set_y(base.get_center()[1])
        cap02 = T("where most explanations stop", 34, GREY).move_to(UP * 0.6 + DOWN * 1.3)
        self.act(self.tr("0.2", 0, 0.05), full.animate.set_color(WHITE).set_opacity(0.6), Create(stop), d=0.8)
        self.act(self.tr("0.2", 1, 0.1), FadeIn(cap02, shift=UP * 0.1), d=0.7)

        # 0.3 试卷：15 个方块
        row = VGroup(*[sq(WHITE, 0.5, 0.12, 3) for _ in range(15)]).arrange(RIGHT, buff=0.14).move_to(UP * 0.6)
        lab = T("AIME 2024  ·  15 problems", 32, WHITE).next_to(row, UP, buff=0.5)
        self.act(self.tr("0.3", 0, 0.0), FadeOut(full), FadeOut(stop), FadeOut(cap02),
                 LaggedStart(*[FadeIn(s, scale=0.6) for s in row], lag_ratio=0.05), FadeIn(lab), d=1.6)
        note = T("OpenAI · September 2024", 24, GREY).next_to(row, DOWN, buff=0.5)
        self.act(self.tr("0.3", 1, 0.0), FadeIn(note), d=0.6)

        # 0.4 左边：GPT-4o 12%
        def grid():
            g = VGroup(*[sq(WHITE, 0.5, 0.12, 3) for _ in range(15)]).arrange_in_grid(3, 5, buff=0.14)
            return g
        gl, gr = grid().move_to(LEFT * 3.6 + UP * 0.5), grid().move_to(RIGHT * 3.6 + UP * 0.5)
        ll, lr = T("GPT-4o", 34, WHITE).next_to(gl, UP, buff=0.4), T("o1", 34, WHITE).next_to(gr, UP, buff=0.4)
        self.act(self.tr("0.4", f=0.0), ReplacementTransform(row, gl), FadeOut(lab), FadeOut(note), FadeIn(ll), d=1.0)
        c1, a1 = counter(lambda v: f"{int(round(v))}%", 0, 12, LEFT * 3.6 + DOWN * 1.65, 80, YELLOW)
        gl[0].set_fill(GREEN, 0.7).set_stroke(GREEN)
        part = Rectangle(width=0.5 * 0.8, height=0.5, stroke_width=0, fill_color=GREEN, fill_opacity=0.7)
        part.align_to(gl[1], LEFT).align_to(gl[1], UP)
        self.act(self.wt("0.4", 0, "solved"), FadeIn(part), gl[0].animate.set_fill(GREEN, 0.7), d=0.3)
        ta, tb = self.wt("0.4", 0, "twelve"), self.wt("0.4", 0, "percent", end=True)
        self.go(ta)
        self.add(c1)
        self.act_mark("12% (0.4)", ta, a1, d=max(0.3, tb - ta))

        # 0.5 右边：o1 74%
        c2, a2 = counter(lambda v: f"{int(round(v))}%", 0, 74, RIGHT * 3.6 + DOWN * 1.65, 80, YELLOW)
        self.act(self.tr("0.5", f=0.0), FadeIn(gr, scale=0.9), FadeIn(lr), d=0.6)
        ta, tb = self.wt("0.5", 0, "seventy"), self.wt("0.5", 0, "percent", end=True)
        self.go(ta)
        self.add(c2)
        self.act_mark("74% (0.5)", ta,
                      LaggedStart(*[gr[i].animate.set_fill(GREEN, 0.7).set_stroke(GREEN) for i in range(11)], lag_ratio=0.08), a2, d=max(0.3, tb - ta))

        # 0.6 思考气泡
        bubble = RoundedRectangle(corner_radius=0.3, width=1.5, height=0.7, stroke_color=BLUE, stroke_width=3,
                                  fill_color=BLUE, fill_opacity=0.15).move_to(RIGHT * 3.6 + UP * 3.15)
        tail = Triangle(color=BLUE, fill_color=BLUE, fill_opacity=0.15, stroke_width=3).scale(0.12).rotate(PI).next_to(bubble, DOWN, buff=-0.02)
        dots = VGroup(*[Dot(radius=0.07, color=BLUE) for _ in range(3)]).arrange(RIGHT, buff=0.2).move_to(bubble)
        self.act(self.tr("0.6", 1, 0.0), FadeIn(bubble, scale=0.7), FadeIn(tail), FadeIn(dots), d=0.6)
        for i, d in enumerate(dots):
            d.add_updater(lambda m, i=i: m.set_opacity(0.35 + 0.65 * (0.5 + 0.5 * np.sin(self.now() * 5 - i * 0.9))))
        self.finish()
