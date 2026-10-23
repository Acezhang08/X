# -*- coding: utf-8 -*-
"""Narration for 'Are Data Centers Raising Your Electric Bill?'.
Segment 0 (the opening) is verbatim from the brief. `spoken` only changes how acronyms are read."""
import re

# (id, english, pre-pause override seconds or None)
SEGMENTS = {
0: [
("0.1", "Two years ago, America's biggest power grid paid twenty-nine dollars to keep one megawatt on standby for a day.", None),
("0.2", "This year: three hundred and twenty-nine.", None),
("0.3", "More than ten times as much — mainly because of data centers.", None),
("0.4", "And sixty-seven million people pay for it, in their electric bills.", None),
("0.5", "But the power industry's own research lab found that until recently, data centers were making those bills cheaper.", None),
("0.6", "Both are true.", 0.6),
("0.7", "So what flipped?", 0.7),
],
1: [
("1.1", "Open your electric bill and it looks like one number. It isn't.", None),
("1.2", "Some of it pays for the power itself. Some pays for the wires that carry it. And one slice pays for something most people have never heard of: capacity.", None),
("1.3", "Capacity is the price of being ready. A grid can't just have enough power on an average day. It needs enough on the hottest afternoon of the year, plus a cushion.", None),
("1.4", "So every year, the grid buys that readiness in advance, at an auction.", None),
("1.5", "In thirteen states and Washington, DC, the grid operator is PJM. The same grid from the start of this video.", None),
("1.6", "Here's how the auction works. PJM first calculates how many megawatts it will need on the hottest days, cushion included.", None),
("1.7", "Power plants bid, each naming the lowest price it will accept.", None),
("1.8", "PJM lines the bids up from cheapest to most expensive, and buys from the bottom until it has enough.", None),
("1.9", "And here's the part that matters. Every plant that wins is paid the price of the last one needed. One price, for everyone.", 0.6),
("1.10", "So when demand grows and supply is tight, the last plant costs more. And everyone gets paid more.", None),
("1.11", "The utilities that buy this power for customers pay that price. It ends up in your bill.", None),
("1.12", "Now look at that price, in dollars per megawatt, per day. Two years ago: twenty-nine. Then two hundred and seventy. Then three hundred and twenty-nine. Then three hundred and thirty-three.", None),
("1.13", "The most recent auction, in July, cleared at three hundred and twenty-five.", None),
("1.14", "The last three all hit a price cap. PJM's own simulation says that without the cap, the latest would have cleared above five hundred and fifty.", None),
("1.15", "So the price of readiness went up more than eleven times in two years, and then hit a ceiling.", 0.5),
("1.16", "Keep it in proportion, though. By the market monitor's count, capacity was about seventeen percent of the wholesale cost of power in early twenty twenty-six, up from about eight percent a year earlier.", None),
],
2: [
("2.1", "Now the surprising part. Nationally, for years, data centers appear to have done the opposite.", None),
("2.2", "In June, researchers at EPRI, the Electric Power Research Institute, posted a paper titled: Have Data Centers Raised Your Electric Bill?", None),
("2.3", "Quick note on who they are. EPRI is the electric power industry's research institute, funded by its members, mostly electric utilities. That doesn't make the numbers wrong. But you should know it.", None),
("2.4", "What did they find? From twenty nineteen to twenty twenty-four, the average American household lived in a state where data center capacity grew a hundred and sixty percent. They estimate that growth made residential electricity rates about six percent lower than they would otherwise have been.", None),
("2.5", "Put another way: each time a state's data center capacity doubled, residential rates fell by about three and a half percent. They're clear it's an estimate, with a wide range, from about one and a half percent to twelve.", None),
("2.6", "Why would more demand lower the price? Because most of a grid's cost is fixed: the power lines, the substations. When more electricity flows through the same wires, each unit carries a smaller share. And new power plants can cost less than the old ones.", None),
("2.7", "Columbia University's Center on Global Energy Policy said in June that recent price increases can't be pinned on any single factor, and that big new loads have not been a principal driver.", None),
("2.8", "But the discount comes with a condition. As one energy economist put it, the states where prices fell already had room on their grids.", None),
("2.9", "And blaming data centers for every price increase would be wrong too. From twenty twenty-one to twenty twenty-four, California's electricity prices rose nearly forty percent, which the same paper says was largely wildfire costs.", None),
("2.10", "So if data centers were pushing prices down, how did one price jump more than nine times, from one auction to the next?", 0.6),
],
3: [
("3.1", "The answer is in one word: room.", None),
("3.2", "Spreading fixed costs only works while the grid has spare capacity. When it's full, a new customer doesn't share the cost of the existing system. A new customer needs a new one.", None),
("3.3", "Look at where PJM's growth is coming from. For the auction covering twenty twenty-seven and twenty twenty-eight, its forecast peak demand rose by about fifty-two hundred and fifty megawatts. Nearly fifty-one hundred of that was data centers.", None),
("3.4", "Supply didn't keep up. That auction added only seven hundred and seventy-four megawatts of new generation and upgrades.", None),
("3.5", "And for the first time, the whole region's total fell short of PJM's own reliability target, by sixty-six hundred and twenty-three megawatts. PJM says that doesn't mean the lights go out. It means thinner reserves.", None),
("3.6", "More demand, less new supply, and the last plant needed sets the price for everyone. That's the jump.", None),
("3.7", "PJM has an independent watchdog, the market monitor. In June twenty twenty-five, it wrote that data center load growth is, in its words, the primary reason for recent and expected capacity market conditions.", 0.6),
("3.8", "Its estimate for the twenty twenty-five, twenty twenty-six auction: data center load alone raised that auction's total by about nine point three billion dollars, or a hundred and seventy-four percent.", None),
("3.9", "In July, it added up the last four auctions: about twenty-nine point four billion dollars tied to data center load. Forty-six percent of all capacity charges across those four auctions.", None),
("3.10", "Nine billion. Twenty-nine billion. Forty-six percent. Those are the monitor's estimates, and they measure charges in the auction, not what lands on each household's bill. But the direction is clear.", None),
("3.11", "And here's what makes it strange. A lot of that demand isn't here yet.", 0.7),
("3.12", "The auction doesn't run on how much power data centers use today. It runs on a forecast. In January, the monitor found that about six point two billion of the six and a half billion dollars it tied to data centers in the December auction came from data centers not yet built.", None),
("3.13", "It called the uncertainty in those forecasts unique and unprecedented.", None),
("3.14", "One reason: developers often don't tell a utility where else they've asked for power. According to the Associated Press, PJM says that means a single project can inflate more than one utility's forecast.", None),
("3.15", "That means part of today's price rests on buildings that don't exist yet. Some will be built. Some may not.", 0.5),
],
4: [
("4.1", "So who pays?", None),
("4.2", "The market monitor describes the problem plainly. It wants data centers to pay for their own capacity, and not impose capacity costs on other customers.", None),
("4.3", "That tells you how it works today: the cost is shared.", None),
("4.4", "How much does that add up to for a household? One estimate, from the think tank IEEFA, is that the higher capacity prices add about eighteen dollars a month to an average bill in western Maryland, and about sixteen dollars in Ohio.", None),
("4.5", "Careful with those numbers. They cover the whole jump in capacity prices, not only the data center share, and they're estimates.", None),
("4.6", "Now the other side. Across the country, residential electricity prices are up about forty-two percent in five years, according to federal data cited by PolitiFact.", None),
("4.7", "EPRI's researchers say aging equipment, disaster recovery and natural gas prices have mattered more than data centers.", None),
("4.8", "So both things are true at once. Nationally, data centers are not the main reason bills rose. But in a grid with no room left, they can be the main reason one price did.", 0.6),
],
5: [
("5.1", "The rules are changing, state by state. Here's what has actually happened.", None),
("5.2", "Oregon passed House Bill thirty-five forty-six. It tells the state's regulator to create a separate rate class for very large energy users, with costs assigned to them and protections for everyone else.", None),
("5.3", "Texas signed Senate Bill six in June twenty twenty-five. It makes very large new loads, seventy-five megawatts and up, contribute to the cost of connecting them to the grid.", None),
("5.4", "In Virginia, regulators approved a separate rate class for customers using twenty-five megawatts or more, starting in January twenty twenty-seven. They must sign fourteen-year contracts with minimum payments, even if they use less.", None),
("5.5", "And the market monitor wants a bigger change: take data centers out of the shared capacity market and give them their own auction.", None),
("5.6", "None of this changes yesterday's prices. It shapes the next ones.", None),
],
6: [
("6.1", "So, will a data center raise your electric bill?", None),
("6.2", "Not automatically. The real question is two questions.", None),
("6.3", "One: does your grid still have room? If it does, new demand can spread fixed costs and push prices down. If it doesn't, the next megawatt gets expensive for everyone.", None),
("6.4", "Two: when it isn't cheap, who pays? Right now, a lot of that cost is shared. The rules being written now will decide whether it stays that way.", None),
("6.5", "Is a data center being built near you — and has your electric bill changed? Tell me in the comments.", 0.8),
],
}

# EPRI is read letter by letter everywhere; PJM likewise.
def spoken(lid, en):
    t = en
    t = re.sub(r"\bEPRI's\b", "E P R I's", t)
    t = re.sub(r"\bEPRI\b", "E P R I", t)
    t = re.sub(r"\bPJM's\b", "P J M's", t)
    t = re.sub(r"\bPJM\b", "P J M", t)
    t = re.sub(r"\bIEEFA\b", "I E E F A", t)
    t = re.sub(r"\bDC\b", "D C", t)
    t = re.sub(r"\bPolitiFact\b", "Politi-Fact", t)
    return t

if __name__ == "__main__":
    n = 0
    for k, v in SEGMENTS.items():
        w = sum(len(e.split()) for _, e, _ in v); n += w; print(k, w)
    print("total words", n)
