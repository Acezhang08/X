# -*- coding: utf-8 -*-
"""fact_check.md: narration column is pulled from script.py (cannot drift); verdicts from facts.py."""
import re, json, os
from script import SEGMENTS
from facts import F, SRC, OK, PART, REW, OP, CALC
tl = json.load(open("build/timeline.json")) if os.path.exists("build/timeline.json") else None
start = {l["id"]: l["start"] for l in tl["lines"]} if tl else {}
def mmss(t): return f"{int(t//60)}:{t%60:04.1f}"
rows = []; missing = []
for seg, lines in SEGMENTS.items():
    for lid, en, pre in lines:
        for i, s in enumerate(re.split(r"(?<=[.?!])\s+", en), 1):
            k = f"{lid}.{i}"
            if k not in F: missing.append(k); continue
            typ, claim, srcs, verdict, note = F[k]
            rows.append((k, start.get(lid, 0), s, typ, claim, srcs, verdict, note))
assert not missing, missing
extra = [k for k in F if k not in {r[0] for r in rows}]
assert not extra, extra
cnt = {}
for r in rows: cnt[r[6]] = cnt.get(r[6], 0) + 1
out = []
out.append("# fact_check.md — Humanoid Robots Can Do Backflips. Why Can't They Fold Laundry?\n")
out.append("Checked 2026-10-17. The narration column is generated from `script.py` (exact words as spoken/subtitled). Fact sentences were checked against the sources listed; opinion/judgement sentences are marked **观点** and are not fact-checked.\n")
out.append("## 汇总\n")
out.append(f"- 旁白共 **{len(rows)}** 句（按句号/问号拆分）。")
fact_rows = [r for r in rows if r[3] in ("事实", "转述", "计算")]
out.append(f"- 事实/转述/计算类 **{len(fact_rows)}** 句：已核实 {sum(1 for r in fact_rows if r[6]==OK)}，部分核实（来源为二手或原文打不开）{sum(1 for r in fact_rows if r[6]==PART)}，核查后改写 {sum(1 for r in fact_rows if r[6]==REW)}。")
out.append(f"- 观点/判断/过渡句 **{sum(1 for r in rows if r[3] in ('观点','过渡'))}** 句：标“观点”，不做事实核查。")
out.append("- **删掉或换说法的内容**（写稿阶段就拿掉了，没进成片）见文末“被删/被改的说法”。\n")
out.append("## 读者须知（来源强度）\n")
out.append("- 这个环境的网络策略拒绝了 arxiv.org、openai.com、wikipedia.org、rodneybrooks.com、figure.ai、frc.ri.cmu.edu 等站点（HTTP 403）。因此**所有来源都是通过网页搜索返回的摘要读到的，没有一篇原文是直接打开的**。表里“读法”一栏如实写明。")
out.append("- 因此：莫拉维克的话、布鲁克斯的话**全部转述，不加引号**；片中没有任何引语卡片。")
out.append("- “部分核实” = 数字/事实在 ≥1 个可靠来源的摘要里出现，但原文没打开，或只有二手报道。发布前如要更稳，可在有网的机器上打开原文再对一遍（尤其是 OpenAI 的 13,000 年、Brooks 2036 一句、Figure Go-Big 的日期）。\n")
out.append("## 逐句核查\n")
out.append("| 句号 | 时间 | 旁白（一字不差） | 类型 | 说法 | 来源名 · 链接 · 日期（读法） | 结论 | 备注 |")
out.append("|---|---|---|---|---|---|---|---|")
for k, st, s, typ, claim, srcs, verdict, note in rows:
    src = "<br>".join(f"{SRC[x][0]} · {SRC[x][1]} · {SRC[x][2]} ({SRC[x][3]})" for x in srcs) or "—"
    out.append(f"| {k} | {mmss(st)} | {s} | {typ} | {claim} | {src} | {verdict} | {note} |")
out.append("\n## 被删/被改的说法\n")
out.append("""| 草稿里的说法 | 处理 | 原因 |
|---|---|---|
| Moravec / Brooks 的原话做成引语卡片 | 删，改为转述（无引号） | 原文都打不开，转述版本在不同二手来源里措辞不一，无法保证“一字不差” |
| “Marc Raibert: a robot that works 70% of the time doesn't work” | 删 | 两次检索都没找到出处，无法核实 |
| “Agility's Jonathan Hurst: ~10 years until useful home robots” | 删 | 只在一个媒体监测站的二手摘要里出现 |
| “PR2 folded a towel in 25 minutes” | 删 | 检索没有任何来源给出耗时 |
| “AgiBot World: >1M trajectories ≈ 3,000 hours” | 改为只讲“近 3,000 小时、100+ 台机器人” | 1M 条轨迹和 2,976.4 小时来自不同口径（论文摘要 vs 数据集 beta 页），合在一起可能把两个量混为一谈 |
| “the oldest known fossil eyes are ~530 million years old” | 改为“Fossil eyes date back more than 500 million years” | “最古老”可能已被新发现取代 |
| “The companies say openly that the human is part of the plan” | 改为“Some companies …” | 上一段讲 Tesla，Tesla 并没有这样“公开说” |
| “the laundry robot on sale” | 改为“a laundry robot on sale” | 不能暗示这是市面上唯一一款 |
| Figure Go-Big 的发布日期（草稿写 2025 年 9 月） | 删日期 | 检索只确认了同月的融资新闻，没有确认 Go-Big 本身的日期 |
| “Humans ‘scam’ / ‘fake’ demos” 一类措辞 | 从未使用 | 按要求，没有出处的指控不说；片中只说“有人远程操作”这一有出处的事实 |
""")
out.append("## 画面上出现、但旁白没逐字说的内容（同样已核对）\n")
out.append("- 1.3：“3.5 - 2.5”（Deep Blue 对 Kasparov 的比分，History.com / ChessBase）。\n- 2.4：“2021 · ETH ZURICH + NVIDIA”（Rudin et al.）。\n- 3.8：“IROBOT CO-FOUNDER”（Rodney Brooks）。\n- 3.9：“OPENAI · 2019”。\n- 5.2：“OCT 2024 · WE, ROBOT EVENT”、“BLOOMBERG, 14 OCT 2024”。\n- 5.3：“OCT 2025 · WSJ HOME-ROBOT TEST”。\n- 6.6：“OUR BET (OPINION)”（我们的判断，已标注）。\n- 所有画面上的“SRC:”小字都对应上表的来源名。\n- 3.2 里的小点点（控制点）、4.4 里的 22 个机器人小图、4.6 里的 124 个方块，都是示意图，数量对应旁白数字（22 种、124 天）。2.3 的“ATTEMPTS”计数器是示意（标有 ILLUSTRATIVE），不代表任何真实次数。\n")
open("fact_check.md", "w", encoding="utf-8").write("\n".join(out))
print(len(rows), "sentences;", cnt)
