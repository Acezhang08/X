# publish.md — Humanoid Robots Can Do Backflips. Why Can't They Fold Laundry?

频道系列：The Future of AI（第 2 条，继电力天花板之后）。成片 10:08，1920×1080 / 30fps / H.264 + AAC，旁白 Kokoro am_michael，无背景音乐。

## 选题依据（10/17 用 Chrome 查的，由人工提供，本次未再查）
- Google Trends（美国、过去 12 个月、YouTube 搜索）：humanoid robot 约是 how ai works 的 4.6 倍，是"AI 的未来"系列里搜索量最大、又不混词的；2025 年 8 月世界人形机器人运动会时有一次尖峰。
- YouTube 搜索补全：humanoid robot / humanoid robots 2026 / humanoid robots 2025 / humanoid robot for sale / humanoid robot games / humanoid robot fight。
- 前排几乎全是新闻和集锦，没有讲原理的：news.com.au 运动会翻车集锦 116 万（1 个月前，4 分钟）、Financial Times 10 万（4 个月前）、CNET 5.7 万（10 个月前）、RoboFrontier 3.4 万。
- 冲突：机器人能翻跟头、能打拳，却做不好一个小孩都会的家务。

## 标题（3 个，做 A/B 测试）
1. **Humanoid Robots Can Do Backflips. Why Can't They Fold Laundry?**　（主推；含搜索原话 humanoid robots；第一分钟兑现：2017 / 2024 的后空翻 vs 2026 年还要远程真人兜底的叠衣机器人）
2. **Humanoid Robots Do Backflips, but Fold Shirts With a Human on Call**　（片中 0:16–0:30 有出处：一家创业公司的叠衣机器人卡住时由远程专员接手 5–10 秒）
3. **Humanoid Robots Backflip Easily. Laundry Is the Hard Part**　（对应 2:00–3:20 的"反转"）

没有用 Explained / Overview / Evolution 一类词；标题里没有数字，避免和片中核实过的数字不一致。

## 缩略图（3 张，1280×720 PNG，蓝图画风）
- `thumbnail_A.png`：**FLIP ✓ | FOLD ✗** —— 左边一个通用线稿机器人后空翻 + 青色对勾，右边一件皱成一团的衬衫 + 红叉；2 个词。
- `thumbnail_B.png`：**BACKFLIP ✓ / LAUNDRY ✗** —— 纯字，上下两行大字 + 对勾/红叉；2 个词，手机小图最易读。
- `thumbnail_C.png`：**FOLD THIS?** —— 机器人双臂伸向一件皱衬衫，琥珀色大问号；2 个词。
建议先测 A 和 B（A 有画面焦点，B 是纯字）。三张都只有一个矛盾，不画任何品牌机器人。

## 描述（直接粘贴；不含任何链接）
Humanoid robots can do backflips. So why can't they fold a shirt? The answer was written down in 1988, and it changes how you read every robot demo.

In this video: Moravec's paradox, why a backflip is a "closed-book exam" for a robot, why cloth is a nightmare to simulate, the huge gap between the data chatbots learn from and the data robots have, and why many demo videos involve a human driving the robot. We finish with a reasoned bet on when a robot might fold your laundry at home, and what two conditions it depends on.

Chapters
0:00 A backflip and a shirt
0:46 Moravec's paradox: what is easy is hard
1:58 Why the backflip is the easy part
3:18 Why laundry is so hard for robots
5:08 The data gap: 90,000 years vs 124 days
7:20 How to read a robot demo
8:38 When will a robot fold your laundry?

Sources (names only; full links and a sentence-by-sentence check are in our fact-check document): Hans Moravec, "Mind Children" (1988); IBM / History.com on Deep Blue (1997); Rudin et al., "Learning to Walk in Minutes" (ETH Zurich + NVIDIA, 2021); OpenAI, "Solving Rubik's Cube with a Robot Hand" (2019); Maitin-Shepard et al., towel folding (UC Berkeley, ICRA 2010); Kadi & Terzic, cloth manipulation survey (2023); SoftGym benchmark (2020); Meta, "The Llama 3 Herd of Models" (2024); OpenAI Help Center on tokens; Brysbaert, "How many words do we read per minute?" (2019); Open X-Embodiment Collaboration (2023); DROID dataset (2024); AgiBot World (2025); Mobile ALOHA, Stanford (2024); Figure AI, Project Go-Big; Bloomberg (14 Oct 2024) on the Tesla We, Robot event; Wall Street Journal test of the 1X Neo (Oct 2025), as reported by Road to VR and DroneXL; eWeek and Interesting Engineering on Weave Robotics' Isaac 0 (Feb 2026); Rodney Brooks, "Why Today's Humanoids Won't Learn Dexterity" (2025) and his predictions; Unitree H1 backflip coverage (New Atlas, SCMP, Interesting Engineering, Mar 2024); Boston Dynamics Atlas backflip coverage (Engadget, Fortune, Nov 2017).

Note: the arithmetic in the video (90,000 years of reading, 124 days, 200,000 to 1) is ours, built from the sources above. The timeline at the end ("our bet") is an opinion.

#humanoidrobots #robotics #AI

## 播放列表
The Future of AI

## 置顶评论（发布后第一时间自己发出并置顶）
Which chore would you hand to a robot first? And would you let a stranger drive it while you are out? (Honest answers welcome. I'll read the replies and pin the best ones.)

## AI 标注
**不勾**。全动画讲解，AI 只用在写稿和配音（Kokoro 是文字转语音，不是合成真人的声音）。

## 发布前清单（给人看的）
1. 上传 `humanoid_robots.mp4`；2. 上传 `subtitles_en.srt`（画面已烧录字幕，SRT 用于 YouTube 的 CC 轨道）；3. 缩略图 A/B/C 做标题+缩略图测试；4. 描述里的章节（已按 timeline.json 实际时间）；5. 播放列表 The Future of AI；6. 发布后发置顶评论；7. 建议先听一遍成片（我无法听音，只做了数值检查），重点听数字多的第 5 段（5:08–7:20）；8. 如要更稳，在有网的机器上对一遍 fact_check.md 里标"部分核实"的条目（OpenAI 的 13,000 年、Brooks 的 2036、Figure Go-Big 的日期）。
