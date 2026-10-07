# Test report: "Ask the AI twice, check where the answers split"

**Claim being tested:** if you ask an AI the same question twice, the details that differ between answers are more likely to be wrong than the details that match.

**Verdict: the claim holds in this test.** Of the 7 details where the runs disagreed, 6 contained at least one wrong value. Of the 41 details where the runs agreed, 2 were wrong. Agreement is not a guarantee (see the Palm Foleo price and RAM), but disagreement was a strong warning sign.

## Method

- Tool: Claude Code CLI `claude -p "<question>"`, version 2.1.292, run on 2026-10-07 (UTC).
- Each question was run 3 times. Each run is a separate process and a fresh session, started from an empty temp directory, with stdin closed (`< /dev/null`). Exact script: [`test_log/run_tests.sh`](test_log/run_tests.sh). Raw outputs: `test_log/Q<n>_run<k>.txt` (unedited).
- No web search happened during the runs. Several runs say so themselves ("I'm answering from memory").
- **A first attempt was thrown away.** In version 1 of the script, `claude -p` read the question file from stdin, so every run got all four questions at once. Those outputs are kept for transparency in `test_log/invalid_first_attempt/` and are **not** used anywhere in this report or the video.
- Verification: done with web search on 2026-10-07. Wikipedia, Olympedia and several news sites were blocked by this environment's network proxy, so I used the sources the search tool could reach. Each source is linked below.

### How details were counted

- A **detail** is a specific fact (date, number, name, place) that at least 2 of the 3 runs stated.
- **Consistent** = every run that stated it gave the same value.
- **Split** = runs gave different values for the same thing.
- Facts stated in only 1 run are listed separately as "single-run details". They are verified but kept out of the main count, because there is nothing to compare them with.
- ✓ = right, ✗ = wrong, ~ = unclear / partly right, ? = I could not confirm it from a reachable source (excluded from the count).

## Questions

| ID | Question (exact text sent) |
|---|---|
| Q1 | Who was Jan Ernst Matzeliger? Give me 5 key facts with dates and numbers, as short bullet points. |
| Q2 | Tell me about the Palm Foleo: when was it announced, what was the price, when was it cancelled, and what were its key specs? Short bullet points. |
| Q3 | What happened in the 1904 Olympic marathon? Give me 5 key facts with names, times and numbers, as short bullet points. |
| Q4 | Who was Elizabeth Magie and what did she invent? Give me 5 key facts with dates and numbers, as short bullet points. |

---

## Q1: Jan Ernst Matzeliger

### Consistent details

