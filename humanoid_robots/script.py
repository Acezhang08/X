# -*- coding: utf-8 -*-
"""Narration for 'Humanoid Robots Can Do Backflips. Why Can't They Fold Laundry?' (The Future of AI #2).
`en` is exactly what the viewer reads (subtitles) and what fact_check.md quotes.
`spoken()` only changes HOW numbers/acronyms are pronounced, never what is said."""
import re

# (id, english, pre-pause override seconds or None)
SEGMENTS = {
0: [
("0.1", "In 2017, a humanoid robot did a backflip.", None),
("0.2", "In 2024, a company called Unitree posted a video of its electric humanoid doing one too.", None),
("0.3", "Now ask one of these robots to fold a shirt.", 0.6),
("0.4", "In February 2026, a startup began shipping a laundry-folding robot for nearly eight thousand dollars. When it gets stuck, a human specialist takes over remotely, for a few seconds at a time.", None),
("0.5", "A backflip makes headlines. Folding laundry is a chore a child can do.", 0.6),
("0.6", "So why has the stunt been solved, and the chore has not?", 0.5),
("0.7", "The answer was written down in 1988, and it says the backflip is the easy part.", 0.7),
],
1: [
("1.1", "In 1988, the roboticist Hans Moravec noticed something strange.", None),
("1.2", "In his book Mind Children, he argued that it is far easier to make a computer play checkers at an adult level than to give it the perception and mobility of a one-year-old.", None),
("1.3", "Nine years later, in 1997, IBM's Deep Blue beat the world chess champion, Garry Kasparov, in a match.", None),
("1.4", "This became known as Moravec's paradox: what is hard for people is often easy for machines, and what is easy for people is often hard.", 0.6),
("1.5", "Why? Moravec's explanation was evolution.", None),
("1.6", "Seeing and moving have been refined for hundreds of millions of years. Fossil eyes date back more than 500 million years.", None),
("1.7", "Writing is about five thousand years old.", 0.5),
("1.8", "Reasoning feels hard because it is new. Seeing and moving feel easy only because evolution has polished them for so long.", None),
("1.9", "A robot gets no such head start. So the real question is not why robots are bad at laundry. It is why they are good at backflips.", 0.7),
],
2: [
("2.1", "Here is the first surprise. A backflip is easy in the same way chess is easy.", None),
("2.2", "A humanoid robot is a stack of rigid metal links joined at motors. Physics engines handle rigid bodies well, so a computer can simulate one.", None),
("2.3", "That means engineers can train the robot in a simulator, where it can fall as many times as it takes without breaking anything.", None),
("2.4", "In 2021, researchers at ETH Zurich and NVIDIA taught a four-legged robot to walk over rough ground in about 20 minutes, on a single graphics card, using thousands of simulated robots at once.", None),
("2.5", "Then the trained controller is copied onto the real machine. Reports say Unitree's 2024 backflip was trained that way too.", None),
("2.6", "A backflip is also short, rehearsed, and flat. The floor is known, the body is known, and nothing in the scene moves unless the robot moves it.", None),
("2.7", "It is an exam where the questions are published in advance.", 0.5),
("2.8", "So here is the twist. A backflip is a hard stunt with an easy problem inside it: a known body, a known floor, a known goal.", 0.8),
("2.9", "Laundry is the reverse. An easy-looking job with a hard problem inside it.", 0.5),
],
3: [
("3.1", "Start with the cloth. A metal link has one shape. A shirt has no fixed shape at all.", None),
("3.2", "Robotics researchers say a deformable object has, in effect, infinite degrees of freedom.", None),
("3.3", "And cloth hides itself. A fold covers a sleeve, and the camera cannot see what is underneath.", None),
("3.4", "Simulating cloth is the other trouble. Studies report that simulated garments stretch, distort, and pass through themselves, and that accurate cloth simulators are often too slow for large-scale training.", None),
("3.5", "So the trick that taught the backflip works much less well on a shirt.", 0.5),
("3.6", "Then there is your home. Every kitchen, every closet, every laundry basket is different.", None),
("3.7", "And there are the hands. A human hand has about 17,000 receptors for light touch.", None),
("3.8", "Rodney Brooks, a co-founder of iRobot, argues that you cannot learn touch if nobody is collecting touch data.", None),
("3.9", "In 2019, OpenAI trained a robot hand in simulation to solve a Rubik's Cube, with training equal to roughly 13,000 years of experience.", 0.6),
("3.10", "A separate program worked out the moves. The hand only had to carry them out. It still solved the cube just 60 percent of the time, and 20 percent for the hardest scrambles.", None),
("3.11", "In 2010, a robot at UC Berkeley folded towels, 50 times out of 50. But a towel is a rectangle with four corners. A shirt is not.", 0.6),
("3.12", "In 2026, a laundry robot on sale reportedly cannot handle bed sheets or inside-out garments.", None),
("3.13", "The robot is not failing at the physics. It is failing at the variety, and at the practice.", 0.6),
],
4: [
("4.1", "Which brings us to the real bottleneck. Not the motors. The data.", None),
("4.2", "Chatbots learned from text, and there is a lot of text. Meta's Llama 3 was trained on more than 15 trillion tokens.", None),
("4.3", "A token is roughly three-quarters of a word. At the average adult reading speed, 238 words a minute, reading that much nonstop would take about 90,000 years.", None),
("4.4", "Now the robots. The Open X-Embodiment project pooled data from 21 institutions into more than a million robot trajectories, from 22 kinds of robot.", 0.6),
("4.5", "A million sounds like a lot. But each trajectory is one short attempt at a task. The DROID dataset, collected by 50 people over 12 months, has 76,000 trajectories. That adds up to about 350 hours.", None),
("4.6", "AgiBot World, from 2025, lists almost 3,000 hours of recordings, gathered by over a hundred robots. That is 124 days.", None),
("4.7", "Ninety thousand years of text, against four months of robot.", 0.7),
("4.8", "A token and an hour of robot time are not the same thing. But in time, the gap is more than 200,000 to one.", None),
("4.9", "So where does robot data come from? There are three places.", 0.6),
("4.10", "First, teleoperation. A person drives the robot through a task while it records. Stanford's Mobile ALOHA team found that 50 demonstrations per task, combined with older data, could raise success rates by up to 90 percent, enough for tasks like cooking a shrimp.", None),
("4.11", "It works, but it is slow by design: an hour of data costs at least an hour of someone's time.", None),
("4.12", "Second, simulation, which we saw works for backflips and badly for cloth.", None),
("4.13", "Third, video of people. Figure says a model trained only on first-person human video could navigate cluttered homes. But video has no touch in it, and that is Brooks's objection.", None),
],
5: [
("5.1", "This is why robot demos are so hard to read.", None),
("5.2", "In October 2024, Tesla showed Optimus robots serving drinks at its We, Robot event. Bloomberg reported that people in another location oversaw many of the interactions, and a Tesla official later said some functions were remotely controlled.", None),
("5.3", "In October 2025, a reporter at the Wall Street Journal tested a home humanoid called Neo, priced at 20,000 dollars. In her test, the work was done by a remote human operator.", None),
("5.4", "That is not necessarily a trick. Some companies say openly that the human is part of the plan. 1X's chief executive told her that without customers' data, the product cannot get better.", None),
("5.5", "The laundry startup says the same: its specialists' corrections feed back into its model.", None),
("5.6", "The remote human is a stopgap. And it is also where the missing data comes from.", 0.6),
("5.7", "So when you watch a robot demo, ask three questions.", 0.6),
("5.8", "Is it autonomous, or is someone driving? Is the video at real speed? And how many tries did it take?", None),
("5.9", "A robot that fails one time in ten still needs someone watching.", 0.5),
],
6: [
("6.1", "So when will a robot fold your laundry at home, on its own?", None),
("6.2", "Here is my bet. It depends on two things.", 0.5),
("6.3", "One: data from real homes. Not thousands of hours. Millions. Probably collected by robots that are partly driven by people today.", None),
("6.4", "Two: reliability. The day the remote helper is no longer needed is the day it works 99 times out of 100, not 9 out of 10.", None),
("6.5", "Robots that fold some clothes, with a human on call, are already for sale. A robot that handles your whole household? Rodney Brooks has written that dexterity will still lag far behind human hands past 2036.", None),
("6.6", "My bet sits in between. A supervised robot that folds most of your laundry by the end of this decade. One that does it with nobody watching, not before the mid-2030s.", 0.6),
("6.7", "A signal to watch: the day a company stops saying remote operator in the fine print.", None),
("6.8", "The lesson is bigger than laundry. What looks easy to us is easy because evolution did the work, and nobody wrote that work down as data.", 0.6),
("6.9", "So the next time you see a robot do a backflip, don't ask how it got so good. Ask what it was never asked to do.", 0.6),
("6.10", "Which chore would you hand to a robot first? And would you let a stranger drive it while you are out? Tell me in the comments.", 0.8),
],
}

