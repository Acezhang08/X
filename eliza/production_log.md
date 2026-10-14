# production_log.md — The First Chatbot（ELIZA）

## 总耗时与额度
- 总耗时：约 1 小时 50 分钟（从你回复“ELIZA”到交付）。大致分配：核实事实与写稿 ≈ 25 分钟；写画风库、道具与三批场景 ≈ 35 分钟；配音 ≈ 4 分钟（含一次局部重做）；整片渲染 ≈ 5 分钟 ×2（4 进程并行，1080p 约 0.1 秒/帧）+ 局部重渲染 2 次；两轮审片与修改 ≈ 30 分钟；文档、缩略图、发布包 ≈ 10 分钟。
- 额度：这一轮对话大约使用了 56 万 token 的上下文（总预算 1500 万的约 4%），其中大头是看联系表图片。我拿不到账户额度的精确数字，这是按 token 计数估的。

## 沿用与新增
- 沿用 `ai_bubble` 的整套管线：skia 逐帧绘制 + ffmpeg、`Timeline` 取词时间、`tts.py` 的停顿与分句规则、`mix.py` 的侧链压缩思路、`render_all.py` 的 4 进程分块。从 `origin/claude/loving-thompson-f5qasq` 分支读取。
- 新增：纸/墨线画风库 `lib.py`、道具 `props.py`、字幕断行规则 `subs.py`、程序化抽检 `qa.py`、客观审片脚本 `review_checks.py`、核查表生成器、`music.py`（全新的温暖怀旧调性）。

## 环境与工具选择
- 容器里没有 scipy / kokoro / skia：`pip install skia-python kokoro-onnx==0.6.1 scipy soundfile pillow fonttools brotli`；skia 缺 libEGL，`apt-get install libegl1 libgl1 libfontconfig1`。Kokoro 模型从 GitHub Releases 下载（`kokoro-v1.0.onnx` 325MB + `voices-v1.0.bin` 28MB），放在 `/home/user/models/`，**没有提交进仓库**。
- 字体：`npm i @fontsource/*`，woff2 用 fonttools 转成 ttf（IM Fell English、Special Elite、Courier Prime、Caveat），OFL 授权，随仓库提交在 `eliza/assets/fonts/`（约 0.7MB）。

## 遇到的问题
1. **选题调研的数据拿不到**：Google Trends、YouTube 搜索补全（两个域名）、youtube.com 都被容器的网络策略拒绝（403 / DNS 失败），只能用 WebSearch 摘要。已在选题汇报里如实写“查不到”。
2. **无法打开原论文与原书**：同上。事实核查改为以 A. Hay 在 GitHub 的转录与引用（`raw.githubusercontent.com` 可访问）为主，再用检索摘要交叉；每一行的来源强度都写在 `fact_check.md`。
3. 手写体与等宽字体没有 → ← 字形（显示成方框），改成文字或墨线箭头。
4. `skia.Path.Op` 在 skia-python 144 里叫 `skia.Op`。
5. 第一次整片拼接时，我的后台等待脚本与手动拼接同时写同一个 mp4，导致文件损坏（`moov atom not found`）；删除后单独重拼解决。
6. 音乐第一版太低（说话时比人声低 34 dB，且 65% 能量堆在 60–120Hz 发闷）：持续音升到 120–300Hz 区间并降到 0.3 倍、拨弦调到 1.0 倍、侧链压缩从 ratio 12 降到 4、整体抬高 10 dB。
7. 事实核查中删掉了 Carl Sagan 的引语与加州 SB 243（核实不了），改写了几处说得过满的句子（见 `fact_check.md`）。

## 时间线（实测）
- 总长 561.6 秒（9:21）；约 1269 词。段起点：段 0 0:01，段 1 0:48，段 2 2:35，段 3 3:56，段 4 5:03，段 5 6:02，段 6 8:48。
- 两处“再抓一次”：约 3:07–3:27 的反转（论文开头就说“讲破了魔法就消失”，可秘书知道了也没破咒；“Knowing did not break the spell” 在 3:27）；6:02–6:50 的图灵测试数字（ELIZA 23% ≈ GPT-4o 21%）。

## 文件
`script.py` → `tts.py` → `scenes_a/b/c.py`（+ `lib.py`、`props.py`）→ `render_all.py` → `music.py`/`mix.py` → `assemble.sh` → `eliza_history_of_ai.mp4`；`subs.py` → `subtitles_en.srt`；`thumbs.py` → `thumbnail_A/B/C.png`；`make_factcheck.py` → `fact_check.md`；`make_publish.py` → `publish.md`；`review_checks.py`、`qa.py`、`review_log.md`。
- 提交到仓库的 `eliza_history_of_ai.mp4` 是重新压缩的版本（crf 24，64MB，画质与音轨与原版一致）；渲染原版（crf 17，约 416MB）在容器的 `eliza/build/eliza_master.mp4`，没有提交。
