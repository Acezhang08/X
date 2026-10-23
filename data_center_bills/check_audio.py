# -*- coding: utf-8 -*-
"""Numeric audio checks (no sound card): onset of every sentence vs timeline.json, clipping, long silences, loudness."""
import json, numpy as np, soundfile as sf, subprocess, re
d = json.load(open("timeline.json"))
x, sr = sf.read("build/final_audio.wav"); x = np.asarray(x)
print("samples", len(x), "sr", sr, "dur", round(len(x)/sr, 2), "timeline dur", round(d["duration"], 2))
print("peak", round(float(np.abs(x).max()), 4), "clipped samples (|x|>=0.999):", int((np.abs(x) >= 0.999).sum()))
env = np.abs(x); k = int(0.01*sr); env = np.convolve(env, np.ones(k)/k, mode="same")
thr = 0.01
bad = []; offs = []
for l in d["lines"]:
    for ch in l["chunks"]:
        a = int(ch["t0"]*sr); w0, w1 = max(0, a - int(0.25*sr)), a + int(0.6*sr)
        seg = env[w0:w1] > thr
        if not seg.any(): bad.append((l["id"], "silent")); continue
        onset = (np.argmax(seg) + w0)/sr
        offs.append(onset - ch["t0"])
        if abs(onset - ch["t0"]) > 0.08: bad.append((l["id"], round(onset - ch["t0"], 3)))
offs = np.array(offs)
print("chunks", len(offs), "onset offset mean %.3f s, max |.| %.3f s" % (offs.mean(), np.abs(offs).max()), "outliers>80ms:", bad[:10])
# silences longer than 2 s inside speech
sil = env < 0.002; runs = []; start = None
for i, s in enumerate(sil):
    if s and start is None: start = i
    if not s and start is not None:
        if (i - start)/sr > 1.6: runs.append((round(start/sr, 1), round(i/sr, 1)))
        start = None
if start is not None and (len(sil) - start)/sr > 1.6: runs.append((round(start/sr, 1), round(len(sil)/sr, 1)))
print("silence runs > 1.6 s:", runs)
