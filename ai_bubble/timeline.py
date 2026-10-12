import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
class Timeline:
    def __init__(self, path=None):
        d = json.load(open(path or os.path.join(HERE, "build", "timeline.json")))
        self.lines = {l["id"]: l for l in d["lines"]}
        self.order = [l["id"] for l in d["lines"]]
        self.seg_start = {int(k): v for k, v in d["seg_start"].items()}
        self.duration = d["duration"]
    def s(self, lid): return self.lines[lid]["start"]
    def e(self, lid): return self.lines[lid]["end"]
    def char_t(self, lid, ci):
        ln = self.lines[lid]
        for ch in ln["chunks"]:
            if ch["c0"] <= ci < ch["c1"]:
                f = (ci - ch["c0"]) / max(1, ch["c1"] - ch["c0"])
                return ch["t0"] + f * (ch["t1"] - ch["t0"])
        return ln["end"]
    def w(self, lid, word, nth=0, after=False):
        """time at which `word` (substring of English text) is spoken (proportional estimate)"""
        en = self.lines[lid]["en"]
        i = -1
        for _ in range(nth + 1):
            i = en.index(word, i + 1)
        if after: i += len(word)
        return self.char_t(lid, min(i, len(en) - 1))
    def seg_of(self, t):
        k = 0
        for s, st in self.seg_start.items():
            if t >= st - 0.0: k = s
        return k
