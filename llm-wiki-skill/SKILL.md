---
name: llm-wiki
description: 用 Codex 直接维护客制化 LLM Wiki / Markdown 知识库。Use when the user wants Codex to ingest sources, query with citations, lint, analyze knowledge graph, manage review/deep-research queues, or emulate nashsu/llm_wiki without an app, API key, or local model server.
---

# LLM Wiki Skill

## Canonical Chinese Technical Writing Gate

For any generated Chinese wiki page, query answer, clipping distillation, source summary, synthesis, comparison, or Obsidian-ready note, also use [`chinese-technical-writing`](../chinese-technical-writing/SKILL.md). Keep this skill's wiki structure and citation rules, but do not leave avoidable English phrase islands in Chinese prose.

## Canonical Platform Delivery Gate

Use [`research-doc-workflow`](../research-doc-workflow/SKILL.md) whenever a wiki source, meeting note, paper card, deep dive, or review may be delivered to Feishu/Lark, Notion, or Obsidian. For Obsidian/vault writes, also use [`obsidian-doc-workflow`](../obsidian-doc-workflow/SKILL.md) for format and verification; this skill owns the Obsidian/Markdown knowledge model and must not force an Obsidian request through Feishu first.

## Canonical Paper Card Gate

For any paper card / 论文卡片 work, also use [`paper-card-delivery`](../paper-card-delivery/SKILL.md). That skill is the canonical source for official-source verification, fixed format, figure/caption requirements, sorting, and validation. Keep this skill's wiki-specific placement rules, but do not finalize paper cards from this skill alone.

## Canonical Paper Deep Dive Gate

For any single-paper deep dive / 深读 / 详细解析 work, also use [`paper-deep-dive`](../paper-deep-dive/SKILL.md). That skill is the single canonical delivery standard for PDF/HTML extraction, main-entry `Paper Card` / `论文解析树` / `精读稿`, linked artifacts `英文原文稿` and `原文中译稿`, paper-card creation, manuscript fidelity, and completion gates. Keep this skill's Research-Wiki placement rules, but do not define, relax, or finalize deep-dive deliverables from this skill alone.

这个 skill 用来让 Codex 直接维护一个可长期积累的 Markdown wiki：原始资料保持不可变，Codex 增量生成和更新 wiki，Obsidian 只是可选的浏览器。

## 核心约定

- 保持三层结构：`raw/` 原始资料、生成的 `wiki/`、控制文档 `purpose.md` 和 `schema.md`。
- Codex 负责生成和维护 wiki 页面；人类负责选择资料、设定优先级、做关键判断。
- 优先把有长期价值的回答写回 wiki，而不是只留在聊天里。重要回答进入 `wiki/queries/` 或 `wiki/synthesis/`。
- 使用 `[[wikilinks]]`、YAML frontmatter、来源引用、`wiki/index.md`、`wiki/overview.md` 和只追加的 `wiki/log.md`。
- 除非用户明确要求导入、移动或删除 source 文件，否则不要修改 `raw/sources/` 下的原始资料。
- 不把整个 Obsidian vault 自动纳入 wiki。`2-Learnings/EmbodiedWorld/`、`2-Learnings/Courses/`、`0-Daily/`、`1-Meetings/` 是宽输入池；`3-Projects/` 是围绕特定项目组织学习、方案和工作推进的项目层；`4-Research-Wiki/raw/` 是已经决定进入该专题 wiki 的精选证据库；`4-Research-Wiki/wiki/` 是 Codex 编译后的理解层。
- 判断资料是否进入 `raw/`，看它是否值得成为该专题的长期证据，而不是看它有没有 property/frontmatter。

## 原子笔记原则

Research-Wiki 的长期理解层遵循 Zettelkasten / 原子笔记理念：它不是资料堆放处，也不是把 source 改写成另一篇长文，而是把可复用的想法编译成彼此连接的小卡片。

