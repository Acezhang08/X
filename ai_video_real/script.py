# -*- coding: utf-8 -*-
"""Narration for 'Why You Can't Tell AI Video From Real Anymore' (How AI Works series).
`en` is exactly what the viewer reads (subtitles) and what fact_check.md quotes.
`spoken()` only changes HOW numbers/acronyms are pronounced, never what is said."""
import re

# (id, english, pre-pause override seconds or None)
SEGMENTS = {
0: [
('0.1', 'Here is a quiz. Ten five-second clips are real. Ten were made by AI. Your job is to say which is which.', None),
('0.2', 'Runway, a company that builds AI video models, ran this quiz with 1,043 people. Each one watched twenty clips.', None),
('0.3', 'The average score was 57.1 percent.', 0.5),
('0.4', 'A coin flip scores 50. So the typical viewer was only slightly better than guessing.', 0.4),
('0.5', 'Only 99 people, about one in ten, did well enough that luck is an unlikely explanation.', None),
('0.52', 'Real clips were judged correctly 58 percent of the time, and fake clips 56 percent. Neither side was much better than the other.', None),
('0.53', 'Animal and building clips fell below chance, at 45 to 47 percent. Clips showing people, hands, or actions were easier, at 58 to 65 percent.', None),
('0.55', 'That is a small group. For most viewers, the honest answer to whether a clip is real is a guess.', 0.5),
('0.6', 'Keep in mind who ran the study. A company that sells these models measured how well people spot them.', 0.6),
('0.7', "Still, the result is hard to ignore. So why can't we tell anymore?", 0.5),
('0.8', 'Here is the short answer. Every checklist for spotting AI video is already out of date, and the reason is built into how these videos are made.', 0.6),
],
1: [
('1.1', 'Most guides to spotting AI video are lists of flaws. Extra fingers. Garbled signs. Faces that blink wrong.', None),
('1.2', 'Those lists are snapshots. To see why they expire, you first need to see how a video is made.', None),
('1.3', 'It starts with pure noise, like the static on an old television.', None),
('1.4', 'A diffusion model learns to remove that noise a little at a time, guided by the text prompt.', None),
('1.5', 'The training works in reverse. Take a real image, add noise until nothing is left, and teach the model to undo the damage one step at a time.', None),
('1.6', 'A 2020 paper from UC Berkeley described this approach for images, and it became influential.', None),
('1.7', 'Each step nudges the picture from static toward something that matches the prompt.', None),
('1.8', 'A video model does the same for many frames at once. The frames have to agree with each other, or the motion looks wrong.', None),
('1.9', 'So the model is not pasting together a fake. It is learning what real footage looks like, and getting better at matching it.', 0.6),
('1.10', 'Notice what that means. The model learns statistical patterns from its training data, and patterns are exactly what a checklist cannot capture.', None),
('1.11', 'That is also why the same prompt gives different results each time. Each run starts from different static, and the model settles on a different picture.', None),
],
2: [
('2.1', 'Take hands. Early image generators drew hands badly, with too many fingers or fused knuckles.', None),
('2.2', 'One reason was the training data. Hands are small in most photos, and often hidden behind objects or other hands.', None),
('2.3', 'A model can only learn from what it sees. As the data grew and the models got bigger, the hands got better.', None),
('2.4', 'Text followed the same path. Early generators produced letters that looked right from a distance and fell apart up close.', None),
('2.45', 'Fingers are a good example, because a hand has a rigid structure that people notice instantly. A model has to learn that structure from pixels alone.', None),
('2.5', 'Blinking and reflections did too. Each flaw was a gap in what the model had learned, and the gaps closed.', None),
('2.6', 'That is why a checklist of tells goes stale. The tells were never a law of physics. They were gaps in training, and gaps get filled.', 0.6),
('2.7', "So a list written this year is a guess about next year's models.", 0.6),
('2.8', 'Each new round of training removes some old tells and brings new ones. The lesson is not that the flaws are gone. It is that the list is always behind.', None),
],
3: [
('3.1', 'Now the second study. Researchers at UC Berkeley showed 376 people clips from three AI video models, along with real footage.', None),
('3.2', 'They changed how long each clip was shown, from a single frame up to eight seconds.', None),
('3.3', 'For the fake clips, watching longer helped. Accuracy rose from about 58 percent on one frame to about 75 percent at eight seconds.', None),
('3.75', 'Seedance was the easiest model for viewers to catch, and Sora the hardest.', None),
('3.4', 'For the real clips, it did not. Accuracy stayed near 60 percent, however long people watched.', 0.6),
('3.5', 'Think about what that means.', 0.6),
('3.6', 'Looking longer helped people catch the fakes. It did not help them with the real clips.', 0.5),
('3.7', 'Viewers in that study leaned on motion, and looked for movement that broke what they expected.', None),
('3.8', 'For real clips, a longer look earned no more trust than a glance.', None),
('3.9', 'So the cost of fake video is not only being fooled. The bigger risk is that real video stops being believed.', 0.6),
('3.95', 'A checklist of tells will never show that cost. Only a habit of checking will.', None),
],
4: [
('4.1', 'If eyes and checklists keep failing, what still works? Three things.', None),
('4.2', 'First, provenance. Some cameras and editing tools attach a signed record called Content Credentials, under a standard called C2PA. It says who captured or generated a file, and with which tool.', None),
('4.3', 'The weakness is that many platforms strip this record when a file is uploaded, and a screenshot removes it too. So a missing record proves nothing in either direction.', None),
('4.4', "Second, invisible watermarks. Google's SynthID hides a signal inside images, video, and audio.", None),
('4.5', 'On October 7, 2026, Google opened its SynthID Detector to anyone, in English. It also reads watermarks from partners such as OpenAI, NVIDIA, and Kakao.', None),
('4.55', "Google's tool is free to use, and it reads only the watermarks it knows. Anything without one, or with a mark from a source it does not check, comes back with no answer.", None),
('4.6', 'A match tells you a watermark is there. No match tells you nothing, because many AI clips carry no SynthID mark at all.', 0.6),
('4.7', 'Those two tools are useful, and both have holes. That is why they are not the whole answer.', 0.5),
('4.8', 'Neither one answers whether a specific clip is real. They answer narrower questions, and you have to know which question you are asking.', None),
],
5: [
('5.1', 'Third, the method that does not depend on any tool. Ask who posted the clip first.', None),
('5.2', 'A repost is not a source. Find the earliest upload you can, and see what the account posted before it.', None),
('5.25', 'Be wary of a clip that arrives with a dramatic caption and no origin. Real footage often arrives that way too, which is why the origin matters more than the look.', None),
('5.3', 'Then look for a second, independent source that reports the same event.', None),
('5.4', 'Check whether the place, the time, and the details line up with what else is known.', None),
('5.45', 'A reverse image search and a look at the original post can settle many cases in a minute.', None),
('5.5', 'None of these asks you to find a flaw in the pixels. That is the point.', 0.5),
('5.6', 'So the question is no longer whether you can tell AI video from real video. Most people cannot do it reliably, and that is not a personal failing.', None),
('5.65', 'None of these checks needs a new tool. They work the same way next year, whatever the models look like.', None),
('5.7', 'The question is what you will still trust when a real video shows up.', 0.6),
('5.8', 'Tell us in the comments. The last time you were not sure a video was AI, how did you decide?', None),
],
}

