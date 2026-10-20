# fact_check.md — 核查表（"Why You Can't Tell AI Video From Real Anymore"）

**读者须知**
- 核查方式：联网搜索 + 搜索摘要核实。容器无法直接打开 runway.com、arxiv.org、techradar.com 等页面（网络策略拒绝），所以**大部分结论基于搜索结果里的原始页面摘要**，不是我逐字读过原文。标 "二手" 的说法至少有一个可信媒体或摘要佐证，但没有逐字核对原文；发布前建议对着原文再过一遍，尤其是 3.3 的两个百分比（原文 PDF 未直接打开，数字与你提供的 57.7% / 74.6% 一致）。
- 结论标签：**确认**（有原始来源或摘要与旁白一致）、**二手**（只有媒体或摘要佐证）、**改写**（原说法过头，已改）、**观点**（判断/修辞/方法建议，不是可核对的事实）。
- 本片中凡提到的 AI 视频模型和公司只用来说明机制或研究对象，不推荐任何生成工具。
- 你提供的 Google Trends、YouTube 搜索补全等数据不进入旁白，仅记在 `publish.md` 的备注里，未重复核查。

## 核查表

| 句号 | 旁白（英文，定稿） | 说法 | 来源（名称 + 链接 + 日期） | 结论 |
|---|---|---|---|---|
| 0.1 | Here is a quiz. Ten five-second clips are real. Ten were made by AI. | 研究设计：每人 20 段，10 真 10 假 | Runway, "The Turing Reel"，runway.com/research/theturingreel（搜索摘要提到方法页；页面未直接打开） | 确认 |
| 0.2 | Runway, a company that builds AI video models, ran this quiz with 1,043 people. Each one watched twenty clips. | 1,043 人；每人 20 段 | 同上（方法页写 1,043 人；首页写 1,000 人，以方法页为准） | 确认 |
| 0.3 | The average score was 57.1 percent. | 整体正确率 57.1% | 同上；TechRadar 报道（techradar.com，搜索摘要） | 确认 |
| 0.4 | A coin flip scores 50. So the typical viewer was only slightly better than guessing. | 抛硬币期望 50%；57.1 "略好于瞎猜" | 数学常识 | 确认（"略好于瞎猜"是对 57.1% 的描述，属观点） |
| 0.5 | Only 99 people, about one in ten, did well enough that luck is an unlikely explanation. | 99 人（9.5%）达到统计显著（≥15/20） | 同上（搜索摘要：99 of 1,043 = 9.5%，显著标准为至少 15 题正确） | 确认 |
| 0.52 | Real clips were judged correctly 58 percent of the time, and fake clips 56 percent. Neither side was much better than the other. | 真片正确 58.0%，假片 56.1% | 同上（搜索摘要） | 确认 |
| 0.53 | Animal and building clips fell below chance, at 45 to 47 percent. Clips showing people, hands, or actions were easier, at 58 to 65 percent. | 动物/建筑 45–47%；人/手/动作 58–65% | 同上（搜索摘要） | 确认 |
| 0.55 | That is a small group. For most viewers, the honest answer to whether a clip is real is a guess. | "大多数人在猜" | 由 0.5 的 9.5% 推出 | 观点 |
| 0.6 | Keep in mind who ran the study. A company that sells these models measured how well people spot them. | 研究方是生成模型公司 | Runway 官方研究页（同上）；Runway 是生成视频公司（公司自述） | 确认 |
| 0.7 | Still, the result is hard to ignore. So why can't we tell anymore? | 修辞过渡 | — | 观点（已删去原稿"多数人以为自己更强"的未经证实说法） |
| 0.8 | Here is the short answer. Every checklist for spotting AI video is already out of date, and the reason is built into how these videos are made. | "清单会过期"是机制判断 | 见 1.x、2.x 的机制与来源 | 观点 |
| 1.1 | Most guides to spotting AI video are lists of flaws. | 常见指南以破绽清单为主 | 你提供的搜索结果观察（TODAY / WSJ / Linus Tech Tips 等标题） | 观点（描述性） |
| 1.2 | Those lists are snapshots. To see why they expire, you first need to see how a video is made. | 叙述过渡 | — | 观点 |
| 1.3 | It starts with pure noise, like the static on an old television. | 扩散模型从纯噪声开始 | Ho, Jain, Abbeel，"Denoising Diffusion Probabilistic Models"，arXiv:2006.11239，2020-06-19（搜索摘要） | 确认 |
| 1.4 | A diffusion model learns to remove that noise a little at a time, guided by the text prompt. | 逐步去噪；文本条件 | 同上（去噪过程）；"文本引导"是文生视频的常见做法，未逐条核原文 | 二手（机制概述） |
| 1.5 | The training works in reverse. Take a real image, add noise until nothing is left, and teach the model to undo the damage one step at a time. | 训练 = 加噪后学习逆过程 | arXiv:2006.11239（搜索摘要：前向加噪 + 学习反向去噪） | 确认 |
| 1.6 | A 2020 paper from UC Berkeley described this approach for images, and it became influential. | 2020 年，UC Berkeley；图像 | arXiv:2006.11239，作者 Jonathan Ho、Ajay Jain、Pieter Abbeel，UC Berkeley，2020 年 6 月提交（搜索摘要） | 确认（"influential" 为观点） |
| 1.7 | Each step nudges the picture from static toward something that matches the prompt. | 每步向提示词靠拢 | 同 1.4 | 二手（机制概述） |
| 1.8 | A video model does the same for many frames at once. The frames have to agree with each other, or the motion looks wrong. | 视频模型同时去噪多帧，需保持帧间一致 | Ho et al.，"Video Diffusion Models"，arXiv:2204.03458，NeurIPS 2022（搜索摘要：联合训练、时间连贯是核心目标） | 确认（"motion looks wrong" 是通俗表述） |
| 1.9 | So the model is not pasting together a fake. It is learning what real footage looks like, and getting better at matching it. | 模型学习数据分布 | 扩散模型的基本目标（arXiv:2006.11239） | 观点（概括性） |
| 1.10 | Notice what that means. The model learns statistical patterns from its training data, and patterns are exactly what a checklist cannot capture. | 学统计规律；清单抓不住规律 | 机制概括 | 观点 |
| 1.11 | That is also why the same prompt gives different results each time. Each run starts from different static, and the model settles on a different picture. | 初始噪声随机 → 结果不同 | 扩散模型采样的基本机制（arXiv:2006.11239） | 确认（机制） |
| 2.1 | Take hands. Early image generators drew hands badly, with too many fingers or fused knuckles. | 早期图像模型画手差，手指多/少，指节粘连 | PetaPixel，"Why AI Image Generators Can't Get Hands Right"，2023-03-02，petapixel.com/2023/03/02/why-ai-image-generators-cant-get-hands-right/（搜索摘要） | 确认 |
| 2.2 | One reason was the training data. Hands are small in most photos, and often hidden behind objects or other hands. | 训练图中手小、常被遮挡 | 同上（搜索摘要：Stability AI 发言人称手在训练图里出现得少、尺寸小） | 确认 |
| 2.3 | A model can only learn from what it sees. As the data grew and the models got bigger, the hands got better. | 数据与规模增大，手变好 | 行业普遍观察，未找到量化来源 | 观点（趋势判断） |
| 2.4 | Text followed the same path. Early generators produced letters that looked right from a distance and fell apart up close. | 早期模型文字：远看对、近看乱 | 常见观察，未找到专门来源 | 观点（未核实来源，保留为描述） |
| 2.45 | Fingers are a good example, because a hand has a rigid structure that people notice instantly. A model has to learn that structure from pixels alone. | 手的结构敏感 | 解释性观点 | 观点 |
| 2.5 | Blinking and reflections did too. Each flaw was a gap in what the model had learned, and the gaps closed. | 眨眼、反光同样改善 | 未找到专门来源 | 观点（未核实，建议发布前确认或删去） |
| 2.6 | That is why a checklist of tells goes stale. The tells were never a law of physics. They were gaps in training, and gaps get filled. | 破绽是训练缺口 | 由 2.1–2.2 的机制推出 | 观点 |
| 2.7 | So a list written this year is a guess about next year's models. | 清单是对未来的猜测 | 观点 | 观点 |
| 2.8 | Each new round of training removes some old tells and brings new ones. The lesson is not that the flaws are gone. It is that the list is always behind. | 每一轮训练去掉旧破绽、带来新破绽 | 观点（未找到专门来源） | 观点 |
| 3.1 | Now the second study. Researchers at UC Berkeley showed 376 people clips from three AI video models, along with real footage. | 376 人；三个 AI 视频模型（Veo 3.1、Sora 2、Seedance Pro 1）；含真实片段 | Davodi, Barrington, Farid, Cooper，"Perceptual Judgments of Video Authenticity…"，farid.berkeley.edu/downloads/publications/cvprw26a.pdf（用户提供；搜索摘要确认 376 人与模型名单） | 确认 |
| 3.2 | They changed how long each clip was shown, from a single frame up to eight seconds. | 观看时长：单帧到 8 秒 | 同上 | 确认 |
| 3.3 | For the fake clips, watching longer helped. Accuracy rose from about 58 percent on one frame to about 75 percent at eight seconds. | 假片：单帧 57.7% → 8 秒 74.6% | 同上（搜索摘要："from about 58% to 75%"；与你提供的 57.7% / 74.6% 一致；PDF 原文未直接打开） | 确认（数字建议对着 PDF 再核） |
| 3.4 | For the real clips, it did not. Accuracy stayed near 60 percent, however long people watched. | 真片准确率 ≈60%，不随时长上升 | 同上（搜索摘要：真视频准确率约 60%，不随时长上升） | 确认 |
| 3.5 | Think about what that means. | 过渡 | — | 观点 |
| 3.6 | Looking longer helped people catch the fakes. It did not help them with the real clips. | 时长对假片有帮助，对真片没有 | 同上（搜索摘要：证据积累不对称） | 确认（**改写**：原稿"多看只会更怀疑"的说法没有直接证据，论文测的是准确率，没有直接测"怀疑度"，已改为有数据支撑的说法） |
| 3.7 | Viewers in that study leaned on motion, and looked for movement that broke what they expected. | 观众依赖运动，寻找违反预期的运动 | 同上（搜索摘要：参与者主要依靠运动线索；作者建议找"违反"而非"真实"的信号） | 确认 |
| 3.75 | Seedance was the easiest model for viewers to catch, and Sora the hardest. | 三个模型中 Seedance 最易识别、Sora 最难 | Davodi et al.（同 3.1）；搜索摘要：Seedance 最易、Sora 最难，原文 PDF 未直接核对 | 二手 |
| 3.8 | For real clips, a longer look earned no more trust than a glance. | 真片：多看并不带来更多信任 | 同上（真片准确率平稳；"信任"是对准确率的解释） | 二手（解释性表述，已与 3.4 数据对齐） |
| 3.9 | So the cost of fake video is not only being fooled. The bigger risk is that real video stops being believed. | 假视频的代价还包括真视频不被相信 | Runway 的 9.5% 与 Berkeley 的真片准确率平稳共同支持"可信度受损"这一推论 | 观点（推论，不是测得的结果） |
| 3.95 | A checklist of tells will never show that cost. Only a habit of checking will. | 清单看不到这种代价 | 观点 | 观点 |
| 4.1 | If eyes and checklists keep failing, what still works? Three things. | 结构过渡 | — | 观点 |
| 4.2 | First, provenance. Some cameras and editing tools attach a signed record called Content Credentials, under a standard called C2PA. It says who captured or generated a file, and with which tool. | C2PA / Content Credentials：签名记录，写明生成或拍摄方与工具 | C2PA 标准；magnetforensics.com/blog/c2pa-and-media-authentication-what-you-need-to-know/（搜索摘要，二手）；softwareseni.com（二手）。未打开 c2pa.org 原文 | 二手 |
| 4.3 | The weakness is that many platforms strip this record when a file is uploaded, and a screenshot removes it too. So a missing record proves nothing in either direction. | 上传时平台常去掉元数据；截图会丢失 | softwareseni.com（"Durable Content Credentials"，二手，多家摘要一致）。旁白不点名平台 | 二手（多来源一致，未核原文；"missing record proves nothing" 是逻辑推断） |
| 4.4 | Second, invisible watermarks. Google's SynthID hides a signal inside images, video, and audio. | SynthID 隐形水印，覆盖图片、视频、音频 | blog.google/technology/ai/google-synthid-ai-content-detector/（搜索摘要，Google 官方博客）；多家媒体 | 确认 |
| 4.5 | On October 7, 2026, Google opened its SynthID Detector to anyone, in English. It also reads watermarks from partners such as OpenAI, NVIDIA, and Kakao. | 2026-10-07 向所有人开放；英文；合作方 OpenAI、NVIDIA、Kakao | Google 官方博客（搜索摘要确认全球、英文、合作方名单）；PetaPixel，2026-10-08，petapixel.com/2026/10/08/googles-synthid-ai-detector-is-now-freely-available-to-everyone/。注：登录方式等细节只有单一媒体，旁白未采用 | 确认（日期取自媒体报道，官方博客页面未显示日期） |
| 4.55 | Google's tool is free to use, and it reads only the watermarks it knows. Anything without one, or with a mark from a source it does not check, comes back with no answer. | 免费；只读它能识别的水印 | 媒体报道（eweek、Notebookcheck 等，搜索摘要）：只检测 SynthID 水印，不检测其他水印 | 二手 |
| 4.6 | A match tells you a watermark is there. No match tells you nothing, because many AI clips carry no SynthID mark at all. | 命中 = 有水印；未命中 ≠ 真片 | 媒体报道：负结果不能证明真实；许多 AI 内容不带 SynthID（搜索摘要） | 确认（"many" 为审慎表述） |
| 4.7 | Those two tools are useful, and both have holes. That is why they are not the whole answer. | 两种工具都有漏洞 | 4.2、4.6 的综合 | 观点 |
| 4.8 | Neither one answers whether a specific clip is real. They answer narrower questions, and you have to know which question you are asking. | 工具回答的是窄问题 | 观点 | 观点 |
| 5.1 | Third, the method that does not depend on any tool. Ask who posted the clip first. | 方法：先问最早发布者 | 核查方法建议 | 观点 |
| 5.2 | A repost is not a source. Find the earliest upload you can, and see what the account posted before it. | 转发不是来源；看账号历史 | 同上 | 观点 |
| 5.25 | Be wary of a clip that arrives with a dramatic caption and no origin. Real footage often arrives that way too, which is why the origin matters more than the look. | 无来源、耸动标题；真片也常如此，所以来源比外观重要 | 同上（方法建议） | 观点 |
| 5.3 | Then look for a second, independent source that reports the same event. | 找独立第二来源 | 同上 | 观点 |
| 5.4 | Check whether the place, the time, and the details line up with what else is known. | 对照地点、时间、细节 | 同上 | 观点 |
| 5.45 | A reverse image search and a look at the original post can settle many cases in a minute. | 反向搜图；看原帖 | 方法建议（"many cases in a minute" 为估计） | 观点 |
| 5.5 | None of these asks you to find a flaw in the pixels. That is the point. | 方法不依赖像素破绽 | 逻辑 | 观点 |
| 5.6 | So the question is no longer whether you can tell AI video from real video. Most people cannot do it reliably, and that is not a personal failing. | 多数人不能稳定分辨 | Runway：仅 99/1,043（9.5%）显著高于随机，即 90% 以上人群未达到显著水平（搜索摘要） | 确认 |
| 5.65 | None of these checks needs a new tool. They work the same way next year, whatever the models look like. | 方法不随模型过时 | 观点 | 观点 |
| 5.7 | The question is what you will still trust when a real video shows up. | 结尾问题 | — | 观点 |
| 5.8 | Tell us in the comments. The last time you were not sure a video was AI, how did you decide? | 评论引导 | — | 观点 |

## 统计

- 旁白共 62 句（表内逐句列出，编号与 `script.py` 一致）。结论分布：**确认 25 句**、**二手 7 句**、**观点 30 句**（观点句的结论列以"观点"开头，其中部分带有"确认（…）"说明，已在表内注明）。
- **改写 2 处**：3.6 "多看只会更怀疑"改为"多看帮助识别假片，不帮助识别真片"（论文测的是准确率，没有直接测怀疑度）；4.6 "大多数 AI 内容没有 SynthID"改为"许多 AI 内容不带 SynthID"（缺占比数据）。
- **删除或改写 5 处**：0.7 "多数人以为自己更强"（无来源，删）；1.9/1.10 "模型不保存真实画面库"（过于绝对，删）；3.8 原稿"只有怀疑在增长"（论文未如此表述，改）；4.4 "设计上能抵抗部分编辑"（未核原文，删）；画面上 "LEARNS PATTERNS, NOT A COPY" 改为 "NOT A CHECKLIST"（同理）。
- **需要你发布前处理的**：2.4、2.5、2.8 的来源未找到（已标为观点，建议确认或删去）；3.3 的两个百分比建议对照 PDF 原文再核一次；4.3 的平台说法是多来源一致的二手说法。
