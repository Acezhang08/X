# Test report: do AI's own [guess] labels flag its mistakes?

**Claim tested:** when an AI marks its own statements [sourced] or [guess], the [guess] ones are wrong much more often than the [sourced] ones.

**Verdict: no image made.** The gap looks big (see below), but it rests on 3 wrong [guess] claims, all from one question. See "Judgment".

## Method

- Tool: `claude -p "<question> <suffix>" < /dev/null`, each run from a fresh empty temp directory (Claude Code 2.1.294, default model, no tools used by the model: it said it answered from memory).
- Suffix, used word for word after every question: `For every specific claim, add [sourced] if you are confident it is well documented, or [guess] if you are not sure.`
- 5 detail-heavy, lesser-known history questions (names, dates, numbers). 2 runs each = 10 raw outputs, saved untouched in `test_log/` (`q1_run1.txt` ... `q5_run2.txt`).
- Each labelled concrete claim was split out and checked against web sources. Verdicts: **right (T)**, **wrong (F)**, **cannot confirm (U)**. U is left out of all error rates.
- Left out as not checkable: vague or opinion lines (for example "exact cause is still debated"), and headings.
- Lines with two parts (for example "born in X, in 1850") were split only when the parts got different verdicts; otherwise kept as one claim.

### Limits you should know

- My page-fetch tool could not reach any website (DNS error), and direct curl was blocked. So I checked claims with **web search result summaries only**, then cited the pages those searches returned. I could not open the full pages myself.
- Because of that, many true-but-unlisted facts came back as **cannot confirm** (U): 13 of 34 [guess] claims and 87 of 223 [sourced] claims. That is about the same share for both tags (38% vs 39%), so it should not skew the comparison, but it shrinks the sample a lot.
- Where sources disagreed (tank size, witness counts), the claim was marked U, not T or F.
- Search summaries can be wrong. Treat each row as a good check, not a court ruling.

## Summary

| Label | Claims | Checked (T+F) | Wrong | Wrong rate | Cannot confirm |
|---|---|---|---|---|---|
| [guess] | 34 | 21 | 3 | 14.3% | 13 |
| [sourced] | 223 | 136 | 2 | 1.5% | 87 |

Fisher exact test (wrong vs right, [guess] vs [sourced]): p = 0.017.

### By question

| Question | [guess] checked | [guess] wrong | [sourced] checked | [sourced] wrong |
|---|---|---|---|---|
| Q1 R101 airship crash (1930) | 3 | 0 | 27 | 0 |
| Q2 Great Molasses Flood (Boston, 1919) | 2 | 0 | 32 | 2 |
| Q3 Eddystone Lighthouse: the four towers | 5 | 0 | 26 | 0 |
| Q4 Voynich manuscript: owners and dating | 0 | 0 | 24 | 0 |
| Q5 Clipper ship Cutty Sark | 11 | 3 | 27 | 0 |

### Surprises (kept in, not hidden)

