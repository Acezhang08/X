"""Tip video: ask the AI twice, check where the answers split.

Every label comes from test_log/Q3_run1.txt and test_log/Q3_run2.txt
(see the "On screen" table in test_report.md).

Render:
  manim -r 1920,1080 --fps 30 video/ask_twice.py AskTwice

Layout rule: everything stays inside an 80 px safe margin
(80 / 1080 * 8 = 0.593 scene units on every side).
"""
from manim import *

BG = "#123A3B"          # deep pine teal
RUN1 = "#5FE3E8"        # aqua
RUN2 = "#FF9EC4"        # soft pink
MUTED = "#8FB3AF"
RIGHT_C = "#6BF29A"
WRONG_C = "#FF5468"
FONT = "Inter"

SAFE_X = 7.111 - 0.593   # 6.518
SAFE_Y = 4.0 - 0.593     # 3.407

Q_LINES = ["What happened in the", "1904 Olympic marathon?"]
SPLIT_1 = "14 of 32 finished"   # Run 1 (and Run 3)
SPLIT_2 = "32 of 69 finished"   # Run 2
# Row order is top to bottom. The split row sits on top so the two answers
# can pull far apart; the shortest label sits at the bottom, clear of the
# corner note.
SHARED = [
    "Aug 30, 1904",
    "Hicks won · 3:28:53",
    "strychnine + brandy",
    "Lorz rode a car ~11 mi",
    "Carvajal 4th",
]

# Two trees side by side: as large as fits inside the safe margin.
SMALL = 34
S_DX, S_BUFF, S_ROW = 1.1, 0.22, 0.66
S_ROWS = [0.72 - i * S_ROW for i in range(6)]     # split row first
S_ROOT_Y = (S_ROWS[0] + S_ROWS[-1]) / 2

# Merged tree: 1.4x the old 33 pt labels.
BIG = 46
K = 1.4
B_DX, B_BUFF = 1.2 * K, 0.22 * K
SPLIT1_Y = 2.36
SPLIT2_Y = SPLIT1_Y - 1.53                         # wide gap between the answers
B_ROWS = [SPLIT2_Y - 0.80 - i * 0.76 for i in range(5)]
B_ROOT_Y = (SPLIT1_Y + B_ROWS[-1]) / 2
MX = -5.13                                          # centres tree + marks + legend


def label(s, size, weight=SEMIBOLD):
    """White text, thin black outline, soft offset shadow."""
    t = Text(s, font=FONT, weight=weight, font_size=size, color=WHITE)
    t.set_stroke(BLACK, width=3, background=True)
    shadow = t.copy().set_fill(BLACK, opacity=0.4).set_stroke(width=0)
    shadow.shift(0.035 * (RIGHT + DOWN))
    t.is_label = True                      # lets the overlap checker find real text
    return VGroup(shadow, t)


def branch(start, end, color, width, dx):
    pull = dx * 0.62
    return CubicBezier(
        start, start + RIGHT * pull, end + LEFT * pull, end,
        stroke_color=color, stroke_width=width,
    )


def pt(x, y):
    return np.array([x, y, 0.0])


def small_tree(root_x, color, split_text):
    """Pre-merge tree: root dot, 6 branches, 6 leaf labels (split row on top)."""
    root = pt(root_x, S_ROOT_Y)
    root_dot = Dot(root, radius=0.1, color=color)
    branches, dots, labels = VGroup(), VGroup(), VGroup()
    for y, s in zip(S_ROWS, [split_text] + SHARED):
        end = pt(root_x + S_DX, y)
        branches.add(branch(root, end, color, 5, S_DX))
        dots.add(Dot(end, radius=0.07, color=color))
        labels.add(label(s, SMALL).next_to(end, RIGHT, buff=S_BUFF))
    return root_dot, branches, dots, labels


def check_mark():
    m = VMobject(stroke_color=RIGHT_C, stroke_width=12)
    m.set_points_as_corners([[-0.17, 0.0, 0], [-0.05, -0.14, 0], [0.2, 0.2, 0]])
    return m.scale(K)


def cross_mark():
    a = Line([-0.15, 0.15, 0], [0.15, -0.15, 0])
    b = Line([-0.15, -0.15, 0], [0.15, 0.15, 0])
    return VGroup(a, b).set_stroke(WRONG_C, width=12).scale(K)


def glow(curve, color):
    return curve.copy().set_stroke(color, width=30, opacity=0.22)


