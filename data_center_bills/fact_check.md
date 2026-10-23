# fact_check.md — Are Data Centers Raising Your Electric Bill?

核查日期：2026-10-23。逐句对 `script.py`（句号 = 脚本里的行 ID）。结论标记：
- **✓原始**：已回到原始文件逐字核对（PJM 报告、监察员 PPT、EPRI 论文、州议会页面）。
- **✓二手**：只有二手来源（已标出来源）。
- **简化**：事实对，但为了讲清楚做了简化，旁边写了原文的限定。
- **观点**：判断/解释句，不是可核事实。
- **改写**：相对你给的大纲，我改了说法（原因写在结论里）。

## 来源缩写（链接只在这里出现）
| 缩写 | 来源 | 日期 |
|---|---|---|
| PJM-27/28 | PJM 新闻稿「PJM Auction Procures 134,479 MW of Generation Resources」https://www.pjm.com/-/media/DotCom/about-pjm/newsroom/2025-releases/20251217-pjm-auction-procures-134479-mw-of-generation-resources.pdf | 2025-12-17 |
| PJM-28/29 | PJM「2028/2029 Base Residual Auction Report」https://www.pjm.com/-/media/DotCom/markets-ops/rpm/rpm-auction-info/2028-2029/2028-2029-bra-results-report.pdf （表 2 是 2018/19–2028/29 每年清算价；附录是"无上限"模拟） | 2026-07-14 |
| EPRI | Watten, Bistline, Blanford「Have Data Centers Raised Your Electric Bill? Causal Evidence from the United States」https://arxiv.org/abs/2606.19777 | 2026-06-18 (arXiv v1) |
| IMM-25 | Monitoring Analytics（PJM 独立市场监察员）MC 网络研讨会 PPT「Market Monitor Report」https://www.pjm.com/-/media/DotCom/committees-groups/committees/mc/2025/20250625-web/item-02---imm-report.pdf | 2025-06-25 |
| IMM-26 | 同上，「Market Monitor Report」https://www.pjm.com/-/media/DotCom/committees-groups/committees/mc/2026/20260727-web/item-02---marketing-monitoring-report---presentation.pdf | 2026-07-27 |
| UD-Jan | Utility Dive 转述 IMM 对 2027/28 拍卖的分析（IMM 报告日期 2026-01-05）https://www.utilitydive.com/news/data-centers-pjm-capacity-auction/808951/ | 2026-01-07 |
| AP | AP（Marc Levy）「Future data centers are driving up forecasts…」（KSAT 转载）https://www.ksat.com/business/2025/11/15/future-data-centers-are-driving-up-forecasts-for-energy-demand-states-want-proof-theyll-get-built/ | 2025-11-14 |
| MKT | Marketplace（Henry Epp）「Data centers lowered electric bills in some places, for now」https://www.marketplace.org/story/2026/07/10/data-centers-lowered-electric-bills-in-some-places-for-now | 2026-07-10 |
| CGEP | 哥伦比亚大学全球能源政策中心研究公告 https://www.energypolicy.columbia.edu/?p=31958 | 2026-06-23 |
| PF | PolitiFact「Data centers, rising electricity costs」https://politifact.com/factchecks/2026/jun/12/elizabeth-warren/data-centers-rising-electricity-costs/ | 2026-06-12 |
| IEEFA | IEEFA「Projected data center growth spurs PJM capacity prices by factor of 10」https://ieefa.org/resources/projected-data-center-growth-spurs-pjm-capacity-prices-factor-10 （页面直接抓取被 403，数字来自搜索结果里的页面摘录） | 2025 |
| OR | Oregon Legislature OLIS，HB 3546 (2025) https://olis.oregonlegislature.gov/liz/2025R1/Measures/Overview/HB3546 | 查于 2026-10-23 |
| TX | Texas Legislature Online，SB 6 (89R) https://capitol.texas.gov/BillLookup/History.aspx?LegSess=89R&Bill=SB6 ；75 MW 门槛来自律所解读 https://www.jw.com/news/insights-senate-bill-6-texas-electric-regulations/ | 2025-06-20 签署 |
| VA | Cardinal News 报道 SCC 对 Dominion 费率案的终裁 https://cardinalnews.org/?p=155240 | 2025-11-26 |

