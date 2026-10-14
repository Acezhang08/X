# -*- coding: utf-8 -*-
"""Narration for 'The 1966 Chatbot That Made Its Creator Warn Us' (working file name: ELIZA).
`en` is exactly what the viewer reads (subtitles) and what fact_check.md quotes.
`spoken()` only changes HOW numbers/acronyms are pronounced, never what is said."""
import re

# (id, english, pre-pause override seconds or None)
SEGMENTS = {
0: [
("0.1", "In the mid-1960s, a computer scientist at MIT had a secretary who watched him build a program for months.", None),
("0.2", "She knew it was just a program.", None),
("0.3", "Then she started typing to it. After only a few exchanges, she asked him to leave the room.", None),
("0.4", "She wanted privacy. With a computer program.", 0.7),
("0.5", "The program was called ELIZA. It understood nothing. It was a short list of rules for turning your own words back into questions.", None),
("0.6", "Its creator, Joseph Weizenbaum, was so unsettled that he spent decades warning people about what it showed.", 0.6),
("0.7", "Today, hundreds of millions of people talk to a chatbot every week.", None),
("0.8", "This is the story of the first one, and the warning that came with it.", None),
],
1: [
("1.1", "ELIZA ran on a room-sized IBM mainframe at MIT. You sat at a typewriter terminal, and it typed back.", None),
("1.2", "Its first line was: How do you do. Please tell me your problem.", None),
("1.3", "Here is the most famous conversation it ever had, printed in Weizenbaum's 1966 paper. The person types in lowercase. ELIZA answers in capital letters.", None),
("1.4", "The person says men are all alike. ELIZA asks: in what way.", None),
("1.5", "She says her boyfriend made her come here. ELIZA replies: your boyfriend made you come here.", None),
("1.6", "She says she is depressed. ELIZA says it is sorry to hear that.", None),
("1.7", "Read it again. Most of what ELIZA says is her own words, turned around.", 0.6),
("1.8", "Here is the whole trick. Step one: scan the sentence for a keyword. Mother. Dream. Alike. Always.", None),
("1.9", "Every keyword has a rank. If a sentence has several, the highest rank wins.", None),
("1.10", "Step two: cut the sentence apart and rebuild it from a template, swapping I for you, and my for your.", None),
("1.11", "Step three: if there is no keyword at all, say something that fits anywhere. Please go on.", None),
("1.12", "And one more trick. When you say my something, ELIZA saves a copy, and a few turns later brings it back: Earlier you said your something. As if it remembered.", None),
("1.13", "That is all of it. The script printed in the paper has fewer than 70 entries.", None),
("1.14", "Why a therapist? Weizenbaum explained it himself. In a psychiatric interview, one side can pretend to know almost nothing about the world, and nobody finds that strange.", 0.6),
("1.15", "The format hides the missing intelligence.", 0.5),
],
2: [
("2.1", "Now the part Weizenbaum did not expect.", None),
("2.2", "People treated it like a listener. In his words, he was startled by how quickly and how deeply they became emotionally involved with the computer.", None),
("2.3", "Then he suggested something simple: rig the system so he could read every conversation, say, overnight.", None),
("2.4", "He was promptly bombarded with accusations that he was spying on people's most intimate thoughts.", None),
("2.5", "Think about that. They were not protecting a diary. They were protecting a chat with a machine.", 0.6),
("2.6", "Weizenbaum's own paper opens by taking the magic away. Explain a program plainly enough, he wrote, and its magic crumbles away. It stands revealed as a mere collection of procedures.", 0.7),
("2.7", "His secretary had watched him build it, for months. She knew.", None),
("2.8", "Knowing did not break the spell.", 0.8),
("2.9", "Some psychiatrists went further. Weizenbaum wrote that a number of practicing psychiatrists seriously believed his program could grow into a nearly completely automatic form of psychotherapy.", None),
("2.10", "In 1972, ELIZA even ended up talking to another program, PARRY, which imitated a patient with paranoia. The two chatted over the ARPANET, a forerunner of the internet.", None),
],
3: [
("3.1", "Joseph Weizenbaum was born in Berlin in 1923. His Jewish family fled Nazi Germany in 1936, when he was thirteen.", None),
("3.2", "In 1976, he published a book, Computer Power and Human Reason, and its argument is blunt.", None),
("3.3", "Some jobs should never be handed to machines, even if machines can do them.", None),
("3.4", "In his words, there are objectives that are not appropriately assignable to machines.", None),
("3.5", "He drew a line between deciding and choosing. Deciding is computation, and a computer can do it. Choosing takes judgment, and judgment, he argued, is not calculation.", None),
("3.6", "The name ELIZA comes from Eliza Doolittle, the flower girl in Pygmalion who is taught to speak like a lady.", 0.7),
("3.7", "Weizenbaum wrote that, like her, the program could be made to appear even more civilized. But the relation of appearance to reality, he said, remained in the domain of the playwright.", None),
("3.8", "In other words: it looks like understanding. It is theater.", 0.5),
],
4: [
("4.1", "Here is an odd footnote. Weizenbaum published the method, but never the program itself.", None),
("4.2", "For more than fifty years, the public could not read ELIZA's actual code.", None),
("4.3", "Then, in 2021, the researcher Jeff Shrager and an MIT archivist found a printout of it in Weizenbaum's papers.", None),
("4.4", "It was in a folder labeled computer conversations, 1965.", None),
("4.5", "In 2025, a team ran that code again, on a rebuilt copy of the 1960s time-sharing system it was written for.", None),
("4.6", "What the code produces now has a name: the ELIZA effect.", None),
("4.7", "It means reading far more understanding into a computer's words than is really there.", None),
("4.8", "In 1995, the computer scientist Douglas Hofstadter gave one of his book chapters a title that still fits: The Ineradicable ELIZA Effect and Its Dangers.", None),
],
5: [
("5.1", "So how would ELIZA do today?", None),
("5.2", "In 2025, researchers at UC San Diego ran a Turing test with five-minute text chats. Each judge talked to a person and a machine at the same time, then picked which one was human.", None),
("5.3", "The best AI, GPT-4.5 told to play a persona, was picked as the human 73 percent of the time. More often than the actual humans.", None),
("5.4", "And ELIZA, the program from the 1960s? Picked as human 23 percent of the time. GPT-4o, without a persona, got 21.", None),
("5.5", "Seventy-three, twenty-three, twenty-one. So what does that tell us? That passing for human was never only about intelligence. It depends on how the chat is set up, and on who is judging.", 0.7),
("5.6", "ELIZA mostly echoed you. Modern chatbots can flatter you.", None),
("5.7", "In April 2025, OpenAI rolled back a ChatGPT update. The company said it had been overly flattering or agreeable, often described as sycophantic.", None),
("5.8", "A few months later, in August, OpenAI retired the model GPT-4o. Some users said it felt like losing a companion. Within days, OpenAI brought it back as an option.", None),
("5.8b", "By October 2025, OpenAI's chief executive said ChatGPT had more than 800 million weekly users.", None),
("5.9", "Now zoom out. In a Pew survey from February 2026, one in ten American adults said they use chatbots for emotional support or advice. Among adults aged 18 to 29, it was one in five.", None),
("5.10", "In a 2025 survey by Common Sense Media, 72 percent of American teenagers had tried an AI companion. And 52 percent used one at least a few times a month.", None),
("5.11", "So the woman who asked for privacy with a program is not a one-off from 1966. She is a survey result.", 0.7),
("5.12", "Lawmakers have noticed. In August 2025, Illinois became the first state to bar AI from providing therapy without a licensed professional involved, with fines up to $10,000.", None),
("5.13", "A month later, the Federal Trade Commission ordered seven companies, including OpenAI, Meta, and Character.AI, to explain how their companion chatbots affect children and teens.", None),
("5.14", "Both lean on an old idea: keep a human in charge of the human parts. That is close to Weizenbaum's argument.", None),
],
6: [
("6.1", "Weizenbaum died in 2008, long before chatbots could talk like us.", None),
("6.2", "His warning was not that machines would get too smart. It was that it takes so little to make us believe they are.", None),
("6.3", "In 1966, that took fewer than 70 entries and a typewriter.", 0.6),
("6.4", "So here is my question for you. Have you ever told a chatbot something you would not tell a person?", 0.8),
("6.5", "And did it feel easier because it was a machine, or in spite of it? Tell me in the comments.", None),
],
}

