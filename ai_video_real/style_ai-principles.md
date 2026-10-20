# 「AI 原理」系列固定画风（3Blue1Brown 式几何动画）

沿用本文件即可，不要改动配色含义。

## 画幅与底色
- 16:9，1920×1080，30fps；底色纯色 `#16181D`，无纹理、无网格
- 内容区：y ∈ [-2.45, 3.55]（Manim 单位，帧高 8）。底部约 1.5 个单位留给字幕

## 颜色（含义固定，不混用）
| 颜色 | 色值 | 含义 |
|---|---|---|
| 蓝 | `#58C4DD` | token、数字、模型内部 |
| 黄 | `#F5D547` | 概率、被选中的词、关键数字 |
| 绿 | `#83C167` | 正确 / 奖励 |
| 红 | `#FC6255` | 错误 / 没有奖励（少用） |
| 白 | `#ECECEC` | 普通文字和线条 |
| 灰 | `#6B7080` | 次要标注、"illustrative" |

## 字体
- 标题、大数字：CMU Serif；标签、注释：Inter；token 与编号：JetBrains Mono
- 画面文字不小于 32px（Manim `font_size` ≥ 18，约 34px）

## 元素语言
- 方块、圆点、箭头、柱状概率条、神经网络点线图；一切都是几何形状
- 不用图标库、插画、照片、人脸、logo；"人"用白色小圆 + 半圆
- 公司和模型名只用文字
- 示意性内容（token 编号、概率值、曲线）角落小字写 "illustrative"

## 动画
- Transform / Write / Create / 数字滚动；段内元素变形衔接；每 20–30 秒一个明显视觉变化
- 段与段之间用淡出淡入（落在停顿里），不用花哨转场

## 字幕
- 白字 + 细黑描边 + 轻阴影，无边框无底色块；英文 46px、中文 42px；抖音版英上中下

## 代码入口
- `common.py`（颜色、字体、`Seg` 基类、`counter`、`prob_chart`、`check`）
- `scenes/seg0.py … seg7.py`，每段一个 Scene，时间全部取自 `build/timeline.json`
- 已知坑：计数器 Text 不能和 `FadeIn` 同时播放；`TransformFromCopy` 的目标不会留在场景里，用 `ReplacementTransform(x.copy(), target)`
