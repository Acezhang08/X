"""Mix narration with a very quiet synthesized room tone + soft whooshes on big camera moves.

All ambience is generated here from noise (no third-party audio). Output: build/mix.wav (48 kHz stereo).
"""
import json, numpy as np, soundfile as sf

SR = 48000
T = json.load(open("build/timings.json"))
voice, vsr = sf.read("build/narration.wav")
# 24k -> 48k（线性插值即可，人声频带在 12k 以下）
n = int(len(voice) * SR / vsr)
voice = np.interp(np.arange(n) * vsr / SR, np.arange(len(voice)), voice)
dur = T["duration"]
N = int(dur * SR)
voice = np.pad(voice, (0, max(0, N - len(voice))))[:N]
rng = np.random.default_rng(7)

def lowpass(x, fc):  # FFT 实现，避免引入 scipy
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    return np.fft.irfft(X / (1 + (f / fc) ** 2), len(x))

def bandpass(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    H = 1 / (1 + (lo / np.maximum(f, 1)) ** 4) / (1 + (f / hi) ** 4)
    return np.fft.irfft(X * H, len(x))

def db(x): return 10 ** (x / 20)

# 房间底噪：低通棕噪，约 -50 dBFS RMS
room = np.stack([lowpass(np.cumsum(rng.standard_normal(N)) * 0.02, 180) for _ in range(2)], 1)
room -= room.mean(0)
room = room / np.sqrt((room ** 2).mean()) * db(-50)
fade = np.minimum(1, np.minimum(np.arange(N) / (0.8 * SR), (N - np.arange(N)) / (1.2 * SR)))
room *= fade[:, None]

# 镜头大动作上的轻 whoosh（-34 dBFS 峰值附近）
S = lambda i: T["lines"][i - 1]["start"]
whooshes = [3.2, S(5) - 0.1, S(9) - 0.05, S(11) - 0.4, S(13) - 0.55, S(15) - 0.3, S(17) - 0.55]
wh = np.zeros((N, 2))
for t0 in whooshes:
    L = int(1.1 * SR); a = int((t0 - 0.4) * SR)
    if a < 0 or a + L > N: continue
    env = np.sin(np.linspace(0, np.pi, L)) ** 3
    sweep = bandpass(rng.standard_normal(L), 300, 2200) * env
    sweep = sweep / np.abs(sweep).max() * db(-34)
    pan = np.linspace(0.3, 0.7, L)
    wh[a:a + L, 0] += sweep * (1 - pan) * 1.4
    wh[a:a + L, 1] += sweep * pan * 1.4

mix = np.stack([voice, voice], 1) + room + wh
peak = np.abs(mix).max()
mix = mix / peak * db(-1.0)
sf.write("build/mix.wav", mix.astype(np.float32), SR, subtype="PCM_24")
print("mix", round(len(mix) / SR, 2), "s; room rms dB", round(20 * np.log10(np.sqrt((room ** 2).mean())), 1))
