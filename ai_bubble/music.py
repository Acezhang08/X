# -*- coding: utf-8 -*-
"""Synthesised background music for the 'AI money' series (no samples, no downloads)."""
import numpy as np, soundfile as sf, os, json
from scipy.signal import butter, sosfilt, sosfilt_zi, fftconvolve
SR = 44100
rng = np.random.default_rng(42)

def t_axis(d): return np.arange(int(d * SR)) / SR

def saw(freq, tt, detune_cents=(0,), phase_seed=0):
    out = np.zeros_like(tt)
    r = np.random.default_rng(phase_seed)
    for i, dc in enumerate(detune_cents):
        f = freq * 2 ** (dc / 1200)
        ph = r.uniform(0, 1)
        out += 2 * ((f * tt + ph) % 1.0) - 1
    return out / len(detune_cents)

def sweep_lp(x, cutoffs, block=2048, order=2):
    """time-varying low-pass: cutoffs = function of time (array per sample); filtered per block with state carried."""
    out = np.zeros_like(x); zi = None
    for s in range(0, len(x), block):
        fc = float(np.clip(cutoffs[min(s + block // 2, len(x) - 1)], 40, SR * 0.45))
        sos = butter(order, fc / (SR / 2), btype="low", output="sos")
        if zi is None: zi = sosfilt_zi(sos) * x[s]
        seg, zi = sosfilt(sos, x[s:s + block], zi=zi)
        out[s:s + block] = seg
    return out

def lp(x, fc, order=2): return sosfilt(butter(order, fc / (SR/2), "low", output="sos"), x)
def hp(x, fc, order=2): return sosfilt(butter(order, fc / (SR/2), "high", output="sos"), x)

def reverb(x, secs=3.5, wet=0.35, seed=1):
    r = np.random.default_rng(seed); n = int(secs * SR)
    out = []
    for ch in range(2):
        ir = r.normal(0, 1, n) * np.exp(-np.arange(n) / (SR * secs / 4.5))
        ir = lp(ir, 4500); ir /= np.sqrt(np.sum(ir**2))
        out.append(fftconvolve(x, ir)[:len(x)])
    wet_sig = np.stack(out, 1)
    return (1 - wet) * np.stack([x, x], 1) + wet * wet_sig

def stereo(x, pan=0.0):
    l = np.cos((pan + 1) * np.pi / 4); r = np.sin((pan + 1) * np.pi / 4)
    return np.stack([x * l, x * r], 1)

def norm(x, peak=0.5):
    return x * (peak / (np.max(np.abs(x)) + 1e-9))

# ------------------------------------------------------------------ A: open (A minor, 90 BPM)
def music_A(dur):
    tt = t_axis(dur)
    cut = 260 + 340 * (0.5 + 0.5 * np.sin(2 * np.pi * tt / 38 - 1.2))
    drone = saw(55.0, tt, (-7, 0, 6), 1) * 0.8 + saw(82.41, tt, (-5, 5), 2) * 0.45 + saw(130.81, tt, (-9, 8), 3) * 0.18
    drone = sweep_lp(drone, cut)
    drone *= 0.75 + 0.25 * np.sin(2 * np.pi * tt / 11.0)
    # soft filtered pulse, 90 BPM eighth notes (0.3333 s), accent on beats
    beat = 60 / 90; step = beat / 2
    pulse = np.zeros_like(tt)
    notes = [110.0, 110.0, 164.81, 110.0, 130.81, 110.0, 146.83, 110.0]
    for i in range(int(dur / step)):
        t0 = i * step; s0 = int(t0 * SR); n = int(0.28 * SR)
        if s0 + n > len(tt): break
        seg_t = np.arange(n) / SR
        f = notes[i % len(notes)]
        env = np.exp(-seg_t / 0.07) * (1.0 if i % 2 == 0 else 0.55)
        tone = (2 * ((f * seg_t) % 1.0) - 1) * 0.5 + np.sin(2 * np.pi * f * seg_t) * 0.5
        pulse[s0:s0 + n] += tone * env
    pulse = lp(pulse, 700, 3) * (0.55 + 0.45 * np.sin(2 * np.pi * tt / 23.0 + 0.8))
    # faint tick (filtered noise) on off-beats
    tick = np.zeros_like(tt)
    for i in range(int(dur / beat)):
        s0 = int((i * beat + step) * SR); n = int(0.03 * SR)
        if s0 + n > len(tt): break
        tick[s0:s0 + n] += rng.normal(0, 1, n) * np.exp(-np.arange(n) / (SR * 0.008))
    tick = hp(tick, 3500) * 0.06
    left = stereo(drone * 0.9, 0.0) + stereo(pulse * 0.55, -0.35) + stereo(np.roll(pulse, int(step * SR)) * 0.25, 0.4) + stereo(tick, 0.2)
    left = reverb(left[:, 0] + left[:, 1], 1.6, 0.18, 7) * 0.5 + left * 0.5
    return norm(left, 0.5)

# ------------------------------------------------------------------ B: tension (E drone, cold)
def music_B(dur):
    tt = t_axis(dur)
    lfo = 0.5 + 0.5 * np.sin(2 * np.pi * tt / 17.0)
    cut = 120 + 260 * lfo + 60 * np.sin(2 * np.pi * tt / 5.3)
    d = saw(41.2, tt, (-9, 0, 8), 11) * 1.0 + saw(61.74, tt, (-6, 7), 12) * 0.5 + saw(87.31, tt, (-12, 10), 13) * 0.22 * (0.4 + 0.6 * np.sin(2 * np.pi * tt / 29.0 + 1.0) ** 2)
    d = sweep_lp(d, cut, order=3)
    d *= 0.7 + 0.3 * np.sin(2 * np.pi * tt / 7.3 + 0.6)
    # very weak heartbeat
    hb = np.zeros_like(tt); per = 1.25
    for i in range(int(dur / per)):
        for off, amp in ((0.0, 1.0), (0.23, 0.6)):
            s0 = int((i * per + off) * SR); n = int(0.4 * SR)
            if s0 + n > len(tt): continue
            x = np.arange(n) / SR
            hb[s0:s0 + n] += amp * np.sin(2 * np.pi * (46 - 12 * x) * x) * np.exp(-x / 0.1)
    hb = lp(hb, 120) * 0.22
    # high cold shimmer
    sh = hp(rng.normal(0, 1, len(tt)), 5000) * 0.012 * (0.4 + 0.6 * lfo)
    mix = stereo(d, 0) + stereo(hb, 0) + stereo(sh, 0.3)
    mix = reverb(mix[:, 0] + mix[:, 1], 2.4, 0.2, 9) * 0.45 + mix * 0.55
    return norm(mix, 0.5)

# ------------------------------------------------------------------ C: wide (open fifths pad, reverb)
def music_C(dur):
    tt = t_axis(dur)
    chords = [(73.42, 110.0, 164.81, 220.0), (98.0, 146.83, 196.0, 293.66), (110.0, 164.81, 220.0, 329.63), (73.42, 110.0, 164.81, 246.94)]
    seg = 20.0
    pad = np.zeros_like(tt)
    for ci in range(int(dur / seg) + 2):
        ch = chords[ci % len(chords)]
        t0 = ci * seg - 3.0
        env = np.clip((tt - t0) / 6.0, 0, 1) * np.clip(1 - (tt - (t0 + seg + 3.0)) / 6.0, 0, 1)
        if env.max() <= 0: continue
        v = np.zeros_like(tt)
        for k, f in enumerate(ch):
            v += saw(f, tt, (-8, 0, 8), 30 + ci * 4 + k) * (0.5 if k < 2 else 0.35)
        pad += v * env
    cut = 900 + 900 * (0.5 + 0.5 * np.sin(2 * np.pi * tt / 31.0))
    pad = sweep_lp(pad, cut, order=2)
    pad *= 0.8 + 0.2 * np.sin(2 * np.pi * tt / 9.0)
    # airy high sine shimmer: fifth drones
    air = (np.sin(2 * np.pi * 659.26 * tt) * 0.05 + np.sin(2 * np.pi * 987.77 * tt) * 0.03) * (0.5 + 0.5 * np.sin(2 * np.pi * tt / 13.0))
    mix = reverb(pad + air, 4.0, 0.45, 5)
    return norm(mix, 0.5)

if __name__ == "__main__":
    from timeline import Timeline
    T = Timeline(); S2 = T.seg_start[2]; S5 = T.seg_start[5]; D = T.duration
    os.makedirs("music/money_series", exist_ok=True)
    spec = {"money_A_open": (S2 + 4), "money_B_tension": (S5 - S2 + 6), "money_C_wide": (D - S5 + 4)}
    for name, fn in (("money_A_open", music_A), ("money_B_tension", music_B), ("money_C_wide", music_C)):
        x = fn(spec[name]); sf.write(f"music/money_series/{name}.wav", x.astype(np.float32), SR, subtype="PCM_16")
        print(name, len(x) / SR, float(np.sqrt(np.mean(x**2))))
