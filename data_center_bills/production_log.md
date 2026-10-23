# production_log.md — Are Data Centers Raising Your Electric Bill?

## 耗时与额度
- 总耗时：约 2 小时 15 分钟（2026-10-23 01:05–03:20 之间）。其中：核实事实和读原文约 35 分钟；搭环境（装 Kokoro / skia、下载模型）约 10 分钟；写稿、写场景代码约 45 分钟；TTS 约 11 分钟（后台，期间写核查稿）；整片渲染 3 次，每次约 10–12 分钟（8 进程并行，每次约 20,000 帧）；审片三轮 + 局部重渲染约 35 分钟。
- 额度：这一轮对话约消耗 **68 万 token**（总预算 1500 万里约 4.5%）。拿不到账户额度的精确数字，这是按剩余 token 估的。

## 工具选择与理由
- 沿用 "AI 的钱"系列管线：Python + skia-python 逐帧绘制（`draw(t)` 纯函数、可随机寻帧、多进程）+ ffmpeg；`lib.py`、`timeline.py`、`subs.py`、`render.py`、`render_all.py` 从 `ai_bubble/`（仓库分支 `claude/loving-thompson-f5qasq`）复制后只改了字体路径、字幕（只留英文）、场景加载。场景是新写的 `scenes_a/b/c.py` + `common.py`。
- 配音：Kokoro（kokoro-onnx，kokoro-v1.0.onnx + voices-v1.0.bin），am_michael，语速 0.97，en-us，24 kHz；片头首句前 1.2 s、段间 1.0 s、句间 0.45 s、强调句前 0.5–0.8 s、片尾 2.5 s；按句合成并缓存（缓存键含文本哈希，改一句只重合成那一句）。PJM / EPRI / IEEFA / DC 在配音时拆成字母读（"P J M"、"E P R I"、"I E E F A"、"D C"），画面字幕保持原样。数字写成英文单词放进脚本（只改读法不改意思）。
- 没有背景音乐，只有人声。

## 实测时间线
- 总长 **652.1 秒（10:52）**。段起点：段 0 0:01、段 1 0:33、段 2 2:45、段 3 4:59、段 4 7:54、段 5 9:12、段 6 10:14。
- 67 行旁白 / 133 个句子 / 约 1,520 词。

## 响度（成片 mp4，ebur128）
- 母版（`data_center_bills_hq.mp4`，crf 17，约 424 MB，在本机，没提交）：**−14.2 LUFS，真峰值 −1.3 dBTP**，响度范围 1.8 LU；无削波；只有结尾 2.5 秒是静音（片尾留白）。
- 仓库里的 `data_center_bills.mp4`（约 82 MB，约 0.84 Mbps 视频 + 160 kbps AAC，供审阅）：−14.3 LUFS，真峰值 −1.1 dBTP。
- 为什么有压缩 + 限幅：TTS 配音波峰比响度高约 20 dB，若只做线性 loudnorm，−1 dBTP 的上限会把响度压在 −15.3 LUFS；`mix.py` 先做温和压缩（5:1，阈值 −30 dB）+ 限幅器，再两遍 loudnorm（I=−14，TP=−1.5）。
- 没有加任何音乐，也没合成任何真人声音。

## 遇到的问题
1. **这台 Mac 上没有旧管线**：仓库默认分支没有 `ai_bubble/`、`power_ceiling/`，要到各自的 `claude/*` 分支取；本机也没有 skia / kokoro / ffmpeg，用 uv 建 Python 3.12 虚拟环境装了 kokoro-onnx、skia-python、soundfile、scipy、pyloudnorm、imageio-ffmpeg，ffmpeg 用的是 imageio-ffmpeg 自带的 7.1（带 libx264）。Kokoro 模型（约 325 MB + 28 MB）是你同意后才下载的。
2. **没有 Inter 字体**：Mac 上没有 Inter TTF，改用 Arial Bold / Arial；Playfair、IBM Plex Mono 沿用旧管线的字体文件。
3. **没有 `gh`**：没装 GitHub CLI 也没有令牌，PR 我只能 push 分支，由你在页面上点"Create pull request"（链接在汇报里）。
4. 一次 `pkill` 把后台的等待任务一起杀了（通知里的 "failed exit 144"），不影响结果。
5. 事实核查中，PJM、EPRI、IMM 的 PDF 用 WebFetch 读不了，改成 curl / 保存下来再用 pypdf 提取文本逐字核对。
6. 成片 mp4 原版 crf 17 约 424 MB，超过 GitHub 单文件 100 MB 限制：提交到仓库的是重新压缩过的版本（约 1 Mbps，供审阅），原版在本机，没有提交。

## 没做到 / 需要你确认
- 没有听过成片（没有声卡），详见 review_log.md 的"已知小瑕疵"。
- 没有逐词强制对齐（字幕时间按句内字符比例分配，句首句尾是准的）。

## 文件
`script.py`（旁白原文）→ `tts.py`（配音 + `timeline.json`）→ `common.py` / `scenes_a.py`（段 0–1）/ `scenes_b.py`（段 2–3）/ `scenes_c.py`（段 4–6）→ `render.py` / `render_all.py`（逐帧渲染 + 烧录字幕）→ `mix.py`（响度）→ `assemble.sh`（合成）；`subs.py`（字幕 + SRT）、`thumbs.py`（缩略图）、`review.py` / `frames.py` / `check_text.py` / `check_audio.py`（审片工具）。
