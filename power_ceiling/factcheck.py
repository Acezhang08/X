import json
tl = json.load(open('timeline.json')); by = {l['id']: l for l in tl['lines']}
def tc(x): m = int(x // 60); s = x - m * 60; return f"{m}:{s:05.2f}"
def rng(k):
    a, b = (k.split('–') + [k])[:2] if '–' in k else (k, k)
    return f"{tc(by[a]['start'])}–{tc(by[b]['end'])}"
ROWS = [
 ("0.1–0.3","Nadella 2025 年 11 月说可能有一批芯片放在库存里插不上电；最大的问题是电","DCD（2025-11-03），BG2 Pod；原话 \"you may actually have a bunch of chips sitting in inventory that I can't plug in\" — https://www.datacenterdynamics.com/en/news/microsoft-has-ai-gpus-sitting-in-inventory-because-it-lacks-the-power-necessary-to-install-them","✅"),
 ("0.5–0.6","会，但不是你想的方式；真正不够的可能不是电","观点","—"),
 ("1.3","2024 年机柜平均用电不到 8 千瓦","Upsite 引 Uptime Institute 2024 年调查（\"not quite at 8 kW\"）— https://www.upsite.com/blog/data-center-trends-rack-density-rises-while-pue-and-outage-frequency-remain-flat/","✅"),
 ("1.4","GB200 NVL72 一个机柜估计约 120 千瓦","DataCrunch — https://datacrunch.io/blog/nvidia-gb200-nvl72-for-ai-training-and-inference （英伟达官网没给机柜功率，所以旁白用了 \"is estimated\"）","✅"),
 ("1.5","约 15 倍","计算：120 ÷ 8 = 15；平均值不到 8，所以用 \"roughly\"","✅"),
 ("1.6","xAI 在孟菲斯约 1.5 吉瓦自建电站","Cleanview：xAI 孟菲斯 Colossus 1 和 2 约 1,498 MW 现场发电在运行 — https://cleanview.co/reports/behind-the-meter-data-centers","✅"),
 ("1.7","1 吉瓦 ≈ 80 万户美国家庭用电","计算：EIA 2022 年户均 10,791 kWh/年 = 平均 1.23 kW；1,000,000 kW ÷ 1.23 ≈ 81 万户 — https://www.eia.gov/tools/faqs/faq.php?id=97&t=3","✅"),
 ("1.8–1.9","2024 年约 415 TWh，约占全球 1.5%","IEA《Energy and AI》— https://www.iea.org/reports/energy-and-ai/executive-summary","✅"),
 ("1.11–1.12","2030 年约 945 TWh，略多于日本","同上","✅"),
 ("1.13","美国占约 45%","同上","✅"),
 ("1.14","美国用电增长将近一半来自数据中心","同上","✅"),
 ("2.2","英伟达称特定 AI 任务上同功率性能最高 25 倍","英伟达官网 GB200 NVL72 页面：\"25x more performance at the same power\"，对比 H100 风冷，脚注为特定大模型推理条件、\"projected\" — https://www.nvidia.com/en-us/data-center/gb200-nvl72/","✅ 旁白写明 \"Nvidia says\" 和 \"on certain AI tasks\"；画面角落标了 \"Nvidia claim, specific workloads only\""),
 ("2.3","2017 年以来数据中心用电年增约 12%，是总用电增速的四倍多","IEA 同上","✅"),
 ("2.4","1865 年杰文斯发现更高效的蒸汽机让英国用煤更多","稳定的历史知识：杰文斯《煤炭问题》（The Coal Question，1865）","✅"),
 ("2.5–2.6","越便宜用得越多；效率让胃口变大","观点（杰文斯悖论的通俗说法）","—"),
 ("3.2","不是电不够，是来不及接","观点（有 3.5–3.15 的数据支撑）","—"),
 ("3.6","2025 年底排队的发电和储能超过 2000 吉瓦","伯克利实验室《Queued Up 2026》（2026-07-01）：约 2,061 GW — https://emp.lbl.gov/news/backlog-power-plants-seeking-transmission-grid-connection-eased-somewhat-2025-amidst","✅"),
 ("3.7","2025 年建成的项目，从申请到发电中位数超过 5 年","同上，\"over 5 years\"（限有数据的地区）","✅"),
 ("3.8","2000–2020 年申请的项目只有 13% 建成","同上","✅"),
 ("3.9","输电线 4–8 年","IEA 同上","✅"),
 ("3.10","变压器交期最长 4 年，五年涨约 80%","pv magazine USA（2026-05-11）— https://pv-magazine-usa.com/2026/05/11/u-s-transformer-market-faces-severe-supply-constraints-as-lead-times-extend-to-four-years/","✅"),
 ("3.11","GE Vernova 2025 年 12 月说 2028 年前卖光","Gas Processing News（2025-12）— https://www.gasprocessingnews.com/news/2025/12/ge-vernova-expects-80-gw-of-gas-turbine-contracts-by-years-end/","✅"),
 ("3.12","约 20% 项目可能延期","IEA 同上","✅"),
 ("3.13–3.14","摩根士丹利 2026 年 9 月：到 2028 年缺约 32 GW，约 34%","Reuters 经 Investing.com — https://investing.com/news/stock-market-news/nvidia-broadcom-shielded-as-ai-power-crunch-hits-chip-supply-chain-says-morgan-stanley-4932458","✅"),
 ("3.15","芯片按产品周期，电力按审批施工周期、五年以上","观点，\"五年以上\"有 3.7 支撑","—"),
 ("4.2","PJM 覆盖 13 个州和华盛顿特区","PJM 官网 — https://www.pjm.com/about-pjm","✅"),
 ("4.4–4.6","$28.92 → $333.44（触顶），无上限约 $530","Utility Dive — https://www.utilitydive.com/news/pjm-interconnection-capacity-auction-data-center/808264/","✅"),
 ("4.7–4.8","未达可靠性目标；需求预测增加 5,250 MW，几乎全因数据中心","同上","✅"),
 ("4.10","华盛顿特区 Pepco 居民电费从 2025 年 6 月起每月涨约 $21，约 $10 来自容量价格","IEEFA — https://ieefa.org/resources/projected-data-center-growth-spurs-pjm-capacity-prices-factor-10","✅"),
 ("5.2","三哩岛反应堆 2019 年关闭，预计 2027 年恢复","NS Energy — https://www.nsenergybusiness.com/news/crane-clean-energy-center-2027-restart/","✅"),
 ("5.3","谷歌–Kairos：最多 500 MW，首座 2030 年，全部 2035 年","World Nuclear News（2024-10-15）— https://www.world-nuclear-news.org/articles/google-and-kairos-power-team-up-for-smr-deployments-in-us-first","✅"),
 ("5.4","解决办法也走电网的时钟","观点","—"),
 ("5.6–5.8","59 个项目约 90 GW，超过规划容量四分之一，92% 是 2025 年以来宣布的","Cleanview（2026 年中）— https://cleanview.co/reports/behind-the-meter-data-centers","✅"),
 ("5.9","截至 2026 年年中只有约 2 GW 在运行，约 2%","同上：\"approximately 2 GW (2.2% of announced capacity) operates today\"","✅"),
 ("5.10","宣布容易建成难","观点","—"),
 ("5.11","2025 年 12 月 Crusoe 向 Boom 订 29 台燃气轮机","Boom 新闻稿（2025-12-09）— https://boomsupersonic.com/press-release/boom-supersonic-to-power-ai-data-centers","✅"),
 ("5.12","2026 年 9 月 Crusoe 取消订单，转向 GE Vernova 等","TechRepublic（2026-09-25）— https://www.techrepublic.com/article/news-crusoe-boom-turbine-deal/","✅"),
 ("5.13","没验证的机器是很少有人敢冒的险","观点","—"),
 ("6.2–6.4","中国发电量是美国两倍多；2025 年新增风光 430+ GW；BNEF 预计未来五年中国新增装机是美国六倍多","Al Jazeera（2026-05-28）— https://www.aljazeera.com/economy/2026/5/28/chinas-secret-weapon-in-ai-race-with-us-lots-of-cheap-energy","✅"),
 ("6.5","美国有芯片缺电，中国有电缺芯片","同上，IMD 商学院一位 director","✅ 卡片里的英文已按审片意见改为原文"),
 ("7.2–7.6","电挡不住 AI；决定速度、地点、赢家；电网接口可能比芯片值钱；判断错了的信号","观点","—"),
 ("8.2","AI 的账单可能已经算进部分地区居民电费","有 4.10 支撑；用了 \"may\"","✅"),
]
out = ["# fact_check：Will Electricity Cap AI?（10 分钟版 v2）", "", "核实日期：2026-10-08。观点句已标注，不需要来源。\"成片时间码\"是该句旁白在 `youtube_power_ceiling_v2.mp4` / `douyin_power_ceiling_v2.mp4`（两版时间轴相同）里的起止时间，格式 分:秒。", "",
       "| # | 成片时间码 | 说法 | 来源 | 结论 |", "|---|---|---|---|---|"]
for r in ROWS: out.append(f"| {r[0]} | {rng(r[0])} | {r[1]} | {r[2]} | {r[3]} |")
out += ["", "**已删掉、不要加回来的说法**：Crusoe 是 OpenAI 星际之门项目的建造商（未核实）；Crusoe 取消订单的具体原因（来源说法不一）。", "",
        "## 全部旁白句时间码", "", "| 句 | 起 | 止 | 英文旁白 |", "|---|---|---|---|"]
for l in tl['lines']: out.append(f"| {l['id']} | {tc(l['start'])} | {tc(l['end'])} | {l['en']} |")
open('fact_check.md', 'w').write('\n'.join(out) + '\n')
