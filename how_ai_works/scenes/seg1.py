# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from common import *


class Seg1(Seg):
    SEG = "1"

    def construct(self):
        # 1.1 一句话
        pieces = ["How", "does", "AI", "work", "?"]
        txt = VGroup(*[Text(p, font=SERIF, font_size=72, color=WHITE) for p in pieces]).arrange(RIGHT, buff=0.32, aligned_edge=DOWN)
        txt[-1].shift(LEFT * 0.2)
        txt.move_to(UP * 2.35)
        cap = T("WHAT THE MODEL SEES", 22, GREY).to_edge(UP, buff=0.3).shift(LEFT * 0 + DOWN * 0.1)
        self.act(self.tr("1.1", 0, 0.05), Write(txt), FadeIn(cap), d=1.6)

        # 1.2 切成 token
        ids = ["4438", "1587", "15592", "990", "30"]
        toks = VGroup(*[tok(p, BLUE, w=max(1.25, 0.34 * max(len(p), len(i)) + 0.85), h=0.9, size=32) for p, i in zip(pieces, ids)]).arrange(RIGHT, buff=0.3)
        toks.move_to(UP * 0.55)
        divs = VGroup()
        for a, b in zip(txt[:-1], txt[1:]):
            x = (a.get_right()[0] + b.get_left()[0]) / 2
            divs.add(Line(UP * 2.95 + RIGHT * x, UP * 1.8 + RIGHT * x, color=BLUE, stroke_width=3))
        self.act(self.tr("1.2", f=0.1), Create(divs), d=0.5)
        self.act(self.tr("1.2", f=0.45), *[ReplacementTransform(txt[i].copy(), toks[i]) for i in range(5)], d=1.2)

        # 1.3 尺寸线
        brace = Brace(toks[3], DOWN, color=YELLOW, buff=0.15)
        lab1 = T("≈ 4 characters", 30, YELLOW).next_to(brace, DOWN, buff=0.2)
        lab2 = T("≈ ¾ of a word", 30, YELLOW).next_to(lab1, DOWN, buff=0.15)
        self.act_mark("4 characters (1.3)", self.wt("1.3", 0, "four"), GrowFromCenter(brace), FadeIn(lab1), d=0.5)
        self.act_mark("3/4 of a word (1.3)", self.wt("1.3", 1, "three"), FadeIn(lab2), d=0.5)

        # 1.4 换成编号
        new_txt = [Text(i, font=MONO, font_size=32, color=BLUE).move_to(toks[k][1]) for k, i in enumerate(ids)]
        tg = illus("IDs illustrative")
        self.act(self.tr("1.4", f=0.05), FadeOut(brace), FadeOut(lab1), FadeOut(lab2),
                 *[Transform(toks[k][1], new_txt[k]) for k in range(5)], FadeIn(tg), d=1.4)

        # 1.5 原句消失，只剩数字
        self.act(self.tr("1.5", 0, 0.1), FadeOut(txt), FadeOut(divs), FadeOut(cap), toks.animate.scale(1.25).move_to(UP * 1.0), d=1.2)
        only = T("numbers only", 28, GREY).next_to(toks, DOWN, buff=0.55)
        self.act(self.tr("1.5", 1, 0.0), FadeIn(only), d=0.6)

        # 1.6 strawberry
        self.act(self.tr("1.6", 0, 0.0), FadeOut(toks), FadeOut(only), FadeOut(tg), d=0.5)
        groups = []
        for part in ["str", "aw", "berry"]:
            groups.append(VGroup(*[Text(c, font=MONO, font_size=60, color=WHITE) for c in part]).arrange(RIGHT, buff=0.12))
        word = VGroup(*groups).arrange(RIGHT, buff=0.35).move_to(UP * 1.2 + LEFT * 0.8)
        self.act(self.tr("1.6", 0, 0.25), LaggedStart(*[FadeIn(g, shift=UP * 0.2) for g in groups], lag_ratio=0.2), d=1.0)
        q = T("How many r's?", 34, WHITE).next_to(word, UP, buff=0.55)
        self.act(self.tr("1.6", 1, 0.0), FadeIn(q), d=0.5)
        boxes = VGroup()
        ids2 = ["496", "675", "15717"]
        for g, i in zip(groups, ids2):
            b = RoundedRectangle(corner_radius=0.08, width=g.width + 0.3, height=g.height + 0.5, stroke_color=BLUE, stroke_width=3,
                                 fill_color="#1E3540", fill_opacity=1).move_to(g)
            t = Text(i, font=MONO, font_size=34, color=BLUE).move_to(b)
            boxes.add(VGroup(b, t))
        self.act(self.tr("1.6", 2, 0.0), *[FadeIn(b) for b in boxes], d=0.8)
        qm = Text("?", font=SERIF, font_size=120, color=YELLOW).next_to(word, RIGHT, buff=0.9)
        tg2 = illus("IDs illustrative")
        self.act(self.tr("1.6", 2, 0.5), FadeIn(qm, scale=0.6), FadeIn(tg2), d=0.6)
        self.finish()
