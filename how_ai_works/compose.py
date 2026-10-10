# -*- coding: utf-8 -*-
"""分段视频 -> 精确帧数 -> 拼接 -> 配音 -> 字幕烧录（YouTube 英文 / 抖音中英）"""
import json, subprocess, os, glob
H = os.path.dirname(os.path.abspath(__file__))
os.chdir(H)
TL = json.load(open("build/timeline.json"))
FPS = 30
def sh(c): subprocess.run(c, shell=True, check=True)

segs = []
for s in TL["segments"]:
    n = round(s["end"] * FPS) - round(s["begin"] * FPS)
    src = glob.glob(f"build/media_hd/videos/seg{s['id']}/1080p30/Seg{s['id']}.mp4")[0]
    out = f"build/final/seg{s['id']}.mp4"
    sh(f'ffmpeg -v error -y -i {src} -vf "tpad=stop_mode=clone:stop_duration=2" -frames:v {n} -c:v libx264 -crf 14 -preset fast -pix_fmt yuv420p -r {FPS} {out}')
    segs.append(out)
open("build/final/list.txt", "w").write("".join(f"file 'seg{s['id']}.mp4'\n" for s in TL["segments"]))
sh("ffmpeg -v error -y -f concat -safe 0 -i build/final/list.txt -c copy build/final/video_raw.mp4")

def ts(x):
    cs = int(round(x * 100)); h, r = divmod(cs, 360000); m, r = divmod(r, 6000); s, c = divmod(r, 100)
    return f"{h}:{m:02d}:{s:02d}.{c:02d}"
HEAD = """[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Default,Inter,46,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,2.2,1.5,2,120,120,48,1

[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
"""
for name, bil in (("youtube", False), ("douyin", True)):
    with open(f"build/{name}.ass", "w", encoding="utf-8") as f:
        f.write(HEAD)
        for c in TL["chunks"]:
            en = c["en"].replace("\\", "")
            txt = en
            if bil:
                txt = en + r"\N{\fnWenQuanYi Zen Hei\fs42}" + c["zh"]
            f.write(f"Dialogue: 0,{ts(c['start'])},{ts(c['end'] + 0.05)},Default,,0,0,0,,{txt}\n")
    out = f"{name}_how_ai_works.mp4"
    sh(f'ffmpeg -v error -y -i build/final/video_raw.mp4 -i build/narration.wav -vf "ass=build/{name}.ass:fontsdir=/usr/share/fonts" '
       f'-c:v libx264 -crf 18 -preset medium -pix_fmt yuv420p -r {FPS} -c:a aac -b:a 192k -ar 48000 -shortest -movflags +faststart {out}')
    print("wrote", out)