- **Two [sourced] claims were wrong**, both in Q2 run 2: the case name ("Dorothy Ann Kelley et al. v. United States Industrial Alcohol"; the lead case was *Dorr v. USIA*) and "about 3,000 pages of testimony" (sources say 25,000 to 45,000 pages).
- **All 3 wrong [guess] claims came from Q5 (Cutty Sark)**: two in run 1 (captain Moore's years; who killed a crewman under Captain Wallace) and one in run 2 (reopening year).
- In Q1 to Q4, **no [guess] claim that could be checked was wrong** (0 of 13). Many [guess] claims were right: survivor names, the $7,000 payout, Hall's age of 94, the 49 m tower height.
- Q4 (Voynich): none of the 4 [guess] claims could be confirmed or refuted, so that question adds nothing to the comparison.
- The model also tagged far fewer claims [guess] (34) than [sourced] (224), and often added its own notes like "I'm less sure of this" next to a [sourced] tag.

## Judgment

- Raw numbers: [guess] wrong **14.3%** (3 of 21), [sourced] wrong **1.5%** (2 of 136). That is about 9 times higher, and the test gives p = 0.017.
- But it is **3 wrong claims**, all from **one topic**. Drop Q5 and the [guess] error rate is 0 of 13. One more or one fewer error flips how this reads.
- Your rule was to stop if the sample is too small to say anything. I think this is that case: suggestive, not solid. **I did not make the image.**
- Options: (a) add 5 to 10 more questions and re-run; (b) go with a softer line such as "in my small test, the [guess] tags pointed at most of the AI's errors" (5 wrong claims total, 3 of them tagged [guess]); (c) get the 87 + 13 unconfirmed claims checked with a working page fetcher to firm this up.

A fair way to say it: [guess] labels did point to errors more often, but they did **not** catch most of them. 2 of the 5 wrong claims were tagged [sourced].

## Claim-by-claim check

### Q1. R101 airship crash (1930)

**Run 1** (raw output: `test_log/q1_run1.txt`)

| # | Claim | Label | Result | Note | Sources |
|---|---|---|---|---|---|
| 1 | Crashed in early hours of 5 Oct 1930 | [sourced] | right |  | [ASN](https://aviation-safety.net/wikibase/1467) |
| 2 | Came down near Allonne, outside Beauvais | [sourced] | right |  | [ASN](https://aviation-safety.net/wikibase/1467) |
| 3 | Left Cardington on evening of 4 Oct | [sourced] | right | departed 18:36 GMT | [CAUSES](https://bedsarchives.bedford.gov.uk/CommunityArchives/Shortstown/CausesOfTheR101Disaster.aspx) |
| 4 | Bound for Karachi | [sourced] | right |  | [CAUSES](https://bedsarchives.bedford.gov.uk/CommunityArchives/Shortstown/CausesOfTheR101Disaster.aspx) |
| 5 | Crash at about 2:09 am | [sourced] | cannot confirm | sources say "just after 2am" / c. 02:10 UTC; exact minute not found | [ASN](https://aviation-safety.net/wikibase/1467), [LDWA](https://ldwa.org.uk/lgt/downloads/BedsBucksAndNorthants/THE_TRAGEDY_OF_THE_AIRSHIP_R101.pdf) |
| 6 | 48 died | [sourced] | right |  | [ASN](https://aviation-safety.net/wikibase/1467), [CAS](https://bedsarchives.bedford.gov.uk/CommunityArchives/Shortstown/TheR101Casualties.aspx) |
| 7 | 46 died at scene or soon after, 2 died later in hospital | [sourced] | cannot confirm | no source found for the 46/2 split | [CAS](https://bedsarchives.bedford.gov.uk/CommunityArchives/Shortstown/TheR101Casualties.aspx) |
| 8 | 54 on board, 6 survived | [sourced] | right |  | [ASN](https://aviation-safety.net/wikibase/1467), [PSI](https://psi-encyclopedia.spr.ac.uk/articles/r-101-airship-disaster) |
| 9 | Lord Thomson (Air Secretary) died | [sourced] | right |  | [CAS](https://bedsarchives.bedford.gov.uk/CommunityArchives/Shortstown/TheR101Casualties.aspx), [PSI](https://psi-encyclopedia.spr.ac.uk/articles/r-101-airship-disaster) |
| 10 | Sir Sefton Brancker (Director of Civil Aviation) died | [sourced] | right |  | [CAS](https://bedsarchives.bedford.gov.uk/CommunityArchives/Shortstown/TheR101Casualties.aspx), [PSI](https://psi-encyclopedia.spr.ac.uk/articles/r-101-airship-disaster) |
| 11 | Major G. H. Scott, Assistant Director of Airship Development, died | [sourced] | cannot confirm | death confirmed; exact title not found | [CAS](https://bedsarchives.bedford.gov.uk/CommunityArchives/Shortstown/TheR101Casualties.aspx) |
| 12 | Flt Lt H. C. Irwin, the captain, died | [sourced] | right |  | [CAS](https://bedsarchives.bedford.gov.uk/CommunityArchives/Shortstown/TheR101Casualties.aspx), [PSI](https://psi-encyclopedia.spr.ac.uk/articles/r-101-airship-disaster) |
| 13 | Lt-Col V. C. Richmond, the designer, died | [sourced] | cannot confirm | death listed; "designer" role not confirmed | [CAS](https://bedsarchives.bedford.gov.uk/CommunityArchives/Shortstown/TheR101Casualties.aspx) |
| 14 | Harry Leech survived | [sourced] | right |  | [NA](https://www.nationalarchives.gov.uk/education/resources/thirties-britain/r101-airship-disaster/) |
| 15 | Arthur Disley (wireless operator/electrician) survived | [sourced] | right |  | [NA](https://www.nationalarchives.gov.uk/education/resources/thirties-britain/r101-airship-disaster/) |
| 16 | Bell, Savory and Binks were among the survivors | [guess] | right |  | [NA](https://www.nationalarchives.gov.uk/education/resources/thirties-britain/r101-airship-disaster/), [NZ](https://dynamic-rsnz.natlib.govt.nz/newspapers/MH19301007.2.11) |
| 17 | Loss of gas in bad weather brought the ship down; inquiry blamed gas loss | [sourced] | right |  | [CAUSES](https://bedsarchives.bedford.gov.uk/CommunityArchives/Shortstown/CausesOfTheR101Disaster.aspx) |
| 18 | Hydrogen caught fire | [sourced] | right |  | [CAUSES](https://bedsarchives.bedford.gov.uk/CommunityArchives/Shortstown/CausesOfTheR101Disaster.aspx), [ASN](https://aviation-safety.net/wikibase/1467) |
| 19 | Disaster ended British rigid airship development | [sourced] | cannot confirm | not found in results | none found |
| 20 | Dead buried in a common grave at Cardington | [sourced] | right |  | [FUN](https://bedsarchives.bedford.gov.uk/CommunityArchives/Shortstown/TheR101VictimsFuneralAndMemorial.aspx) |
| 21 | Lying in state at Westminster Hall before burial | [sourced] | right |  | [FUN](https://bedsarchives.bedford.gov.uk/CommunityArchives/Shortstown/TheR101VictimsFuneralAndMemorial.aspx) |

**Run 2** (raw output: `test_log/q1_run2.txt`)

| # | Claim | Label | Result | Note | Sources |
|---|---|---|---|---|---|
| 1 | Crashed early 5 Oct 1930 at about 2:00 am local time | [sourced] | right | "soon after 02:00" | [LDWA](https://ldwa.org.uk/lgt/downloads/BedsBucksAndNorthants/THE_TRAGEDY_OF_THE_AIRSHIP_R101.pdf), [ASN](https://aviation-safety.net/wikibase/1467) |
| 2 | Came down near Allonne, outside Beauvais | [sourced] | right |  | [ASN](https://aviation-safety.net/wikibase/1467) |
| 3 | Left Cardington on evening of 4 Oct | [sourced] | right |  | [CAUSES](https://bedsarchives.bedford.gov.uk/CommunityArchives/Shortstown/CausesOfTheR101Disaster.aspx) |
| 4 | Bound for Karachi | [sourced] | right |  | [CAUSES](https://bedsarchives.bedford.gov.uk/CommunityArchives/Shortstown/CausesOfTheR101Disaster.aspx) |
| 5 | Departure time roughly 6:30 pm | [guess] | right | 18:36 GMT | [CAUSES](https://bedsarchives.bedford.gov.uk/CommunityArchives/Shortstown/CausesOfTheR101Disaster.aspx) |
| 6 | 54 people aboard | [sourced] | right |  | [ASN](https://aviation-safety.net/wikibase/1467) |
| 7 | 48 died: 46 in crash and fire, 2 later in hospital | [sourced] | cannot confirm | 48 confirmed; 46/2 split not found | [CAS](https://bedsarchives.bedford.gov.uk/CommunityArchives/Shortstown/TheR101Casualties.aspx) |
| 8 | 6 survived | [sourced] | right |  | [ASN](https://aviation-safety.net/wikibase/1467) |
| 9 | Lord Thomson, Secretary of State for Air, aboard | [sourced] | right |  | [PSI](https://psi-encyclopedia.spr.ac.uk/articles/r-101-airship-disaster) |
| 10 | Sir Sefton Brancker, Director of Civil Aviation, aboard | [sourced] | right |  | [PSI](https://psi-encyclopedia.spr.ac.uk/articles/r-101-airship-disaster) |
| 11 | Flt Lt H. C. Irwin was the captain | [sourced] | right |  | [CAS](https://bedsarchives.bedford.gov.uk/CommunityArchives/Shortstown/TheR101Casualties.aspx), [PSI](https://psi-encyclopedia.spr.ac.uk/articles/r-101-airship-disaster) |
| 12 | Major G. H. Scott, Assistant Director of Airship Development | [sourced] | cannot confirm | title not found | [CAS](https://bedsarchives.bedford.gov.uk/CommunityArchives/Shortstown/TheR101Casualties.aspx) |
| 13 | Lt-Col Vincent Richmond was the airship's designer | [sourced] | cannot confirm | role not confirmed | [CAS](https://bedsarchives.bedford.gov.uk/CommunityArchives/Shortstown/TheR101Casualties.aspx) |
| 14 | Sqn Ldr E. L. Johnston was the navigator | [sourced] | right |  | [PSI](https://psi-encyclopedia.spr.ac.uk/articles/r-101-airship-disaster) |
| 15 | Sqn Ldr William Palstra, RAAF, aboard as an observer | [guess] | cannot confirm | name, RAAF and presence confirmed; sources call him a passenger/government representative, not "observer" | [PSI](https://psi-encyclopedia.spr.ac.uk/articles/r-101-airship-disaster) |
| 16 | Survivors: Leech, Disley, Savory, Bell, Binks, Cook | [guess] | right | all six names appear in survivor lists | [NZ](https://dynamic-rsnz.natlib.govt.nz/newspapers/MH19301007.2.11), [NA](https://www.nationalarchives.gov.uk/education/resources/thirties-britain/r101-airship-disaster/) |
| 17 | Airship lost gas and altitude in bad weather and dived | [sourced] | right |  | [CAUSES](https://bedsarchives.bedford.gov.uk/CommunityArchives/Shortstown/CausesOfTheR101Disaster.aspx) |
| 18 | Hydrogen then ignited | [sourced] | right |  | [CAUSES](https://bedsarchives.bedford.gov.uk/CommunityArchives/Shortstown/CausesOfTheR101Disaster.aspx) |
| 19 | Inquiry led by Sir John Simon | [sourced] | cannot confirm | not found in results | none found |
| 20 | Disaster ended British rigid airship development | [sourced] | cannot confirm | not found in results | none found |

### Q2. Great Molasses Flood (Boston, 1919)

**Run 1** (raw output: `test_log/q2_run1.txt`)

| # | Claim | Label | Result | Note | Sources |
|---|---|---|---|---|---|
| 1 | Happened 15 January 1919 | [sourced] | right |  | [MWIKI](https://en.wikipedia.org/wiki/Great_Molasses_Flood), [MHIST](https://www.history.com/news/the-great-molasses-flood-of-1919) |
| 2 | At about 12:30 pm | [sourced] | cannot confirm | time not shown in results | none found |
| 3 | Site was in the North End | [sourced] | right |  | [MWIKI](https://en.wikipedia.org/wiki/Great_Molasses_Flood) |
| 4 | About 40°F, unusually warm | [sourced] | cannot confirm |  | none found |
| 5 | Tank owned by USIA, which owned Purity Distilling | [sourced] | cannot confirm |  | none found |
| 6 | Tank about 50 feet tall | [sourced] | right | sources also give 58 ft | [MHIST](https://www.history.com/news/the-great-molasses-flood-of-1919), [MOLD](https://oldnorth.com/blog/the-1919-molasses-flood/) |
| 7 | Tank about 90 feet in diameter | [sourced] | cannot confirm | one source says 90, another 98 | [MHIST](https://www.history.com/news/the-great-molasses-flood-of-1919) |
| 8 | Held roughly 2.3 million gallons | [sourced] | right |  | [MHIST](https://www.history.com/news/the-great-molasses-flood-of-1919), [MWIKI](https://en.wikipedia.org/wiki/Great_Molasses_Flood) |
| 9 | Built in 1915 | [sourced] | right |  | [MOLD](https://oldnorth.com/blog/the-1919-molasses-flood/) |
| 10 | Known to leak; painted brown to hide leaks | [sourced] | cannot confirm |  | none found |
| 11 | Molasses destined for industrial alcohol for munitions | [sourced] | cannot confirm |  | none found |
| 12 | Tank poorly tested, steel too thin | [sourced] | cannot confirm | Ogden found structural failure / poor planning; details not shown | [MSEC](https://www.sec.state.ma.us/divisions/state-house-tours/did-you-know/Molasses-Flood.htm) |
| 13 | Wave up to about 25 feet high | [sourced] | right | estimates range 15 to 30 ft | [MHIST](https://www.history.com/news/the-great-molasses-flood-of-1919), [MWIKI](https://en.wikipedia.org/wiki/Great_Molasses_Flood) |
| 14 | Wave speed around 35 mph | [sourced] | right | one source says 25 mph | [MHIST](https://www.history.com/news/the-great-molasses-flood-of-1919) |
| 15 | Damaged the elevated railway | [sourced] | cannot confirm |  | none found |
| 16 | 21 people died | [sourced] | right |  | [MHIST](https://www.history.com/news/the-great-molasses-flood-of-1919), [MWIKI](https://en.wikipedia.org/wiki/Great_Molasses_Flood) |
| 17 | About 150 injured | [sourced] | right |  | [MHIST](https://www.history.com/news/the-great-molasses-flood-of-1919), [MWIKI](https://en.wikipedia.org/wiki/Great_Molasses_Flood) |
| 18 | Dead included children and city workers | [sourced] | cannot confirm |  | none found |
| 19 | Cleanup took weeks; harbor brown for months | [sourced] | cannot confirm |  | none found |
| 20 | Area smelled of molasses for decades | [guess] | cannot confirm | folk claim, no source | none found |
| 21 | Class action, one of the earliest major ones in Massachusetts | [sourced] | cannot confirm | class action confirmed; "one of earliest" not shown | [MOLD](https://oldnorth.com/blog/the-1919-molasses-flood/) |
| 22 | Brought against USIA by victims and families | [sourced] | right |  | [MOLD](https://oldnorth.com/blog/the-1919-molasses-flood/) |
| 23 | USIA argued anarchists sabotaged the tank | [sourced] | right |  | [MSEC](https://www.sec.state.ma.us/divisions/state-house-tours/did-you-know/Molasses-Flood.htm) |
| 24 | Court appointed auditor Hugh W. Ogden | [sourced] | right |  | [MSEC](https://www.sec.state.ma.us/divisions/state-house-tours/did-you-know/Molasses-Flood.htm) |
| 25 | Hearings involved about 3,000 witnesses | [sourced] | cannot confirm | sources range from ~1,000 to ~3,000 | [MHIST](https://www.history.com/news/the-great-molasses-flood-of-1919), [MOLD](https://oldnorth.com/blog/the-1919-molasses-flood/) |
| 26 | Ogden ruled in 1925 tank unsound, USIA liable | [sourced] | right | April 1925 | [MSEC](https://www.sec.state.ma.us/divisions/state-house-tours/did-you-know/Molasses-Flood.htm) |
| 27 | USIA paid roughly $628,000 | [sourced] | right |  | [MSEC](https://www.sec.state.ma.us/divisions/state-house-tours/did-you-know/Molasses-Flood.htm), [MNEHS](https://newenglandhistoricalsociety.com/great-boston-molasses-disaster-1919/) |
| 28 | About $7,000 per victim's family | [guess] | right | New England Historical Society | [MNEHS](https://newenglandhistoricalsociety.com/great-boston-molasses-disaster-1919/) |
| 29 | Case credited with stricter building codes and licensed-engineer sign-off | [sourced] | right |  | [MPS](https://psmag.com/environment/how-the-boston-molasses-disaster-ushered-in-the-era-of-modern-regulation/) |

**Run 2** (raw output: `test_log/q2_run2.txt`)

| # | Claim | Label | Result | Note | Sources |
|---|---|---|---|---|---|
| 1 | Happened 15 January 1919 | [sourced] | right |  | [MWIKI](https://en.wikipedia.org/wiki/Great_Molasses_Flood) |
| 2 | At about 12:30 pm | [sourced] | cannot confirm |  | none found |
| 3 | Site in the North End | [sourced] | right |  | [MWIKI](https://en.wikipedia.org/wiki/Great_Molasses_Flood) |
| 4 | About 40°F, after a very cold spell | [sourced] | cannot confirm |  | none found |
| 5 | Owner Purity Distilling, a USIA subsidiary | [sourced] | cannot confirm |  | none found |
| 6 | Held about 2.3 million gallons | [sourced] | right |  | [MHIST](https://www.history.com/news/the-great-molasses-flood-of-1919) |
| 7 | About 50 feet tall | [sourced] | right |  | [MHIST](https://www.history.com/news/the-great-molasses-flood-of-1919) |
| 8 | About 90 feet in diameter | [sourced] | cannot confirm | one source says 90, another 98 | [MHIST](https://www.history.com/news/the-great-molasses-flood-of-1919) |
| 9 | Built in 1915 | [sourced] | right |  | [MOLD](https://oldnorth.com/blog/the-1919-molasses-flood/) |
| 10 | Filled to near capacity the day before | [sourced] | cannot confirm |  | none found |
| 11 | Leaked from the start; painted brown | [sourced] | cannot confirm |  | none found |
| 12 | Molasses destined for industrial alcohol/munitions | [sourced] | cannot confirm |  | none found |
| 13 | Wave about 25 feet high | [sourced] | right |  | [MHIST](https://www.history.com/news/the-great-molasses-flood-of-1919) |
| 14 | Wave speed about 35 mph | [sourced] | right |  | [MHIST](https://www.history.com/news/the-great-molasses-flood-of-1919) |
| 15 | 21 died | [sourced] | right |  | [MHIST](https://www.history.com/news/the-great-molasses-flood-of-1919) |
| 16 | About 150 injured | [sourced] | right |  | [MHIST](https://www.history.com/news/the-great-molasses-flood-of-1919) |
| 17 | Victims included children, teamsters; horses killed | [sourced] | cannot confirm |  | none found |
| 18 | Cleanup took weeks | [sourced] | cannot confirm |  | none found |
| 19 | Harbor brown for months; area smelled for years | [guess] | cannot confirm |  | none found |
| 20 | Case was "Dorothy Ann Kelley et al. v. United States Industrial Alcohol Co." | [sourced] | **WRONG** | the lead case was Dorr v. United States Industrial Alcohol Co.; no "Kelley" found | [MWC](https://search.worldcat.org/title/Dorr-trustee-v.-United-States-Industrial-Alcohol-Company/oclc/761310649), [MOLD](https://oldnorth.com/blog/the-1919-molasses-flood/) |
| 21 | One of the first major class actions in Massachusetts | [sourced] | cannot confirm |  | [MOLD](https://oldnorth.com/blog/the-1919-molasses-flood/) |
| 22 | USIA claimed anarchists sabotaged the tank | [sourced] | right |  | [MSEC](https://www.sec.state.ma.us/divisions/state-house-tours/did-you-know/Molasses-Flood.htm) |
| 23 | Auditor Hugh Ogden heard evidence for years | [sourced] | right |  | [MSEC](https://www.sec.state.ma.us/divisions/state-house-tours/did-you-know/Molasses-Flood.htm) |
| 24 | About 3,000 pages of testimony | [sourced] | **WRONG** | sources say 25,000 to 45,000 pages | [MOLD](https://oldnorth.com/blog/the-1919-molasses-flood/) |
| 25 | About 900 witnesses | [sourced] | cannot confirm | sources range from ~1,000 to ~3,000 | [MHIST](https://www.history.com/news/the-great-molasses-flood-of-1919) |
| 26 | Ogden rejected sabotage; tank structurally inadequate | [sourced] | right |  | [MSEC](https://www.sec.state.ma.us/divisions/state-house-tours/did-you-know/Molasses-Flood.htm) |
| 27 | 1925: company found liable | [sourced] | right |  | [MSEC](https://www.sec.state.ma.us/divisions/state-house-tours/did-you-know/Molasses-Flood.htm) |
| 28 | Paid roughly $628,000 | [sourced] | right |  | [MSEC](https://www.sec.state.ma.us/divisions/state-house-tours/did-you-know/Molasses-Flood.htm) |
| 29 | Families got about $7,000 each | [guess] | right |  | [MNEHS](https://newenglandhistoricalsociety.com/great-boston-molasses-disaster-1919/) |
| 30 | Case pushed stricter engineering oversight and qualified-engineer certification | [sourced] | right |  | [MPS](https://psmag.com/environment/how-the-boston-molasses-disaster-ushered-in-the-era-of-modern-regulation/) |

### Q3. Eddystone Lighthouse: the four towers

**Run 1** (raw output: `test_log/q3_run1.txt`)

| # | Claim | Label | Result | Note | Sources |
|---|---|---|---|---|---|
| 1 | Winstanley began building from 1696 | [sourced] | right |  | [EGR](https://www.gracesguide.co.uk/Eddystone_Lighthouse), [EBRIT](https://www.britannica.com/topic/Eddystone-Lighthouse-Eddystone-Rocks-English-Channel) |
| 2 | Light first lit November 1698 | [sourced] | right | 14 Nov 1698 | [EGR](https://www.gracesguide.co.uk/Eddystone_Lighthouse) |
| 3 | Polygonal timber-and-iron tower, later enlarged | [sourced] | cannot confirm |  | none found |
| 4 | Destroyed in Great Storm of Nov 1703; Winstanley died | [sourced] | right |  | [EGR](https://www.gracesguide.co.uk/Eddystone_Lighthouse) |
| 5 | First open-sea lighthouse in the world | [sourced] | cannot confirm |  | none found |
| 6 | Rudyerd built from 1706; lit July 1709 | [sourced] | cannot confirm | 1709 confirmed; one source says built 1708 | [EBRIT](https://www.britannica.com/topic/Eddystone-Lighthouse-Eddystone-Rocks-English-Channel), [EBRIT](https://www.britannica.com/topic/Eddystone-Lighthouse-Eddystone-Rocks-English-Channel) |
| 7 | Rudyerd was a London silk merchant with no engineering background | [sourced] | cannot confirm |  | none found |
| 8 | Tapering timber tower, stone-and-timber base, ship-hull ballast | [sourced] | cannot confirm | "conical wooden" confirmed; rest not | [EBRIT](https://www.britannica.com/topic/Eddystone-Lighthouse-Eddystone-Rocks-English-Channel) |
| 9 | Modelled on an East Indiaman | [guess] | cannot confirm |  | none found |
| 10 | Destroyed by fire in December 1755 | [sourced] | right | 2 Dec 1755 | [EHALL](https://en.wikipedia.org/wiki/Henry_Hall_(lighthouse_keeper)) |
| 11 | Keeper Henry Hall swallowed molten lead and later died | [sourced] | right |  | [EHALL](https://en.wikipedia.org/wiki/Henry_Hall_(lighthouse_keeper)), [ETH](https://trinityhouse.co.uk/lighthouses-and-lightvessels/eddystone-lighthouse) |
| 12 | Smeaton's light first shown 16 October 1759 | [sourced] | right | sources: October 1759 | [EBOX](https://www.theboxplymouth.com/outside-the-box/smeatons-tower/about-smeatons-tower) |
| 13 | Built of interlocking granite and Portland stone | [sourced] | cannot confirm | "interlocking stone" confirmed; stone types not | [EBRIT](https://www.britannica.com/topic/Eddystone-Lighthouse-Eddystone-Rocks-English-Channel) |
| 14 | Smeaton took the oak tree as his model | [sourced] | cannot confirm |  | none found |
| 15 | Smeaton developed hydraulic lime mortar | [sourced] | cannot confirm |  | none found |
| 16 | Stood about 120 years | [sourced] | right | 1759 to 1882 | [EBOX](https://www.theboxplymouth.com/outside-the-box/smeatons-tower/about-smeatons-tower), [ETH](https://trinityhouse.co.uk/lighthouses-and-lightvessels/eddystone-lighthouse) |
| 17 | Erosion beneath it; replaced in the 1870s | [sourced] | cannot confirm | replaced 1882; "1870s" conflicts | [ETH](https://trinityhouse.co.uk/lighthouses-and-lightvessels/eddystone-lighthouse) |
| 18 | Upper part re-erected on Plymouth Hoe | [sourced] | right |  | [ETH](https://trinityhouse.co.uk/lighthouses-and-lightvessels/eddystone-lighthouse) |
| 19 | Stump remains on the rocks | [sourced] | right |  | [ETH](https://trinityhouse.co.uk/lighthouses-and-lightvessels/eddystone-lighthouse) |
| 20 | Douglass was Engineer-in-Chief to Trinity House | [sourced] | cannot confirm |  | none found |
| 21 | Douglass tower built on the South Rock | [sourced] | cannot confirm |  | none found |
| 22 | Douglass light lit 18 May 1882 | [sourced] | right |  | [ETH](https://trinityhouse.co.uk/lighthouses-and-lightvessels/eddystone-lighthouse) |
| 23 | Douglass tower about 49 m (161 ft) tall | [sourced] | right | two sources say ~40 m | [EWI](https://en.wikipedia.org/wiki/Eddystone_Lighthouse), [EBH](https://brucehunt.co.uk/Eddystone%20Lighthouses.html) |
| 24 | Smeaton's tower about 22 m | [guess] | right |  | [EWI](https://en.wikipedia.org/wiki/Eddystone_Lighthouse), [EBOX](https://www.theboxplymouth.com/outside-the-box/smeatons-tower/about-smeatons-tower) |
| 25 | Automated in 1982 | [sourced] | right |  | [ETH](https://trinityhouse.co.uk/lighthouses-and-lightvessels/eddystone-lighthouse) |
| 26 | Helipad above the lantern; light still operates | [sourced] | right |  | [EBH](https://brucehunt.co.uk/Eddystone%20Lighthouses.html) |
| 27 | Light range around 17 nautical miles | [guess] | cannot confirm | sources say 17 and 22 nmi | [EWI](https://en.wikipedia.org/wiki/Eddystone_Lighthouse) |

**Run 2** (raw output: `test_log/q3_run2.txt`)

| # | Claim | Label | Result | Note | Sources |
|---|---|---|---|---|---|
| 1 | Henry Winstanley built it | [sourced] | right |  | [EGR](https://www.gracesguide.co.uk/Eddystone_Lighthouse) |
| 2 | Started 1696; lit 14 November 1698 | [sourced] | right |  | [EGR](https://www.gracesguide.co.uk/Eddystone_Lighthouse) |
| 3 | Polygonal timber-and-iron on stone base; enlarged 1699 | [sourced] | cannot confirm |  | none found |
| 4 | First lighthouse built on an open-sea rock | [sourced] | cannot confirm |  | none found |
| 5 | Great Storm of Nov 1703 destroyed it; Winstanley died; 26-27 Nov | [sourced] | right | 27 Nov | [EGR](https://www.gracesguide.co.uk/Eddystone_Lighthouse) |
| 6 | Winstanley wished to be there in "the greatest storm there ever was" | [guess] | cannot confirm |  | none found |
| 7 | Rudyerd was a silk mercer with no formal training | [sourced] | cannot confirm |  | none found |
| 8 | Rudyerd's tower lit in 1709 | [sourced] | right |  | [EBRIT](https://www.britannica.com/topic/Eddystone-Lighthouse-Eddystone-Rocks-English-Channel) |
| 9 | John Lovett held the lease; his commission was to rebuild | [guess] | cannot confirm |  | none found |
| 10 | Conical timber structure with stone ballast and stone-filled core | [sourced] | cannot confirm | "conical wooden" confirmed; rest not | [EBRIT](https://www.britannica.com/topic/Eddystone-Lighthouse-Eddystone-Rocks-English-Channel) |
| 11 | Burned December 1755; fire started at the lantern | [sourced] | right |  | [EHALL](https://en.wikipedia.org/wiki/Henry_Hall_(lighthouse_keeper)) |
| 12 | Keeper Henry Hall swallowed molten lead and died | [sourced] | right |  | [EHALL](https://en.wikipedia.org/wiki/Henry_Hall_(lighthouse_keeper)), [ETH](https://trinityhouse.co.uk/lighthouses-and-lightvessels/eddystone-lighthouse) |
| 13 | Hall was about 94 | [guess] | right |  | [EHALL](https://en.wikipedia.org/wiki/Henry_Hall_(lighthouse_keeper)) |
| 14 | Hall died about 12 days later | [guess] | right | one source says several days; Trinity House and Guinness say 12 | [ETH](https://trinityhouse.co.uk/lighthouses-and-lightvessels/eddystone-lighthouse), [EHALL](https://en.wikipedia.org/wiki/Henry_Hall_(lighthouse_keeper)) |
| 15 | Smeaton designed and built it | [sourced] | right |  | [EBOX](https://www.theboxplymouth.com/outside-the-box/smeatons-tower/about-smeatons-tower) |
| 16 | Work began 1756; lit 16 October 1759 | [sourced] | right | sources: 1756-59, Oct 1759 | [EBOX](https://www.theboxplymouth.com/outside-the-box/smeatons-tower/about-smeatons-tower), [EBRIT](https://www.britannica.com/topic/Eddystone-Lighthouse-Eddystone-Rocks-English-Channel) |
| 17 | Interlocking dovetailed granite, hydraulic lime mortar, oak-tree profile | [sourced] | cannot confirm |  | none found |
| 18 | Tower replaced in 1882 | [sourced] | right |  | [ETH](https://trinityhouse.co.uk/lighthouses-and-lightvessels/eddystone-lighthouse) |
| 19 | Smeaton credited with early hydraulic cement work | [sourced] | cannot confirm |  | none found |
| 20 | Upper part rebuilt on Plymouth Hoe; stub remains | [sourced] | right |  | [ETH](https://trinityhouse.co.uk/lighthouses-and-lightvessels/eddystone-lighthouse) |
| 21 | Douglass designed the present tower | [sourced] | right |  | [EBRIT](https://www.britannica.com/topic/Eddystone-Lighthouse-Eddystone-Rocks-English-Channel) |
| 22 | Douglass tower lit 18 May 1882 | [sourced] | right |  | [ETH](https://trinityhouse.co.uk/lighthouses-and-lightvessels/eddystone-lighthouse) |
| 23 | Interlocking dovetailed granite; stands next to Smeaton stump | [sourced] | cannot confirm |  | none found |
| 24 | Douglass tower about 49 m to the lantern | [guess] | right |  | [EWI](https://en.wikipedia.org/wiki/Eddystone_Lighthouse), [EBH](https://brucehunt.co.uk/Eddystone%20Lighthouses.html) |
| 25 | Automated in 1982 | [sourced] | right |  | [ETH](https://trinityhouse.co.uk/lighthouses-and-lightvessels/eddystone-lighthouse) |
| 26 | Helipad added in 1980 | [guess] | right |  | [EBH](https://brucehunt.co.uk/Eddystone%20Lighthouses.html) |

### Q4. Voynich manuscript: owners and dating

**Run 1** (raw output: `test_log/q4_run1.txt`)

| # | Claim | Label | Result | Note | Sources |
|---|---|---|---|---|---|
| 1 | Rudolf II said to have bought it for 600 gold ducats | [sourced] | right | claim comes from Marci letter | [VRBH](https://www.rarebookhub.com/articles/3334) |
| 2 | That claim rests on a 1665 letter from Marci | [sourced] | right | letter dated 1665 or 1666 | [VRBH](https://www.rarebookhub.com/articles/3334), [VWI](https://en.wikipedia.org/wiki/Voynich_manuscript) |
| 3 | Rudolf II thought it was by Roger Bacon | [sourced] | cannot confirm |  | none found |
| 4 | Horcicky de Tepenec owned it early 1600s; signature seen under UV | [sourced] | right |  | [VRBH](https://www.rarebookhub.com/articles/3334) |
| 5 | Georg Baresch, Prague alchemist, wrote to Kircher in 1630s | [sourced] | right | about 30 years before 1665 | [VRBH](https://www.rarebookhub.com/articles/3334) |
| 6 | Marci sent it to Kircher about 1665 | [sourced] | right |  | [VRBH](https://www.rarebookhub.com/articles/3334) |
| 7 | Kircher held it at the Collegio Romano | [sourced] | cannot confirm |  | none found |
| 8 | Jesuits kept it about two centuries at Collegio Romano | [sourced] | cannot confirm |  | none found |
| 9 | 1870 Italian seizure; moved to Villa Mondragone | [sourced] | cannot confirm |  | none found |
| 10 | Jesuits moved books to private ownership to protect them | [sourced] | cannot confirm |  | none found |
| 11 | Wilfrid Voynich bought it in 1912 from Jesuits at Villa Mondragone | [sourced] | right | traditional account; one 2024 essay disputes the place | [VRBH](https://www.rarebookhub.com/articles/3334), [VORIG](https://www.voynich.nu/origin.html) |
| 12 | After 1930 his widow Ethel inherited it | [sourced] | right |  | [VRBH](https://www.rarebookhub.com/articles/3334) |
| 13 | Ethel left it to her friend Anne Nill | [sourced] | right | Beinecke account; a probate study differs | [VYALE](https://news.yale.edu/2016/10/31/mysterious-voynich-manuscript-reborn-facsimile-edition) |
| 14 | Nill sold it to Hans Kraus in 1961 | [sourced] | right |  | [VRBH](https://www.rarebookhub.com/articles/3334) |
| 15 | Kraus donated it to Yale in 1969 | [sourced] | right |  | [VRBH](https://www.rarebookhub.com/articles/3334), [VYALE](https://news.yale.edu/2016/10/31/mysterious-voynich-manuscript-reborn-facsimile-edition) |
| 16 | Arizona radiocarbon on four samples, 2009: about 1404-1438 | [sourced] | right |  | [VCARB](https://www.voynich.nu/extra/carbon.html) |
| 17 | Dating rules out Rudolf II and Bacon as authors | [sourced] | right | dates precede Rudolf; Bacon is 13th c. | [VCARB](https://www.voynich.nu/extra/carbon.html) |
| 18 | McCrone found ink period-consistent, no anachronistic pigments | [sourced] | cannot confirm |  | [VMC](https://ciphermysteries.com/2011/06/01/voynich-the-mccrone-report-now-online) |
| 19 | Earlier tests were from 2009-2010 | [guess] | cannot confirm | McCrone report 2009, released 2011 | [VMC](https://ciphermysteries.com/2011/06/01/voynich-the-mccrone-report-now-online) |
| 20 | Illustrations suggest northern Italy in 15th century | [sourced] | cannot confirm |  | none found |
| 21 | Radiocarbon dates the skin, not the writing | [sourced] | right |  | [VCARB](https://www.voynich.nu/extra/carbon.html) |
| 22 | Marci's letter is the main link to Rudolf II; reliability questioned | [sourced] | right |  | [VRBH](https://www.rarebookhub.com/articles/3334) |

**Run 2** (raw output: `test_log/q4_run2.txt`)

| # | Claim | Label | Result | Note | Sources |
|---|---|---|---|---|---|
| 1 | About 240 vellum pages | [sourced] | cannot confirm |  | none found |
| 2 | Central Europe and northern Italy are the usual origin suggestions | [guess] | cannot confirm |  | none found |
| 3 | Rudolf II bought it for 600 ducats; hearsay from 1665 Marci letter | [sourced] | right |  | [VRBH](https://www.rarebookhub.com/articles/3334) |
| 4 | Horcicky was a pharmacist and curator; signature found with chemical reagents | [sourced] | cannot confirm | sources call him court alchemist/physician; UV seen | [VRBH](https://www.rarebookhub.com/articles/3334) |
| 5 | Baresch wrote to Kircher in the 1630s | [sourced] | right |  | [VRBH](https://www.rarebookhub.com/articles/3334) |
| 6 | Marci sent it to Kircher in 1665 or 1666 | [sourced] | right |  | [VRBH](https://www.rarebookhub.com/articles/3334) |
| 7 | Kircher's ownership documented by the letter | [sourced] | cannot confirm |  | none found |
| 8 | Vanishes about 200 years, probably in Collegio Romano | [guess] | cannot confirm | gap confirmed; location not | [VRBH](https://www.rarebookhub.com/articles/3334) |
| 9 | Jesuits kept it at Villa Mondragone until the 1870 seizure | [sourced] | cannot confirm | conflicts with 1912 sale from Jesuits | [VRBH](https://www.rarebookhub.com/articles/3334) |
| 10 | Wilfrid Voynich bought it in 1912 | [sourced] | right |  | [VRBH](https://www.rarebookhub.com/articles/3334) |
| 11 | Sale was secret and tied to Jesuit money trouble | [guess] | cannot confirm |  | [VORIG](https://www.voynich.nu/origin.html) |
| 12 | Ethel inherited in 1930; Anne Nill then held it | [sourced] | right |  | [VYALE](https://news.yale.edu/2016/10/31/mysterious-voynich-manuscript-reborn-facsimile-edition) |
| 13 | Kraus bought it in 1961 | [sourced] | right |  | [VRBH](https://www.rarebookhub.com/articles/3334) |
| 14 | Yale received it from Kraus in 1969 | [sourced] | right |  | [VYALE](https://news.yale.edu/2016/10/31/mysterious-voynich-manuscript-reborn-facsimile-edition) |
| 15 | Arizona radiocarbon 2009, four samples: about 1404-1438 | [sourced] | right |  | [VCARB](https://www.voynich.nu/extra/carbon.html) |
| 16 | Radiocarbon dates the skin, not the ink | [sourced] | right |  | [VCARB](https://www.voynich.nu/extra/carbon.html) |
| 17 | 2010s ink analysis found mostly iron-gall ink, 15th-century consistent | [sourced] | cannot confirm | McCrone report 2009; iron-gall finding disputed | [VMC](https://ciphermysteries.com/2011/06/01/voynich-the-mccrone-report-now-online) |
| 18 | Art historians compare illustrations to northern Italian work | [sourced] | cannot confirm |  | none found |
| 19 | Radiocarbon dating ruled out Roger Bacon | [sourced] | right |  | [VCARB](https://www.voynich.nu/extra/carbon.html) |
| 20 | Old blank vellum could be reused | [sourced] | cannot confirm |  | none found |

### Q5. Clipper ship Cutty Sark

**Run 1** (raw output: `test_log/q5_run1.txt`)

| # | Claim | Label | Result | Note | Sources |
|---|---|---|---|---|---|
| 1 | Launched 22 November 1869 | [sourced] | right |  | [CGEN](https://www.thegenealogist.co.uk/featuredarticles/discover-your-ancestors/periodical/79/celebrating-150-years-of-cutty-sark-6719/), [CRMG](https://www.rmg.co.uk/cutty-sark/history) |
| 2 | Built by Scott & Linton | [sourced] | right |  | [CGEN](https://www.thegenealogist.co.uk/featuredarticles/discover-your-ancestors/periodical/79/celebrating-150-years-of-cutty-sark-6719/) |
| 3 | Designed by Hercules Linton | [sourced] | cannot confirm |  | none found |
| 4 | Scott & Linton ran out of money; Denny finished her | [sourced] | right |  | [CGEN](https://www.thegenealogist.co.uk/featuredarticles/discover-your-ancestors/periodical/79/celebrating-150-years-of-cutty-sark-6719/) |
| 5 | Owner John "Jock" Willis; China tea trade | [sourced] | cannot confirm |  | none found |
| 6 | Composite clipper, iron frame, wood planking | [sourced] | cannot confirm |  | none found |
| 7 | About 212 ft long, about 963 gross tons | [sourced] | right | 212.5 ft, 963 GRT | [CWI](https://en.wikipedia.org/wiki/Cutty_Sark) |
| 8 | Cost roughly 16,000 pounds | [guess] | right | 16,150 pounds | [CRMG](https://www.rmg.co.uk/cutty-sark/history) |
| 9 | Name from Tam o' Shanter; Nannie Dee | [sourced] | cannot confirm |  | none found |
| 10 | Figurehead is Nannie Dee holding a horse's tail | [sourced] | cannot confirm |  | none found |
| 11 | First voyage 1870 London to Shanghai | [sourced] | cannot confirm |  | none found |
| 12 | Suez Canal opened 1869 and favoured steamers | [sourced] | right | opened 17 Nov 1869 | [CGEN](https://www.thegenealogist.co.uk/featuredarticles/discover-your-ancestors/periodical/79/celebrating-150-years-of-cutty-sark-6719/) |
| 13 | Only about eight tea cargoes | [sourced] | cannot confirm |  | none found |
| 14 | She never won a tea race | [sourced] | cannot confirm |  | none found |
| 15 | Main rival was Thermopylae | [sourced] | right |  | [CGEN](https://www.thegenealogist.co.uk/featuredarticles/discover-your-ancestors/periodical/79/celebrating-150-years-of-cutty-sark-6719/) |
| 16 | 1872 race: lost rudder in Indian Ocean gale | [sourced] | right | jury rudder not confirmed | [CGEN](https://www.thegenealogist.co.uk/featuredarticles/discover-your-ancestors/periodical/79/celebrating-150-years-of-cutty-sark-6719/) |
| 17 | Thermopylae arrived about a week ahead | [sourced] | right |  | [CGEN](https://www.thegenealogist.co.uk/featuredarticles/discover-your-ancestors/periodical/79/celebrating-150-years-of-cutty-sark-6719/) |
| 18 | George Moodie was first captain | [sourced] | right |  | [CWT](https://www.wikitree.com/wiki/Space:Cutty_Sark) |
| 19 | Moodie commanded her in the 1872 race | [guess] | right | Moodie 1869-72 | [CWT](https://www.wikitree.com/wiki/Space:Cutty_Sark) |
| 20 | F. W. Moore commanded through much of the 1870s and early 1880s | [guess] | **WRONG** | Moore 1872-73; Tiptaft 1874-78; Wallace 1878-80; Bruce 1880-82 | [CWT](https://www.wikitree.com/wiki/Space:Cutty_Sark), [CMUR](https://rmg.co.uk/stories/topics/1878-83-tramping-cargoes-murder-mutiny) |
| 21 | Captain Wallace killed a crewman, then took his own life | [guess] | **WRONG** | the mate, Sidney Smith, killed the crewman; Wallace jumped overboard | [CMUR](https://rmg.co.uk/stories/topics/1878-83-tramping-cargoes-murder-mutiny) |
| 22 | Woodget commanded 1885-1895 | [sourced] | right |  | [CWT](https://www.wikitree.com/wiki/Space:Cutty_Sark), [CNMM](https://www.nmm.ac.uk/stories/topics/1883-95-australian-wool-years) |
| 23 | From 1883 she carried Australian wool | [sourced] | right |  | [CNMM](https://www.nmm.ac.uk/stories/topics/1883-95-australian-wool-years) |
| 24 | Often faster than Thermopylae on wool route | [sourced] | right |  | [CNMM](https://www.nmm.ac.uk/stories/topics/1883-95-australian-wool-years), [CWT](https://www.wikitree.com/wiki/Space:Cutty_Sark) |
| 25 | Woodget passages about 70-80 days | [guess] | right | 73 days documented | [CWT](https://www.wikitree.com/wiki/Space:Cutty_Sark) |
| 26 | Best passage about 67 days | [guess] | cannot confirm | 73 days is the best documented | [CWT](https://www.wikitree.com/wiki/Space:Cutty_Sark) |
| 27 | Best 24-hour run about 360 nautical miles | [guess] | right | 363 nmi | [CFOX](https://www.foxnews.com/story/a-brief-look-at-the-cutty-sark-clipper-ship) |
| 28 | 1895 sold to Portuguese owners, renamed Ferreira | [sourced] | cannot confirm |  | none found |
| 29 | Later renamed Maria do Amparo | [sourced] | cannot confirm |  | none found |
| 30 | Captain Dowman restored her at Falmouth in 1922 | [sourced] | cannot confirm |  | none found |
| 31 | Training ship from 1938 | [sourced] | cannot confirm |  | none found |
| 32 | Greenwich dry dock 1954; opened 1957 | [sourced] | cannot confirm |  | none found |
| 33 | Fire in May 2007 during conservation | [sourced] | right | 21 May 2007 | [CGEN](https://www.thegenealogist.co.uk/featuredarticles/discover-your-ancestors/periodical/79/celebrating-150-years-of-cutty-sark-6719/) |
| 34 | Reopened in 2012 | [sourced] | right | 25 April 2012 | [CGEN](https://www.thegenealogist.co.uk/featuredarticles/discover-your-ancestors/periodical/79/celebrating-150-years-of-cutty-sark-6719/) |

**Run 2** (raw output: `test_log/q5_run2.txt`)

| # | Claim | Label | Result | Note | Sources |
|---|---|---|---|---|---|
| 1 | Built 1869 by Scott & Linton | [sourced] | right |  | [CGEN](https://www.thegenealogist.co.uk/featuredarticles/discover-your-ancestors/periodical/79/celebrating-150-years-of-cutty-sark-6719/) |
| 2 | Hercules Linton designed her | [sourced] | cannot confirm |  | none found |
| 3 | Ordered by Jock Willis for China tea | [sourced] | cannot confirm |  | none found |
| 4 | Scott & Linton in financial trouble; Denny finished her | [sourced] | right |  | [CGEN](https://www.thegenealogist.co.uk/featuredarticles/discover-your-ancestors/periodical/79/celebrating-150-years-of-cutty-sark-6719/) |
| 5 | Launched 22 November 1869 | [sourced] | right |  | [CGEN](https://www.thegenealogist.co.uk/featuredarticles/discover-your-ancestors/periodical/79/celebrating-150-years-of-cutty-sark-6719/) |
| 6 | About 212 ft, 963 gross tons | [sourced] | right |  | [CWI](https://en.wikipedia.org/wiki/Cutty_Sark) |
| 7 | Name from Tam o' Shanter; figurehead is Nannie | [sourced] | cannot confirm |  | none found |
| 8 | Suez opened 1869, hurt sailing tea trade | [sourced] | right |  | [CGEN](https://www.thegenealogist.co.uk/featuredarticles/discover-your-ancestors/periodical/79/celebrating-150-years-of-cutty-sark-6719/) |
| 9 | About eight tea voyages, 1870-1877 | [sourced] | cannot confirm |  | none found |
| 10 | 1872 race: rudder lost; Thermopylae won by about a week | [sourced] | right |  | [CGEN](https://www.thegenealogist.co.uk/featuredarticles/discover-your-ancestors/periodical/79/celebrating-150-years-of-cutty-sark-6719/) |
| 11 | Carried jute and coal in late 1870s | [sourced] | cannot confirm |  | none found |
| 12 | From 1883 wool; often the fastest ship afloat | [sourced] | right |  | [CNMM](https://www.nmm.ac.uk/stories/topics/1883-95-australian-wool-years) |
| 13 | 1895 sold to Portuguese firm, renamed Ferreira, then Maria do Amparo | [sourced] | cannot confirm |  | none found |
| 14 | 1922 Dowman bought and restored her at Falmouth | [sourced] | cannot confirm |  | none found |
| 15 | Training ship at Greenhithe from 1938 | [sourced] | cannot confirm |  | none found |
| 16 | 1954 Greenwich dry dock; public 1957 | [sourced] | cannot confirm |  | none found |
| 17 | Fire in May 2007 during conservation | [sourced] | right |  | [CGEN](https://www.thegenealogist.co.uk/featuredarticles/discover-your-ancestors/periodical/79/celebrating-150-years-of-cutty-sark-6719/) |
| 18 | She reopened in 2010 and was raised in 2012 | [guess] | **WRONG** | reopened 25 April 2012 | [CGEN](https://www.thegenealogist.co.uk/featuredarticles/discover-your-ancestors/periodical/79/celebrating-150-years-of-cutty-sark-6719/) |
| 19 | George Moodie first captain, 1869/70 to 1872 | [sourced] | right |  | [CWT](https://www.wikitree.com/wiki/Space:Cutty_Sark) |
| 20 | F. W. Moore commanded in the 1870s | [sourced] | right | 1872-73 | [CWT](https://www.wikitree.com/wiki/Space:Cutty_Sark), [CCAP](https://rmg.co.uk/cutty-sark/history/captains-of-cutty-sark) |
| 21 | Wallace died 1880 after mate killed crewman John Francis | [sourced] | right | Wallace jumped overboard 5 Sep 1880 | [CMUR](https://rmg.co.uk/stories/topics/1878-83-tramping-cargoes-murder-mutiny) |
| 22 | Captain Bruce took over around 1880 | [guess] | right | Bruce 1880-82 | [CMUR](https://rmg.co.uk/stories/topics/1878-83-tramping-cargoes-murder-mutiny), [CWT](https://www.wikitree.com/wiki/Space:Cutty_Sark) |
| 23 | Woodget commanded 1885-1895 | [sourced] | right |  | [CWT](https://www.wikitree.com/wiki/Space:Cutty_Sark) |
| 24 | Woodget's wool passages often beat Thermopylae | [sourced] | right |  | [CGEN](https://www.thegenealogist.co.uk/featuredarticles/discover-your-ancestors/periodical/79/celebrating-150-years-of-cutty-sark-6719/) |
| 25 | Best day's run about 363 nautical miles | [guess] | right |  | [CFOX](https://www.foxnews.com/story/a-brief-look-at-the-cutty-sark-clipper-ship) |
| 26 | Top speed about 17 knots | [guess] | right | 17.15 knots | [CFOX](https://www.foxnews.com/story/a-brief-look-at-the-cutty-sark-clipper-ship) |
| 27 | Woodget's fastest wool passages about 70-75 days | [guess] | right | 73 days | [CWT](https://www.wikitree.com/wiki/Space:Cutty_Sark) |
| 28 | Fastest tea passage around 107 days | [guess] | cannot confirm |  | none found |

## Raw outputs

The ten outputs are stored unedited in `test_log/`. The question text for each:

- Q1: Tell me about the R101 airship crash of 1930: the date, where it happened, how many people died, and who was on board. (+ suffix)
- Q2: Tell me about the Great Molasses Flood in Boston in 1919: the date, the size of the tank, how many died, and the court case afterwards. (+ suffix)
- Q3: Tell me about the history of the Eddystone Lighthouse: who built each of the towers and when. (+ suffix)
- Q4: Tell me about the Voynich manuscript: who owned it over the years, and how it was dated. (+ suffix)
- Q5: Tell me about the clipper ship Cutty Sark: who built her, her famous voyages, her captains, and her record times. (+ suffix)

### Full text of each output

<details><summary>Q1 run 1</summary>

```
**The R101 disaster, from memory (I did no searches)**

**Date and place**
- The R101 crashed in the early hours of **5 October 1930**. [sourced]
- It came down on a hillside near **Allonne, just outside Beauvais, in northern France**. [sourced]
- It had left its mooring mast at **Cardington, Bedfordshire**, on the evening of 4 October. [sourced]
- It was on its first overseas flight, bound for **Karachi, India**. [sourced]
- The crash came at about **2:09 am**. [sourced] I'm less sure of the exact minute, so treat that as approximate.

**Deaths**
- **48 people died** in total. [sourced]
- 46 died at the scene or soon after, and 2 more died later in hospital. [sourced]
- There were **54 people on board**, so **6 survived**. [sourced]
- I'm moderately sure of the 54 figure, which fits the 48 dead plus 6 survivors.

**Who was on board**
- **Lord Thomson**, the Secretary of State for Air, died. [sourced]
- **Air Vice-Marshal Sir Sefton Brancker**, the Director of Civil Aviation, died. [sourced]
- **Major G. H. Scott**, the Assistant Director of Airship Development, died. [sourced]
- **Flight Lieutenant H. Carmichael Irwin**, the captain, died. [sourced]
- **Lt-Col V. C. Richmond**, the designer, died. [sourced]
- The crew included riggers, engineers, a wireless operator and others. [sourced]
- Most of the dead were crew members. Passengers and officials made up a smaller group. [sourced]
- **Harry Leech**, a foreman engineer, survived. [sourced]
- **Arthur Disley**, the wireless operator and electrician, survived. [sourced]
- The other survivors were mostly engine-car crew, and I believe **Arthur Bell, Victor Savory and Joe Binks** were among them. [guess] I'm not sure of those names or of the full list of six.

**Cause and aftermath**
- The airship hit the ground in rain and strong winds, and the hydrogen caught fire. [sourced]
- The inquiry pointed to a **loss of gas, probably from tears in the outer cover and leaking gas bags, combined with a dive**. [sourced]
- Exactly how the ship came to dive is still debated. [guess]
- The disaster effectively ended British rigid airship development. [sourced]
- The dead were buried in a **common grave at Cardington**. [sourced]
- A national day of mourning and a lying in state at Westminster Hall preceded the burial. [sourced] I'm less sure of the exact details.

I can run searches to check the guessed items, especially the survivor list and the exact timing, if you want.

```

</details>

<details><summary>Q1 run 2</summary>

```
**R101 airship disaster, 1930**

**Date and place**
- The R101 crashed in the early hours of **5 October 1930**, at about 2:00 am local time. [sourced]
- It came down on a hillside near **Allonne, just outside Beauvais, northern France**. [sourced]
- It had left its mooring mast at Cardington, Bedfordshire, on the evening of 4 October. [sourced] It was bound for Karachi, in British India, on a long-distance test flight. [sourced]
- The departure time was roughly 6:30 pm. [guess]

**Deaths**
- There were **54 people aboard**. [sourced]
- **48 died**: 46 in the crash and fire, and 2 more later in hospital. [sourced]
- **6 survived**. [sourced]

**Notable people aboard**
- **Lord Thomson**, Secretary of State for Air, who was a main champion of the flight. [sourced]
- **Air Vice-Marshal Sir Sefton Brancker**, Director of Civil Aviation. [sourced]
- **Flt Lt H. Carmichael Irwin**, the captain. [sourced]
- **Major G. H. Scott**, Assistant Director of Airship Development. [sourced]
- **Lt-Col Vincent Richmond**, the airship's designer. [sourced]
- **Sqn Ldr E. L. Johnston**, the navigator. [sourced]
- Sqn Ldr **William Palstra** of the Royal Australian Air Force was aboard as an observer. [guess] I'm unsure of his name and role.
- The rest were crew, such as riggers, engineers and wireless operators, plus a few officials and passengers. [sourced]

**Survivors**
- The survivors were mostly engine-car crew and engineers. [sourced]
- Names I recall are **Harry Leech**, **Arthur Disley**, **Victor Savory**, **Arthur Bell**, **Joe Binks** and **Alf Cook**. [guess] I'm fairly but not fully sure of the list and spellings.

**Cause**
- The airship lost gas and altitude in bad weather and dived into the ground. [sourced]
- Its hydrogen then ignited. [sourced]
- An official inquiry led by Sir John Simon blamed the failure of the outer cover and gas bags, and the airship's design. [sourced]
- The disaster effectively ended British rigid airship development. [sourced]

I answered from memory without searching. I can check the names and figures against sources if you'd like.

```

</details>

<details><summary>Q2 run 1</summary>

```
**The Great Molasses Flood (Boston, 1919)**

**Date and place**
- It happened on January 15, 1919, around 12:30 p.m. [sourced]
- The site was the North End, at the Purity Distilling Company's storage facility near Commercial Street. [sourced]
- The weather was unusually warm for a Boston January, about 40°F after a spell of intense cold. [sourced]

**The tank**
- It was a steel tank owned by the United States Industrial Alcohol Company (USIA), which owned Purity Distilling. [sourced]
- It stood about 50 feet tall. [sourced]
- It was about 90 feet in diameter. [sourced]
- It held roughly 2.3 million gallons of molasses when it failed, close to full capacity. [sourced]
- It had been built in 1915. [sourced]
- It was known to leak, and the company reportedly painted it brown to hide the leaks. [sourced]
- The molasses was destined largely for industrial alcohol, which was used for munitions. [sourced]
- The tank had not been properly tested, and the engineering was poor, with steel that was too thin and a weak design. [sourced]

**The wave**
- Estimates put the wave at up to about 25 feet high at first. [sourced]
- Its speed is commonly quoted at around 35 mph. [sourced]
- It destroyed buildings, damaged the elevated railway structure, and swept up people, horses and vehicles. [sourced]

**Deaths and injuries**
- 21 people died. [sourced]
- About 150 people were injured. [sourced]
- Among the dead were children and city workers. [sourced]
- Cleanup took weeks, and the harbor was said to be brown with molasses for months. [sourced]
- The claim that the area smelled of molasses for decades is a popular story. [guess]

**The court case**
- It was a class action, one of the earliest major ones in Massachusetts. [sourced]
- It was brought against USIA by victims and families. [sourced]
- USIA first argued that anarchists had sabotaged the tank. [sourced]
- The court appointed an auditor, Hugh W. Ogden, to hear the evidence. [sourced]
- The hearings ran for years and involved about 3,000 witnesses. [sourced]
- Ogden ruled in 1925 that the tank was structurally unsound, so USIA was liable. [sourced]
- USIA settled and paid roughly $628,000 in damages. [sourced]
- The widely repeated figure of about $7,000 per victim's family is approximate. [guess]
- The case is credited with helping drive stricter building codes and engineering requirements, including the use of licensed engineers and professional sign-off on plans. [sourced]

**A caution:** the numbers for wave height, speed and settlement are the ones most often repeated with variation. The date, the death toll, the tank's capacity and the outcome of the case are the best documented.

I answered from memory, with no searches, so the [sourced] tags mean "well documented as far as I know." They do not mean I checked a source just now. If you plan to cite any of this, verify it first. I can search for primary sources if you'd like.

```

</details>

<details><summary>Q2 run 2</summary>

```
**The Great Molasses Flood (Boston, 1919)**

**Date and place**
- It happened on January 15, 1919, around 12:30 pm. [sourced]
- The site was the North End, near Commercial Street, by the waterfront. [sourced]
- The weather was unusually warm for January, about 40°F (4°C), after a very cold spell. [sourced]

**The tank**
- The owner was the Purity Distilling Company, a subsidiary of United States Industrial Alcohol (USIA). [sourced]
- It held about 2.3 million gallons of molasses when it failed. [sourced]
- It was around 50 feet tall and about 90 feet in diameter. [sourced]
- It had been built in 1915 and was filled to near capacity just the day before. [sourced]
- It was said to have leaked from the start. USIA reportedly painted it brown instead of fixing it. [sourced]
- The molasses was destined largely for industrial alcohol, used in munitions production. [sourced]

**The wave**
- The wave is commonly described as about 25 feet high at its peak. [sourced]
- Its speed is commonly given as about 35 mph. [sourced]
- Both figures are estimates from witness accounts and later modeling. [guess]

**Casualties**
- 21 people died. [sourced]
- About 150 people were injured. [sourced]
- Victims included children, city workers and teamsters, and horses were also killed. [sourced]
- The cleanup took weeks. [sourced]
- Locals reported that the harbor stayed brown for months, and that the area smelled of molasses for years. [guess]

**The court case**
- The class-action suit was *Dorothy Ann Kelley et al. v. United States Industrial Alcohol Co.* [sourced]
- It was one of the first major class actions in Massachusetts. [sourced]
- USIA claimed anarchists had sabotaged the tank. [sourced]
- The court-appointed auditor, Hugh Ogden, took years to hear the evidence. There were roughly 3,000 pages of testimony and about 900 witnesses. [sourced]
- Ogden rejected the sabotage theory. He found the tank was structurally inadequate and had not been properly tested. [sourced]
- In 1925 the company was found liable. [sourced]
- It paid out roughly $628,000 in damages. [sourced]
- Families of the dead are often said to have received about $7,000 each. [guess]
- The case is often credited with pushing stricter engineering oversight and building regulation, including the need for qualified engineers to certify plans. [sourced]
- The claim that it directly produced specific Massachusetts licensing laws is less clear. [guess]

I answered from memory without searching. The "[sourced]" tags mark claims I'm confident are well documented, not claims I checked just now. I can run a search to verify the [guess] items if you want.

```

</details>

<details><summary>Q3 run 1</summary>

```
# Eddystone Lighthouse: the four towers

The Eddystone Rocks lie about 14 miles (22 km) south-southwest of Plymouth, England. Four lighthouses have stood there.

## 1. Winstanley's Tower (1698–1703)
- Built by **Henry Winstanley**, an engineer and showman, on the rocks from 1696 [sourced].
- The light was first lit in **November 1698** [sourced].
- The tower was a polygonal, timber-and-iron structure, decorated and fanciful. Winstanley later enlarged it [sourced].
- It was destroyed in the **Great Storm of November 1703**. Winstanley, who was at the lighthouse for repairs, died with it [sourced].
- It was the first open-sea lighthouse in the world [sourced]. Some accounts hedge on that "first" claim, though.

## 2. Rudyerd's Tower (1709–1755)
- Built by **John Rudyerd**, a silk mercer, from 1706. It was lit in **July 1709** [sourced].
- Rudyerd was a London silk merchant and had no engineering background [sourced].
- The design was a tapering timber structure with a stone-and-timber base, and was ballasted to resemble a ship's hull [sourced]. It was said to be modelled on an East Indiaman's form [guess].
- It was destroyed by **fire in December 1755**. Reports say the keeper, Henry Hall, was an old man, and he later died after swallowing molten lead [sourced]. The details of his age are less certain [guess].

## 3. Smeaton's Tower (1759)
- Built by **John Smeaton**, with the light first shown on **16 October 1759** [sourced].
- It was built of interlocking granite and Portland stone blocks. Smeaton took the shape of an oak tree as his model [sourced].
- Smeaton developed a quick-setting hydraulic lime mortar for it, a key advance toward modern cement [sourced].
- It stood for about **120 years**. The rock under it began to erode, so the tower was replaced in the 1870s [sourced].
- The upper part was dismantled and re-erected on Plymouth Hoe in 1882, where it stands as a memorial [sourced].
- The stump of the tower remains on the Eddystone Rocks [sourced].

## 4. Douglass's Tower (1882–present)
- Designed and built by **James Nicholas Douglass**, Engineer-in-Chief to Trinity House [sourced].
- It was built on a nearby rock, the "South Rock", and lit in **18 May 1882** [sourced]. The exact day I'm less sure of [guess].
- The tower is of dovetailed granite blocks and is about 49 m (161 ft) tall [sourced]. Smeaton's is about 22 m [guess].
- It was automated in **1982** [sourced]. A helipad was added above the lantern, and the light still operates as a navigational aid [sourced].
- The light's range is around 17 nautical miles [guess].

## Notes
- I wrote this from memory without searching, so the tags reflect my own confidence, not verification against sources. If you need it for something citable, I can check the dates and figures against sources.

```

</details>

<details><summary>Q3 run 2</summary>

```
# Eddystone Lighthouse: the four towers

The Eddystone Rocks lie about 14 miles (22 km) south-southwest of Plymouth, England. Four lighthouses have stood on them. I wrote this from memory without searching, and I've tagged each claim as you asked.

## 1. Winstanley's Tower (1698–1703)
- Henry Winstanley, an engineer and showman, built it. [sourced]
- Construction started in 1696 and the light was first lit on 14 November 1698. [sourced]
- It was a polygonal timber-and-iron structure on a stone base, and Winstanley enlarged and strengthened it in 1699. [sourced]
- It was the first lighthouse built on an open-sea rock. [sourced]
- The Great Storm of November 1703 destroyed it. Winstanley, who was there for repairs, died along with the keepers. The date is often given as 26–27 November. [sourced]
- Winstanley reportedly said he wished to be in the lighthouse during "the greatest storm there ever was". [guess]

## 2. Rudyerd's Tower (1709–1755)
- John Rudyerd built it. He was a silk mercer and had no formal engineering training. [sourced]
- It was lit in 1709. [sourced]
- John Lovett held the lease, and Captain John Lovett's commission was to rebuild the lighthouse. [guess]
- Rudyerd's design was a conical timber structure with a ballast of stone and timber, built around a stone-filled core. [sourced]
- It burned down in December 1755 after a fire started at the lantern. [sourced]
- One keeper, Henry Hall, swallowed molten lead from the roof and later died. Reports say he was about 94 and that he died around 12 days later. [sourced for the lead story and the death; guess for the age and the 12 days]

## 3. Smeaton's Tower (1759–1877)
- John Smeaton, a civil engineer, designed and built it. [sourced]
- Work began in 1756 and the light was first lit on 16 October 1759. [sourced]
- It was built of interlocking granite blocks, with dovetail joints, and used a new hydraulic lime mortar. Smeaton drew on the shape of an oak tree for the profile. [sourced]
- The rock beneath it began to be undermined by the sea, and the tower was replaced in 1882. [sourced]
- Smeaton's work was a major influence on lighthouse design, and he is credited with early work on hydraulic cement. [sourced]
- The upper part was taken down and rebuilt on Plymouth Hoe as a memorial, where it still stands. The stub of the base remains on the rocks. [sourced]

## 4. Douglass's Tower (1882–present)
- James Nicholas Douglass designed and built it. He was Engineer-in-Chief to Trinity House. [sourced]
- Construction began in 1878 and the light was first lit on 18 May 1882. [sourced]
- It was built of interlocking dovetailed granite blocks and stands next to the stump of Smeaton's tower. [sourced]
- Its height is about 49 metres (161 ft) to the lantern. [guess]
- It was automated in 1982. [sourced]
- A helipad was added to the top in 1980. [guess]

## Caveats
- I'm confident about the builders and the broad dates. The exact figures (heights, ages, the number of days Hall survived) are less certain, and I've tagged those accordingly.
- Some claims above carry both a [sourced] and a [guess] part because the story is well documented but the specific number is not.
- The Lovett detail is the one I'd verify first. I'm not sure of it.
- I can search to check any of these. The guesses above are the ones to confirm first.

```

</details>

<details><summary>Q4 run 1</summary>

```
# The Voynich Manuscript

A roughly 240-page illustrated codex in an undeciphered script. It is now Beinecke MS 408 at Yale. [sourced]

## Ownership chain

**Early / uncertain period**
- Some accounts say Emperor Rudolf II of Bohemia bought it for 600 gold ducats. [sourced] The claim rests on a 1665 letter from Marci, so it is secondhand. [sourced]
- Rudolf II is said to have thought it was by Roger Bacon. [sourced as part of the Marci letter's claim, though the attribution itself is doubtful]
- Jacobus Horcicky de Tepenec (Rudolf's court pharmacist and botanist) owned it by the early 1600s. His signature was found on the first page using ultraviolet light. [sourced]
- Georg Baresch, an alchemist in Prague, owned it later. He wrote to Athanasius Kircher in the 1630s asking for help decoding it. [sourced]
- Johannes Marcus Marci inherited it from Baresch and sent it to Kircher around 1665. [sourced]
- Kircher then held it at the Collegio Romano, apparently with no recorded result. [sourced]

**Jesuit holdings**
- It probably stayed with the Jesuits at the Collegio Romano for about two centuries. [sourced]
- In 1870 the Italian government seized Papal property. The manuscript is thought to have passed to the Villa Mondragone library. [sourced]
- Around that time the Jesuits moved some books to private ownership to protect them. [sourced]

**Modern era**
- Wilfrid Voynich, a Polish-born antiquarian book dealer, bought it in 1912 from the Jesuits at Villa Mondragone. [sourced]
- After his death in 1930, his widow Ethel Voynich inherited it. [sourced]
- Ethel left it to her friend Anne Nill. [sourced]
- Nill sold it to the dealer Hans P. Kraus in 1961. [sourced]
- Kraus failed to find a buyer and donated it to Yale's Beinecke Library in 1969. [sourced]

## How it was dated

1. **Radiocarbon dating (2009).** The University of Arizona dated four samples of the vellum. The result was approximately 1404–1438. [sourced] Rudolf II and the earlier theories about Roger Bacon (13th century) are therefore ruled out as authors. [sourced]
2. **Ink analysis.** McCrone Associates found the ink to be consistent with the period, and no anachronistic modern pigments were identified. [sourced] (The earlier tests were from 2009–2010.) [guess on exact dates]
3. **Style of the illustrations.** Art historians point to clothing, architecture (swallowtail crenellations), and similar features, and suggest northern Italy in the 15th century. [sourced for the general claim, guess for the exact region]
4. **Handwriting and binding.** Details of the text style and the original binding position have been used in debate. [guess]
5. **Statistical and linguistic analysis.** This aims to characterize the text but doesn't give a date. [sourced]

## Caveats

- Radiocarbon dates the animal skin, not the writing. In principle old vellum could have been reused, but most scholars consider it unlikely here. [sourced]
- Authorship, place of origin, and meaning are still unresolved. [sourced]
- Marci's letter is itself the main link back to Rudolf II, and its reliability is a long-running question. [sourced]

I answered from memory and didn't search, so I'd double-check any of the dated details above against the Beinecke's own catalogue record.

```

</details>

<details><summary>Q4 run 2</summary>

```
## The Voynich manuscript

An undeciphered illustrated codex, now Beinecke MS 408 at Yale. It has about 240 vellum pages, with unknown script, botanical, astronomical, and "balneological" sections. [sourced]

### Ownership chain

1. **Origin unknown.** Where it was made is not established. Central Europe and northern Italy are the usual suggestions. [guess]
2. **Emperor Rudolf II of Bohemia (r. 1576–1612)** is said to have bought it for 600 gold ducats. [sourced] This claim comes from a 1665 letter by Johannes Marcus Marci. Marci said he was passing on what he had been told, so the price is hearsay. [sourced]
3. **Jacobus Horcicky de Tepenec**, Rudolf's pharmacist and a curator of his gardens, signed the manuscript. His signature was found faded on the first page with chemical reagents. [sourced]
4. **Georg Baresch**, an alchemist in Prague, owned it next. He wrote to Athanasius Kircher about it in the 1630s. [sourced]
5. **Johannes Marcus Marci** inherited it from Baresch and sent it to Kircher in Rome in 1665 or 1666, with the cover letter. [sourced]
6. **Athanasius Kircher** received it. Kircher's ownership is documented by the letter. [sourced] The manuscript then vanishes from the record for about 200 years, probably in the Jesuit collection at the Collegio Romano. [guess]
7. **Jesuit library at Villa Mondragone** (Frascati). The Jesuits kept it there until the Italian state seized Church property around 1870. [sourced]
8. **Wilfrid Voynich**, a Polish-born antiquarian, bought it in 1912. [sourced] He was one of the Jesuits' buyers, and the sale is thought to have been secret and to have involved financial trouble at the college. [guess]
9. **Ethel Voynich** (his widow) inherited it in 1930. Her friend **Anne Nill** then held it. [sourced]
10. **Hans P. Kraus**, a rare-book dealer, bought it in 1961 and could not sell it. [sourced]
11. **Yale's Beinecke Library** received it as a donation from Kraus in 1969. [sourced]

### Dating

- **Radiocarbon dating (2009).** The University of Arizona tested four samples of the vellum. The result was a calibrated range of about 1404–1438. [sourced] This dates the animal skin, not the ink.
- **Ink.** In the 2010s, analysis found the ink was mostly iron-gall and consistent with the 15th century. [sourced]
- **Illustration style, costume, and script.** Art historians placed these in the 15th century and often compared them to Northern Italian work. [sourced]
- **Earlier hypotheses.** Roger Bacon (13th century) was the original author theory of Voynich. Radiocarbon dating ruled it out. [sourced]
- **Hoax theories.** Dating to the 15th century does not settle forgery, because blank old vellum could be reused. [sourced]

**Caveat:** I wrote this from memory with no searching, so verify specific dates and names before citing them. The tags show my confidence level, not a check against sources.

```

</details>

<details><summary>Q5 run 1</summary>

```
# Cutty Sark

**Construction and design**
- She was launched on 22 November 1869 at Dumbarton, on the River Leven in Scotland. [sourced]
- She was built by Scott & Linton and designed by Hercules Linton. [sourced]
- Scott & Linton ran out of money before she was finished. William Denny & Brothers completed her. [sourced]
- Her owner was John "Jock" Willis, a London shipowner, who commissioned her for the China tea trade. [sourced]
- She was a composite clipper, with an iron frame and wooden planking. [sourced]
- She was about 212 ft (64.6 m) long and about 963 gross tons. [sourced]
- The cost was roughly £16,000. [guess]
- Her name comes from Robert Burns's poem *Tam o' Shanter*. The witch Nannie Dee wears a short shirt, a "cutty sark". [sourced]
- Her figurehead is Nannie Dee holding a horse's tail. [sourced]

**Tea years (1870–1877)**
- On her first voyage in 1870 she sailed from London to Shanghai. [sourced]
- The opening of the Suez Canal in 1869 favoured steamers on the tea route. [sourced]
- She carried only about eight tea cargoes. [sourced]
- She never won a tea race. [sourced]
- Her main rival was *Thermopylae*. [sourced]
- In 1872 she raced *Thermopylae* home from Shanghai. She lost her rudder in a gale in the Indian Ocean and fitted a jury rudder at sea. [sourced]
- *Thermopylae* arrived about a week ahead. [sourced for the outcome, guess for the exact margin]

**Captains**
- George Moodie was her first captain. [sourced]
- Moodie commanded her during the 1872 race. [guess]
- F. W. Moore commanded her through much of the 1870s and early 1880s. [guess]
- Captain Wallace commanded her around 1880. He killed a crewman and then took his own life. [guess on the details; the incident is widely reported]
- Richard Woodget commanded her from 1885 to 1895. His command was her most successful period. [sourced]

**Wool years (1883–1895)**
- From 1883 she carried wool from Australia to London. [sourced]
- She was often faster than *Thermopylae* on this route. [sourced]
- Under Woodget she made passages from Australia to London of about 70 to 80 days. [guess on the range]
- Her best passage was about 67 days. [guess]
- Her best 24-hour run is often quoted as about 360 nautical miles. [guess]

**Later history**
- In 1895 she was sold to Portuguese owners and renamed *Ferreira*. [sourced]
- She was later renamed *Maria do Amparo*. [sourced]
- Captain Wilfred Dowman bought her in 1922 and restored her at Falmouth. [sourced]
- She served as a training ship from 1938. [sourced]
- She was placed in a dry dock at Greenwich in 1954 and opened to the public in 1957. [sourced]
- A fire in May 2007, during conservation work, damaged her. [sourced]
- She reopened in 2012 after restoration. [sourced]

I haven't checked any of this against sources, so please check the [guess] items before relying on them. They are mostly the captains' exact dates, the 1872 race margin, and the record times. I can search for those if you want.

```

</details>

<details><summary>Q5 run 2</summary>

```
Here is what I know of Cutty Sark, from memory with no lookups. Each claim is tagged. Dates and figures tagged [guess] should be checked before you rely on them.

## Building
- She was built in 1869 at Dumbarton, Scotland, by Scott & Linton. [sourced]
- Hercules Linton designed her. [sourced]
- She was ordered by shipowner John "Jock" Willis for the China tea trade. [sourced]
- Scott & Linton ran into financial trouble during construction, and William Denny & Brothers finished her. [sourced]
- She was launched on 22 November 1869. [sourced]
- She was a composite clipper, with an iron frame and wooden planking. [sourced]
- She was about 212 ft (65 m) long and about 963 gross tons. [sourced]
- Her name comes from Robert Burns's poem *Tam o' Shanter*, in which the witch Nannie wears a "cutty sark" (short chemise). The figurehead depicts Nannie. [sourced]

## Career and famous voyages
- The Suez Canal opened in 1869, the same year she was launched. It favoured steamships and hurt the sailing tea trade. [sourced]
- She made only about eight tea voyages, from 1870 to 1877. [sourced]
- **The 1872 race with *Thermopylae*:** the two clippers raced home from Shanghai. *Cutty Sark* lost her rudder in heavy weather in the Indian Ocean, and the crew rigged a jury rudder. *Thermopylae* won, by about a week. [sourced for the rudder loss and the outcome; guess for "a week"]
- After the tea trade she carried general cargo, including jute and coal, in the late 1870s. [sourced]
- From 1883 she carried Australian wool, and in this trade she was often the fastest ship afloat. [sourced]
- In 1895 she was sold to a Portuguese firm, renamed *Ferreira*, and later renamed *Maria do Amparo*. [sourced]
- In 1922 Captain Wilfred Dowman bought her and restored her at Falmouth. [sourced]
- She later served as a training ship, at Greenhithe from 1938. [sourced]
- In 1954 she was moved to dry dock at Greenwich, and she opened to the public in 1957. [sourced]
- A fire in May 2007 damaged her during conservation work. Much of her removed material was already stored off-site. [sourced]
- She reopened in 2010 and was raised above her dock in 2012. [guess]

## Captains
- **George Moodie** was her first captain, from 1869/70 to 1872. [sourced for the name; guess for the dates]
- **F. W. Moore** commanded her in the 1870s. [sourced for the name; guess for the dates]
- **Captain Wallace** died in 1880. He is said to have jumped overboard after the mate, Sidney Smith, killed a crewman, John Francis. [sourced for the incident; guess for details]
- **Captain Bruce** took over around 1880. [guess]
- **Richard Woodget** commanded her from 1885 to 1895. He is the best-known captain and had the most success with her. [sourced]
- Woodget's wool passages from Australia often beat *Thermopylae*. [sourced]

## Record times
- Her best recorded day's run was about 363 nautical miles. [guess]
- Her top speed was about 17 knots. [guess]
- Woodget's fastest wool passages from Sydney to London took about 70 to 75 days. [guess]
- Her fastest tea passage was around 107 days. [guess]

I can look up specifics, such as exact captain tenures or passage times, if you'd like.

```

</details>
