"""Generate the narration with Kokoro-82M (settings: see voice-settings.txt).

Writes build/narration.wav and build/timings.json (per-sentence start/end in seconds).
"""
import json, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro

VOICE, SPEED, LANG = "af_heart", 1.0, "en-us"
LEAD_IN, TAIL = 0.6, 1.9  # silence before first line / after last line (last subtitle holds >=1.5s)

import os; os.makedirs("build", exist_ok=True)
k = Kokoro("/opt/kokoro/kokoro-v1.0.onnx", "/opt/kokoro/voices-v1.0.bin")
script = json.load(open("script.json"))
sr, parts, t, timings = 24000, [], LEAD_IN, []
parts.append(np.zeros(int(LEAD_IN * sr), np.float32))

def trim(x, thr=0.004):
    idx = np.where(np.abs(x) > thr)[0]
    a, b = max(0, idx[0] - int(0.02 * sr)), min(len(x), idx[-1] + int(0.06 * sr))
    return x[a:b]

for i, line in enumerate(script):
    s, sr = k.create(line.get("tts", line["en"]), voice=VOICE, speed=SPEED, lang=LANG)
    s = trim(s.astype(np.float32))
    d = len(s) / sr
    timings.append({"i": i + 1, "start": round(t, 3), "end": round(t + d, 3), "en": line["en"], "zh": line["zh"], "g": line["g"]})
    parts.append(s)
    t += d
    gap = line["gap"] if i < len(script) - 1 else TAIL
    parts.append(np.zeros(int(gap * sr), np.float32))
    t += gap

audio = np.concatenate(parts)
audio = audio / max(1e-6, np.abs(audio).max()) * 0.89
sf.write("build/narration.wav", audio, sr)
total = len(audio) / sr
json.dump({"duration": round(total, 3), "lines": timings}, open("build/timings.json", "w"), ensure_ascii=False, indent=1)
for l in timings:
    print(f'{l["i"]:2d} {l["start"]:6.2f}-{l["end"]:6.2f} ({l["end"]-l["start"]:.2f}s) {l["en"]}')
print("total", round(total, 2))