- 一条稳定笔记只承载一个核心想法：一个 concept、claim、question、method、research-practice 或清晰的关系判断。
- `source` 页面可以稍长，用来保存来源上下文；`concept`、`claim`、`question`、`research-practice` 应尽量原子化，不写成无边界综述。
- 写笔记时先问：未来的我会在什么情境下重新需要这个想法？它应该和哪些旧笔记互相发现？
- 不做 source 原文搬运。用自己的话重写理解，同时保留来源引用、PDF/arXiv/网页链接和必要的原句定位。
- 优先创建或更新多条互相链接的小笔记，而不是把多个可独立复用的想法塞进一个大 synthesis。
- 每条 durable note 至少说明：单一想法是什么、来自哪里、连接到哪些旧笔记、还存在哪些待验证问题。
- 每条 durable note 必须能通过 `wiki/index.md`、`wiki/overview.md` 或一条清晰的 wikilink 路径重新找到；孤立笔记不算完成。
- 如果一条内容没有未来复用途径、没有可连接对象，也不能形成概念/主张/问题/方法论，就暂时留在 Daily、Projects 或 raw，不进入 wiki 理解层。

## 输入层边界

推荐关系：

```text
2-Learnings/EmbodiedWorld / 2-Learnings/Courses / 0-Daily / 1-Meetings
= 未筛选或半筛选输入池

3-Projects
= 项目级学习、方案、推进记录和待验证判断

4-Research-Wiki/raw
= 已决定进入世界模型研究语境的证据库

4-Research-Wiki/wiki
= Codex 编译后的概念、主张、问题、综合与方法论
```

操作原则：

- 外层资料池可以宽，`4-Research-Wiki/raw` 必须精选，`4-Research-Wiki/wiki` 必须编译。
- `2-Learnings/EmbodiedWorld/` 不放进 `4-Research-Wiki/` 内部；它是世界模型专题学习层、paper cards 和候选池，不再包一层 `Papers/`。
- `2-Learnings/Courses/` 单独保存课程资料、课件和课程笔记；课程中的稳定概念或方法论应先蒸馏为 study note，再进入 Research-Wiki。
- `0-Daily/` 和 `1-Meetings/` 不全量进入 `raw/`；只把蒸馏后的高价值片段放入 `raw/sources/daily-distillations/` 或 `raw/sources/meeting-extracts/`。
- `3-Projects/` 不保存实验代码、训练日志和论文写作工程；它保存项目目标、方案推理、定向学习、任务拆解、风险判断和阶段总结。
- Projects 中稳定、可复用、跨项目成立的概念、claim、open question 或 research-practice，才进一步蒸馏进入 `4-Research-Wiki/`。
- README 只保留在 vault 根目录下的一级模块中：`0-Daily/README.md`、`1-Meetings/README.md`、`2-Learnings/README.md`、`3-Projects/README.md`、`4-Research-Wiki/README.md`。不要在二级或更深层目录继续散落 README；需要说明时合并进对应一级 README。
- 一份材料进入 `raw/` 前，先问：它是否值得成为 Research-Wiki 的证据？
- 如果不能生成或更新 concept、claim、question、synthesis 或 research-practice，就暂时不要进入 `4-Research-Wiki/wiki/`。
- 进入 `4-Research-Wiki/wiki/` 时，先判断是否应拆成原子笔记：source summary 负责记录来源，长期理解优先拆成可链接的 concept、claim、question 或 research-practice。
- 原始输入文件可以没有 property/frontmatter；生成的 wiki 页面必须有 frontmatter。
- 多机器同步时，skill 源文件保存在 vault 内的 `.tools/skills/llm-wiki-skill/`；每台 Mac 通过 `~/.codex/skills/llm-wiki` 软链接到该目录。新机器按 `Vault Setup.md` 运行 `.tools/setup-vault-mac.sh`，不要手动复制整份 `~/.codex/`。

Daily 输入层包括：

