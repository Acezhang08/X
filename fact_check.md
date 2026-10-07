# 事实核查：布尔巴基 × OpenAI 数学论文

核查日期：2026-10-07。方法：对每一条历史事实联网检索，至少找到一个可引用来源，并和第二个来源交叉对照。
**说明**：本环境的网络代理拦截了 Wikipedia / MacTutor / Britannica / PMC 等站点的直接抓取，所以这些来源的内容是通过搜索结果摘要读到的，没有逐字读原页面；`openai/math` 的 README 是直接抓取的。下面"来源"一栏标明了哪一条属于哪种。

## 一、六个待核实点

| # | 待核实说法 | 结论 | 依据 / 来源 |
|---|---|---|---|
| 1 | 1930 年代中期由年轻法国数学家成立；至少 3 位创始人 | **属实** | 首次非正式聚会 1934-12-10，正式创立会议 1935-07-10 至 17 日（Besse-en-Chandesse）。创始成员：Henri Cartan、Claude Chevalley、Jean Coulomb、Jean Delsarte、**Jean Dieudonné**、Charles Ehresmann、Szolem Mandelbrojt、René de Possel、**André Weil**。主要来自巴黎高师（ENS）校友。来源：[Wikipedia: Nicolas Bourbaki](https://en.wikipedia.org/wiki/Nicolas_Bourbaki)；[MacTutor: Bourbaki, the pre-war years](https://mathshistory.st-andrews.ac.uk/HistTopics/Bourbaki_1/)；[CNRS News](https://news.cnrs.fr/node/1166)（均经搜索摘要读取） |
| 2 | 集体署名"Nicolas Bourbaki"，主要著作《数学原本》 | **属实** | "集体化名"，系列教科书合称 *Éléments de mathématique*（Elements of Mathematics），是该团体的核心著作。来源：同上 Wikipedia；[MacTutor: Nicolas Bourbaki](https://mathshistory.st-andrews.ac.uk/Biographies/Bourbaki/) |
| 3 | 成员 50 岁必须退出 | **需改写**：不是严格规定 | 来源写的是"guideline / semi-mandatory"：成员应在 50 岁退出，"从来不是严格规则"，执行情况难以评估，因为任期很少公开。该惯例由 Weil 提议，1956 年夏季会议上（Dieudonné 五十岁生日午宴）由 Cartan 宣读他的信。Dieudonné 的解释：许多数学家对年轻时学到的东西过分迷恋，所以要让团体对新想法保持开放。来源：Wikipedia；[numericana: Bourbaki](https://numericana.com/fame/bourbaki.htm)；[Britannica: Nicolas Bourbaki](https://www.britannica.com/topic/Nicolas-Bourbaki)（均经搜索摘要读取）。**旁白改为 "were expected to leave at 50"**，不说 "had to"。 |
| 4 | Ralph Boas 揭穿后，Bourbaki 反称"Boas 才是不存在的人" | **大意属实，措辞需精确** | Boas（《Mathematical Reviews》执行编辑）写文章（《大英百科全书》条目；1949 年他又两次在 MR 中点明）说明 Bourbaki 是一群年轻法国数学家的化名。随后出版方收到 Bourbaki 措辞强烈的信，抗议"他的生存权被质疑"；Bourbaki 另函称 **B.O.A.S. 只是该刊编辑们姓氏首字母的缩写**，即把"Boas"说成也是个化名。来源：[PMC: Impersonation and personification in mid-twentieth century mathematics](https://pmc.ncbi.nlm.nih.gov/articles/PMC7731645/)；[Newsweek](https://www.newsweek.com/nicolas-bourbaki-math-never-existed-1478175)；[The Conversation](https://theconversation.com/nicolas-bourbaki-the-greatest-mathematician-who-never-was-122845)；Boas 自述见 *Lion Hunting & Other Mathematical Pursuits*（均经搜索摘要读取）。**不是"散布谣言"，是"回信声称 Boas 只是个缩写"**，旁白据此改写。具体年份各来源略有出入，旁白不写年份。 |
| 5 | 空集符号 ∅ 来自布尔巴基（André Weil） | **属实，依据是 Weil 本人的说法** | Weil 在自传 *The Apprenticeship of a Mathematician* 中说，空集符号的采用由他本人负责："The symbol came from the Norwegian alphabet, with which I alone among the Bourbaki group was familiar."（取自挪威语字母 Ø）。Wikipedia 把符号的引入记在 Bourbaki 名下，约 1939 年。来源：[FOM 邮件列表引述 Weil 原文](https://cs.nyu.edu/pipermail/fom/2009-April/013522.html)；[Wikipedia: Empty set](https://en.wikipedia.org/wiki/Empty_set)。注意：这主要是 Weil 自己的回忆，没有独立文献推翻或另证。 |
| 6 | openai/math：722 篇论文，由未公开的内部模型产出 | **属实** | README 原文（直接抓取）："The current catalogue contains 722 manuscripts organized into 372 families."；"The vast majority of results were obtained with the same procedure using an unreleased internal OpenAI model."；平均每个结果用约 3 小时 ChatGPT Pro 推理算力。README 没有给模型起名，没有作者署名行（只说引用见各目录 BibTeX）。有一篇（黎曼 ζ 函数零点自由区）"was human edited for readability"。仓库只有一个提交 "Initial commit"，日期 **2026-10-06**，所以"这周"成立。来源：<https://github.com/openai/math>（README 与提交页，2026-10-07 抓取） |

## 二、逐句旁白核对

| 句 | 最终旁白 | 对应核实点 / 来源 | 备注 |
|---|---|---|---|
| 1 | In the 1930s, a new mathematician appeared in France: Nicolas Bourbaki. | #1 #2 | 原稿写"in Paris"，来源只确认是法国数学家群体，没有确认姓名首次在巴黎出现，所以**改为 France**。 |
| 2 | His books helped change how math was written, for decades. | #2；风格影响见 [Structuralist Mathematical Style: Bourbaki as a Case Study](https://philarchive.org/archive/MARTSM-7)、Britannica | 原稿"changed"改为"**helped change**"，因为这是评价性说法，不是单一史实。 |
| 3 | There was one problem. He did not exist. | #2 | "Bourbaki"是集体化名，没有这个人。 |
| 4 | Bourbaki was a group of young French mathematicians. They wrote together and signed one name. | #1 #2 | 原稿"secret club"**删掉了"secret"**：核实来源里没有明确写"秘密团体"，不硬留。 |
| 5 | Members were expected to leave at 50. So the author never grew old. | #3 | "had to"→"**were expected to**"。后半句是修辞，依据是该惯例的目的：让团体不断换新（Dieudonné 的解释）。 |
| 6 | Ralph Boas wrote that Bourbaki was a pseudonym. Bourbaki replied that Boas was the fake: just an acronym. | #4 | 按来源改写，见上。 |
| 7 | Their work is still everywhere. Even the empty set symbol comes from them. | #5 | "still everywhere"是概括性说法；符号出处以 Weil 自述为准。 |
| 8 | This week, OpenAI released 722 math papers. Their author has no name either: an unreleased internal model. | #6 | 原稿"Their author has no name either"保留，并补上 README 的原话含义。"papers"对应 README 的 "manuscripts"。 |
| 9 | Bourbaki was many people behind one name. This time it is one model behind hundreds of papers. | #1 #2 #6 | 原稿"one machine"改为"one model"（README 用词）。README 说"绝大多数结果"用同一流程，且有一篇经人工润色，所以"hundreds of papers"保守准确，不说"全部"。 |
| 10 | So who gets the credit? | 问句，无事实陈述 | |

## 三、画面里的事实边界

- 所有人物均为无脸剪影，不使用真实照片，不画成可辨认的真人。
- 书脊文字 "ÉLÉMENTS DE MATHÉMATIQUE" 是真实书名（#2）。
- 第 6 句的纸张是抽象版面（灰条 + 问号），**没有伪造真实报纸版面**。纸上的 "B.O.A.S." 字样对应来源 #4 中 Bourbaki 的回函说法。
- 第 8 句画面里出现的 "722" 来自 README（#6）；塔里每一页只是示意，不对应具体论文。
- 画面中的 "openai / math" 字样仅用作屏幕感装饰，不是对 GitHub 界面的复制。
