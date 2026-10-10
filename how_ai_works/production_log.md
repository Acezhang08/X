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
- 未完成/需人工确认：关键数字上屏时间未逐词对齐；逐段 3 帧抽查未做满；事实来源未重新联网复核；第 1 段动画比配音多约 0.18 秒
- 提示词里要求"旁白文字不要改动"：`narration.py` 中的英文块拼起来与提示词逐字一致
