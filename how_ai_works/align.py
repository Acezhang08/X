# -*- coding: utf-8 -*-
"""逐词对齐：用 pocketsphinx 强制对齐 narration.wav 的每个字幕块，输出 build/words.json"""
import json, re, sys, os
import numpy as np, soundfile as sf
from scipy.signal import resample_poly
from pocketsphinx import Decoder, get_model_path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from narration import tts_text
H = os.path.dirname(os.path.abspath(__file__))
TL = json.load(open(f"{H}/build/timeline.json"))
a, sr = sf.read(f"{H}/build/narration.wav")
a16 = resample_poly(a, 2, 3).astype(np.float32)  # 24k -> 16k
OOV = {"openai": "open a i", "deepseek": "deep seek", "llama": "lama", "instructgpt": "instruct g p t", "chatbot": "chat bot",
       "nonstop": "non stop", "anthropic": "anthropic", "aime": "a i m e", "oh": "oh", "autocomplete": "auto complete"}
out = []
mp = get_model_path()
DICT = {l.split()[0].split("(")[0] for l in open(f"{mp}/en-us/cmudict-en-us.dict", encoding="utf-8", errors="ignore") if l.strip()}
for c in TL["chunks"]:
    spoken = tts_text(c["en"]).lower().replace("-", " ")
    words = re.findall(r"[a-z']+", spoken)
    exp = []
    for w in words:
        for t in OOV.get(w, w).split():
            if t in DICT:
                exp.append(t)
            elif t.endswith("'s") and t[:-2] in DICT:
                exp += [t[:-2], "s"] if "s" in DICT else [t[:-2]]
            else:
                print("OOV skipped:", t)
    s0, e0 = c["start"] - 0.1, c["end"] + 0.1
    seg = a16[max(0, int(s0 * 16000)): int(e0 * 16000)]
    pcm = (seg * 32767).astype(np.int16).tobytes()
    cfg = Decoder.default_config()
    cfg.set_string("-hmm", f"{mp}/en-us/en-us"); cfg.set_string("-dict", f"{mp}/en-us/cmudict-en-us.dict")
    cfg.set_string("-loglevel", "FATAL")
    d = Decoder(cfg)
    d.set_align_text(" ".join(exp))
    d.start_utt(); d.process_raw(pcm, full_utt=True); d.end_utt()
    ws = []
    base = max(c["start"] - 0.1, 0)
    try:
        for sg in d.seg():
            ws.append((sg.word, round(base + sg.start_frame / 100.0, 3), round(base + (sg.end_frame + 1) / 100.0, 3)))
    except Exception as ex:
        print("ALIGN FAIL", c["row"], c["i"], ex)
    out.append({"row": c["row"], "i": c["i"], "text": c["en"], "words": ws})
json.dump(out, open(f"{H}/build/words.json", "w"), indent=1)
print("chunks", len(out))
