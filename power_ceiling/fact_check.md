# fact_check：Will Electricity Cap AI?（10 分钟版 v2）

核实日期：2026-10-08。观点句已标注，不需要来源。"成片时间码"是该句旁白在 `youtube_power_ceiling_v2.mp4` / `douyin_power_ceiling_v2.mp4`（两版时间轴相同）里的起止时间，格式 分:秒。

| # | 成片时间码 | 说法 | 来源 | 结论 |
|---|---|---|---|---|
| 0.1–0.3 | 0:01.20–0:16.38 | Nadella 2025 年 11 月说可能有一批芯片放在库存里插不上电；最大的问题是电 | DCD（2025-11-03），BG2 Pod；原话 "you may actually have a bunch of chips sitting in inventory that I can't plug in" — https://www.datacenterdynamics.com/en/news/microsoft-has-ai-gpus-sitting-in-inventory-because-it-lacks-the-power-necessary-to-install-them | ✅ |
| 0.5–0.6 | 0:21.77–0:29.62 | 会，但不是你想的方式；真正不够的可能不是电 | 观点 | — |
| 1.3 | 0:40.02–0:44.10 | 2024 年机柜平均用电不到 8 千瓦 | Upsite 引 Uptime Institute 2024 年调查（"not quite at 8 kW"）— https://www.upsite.com/blog/data-center-trends-rack-density-rises-while-pue-and-outage-frequency-remain-flat/ | ✅ |
| 1.4 | 0:44.55–0:52.22 | GB200 NVL72 一个机柜估计约 120 千瓦 | DataCrunch — https://datacrunch.io/blog/nvidia-gb200-nvl72-for-ai-training-and-inference （英伟达官网没给机柜功率，所以旁白用了 "is estimated"） | ✅ |
| 1.5 | 0:52.67–0:56.00 | 约 15 倍 | 计算：120 ÷ 8 = 15；平均值不到 8，所以用 "roughly" | ✅ |
| 1.6 | 0:56.45–1:06.99 | xAI 在孟菲斯约 1.5 吉瓦自建电站 | Cleanview：xAI 孟菲斯 Colossus 1 和 2 约 1,498 MW 现场发电在运行 — https://cleanview.co/reports/behind-the-meter-data-centers | ✅ |
| 1.7 | 1:07.44–1:14.31 | 1 吉瓦 ≈ 80 万户美国家庭用电 | 计算：EIA 2022 年户均 10,791 kWh/年 = 平均 1.23 kW；1,000,000 kW ÷ 1.23 ≈ 81 万户 — https://www.eia.gov/tools/faqs/faq.php?id=97&t=3 | ✅ |
| 1.8–1.9 | 1:14.76–1:28.09 | 2024 年约 415 TWh，约占全球 1.5% | IEA《Energy and AI》— https://www.iea.org/reports/energy-and-ai/executive-summary | ✅ |
| 1.11–1.12 | 1:32.12–1:44.69 | 2030 年约 945 TWh，略多于日本 | 同上 | ✅ |
| 1.13 | 1:45.14–1:52.87 | 美国占约 45% | 同上 | ✅ |
| 1.14 | 1:53.32–2:00.52 | 美国用电增长将近一半来自数据中心 | 同上 | ✅ |
| 2.2 | 2:05.68–2:18.02 | 英伟达称特定 AI 任务上同功率性能最高 25 倍 | 英伟达官网 GB200 NVL72 页面："25x more performance at the same power"，对比 H100 风冷，脚注为特定大模型推理条件、"projected" — https://www.nvidia.com/en-us/data-center/gb200-nvl72/ | ✅ 旁白写明 "Nvidia says" 和 "on certain AI tasks"；画面角落标了 "Nvidia claim, specific workloads only" |
| 2.3 | 2:18.47–2:29.16 | 2017 年以来数据中心用电年增约 12%，是总用电增速的四倍多 | IEA 同上 | ✅ |
| 2.4 | 2:29.61–2:41.53 | 1865 年杰文斯发现更高效的蒸汽机让英国用煤更多 | 稳定的历史知识：杰文斯《煤炭问题》（The Coal Question，1865） | ✅ |
| 2.5–2.6 | 2:41.98–2:52.66 | 越便宜用得越多；效率让胃口变大 | 观点（杰文斯悖论的通俗说法） | — |
| 3.2 | 2:56.00–3:00.81 | 不是电不够，是来不及接 | 观点（有 3.5–3.15 的数据支撑） | — |
| 3.6 | 3:20.78–3:28.36 | 2025 年底排队的发电和储能超过 2000 吉瓦 | 伯克利实验室《Queued Up 2026》（2026-07-01）：约 2,061 GW — https://emp.lbl.gov/news/backlog-power-plants-seeking-transmission-grid-connection-eased-somewhat-2025-amidst | ✅ |
| 3.7 | 3:28.81–3:37.72 | 2025 年建成的项目，从申请到发电中位数超过 5 年 | 同上，"over 5 years"（限有数据的地区） | ✅ |
| 3.8 | 3:38.17–3:46.66 | 2000–2020 年申请的项目只有 13% 建成 | 同上 | ✅ |
| 3.9 | 3:47.11–3:52.23 | 输电线 4–8 年 | IEA 同上 | ✅ |
| 3.10 | 3:52.68–4:01.23 | 变压器交期最长 4 年，五年涨约 80% | pv magazine USA（2026-05-11）— https://pv-magazine-usa.com/2026/05/11/u-s-transformer-market-faces-severe-supply-constraints-as-lead-times-extend-to-four-years/ | ✅ |
| 3.11 | 4:01.68–4:11.09 | GE Vernova 2025 年 12 月说 2028 年前卖光 | Gas Processing News（2025-12）— https://www.gasprocessingnews.com/news/2025/12/ge-vernova-expects-80-gw-of-gas-turbine-contracts-by-years-end/ | ✅ |
| 3.12 | 4:11.54–4:20.03 | 约 20% 项目可能延期 | IEA 同上 | ✅ |
| 3.13–3.14 | 4:20.48–4:33.85 | 摩根士丹利 2026 年 9 月：到 2028 年缺约 32 GW，约 34% | Reuters 经 Investing.com — https://investing.com/news/stock-market-news/nvidia-broadcom-shielded-as-ai-power-crunch-hits-chip-supply-chain-says-morgan-stanley-4932458 | ✅ |
| 3.15 | 4:34.30–4:42.01 | 芯片按产品周期，电力按审批施工周期、五年以上 | 观点，"五年以上"有 3.7 支撑 | — |
| 4.2 | 4:46.06–4:52.86 | PJM 覆盖 13 个州和华盛顿特区 | PJM 官网 — https://www.pjm.com/about-pjm | ✅ |
| 4.4–4.6 | 4:57.20–5:16.85 | $28.92 → $333.44（触顶），无上限约 $530 | Utility Dive — https://www.utilitydive.com/news/pjm-interconnection-capacity-auction-data-center/808264/ | ✅ |
| 4.7–4.8 | 5:17.30–5:32.36 | 未达可靠性目标；需求预测增加 5,250 MW，几乎全因数据中心 | 同上 | ✅ |
| 4.10 | 5:35.70–5:49.09 | 华盛顿特区 Pepco 居民电费从 2025 年 6 月起每月涨约 $21，约 $10 来自容量价格 | IEEFA — https://ieefa.org/resources/projected-data-center-growth-spurs-pjm-capacity-prices-factor-10 | ✅ |
| 5.2 | 5:52.31–6:03.17 | 三哩岛反应堆 2019 年关闭，预计 2027 年恢复 | NS Energy — https://www.nsenergybusiness.com/news/crane-clean-energy-center-2027-restart/ | ✅ |
| 5.3 | 6:03.62–6:16.10 | 谷歌–Kairos：最多 500 MW，首座 2030 年，全部 2035 年 | World Nuclear News（2024-10-15）— https://www.world-nuclear-news.org/articles/google-and-kairos-power-team-up-for-smr-deployments-in-us-first | ✅ |
| 5.4 | 6:16.55–6:21.04 | 解决办法也走电网的时钟 | 观点 | — |
| 5.6–5.8 | 6:24.00–6:42.60 | 59 个项目约 90 GW，超过规划容量四分之一，92% 是 2025 年以来宣布的 | Cleanview（2026 年中）— https://cleanview.co/reports/behind-the-meter-data-centers | ✅ |
| 5.9 | 6:43.20–6:51.52 | 截至 2026 年年中只有约 2 GW 在运行，约 2% | 同上："approximately 2 GW (2.2% of announced capacity) operates today" | ✅ |
| 5.10 | 6:51.97–6:56.04 | 宣布容易建成难 | 观点 | — |
| 5.11 | 6:56.49–7:11.68 | 2025 年 12 月 Crusoe 向 Boom 订 29 台燃气轮机 | Boom 新闻稿（2025-12-09）— https://boomsupersonic.com/press-release/boom-supersonic-to-power-ai-data-centers | ✅ |
| 5.12 | 7:12.13–7:20.61 | 2026 年 9 月 Crusoe 取消订单，转向 GE Vernova 等 | TechRepublic（2026-09-25）— https://www.techrepublic.com/article/news-crusoe-boom-turbine-deal/ | ✅ |
| 5.13 | 7:21.06–7:26.17 | 没验证的机器是很少有人敢冒的险 | 观点 | — |
| 6.2–6.4 | 7:28.71–7:50.64 | 中国发电量是美国两倍多；2025 年新增风光 430+ GW；BNEF 预计未来五年中国新增装机是美国六倍多 | Al Jazeera（2026-05-28）— https://www.aljazeera.com/economy/2026/5/28/chinas-secret-weapon-in-ai-race-with-us-lots-of-cheap-energy | ✅ |
| 6.5 | 7:51.09–8:00.21 | 美国有芯片缺电，中国有电缺芯片 | 同上，IMD 商学院一位 director | ✅ 卡片里的英文按旁白转述写成，未逐字比对原文 |
| 7.2–7.6 | 8:08.87–8:49.89 | 电挡不住 AI；决定速度、地点、赢家；电网接口可能比芯片值钱；判断错了的信号 | 观点 | — |
| 8.2 | 8:52.73–8:59.22 | AI 的账单可能已经算进部分地区居民电费 | 有 4.10 支撑；用了 "may" | ✅ |

