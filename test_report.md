# Test report: do AI's own [guess] labels flag its mistakes?

**Claim tested:** when an AI marks its own statements [sourced] or [guess], the [guess] ones are wrong much more often than the [sourced] ones.

**Verdict: no image made.** After a second round (10 more, harder questions), the gap shrank a lot. The only clear gap comes from one question (Cutty Sark). See "Judgment".

## Method

- Tool: `claude -p "<question> <suffix>" < /dev/null`, each run from a fresh empty temp directory (Claude Code 2.1.294, default model). The model said every time that it answered from memory with no search.
- Suffix, used word for word after every question: `For every specific claim, add [sourced] if you are confident it is well documented, or [guess] if you are not sure.`
- **Round 1:** 5 history questions (Q1 to Q5). **Round 2:** 10 more, picked to be more obscure and number-heavy (Q6 to Q15). 2 runs each, so 30 raw outputs in `test_log/` (`q1_run1.txt` ... `q15_run2.txt`), saved untouched.
- Every labelled concrete claim was split out and checked against web sources. Verdicts: **right (T)**, **wrong (F)**, **cannot confirm (U)**. U is left out of all error rates.
- Left out as not checkable: vague or opinion lines (for example "exact cause is still debated"), and headings.
- Lines with several parts were split only when the parts got different verdicts; otherwise kept as one claim.

### Limits you should know

- **I could not open the original web pages.** The page-fetch tool failed with a DNS error on every site I tried (Wikipedia, Britannica, voynich.nu), in both rounds, and direct curl was blocked. So all checks use **web search result summaries**, and the links in the tables are the pages those searches returned. Search summaries can be wrong, and they sometimes repeat my own query back as if confirmed. I only marked a claim right when the summary gave its own support.
- As a result, many true-but-unlisted facts came back as **cannot confirm**: 61 of 99 [guess] claims (61.6%) and 310 of 652 [sourced] claims (47.5%). The [guess] claims were hit harder, and they are the ones that matter here, so the [guess] sample is thin.
- Where sources disagreed (tank size, witness counts, death tolls), the claim was marked U, not T or F, unless the claim fit the usual range.
- Round 2 did not give "more errors": the model was right on most of the checkable claims, even on obscure topics.

## Summary

| Label | Claims | Checked (T+F) | Wrong | Wrong rate | Cannot confirm | Wrong claims by question |
|---|---|---|---|---|---|---|
| [guess] | 99 | 38 | 3 | 7.9% | 61 | Q5: 3 |
| [sourced] | 652 | 342 | 6 | 1.8% | 310 | Q2: 2, Q6: 2, Q10: 1, Q12: 1 |

Fisher exact test over all claims: p = 0.051. It is borderline, and it counts claims from the same question as if they were independent.

### Does one question drive the result?

| Subset | [guess] wrong | [sourced] wrong | Fisher p |
|---|---|---|---|
| All 15 questions | 3 of 38 (7.9%) | 6 of 342 (1.8%) | 0.051 |
| Round 1 only (Q1-Q5) | 3 of 21 (14.3%) | 2 of 136 (1.5%) | 0.017 |
| Round 2 only (Q6-Q15) | 0 of 17 (0.0%) | 4 of 206 (1.9%) | 1.000 |
| All except Q5 (Cutty Sark) | 0 of 27 (0.0%) | 6 of 315 (1.9%) | 1.000 |

### By question

| Question | [guess] checked | [guess] wrong | [sourced] checked | [sourced] wrong |
|---|---|---|---|---|
| Q1 R101 airship crash (1930) | 3 | 0 | 27 | 0 |
| Q2 Great Molasses Flood (Boston, 1919) | 2 | 0 | 32 | 2 |
| Q3 Eddystone Lighthouse: the four towers | 5 | 0 | 26 | 0 |
| Q4 Voynich manuscript: owners and dating | 0 | 0 | 24 | 0 |
| Q5 Clipper ship Cutty Sark | 11 | 3 | 27 | 0 |
| Q6 Tay Bridge disaster (1879) | 2 | 0 | 26 | 2 |
| Q7 Anglo-Zanzibar War (1896) | 1 | 0 | 20 | 0 |
| Q8 Eastland disaster (1915) | 3 | 0 | 18 | 0 |
| Q9 Great Stink of London (1858) | 3 | 0 | 11 | 0 |
| Q10 Quebec Bridge collapses (1907, 1916) | 0 | 0 | 25 | 1 |
| Q11 Peshtigo Fire (1871) | 3 | 0 | 23 | 0 |
| Q12 Ronan Point collapse (1968) | 0 | 0 | 25 | 1 |
| Q13 Building of Hoover Dam | 1 | 0 | 17 | 0 |
| Q14 Tacoma Narrows Bridge collapse (1940) | 1 | 0 | 24 | 0 |
| Q15 Johnstown Flood (1889) | 3 | 0 | 17 | 0 |

### Surprises (kept in, not hidden)

All 9 wrong claims:

- Q2 run 2, [sourced]: "Case was "Dorothy Ann Kelley et al. v. United States Industrial Alcohol Co."" (the lead case was Dorr v. United States Industrial Alcohol Co.; no "Kelley" found)
- Q2 run 2, [sourced]: "About 3,000 pages of testimony" (sources say 25,000 to 45,000 pages)
- Q5 run 1, [guess]: "F. W. Moore commanded through much of the 1870s and early 1880s" (Moore 1872-73; Tiptaft 1874-78; Wallace 1878-80; Bruce 1880-82)
- Q5 run 1, [guess]: "Captain Wallace killed a crewman, then took his own life" (the mate, Sidney Smith, killed the crewman; Wallace jumped overboard)
- Q5 run 2, [guess]: "She reopened in 2010 and was raised in 2012" (reopened 25 April 2012)
- Q6 run 1, [sourced]: "Train was a small tank locomotive (NBR No. 224) with six carriages" (sources: a 4-4-0 tender engine, five carriages and a luggage van)
- Q6 run 1, [sourced]: "Rothery wrote the main findings; Barlow and Yolland signed a separate, more cautious report" (reversed: Yolland and Barlow issued the main report, Rothery a separate one blaming Bouch)
- Q10 run 2, [sourced]: "Bridge finished and opened to traffic in December 1919" (completed 1917; officially inaugurated Aug 1919)
- Q12 run 1, [sourced]: "Other members Pugsley and Skempton" (members were Pugsley and Saunders; no Skempton found)

- **6 of the 9 wrong claims were tagged [sourced].** Two of them (Q2 run 2) were confident legal details: a wrong case name, and a page count about 8 to 15 times too small.
- **All 3 wrong [guess] claims came from Q5 (Cutty Sark).** Across the 10 questions of round 2, **no checkable [guess] claim was wrong** (0 of 17).
- Round 2 was meant to produce more errors. It did not: 4 wrong claims out of 206 checked [sourced] claims.
- The model labelled few claims [guess]: 99 against 652 [sourced].
- In Q6 the two runs of the same question gave opposite versions of who wrote which Tay Bridge inquiry report. The reversed one was tagged [sourced].

## Judgment

- Over all 15 questions: [guess] wrong **7.9%** (3 of 38), [sourced] wrong **1.8%** (6 of 342). p = 0.051.
- **Without Q5 the [guess] error rate is 0 of 27.** The whole gap rests on 3 claims in one question. In round 2 alone it is 0 of 17 for [guess], against 1.9% for [sourced].
- That is not strong enough to say "[guess] labels flag the errors". It is also not enough to say they don't. The fair summary: **in this test the [guess] labels did not reliably point at mistakes.** Most errors (6 of 9) carried a [sourced] tag.
- Your rule was to stop if the result is still not solid. **I did not make the image.**

One thing the data does support: "Most of the AI's mistakes were tagged [sourced]." That is 6 of 9 wrong claims. It would need an honest note about how small the sample is (9 wrong claims) and about the cannot-confirm pile.

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

### Q6. Tay Bridge disaster (1879)

**Run 1** (raw output: `test_log/q6_run1.txt`)

