# production_log.md — 制作记录（Why You Can't Tell AI Video From Real Anymore）

## 成片
- 文件：`ai_video_real.mp4`，1920×1080，30 fps，H.264（yuv420p，CRF 20）+ AAC 48 kHz 单声道，时长 484.63 秒（8 分 04 秒），约 19.6 MB。
- 响度：积分 −14.05 LUFS（目标 −14），真峰值 −1.52 dBTP（上限 −1），采样峰值 −1.96 dBFS，削波 0。
- 字幕：烧录英文字幕，`subtitles_en.srt`（129 条）。

## 时间与额度（估算）
- 墙钟时间：约 70 分钟（09:10 起，10:21 写完审片日志）。其中渲染约 4 轮，每轮整片或分块约 6–8 分钟；Kokoro TTS 每次全量约 3.5 分钟，增量约 40 秒。
- Token：约 33 万（会话额度从 1,500 万降至约 1,467 万）。

## 步骤
1. **选题**：题目已定，未重新查 Trends / YouTube（按要求）。
2. **核查（先于写稿）**：Runway Turing Reel、Berkeley 论文、C2PA、SynthID Detector、扩散模型原文（arXiv 2006.11239、2204.03458）、早期手部问题报道。容器拒绝访问 runway.com、arxiv.org、techradar.com、blog.google 直连，改为搜索摘要核实，结论分级见 `fact_check.md`。
3. **写稿**：`script.py`。第一版 754 词（约 5.5 分钟），补充到 1,207 词、62 句，总时长 484.6 秒。反转句（3.6）按数据改写，见 `fact_check.md`。
4. **配音**：`tts.py`（沿用 humanoid_robots），Kokoro v1.0 am_michael，语速 0.97，en-us，24 kHz；`spoken()` 只改读法；生成 `timeline.json`。
5. **画面**：沿用 humanoid_robots 的 Skia 管线（`lib.py`、`subs.py`、`timeline.py`、`render_all.py`、`qa.py`），配色与底色按 `style_ai-principles.md` 改为 3B1B 式 #16181D；新增 `scene_util.py`、`scenes_a.py`（seg0–1）、`scenes_b.py`（seg2–3）、`scenes_c.py`（seg4–5）。
6. **渲染**：`render_all.py`（4 进程，450 帧一块，共 33 块），`assemble` 命令见下。
7. **音频**：`make_audio.py`（−14 LUFS、真峰值限制），`audio_check.py` 数值检查。
8. **审片**：2 轮，见 `review_log.md`。
9. **缩略图**：`thumbs.py`，三张 1280×720 PNG。
10. **发布包**：`publish.md`（标题、描述、章节、置顶评论、AI 标注说明）。

## 复现命令（在本目录下）
```
python3 tts.py            # build/voice.wav, build/timeline.json（需 build/kokoro.onnx、build/voices.bin）
python3 make_audio.py     # build/final_audio.wav
python3 subs.py           # subtitles_en.srt
python3 qa.py 2.0         # 帧级 QA
NPROC=4 python3 render_all.py   # build/chunks/*.mp4
ls build/chunks/v_*.mp4 | sort | sed "s|^|file '$PWD/|; s|$|'|" > build/list_v.txt
ffmpeg -y -f concat -safe 0 -i build/list_v.txt -c copy build/master_video.mp4
ffmpeg -y -i build/master_video.mp4 -i build/final_audio.wav -map 0:v -map 1:a -c:v libx264 -preset slow -crf 20 -pix_fmt yuv420p -r 30 -c:a aac -b:a 192k -ar 48000 -shortest -movflags +faststart ai_video_real.mp4
python3 thumbs.py         # thumbnail_A/B/C.png
```

## 环境与限制
- 容器无法直连 runway.com、arxiv.org、techradar.com；核查基于搜索摘要。
- 无声卡，音频只做数值检查，没有听感评估。
- 字体：CMU Serif 和 Inter 不在容器内；大号数字用 Liberation Serif Bold，标签用 JetBrains Mono，正文字幕用 Liberation Sans Bold。
- 模型：Kokoro v1.0（model-files-v1.0）从 GitHub release 下载。

## 交付文件（`ai_video_real/`）
script.py、fact_check.md、timeline.json、ai_video_real.mp4、subtitles_en.srt、thumbnail_A.png、thumbnail_B.png、thumbnail_C.png、publish.md、review_log.md、production_log.md，以及渲染所需的代码（`lib.py`、`scene_util.py`、`scenes_*.py`、`render*.py`、`subs.py`、`timeline.py`、`tts.py`、`make_audio.py`、`audio_check.py`、`qa.py`、`thumbs.py`）。`build/` 为中间产物，已在 `.gitignore` 中忽略。
