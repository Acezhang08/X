# -*- coding: utf-8 -*-
"""Mix: music bed (A -> B -> C cross-faded at narrative turns) under the voice, ducked by side-chain,
slightly lifted in the segment-change pauses. Final loudness -14 LUFS."""
import numpy as np, soundfile as sf, subprocess, json, re, sys, os
from timeline import Timeline
T = Timeline(); SR = 44100
S2 = T.seg_start[2]; S5 = T.seg_start[5]; D = T.duration
BED_DB = float(sys.argv[1]) if len(sys.argv) > 1 else -15.0
MD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "music", "history_series")
def load(n): return sf.read(os.path.join(MD, n + ".wav"))[0]
A, B, C = load("history_A_curious"), load("history_B_tense"), load("history_C_open")
N = int((D + 1) * SR); bed = np.zeros((N, 2)); X = 4.0
def fin(x, k): k = min(int(k * SR), len(x)); x[:k] *= np.sin(np.linspace(0, np.pi / 2, k))[:, None]; return x
def put(x, start):
    s0 = int(start * SR); n = min(len(x), N - s0); bed[s0:s0 + n] += x[:n]
a = A.copy(); k0 = int((S2 - X / 2) * SR); k = int(X * SR); a = a[:k0 + k]; a[k0:] *= np.cos(np.linspace(0, np.pi / 2, k))[:, None]; put(a, 0)
b = fin(B.copy(), X); kk0 = int((S5 - S2) * SR); b = b[:kk0 + k]; b[kk0:] *= np.cos(np.linspace(0, np.pi / 2, k))[:, None]; put(b, S2 - X / 2)
c = fin(C.copy(), X); put(c, S5 - X / 2)
# lift +3 dB during the pauses between segments (smoothed)
env = np.ones(N)
for sg, st in T.seg_start.items():
    if sg == 0: continue
    prev_end = max(l["end"] for l in T.lines.values() if l["seg"] == sg - 1)
    i0, i1 = int((prev_end - 0.3) * SR), int((st + 0.3) * SR)
    ramp = np.sin(np.linspace(0, np.pi, i1 - i0)) ** 2
    env[i0:i1] *= 10 ** (3.0 * ramp / 20)
bed *= env[:, None]
sf.write("build/bed.wav", (bed * 10 ** (BED_DB / 20)).astype(np.float32), SR, subtype="FLOAT")

SC = "sidechaincompress=threshold=0.02:ratio=4:attack=50:release=800:makeup=1"
def run(cmd): return subprocess.run(cmd, capture_output=True, text=True)
EQ = "aresample=48000,highpass=f=70,equalizer=f=250:t=h:w=300:g=-2"
fc = f"[0:a]{EQ}[m];[1:a]aresample=48000,asplit=2[v][vs];[m][vs]{SC}[md];[v][md]amix=inputs=2:normalize=0:duration=longest,afade=t=out:st={D-2.2}:d=2.2[o]"
common = ["ffmpeg", "-y", "-i", "build/bed.wav", "-i", "build/voice.wav", "-filter_complex"]
r = run(common + [fc.replace("[o]", "[o1]") + ";[o1]loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json[o]", "-map", "[o]", "-f", "null", "-"])
j = json.loads(re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", r.stderr, re.S).group(0))
ln = f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}:measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true"
r = run(common + [fc.replace("[o]", "[o1]") + ";[o1]" + ln + "[o]", "-map", "[o]", "-ar", "48000", "-t", str(D), "build/final_audio.wav"])
# diagnostics: ducked music-only track
run(["ffmpeg", "-y", "-i", "build/bed.wav", "-i", "build/voice.wav", "-filter_complex", f"[0:a]{EQ}[m];[1:a]aresample=48000[v];[m][v]{SC}[o]", "-map", "[o]", "-t", str(D), "build/music_ducked.wav"])
r = run(["ffmpeg", "-i", "build/final_audio.wav", "-af", "ebur128=peak=true", "-f", "null", "-"])
print("LUFS", re.findall(r"I:\s+(-?\d+\.\d) LUFS", r.stderr)[-1:], "peak", re.findall(r"Peak:\s+(-?\d+\.\d) dBFS", r.stderr)[-1:])
