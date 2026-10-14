# -*- coding: utf-8 -*-
"""English-only burned-in subtitles: white fill, thin black outline, soft shadow, no box.
Cues never break after a function word; one line per cue; also writes subtitles_en.srt."""
import re, math
import skia
from lib import *
from timeline import Timeline

EN_SIZE = 44
MAXW = 1500
SUB_Y = 958
FUNC = set("""a an the of to and or but nor for so yet in on at by with from into onto over under as than that this these those
is are was were be been am it its it's he she they we you i his her their our your my me him them us who whom which what
if then not no do does did can could would should will shall may might must have has had about around after before""".split())

def _words(en): return en.split(" ")

def split_cue(en):
    if tw(en, "sans", EN_SIZE) <= MAXW: return [en]
    n = max(2, math.ceil(tw(en, "sans", EN_SIZE) / MAXW))
    while True:
        words = _words(en); total = tw(en, "sans", EN_SIZE)
        # candidate cut indices (cut AFTER words[i]); never after a function word
        cands = []
        for i in range(len(words) - 1):
            w = re.sub(r"[^\w']", "", words[i]).lower()
            if w in FUNC and not re.search(r"[,;:.?!]$", words[i]): continue
            pen = 0.0 if re.search(r"[,;:.?!]$", words[i]) else 1.0
            cands.append((i, pen))
        cuts = []; last = -1
        for k in range(1, n):
            target = total * k / n; best = None; bd = 1e18
            for i, pen in cands:
                if i <= last: continue
                d = abs(tw(" ".join(words[:i+1]), "sans", EN_SIZE) - target) * (0.6 if pen == 0 else 1.0)
                if d < bd: bd = d; best = i
            if best is None: break
            cuts.append(best); last = best
        parts = []; prev = 0
        for ci in cuts + [len(words) - 1]:
            parts.append(" ".join(words[prev:ci+1])); prev = ci + 1
        if all(tw(p, "sans", EN_SIZE) <= MAXW for p in parts) or n > 6: return parts
        n += 1

def build_cues(T):
    cues = []
    for lid in T.order:
        ln = T.lines[lid]; en = ln["en"]
        parts = split_cue(en)
        pos = 0; starts = []
        for p in parts:
            i = en.index(p, pos); starts.append(i); pos = i + len(p)
        for k, p in enumerate(parts):
            t0 = ln["start"] if k == 0 else T.char_t(lid, starts[k])
            t1 = ln["end"] if k == len(parts) - 1 else T.char_t(lid, starts[k+1])
            cues.append(dict(id=lid, en=p, t0=t0, t1=t1 + (0.18 if k == len(parts) - 1 else 0)))
    for i in range(len(cues) - 1):
        if cues[i]["t1"] > cues[i+1]["t0"]: cues[i]["t1"] = cues[i+1]["t0"]
    return cues

def srt_time(t):
    ms = int(round(t * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return "%02d:%02d:%02d,%03d" % (h, m, s, ms)

def write_srt(cues, path):
    with open(path, "w", encoding="utf-8") as f:
        for i, c in enumerate(cues, 1):
            f.write("%d\n%s --> %s\n%s\n\n" % (i, srt_time(c["t0"]), srt_time(c["t1"]), c["en"]))

def draw_subs(c, cue):
    if cue is None: return
    s = cue["en"]; f = font("sans", EN_SIZE)
    w = f.measureText(s); x0 = W/2 - w/2; by = SUB_Y + EN_SIZE*0.34
    c.drawString(s, x0 + 2, by + 3, f, P(0x000000, alpha=0.55, blur=2.5))
    c.drawString(s, x0, by, f, P(0x000000, "stroke", 3.2, 0.95))
    c.drawString(s, x0, by, f, P(0xFFFFFFFF))
    if QA["on"]: QA["log"].append(dict(s=s, size=EN_SIZE, x0=x0, x1=x0+w, y0=SUB_Y-EN_SIZE*0.5, y1=SUB_Y+EN_SIZE*0.5, deco=False, alpha=1, tag="sub"))

def cue_at(cues, t):
    for c_ in cues:
        if c_["t0"] <= t < c_["t1"]: return c_
    return None

if __name__ == "__main__":
    T = Timeline(); cues = build_cues(T)
    write_srt(cues, "subtitles_en.srt")
    print(len(cues), "cues; max width", max(tw(c["en"], "sans", EN_SIZE) for c in cues))
    bad = [c["en"] for c in cues if re.sub(r"[^\w']", "", c["en"].split()[-1]).lower() in FUNC and not re.search(r"[.?!,;:]$", c["en"])]
    print("cues ending on function word:", bad)
