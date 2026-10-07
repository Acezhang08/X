"""Checks every frame of a rendered video: smallest distance from any drawn pixel to the frame edge.

Usage: python video/check_margins.py tip_ask_twice.mp4
"""
import subprocess, sys, numpy as np
f = sys.argv[1]
W, H = 1920, 1080
bg = np.array([0x12, 0x3A, 0x3B], dtype=np.int16)
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
frames = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)
worst = None
for i, fr in enumerate(frames):
    diff = np.abs(fr.astype(np.int16) - bg).max(axis=2) > 24
    ys, xs = np.nonzero(diff)
    if len(xs) == 0: continue
    m = min(xs.min(), W - 1 - xs.max(), ys.min(), H - 1 - ys.max())
    if worst is None or m < worst[0]: worst = (m, i / 30, xs.min(), W-1-xs.max(), ys.min(), H-1-ys.max())
print(f"{len(frames)} frames; smallest margin {worst[0]}px at t={worst[1]:.2f}s (L {worst[2]}, R {worst[3]}, T {worst[4]}, B {worst[5]})")
