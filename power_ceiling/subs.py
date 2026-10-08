import json, math, re
tl = json.load(open('timeline.json'))
EN_MAX, ZH_MAX = 56, 30
WEAK = set("a an the of to than its it's their his her our your my this that these those and or but nor as at by for from in into on onto over with within without per via is are was were be been being has have had will would can could may might must shall should not no if while when which who about more so than then there here what how why it up much william stanley now".split())
def weak_end(w): return (not re.search(r'[,:;.?!—)]$', w)) and re.sub(r"[^\w']", '', w).lower() in WEAK
def dp_split(units, n, bonus, bad=frozenset()):
    """units: 每个单元的字符长度；bonus: 在第 i 个单元之后切有奖励；bad: 在第 i 个单元之后切要重罚（停在虚词上）。返回 n 段 [a,b)"""
    N = len(units); pre = [0]
    for u in units: pre.append(pre[-1] + u)
    INF = 1e18; dp = [[INF] * (N + 1) for _ in range(n + 1)]; bk = [[0] * (N + 1) for _ in range(n + 1)]; dp[0][0] = 0
    for k in range(1, n + 1):
        for i in range(k, N + 1):
            for j in range(k - 1, i):
                ln_ = pre[i] - pre[j]
                c = dp[k - 1][j] + ln_ ** 2 + max(0, ln_ - 62) ** 2 * 60 - (700 if (j in bonus and k > 1) else 0) + (400000 if (j in bad and k > 1) else 0)
                if c < dp[k][i]: dp[k][i] = c; bk[k][i] = j
    out, i = [], N
    for k in range(n, 0, -1): j = bk[k][i]; out.append((j, i)); i = j
    return out[::-1]
def split_en(s, n):
    words = s.split(' ')
    if n == 1 or len(words) < n: return [s]
    bonus = {i + 1 for i, w in enumerate(words[:-1]) if re.search(r'[,:;.?!—]$', w)}
    bad = {i + 1 for i, w in enumerate(words[:-1]) if weak_end(w)}
    return [' '.join(words[a:b]) for a, b in dp_split([len(w) + 1 for w in words], n, bonus, bad)]
def cuts(s, n, punct):
    if n == 1: return [s]
    chars = list(s); bonus = {m.end() for m in re.finditer(punct, s)}
    return [s[a:b].strip() for a, b in dp_split([1] * len(chars), n, bonus)]
def zh_align(z, en_lens):
    """中文按英文各段的字数占比来切，尽量落在标点后（±7 字内），不切在数字或英文单词中间"""
    n = len(en_lens)
    if n == 1: return [z]
    tot = sum(en_lens); cum = 0; cuts_ = []
    punct = {m.end() for m in re.finditer(r'[，。？！：；、]', z)}
    for k in range(n - 1):
        cum += en_lens[k]; tgt = round(len(z) * cum / tot)
        near = [p for p in punct if abs(p - tgt) <= 12 and p > (cuts_[-1] if cuts_ else 0) and p < len(z)]
        if near: c = min(near, key=lambda p: abs(p - tgt))
        else:
            AV = set('的没把在向对从和与了着是有就为被让给按比到跟同将并而且但也都还很更最')
            ok = [p for p in range(max(1, tgt - 8), min(len(z), tgt + 8) + 1) if z[p - 1] not in AV and not (re.match(r'[A-Za-z0-9.,%$]', z[p - 1]) and p < len(z) and re.match(r'[A-Za-z0-9.,%$]', z[p]))]
            c = min(ok, key=lambda p: abs(p - tgt)) if ok else tgt
        c = max(c, (cuts_[-1] if cuts_ else 0) + 1); cuts_.append(min(c, len(z)))
    out, a = [], 0
    for c in cuts_ + [len(z)]: out.append(z[a:c].strip()); a = c
    return out
cues = []
for L in tl['lines']:
    n = max(math.ceil(len(L['en']) / 54), math.ceil(len(L['zh']) / 28))
    en = split_en(L['en'], n); n = len(en)
    zh = zh_align(L['zh'], [len(e) for e in en])
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