**已删掉、不要加回来的说法**：Crusoe 是 OpenAI 星际之门项目的建造商（未核实）；Crusoe 取消订单的具体原因（来源说法不一）。

## 全部旁白句时间码

| 句 | 起 | 止 | 英文旁白 |
|---|---|---|---|
| 0.1 | 0:01.20 | 0:06.12 | In November 2025, Microsoft's CEO said something strange. |
| 0.2 | 0:06.57 | 0:12.09 | His company may have a bunch of AI chips sitting in inventory — that it can't plug in. |
| 0.3 | 0:12.54 | 0:16.38 | The chips weren't the problem. The problem, in his words, was power. |
| 0.4 | 0:16.83 | 0:21.27 | So here's the question: will electricity become the ceiling on AI? |
| 0.5 | 0:21.77 | 0:24.73 | My answer is yes. But not in the way you think. |
| 0.6 | 0:25.33 | 0:29.62 | Because the thing that's really running out might not be electricity at all. |
| 1.1 | 0:30.62 | 0:34.59 | First, why does AI need so much electricity in the first place? |
| 1.2 | 0:35.04 | 0:39.57 | Data centers are built from racks, tall cabinets packed with computers. |
| 1.3 | 0:40.02 | 0:44.10 | In 2024, the average rack drew under 8 kilowatts. |
| 1.4 | 0:44.55 | 0:52.22 | A single rack of Nvidia's GB200 AI system is estimated to draw around 120. |
| 1.5 | 0:52.67 | 0:56.00 | That's roughly fifteen times as much, in one cabinet. |
| 1.6 | 0:56.45 | 1:06.99 | Now fill a whole campus with them. Elon Musk's xAI already runs about one and a half gigawatts of its own power plants for its data centers in Memphis. |
| 1.7 | 1:07.44 | 1:14.31 | One gigawatt, running around the clock, is about what 800,000 average American homes use. |
| 1.8 | 1:14.76 | 1:23.22 | Add it all up, and in 2024, data centers worldwide used about 415 terawatt-hours of electricity. |
| 1.9 | 1:23.67 | 1:28.09 | That's around one and a half percent of all the electricity the world uses. |
| 1.10 | 1:28.89 | 1:31.67 | One and a half percent doesn't sound like a crisis. |
| 1.11 | 1:32.12 | 1:41.27 | But the International Energy Agency expects it to more than double by 2030, to around 945 terawatt-hours. |
| 1.12 | 1:41.72 | 1:44.69 | That's slightly more than all of Japan uses today. |
| 1.13 | 1:45.14 | 1:52.87 | And it's concentrated. The United States alone accounts for about 45 percent of data center electricity. |
| 1.14 | 1:53.32 | 2:00.52 | Through 2030, data centers are expected to drive nearly half of America's growth in electricity demand. |
| 2.1 | 2:01.52 | 2:05.23 | You might think: chips keep getting more efficient. Won't that solve it? |
| 2.2 | 2:05.68 | 2:18.02 | They are getting more efficient. Nvidia says its newest system delivers up to 25 times more performance at the same power than the previous generation, on certain AI tasks. |
| 2.3 | 2:18.47 | 2:29.16 | And yet, data center electricity use has grown about 12 percent a year since 2017, more than four times faster than electricity use overall. |
| 2.4 | 2:29.61 | 2:41.53 | This is an old story. In 1865, the economist William Stanley Jevons noticed that more efficient steam engines didn't cut Britain's coal use. They increased it. |
| 2.5 | 2:41.98 | 2:46.13 | When something gets cheaper to use, we find far more ways to use it. |
| 2.6 | 2:46.58 | 2:52.66 | Cheaper AI means more AI. Efficiency doesn't shrink the bill. It grows the appetite. |
| 3.1 | 2:53.66 | 2:55.20 | Here's what most people miss. |
| 3.2 | 2:56.00 | 3:00.81 | The world isn't running out of electricity. It's running out of time to connect it. |
| 3.3 | 3:01.26 | 3:08.78 | A data center is just a building. Feeding it takes a whole chain: power plants, transmission lines, transformers. |
| 3.4 | 3:09.23 | 3:11.99 | And every link in that chain has a waiting line. |
| 3.5 | 3:12.44 | 3:20.33 | Start with power plants. In the US, a new power project has to apply to connect to the grid, then wait its turn. |
| 3.6 | 3:20.78 | 3:28.36 | At the end of 2025, more than 2,000 gigawatts of generation and storage were sitting in those lines. |
| 3.7 | 3:28.81 | 3:37.72 | For projects that finally came online in 2025, the typical wait from application to switching on was more than five years. |
| 3.8 | 3:38.17 | 3:46.66 | And most never make it at all. Of everything that applied between 2000 and 2020, only 13 percent was ever built. |
| 3.9 | 3:47.11 | 3:52.23 | New transmission lines in advanced economies take four to eight years to build. |
| 3.10 | 3:52.68 | 4:01.23 | Large power transformers now have lead times of up to four years, and prices have jumped roughly 80 percent in five years. |
| 3.11 | 4:01.68 | 4:11.09 | Gas turbines? GE Vernova, one of the biggest makers, said in December 2025 that it was sold out through 2028. |
| 3.12 | 4:11.54 | 4:20.03 | The IEA estimates that, unless these bottlenecks are fixed, around 20 percent of planned data center projects could be delayed. |
| 3.13 | 4:20.48 | 4:31.28 | In September 2026, Morgan Stanley put a number on the gap: a shortfall of about 32 gigawatts for US data centers through 2028. |
| 3.14 | 4:31.73 | 4:33.85 | That's roughly a third of what they need. |
| 3.15 | 4:34.30 | 4:42.01 | Chips move on product cycles. Power moves on permit and construction cycles, and those run five years and more. |
| 4.1 | 4:43.01 | 4:45.61 | When something is scarce, its price tells you. |
| 4.2 | 4:46.06 | 4:52.86 | PJM runs the power grid across all or parts of 13 US states and Washington, D.C. |
| 4.3 | 4:53.31 | 4:56.75 | Every year, it holds an auction for future power supply. |
| 4.4 | 4:57.20 | 5:03.65 | For 2024 to 2025, the price was about 29 dollars per megawatt-day. |
| 4.5 | 5:04.10 | 5:11.37 | For 2027 to 2028, it hit 333 dollars, the maximum the rules allowed. |
| 4.6 | 5:11.82 | 5:16.85 | Analysts estimate that without the cap, it would have been close to 530. |
| 4.7 | 5:17.30 | 5:22.09 | And even at that price, the auction still fell short of its reliability target. |
| 4.8 | 5:22.54 | 5:32.36 | The reason? PJM's demand forecast jumped by 5,250 megawatts, almost entirely because of data centers. |
| 4.9 | 5:32.81 | 5:35.25 | And that cost doesn't stay with tech companies. |
| 4.10 | 5:35.70 | 5:49.09 | In Washington, D.C., one utility's residential customers saw bills rise about 21 dollars a month starting in June 2025, around 10 of it from these capacity prices. |
| 5.1 | 5:50.09 | 5:51.86 | So the tech giants stopped waiting. |
| 5.2 | 5:52.31 | 6:03.17 | Microsoft signed a deal to bring back a reactor at Three Mile Island, which shut down in 2019. It's now expected back online in 2027. |
| 5.3 | 6:03.62 | 6:16.10 | Google signed up for small nuclear reactors from a company called Kairos Power: up to 500 megawatts, with the first targeted for 2030 and the rest by 2035. |
| 5.4 | 6:16.55 | 6:21.04 | Notice the dates. Even the fixes run on the grid's clock, not the chip's. |
| 5.5 | 6:21.49 | 6:23.55 | Others are skipping the grid entirely. |
| 5.6 | 6:24.00 | 6:32.03 | One analysis counted 59 US data center projects planning about 90 gigawatts of their own on-site power. |
| 5.7 | 6:32.48 | 6:36.92 | That's more than a quarter of all planned data center capacity in the country. |
| 5.8 | 6:37.37 | 6:42.60 | And 92 percent of those projects were announced since the start of 2025. |
| 5.9 | 6:43.20 | 6:51.52 | But here's the catch. As of mid-2026, only about 2 gigawatts of that was actually running. Roughly 2 percent. |
| 5.10 | 6:51.97 | 6:56.04 | Announcing a power plant is easy. Building one is the bottleneck. |
| 5.11 | 6:56.49 | 7:11.68 | It got strange. In December 2025, Crusoe, a company that builds AI data centers, ordered 29 gas turbines from Boom Supersonic, a startup best known for designing supersonic jets. |
| 5.12 | 7:12.13 | 7:20.61 | Then, in September 2026, Crusoe walked away from that deal and turned to established suppliers like GE Vernova. |
| 5.13 | 7:21.06 | 7:26.17 | When time is the bottleneck, an untested machine is a risk few can afford. |
| 6.1 | 7:27.17 | 7:28.26 | Now flip the map. |
| 6.2 | 7:28.71 | 7:33.78 | China generates more than twice as much electricity as the United States. |
| 6.3 | 7:34.23 | 7:41.03 | In 2025 alone, it added more than 430 gigawatts of wind and solar capacity. |
| 6.4 | 7:41.48 | 7:50.64 | BloombergNEF expects China to add more than six times as much generation capacity as the US over the next five years. |
| 6.5 | 7:51.09 | 8:00.21 | One business school researcher put it simply: the US has the chips and is short on power. China has the power and is short on chips. |
| 6.6 | 8:00.66 | 8:06.17 | So electricity isn't one ceiling. It's a different ceiling, depending on where you stand. |
| 7.1 | 8:07.17 | 8:08.42 | So here's my call. |
| 7.2 | 8:08.87 | 8:13.92 | Electricity won't stop AI. Too much money is chasing this problem for that. |
| 7.3 | 8:14.37 | 8:21.93 | But for the next few years, power will decide three things: how fast AI grows, where it gets built, and who wins. |
| 7.4 | 8:22.38 | 8:28.13 | The winners won't just be the ones with the best models. They'll be the ones who locked in power early. |
| 7.5 | 8:28.58 | 8:35.74 | I'd go further: by the end of this decade, a guaranteed grid connection may be worth more than the chips you plug into it. |
| 7.6 | 8:36.34 | 8:49.89 | And if I'm wrong, it'll be because the grid suddenly started moving at chip speed: new lines, plants and transformers arriving in two or three years instead of five or more. That's the signal to watch. |
| 8.1 | 8:50.89 | 8:52.28 | What does this mean for you? |
| 8.2 | 8:52.73 | 8:59.22 | If you live where data centers are booming, part of AI's bill may already be on your electricity bill. |
| 8.3 | 8:59.67 | 9:07.97 | And next time someone says AI is limited by chips, remember Microsoft's problem. The chips were there. The power wasn't. |
| 8.4 | 9:08.42 | 9:13.61 | So which do you think runs out first: chips, or electricity? Tell me in the comments. |

