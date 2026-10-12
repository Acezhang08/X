# -*- coding: utf-8 -*-
"""Narration script for 'The AI Bubble, Explained: Follow the Money'.
English text is verbatim from the brief. `spoken` only changes how numbers/acronyms are read."""
import re

# (id, english, chinese, pre-pause override seconds or None)
SEGMENTS = {
0: [
("0.1","In 2025, five tech companies spent about four hundred billion dollars building AI.","2025 年，五家科技公司花了大约 4000 亿美元建 AI。",None),
("0.2","This year, they're on track to spend around eight hundred billion. Double, in one year.","今年，按计划要花大约 8000 亿。一年翻一倍。",None),
("0.3","And the question everyone types into YouTube is: is this a bubble?","大家在 YouTube 上搜的问题是：这是不是泡沫？",None),
("0.4","I think that's the wrong question. The better one is: where is the money actually going, and what's left standing if it stops?","我觉得问错了。更好的问题是：这些钱到底去了哪里？如果有一天停了，还剩下什么？",0.7),
("0.5","So let's follow one dollar all the way around. Because it doesn't go in a straight line. It goes in a circle.","我们跟着一美元走一圈。因为它不是直线走的，是在转圈。",None),
],
1: [
("1.1","Start with Nvidia. It makes the chips that almost every AI model runs on.","先看英伟达。几乎所有 AI 模型都跑在它的芯片上。",None),
("1.2","In September 2025, Nvidia announced it intended to invest up to one hundred billion dollars in OpenAI.","2025 年 9 月，英伟达宣布打算向 OpenAI 投资最多 1000 亿美元。",None),
("1.3","Read the fine print: the money would arrive in stages, as each gigawatt of computing power was deployed.","细则是：钱分批到，每部署 1 吉瓦算力就给一批。",None),
("1.4","Computing power built on what? Nvidia systems.","用什么算力？英伟达的系统。",None),
("1.5","Two weeks later, OpenAI signed a deal with Nvidia's rival, AMD. OpenAI would buy six gigawatts of AMD chips.","两周后，OpenAI 和英伟达的对手 AMD 签约：买 6 吉瓦的 AMD 芯片。",None),
("1.6","And AMD handed OpenAI the right to buy up to 160 million AMD shares, unlocked step by step as OpenAI's purchases grow.","AMD 给了 OpenAI 一个权利，可以买最多 1.6 亿股 AMD 股票，OpenAI 买得越多，解锁得越多。",None),
("1.7","The hundred-billion plan never got finalized.","1000 亿的计划最后没落地。",0.6),
("1.8","But this April, OpenAI closed a funding round of 122 billion dollars. One of the biggest checks, 30 billion, came from Nvidia.","但今年 4 月，OpenAI 完成了 1220 亿美元的融资，其中最大的几张支票之一，300 亿，来自英伟达。",None),
("1.9","So: the company selling the chips puts money into the company buying the chips.","所以：卖芯片的公司把钱投给买芯片的公司。",0.6),
("1.10","The buyer uses that money to buy more chips.","买家拿这笔钱再去买芯片。",None),
("1.11","And the seller books that as revenue.","卖家把它记成收入。",None),
],
2: [
("2.1","Is that illegal? No. Is it new? Also no. It has a name: vendor financing.","这违法吗？不违法。新鲜吗？也不新鲜。它有个名字：卖方融资。",None),
("2.2","And the last time it happened at this scale, it didn't end well.","上一次这么大规模地出现，结局不太好。",0.7),
("2.3","Late 1990s. The internet boom. Lucent was one of the biggest telecom equipment makers in the world.","1990 年代末，互联网热潮。朗讯是全世界最大的电信设备商之一。",None),
("2.4","Its customers were new internet companies racing to build networks, and many of them didn't have the cash.","它的客户是一批抢着建网络的新互联网公司，很多都没现金。",None),
("2.5","So Lucent lent it to them.","朗讯就借钱给它们。",None),
("2.6","In one deal it agreed to finance more than one hundred percent of a small carrier's equipment purchases.","有一单，它同意替一家小运营商出超过 100% 的设备钱。",None),
("2.7","By the time the bubble burst, Lucent had about seven billion dollars in loan commitments to its own customers.","泡沫破的时候，朗讯给自己客户的贷款承诺有大约 70 亿美元。",None),
("2.8","Then the customers started going bankrupt. That small carrier filed in 2001. The loans went bad.","然后客户开始破产。那家小运营商 2001 年申请破产。贷款收不回来。",None),
("2.9","Lucent's stock fell below one dollar.","朗讯股价跌到 1 美元以下。",None),
("2.10","Now, Nvidia is not Lucent. Nvidia is enormously profitable.","不过，英伟达不是朗讯。英伟达非常赚钱。",0.6),
("2.11","Last quarter alone, its data center business brought in 89 billion dollars, and it holds more than 50 billion dollars in cash and bonds. It can afford to be wrong.","光上个季度，它的数据中心业务就收入 890 亿美元，手里有超过 500 亿美元的现金和债券。它赔得起。",None),
("2.12","The real question isn't whether Nvidia survives. It's whether its customers can pay for what they've ordered.","真正的问题不是英伟达能不能活，而是它的客户付不付得起已经下的单。",None),
("2.13","And for that, we need to look at who's paying for the eight hundred billion.","所以要看：8000 亿到底是谁在出。",None),
],
3: [
("3.1","Most of it still comes from cash these companies earn. But not all of it anymore.","大部分钱还是这些公司自己赚来的现金。但已经不全是了。",None),
("3.2","By the end of June this year, the biggest cloud companies had already sold around 170 billion dollars of bonds in 2026. That's borrowed money.","到今年 6 月底，最大的几家云计算公司今年已经发了大约 1700 亿美元的债券。这是借来的钱。",None),
("3.3","And some of the borrowing doesn't show up where you'd look.","有些借款还不在你会去找的地方。",None),
("3.4","Take Meta's giant data center in Louisiana, called Hyperion.","比如 Meta 在路易斯安那的巨型数据中心 Hyperion。",None),
("3.5","Meta didn't put the 27 billion dollars of debt on its own books.","Meta 没把那 270 亿美元的债放在自己账上。",None),
("3.6","It set up a separate company: an investment firm, Blue Owl, owns 80 percent, Meta owns 20.","它另外成立了一家公司：投资公司 Blue Owl 占 80%，Meta 占 20%。",None),
("3.7","That company borrowed the money and built the data center. Meta rents it.","这家公司去借钱、建数据中心，Meta 来租。",None),
("3.8","But here's the catch. If Meta walks away, Meta has promised to cover the building's value for the first 16 years.","但关键在这：如果 Meta 不租了，它承诺前 16 年会补上这栋楼的价值。",None),
("3.9","So the risk is Meta's. The debt just isn't on Meta's balance sheet.","所以风险是 Meta 的，只是债不在 Meta 的资产负债表上。",None),
("3.10","Or take Oracle, one of the companies building computing capacity for OpenAI.","再看甲骨文，替 OpenAI 建算力的公司之一。",None),
("3.11","This year alone it has sold 25 billion dollars of bonds, issued 5 billion of a special kind of preferred stock, and planned up to 20 billion more in new shares.","光今年，它发了 250 亿美元债券，发了 50 亿一种特殊的优先股，还计划再发最多 200 亿新股。",None),
("3.12","That's three different ways of raising money in one year. When a company is reaching for every tool at once, it tells you how much cash this race eats.","一年里用了三种方式筹钱。一家公司同时把所有工具都用上，说明这场竞赛有多烧钱。",0.5),
],
4: [
("4.1","All that borrowing only makes sense if the money comes back as revenue. So does it?","这些借款只有在钱能以收入的形式回来时才说得通。回来了吗？",None),
("4.2","In 2024, an investor at Sequoia Capital, David Cahn, did a simple calculation.","2024 年，红杉资本的投资人 David Cahn 算过一笔简单的账。",None),
("4.3","Take what companies are spending on AI chips, double it for the buildings and electricity, double it again so the customers make a profit.","看大家花在 AI 芯片上的钱，乘 2 算上厂房和电费，再乘 2 让客户有钱赚。",None),
("4.4","His answer: AI needed to earn about 600 billion dollars a year to justify the spending. It was earning a small fraction of that.","结论是：AI 每年要赚大约 6000 亿美元才对得起这些投入。当时实际赚的只是零头。",None),
("4.5","Look at OpenAI, the most-used AI company in the world.","看 OpenAI，全世界用的人最多的 AI 公司。",None),
("4.6","In 2025, it made about 13 billion dollars in revenue.","2025 年收入大约 130 亿美元。",None),
("4.7","Its CEO has talked about computing commitments of about 1.4 trillion dollars over eight years.","它的 CEO 说过，未来 8 年的算力承诺大约 1.4 万亿美元。",None),
("4.8","It later scaled its plan to about 600 billion through 2030, and projects revenue of more than 280 billion that year.","后来计划缩到 2030 年前大约 6000 亿，并预计那一年收入超过 2800 亿。",None),
("4.9","So: from 13 billion to 280 billion in five years. That's about twenty times.","所以：5 年从 130 亿到 2800 亿，大约 20 倍。",0.6),
("4.10","Possible? Maybe. But the whole loop depends on it.","可能吗？也许。但整个圈都靠它。",0.6),
],
5: [
("5.1","Here's the part most bubble videos skip. Bubbles don't only destroy. Sometimes they build.","这一段是大部分讲泡沫的视频跳过的。泡沫不只会毁东西，有时候也会建东西。",None),
("5.2","Back to 2001. In the two years before the crash, telecom companies laid about 100 million miles of fiber optic cable.","回到 2001 年。崩盘前两年，电信公司铺了大约 1 亿英里光纤。",None),
("5.3","When the bubble burst, about 95 percent of it was sitting dark, unused. Investors lost fortunes.","泡沫破的时候，大约 95% 是暗的，没人用。投资人赔了大钱。",None),
("5.4","But the fiber stayed in the ground. Later, other companies bought that unused capacity cheaply and switched it on.","但光纤留在了地下。后来，别的公司低价买下这些闲置的线路，把它们点亮了。",None),
("5.5","The bubble was a disaster for the people who paid for it, and a bargain for everyone who came after.","那次泡沫对出钱的人是灾难，对后来的人是便宜货。",None),
("5.6","So will the AI bubble leave something behind too? This is where it gets uncomfortable.","那 AI 泡沫也会留下点什么吗？这里就让人不舒服了。",None),
("5.7","Fiber lasts for decades. AI chips don't. A new generation comes out every year or two.","光纤能用几十年，AI 芯片不行，一两年就出新一代。",None),
("5.8","Most of these companies spread the cost of their servers over five or six years.","这些公司大多把服务器的成本分摊到 5 到 6 年。",None),
("5.9","The investor Michael Burry, the one from The Big Short, argues that's too long for chips that go out of date this fast.","《大空头》里那位投资人 Michael Burry 认为，对过时这么快的芯片来说太长了。",None),
("5.10","By his estimate, it makes the industry's profits look about 176 billion dollars bigger than they are, through 2028.","按他的估算，到 2028 年，这会让整个行业的利润看起来多出大约 1760 亿美元。",None),
("5.11","You don't have to agree with him. But it changes the question.","你不一定要同意他。但问题变了。",0.6),
],
6: [
("6.1","There are really two bubbles here.","这里其实有两个泡沫。",None),
("6.2","One is in prices: stocks, valuations, deals that loop back on themselves. That one can pop fast.","一个在价格里：股价、估值、绕回自己身上的交易。这个可能破得很快。",None),
("6.3","The other is in things: buildings, power lines, grid connections, chips. Some of those will last decades. Some will be obsolete in three years.","另一个在实物里：厂房、电线、电网接入、芯片。有些能用几十年，有些三年就过时。",None),
("6.4","Think about what's actually hard to get right now. It isn't chips. It's electricity.","想想现在真正难拿到的是什么。不是芯片，是电。",0.5),
("6.5","Microsoft's CEO has said the company has AI chips sitting in inventory because it doesn't have the power to plug them in.","微软 CEO 说过，公司有 AI 芯片堆在仓库里，因为没有电插上。",None),
("6.6","And in the US, new power projects that came online in 2025 typically waited more than five years for their grid connection.","在美国，2025 年建成的发电项目，接入电网一般要等 5 年以上。",None),
("6.7","A building with a power connection is still worth something after the chips inside it are scrap.","芯片报废以后，一栋接好了电的楼还值钱。",None),
("6.8","That may be the fiber of this bubble: not the silicon, but the concrete and the copper around it.","这次泡沫的“光纤”可能就是这个：不是芯片，而是围着芯片的水泥和铜线。",0.5),
("6.9","So instead of asking \"is AI a bubble,\" ask: which parts last?","所以别问“AI 是不是泡沫”，问：哪些部分能留下来？",0.6),
("6.10","Because if you own an index fund, you already own a piece of this loop.","因为如果你买了指数基金，你已经拥有这个圈的一小块了。",None),
("6.11","My guess: the buildings and the power lines survive. The chips don't. What do you think survives? Tell me in the comments.","我的猜测：厂房和电线留得下来，芯片留不下来。你觉得什么会留下来？评论区告诉我。",None),
("6.12","This isn't investment advice. It's just following the money.","这不构成投资建议，只是跟着钱走了一遍。",None),
],
}

