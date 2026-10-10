# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from common import *


class Seg3(Seg):
    SEG = "3"

    def construct(self):
        random.seed(7)
        # 3.1 神经网络
        cols, dots, edges = make_net((4, 6, 6, 4), 7.0, 3.2, UP * 0.9)
        net = VGroup(edges, dots)
        plab = T("parameters", 30, WHITE).move_to(DOWN * 1.2)
        self.act(self.tr("3.1", f=0.05), LaggedStart(*[Create(e) for e in edges], lag_ratio=0.004), FadeIn(dots), d=2.2)
        self.act(self.tr("3.1", f=0.6), FadeIn(plab), d=0.5)
        # 3.2 175 billion
        c, a = counter(lambda v: f"{int(round(v)):,}", 0, 175_000_000_000, DOWN * 0.15 + UP * 0.0, 66, BLUE, rate=rate_functions.smooth)
        c.move_to(DOWN * 0.4)
        cl = T("GPT-3 · 2020", 30, GREY).move_to(DOWN * 1.5)
        self.act(self.tr("3.2", f=0.0), net.animate.scale(0.6).move_to(UP * 2.1), FadeOut(plab), FadeIn(cl), d=0.9)
        ta, tb = self.wt("3.2", 0, "one"), self.wt("3.2", 0, "billion", end=True)
        self.go(ta)
        self.add(c)
        self.act_mark("175 billion (3.2)", ta, a, d=tb - ta)

        # 3.3 token -> 向量 -> 层
        self.act(self.tr("3.3", 0, 0.0), FadeOut(net), FadeOut(c), FadeOut(cl), d=0.6)
        words = "The cat sat on the mat because it was tired".split()
        toks = VGroup(*[tok(w, BLUE, w=len(w) * 0.19 + 0.5, h=0.6, size=20) for w in words]).arrange(RIGHT, buff=0.08)
        toks.move_to(DOWN * 1.7)
        self.act(self.tr("3.3", 0, 0.1), LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in toks], lag_ratio=0.08), d=1.5)
        levels = [-0.6, 0.5, 1.6]
        bands = VGroup(*[RoundedRectangle(corner_radius=0.15, width=11.8, height=0.95, stroke_color=DIM, stroke_width=2,
                                          fill_color=DIM, fill_opacity=0.18).move_to(UP * y) for y in levels])
        blabs = VGroup(*[T(f"L{i + 1}", 20, GREY).move_to(LEFT * 6.7 + UP * y) for i, y in enumerate(levels)])

        def vec(x, y):
            g = VGroup(*[Square(0.17, stroke_width=0, fill_color=BLUE, fill_opacity=random.uniform(0.25, 1)) for _ in range(4)])
            g.arrange(DOWN, buff=0.03).move_to(RIGHT * x + UP * y)
            return g
        vecs = [[vec(t.get_center()[0], y) for t in toks] for y in levels]
        self.act(self.tr("3.3", 1, 0.0), LaggedStart(*[GrowFromEdge(v, DOWN) for v in vecs[0]], lag_ratio=0.06), d=1.8)
        self.act(self.tr("3.3", 2, 0.0), FadeIn(bands), FadeIn(blabs), d=0.5)
        self.act(self.tr("3.3", 2, 0.2), LaggedStart(*[FadeIn(v, shift=UP * 0.2) for v in vecs[1]], lag_ratio=0.05),
                 LaggedStart(*[FadeIn(v, shift=UP * 0.2) for v in vecs[2]], lag_ratio=0.05), d=2.0)
        layers = VGroup(bands, blabs, *[v for lv in vecs for v in lv])

        # 3.4 注意力弧线
        def arcs_from(i, targets, widths, colors):
            out = VGroup()
            p = toks[i].get_top() + UP * 0.02
            for j, w, col in zip(targets, widths, colors):
                q = toks[j].get_top() + UP * 0.02
                out.add(ArcBetweenPoints(p, q, angle=PI / 2.2, stroke_width=w, stroke_color=col, stroke_opacity=0.9))
            return out
        self.act(self.tr("3.4", 0, 0.0), layers.animate.set_opacity(0.18), d=0.6)
        arcs = arcs_from(5, [0, 1, 2, 3, 4], [2, 6, 3, 1.5, 7], [BLUE, BLUE, BLUE, BLUE, YELLOW])
        self.act(self.tr("3.4", 0, 0.4), LaggedStart(*[Create(a_) for a_ in arcs], lag_ratio=0.15), d=1.8)
        tg = illus()
        # 3.5 it -> cat
        self.act(self.tr("3.5", 0, 0.0), FadeOut(arcs), FadeIn(tg), d=0.5)
        self.act(self.tr("3.5", 0, 0.45), toks[7].animate.set_color(YELLOW), d=0.4)
        arcs2 = VGroup(
            ArcBetweenPoints(toks[7].get_top() + UP * 0.02, toks[5].get_top() + UP * 0.02, angle=PI / 2.4, stroke_width=2, stroke_color=BLUE, stroke_opacity=0.35),
            ArcBetweenPoints(toks[7].get_top() + UP * 0.02, toks[1].get_top() + UP * 0.02, angle=PI / 2.6, stroke_width=9, stroke_color=YELLOW),
        )
        t_cat = T("cat", 26, YELLOW).next_to(toks[1], UP, buff=1.9)
        t_mat = T("mat", 26, GREY).next_to(toks[5], UP, buff=0.95)
        self.act(self.tr("3.5", 1, 0.1), Create(arcs2[0]), Create(arcs2[1]), d=1.6)
        self.act(self.tr("3.5", 1, 0.7), toks[1].animate.set_color(YELLOW), d=0.4)

        # 3.6 attention
        self.act(self.tr("3.6", 0, 0.0), *[FadeOut(m) for m in list(self.mobjects)], d=0.6)
        tag = T("A T T E N T I O N   ·   2 0 1 7", 26, GREY).move_to(UP * 2.9)
        title = Text("Attention Is All You Need", font=SERIF, font_size=72, color=WHITE).move_to(UP * 1.2)
        sub = T("researchers at Google · 2017", 30, GREY).move_to(UP * 0.1)
        self.act(self.tr("3.6", 0, 0.1), FadeIn(tag), d=0.5)
        self.act(self.tr("3.6", 1, 0.3), Write(title), FadeIn(sub), d=2.0)
        core = T("the core of today's large language models", 34, BLUE).move_to(DOWN * 1.3)
        self.act(self.tr("3.6", 3, 0.0), FadeIn(core, shift=UP * 0.2), d=0.8)

        # 3.7 随机参数
        self.act(self.tr("3.7", 0, 0.0), *[FadeOut(m) for m in list(self.mobjects)], d=0.6)
        cols, dots, edges = make_net((4, 6, 6, 4), 6.0, 3.0, LEFT * 3.5 + UP * 0.3)
        palette = [BLUE, RED, GREEN, YELLOW, WHITE]
        for e in edges:
            e.set_stroke(random.choice(palette), 1.6, 0.55)
        net = VGroup(edges, dots)
        items = ["mat", "floor", "sofa", "dog", "banana"]
        ch = prob_chart(items, [0.10, 0.14, 0.18, 0.12, 0.46], hi=4, left=1.6, top=1.1, gap=0.65, scale=4.4, color=BLUE)
        nl = T("random parameters", 28, WHITE).next_to(net, UP, buff=0.3)
        cl2 = T("nonsense guesses", 28, WHITE).next_to(ch, UP, buff=0.35).align_to(ch, LEFT).shift(RIGHT * 0.0)
        self.act(self.tr("3.7", 0, 0.1), FadeIn(net), FadeIn(nl), d=1.0)
        self.act(self.tr("3.7", 1, 0.0), FadeIn(ch), FadeIn(cl2), FadeIn(illus()), d=0.8)
        self.act(self.tr("3.7", 1, 0.4), *[e.animate.set_stroke(random.choice(palette)) for e in random.sample(list(edges), 40)], d=0.9)

        # 3.8 猜词游戏
        sent = VGroup(*[tok(w, BLUE, size=22, h=0.65) for w in ["The", "cat", "sat", "on", "the"]])
        hidden = tok("■■■", GREY, size=22, h=0.65)
        sent.add(hidden)
        sent.arrange(RIGHT, buff=0.12).move_to(UP * 3.2)
        self.act(self.tr("3.8", 0, 0.0), FadeIn(sent), d=0.8)
        self.act(self.tr("3.8", 1, 0.2), Indicate(hidden, color=YELLOW, scale_factor=1.15), d=0.8)
        right = ch[0]
        mat_bar, ban_bar = ch[0][1], ch[4][1]
        self.act(self.tr("3.8", 1, 0.6), mat_bar.animate.set_fill(GREEN, 1), ch[0][2].animate.set_color(GREEN), d=0.6)
        calm = [BLUE] * len(edges)
        self.act(self.tr("3.8", 2, 0.1),
                 ban_bar.animate.stretch_to_fit_width(0.9, about_edge=LEFT),
                 mat_bar.animate.stretch_to_fit_width(2.2, about_edge=LEFT),
                 LaggedStart(*[e.animate.set_stroke(BLUE, 1.6, 0.4) for e in edges], lag_ratio=0.01), d=2.4)
        ch[4][2].become(Text("0.20", font=MONO, font_size=20, color=BLUE).next_to(ban_bar, RIGHT, buff=0.2))

        # 3.9 一遍又一遍 + 15 trillion
        self.go(self.tr("3.9", 0, 0.0))
        for k in range(4):
            vs = [random.random() for _ in range(5)]
            s_ = sum(vs)
            vs = [v / s_ for v in vs]
            self.play(*[ch[i][1].animate.stretch_to_fit_width(max(vs[i] * 4.4 * 1.2, 0.05), about_edge=LEFT) for i in range(5)],
                      *[e.animate.set_stroke(random.choice([BLUE, GREEN, YELLOW]), 1.6, 0.5) for e in random.sample(list(edges), 25)],
                      run_time=0.32)
        self.act(self.tr("3.9", 1, 0.0), *[FadeOut(m) for m in list(self.mobjects)], d=0.5)
        c, a = counter(lambda v: f"{int(round(v)):,}+", 0, 15_000_000_000_000, UP * 0.7, 62, BLUE, rate=rate_functions.smooth)
        lab = T("tokens  ·  Meta's Llama 3", 32, GREY).move_to(DOWN * 0.5)
        self.go(self.tr("3.9", 1, 0.0) + 0.5)
        self.add(c)
        self.play(FadeIn(lab), run_time=0.4)
        ta, tb = self.wt("3.9", 1, "more"), self.wt("3.9", 1, "tokens", end=True)
        self.act_mark("15 trillion (3.9)", ta, a, d=tb - ta)
        t_hold_end = self.now() + 1.5   # 满亮度停留至少 1.5 秒

        # 3.10 九万年
        self.act(t_hold_end, *[FadeOut(m) for m in list(self.mobjects)], d=0.5)
        axis = Line(LEFT * 5.8 + DOWN * 0.3, RIGHT * 5.8 + DOWN * 0.3, color=WHITE, stroke_width=3)
        ticks = VGroup()
        for k in range(10):
            x = -5.8 + 11.6 * k / 9
            ticks.add(Line(RIGHT * x + DOWN * 0.2, RIGHT * x + DOWN * 0.4, color=WHITE, stroke_width=2))
            ticks.add(T(f"{k * 10_000:,}", 20, GREY).move_to(RIGHT * x + DOWN * 0.78))
        self.act(self.now(), Create(axis), FadeIn(ticks), d=0.9)
        rd = person(WHITE, 1.2).move_to(LEFT * 5.8 + UP * 0.35)
        read = T("reading nonstop, at an average speed", 28, GREY).move_to(DOWN * 1.7)
        self.act(self.tr("3.10", 1, 0.0), FadeIn(rd), FadeIn(read), d=0.6)
        yc, ya = counter(lambda v: f"≈ {int(round(v)):,}", 0, 90_000, UP * 2.9, 80, YELLOW, rate=rate_functions.smooth)
        yl = T("YEARS", 36, YELLOW).move_to(UP * 1.85)
        ta, tb = self.wt("3.10", 2, "roughly"), self.wt("3.10", 2, "years", end=True)
        self.go(ta)
        self.add(yc, yl)
        self.act_mark("90,000 years (3.10)", ta, ya, rd.animate.move_to(RIGHT * 5.8 + UP * 0.35), d=tb - ta, rate_func=rate_functions.smooth)
        self.go(self.tr("3.10", 2, 1.0))

        # 3.11 / 3.12 网络里浮现语法、事实、推理
        self.act(self.tr("3.11", 0, 0.0), *[FadeOut(m) for m in list(self.mobjects)], d=0.5)
        cols, dots, edges = make_net((5, 7, 7, 5), 8.6, 3.2, UP * 1.2)
        net = VGroup(edges, dots)
        self.act(self.tr("3.11", 0, 0.1), FadeIn(net), d=1.0)
        centers = [LEFT * 3.0 + UP * 1.0, UP * 1.9, RIGHT * 3.0 + UP * 1.0]
        names = ["grammar", "facts", "reasoning patterns"]
        blobs, labs, lines = [], [], []
        for cpos, nm in zip(centers, names):
            blob = Ellipse(width=2.7, height=2.3, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.12).move_to(cpos)
            blobs.append(blob)
        lab_pos = [LEFT * 4.2 + DOWN * 1.05, UP * 0.0 + DOWN * 1.05, RIGHT * 4.0 + DOWN * 1.05]
        for blob, nm, lp in zip(blobs, names, lab_pos):
            labs.append(T(nm, 28, YELLOW).move_to(lp))
            lines.append(Line(lp + UP * 0.3, blob.get_bottom() + (UP * 0.35 if nm != "facts" else UP * 0.0), color=YELLOW, stroke_width=2, stroke_opacity=0.6))
        # 把 facts 的标签放在最上面更清楚
        labs[1].move_to(UP * 3.5)
        lines[1] = Line(labs[1].get_bottom() + DOWN * 0.05, blobs[1].get_top(), color=YELLOW, stroke_width=2, stroke_opacity=0.6)
        self.act(self.tr("3.11", 1, 0.2), FadeIn(illus("illustrative")), d=0.3)
        self.act(self.tr("3.11", 2, 0.05), FadeIn(blobs[0]), FadeIn(labs[0]), Create(lines[0]), d=0.7)
        self.act(self.tr("3.11", 2, 0.55), FadeIn(blobs[1]), FadeIn(labs[1]), Create(lines[1]), d=0.7)
        self.act(self.tr("3.11", 3, 0.1), FadeIn(blobs[2]), FadeIn(labs[2]), Create(lines[2]), d=0.8)
        prog = T("not programmed in", 30, WHITE).move_to(DOWN * 2.1)
        self.act(self.tr("3.12", 0, 0.0), FadeIn(prog), d=0.6)
        cks = [check(labs[0].get_right() + RIGHT * 0.4, s=2.2), check(labs[1].get_right() + RIGHT * 0.4, s=2.2), check(labs[2].get_right() + RIGHT * 0.4, s=2.2)]
        self.act(self.tr("3.12", 1, 0.0), LaggedStart(*[Create(c_) for c_ in cks], lag_ratio=0.3), d=1.4)
        self.finish()