## 交付前自查（2026-10-08，10 分钟版 v2）

- [x] 两个版本都能完整播放：`ffmpeg -f null` 全片解码无报错；H.264 yuv420p，1920×1080，30fps；AAC 48kHz；时长 556.1 秒（9:16，超过 8 分钟下限）。
- [x] 抖音版双语字幕英上中下，YouTube 版只有英文：字幕烧录自 `subs_dy.ass` / `subs_yt.ass`；白字 + 黑描边 + 轻阴影，无底色块无边框；英文约 51px、中文约 43px（YouTube 版英文约 53px）；字幕区 y ≥ 910，在图号框下方。
- [~] 抽查画面：新增的 30 多个画面逐个看过；【留】的画面每段都抽了 3 帧以上（共约 60 帧）。另对成片每 2 秒一帧（278 帧）自动检测字幕区、画面边缘、图号框上方缓冲带有没有内容：只有转场帧被标出（图纸翻页的扫线、3.1 开头沿导线平移时导线贯穿画面边缘、翻地图）。静止元素没有出画，也没有被字幕遮挡。
- [~] 字幕与配音对齐：配音按句分别合成，每句的起止是精确值，字幕按这个出；长句拆成 2–4 段短字幕时切点按字符数估算，和实际读音可能差 0.3–0.5 秒，个别切点会切在句子中间（例如 3.13 的 "In September 2026, Morgan Stanley put a" / "number on the gap…"），没有逐词对齐。
- [~] 画面数字和旁白同步：数字出现的时刻按短语在句中的位置估算，没有逐词强制对齐，也没有人工听过成片，0.3 秒的容差没有实测。需要抽查的：1.3（8 kW）、1.4（120 kW）、1.7（800,000）、2.2（25×）、3.6（2,061 GW）、3.8（13%）、5.9（2%）。
- [x] 每个数字在画面、旁白、字幕三处一致：已逐个核对。新增数字在画面上的写法：< 8 kW (avg)、≈ 120 kW、×15、≈ 1.5 GW on-site、800,000（每个房子图标 = 10,000 户，共 80 个）、25× perf / same power*、+12%/yr、×4 faster、1865、2,061 GW、> 5 YRS (median)、13% BUILT、≤ 500 MW、2030 / 2035、~2 GW、2% BUILT、2–3 YRS。
- [x] 【留】的画面重新对齐后没有错位：用旧→新编号映射（`scenes_d.js` 里的 M1–M7）接到新旁白上，抽查的画面都对得上对应的句子；被新画面插入打断的几组（供电链和排队计时器、需求缺口、三哩岛、59 个点的地图、天平）都截到了新画面开始的位置。
- [x] 没有超过 30 秒不变的画面：成片每 0.5 秒取一帧，只要有任何像素变化就算变化，最长的静止段是 10 秒。
- [x] 红色印章 4 个：NO POWER（0.3）、SOLD OUT → 2028（3.11）、2% BUILT（5.9）、CANCELLED（5.12）。琥珀色 7 处：0.4 / 0.5 屋顶虚线、1.11 的 ×2+、3.14 缺口闪一下、4.5 的上限线和 $333、4.10 的 +$21/mo、6.6 两条天花板虚线、7.2 天花板虚线。
- [x] 没有真实照片、没有公司 logo、没有人脸；文字最小 32px。
- [x] 引语卡片：0.2 / 0.3 引 Nadella（出处 "Satya Nadella, Microsoft CEO — BG2 Pod, Nov 2025"），6.5 引 IMD 研究者（出处 "IMD Business School, via Al Jazeera, May 2026"）；2.2 的 25 倍在画面角落标了 "*Nvidia claim, specific workloads only"。6.5 卡片里的英文按旁白转述写成，未逐字比对 Al Jazeera 原文。
- [~] 配音：没找到 `voice-settings.txt`。这版沿用 5 分钟版用过的同一个 TTS 和声音（Kokoro v1.0，`am_michael`，语速 0.97），整条重新生成；这个声音当初是我挑的，不是你定好的那个。
- [x] `style_ai-future.md` 和 `production_log.md` 已输出。
