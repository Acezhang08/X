"""Re-runs the scene and checks every frame (30 fps):
- no two visible text labels have overlapping bounding boxes
- no visible branch curve passes through a visible text bounding box
"""
import sys
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from manim import *
import ask_twice

problems = []

def visible_texts(scene):
    out = []
    for m in scene.mobjects:
        for sub in m.get_family():
            if getattr(sub, "is_label", False):
                op = max((g.get_fill_opacity() for g in sub.family_members_with_points()), default=0)
                if op > 0.03:
                    out.append(sub)
    return out

def curves(scene):
    out = []
    for m in scene.mobjects:
        for sub in m.get_family():
            if isinstance(sub, CubicBezier) and sub.get_stroke_opacity() > 0.03 and sub.get_stroke_width() < 20:
                out.append(sub)
    return out

def box(m, pad=0.0):
    return (m.get_left()[0] - pad, m.get_right()[0] + pad, m.get_bottom()[1] - pad, m.get_top()[1] + pad)

class Checked(ask_twice.AskTwice):
    def construct(self):
        self.t = 0.0
        def check(dt):
            self.t += dt
            texts = visible_texts(self)
            # merge glyph-level Text objects into whole labels: Text is one object per label already
            for i in range(len(texts)):
                for j in range(i + 1, len(texts)):
                    a, b = box(texts[i]), box(texts[j])
                    if a[0] < b[1] and b[0] < a[1] and a[2] < b[3] and b[2] < a[3]:
                        problems.append((round(self.t, 2), "text/text", texts[i].text, texts[j].text))
            for c in curves(self):
                pts = c.points
                for t in texts:
                    l, r, bt, tp = box(t, pad=-0.02)
                    inside = (pts[:, 0] > l) & (pts[:, 0] < r) & (pts[:, 1] > bt) & (pts[:, 1] < tp)
                    # sample the curve itself, not only control points
                    samp = np.array([c.point_from_proportion(a) for a in np.linspace(0, 1, 40)])
                    inside = (samp[:, 0] > l) & (samp[:, 0] < r) & (samp[:, 1] > bt) & (samp[:, 1] < tp)
                    if inside.any():
                        problems.append((round(self.t, 2), "line/text", t.text, ""))
        self.add_updater(check)
        super().construct()

if __name__ == "__main__":
    config.frame_rate = 30
    config.pixel_width, config.pixel_height = 480, 270
    config.dry_run = True
    Checked().render()
    seen = set()
    for p in problems:
        key = (p[1], p[2], p[3])
        if key in seen: continue
        seen.add(key)
        print("PROBLEM", p)
    print("total problem frames:", len(problems))
