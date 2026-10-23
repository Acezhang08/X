# -*- coding: utf-8 -*-
"""Segments 4 (who pays), 5 (the rules) and 6 (the ending)."""
from common import *
from scenes_a import cam, ftext
from scenes_b import quote_card

# ================================================================== SEGMENT 4
def seg4(c, t):
    s = S
    # ---- who pays? (4.1)
    a0, b0 = s("4.1") - 0.05, s("4.2") - 0.5
    with ph(c, t, a0, b0, 0.35):
        stamp(c, "WHO PAYS?", 960, 440, t, a0 + 0.1, INK, -3, 190, pad=(70, 40))
    # ---- monitor's problem statement (4.2 - 4.3)
    a1, b1 = s("4.2") - 0.05, s("4.4") - 0.5
    with ph(c, t, a1, b1, 0.35):
        quote_card(c, 960, 400, 1560, 520, t, a1, None,
                   ["data centers “pay for their own capacity and", "do not impose capacity costs", "on other customers”"],
                   "PJM's market monitor, on what it wants · July 27, 2026", 60, 61)
        w1 = tw("data centers “pay for their own capacity and", "serif", 60); w3 = tw("on other customers”", "serif", 60)
        pen_line(c, 960 - w1/2, 345, 960 + w1/2, 345, prog(t, Wd("4.2", "pay for") - 0.5, Wd("4.2", "pay for") + 0.8), RED, 9, 1.0, 2)
        pen_line(c, 960 - w3/2, 482, 960 + w3/2, 482, prog(t, Wd("4.2", "other customers") - 0.8, Wd("4.2", "other customers") + 0.3), RED, 9, 1.0, 4)
        stamp(c, "TODAY: THE COST IS SHARED", 960, 780, t, s("4.3") - 0.05, RED, -2, 64, pad=(40, 22))
    # ---- household estimates (4.4 - 4.5)
    a2, b2 = s("4.4") - 0.05, s("4.6") - 0.5
    with ph(c, t, a2, b2, 0.35):
        for x, nm, v, ta, sd in ((520, "WESTERN MARYLAND", 18, Wd("4.4", "eighteen"), 71), (1400, "OHIO", 16, Wd("4.4", "sixteen"), 72)):
            with clip(c, x, 400, 720, 500, t, a2 + 0.1, None, rot=(-1.5 if x < 900 else 1.5), seed=sd) as ok:
                if ok:
                    text(c, nm, 0, -170, "sans", 50, INK)
                    vv = roll(t, ta - 0.3, 0.9, 0, v)
                    text(c, "≈ $%d" % round(vv) if t >= ta - 0.3 else "≈ $?", 0, -20, "mono", 150, RED if t >= ta - 0.3 else DKGRAY)
                    text(c, "per month, average home", 0, 100, "sansr", 40, DKGRAY)
                    text(c, "higher capacity prices", 0, 155, "sansr", 40, DKGRAY)
        tag(c, "ESTIMATE · IEEFA, A THINK TANK", 960, 740, t, Wd("4.4", "think tank") - 0.1, INK, 40, "sans")
        c5 = s("4.5") - 0.05
        for xr in (520, 1400):
            pen_ellipse(c, xr, 380, 290, 78, prog(t, Wd("4.5", "Careful"), Wd("4.5", "Careful") + 0.9), RED, 9, xr % 7)
        stamp(c, "THE WHOLE CAPACITY JUMP — NOT ONLY DATA CENTERS", 960, 830, t, c5, RED, -1.5, 40, pad=(30, 16))
    # ---- +42% (4.6)
    a3, b3 = s("4.6") - 0.05, s("4.7") - 0.5
    with ph(c, t, a3, b3, 0.35):
        with board(c, 960, 420, 1400, 600, t, a3, None, rot=0.5, seed=15) as ok:
            if ok:
                text(c, "US RESIDENTIAL ELECTRICITY PRICES · FIVE YEARS", 0, -230, "sans", 44, 0xFFC9C2B2)
                t1 = Wd("4.6", "forty-two") - 0.5
                v = roll(t, t1, 1.2, 0, 42)
                text(c, "+%d%%" % round(v) if t >= t1 else "+?%", 0, -40, "mono", 260, VERM if t >= t1 else DKGRAY)
                text(c, "not just data centers", 0, 150, "sansr", 56, CREAM)
        src(c, "Source: federal EIA data, cited by PolitiFact, June 2026", 960, 880, "c")
    # ---- other drivers (4.7)
    a4, b4 = s("4.7") - 0.05, s("4.8") - 0.5
    with ph(c, t, a4, b4, 0.35):
        items = [("AGING\nEQUIPMENT", 400, "pylon"), ("DISASTER\nRECOVERY", 960, "flame"), ("NATURAL GAS\nPRICES", 1520, "gas")]
        for i, (nm, x, ic) in enumerate(items):
            ta = a4 + 0.1 if i == 0 else Wd("4.7", ("aging", "disaster", "natural gas")[i]) - 0.3
            with clip(c, x, 420, 460, 560, t, ta, None, rot=(-2, 1, -1)[i], seed=80 + i) as ok:
                if ok:
                    if ic == "pylon": pylon(c, 0, 90, 0.85, INK)
                    elif ic == "flame": flame(c, 0, 60, 1.5, RED)
                    else:
                        c.drawCircle(0, -30, 80, P(INK, "stroke", 9)); text(c, "GAS", 0, -30, "mono", 56, INK)
                    a_, b_ = nm.split("\n")
                    text(c, a_, 0, 140, "sans", 46, INK); text(c, b_, 0, 192, "sans", 46, INK)
        ftext(c, "EPRI: THESE MATTERED MORE", 960, 800, t, Wd("4.7", "mattered") - 0.3, "sans", 56, GREEN)
    # ---- both true (4.8)
    a5 = s("4.8") - 0.05
    with ph(c, t, a5, None, 0.35):
        with clip(c, 520, 430, 740, 520, t, a5, None, rot=-1.5, seed=91) as ok:
            if ok:
                text(c, "NATIONALLY", 0, -170, "sans", 54, INK)
                text(c, "NOT THE MAIN", 0, -50, "serif", 66, GREEN)
                text(c, "REASON BILLS ROSE", 0, 30, "serif", 66, GREEN)
                text(c, "(per EPRI)", 0, 130, "sansr", 40, DKGRAY)
        with clip(c, 1400, 430, 740, 520, t, Wd("4.8", "But in a grid") - 0.2, None, rot=1.5, seed=92) as ok:
            if ok:
                text(c, "GRID WITH NO ROOM", 0, -170, "sans", 54, INK)
                text(c, "CAN BE THE MAIN", 0, -50, "serif", 66, RED)
                text(c, "REASON ONE PRICE DID", 0, 30, "serif", 60, RED)
                text(c, "(per the market monitor)", 0, 130, "sansr", 40, DKGRAY)