---

## 第 0 段 开头（用户给定，一字未改）
| 句号 | 说法 | 来源 | 结论 |
|---|---|---|---|
| 0.1 | 两年前 PJM 为"一天一兆瓦待命"付 29 美元 | PJM-28/29 表 2：2024/25 清算价 $28.92 /MW-day（UCAP） | ✓原始。"两年前"= 2024/25 交付年 vs 2026/27 交付年，相隔两年。 |
| 0.1 | "America's biggest power grid" | Wikipedia、Bloomberg Law（2026-07-21）、Renewable Energy World 都称 PJM 为美国最大电网运营商；PJM 自己的稿子只写"67 million people" | ✓二手 |
| 0.2 | 今年 329 美元 | PJM-28/29 表 2：2026/27 $329.17 | ✓原始 |
| 0.3 | "More than ten times" | 329.17 ÷ 28.92 = 11.38 | ✓原始（算术） |
| 0.3 | "mainly because of data centers" | IMM-25：数据中心负荷增长是"primary reason"。PJM-27/28 只说"data centers' demand … continues to far outstrip new supply"，没给占比 | **有出入（见汇报）**：这是监察员的归因，不是 PJM 自己的结论；开头没标出处。 |
| 0.4 | 6700 万人 | PJM-27/28：「more than 67 million people across 13 states and DC」 | ✓原始 |
| 0.4 | "pay for it, in their electric bills" | PJM-27/28 与 PJM-28/29：「not all load pays this clearing price because of … self-supply and bilateral contract arrangements」 | **有出入（见汇报）**：并非所有人都按此价付费；开头说得比原文绝对。 |
| 0.5 | 电力行业自己的研究机构发现，直到最近数据中心让电费变便宜 | EPRI：数据中心使全美平均零售电价在 2015–2024 年"modestly"下降 | **有出入（见汇报）**：论文研究的是电价（rate，每度电价格），不是"账单"；结果是全美平均，不是 PJM 地区；"lab"是研究所。 |
| 0.6–0.7 | Both are true. So what flipped? | — | 观点（修辞） |

