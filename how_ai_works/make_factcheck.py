# -*- coding: utf-8 -*-
import json, re
TL = json.load(open("build/timeline.json"))
R = {r["id"]: r for r in TL["rows"]}
def tc(x): return f"{int(x//60)}:{x%60:05.2f}"
def span(ids):
    ids = ids.replace("–", "-")
    parts = re.split(r"[,\s]+", ids.strip())
    keys = []
    for p in parts:
        if "-" in p:
            a, b = p.split("-"); seg = a.split(".")[0]
            keys += [a, f"{seg}.{b}" if "." not in b else b]
        else: keys.append(p)
    ks = [R[k] for k in keys if k in R]
    return f"{tc(min(k['start'] for k in ks))}–{tc(max(k['end'] for k in ks))}"
ROWS = open("factcheck_rows.txt", encoding="utf-8").read().strip().splitlines()
out = ["# fact_check：旁白事实核查表（含成片时间码）", "", "核实日期：2026-10-09。观点句和示意句已标注。时间码 = 该说法在成片里的起止（mm:ss）。", "",
       "| # | 成片时间码 | 说法 | 来源 | 结论 |", "|---|---|---|---|---|"]
for l in ROWS:
    c = [x.strip() for x in l.split("|")]
    out.append(f"| {c[0]} | {span(c[0])} | {c[1]} | {c[2]} | {c[3]} |")
out += ["", "**刻意没写的说法**：o1 和 GPT-4o 的模型大小、训练数据量（OpenAI 没公开，所以没说「o1 没变大」）；推理模型能「真正思考」（留作结尾问题，不下结论）。", ""]
out.append(open("alignment_check.md", encoding="utf-8").read())
out.append(open("selfcheck.md", encoding="utf-8").read())
open("fact_check.md", "w", encoding="utf-8").write("\n".join(out))
