---
title: LLM Wiki Skill 英中整理
source: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
author: Andrej Karpathy
created: 2026-05-13
type: bilingual-notes
tags:
  - llm
  - knowledge-management
  - obsidian
  - karpathy
---

![LLM Wiki Skill Architecture](assets/llm-wiki-architecture.svg)

# LLM Wiki Skill

原文链接：[LLM Wiki by Andrej Karpathy](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)

说明：下面不是对原文的逐字全文转载，而是按原文结构整理的英文复述版和中文翻译版。这样既适合放进 Obsidian 长期保存，也方便之后继续扩展成自己的 LLM Wiki 工作流。

---

# English

## LLM Wiki

This note describes a pattern for building personal knowledge bases with large language models. It is not meant to be a complete product specification. It is an idea file: something you can give to an LLM agent such as Codex, Claude Code, OpenCode, Pi, or a similar tool, and ask it to help instantiate the pattern for your own needs.

The specific directory layout, naming conventions, schemas, and tools can vary. The important part is the workflow: use the LLM not only as a question-answering interface, but as an active maintainer of a persistent, structured, interlinked knowledge base.

## The Core Idea

Most people currently interact with documents through a RAG-like workflow. They upload a set of files, the system retrieves relevant chunks at query time, and the LLM generates an answer from those chunks. This is useful, but it has an important limitation: the model is often rediscovering the same knowledge again and again.

If a question requires synthesizing five documents, the system must retrieve fragments from those documents and assemble the answer each time. The result may be good, but the synthesis itself usually does not become a durable artifact. The system answers the question, and then the reasoning disappears back into the chat history.

The LLM Wiki pattern changes this. Instead of treating raw documents as the only long-term knowledge store, the LLM incrementally builds and maintains a wiki: a structured collection of Markdown files that sits between the user and the raw sources.

When a new source is added, the LLM does more than index it. It reads the source, extracts key information, creates or updates summary pages, revises concept pages, updates entity pages, notes contradictions, strengthens earlier syntheses, and adds cross-links. The knowledge is compiled once and then kept current.

The result is a persistent and compounding artifact. The wiki becomes richer with every source added and every useful question asked. Cross-references accumulate. Contradictions are flagged. Summaries evolve. The system does not start from scratch every time.

In this pattern, the human rarely writes the wiki directly. The human chooses sources, explores directions, reviews important changes, and asks good questions. The LLM performs the maintenance work: summarizing, filing, linking, updating, and bookkeeping.

A practical setup is to keep the LLM agent open on one side and Obsidian open on the other. The LLM edits the files, while the human browses the result in real time through links, graph view, and page previews. Obsidian becomes the IDE, the LLM becomes the programmer, and the wiki becomes the codebase.

## Possible Uses

This pattern can apply to many domains.

For personal knowledge management, it can track goals, health, psychology, self-improvement, journal entries, podcast notes, articles, and reflections. Over time, the wiki can build a structured picture of a person, their interests, their recurring themes, and their evolving priorities.

For research, it can support a deep investigation over weeks or months. Papers, articles, reports, and notes can be compiled into a growing body of topic pages, source summaries, entity pages, comparison pages, and evolving theses.

For reading a book, the LLM can file each chapter as it is read. It can create pages for characters, themes, locations, concepts, plot threads, and important connections. By the end, the reader has a companion wiki rather than a pile of disconnected notes.

For business or team use, the wiki can be fed by meeting transcripts, Slack threads, project documents, customer calls, decision records, and product notes. Humans can remain in the loop for review, but the LLM handles the maintenance that teams often neglect.

The same idea can also support competitive analysis, due diligence, trip planning, course notes, hobby research, and any other activity where knowledge accumulates over time and needs to remain organized.

## Architecture

The system has three main layers.

The first layer is raw sources. These are the curated source documents: articles, papers, images, data files, transcripts, notes, and other materials. This layer is treated as evidence and should generally be immutable. The LLM reads from this layer, but does not casually rewrite it.

The second layer is the wiki. This is a directory of LLM-generated Markdown files. It may include source summaries, entity pages, concept pages, comparison pages, overviews, syntheses, question answers, and research notes. The LLM owns this layer. It creates pages, updates them when new sources arrive, maintains links, and keeps the structure coherent.

