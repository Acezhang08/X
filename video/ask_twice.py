"""Tip video: ask the AI twice, check where the answers split.

Every label comes from test_log/Q3_run1.txt and test_log/Q3_run2.txt
(see the "On screen" table in test_report.md).

Render:
  manim -r 1920,1080 --fps 30 video/ask_twice.py AskTwice
"""
from manim import *

BG = "#123A3B"          # deep pine teal
RUN1 = "#5FE3E8"        # aqua
RUN2 = "#FF9EC4"        # soft pink
MUTED = "#8FB3AF"
RIGHT_C = "#6BF29A"
WRONG_C = "#FF5468"
FONT = "Inter"

QUESTION = "What happened in the 1904 Olympic marathon?"
SHARED = [
    "Aug 30, 1904",
    "Hicks won · 3:28:53",
    "strychnine + brandy",
    "Lorz rode a car ~11 mi",
    "Carvajal 4th",
]
SPLIT_1 = "14 of 32 finished"   # Run 1 (and Run 3)
SPLIT_2 = "32 of 69 finished"   # Run 2

ROW_Y = [1.75, 1.05, 0.35, -0.35, -1.05, -1.75]
ROOT_Y = 0.0
BRANCH_DX = 1.2
LEAF_SIZE = 33
X1, X2 = -6.75, 0.2   # tree roots before the merge
MX = -3.4             # merged tree root


def label(s, size=30, weight=SEMIBOLD):
    """White text, thin black outline, soft offset shadow."""
    t = Text(s, font=FONT, weight=weight, font_size=size, color=WHITE)
    t.set_stroke(BLACK, width=3, background=True)
    shadow = t.copy().set_fill(BLACK, opacity=0.4).set_stroke(width=0)
    shadow.shift(0.035 * (RIGHT + DOWN))
    return VGroup(shadow, t)


def branch(start, end, color, width=5):
    return CubicBezier(
        start, start + RIGHT * 0.75, end + LEFT * 0.75, end,
        stroke_color=color, stroke_width=width,
    )


def build_tree(root_x, color, split_text):
    """Root dot + 6 branches growing right, one leaf label per branch."""
    root = np.array([root_x, ROOT_Y, 0])
    root_dot = Dot(root, radius=0.11, color=color)
    branches, dots, labels = VGroup(), VGroup(), VGroup()
    texts = SHARED + [split_text]
    for y, s in zip(ROW_Y, texts):
        end = np.array([root_x + BRANCH_DX, y, 0])
        branches.add(branch(root, end, color))
        dots.add(Dot(end, radius=0.075, color=color))
        lab = label(s, size=LEAF_SIZE)
        lab.next_to(end, RIGHT, buff=0.22)
        labels.add(lab)
    return root_dot, branches, dots, labels


def slide_and_fade(mob, vec):
    """Slide with the tree but fade out early, so duplicate labels never pile up."""
    start = mob.copy()

    def update(m, alpha):
        m.become(start.copy().shift(vec * smooth(alpha)))
        m.set_opacity(max(0.0, 1 - 3 * alpha))
    return update


def check_mark():
    m = VMobject(stroke_color=RIGHT_C, stroke_width=9)
    m.set_points_as_corners([[-0.17, 0.0, 0], [-0.05, -0.14, 0], [0.2, 0.2, 0]])
    return m


def cross_mark():
    a = Line([-0.15, 0.15, 0], [0.15, -0.15, 0])
    b = Line([-0.15, -0.15, 0], [0.15, 0.15, 0])
    return VGroup(a, b).set_stroke(WRONG_C, width=9)


def glow(curve, color):
    g = curve.copy().set_stroke(color, width=22, opacity=0.22)
    return g