- 文本形式的日常记录：想法、问题、反思、灵感、即时理解。默认写入 `0-Daily/Diary/YYYY-MM-DD.md`；历史研究日记和已整理文本记录保存在 `0-Daily/Diary/Research Diary.md`。注意目录名是大写 `Diary`，不要使用 `0-Daily/diary/` 或旧路径 `0-Daily/Research Diary.md`。
- AI 聊天记录：GPT、Gemini、NotebookLM 等对话。它们是思考痕迹和候选观点，不是默认可靠来源；不需要每天处理，应周期性批量提取核心知识。
- 手机截图：主要来自微信/公众号和小红书。它们默认上下文不完整、来源质量不稳定，需要更强筛选。截图原图放入 `0-Daily/Screenshots/assets/`；整理稿（`0-Daily/Screenshots/YYYY-MM-DD-简短主题.md`）**不放内嵌原图**，结构固定为：**上半「总结」**（主题、要点、与 vault 的衔接、待核验），**下半「全部原文（OCR）」**——将截图中**可见文字尽数转写**（含标题、副标题、段落、列表、小标题、按钮文案、评论等版面文字），并标 `ocr.status`；不是「摘录」或大幅删节。**写作前须校验原图**：若宽高异常（例如宽度仅数十像素的长条），说明导出损坏或误选文件，须请用户重导原图后再 OCR，**禁止**仅凭多模态「读图描述」编造正文。论文线索与判断写在「总结」中即可。B 站内容通常不走截图主流程，更适合以链接或剪藏进入 `0-Daily/Clippings/`。
- Clippings / 剪藏：网页文章、公众号网页、访谈、博客、平台内容等网页剪藏。它们属于 Daily 日常摄取，不等同于已进入 Research-Wiki 的证据；不要把截图整理稿默认放进 `0-Daily/Clippings/`。

如果用户对 clipping / 网页文章 / pasted text 明确要求 `原文`、`提取原文`、`英文原文与中文译文`、English original plus Chinese translation，或强调 `不要总结`，不要进入本 skill 的蒸馏/原子笔记流程。先使用 [`bilingual-source-archive`](../bilingual-source-archive/SKILL.md) 在用户选择的平台生成原文与中文译文归档；只有后续用户要求沉淀长期知识时，再从该 source archive 蒸馏进 Research-Wiki。

处理 Daily 时：

- 不直接把 daily 全量摄入 wiki。
- 每日原始日记主入口是 `0-Daily/Diary/YYYY-MM-DD.md`。如果用户说“写进今天的日记”或“记录到 Daily”，优先写入当天日期文件，而不是写入 `0-Daily/Diary/Research Diary.md`；只有历史整理、跨日合并或用户明确要求时，才维护 `0-Daily/Diary/Research Diary.md`。
- 先生成 `raw/sources/daily-distillations/YYYY-MM-DD.md` 这类蒸馏稿。
- 只有能转化为 concept、claim、question、synthesis 或 research-practice 的部分，才进入 wiki。
- AI 聊天应低频、批量、少手动地处理。不要要求用户每天导出或整理；当用户提供一批 ChatGPT/Gemini/NotebookLM 记录时，只提取核心知识。
- AI 聊天中的事实主张需要追溯到论文、原文、实验或可靠资料；如果暂时无法验证，放入 `reviews.md`。
- 从 AI 聊天中只保留：用户反复追问的问题、被用户认可的判断、概念澄清、研究路线、阅读路线、实验想法、待验证 claim。忽略寒暄、工具性问答、泛泛建议和重复解释。
- 推荐批处理路径：`0-Daily/ai-chats/batches/` 存放定期导出的原始聊天记录，`raw/sources/daily-distillations/YYYY-MM-DD-ai-chats.md` 存放蒸馏后的核心知识。
- 截图内容可以保留启发价值，但事实可靠性需要二次验证。**整理稿**须含可复制检索的 **全文 OCR**（版面文字尽量不漏），且**不嵌原图**，避免体积与检索问题。
- Clippings 先提取正文、元数据、论文线索、核心观点、启发和待验证事实；只有能转化为 concept、claim、question、synthesis 或 research-practice 的内容，才进入 wiki。
- 从 Clippings 提炼长期知识时，不按原文段落机械摘要；先识别可复用的单一想法，再写成原子笔记或更新已有笔记。

