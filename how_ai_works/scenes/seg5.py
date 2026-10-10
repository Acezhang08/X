# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from common import *


def grid15(n_full, part=0.0, scale=1.0):
    g = VGroup(*[sq(WHITE, 0.5, 0.12, 3) for _ in range(15)]).arrange_in_grid(3, 5, buff=0.14)
    extra = VGroup()
    for i in range(n_full):
        g[i].set_fill(GREEN, 0.7).set_stroke(GREEN)
    if part > 0:
        p = Rectangle(width=0.5 * part, height=0.5, stroke_width=0, fill_color=GREEN, fill_opacity=0.7)
        p.align_to(g[n_full], LEFT).align_to(g[n_full], UP)
        extra.add(p)
    return VGroup(g, extra).scale(scale)


def stream(n, color=BLUE, s=0.3, gap=0.38, op=0.3):
    return VGroup(*[sq(color, s, op, 2).move_to(RIGHT * i * gap) for i in range(n)])


def axes(x0, x1, y0, y1, xl, yl):
    ax = VGroup(Line(RIGHT * x0 + UP * y0, RIGHT * x1 + UP * y0, color=WHITE, stroke_width=3),
                Line(RIGHT * x0 + UP * y0, RIGHT * x0 + UP * y1, color=WHITE, stroke_width=3))
    lx = T(xl, 26, GREY).next_to(ax[0], DOWN, buff=0.2).align_to(ax[0], RIGHT)
    ly = T(yl, 26, GREY).move_to(RIGHT * x0 + UP * (y1 + 0.35), aligned_edge=LEFT)
    return VGroup(ax, lx, ly)


