import re, json, os, sys, hashlib, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
sys.path.insert(0, os.path.dirname(__file__))
from script import SEGMENTS, spoken
SR = 24000
os.makedirs("build/tts", exist_ok=True)
k = Kokoro("build/kokoro.onnx", "build/voices.bin")

def chunks(en):
    # split into sentences on . ? ! (keeping char offsets), merge <=2-word ones into previous
    parts = []
    pos = 0
    for m in re.finditer(r"[.?!][\"']?(?=\s|$)", en):
        parts.append([pos, m.end()]); pos = m.end()
    if en[pos:].strip(): parts.append([pos, len(en)])
    merged = []
    for p in parts:
        words = len(en[p[0]:p[1]].split())
        if merged and words <= 2:
            merged[-1][1] = p[1]
        else:
            merged.append(p)
    return merged

def split_spoken(sp, n_en_chunks, en_chunks, en):
    # split spoken text into same number of sentence chunks using same merge rule
    return chunks(sp)

def trim(a, thr=0.004, pad=int(0.03*SR)):
    idx = np.where(np.abs(a) > thr)[0]
    if len(idx) == 0: return a
    return a[max(0, idx[0]-pad): min(len(a), idx[-1]+pad)]

timeline = []
audio = [np.zeros(int(1.2*SR), dtype=np.float32)]
t = 1.2
first = True
seg_start = {}
for seg, lines in SEGMENTS.items():
    for li, (lid, en, pre) in enumerate(lines):
        if first: first = False
        else:
            gap = 1.0 if li == 0 else (pre if pre is not None else 0.45)
            audio.append(np.zeros(int(gap*SR), dtype=np.float32)); t += gap
        if li == 0: seg_start[seg] = t
        sp = spoken(lid, en)
        ec = chunks(en); sc = chunks(sp)
        assert len(ec) == len(sc), (lid, ec, sc)
        line = dict(id=lid, seg=seg, en=en, chunks=[])
        line["start"] = t
        for ci, (e, s) in enumerate(zip(ec, sc)):
            if ci > 0:
                audio.append(np.zeros(int(0.45*SR), dtype=np.float32)); t += 0.45
            txt = sp[s[0]:s[1]].strip()
            fn = f"build/tts/{lid}_{ci}_{hashlib.md5(txt.encode()).hexdigest()[:8]}.npy"
            if os.path.exists(fn): a = np.load(fn)
            else:
                a, sr = k.create(txt, voice="am_michael", speed=0.97, lang="en-us")
                assert sr == SR
                a = trim(a.astype(np.float32)); np.save(fn, a)
            d = len(a)/SR
            line["chunks"].append(dict(t0=t, t1=t+d, c0=e[0], c1=e[1], text=txt))
            audio.append(a); t += d
        line["end"] = t
        timeline.append(line)
        print(lid, round(line["start"],2), round(line["end"],2), flush=True)
audio.append(np.zeros(int(2.5*SR), dtype=np.float32)); t += 2.5
wav = np.concatenate(audio)
sf.write("build/voice.wav", wav, SR)
json.dump(dict(lines=timeline, seg_start=seg_start, duration=len(wav)/SR), open("build/timeline.json","w"), indent=1)
print("TOTAL", len(wav)/SR, seg_start)
