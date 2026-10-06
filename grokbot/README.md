# Grok Bot：名字不是墙（配音讲解短视频）

两个成品在 `../out/`：

- `grokbot-x.mp4`：英文配音 + 英文字幕（X / YouTube）
- `grokbot-douyin.mp4`：同一画面和配音，中英双语字幕（英上中下）

## 流程

| 步骤 | 文件 | 说明 |
|---|---|---|
| 旁白文本 | `script.json` | 每句英文/中文、句后停顿；`tts` 字段只改发音，`sub_en`/`sub_zh` 手动断行 |
| 配音 | `tts.py` | Kokoro-82M 本地 TTS，参数见 `voice-settings.txt`，输出 `build/narration.wav` + `build/timings.json` |
| 混音 | `make_audio.py` | 人声 + 程序合成的极轻房间底噪和转场 whoosh（无第三方音频） |
| 字幕 | `make_subs.py` | 生成 ASS：白字、细黑描边、轻阴影、无底色 |
| 画面 | `scene/main.js` | three.js 等距 3D 场景，所有动画由 `timings.json` 驱动，逐帧确定性渲染 |
| 录制 | `capture.mjs` | Playwright + Chromium 逐帧截图 |
| 编码 | `render.sh` | 一键跑完全部步骤，ffmpeg 烧录字幕，H.264 + AAC |
| 自查 | `check.py` | 时长/编码、完整解码、每 5 秒截帧（含手机尺寸）、人声起点 vs 字幕起点 |

```bash
cd grokbot
./render.sh            # 改了旁白就整条重跑
SKIP_TTS=1 ./render.sh # 只改了画面或字幕
python3 check.py
```

依赖：`pip install kokoro-onnx soundfile pillow numpy`，Kokoro 模型放在 `/opt/kokoro/`，
Noto Sans CJK SC（OFL）放在 `/opt/fonts/`，Inter（OFL）用系统自带。repo 根目录下要先 `npm install`（three.js）。
