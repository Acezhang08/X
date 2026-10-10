# production_log：How AI Actually Works

- 日期：2026-10-10；环境：云端容器，4 核，无 GPU
- 工具：Manim Community 0.22.0、Kokoro（kokoro-onnx 0.6.1，kokoro-v1.0.onnx + voices-v1.0.bin，am_michael，语速 0.97，en-us，24kHz）、ffmpeg（libass 烧字幕）
- 流程：`make_tts.py`（配音+时间轴+字幕）→ `scenes/seg*.py` 分段渲染（`render_all.sh`，4 并行）→ `compose.py`（按帧数裁齐、拼接、混音、烧字幕）→ `thumbs.py`、`make_factcheck.py`
- 成片时长：487.9 秒（8:08）。配音按 Kokoro 实际长度，没有拉长；比预计的 8.5–9.5 分钟短，但满足"不短于 8 分钟"
- 耗时：1080p30 八段全部渲染约 3 分钟（并行）；整个制作含调试约 1 小时。额度用量没有可读取的计数，未统计
- 配音分块：每行旁白按子句拆块单独合成（块间 0.18 秒，句间 0.45 秒），字幕起止因此是精确值，不是估算
- 数字读法：只改读法（G P T four oh、oh one、A I M E、twenty twenty-four 等），见 `narration.py` 的 `TTS_SUBS`
- 遇到的问题：
  1. `srt` 依赖在新 setuptools 下无法编译 → 降级 setuptools 后装上
  2. Manim 的 Text 在计数器里字符数变化，和 FadeIn 同播会报 zip 错误 → 计数器直接 add
  3. `TransformFromCopy` 后目标不在场景里，后续 Transform 出现重影 → 改用 ReplacementTransform
  4. 字幕 ASS 的 Events Format 少了字段，导致字幕前出现 "0,0,," → 已修正
  5. 若干文字溢出框、标签重叠 → 抽帧检查后逐一修掉
- 未完成/需人工确认：事实来源未重新联网复核；第 1 段动画比配音多约 0.18 秒
- 提示词里要求"旁白文字不要改动"：`narration.py` 中的英文块拼起来与提示词逐字一致

## 第二轮修改（评审意见 1–10）
- 逐词对齐：`align.py`（pocketsphinx 强制对齐，Whisper 模型下载被代理拦截）→ `build/words.json`（副本 `words.json`）；场景用 `Seg.wt(行, 块, 词)` 取词时间，`act_mark` 记录数字实际上屏起止，`analyze.py` 生成 `alignment_check.md`（已并入 fact_check.md）。最大误差 0.03 秒
- 1 旁白 0.2：句子留在中央（白 60%），句末竖线 + "where most explanations stop"，0.3 开始时才转场
- 2 旁白 3.9：计数器从 "more" 开始滚、在 "tokens" 说完时到 15,000,000,000,000+，满亮度停留 1.5 秒再淡出
- 3 旁白 3.10：终值 "≈ 90,000"，"YEARS" 在数字正下方；说完 "years" 时到位
- 4 旁白 5.1：12% 在 "twelve" 弹出，74% 在 "seventy" 弹出（误差 −0.01 / −0.03 秒）
- 5 旁白 4.9：流程图整体缩放后居左，最左元素离边约 157px（≥80px）
- 6 旁白 7.4：THINKING / PREDICTING 都是白色边框和白字，光标在中间闪烁
- 7 缩略图 B：大字 WHAT CHANGED?，12%/74% 方块移到上半部，右下 1/4 留空
- 8 旁白 5.7：15.6% 在曲线起点左上方，"curve shape illustrative" 挪到左下角，与 "training steps" 分开
- 9 旁白 1.4：编号方块按数字位数加宽，15592 不再贴边
- 10 旁白 6.5：PREDICT 台阶在旁白一开始就画出
- 顺带调整：4.6 里 1.3B 和 175B 圆圈改成各自在说到对应数字时出现（原来 175B 提前出现）
- 遇到的问题：`act_mark` 的 `rate_func` 对已构造好的计数器动画无效，所以计数器的缓动在 `counter(rate=...)` 里设

## 第二轮每段抽 3 帧检查（douyin 成片，时间码 mm:ss）
- 段 0：0:06、0:14、0:30（另 0:08.5、0:09 看旁白 0.2 过渡）— 句子居中可读，格子/数字无出画
- 段 1：0:41、0:55、1:06 — 编号方块不贴边，字母被盖住
- 段 2：1:20、1:40、2:00 — 柱状图、方块流、总结图无遮挡
- 段 3：2:20、3:19（15 万亿停留中）、3:26（YEARS 在数字下方）— 无重叠
- 段 4：4:10、4:30、4:49.8 — 4.9 的 PREDICT 框离左边缘约 157px
- 段 5：4:54.6（12% 先出，74% 未出）、5:38、6:35 — 15.6% 在曲线起点左上方
- 段 6：6:50、7:10.5（只有 PREDICT 台阶）、7:25 — 台阶随旁白出现
- 段 7：7:35、7:48、8:04 — THINKING / PREDICTING 均为白框，光标闪烁
- 抽查中发现并修掉的问题：5.7 的 "15.6%" 标签离左边缘只有约 75px，已把坐标轴整体右移