## 第 1 段 你的电费单与拍卖
| 句号 | 说法 | 来源 | 结论 |
|---|---|---|---|
| 1.1 | 账单看着是一个数字，其实不是 | — | 观点（引入） |
| 1.2 | 账单分"电本身、输配电、容量"三块 | PJM-27/28："Wholesale capacity … accounts for a fraction of wholesale electricity costs; other contributing elements include the daily cost of power … and … transmission … Wholesale costs make up a portion of retail electricity bills." | 简化。各州账单科目不同，容量通常不单列，而是包在"供电"价里；画面上的三行是示意，没有写成真实账单科目。 |
| 1.3 | 容量 = 为最热的那天备好电，外加缓冲 | PJM-28/29：需要一个"Reliability Requirement"，含 20% 目标备用率（IRM）；1 天/10 年的可靠性标准 | ✓原始（解释性表述） |
| 1.4 | 每年提前在拍卖里买 | PJM-28/29：2028/29 拍卖在交付年开始前约 23 个月举行；"A typical BRA is held more than three years before" | ✓原始（"提前"，没说多久） |
| 1.5 | PJM 管 13 州 + DC | PJM-27/28 末段列出 DE, IL, IN, KY, MD, MI, NJ, NC, OH, PA, TN, VA, WV 和 DC（"all or parts of"） | ✓原始 |
| 1.6 | PJM 先算要多少兆瓦（含缓冲） | PJM-28/29：RTO Reliability Requirement 156,013 MW UCAP（IRM 20%） | ✓原始 |
| 1.7–1.8 | 电厂报价，PJM 从便宜到贵排序、从下往上买到够数 | PJM-28/29 引言："procure a target capacity reserve level … in a least-cost manner" | ✓原始（最低成本采购的通俗说法；实际还有地区约束，画面标 illustrative） |
| 1.9 | 所有中标者按最后一个的价格拿钱（统一清算价） | PJM-28/29：「all prices cleared at the cap」；"Resource Clearing Price" 为全区统一（无受限地区时）；市场机制为统一清算价 | ✓原始（机制）。注：中标者按"清算价"而非各自报价拿钱，是 RPM 的标准规则。 |
| 1.10 | 需求增长、供给紧时，最后一个电厂更贵，所有人都拿更高的价 | 同上 | 观点/解释（原理图，标 illustrative） |
| 1.11 | 为客户买电的电力公司付这个价，进入账单 | PJM-28/29："the $16.4 billion value does not equate to a total cost to load because load that is hedged through self-supply or bilateral contracts is not exposed to the clearing prices" | 简化（原文限定：自供电/双边合约的负荷不按此价付）。 |
| 1.12 | $28.92 → $269.92 → $329.17 → $333.44（每兆瓦每天；脚本念"29、270、329、333"） | PJM-28/29 表 2：2024/25 $28.92；2025/26 $269.92；2026/27 $329.17；2027/28 $333.44 | ✓原始 |
| 1.13 | 最近一次（7 月）拍卖 325 美元 | PJM-28/29：2028/29 BRA，报告日期 2026-07-14，$325.00 | ✓原始 |
| 1.14 | 后三次都顶到价格上限 | PJM-28/29：cap 和 floor 适用于 2026/27、2027/28、2028/29 三次拍卖，三次都按 cap 清算（$329.17 / $333.44 / $325.00 = "all prices cleared at the cap"） | ✓原始 |
| 1.14 | 无上限时最近一次会超过 550 美元 | PJM-28/29 附录：无 cap/floor 模拟，全 RTO 清算价 $554.72 | ✓原始 |
| 1.15 | 两年里涨了 11 倍多，然后顶到天花板 | 329.17 ÷ 28.92 = 11.4；后续 333.44、325.00 均为 cap | ✓原始（算术） |
| 1.16 | 监察员的统计：2026 年上半年容量占批发电力成本约 17%，一年前约 8% | IMM-26 第 11 页：Capacity 17.1%（2026 Jan–Jun）、8.4%（2025 Jan–Jun），占 total cost of wholesale power | ✓原始 |

