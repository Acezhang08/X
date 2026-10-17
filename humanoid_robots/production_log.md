# production_log.md — Humanoid Robots Can Do Backflips. Why Can't They Fold Laundry?

## 总耗时与额度
- 总耗时：约 1 小时 25 分钟（从开工到交付 PR）。大致分配：搭环境 + 读旧管线 ≈ 8 分钟；事实调研（约 35 次检索）≈ 15 分钟；写稿 + 重排结构 ≈ 10 分钟；配音 ≈ 3 分钟 ×2；写画风库、道具和三批场景 ≈ 25 分钟；整片渲染 ≈ 6 分钟 ×2 + 局部重渲染 3 次；两轮审片与修改 ≈ 20 分钟；发布包、日志、PR ≈ 8 分钟。
- 额度：这一轮对话大约使用了 56–60 万 token 的上下文（总预算 1500 万的约 4%），大头是看联系表图片（32 张 + 若干预览）。拿不到账户额度的精确数字，这是按 token 计数估的。

## 沿用与新增
- 沿用 `ai_bubble` / `eliza` 的管线：skia 逐帧绘制 + ffmpeg、`Timeline` 取词时间、`tts.py` 的停顿与分句规则、`render_all.py` 的 4 进程分块、`subs.py` 的断行规则、`qa.py` / `review_checks.py` 的程序化抽检。旧代码来自 `origin/claude/ecstatic-fermat-gqkoxa`（eliza）、`loving-thompson-f5qasq`（ai_bubble）、`focused-planck-kisqxl`（power_ceiling）。
- 新增：蓝图画风库 `lib.py`、道具 `props.py`（通用线稿机器人、会折叠的衬衫、手、剪影、图标）、`scenes_a/b/c.py`、`make_audio.py`（−14 LUFS + 预读限幅器）、`audio_check.py`、`sheets.py`（联系表）、`facts.py` + `make_factcheck.py`（核查表自动生成）、`make_publish.py`。
- 画风：`power_ceiling` 是 canvas 2D（Chromium）渲染；这次按要求用 skia 管线重新实现同一套色值和版式，并把最小字号提到 36px、出处字提到 36px，图号框移进 80px 安全边距，写成根目录 `style_ai-future.md`。

## 环境与工具选择
- 容器里没有 skia / kokoro：`pip install skia-python kokoro-onnx==0.6.1 scipy soundfile pillow fonttools brotli pyloudnorm`；skia 缺 libEGL，`apt-get update && apt-get install libegl1 libgl1 libfontconfig1`。Kokoro 模型从 GitHub Releases 下载（`kokoro-v1.0.onnx` 325 MB + `voices-v1.0.bin` 28 MB），放在 `/home/user/models/`，**没有提交进仓库**；`tts.py` 读 `build/kokoro.onnx`、`build/voices.bin`（软链）。
- 字体：JetBrains Mono、Architects Daughter 取自 `power_ceiling/fonts/*.woff2`，用 fonttools 转成 ttf；Liberation Sans Bold 取自系统；全部放在 `assets/fonts/`。
- 配音：Kokoro `am_michael`，speed 0.97，en-us，24 kHz，按规定的停顿；`spoken()` 把年份、数字、缩写改成英文读法。
- 响度：线性归一化做不到 −14 LUFS（人声峰值/平均比偏大，ELIZA 那条因此是 −15.3），所以用 `make_audio.py`：升到 −14 LUFS 后用带预读的峰值限幅器压住峰值。实测 −14.04 LUFS，真峰值 −1.47 dBTP。
- 成片压缩：渲染原版（crf 17，约 136 MB）超过 GitHub 单文件 100 MB 上限，所以提交的 `humanoid_robots.mp4` 是 crf 23 重压缩版（42 MB，画面和音轨与原版一致）；原版在容器的 `build/master_video.mp4`，没有提交。

## 遇到的问题
1. **网络限制**：arxiv.org、openai.com、wikipedia.org、rodneybrooks.com、figure.ai、frc.ri.cmu.edu 都被容器的代理 403 拒绝（`WebFetch` 与 curl 都不行），只能靠网页搜索返回的摘要。已在 `fact_check.md` 开头如实写明；Moravec 和 Brooks 的话因此全部转述、不加引号。
2. 旧作品都在未合并的 PR 分支里，当前分支只有 `city/`、`out/`、`tools/`；用 `git worktree` 把 4 个分支检出到 scratchpad 当参考，没有把旧文件带进这个 PR。
3. 手写体/等宽字体没有 ✓ ✗ ∞ ≠ → 字形：全部用线条画出来（`check()`、`cross()`、`infinity()`、两条线加斜杠）。
4. 第一版稿子的"反转"在 3:47、数据对比在 6:38，偏晚；重排了结构（魔方实验挪到"为什么叠衣服难"）后分别提前到 3:04 和 6:19，总长从 10:30 缩到 10:09。
5. `pkill -f` 会把我自己的 shell 杀掉（退出码 144），改用脚本文件加 `setsid nohup` 启动后台渲染。
6. `ffmpeg loudnorm` 的 linear 模式给出 −15.3 LUFS（和 ELIZA 同样的问题）；换成自己写的增益 + 限幅器解决。

## 时间线（实测）
- 总长 608.97 秒（10:09）；1,425 词；70 行旁白 / 129 句。段起点：段 0 0:01，段 1 0:47，段 2 1:58，段 3 3:19，段 4 5:09，段 5 7:20，段 6 8:38。
- 两处"再抓一次"：约 3:04–3:18 的反转（"后空翻是一个藏着简单问题的难动作；叠衣服是反过来"，2.8–2.9）；约 6:19 的 "Ninety thousand years of text, against four months of robot"（4.7）。

## 文件
`script.py` → `tts.py` → `scenes_a/b/c.py`（+ `lib.py`、`props.py`）→ `render_all.py` → `make_audio.py` → `assemble.sh` → `humanoid_robots.mp4`；`subs.py` → `subtitles_en.srt`；`thumbs.py` → `thumbnail_A/B/C.png`；`facts.py` → `make_factcheck.py` → `fact_check.md`；`make_publish.py` → `publish.md`；`qa.py`、`review_checks.py`、`audio_check.py`、`sheets.py`、`review_log.md`。系列画风规范在仓库根目录 `style_ai-future.md`。