截图处理分流：

- 如果截图中识别到论文线索，例如标题、作者、arXiv ID、DOI、会议名、论文页面、论文 PDF 或论文总结，应自动进入论文追踪流程：联网搜索对应论文资源，优先找到 arXiv、DOI、PDF、OpenReview、会议页面、项目页和代码仓库；总结论文内容，并判断它与世界模型研究的相关性。截图整理稿默认写入 `0-Daily/Screenshots/YYYY-MM-DD-简短主题.md`：**不得**用 `![[...]]` 嵌入原图；须按 **总结 / 全部原文（OCR）** 两截书写，原文部分**尽录可见文字**。原图只保留在 `0-Daily/Screenshots/assets/`（整理稿中可用 YAML `source` 指路径，不嵌图）。
- 如果截图是公众号、小红书等普通文章或观点内容，同样：**先**在「全部原文（OCR）」中转写全文，**再**在顶部「总结」中写启发、问题、类比、方法论反思和待验证事实。
- 普通平台内容的事实主张不能直接写成 stable claim；未验证时进入 `reviews.md` 或以 `status: review` 保存。
- 论文资源总结可进入 `raw/sources/papers/`；普通文章截图的蒸馏结果进入 `raw/sources/daily-distillations/`。

论文卡片处理：

- 本 skill 不再定义 paper card 的正文格式、metadata 字段、图像选择、图注标准、排序或验证门槛；这些统一以 [`paper-card-delivery`](../paper-card-delivery/SKILL.md) 为准。
- 无论论文来自 `0-Daily` 截图、clipping、`1-Meetings` 链接、Zotero、`2-Learnings/EmbodiedWorld/` 还是 `3-Projects/`，只要要生成、补全、审核或同步 paper card，都必须先使用 `paper-card-delivery` 的六槽位格式与 source-grounded 验证流程。
- 本 skill 只补充 Research-Wiki / local vault 归档边界；本地 Markdown 图片资产、文件命名、相对路径、缺图状态、候选状态等 paper-card 规则也统一按 `paper-card-delivery` 执行。
- 写入或同步到任一平台时，必须同时使用 `research-doc-workflow` 与对应 `*-doc-workflow`；paper-card 的图片位置、图注、布局验证和迁移残留检查按 `paper-card-delivery` 的目标平台分支执行。

Meeting 论文处理完成后，`1-Meetings/assets/` 只保留最终会被 meeting 文档引用的流程图或必要图像；下载的 PDF、整页渲染截图、临时裁图和其他中间文件必须删除。具体 paper-card 图片资产命名和清理规则按 `paper-card-delivery` 执行。

论文处理分层：