## 第 2 段 数据中心让电价变便宜
| 句号 | 说法 | 来源 | 结论 |
|---|---|---|---|
| 2.1 | 全国范围内多年来数据中心似乎起了相反作用 | EPRI 摘要 | ✓原始（已加"appear"） |
| 2.2 | 6 月 EPRI 研究员发了论文，题目「Have Data Centers Raised Your Electric Bill?」 | EPRI：arXiv v1，2026-06-18 | ✓原始 |
| 2.3 | EPRI 是电力行业研究所，由会员出资，多为电力公司 | EPRI 自述与 Wikipedia：独立非营利、会员出资，会员代表约 90% 美国电力公司收入，"most members are electric utilities" | ✓二手（EPRI 官网 /about 抓取失败，未逐字核到原话）。 |
| 2.3 | 作者：Watten、Blanford 属 EPRI，Bistline 属 Watershed | EPRI 首页脚注 | ✓原始（脚本没细讲，画面写"Watten · Bistline · Blanford"） |
| 2.4 | 2019–2024 年平均美国家庭所在州数据中心容量涨了 160% | EPRI 第 3 页："from 2019 to 2024 the average residential customer lived in a state where data center capacity grew 160%" | ✓原始 |
| 2.4 | 使居民电价比本来低约 6% | EPRI 同句："which caused their rates to fall by 6%" | ✓原始 |
| 2.5 | 容量翻倍→居民电价降约 3.5% | EPRI 第 21 页："a doubling of data center capacity causes residential retail prices to fall by 3.5%"（固定居民需求下，首选设定） | ✓原始 |
| 2.5 | 区间约 1.5%–12% | EPRI 同页：Anderson-Rubin 置信区间 −12.1% 至 −1.4% | ✓原始 |
| 2.5 | （未讲）2019–2024 子样本的效应约为全样本的一半 | EPRI 同页 | 脚本没讲；已知局限（写进汇报）。 |
| 2.6 | 电网成本多为固定，更多电量摊薄固定成本；新电厂可能比老的便宜 | EPRI 引言："fixed costs … spread across more kilowatt-hours"；"incremental mix of new generation assets tends to have a lower average cost than the embedded incumbent asset mix" | ✓原始 |
| 2.7 | 哥大全球能源政策中心 6 月称涨价"cannot be attributed to any single factor"，大负荷"not a principal driver" | CGEP 2026-06-23 公告（圆桌参与者观点） | ✓原始（来自公告页）。**改写**：你给的"强调不是自动的"我没找到原话，没用。 |
| 2.8 | 一位能源经济学家：电价下降的州"already had room" | MKT：Ryan Hledik（Brattle Group）："already had room on their power grid to accommodate these new customers" | ✓二手（Marketplace 转述）。**改写**：你给的"北达科他"例子，EPRI 论文没有；Marketplace 里是 Hledik 举的例；且另有报道称北达科他居民电价 2020–2024 涨了近 30%，故删掉。 |
| 2.9 | 2021–2024 加州电价涨近 40%，论文称主要是山火成本 | EPRI 第 2 页："California in particular saw average prices increase nearly 40% during the same period owing largely to wildfire costs"（"same period" = 2021–2024） | ✓原始。**改写**：你的"数据中心增长并不多"论文没有这句，删掉。 |
| 2.10 | 一次拍卖到下一次，价格涨了 9 倍多 | $269.92 ÷ $28.92 = 9.33（2024/25 → 2025/26） | ✓原始。**改写**：你写的"将近九倍"不准，实际是"超过九倍"。 |

## 第 3 段 翻转
| 句号 | 说法 | 来源 | 结论 |
|---|---|---|---|
| 3.1–3.2 | 摊薄固定成本只在电网有余量时成立；满了以后新用户需要新系统 | EPRI 摘要"future supply constraints could reverse the effect"；MKT/Hledik | 观点/解释（有来源支持） |
| 3.3 | 2027/28 拍卖的预测峰值比上一次高约 5,250 MW，其中近 5,100 MW 是数据中心 | PJM-27/28 末段："approximately 5,250 MW higher … Nearly 5,100 MW of that increase is attributable to data center demand" | ✓原始。**改写**：你给的"2024–2030 新增约 32 GW、约 30 GW 数据中心"是二手，没核到，换成 PJM 原文这组数。 |
| 3.4 | 该次拍卖只新增 774 MW 新发电和增容 | PJM-27/28："cleared 774 MW UCAP of new generation and generation uprates" | ✓原始 |
| 3.5 | 全区第一次低于可靠性要求，差 6,623 MW | PJM-27/28："the first auction in which the entire RTO, including FRR areas, fell short"；"short … by 6,623 MW" | ✓原始 |
| 3.5 | PJM 说这不代表停电，而是备用更薄 | PJM-27/28："does not necessarily mean … unable to serve load"；PJM-28/29："it means that PJM would have to operate with slimmer reserves" | ✓原始 |
| 3.6 | 需求多、新供给少，最后一个电厂定价 | 同 1.9–1.10 | 观点/解释 |
| 3.7 | 2025 年 6 月监察员写道数据中心负荷增长是"the primary reason for recent and expected capacity market conditions" | IMM-25 第 3 页（原句：「Data center load growth is the primary reason for recent and expected capacity market conditions, including …」） | ✓原始 |
| 3.8 | 2025/26 拍卖：数据中心负荷单独使收入增加约 93 亿美元，174% | IMM-25："data center load by itself resulted in an increase in the 2025/2026 BRA revenues of $9,332,103,858 or 174.3 percent (Scenario 88)" | ✓原始（监察员估算） |
| 3.9 | 7 月：最近四次拍卖共约 294 亿美元与数据中心负荷有关，占 46% | IMM-26 第 4 页：「$29.4B, or 46.2 percent of total capacity market charges over those four auctions」 | ✓原始。**改写**：你写"7 月 27 日 IMM 报告"，实际是 7 月 27 日 MC 网络研讨会 PPT，完整分析报告当时尚未发布。 |
| 3.10 | 这些是监察员的估算，衡量的是拍卖费用，不是每个家庭的账单 | PJM-28/29 "does not equate to a total cost to load" | ✓原始 / 观点 |
| 3.11 | 很多需求还没到 | IMM-26 第 6 页：预测里含数据中心负荷 21,470 MW（其中 16,436 MW 在"已嵌入负荷"之上）；UD-Jan | ✓原始 |
| 3.12 | 拍卖用预测不用现在的用电；1 月监察员发现：在那次（2025 年 12 月）拍卖中，其归因于数据中心的 65 亿美元里约 62 亿对应还没建的数据中心 | UD-Jan 转述 IMM 2026-01-05 报告："$6.5 billion, or 40%, of the $16.4 billion … Roughly $6.2 billion of those costs relates to data centers that haven't been built" | ✓二手（Utility Dive 转述；IMM 原报告 PDF 未取到）。 |
| 3.13 | 监察员称预测不确定性"unique and unprecedented" | UD-Jan | ✓二手 |
| 3.14 | 开发商常不告诉电力公司还向别处申请；据 AP，PJM 称同一项目可能被多家电力公司预测重复计入 | AP：开发商"for competitive reasons, won't tell utilities if or where they've submitted other requests"，一个项目可能抬高多家预测（AP 对 PJM 说法的转述，非 PJM 原话） | ✓二手。**改写**：大纲里的来源是 Inside Climate News，没找到原文；改用 AP，措辞压成"可能"（could）。 |
| 3.15 | 今天价格有一部分建立在尚不存在的楼上 | 3.12 的来源；"有些会建，有些可能不会"是推断 | 观点（有来源支撑前半句） |