# ================================================================== SEGMENT 5
def seg5(c, t):
    s = S
    a0 = s("5.1") - 0.05
    ftext(c, "THE RULES, STATE BY STATE", 960, 125, t, a0, "sans", 56, INK)
    ftext(c, "what has actually happened", 960, 182, t, a0 + 0.2, "sansr", 40, DKGRAY, b=s("5.6") - 0.4)
    cards = [
        (500, 450, "5.2", "OREGON · HOUSE BILL 3546", ["A separate rate class", "for very large energy users", "Costs assigned to them"], "LAW", GREEN),
        (1420, 450, "5.3", "TEXAS · SENATE BILL 6", ["Signed June 2025", "Loads of 75 MW and up", "help pay to connect"], "SIGNED", GREEN),
        (500, 745, "5.4", "VIRGINIA · REGULATORS", ["Rate class for 25 MW and up", "Starts January 2027", "14-year contracts, minimums"], "APPROVED", GREEN),
        (1420, 745, "5.5", "PJM'S MARKET MONITOR", ["Take data centers out of", "the shared capacity market", "Give them their own auction"], "PROPOSAL", 0xFFA06E00),
    ]
    for i, (x, y, lid, head, lines, stp, col) in enumerate(cards):
        ta = s(lid) - 0.05
        pa = e_out(prog(t, a0 + 0.5 + i*0.9, a0 + 0.9 + i*0.9)) * (1 - e_out(prog(t, ta, ta + 0.25)))
        if pa > 0.01:      # placeholder slot: shows who is coming up while the intro line plays
            c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x - 390, y - 135, 780, 270), 14, 14), P(GRAY, "stroke", 5, pa, dash=[22, 14]))
            text(c, head, x - 350, y - 8, "sans", 40, GRAY, "l", pa)
        with clip(c, x, y, 780, 270, t, ta, None, rot=(-1.0 if x < 900 else 1.0), seed=100 + int(lid[-1])) as ok:
            if ok:
                text(c, head, -350, -85, "sans", 40, INK, "l")
                for k, ln in enumerate(lines):
                    tl = ta + 0.6 + (k + 0.5)*(E(lid) - S(lid) - 1.0)/len(lines)
                    text(c, ln, -350, -15 + k*52, "sansr" if k else "sans", 42, INK, "l", e_out(prog(t, tl, tl + 0.4)))
                sa_ = E(lid) - 1.4
                text(c, stp, 350, -85, "mono", 38, col, "r", e_out(prog(t, sa_, sa_ + 0.4)))
    stamp(c, "SHAPES THE NEXT PRICES", 960, 215, t, s("5.6") - 0.05, GREEN, -1, 44, pad=(30, 12))

