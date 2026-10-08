import sys, json, numpy as np, soundfile as sf
sys.path.insert(0, '.')
from script import LINES, spoken
from kokoro_onnx import Kokoro
k = Kokoro('/tmp/claude-0/w/models/kokoro-v1.0.onnx', '/tmp/claude-0/w/models/voices-v1.0.bin')
VOICE, SPEED = 'am_michael', 0.97      # 与 5 分钟版相同的 TTS 与声音
SR = 24000
PAUSE_BEFORE = {'0.5': .5, '0.6': .6, '1.10': .8, '3.2': .8, '7.1': .8, '7.6': .6, '5.9': .6}
out, t, tl, prev = [], 0.0, [], None
for L in LINES:
    s, sr = k.create(spoken(L['en']), voice=VOICE, speed=SPEED, lang='en-us'); assert sr == SR
    nz = np.where(np.abs(s) > 0.004)[0]; s = s[nz[0]:nz[-1] + 1]
    gap = 1.2 if prev is None else 1.0 if L['sec'] != prev else PAUSE_BEFORE.get(L['id'], .45)
    out.append(np.zeros(int(gap * SR), np.float32)); t += gap
    d = len(s) / SR
    tl.append(dict(id=L['id'], sec=L['sec'], start=round(t, 3), end=round(t + d, 3), en=L['en'], zh=L['zh']))
    out.append(s.astype(np.float32)); t += d; prev = L['sec']
    print(L['id'], round(t - d, 2), round(d, 2), flush=True)
out.append(np.zeros(int(2.5 * SR), np.float32)); t += 2.5
sf.write('narration.wav', np.concatenate(out), SR)
json.dump(dict(total=round(t, 3), lines=tl), open('timeline.json', 'w'), ensure_ascii=False, indent=1)
print('TOTAL', t)
