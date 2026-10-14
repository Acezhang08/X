# -*- coding: utf-8 -*-
"""Writes publish.md. Chapter times come straight from timeline.json (first sentence of each segment)."""
import json
d = json.load(open("build/timeline.json"))
st = {int(k): v for k, v in d["seg_start"].items()}
def mmss(t): t = int(t); return f"{t // 60}:{t % 60:02d}"
names = {
    0: "The secretary who asked him to leave the room",
    1: "How ELIZA's trick actually works",
    2: "The part Weizenbaum did not expect",
    3: "Who Weizenbaum was, and his warning",
    4: "The code nobody could read for 55 years",
    5: "How ELIZA does against today's AI",
    6: "What he was really warning about",
}
chap = [("0:00", names[0])] + [(mmss(st[k]), names[k]) for k in range(1, 7)]
dur = d["duration"]
titles = [
    ("A", "She Knew It Was Just a Program. She Still Asked Him to Leave the Room.", "thumbnail_A.png（LEAVE THE ROOM）",
     "冲突式：用开场 0:00–0:20 的事实（0.2、0.3 句）。"),
    ("B", "Why the Inventor of the First Chatbot Warned Us About AI", "thumbnail_C.png（NOTHING INSIDE）",
     "搜索式：对应“first chatbot / who invented AI”类问法；讲的是 1976 年他的书与 1966 年论文里的警告。"),
    ("C", "A 1966 Chatbot Scored 23% on a Turing Test. GPT-4o Scored 21%.", "thumbnail_B.png（1966 CHATBOT）",
     "数字式：23% 与 21% 都在 5.4 句，来源 Jones & Bergen 2025；没有写“打败”（两者差距不显著）。"),
]
desc = f"""In the mid-1960s, a secretary at MIT knew the program she was typing to was only a program — and still asked its creator to leave the room. This video explains how the first chatbot, ELIZA, really worked, why its creator Joseph Weizenbaum spent decades warning about it, and why that warning fits today's chatbots.

Chapters
""" + "\n".join(f"{t} {n}" for t, n in chap) + """

Sources (names only)
Joseph Weizenbaum, "ELIZA — A Computer Program For the Study of Natural Language Communication Between Man and Machine" (Communications of the ACM, January 1966) · Joseph Weizenbaum, Computer Power and Human Reason (1976) · Anthony Hay's ELIZA transcriptions and notes · Shrager et al., "ELIZA Reanimated" (arXiv, 2025) · Douglas Hofstadter, Fluid Concepts and Creative Analogies (1995) · RFC 439 "PARRY Encounters the DOCTOR" · Cameron Jones and Benjamin Bergen (UC San Diego), "Large Language Models Pass the Turing Test" (2025) · OpenAI statement on the April 2025 ChatGPT update, as reported by TechCrunch · TechCrunch report on ChatGPT's 800 million weekly users (October 2025) · Pew Research Center, Americans and AI 2026 · Common Sense Media teen AI companion survey (2025) · Illinois Wellness and Oversight for Psychological Resources Act (2025) · Federal Trade Commission 6(b) orders on AI companion chatbots (September 2025) · MIT News obituary of Joseph Weizenbaum (2008)

All illustrations are original drawings. People are shown only as silhouettes; no photos and no synthesized voices of real people.
"""
pinned = "Have you ever told a chatbot something you would not tell a person? Did it feel easier because it was a machine — or in spite of it? I read every reply."
md = f"""# publish.md — 发布包（《ELIZA》，"AI 的历史"系列第 1 期）

成片时长 {mmss(dur)}（{dur:.1f} 秒），1920×1080，30fps，H.264 + AAC。播放列表：**The History of AI**。

## 1. 三个标题（用于 A/B 测试）
每个数字和说法都在视频里讲到并核实过（见 `fact_check.md`）；没有用 Explained / Overview / Evolution。

| 版本 | 标题 | 配的缩略图 | 说明 |
|---|---|---|---|
""" + "\n".join(f"| {a} | {t} | {th} | {n} |" for a, t, th, n in titles) + f"""

## 2. 三张缩略图（1280×720 PNG，同一旧纸墨线画风）
- `thumbnail_A.png` — **LEAVE THE ROOM**：敞开的暗门 + 打字机前的秘书剪影（3 个词，焦点是那扇门，朱红只用在 ROOM）。
- `thumbnail_B.png` — **1966 CHATBOT**：巨大的朱红 1966（2 个词）。
- `thumbnail_C.png` — **NOTHING INSIDE**：虚线空心人像 + 朱红问号 + 省略号气泡（2 个词）。
- 都已在 320×180 缩略尺寸下检查：文字与焦点 0.5 秒内可读，高反差（深墨 + 朱红 on 浅米黄）。

## 3. 描述（可直接粘贴；不含任何链接）
```
{desc}```

## 4. 播放列表
The History of AI

## 5. 置顶评论
> {pinned}

## 6. AI 标注
**不勾**。全动画讲解；AI 只用在写稿与配音（Kokoro 合成的是通用旁白声，不是任何真人的声音），画面是程序绘制的插画，没有仿真人物或伪造的真实片段。

## 7. 其他建议
- 字幕：上传 `subtitles_en.srt`（画面里已烧录英文字幕；上传 SRT 是为了让 YouTube 能索引文字，也可在 YouTube 里关闭字幕轨道避免重复）。
- 标签（Tags）：ELIZA, first chatbot, Joseph Weizenbaum, history of AI, ELIZA effect, Turing test, chatbot history, AI companions
- 章节第一个是 0:00，每段时间来自 `timeline.json` 里该段第一句的实际开始时间。
"""
open("publish.md", "w", encoding="utf-8").write(md)
print(md[:1500])
