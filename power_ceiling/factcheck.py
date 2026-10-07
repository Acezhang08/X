import json
tl = json.load(open('timeline.json')); by = {l['id']: l for l in tl['lines']}
def tc(x): m = int(x // 60); s = x - m * 60; return f"{m}:{s:05.2f}"
def rng(a, b=None):
    b = b or a; return f"{tc(by[a]['start'])}–{tc(by[b]['end'])}"
ROWS = [
 ("0.1–0.3","0.1","0.3","微软 CEO Nadella 说可能有一批芯片放在库存里插不上电；最大的问题是电","DCD（2025-11-03），BG2 Pod，与 Sam Altman 同场；原话：\"you may actually have a bunch of chips sitting in inventory that I can't plug in\"、\"The biggest issue we are now having is not a compute glut, but it's power\" — https://www.datacenterdynamics.com/en/news/microsoft-has-ai-gpus-sitting-in-inventory-because-it-lacks-the-power-necessary-to-install-them ；TechRadar 同引","✅ 旁白用了\"may\"，和原话语气一致"),
 ("0.5","0.5","0.5","\"会，但不是你想的那种方式\"","观点","—"),
 ("1.2–1.3","1.2","1.3","2024 年数据中心用电约 415 TWh，约占全球 1.5%","IEA《Energy and AI》执行摘要 — https://www.iea.org/reports/energy-and-ai/executive-summary","✅"),
 ("1.5–1.6","1.5","1.6","2030 年翻一倍多到约 945 TWh，略多于日本今天的总用电量","同上","✅"),
 ("1.7","1.7","1.7","美国占数据中心用电约 45%","同上","✅"),
 ("1.8","1.8","1.8","到 2030 年美国用电增长将近一半来自数据中心","同上","✅"),
 ("2.2","2.2","2.2","不是电不够，是来不及接","观点（有 2.5–2.9 的数据支撑）","—"),
 ("2.5","2.5","2.5","发达经济体建输电线要 4–8 年","IEA 同上","✅"),
 ("2.6","2.6","2.6","大型变压器交期最长 4 年，五年涨价约 80%","pv magazine USA（2026-05-11），引 PwC 和业内人士 — https://pv-magazine-usa.com/2026/05/11/u-s-transformer-market-faces-severe-supply-constraints-as-lead-times-extend-to-four-years/","✅"),
 ("2.7","2.7","2.7","GE Vernova 去年年底说燃气轮机 2028 年以前已卖完","Gas Processing News（2025-12），CEO Scott Strazik — https://www.gasprocessingnews.com/news/2025/12/ge-vernova-expects-80-gw-of-gas-turbine-contracts-by-years-end/","✅"),
 ("2.8","2.8","2.8","约 20% 规划中的数据中心项目可能延期","IEA 同上","✅"),
 ("2.9–2.10","2.9","2.10","摩根士丹利：到 2028 年缺口约 32 GW，约为需求的 34%","Reuters 经 Investing.com（2026-10），引摩根士丹利 2026 年 9 月报告 — https://investing.com/news/stock-market-news/nvidia-broadcom-shielded-as-ai-power-crunch-hits-chip-supply-chain-says-morgan-stanley-4932458","✅ 34% 在旁白里写成\"约三分之一\""),
 ("3.2","3.2","3.2","PJM 覆盖 13 个州（全部或部分）和华盛顿特区","PJM 官网 — https://www.pjm.com/about-pjm","✅"),
 ("3.4–3.6","3.4","3.6","容量拍卖：2024/25 年度 $28.92，2027/28 年度 $333.44 触顶，无上限约 $530","Utility Dive — https://www.utilitydive.com/news/pjm-interconnection-capacity-auction-data-center/808264/","✅ 旁白取整为 29 和 333"),
 ("3.7","3.7","3.7","仍未达到可靠性目标（缺 6,625 MW）","同上","✅"),
 ("3.8","3.8","3.8","需求预测增加 5,250 MW，几乎全因数据中心","同上","✅"),
 ("3.10","3.10","3.10","华盛顿特区 Pepco 居民电费从 2025 年 6 月起每月涨约 $21，其中约 $10 来自容量价格","IEEFA — https://ieefa.org/resources/projected-data-center-growth-spurs-pjm-capacity-prices-factor-10","✅ 旁白写\"one utility\"，没有点 Pepco 的名字"),
 ("4.2","4.2","4.2","微软协议重启三哩岛反应堆，2019 年关闭，预计 2027 年恢复","NS Energy — https://www.nsenergybusiness.com/news/crane-clean-energy-center-2027-restart/ ；FOX29 报道提前重启","✅"),
 ("4.4–4.6","4.4","4.6","59 个项目、约 90 GW 现场发电，超过规划容量的四分之一，92% 是 2025 年以来宣布的","Cleanview《Behind-the-Meter Data Centers》（2026 年中） — https://cleanview.co/reports/behind-the-meter-data-centers","✅"),
 ("4.7","4.7","4.7","Crusoe 向 Boom Supersonic 订 29 台燃气轮机","Boom 新闻稿（2025-12-09）：29 台，共 1.21 GW — https://boomsupersonic.com/press-release/boom-supersonic-to-power-ai-data-centers","✅"),
 ("4.8","4.8","4.8","上个月 Crusoe 取消订单，转向 GE Vernova 等老牌供应商","TechRepublic（2026-09-25） — https://www.techrepublic.com/article/news-crusoe-boom-turbine-deal/ ；Baxtel 交叉印证","✅ 两家来源都提到转向 GE Vernova；取消原因的说法不一，旁白没有写原因"),
 ("4.9","4.9","4.9","没被验证过的机器是很少有人敢冒的险","观点","—"),
 ("5.2–5.4","5.2","5.4","中国发电量是美国两倍多；2025 年新增风光 430+ GW；BNEF 预计未来五年中国新增装机是美国的六倍多","Al Jazeera（2026-05-28） — https://www.aljazeera.com/economy/2026/5/28/chinas-secret-weapon-in-ai-race-with-us-lots-of-cheap-energy","✅"),
 ("5.5","5.5","5.5","\"美国有芯片缺电，中国有电缺芯片\"","同上，IMD 商学院一位 director 的原话","✅ 旁白写\"business school researcher\""),
 ("6.2–6.5","6.2","6.5","电挡不住 AI；决定速度、地点、赢家；电网接口可能比芯片值钱","观点（明确用了 \"my call\"\"I'd go further\"\"may\"）","—"),
 ("7.2","7.2","7.2","AI 的账单可能已经算进部分地区居民的电费","有 3.10 支撑；用了 \"may\"","✅"),
]
out = ["# fact_check：Will Electricity Cap AI?", "", "核实日期：2026-10-08。观点句（我的判断）已标注，不需要来源。\"成片时间码\"是该句旁白在 `youtube_power_ceiling.mp4` / `douyin_power_ceiling.mp4`（两版时间轴相同）里的起止时间，格式 分:秒。", "",
       "| # | 成片时间码 | 说法 | 来源 | 结论 |", "|---|---|---|---|---|"]
for r in ROWS: out.append(f"| {r[0]} | {rng(r[1], r[2])} | {r[3]} | {r[4]} | {r[5]} |")
out += ["", "**已删掉的说法**：Crusoe 是 OpenAI 星际之门项目的建造商（没有核实，删了）；Crusoe 取消订单的具体原因（来源说法不一，删了）。", ""]
out += ["## 全部旁白句时间码", "", "| 句 | 起 | 止 | 英文旁白 |", "|---|---|---|---|"]
for l in tl['lines']: out.append(f"| {l['id']} | {tc(l['start'])} | {tc(l['end'])} | {l['en']} |")
open('fact_check.md', 'w').write('\n'.join(out) + '\n')