- Paper card 和 deep dive 的边界统一以 `paper-card-delivery` 为准：paper card 是阅读全文后的轻量索引，不是全文结构化解析或完整翻译。
- Dive into paper / 深入论文阶段才进行 PDF-to-Markdown 解析。当用户说“深入读这篇论文”“详细解析”“dive into”“转成 md”“逐节分析”“做深读笔记”时，优先把 PDF 转为结构化 Markdown，再基于 Markdown 深读。
- PDF-to-Markdown 优先考虑 MinerU、Docling、Marker、Unstructured、PDFFigures2 这类结构化解析工具；若本机未安装，先用轻量 PyMuPDF / pdfplumber 作为 fallback，不把缺工具作为停止理由。
- 当前 vault **默认**本地主工具为 **MinerU**：便捷脚本 **`.tools/mineru-md.sh INPUT.pdf OUTPUT_DIR`**（默认 `pipeline` 后端，纯 CPU 可跑）。脚本保存在 vault 内，MinerU Python 环境默认保存在本机 `~/Library/Application Support/WorldModelVault/envs/mineru-env/`，不随 iCloud vault 同步。做深读解析时优先使用该脚本；输出目录结构与 MinerU 版本相关，以生成物为准。若仍需 Docling，使用 `.tools/setup-docling-mac.sh` 与 `.tools/docling-md.sh`。
- PDF-to-Markdown 结果是深读中间层，不等同于 Research-Wiki。不要把论文全文 Markdown 全量塞进 `4-Research-Wiki/wiki/`；只把经过提炼的 concept、claim、method、evidence、limitation、open question 或 research-practice 写入 wiki。
- Deep dive 成品遵循用户选择的平台，不再默认放入飞书。若目标是 Obsidian，将完整 deep-dive 包放在独立、稳定的论文阅读目录或用户指定路径，不要把英文原文稿、原文中译稿和整篇论文正文直接塞进 `4-Research-Wiki/wiki/` 的原子理解层。只有长期成立的概念、主张、问题、方法和证据才进一步蒸馏进入 `4-Research-Wiki/raw/sources/papers/` 与 `4-Research-Wiki/wiki/`。
- 结构化解析时保留章节层级、公式/表格占位、figure caption、正文引用线索、参考文献和关键术语；如果解析质量差，需要回到 PDF 原文核验，不得只依赖损坏的 Markdown。

Deep dive 标准只保留在 [`paper-deep-dive`](../paper-deep-dive/SKILL.md)。本 skill 不再维护第二份 deep dive 结构、翻译规则、图表规则或质量门槛，以免和主标准漂移。

当用户在 wiki / Obsidian / Research-Wiki 语境中要求 deep dive：

- 先按 `paper-deep-dive` 在用户选择的平台完成或修复完整 deep-dive 交付包；Obsidian 请求可直接生成 Obsidian 包，不需要经过飞书。
- 不把半成品、结构稿、选摘稿或章节摘要写成 Research-Wiki 的正式 deep-dive 产物。
- Deep dive 完成后，只把仍有长期价值的内容蒸馏为 Research-Wiki 的 concept、claim、question、method、evidence、limitation、open question 或 research-practice。
- 如果需要在 Research-Wiki 中记录 deep dive 来源，只记录目标平台链接或相对路径、论文元信息、关键 source anchors 和蒸馏后的稳定认识，不复制整篇英文原文稿、原文中译稿或主入口精读稿。

Meeting 输入层包括：

- 豆包总结记录：会议总结、转写、要点提炼。它们是快速入口，不是最终证据。
- 拍摄图像：slides、白板、论文截图、方法图、实验表格等。需要先识别文字和结构。
- 论文链接信息：arXiv、DOI、OpenReview、会议页、代码仓库、项目页等。

Meeting 总结默认包含两层：**保守纪要** 和 **会后头脑风暴**。保守纪要只写可由转写、图像、论文链接或原文校验的信息；会后头脑风暴明确标注为研究发散，用来把当天论文、组内项目和更大的研究主线连接起来。

Meeting 使用 `research-doc-workflow` 选择目标平台并叠加对应适配器，并保留现有会议库的平台。用户给出 Notion/飞书链接时更新对应平台；给出 vault 路径或明确写 Obsidian 时用 `obsidian-doc-workflow`；无目标时只追问一句目的地，不建立无必要的平行副本。

一次组会、一次文献整理、一次导师讨论或一次科研交流，对应一个按日期组织的 durable meeting page/note。内容保留日期、简述、关键论文/链接/图片、Paper Cards、保守纪要、会后头脑风暴和待办。标题使用 `YYYY-MM-DD 简短主题`，主题应根据当日核心内容命名，不使用无信息量的固定尾缀。Meeting 页面是输入层，不代表已纳入 Research-Wiki。如果材料来自 Zotero collection，而 collection 本身跨越多个日期，应优先按日期子 collection 名或明确记录中的日期拆成多个日期页面；没有日期子 collection 时，再参考条目的 `dateAdded`。不要把导出日期当成组会日期。