## 第 4 段 谁在付
| 句号 | 说法 | 来源 | 结论 |
|---|---|---|---|
| 4.1 | So who pays? | — | 观点 |
| 4.2 | 监察员希望数据中心自付容量成本，不转嫁其他用户 | IMM-26 第 4 页：「ensure that data centers pay for their own capacity and do not impose capacity costs on other customers」 | ✓原始 |
| 4.3 | 这说明现在成本是共担的 | 对 4.2 的推断 | 观点 |
| 4.4 | IEEFA 估计容量涨价让西马里兰平均每户每月多约 18 美元，俄亥俄约 16 美元 | IEEFA："capacity market prices are estimated to increase the average residential bill by $18/month in western Maryland and by about $16/month in Ohio" | ✓二手（智库估算；页面 403，数字取自搜索摘录）。 |
| 4.5 | 这是整个容量涨价，不只数据中心；是估算 | IEEFA 口径 | ✓二手/观点 |
| 4.6 | 全美居民电价五年涨约 42% | PF：「U.S. residential electricity costs rose about 42% over five years, according to the U.S. Energy Information Administration」（2021-03 至 2026-03） | ✓二手（PolitiFact 转述 EIA） |
| 4.7 | EPRI 研究员说老化设备、灾后修复、天然气价格比数据中心更重要 | MKT："EPRI found data centers were not the main cause … aging infrastructure, natural disaster recovery, and natural gas prices were larger drivers" | ✓二手（Marketplace 转述；EPRI 论文本身列了加州山火和 2021–24 通胀）。**改写**：你给的"AEP 说收入能抵成本"没找到原话，删掉。 |
| 4.8 | 全国范围数据中心不是账单上涨的主因；但没余量的电网里，可能是那一个价格的主因 | EPRI/CGEP/MKT + IMM-25 | 观点（总结） |

