# -*- coding: utf-8 -*-
import re, math
import skia
from lib import *
from timeline import Timeline

EN_SIZE, ZH_SIZE = 44, 40
MAXW = 1640

def _split_points(text, n, kind, size, zh=False):
    """return list of n substrings, balanced by width, preferring punctuation boundaries"""
    if n == 1: return [text]
    total = tw(text, kind, size)
    if zh:
        cand = [i+1 for i, ch in enumerate(text) if ch in "，。？！：；、,"]
        cand += [i for i, ch in enumerate(text) if ch == " "]
        allpos = list(range(1, len(text)))
    else:
        cand = [m.end() for m in re.finditer(r"[,:;.?!]\s", text)]
        allpos = [m.start() + 1 for m in re.finditer(r" ", text)]
    cuts = []; last = 0
    for k in range(1, n):
        target = total * k / n
        def wpos(p): return tw(text[:p], kind, size)
        best = None; bd = 1e9
        for p in allpos + cand:
            if p <= last or p >= len(text): continue
            d = abs(wpos(p) - target)
            if p in cand: d *= 0.55
            if d < bd: bd = d; best = p
        if best is None: best = min(len(text)-1, last + 1)
        cuts.append(best); last = best
    cuts = sorted(set(cuts))
    parts = []; prev = 0
    for p in cuts + [len(text)]:
        parts.append(text[prev:p].strip()); prev = p
    return [p for p in parts if p]

def build_cues(T):
    cues = []
    for lid in T.order:
        ln = T.lines[lid]; en = ln["en"]; zh = ln["zh"]
        n = max(math.ceil(tw(en, "sans", EN_SIZE) / MAXW), math.ceil(tw(zh, "zh", ZH_SIZE) / MAXW), 1)
        # also keep cues short for readability
        while n < 6 and tw(en, "sans", EN_SIZE) / n > 1500: n += 1
        ens = _split_points(en, n, "sans", EN_SIZE)
        if tw(zh, "zh", ZH_SIZE) <= MAXW: zhs = [zh] * len(ens)
        else:
            m = math.ceil(tw(zh, "zh", ZH_SIZE) / MAXW)
            zp = _split_points(zh, m, "zh", ZH_SIZE, True)
            zhs = [zp[min(len(zp) - 1, int(k * len(zp) / len(ens)))] for k in range(len(ens))]
        # char offset of each en part start
        pos = 0; starts = []
        for p in ens:
            i = en.index(p, pos); starts.append(i); pos = i + len(p)
        for k, (e_, z_) in enumerate(zip(ens, zhs)):
            t0 = ln["start"] if k == 0 else T.char_t(lid, starts[k])
            t1 = ln["end"] if k == len(ens) - 1 else T.char_t(lid, starts[k+1])
            cues.append(dict(id=lid, en=e_, zh=z_, t0=t0, t1=t1 + (0.15 if k == len(ens)-1 else 0)))
    # make contiguous inside a line, no overlap across lines
    for i in range(len(cues) - 1):
        if cues[i]["t1"] > cues[i+1]["t0"]: cues[i]["t1"] = cues[i+1]["t0"]
    return cues

def srt_time(t):
    ms = int(round(t * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return "%02d:%02d:%02d,%03d" % (h, m, s, ms)

def write_srt(cues, key, path):
    with open(path, "w", encoding="utf-8") as f:
        for i, c in enumerate(cues, 1):
            f.write("%d\n%s --> %s\n%s\n\n" % (i, srt_time(c["t0"]), srt_time(c["t1"]), c[key]))

def _outlined(c, s, x, y, kind, size):
    f = font(kind, size)
    w = f.measureText(s); x0 = x - w/2; by = y + size*0.36
    c.drawString(s, x0 + 2, by + 3, f, P(0x000000, alpha=0.5, blur=2.5))
    c.drawString(s, x0, by, f, P(0x000000, "stroke", 4.0 if kind == "sans" else 3.4, 0.95))
    c.drawString(s, x0, by, f, P(0xFFFFFFFF))

def draw_subs(c, cue, bilingual):
    if cue is None: return
    if bilingual:
        _outlined(c, cue["en"], W/2, 968, "sans", EN_SIZE)
        _outlined(c, cue["zh"], W/2, 1032, "zh", ZH_SIZE)
    else:
        _outlined(c, cue["en"], W/2, 1008, "sans", EN_SIZE)

def cue_at(cues, t):
    # binary search could be used; linear is fine (few hundred)
    for c_ in cues:
        if c_["t0"] <= t < c_["t1"]: return c_
    return None

def zh_cues(T):
    out = []
    for lid in T.order:
        ln = T.lines[lid]; zh = ln["zh"]
        m = math.ceil(tw(zh, "zh", ZH_SIZE) / MAXW)
        parts = _split_points(zh, m, "zh", ZH_SIZE, True) if m > 1 else [zh]
        tot = sum(len(p) for p in parts); a = ln["start"]; dur = ln["end"] + 0.15 - a
        for p in parts:
            b = a + dur * len(p) / tot; out.append(dict(zh=p, t0=a, t1=b)); a = b
    return out

if __name__ == "__main__":
    T = Timeline(); cues = build_cues(T)
    write_srt(cues, "en", "subtitles_en.srt"); write_srt(zh_cues(T), "zh", "subtitles_zh.srt")
    print(len(cues), max(tw(c["en"], "sans", EN_SIZE) for c in cues), max(tw(c["zh"], "zh", ZH_SIZE) for c in cues))