平台映射：Feishu 使用 wiki/doc 页面；Notion 使用会议数据库记录或日期子页面；Obsidian 使用既有 `1-Meetings/` 目录、frontmatter、相对资源和 MOC 链接。写后必须按目标平台重新读取并验证标题、日期、图片、Paper Cards、纪要和头脑风暴边界。

处理 Meeting 时：

- 不直接把整场会议记录编译进 wiki，只提取高价值科研片段。
- 先写用户选择平台的 meeting 页面；只有当 meeting 中的内容需要长期进入 Research-Wiki 时，再从该页面蒸馏 `raw/sources/meeting-extracts/YYYY-MM-DD.md`，不要把完整会议纪要复制进 Research-Wiki。
- 如果 meeting 页面已经基于 `个人研究名片` 做了讲者匹配，蒸馏进 Research-Wiki 时保留这个身份锚点，例如 `speaker`、`research_card` 或正文中的人物链接。它用于追溯某个观点/项目/论文线索来自谁，不等于该人物主页，也不替代原始会议证据。
- 如果讲者只由转写或模型推断得到，保留 `讲者待核验` / `可能为 <name>（待核验）`，不要把不确定归因写成 stable claim。缺失的研究名片应进入 meeting TODO，而不是阻塞会议整理。
- 豆包总结中的关键信息需要和图像、论文链接或原论文互相校验。
- 如果图像或链接中识别到论文线索，自动进入论文追踪流程：搜索论文资源，总结论文，判断与世界模型研究的相关性；正式 meeting 文档中的论文应优先按 `paper-card-delivery` 补成 source-grounded paper card。
- 与世界模型高度相关的论文资源总结可进入 `raw/sources/papers/`；组会启发、科研通法、问题意识进入 `raw/sources/meeting-extracts/`。
- 未验证事实主张进入 `reviews.md` 或以 `status: review` 保存。
- 推荐 meeting 文档结构：frontmatter、简述、论文列表、Paper Cards、保守纪要/讨论脉络、横向结论、会后头脑风暴、待办。
- `会后头脑风暴` 必须与保守纪要分开写，避免把发散判断伪装成已发生讨论或论文事实。开头写清楚“这一节不是保守纪要，而是研究发散”。
- 头脑风暴不只服务 JEPA / world model；它也应主动连接组内其他课题，例如动作理解、长尾识别、3DGS/PBR、PEFT/LoRA/Adapter、机器人策略、多模态融合、实验设计和论文写作方法论。也可以另设“个人兴趣连接”，把音乐生成、折纸艺术等用户长期兴趣作为灵感来源，但不要误写成组内课题。
- 头脑风暴可固定回答这些问题：这篇论文预测的是 pixel、token、latent、object state、reward 还是 action？它的状态表示是隐式还是显式？prediction 是训练期辅助任务还是测试时决策模块？如果改成 JEPA/world-model/PEFT/3DGS/PBR/长尾识别等组内范式，context、target、loss、模块、数据和指标应如何改？它能否转化为组内可做实验？是否能和个人兴趣如音乐生成、折纸艺术形成概念类比或创作灵感？限制来自数据、任务定义、物理假设、评价指标、baseline 还是计算资源？
- 对头脑风暴中的想法分级：`可立即做实验`、`需要补文献`、`概念启发`、`高风险猜想`。只有经过后续验证、可复用且跨项目成立的想法，才进一步蒸馏进 Research-Wiki 的 concept、claim、question 或 research-practice。

## Wiki 目录结构

默认项目根目录：

```text
<project>/
  purpose.md
  schema.md
  raw/sources/
  raw/assets/
  wiki/index.md
  wiki/log.md
  wiki/overview.md
  wiki/entities/
  wiki/concepts/
  wiki/sources/
  wiki/claims/
  wiki/questions/
  wiki/queries/
  wiki/synthesis/
  wiki/comparisons/
  wiki/reviews.md
  wiki/research.md
  .llm-wiki/manifest.json
  .llm-wiki/queue.json
  .llm-wiki/graph.json
  .llm-wiki/lint.json
```

