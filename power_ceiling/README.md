# Will Electricity Cap AI?（DWG-08 / POWER CEILING）

成片：`youtube_power_ceiling.mp4`（英文字幕）、`douyin_power_ceiling.mp4`（中英双语字幕）。字幕：`subtitles_en.srt`、`subtitles_zh.srt`。核查表：`fact_check.md`。

重新生成：
1. `python3 tts.py`：用 Kokoro 逐句合成 `narration.wav` 和 `timeline.json`（模型路径写在 `tts.py` 里，需要先下载 `kokoro-v1.0.onnx` 和 `voices-v1.0.bin`）。
2. `python3 subs.py`：切分字幕，生成 SRT 和 ASS。
3. 起静态服务（`http-server -p 8124 .`），分段渲染 `node render.mjs <from> <to> <out.mp4>`（共 10730 帧），用 ffmpeg concat 拼接。
4. `ffmpeg -i base.mp4 -i narration.wav -vf ass=subs_dy.ass ...` 烧字幕、混音。
5. `python3 factcheck.py` 重生成核查表的时间码部分（自查清单是手写的，在 `fact_check.md` 末尾）。

画面是 canvas 2D，代码在 `engine.js`、`icons.js`、`scenes_*.js`，每一帧是时间 t 的纯函数；地图数据在 `geo.js`（Natural Earth 110m / US Atlas 烘焙）。字体：JetBrains Mono、Architects Daughter（OFL）。