class Seg5(Seg):
    SEG = "5"

    def clear(self, t, d=0.5):
        self.act(t, *[FadeOut(m) for m in list(self.mobjects)], d=d)

    def construct(self):
        random.seed(3)
        # 5.1
        gl = grid15(1, 0.8).move_to(LEFT * 3.6 + UP * 1.0)
        gr = grid15(11, 0.1).move_to(RIGHT * 3.6 + UP * 1.0)
        ll = T("GPT-4o", 34).next_to(gl, UP, buff=0.4)
        lr = T("o1", 34).next_to(gr, UP, buff=0.4)
        self.act(self.tr("5.1", 0, 0.0), FadeIn(gl), FadeIn(gr), FadeIn(ll), FadeIn(lr), d=1.0)
        n1 = Text("12%", font=SERIF, font_size=88, color=YELLOW).move_to(LEFT * 3.6 + DOWN * 1.2)
        n2 = Text("74%", font=SERIF, font_size=88, color=YELLOW).move_to(RIGHT * 3.6 + DOWN * 1.2)
        self.act(self.tr("5.1", 1, 0.0), FadeIn(n1, scale=0.8), d=0.5)
        self.act(self.tr("5.1", 1, 0.6), FadeIn(n2, scale=0.8), d=0.5)

        # 5.2 强化学习
        self.clear(self.tr("5.2", 0, 0.0))
        title = Text("REINFORCEMENT LEARNING", font=SERIF, font_size=56, color=WHITE).move_to(UP * 3.0)
        self.act(self.tr("5.2", 0, 0.2), Write(title), d=1.6)
        note = T("OpenAI hasn't published the details", 28, GREY).move_to(UP * 2.1)
        self.act(self.tr("5.2", 2, 0.0), FadeIn(note), d=0.6)
        prob = VGroup(RoundedRectangle(corner_radius=0.12, width=3.4, height=1.5, stroke_color=WHITE, stroke_width=3, fill_color=WHITE, fill_opacity=0.08),
                      Text("x² + 3x = 10", font=MONO, font_size=26, color=WHITE)).move_to(LEFT * 4.6 + DOWN * 0.1)
        prob[1].move_to(prob[0])
        pl = T("math problem", 24, GREY).next_to(prob, UP, buff=0.2)
        ans = VGroup(RoundedRectangle(corner_radius=0.12, width=2.4, height=1.2, stroke_color=GREY, stroke_width=3, fill_opacity=0.0),
                     Text("?", font=SERIF, font_size=60, color=GREY)).move_to(RIGHT * 5.0 + DOWN * 0.1)
        ans[1].move_to(ans[0])
        al = T("final answer", 24, GREY).next_to(ans, UP, buff=0.2)
        self.act(self.tr("5.2", 3, 0.0), FadeIn(note.copy().set_opacity(0)), d=0.1)
        self.act(self.tr("5.2", 3, 0.1), FadeIn(prob), FadeIn(pl), FadeIn(ans), FadeIn(al), d=1.0)

        # 5.3 想多久都行
        st = stream(15).move_to(UP * -0.1 + RIGHT * 0.1)
        thinking = T("thinking", 28, BLUE).next_to(st, UP, buff=0.4)
        a1 = Arrow(prob.get_right(), st.get_left(), buff=0.1, color=GREY, stroke_width=3, max_tip_length_to_length_ratio=0.2)
        self.act(self.tr("5.3", 0, 0.0), FadeOut(note), FadeIn(thinking), d=0.5)
        self.act(self.tr("5.3", 1, 0.0), LaggedStart(*[FadeIn(s, scale=0.4) for s in st], lag_ratio=0.12), d=4.0)
        a2 = Arrow(st.get_right(), ans.get_left(), buff=0.1, color=GREY, stroke_width=3, max_tip_length_to_length_ratio=0.2)
        ans1 = VGroup(RoundedRectangle(corner_radius=0.12, width=2.4, height=1.2, stroke_color=WHITE, stroke_width=3, fill_color=WHITE, fill_opacity=0.1),
                      Text("x = 2", font=MONO, font_size=30, color=WHITE)).move_to(ans)
        ans1[1].move_to(ans1[0])
        self.act(self.tr("5.3", 1, 0.95), Create(a2), Transform(ans, ans1), d=0.6)

        # 5.4 奖励
        att1 = VGroup(prob, pl, st, thinking, ans, al, a2)
        self.act(self.tr("5.4", 0, 0.0), FadeOut(title), att1.animate.scale(0.62).move_to(UP * 2.3), d=0.7)
        self.act(self.tr("5.4", 0, 0.3), ans[0].animate.set_stroke(GREEN).set_fill(GREEN, 0.25), d=0.5)
        plus = Text("+1", font=SERIF, font_size=72, color=GREEN).next_to(ans, RIGHT, buff=0.2)
        self.play(FadeIn(plus, scale=0.5), run_time=0.4)
        prob2 = prob.copy().move_to(att1[0].get_center() + DOWN * 2.6)
        st2 = stream(9).scale(0.62).move_to(st.get_center() + DOWN * 2.6 + LEFT * 0.5)
        ans2 = ans.copy()
        ans2[1].become(Text("x = 5", font=MONO, font_size=30, color=WHITE).scale(0.62).move_to(ans2[0]))
        ans2.move_to(ans.get_center() + DOWN * 2.6)
        ans2[0].set_stroke(RED).set_fill(RED, 0.25)
        st2.next_to(prob2, RIGHT, buff=0.5)
        self.act(self.tr("5.4", 1, 0.0), FadeIn(prob2), LaggedStart(*[FadeIn(s) for s in st2], lag_ratio=0.1), FadeIn(ans2), d=1.0)
        nore = T("no reward", 26, RED).next_to(ans2, RIGHT, buff=0.25)
        self.act(self.tr("5.4", 1, 0.6), FadeIn(nore), d=0.4)

        # 5.5 只知道答没答对
        t5 = T("nobody shows it how to reason", 32, WHITE).move_to(DOWN * 2.05)
        self.act(self.tr("5.5", 0, 0.0), st.animate.set_opacity(0.18), st2.animate.set_opacity(0.18), FadeIn(t5), d=1.0)
        t6 = T("it only learns: right or wrong", 32, YELLOW).move_to(DOWN * 2.05)
        self.act(self.tr("5.5", 1, 0.0), FadeOut(t5), FadeIn(t6), Indicate(ans[0], color=GREEN), Indicate(ans2[0], color=RED), d=1.2)

        # 5.6 DeepSeek-R1
        self.clear(self.tr("5.6", 0, 0.0))
        cover = RoundedRectangle(corner_radius=0.15, width=10.4, height=3.4, stroke_color=WHITE, stroke_width=3, fill_color=WHITE, fill_opacity=0.05).move_to(UP * 1.0)
        t_ds = Text("DeepSeek-R1, Jan 2025", font=SERIF, font_size=56, color=WHITE).move_to(cover)
        self.act(self.tr("5.6", 0, 0.3), FadeIn(cover), Write(t_ds), d=1.6)
        t_rl = T("trained with reinforcement learning", 30, GREY).next_to(cover, DOWN, buff=0.5)
        self.act(self.tr("5.6", 1, 0.0), FadeIn(t_rl), d=0.6)

        # 5.7 15.6 -> 71
        self.clear(self.tr("5.7", 0, 0.0))
        x0, x1, y0, y1 = -4.6, 4.6, -1.7, 2.7
        ax = axes(x0, x1, y0, y1, "training steps", "AIME 2024 score")
        self.act(self.tr("5.7", 0, 0.1), Create(ax[0]), FadeIn(ax[1]), FadeIn(ax[2]), d=1.0)

        def yv(v):
            return y0 + (y1 - y0 - 0.3) * v / 100

        def f(t):
            base = 15.6 + (71 - 15.6) * (1 - np.exp(-2.6 * t)) / (1 - np.exp(-2.6))
            wig = 2.2 * np.sin(14 * t) * (1 - t) * t * 3
            v = base + wig
            return np.array([x0 + (x1 - x0) * t, yv(v), 0])
        curve = ParametricFunction(f, t_range=[0, 1], color=YELLOW, stroke_width=6)
        l1 = Text("15.6%", font=SERIF, font_size=48, color=YELLOW).move_to(RIGHT * (x0 + 1.0) + UP * (yv(15.6) - 0.55))
        l2 = Text("71%", font=SERIF, font_size=60, color=YELLOW).move_to(RIGHT * (x1 - 0.5) + UP * (yv(71) + 0.6))
        self.act(self.tr("5.7", 1, 0.0), FadeIn(l1), d=0.4)
        self.act(self.tr("5.7", 1, 0.1), Create(curve), d=2.8)
        self.act(self.tr("5.7", 1, 0.85), FadeIn(l2, scale=0.8), FadeIn(illus("curve shape illustrative")), d=0.5)

        # 5.8 越想越久、回头检查
        self.clear(self.tr("5.8", 0, 0.0))
        h1 = T("early in training", 26, GREY).move_to(LEFT * 6.6 + UP * 1.7, aligned_edge=LEFT)
        s_e = stream(5).move_to(LEFT * 6.4 + UP * 1.1, aligned_edge=LEFT)
        h2 = T("later in training", 26, GREY).move_to(LEFT * 6.6 + UP * -0.3, aligned_edge=LEFT)
        s_l = stream(22, gap=0.38).move_to(LEFT * 6.4 + UP * -0.9, aligned_edge=LEFT)
        self.act(self.tr("5.8", 0, 0.2), FadeIn(h1), FadeIn(s_e), d=0.8)
        self.act(self.tr("5.8", 1, 0.0), FadeIn(h2), LaggedStart(*[FadeIn(s, scale=0.4) for s in s_l], lag_ratio=0.12), d=2.6)
        back = CurvedArrow(s_l[16].get_top() + UP * 0.05, s_l[8].get_top() + UP * 0.05, angle=TAU / 5, color=YELLOW, stroke_width=5)
        self.act(self.tr("5.8", 2, 0.1), Create(back), d=1.0)
        ck = check(s_l[8].get_top() + UP * 0.8, GREEN, 2.4)
        self.act(self.tr("5.8", 2, 0.6), Create(ck), d=0.5)

        # 5.9 Wait, wait. Wait.
        self.act(self.tr("5.9", 0, 0.0), FadeOut(s_e), FadeOut(h1), FadeOut(h2), FadeOut(back), FadeOut(ck), s_l.animate.move_to(DOWN * 1.2 + LEFT * 0.0), d=0.8)
        quote = VGroup(RoundedRectangle(corner_radius=0.2, width=7.4, height=2.0, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.08),
                       Text("Wait, wait. Wait.", font=SERIF, font_size=60, color=WHITE)).move_to(UP * 1.5)
        quote[1].move_to(quote[0]).shift(UP * 0.1)
        src = T("DeepSeek-R1 paper, 2025", 24, GREY).move_to(quote[0].get_bottom() + UP * 0.32)
        self.act(self.tr("5.9", 1, 0.0), FadeIn(quote, scale=0.9), FadeIn(src), s_l[9].animate.set_fill(RED, 0.7).set_stroke(RED), d=0.8)
        self.act(self.tr("5.9", 2, 0.3), s_l[9].animate.set_fill(GREEN, 0.7).set_stroke(GREEN), d=0.8)
        aha = T("aha moment", 36, YELLOW).next_to(quote, DOWN, buff=0.35)
        self.act(self.tr("5.10", f=0.1), FadeIn(aha, shift=UP * 0.15), s_l.animate.shift(DOWN * 0.3), d=0.8)

        # 5.11 时间线
        self.clear(self.tr("5.11", 0, 0.0))
        line = Line(LEFT * 5.8 + UP * 0.9, RIGHT * 5.8 + UP * 0.9, color=GREY, stroke_width=3)
        xs = [-4.8, -1.6, 1.6, 4.8]
        labs = [("Sep 2024", "OpenAI"), ("Jan 2025", "DeepSeek"), ("Feb 2025", "Anthropic"), ("Mar 2025", "Google")]
        self.act(self.tr("5.11", 0, 0.0), Create(line), d=0.5)
        dots, texts = [], []
        for x, (d_, c_) in zip(xs, labs):
            dot = Dot(RIGHT * x + UP * 0.9, radius=0.16, color=YELLOW)
            tt = VGroup(T(d_, 26, GREY), T(c_, 36, WHITE)).arrange(DOWN, buff=0.15).next_to(dot, DOWN, buff=0.35)
            dots.append(dot); texts.append(tt)
        for k, fr in enumerate([0.0, 0.28, 0.52, 0.78]):
            self.act(self.tr("5.11", 0, fr), FadeIn(dots[k], scale=2), FadeIn(texts[k], shift=UP * 0.1), d=0.5)
        cp = T("models that think before they answer", 34, BLUE).move_to(DOWN * 1.8)
        self.act(self.tr("5.11", 1, 0.0), FadeIn(cp), d=0.7)

        # 5.12 想得越久越好
        self.clear(self.tr("5.12", 0, 0.0))
        ax2 = axes(-4.6, 4.6, -1.3, 2.7, "thinking time", "accuracy")
        self.act(self.tr("5.12", 0, 0.1), Create(ax2[0]), FadeIn(ax2[1]), FadeIn(ax2[2]), d=1.0)
        g = ParametricFunction(lambda t: np.array([-4.6 + 9.2 * t * 0.96 + 0.2, -0.8 + 3.3 * np.log1p(6 * t) / np.log1p(6), 0]), t_range=[0, 1], color=YELLOW, stroke_width=6)
        self.act(self.tr("5.12", 1, 0.0), Create(g), FadeIn(illus("trend shown in OpenAI's o1 post, illustrative")), d=3.2)

        # 5.13 Thinking…
        self.clear(self.tr("5.13", 0, 0.0))
        box = RoundedRectangle(corner_radius=0.3, width=8.6, height=4.4, stroke_color=WHITE, stroke_width=3, fill_color=WHITE, fill_opacity=0.04).move_to(UP * 0.7)
        th = T("Thinking", 36, WHITE).move_to(box.get_top() + DOWN * 0.7 + LEFT * 0.4)
        ds = VGroup(*[Dot(radius=0.07, color=WHITE) for _ in range(3)]).arrange(RIGHT, buff=0.15).next_to(th, RIGHT, buff=0.2).align_to(th, DOWN).shift(UP * 0.08)
        for i, d_ in enumerate(ds):
            d_.add_updater(lambda m, i=i: m.set_opacity(0.25 + 0.75 * (0.5 + 0.5 * np.sin(self.now() * 5 - i * 0.9))))
        self.act(self.tr("5.13", 0, 0.1), FadeIn(box), FadeIn(th), FadeIn(ds), d=0.9)
        rows = VGroup(*[stream(18, op=0.22).move_to(UP * (0.6 - r * 0.6) + LEFT * 0.0) for r in range(4)])
        rows.move_to(box.get_center() + DOWN * 0.45)
        self.act(self.tr("5.13", 2, 0.0), LaggedStart(*[FadeIn(r, scale=0.9) for r in rows], lag_ratio=0.35), d=2.8)
        out = VGroup(RoundedRectangle(corner_radius=0.12, width=3.0, height=0.8, stroke_color=WHITE, stroke_width=3, fill_color=WHITE, fill_opacity=0.12),
                     T("answer", 30, WHITE)).move_to(DOWN * 2.1)
        out[1].move_to(out[0])
        self.act(self.tr("5.13", 2, 0.85), FadeIn(out, shift=UP * 0.2), d=0.6)

        # 5.14 推理 token 计费
        self.clear(self.tr("5.14", 0, 0.0))
        ds.clear_updaters()
        t_free = T("the working isn't free", 34, WHITE).move_to(UP * 3.1)
        self.act(self.tr("5.14", 0, 0.1), FadeIn(t_free), d=0.5)
        rs = VGroup(*[sq(BLUE, 0.34, 0.12, 2) for _ in range(36)]).arrange_in_grid(3, 12, buff=0.09).move_to(LEFT * 3.4 + UP * 1.3)
        ans_s = VGroup(*[sq(WHITE, 0.34, 0.12, 2) for _ in range(6)]).arrange(RIGHT, buff=0.09).move_to(LEFT * 3.4 + DOWN * 0.45)
        rl = T("reasoning tokens", 26, BLUE).next_to(rs, UP, buff=0.25)
        al2 = T("answer tokens", 26, WHITE).next_to(ans_s, DOWN, buff=0.25)
        gauge_o = RoundedRectangle(corner_radius=0.12, width=0.9, height=3.4, stroke_color=WHITE, stroke_width=3).move_to(RIGHT * 4.6 + UP * 0.8)
        gl_ = T("output billed", 26, WHITE).next_to(gauge_o, UP, buff=0.25)
        self.act(self.tr("5.14", 1, 0.0), FadeIn(rs), FadeIn(ans_s), FadeIn(rl), FadeIn(al2), FadeIn(gauge_o), FadeIn(gl_), d=0.8)
        fill = Rectangle(width=0.78, height=0.02, stroke_width=0, fill_color=YELLOW, fill_opacity=0.9).move_to(gauge_o.get_bottom() + UP * 0.08, aligned_edge=DOWN)
        self.add(fill)
        cnt = ValueTracker(0)
        fill.add_updater(lambda m: m.stretch_to_fit_height(max(0.02, 3.2 * cnt.get_value() / 42), about_edge=DOWN) if False else None)
        self.act(self.tr("5.14", 1, 0.3),
                 LaggedStart(*[AnimationGroup(s.animate.set_fill(BLUE, 0.9)) for s in rs], lag_ratio=0.06),
                 d=2.4)
        self.act(self.tr("5.14", 1, 0.95),
                 LaggedStart(*[s.animate.set_fill(WHITE, 0.9) for s in ans_s], lag_ratio=0.12),
                 d=0.8)
        lab_b = T("reasoning tokens = billed as output", 30, YELLOW).move_to(DOWN * 1.95)
        self.act(self.tr("5.14", 2, 0.0), fill.animate.stretch_to_fit_height(3.1, about_edge=DOWN).move_to(gauge_o.get_bottom() + UP * 1.6), FadeIn(lab_b), d=2.8)
        self.act(self.tr("5.14", 3, 0.0), rs.animate.set_opacity(0.2), rl.animate.set_opacity(0.4), d=0.6)
        hid = T("you never see them", 26, GREY).next_to(rs, RIGHT, buff=0.4)
        hid.move_to(LEFT * 3.4 + UP * 2.55)
        self.act(self.tr("5.14", 3, 0.3), FadeIn(hid), d=0.5)

        # 5.15 更慢更贵
        self.clear(self.tr("5.15", 0, 0.0))
        b1l = T("standard answer", 28, WHITE).move_to(LEFT * 6.6 + UP * 1.5, aligned_edge=LEFT)
        b2l = T("thinking mode", 28, BLUE).move_to(LEFT * 6.6 + UP * -0.2, aligned_edge=LEFT)
        b1 = Rectangle(width=1.8, height=0.5, stroke_width=0, fill_color=WHITE, fill_opacity=0.85).move_to(LEFT * 6.6 + UP * 0.9, aligned_edge=LEFT)
        b2 = Rectangle(width=11.8, height=0.5, stroke_width=0, fill_color=BLUE, fill_opacity=0.85).move_to(LEFT * 6.6 + DOWN * 0.8, aligned_edge=LEFT)
        self.act(self.tr("5.15", 0, 0.0), FadeIn(b1l), FadeIn(b2l), GrowFromEdge(b1, LEFT), d=0.6)
        self.act(self.tr("5.15", 0, 0.3), GrowFromEdge(b2, LEFT), d=1.2)
        sl = T("slower", 34, YELLOW).move_to(LEFT * 3 + DOWN * 1.8)
        co = T("often costs more", 34, YELLOW).move_to(RIGHT * 2.5 + DOWN * 1.8)
        self.act(self.tr("5.15", 1, 0.0), FadeIn(sl), FadeIn(co), d=0.6)
        self.finish()
