# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from common import *


def doc_box(color=WHITE, w=3.4, h=2.0, lines=3, fill=0.1):
    b = RoundedRectangle(corner_radius=0.12, width=w, height=h, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=fill)
    ls = VGroup(*[Line(LEFT * (w / 2 - 0.35), RIGHT * (w / 2 - 0.35 - (0.6 if i == lines - 1 else 0)), stroke_color=color, stroke_width=4, stroke_opacity=0.7)
                  for i in range(lines)]).arrange(DOWN, buff=0.3).move_to(b)
    return VGroup(b, ls)


class Seg4(Seg):
    SEG = "4"

    def construct(self):
        # 4.1
        cap = T("B A S E   M O D E L", 28, GREY).move_to(UP * 3.2)
        blk = RoundedRectangle(corner_radius=0.2, width=6.8, height=1.6, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.15).move_to(UP * 1.3)
        bt = Text("predict the next word", font=SERIF, font_size=44, color=BLUE).move_to(blk)
        self.act(self.tr("4.1", f=0.05), FadeIn(cap), FadeIn(blk, scale=0.9), Write(bt), d=1.6)

        # 4.2 互联网自动补全
        self.act(self.tr("4.2", 0, 0.0), blk.animate.scale(0.55).move_to(LEFT * 4.4 + UP * 3.15), bt.animate.scale(0.55).move_to(LEFT * 4.4 + UP * 3.15), d=0.8)
        prompt = Text("What is the capital of France?", font=MONO, font_size=30, color=WHITE).move_to(UP * 1.7 + LEFT * 0.4)
        lines = ["What is the capital of Germany?", "What is the capital of Spain?", "What is the capital of Italy?", "What is the capital of Japan?"]
        outs = VGroup(*[Text(l, font=MONO, font_size=30, color=BLUE) for l in lines]).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        outs.next_to(prompt, DOWN, buff=0.5, aligned_edge=LEFT)
        you = T("you", 24, GREY).next_to(prompt, UP, buff=0.2, aligned_edge=LEFT)
        mod = T("model keeps going", 24, BLUE).next_to(outs, UP, buff=0.12, aligned_edge=LEFT).shift(UP * 0.0)
        mod.move_to(prompt.get_left() + DOWN * 0.7, aligned_edge=LEFT)
        outs.next_to(mod, DOWN, buff=0.2, aligned_edge=LEFT)
        self.act(self.tr("4.2", 0, 0.3), FadeIn(you), Write(prompt), FadeIn(illus()), d=1.4)
        self.act(self.tr("4.2", 1, 0.2), FadeIn(mod), LaggedStart(*[Write(o) for o in outs], lag_ratio=0.55), d=3.3)

        # 4.3 大圆 + 小圆
        self.act(self.tr("4.3", f=0.0), *[FadeOut(m) for m in list(self.mobjects)], d=0.6)
        big_c = Circle(radius=1.9, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.15).move_to(LEFT * 3.4 + UP * 0.9)
        small_c = Circle(radius=0.6, stroke_color=WHITE, stroke_width=4, fill_color=WHITE, fill_opacity=0.15).move_to(RIGHT * 3.4 + UP * 0.9)
        l_big = T("round 1: predict the next word", 28, BLUE).next_to(big_c, DOWN, buff=0.35)
        l_small = T("round 2: much smaller", 28, WHITE).next_to(small_c, DOWN, buff=0.35)
        self.act(self.tr("4.3", f=0.05), GrowFromCenter(big_c), FadeIn(l_big), d=1.0)
        self.act(self.tr("4.3", f=0.5), GrowFromCenter(small_c), FadeIn(l_small), d=0.9)

        # 4.4 人写示范 + 排名
        self.act(self.tr("4.4", 0, 0.0), *[FadeOut(m) for m in list(self.mobjects)], d=0.5)
        A = doc_box(WHITE).move_to(LEFT * 3.2 + UP * 0.9)
        B = doc_box(WHITE, lines=3).move_to(RIGHT * 3.2 + UP * 0.9)
        la = T("reply A", 26, GREY).next_to(A, UP, buff=0.25)
        lb = T("reply B", 26, GREY).next_to(B, UP, buff=0.25)
        ppl = person(WHITE, 1.4).move_to(UP * 0.9 + DOWN * 0.0)
        self.act(self.tr("4.4", 0, 0.3), FadeIn(A), FadeIn(B), FadeIn(la), FadeIn(lb), FadeIn(ppl), d=1.2)
        arr = Arrow(ppl.get_left() + LEFT * 0.1, A.get_right(), buff=0.12, color=WHITE, stroke_width=4)
        self.act(self.tr("4.4", 1, 0.2), Create(arr), d=0.5)
        pref = T("preferred", 28, GREEN).next_to(A, DOWN, buff=0.3)
        self.act(self.tr("4.4", 1, 0.55), A[0].animate.set_stroke(GREEN).set_fill(GREEN, 0.18), FadeIn(pref), d=0.7)

        # 4.5 写 vs 选
        self.act(self.tr("4.5", 0, 0.0), *[FadeOut(m) for m in list(self.mobjects)], d=0.5)
        ttl = T("R A N K I N G", 28, GREY).move_to(UP * 3.2)
        self.act(self.tr("4.5", 0, 0.1), FadeIn(ttl), d=0.5)
        p1 = person(WHITE, 1.3).move_to(LEFT * 5.3 + UP * 1.0)
        blank = RoundedRectangle(corner_radius=0.1, width=2.4, height=2.2, stroke_color=WHITE, stroke_width=3, fill_opacity=0.0).move_to(LEFT * 2.8 + UP * 1.0)
        q = Text("?", font=SERIF, font_size=72, color=YELLOW).move_to(blank)
        t1 = T("write the perfect answer", 26, WHITE).next_to(blank, DOWN, buff=0.7).shift(LEFT * 1.2)
        p2 = person(WHITE, 1.3).move_to(RIGHT * 1.2 + UP * 1.0)
        bx1 = doc_box(WHITE, w=1.9, h=1.6, lines=2).move_to(RIGHT * 3.4 + UP * 1.0)
        bx2 = doc_box(WHITE, w=1.9, h=1.6, lines=2).move_to(RIGHT * 5.7 + UP * 1.0)
        t2 = T("pick the better one", 26, WHITE).next_to(bx1, DOWN, buff=0.7).shift(RIGHT * 1.15)
        self.act(self.tr("4.5", 1, 0.0), FadeIn(p1), FadeIn(blank), FadeIn(q), FadeIn(t1), d=0.8)
        self.act(self.tr("4.5", 1, 0.5), FadeIn(p2), FadeIn(bx1), FadeIn(bx2), FadeIn(t2), d=0.8)
        ck = check(bx1.get_corner(UR) + LEFT * 0.35 + DOWN * 0.35, s=2.6)
        hard = T("hard", 30, RED).move_to(LEFT * 2.8 + DOWN * 1.9)
        easy = T("much easier", 30, GREEN).move_to(RIGHT * 4.5 + DOWN * 1.9)
        self.act(self.tr("4.5", 2, 0.0), Create(ck), bx1[0].animate.set_stroke(GREEN), FadeIn(hard), FadeIn(easy), d=0.9)

        # 4.6 / 4.7 1.3B vs 175B
        self.act(self.tr("4.6", 0, 0.0), *[FadeOut(m) for m in list(self.mobjects)], d=0.5)
        sm = Circle(radius=0.75, stroke_color=YELLOW, stroke_width=4, fill_color=YELLOW, fill_opacity=0.15).move_to(LEFT * 3.4 + UP * 1.3)
        bg = Circle(radius=2.0, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.15).move_to(RIGHT * 2.8 + UP * 1.3)
        t_sm = Text("1.3B", font=SERIF, font_size=46, color=YELLOW).move_to(sm)
        t_bg = Text("175B", font=SERIF, font_size=72, color=BLUE).move_to(bg)
        n_sm = T("InstructGPT · 1.3 billion", 26, WHITE).next_to(sm, DOWN, buff=1.55)
        n_bg = T("GPT-3 · 175 billion", 26, WHITE).next_to(bg, DOWN, buff=0.4)
        n_sm.move_to(LEFT * 3.4 + DOWN * 0.95)
        self.act(self.tr("4.6", 0, 0.3), FadeIn(t_bg), FadeIn(bg), FadeIn(n_bg), d=0.8)
        self.act(self.tr("4.6", 1, 0.0), FadeIn(sm), FadeIn(t_sm), FadeIn(n_sm), d=0.8)
        ck2 = check(sm.get_top() + UP * 0.5, YELLOW, s=3.0)
        pr = T("preferred by people", 28, YELLOW).next_to(sm, UP, buff=0.9)
        self.act(self.tr("4.6", 2, 0.0), Create(ck2), FadeIn(pr), d=0.8)
        self.act(self.tr("4.6", 2, 0.6), FadeIn(illus("circles not to scale")), d=0.3)
        dim = DoubleArrow(sm.get_center() + DOWN * 2.4, bg.get_center() + DOWN * 2.4, buff=0.0, color=YELLOW, stroke_width=4, tip_length=0.2)
        dim = Line(LEFT * 3.4 + DOWN * 1.65, RIGHT * 2.8 + DOWN * 1.65, color=YELLOW, stroke_width=4)
        x100 = Text("×100+", font=SERIF, font_size=60, color=YELLOW).move_to(RIGHT * -0.3 + DOWN * 2.05)
        dim.set_z_index(0)
        self.act(self.tr("4.7", f=0.1), Create(dim), d=0.6)
        self.act(self.tr("4.7", f=0.4), FadeIn(x100, scale=0.7), d=0.6)

        # 4.8 PREDICT -> POLISH
        self.act(self.tr("4.8", 0, 0.0), *[FadeOut(m) for m in list(self.mobjects)], d=0.5)
        yr = Text("2023", font=SERIF, font_size=60, color=GREY).move_to(UP * 2.9)
        pb = VGroup(RoundedRectangle(corner_radius=0.2, width=4.2, height=1.5, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.15),
                    Text("PREDICT", font=SERIF, font_size=48, color=BLUE)).move_to(LEFT * 3.4 + UP * 0.8)
        pb[1].move_to(pb[0])
        ob = VGroup(RoundedRectangle(corner_radius=0.2, width=4.2, height=1.5, stroke_color=WHITE, stroke_width=4, fill_color=WHITE, fill_opacity=0.1),
                    Text("POLISH", font=SERIF, font_size=48, color=WHITE)).move_to(RIGHT * 3.4 + UP * 0.8)
        ob[1].move_to(ob[0])
        arrow = Arrow(pb.get_right(), ob.get_left(), buff=0.15, color=WHITE, stroke_width=5)
        c1 = T("pre-training", 26, GREY).next_to(pb, DOWN, buff=0.3)
        c2 = T("human feedback", 26, GREY).next_to(ob, DOWN, buff=0.3)
        self.act(self.tr("4.8", 0, 0.2), FadeIn(yr), d=0.6)
        self.act(self.tr("4.8", 1, 0.0), FadeIn(pb), FadeIn(c1), d=0.7)
        self.act(self.tr("4.8", 1, 0.5), Create(arrow), FadeIn(ob), FadeIn(c2), d=0.9)

        # 4.9 然后，故事变了
        qm = Text("?", font=SERIF, font_size=140, color=YELLOW).move_to(UP * 0.8 + RIGHT * 7.0 * 0)
        self.act(self.tr("4.9", f=0.0), FadeOut(yr), ob.animate.shift(LEFT * 1.6), arrow.animate.shift(LEFT * 0.8), pb.animate.shift(LEFT * 1.6), c1.animate.shift(LEFT * 1.6), c2.animate.shift(LEFT * 1.6), d=0.6)
        qm.move_to(RIGHT * 4.3 + UP * 0.8)
        arrow2 = Arrow(ob.get_right() + LEFT * 0.0, qm.get_left() + LEFT * 0.2, buff=0.15, color=WHITE, stroke_width=5)
        self.play(Create(arrow2), FadeIn(qm, scale=0.5), run_time=0.5)
        self.finish()
