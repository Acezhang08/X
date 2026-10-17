# -*- coding: utf-8 -*-
"""Objective review checks on the finished mp4 + timeline.json + subtitles_en.srt.
 1. blank-screen runs (> 1 s with almost no ink on the paper)
 2. static runs (> 8 s with no visible change in the content area)
 3. subtitle <-> voice alignment against timeline.json, and subtitle text == script text
 4. audio/video duration and sync"""
import sys, os, re, json, subprocess
import numpy as np
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from script import SEGMENTS

MP4 = sys.argv[1] if len(sys.argv) > 1 else "humanoid_robots.mp4"
d = json.load(open("build/timeline.json")); D = d["duration"]
FPS = 5; W, H = 480, 270; ZONE = int(925 / 1080 * H)

def frames():
    p = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-i", MP4, "-vf", f"fps={FPS},scale={W}:{H},format=gray", "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
    n = W * H
    while True:
        b = p.stdout.read(n)
        if len(b) < n: break
        yield np.frombuffer(b, np.uint8).reshape(H, W)

# ---- 1 & 2
import lib
paper = np.asarray(Image.fromarray(np.asarray(lib.bg_image().toarray())[..., :3]).convert("L").resize((W, H), Image.LANCZOS)).astype(np.int16)
content = []; diffs = []; prev = None
for f in frames():
    fz = f[:ZONE].astype(np.int16)
    content.append(float((np.abs(fz - paper[:ZONE]) > 28).mean()))
    diffs.append(0.0 if prev is None else float(np.abs(fz - prev).mean()))
    prev = fz
content = np.array(content); diffs = np.array(diffs)

def runs(mask, min_len):
    out = []; i = 0
    while i < len(mask):
        if mask[i]:
            j = i
            while j < len(mask) and mask[j]: j += 1
            if (j - i) / FPS >= min_len: out.append((i / FPS, j / FPS))
            i = j
        else: i += 1
    return out

blank = content < 0.004
blank[: int(1.3 * FPS)] = False
print("BLANK runs >= 1.0 s:", runs(blank, 1.0))
print("BLANK runs >= 0.6 s:", runs(blank, 0.6))
static = diffs < 0.12
print("STATIC runs >= 8 s:", runs(static, 8.0))
print("STATIC runs >= 6 s:", runs(static, 6.0))
print("mean content coverage", round(float(content.mean()), 3))

# ---- 3 subtitles
txt = open("subtitles_en.srt", encoding="utf-8").read().strip().split("\n\n")
def tsec(s): h, m, rest = s.split(":"); sec, ms = rest.split(","); return int(h) * 3600 + int(m) * 60 + int(sec) + int(ms) / 1000
cues = []
for blk in txt:
    ls = blk.split("\n"); a, b = ls[1].split(" --> "); cues.append((tsec(a), tsec(b), " ".join(ls[2:])))
bad = 0; maxs = 0; maxe = 0
for seg, lns in SEGMENTS.items():
    for lid, en, pre in lns:
        ln = [l for l in d["lines"] if l["id"] == lid][0]
        mine = [c for c in cues if c[0] >= ln["start"] - 0.02 and c[1] <= ln["end"] + 0.25]
        joined = " ".join(c[2] for c in mine)
        if joined != en: bad += 1; print("TEXT MISMATCH", lid, "|", joined, "|", en)
        if mine:
            maxs = max(maxs, abs(mine[0][0] - ln["start"])); maxe = max(maxe, abs(mine[-1][1] - (ln["end"] + 0.18)))
print("subtitle text mismatches:", bad, "| max start offset", round(maxs, 3), "s | max end offset", round(maxe, 3), "s")
print("cues:", len(cues), "| max cue length", round(max(c[1] - c[0] for c in cues), 2), "s | min", round(min(c[1] - c[0] for c in cues), 2), "s")
# no overlaps
ov = [(cues[i][2], cues[i+1][2]) for i in range(len(cues) - 1) if cues[i][1] > cues[i+1][0] + 1e-3]
print("overlapping cues:", len(ov))

# ---- 4 durations
def probe(stream):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", stream, "-show_entries", "stream=duration", "-of", "default=nw=1:nk=1", MP4], capture_output=True, text=True)
    return float(r.stdout.strip())
print("video", probe("v:0"), "audio", probe("a:0"), "timeline", round(D, 3))
