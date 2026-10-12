# -*- coding: utf-8 -*-
import numpy as np, soundfile as sf, subprocess, json, re, sys
from timeline import Timeline
T = Timeline(); SR = 44100
S2 = T.seg_start[2]; S5 = T.seg_start[5]; D = T.duration
BED_DB = float(sys.argv[1]) if len(sys.argv) > 1 else -15.0

def load(n): return sf.read(f"music/money_series/{n}.wav")[0]
A, B, C = load("money_A_open"), load("money_B_tension"), load("money_C_wide")
N = int((D + 1) * SR); bed = np.zeros((N, 2))
X = 3.0
def put(x, start, fin=None, fout=None):
    s0 = int(start * SR); x = x.copy()
    n = min(len(x), N - s0); x = x[:n]
    if fin:
        k = min(int(fin * SR), n); x[:k] *= np.sin(np.linspace(0, np.pi/2, k))[:, None]
    if fout:
        k = int(fout * SR); x[n-k:] *= np.cos(np.linspace(0, np.pi/2, k))[:, None] if n >= k else 1
    bed[s0:s0 + n] += x
# A: fades out across [S2-1.5, S2+1.5]
a = A.copy(); k0 = int((S2 - X/2) * SR); k = int(X * SR)
a = a[:k0 + k]; a[k0:] *= np.cos(np.linspace(0, np.pi/2, k))[:, None]
put(a, 0)
b = B.copy(); kb = int(X * SR); b[:kb] *= np.sin(np.linspace(0, np.pi/2, kb))[:, None]
kk0 = int((S5 - X/2 - (S2 - X/2)) * SR); b = b[:kk0 + kb]; b[kk0:] *= np.cos(np.linspace(0, np.pi/2, kb))[:, None]
put(b, S2 - X/2)
c = C.copy(); c[:kb] *= np.sin(np.linspace(0, np.pi/2, kb))[:, None]
put(c, S5 - X/2)
sf.write("build/bed.wav", (bed * 10 ** (BED_DB/20)).astype(np.float32), SR, subtype="FLOAT")

SC = "sidechaincompress=threshold=0.01:ratio=14:attack=40:release=800:makeup=1"
def run(cmd): return subprocess.run(cmd, capture_output=True, text=True)
# music-only after ducking (for diagnostics)
fc = f"[0:a]aresample=48000,highpass=f=35,equalizer=f=300:t=h:w=350:g=-4[m];[1:a]aresample=48000,asplit=2[v][vs];[m][vs]{SC}[md]"
run(["ffmpeg", "-y", "-i", "build/bed.wav", "-i", "build/voice.wav", "-filter_complex", fc + ";[md]anull[o]", "-map", "[o]", "-t", str(D), "build/music_ducked.wav"])
fc = f"[0:a]aresample=48000,highpass=f=35,equalizer=f=300:t=h:w=350:g=-4[m];[1:a]aresample=48000,asplit=2[v][vs];[m][vs]{SC}[md];[v][md]amix=inputs=2:normalize=0:duration=longest,afade=t=out:st={D-2.2}:d=2.2[o]"
common = ["ffmpeg", "-y", "-i", "build/bed.wav", "-i", "build/voice.wav", "-filter_complex"]
r = run(common + [fc.replace("[o]", "[o1]") + ";[o1]loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json[o]", "-map", "[o]", "-f", "null", "-"])
j = json.loads(re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", r.stderr, re.S).group(0)); print(j)
ln = f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}:measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true"
r = run(common + [fc.replace("[o]", "[o1]") + ";[o1]" + ln + "[o]", "-map", "[o]", "-ar", "48000", "-t", str(D), "build/final_audio.wav"])
print(r.stderr[-300:])
r = run(["ffmpeg", "-i", "build/final_audio.wav", "-af", "ebur128=peak=true", "-f", "null", "-"]); print(re.findall(r"I:\s+(-?\d+\.\d) LUFS", r.stderr)[-1:], re.findall(r"Peak:\s+(-?\d+\.\d) dBFS", r.stderr)[-1:])
