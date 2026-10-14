# -*- coding: utf-8 -*-
"""Synthesised background music for the 'AI history' series (no samples, nothing downloaded).
Warm, nostalgic, minimal: a very soft sustained pad (low-passed to 100-300 Hz so it never clouds the voice)
plus sparse piano-like plucked notes. Three moods: A curious / B tense / C open."""
import numpy as np, soundfile as sf, os, sys
from scipy.signal import butter, sosfilt, sosfilt_zi, fftconvolve
SR = 44100
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "music", "history_series")

def t_axis(d): return np.arange(int(d * SR)) / SR
def lp(x, fc, order=2): return sosfilt(butter(order, fc / (SR / 2), "low", output="sos"), x)
def hp(x, fc, order=2): return sosfilt(butter(order, fc / (SR / 2), "high", output="sos"), x)

def sweep_lp(x, cutoffs, block=2048, order=2):
    out = np.zeros_like(x); zi = None
    for s in range(0, len(x), block):
        fc = float(np.clip(cutoffs[min(s + block // 2, len(x) - 1)], 60, SR * 0.45))
        sos = butter(order, fc / (SR / 2), btype="low", output="sos")
        if zi is None: zi = sosfilt_zi(sos) * x[s]
        seg, zi = sosfilt(sos, x[s:s + block], zi=zi); out[s:s + block] = seg
    return out

def reverb(x, secs=3.5, wet=0.35, seed=1):
    r = np.random.default_rng(seed); n = int(secs * SR); chans = []
    for ch in range(2):
        ir = r.normal(0, 1, n) * np.exp(-np.arange(n) / (SR * secs / 4.5))
        ir = lp(ir, 4200); ir /= np.sqrt(np.sum(ir ** 2)); chans.append(fftconvolve(x, ir)[:len(x)])
    w = np.stack(chans, 1)
    return (1 - wet) * np.stack([x, x], 1) + wet * w

def note_hz(name):
    names = {"C": 0, "C#": 1, "D": 2, "Eb": 3, "E": 4, "F": 5, "F#": 6, "G": 7, "Ab": 8, "A": 9, "Bb": 10, "B": 11}
    p = name[:-1]; o = int(name[-1]); return 440.0 * 2 ** ((names[p] + 12 * (o + 1) - 69) / 12)

def pluck(f, dur=3.2, vel=1.0, seed=0):
    """Soft felt-piano-ish tone: few decaying partials + short filtered 'hammer' noise."""
    n = int(dur * SR); tt = np.arange(n) / SR; r = np.random.default_rng(seed)
    y = np.zeros(n)
    for k, (amp, dec) in enumerate(((1.0, 1.7), (0.42, 0.8), (0.16, 0.38), (0.06, 0.2)), 1):
        det = 1 + r.uniform(-0.0006, 0.0006)
        y += amp * np.sin(2 * np.pi * f * k * det * tt + r.uniform(0, 6.28)) * np.exp(-tt / dec)
    att = np.minimum(1, tt / 0.006); y *= att
    nz = r.normal(0, 1, int(0.03 * SR)); nz = lp(nz, 1800) * np.exp(-np.arange(len(nz)) / (SR * 0.006)) * 0.10
    y[:len(nz)] += nz
    return y * vel

def place(buf, y, t0):
    s0 = int(t0 * SR)
    if s0 >= len(buf): return
    n = min(len(y), len(buf) - s0); buf[s0:s0 + n] += y[:n]

def pad(dur, chords, seg, cut_lo=110, cut_hi=290, tremolo=None, seed=0):
    """Slow overlapping sustained chords (root/fifth/octave, 80-200 Hz), low-passed to 100-300 Hz."""
    tt = t_axis(dur); r = np.random.default_rng(seed); out = np.zeros_like(tt)
    for ci in range(int(dur / seg) + 2):
        ch = chords[ci % len(chords)]; t0 = ci * seg - 4.0
        env = np.clip((tt - t0) / 5.0, 0, 1) * np.clip(1 - (tt - (t0 + seg + 4.0)) / 5.0, 0, 1)
        if env.max() <= 0: continue
        v = np.zeros_like(tt)
        for k, f in enumerate(ch):
            for dc in (-6, 5):
                f2 = f * 2 ** (dc / 1200)
                v += (np.sin(2 * np.pi * f2 * tt + r.uniform(0, 6.28)) + 0.35 * np.sin(4 * np.pi * f2 * tt + r.uniform(0, 6.28))) * (0.6 if k == 0 else 0.4)
        out += v * env
    cut = cut_lo + (cut_hi - cut_lo) * (0.5 + 0.5 * np.sin(2 * np.pi * tt / 27.0))
    out = sweep_lp(out, cut, order=3)
    out = hp(out, 85, 2)
    out *= 0.8 + 0.2 * np.sin(2 * np.pi * tt / 9.0)
    if tremolo: out *= 1 - tremolo + tremolo * (0.5 + 0.5 * np.sin(2 * np.pi * tt / 4.3))
    return out

def plucks(dur, scale, rate, vel_range, octave_shift=0, seed=0, motif=None, hi=0):
    """Sparse plucked notes; `rate` = mean seconds between notes."""
    r = np.random.default_rng(seed); buf = np.zeros(int(dur * SR) + SR * 4); t = r.uniform(1.0, 2.5); idx = 0
    while t < dur - 1:
        name = motif[idx % len(motif)] if motif else scale[r.integers(len(scale))]
        f = note_hz(name) * (2 ** octave_shift)
        y = pluck(f, 3.4, r.uniform(*vel_range), seed=int(t * 10))
        place(buf, y, t)
        if hi and r.random() < 0.18: place(buf, pluck(f * 2, 2.4, vel_range[0] * 0.5, seed=int(t * 7)), t + 0.34)   # occasional soft octave echo
        idx += 1; t += rate * r.uniform(0.7, 1.45)
    return buf[:int(dur * SR)]

def stereo_mix(pad_sig, pl_sig, pad_gain, pl_gain, rev_secs, wet, seed):
    x = pad_sig * pad_gain + pl_sig * pl_gain
    m = reverb(x, rev_secs, wet, seed)
    # gentle width on the plucks
    return m

def norm(x, peak=0.5): return x * (peak / (np.max(np.abs(x)) + 1e-9))

def music_A(dur):   # curious: C lydian-ish, open voicings, upward motifs
    chords = [(130.81, 196.0, 261.63), (174.61, 261.63, 196.0), (130.81, 196.0, 293.66), (196.0, 293.66, 246.94)]
    p = pad(dur, chords, 22.0, 120, 290, seed=11)
    scale = ["C4", "D4", "E4", "G4", "A4", "C5", "D5", "E5", "F#4"]
    motif = ["E4", "G4", "A4", "G4", "D5", "C5", "E4", "A4", "F#4", "G4", "E5", "D5"]
    pl = plucks(dur, scale, 3.1, (0.30, 0.55), 0, seed=3, motif=motif, hi=1)
    return norm(stereo_mix(p, pl, 0.30, 1.0, 3.2, 0.32, 5), 0.5)

def music_B(dur):   # tense: A dorian/minor with b2 colour, lower, sparser, slow tremolo
    chords = [(110.0, 164.81, 220.0), (116.54, 174.61, 233.08), (110.0, 164.81, 246.94), (146.83, 220.0, 293.66)]
    p = pad(dur, chords, 24.0, 110, 270, tremolo=0.25, seed=21)
    scale = ["A3", "C4", "E4", "G4", "B3", "D4"]
    motif = ["A3", "E4", "Bb3", "A3", "C4", "G3", "B3", "E4", "Bb3", "A3"]
    pl = plucks(dur, scale, 4.4, (0.28, 0.50), 0, seed=8, motif=motif)
    return norm(stereo_mix(p, pl, 0.32, 0.95, 3.0, 0.28, 9), 0.5)

def music_C(dur):   # open: D major / sus2, wide reverb, slow arpeggio
    chords = [(146.83, 220.0, 293.66), (196.0, 293.66, 246.94), (164.81, 246.94, 185.0), (146.83, 220.0, 185.0)]
    p = pad(dur, chords, 21.0, 130, 300, seed=31)
    scale = ["D4", "E4", "F#4", "A4", "B4", "D5", "E5", "F#5"]
    motif = ["D4", "A4", "F#4", "B4", "E4", "A4", "D5", "F#4", "E5", "B4", "A4", "D5"]
    pl = plucks(dur, scale, 3.4, (0.30, 0.55), 0, seed=14, motif=motif, hi=1)
    return norm(stereo_mix(p, pl, 0.30, 1.0, 4.2, 0.42, 7), 0.5)

if __name__ == "__main__":
    from timeline import Timeline
    T = Timeline(); S2 = T.seg_start[2]; S5 = T.seg_start[5]; D = T.duration
    os.makedirs(OUT, exist_ok=True)
    spec = {"history_A_curious": (S2 + 6, music_A), "history_B_tense": (S5 - S2 + 8, music_B), "history_C_open": (D - S5 + 5, music_C)}
    for name, (dur, fn) in spec.items():
        x = fn(dur); sf.write(os.path.join(OUT, f"{name}.wav"), x.astype(np.float32), SR, subtype="PCM_16")
        print(name, round(len(x) / SR, 1), "s, rms", round(float(np.sqrt(np.mean(x ** 2))), 4))