用下面命令创建结构：

```bash
scripts/llm_wiki_tools.py init <project>
```

## 页面 Frontmatter

每个生成的 wiki 页面都必须用下面的 YAML frontmatter 开头：

```yaml
---
title: "Readable title"
type: "source|entity|concept|claim|question|query|synthesis|comparison|overview|index"
status: "seed|draft|review|stable|deprecated"
created: "YYYY-MM-DD"
updated: "YYYY-MM-DD"
sources:
  - "raw/sources/example.md"
tags: []
---
```

说明：

- `sources` 使用相对路径。
- 生成页面文件名使用稳定的小写连字符格式，例如 `large-language-model.md`。
- 长期 wiki 页面正文优先使用中文；字段名和枚举值保持英文，方便脚本和未来工具读取。

## 页面写作规范

- 正文主体用中文。重要英文术语首次出现时写成 `中文（English term）`，后文可按语境使用中文或缩写。
- 数学符号、变量、概率表达式和结构方程必须使用 LaTeX：行内用 `$...$`，块级用 `$$...$$`。行内数学同样需要从官方源校准；不要把 `$x_t$`、`$\pi(a\mid s)$`、`$\mathcal{L}$` 这类符号写成普通文本或翻译成中文词。
- 不要用反引号包裹数学符号或公式，例如不要写 `` `PA_i` ``、`` `P(Y | X=x)` ``；应写成 $\mathrm{PA}_i$、$P(Y \mid X=x)$。
- 反引号只用于文件路径、命令、代码标识符、字段名、枚举值、脚本参数和确实属于代码的片段。
- 论文标题、模型名、数据集名、仓库名和链接保持原文；必要时在中文解释后保留英文括注。

## 工作流

### 初始化

1. 只有当项目目录不明确时才询问用户。
2. 运行 `scripts/llm_wiki_tools.py init <project>`。
3. 如果用户给了领域目标，按领域改写 `purpose.md`。
4. 把 `schema.md` 当作操作契约；当目录、页面类型、引用规则变化时同步更新。

### 摄入资料

采用 `nashsu/llm_wiki` 启发的两步摄入法：

摄入前先确认资料是否应该进入该专题 wiki：

- **一定纳入**：与世界模型直接相关的论文、综述、课程笔记、学习总结；会长期复用的概念；能形成明确 claim 的内容；改变已有理解的材料。
- **选择性纳入**：组会中的高价值片段；daily 中经过蒸馏的科研想法；AI 聊天中被用户认可且可追溯/可验证的观点；截图触发的科研类比、问题意识或方法论启发；低度相关但高启发的材料；可复用科研通法。
- **不纳入**：临时 todo、行政信息、日常流水、只对当天有意义的记录、没有形成问题/概念/claim/方法论启发的摘抄、实验代码、实验日志、论文正文工程、单纯“以后可能有用”的剪藏。

1. **分析**：阅读 source、`purpose.md`、`schema.md`、`wiki/index.md`、`wiki/overview.md` 和相关旧页面。提取实体、概念、主张、证据、矛盾、可能要创建/更新的页面、review 项、deep research 线索。
2. **生成**：创建或更新 source 摘要页，然后把长期价值拆成受影响的 entity/concept/claim/question/research-practice/synthesis 页面。能原子化的内容优先进入小笔记；只有跨多条笔记形成叙事、比较或阶段性判断时，才写 synthesis。更新 `index.md`、`overview.md`、`reviews.md`、`research.md`，并向 `log.md` 追加记录。

摄入前先运行：

```bash
scripts/llm_wiki_tools.py manifest <project>
```

如果 source 没变化，默认跳过，除非用户要求重新摄入。摄入文件夹时保留相对路径，并把文件夹路径当作分类上下文。

Source 摘要页放在 `wiki/sources/`，必须包含：