| Detail | Run 1 | Run 2 | Run 3 | Check |
|---|---|---|---|---|
| Born 15 Sept 1852, Paramaribo, Dutch Guiana | same | same | same | ✓ [biography.com](https://www.biography.com/inventors/jan-matzeliger), [MIT Lemelson](https://lemelson.mit.edu/resources/jan-matzlieger) |
| Father a Dutch engineer, mother Surinamese | same | same | same | ✓ [biography.com](https://www.biography.com/inventors/jan-matzeliger). (All 3 runs add "enslaved"; I did not find that word in a reachable source, so only the core fact is counted.) |
| Lasting machine patent, 20 Mar 1883, US No. 274,207 | same | same | same | ✓ [madehow.com](https://www.madehow.com/inventorbios/44/Jan-Ernst-Matzeliger.html) |
| 150–700 pairs a day vs ~50 by hand | same | same | same | ✓ [Invention & Technology](https://www.inventionandtech.com/node/86844) |
| Died 24 Aug 1889, tuberculosis, age 36 | same | same | same | ✓ [biography.com](https://www.biography.com/inventors/jan-matzeliger) |
| US stamp in 1991 | same | same | same | ✓ [Mystic Stamp, Scott 2567](https://www.mysticstamp.com/2567-1991-29c-black-heritage-jan-e-matzeliger/) (issued 15 Sept 1991) |

### Split details

| Detail | Run 1 | Run 2 | Run 3 | Truth | Check |
|---|---|---|---|---|---|
| When he came to the US | "Emigrated to the U.S. in 1876 at age 24" ✗ | "Arrived in Philadelphia in 1876 at about age 24" ✗ | "Reached Philadelphia in 1871 at about age 19" ✗ | Left Suriname at 19 (1871) as a sailor; settled in Philadelphia in **1873**; moved to Lynn in 1877 | [biography.com](https://www.biography.com/inventors/jan-matzeliger), [ETHW](https://ethw.org/Jan_Matzeliger) |
| Who got his patents | "United Shoe Machinery Company later acquired his patents" ✓ | "His patents were largely sold to the United Shoe Machinery Company" ~ | "Consolidated Lasting Machine Company bought most of his patents" ✓ | He got stock in the Consolidated Lasting Machine Co. (formed 1889); United Shoe Machinery acquired the patent after his death | [madehow.com](https://www.madehow.com/inventorbios/44/Jan-Ernst-Matzeliger.html) |

Note on the first split: 2 of 3 runs agreed on 1876, and 1876 is still wrong. Majority vote would not have saved you here. The split is what pointed at the problem.

The second split is counted as **unclear**, not wrong: run 2's wording blurs who sold to whom, but it is not clearly false.

### Single-run details

- Moved to Lynn in 1877 (run 3) ✓ [biography.com](https://www.biography.com/inventors/jan-matzeliger)
- About 6 years of work on the machine (run 2) ? (1877 to 1883 fits, but no source states it)
- Worked for about $1.50 a day (run 3) ? (the source I found says $9 a week, [biography.com](https://www.biography.com/inventors/jan-matzeliger))
- Machine cut shoe prices roughly in half (run 2) ✓ [Lemelson](https://lemelson.mit.edu/resources/jan-matzlieger)

---

## Q2: Palm Foleo

### Consistent details

| Detail | Run 1 | Run 2 | Run 3 | Check |
|---|---|---|---|---|
| Announced 30 May 2007 | same | same | same | ✓ [Engadget](https://www.engadget.com/2007-05-30-palm-foleo-announced.html) |
| **Price: "$499, $399 after a $100 mail-in rebate"** | same | same | same | **✗** It was **$499 after** the $100 rebate (i.e. $599 before). [Engadget](https://www.engadget.com/2007-05-30-palm-foleo-announced.html), [Wikipedia via search](https://en.wikipedia.org/wiki/Palm_Foleo) |
| Cancelled 4 Sept 2007 | same | same | same | ✓ [Phone Scoop](https://www.phonescoop.com/articles/article.php?a=2371), [Fortune](https://fortune.com/2007/09/04/palm-cancels-ill-advised-foleo-will-take-multi-million-dollar-charge) |
| Reason: refocus on a new smartphone platform | same | same | same | ✓ [Phone Scoop](https://www.phonescoop.com/articles/article.php?a=2371) |
| 10.2" display, 1024×600 | same | same | same | ✓ [OSnews](https://www.osnews.com/story/18001/palm-unveils-palm-foleo/) |
| Linux-based OS | same | same | same | ✓ [OSnews](https://www.osnews.com/story/18001/palm-unveils-palm-foleo/) |
| **RAM: 256 MB** | same | same | same | **✗** It had **128 MB** RAM. [Wikipedia via search](https://en.wikipedia.org/wiki/Palm_Foleo), [Pen Computing](https://www.pencomputing.com/palm/penreviews/hardware_palm_foleo.html) |
| Wi-Fi and Bluetooth | same | same | same | ✓ [OSnews](https://www.osnews.com/story/18001/palm-unveils-palm-foleo/) |
| Instant-on | same | same | same | ✓ [OSnews](https://www.osnews.com/story/18001/palm-unveils-palm-foleo/) |
| Office document viewer/editor | same | same | same | ✓ (Documents To Go) [OSnews](https://www.osnews.com/story/18001/palm-unveils-palm-foleo/) |
| Opera-based browser | Opera | "web browser" | Opera | ✓ [OSnews](https://www.osnews.com/story/18001/palm-unveils-palm-foleo/) |
| About 5 hours battery | 5 h | (not stated) | 5 h | ✓ [Engadget](https://www.engadget.com/2007-05-30-palm-foleo-announced.html) |
| Announced by Jeff Hawkins and Ed Colligan | same | same | same | ? Hawkins confirmed ([Engadget](https://www.engadget.com/2007-05-30-palms-jeff-hawkins-live-from-d-2007.html)); Colligan's on-stage role not confirmed. Excluded. |
| SD card slot | same | same | same | ? Not confirmed from a reachable source. Excluded. |

### Split details

| Detail | Run 1 | Run 2 | Run 3 | Truth | Check |
|---|---|---|---|---|---|
| Flash storage | 512 MB ✗ | 1.0 GB ✗ | 512 MB ✗ | **256 MB** | [Wikipedia via search](https://en.wikipedia.org/wiki/Palm_Foleo), [OSnews](https://www.osnews.com/story/18001/palm-unveils-palm-foleo/) |
| Processor | "Around 1 GHz-class ARM" ✗ | "Marvell PXA270, 312 MHz" ✗ | (not stated) | **Intel PXA27x, 416 MHz** | [Wikipedia via search](https://en.wikipedia.org/wiki/Palm_Foleo) |
| Weight | "about 2.5 lb (1.1 kg)" ✓ | "Under 3 pounds (about 1.36 kg)" ✗ | "1.0 lb (about 2.5 lb with the battery)" ✗ | **2.5 lb** (1.13 kg) | [The Register](https://www.theregister.com/2007/05/30/palm_announces_foleo/), [InformationWeek](https://www.informationweek.com/mobile/palm-adds-the-folly-er-the-foleo-to-its-portfolio) |

### Single-run details

- Meant to ship in Q3 2007 (run 2) ✓ [Wikipedia via search](https://en.wikipedia.org/wiki/Palm_Foleo)
- Colligan announced the cancellation in a blog post (run 2) ✓ [Phone Scoop](https://www.phonescoop.com/articles/article.php?a=2371)
- USB ports (runs 1, 2) ? not confirmed, excluded

Q2 is the warning case for this tip: two details were wrong in all three runs (price, RAM). Agreement lowered the error rate a lot, but it did not remove it.

---

## Q3: 1904 Olympic marathon

### Consistent details

| Detail | Run 1 | Run 2 | Run 3 | Check |
|---|---|---|---|---|
| 30 Aug 1904, St. Louis | same | same | same | ✓ [olympicgamesmarathon.com](https://olympicgamesmarathon.com/olympiad1904.php) |
| About 90°F (32°C) heat | same | same | (not stated) | ✓ [The Collector](https://www.thecollector.com/1904-olympic-marathon-disaster/) |
| Thomas Hicks won in 3:28:53 | same | same | same | ✓ [olympicgamesmarathon.com](https://olympicgamesmarathon.com/olympiad1904.php) (one popular article says 3:28:45; the Olympic record is 3:28:53) |
| Hicks was born in England | "British-born" | "English-born" | (not stated) | ✓ born in Birmingham, England, [Google Arts & Culture](https://artsandculture.google.com/entity/m03ddn8) |
| Hicks given strychnine, egg whites and brandy | same | same | same | ✓ [The Collector](https://www.thecollector.com/1904-olympic-marathon-disaster/) |
| Hicks near collapse at the end | same | same | same | ✓ [The Collector](https://www.thecollector.com/1904-olympic-marathon-disaster/) |
| Fred Lorz crossed first after ~11 miles in a car | same | same | same | ✓ [Populous](https://populous.com/article/the-bizarre-tale-of-the-1904-st-louis-marathon) |
| Lorz banned, ban later lifted | same | same | same | ✓ [Jalopnik](https://jalopnik.com/5928842/the-first-winner-of-the-1904-olympic-marathon-used-a-car-the-second-winner-used-drugs-and-booze) |
| Lorz won the 1905 Boston Marathon | same | (not stated) | same | ✓ [The Olympians](https://theolympians.co/tag/fred-lorz/) |
| Carvajal (Cuban postman) finished 4th, ate rotten apples | same | same | same | ✓ [Today I Found Out](https://www.todayifoundout.com/?p=46424) |
| Carvajal ran in street clothes | (not stated) | same | same | ✓ [Today I Found Out](https://www.todayifoundout.com/?p=46424) |
| Len Tau (Taunyane) and Jan Mashiani, Tswana runners; Tau 9th | same | same | same | ✓ [Running Magazine](https://runningmagazine.ca/?p=68422) |
| Tau chased off course by dog(s) | same | same | same | ✓ [Running Magazine](https://runningmagazine.ca/?p=68422) |
| First Black Africans at the Olympics | same | (not stated) | same | ✓ [Running Magazine](https://runningmagazine.ca/?p=68422) |

### Split details

| Detail | Run 1 | Run 2 | Run 3 | Truth | Check |
|---|---|---|---|---|---|
| Starters and finishers | "Only 14 of the 32 starters finished" ✓ | "Only 32 of the 69 starters finished" ✗ | "Only 14 of the 32 starters finished" ✓ | 32 starters, **14 finished** | [Running Magazine](https://runningmagazine.ca/?p=68422), [olympicgamesmarathon.com](https://olympicgamesmarathon.com/olympiad1904.php) |

### Single-run details (all run 2)

- One water station, at about 12 miles ✓ [Today I Found Out](https://www.todayifoundout.com/?p=46424)
- Lorz crossed in 3:13 ✓ [Populous](https://populous.com/article/the-bizarre-tale-of-the-1904-st-louis-marathon)
- Mashiani finished 12th ✓ [Running Magazine](https://runningmagazine.ca/?p=68422)
- William Garcia collapsed from inhaling dust ✓ [Today I Found Out](https://www.todayifoundout.com/?p=46424)

**Q3 is the cleanest result:** 14 consistent details, all right. 1 split detail, and the odd one out was wrong.

---

## Q4: Elizabeth Magie

### Consistent details

| Detail | Run 1 | Run 2 | Run 3 | Check |
|---|---|---|---|---|
| Born 1866, Macomb, Illinois | same | same | same | ✓ [Find a Grave](https://findagrave.com/memorial/100848078/lizzie-magie) |
| Worked as stenographer and typist | same | same | same | ✓ [Women's Activism NYC](https://www.womensactivism.nyc/stories/5125) |
| Georgist / Henry George ideas | same | same | same | ✓ [Public Domain Review](https://publicdomainreview.org/collection/the-landlords-game) |
| The Landlord's Game, US Patent 748,626, 1904 | same | same | same | ✓ [Public Domain Review](https://publicdomainreview.org/collection/the-landlords-game) |
| Patent issued 5 Jan 1904 | same | (year only) | same | ✓ [Public Domain Review](https://publicdomainreview.org/collection/the-landlords-game) |
| Two rule sets (monopolist / anti-monopolist) | same | same | same | ✓ [History.com](https://www.history.com/articles/monopoly-game-inventor-elizabeth-magie) |
| 1935: Darrow sold Monopoly to Parker Brothers | same | same | same | ✓ [History.com](https://www.history.com/articles/monopoly-game-inventor-elizabeth-magie) |
| Parker Brothers paid her $500, no royalties | same | same | same | ✓ [Inventors Digest](https://www.inventorsdigest.com/articles/whose-monopoly-anyway/) |
| Died 1948 | same | same | same | ✓ [Find a Grave](https://findagrave.com/memorial/100848078/lizzie-magie) |
| Her role surfaced in the 1970s (Anti-Monopoly case) | same | same | same | ✓ [NPR](https://www.npr.org/transcripts/382662772) |

### Split details

| Detail | Run 1 | Run 2 | Run 3 | Truth | Check |
|---|---|---|---|---|---|
| Which patent Parker Brothers bought | "Magie's 1904 patent" ✗ | "Magie's 1924 patent" ✓ | "Magie's patent" (no year) | The **1924** patent (No. 1,509,312). The 1904 patent had already expired. | [Loyola IP Bytes](https://blogs.luc.edu/ipbytes/?p=4924), [landlordsgame.info](https://landlordsgame.info/games/lg-1924/lg-1924.html) |

### Single-run details

- Born 9 May (run 1) ✓, died 2 March 1948 (run 1) ✓ [Find a Grave](https://findagrave.com/memorial/100848078/lizzie-magie)
- "1923: She won a second patent" (run 2) ✗ she applied in 1923; it was issued 23 Sept 1924. [Loyola IP Bytes](https://blogs.luc.edu/ipbytes/?p=4924). (Run 2 also contradicts itself, calling it the 1924 patent two lines later.)
- Also a writer, actress and comedian (run 3) ✓ [Women's Activism NYC](https://www.womensactivism.nyc/stories/5125)
- Ralph Anspach's Anti-Monopoly fight, 1973 (run 3) ✓ [NPR](https://www.npr.org/transcripts/382662772)
- Mary Pilon's 2015 book *The Monopolists* (run 1) ✓ [Longreads](https://longreads.com/2015/03/12/the-twisted-history-of-your-favorite-board-game-2/)

---

## Totals

| | Consistent details | Split details |
|---|---|---|
| Q1 Matzeliger | 6 (0 wrong) | 2 (1 with errors, 1 unclear) |
| Q2 Palm Foleo | 12 (2 wrong) | 3 (3 with errors) |
| Q3 1904 marathon | 14 (0 wrong) | 1 (1 with an error) |
| Q4 Magie | 10 (0 wrong) | 1 (1 with an error) |
| **All** | **42 details, 2 wrong (5%)** | **7 details, 6 had an error (86%), 1 unclear** |

Counting individual stated values inside the split details: 19 values were stated, 12 were wrong, 6 right, 1 unclear.

**Conclusion:** the tip holds. Where the answers split, something was wrong 6 times out of 7. Where they matched, something was wrong 2 times out of 42. Two cautions belong with the tip:

1. Matching answers can still both be wrong (Foleo price and RAM).
2. Majority vote is not a fix: in Q1, two runs agreed on 1876 and were both wrong.

So the tip is "check the splits first", not "trust whatever matches".

## Question picked for the video: Q3

Q3 is the clearest: everything that matched was right, and the only split was wrong. The video shows Run 1 and Run 2, because those are the two runs that disagree (Run 3 agreed with Run 1).

Every word on screen and where it comes from:

| On screen | Source |
|---|---|
| "What happened in the 1904 Olympic marathon?" | Q3 prompt (first sentence, unchanged) |
| "Aug 30, 1904" | Run 1: "Held August 30, 1904"; Run 2: "Held August 30, 1904" |
| "Hicks won · 3:28:53" | Run 1 and Run 2: "won in 3:28:53" |
| "strychnine + brandy" | Run 1: "strychnine mixed with brandy and egg whites"; Run 2: "strychnine mixed with egg white and brandy" |
| "Lorz rode a car ~11 mi" | Run 1: "after riding about 11 miles in a car"; Run 2: "ridden about 11 miles in a car" |
| "Carvajal 4th" | Run 1: "still finished 4th"; Run 2: "he finished 4th" |
| "14 of 32 finished" ✓ right | Run 1: "Only 14 of the 32 starters finished"; verified above |
| "32 of 69 finished" ✗ wrong | Run 2: "Only 32 of the 69 starters finished"; verified above |
| "real test · Claude · 3 runs" | This report |

---

## Raw outputs

Copied unedited from `test_log/`. The first 3 lines of each file are the header written by the script (command and start time).

### Q1 · Run 1 (`test_log/Q1_run1.txt`)

````text
# command: claude -p "Who was Jan Ernst Matzeliger? Give me 5 key facts with dates and numbers, as short bullet points."
# started: 2026-10-07T06:29:27Z
# ---- raw output below ----
**Jan Ernst Matzeliger** was an inventor whose machine transformed shoemaking.

- **Born September 15, 1852**, in Paramaribo, Dutch Guiana (now Suriname), to a Dutch engineer father and an enslaved Surinamese mother.
- **Emigrated to the U.S. in 1876** at age 24. He settled in Lynn, Massachusetts, a major shoemaking center, and worked in a shoe factory.
- **Lasting machine, patented March 20, 1883** (U.S. Patent No. 274,207). It attached the upper part of a shoe to the sole automatically.
- **Output jumped from about 50 pairs a day by hand to 150–700 pairs a day** by machine. This cut shoe costs sharply.
- **Died of tuberculosis on August 24, 1889**, at age 36. The United Shoe Machinery Company later acquired his patents. The U.S. Postal Service honored him with a stamp in 1991.
````

### Q1 · Run 2 (`test_log/Q1_run2.txt`)

````text
# command: claude -p "Who was Jan Ernst Matzeliger? Give me 5 key facts with dates and numbers, as short bullet points."
# started: 2026-10-07T06:29:27Z
# ---- raw output below ----
- **Born:** September 15, 1852, in Paramaribo, Dutch Guiana (now Suriname), to a Dutch engineer father and an enslaved Surinamese mother.
- **Emigrated:** Arrived in Philadelphia in 1876 at about age 24, after working as a sailor, and later settled in Lynn, Massachusetts, a shoemaking hub.
- **Invention:** Patented his shoe-lasting machine on March 20, 1883 (U.S. Patent No. 274,207), after about 6 years of work. It attached the upper part of a shoe to the sole mechanically.
- **Impact:** The machine could produce 150 to 700 pairs of shoes a day. A hand laster managed about 50, and the machine cut shoe prices roughly in half.
- **Death:** Died of tuberculosis on August 24, 1889, at age 36. His patents were largely sold to the United Shoe Machinery Company, and he was honored with a U.S. postage stamp in 1991.
````

### Q1 · Run 3 (`test_log/Q1_run3.txt`)

````text
# command: claude -p "Who was Jan Ernst Matzeliger? Give me 5 key facts with dates and numbers, as short bullet points."
# started: 2026-10-07T06:29:27Z
# ---- raw output below ----
- **Born:** September 15, 1852, in Paramaribo, Dutch Guiana (now Suriname), to a Dutch engineer father and an enslaved Surinamese mother.
- **Emigrated:** Reached Philadelphia in 1871 at about age 19, after working as a sailor and learning machine work in Suriname from age 10.
- **Settled in Lynn, Massachusetts:** Moved there in 1877 and worked in shoe factories for about $1.50 a day. He taught himself English and studied physics.
- **Invention:** Patented his shoe-lasting machine on March 20, 1883 (U.S. Patent No. 274,207). It attached the upper part of a shoe to the sole and could produce 150 to 700 pairs a day, against about 50 by hand. The machine cut shoe prices and helped make mass production possible.
- **Death:** Died of tuberculosis on August 24, 1889, aged 36. The Consolidated Lasting Machine Company bought most of his patents, and its shares, which were worth a lot, went to his estate. The U.S. Postal Service issued a stamp in his honor in 1991.
````

### Q2 · Run 1 (`test_log/Q2_run1.txt`)

````text
# command: claude -p "Tell me about the Palm Foleo: when was it announced, what was the price, when was it cancelled, and what were its key specs? Short bullet points."
# started: 2026-10-07T06:29:27Z
# ---- raw output below ----
**Palm Foleo** (a "mobile companion" subnotebook for smartphones)

- **Announced:** May 30, 2007, by Palm (Jeff Hawkins and Palm's then-CEO Ed Colligan presented it).
- **Price:** $499 list, with a $100 mail-in rebate bringing it to about $399.
- **Cancelled:** Palm announced the cancellation on September 4, 2007, before it shipped. It had been expected to launch in late summer or fall 2007. Palm said it would refocus on a new smartphone platform, which became webOS and the Palm Pre.
- **Key specs:**
  - 10.2" display, 1024×600
  - Linux-based OS
  - Around 1 GHz-class ARM processor
  - 256 MB RAM, 512 MB flash storage, with no hard drive
  - SD/MMC slot and USB ports
  - Wi-Fi and Bluetooth
  - Instant-on, with about 5 hours of battery life and a weight of about 2.5 lb (1.1 kg)
  - Bundled apps: Opera-based browser, email client, and viewers/editors for Microsoft Office documents
  - Designed to sync with a Treo or other smartphone, using the phone's data connection

I'm answering from memory, so the exact processor and battery figures are the least certain. I can verify them with a search if you want.
````

### Q2 · Run 2 (`test_log/Q2_run2.txt`)

````text
# command: claude -p "Tell me about the Palm Foleo: when was it announced, what was the price, when was it cancelled, and what were its key specs? Short bullet points."
# started: 2026-10-07T06:29:27Z
# ---- raw output below ----
**Palm Foleo** (a "mobile companion" subnotebook for smartphones)

- **Announced:** May 30, 2007, by Palm co-founder Jeff Hawkins and Palm CEO Ed Colligan.
- **Price:** $499 US, with a $100 mail-in rebate that brought it to about $399. It was meant to ship in Q3 2007.
- **Cancelled:** September 4, 2007. Palm said it would drop the Foleo to focus on a unified smartphone platform. Colligan announced the cancellation in a blog post.
- **Key specs:**
  - 10.2-inch display, 1024×600
  - Linux-based OS
  - 1.0 GB flash storage with an SD card slot, and no hard drive
  - ARM-based processor (Marvell PXA270, 312 MHz)
  - 256 MB RAM
  - Wi-Fi and Bluetooth
  - USB ports
  - Under 3 pounds (about 1.36 kg)
  - Instant-on boot
  - Included a web browser, email client and document viewer/editor (Microsoft Office-compatible). It was designed to sync with Palm Treo smartphones, including email.
- **Why it flopped:** Critics questioned why anyone would need a device that depended on a smartphone. It also arrived just before the netbook wave, which offered more capability at similar prices.

These figures come from my own knowledge, not a fresh lookup, so verify the dates and specs if you need them to be exact.
````

### Q2 · Run 3 (`test_log/Q2_run3.txt`)

````text
# command: claude -p "Tell me about the Palm Foleo: when was it announced, what was the price, when was it cancelled, and what were its key specs? Short bullet points."
# started: 2026-10-07T06:29:27Z
# ---- raw output below ----
**Palm Foleo** (from memory)

- **Announced:** May 30, 2007, by Palm co-founder Jeff Hawkins and Palm's CEO Ed Colligan. It was billed as a "mobile companion" for smartphones, not a standalone laptop.
- **Price:** $499 list, with a $100 mail-in rebate that brought it to $399.
- **Cancelled:** September 4, 2007, before it shipped. Colligan said Palm would refocus on a new smartphone platform. That platform later became webOS.
- **Key specs:**
  - 10.2" screen at 1024×600
  - 1.0 lb (about 2.5 lb with the battery), very thin
  - Linux-based OS
  - 256 MB RAM and 512 MB flash storage, with an SD card slot
  - Wi-Fi and Bluetooth, with no built-in cellular radio. It was meant to use a paired phone's connection.
  - Full-size keyboard
  - Instant-on, with a battery rated at roughly 5 hours
  - Included Opera-based browser, email client that synced with Treo/Palm smartphones, and viewers/editors for Office documents
  - Planned as a smartphone companion before the "netbook" category existed

I'm giving this from memory and didn't verify it with a search. The exact spec figures, such as RAM, flash and battery life, are the ones most worth double-checking.
````

### Q3 · Run 1 (`test_log/Q3_run1.txt`)

````text
# command: claude -p "What happened in the 1904 Olympic marathon? Give me 5 key facts with names, times and numbers, as short bullet points."
# started: 2026-10-07T06:29:27Z
# ---- raw output below ----
- **Date and place:** Held August 30, 1904, in St. Louis, Missouri, as part of the World's Fair games, in about 90°F (32°C) heat. Only 14 of the 32 starters finished.
- **Winner:** Thomas Hicks, a British-born American, won in 3:28:53. He was given strychnine mixed with brandy and egg whites during the race, and he nearly collapsed at the finish.
- **Fred Lorz:** The American crossed the line first, after riding about 11 miles in a car when he cramped. He was exposed as a fraud before receiving the medal and was banned, though later allowed back, and he won the 1905 Boston Marathon.
- **Andarín Carvajal:** The Cuban postman raised money for the trip by running in the streets of Havana. He stopped to eat apples along the way, which turned out to be rotten, and still finished 4th.
- **Tswana runners:** Len Tau and Jan Mashiani, the first Black Africans to compete at the Olympics, ran in the race. Tau finished 9th, and he was reportedly chased off the course by dogs.
````

### Q3 · Run 2 (`test_log/Q3_run2.txt`)

````text
# command: claude -p "What happened in the 1904 Olympic marathon? Give me 5 key facts with names, times and numbers, as short bullet points."
# started: 2026-10-07T06:29:27Z
# ---- raw output below ----
- **Date and place:** Held August 30, 1904, at the St. Louis Games, in sweltering heat (about 90°F/32°C) on dusty roads. Only 32 of the 69 starters finished, and the course had just one water station, at about the 12-mile mark.
- **Winner:** Thomas Hicks, an English-born American, won in 3:28:53. He was helped by his trainers, who gave him strychnine mixed with egg white and brandy during the race. He was close to collapse at the finish.
- **First across the line:** Fred Lorz, an American, crossed first in 3:13. He had dropped out around mile 9 with cramps and ridden about 11 miles in a car before the car broke down. He then ran the rest of the way. He admitted the ruse soon after and was banned, though the ban was lifted later.
- **Africans in the race:** Len Taunyane and Jan Mashiani, two Tswana runners from South Africa, finished 9th and 12th. They were in St. Louis for the Boer War exhibit at the World's Fair. Taunyane lost time when a dog chased him off course.
- **Other mishaps:** Cuban runner Félix Carvajal, who had arrived at the Games with little money, ran in street clothes with his trousers cut into shorts, and he finished 4th. He stopped to eat apples from an orchard, which gave him stomach cramps, and then lay down for a nap. Another runner, William Garcia, collapsed with internal bleeding from breathing in dust.
````

### Q3 · Run 3 (`test_log/Q3_run3.txt`)

````text
# command: claude -p "What happened in the 1904 Olympic marathon? Give me 5 key facts with names, times and numbers, as short bullet points."
# started: 2026-10-07T06:29:27Z
# ---- raw output below ----
- **Winner:** Thomas Hicks (USA) won in 3:28:53 on August 30, 1904, in St. Louis, but only after being propped up by his trainers.
- **Drugs:** Hicks was given strychnine mixed with egg whites and brandy during the race. He collapsed shortly after finishing and nearly died.
- **Disqualification:** Fred Lorz (USA) crossed the line first, having ridden about 11 miles in a car after cramping up. He was disqualified and later banned, though the ban was lifted and he won the 1905 Boston Marathon.
- **Small, odd field:** Only 14 of the 32 starters finished, and the field was largely American. Cuban Félix Carvajal, who had run to the race and arrived in street clothes, finished fourth after stopping to eat apples (which turned out to be rotten).
- **Africans' debut:** Tswana runners Len Tau and Jan Mashiani, there as part of the World's Fair exhibits, were the first black Africans in the Olympics. Tau finished ninth after being chased off course by dogs.
````

### Q4 · Run 1 (`test_log/Q4_run1.txt`)

````text
# command: claude -p "Who was Elizabeth Magie and what did she invent? Give me 5 key facts with dates and numbers, as short bullet points."
# started: 2026-10-07T06:29:27Z
# ---- raw output below ----
**Elizabeth Magie (1866–1948)** was an American game designer, writer, and Georgist (a follower of economist Henry George's land-tax ideas). She invented the game that became Monopoly.

- **1866:** Born in Macomb, Illinois, on May 9. She later worked as a stenographer and typist and wrote poetry and short stories.
- **1904:** Patented "The Landlord's Game" (U.S. Patent No. 748,626, issued January 5, 1904). It was meant to show how land monopolies enrich landlords and impoverish tenants.
- **Two rule sets:** Her game had an anti-monopolist version, where wealth was shared, and a monopolist version, where players won by bankrupting opponents. The second version is the one most people know today.
- **1935:** Parker Brothers bought Charles Darrow's version, Monopoly, which was based on her game. Darrow was long credited as the sole inventor and became a millionaire. Parker Brothers also bought Magie's 1904 patent for just **$500** and paid her no royalties.
- **1948:** She died on March 2, largely unrecognized. Her role was only widely acknowledged after the 1970s Anti-Monopoly trademark lawsuit and later research, including Mary Pilon's 2015 book *The Monopolists*.
````

### Q4 · Run 2 (`test_log/Q4_run2.txt`)

````text
# command: claude -p "Who was Elizabeth Magie and what did she invent? Give me 5 key facts with dates and numbers, as short bullet points."
# started: 2026-10-07T06:29:27Z
# ---- raw output below ----
**Elizabeth Magie (1866–1948)** was an American game designer, writer, and Georgist activist. She invented the game that became Monopoly.

- **Born 1866** in Macomb, Illinois. She worked as a stenographer and typist, and also wrote poetry and short stories.
- **1904:** She received US Patent 748,626 for "The Landlord's Game." It was designed to show how land monopolies enrich landlords and impoverish tenants, based on Henry George's single-tax ideas.
- **Two rule sets:** The game had an anti-monopolist rule set, where wealth was shared, and a monopolist one, where players tried to bankrupt each other. She wanted players to see why the first was fairer.
- **1923:** She won a second patent for an updated version. The game spread by hand-copied boards, notably among Quaker communities and college students in the 1910s–30s, picking up names like Atlantic City street names along the way.
- **1935:** Charles Darrow sold his version, "Monopoly," to Parker Brothers and was credited as its inventor. Parker Brothers bought Magie's 1924 patent for just **$500**, with no royalties. She died in 1948, largely unrecognized, and her role was only widely documented from the 1970s onward.
````

### Q4 · Run 3 (`test_log/Q4_run3.txt`)

````text
# command: claude -p "Who was Elizabeth Magie and what did she invent? Give me 5 key facts with dates and numbers, as short bullet points."
# started: 2026-10-07T06:29:27Z
# ---- raw output below ----
**Elizabeth Magie (1866–1948)** was an American game designer, writer, and Georgist (a follower of economist Henry George). She invented the game that became Monopoly.

- **Born 1866** in Macomb, Illinois. She worked as a stenographer and typist, and was also a writer, actress, and comedian.
- **Patented "The Landlord's Game" on January 5, 1904** (U.S. Patent No. 748,626). She designed it to show how land monopolies enrich landlords and impoverish tenants.
- **Two rule sets:** An "anti-monopolist" version rewarded shared prosperity. A "monopolist" version rewarded driving opponents bankrupt. Her aim was to show that the first system was fairer.
- **1935: Charles Darrow sold his version to Parker Brothers** as "Monopoly," after learning the game from players of Magie's earlier design. He was long credited as the sole inventor. Parker Brothers bought Magie's patent for just **$500** and paid her no royalties.
- **Recognition came late.** She died in **1948**, still largely unknown. In 1973, economics professor Ralph Anspach's legal fight over his game "Anti-Monopoly" uncovered her role, and her contribution has been recognized more widely since then.
````

