# v2（10 分钟版）旁白（英文，一字不改）+ 中文字幕。id 形如 "段.句"
import re
SECTIONS = [
 ("0", [
  ("0.1","In November 2025, Microsoft's CEO said something strange.","2025 年 11 月，微软的 CEO 说了一句奇怪的话。"),
  ("0.2","His company may have a bunch of AI chips sitting in inventory — that it can't plug in.","他们可能有一大批 AI 芯片躺在库存里，插不上电。"),
  ("0.3","The chips weren't the problem. The problem, in his words, was power.","问题不在芯片。用他的话说，问题在电。"),
  ("0.4","So here's the question: will electricity become the ceiling on AI?","所以问题来了：电，会不会成为 AI 的天花板？"),
  ("0.5","My answer is yes. But not in the way you think.","我的答案是：会。但不是你想的那种方式。"),
  ("0.6","Because the thing that's really running out might not be electricity at all.","因为真正不够用的，可能根本不是电。")]),
 ("1", [
  ("1.1","First, why does AI need so much electricity in the first place?","先说说，AI 到底为什么这么耗电？"),
  ("1.2","Data centers are built from racks, tall cabinets packed with computers.","数据中心是由一个个机柜组成的，就是塞满电脑的高柜子。"),
  ("1.3","In 2024, the average rack drew under 8 kilowatts.","2024 年，一个机柜平均用电不到 8 千瓦。"),
  ("1.4","A single rack of Nvidia's GB200 AI system is estimated to draw around 120.","而英伟达 GB200 AI 系统的一个机柜，估计要用大约 120 千瓦。"),
  ("1.5","That's roughly fifteen times as much, in one cabinet.","一个柜子，差不多是普通机柜的 15 倍。"),
  ("1.6","Now fill a whole campus with them. Elon Musk's xAI already runs about one and a half gigawatts of its own power plants for its data centers in Memphis.","现在把整个园区都装满这种机柜。马斯克的 xAI，光在孟菲斯就为自己的数据中心配了大约 1.5 吉瓦的自建电站。"),
  ("1.7","One gigawatt, running around the clock, is about what 800,000 average American homes use.","1 吉瓦全天候运转，大约相当于 80 万户美国普通家庭的用电量。"),
  ("1.8","Add it all up, and in 2024, data centers worldwide used about 415 terawatt-hours of electricity.","全部加起来，2024 年全球数据中心用了大约 415 太瓦时的电。"),
  ("1.9","That's around one and a half percent of all the electricity the world uses.","大约占全世界用电量的 1.5%。"),
  ("1.10","One and a half percent doesn't sound like a crisis.","1.5%，听起来不像什么危机。"),
  ("1.11","But the International Energy Agency expects it to more than double by 2030, to around 945 terawatt-hours.","但国际能源署预计，到 2030 年这个数字会翻一倍多，达到约 945 太瓦时。"),
  ("1.12","That's slightly more than all of Japan uses today.","比整个日本今天的用电量还略多一点。"),
  ("1.13","And it's concentrated. The United States alone accounts for about 45 percent of data center electricity.","而且非常集中。光美国一家，就占了全球数据中心用电的约 45%。"),
  ("1.14","Through 2030, data centers are expected to drive nearly half of America's growth in electricity demand.","到 2030 年，美国新增的用电需求里，预计将近一半来自数据中心。")]),
 ("2", [
  ("2.1","You might think: chips keep getting more efficient. Won't that solve it?","你可能会想：芯片越来越省电，问题不就解决了吗？"),
  ("2.2","They are getting more efficient. Nvidia says its newest system delivers up to 25 times more performance at the same power than the previous generation, on certain AI tasks.","芯片确实越来越省电。英伟达说，在某些 AI 任务上，它最新的系统在同样的用电下，性能最高是上一代的 25 倍。"),
  ("2.3","And yet, data center electricity use has grown about 12 percent a year since 2017, more than four times faster than electricity use overall.","但从 2017 年到现在，数据中心的用电量每年增长约 12%，是全社会用电增速的四倍多。"),
  ("2.4","This is an old story. In 1865, the economist William Stanley Jevons noticed that more efficient steam engines didn't cut Britain's coal use. They increased it.","这是个老故事了。1865 年，经济学家杰文斯发现：更高效的蒸汽机并没有让英国少烧煤，反而让英国烧得更多了。"),
  ("2.5","When something gets cheaper to use, we find far more ways to use it.","一样东西用起来越便宜，我们就会找到越多的用法。"),
  ("2.6","Cheaper AI means more AI. Efficiency doesn't shrink the bill. It grows the appetite.","AI 越便宜，用的人就越多。效率不会让账单变小，只会让胃口变大。")]),
 ("3", [
  ("3.1","Here's what most people miss.","但大多数人没注意到这一点。"),
  ("3.2","The world isn't running out of electricity. It's running out of time to connect it.","世界不是电不够了，而是来不及把电接过来。"),
  ("3.3","A data center is just a building. Feeding it takes a whole chain: power plants, transmission lines, transformers.","数据中心只是一栋楼。给它供电，需要一整条链：发电厂、输电线、变压器。"),
  ("3.4","And every link in that chain has a waiting line.","而这条链上的每一环，都在排队。"),
  ("3.5","Start with power plants. In the US, a new power project has to apply to connect to the grid, then wait its turn.","先说发电厂。在美国，新建一个发电项目，要先申请接入电网，然后排队等着。"),
  ("3.6","At the end of 2025, more than 2,000 gigawatts of generation and storage were sitting in those lines.","到 2025 年底，排在队伍里的发电和储能项目，加起来超过 2000 吉瓦。"),
  ("3.7","For projects that finally came online in 2025, the typical wait from application to switching on was more than five years.","2025 年终于建成的项目，从申请到真正发电，中位等待时间超过 5 年。"),
  ("3.8","And most never make it at all. Of everything that applied between 2000 and 2020, only 13 percent was ever built.","而且大多数项目根本建不成。2000 到 2020 年申请的项目里，最后真正建成的只有 13%。"),
  ("3.9","New transmission lines in advanced economies take four to eight years to build.","在发达经济体，建一条新的输电线要 4 到 8 年。"),
  ("3.10","Large power transformers now have lead times of up to four years, and prices have jumped roughly 80 percent in five years.","大型变压器的交货期已经拉长到最多 4 年，价格五年里涨了大约 80%。"),
  ("3.11","Gas turbines? GE Vernova, one of the biggest makers, said in December 2025 that it was sold out through 2028.","燃气轮机呢？最大的制造商之一 GE Vernova 在 2025 年 12 月说，2028 年以前的产能已经卖光了。"),
  ("3.12","The IEA estimates that, unless these bottlenecks are fixed, around 20 percent of planned data center projects could be delayed.","国际能源署估计，如果这些瓶颈解决不了，大约 20% 的在建数据中心项目可能延期。"),
  ("3.13","In September 2026, Morgan Stanley put a number on the gap: a shortfall of about 32 gigawatts for US data centers through 2028.","2026 年 9 月，摩根士丹利算了一下缺口：到 2028 年，美国数据中心大约缺 32 吉瓦的电。"),
  ("3.14","That's roughly a third of what they need.","差不多是需求的三分之一。"),
  ("3.15","Chips move on product cycles. Power moves on permit and construction cycles, and those run five years and more.","芯片按产品周期更新，电力却要按审批和施工的周期走，而这个周期动不动就是五年以上。")]),
 ("4", [
  ("4.1","When something is scarce, its price tells you.","一样东西缺不缺，看价格就知道。"),
  ("4.2","PJM runs the power grid across all or parts of 13 US states and Washington, D.C.","PJM 负责管理美国 13 个州（全部或部分地区）加上华盛顿特区的电网。"),
  ("4.3","Every year, it holds an auction for future power supply.","它每年都会拍卖未来的供电能力。"),
  ("4.4","For 2024 to 2025, the price was about 29 dollars per megawatt-day.","2024 到 2025 年度，价格大约是每兆瓦每天 29 美元。"),
  ("4.5","For 2027 to 2028, it hit 333 dollars, the maximum the rules allowed.","到了 2027 到 2028 年度，价格涨到 333 美元，碰到了规则允许的上限。"),
  ("4.6","Analysts estimate that without the cap, it would have been close to 530.","分析师估计，如果没有上限，价格会接近 530 美元。"),
  ("4.7","And even at that price, the auction still fell short of its reliability target.","而且就算开出这个价，拍卖还是没凑够保障供电稳定所需的量。"),
  ("4.8","The reason? PJM's demand forecast jumped by 5,250 megawatts, almost entirely because of data centers.","原因呢？PJM 预测的用电需求一下子多了 5250 兆瓦，几乎全是因为数据中心。"),
  ("4.9","And that cost doesn't stay with tech companies.","而这笔钱，不只是科技公司在付。"),
  ("4.10","In Washington, D.C., one utility's residential customers saw bills rise about 21 dollars a month starting in June 2025, around 10 of it from these capacity prices.","在华盛顿特区，一家电力公司的居民用户从 2025 年 6 月起，电费每月涨了约 21 美元，其中约 10 美元来自这类容量价格。")]),
 ("5", [
  ("5.1","So the tech giants stopped waiting.","于是，科技巨头们不等了。"),
  ("5.2","Microsoft signed a deal to bring back a reactor at Three Mile Island, which shut down in 2019. It's now expected back online in 2027.","微软签了协议，让三哩岛一座 2019 年就关掉的核反应堆重新启动，现在预计 2027 年恢复发电。"),
  ("5.3","Google signed up for small nuclear reactors from a company called Kairos Power: up to 500 megawatts, with the first targeted for 2030 and the rest by 2035.","谷歌向一家叫 Kairos Power 的公司订了小型核反应堆：最多 500 兆瓦，第一座目标 2030 年投运，其余的到 2035 年。"),
  ("5.4","Notice the dates. Even the fixes run on the grid's clock, not the chip's.","注意这些年份。就连解决办法，走的也是电网的时钟，而不是芯片的时钟。"),
  ("5.5","Others are skipping the grid entirely.","还有人干脆绕开电网。"),
  ("5.6","One analysis counted 59 US data center projects planning about 90 gigawatts of their own on-site power.","一份分析统计，美国有 59 个数据中心项目计划自建现场发电，总共约 90 吉瓦。"),
  ("5.7","That's more than a quarter of all planned data center capacity in the country.","这超过了全美规划中数据中心总容量的四分之一。"),
  ("5.8","And 92 percent of those projects were announced since the start of 2025.","而其中 92% 的项目，都是 2025 年以后才宣布的。"),
  ("5.9","But here's the catch. As of mid-2026, only about 2 gigawatts of that was actually running. Roughly 2 percent.","但问题来了：截至 2026 年年中，真正在运行的只有大约 2 吉瓦，差不多只占 2%。"),
  ("5.10","Announcing a power plant is easy. Building one is the bottleneck.","宣布要建电厂很容易，真正建起来才是瓶颈。"),
  ("5.11","It got strange. In December 2025, Crusoe, a company that builds AI data centers, ordered 29 gas turbines from Boom Supersonic, a startup best known for designing supersonic jets.","事情开始变得离奇。2025 年 12 月，AI 数据中心建造商 Crusoe 向 Boom Supersonic 订了 29 台燃气轮机，而这家公司最出名的是设计超音速客机。"),
  ("5.12","Then, in September 2026, Crusoe walked away from that deal and turned to established suppliers like GE Vernova.","结果到了 2026 年 9 月，Crusoe 放弃了这笔订单，转向 GE Vernova 这样的老牌供应商。"),
  ("5.13","When time is the bottleneck, an untested machine is a risk few can afford.","当时间就是瓶颈，没被验证过的机器，是很少有人敢冒的险。")]),
 ("6", [
  ("6.1","Now flip the map.","现在，把地图翻过来。"),
  ("6.2","China generates more than twice as much electricity as the United States.","中国的发电量，是美国的两倍多。"),
  ("6.3","In 2025 alone, it added more than 430 gigawatts of wind and solar capacity.","光是 2025 年一年，中国就新增了超过 430 吉瓦的风电和光伏装机。"),
  ("6.4","BloombergNEF expects China to add more than six times as much generation capacity as the US over the next five years.","彭博新能源财经预计，未来五年，中国新增的发电装机将是美国的六倍多。"),
  ("6.5","One business school researcher put it simply: the US has the chips and is short on power. China has the power and is short on chips.","一位商学院的研究者说得很直白：美国有芯片、缺电；中国有电、缺芯片。"),
  ("6.6","So electricity isn't one ceiling. It's a different ceiling, depending on where you stand.","所以电不是一块天花板。站在哪里，天花板就不一样。")]),
 ("7", [
  ("7.1","So here's my call.","所以，我的判断是："),
  ("7.2","Electricity won't stop AI. Too much money is chasing this problem for that.","电挡不住 AI，追着这个问题砸的钱太多了。"),
  ("7.3","But for the next few years, power will decide three things: how fast AI grows, where it gets built, and who wins.","但未来几年，电会决定三件事：AI 长得多快、建在哪里，以及谁会赢。"),
  ("7.4","The winners won't just be the ones with the best models. They'll be the ones who locked in power early.","赢家不只是模型最好的那家，而是最早锁定电力的那家。"),
  ("7.5","I'd go further: by the end of this decade, a guaranteed grid connection may be worth more than the chips you plug into it.","我甚至觉得：到这个十年结束时，一个有保障的电网接口，可能比插在上面的芯片还值钱。"),
  ("7.6","And if I'm wrong, it'll be because the grid suddenly started moving at chip speed: new lines, plants and transformers arriving in two or three years instead of five or more. That's the signal to watch.","如果我错了，那一定是因为电网突然跑出了芯片的速度：新的输电线、电厂和变压器，两三年就能到位，而不是五年以上。这就是值得盯住的信号。")]),
 ("8", [
  ("8.1","What does this mean for you?","这和你有什么关系？"),
  ("8.2","If you live where data centers are booming, part of AI's bill may already be on your electricity bill.","如果你住在数据中心扎堆的地方，AI 的一部分账单，可能已经算进你的电费里了。"),
  ("8.3","And next time someone says AI is limited by chips, remember Microsoft's problem. The chips were there. The power wasn't.","下次再有人说 AI 卡在芯片上，想想微软的问题：芯片有了，电没有。"),
  ("8.4","So which do you think runs out first: chips, or electricity? Tell me in the comments.","那你觉得，芯片和电，哪个会先不够用？评论区告诉我。")]),
]
LINES = [dict(id=i, en=e, zh=z, sec=s) for s, ls in SECTIONS for (i, e, z) in ls]