class AskTwice(Scene):
    def construct(self):
        self.camera.background_color = BG

        # Corner note, stays on screen.
        note = label("real test · Claude · 3 runs", 32, weight=MEDIUM)
        note.move_to(pt(SAFE_X - 0.05, -SAFE_Y + 0.05), aligned_edge=DR)  # room for shadow

        # ---- 0-3s: the question, big, on two lines ----
        q_big = VGroup(*[label(s, 58, weight=BOLD) for s in Q_LINES])
        q_big.arrange(DOWN, buff=0.1).move_to(pt(0, SAFE_Y - 0.05), aligned_edge=UP)
        self.play(FadeIn(q_big, shift=UP * 0.2), run_time=1.3)
        self.play(FadeIn(note), run_time=0.5)
        self.wait(1.2)

        # ---- 3-10s: two answer trees grow ----
        x1 = -SAFE_X + 0.13
        x2 = SAFE_X - 0.05 - (S_DX + S_BUFF + label(SHARED[3], SMALL).width)
        t1 = small_tree(x1, RUN1, SPLIT_1)
        t2 = small_tree(x2, RUN2, SPLIT_2)

        def header(text, color, x):
            g = VGroup(Dot(radius=0.1, color=color), label(text, SMALL, weight=BOLD))
            g.arrange(RIGHT, buff=0.18)
            g.move_to(pt(x - 0.1, q_big.get_bottom()[1] - 0.12), aligned_edge=UL)
            return g

        h1, h2 = header("Run 1", RUN1, x1), header("Run 2", RUN2, x2)
        self.play(
            GrowFromCenter(t1[0]), GrowFromCenter(t2[0]),
            FadeIn(h1, shift=DOWN * 0.15), FadeIn(h2, shift=DOWN * 0.15),
            run_time=0.7,
        )
        grow = [
            AnimationGroup(
                Create(t1[1][i]), Create(t2[1][i]),
                GrowFromCenter(t1[2][i]), GrowFromCenter(t2[2][i]),
                FadeIn(t1[3][i], shift=RIGHT * 0.2), FadeIn(t2[3][i], shift=RIGHT * 0.2),
            )
            for i in range(6)
        ]
        self.play(LaggedStart(*grow, lag_ratio=0.45), run_time=4.2)
        self.wait(1.6)

        # ---- 10-16s: merge ----
        r1, b1, d1, l1 = t1
        r2, b2, d2, l2 = t2

        # 1) All words leave first, so no moving line ever crosses text.
        q_line = label(" ".join(Q_LINES), 58, weight=BOLD)
        q_line.scale_to_fit_width(2 * SAFE_X - 0.15)
        q_line.move_to(pt(0, SAFE_Y - 0.05), aligned_edge=UP)
        self.play(FadeOut(l1), FadeOut(l2), FadeOut(h1), FadeOut(h2), FadeOut(q_big),
                  run_time=0.7)

        # 2) Only the lines move. Both trees slide onto one big tree; both
        #    split branches land on the same top row for now.
        root = pt(MX, B_ROOT_Y)
        leaf_x = MX + B_DX
        split_mid = (SPLIT1_Y + SPLIT2_Y) / 2
        targets_y = [split_mid] + B_ROWS

        def to_big(tree_r, tree_b, tree_d, color):
            anims = [tree_r.animate.move_to(root).scale(1.4)]
            for i, y in enumerate(targets_y):
                end = pt(leaf_x, y)
                anims.append(Transform(tree_b[i], branch(root, end, color, 7, B_DX)))
                anims.append(tree_d[i].animate.move_to(end).scale(1.4))
            return anims

        self.play(*to_big(r1, b1, d1, RUN1), *to_big(r2, b2, d2, RUN2),
                  FadeIn(q_line), run_time=1.6, rate_func=smooth)
        # Matching branches now sit exactly on top of each other: keep one.
        self.remove(*b2[1:], *d2[1:], r2)

        # 3) The matching branches fade, and their merged words appear.
        merged_color = interpolate_color(ManimColor(RUN1), ManimColor(RUN2), 0.5)
        shared_labels = VGroup(*[
            label(s, BIG).next_to(pt(leaf_x, y), RIGHT, buff=B_BUFF)
            for s, y in zip(SHARED, B_ROWS)
        ]).set_opacity(0.5)
        legend = VGroup(
            VGroup(Dot(radius=0.1, color=RUN1), label("Run 1", SMALL, weight=BOLD)).arrange(RIGHT, buff=0.15),
            VGroup(Dot(radius=0.1, color=RUN2), label("Run 2", SMALL, weight=BOLD)).arrange(RIGHT, buff=0.15),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        legend.next_to(shared_labels, RIGHT, buff=0.45).align_to(shared_labels, UP)

        fade = []
        for i in range(1, 6):
            fade += [b1[i].animate.set_stroke(MUTED, width=5, opacity=0.35),
                     d1[i].animate.set_color(MUTED).set_opacity(0.35)]
        self.play(*fade, r1.animate.set_color(merged_color),
                  FadeIn(shared_labels), FadeIn(legend), run_time=0.9)

        # 4) The two different answers pull apart (one up, one down), then hold.
        end1, end2 = pt(leaf_x, SPLIT1_Y), pt(leaf_x, SPLIT2_Y)
        self.play(
            Transform(b1[0], branch(root, end1, RUN1, 10, B_DX)),
            Transform(b2[0], branch(root, end2, RUN2, 10, B_DX)),
            d1[0].animate.move_to(end1).scale(1.3),
            d2[0].animate.move_to(end2).scale(1.3),
            run_time=1.0, rate_func=rate_functions.ease_in_out_cubic,
        )
        g1, g2 = glow(b1[0], RUN1), glow(b2[0], RUN2)
        self.add(g1, g2, b1[0], b2[0], d1[0], d2[0], r1)
        g1.set_stroke(opacity=0)
        g2.set_stroke(opacity=0)
        self.play(g1.animate.set_stroke(opacity=0.22), g2.animate.set_stroke(opacity=0.22),
                  Flash(d1[0], color=RUN1, line_length=0.3),
                  Flash(d2[0], color=RUN2, line_length=0.3), run_time=0.6)
        self.wait(0.5)

        s1 = label(SPLIT_1, BIG).next_to(d1[0], RIGHT, buff=B_BUFF)
        s2 = label(SPLIT_2, BIG).next_to(d2[0], RIGHT, buff=B_BUFF)
        self.play(FadeIn(s1, shift=RIGHT * 0.2), FadeIn(s2, shift=RIGHT * 0.2), run_time=0.6)
        self.wait(1.0)

        # ---- 16-22s: what the check found ----
        cx = cross_mark().next_to(s2, RIGHT, buff=0.5)
        cx_t = label("wrong", BIG, weight=BOLD).next_to(cx, RIGHT, buff=0.25)
        ck = check_mark().next_to(s1, RIGHT, buff=0.5).align_to(cx, LEFT)
        ck_t = label("right", BIG, weight=BOLD).next_to(ck, RIGHT, buff=0.25).align_to(cx_t, LEFT)

        self.play(Create(cx), run_time=0.5)
        self.play(FadeIn(cx_t, shift=RIGHT * 0.15), run_time=0.35)
        self.play(Create(ck), run_time=0.5)
        self.play(FadeIn(ck_t, shift=RIGHT * 0.15), run_time=0.35)
        self.play(Indicate(s2, color=WHITE, scale_factor=1.06), run_time=0.7)
        self.wait(2.3)

        # ---- 22-28s: conclusion ----
        fork = VGroup(g1, g2, b1[0], b2[0], d1[0], d2[0], r1)
        rest = VGroup(*b1[1:], *d1[1:], shared_labels, legend, s1, s2,
                      ck, ck_t, cx, cx_t, q_line)
        self.play(FadeOut(rest), run_time=0.9)
        # Make sure nothing else is left on screen besides the fork and the note.
        self.clear()
        self.add(note, fork)

        icon_root = pt(-1.2, 2.2)
        ends = [pt(1.2, 2.85), pt(1.2, 1.55)]
        icon = VGroup(
            glow(branch(icon_root, ends[0], RUN1, 10, 2.4), RUN1),
            glow(branch(icon_root, ends[1], RUN2, 10, 2.4), RUN2),
            branch(icon_root, ends[0], RUN1, 10, 2.4),
            branch(icon_root, ends[1], RUN2, 10, 2.4),
            Dot(ends[0], radius=0.14, color=RUN1),
            Dot(ends[1], radius=0.14, color=RUN2),
            Dot(icon_root, radius=0.15, color=merged_color),
        )
        self.play(ReplacementTransform(fork, icon), run_time=1.0)

        line1 = label("ask twice.", 80, weight=BOLD)
        line2 = label("check where the", 80, weight=BOLD)
        line3 = label("answers split.", 80, weight=BOLD)
        VGroup(line1, line2, line3).arrange(DOWN, buff=0.25).next_to(icon, DOWN, buff=0.45)
        self.play(FadeIn(line1, shift=UP * 0.2), run_time=0.7)
        self.play(FadeIn(VGroup(line2, line3), shift=UP * 0.2), run_time=0.9)
        self.wait(3.0)
