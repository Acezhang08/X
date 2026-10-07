"""Self-check for the two final MP4s.

- ffprobe: codec / size / fps / duration (must be 40-55 s)
- full decode of each file (catches broken streams)
- one frame every 5 s -> contact sheet at full size and at phone size (844 px wide)
- voice onsets detected from the MP4's own audio vs subtitle start times
"""
import json, re, subprocess, sys, numpy as np
from PIL import Image

OUT = sys.argv[1] if len(sys.argv) > 1 else "build/check"
subprocess.run(["mkdir", "-p", OUT])
T = json.load(open("build/timings.json"))

def sh(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)

def ass_starts(path):
    st = []
    for line in open(path):
        m = re.match(r"Dialogue: 1,(\d+):(\d+):([\d.]+),", line)
        if m: st.append(int(m[1]) * 3600 + int(m[2]) * 60 + float(m[3]))
    return st

for name, subs in [("bourbaki_x", "subs-en.ass"), ("bourbaki_douyin", "subs-bi.ass")]:
    f = f"../{name}.mp4"
    info = json.loads(sh(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", f]).stdout)
    v = next(s for s in info["streams"] if s["codec_type"] == "video")
    a = next(s for s in info["streams"] if s["codec_type"] == "audio")
    dur = float(info["format"]["duration"])
    print(f"\n== {name}.mp4  {v['codec_name']} {v['width']}x{v['height']} {v['r_frame_rate']} | {a['codec_name']} {a['sample_rate']}Hz | {dur:.2f}s | {int(info['format']['size'])/1e6:.1f} MB")
    assert v["codec_name"] == "h264" and a["codec_name"] == "aac" and (v["width"], v["height"]) == (1920, 1080)
    assert 40 <= dur <= 55, dur
    dec = sh(["ffmpeg", "-v", "error", "-i", f, "-f", "null", "-"])
    print("full decode:", "OK" if not dec.stderr.strip() else dec.stderr[:500])
    # 每 5 秒一帧
    times = list(np.arange(0, dur, 1.0)) + [dur - 0.1]
    frames = []
    for t in times:
        p = f"{OUT}/{name}-{t:05.1f}.png"
        sh(["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.2f}", "-i", f, "-frames:v", "1", p])
        frames.append(p)
    for w, tag in [(480, "sheet"), (844, "phone")]:
        h = w * 9 // 16; cols = 4 if tag == "sheet" else 2
        rows = (len(frames) + cols - 1) // cols
        S = Image.new("RGB", (cols * w, rows * h))
        for i, p in enumerate(frames):
            S.paste(Image.open(p).convert("RGB").resize((w, h), Image.LANCZOS), ((i % cols) * w, (i // cols) * h))
        S.save(f"{OUT}/{name}-{tag}.png")
    # 音频起点 vs 字幕起点
    pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-ac", "1", "-ar", "16000", "-f", "f32le", "-"], capture_output=True).stdout
    x = np.frombuffer(pcm, np.float32)
    hop = 160; e = np.sqrt(np.convolve(x ** 2, np.ones(400) / 400, "same")[::hop])
    speech = e > 0.02
    onsets, quiet = [], 999
    for i, s in enumerate(speech):
        if s and quiet >= 30: onsets.append(i * hop / 16000)  # 前面至少 0.3 s 安静
        quiet = 0 if s else quiet + 1
    starts = ass_starts(f"build/{subs}")
    print("line  sub_start  voice_onset  diff")
    worst = 0
    for i, st in enumerate(starts):
        near = min(onsets, key=lambda o: abs(o - st))
        worst = max(worst, abs(near - st - 0.08))
        print(f"{i+1:4d}  {st:9.2f}  {near:11.2f}  {near - st:+.2f}")
    print(f"voice onsets found: {len(onsets)} | worst |diff| vs planned 0.08 s lead: {worst:.2f}s")
    print(f"last subtitle on screen after last word: {dur - T['lines'][-1]['end']:.2f}s")
