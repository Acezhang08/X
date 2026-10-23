# -*- coding: utf-8 -*-
"""Text/subtitle consistency checks: script.py == timeline.json == fact_check.md appendix; SRT sanity."""
import json, re, script
from lib import tw
d = json.load(open("timeline.json"))
tl = {l["id"]: l["en"] for l in d["lines"]}
sc = {lid: en for v in script.SEGMENTS.values() for lid, en, _ in v}
fc = dict(re.findall(r"^- `([\d.]+)` (.*)$", open("fact_check.md", encoding="utf-8").read(), re.M))
print("script==timeline:", tl == sc, "| script==fact_check appendix:", fc == sc, "| lines:", len(sc))
srt = open("subtitles_en.srt", encoding="utf-8").read().strip().split("\n\n")
def tsec(s): h, m, x = s.split(":"); sec, ms = x.split(","); return int(h)*3600 + int(m)*60 + int(sec) + int(ms)/1000
prev = 0; bad = []; maxw = 0; short = []
for b in srt:
    n, tt, *tx = b.split("\n"); a, e = [tsec(x) for x in tt.split(" --> ")]
    if a < prev - 1e-3: bad.append(("overlap", n))
    if e <= a: bad.append(("neg", n))
    if e - a < 0.7: short.append((n, round(e - a, 2)))
    prev = e; maxw = max(maxw, tw(" ".join(tx), "sans", 44))
    if len(tx) != 1: bad.append(("multiline", n))
print("cues", len(srt), "problems", bad, "short(<0.7s)", short, "max width px", round(maxw))
# every cue lies inside its sentence window and cues cover each sentence
last = d["lines"][-1]["end"]; print("last cue end", round(prev, 2), "voice end", round(last, 2))
fw = set("a an the of to in on at for and or but so if as is are was were be it its that this with by from than then not no into per until because while".split())
ends = [re.sub(r"[^a-z']", "", b.split("\n")[2].split()[-1].lower()) for b in srt]
print("cue lines ending on a function word:", [(i+1, e) for i, e in enumerate(ends) if e in fw][:20])