The third layer is the schema. This is the instruction document that tells the LLM how the wiki should be structured and maintained. In Claude Code it might be `CLAUDE.md`; in Codex it might be `AGENTS.md`. The schema defines conventions, workflows, page templates, citation rules, logging rules, and maintenance expectations.

The schema is crucial because it turns the LLM from a generic chatbot into a disciplined wiki maintainer. It can also evolve over time as the user and the LLM discover what works for a specific domain.

## Operations

The first core operation is ingestion. The user adds a new source to the raw collection and asks the LLM to process it. The LLM reads the source, identifies the key takeaways, creates a source summary, updates related entity and concept pages, adds cross-links, updates the index, and appends an entry to the log.

A single source may touch many pages. For careful work, it is useful to ingest one source at a time and stay involved. The user can read the summary, check the updates, and tell the LLM what should be emphasized. Batch ingestion is possible, but the workflow should match the user's level of desired supervision.

The second core operation is querying. The user asks a question against the wiki. The LLM searches or reads the relevant pages, synthesizes an answer, and cites the wiki pages or source summaries it used. The answer can take many forms: a Markdown note, a comparison table, a slide outline, a chart, or another artifact.

The important point is that a valuable answer should not vanish into chat history. If the answer contains a useful comparison, synthesis, or new connection, it can be saved back into the wiki as a new page. This makes exploration itself compound.

The third core operation is linting. Periodically, the user asks the LLM to audit the wiki. It should look for contradictions, stale claims, orphan pages, missing backlinks, important concepts that deserve their own pages, weak citations, and research gaps. This maintenance keeps the wiki healthy as it grows.

## Indexing and Logging

Two special files are especially useful: `index.md` and `log.md`.

`index.md` is content-oriented. It acts as a catalog of the wiki. It lists pages, short descriptions, categories, and sometimes metadata such as dates, tags, or source counts. The LLM updates it after ingesting new sources or creating important new pages. When answering a query, the LLM can read the index first to decide which pages deserve closer attention.

This index-based approach works well at moderate scale. For a small or medium wiki, it can reduce the need for more complex embedding infrastructure.

`log.md` is chronological. It records what happened and when: ingests, queries, major updates, lint passes, and maintenance actions. A consistent log format makes it easy for both humans and command-line tools to inspect the wiki's recent history.

The index tells the system what exists. The log tells the system what changed.

## Optional Tools

As the wiki grows, additional tools can help. A local Markdown search engine can make it easier for the LLM to find relevant pages. At small scale, `index.md` may be enough; at larger scale, search becomes more valuable.

Obsidian is a natural interface for this workflow. It provides Markdown editing, backlinks, graph view, plugins, local files, and a good browsing experience for interconnected notes.

A web clipper is useful for turning web articles into Markdown sources. Local image handling can also matter. If images are saved locally, the LLM can inspect or reference them more reliably than if they remain as remote URLs that may break.

Obsidian's graph view helps reveal the shape of the wiki: which pages are hubs, which pages are isolated, and which concepts are becoming central.

Plugins such as Dataview can make frontmatter useful by generating dynamic tables and lists. Markdown-based slide tools such as Marp can turn wiki content into presentations.

Because the wiki is just a folder of Markdown files, it can be stored in Git. That gives it version history, branching, review, and collaboration.

## Why It Works

The hard part of maintaining a knowledge base is not only reading or thinking. It is the ongoing bookkeeping: updating links, keeping summaries current, reconciling contradictions, moving information to the right page, and maintaining consistency across many files.

Humans often abandon personal wikis because the maintenance burden grows faster than the perceived value. LLMs are well suited to this maintenance work. They can update many files in one pass, add links, revise summaries, and keep track of repeated structural tasks.

This allows the human to focus on higher-level work: choosing sources, directing the investigation, judging what matters, and asking better questions.

The idea is related in spirit to Vannevar Bush's Memex: a personal, curated knowledge store organized through associative trails. The LLM Wiki pattern supplies the missing maintainer. The LLM performs the labor of keeping the trails alive.

