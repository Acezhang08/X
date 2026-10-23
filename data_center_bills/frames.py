# -*- coding: utf-8 -*-
"""Extract a frame every 2 s (+ segment change points) from the mp4 and build 3x4 contact sheets, time-stamped."""
import subprocess, sys, os, json, glob
from PIL import Image, ImageDraw, ImageFont
vid = sys.argv[1]; out = sys.argv[2]; step = float(sys.argv[3]) if len(sys.argv) > 3 else 2.0
extra = [float(x) for x in sys.argv[4:]]
os.makedirs(out, exist_ok=True)
for f in glob.glob(out + "/*"): os.remove(f)
T = json.load(open("timeline.json"))
dur = T["duration"]
times = [round(i*step, 2) for i in range(int(dur/step))]
for k, st in T["seg_start"].items():
    for d in (-1.2, -0.6, 0.0, 0.5): times.append(round(st + d, 2))
for l in T["lines"]: times.append(round(l["start"] + 0.3, 2))
times = sorted({t for t in times + extra if 0 <= t < dur})
font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 26)
tiles = []
for i, t in enumerate(times):
    fn = f"{out}/f_{i:04d}.jpg"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(t), "-i", vid, "-frames:v", "1", "-vf", "scale=640:360", "-q:v", "4", fn])
    tiles.append((t, fn))
per = 12; n = 0
for s in range(0, len(tiles), per):
    sheet = Image.new("RGB", (1920, 1440))
    for j, (t, fn) in enumerate(tiles[s:s+per]):
        im = Image.open(fn); d = ImageDraw.Draw(im); d.rectangle((0, 0, 150, 34), fill=(0, 0, 0)); d.text((6, 2), f"{int(t//60)}:{t%60:05.2f}", fill=(255, 255, 0), font=font)
        sheet.paste(im, ((j % 3)*640, (j//3)*360))
    sheet.save(f"{out}/sheet_{n:02d}.jpg", quality=80); n += 1
print(len(tiles), "frames", n, "sheets")