# hand-written pronunciations (spoken form only); keys are line ids
SPOKEN = {}

def num(s):
    """integer string -> English words (Kokoro reads digits badly)"""
    ones = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen".split()
    tens = "twenty thirty forty fifty sixty seventy eighty ninety".split()
    n = int(s)
    if n < 20: return ones[n]
    if n < 100: return tens[n // 10 - 2] + ("" if n % 10 == 0 else " " + ones[n % 10])
    if n < 1000: return ones[n // 100] + " hundred" + ("" if n % 100 == 0 else " " + num(str(n % 100)))
    if n < 1000000: return num(str(n // 1000)) + " thousand" + ("" if n % 1000 == 0 else " " + num(str(n % 1000)))
    return str(n)

def year(s):
    n = int(s)
    if 2000 <= n < 2010: return "two thousand " + ("" if n == 2000 else ones_(n % 10))
    if n % 100 == 0: return num(str(n // 100)) + " hundred"
    return num(str(n // 100)) + " " + (num(str(n % 100)))

def ones_(n):
    return ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"][n]

def spoken(lid, en):
    if lid in SPOKEN: return SPOKEN[lid]
    t = en
    t = re.sub(r"\bAI\b", "A I", t)
    t = re.sub(r"\bUC\b", "U C", t)
    t = re.sub(r"\bC2PA\b", "C two P A", t)
    t = re.sub(r"\bNVIDIA\b", "Nvidia", t)
    t = re.sub(r"\bSynthID\b", "Synth I D", t)
    t = re.sub(r"\bVideo\b", "Video", t)
    t = re.sub(r"\bStates\b", "States", t)
    # decimals and percentages
    t = re.sub(r"\b(\d+)\.(\d+) percent\b", lambda m: num(m.group(1)) + " point " + " ".join(num(d) for d in m.group(2)) + " percent", t)
    t = re.sub(r"\b(\d+) percent\b", lambda m: num(m.group(1)) + " percent", t)
    # dates
    t = re.sub(r"October 7, 2026", "October seventh, twenty twenty six", t)
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