## 第 5 段 规则
| 句号 | 说法 | 来源 | 结论 |
|---|---|---|---|
| 5.1 | — | — | 观点 |
| 5.2 | 俄勒冈 HB 3546：让监管机构为超大用电设施设单独费率类别，成本分摊给它们，保护其他用户 | OR：已 Enrolled，Chapter 323；"classification of service for large energy use facilities … allocate serving costs to those facilities and mitigate risks to other retail electricity customers" | ✓原始。**改写**：你写的"POWER Act 给数据中心单独设电价类别"，法案页面没写"数据中心"和"POWER Act"，我用"超大用电设施"。 |
| 5.3 | 德州 SB 6，2025 年 6 月签署；75 MW 以上大负荷出资承担并网成本 | TX：2025-06-20 签署；75 MW 门槛与成本分担来自律所解读（Jackson Walker） | 签署 ✓原始；条款内容 ✓二手 |
| 5.4 | 弗吉尼亚监管机构批准 25 MW 以上单独费率类别，2027 年 1 月起，14 年合同、最低付费 | VA（Cardinal News 转述 SCC 2025-11 终裁）：25 MW+、2027-01-01 生效、14 年合同、≥85% 配电/输电需量、≥60% 发电需量 | ✓二手。**改写**：你给的 SB 253 我没讲：4 月州长修订、5 月签署的最终文本我没能核到（相关页面 403/只有摘要），不确定通过的是什么版本，所以只讲有出处的 SCC 费率类别。 |
| 5.5 | 监察员主张把数据中心移出共享容量市场，设单独拍卖 | IMM-26 第 4 页："data center load should be removed from the capacity market and procured through a dedicated auction" | ✓原始。（监察员的"自带发电"主张来自 UD-Jan，没用。） |
| 5.6 | 这些不改变过去的价格，只塑造之后的价格 | — | 观点 |

## 第 6 段 结尾
| 句号 | 说法 | 来源 | 结论 |
|---|---|---|---|
| 6.1–6.5 | 结论与评论引导 | — | 观点（结论只复述上面核过的内容） |

---
## 汇总
- 脚本共 **67 行旁白（133 个句子）**。其中 **18 行**是观点/判断/引导句（标"观点"），**49 行**含可核事实，已逐条核对。
- **只有二手来源的行：11 行**（0.1 的"biggest"、2.3、2.8、3.12、3.13、3.14、4.4、4.6、4.7、5.3 的条款内容、5.4）。其中 3.12/3.13 是 Utility Dive 转述监察员 1 月报告，原报告 PDF 没取到；4.4 的 IEEFA 数字来自搜索摘录（页面 403）。
- **相对大纲改写或删掉：11 处**：① 北达科他例子删（论文里没有；报道称该州居民电价 2020–24 涨近 30%）；② 加州"数据中心增长并不多"删（论文没这句）；③ "将近九倍"→"超过九倍"（9.33×）；④ 二手的 32 GW/30 GW → PJM 原文 5,250 / 5,100 MW；⑤ "7 月 27 日 IMM 报告"→ 实为 MC 网络研讨会 PPT；⑥ Inside Climate News → AP（原文没找到）；⑦ AEP 说法删（没找到）；⑧ Columbia"不是自动的"没找到原话，没用；⑨ SB 253 没讲（最终文本核不到）；⑩ Dominion $8.51 没用；⑪ "大用户按度电算更便宜（批量折扣）"没核到，没讲。
- **开头 30 秒与原始来源有出入的三处**（未改动，见汇报）：0.3 的"mainly because of data centers"、0.4 的"pay for it, in their electric bills"、0.5 的"bills / research lab"（论文研究的是全美平均电价而非账单，也不是 PJM 地区）。数字本身（$28.92、$329.17、>10×、6700 万人）全部对得上。
- 没有用任何真实人物台词；引语卡片的引文都逐字来自上表原文（IMM-25、IMM-26、CGEP、Hledik/MKT、UD-Jan）。

---
## 附：旁白全文（与 `script.py`、`timeline.json` 逐字一致；脚本里的 PJM / EPRI / IEEFA / DC 在配音时按字母读，画面字幕保持原样）

**段 0**