## Final Note

This pattern is intentionally abstract. It does not prescribe one universal implementation. The right directory structure, page schema, tooling, and level of automation depend on the domain and the user.

Some wikis may be text-only. Some may need images. Some may need search tools; others may work with only an index. Some users may want slide decks and charts; others may only want Markdown notes.

The best way to use this idea is to share the pattern with an LLM agent and collaborate with it to create a version that fits the actual workflow.

---

# 中文

## LLM Wiki

这篇笔记描述了一种用大语言模型构建个人知识库的模式。它不是一个完整产品规格，而是一个想法文件：你可以把它交给 Codex、Claude Code、OpenCode、Pi 或类似的 LLM Agent，让它根据你的需要帮你搭建一套具体系统。

具体目录结构、命名规则、schema 和工具都可以变化。真正重要的是工作流：不要只把 LLM 当作问答界面，而要把它当作一个持续维护结构化、互链知识库的主动维护者。

## 核心思想

现在多数人与文档互动的方式都类似 RAG。用户上传一批文件，系统在提问时检索相关片段，然后 LLM 基于这些片段生成回答。这很有用，但有一个重要限制：模型经常在一遍又一遍地重新发现同样的知识。

如果一个问题需要综合五份文档，系统每次都要重新从这些文档里检索片段，再临时拼出答案。答案可能不错，但这个综合过程本身通常不会变成一个持久资产。问题回答完以后，推理就散落回聊天记录里了。

LLM Wiki 模式改变了这一点。它不再把原始文档当作唯一的长期知识存储，而是让 LLM 逐步建立并维护一个 wiki：一组结构化的 Markdown 文件，位于用户和原始资料之间。

当加入一个新来源时，LLM 不只是给它建索引。它会阅读来源，提取关键信息，创建或更新摘要页，修订概念页，更新实体页，标注矛盾，强化已有综合，并增加交叉链接。知识被“编译”一次，然后持续保持更新。

结果就是一个持久且会复利增长的知识产物。每加入一个来源、每提出一个有价值的问题，wiki 都会变得更丰富。交叉引用会累积，矛盾会被标出，摘要会演化，系统不再每次都从零开始。

在这个模式中，人通常很少直接写 wiki。人负责选择资料、探索方向、审阅关键改动、提出好问题。LLM 负责维护工作：总结、归档、链接、更新和记录。

一种实用设置是：一边打开 LLM Agent，一边打开 Obsidian。LLM 负责编辑文件，人通过链接、图谱视图和页面预览实时浏览结果。Obsidian 成为 IDE，LLM 成为程序员，wiki 本身成为代码库。

## 可能用途

这种模式可以应用在很多领域。

在个人知识管理中，它可以跟踪目标、健康、心理、自我提升、日记、播客笔记、文章和反思。随着时间推移，wiki 可以逐渐形成一个关于个人、兴趣、反复出现的主题和优先级变化的结构化图景。

在研究中，它可以支持持续数周或数月的深入探索。论文、文章、报告和笔记可以被编译成不断增长的主题页、来源摘要、实体页、比较页和演化中的论点。

在读书时，LLM 可以随着阅读进度整理每一章。它可以为人物、主题、地点、概念、情节线和重要联系创建页面。读到最后，读者得到的不是一堆分散笔记，而是一本伴读 wiki。

在商业或团队场景中，wiki 可以由会议记录、Slack 讨论、项目文档、客户访谈、决策记录和产品笔记喂养。人类仍然可以参与审阅，但 LLM 负责团队常常忽略的维护工作。

同样的思路也适用于竞品分析、尽职调查、旅行计划、课程笔记、兴趣研究，以及任何知识会长期积累且需要保持组织性的活动。

## 架构

这个系统有三层。

第一层是raw。它们是经过选择的来源文档：文章、论文、图片、数据文件、访谈记录、笔记和其他材料。这一层应被视为证据，通常不应随意改写。LLM 可以读取这一层，但不应轻易修改它。