- 这份资料实际说了什么，而不是泛泛背景介绍
- source 元数据和路径
- 关键主张、证据、结论
- 指向相关页面的 `[[wikilinks]]`
- 开放问题和需要人工判断的 review 项

### 查询

1. 读取 `purpose.md`、`schema.md`、`wiki/index.md` 和 `wiki/overview.md`。
2. 运行 `scripts/llm_wiki_tools.py search <project> "<query>"`。
3. 阅读搜索结果中的高相关页面；必要时再读图谱邻居页面。
4. 回答时引用 wiki 页面和 source 路径。
5. 如果答案有长期价值，把它创建或更新到 `wiki/queries/`、`wiki/synthesis/` 或 `wiki/comparisons/`，然后更新 `index.md` 和 `log.md`。

### Lint / 健康检查

运行：

```bash
scripts/llm_wiki_tools.py lint <project>
```

然后修复或记录：

- 缺失 frontmatter
- 断掉的 `[[wikilinks]]`
- 孤立页面或弱连接页面
- `sources` 过期或缺失
- 重复实体/重复概念
- 与更新或更强来源冲突的 claim
- 被反复提到但没有独立页面的重要概念

Lint 完成后向 `wiki/log.md` 追加记录；不能自动判断的事项放到 `wiki/reviews.md`。

### 图谱和洞察

运行：

```bash
scripts/llm_wiki_tools.py graph <project>
```

使用 `.llm-wiki/graph.json` 识别：

- 直接 `[[wikilinks]]`
- 共享 source 的页面
- Adamic-Adar 风格的共同邻居关联
- 同类型页面关联
- 用 connected components 作为无依赖版 Louvain 替代
- 孤立页面、稀疏社区、桥接页面、意外跨类型连接

如果用户要“图谱视图”，不要假装有 App UI；用 Markdown 表格和 Mermaid 图替代。

### Deep Research / 深度研究

如果需要当前网页信息，并且用户允许或明确要求联网，使用 Codex 浏览网页做研究。否则在 `wiki/research.md` 创建研究任务，包含：

- topic
- 为什么它对 `purpose.md` 重要
- 建议搜索查询
- 相关页面
- 预期输出页面

研究完成后，把结果保存为 `wiki/synthesis/` 或 `wiki/sources/` 页面，并按正常摄入流程更新链接、索引和日志。

### Review Queue / 人工审核队列

用 `wiki/reviews.md` 记录异步人工判断。每个 item 应包含：

- id、date、status
- source/path
- issue
- recommended actions：create page、merge pages、mark conflict、deep research、skip
- 如果需要研究，提前写好 search queries

不要因为主观判断阻塞摄入；保守记录，继续处理确定部分。

## 功能等价说明

这个 skill 可以通过 Codex + 文件系统模拟 `nashsu/llm_wiki` 的大部分信息效果。它不能原生提供桌面 UI、后台文件夹监听、流式聊天持久化、Chrome 扩展、LanceDB 向量搜索、Tauri 系统集成或真正的 Louvain 可视化布局。

替代方案：

- App UI → Markdown 文件、Codex 摘要、Mermaid、JSON 报告。
- 后台 watcher → 每次会话前或用户要求同步时运行 `manifest`。
- 持久队列 → `.llm-wiki/queue.json` 加 `wiki/log.md`。
- 向量搜索 → 关键词搜索加图谱扩展；以后可接入 qmd 或 embedding 工具。
- Louvain → `graph` 里的 connected components 和稀疏社区启发式。
- 网页剪藏 → 把剪藏后的 Markdown 放进 `raw/sources/`，或让 Codex 浏览网页后归档 source 页面。
- 多模态图片/PDF → 能提取文本就先提取；图片只有在作为本地文件或对话附件可见时再用 Codex 视觉能力处理。

## 参考文件

- 当需要判断 `nashsu/llm_wiki` 的某个功能在无 App 工作流里怎么替代时，读取 `references/feature-map.md`。
- 需要确定性维护命令时，运行 `scripts/llm_wiki_tools.py --help`。