# ------------------------------------------------------------------ spoken forms
_ONES = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen".split()
_TENS = "_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()

def num(n):
    n = int(n)
    if n < 20: return _ONES[n]
    if n < 100: return _TENS[n // 10] + ("-" + _ONES[n % 10] if n % 10 else "")
    if n < 1000: return _ONES[n // 100] + " hundred" + (" " + num(n % 100) if n % 100 else "")
    if n < 1000000: return num(n // 1000) + " thousand" + (" " + num(n % 1000) if n % 1000 else "")
    if n < 10**9: return num(n // 10**6) + " million" + (" " + num(n % 10**6) if n % 10**6 else "")
    return str(n)

def year(y):
    y = int(y)
    if 2000 <= y < 2010: return "two thousand" + (" " + _ONES[y - 2000] if y > 2000 else "")
    return num(y // 100) + " " + (("oh " + _ONES[y % 100]) if 0 < y % 100 < 10 else (num(y % 100) if y % 100 else "hundred"))

YEARS = {"1988", "1997", "2017", "2024", "2026", "2025", "2021", "2019", "2010", "2036", "2024"}

SPOKEN = {
"6.6": "My bet sits in between. A supervised robot that folds most of your laundry by the end of this decade. One that does it with nobody watching, not before the mid twenty-thirties.",
"1.6": "Seeing and moving have been refined for hundreds of millions of years. Fossil eyes date back more than five hundred million years.",
"3.9": "In twenty nineteen, Open A I trained a robot hand in simulation to solve a Rubik's Cube, with training equal to roughly thirteen thousand years of experience.",
"3.7": "And there are the hands. A human hand has about seventeen thousand receptors for light touch.",
"4.3": "A token is roughly three-quarters of a word. At the average adult reading speed, two hundred and thirty-eight words a minute, reading that much nonstop would take about ninety thousand years.",
"4.4": "Now the robots. The Open X-Embodiment project pooled data from twenty-one institutions into more than a million robot trajectories, from twenty-two kinds of robot.",
"4.5": "A million sounds like a lot. But each trajectory is one short attempt at a task. The Droid dataset, collected by fifty people over twelve months, has seventy-six thousand trajectories. That adds up to about three hundred and fifty hours.",
"4.6": "Agi-Bot World, from twenty twenty-five, lists almost three thousand hours of recordings, gathered by over a hundred robots. That is a hundred and twenty-four days.",
"4.8": "A token and an hour of robot time are not the same thing. But in time, the gap is more than two hundred thousand to one.",
"4.10": "First, teleoperation. A person drives the robot through a task while it records. Stanford's Mobile Aloha team found that fifty demonstrations per task, combined with older data, could raise success rates by up to ninety percent, enough for tasks like cooking a shrimp.",
"5.3": "In October twenty twenty-five, a reporter at the Wall Street Journal tested a home humanoid called Neo, priced at twenty thousand dollars. In her test, the work was done by a remote human operator.",
"5.4": "That is not necessarily a trick. Some companies say openly that the human is part of the plan. One X's chief executive told her that without customers' data, the product cannot get better.",
"6.4": "Two: reliability. The day the remote helper is no longer needed is the day it works ninety-nine times out of a hundred, not nine out of ten.",
"2.5": "Then the trained controller is copied onto the real machine. Reports say Unitree's twenty twenty-four backflip was trained that way too.",
"0.4": "In February twenty twenty-six, a startup began shipping a laundry-folding robot for nearly eight thousand dollars. When it gets stuck, a human specialist takes over remotely, for a few seconds at a time.",
"1.1": "In nineteen eighty-eight, the roboticist Hans Moravek noticed something strange.",
}

def spoken(lid, en):
    if lid in SPOKEN: return SPOKEN[lid]
    t = en
    t = re.sub(r"\bAI\b", "A I", t)
    t = re.sub(r"\bUC\b", "U C", t)
    t = re.sub(r"\bETH\b", "E T H", t)
    t = re.sub(r"\bNVIDIA\b", "Nvidia", t)
    t = re.sub(r"\bLlama 3\b", "Llama three", t)
    t = re.sub(r"\bIBM\b", "I B M", t)
    t = re.sub(r"\biRobot\b", "eye-Robot", t)
    t = re.sub(r"\bMoravec\b", "Moravek", t)
    t = re.sub(r"\bDROID\b", "Droid", t)
    # percentages and years
    t = re.sub(r"\b(\d+) percent\b", lambda m: num(m.group(1)) + " percent", t)
    t = re.sub(r"\b(1[89]\d\d|20\d\d)\b", lambda m: year(m.group(1)), t)
    t = re.sub(r"\b(\d{1,3}(?:,\d{3})+)\b", lambda m: num(m.group(1).replace(",", "")), t)
    t = re.sub(r"\b(\d+)\b", lambda m: num(m.group(1)), t)
    return t

if __name__ == "__main__":
    n = sum(len(l[1].split()) for ls in SEGMENTS.values() for l in ls)
    print(n, "words", sum(len(ls) for ls in SEGMENTS.values()), "lines")
    for k, ls in SEGMENTS.items(): print(k, sum(len(l[1].split()) for l in ls))
    for k, ls in SEGMENTS.items():
        for lid, en, pre in ls:
            sp = spoken(lid, en)
            if re.search(r"\d", sp): print("DIGIT LEFT", lid, sp)
