"""Build the two burned-in subtitle tracks from build/timings.json.

build/subs-en.ass : English only (X / YouTube)
build/subs-bi.ass : English on top, Chinese below (Douyin)
White text, thin black outline, light shadow + soft blurred halo underneath, no box.
"""
import json
from PIL import ImageFont

T = json.load(open("build/timings.json"))
SCRIPT = json.load(open("script.json"))
EN_FONT, EN_SIZE = "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf", 60
ZH_FONT, ZH_SIZE = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc", 54
MAXW = 1740
fen, fzh = ImageFont.truetype(EN_FONT, EN_SIZE), ImageFont.truetype(ZH_FONT, ZH_SIZE, index=2)

def wrap(text, font, cjk=False):
    if font.getlength(text) <= MAXW:
        return [text]
    units = list(text) if cjk else text.split(" ")
    sep = "" if cjk else " "
    best = None
    for i in range(1, len(units)):
        a, b = sep.join(units[:i]), sep.join(units[i:])
        if cjk and b[:1] in "，。、：”）!?,.":  # 不让标点开头
            continue
        if max(font.getlength(a), font.getlength(b)) > MAXW:
            continue
        score = max(font.getlength(a), font.getlength(b)) + (0 if a[-1] in ",.:;，。：" else 400)
        if best is None or score < best[0]:
            best = (score, [a, b])
    return best[1]

def ts(t):
    t = max(0, t); h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"

HEAD = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: EN,Inter SemiBold,{EN_SIZE},&H00FFFFFF,&H00FFFFFF,&H00000000,&H7A000000,0,0,0,0,100,100,0,0,1,2.6,2,2,100,100,58,1
Style: HALO,Inter SemiBold,{EN_SIZE},&HFF000000,&HFF000000,&H9A000000,&HFF000000,0,0,0,0,100,100,0,0,1,9,0,2,100,100,58,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
lines = T["lines"]
for name, bi in [("subs-en.ass", False), ("subs-bi.ass", True)]:
    ev = []
    for i, l in enumerate(lines):
        start = l["start"] - 0.08
        end = lines[i + 1]["start"] - 0.1 if i + 1 < len(lines) else T["duration"]
        end = max(end, l["end"] + 0.25)
        sc = SCRIPT[i]
        en = sc.get("sub_en") or r"\N".join(wrap(l["en"], fen))
        txt = en
        if bi:
            zh = sc.get("sub_zh") or r"\N".join(wrap(l["zh"], fzh, cjk=True))
            txt = en + r"\N{\r\fnNoto Sans CJK SC\b1\fs" + str(ZH_SIZE) + r"\fsp1}" + zh
        # 底层：模糊的半透明黑色光晕（白色画面上也看得清），不是底色块
        halo = r"{\blur12}" + txt.replace("{\\r", "{\\rHALO\\blur12")
        ev.append(f"Dialogue: 0,{ts(start)},{ts(end)},HALO,,0,0,0,,{halo}")
        ev.append(f"Dialogue: 1,{ts(start)},{ts(end)},EN,,0,0,0,,{txt}")
    open("build/" + name, "w").write(HEAD + "\n".join(ev) + "\n")
    print(name, len(ev), "events")
for l in lines:
    print(wrap(l["en"], fen), wrap(l["zh"], fzh, True))