第二层是 wiki。这是一组由 LLM 生成的 Markdown 文件。它可以包含来源摘要、实体页、概念页、比较页、总览页、综合分析、问题回答和研究笔记。LLM 拥有这一层：它创建页面，在新来源加入时更新页面，维护链接，并保持结构一致。

第三层是 schema。它是告诉 LLM 如何组织和维护 wiki 的说明文档。在 Claude Code 中可能叫 `CLAUDE.md`；在 Codex 中可能叫 `AGENTS.md`。schema 定义约定、工作流、页面模板、引用规则、日志规则和维护要求。

schema 非常关键，因为它把 LLM 从普通聊天机器人变成一个有纪律的 wiki 维护者。它也可以随着用户和 LLM 对某个领域的实践不断演化。

## 操作

第一个核心操作是导入。用户把一个新来源加入原始资料集合，然后让 LLM 处理它。LLM 阅读来源，识别关键要点，创建来源摘要，更新相关实体页和概念页，添加交叉链接，更新索引，并在日志中追加记录。

一个来源可能会影响很多页面。对于严肃工作，最好一次导入一个来源，并保持人参与其中。用户可以阅读摘要，检查更新，并告诉 LLM 应强调什么。批量导入也可以，但工作流应匹配用户想要的监督程度。

第二个核心操作是查询。用户围绕 wiki 提问。LLM 搜索或阅读相关页面，综合出答案，并引用它使用的 wiki 页面或来源摘要。答案可以有很多形式：Markdown 笔记、比较表、幻灯片提纲、图表或其他产物。

重点是：有价值的答案不应该消失在聊天记录中。如果答案包含有用的比较、综合或新连接，就可以被保存回 wiki，成为一个新页面。这样，探索本身也会复利增长。

第三个核心操作是体检。用户定期让 LLM 审计 wiki。它应该寻找矛盾、过时结论、孤立页面、缺失反向链接、值得单独建页的重要概念、薄弱引用和研究空白。这种维护能让 wiki 在增长中保持健康。

## 索引和日志

两个特殊文件特别有用：`index.md` 和 `log.md`。

`index.md` 是面向内容的。它是 wiki 的目录，列出页面、简短描述、分类，有时也包括日期、标签、来源数量等元数据。LLM 在导入新来源或创建重要新页面后更新它。回答问题时，LLM 可以先阅读索引，再决定哪些页面值得深入查看。

在中等规模内，这种基于索引的方法很好用。对于小型或中型 wiki，它可以减少对复杂 embedding 基础设施的依赖。

`log.md` 是按时间顺序的。它记录发生了什么以及何时发生：导入、查询、重大更新、体检和维护操作。一致的日志格式让人和命令行工具都能轻松查看 wiki 最近的变化。

索引告诉系统“有什么”。日志告诉系统“发生了什么变化”。

## 可选工具

随着 wiki 变大，额外工具会变得有用。本地 Markdown 搜索引擎可以帮助 LLM 更容易地找到相关页面。在小规模时，`index.md` 可能已经够用；在更大规模时，搜索会更重要。

Obsidian 是这个工作流的天然界面。它提供 Markdown 编辑、反向链接、图谱视图、插件、本地文件，以及非常适合浏览互联笔记的体验。

网页剪藏工具可以把网页文章快速转成 Markdown 来源。本地图片处理也很重要。如果图片被保存在本地，LLM 就能比依赖远程 URL 更可靠地检查或引用它们。

Obsidian 的图谱视图可以帮助观察 wiki 的形状：哪些页面是枢纽，哪些页面是孤立的，哪些概念正在变得核心。

Dataview 这类插件可以利用 frontmatter 生成动态表格和列表。Marp 这类 Markdown 幻灯片工具可以把 wiki 内容转成演示文稿。

因为 wiki 本质上只是一组 Markdown 文件，所以它可以放进 Git。这样就能获得版本历史、分支、审查和协作。

## 为什么有效

维护知识库的难点不只是阅读或思考，而是持续的整理工作：更新链接、保持摘要新鲜、调和矛盾、把信息移动到正确页面、在许多文件之间保持一致。

人类经常放弃个人 wiki，是因为维护成本增长得比感知价值更快。LLM 很适合承担这些维护工作。它们可以一次更新很多文件，添加链接，修订摘要，并处理重复性的结构任务。