class AskTwice(Scene):
    def construct(self):
        self.camera.background_color = BG

        # Corner note, small, stays on screen.
        note = label("real test · Claude · 3 runs", size=26, weight=MEDIUM)
        note.to_corner(DR, buff=0.35)

        # ---- 0-3s: the question ----
        q = label(QUESTION, size=44, weight=BOLD)
        q.scale_to_fit_width(min(q.width, 12.4))
        q.move_to(UP * 3.3)
        self.play(FadeIn(q[0]), Write(q[1]), run_time=1.6)
        self.play(FadeIn(note, shift=UP * 0.1), run_time=0.5)
        self.wait(0.9)

        # ---- 3-10s: two answer trees grow ----
        t1 = build_tree(X1, RUN1, SPLIT_1)
        t2 = build_tree(X2, RUN2, SPLIT_2)

        def header(text, color, x):
            dot = Dot(radius=0.1, color=color)
            lab = label(text, size=30, weight=BOLD)
            g = VGroup(dot, lab).arrange(RIGHT, buff=0.18)
            g.move_to([x, 2.55, 0], aligned_edge=LEFT)
            return g

        h1 = header("Run 1", RUN1, X1 - 0.1)
        h2 = header("Run 2", RUN2, X2 - 0.1)

        self.play(
            GrowFromCenter(t1[0]), GrowFromCenter(t2[0]),
            FadeIn(h1, shift=DOWN * 0.15), FadeIn(h2, shift=DOWN * 0.15),
            run_time=0.7,
        )
        grow = []
        for i in range(6):
            grow.append(AnimationGroup(
                Create(t1[1][i]), Create(t2[1][i]),
                GrowFromCenter(t1[2][i]), GrowFromCenter(t2[2][i]),
                FadeIn(t1[3][i], shift=RIGHT * 0.2), FadeIn(t2[3][i], shift=RIGHT * 0.2),
            ))
        self.play(LaggedStart(*grow, lag_ratio=0.45), run_time=4.2)
        self.wait(1.9)

        # ---- 10-16s: slide together and overlap ----
        legend = VGroup(
            VGroup(Dot(radius=0.09, color=RUN1), label("Run 1", size=28, weight=BOLD)).arrange(RIGHT, buff=0.15),
            VGroup(Dot(radius=0.09, color=RUN2), label("Run 2", size=28, weight=BOLD)).arrange(RIGHT, buff=0.15),
        ).arrange(RIGHT, buff=0.5)
        legend.move_to([MX - 0.2, 2.55, 0], aligned_edge=LEFT)

        r1, b1, d1, l1 = t1
        r2, b2, d2, l2 = t2
        root_pt = np.array([MX, ROOT_Y, 0])
        leaf_x = MX + BRANCH_DX
        split_y2 = -2.75

        # Run 2's split leaf heads for its own row while everything slides,
        # so the two different answers pull apart instead of stacking.
        new_b2 = branch(root_pt, np.array([leaf_x, split_y2, 0]), RUN2)
        new_d2 = Dot([leaf_x, split_y2, 0], radius=0.075, color=RUN2)
        new_l2 = label(SPLIT_2, size=LEAF_SIZE).next_to(new_d2, RIGHT, buff=0.22)

        shared2 = VGroup(*[m[i] for m in (b2, d2, l2) for i in range(5)], r2)
        self.play(
            VGroup(r1, b1, d1, l1).animate.shift(RIGHT * (MX - X1)),
            shared2.animate.shift(LEFT * (X2 - MX)),
            *[UpdateFromAlphaFunc(l2[i], slide_and_fade(l2[i], LEFT * (X2 - MX))) for i in range(5)],
            Transform(b2[5], new_b2), Transform(d2[5], new_d2), Transform(l2[5], new_l2),
            ReplacementTransform(VGroup(h1, h2), legend),
            run_time=2.0, rate_func=smooth,
        )
        # The matching branches now sit exactly on top of each other: keep one.
        self.remove(*[b2[i] for i in range(5)], *[d2[i] for i in range(5)],
                    *[l2[i] for i in range(5)])
        merged_color = interpolate_color(ManimColor(RUN1), ManimColor(RUN2), 0.5)

        fade_anims = []
        for i in range(5):
            fade_anims += [
                b1[i].animate.set_stroke(MUTED, width=4, opacity=0.35),
                d1[i].animate.set_color(MUTED).set_opacity(0.35),
                l1[i].animate.set_opacity(0.4),
            ]
        self.play(
            *fade_anims,
            r1.animate.set_color(merged_color), r2.animate.set_color(merged_color),
            b1[5].animate.set_stroke(width=7), b2[5].animate.set_stroke(width=7),
            d1[5].animate.scale(1.35), d2[5].animate.scale(1.35),
            run_time=1.3,
        )
        self.remove(r2)
        g1, g2 = glow(b1[5], RUN1), glow(b2[5], RUN2)
        self.add(g1, g2, b1[5], b2[5], d1[5], d2[5], r1)
        g1.set_opacity(0); g2.set_opacity(0)
        self.play(g1.animate.set_stroke(opacity=0.22), g2.animate.set_stroke(opacity=0.22),
                  Flash(d1[5], color=RUN1, line_length=0.25),
                  Flash(d2[5], color=RUN2, line_length=0.25), run_time=0.8)
        self.wait(1.6)

        # ---- 16-22s: what the check found ----
        ck = check_mark().next_to(l1[5], RIGHT, buff=0.45)
        ck_t = label("right", size=30, weight=BOLD).next_to(ck, RIGHT, buff=0.2)
        cx = cross_mark().next_to(l2[5], RIGHT, buff=0.45)
        cx_t = label("wrong", size=30, weight=BOLD).next_to(cx, RIGHT, buff=0.2)
        ck.align_to(cx, LEFT)
        ck_t.next_to(ck, RIGHT, buff=0.2)
        ck_t.align_to(cx_t, LEFT)

        self.play(Create(cx), run_time=0.6)
        self.play(FadeIn(cx_t, shift=RIGHT * 0.15), run_time=0.4)
        self.play(Create(ck), run_time=0.6)
        self.play(FadeIn(ck_t, shift=RIGHT * 0.15), run_time=0.4)
        self.play(Indicate(l2[5], color=WHITE, scale_factor=1.08), run_time=0.8)
        self.wait(2.7)

        # ---- 22-28s: conclusion ----
        fork = VGroup(g1, g2, b1[5], b2[5], d1[5], d2[5], r1)
        rest = VGroup(*[b1[i] for i in range(5)], *[d1[i] for i in range(5)],
                      *[l1[i] for i in range(5)], l1[5], l2[5],
                      ck, ck_t, cx, cx_t, legend, q)
        self.play(FadeOut(rest, shift=UP * 0.2), run_time=0.9)
        # The split collapses into a small fork icon above the takeaway.
        icon_root = np.array([-0.9, 1.55, 0])
        ends = [np.array([0.9, 2.05, 0]), np.array([0.9, 1.05, 0])]
        icon = VGroup(
            glow(branch(icon_root, ends[0], RUN1, width=7), RUN1),
            glow(branch(icon_root, ends[1], RUN2, width=7), RUN2),
            branch(icon_root, ends[0], RUN1, width=7),
            branch(icon_root, ends[1], RUN2, width=7),
            Dot(ends[0], radius=0.1, color=RUN1),
            Dot(ends[1], radius=0.1, color=RUN2),
            Dot(icon_root, radius=0.11, color=r1.get_color()),
        )
        self.play(ReplacementTransform(fork, icon), run_time=1.0)

        line1 = label("ask twice.", size=60, weight=BOLD)
        line2 = label("check where the answers split.", size=60, weight=BOLD)
        concl = VGroup(line1, line2).arrange(DOWN, buff=0.35).move_to(DOWN * 0.75)
        self.play(FadeIn(line1[0]), Write(line1[1]), run_time=0.9)
        self.play(FadeIn(line2[0]), Write(line2[1]), run_time=1.5)
        self.wait(2.6)