# per-line spoken overrides (numbers / acronyms spelled out). Meaning unchanged.
SPOKEN = {
"0.1":"In twenty twenty-five, five tech companies spent about four hundred billion dollars building A I.",
"1.1":"Start with Nvidia. It makes the chips that almost every A I model runs on.",
"1.2":"In September twenty twenty-five, Nvidia announced it intended to invest up to one hundred billion dollars in Open A I.",
"1.5":"Two weeks later, Open A I signed a deal with Nvidia's rival, A M D. Open A I would buy six gigawatts of A M D chips.",
"1.6":"And A M D handed Open A I the right to buy up to one hundred sixty million A M D shares, unlocked step by step as Open A I's purchases grow.",
"1.8":"But this April, Open A I closed a funding round of one hundred twenty-two billion dollars. One of the biggest checks, thirty billion, came from Nvidia.",
"2.3":"Late nineteen nineties. The internet boom. Lucent was one of the biggest telecom equipment makers in the world.",
"2.8":"Then the customers started going bankrupt. That small carrier filed in two thousand one. The loans went bad.",
"2.11":"Last quarter alone, its data center business brought in eighty-nine billion dollars, and it holds more than fifty billion dollars in cash and bonds. It can afford to be wrong.",
"3.2":"By the end of June this year, the biggest cloud companies had already sold around one hundred seventy billion dollars of bonds in twenty twenty-six. That's borrowed money.",
"3.5":"Meta didn't put the twenty-seven billion dollars of debt on its own books.",
"3.6":"It set up a separate company: an investment firm, Blue Owl, owns eighty percent, Meta owns twenty.",
"3.8":"But here's the catch. If Meta walks away, Meta has promised to cover the building's value for the first sixteen years.",
"3.10":"Or take Oracle, one of the companies building computing capacity for Open A I.",
"3.11":"This year alone it has sold twenty-five billion dollars of bonds, issued five billion of a special kind of preferred stock, and planned up to twenty billion more in new shares.",
"4.1":"All that borrowing only makes sense if the money comes back as revenue. So does it?",
"4.2":"In twenty twenty-four, an investor at Sequoia Capital, David Kahn, did a simple calculation.",
"4.3":"Take what companies are spending on A I chips, double it for the buildings and electricity, double it again so the customers make a profit.",
"4.4":"His answer: A I needed to earn about six hundred billion dollars a year to justify the spending. It was earning a small fraction of that.",
"4.5":"Look at Open A I, the most-used A I company in the world.",
"4.6":"In twenty twenty-five, it made about thirteen billion dollars in revenue.",
"4.7":"Its C E O has talked about computing commitments of about one point four trillion dollars over eight years.",
"4.8":"It later scaled its plan to about six hundred billion through twenty thirty, and projects revenue of more than two hundred eighty billion that year.",
"4.9":"So: from thirteen billion to two hundred eighty billion in five years. That's about twenty times.",
"5.2":"Back to two thousand one. In the two years before the crash, telecom companies laid about one hundred million miles of fiber optic cable.",
"5.3":"When the bubble burst, about ninety-five percent of it was sitting dark, unused. Investors lost fortunes.",
"5.6":"So will the A I bubble leave something behind too? This is where it gets uncomfortable.",
"5.7":"Fiber lasts for decades. A I chips don't. A new generation comes out every year or two.",
"5.10":"By his estimate, it makes the industry's profits look about one hundred seventy-six billion dollars bigger than they are, through twenty twenty-eight.",
"6.5":"Microsoft's C E O has said the company has A I chips sitting in inventory because it doesn't have the power to plug them in.",
"6.6":"And in the U S, new power projects that came online in twenty twenty-five typically waited more than five years for their grid connection.",
"6.9":"So instead of asking \"is A I a bubble,\" ask: which parts last?",
"5.9":"The investor Michael Burry, the one from The Big Short, argues that's too long for chips that go out of date this fast.",
}

def spoken(lid, en):
    if lid in SPOKEN: return SPOKEN[lid]
    t = en
    t = re.sub(r"\bOpenAI\b","Open A I",t)
    t = re.sub(r"\bAI\b","A I",t)
    t = re.sub(r"\bAMD\b","A M D",t)
    t = re.sub(r"\bCEO\b","C E O",t)
    return t
