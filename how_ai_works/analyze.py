# -*- coding: utf-8 -*-
"""关键数字上屏时间 vs 逐词对齐的口播时间 -> alignment_check.md"""
import json, re, glob
H = "/home/user/X/how_ai_works"
W = {(w["row"], w["i"]): [(re.sub(r"\(\d+\)", "", n), a, b) for n, a, b in w["words"] if n not in ("<sil>", "+SPN+")] for w in json.load(open(f"{H}/build/words.json"))}
marks = {}
for f in glob.glob(f"{H}/build/marks_*.json"):
    marks.update(json.load(open(f)))
# 名称: (行, 块, 起始词, 起始词序号, 结束词, 结束词序号)
SPEC = {
    "12% (0.4)": ("0.4", 0, "twelve", 0, "percent", 0),
    "74% (0.5)": ("0.5", 0, "seventy", 0, "percent", 0),
    "4 characters (1.3)": ("1.3", 0, "four", 0, "characters", 0),
    "3/4 of a word (1.3)": ("1.3", 1, "three", 0, "quarters", 0),
    "175 billion (3.2)": ("3.2", 0, "one", 0, "billion", 0),
    "15 trillion (3.9)": ("3.9", 1, "fifteen", 0, "tokens", 0),
    "90,000 years (3.10)": ("3.10", 2, "ninety", 0, "years", 0),
    "1.3B (4.6)": ("4.6", 1, "one", 0, "billion", 0),
    "175B (4.6)": ("4.6", 2, "one", 0, "billion", 0),
    "x100+ (4.7)": ("4.7", 0, "one", 0, "times", 0),
    "12% (5.1)": ("5.1", 1, "twelve", 0, "percent", 0),
    "74% (5.1)": ("5.1", 1, "seventy", 0, "four", 0),
    "15.6% (5.7)": ("5.7", 1, "fifteen", 0, "percent", 0),
    "71% (5.7)": ("5.7", 1, "seventy", 0, "percent", 1),
}
COUNT = {"12% (0.4)", "74% (0.5)", "175 billion (3.2)", "15 trillion (3.9)", "90,000 years (3.10)"}
def pick(row, ci, word, k, end):
    hits = [(a, b) for n, a, b in W[(row, ci)] if n == word]
    return hits[k][1 if end else 0]
def tc(x): return f"{int(x//60)}:{x%60:05.2f}"
lines = ["| 数字 | 类型 | 口播词（逐词对齐） | 口播起止 | 画面上屏起止（实测） | 判定误差 | ≤0.3s |", "|---|---|---|---|---|---|---|"]
worst = 0
for name, (row, ci, w0, k0, w1, k1) in SPEC.items():
    ws, we = pick(row, ci, w0, k0, False), pick(row, ci, w1, k1, True)
    ms, me = marks[name]
    kind = "滚动计数" if name in COUNT else "弹出"
    err = (me - we) if name in COUNT else (ms - ws)
    worst = max(worst, abs(err))
    lines.append(f"| {name} | {kind} | {w0} … {w1} | {tc(ws)}–{tc(we)} | {tc(ms)}–{tc(me)} | {err:+.2f}s | {'✅' if abs(err) <= 0.3 else '❌'} |")
txt = ["## 关键数字逐词对齐检查", "",
       "方法：用 pocketsphinx 对 narration.wav 的每个字幕块做强制对齐（Whisper 模型在本环境下载被拦，改用此法），得到每个词的起止时间；"
       "画面时间来自场景代码里每个数字动画的实际起止（`marks_*.json`）。"
       "判定误差：「弹出」类 = 数字动画开始 − 口播起始词开始；「滚动计数」类 = 计数器滚到终值的时刻 − 口播结束词结束（边说边滚，说完时到位）。正数 = 画面晚于口播。", "",
       *lines, "",
       f"最大绝对误差：{worst:.2f} 秒。强制对齐本身有约 ±0.05–0.1 秒的不确定度。"
       "滚动计数在口播起始词之前就开始滚是设计（要说完时到位），所以只看到位时刻。", ""]
open(f"{H}/alignment_check.md", "w", encoding="utf-8").write("\n".join(txt))
print("\n".join(lines)); print("worst", worst)