- `0.1` Two years ago, America's biggest power grid paid twenty-nine dollars to keep one megawatt on standby for a day.
- `0.2` This year: three hundred and twenty-nine.
- `0.3` More than ten times as much — mainly because of data centers.
- `0.4` And sixty-seven million people pay for it, in their electric bills.
- `0.5` But the power industry's own research lab found that until recently, data centers were making those bills cheaper.
- `0.6` Both are true.
- `0.7` So what flipped?

**段 1**

- `1.1` Open your electric bill and it looks like one number. It isn't.
- `1.2` Some of it pays for the power itself. Some pays for the wires that carry it. And one slice pays for something most people have never heard of: capacity.
- `1.3` Capacity is the price of being ready. A grid can't just have enough power on an average day. It needs enough on the hottest afternoon of the year, plus a cushion.
- `1.4` So every year, the grid buys that readiness in advance, at an auction.
- `1.5` In thirteen states and Washington, DC, the grid operator is PJM. The same grid from the start of this video.
- `1.6` Here's how the auction works. PJM first calculates how many megawatts it will need on the hottest days, cushion included.
- `1.7` Power plants bid, each naming the lowest price it will accept.
- `1.8` PJM lines the bids up from cheapest to most expensive, and buys from the bottom until it has enough.
- `1.9` And here's the part that matters. Every plant that wins is paid the price of the last one needed. One price, for everyone.
- `1.10` So when demand grows and supply is tight, the last plant costs more. And everyone gets paid more.
- `1.11` The utilities that buy this power for customers pay that price. It ends up in your bill.
- `1.12` Now look at that price, in dollars per megawatt, per day. Two years ago: twenty-nine. Then two hundred and seventy. Then three hundred and twenty-nine. Then three hundred and thirty-three.
- `1.13` The most recent auction, in July, cleared at three hundred and twenty-five.
- `1.14` The last three all hit a price cap. PJM's own simulation says that without the cap, the latest would have cleared above five hundred and fifty.
- `1.15` So the price of readiness went up more than eleven times in two years, and then hit a ceiling.
- `1.16` Keep it in proportion, though. By the market monitor's count, capacity was about seventeen percent of the wholesale cost of power in early twenty twenty-six, up from about eight percent a year earlier.

**段 2**

- `2.1` Now the surprising part. Nationally, for years, data centers appear to have done the opposite.
- `2.2` In June, researchers at EPRI, the Electric Power Research Institute, posted a paper titled: Have Data Centers Raised Your Electric Bill?
- `2.3` Quick note on who they are. EPRI is the electric power industry's research institute, funded by its members, mostly electric utilities. That doesn't make the numbers wrong. But you should know it.
- `2.4` What did they find? From twenty nineteen to twenty twenty-four, the average American household lived in a state where data center capacity grew a hundred and sixty percent. They estimate that growth made residential electricity rates about six percent lower than they would otherwise have been.
- `2.5` Put another way: each time a state's data center capacity doubled, residential rates fell by about three and a half percent. They're clear it's an estimate, with a wide range, from about one and a half percent to twelve.
- `2.6` Why would more demand lower the price? Because most of a grid's cost is fixed: the power lines, the substations. When more electricity flows through the same wires, each unit carries a smaller share. And new power plants can cost less than the old ones.
- `2.7` Columbia University's Center on Global Energy Policy said in June that recent price increases can't be pinned on any single factor, and that big new loads have not been a principal driver.
- `2.8` But the discount comes with a condition. As one energy economist put it, the states where prices fell already had room on their grids.
- `2.9` And blaming data centers for every price increase would be wrong too. From twenty twenty-one to twenty twenty-four, California's electricity prices rose nearly forty percent, which the same paper says was largely wildfire costs.
- `2.10` So if data centers were pushing prices down, how did one price jump more than nine times, from one auction to the next?

**段 3**

