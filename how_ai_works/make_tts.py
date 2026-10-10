# -*- coding: utf-8 -*-
"""Kokoro 配音 -> narration.wav + timeline.json + 字幕 srt"""
import json, sys, os
import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro
sys.path.insert(0, os.path.dirname(__file__))
from narration import ROWS, SEGMENTS, tts_text

HERE = os.path.dirname(os.path.abspath(__file__))
SR = 24000
VOICE, SPEED, LANG = "am_michael", 0.97, "en-us"
PAUSE_ROW, GAP_SENT, GAP_CLAUSE, TAIL = 0.45, 0.45, 0.18, 2.5

kokoro = Kokoro(f"{HERE}/assets/kokoro-v1.0.onnx", f"{HERE}/assets/voices-v1.0.bin")


def synth(text):
    s, sr = kokoro.create(tts_text(text), voice=VOICE, speed=SPEED, lang=LANG)
    assert sr == SR
    # 裁掉首尾静音，停顿由我们自己精确控制
    a = np.abs(s)
    idx = np.where(a > 0.004)[0]
    if len(idx):
        s = s[max(0, idx[0] - int(0.02 * SR)): idx[-1] + int(0.04 * SR)]
    return s.astype(np.float32)


def sil(sec):
    return np.zeros(int(round(sec * SR)), dtype=np.float32)


parts, t = [], 0.0
timeline = {"rows": [], "chunks": []}
seg_first = {}
for rid, chunks, pause in ROWS:
    seg = rid.split(".")[0]
    p = pause if pause is not None else PAUSE_ROW
    parts.append(sil(p)); t += p
    row_start = t
    for ci, (en, zh) in enumerate(chunks):
        if ci > 0:
            g = GAP_SENT if chunks[ci - 1][0].rstrip('"').endswith((".", "?", "!")) else GAP_CLAUSE
            parts.append(sil(g)); t += g
        a = synth(en)
        d = len(a) / SR
        timeline["chunks"].append({"row": rid, "i": ci, "en": en, "zh": zh, "start": round(t, 3), "end": round(t + d, 3)})
        parts.append(a); t += d
        print(f"{rid}.{ci} {d:.2f}s  {en[:50]}", flush=True)
    timeline["rows"].append({"id": rid, "seg": seg, "pause": p, "start": round(row_start, 3), "end": round(t, 3)})
    seg_first.setdefault(seg, (rid, p, row_start))
parts.append(sil(TAIL)); t += TAIL

audio = np.concatenate(parts)
sf.write(f"{HERE}/build/narration.wav", audio, SR)
timeline["total"] = round(len(audio) / SR, 3)

# 分段边界：每段从"停顿开始处"算起，保证首尾相接
names = [s for s, _ in SEGMENTS]
bounds = []
for k, s in enumerate(names):
    rid, p, rs = seg_first[s]
    begin = 0.0 if k == 0 else rs - p
    bounds.append(begin)
bounds.append(timeline["total"])
timeline["segments"] = [{"id": names[k], "begin": round(bounds[k], 3), "end": round(bounds[k + 1], 3)} for k in range(len(names))]
json.dump(timeline, open(f"{HERE}/build/timeline.json", "w"), ensure_ascii=False, indent=1)


def ts(x):
    h, m, s = int(x // 3600), int(x % 3600 // 60), x % 60
    return f"{h:02d}:{m:02d}:{int(s):02d},{int(round((s - int(s)) * 1000)):03d}"


for lang in ("en", "zh"):
    with open(f"{HERE}/subtitles_{lang}.srt", "w", encoding="utf-8") as f:
        for n, c in enumerate(timeline["chunks"], 1):
            f.write(f"{n}\n{ts(c['start'])} --> {ts(c['end'] + 0.05)}\n{c[lang]}\n\n")
print("TOTAL", timeline["total"], "sec =", round(timeline["total"] / 60, 2), "min")
