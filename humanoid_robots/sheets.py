# -*- coding: utf-8 -*-
"""Contact sheets for review: every 2 s + each line start+0.6 s + each segment boundary -0.5 s. 12 frames per sheet (3x4)."""
import sys, os
from PIL import Image, ImageDraw, ImageFont
import render, subs
T = render.load_scenes(); cues = subs.build_cues(T)
step = float(sys.argv[1]) if len(sys.argv) > 1 else 2.0
t0 = float(sys.argv[2]) if len(sys.argv) > 2 else 0; t1 = float(sys.argv[3]) if len(sys.argv) > 3 else T.duration
pts = set()
t = t0
while t < t1: pts.add(round(t, 2)); t += step
for lid in T.order:
    for off in (0.6,):
        x = T.s(lid) + off
        if t0 <= x < t1: pts.add(round(x, 2))
for k, st in T.seg_start.items():
    if k > 0 and t0 <= st - .5 < t1: pts.add(round(st - .5, 2))
pts = sorted(pts)
os.makedirs("build/sheets", exist_ok=True)
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 30)
n = 0
for i in range(0, len(pts), 12):
    grp = pts[i:i + 12]
    im = Image.new("RGB", (1920, 1440), "white")
    for j, t in enumerate(grp):
        s = render.frame_surface(t, T); cv = s.getCanvas(); subs.draw_subs(cv, subs.cue_at(cues, t))
        s.makeImageSnapshot().save("build/_f.png")
        fr = Image.open("build/_f.png").convert("RGB").resize((640, 360), Image.LANCZOS)
        d = ImageDraw.Draw(fr); d.rectangle([0, 0, 130, 36], fill=(0, 0, 0)); d.text((6, 2), f"{t:.1f}s", fill=(255, 255, 0), font=font)
        im.paste(fr, ((j % 3) * 640, (j // 3) * 360))
    im.save(f"build/sheets/s_{n:02d}.png"); n += 1
print(n, "sheets", len(pts), "frames")