这样，人就可以专注于更高层次的工作：选择来源、指挥研究、判断什么重要，以及提出更好的问题。

这个想法在精神上接近 Vannevar Bush 的 Memex：一个通过联想路径组织起来的个人策展式知识存储。LLM Wiki 模式补上了缺失的维护者。LLM 承担让这些路径持续活着的劳动。

## 最后说明

这个模式是有意保持抽象的。它不规定一个放之四海皆准的实现。正确的目录结构、页面 schema、工具和自动化程度，都取决于领域和用户。

有些 wiki 可能只处理文本。有些可能需要图片。有些需要搜索工具，另一些只靠索引就够了。有些用户需要幻灯片和图表，另一些用户只需要 Markdown 笔记。

使用这个想法的最好方式，是把这种模式交给一个 LLM Agent，然后和它协作，创建一个真正适合自己工作流的版本。

---

## 基于原始 LLM Wiki 理念的高星仓库

> Stars 为 2026-05-14 重新核对的近似值，GitHub 数字会持续变化。

| 仓库                                                                                              | Stars | 类型                         | 说明                                                                             |
| ----------------------------------------------------------------------------------------------- | ----: | -------------------------- | ------------------------------------------------------------------------------ |
| [Lum1104/Understand-Anything](https://github.com/Lum1104/Understand-Anything)                   | 14.6k | 知识图谱 / 可视化工具               | 将代码或 LLM Wiki Skill 知识库转成交互式知识图谱，可搜索、探索和问答。                                 |
| [nashsu/llm_wiki](https://github.com/nashsu/llm_wiki)                                           |  7.3k | 完整桌面 App                   | Tauri 桌面应用，把文档自动组织成互链 wiki，包含摄入、搜索、图谱、Lint、Deep Research 等。                    |
| [AgriciDaniel/claude-obsidian](https://github.com/AgriciDaniel/claude-obsidian)                 |  5.0k | Obsidian + Agent 工作流       | Claude + Obsidian companion，基于 LLM Wiki Skill pattern 维护持续增长的 vault。        |
| [sdyckjq-lab/llm-wiki-skill](https://github.com/sdyckjq-lab/llm-wiki-skill)                     |  1.5k | Agent Skill                | 中文友好的 LLM Wiki Skill 方法论 Skill，支持多平台 Agent。                                 |
| [Ar9av/obsidian-wiki](https://github.com/Ar9av/obsidian-wiki)                                   |  1.2k | Obsidian 框架                | 让 AI agents 构建和维护 Obsidian wiki 的框架。                                           |
| [atomicstrata/llm-wiki-compiler](https://github.com/atomicstrata/llm-wiki-compiler)             |  1.2k | Compiler / CLI-like        | “Raw sources in, interlinked wiki out”，强调知识编译器思路。                              |
| [eugeniughelbur/obsidian-second-brain](https://github.com/eugeniughelbur/obsidian-second-brain) |  1.1k | Obsidian + Cross-CLI Skill | 面向 Claude Code、Codex CLI、Gemini CLI、OpenCode 的 AI-first second brain。          |
| [lucasastorian/llmwiki](https://github.com/lucasastorian/llmwiki)                               |   893 | App 实现                     | 上传文档并连接 Claude，让 LLM 写 wiki 的开源实现。                                             |
| [Astro-Han/llm-wiki](https://github.com/Astro-Han/llm-wiki)                   |   828 | Agent Skill / 模板           | 面向 Claude Code、Cursor、Codex 的 Agent Skills-compatible LLM Wiki。 |

相关但不完全等同于 LLM Wiki 的仓库：

| 仓库 | Stars | 说明 |
|---|---:|---|
| [wanshuiyin/Auto-claude-code-research-in-sleep](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep) | 9.3k | 更偏自动科研循环和 Agent research workflow，不是纯 LLM Wiki，但与自维护研究系统高度相邻。 |
| [nex-crm/wuphf](https://github.com/nex-crm/wuphf) | 1.0k | 协作式 AI employees / agent memory 系统，强调 AI 自维护知识库。 |