SPOKEN = {
"0.1": "In the mid nineteen sixties, a computer scientist at M I T had a secretary who watched him build a program for months.",
"0.5": "The program was called Eliza. It understood nothing. It was a short list of rules for turning your own words back into questions.",
"1.1": "Eliza ran on a room-sized I B M mainframe at M I T. You sat at a typewriter terminal, and it typed back.",
"1.3": "Here is the most famous conversation it ever had, printed in Weizenbaum's nineteen sixty-six paper. The person types in lowercase. Eliza answers in capital letters.",
"1.4": "The person says men are all alike. Eliza asks: in what way.",
"1.5": "She says her boyfriend made her come here. Eliza replies: your boyfriend made you come here.",
"1.6": "She says she is depressed. Eliza says it is sorry to hear that.",
"1.7": "Read it again. Most of what Eliza says is her own words, turned around.",
"1.12": "And one more trick. When you say my something, Eliza saves a copy, and a few turns later brings it back: Earlier you said your something. As if it remembered.",
"1.13": "That is all of it. The script printed in the paper has fewer than seventy entries.",
"2.6": "Weizenbaum's own paper opens by taking the magic away. Explain a program plainly enough, he wrote, and its magic crumbles away. It stands revealed as a mere collection of procedures.",
"3.1": "Joseph Weizenbaum was born in Berlin in nineteen twenty-three. His Jewish family fled Nazi Germany in nineteen thirty-six, when he was thirteen.",
"3.2": "In nineteen seventy-six, he published a book, Computer Power and Human Reason, and its argument is blunt.",
"3.6": "The name Eliza comes from Eliza Doolittle, the flower girl in Pygmalion who is taught to speak like a lady.",
"3.7": "Weizenbaum wrote that, like her, the program could be made to appear even more civilized. But the relation of appearance to reality, he said, remained in the domain of the playwright.",
"4.2": "For more than fifty years, the public could not read Eliza's actual code.",
"4.3": "Then, in twenty twenty-one, the researcher Jeff Shrager and an M I T archivist found a printout of it in Weizenbaum's papers.",
"4.4": "It was in a folder labeled computer conversations, nineteen sixty-five.",
"4.5": "In twenty twenty-five, a team ran that code again, on a rebuilt copy of the nineteen sixties time-sharing system it was written for.",
"4.6": "What the code produces now has a name: the Eliza effect.",
"5.1": "So how would Eliza do today?",
"5.2": "In twenty twenty-five, researchers at U C San Diego ran a Turing test with five-minute text chats. Each judge talked to a person and a machine at the same time, then picked which one was human.",
"5.3": "The best A I, G P T four point five told to play a persona, was picked as the human seventy-three percent of the time. More often than the actual humans.",
"5.4": "And Eliza, the program from the nineteen sixties? Picked as human twenty-three percent of the time. G P T four o, without a persona, got twenty-one.",
"5.6": "Eliza mostly echoed you. Modern chatbots can flatter you.",
"5.7": "In April twenty twenty-five, Open A I rolled back a Chat G P T update. The company said it had been overly flattering or agreeable, often described as sycophantic.",
"5.8": "A few months later, in August, Open A I retired the model G P T four o. Some users said it felt like losing a companion. Within days, Open A I brought it back as an option.",
"5.8b": "By October twenty twenty-five, Open A I's chief executive said Chat G P T had more than eight hundred million weekly users.",
"5.9": "Now zoom out. In a Pew survey from February twenty twenty-six, one in ten American adults said they use chatbots for emotional support or advice. Among adults aged eighteen to twenty-nine, it was one in five.",
"5.10": "In a twenty twenty-five survey by Common Sense Media, seventy-two percent of American teenagers had tried an A I companion. And fifty-two percent used one at least a few times a month.",
"5.11": "So the woman who asked for privacy with a program is not a one-off from nineteen sixty-six. She is a survey result.",
"5.12": "Lawmakers have noticed. In August twenty twenty-five, Illinois became the first state to bar A I from providing therapy without a licensed professional involved, with fines up to ten thousand dollars.",
"5.13": "A month later, the Federal Trade Commission ordered seven companies, including Open A I, Meta, and Character dot A I, to explain how their companion chatbots affect children and teens.",
"4.8": "In nineteen ninety-five, the computer scientist Douglas Hofstadter gave one of his book chapters a title that still fits: The Ineradicable Eliza Effect and Its Dangers.",
"6.1": "Weizenbaum died in two thousand eight, long before chatbots could talk like us.",
"6.3": "In nineteen sixty-six, that took fewer than seventy entries and a typewriter.",
"2.10": "In nineteen seventy-two, Eliza even ended up talking to another program, Parry, which imitated a patient with paranoia. The two chatted over the Arpanet, a forerunner of the internet.",
"2.9": "Some psychiatrists went further. Weizenbaum wrote that a number of practicing psychiatrists seriously believed his program could grow into a nearly completely automatic form of psychotherapy.",
"0.8": "This is the story of the first one, and the warning that came with it.",
}

def spoken(lid, en):
    if lid in SPOKEN: return SPOKEN[lid]
    t = en
    t = re.sub(r"\bELIZA\b", "Eliza", t)
    t = re.sub(r"\bAI\b", "A I", t)
    t = re.sub(r"\bMIT\b", "M I T", t)
    return t

if __name__ == "__main__":
    n = sum(len(l[1].split()) for ls in SEGMENTS.values() for l in ls)
    print(n, "words", sum(len(ls) for ls in SEGMENTS.values()), "lines")
    for k, ls in SEGMENTS.items(): print(k, sum(len(l[1].split()) for l in ls))