# ================================================================== SEGMENT 6
def seg6(c, t):
    s = S
    a0, b0 = s("6.1") - 0.05, s("6.3") - 0.5
    with ph(c, t, a0, b0, 0.35):
        with clip(c, 960, 380, 1500, 380, t, a0, None, rot=-1, seed=111) as ok:
            if ok:
                text(c, "WILL A DATA CENTER", 0, -75, "serif", 100)
                text(c, "RAISE YOUR BILL?", 0, 55, "serif", 100)
        stamp(c, "NOT AUTOMATICALLY", 960, 700, t, s("6.2") - 0.05, RED, -2, 90, pad=(50, 28))
    a1, b1 = s("6.3") - 0.05, s("6.5") - 0.5
    with ph(c, t, a1, b1, 0.35):
        with clip(c, 520, 440, 760, 640, t, a1, None, rot=-1.2, seed=112) as ok:
            if ok:
                text(c, "1", -330, -260, "mono", 100, RED)
                text(c, "DOES YOUR GRID", 0, -220, "serif", 52)
                text(c, "STILL HAVE ROOM?", 0, -160, "serif", 52)
                p = e_out(prog(t, s("6.3") + 1.6, s("6.3") + 2.2))
                q = e_out(prog(t, Wd("6.3", "If it doesn't"), Wd("6.3", "If it doesn't") + 0.6))
                c.drawRect(skia.Rect.MakeXYWH(-300, -90, 600 * 0.5, 70), P(0xFF8A857C, alpha=p)); c.drawRect(skia.Rect.MakeXYWH(-300, -90, 600, 70), P(INK, "stroke", 4, p))
                text(c, "ROOM  →  prices can fall ↓", 0, 30, "sans", 42, GREEN, alpha=p)
                c.drawRect(skia.Rect.MakeXYWH(-300, 100, 600 * 0.95, 70), P(0xFF8A857C, alpha=q)); c.drawRect(skia.Rect.MakeXYWH(-300, 100, 600, 70), P(INK, "stroke", 4, q))
                text(c, "FULL  →  prices rise ↑", 0, 220, "sans", 42, RED, alpha=q)
        with clip(c, 1400, 440, 760, 640, t, s("6.4") - 0.05, None, rot=1.2, seed=113) as ok:
            if ok:
                text(c, "2", -330, -260, "mono", 100, RED)
                text(c, "WHEN IT ISN'T CHEAP,", 0, -220, "serif", 52)
                text(c, "WHO PAYS?", 0, -160, "serif", 52)
                for k in range(4):
                    house(c, -255 + k*170, 10, 0.78, INK)
                    pk = e_out(prog(t, s("6.4") + 1.2 + k*1.0, s("6.4") + 1.6 + k*1.0))
                    c.drawRect(skia.Rect.MakeXYWH(-300 + k*170, 30, 90, 40), P(RED, alpha=0.25*pk)); c.drawRect(skia.Rect.MakeXYWH(-300 + k*170, 30, 90, 40), P(RED, "stroke", 4, pk))
                text(c, "shared today —", 0, 150, "sans", 44, INK, alpha=e_out(prog(t, Wd("6.4", "a lot of that") - 0.2, Wd("6.4", "a lot of that") + 0.4)))
                text(c, "the rules decide if it stays", 0, 205, "sans", 44, RED, alpha=e_out(prog(t, Wd("6.4", "rules being") - 0.2, Wd("6.4", "rules being") + 0.4)))
    a2 = s("6.5") - 0.05
    with ph(c, t, a2, None, 0.35):
        with clip(c, 960, 360, 1560, 420, t, a2, None, rot=-1, seed=114) as ok:
            if ok:
                text(c, "Is a data center being built near you —", 0, -85, "serif", 64)
                text(c, "and has your electric bill changed?", 0, 5, "serif", 64)
                text(c, "TELL ME IN THE COMMENTS", 0, 115, "sans", 52, RED, spacing=4)
        for i in range(3):
            house(c, 660 + i*300, 830, 1.0, INK)
        building(c, 1560, 830, 0.62, INK)
        pen_line(c, 520, 507, 1400, 507, prog(t, Wd("6.5", "Tell me") - 0.3, Wd("6.5", "Tell me") + 0.9), RED, 9, 1.0, 5)
        for i in range(3):
            fq = Wd("6.5", "has your") + i*0.5
            ftext(c, "?", 660 + i*300, 650, t, fq, "mono", 90, RED)

REG = {4: (cam, seg4, None), 5: (cam, seg5, None), 6: (cam, seg6, None)}