# ---- TTS 发音写法：只改读法，不改意思 ----
_ONES = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen".split()
_TENS = "_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()
def _two(n): return _ONES[n] if n < 20 else _TENS[n // 10] + ("-" + _ONES[n % 10] if n % 10 else "")
def int2w(n):
    if n < 100: return _two(n)
    if n < 1000: return _ONES[n // 100] + " hundred" + (" " + _two(n % 100) if n % 100 else "")
    if n < 1000000: return int2w(n // 1000) + " thousand" + (" " + int2w(n % 1000) if n % 1000 else "")
    return str(n)
def year2w(y):
    a, b = divmod(y, 100)
    if y == 2000: return "two thousand"
    if 2000 < y < 2010: return "two thousand " + _ONES[b]
    return _two(a) + " " + (("oh " + _ONES[b]) if 0 < b < 10 else (_two(b) if b else "hundred"))
def spoken(s):
    for a, b in [("GB200", "G B two hundred"), ("xAI", "x A I"), ("GE Vernova", "G E Vernova"), ("PJM", "P J M"), ("IEA", "I E A"),
                 ("BloombergNEF", "Bloomberg N E F"), ("D.C.", "D C"), ("Jevons", "Jevons")]:
        s = s.replace(a, b)
    s = re.sub(r'(?<![\d,])(1[89]\d\d|20\d\d)(?!,?\d)', lambda m: year2w(int(m.group(1))), s)
    s = re.sub(r'\d+(?:,\d{3})*', lambda m: int2w(int(m.group(0).replace(',', ''))), s)
    return s