| # | Claim | Label | Result | Note | Sources |
|---|---|---|---|---|---|
| 1 | Collapsed night of Sunday 28 December 1879 | [sourced] | cannot confirm |  | none found |
| 2 | Happened in a violent storm | [sourced] | cannot confirm |  | none found |
| 3 | Bridge crossed the Firth of Tay between Wormit and Dundee | [sourced] | cannot confirm |  | none found |
| 4 | The "High Girders" section fell with the train | [sourced] | cannot confirm |  | none found |
| 5 | Evening mail train from Burntisland to Dundee | [sourced] | right |  | [TAY1](https://en.wikipedia.org/wiki/Tay_Bridge_disaster) |
| 6 | Train run by the North British Railway | [sourced] | right |  | [TAY1](https://en.wikipedia.org/wiki/Tay_Bridge_disaster) |
| 7 | Train was a small tank locomotive (NBR No. 224) with six carriages | [sourced] | **WRONG** | sources: a 4-4-0 tender engine, five carriages and a luggage van | [TAY1](https://en.wikipedia.org/wiki/Tay_Bridge_disaster) |
| 8 | Locomotive recovered from the river and returned to service | [sourced] | right |  | [TAY1](https://en.wikipedia.org/wiki/Tay_Bridge_disaster) |
| 9 | Train came from Edinburgh with change at Burntisland and St Fort | [guess] | cannot confirm |  | none found |
| 10 | No one survived | [sourced] | right |  | [TAY1](https://en.wikipedia.org/wiki/Tay_Bridge_disaster), [TAY2](https://www.leisureandculturedundee.com/tay-rail-bridge-disaster-1879) |
| 11 | Usual death figure is about 75 | [sourced] | right |  | [TAY1](https://en.wikipedia.org/wiki/Tay_Bridge_disaster), [TAY2](https://www.leisureandculturedundee.com/tay-rail-bridge-disaster-1879) |
| 12 | Only 46 bodies recovered | [sourced] | right |  | [TAY2](https://www.leisureandculturedundee.com/tay-rail-bridge-disaster-1879) |
| 13 | Toll may be as low as 59 | [guess] | right |  | [TAY2](https://www.leisureandculturedundee.com/tay-rail-bridge-disaster-1879) |
| 14 | Sir Thomas Bouch designed the bridge | [sourced] | right |  | [TAY1](https://en.wikipedia.org/wiki/Tay_Bridge_disaster) |
| 15 | Cast-iron columns, wrought-iron girders on brick and masonry piers | [sourced] | cannot confirm |  | none found |
| 16 | Bridge opened in 1878 | [sourced] | cannot confirm |  | none found |
| 17 | Queen Victoria crossed in June 1879; Bouch knighted | [sourced] | cannot confirm |  | none found |
| 18 | High Girders contractor was Hopkins Gilkes | [guess] | cannot confirm |  | none found |
| 19 | Cast iron made at Wormit foundry run by Hopkins Gilkes | [guess] | cannot confirm |  | none found |
| 20 | Court of Inquiry sat in 1880 | [sourced] | right | report issued June 1880 | [TAY3](https://www.thecourier.co.uk/fp/past-times/1393289/the-tay-rail-bridge-disaster-report-published-140-years-ago-which-ruined-engineer-sir-thomas-bouchs-reputation/) |
| 21 | Members: Rothery, Yolland, Barlow | [sourced] | right |  | [TAY1](https://en.wikipedia.org/wiki/Tay_Bridge_disaster), [TAY3](https://www.thecourier.co.uk/fp/past-times/1393289/the-tay-rail-bridge-disaster-report-published-140-years-ago-which-ruined-engineer-sir-thomas-bouchs-reputation/) |
| 22 | Bouch found chiefly to blame for design, construction, maintenance | [sourced] | right |  | [TAY3](https://www.thecourier.co.uk/fp/past-times/1393289/the-tay-rail-bridge-disaster-report-published-140-years-ago-which-ruined-engineer-sir-thomas-bouchs-reputation/) |
| 23 | Design did not properly allow for wind pressure | [sourced] | cannot confirm |  | none found |
| 24 | Rothery wrote the main findings; Barlow and Yolland signed a separate, more cautious report | [sourced] | **WRONG** | reversed: Yolland and Barlow issued the main report, Rothery a separate one blaming Bouch | [TAY3](https://www.thecourier.co.uk/fp/past-times/1393289/the-tay-rail-bridge-disaster-report-published-140-years-ago-which-ruined-engineer-sir-thomas-bouchs-reputation/) |
| 25 | Yolland and Barlow's report was more cautious about wind | [guess] | cannot confirm |  | none found |
| 26 | Inquiry criticised foundry quality control; lugs were a weak point | [sourced] | cannot confirm |  | none found |
| 27 | Later reanalysis suggests fatigue and fractures | [guess] | cannot confirm |  | none found |
| 28 | Bouch's reputation ruined; died in 1880 months after report | [sourced] | right |  | [TAY3](https://www.thecourier.co.uk/fp/past-times/1393289/the-tay-rail-bridge-disaster-report-published-140-years-ago-which-ruined-engineer-sir-thomas-bouchs-reputation/) |
| 29 | Disaster changed how wind loading was treated | [sourced] | cannot confirm |  | none found |
| 30 | Replacement built alongside using the surviving piers | [sourced] | cannot confirm | opening 1887 confirmed; reuse of piers not | [TAY1](https://en.wikipedia.org/wiki/Tay_Bridge_disaster) |

**Run 2** (raw output: `test_log/q6_run2.txt`)

| # | Claim | Label | Result | Note | Sources |
|---|---|---|---|---|---|
| 1 | Collapsed Sunday 28 December 1879 in a storm | [sourced] | cannot confirm |  | none found |
| 2 | Collapse at about 7:15 pm | [sourced] | cannot confirm |  | none found |
| 3 | Bridge crossed the Tay between Wormit and Dundee | [sourced] | cannot confirm |  | none found |
| 4 | NBR passenger train from Burntisland to Dundee | [sourced] | right |  | [TAY1](https://en.wikipedia.org/wiki/Tay_Bridge_disaster) |
| 5 | Hauled by a 4-4-0 locomotive | [sourced] | right | number and builder not confirmed | [TAY1](https://en.wikipedia.org/wiki/Tay_Bridge_disaster) |
| 6 | Five or six carriages and a brake van | [sourced] | right | five carriages and a luggage van | [TAY1](https://en.wikipedia.org/wiki/Tay_Bridge_disaster) |
| 7 | Locomotive recovered and returned to service | [sourced] | right |  | [TAY1](https://en.wikipedia.org/wiki/Tay_Bridge_disaster) |
| 8 | Commonly cited toll is 75 | [sourced] | right |  | [TAY1](https://en.wikipedia.org/wiki/Tay_Bridge_disaster), [TAY2](https://www.leisureandculturedundee.com/tay-rail-bridge-disaster-1879) |
| 9 | No full passenger list because tickets were collected earlier | [sourced] | cannot confirm |  | none found |
| 10 | Estimates range from about 59 to 75 | [guess] | right |  | [TAY2](https://www.leisureandculturedundee.com/tay-rail-bridge-disaster-1879) |
| 11 | Recent research names roughly 60 victims | [guess] | cannot confirm |  | none found |
| 12 | No survivors | [sourced] | right |  | [TAY1](https://en.wikipedia.org/wiki/Tay_Bridge_disaster) |
| 13 | Only 46 bodies recovered | [sourced] | right |  | [TAY2](https://www.leisureandculturedundee.com/tay-rail-bridge-disaster-1879) |
| 14 | Designed by Sir Thomas Bouch | [sourced] | right |  | [TAY1](https://en.wikipedia.org/wiki/Tay_Bridge_disaster) |
| 15 | Bouch knighted after the bridge opened | [sourced] | cannot confirm |  | none found |
| 16 | Bridge almost two miles long (3,150 yards) | [sourced] | cannot confirm |  | none found |
| 17 | Opened in 1878 | [sourced] | cannot confirm |  | none found |
| 18 | Contractor first de Bergue, then Hopkins Gilkes | [sourced] | cannot confirm |  | none found |
| 19 | Ironwork cast at a Wormit foundry set up by the contractor | [guess] | cannot confirm |  | none found |
| 20 | Inquiry sat in early 1880 | [sourced] | cannot confirm |  | none found |
| 21 | Three members: Rothery, Yolland, Barlow | [sourced] | right |  | [TAY1](https://en.wikipedia.org/wiki/Tay_Bridge_disaster), [TAY3](https://www.thecourier.co.uk/fp/past-times/1393289/the-tay-rail-bridge-disaster-report-published-140-years-ago-which-ruined-engineer-sir-thomas-bouchs-reputation/) |
| 22 | Bridge badly designed, built and maintained | [sourced] | right |  | [TAY3](https://www.thecourier.co.uk/fp/past-times/1393289/the-tay-rail-bridge-disaster-report-published-140-years-ago-which-ruined-engineer-sir-thomas-bouchs-reputation/) |
| 23 | Cast-iron lugs and bracing ties failed | [sourced] | cannot confirm |  | none found |
| 24 | Poor casting and inadequate inspection found | [sourced] | cannot confirm |  | none found |
| 25 | Yolland and Barlow's report blamed Bouch for design and wind; Rothery's separate report went further | [sourced] | right |  | [TAY3](https://www.thecourier.co.uk/fp/past-times/1393289/the-tay-rail-bridge-disaster-report-published-140-years-ago-which-ruined-engineer-sir-thomas-bouchs-reputation/) |
| 26 | Bouch ruined; died in 1880 | [sourced] | right |  | [TAY3](https://www.thecourier.co.uk/fp/past-times/1393289/the-tay-rail-bridge-disaster-report-published-140-years-ago-which-ruined-engineer-sir-thomas-bouchs-reputation/) |
| 27 | Bouch's Forth Bridge design abandoned | [sourced] | cannot confirm |  | none found |
| 28 | New bridge built alongside; opened 1887 | [sourced] | right |  | [TAY1](https://en.wikipedia.org/wiki/Tay_Bridge_disaster) |
| 29 | Wind loading became a formal factor afterward | [sourced] | cannot confirm |  | none found |

### Q7. Anglo-Zanzibar War (1896)

**Run 1** (raw output: `test_log/q7_run1.txt`)

| # | Claim | Label | Result | Note | Sources |
|---|---|---|---|---|---|
| 1 | Fought on 27 August 1896 | [sourced] | right |  | [ZAN1](https://en.wikipedia.org/wiki/Anglo-Zanzibar_War) |
| 2 | Ultimatum expired 09:00; bombardment began about then | [sourced] | right | Wikipedia: 09:02 | [ZAN1](https://en.wikipedia.org/wiki/Anglo-Zanzibar_War) |
| 3 | Ended after roughly 38 minutes | [sourced] | right |  | [ZAN1](https://en.wikipedia.org/wiki/Anglo-Zanzibar_War) |
| 4 | Some accounts say 40 to 45 minutes | [sourced] | right |  | [ZAN1](https://en.wikipedia.org/wiki/Anglo-Zanzibar_War) |
| 5 | Generally called the shortest war in history | [sourced] | right |  | [ZAN1](https://en.wikipedia.org/wiki/Anglo-Zanzibar_War) |
| 6 | Sultan Hamad died suddenly on 25 August 1896 | [sourced] | cannot confirm |  | none found |
| 7 | Khalid took the palace without British approval | [sourced] | cannot confirm |  | none found |
| 8 | 1890 agreement required consul's consent to a new sultan | [sourced] | cannot confirm |  | none found |
| 9 | Britain preferred Hammud bin Muhammed | [sourced] | cannot confirm |  | none found |
| 10 | Rumours say Khalid poisoned Hamad | [guess] | cannot confirm |  | none found |
| 11 | Hamad ruled 1893 to 1896 | [sourced] | cannot confirm |  | none found |
| 12 | Khalid held power about two days | [sourced] | cannot confirm |  | none found |
| 13 | Khalid took refuge in the German consulate | [sourced] | right | exile confirmed | [ZAN1](https://en.wikipedia.org/wiki/Anglo-Zanzibar_War) |
| 14 | British captured Khalid in 1916 and exiled him | [sourced] | cannot confirm |  | none found |
| 15 | Hammud installed, ruled until 1902 | [sourced] | cannot confirm |  | none found |
| 16 | HMS St George was Rawson's flagship | [sourced] | right | St George led the flotilla | [ZAN1](https://en.wikipedia.org/wiki/Anglo-Zanzibar_War) |
| 17 | HMS Philomel took part | [sourced] | cannot confirm |  | none found |
| 18 | HMS Racoon took part | [sourced] | cannot confirm |  | none found |
| 19 | HMS Thrush took part | [sourced] | cannot confirm |  | none found |
| 20 | HMS Sparrow took part | [sourced] | cannot confirm |  | none found |
| 21 | Royal yacht Glasgow sunk in harbour | [sourced] | right |  | [ZAN1](https://en.wikipedia.org/wiki/Anglo-Zanzibar_War) |
| 22 | A small launch was also sunk | [guess] | right | two smaller boats destroyed | [ZAN1](https://en.wikipedia.org/wiki/Anglo-Zanzibar_War) |
| 23 | Mathews was first minister of the sultanate | [sourced] | cannot confirm |  | none found |
| 24 | About 500 Zanzibaris killed or wounded | [sourced] | right |  | [ZAN1](https://en.wikipedia.org/wiki/Anglo-Zanzibar_War) |
| 25 | One British petty officer wounded | [sourced] | right | one British wounded | [ZAN1](https://en.wikipedia.org/wiki/Anglo-Zanzibar_War) |
| 26 | Khalid had about 2,800 men | [sourced] | cannot confirm |  | none found |
| 27 | Palace and harbour buildings heavily damaged | [sourced] | cannot confirm |  | none found |

**Run 2** (raw output: `test_log/q7_run2.txt`)

| # | Claim | Label | Result | Note | Sources |
|---|---|---|---|---|---|
| 1 | Took place on 27 August 1896 | [sourced] | right |  | [ZAN1](https://en.wikipedia.org/wiki/Anglo-Zanzibar_War) |
| 2 | Ultimatum expired 9:00; bombardment began about 9:02 | [sourced] | right |  | [ZAN1](https://en.wikipedia.org/wiki/Anglo-Zanzibar_War) |
| 3 | Lasted roughly 38 to 45 minutes | [sourced] | right |  | [ZAN1](https://en.wikipedia.org/wiki/Anglo-Zanzibar_War) |
| 4 | Usually called shortest war in history | [sourced] | right |  | [ZAN1](https://en.wikipedia.org/wiki/Anglo-Zanzibar_War) |
| 5 | Hamad died 25 August 1896, poisoning suspected | [sourced] | cannot confirm |  | none found |
| 6 | Khalid seized palace without consul's approval | [sourced] | cannot confirm |  | none found |
| 7 | British wanted Hamud bin Muhammed | [sourced] | cannot confirm |  | none found |
| 8 | British demanded Khalid stand down; he refused | [sourced] | cannot confirm |  | none found |
| 9 | Khalid took refuge in German consulate | [sourced] | right |  | [ZAN1](https://en.wikipedia.org/wiki/Anglo-Zanzibar_War) |
| 10 | Khalid captured 1916, died 1927 | [guess] | cannot confirm |  | none found |
| 11 | Hamud ruled until 1902 | [sourced] | cannot confirm |  | none found |
| 12 | Rear Admiral Harry Rawson commanded British force | [sourced] | right |  | [ZAN1](https://en.wikipedia.org/wiki/Anglo-Zanzibar_War) |
| 13 | HMS St George was his flagship | [sourced] | right |  | [ZAN1](https://en.wikipedia.org/wiki/Anglo-Zanzibar_War) |
| 14 | Other ships: Philomel, Racoon, Thrush, Sparrow | [sourced] | cannot confirm |  | none found |
| 15 | Lloyd Mathews led Zanzibar army and backed the British | [sourced] | cannot confirm |  | none found |
| 16 | Royal Marines and sailors landed | [sourced] | cannot confirm |  | none found |
| 17 | Khalid's side had about 2,800 men | [guess] | cannot confirm |  | none found |
| 18 | Royal yacht Glasgow was sunk | [sourced] | right | masts visible not confirmed | [ZAN1](https://en.wikipedia.org/wiki/Anglo-Zanzibar_War) |
| 19 | Palace and harbour defences shelled | [sourced] | cannot confirm |  | none found |
| 20 | About 500 Zanzibaris killed or wounded | [sourced] | right |  | [ZAN1](https://en.wikipedia.org/wiki/Anglo-Zanzibar_War) |
| 21 | British had one man slightly wounded | [sourced] | right |  | [ZAN1](https://en.wikipedia.org/wiki/Anglo-Zanzibar_War) |

### Q8. Eastland disaster (1915)

**Run 1** (raw output: `test_log/q8_run1.txt`)

| # | Claim | Label | Result | Note | Sources |
|---|---|---|---|---|---|
| 1 | Eastland capsized on 24 July 1915 | [sourced] | right |  | [EAS1](https://www.smithsonianmag.com/history/eastland-disaster-killed-more-passengers-titanic-and-lusitania-why-has-it-been-forgotten-180953146/) |
| 2 | Rolled over tied to dock between Clark and LaSalle | [sourced] | cannot confirm |  | none found |
| 3 | Chartered for Western Electric picnic to Michigan City | [sourced] | cannot confirm |  | none found |
| 4 | 844 people died | [sourced] | right |  | [EAS1](https://www.smithsonianmag.com/history/eastland-disaster-killed-more-passengers-titanic-and-lusitania-why-has-it-been-forgotten-180953146/) |
| 5 | Many dead were children and young women | [sourced] | cannot confirm |  | none found |
| 6 | About 2,500 passengers aboard | [sourced] | right |  | [EAS1](https://www.smithsonianmag.com/history/eastland-disaster-killed-more-passengers-titanic-and-lusitania-why-has-it-been-forgotten-180953146/) |
| 7 | Certified capacity 2,570 | [sourced] | right |  | [EAS2](https://www.maritimequest.com/liners/eastland/ss_eastland_data.htm), [EAS4](https://www.history.navy.mil/research/histories/ship-histories/danfs/w/wilmette.html) |
| 8 | Passengers boarded faster than crew could manage balance | [sourced] | cannot confirm |  | none found |
| 9 | Built by Jenks Shipbuilding, Port Huron, in 1903 | [sourced] | right |  | [EAS2](https://www.maritimequest.com/liners/eastland/ss_eastland_data.htm), [EAS4](https://www.history.navy.mil/research/histories/ship-histories/danfs/w/wilmette.html) |
| 10 | Built for Michigan Steamship Company | [guess] | cannot confirm |  | none found |
| 11 | Top-heavy with a history of listing | [sourced] | cannot confirm |  | none found |
| 12 | Added lifeboats after Titanic made her less stable | [sourced] | cannot confirm |  | none found |
| 13 | Ballast handling contributed | [sourced] | cannot confirm |  | none found |
| 14 | Federal criminal charges brought against owners and officers | [sourced] | right |  | [EAS3](https://www.flowerintheriver.com/launch-to-tragedy/eastland-disaster-legal-proceedings) |
| 15 | Defendants included captain and chief engineer | [sourced] | cannot confirm |  | none found |
| 16 | Case heard in federal court at Grand Rapids in 1916 | [guess] | right |  | [EAS3](https://www.flowerintheriver.com/launch-to-tragedy/eastland-disaster-legal-proceedings) |
| 17 | Charges were conspiracy and negligence | [sourced] | cannot confirm |  | none found |
| 18 | Trial ended in acquittals | [sourced] | right |  | [EAS3](https://www.flowerintheriver.com/launch-to-tragedy/eastland-disaster-legal-proceedings) |
| 19 | Supreme Court held owners could limit liability to vessel value | [guess] | cannot confirm | no Supreme Court ruling found | [EAS3](https://www.flowerintheriver.com/launch-to-tragedy/eastland-disaster-legal-proceedings) |
| 20 | No convictions and little compensation | [sourced] | cannot confirm |  | none found |
| 21 | Ship sold to Navy, became gunboat USS Wilmette | [sourced] | right |  | [EAS2](https://www.maritimequest.com/liners/eastland/ss_eastland_data.htm), [EAS4](https://www.history.navy.mil/research/histories/ship-histories/danfs/w/wilmette.html) |
| 22 | Scrapped in 1947 | [sourced] | right |  | [EAS2](https://www.maritimequest.com/liners/eastland/ss_eastland_data.htm), [EAS4](https://www.history.navy.mil/research/histories/ship-histories/danfs/w/wilmette.html) |

**Run 2** (raw output: `test_log/q8_run2.txt`)

| # | Claim | Label | Result | Note | Sources |
|---|---|---|---|---|---|
| 1 | Capsized 24 July 1915 in the Chicago River | [sourced] | right |  | [EAS1](https://www.smithsonianmag.com/history/eastland-disaster-killed-more-passengers-titanic-and-lusitania-why-has-it-been-forgotten-180953146/) |
| 2 | Western Electric employees headed to Michigan City picnic | [sourced] | cannot confirm |  | none found |
| 3 | 844 died | [sourced] | right |  | [EAS1](https://www.smithsonianmag.com/history/eastland-disaster-killed-more-passengers-titanic-and-lusitania-why-has-it-been-forgotten-180953146/) |
| 4 | 841 passengers and 3 crew | [guess] | cannot confirm |  | none found |
| 5 | 22 entire families died | [guess] | cannot confirm |  | none found |
| 6 | Largest Great Lakes shipwreck loss of life | [sourced] | right |  | [EAS1](https://www.smithsonianmag.com/history/eastland-disaster-killed-more-passengers-titanic-and-lusitania-why-has-it-been-forgotten-180953146/) |
| 7 | Many victims were young women of Czech descent | [sourced] | cannot confirm |  | none found |
| 8 | About 2,500 passengers aboard | [sourced] | right |  | [EAS1](https://www.smithsonianmag.com/history/eastland-disaster-killed-more-passengers-titanic-and-lusitania-why-has-it-been-forgotten-180953146/) |
| 9 | Rated capacity 2,570 | [sourced] | right |  | [EAS2](https://www.maritimequest.com/liners/eastland/ss_eastland_data.htm), [EAS4](https://www.history.navy.mil/research/histories/ship-histories/danfs/w/wilmette.html) |
| 10 | Roughly 2,572 people incl. crew | [guess] | right | Smithsonian: 2,573 | [EAS1](https://www.smithsonianmag.com/history/eastland-disaster-killed-more-passengers-titanic-and-lusitania-why-has-it-been-forgotten-180953146/) |
| 11 | Built by Jenks, Port Huron; launched 1903 | [sourced] | right |  | [EAS2](https://www.maritimequest.com/liners/eastland/ss_eastland_data.htm), [EAS4](https://www.history.navy.mil/research/histories/ship-histories/danfs/w/wilmette.html) |
| 12 | Top-heavy with history of listing | [sourced] | cannot confirm |  | none found |
| 13 | Lifeboats added after Titanic; ballast handling a factor | [sourced] | cannot confirm |  | none found |
| 14 | Federal criminal charges against owners and officers | [sourced] | right |  | [EAS3](https://www.flowerintheriver.com/launch-to-tragedy/eastland-disaster-legal-proceedings) |
| 15 | Charges were conspiracy and negligence | [guess] | cannot confirm |  | none found |
| 16 | 1916 criminal trial ended in acquittal | [sourced] | right |  | [EAS3](https://www.flowerintheriver.com/launch-to-tragedy/eastland-disaster-legal-proceedings) |
| 17 | In 1917 a federal judge dismissed the case | [guess] | cannot confirm |  | none found |
| 18 | Courts ruled owners not liable for damages | [guess] | cannot confirm | sources: liability limited to salvage value | [EAS3](https://www.flowerintheriver.com/launch-to-tragedy/eastland-disaster-legal-proceedings) |
| 19 | Families received little or no compensation | [sourced] | cannot confirm |  | none found |
| 20 | Navy renamed her USS Wilmette | [sourced] | right |  | [EAS2](https://www.maritimequest.com/liners/eastland/ss_eastland_data.htm), [EAS4](https://www.history.navy.mil/research/histories/ship-histories/danfs/w/wilmette.html) |
| 21 | Scrapped in 1947 | [guess] | right |  | [EAS2](https://www.maritimequest.com/liners/eastland/ss_eastland_data.htm), [EAS4](https://www.history.navy.mil/research/histories/ship-histories/danfs/w/wilmette.html) |

### Q9. Great Stink of London (1858)

**Run 1** (raw output: `test_log/q9_run1.txt`)

| # | Claim | Label | Result | Note | Sources |
|---|---|---|---|---|---|
| 1 | Stink peaked in hot summer of 1858 | [sourced] | right |  | [STK1](https://www.londonmuseum.org.uk/collections/london-stories/great-stink-of-1858/) |
| 2 | Sewage from a city of 2.5-3 million | [sourced] | cannot confirm |  | none found |
| 3 | Cholera outbreaks 1848-49 and 1853-54; miasma theory | [sourced] | cannot confirm |  | none found |
| 4 | Lime-chloride curtains hung at Parliament | [sourced] | cannot confirm |  | none found |
| 5 | Disraeli fled committee room | [sourced] | cannot confirm |  | none found |
| 6 | Parliament passed enabling act in 1858 | [sourced] | right |  | [STK1](https://www.londonmuseum.org.uk/collections/london-stories/great-stink-of-1858/) |
| 7 | Bill passed in about 18 days | [guess] | cannot confirm |  | none found |
| 8 | Bazalgette was chief engineer of Metropolitan Board of Works | [sourced] | cannot confirm |  | none found |
| 9 | Interceptor sewers ran parallel to the Thames | [sourced] | cannot confirm |  | none found |
| 10 | Three interceptors north, two south | [sourced] | cannot confirm |  | none found |
| 11 | Outfalls at Beckton and Crossness | [sourced] | cannot confirm |  | none found |
| 12 | Construction began 1859 | [sourced] | right |  | [STK1](https://www.londonmuseum.org.uk/collections/london-stories/great-stink-of-1858/) |
| 13 | Embankments built partly to house sewers | [sourced] | cannot confirm |  | none found |
| 14 | System opened 1865 by Prince of Wales | [sourced] | cannot confirm |  | none found |
| 15 | About 82 miles of main sewers | [sourced] | right | one source says 85 | [STK1](https://www.londonmuseum.org.uk/collections/london-stories/great-stink-of-1858/) |
| 16 | About 1,100 miles of street sewers | [sourced] | right |  | [STK1](https://www.londonmuseum.org.uk/collections/london-stories/great-stink-of-1858/) |
| 17 | Roughly 318 million bricks | [guess] | right |  | [STK2](https://historicengland.org.uk/images-books/archive/collections/photographs/the-great-stink/) |
| 18 | Cost about £4.2 million | [sourced] | cannot confirm |  | none found |
| 19 | Bazalgette knighted 1875 | [sourced] | cannot confirm |  | none found |
| 20 | Four stations: Abbey Mills, Crossness, Deptford, Western | [sourced] | cannot confirm |  | none found |
| 21 | Abbey Mills nicknamed "Cathedral of Sewage" | [sourced] | cannot confirm |  | none found |
| 22 | Crossness has beam engines | [sourced] | cannot confirm |  | none found |
| 23 | Crossness designed with Charles Driver | [sourced] | cannot confirm |  | none found |
| 24 | Cholera fell; 1866 East End outbreak | [sourced] | cannot confirm |  | none found |
| 25 | Thames Tideway Tunnel completed in 2020s | [sourced] | cannot confirm |  | none found |

**Run 2** (raw output: `test_log/q9_run2.txt`)

| # | Claim | Label | Result | Note | Sources |
|---|---|---|---|---|---|
| 1 | Sewage flowed into Thames, a drinking water source | [sourced] | cannot confirm |  | none found |
| 2 | Cholera 1848-49, 1853-54; miasma theory | [sourced] | cannot confirm |  | none found |
| 3 | Parliament sat on the riverbank | [sourced] | cannot confirm |  | none found |
| 4 | Stink peaked in summer 1858, June to August | [sourced] | right |  | [STK1](https://www.londonmuseum.org.uk/collections/london-stories/great-stink-of-1858/) |
| 5 | June 1858 temperatures about 30-35 C | [guess] | right | sources: about 30 C | [STK1](https://www.londonmuseum.org.uk/collections/london-stories/great-stink-of-1858/) |
| 6 | Lime-chloride curtains at Parliament | [sourced] | cannot confirm |  | none found |
| 7 | MPs considered leaving Westminster | [sourced] | cannot confirm |  | none found |
| 8 | Disraeli fled committee room | [sourced] | cannot confirm |  | none found |
| 9 | Act passed in 1858 | [sourced] | right |  | [STK1](https://www.londonmuseum.org.uk/collections/london-stories/great-stink-of-1858/) |
| 10 | Passed within about 18 days | [guess] | cannot confirm |  | none found |
| 11 | Bazalgette chief engineer of MBW | [sourced] | cannot confirm |  | none found |
| 12 | Interceptor sewer design caught flow and carried it east | [sourced] | cannot confirm |  | none found |
| 13 | Outfalls at Beckton and Crossness | [sourced] | cannot confirm |  | none found |
| 14 | Sewers built larger than estimates required | [sourced] | cannot confirm |  | none found |
| 15 | Construction began 1859 | [sourced] | right |  | [STK1](https://www.londonmuseum.org.uk/collections/london-stories/great-stink-of-1858/) |
| 16 | Prince of Wales opened southern part at Crossness 1865 | [sourced] | cannot confirm |  | none found |
| 17 | Main works finished around 1875 | [sourced] | right |  | [STK1](https://www.londonmuseum.org.uk/collections/london-stories/great-stink-of-1858/) |
| 18 | About 82 miles of main sewers | [sourced] | right |  | [STK1](https://www.londonmuseum.org.uk/collections/london-stories/great-stink-of-1858/) |
| 19 | About 1,100 miles of street sewers | [sourced] | right |  | [STK1](https://www.londonmuseum.org.uk/collections/london-stories/great-stink-of-1858/) |
| 20 | Over 300 million bricks (about 318 million) | [guess] | right |  | [STK2](https://historicengland.org.uk/images-books/archive/collections/photographs/the-great-stink/) |
| 21 | Cost about £4.2 million | [sourced] | cannot confirm |  | none found |
| 22 | Total larger with extensions and embankments | [guess] | cannot confirm |  | none found |
| 23 | Financed by loans repaid by local property tax | [sourced] | cannot confirm |  | none found |
| 24 | Pumping stations lifted sewage | [sourced] | cannot confirm |  | none found |
| 25 | Abbey Mills nickname; Crossness beam engines | [sourced] | cannot confirm |  | none found |
| 26 | Deptford and Western (Pimlico) pumping stations | [sourced] | cannot confirm |  | none found |
| 27 | Chelsea pumping station | [guess] | cannot confirm |  | none found |
| 28 | Crossness and Abbey Mills opened 1865-68 | [sourced] | cannot confirm |  | none found |
| 29 | Crossness engines named Victoria, Prince Consort, Albert Edward, Alexandra | [sourced] | cannot confirm |  | none found |
| 30 | Cholera fell after the system was built | [sourced] | cannot confirm |  | none found |
| 31 | Much of network still in use | [sourced] | cannot confirm |  | none found |
| 32 | Embankments hid interceptor sewers | [sourced] | cannot confirm |  | none found |
| 33 | Bazalgette knighted 1875 | [sourced] | cannot confirm |  | none found |

### Q10. Quebec Bridge collapses (1907, 1916)

**Run 1** (raw output: `test_log/q10_run1.txt`)

| # | Claim | Label | Result | Note | Sources |
|---|---|---|---|---|---|
| 1 | Bridge crosses St Lawrence upstream of Quebec City to Lévis | [sourced] | cannot confirm |  | none found |
| 2 | Design called for main span of about 1,800 ft | [sourced] | right |  | [QUE1](https://www.canada.ca/en/housing-infrastructure-communities/news/2019/08/the-history-of-the-quebec-bridge.html), [QUE2](https://legacy.csce.ca/en/historic-site/the-quebec-bridge/) |
| 3 | Rebuilt span is longest cantilever span and still holds the record | [sourced] | cannot confirm |  | none found |
| 4 | First collapse on 29 August 1907 | [sourced] | right |  | [QUE1](https://www.canada.ca/en/housing-infrastructure-communities/news/2019/08/the-history-of-the-quebec-bridge.html), [QUE2](https://legacy.csce.ca/en/historic-site/the-quebec-bridge/) |
| 5 | Collapse at about 5:30 pm | [sourced] | cannot confirm |  | none found |
| 6 | 75 workers killed | [sourced] | right | other sources say 76, 77, 85 | [QUE1](https://www.canada.ca/en/housing-infrastructure-communities/news/2019/08/the-history-of-the-quebec-bridge.html), [QUE2](https://legacy.csce.ca/en/historic-site/the-quebec-bridge/) |
| 7 | 33 of the dead were Mohawk ironworkers | [sourced] | right |  | [QUE1](https://www.canada.ca/en/housing-infrastructure-communities/news/2019/08/the-history-of-the-quebec-bridge.html), [QUE2](https://legacy.csce.ca/en/historic-site/the-quebec-bridge/) |
| 8 | Only about 11 men survived | [guess] | cannot confirm |  | none found |
| 9 | South arm and anchor arm fell, about 19,000 tons | [sourced] | cannot confirm |  | none found |
| 10 | Failure of lower chord compression members; dead load underestimated | [sourced] | cannot confirm |  | none found |
| 11 | Royal Commission blamed Cooper and Szlapka | [sourced] | right |  | [QUE1](https://www.canada.ca/en/housing-infrastructure-communities/news/2019/08/the-history-of-the-quebec-bridge.html), [QUE2](https://legacy.csce.ca/en/historic-site/the-quebec-bridge/) |
| 12 | 1916 collapse happened while central span was being raised | [sourced] | right |  | [QUE1](https://www.canada.ca/en/housing-infrastructure-communities/news/2019/08/the-history-of-the-quebec-bridge.html), [QUE2](https://legacy.csce.ca/en/historic-site/the-quebec-bridge/) |
| 13 | Cause: failure of a lifting bearing/casting | [sourced] | right | jack bearing failed | [QUE1](https://www.canada.ca/en/housing-infrastructure-communities/news/2019/08/the-history-of-the-quebec-bridge.html), [QUE2](https://legacy.csce.ca/en/historic-site/the-quebec-bridge/) |
| 14 | 13 workers died in 1916 | [sourced] | right |  | [QUE1](https://www.canada.ca/en/housing-infrastructure-communities/news/2019/08/the-history-of-the-quebec-bridge.html), [QUE2](https://legacy.csce.ca/en/historic-site/the-quebec-bridge/) |
| 15 | Span about 640 ft and 5,000 tons | [guess] | cannot confirm |  | none found |
| 16 | Opened to traffic in December 1917 | [guess] | cannot confirm |  | none found |
| 17 | Cooper was consulting engineer in overall charge | [sourced] | right |  | [QUE1](https://www.canada.ca/en/housing-infrastructure-communities/news/2019/08/the-history-of-the-quebec-bridge.html), [QUE2](https://legacy.csce.ca/en/historic-site/the-quebec-bridge/) |
| 18 | Szlapka of Phoenix Bridge did the detailed design | [sourced] | right |  | [QUE1](https://www.canada.ca/en/housing-infrastructure-communities/news/2019/08/the-history-of-the-quebec-bridge.html), [QUE2](https://legacy.csce.ca/en/historic-site/the-quebec-bridge/) |
| 19 | Redesign board included Schneider and Holgate | [sourced] | cannot confirm |  | none found |
| 20 | FitzMaurice on the redesign board | [guess] | cannot confirm |  | none found |
| 21 | Phoenix Bridge Company was contractor and fabricator | [sourced] | cannot confirm |  | none found |
| 22 | Quebec Bridge Company was the owner | [sourced] | right |  | [QUE1](https://www.canada.ca/en/housing-infrastructure-communities/news/2019/08/the-history-of-the-quebec-bridge.html), [QUE2](https://legacy.csce.ca/en/historic-site/the-quebec-bridge/) |
| 23 | Federal government took over after first collapse | [sourced] | cannot confirm |  | none found |
| 24 | Rebuilt by St. Lawrence Bridge Company | [sourced] | cannot confirm |  | none found |
| 25 | Iron Ring text by Kipling; first ceremony 1925 | [sourced] | cannot confirm |  | none found |
| 26 | Rings said to be made from the wreckage | [guess] | cannot confirm |  | none found |

**Run 2** (raw output: `test_log/q10_run2.txt`)

| # | Claim | Label | Result | Note | Sources |
|---|---|---|---|---|---|
| 1 | Bridge between Quebec City and Lévis | [sourced] | cannot confirm |  | none found |
| 2 | Collapse on 29 August 1907 | [sourced] | right |  | [QUE1](https://www.canada.ca/en/housing-infrastructure-communities/news/2019/08/the-history-of-the-quebec-bridge.html), [QUE2](https://legacy.csce.ca/en/historic-site/the-quebec-bridge/) |
| 3 | About 75 killed | [sourced] | right |  | [QUE1](https://www.canada.ca/en/housing-infrastructure-communities/news/2019/08/the-history-of-the-quebec-bridge.html), [QUE2](https://legacy.csce.ca/en/historic-site/the-quebec-bridge/) |
| 4 | About 33 were Mohawk ironworkers | [sourced] | right |  | [QUE1](https://www.canada.ca/en/housing-infrastructure-communities/news/2019/08/the-history-of-the-quebec-bridge.html), [QUE2](https://legacy.csce.ca/en/historic-site/the-quebec-bridge/) |
| 5 | Compression chords in anchor arm buckled | [sourced] | cannot confirm |  | none found |
| 6 | Royal Commission found dead load underestimated | [sourced] | cannot confirm |  | none found |
| 7 | Cooper was consulting engineer in overall charge | [sourced] | right |  | [QUE1](https://www.canada.ca/en/housing-infrastructure-communities/news/2019/08/the-history-of-the-quebec-bridge.html), [QUE2](https://legacy.csce.ca/en/historic-site/the-quebec-bridge/) |
| 8 | Szlapka of Phoenix did detailed design | [sourced] | right |  | [QUE1](https://www.canada.ca/en/housing-infrastructure-communities/news/2019/08/the-history-of-the-quebec-bridge.html), [QUE2](https://legacy.csce.ca/en/historic-site/the-quebec-bridge/) |
| 9 | Commission blamed both | [sourced] | right |  | [QUE1](https://www.canada.ca/en/housing-infrastructure-communities/news/2019/08/the-history-of-the-quebec-bridge.html), [QUE2](https://legacy.csce.ca/en/historic-site/the-quebec-bridge/) |
| 10 | Cooper elderly, ill, rarely on site | [sourced] | cannot confirm |  | none found |
| 11 | Quebec Bridge Company was the owner | [sourced] | right |  | [QUE1](https://www.canada.ca/en/housing-infrastructure-communities/news/2019/08/the-history-of-the-quebec-bridge.html), [QUE2](https://legacy.csce.ca/en/historic-site/the-quebec-bridge/) |
| 12 | Phoenix of Phoenixville fabricated and erected steel | [sourced] | cannot confirm |  | none found |
| 13 | Federal government took over | [sourced] | cannot confirm |  | none found |
| 14 | Planned 1,800 ft span would be longest cantilever span | [sourced] | right |  | [QUE1](https://www.canada.ca/en/housing-infrastructure-communities/news/2019/08/the-history-of-the-quebec-bridge.html), [QUE2](https://legacy.csce.ca/en/historic-site/the-quebec-bridge/) |
| 15 | 1916 collapse on 11 September 1916 | [sourced] | right |  | [QUE1](https://www.canada.ca/en/housing-infrastructure-communities/news/2019/08/the-history-of-the-quebec-bridge.html), [QUE2](https://legacy.csce.ca/en/historic-site/the-quebec-bridge/) |
| 16 | Central span hoisted into place fell into the river | [sourced] | right |  | [QUE1](https://www.canada.ca/en/housing-infrastructure-communities/news/2019/08/the-history-of-the-quebec-bridge.html), [QUE2](https://legacy.csce.ca/en/historic-site/the-quebec-bridge/) |
| 17 | 13 workers killed in 1916 | [sourced] | right |  | [QUE1](https://www.canada.ca/en/housing-infrastructure-communities/news/2019/08/the-history-of-the-quebec-bridge.html), [QUE2](https://legacy.csce.ca/en/historic-site/the-quebec-bridge/) |
| 18 | Lifting-equipment casting failed | [sourced] | right | jack bearing failed | [QUE1](https://www.canada.ca/en/housing-infrastructure-communities/news/2019/08/the-history-of-the-quebec-bridge.html), [QUE2](https://legacy.csce.ca/en/historic-site/the-quebec-bridge/) |
| 19 | St. Lawrence Bridge Company, a Dominion Bridge consortium | [sourced] | cannot confirm |  | none found |
| 20 | Redesign board incl. Modjeski, Monsarrat, FitzMaurice | [sourced] | cannot confirm |  | none found |
| 21 | Bridge finished and opened to traffic in December 1919 | [sourced] | **WRONG** | completed 1917; officially inaugurated Aug 1919 | [QUE1](https://www.canada.ca/en/housing-infrastructure-communities/news/2019/08/the-history-of-the-quebec-bridge.html), [QUE2](https://legacy.csce.ca/en/historic-site/the-quebec-bridge/) |
| 22 | Two disasters killed about 88-89 | [sourced] | right |  | [QUE1](https://www.canada.ca/en/housing-infrastructure-communities/news/2019/08/the-history-of-the-quebec-bridge.html), [QUE2](https://legacy.csce.ca/en/historic-site/the-quebec-bridge/) |
| 23 | Mohawk loss led to the Iron Ring | [sourced] | cannot confirm |  | none found |

### Q11. Peshtigo Fire (1871)

**Run 1** (raw output: `test_log/q11_run1.txt`)

| # | Claim | Label | Result | Note | Sources |
|---|---|---|---|---|---|
| 1 | Began night of 8 October 1871 | [sourced] | right |  | [PES1](https://en.wikipedia.org/wiki/Peshtigo_fire) |
| 2 | Same night as Great Chicago Fire | [sourced] | right |  | [PES1](https://en.wikipedia.org/wiki/Peshtigo_fire) |
| 3 | Peshtigo destroyed within an hour or two | [sourced] | cannot confirm |  | none found |
| 4 | About 1.2 million acres (1,875 sq mi) burned | [sourced] | right |  | [PES1](https://en.wikipedia.org/wiki/Peshtigo_fire), [PES2](https://www.britannica.com/topic/What-Is-the-Deadliest-Wildfire-in-History) |
| 5 | Covered NE Wisconsin and Michigan's Upper Peninsula | [sourced] | cannot confirm |  | none found |
| 6 | Largest forest fire in US history by area | [sourced] | cannot confirm |  | none found |
| 7 | Reached Door County and Green Bay region | [sourced] | cannot confirm | sources say separate fires | [PES1](https://en.wikipedia.org/wiki/Peshtigo_fire) |
| 8 | At least 1,200 died; estimates up to 2,500 | [sourced] | right |  | [PES1](https://en.wikipedia.org/wiki/Peshtigo_fire) |
| 9 | Deadliest wildfire in US history | [sourced] | right |  | [PES1](https://en.wikipedia.org/wiki/Peshtigo_fire), [PES2](https://www.britannica.com/topic/What-Is-the-Deadliest-Wildfire-in-History) |
| 10 | Records lost, exact toll uncertain | [sourced] | right |  | [PES2](https://www.britannica.com/topic/What-Is-the-Deadliest-Wildfire-in-History) |
| 11 | Roughly 800 dead in or near Peshtigo | [guess] | right |  | [PES2](https://www.britannica.com/topic/What-Is-the-Deadliest-Wildfire-in-History) |
| 12 | Survivors jumped into river, wells, tanks | [sourced] | cannot confirm |  | none found |
| 13 | Some drowned or died of exposure in river | [guess] | cannot confirm |  | none found |
| 14 | Dry, drought-like conditions | [sourced] | right |  | [PES1](https://en.wikipedia.org/wiki/Peshtigo_fire), [PES3](https://www.weather.gov/grb/peshtigofire) |
| 15 | Logging, railroads and clearing left slash | [sourced] | right |  | [PES3](https://www.weather.gov/grb/peshtigofire) |
| 16 | Small fires already burning | [sourced] | cannot confirm |  | none found |
| 17 | Strong storm system brought high winds that night | [sourced] | right |  | [PES3](https://www.weather.gov/grb/peshtigofire) |
| 18 | Survivors described tornado-like roar | [sourced] | cannot confirm |  | none found |
| 19 | Gusts above 60 mph | [guess] | cannot confirm |  | none found |
| 20 | Rain came only after the worst had passed | [guess] | right |  | [PES1](https://en.wikipedia.org/wiki/Peshtigo_fire) |
| 21 | Peshtigo was a lumber town with a woodenware factory | [sourced] | cannot confirm |  | none found |
| 22 | Overshadowed by Chicago fire | [sourced] | cannot confirm |  | none found |
| 23 | Comet theory speculative, not accepted | [sourced] | right |  | [PES1](https://en.wikipedia.org/wiki/Peshtigo_fire) |

**Run 2** (raw output: `test_log/q11_run2.txt`)

| # | Claim | Label | Result | Note | Sources |
|---|---|---|---|---|---|
| 1 | Began night of Sunday 8 October 1871 | [sourced] | right |  | [PES1](https://en.wikipedia.org/wiki/Peshtigo_fire) |
| 2 | Same night as Chicago fire | [sourced] | right |  | [PES1](https://en.wikipedia.org/wiki/Peshtigo_fire) |
| 3 | Deadliest US wildfire | [sourced] | right |  | [PES1](https://en.wikipedia.org/wiki/Peshtigo_fire) |
| 4 | About 1.2 million acres burned | [sourced] | right |  | [PES1](https://en.wikipedia.org/wiki/Peshtigo_fire) |
| 5 | Extended into Upper Peninsula | [sourced] | cannot confirm |  | none found |
| 6 | Peshtigo almost completely destroyed | [sourced] | right |  | [PES2](https://www.britannica.com/topic/What-Is-the-Deadliest-Wildfire-in-History) |
| 7 | Williamsonville and Brussels also hit | [sourced] | right |  | [PES1](https://en.wikipedia.org/wiki/Peshtigo_fire) |
| 8 | At least 1,200 deaths; estimates up to 2,500 | [sourced] | right |  | [PES1](https://en.wikipedia.org/wiki/Peshtigo_fire) |
| 9 | Records lost, many unidentified | [sourced] | right |  | [PES2](https://www.britannica.com/topic/What-Is-the-Deadliest-Wildfire-in-History) |
| 10 | About 800 dead in Peshtigo | [guess] | right |  | [PES2](https://www.britannica.com/topic/What-Is-the-Deadliest-Wildfire-in-History) |
| 11 | Mass grave of unidentified victims | [sourced] | right |  | [PES2](https://www.britannica.com/topic/What-Is-the-Deadliest-Wildfire-in-History) |
| 12 | Dry, drought conditions | [sourced] | right |  | [PES1](https://en.wikipedia.org/wiki/Peshtigo_fire), [PES3](https://www.weather.gov/grb/peshtigofire) |
| 13 | Logging and clearing slash fed fires | [sourced] | right |  | [PES3](https://www.weather.gov/grb/peshtigofire) |
| 14 | Small fires already burning | [sourced] | cannot confirm |  | none found |
| 15 | Strong wind, possibly cold front | [sourced] | right |  | [PES3](https://www.weather.gov/grb/peshtigofire) |
| 16 | Roaring sound like a train | [sourced] | cannot confirm |  | none found |
| 17 | Extreme heat and fire whirls | [guess] | cannot confirm |  | none found |
| 18 | Refuge in river and wells; many drowned | [sourced] | cannot confirm |  | none found |
| 19 | Comet theory not accepted | [sourced] | right |  | [PES1](https://en.wikipedia.org/wiki/Peshtigo_fire) |

### Q12. Ronan Point collapse (1968)

**Run 1** (raw output: `test_log/q12_run1.txt`)

| # | Claim | Label | Result | Note | Sources |
|---|---|---|---|---|---|
| 1 | Collapse morning of 16 May 1968 | [sourced] | right |  | [RON1](https://en.wikipedia.org/wiki/Ronan_Point), [RON2](https://www.designingbuildings.co.uk/wiki/Ronan_Point) |
| 2 | At about 5:45 am | [sourced] | right |  | [RON1](https://en.wikipedia.org/wiki/Ronan_Point), [RON2](https://www.designingbuildings.co.uk/wiki/Ronan_Point) |
| 3 | 22-storey tower in Canning Town, Newham | [sourced] | cannot confirm |  | none found |
| 4 | Completed March 1968 | [sourced] | cannot confirm |  | none found |
| 5 | Gas explosion in flat 90, 18th floor | [sourced] | right |  | [RON1](https://en.wikipedia.org/wiki/Ronan_Point), [RON2](https://www.designingbuildings.co.uk/wiki/Ronan_Point) |
| 6 | Ivy Hodge lit a stove/match | [sourced] | right |  | [RON1](https://en.wikipedia.org/wiki/Ronan_Point), [RON2](https://www.designingbuildings.co.uk/wiki/Ronan_Point) |
| 7 | She survived | [sourced] | right |  | [RON1](https://en.wikipedia.org/wiki/Ronan_Point), [RON2](https://www.designingbuildings.co.uk/wiki/Ronan_Point) |
| 8 | Blast blew out load-bearing flank wall; progressive collapse | [sourced] | cannot confirm |  | none found |
| 9 | Gas leak from faulty stove connection | [sourced] | cannot confirm |  | none found |
| 10 | Explosion pressure about 2 psi | [guess] | cannot confirm | sources give 2.5 psi | [RON1](https://en.wikipedia.org/wiki/Ronan_Point), [RON2](https://www.designingbuildings.co.uk/wiki/Ronan_Point) |
| 11 | Four died | [sourced] | right | four or five depending on source | [RON1](https://en.wikipedia.org/wiki/Ronan_Point), [RON2](https://www.designingbuildings.co.uk/wiki/Ronan_Point) |
| 12 | About 17 injured | [sourced] | right |  | [RON1](https://en.wikipedia.org/wiki/Ronan_Point), [RON2](https://www.designingbuildings.co.uk/wiki/Ronan_Point) |
| 13 | Low toll due to early hour | [sourced] | cannot confirm |  | none found |
| 14 | Larsen-Nielsen Danish large-panel system | [sourced] | right |  | [RON1](https://en.wikipedia.org/wiki/Ronan_Point), [RON2](https://www.designingbuildings.co.uk/wiki/Ronan_Point) |
| 15 | Built by Taylor Woodrow-Anglian | [sourced] | right |  | [RON1](https://en.wikipedia.org/wiki/Ronan_Point), [RON2](https://www.designingbuildings.co.uk/wiki/Ronan_Point) |
| 16 | Panels bolted; load-bearing walls; weak joints; poor mortar | [sourced] | cannot confirm |  | none found |
| 17 | Inquiry chaired by Hugh Griffiths QC | [sourced] | right |  | [RON1](https://en.wikipedia.org/wiki/Ronan_Point), [RON2](https://www.designingbuildings.co.uk/wiki/Ronan_Point) |
| 18 | Other members Pugsley and Skempton | [sourced] | **WRONG** | members were Pugsley and Saunders; no Skempton found | [RON1](https://en.wikipedia.org/wiki/Ronan_Point), [RON2](https://www.designingbuildings.co.uk/wiki/Ronan_Point) |
| 19 | Report out later in 1968 | [sourced] | cannot confirm |  | none found |
| 20 | Report found design and joints deficient; did not blame occupant | [sourced] | cannot confirm |  | none found |
| 21 | Building Regulations amended in 1970 | [sourced] | right |  | [RON1](https://en.wikipedia.org/wiki/Ronan_Point), [RON2](https://www.designingbuildings.co.uk/wiki/Ronan_Point) |
| 22 | Key element and tie-force concepts | [sourced] | cannot confirm |  | none found |
| 23 | Similar blocks strengthened or demolished | [sourced] | cannot confirm |  | none found |
| 24 | Demolished in 1986 | [sourced] | right |  | [RON1](https://en.wikipedia.org/wiki/Ronan_Point), [RON2](https://www.designingbuildings.co.uk/wiki/Ronan_Point) |
| 25 | Public confidence in tower blocks fell | [sourced] | cannot confirm |  | none found |

**Run 2** (raw output: `test_log/q12_run2.txt`)

| # | Claim | Label | Result | Note | Sources |
|---|---|---|---|---|---|
| 1 | Collapse 16 May 1968 at about 5:45 am | [sourced] | right |  | [RON1](https://en.wikipedia.org/wiki/Ronan_Point), [RON2](https://www.designingbuildings.co.uk/wiki/Ronan_Point) |
| 2 | 22-storey block in Canning Town, opened March 1968 | [sourced] | cannot confirm |  | none found |
| 3 | Gas explosion in flat 90 on 18th floor | [sourced] | right |  | [RON1](https://en.wikipedia.org/wiki/Ronan_Point), [RON2](https://www.designingbuildings.co.uk/wiki/Ronan_Point) |
| 4 | Ivy Hodge lit a match | [sourced] | right |  | [RON1](https://en.wikipedia.org/wiki/Ronan_Point), [RON2](https://www.designingbuildings.co.uk/wiki/Ronan_Point) |
| 5 | Flank wall blown out; progressive collapse | [sourced] | cannot confirm |  | none found |
| 6 | Four died at first | [sourced] | right |  | [RON1](https://en.wikipedia.org/wiki/Ronan_Point), [RON2](https://www.designingbuildings.co.uk/wiki/Ronan_Point) |
| 7 | Fifth died later | [sourced] | right | one source | [RON1](https://en.wikipedia.org/wiki/Ronan_Point), [RON2](https://www.designingbuildings.co.uk/wiki/Ronan_Point) |
| 8 | 4 or 5 deaths, about 17 injured | [sourced] | right |  | [RON1](https://en.wikipedia.org/wiki/Ronan_Point), [RON2](https://www.designingbuildings.co.uk/wiki/Ronan_Point) |
| 9 | Ivy Hodge survived | [sourced] | right |  | [RON1](https://en.wikipedia.org/wiki/Ronan_Point), [RON2](https://www.designingbuildings.co.uk/wiki/Ronan_Point) |
| 10 | Larsen-Nielsen system | [sourced] | right |  | [RON1](https://en.wikipedia.org/wiki/Ronan_Point), [RON2](https://www.designingbuildings.co.uk/wiki/Ronan_Point) |
| 11 | Contractor Taylor Woodrow-Anglian | [sourced] | right |  | [RON1](https://en.wikipedia.org/wiki/Ronan_Point), [RON2](https://www.designingbuildings.co.uk/wiki/Ronan_Point) |
| 12 | Joints weak, poor workmanship | [sourced] | cannot confirm |  | none found |
| 13 | Gas supply poorly tightened joint | [guess] | cannot confirm |  | none found |
| 14 | Inquiry chaired by Hugh Griffiths QC | [sourced] | right |  | [RON1](https://en.wikipedia.org/wiki/Ronan_Point), [RON2](https://www.designingbuildings.co.uk/wiki/Ronan_Point) |
| 15 | Report published 1968; found building inadequate | [sourced] | cannot confirm |  | none found |
| 16 | About 2 psi (14 kPa) was enough | [guess] | cannot confirm | sources give 2.5 psi | [RON1](https://en.wikipedia.org/wiki/Ronan_Point), [RON2](https://www.designingbuildings.co.uk/wiki/Ronan_Point) |
| 17 | 1970 Building Regulation changes on progressive collapse | [sourced] | right |  | [RON1](https://en.wikipedia.org/wiki/Ronan_Point), [RON2](https://www.designingbuildings.co.uk/wiki/Ronan_Point) |
| 18 | Existing blocks strengthened or demolished | [sourced] | cannot confirm |  | none found |
| 19 | Ronan Point demolished in 1986 | [sourced] | right |  | [RON1](https://en.wikipedia.org/wiki/Ronan_Point), [RON2](https://www.designingbuildings.co.uk/wiki/Ronan_Point) |
| 20 | Collapse contributed to decline of high-rise housing | [sourced] | cannot confirm |  | none found |

### Q13. Building of Hoover Dam

**Run 1** (raw output: `test_log/q13_run1.txt`)

| # | Claim | Label | Result | Note | Sources |
|---|---|---|---|---|---|
| 1 | Boulder Canyon Project Act signed 21 Dec 1928 | [sourced] | cannot confirm |  | none found |
| 2 | Six Companies won contract March 1931 | [sourced] | cannot confirm |  | none found |
| 3 | Construction began 1931; river diverted late 1932 | [sourced] | cannot confirm |  | none found |
| 4 | First concrete poured 6 June 1933 | [sourced] | right |  | [HOO1](https://www.history.com/articles/7-things-you-might-not-know-about-the-hoover-dam) |
| 5 | Last concrete 29 May 1935 | [sourced] | cannot confirm |  | none found |
| 6 | Roosevelt dedicated dam 30 September 1935 | [sourced] | right |  | [HOO1](https://www.history.com/articles/7-things-you-might-not-know-about-the-hoover-dam) |
| 7 | First generator online 1936 | [sourced] | cannot confirm |  | none found |
| 8 | Finished about two years early | [sourced] | cannot confirm |  | none found |
| 9 | Formally complete March 1936 | [guess] | cannot confirm |  | none found |
| 10 | Six Companies bid about $48.9 million | [sourced] | right |  | [HOO1](https://www.history.com/articles/7-things-you-might-not-know-about-the-hoover-dam) |
| 11 | Total project cost roughly $165 million | [sourced] | cannot confirm | only a blog source | [HOO1](https://www.history.com/articles/7-things-you-might-not-know-about-the-hoover-dam) |
| 12 | About $49 million attaches to the contract, not total cost | [guess] | right |  | [HOO1](https://www.history.com/articles/7-things-you-might-not-know-about-the-hoover-dam) |
| 13 | Modern equivalent about $1 billion | [guess] | cannot confirm |  | none found |
| 14 | About 3.25 million cubic yards in the dam | [sourced] | right |  | [HOO1](https://www.history.com/articles/7-things-you-might-not-know-about-the-hoover-dam) |
| 15 | About 4.4 million cubic yards in total | [sourced] | cannot confirm | source says 4.3 million | [HOO1](https://www.history.com/articles/7-things-you-might-not-know-about-the-hoover-dam) |
| 16 | Cooled with embedded pipes; 125 years to cool | [sourced] | cannot confirm |  | none found |
| 17 | Official count 96 deaths | [sourced] | right |  | [HOO1](https://www.history.com/articles/7-things-you-might-not-know-about-the-hoover-dam) |
| 18 | J.G. Tierney drowned in 1922 looking for dam sites | [sourced] | right |  | [HOO1](https://www.history.com/articles/7-things-you-might-not-know-about-the-hoover-dam) |
| 19 | Patrick Tierney died 20 Dec 1935, 13 years later | [sourced] | right |  | [HOO1](https://www.history.com/articles/7-things-you-might-not-know-about-the-hoover-dam) |
| 20 | Official count excludes heat and pneumonia deaths | [sourced] | cannot confirm |  | none found |
| 21 | Peak workforce about 5,200 | [sourced] | cannot confirm |  | none found |
| 22 | Six Companies members list | [sourced] | cannot confirm |  | none found |
| 23 | Bechtel, Kaiser, Wattis, Crowe roles | [sourced] | cannot confirm |  | none found |
| 24 | Bureau of Reclamation oversaw project | [sourced] | cannot confirm |  | none found |
| 25 | Ralph Lowry's role was minor | [guess] | cannot confirm |  | none found |

**Run 2** (raw output: `test_log/q13_run2.txt`)

| # | Claim | Label | Result | Note | Sources |
|---|---|---|---|---|---|
| 1 | Act signed December 1928 | [sourced] | cannot confirm |  | none found |
| 2 | Dam on Colorado River, Nevada-Arizona border | [sourced] | cannot confirm |  | none found |
| 3 | Name restored to Hoover Dam in 1947 | [sourced] | cannot confirm |  | none found |
| 4 | Contract awarded March 1931; work began 1931 | [sourced] | cannot confirm |  | none found |
| 5 | River diverted late 1932 | [sourced] | cannot confirm |  | none found |
| 6 | First concrete June 1933 | [sourced] | right |  | [HOO1](https://www.history.com/articles/7-things-you-might-not-know-about-the-hoover-dam) |
| 7 | Last concrete May 1935 | [sourced] | cannot confirm |  | none found |
| 8 | Roosevelt dedicated it 30 Sept 1935 | [sourced] | right |  | [HOO1](https://www.history.com/articles/7-things-you-might-not-know-about-the-hoover-dam) |
| 9 | First generator 1936 | [sourced] | cannot confirm |  | none found |
| 10 | Finished more than two years early | [sourced] | cannot confirm |  | none found |
| 11 | Winning bidder Six Companies, bid about $48.9 million | [sourced] | right |  | [HOO1](https://www.history.com/articles/7-things-you-might-not-know-about-the-hoover-dam) |
| 12 | Kaiser best known; member list | [sourced] | cannot confirm |  | none found |
| 13 | Crowe directed construction | [sourced] | cannot confirm |  | none found |
| 14 | Raymond F. Walter government chief engineer | [guess] | cannot confirm |  | none found |
| 15 | About $49 million for main contract | [sourced] | right |  | [HOO1](https://www.history.com/articles/7-things-you-might-not-know-about-the-hoover-dam) |
| 16 | Overall cost roughly $165 million | [guess] | cannot confirm | only a blog source | [HOO1](https://www.history.com/articles/7-things-you-might-not-know-about-the-hoover-dam) |
| 17 | Overall cost cited at $120-165 million | [guess] | cannot confirm |  | none found |
| 18 | Came in under budget | [guess] | cannot confirm |  | none found |
| 19 | About 3.25 million cubic yards of concrete | [sourced] | right |  | [HOO1](https://www.history.com/articles/7-things-you-might-not-know-about-the-hoover-dam) |
| 20 | 4.4 million cubic yards in total | [sourced] | cannot confirm | source says 4.3 million | [HOO1](https://www.history.com/articles/7-things-you-might-not-know-about-the-hoover-dam) |
| 21 | Cooled with pipes; over a century to cool | [sourced] | cannot confirm |  | none found |
| 22 | 726 feet tall | [sourced] | right |  | [HOO1](https://www.history.com/articles/7-things-you-might-not-know-about-the-hoover-dam) |
| 23 | 1,244 feet long at the crest | [sourced] | right |  | [HOO1](https://www.history.com/articles/7-things-you-might-not-know-about-the-hoover-dam) |
| 24 | Official count 96 deaths | [sourced] | right |  | [HOO1](https://www.history.com/articles/7-things-you-might-not-know-about-the-hoover-dam) |
| 25 | J.G. Tierney drowned December 1922 | [sourced] | right |  | [HOO1](https://www.history.com/articles/7-things-you-might-not-know-about-the-hoover-dam) |
| 26 | Patrick Tierney died December 1935 | [sourced] | right |  | [HOO1](https://www.history.com/articles/7-things-you-might-not-know-about-the-hoover-dam) |
| 27 | Heat and pneumonia deaths not counted | [sourced] | cannot confirm |  | none found |
| 28 | About 5,000 workers at peak | [sourced] | cannot confirm |  | none found |
| 29 | Boulder City; 1931 strike; Black workers excluded | [sourced] | cannot confirm |  | none found |

### Q14. Tacoma Narrows Bridge collapse (1940)

**Run 1** (raw output: `test_log/q14_run1.txt`)

| # | Claim | Label | Result | Note | Sources |
|---|---|---|---|---|---|
| 1 | Collapsed 7 November 1940 | [sourced] | right |  | [TAC1](https://www.wsdot.wa.gov/tnbhistory/collapse.htm), [TAC2](https://en.wikipedia.org/wiki/Tacoma_Narrows_Bridge_(1940)) |
| 2 | Opened 1 July 1940 | [sourced] | right |  | [TAC1](https://www.wsdot.wa.gov/tnbhistory/collapse.htm), [TAC2](https://en.wikipedia.org/wiki/Tacoma_Narrows_Bridge_(1940)) |
| 3 | Wind about 40 mph | [sourced] | right |  | [TAC1](https://www.wsdot.wa.gov/tnbhistory/collapse.htm), [TAC2](https://en.wikipedia.org/wiki/Tacoma_Narrows_Bridge_(1940)) |
| 4 | Designed for winds around 100 mph | [sourced] | cannot confirm |  | none found |
| 5 | Leon Moisseiff lead designer | [sourced] | right |  | [TAC1](https://www.wsdot.wa.gov/tnbhistory/collapse.htm), [TAC2](https://en.wikipedia.org/wiki/Tacoma_Narrows_Bridge_(1940)) |
| 6 | Clark Eldridge made the original more conservative design | [sourced] | right |  | [TAC1](https://www.wsdot.wa.gov/tnbhistory/collapse.htm), [TAC2](https://en.wikipedia.org/wiki/Tacoma_Narrows_Bridge_(1940)) |
| 7 | Moisseiff's cheaper design was adopted | [sourced] | right |  | [TAC1](https://www.wsdot.wa.gov/tnbhistory/collapse.htm), [TAC2](https://en.wikipedia.org/wiki/Tacoma_Narrows_Bridge_(1940)) |
| 8 | Funding limits pushed the cheaper design | [guess] | right |  | [TAC1](https://www.wsdot.wa.gov/tnbhistory/collapse.htm), [TAC2](https://en.wikipedia.org/wiki/Tacoma_Narrows_Bridge_(1940)) |
| 9 | Cost about $6.4 million | [sourced] | right |  | [TAC1](https://www.wsdot.wa.gov/tnbhistory/collapse.htm), [TAC2](https://en.wikipedia.org/wiki/Tacoma_Narrows_Bridge_(1940)) |
| 10 | Largely funded by PWA and tolls | [sourced] | cannot confirm |  | none found |
| 11 | Main span 2,800 ft | [sourced] | right |  | [TAC1](https://www.wsdot.wa.gov/tnbhistory/collapse.htm), [TAC2](https://en.wikipedia.org/wiki/Tacoma_Narrows_Bridge_(1940)) |
| 12 | Third-longest suspension span at the time | [sourced] | right |  | [TAC1](https://www.wsdot.wa.gov/tnbhistory/collapse.htm), [TAC2](https://en.wikipedia.org/wiki/Tacoma_Narrows_Bridge_(1940)) |
| 13 | Total length about 5,939 ft | [sourced] | right |  | [TAC1](https://www.wsdot.wa.gov/tnbhistory/collapse.htm), [TAC2](https://en.wikipedia.org/wiki/Tacoma_Narrows_Bridge_(1940)) |
| 14 | Deck 39 feet wide | [sourced] | cannot confirm |  | none found |
| 15 | Plate girders 8 feet deep | [sourced] | right |  | [TAC1](https://www.wsdot.wa.gov/tnbhistory/collapse.htm), [TAC2](https://en.wikipedia.org/wiki/Tacoma_Narrows_Bridge_(1940)) |
| 16 | Nicknamed Galloping Gertie | [sourced] | cannot confirm |  | none found |
| 17 | Only fatality was dog Tubby | [sourced] | right |  | [TAC1](https://www.wsdot.wa.gov/tnbhistory/collapse.htm), [TAC2](https://en.wikipedia.org/wiki/Tacoma_Narrows_Bridge_(1940)) |
| 18 | Failure due to aeroelastic flutter | [sourced] | cannot confirm |  | none found |
| 19 | Replacement opened in 1950 | [sourced] | right |  | [TAC1](https://www.wsdot.wa.gov/tnbhistory/collapse.htm), [TAC2](https://en.wikipedia.org/wiki/Tacoma_Narrows_Bridge_(1940)) |

**Run 2** (raw output: `test_log/q14_run2.txt`)

| # | Claim | Label | Result | Note | Sources |
|---|---|---|---|---|---|
| 1 | Collapsed 7 November 1940 | [sourced] | right |  | [TAC1](https://www.wsdot.wa.gov/tnbhistory/collapse.htm), [TAC2](https://en.wikipedia.org/wiki/Tacoma_Narrows_Bridge_(1940)) |
| 2 | Opened 1 July 1940 | [sourced] | right |  | [TAC1](https://www.wsdot.wa.gov/tnbhistory/collapse.htm), [TAC2](https://en.wikipedia.org/wiki/Tacoma_Narrows_Bridge_(1940)) |
| 3 | Wind about 40 mph | [sourced] | right |  | [TAC1](https://www.wsdot.wa.gov/tnbhistory/collapse.htm), [TAC2](https://en.wikipedia.org/wiki/Tacoma_Narrows_Bridge_(1940)) |
| 4 | Wind well below design assumptions | [sourced] | cannot confirm |  | none found |
| 5 | Moisseiff lead design engineer | [sourced] | right |  | [TAC1](https://www.wsdot.wa.gov/tnbhistory/collapse.htm), [TAC2](https://en.wikipedia.org/wiki/Tacoma_Narrows_Bridge_(1940)) |
| 6 | Deflection theory favoured slender girders | [sourced] | cannot confirm |  | none found |
| 7 | Charles Andrew approved a stiffer design | [sourced] | cannot confirm | the stiffer design was Clark Eldridge's; Andrew not found | [TAC1](https://www.wsdot.wa.gov/tnbhistory/collapse.htm), [TAC2](https://en.wikipedia.org/wiki/Tacoma_Narrows_Bridge_(1940)) |
| 8 | Cost about $6.4 million | [sourced] | right |  | [TAC1](https://www.wsdot.wa.gov/tnbhistory/collapse.htm), [TAC2](https://en.wikipedia.org/wiki/Tacoma_Narrows_Bridge_(1940)) |
| 9 | Funded by PWA grant and loan | [sourced] | cannot confirm |  | none found |
| 10 | Main span 2,800 ft | [sourced] | right |  | [TAC1](https://www.wsdot.wa.gov/tnbhistory/collapse.htm), [TAC2](https://en.wikipedia.org/wiki/Tacoma_Narrows_Bridge_(1940)) |
| 11 | Third-longest span at the time | [sourced] | right |  | [TAC1](https://www.wsdot.wa.gov/tnbhistory/collapse.htm), [TAC2](https://en.wikipedia.org/wiki/Tacoma_Narrows_Bridge_(1940)) |
| 12 | Total length about 5,939 ft | [sourced] | right |  | [TAC1](https://www.wsdot.wa.gov/tnbhistory/collapse.htm), [TAC2](https://en.wikipedia.org/wiki/Tacoma_Narrows_Bridge_(1940)) |
| 13 | Nicknamed Galloping Gertie | [sourced] | cannot confirm |  | none found |
| 14 | Deck 39 ft wide | [sourced] | cannot confirm |  | none found |
| 15 | Plate girders 8 ft deep | [sourced] | right |  | [TAC1](https://www.wsdot.wa.gov/tnbhistory/collapse.htm), [TAC2](https://en.wikipedia.org/wiki/Tacoma_Narrows_Bridge_(1940)) |
| 16 | Failure due to aeroelastic flutter | [sourced] | cannot confirm |  | none found |
| 17 | Only fatality was dog Tubby | [sourced] | right |  | [TAC1](https://www.wsdot.wa.gov/tnbhistory/collapse.htm), [TAC2](https://en.wikipedia.org/wiki/Tacoma_Narrows_Bridge_(1940)) |
| 18 | Replacement opened in 1950 | [sourced] | right |  | [TAC1](https://www.wsdot.wa.gov/tnbhistory/collapse.htm), [TAC2](https://en.wikipedia.org/wiki/Tacoma_Narrows_Bridge_(1940)) |

### Q15. Johnstown Flood (1889)

**Run 1** (raw output: `test_log/q15_run1.txt`)

| # | Claim | Label | Result | Note | Sources |
|---|---|---|---|---|---|
| 1 | Flood on 31 May 1889 | [sourced] | right |  | [JOH1](https://www.heritagejohnstown.org/attractions/johnstown-flood-museum/flood-history/facts-about-the-1889-flood/) |
| 2 | After days of extreme rain | [sourced] | cannot confirm |  | none found |
| 3 | Dam failed at about 3:10 pm | [sourced] | right |  | [JOH1](https://www.heritagejohnstown.org/attractions/johnstown-flood-museum/flood-history/facts-about-the-1889-flood/) |
| 4 | Flood reached Johnstown about 4:07 pm | [sourced] | cannot confirm |  | none found |
| 5 | South Fork Dam on Little Conemaugh, 14 miles upstream | [sourced] | cannot confirm |  | none found |
| 6 | Dam about 72 feet high | [sourced] | right |  | [JOH1](https://www.heritagejohnstown.org/attractions/johnstown-flood-museum/flood-history/facts-about-the-1889-flood/) |
| 7 | Dam about 931 feet long | [sourced] | cannot confirm | source says about 900 | [JOH1](https://www.heritagejohnstown.org/attractions/johnstown-flood-museum/flood-history/facts-about-the-1889-flood/) |
| 8 | Lake 2 miles long, 1 mile wide, 60 ft deep | [sourced] | cannot confirm |  | none found |
| 9 | 20 million tons of water | [sourced] | cannot confirm |  | none found |
| 10 | Earthen dam built 1840s for canal system | [sourced] | cannot confirm |  | none found |
| 11 | Overtopping; crest lowered, pipes removed | [sourced] | cannot confirm |  | none found |
| 12 | 2,209 died | [sourced] | right |  | [JOH1](https://www.heritagejohnstown.org/attractions/johnstown-flood-museum/flood-history/facts-about-the-1889-flood/) |
| 13 | 777 unidentified | [guess] | cannot confirm | sources: more than 750 | [JOH1](https://www.heritagejohnstown.org/attractions/johnstown-flood-museum/flood-history/facts-about-the-1889-flood/) |
| 14 | 99 families lost completely | [guess] | right |  | [JOH1](https://www.heritagejohnstown.org/attractions/johnstown-flood-museum/flood-history/facts-about-the-1889-flood/) |
| 15 | 396 children killed | [guess] | right |  | [JOH1](https://www.heritagejohnstown.org/attractions/johnstown-flood-museum/flood-history/facts-about-the-1889-flood/) |
| 16 | Among deadliest US disasters of the time | [sourced] | cannot confirm |  | none found |
| 17 | Fire at Stone Bridge debris caused more deaths | [sourced] | right |  | [JOH1](https://www.heritagejohnstown.org/attractions/johnstown-flood-museum/flood-history/facts-about-the-1889-flood/) |
| 18 | Club was private resort of Pittsburgh industrialists | [sourced] | cannot confirm |  | none found |
| 19 | Members included Carnegie, Frick, Mellon | [sourced] | cannot confirm | Mellon not found | [JOH1](https://www.heritagejohnstown.org/attractions/johnstown-flood-museum/flood-history/facts-about-the-1889-flood/) |
| 20 | Frick key figure in organising the club | [sourced] | cannot confirm |  | none found |
| 21 | Ruff was club president at time of flood | [guess] | cannot confirm |  | none found |
| 22 | Members lowered crest and removed pipes | [sourced] | cannot confirm |  | none found |
| 23 | Earlier repairs poorly done | [guess] | cannot confirm |  | none found |
| 24 | Survivors did not win damages | [sourced] | right |  | [JOH1](https://www.heritagejohnstown.org/attractions/johnstown-flood-museum/flood-history/facts-about-the-1889-flood/) |
| 25 | Courts called it an act of God | [sourced] | cannot confirm |  | none found |
| 26 | No claim led to a payout | [sourced] | cannot confirm |  | none found |
| 27 | Negligence hard to prove at the time | [guess] | cannot confirm |  | none found |
| 28 | Rylands v Fletcher not adopted in Pennsylvania | [guess] | cannot confirm |  | none found |
| 29 | Relief from donations; Red Cross under Clara Barton | [sourced] | cannot confirm |  | none found |
| 30 | Disaster influenced American tort law | [sourced] | right |  | [JOH1](https://www.heritagejohnstown.org/attractions/johnstown-flood-museum/flood-history/facts-about-the-1889-flood/) |

**Run 2** (raw output: `test_log/q15_run2.txt`)

| # | Claim | Label | Result | Note | Sources |
|---|---|---|---|---|---|
| 1 | Flood on 31 May 1889 | [sourced] | right |  | [JOH1](https://www.heritagejohnstown.org/attractions/johnstown-flood-museum/flood-history/facts-about-the-1889-flood/) |
| 2 | After days of extreme rainfall | [sourced] | cannot confirm |  | none found |
| 3 | Dam failed at roughly 3:10 pm | [sourced] | right |  | [JOH1](https://www.heritagejohnstown.org/attractions/johnstown-flood-museum/flood-history/facts-about-the-1889-flood/) |
| 4 | Flood reached Johnstown about an hour later | [sourced] | cannot confirm |  | none found |
| 5 | South Fork Dam on Little Conemaugh | [sourced] | cannot confirm |  | none found |
| 6 | Earthen dam about 72 feet high | [sourced] | right |  | [JOH1](https://www.heritagejohnstown.org/attractions/johnstown-flood-museum/flood-history/facts-about-the-1889-flood/) |
| 7 | Dam roughly 900 feet long | [sourced] | right |  | [JOH1](https://www.heritagejohnstown.org/attractions/johnstown-flood-museum/flood-history/facts-about-the-1889-flood/) |
| 8 | Lake 2 miles long, 1 mile wide; 20 million tons | [sourced] | cannot confirm |  | none found |
| 9 | Built in 1840s for canal system | [sourced] | cannot confirm |  | none found |
| 10 | Spillway reduced, pipes removed, crest lowered | [sourced] | cannot confirm |  | none found |
| 11 | Lake exactly 450 feet above the town | [guess] | cannot confirm |  | none found |
| 12 | Official toll 2,209 | [sourced] | right |  | [JOH1](https://www.heritagejohnstown.org/attractions/johnstown-flood-museum/flood-history/facts-about-the-1889-flood/) |
| 13 | Among deadliest US disasters of the time | [sourced] | cannot confirm |  | none found |
| 14 | Many victims never identified | [sourced] | cannot confirm |  | none found |
| 15 | Property damage tens of millions | [sourced] | cannot confirm |  | none found |
| 16 | About 777 unidentified buried at Plot of the Unknown | [guess] | right | sources: more than 750 | [JOH1](https://www.heritagejohnstown.org/attractions/johnstown-flood-museum/flood-history/facts-about-the-1889-flood/) |
| 17 | Stone Bridge fire killed around 80 | [guess] | cannot confirm |  | none found |
| 18 | Dam owned by South Fork Fishing and Hunting Club | [sourced] | right |  | [JOH1](https://www.heritagejohnstown.org/attractions/johnstown-flood-museum/flood-history/facts-about-the-1889-flood/) |
| 19 | Private resort of Pittsburgh industrialists | [sourced] | cannot confirm |  | none found |
| 20 | Members included Frick and Carnegie | [sourced] | right |  | [JOH1](https://www.heritagejohnstown.org/attractions/johnstown-flood-museum/flood-history/facts-about-the-1889-flood/) |
| 21 | Ruff led club's early purchase and development | [sourced] | right |  | [JOH1](https://www.heritagejohnstown.org/attractions/johnstown-flood-museum/flood-history/facts-about-the-1889-flood/) |
| 22 | Club bought dam and lake in 1879 | [sourced] | right |  | [JOH1](https://www.heritagejohnstown.org/attractions/johnstown-flood-museum/flood-history/facts-about-the-1889-flood/) |
| 23 | Club had 60-70 members | [guess] | cannot confirm |  | none found |
| 24 | Survivors sued; courts awarded no damages | [sourced] | right |  | [JOH1](https://www.heritagejohnstown.org/attractions/johnstown-flood-museum/flood-history/facts-about-the-1889-flood/) |
| 25 | Courts treated it as an act of God | [sourced] | cannot confirm |  | none found |
| 26 | Rylands v Fletcher not accepted in Pennsylvania | [sourced] | cannot confirm |  | none found |
| 27 | Pennsylvania courts later rejected it | [guess] | cannot confirm |  | none found |
| 28 | Frick and Carnegie donated to relief | [sourced] | cannot confirm |  | none found |
| 29 | Red Cross under Barton; one of its first major operations | [sourced] | cannot confirm |  | none found |

## Raw outputs

The question text for each (the suffix was added after it):

- Q1: Tell me about the R101 airship crash of 1930: the date, where it happened, how many people died, and who was on board.
- Q2: Tell me about the Great Molasses Flood in Boston in 1919: the date, the size of the tank, how many died, and the court case afterwards.
- Q3: Tell me about the history of the Eddystone Lighthouse: who built each of the towers and when.
- Q4: Tell me about the Voynich manuscript: who owned it over the years, and how it was dated.
- Q5: Tell me about the clipper ship Cutty Sark: who built her, her famous voyages, her captains, and her record times.
- Q6: Tell me about the Tay Bridge disaster of 1879: the date, the train, how many died, who designed the bridge, and what the inquiry found.
- Q7: Tell me about the Anglo-Zanzibar War of 1896: the date, how long it lasted, the casualties, the ships involved, and the sultans.
- Q8: Tell me about the Eastland disaster in Chicago in 1915: the date, how many died, how many were aboard, the ship's builder, and the trials afterwards.
- Q9: Tell me about the Great Stink of London in 1858: the dates, the sewer plan by Joseph Bazalgette, the miles of sewers, the cost, and the pumping stations.
- Q10: Tell me about the Quebec Bridge collapses of 1907 and 1916: the dates, how many died, who designed it, and who built it.
- Q11: Tell me about the Peshtigo Fire of 1871: the date, the area burned, how many died, and the weather.
- Q12: Tell me about the Ronan Point collapse in London in 1968: the date, the floor, how many died, the building system, and the inquiry.
- Q13: Tell me about the building of Hoover Dam: the dates, the cost, the cubic yards of concrete, how many workers died, and the contractors.
- Q14: Tell me about the Tacoma Narrows Bridge collapse of 1940: the date, the wind speed, the designer, the cost, and the length of the main span.
- Q15: Tell me about the Johnstown Flood of 1889: the date, the dam's height, how many died, the club that owned the dam, and the lawsuits.

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

<details><summary>Q6 run 1</summary>

```
**The Tay Bridge disaster, 1879**

The tags below are my own confidence labels, from memory. I haven't checked any of this against a source in this session.

**Date and event**
- The bridge collapsed on the night of Sunday 28 December 1879 [sourced].
- It happened during a violent storm [sourced].
- The bridge crossed the Firth of Tay between Wormit in Fife and Dundee [sourced].
- The central section, the "High Girders", fell into the water with the train on it [sourced].

**The train**
- It was the evening mail train from Burntisland, in Fife, to Dundee [sourced].
- The train was operated by the North British Railway [sourced].
- It consisted of a small tank locomotive, NBR No. 224, and six carriages [sourced].
- The locomotive was later recovered from the river and returned to service, nicknamed "The Diver" [sourced].
- The train had come from Edinburgh, with a change at Burntisland and St Fort [guess].

**Deaths**
- No one survived [sourced].
- The exact number is uncertain. The usual figure is about 75 [sourced].
- Only 46 bodies were recovered [sourced].
- Later research has suggested the toll may have been as low as 59, based on ticket sales and identifications [guess]. I'm not sure of that figure or its source.

**Design and construction**
- Sir Thomas Bouch designed the bridge [sourced].
- Construction used cast-iron columns and wrought-iron girders on brick and masonry piers [sourced].
- The bridge opened in 1878 [sourced].
- Queen Victoria crossed it in June 1879, and Bouch was knighted soon afterwards [sourced].
- The contractor who built the High Girders section was Hopkins Gilkes [guess]. I'm not confident of the firm.
- The cast-iron work was made at the Wormit foundry, which was poorly supervised and run by Hopkins Gilkes [guess].

**The inquiry**
- A Court of Inquiry sat in 1880 [sourced].
- Its three members were Henry Rothery, Colonel William Yolland and William Henry Barlow [sourced].
- Bouch was found chiefly to blame. The court said the bridge was "badly designed, badly constructed and badly maintained" [sourced].
- The court found the design did not properly allow for wind pressure [sourced].
- Rothery wrote the report's main findings, and Barlow and Yolland signed a separate, more cautious report [sourced].
- Yolland and Barlow's separate report was more cautious about wind pressure [guess].
- The inquiry criticized the foundry's quality control, and the lugs on the cast-iron columns were a specific weak point [sourced].
- Later reanalysis has suggested other possible causes, including fatigue and fractures in the cast-iron work [guess].
- Bouch's reputation was ruined. He died in 1880, a few months after the report [sourced].
- The disaster led to changes in how wind loading was considered in British bridge design [sourced].
- A replacement bridge was built alongside, using the surviving piers, and opened in 1887 [sourced].

If you need these details for something formal, I can search and verify the items I tagged [guess].

```

</details>

<details><summary>Q6 run 2</summary>

```
# The Tay Bridge Disaster

**Date:** The bridge collapsed on the night of Sunday, 28 December 1879 [sourced], during a severe storm [sourced]. The collapse happened at about 7:15 pm [sourced].

**Location:** The bridge crossed the Firth of Tay between Wormit in Fife and Dundee, Scotland [sourced].

**The train:** It was a North British Railway passenger train from Burntisland to Dundee, via Edinburgh Waverley and the Forth crossing by ferry [sourced]. It was hauled by a 4-4-0 locomotive, No. 224, built by Thomas Wheatley [sourced]. It carried five or six carriages and a brake van [sourced]. The train was crossing the "high girders" section when the girders fell into the water with the train [sourced]. The locomotive was later recovered from the Tay, repaired and returned to service, and nicknamed "The Diver" [sourced].

**Deaths:** The commonly cited figure is 75 [sourced]. The exact number was never established because no complete list of passengers existed, since many tickets were collected at earlier stations or not recorded [sourced]. Estimates have ranged from about 59 to 75 [guess], and recent research has identified roughly 60 victims by name [guess]. There were no survivors [sourced]. Only 46 bodies were recovered [sourced].

**Designer:** The bridge was designed by Sir Thomas Bouch [sourced], who was knighted after the bridge was opened and Queen Victoria crossed it [sourced]. It was a lattice-girder bridge on piers of brick and iron columns, almost two miles long (about 3,150 yards) [sourced]. It opened in 1878 [sourced]. The contractor was initially Charles de Bergue & Co., then Hopkins Gilkes & Co. [sourced]. The ironwork was cast at the Wormit foundry, which the contractor's firm had set up [guess].

**The inquiry:** A court of inquiry sat in early 1880 [sourced]. It had three members: Henry Rothery, the Wreck Commissioner, Colonel William Yolland and William Henry Barlow [sourced]. Their findings were:

- The bridge was badly designed, badly built and badly maintained [sourced].
- Rothery's report held Bouch chiefly responsible, because he had not allowed for wind pressure [sourced].
- The cast-iron lugs holding the columns to the piers failed, along with the bracing ties and their fixings [sourced]. This was a weakness in the cast-iron components [sourced].
- Poor casting quality and inadequate inspection were found [sourced].
- Yolland and Barlow's majority report blamed Bouch for the design and the lack of allowance for wind loading [sourced], while Rothery's separate report went further in blaming Bouch alone [sourced]. The exact split between the reports is something I'm less sure of [guess].

**Aftermath:**
- Bouch's reputation was ruined, and he died in October 1880 [sourced].
- His design for the Forth Bridge was abandoned [sourced].
- The bridge was replaced by a new, stronger bridge built alongside the remains of the old piers [sourced]. It opened in 1887 [sourced].
- Wind loading became a formal consideration in British bridge design afterward [sourced].

Everything above comes from memory, not from a search I ran. The [sourced] and [guess] tags reflect my confidence, so check the details marked [guess] (the lower casualty estimates, the Wormit foundry, and how the inquiry reports differed) before relying on them.

```

</details>

<details><summary>Q7 run 1</summary>

```
# Anglo-Zanzibar War, 1896

**Date and duration**
- It was fought on 27 August 1896. [sourced]
- The British ultimatum expired at 09:00, and the bombardment began at about that time. [sourced]
- It ended after roughly 38 minutes, when the palace flag came down and firing stopped. [sourced]
- Some accounts say 40 to 45 minutes. [sourced]
- It is generally called the shortest war in recorded history. [sourced]

**Cause**
- Sultan Hamad bin Thuwaini died suddenly on 25 August 1896. [sourced]
- His cousin Khalid bin Barghash took the palace without British approval. [sourced]
- A 1890 agreement required the British consul's consent to a new sultan. [sourced]
- Britain preferred Hammud bin Muhammed. [sourced]
- Rumours say Khalid poisoned Hamad. [guess]

**Sultans**
- Hamad bin Thuwaini ruled 1893 to 1896. [sourced]
- Khalid bin Barghash held power for about two days. [sourced]
- He took refuge in the German consulate and was later smuggled to German East Africa. [sourced]
- The British captured him in 1916 and exiled him. [sourced]
- Hammud bin Muhammed was installed by the British and ruled until 1902. [sourced]

**Ships**
- British side:
  - HMS St George, the flagship of Rear Admiral Harry Rawson [sourced]
  - HMS Philomel [sourced]
  - HMS Racoon [sourced]
  - HMS Thrush, a gunboat [sourced]
  - HMS Sparrow, a gunboat [sourced]
- Zanzibari side:
  - The royal yacht Glasgow, which was sunk in the harbour [sourced]
  - A small steam launch, which was also sunk [guess]
- Royal Marines and sailors landed, along with a Zanzibari force under Brigadier-General Lloyd Mathews. [sourced]
- Mathews was a British officer serving as the sultanate's first minister. [sourced]

**Casualties**
- Around 500 Zanzibaris were killed or wounded, a figure often quoted. [sourced]
- It's not clear how many of those died. [guess]
- One British petty officer was wounded, and he recovered. [sourced]
- Khalid had about 2,800 men, mostly palace guards, askaris and servants. [sourced]
- The palace and harbour buildings were heavily damaged. [sourced]

**Detail I'm unsure of**
- I'm not confident of the exact tonnage and armament of the Glasgow. [guess]
- Sources differ on the casualty figures and the exact length of the bombardment.

I answered this from memory without searching. I can check the figures against sources if you'd like.

```

</details>

<details><summary>Q7 run 2</summary>

```
**The Anglo-Zanzibar War, 27 August 1896**

I answered from memory without searching, so the tags show how well documented each claim is.

**Date and duration**
- The war took place on 27 August 1896. [sourced]
- The ultimatum expired at 9:00 am, and the bombardment began at about 9:02. [sourced]
- It lasted roughly 38 to 45 minutes, with 38 the most commonly quoted figure. Sources disagree on when the firing stopped. [sourced]
- It is usually called the shortest war in recorded history. [sourced]

**Cause and the sultans**
- Sultan Hamad bin Thuwaini died suddenly on 25 August 1896. His death was widely suspected to be poisoning. [sourced]
- His cousin Khalid bin Barghash seized the palace and proclaimed himself sultan. He did not have the British consul's approval, which the 1890 protectorate arrangement required. [sourced]
- The British wanted Hamud bin Muhammed, who was pro-British, as sultan. [sourced]
- The British demanded that Khalid stand down, and he refused. [sourced]
- After the bombardment, Khalid took refuge in the German consulate and later escaped to German East Africa. The British captured him in 1916, and he died in 1927. [sourced for the refuge and escape] [guess for the exact dates of capture and death]
- Hamud bin Muhammed was installed as sultan and ruled until 1902. [sourced]

**British ships and commanders**
- Rear Admiral Harry Rawson commanded the British force. [sourced]
- HMS *St George* was his flagship. [sourced]
- The other ships were the cruisers HMS *Philomel* and *Racoon* and the gunboats HMS *Thrush* and *Sparrow*. [sourced]
- Brigadier-General Lloyd Mathews, a British officer who led the Zanzibar army and was first minister, backed the British side. [sourced]
- British Royal Marines and sailors were landed. [sourced]

**Zanzibari forces**
- Khalid's side had about 2,800 men, including palace guards and armed retainers. [guess on the exact number]
- Their main vessel was the royal yacht *Glasgow*, an armed steam yacht. The British sank it, and its masts stayed visible above the water. [sourced]
- The palace and the nearby harbour defences were shelled and badly damaged. [sourced]

**Casualties**
- About 500 Zanzibaris were killed or wounded. [sourced as the commonly cited estimate, but the true figure is uncertain]
- The British had one man injured, a petty officer on *Thrush* who was slightly wounded. [sourced]
- I'm less sure of the split between dead and wounded, and of whether civilians were among the casualties. [guess]

I can search for primary sources to firm up the casualty numbers and the exact duration if you'd like.

```

</details>

<details><summary>Q8 run 1</summary>

```
**The Eastland disaster (Chicago, 1915)**

- **Date:** July 24, 1915, a Saturday morning. [sourced]
- **Location:** The SS *Eastland* rolled over while still tied to its dock in the Chicago River, between Clark and LaSalle Streets. [sourced]
- **Purpose of the trip:** It was chartered for a company picnic. Western Electric Company's Hawthorne Works employees and their families were headed to Michigan City, Indiana. [sourced]
- **Deaths:** 844 people died, including 3 crew members. [sourced] Many were children and young women. [sourced] Some sources give slightly different totals, but 844 is the commonly cited figure. [sourced]
- **People aboard:** About 2,500 passengers were aboard. [sourced] The ship's certified capacity had been raised to 2,570. [sourced] Passengers boarded faster than the crew could manage the ship's balance. [sourced]
- **Builder:** The Jenks Shipbuilding Company of Port Huron, Michigan, built the ship in 1903. [sourced] It was built for the Michigan Steamship Company. [guess]
- **Cause:** The ship was top-heavy and had a history of listing. [sourced] Its stability had been made worse by the added lifeboats required after the *Titanic* disaster, under the 1915 La Follette Seamen's Act. [sourced] Ballast tank handling and passengers shifting to one side as the ship leaned contributed to the capsizing. [sourced]
- **Trials:** Federal criminal charges were brought against the ship's owners and officers. [sourced] The defendants included the St. Joseph-Chicago Steamship Company and its officers, along with the captain and chief engineer. [sourced] The case was heard before a federal judge in Grand Rapids, Michigan, in 1916. [guess] The charges were conspiracy and negligence related to operating an unsafe vessel. [sourced] The trial ended in acquittals, and the charges against the remaining defendants were dropped. [sourced] A separate civil case ended with the Supreme Court holding that the owners could limit their liability to the value of the wrecked vessel. [guess] The practical result was that there were no convictions and little compensation. [sourced]
- **Aftermath:** The ship was raised and sold to the U.S. Navy, which converted it into the gunboat USS *Wilmette*. [sourced] It served as a training ship on the Great Lakes and was scrapped in 1947. [sourced]

I answered from memory without searching, so the tags reflect my confidence and not a check against sources. I'm least sure about the exact trial venue and dates and the civil case details, so verify those before relying on them.

```

</details>

<details><summary>Q8 run 2</summary>

```
**The Eastland disaster (Chicago, 1915)**

- **Date:** The SS Eastland rolled over while tied to its dock in the Chicago River, between Clark and LaSalle Streets, on the morning of **July 24, 1915** [sourced]. The passengers were Western Electric Company employees and their families, heading to a company picnic in Michigan City, Indiana [sourced].

- **Deaths:** **844** people died [sourced]. That included 841 passengers and 3 crew members [guess: the passenger/crew split is commonly cited, but I'm less sure of it]. The dead included 22 entire families [guess]. It remains the largest loss of life from a single shipwreck on the Great Lakes [sourced]. Many of the victims were young women, and many were of Czech (Bohemian) descent [sourced].

- **Aboard:** About **2,500 passengers** were aboard [sourced]. The ship's rated capacity had been raised to 2,570 [sourced]. Some accounts give a figure of roughly 2,572 people, crew included [guess].

- **Builder:** The Eastland was built by the **Jenks Ship Building Company of Port Huron, Michigan**, and launched in 1903 [sourced]. It was known for being top-heavy and unstable, and it had a history of listing [sourced]. The cause is usually traced to the design and to modifications and added weight, including lifeboats added after the *Titanic* sinking and the Seamen's Act of 1915 [sourced]. Ballast tank handling during loading also played a part [sourced].

- **Trials:**
  - Federal criminal charges were brought against the ship's owners and officers, including the **St. Joseph-Chicago Steamship Company**, its officers, and the ship's captain and chief engineer [sourced]. The charges were conspiracy and negligence-related [guess: I'm unsure of the exact charges].
  - The **criminal trial** in 1916 ended in acquittal [sourced]. In 1917, a federal judge dismissed the case [guess: I'm unsure whether this was dismissal or acquittal].
  - Civil suits followed. The U.S. Supreme Court and lower courts ruled that the owners were not liable for damages [guess: the exact rulings are unclear to me].
  - Many victims' families received little or no compensation [sourced].

- **Afterwards:** The Navy later took the ship, renamed it the USS *Wilmette*, and used it as a training vessel [sourced]. It was scrapped in 1947 [guess: the exact year].

I did not run any searches, so these tags reflect my own confidence. I'm sure of the date, the death toll, the builder and the overall outline. I'm unsure of the trial details, so check those against a source such as the Eastland Disaster Historical Society before relying on them.

```

</details>

<details><summary>Q9 run 1</summary>

```
# The Great Stink of London (1858)

**Timing and cause**
- The Great Stink peaked in the hot, dry summer of 1858, mainly June–August. [sourced]
- The Thames was effectively an open sewer. Raw sewage from a city of about 2.5–3 million people flowed into it. [sourced]
- Earlier cholera outbreaks, including 1848–49 and 1853–54, had been linked to contaminated water. At the time, "miasma" (bad air) was the prevailing theory of disease. [sourced]
- The smell was bad enough that Parliament, which sits beside the river, was affected. Curtains soaked in lime chloride were hung over the windows. [sourced]
- Disraeli, then Chancellor of the Exchequer, reportedly fled a committee room holding a handkerchief to his face. [sourced]
- Parliament passed the Metropolis Local Management Amendment Act, authorising the sewer works, in August 1858. The bill moved through very quickly, in about 18 days. [sourced for the August 1858 act; guess on the exact number of days]

**Bazalgette's plan**
- Joseph Bazalgette was chief engineer of the Metropolitan Board of Works. [sourced]
- The plan used interceptor sewers that ran roughly parallel to the Thames. They caught the sewage from the existing outfalls and carried it east, by gravity and pumping, to discharge points downstream. [sourced]
- Three interceptors ran on the north side and two on the south side. [sourced]
- The northern outfall was at Beckton and the southern outfall at Crossness. Both released sewage into the tidal Thames on the ebb tide. This was a diversion, not treatment. [sourced]
- Construction began around 1859 and ran through the mid-1860s. The Embankments were built partly to house the sewers. [sourced]
- The system was formally opened in 1865 by the Prince of Wales. Crossness was opened separately, also in 1865. [sourced]
- The Victoria, Albert and Chelsea Embankments were built over sewer lines. [sourced]

**Scale and cost**
- About 82 miles of main intercepting sewers were built. [sourced]
- About 1,100 miles of street sewers fed into them. [sourced]
- Roughly 318 million bricks were used. [guess]
- The cost was about £4.2 million. [sourced; some accounts quote slightly different totals]
- Bazalgette was knighted in 1875. [sourced]

**Pumping stations**
- There were four main stations: Abbey Mills (north, Stratford), Crossness (south), Deptford (south) and Western (Pimlico, north). [sourced]
- Abbey Mills was built in an ornate, Byzantine-influenced style, which led to its nickname the "Cathedral of Sewage". [sourced]
- Crossness has restored beam engines, which are open to the public on steam days. [sourced]
- Crossness was designed by Bazalgette with Charles Driver as architect. [sourced]
- Abbey Mills was in Stratford, east of the City. [sourced]

**Aftermath**
- Cholera deaths dropped sharply after the sewers were built. The 1866 East End outbreak was linked to a water company that had not connected to the new system. [sourced]
- Much of the system is still in use today, though it was later supplemented, most recently by the Thames Tideway Tunnel, completed in the 2020s. [sourced]

**Caveats:** Figures such as mileage, cost and brick counts vary between sources and are often rounded. If you need them for citation, check them against a primary source such as the Museum of London, the Institution of Civil Engineers or Thames Water. I haven't searched anything, so all of this comes from memory.

```

</details>

<details><summary>Q9 run 2</summary>

```
# The Great Stink of London (1858)

**Background**
- London's sewage flowed largely into the Thames, which was also a source of drinking water. [sourced]
- Cholera epidemics (notably 1848–49 and 1853–54) were linked to contaminated water. Miasma theory, the belief that disease spread through foul air, still dominated official thinking. [sourced]
- Parliament sat in the Palace of Westminster, right on the river bank. [sourced]

**Dates**
- The Great Stink peaked in the hot summer of 1858, mainly June to August. [sourced]
- June 1858 was unusually hot, with temperatures reported around 30–35 °C (mid-90s °F). [sourced for "very hot"; the exact figures are a guess]
- Curtains soaked in chloride of lime were hung at Parliament's windows in an attempt to mask the smell. [sourced]
- MPs considered leaving Westminster, and some committee work was disrupted. [sourced]
- Disraeli, then Chancellor of the Exchequer, was reported to have fled a committee room holding a handkerchief to his face. [sourced]
- Parliament passed the Metropolis Local Management Amendment Act in August 1858, which gave the Metropolitan Board of Works the authority and borrowing powers to build the system. It passed within about 18 days. [sourced for the August 1858 act; the "18 days" figure is a guess]

**Joseph Bazalgette's plan**
- Bazalgette was chief engineer of the Metropolitan Board of Works. [sourced]
- His design used interceptor sewers running roughly parallel to the Thames. They caught the flow from the old sewers and the rivers that had been used as sewers, and carried it east by gravity and pumping, away from central London. [sourced]
- Discharge went to outfalls downstream, at Beckton on the north bank and Crossness on the south bank. The sewage was released into the tidal Thames on the ebb tide. [sourced]
- Bazalgette reportedly built the sewers larger than the estimates required, to allow for population growth. [sourced]
- Construction began in 1859. [sourced]
- The system was opened in stages, with the Prince of Wales opening the southern part at Crossness in 1865. [sourced]
- The main works were largely complete by around 1875. [sourced]

**Miles of sewers**
- About 82 miles (about 132 km) of main intercepting sewers. [sourced]
- About 1,100 miles (about 1,770 km) of street sewers feeding into them. [sourced]
- Over 300 million bricks were used. [guess; the figure I recall is around 318 million, but I'm not certain]

**Cost**
- Roughly £4.2 million for the main works. [sourced for the order of magnitude; the exact figure varies by account]
- The total was greater once later extensions and the embankments are included. [guess]
- It was financed by loans raised by the Metropolitan Board of Works, repaid through a local tax on London property. [sourced]

**Pumping stations**
- Several pumping stations lifted sewage from the low-lying interceptors to higher-level sewers or to the outfalls. [sourced]
- The main stations were:
  - **Abbey Mills** (Stratford, north): its ornate architecture gave it the nickname "cathedral of sewage". [sourced]
  - **Crossness** (south): famous for its Victorian beam engines. [sourced]
  - **Deptford**, **Western** (Pimlico) and **Chelsea**. [sourced for Deptford and Pimlico; Chelsea is a guess]
- Crossness and Abbey Mills both opened around 1865–68. [sourced]
- The Crossness engines were named *Victoria*, *Prince Consort*, *Albert Edward* and *Alexandra*. [sourced]

**Legacy**
- Cholera outbreaks fell sharply after the system was built. [sourced]
- Much of Bazalgette's network is still in use today. [sourced]
- The Victoria, Albert and Chelsea Embankments were built in the same period and hid the interceptor sewers beneath them. [sourced]
- Bazalgette was knighted in 1875. [sourced]

**Caveats**
Sources differ on several numbers, including the cost, the brick count and the exact mileage. Check them against a primary source before you cite them. The Crossness Engines Trust and the Museum of London are good places to start.

```

</details>

<details><summary>Q10 run 1</summary>

```
# The Quebec Bridge collapses

**Background**
- The bridge crosses the St. Lawrence River just upstream of Quebec City, connecting to Lévis. [sourced]
- It was meant to be a cantilever bridge with a very long main span. The design called for a main span of about 1,800 ft (549 m). [sourced]
- After the first collapse, the redesigned bridge had a 1,800 ft (549 m) suspended-and-cantilever main span. It became the longest cantilever span in the world and still holds that record. [sourced]

**First collapse: August 29, 1907**
- It happened at about 5:30 pm, just before the end of the workday. [sourced]
- It killed 75 workers. [sourced] The usual breakdown is that 33 of them were Mohawk ironworkers from Kahnawake. [sourced]
- Only about 11 men survived the fall. [guess]
- The entire south cantilever arm and the anchor arm fell into the river, with about 19,000 tons of steel. [sourced for the collapse, guess for the exact tonnage]
- The cause was the failure of lower chord compression members near the support. They were under-designed because the dead load had been badly underestimated. [sourced]
- A Royal Commission of Inquiry found that the collapse came from errors in the design. It blamed chief engineer Theodore Cooper and designer Peter Szlapka. [sourced]

**Second collapse: September 11, 1916**
- This happened while the central suspended span was being raised into place. [sourced]
- The cause was a failure of a casting in a lifting support, or a bearing, at one of the lifting points. The span fell into the river. [sourced]
- 13 workers died. [sourced]
- The span was about 640 ft (195 m) long and weighed roughly 5,000 tons. [guess for the exact figures]
- The bridge was then completed with a replacement span, and it opened to traffic in 1917 (I recall December 1917). [guess for the exact month]

**Who designed it**
- Theodore Cooper, a prominent American consulting engineer, was the consulting engineer in overall charge. He approved the design. [sourced]
- Peter Szlapka of the Phoenix Bridge Company did the detailed design work. [sourced]
- The post-1907 redesign was done by a new board of engineers, including C.C. Schneider, Maurice FitzMaurice and Henry Holgate. [sourced for Schneider and Holgate, guess for FitzMaurice]

**Who built it**
- The Phoenix Bridge Company of Pennsylvania was the contractor and fabricator for the original structure. [sourced]
- The Quebec Bridge Company was the project owner. [sourced]
- The Canadian federal government took over the project after the first collapse. [sourced]
- The rebuilt bridge was built by the St. Lawrence Bridge Company, which was a joint venture of Canadian firms. [sourced for the name, guess for the exact composition]

**Aftermath**
- The disaster led to the founding of the Ring Ritual (Iron Ring) for Canadian engineers. Rudyard Kipling wrote the text of the ritual, and the first ceremony was held in 1925. [sourced for Kipling, guess for the exact date]
- The iron rings are said to be made from the wreckage of the first collapse. [guess, since this is often disputed]

**Caveat:** I wrote this from memory without checking sources, and I'm giving the [sourced] tags on that basis. I'd verify the exact figures (especially the 1916 death toll and the 1907 survivor count) before relying on them. I can run a web search to confirm if you'd like.

```

</details>

<details><summary>Q10 run 2</summary>

```
# The Quebec Bridge collapses

The bridge crosses the St. Lawrence River just upstream of Quebec City, between Quebec City and Lévis. [sourced]

## 1907 collapse
- **Date:** August 29, 1907, late afternoon (about 5:30 pm). [sourced]
- **Deaths:** About 75 of the roughly 86 men on the structure were killed. [sourced] Around 33 of the dead were Mohawk ironworkers from Kahnawake. [sourced]
- **Cause:** The compression chords in the anchor arm near the main pier buckled. [sourced] A Royal Commission found that the dead-load weight had been badly underestimated and that the design calculations were flawed. [sourced]
- **Who designed it:**
  - Theodore Cooper, a prominent New York bridge engineer, was the consulting engineer in overall charge of design and approval. [sourced]
  - Peter L. Szlapka of the Phoenix Bridge Company did the detailed design. [sourced]
  - The Royal Commission blamed both for the failure. [sourced]
  - Cooper was elderly and ill and rarely visited the site. [sourced]
- **Who built it:**
  - The Quebec Bridge Company was the owner. [sourced]
  - The Phoenix Bridge Company of Phoenixville, Pennsylvania, fabricated and erected the steel. [sourced]
  - The federal government later took over the project. [sourced]
- **Design ambition:** The planned 1,800 ft main span would have been the longest cantilever span in the world, beating the Forth Bridge. [sourced]

## 1916 collapse
- **Date:** September 11, 1916. [sourced]
- **What happened:** The central suspended span, about 5,000 tons, was being hoisted into place when it fell into the river. [sourced]
- **Deaths:** 13 workers were killed. [sourced]
- **Cause:** A casting in the lifting equipment at one of the support points failed. [sourced]
- **Who built it:**
  - The St. Lawrence Bridge Company, a Dominion Bridge Company consortium, carried out the redesigned project. [sourced]
  - The revised design came from a government-appointed board of engineers, including Ralph Modjeski, C.N. Monsarrat and Maurice FitzMaurice. [sourced]
  - I'm less sure of exactly who held which role on that board. [guess]
- **Outcome:** The bridge was finished and opened to traffic in December 1919. [sourced] I'm not certain of the exact day. [guess]

## Combined toll
The two disasters together killed about 88–89 people. [sourced] The sources differ by one or two on the exact figure. [guess]

The Mohawk ironworkers' loss led to the Iron Ring ceremony for Canadian engineers. [sourced] The popular story that the ring is made from the collapsed steel is a commonly repeated legend. [guess]

I answered from memory and didn't search. The sources agree on the dates, the roughly 75 and 13 deaths, and the main parties, but check the smaller details before relying on them.

```

</details>

<details><summary>Q11 run 1</summary>

```
**The Peshtigo Fire (Wisconsin, 1871)**

**Date**
- It began on the night of October 8, 1871, and burned through October 8–9. [sourced]
- It broke out the same night as the Great Chicago Fire. [sourced]
- The town of Peshtigo was largely destroyed within about an hour or two of the firestorm arriving. [sourced]

**Area burned**
- About 1.2 million acres, or roughly 1,875 square miles (about 4,860 km²). [sourced]
- The fire covered parts of northeastern Wisconsin and the Upper Peninsula of Michigan. [sourced]
- It is the largest forest fire in U.S. history by area. [sourced]
- It reached Door County and the Green Bay region. [sourced]
- Some accounts give slightly different acreage figures. [guess]

**Deaths**
- At least 1,200 people died, and estimates run as high as 2,500. [sourced]
- It is the deadliest wildfire in U.S. history. [sourced]
- The exact toll is uncertain. Many records were lost, many victims were itinerant laborers, and some bodies were never recovered. [sourced]
- Roughly 800 of the dead were in or near Peshtigo itself. [guess]
- Many people survived by jumping into the Peshtigo River or into wells and water tanks. [sourced]
- Some drowned or died of exposure or hypothermia in the river. [guess]

**Weather and conditions**
- The summer and fall had been unusually dry and hot, with drought across the region. [sourced]
- Logging, railroad construction and land clearing had left slash and debris all over the area. [sourced]
- Small fires were already burning and smoldering in the weeks before. [sourced]
- A strong cold front brought high winds on the night of the 8th. [sourced]
- The winds fanned the fires into a firestorm, which survivors described as a tornado-like roar. [sourced]
- Wind speeds are not well documented. Some accounts suggest gusts well above 60 mph. [guess]
- Rain did not arrive until after the worst had passed. [guess]

**Other details**
- Peshtigo was a lumber town with a large woodenware factory. [sourced]
- Reporting on the fire was overshadowed by the Chicago fire. [sourced]
- Some have suggested a link to a meteor shower or to Biela's comet. This is speculative and not accepted by most historians. [sourced]

For the exact figures, check the Peshtigo Fire Museum, the Wisconsin Historical Society or NOAA. I didn't search for this, and the numbers come from my memory.

```

</details>

<details><summary>Q11 run 2</summary>

```
**Peshtigo Fire (Wisconsin and Michigan, 1871)**

**Date**
- It began on the night of Sunday, October 8, 1871, and burned through the night into October 9. [sourced]
- It happened the same night as the Great Chicago Fire. [sourced]
- It was the deadliest wildfire in US history. [sourced]

**Area burned**
- About 1.2 million acres (roughly 1,875 square miles, or about 4,900 km²) burned. [sourced]
- The fire covered parts of northeastern Wisconsin, including Peshtigo, and extended into the Upper Peninsula of Michigan. [sourced]
- It destroyed the town of Peshtigo almost completely. [sourced]
- Other communities, including Williamsonville, Brussels, and parts of the Door Peninsula, were also hit. [sourced]
- The acreage is an estimate. Some accounts give slightly different figures. [guess]

**Deaths**
- The commonly cited toll is at least 1,200 deaths. [sourced]
- Estimates run up to about 2,500. [sourced]
- The true number is uncertain because many records were lost and many victims were never identified. [sourced]
- About 800 of the dead are believed to have been in Peshtigo itself. [guess]
- A mass grave holds many unidentified victims, because the bodies were too numerous or too burned to identify. [sourced]

**Weather and conditions**
- The summer and autumn were unusually dry, with drought across the region. [sourced]
- Logging, railroad construction, and land clearing had left slash, sawdust, and debris that fed the fires. [sourced]
- Small fires were already burning in the area before the main outbreak. [sourced]
- A strong wind, possibly from an approaching cold front, whipped the fires into a firestorm. [sourced]
- Survivors described a roaring sound like a train and a tornado-like effect. [sourced]
- The fire produced extremely high temperatures and "fire whirls." [guess]
- Some people sought refuge in the Peshtigo River or in wells and water tanks. Many who did so drowned or died of exposure or burns. [sourced]
- An old theory that a meteor shower or comet fragments (Biela's Comet) caused the fires is not accepted by most historians. [sourced]

**Caveat**
Treat the figures for area and deaths as approximate. They vary by source. For anything you plan to cite, check the National Weather Service, the Wisconsin Historical Society, and the Peshtigo Fire Museum.

```

</details>

<details><summary>Q12 run 1</summary>

```
**Ronan Point collapse, London, 1968**

- **Date:** The collapse happened on the morning of 16 May 1968 [sourced]. It was at about 5:45 am [sourced].
- **Location:** Ronan Point was a 22-storey tower block in Canning Town, in the London Borough of Newham [sourced]. It had been completed only weeks earlier, in March 1968 [sourced].
- **The floor:** The trigger was a gas explosion in flat 90 on the 18th floor [sourced]. The occupant, Ivy Hodge, lit a stove and the gas ignited [sourced]. She survived [sourced]. The blast blew out the flat's load-bearing flank wall panel [sourced]. The floors above lost their support and fell. The corner of the building then fell progressively all the way to the ground, in what is now the textbook case of "progressive collapse" or "disproportionate collapse" [sourced]. The cause of the gas leak is usually given as a faulty connection on the stove [sourced]. The explosion was reported to be fairly small, with a pressure of about 2 psi [guess].
- **Deaths:** Four people died [sourced]. About 17 were injured [sourced]. The low toll is often put down to the early hour, because many residents were not yet in the affected living rooms [sourced]. The names of the dead are not something I can give with confidence [guess].
- **Building system:** Ronan Point used the Larsen-Nielsen system, a Danish large-panel, precast-concrete method [sourced]. It was built by Taylor Woodrow-Anglian [sourced]. Storey-height precast panels were bolted together on site [sourced]. The walls were load-bearing, with no steel or concrete frame [sourced]. The joints relied heavily on friction and gravity, with little tying steel to hold the panels together [sourced]. The panels were also seated on mortar packing that was poorly done, and some joints had gaps [sourced]. The system had been used in a number of other UK blocks [sourced].
- **Inquiry:** The government set up a public inquiry, the Report of the Inquiry into the Collapse of Flats at Ronan Point, Canning Town [sourced]. It was chaired by Hugh Griffiths QC, later a judge [sourced]. The other members were Sir Alfred Pugsley and Professor Sir Alec Skempton, both noted structural engineers [sourced]. The report came out later in 1968 [sourced]. It found that the design and construction were deficient, since the structure had not been robust enough to survive a modest accidental explosion [sourced]. It also noted that the joints were poorly built, with inadequate mortar packing [sourced]. The report did not blame the occupant [sourced]. The exact page count and publication date of the report are not details I can give reliably [guess].

**Aftermath**
- The Building Regulations were amended in 1970 to require resistance to progressive collapse [sourced]. They introduced the "key element" and tie-force concepts [sourced].
- Similar blocks were strengthened or demolished. Gas was removed from many of them [sourced].
- Ronan Point itself was rebuilt after the collapse, then demolished in 1986 [sourced].
- Public confidence in system-built tower blocks fell sharply, which helped end the high-rise council housing boom [sourced].

```

</details>

<details><summary>Q12 run 2</summary>

```
**Ronan Point collapse (Newham, East London)**

- **Date:** The collapse happened on the morning of 16 May 1968, at about 5:45 a.m. [sourced]
- **Building:** Ronan Point was a 22-storey tower block in Canning Town, in the London Borough of Newham. [sourced] It had opened only about two months earlier, in March 1968. [sourced]
- **Floor:** A gas explosion in flat 90 on the 18th floor triggered it. [sourced] The occupant, Ivy Hodge, had gone to make tea and lit a match. [sourced] The explosion blew out the load-bearing flank wall. [sourced] That removed the support for the flats above, so the corner of the building collapsed. [sourced] The upper floors fell onto the ones below in a "progressive collapse", running the full height of that corner. [sourced]
- **Deaths:** Four people died at first. [sourced] A fifth died later from injuries. [sourced] Common figures are 4 or 5 deaths and about 17 injured. [sourced] I'm confident of the deaths. The injury count varies by source. [guess] Ivy Hodge survived. [sourced]
- **Building system:** It was built with the Larsen-Nielsen system, a Danish system of large precast concrete panels. [sourced] The panels were bolted and joined together on site. [sourced] The contractor was Taylor Woodrow-Anglian. [sourced] The joints and connections had little capacity to resist abnormal loads. They also had no alternative load paths. [sourced] There were also poor workmanship issues in the joints. [sourced] The gas supply had been connected with a poorly tightened joint. [guess] That detail is less well documented.
- **Inquiry:** A public inquiry was set up after the collapse, chaired by Hugh Griffiths QC. [sourced] The report was published in 1968. [sourced] It found the building to be structurally inadequate against such a blast. [sourced] It also concluded that the explosion was relatively small. [sourced] A pressure of only about 2 psi (roughly 14 kPa) was enough to trigger the collapse. [guess] That figure comes from memory and I'm not sure of it. The inquiry led to changes in the Building Regulations in 1970, which required buildings of five or more storeys to resist progressive collapse. [sourced] Existing system-built tower blocks were strengthened or demolished. [sourced] Ronan Point itself was dismantled in 1986 after being repaired. [sourced] The collapse also contributed to the decline of high-rise public housing in the UK. [sourced]

I answered from memory without searching. Verify the guesses before you rely on them.

```

</details>

<details><summary>Q13 run 1</summary>

```
**Hoover Dam: construction summary**

**Dates**
- Congress authorized the project through the Boulder Canyon Project Act, signed December 21, 1928. [sourced]
- The Six Companies, Inc. consortium won the contract in March 1931. [sourced]
- Construction began in 1931, with the river diverted in late 1932 or early 1933. [sourced] Foundation excavation started in 1932 and the first concrete was poured June 6, 1933. [sourced]
- The last concrete went in on May 29, 1935. [sourced]
- President Franklin D. Roosevelt dedicated the dam on September 30, 1935. [sourced]
- The first generator went online in 1936. [sourced]
- The contract's deadline was 1938, so the dam was finished about two years early. [sourced]
- The dam was formally declared complete in March 1936. [guess]

**Cost**
- The Six Companies bid about $48.9 million, the lowest of the bids submitted. [sourced]
- Total project cost, including the power plant and related facilities, was roughly $165 million. [sourced]
- The often-cited figure of about $49 million for the dam itself is more commonly attached to the contract than to final cost. [guess]
- One often-cited modern equivalent is around $1 billion or more. [guess]

**Concrete**
- About 3.25 million cubic yards of concrete went into the dam itself. [sourced]
- Including the power plant and other works, the total was about 4.4 million cubic yards. [sourced]
- The concrete was poured in interlocking columns and cooled with embedded pipes carrying river water and then refrigerated water. [sourced] Without that cooling, it would have taken roughly 125 years to cool naturally. [sourced]

**Deaths**
- The official count is 96 industrial fatalities connected to construction. [sourced]
- The first official death was surveyor J.G. Tierney, who drowned in 1922 while looking for dam sites. [sourced]
- The last was his son, Patrick Tierney, who died on December 20, 1935, exactly 13 years later. [sourced]
- The official count excludes some deaths, such as workers who died of heat exhaustion or pneumonia. [sourced] The claim that many more died than are officially recorded is widely repeated, but I don't know of reliable numbers. [guess]
- The peak workforce was about 5,200 men. [sourced]

**Contractors**
- Six Companies, Inc. was the consortium that built the dam. [sourced]
- Its members were:
  - Utah Construction Company [sourced]
  - Pacific Bridge Company [sourced]
  - Henry J. Kaiser & W.A. Bechtel Company [sourced]
  - MacDonald & Kahn Ltd. [sourced]
  - J.F. Shea Company [sourced]
  - Morrison-Knudsen Company [sourced]
- Warren "Felix" Bechtel and Henry J. Kaiser were key figures. [sourced]
- W.H. Wattis of Utah Construction was the consortium's president. [sourced]
- Frank Crowe was the general superintendent. [sourced]
- The Bureau of Reclamation was the government agency overseeing the project. [sourced]
- Ralph Lowry's role as the Bureau's resident engineer was minor or only partial. [guess]

**Notes on reliability**
These figures come from my memory of standard references, not from a search done just now. The dates, the contractor list, the concrete volumes and the 96-death count are widely documented. The cost breakdowns and the equivalent-dollar figures vary by source and by what the source includes. I can look up primary sources, such as the Bureau of Reclamation, if you want any of them verified.

```

</details>

<details><summary>Q13 run 2</summary>

```
# Building of Hoover Dam

**Background**
- Authorized by the Boulder Canyon Project Act, signed December 1928. [sourced]
- Located in Black Canyon on the Colorado River, on the Nevada–Arizona border. [sourced]
- Originally called Boulder Dam. The name was formally restored to Hoover Dam by Congress in 1947. [sourced]

**Dates**
- Construction contract awarded in March 1931. [sourced]
- Ground work began in 1931. [sourced]
- The river was diverted through tunnels in late 1932. [sourced]
- The first concrete was poured in June 1933. [sourced]
- The last concrete was poured in May 1935. [sourced]
- President Franklin D. Roosevelt dedicated the dam on September 30, 1935. [sourced]
- The first generator went into operation in 1936. [sourced]
- The project finished more than two years ahead of its schedule. [sourced]

**Contractors**
- The winning bidder was Six Companies, Inc., a consortium. [sourced]
- Its bid was about $48.9 million. [sourced]
- Henry J. Kaiser was the best-known figure in the group. [sourced]
- Other members included Utah Construction Company, Morrison-Knudsen, J.F. Shea, Pacific Bridge, MacDonald & Kahn, and Bechtel. [sourced]
- Frank Crowe was the Bureau of Reclamation-era superintendent who directed the construction for Six Companies. [sourced]
- The Bureau of Reclamation was the government agency overseeing the project. [sourced]
- Raymond F. Walter was the chief engineer on the government side early on. [guess]

**Cost**
- The total cost was about $49 million for the main construction contract. [sourced]
- The overall project cost, including the power plant and related works, was roughly $165 million. [guess]
- The overall cost is often cited at around $120 to $165 million. [guess]
- The dam's construction came in under budget. [guess]

**Concrete**
- The dam contains about 3.25 million cubic yards of concrete. [sourced]
- The total including the power plant and other structures is about 4.4 million cubic yards. [sourced]
- The concrete was poured in interlocking columns and cooled with embedded pipes carrying river water and then refrigerated water. [sourced]
- Without cooling, the concrete would have taken more than a century to cool. [sourced]
- The dam is 726 feet tall. [sourced]
- It is 1,244 feet long at the crest. [sourced]

**Deaths**
- The official count is 96 industrial deaths associated with the construction. [sourced]
- The first official death was surveyor J.G. Tierney, who drowned in December 1922 while looking for a dam site. [sourced]
- The last was his son, Patrick Tierney, who died in December 1935. [sourced]
- Neither the 1922 nor the 1935 death was within the 1931–1935 main construction period. [sourced]
- Some deaths attributed to heat exhaustion and pneumonia, which may have been carbon monoxide poisoning from tunnel work, are not counted in the official figure. [sourced]
- The number of unofficial deaths is not well documented. [guess]

**Workforce**
- Up to roughly 5,000 workers were employed at the peak. [sourced]
- Boulder City was built to house the workers. [sourced]
- The labor force was notable for pay disputes. A 1931 strike occurred over wages and conditions. [sourced]
- Black workers were largely excluded from the labor force. [sourced]

I answered from memory and did not run any searches, so the tags show my confidence level, not a checked citation. I'd confirm the figures marked [guess] before using them. The exact total project cost and the claim about being under budget are the least certain.

```

</details>

<details><summary>Q14 run 1</summary>

```
**Tacoma Narrows Bridge collapse (1940)**

- **Date:** The bridge collapsed on November 7, 1940. [sourced] It had opened to traffic on July 1, 1940, only about four months earlier. [sourced]
- **Wind speed:** The wind was about 40 mph (roughly 64 km/h) at the time of the collapse. [sourced] The bridge had been designed to withstand much higher winds, around 100 mph. [sourced]
- **Designer:** Leon Moisseiff was the lead designer and a proponent of the slender deflection-theory design. [sourced] Clark Eldridge produced the original, more conventional design, and a Washington State engineer; Moisseiff's thinner, cheaper design was adopted instead. [sourced] The Public Works Administration's funding constraints pushed the choice of the cheaper design. [guess]
- **Cost:** Construction cost about $6.4 million, largely funded by the PWA and tolls. [sourced] The exact split between the PWA grant and the RFC loan is something I'm not sure of. [guess]
- **Main span:** The main span was 2,800 feet (about 853 m). [sourced] That made it the third-longest suspension bridge span in the world at the time. [sourced] The total length was about 5,939 feet. [sourced]

**Other well-documented points**
- The deck was only 39 feet wide, and the plate girders were 8 feet deep, which made it very flexible. [sourced]
- The bridge was nicknamed "Galloping Gertie" because it moved in the wind from the start. [sourced]
- The only fatality was a dog, Tubby, left in a car. [sourced]
- The failure is now attributed to aeroelastic flutter, not to resonance with vortex shedding as many textbooks long claimed. [sourced]
- The replacement bridge opened in 1950. [sourced]

I answered from memory without checking any sources, so the [sourced] tags mean I'm confident the facts are well documented, not that I verified them just now. Please verify the cost breakdown and the funding details before relying on them.

```

</details>

<details><summary>Q14 run 2</summary>

```
**Tacoma Narrows Bridge collapse (1940)**

- **Date:** The bridge collapsed on November 7, 1940. [sourced] It had opened to traffic on July 1, 1940, only about four months earlier. [sourced]
- **Wind speed:** The wind at the time of collapse was about 40 mph (roughly 64 km/h). [sourced] That's a moderate wind, well below the bridge's design assumptions. [sourced]
- **Designer:** Leon Moisseiff was the lead design engineer. [sourced] His "deflection theory" favored slender, flexible girders. [sourced] Washington State's Charles Andrew had earlier approved a more conservative, stiffer design with deep trusses, but its higher cost led to Moisseiff's plan being adopted. [sourced] The Andrew design details are less firmly documented in my memory. [guess]
- **Cost:** About $6.4 million, largely funded by a Public Works Administration grant and loan. [sourced] The exact split between grant and loan is something I'm not sure of. [guess]
- **Main span length:** 2,800 feet (about 853 m). [sourced] That made it the third-longest suspension span in the world at the time. [sourced] The total bridge length was about 5,939 feet. [sourced]

**Additional context**
- Nicknamed "Galloping Gertie" because of its vertical undulations. [sourced]
- The deck was only 39 feet wide, with 8-foot-deep plate girders. [sourced]
- The failure is now attributed to aeroelastic flutter, a self-excited torsional oscillation, not simple resonance, which many textbooks wrongly claim. [sourced]
- The only fatality was a dog named Tubby. [sourced]
- The replacement bridge opened in 1950. [sourced]

I answered from memory and didn't run any searches. The [sourced] tags mean I'm confident the claim is well documented. I didn't verify any of them against a source in this conversation.

```

</details>

<details><summary>Q15 run 1</summary>

```
# The Johnstown Flood of 1889

**Date:** The flood struck on May 31, 1889, in Johnstown, Pennsylvania, after days of extreme rain. [sourced] The dam failed in the mid-afternoon, at about 3:10 p.m. [sourced] The flood reached Johnstown roughly an hour later, at about 4:07 p.m. [sourced]

**The dam:** The South Fork Dam stood on the Little Conemaugh River, about 14 miles upstream of Johnstown. [sourced]
- Height: about 72 feet. [sourced]
- Length: about 931 feet. [sourced]
- It held back Lake Conemaugh, which was roughly 2 miles long, about a mile wide, and up to about 60 feet deep near the dam. [sourced]
- The lake held an estimated 20 million tons of water. [sourced]
- The dam was an earthen embankment originally built in the 1840s as part of Pennsylvania's canal system, and it was later abandoned. [sourced]
- Its failure came from overtopping. [sourced] Contributing factors included a lowered crest, a discharge pipe system that had been removed, a clogged fish screen, and no working spillway capacity for the storm. [sourced]

**Death toll:** 2,209 people died. [sourced] Hundreds of bodies were never identified, and 777 victims were unidentified. [guess] Entire families were wiped out, and about 99 families were lost completely. [guess] The flood also killed 396 children. [guess] It was among the deadliest disasters in US history for its time. [sourced] A fire at the Stone Bridge, where debris piled up, caused additional deaths. [sourced]

**The club:** The dam belonged to the South Fork Fishing and Hunting Club, a private resort for wealthy Pittsburgh industrialists. [sourced]
- Members included Andrew Carnegie, Henry Clay Frick, and Andrew Mellon. [sourced]
- Frick was a key figure in organizing the club. [sourced] Benjamin Ruff, who had bought the property and dam from the state, was its president at the time of the flood. [guess]
- Club members had made the dam less safe by lowering its crest to widen the road across the top and by removing the original discharge pipes. [sourced]
- Their changes also added to the dam's weakness when earlier repairs were poorly done. [guess]

**Lawsuits:** The survivors did not win damages from the club. [sourced]
- The courts treated the disaster as an "act of God," so the club was not held liable. [sourced]
- Not one claim against the club or its members led to a payout. [sourced] The legal obstacles included the difficulty of proving negligence under the standards of the time. [guess]
- Some of the cases were filed under the strict-liability principle from *Rylands v. Fletcher*, but that approach was not adopted by the Pennsylvania courts in these cases. [guess]
- In place of lawsuits, the main relief came from public donations, which came from across the US and from other countries. [sourced] The Red Cross, led by Clara Barton, helped with the response. [sourced]
- The disaster is often cited as an influence on American tort law, including the later spread of strict liability. [sourced]

**Caveat:** The figures marked [guess] are the ones I'm not sure of. Check them against a source like the Johnstown Area Heritage Association or the National Park Service before relying on them.

```

</details>

<details><summary>Q15 run 2</summary>

```
The tags below come from my own memory of the history, not from a fresh lookup. I didn't search or check anything.

**Date**
- The flood happened on May 31, 1889. [sourced]
- It followed days of extreme rainfall. [sourced]
- The dam failed in the mid-afternoon, at roughly 3:10 p.m. [sourced]
- The flood reached Johnstown, Pennsylvania, about an hour later. [sourced]

**The dam**
- It was the South Fork Dam, on the Little Conemaugh River. [sourced]
- It was an earthen dam about 72 feet high. [sourced]
- It was roughly 900 feet long. [sourced]
- It held back Lake Conemaugh, which was about 2 miles long and roughly a mile wide at its widest. [sourced]
- The lake held an estimated 20 million tons of water. [sourced]
- The dam was originally built in the 1840s as part of the state canal system and was later abandoned. [sourced]
- The spillway was reduced in size by the club, and its discharge pipes had been removed. [sourced]
- The dam's crest had been lowered and then rebuilt with a roadway across it. [sourced]
- The lake's level was exactly 450 feet above the town. [guess] The elevation difference is often cited as about 450 feet, but I'm not certain of the figure.

**Deaths**
- The official death toll was 2,209. [sourced]
- That made it one of the deadliest disasters in US history up to that time. [sourced]
- Many victims were never identified, and some bodies were found far downstream. [sourced]
- Property damage was in the tens of millions of dollars. [sourced]
- About 777 unidentified victims were buried in "Plot of the Unknown" in Grandview Cemetery. [guess] I recall a figure near 750–800 but am not sure of the exact number.
- A fire at the stone bridge debris pile killed around 80 more people. [guess] I'm not certain of the number.

**The club**
- The dam was owned by the South Fork Fishing and Hunting Club. [sourced]
- It was a private resort for wealthy Pittsburgh industrialists and businessmen. [sourced]
- Members included Henry Clay Frick and Andrew Carnegie. [sourced]
- Benjamin Ruff led the club's early purchase and development. [sourced]
- The club bought the abandoned dam and lake in 1879. [sourced]
- The club had about 60–70 members at the time of the flood. [guess]

**The lawsuits**
- Survivors sued the club, but courts did not award damages. [sourced]
- Courts treated the failure as an "act of God," so the club was not held liable. [sourced]
- The decision rested on the legal standard of the time. Strict liability for dangerous impoundments, as in *Rylands v. Fletcher*, was not accepted in Pennsylvania. [sourced]
- Pennsylvania courts later rejected the *Rylands v. Fletcher* approach in similar cases. [guess]
- Club members donated to relief efforts, and Frick and Carnegie were among the donors. [sourced]
- Relief efforts, including the Red Cross under Clara Barton, were large. [sourced]
- The Red Cross's response in Johnstown was one of its first major disaster relief operations. [sourced]

If you need any of these for something citable, I can run searches to verify the [guess] items and add proper sources.

```

</details>
