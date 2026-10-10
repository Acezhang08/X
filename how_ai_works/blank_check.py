# -*- coding: utf-8 -*-
"""空屏检测：主体区域（去掉底部字幕区）连续 >= 1.5 秒几乎没有非底色像素的区间"""
import subprocess, numpy as np, sys
W, Hh, FPS = 480, 270, 10
ROWS = int(Hh * 880 / 1080)   # 内容区 y ∈ [-2.45, 4]，对应前 880px
THRESH = int(sys.argv[2]) if len(sys.argv) > 2 else 60   # 非底色像素数（480x270 尺度）
src = sys.argv[1] if len(sys.argv) > 1 else "build/final/video_raw.mp4"
p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", src, "-vf", f"fps={FPS},scale={W}:{Hh}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
bg = np.array([0x16, 0x18, 0x1D])
fs = W * Hh * 3
cnt = []
while True:
    buf = p.stdout.read(fs)
    if len(buf) < fs: break
    f = np.frombuffer(buf, np.uint8).reshape(Hh, W, 3)[:ROWS]
    cnt.append(int((np.abs(f.astype(np.int16) - bg).max(axis=2) > 24).sum()))
cnt = np.array(cnt)
empty = cnt < THRESH
runs, i = [], 0
while i < len(empty):
    if empty[i]:
        j = i
        while j < len(empty) and empty[j]: j += 1
        runs.append((i / FPS, j / FPS)); i = j
    else: i += 1
def tc(x): return f"{int(x//60)}:{x%60:05.2f}"
long = [(s, e) for s, e in runs if e - s >= 1.5]
print(f"帧数 {len(cnt)}，阈值 {THRESH}px，≥1.5s 空屏区间 {len(long)} 个")
for s, e in long: print(f"  {tc(s)}–{tc(e)}  ({e-s:.1f}s)")
print("所有空区间(>=0.5s):", [(tc(s), tc(e)) for s, e in runs if e - s >= 0.5])
