# -*- coding: utf-8 -*-
"""Numeric audio QA on the final mp4: loudness, true peak, clipping, long silences, per-sentence voice alignment."""
import sys, json, subprocess, numpy as np, soundfile as sf, pyloudnorm as pln
from scipy.signal import resample_poly
MP4 = sys.argv[1] if len(sys.argv) > 1 else "ai_video_real.mp4"
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", MP4, "-vn", "-ac", "1", "-ar", "48000", "build/_final_dec.wav"], check=True)
x, sr = sf.read("build/_final_dec.wav")
m = pln.Meter(sr); L = m.integrated_loudness(x)
tp = 20 * np.log10(np.max(np.abs(resample_poly(x, 4, 1))) + 1e-12)
print(f"integrated loudness {L:.2f} LUFS | true peak {tp:.2f} dBTP | sample peak {20*np.log10(np.abs(x).max()):.2f} dBFS | duration {len(x)/sr:.2f}s")
print("clipped samples (|x|>=0.999):", int((np.abs(x) >= 0.999).sum()))
# silence runs (frame RMS < -50 dBFS)
hop = int(0.02 * sr); n = len(x) // hop
rms = np.array([np.sqrt(np.mean(x[i*hop:(i+1)*hop] ** 2) + 1e-12) for i in range(n)]); db = 20 * np.log10(rms)
sil = db < -50; runs = []; i = 0
while i < n:
    if sil[i]:
        j = i
        while j < n and sil[j]: j += 1
        runs.append((i * .02, j * .02)); i = j
    else: i += 1
d = json.load(open("build/timeline.json")); D = d["duration"]
long_ = [(round(a, 2), round(b, 2), round(b - a, 2)) for a, b in runs if b - a > 1.0]
print("silence runs > 1.0 s:", long_)
seg_gaps = sorted([l["start"] for l in d["lines"] if l["id"].endswith(".1") or l["id"].split(".")[1] == "1"])
print("expected: intro 0-1.2, segment gaps ~1.0 s (6), outro 2.5 s")
extra = [r for r in long_ if r[2] > 1.25 and not (r[0] < 0.1 or r[1] > D - 2.6)]
print("unexpected long silences (>1.25 s, not intro/outro):", extra)
# alignment: voice energy right after each line start vs just before
bad = 0
for l in d["lines"]:
    a = int((l["start"] + .05) * sr); b = int((l["start"] + .35) * sr); pa = int((l["start"] - .3) * sr)
    after = np.sqrt(np.mean(x[a:b] ** 2)); before = np.sqrt(np.mean(x[max(0, pa):a - int(.1*sr)] ** 2)) if pa > 0 else 0
    e = int((l["end"] - .3) * sr); f = int((l["end"] - .05) * sr); g = int((l["end"] + .1) * sr); h = int((l["end"] + .4) * sr)
    end_in = np.sqrt(np.mean(x[e:f] ** 2)); end_out = np.sqrt(np.mean(x[g:min(len(x), h)] ** 2)) if h < len(x) else 0
    if after < 3 * before or after < 0.003 or end_in < 3 * end_out: bad += 1; print("misaligned?", l["id"], round(after, 4), round(before, 4), round(end_in, 4), round(end_out, 4))
print("lines checked", len(d["lines"]), "misaligned", bad)
