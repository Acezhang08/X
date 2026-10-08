import json, math, re
tl = json.load(open('timeline.json'))
EN_MAX, ZH_MAX = 56, 30
def dp_split(units, n, bonus):
    """units: 每个单元的字符长度列表；bonus: 在第 i 个单元之后切有奖励的集合。返回 n 段的 [a,b) 区间"""
    N = len(units); pre = [0]
    for u in units: pre.append(pre[-1] + u)
    INF = 1e18; dp = [[INF] * (N + 1) for _ in range(n + 1)]; bk = [[0] * (N + 1) for _ in range(n + 1)]; dp[0][0] = 0
    for k in range(1, n + 1):
        for i in range(k, N + 1):
            for j in range(k - 1, i):
                c = dp[k - 1][j] + (pre[i] - pre[j]) ** 2 - (250 if (j in bonus and k > 1) else 0)
                if c < dp[k][i]: dp[k][i] = c; bk[k][i] = j
    out, i = [], N
    for k in range(n, 0, -1): j = bk[k][i]; out.append((j, i)); i = j
    return out[::-1]
def split_en(s, n):
    words = s.split(' ')
    if n == 1 or len(words) < n: return [s]
    bonus = {i + 1 for i, w in enumerate(words[:-1]) if re.search(r'[,:;.?!—]$', w)}
    return [' '.join(words[a:b]) for a, b in dp_split([len(w) + 1 for w in words], n, bonus)]
def cuts(s, n, punct):
    if n == 1: return [s]
    chars = list(s); bonus = {m.end() for m in re.finditer(punct, s)}
    return [s[a:b].strip() for a, b in dp_split([1] * len(chars), n, bonus)]
cues = []
for L in tl['lines']:
    n = max(math.ceil(len(L['en']) / 54), math.ceil(len(L['zh']) / 28))
    en = split_en(L['en'], n); n = len(en)
    zh = cuts(L['zh'], n, r'[，。？！：；、]')
    while len(zh) < n: zh.append('')
    tot = sum(len(x) for x in en); t = L['start']
    for i, (e, z) in enumerate(zip(en, zh)):
        d = (L['end'] - L['start']) * len(e) / tot
        end = L['end'] + .2 if i == n - 1 else t + d
        cues.append(dict(id=L['id'], start=round(t, 3), end=round(end, 3), en=e, zh=z)); t += d
def ts(x, sep=','):
    h = int(x // 3600); m = int(x % 3600 // 60); s = x % 60
    return f"{h:02d}:{m:02d}:{int(s):02d}{sep}{int(round((s - int(s)) * 1000)):03d}".replace('1000', '999')
open('subtitles_en.srt', 'w').write('\n'.join(f"{i+1}\n{ts(c['start'])} --> {ts(c['end'])}\n{c['en']}\n" for i, c in enumerate(cues)))
open('subtitles_zh.srt', 'w').write('\n'.join(f"{i+1}\n{ts(c['start'])} --> {ts(c['end'])}\n{c['zh']}\n" for i, c in enumerate(cues)))
def ass(bi):
    hdr = """[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Liberation Sans,%d,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,2.4,1.8,2,60,60,%d,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
""" % ((58, 34) if bi else (60, 60))
    def at(x):
        h = int(x // 3600); m = int(x % 3600 // 60); s = x % 60
        return f"{h}:{m:02d}:{s:05.2f}"
    ev = []
    for c in cues:
        txt = c['en'].replace('—', '–')
        if bi: txt += r"\N{\fnWenQuanYi Zen Hei\fs52\b0}" + c['zh']
        ev.append(f"Dialogue: 0,{at(c['start'])},{at(c['end'])},Default,,0,0,0,,{txt}")
    return hdr + '\n'.join(ev) + '\n'
open('subs_yt.ass', 'w').write(ass(False)); open('subs_dy.ass', 'w').write(ass(True))
json.dump(cues, open('cues.json', 'w'), ensure_ascii=False, indent=1)
print(len(cues), 'cues; max EN', max(len(c['en']) for c in cues), 'max ZH', max(len(c['zh']) for c in cues))