- `3.1` The answer is in one word: room.
- `3.2` Spreading fixed costs only works while the grid has spare capacity. When it's full, a new customer doesn't share the cost of the existing system. A new customer needs a new one.
- `3.3` Look at where PJM's growth is coming from. For the auction covering twenty twenty-seven and twenty twenty-eight, its forecast peak demand rose by about fifty-two hundred and fifty megawatts. Nearly fifty-one hundred of that was data centers.
- `3.4` Supply didn't keep up. That auction added only seven hundred and seventy-four megawatts of new generation and upgrades.
- `3.5` And for the first time, the whole region's total fell short of PJM's own reliability target, by sixty-six hundred and twenty-three megawatts. PJM says that doesn't mean the lights go out. It means thinner reserves.
- `3.6` More demand, less new supply, and the last plant needed sets the price for everyone. That's the jump.
- `3.7` PJM has an independent watchdog, the market monitor. In June twenty twenty-five, it wrote that data center load growth is, in its words, the primary reason for recent and expected capacity market conditions.
- `3.8` Its estimate for the twenty twenty-five, twenty twenty-six auction: data center load alone raised that auction's total by about nine point three billion dollars, or a hundred and seventy-four percent.
- `3.9` In July, it added up the last four auctions: about twenty-nine point four billion dollars tied to data center load. Forty-six percent of all capacity charges across those four auctions.
- `3.10` Nine billion. Twenty-nine billion. Forty-six percent. Those are the monitor's estimates, and they measure charges in the auction, not what lands on each household's bill. But the direction is clear.
- `3.11` And here's what makes it strange. A lot of that demand isn't here yet.
- `3.12` The auction doesn't run on how much power data centers use today. It runs on a forecast. In January, the monitor found that about six point two billion of the six and a half billion dollars it tied to data centers in the December auction came from data centers not yet built.
- `3.13` It called the uncertainty in those forecasts unique and unprecedented.
- `3.14` One reason: developers often don't tell a utility where else they've asked for power. According to the Associated Press, PJM says that means a single project can inflate more than one utility's forecast.
- `3.15` That means part of today's price rests on buildings that don't exist yet. Some will be built. Some may not.

**段 4**

- `4.1` So who pays?
- `4.2` The market monitor describes the problem plainly. It wants data centers to pay for their own capacity, and not impose capacity costs on other customers.
- `4.3` That tells you how it works today: the cost is shared.
- `4.4` How much does that add up to for a household? One estimate, from the think tank IEEFA, is that the higher capacity prices add about eighteen dollars a month to an average bill in western Maryland, and about sixteen dollars in Ohio.
- `4.5` Careful with those numbers. They cover the whole jump in capacity prices, not only the data center share, and they're estimates.
- `4.6` Now the other side. Across the country, residential electricity prices are up about forty-two percent in five years, according to federal data cited by PolitiFact.
- `4.7` EPRI's researchers say aging equipment, disaster recovery and natural gas prices have mattered more than data centers.
- `4.8` So both things are true at once. Nationally, data centers are not the main reason bills rose. But in a grid with no room left, they can be the main reason one price did.

**段 5**

- `5.1` The rules are changing, state by state. Here's what has actually happened.
- `5.2` Oregon passed House Bill thirty-five forty-six. It tells the state's regulator to create a separate rate class for very large energy users, with costs assigned to them and protections for everyone else.
- `5.3` Texas signed Senate Bill six in June twenty twenty-five. It makes very large new loads, seventy-five megawatts and up, contribute to the cost of connecting them to the grid.
- `5.4` In Virginia, regulators approved a separate rate class for customers using twenty-five megawatts or more, starting in January twenty twenty-seven. They must sign fourteen-year contracts with minimum payments, even if they use less.
- `5.5` And the market monitor wants a bigger change: take data centers out of the shared capacity market and give them their own auction.
- `5.6` None of this changes yesterday's prices. It shapes the next ones.

**段 6**

- `6.1` So, will a data center raise your electric bill?
- `6.2` Not automatically. The real question is two questions.
- `6.3` One: does your grid still have room? If it does, new demand can spread fixed costs and push prices down. If it doesn't, the next megawatt gets expensive for everyone.
- `6.4` Two: when it isn't cheap, who pays? Right now, a lot of that cost is shared. The rules being written now will decide whether it stays that way.
- `6.5` Is a data center being built near you — and has your electric bill changed? Tell me in the comments.
