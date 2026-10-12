# production_log.md — The AI Bubble, Explained: Follow the Money

## 耗时与额度
- 总耗时：约 1 小时 15 分钟（含写代码、迭代看图、配音、整片渲染、混音、缩略图、文档）。其中整片渲染（4 进程并行，两个版本同时编码）约 12 分钟，TTS 约 5 分钟。
- 额度：这一轮对话大约消耗 31 万 token 的上下文（总预算 1500 万里用掉约 2%）。我拿不到账户额度的精确数字，这是按 token 计数估的。

## 工具选择与理由
- 没有沿用 Manim。仓库里没有 `how_ai_works/`、`power_ceiling/`（本分支只有 `city/`、`out/`、`tools/`），所以无法照搬那套流程；而且 Manim 需要 pycairo/pango，在这个容器里装起来麻烦，拼贴风格（撕边、胶带、投影、红笔）也要自己写很多。
- 选择 **Python + skia-python 逐帧绘制 + ffmpeg**：每帧是 `draw(t)` 的纯函数，字体、路径部分绘制（箭头“画”出来、红笔）、模糊投影都现成，4 进程并行。1080p 约 0.1 秒/帧。
- 配音：Kokoro（kokoro-onnx 0.6.1，kokoro-v1.0.onnx + voices-v1.0.bin），am_michael，语速 0.97，en-us，24kHz。按句合成后按规格拼接停顿：片头 1.2s、换段 1.0s、同段句间 0.45s、强调句前 0.5–0.8s、片尾 2.5s；数字/缩写的读法在 `script.py` 的 `SPOKEN`（如 “A I”、“Open A I”、“David Kahn” 防止读成 Kan）。
- 背景音乐：`music.py` 自己合成，见 `music/money_series/music_notes.md`。

## 时间线（实测）
- 总长 504.2 秒（8:24）。段起点：段 0 0:01，段 1 0:35，段 2 1:46，段 3 3:10，段 4 4:33，段 5 5:43，段 6 7:03。
- 提示词里的“约 2:20 / 6:35”等是预估；实际配音更快，音乐切换点按实测的段 2、段 5 起点放。

## 遇到的问题
1. 容器没有 scipy / kokoro / skia：pip 安装；skia 还缺 libEGL（apt 装 libegl1）。
2. 句子切分 bug：`1.4 trillion` 里的小数点被当成句号，导致文本块数对不上，改成“标点后必须跟空白或结尾”。
3. `fade()` / `card()` 在“不可见”时我最初是 `yield False`，但 `with` 块体仍会执行，导致本该消失的元素还在；改成不可见时把画布裁剪为空矩形。
4. Playfair Display 的数字是旧式数字（$100B 读成 $1oob），数字改用 Inter Bold 绘制。
5. 字幕描边在 5px 时糊成一团，改成英文 4px、中文 3.4px。
6. 音乐一开始比人声低 28 dB（几乎听不见），把底噪抬高并加强侧链压缩，实测说话时低约 15 dB、停顿时低约 10 dB。
7. 抽帧检查发现 3.2 的债券堆挡住来源小字，已改版并只重渲相关 450 帧片段。
8. Playfair 在剪报标题里用到 ↔、× 等符号时缺字形，同样改用 Inter。
9. 第一次建 PR 时 base 写成了 main，仓库默认分支实际是 `claude/ai-free-tier-comparison-video-hqwumi`。

## 没做到 / 需要你确认
- 没有听过合成的音乐，也没有逐词强制对齐（见 fact_check.md 末尾自查）。
- 成片提交到仓库的是重新压缩过的版本（crf 25，各约 48MB）；渲染原版（crf 17，各约 370MB）在容器里，没有提交。

## 文件
`script.py`（旁白原文）→ `tts.py`（配音+时间线）→ `scenes_a/b/c.py`（画面）→ `render_all.py`（逐帧渲染+字幕）→ `mix.py`（混音）→ `assemble.sh`（合成）；`subs.py`、`thumbs.py`、`make_docs.py`。
