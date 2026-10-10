# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from common import *


class Seg2(Seg):
    SEG = "2"

    def construct(self):
        words = ["The", "cat", "sat", "on", "the"]
        row = VGroup(*[tok(w, BLUE, size=30, h=0.8) for w in words]).arrange(RIGHT, buff=0.2)
        qbox = tok("?", YELLOW, w=0.9, size=34, h=0.8, dashed=True)
        row.add(qbox)
        row.arrange(RIGHT, buff=0.2).move_to(UP * 2.0)
        tg = illus()
        # 2.1
        self.act(self.tr("2.1", 0, 0.1), LaggedStart(*[FadeIn(t, shift=RIGHT * 0.2) for t in row[:5]], lag_ratio=0.15), d=1.2)
        self.act(self.tr("2.1", 1, 0.0), FadeIn(qbox, scale=0.7), FadeIn(tg), d=0.6)
        cap = T("given everything so far, what comes next?", 28, GREY).move_to(UP * 0.75)
        self.act(self.tr("2.1", 2, 0.0), FadeIn(cap), d=0.6)

        # 2.2 概率柱
        items = ["mat", "floor", "sofa", "dog", "banana"]
        vals = [0.62, 0.21, 0.09, 0.05, 0.001]
        ch = prob_chart(items, vals, hi=-1, top=-0.15, gap=0.55, left=-1.2, color=BLUE, show_vals=False)
        self.act(self.tr("2.2", f=0.05), FadeOut(cap), *[FadeIn(r[0]) for r in ch],
                 LaggedStart(*[GrowFromEdge(r[1], LEFT) for r in ch], lag_ratio=0.2), d=1.8)
        # 2.3 mat 高 / floor 低 / banana 几乎零
        self.act(self.tr("2.3", 0, 0.45), ch[0][1].animate.set_fill(YELLOW, 1), ch[0][2].animate.set_opacity(1).set_color(YELLOW), d=0.5)
        self.act(self.tr("2.3", 1, 0.0), ch[1][2].animate.set_opacity(1), ch[2][2].animate.set_opacity(1), ch[3][2].animate.set_opacity(1), d=0.4)
        self.act(self.tr("2.3", 1, 0.55), ch[4][2].animate.set_opacity(1), Indicate(ch[4][0], color=RED, scale_factor=1.15), d=0.6)

        # 2.4 选一个、接上、重复
        def step(word, new_items, new_vals, dur):
            nonlocal row, qbox, ch
            w = tok(word, BLUE, size=30, h=0.8)
            w.move_to(qbox)
            newq = tok("?", YELLOW, w=0.9, size=34, h=0.8, dashed=True).next_to(qbox, RIGHT, buff=0.2)
            shift = -(w.width + 0.2) / 2
            nch = prob_chart(new_items, new_vals, hi=0, top=-0.15, gap=0.55, left=-1.2, color=BLUE)
            self.play(FadeOut(qbox), FadeIn(w, scale=0.6), FadeIn(newq, scale=0.7),
                      *[Transform(a, b) for a, b in zip(ch, nch)], run_time=dur)
            row.remove(qbox)
            row.add(w, newq)
            qbox = newq
            self.play(row.animate.shift(RIGHT * shift), run_time=0.2)

        # 先把 mat 飞进句尾
        self.go(self.tr("2.4", f=0.0))
        fly = tok("mat", YELLOW, size=30, h=0.8).move_to(ch[0][0])
        self.add(fly)
        self.play(fly.animate.move_to(qbox), FadeOut(qbox), run_time=0.7)
        fly[0].set_stroke(BLUE); fly[0].set_fill(BLUE, 0.18); fly[1].set_color(BLUE)
        newq = tok("?", YELLOW, w=0.9, size=34, h=0.8, dashed=True).next_to(fly, RIGHT, buff=0.2)
        row.remove(qbox)
        row.add(fly, newq)
        qbox = newq
        nch = prob_chart([".", "and", ",", "because", "banana"], [0.71, 0.14, 0.08, 0.04, 0.001], hi=0, top=-0.15, gap=0.55, left=-1.2)
        self.play(FadeIn(qbox, scale=0.7), row.animate.shift(LEFT * 0.5), *[Transform(a, b) for a, b in zip(ch, nch)], run_time=0.8)
        step(".", ["The", "It", "She", "Then", "banana"], [0.46, 0.22, 0.12, 0.09, 0.001], 0.7)
        step("The", ["cat", "dog", "mat", "sun", "banana"], [0.4, 0.3, 0.1, 0.08, 0.001], 0.5)

        # 2.5 拉远：方块像流水一样生长
        stream = VGroup()
        for r in range(7):
            for c in range(30):
                s = sq(BLUE, 0.3, 0.25, 2)
                s.move_to(RIGHT * (-5.5 + c * 0.38) + UP * (1.7 - r * 0.62))
                stream.add(s)
        self.act(self.tr("2.5", 0, 0.0), FadeOut(ch), FadeOut(row), FadeOut(tg), d=0.6)
        self.act(self.tr("2.5", 0, 0.5), LaggedStart(*[FadeIn(s, scale=0.5) for s in stream[:90]], lag_ratio=0.025), d=4.0)

        # 2.6 计数器 1 -> 1,000
        c, a = counter(lambda v: f"{int(round(v)):,}", 1, 1000, UP * 3.0 + LEFT * 0.6, 60, BLUE, edge=None)
        lab = T("predictions", 28, GREY)
        lab.move_to(RIGHT * 1.3 + UP * 2.85, aligned_edge=LEFT)
        self.go(self.tr("2.6", 0, 0.0))
        self.add(c, lab)
        self.act(self.tr("2.6", 0, 0.0), a, LaggedStart(*[FadeIn(s, scale=0.5) for s in stream[90:]], lag_ratio=0.02), d=6.5)

        # 2.7 分叉
        self.act(self.tr("2.7", 0, 0.0), FadeOut(stream), FadeOut(c), FadeOut(lab), d=0.6)
        start = VGroup(*[tok(w, BLUE, size=24, h=0.7) for w in words]).arrange(RIGHT, buff=0.12).scale(0.8)
        start.move_to(LEFT * 4.6 + UP * 0.5)
        self.act(self.tr("2.7", 0, 0.3), FadeIn(start), d=0.6)
        top_chain = VGroup(*[tok(w, BLUE, size=24, h=0.7) for w in ["mat", "."]]).arrange(RIGHT, buff=0.12).scale(0.8)
        bot_chain = VGroup(*[tok(w, GREEN, size=24, h=0.7) for w in ["sofa", "and", "purred", "."]]).arrange(RIGHT, buff=0.12).scale(0.8)
        top_chain.move_to(RIGHT * 1.2 + UP * 1.7, aligned_edge=LEFT).align_to(start, LEFT).shift(RIGHT * 6.0 - RIGHT * 0)
        top_chain.move_to(RIGHT * 2.9 + UP * 1.7)
        bot_chain.move_to(RIGHT * 2.9 + DOWN * 0.75)
        a1 = Arrow(start.get_right() + UP * 0.1, top_chain.get_left() + LEFT * 0.1, color=GREY, buff=0.1, stroke_width=3, max_tip_length_to_length_ratio=0.12)
        a2 = Arrow(start.get_right() + DOWN * 0.1, bot_chain.get_left() + LEFT * 0.1, color=GREY, buff=0.1, stroke_width=3, max_tip_length_to_length_ratio=0.12)
        rnd = T("a little randomness", 28, YELLOW).next_to(start, DOWN, buff=0.55)
        self.act(self.tr("2.7", 1, 0.0), FadeIn(rnd, scale=0.9), d=0.6)
        self.act(self.tr("2.7", 2, 0.0), Create(a1), Create(a2), d=0.6)
        self.act(self.tr("2.7", 2, 0.3), LaggedStart(*[FadeIn(t, shift=RIGHT * 0.15) for t in top_chain], lag_ratio=0.3),
                 LaggedStart(*[FadeIn(t, shift=RIGHT * 0.15) for t in bot_chain], lag_ratio=0.3), d=2.2)
        l1 = T("answer 1", 24, GREY).next_to(top_chain, UP, buff=0.25)
        l2 = T("answer 2", 24, GREY).next_to(bot_chain, DOWN, buff=0.25)
        self.act(self.tr("2.7", 2, 0.85), FadeIn(l1), FadeIn(l2), d=0.5)

        # 2.8 回到柱状图
        self.act(self.tr("2.8", 0, 0.0), *[FadeOut(m) for m in list(self.mobjects)], d=0.6)
        big_chart = prob_chart(["mat", "floor", "sofa", "dog", "banana"], [0.62, 0.21, 0.09, 0.05, 0.001], hi=0,
                               left=-2.6, top=1.3, gap=0.7, scale=6.0, size=30)
        title = Text("where do the probabilities come from?", font=SERIF, font_size=44, color=WHITE).move_to(UP * 3.0)
        self.act(self.tr("2.8", 0, 0.12), FadeIn(big_chart), FadeIn(illus()), d=0.8)
        self.act(self.tr("2.8", 1, 0.0), Write(title), big_chart.animate.scale(1.08).shift(DOWN * 0.1), d=1.5)
        self.finish()
