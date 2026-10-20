# -*- coding: utf-8 -*-
"""Voice only. 48 kHz mono. Gain to -14 LUFS integrated, look-ahead peak limiter so true peak <= -1.2 dBTP."""
import numpy as np, soundfile as sf, pyloudnorm as pln
from scipy.signal import resample_poly
from scipy.ndimage import minimum_filter1d, uniform_filter1d
x, sr = sf.read("build/voice.wav"); x = x.astype(np.float64)
x = resample_poly(x, 2, 1); sr = 48000                       # 24k -> 48k
meter = pln.Meter(sr)
def limit(y, thr, look=240):
    need = np.minimum(1.0, thr / np.maximum(np.abs(y), 1e-9))
    g = minimum_filter1d(need, size=look * 2 + 1, mode="nearest")
    g = uniform_filter1d(g, size=look + 1, mode="nearest")
    return y * np.minimum(g, 1.0) if False else y * g
def tp(y): return 20 * np.log10(np.max(np.abs(resample_poly(y, 4, 1))) + 1e-12)
g_db = -14.0 - meter.integrated_loudness(x)
thr = 10 ** (-2.2 / 20)
for it in range(12):
    y = limit(x * 10 ** (g_db / 20), thr)
    L = meter.integrated_loudness(y); T = tp(y)
    if abs(L + 14.0) < 0.05 and T <= -1.15: break
    g_db += (-14.0 - L) * 0.9
    thr = thr * (10 ** (min(0, -1.2 - T) / 20)) if T > -1.2 else thr
print(f"integrated {L:.2f} LUFS, true peak {T:.2f} dBTP, sample peak {20*np.log10(np.abs(y).max()):.2f} dBFS, gain {g_db:.2f} dB")
sf.write("build/final_audio.wav", y.astype(np.float32), sr, subtype="PCM_24")
