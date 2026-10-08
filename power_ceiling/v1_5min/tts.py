import sys, json, numpy as np, soundfile as sf
sys.path.insert(0, '.')
from script import LINES, TTS_FIX
from kokoro_onnx import Kokoro
k = Kokoro('/tmp/claude-0/w/models/kokoro-v1.0.onnx', '/tmp/claude-0/w/models/voices-v1.0.bin')
VOICE, SPEED = 'am_michael', 0.97
SR = 24000
def fix(t):
    for a, b in sorted(TTS_FIX.items(), key=lambda x: -len(x[0])): t = t.replace(a, b)
    return t
out, t, tl = [], 0.0, []
prev = None
for L in LINES:
    s, sr = k.create(fix(L['en']), voice=VOICE, speed=SPEED, lang='en-us')
    assert sr == SR
    # trim leading/trailing silence
    nz = np.where(np.abs(s) > 0.004)[0]; s = s[nz[0]:nz[-1] + 1]
    # pause before this line
    if prev is None: gap = 1.2
    elif L['sec'] != prev: gap = 1.0
    elif L['id'] in ('0.5','1.4','2.2','6.1'): gap = 0.8
    else: gap = 0.45
    if L['id'] == '0.5': gap = 0.5
    out.append(np.zeros(int(gap * SR), np.float32)); t += gap
    d = len(s) / SR
    tl.append(dict(id=L['id'], sec=L['sec'], start=round(t, 3), end=round(t + d, 3), en=L['en'], zh=L['zh']))
    out.append(s.astype(np.float32)); t += d; prev = L['sec']
    print(L['id'], round(t - d, 2), round(d, 2), flush=True)
out.append(np.zeros(int(2.5 * SR), np.float32)); t += 2.5
sf.write('narration.wav', np.concatenate(out), SR)
json.dump(dict(total=round(t, 3), lines=tl), open('timeline.json', 'w'), ensure_ascii=False, indent=1)
print('TOTAL', t)
