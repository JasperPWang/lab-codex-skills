---
name: ai-research-workflow
description: Orchestrates AI research agent workflows (paper deep-dive, survey builder, cite verify, repro pack) with durable delivery to Feishu/Lark, Notion, or Obsidian/Markdown. Use when the user asks for literature workflows, paper cards, survey/taxonomy, citation verification, reproducibility packages, cross-platform research documentation, or mentions AI Research Skills / 科研 skill 工作流.
---

# AI Research Workflow

基于既有科研工作流调研报告组织的跨平台入口。历史源文档保留在飞书：
<FEISHU_OR_LARK_URL>

All durable document writes must also use [`research-doc-workflow`](../research-doc-workflow/SKILL.md) plus the matching platform adapter (`feishu-doc-workflow`, `notion-doc-workflow`, or `obsidian-doc-workflow`). The source of a workflow may be Feishu, but the destination is selected from Feishu, Notion, or Obsidian according to the user's current URL or explicit instruction.

## Canonical Paper Card Gate

Whenever a workflow will create, normalize, audit, or sync paper cards, first use [`paper-card-delivery`](../paper-card-delivery/SKILL.md). That skill is the canonical source for paper-card verification, fixed format, image/caption rules, and validation. This router must not finalize a paper card from its local summary rules alone.

## Canonical Paper Deep Dive Gate

Whenever a workflow will create, audit, repair, or route a single-paper deep dive, use [`paper-deep-dive`](../paper-deep-dive/SKILL.md). That skill is the only delivery standard for what counts as a completed deep dive: main entry `Paper Card` / `论文解析树` / source-order `精读稿`, complete `英文原文稿`, complete `原文中译稿`, source-fidelity formulas/captions/references, and target-platform read-back verification. This router may choose the skill stack, but it must not define a looser deep-dive artifact or call a partial package complete.

## Canonical Chinese Technical Writing Gate

Whenever a workflow will produce Chinese reader-facing research notes, Notion/Obsidian/Feishu pages, paper-card prose, deep-dive notes, survey summaries, or meeting/daily-review text, also use [`chinese-technical-writing`](../chinese-technical-writing/SKILL.md). Keep English for names, acronyms, code, formulas, datasets, and exact source text; translate ordinary technical concepts into Chinese.

## Good Research Operating Loop Gate

For research planning, paper reading, survey work, experiments, reproduction, and writing, treat the workflow as a loop that improves judgment:

1. Problem choice: state why the problem matters, why it generalizes beyond one narrow trick, and why the next attack is simple enough to test.
2. Ownership: distinguish the user's own reasoning from advisor framing, paper framing, social-media framing, and AI-generated framing.
3. Forecast: before reading the result, asking a mentor, or running an experiment, write the expected outcome and the reason.
4. Correction: after evidence arrives, write what belief changed and what remains unknown.
5. Speed: prefer the path that discovers wrong assumptions fastest: one-command run, one-command plot, reproducible config, small data slice, or single-batch overfit check.
6. Output inspection: inspect raw outputs, failure cases, visual samples, logs, transcripts, geometry, and qualitative artifacts before trusting an aggregate metric.
7. Baseline pressure: tune baselines, run ablations, and compare against the simplest strong alternative before claiming novelty.
8. Research notebook compression: preserve experiment findings, insights, code progress, failed runs, and next steps in a form that can be compressed weekly or reused in Notion/Obsidian/Feishu/paper assets.
9. Focus budget: protect the main research line; give wandering, new fields, and speculative ideas a bounded exploration budget unless evidence justifies a pivot.
10. Communication asset: convert useful understanding into an explanation, tool, code snippet, paper card, durable research page, or draft paragraph.

Do not turn this gate into a long questionnaire. Use it to catch missing reasoning before choosing a downstream skill.

## Mechanism Review Gate

Before routing any paper card, deep dive, survey, or paper-discussion artifact to durable delivery, perform a mechanism review:

1. Reconstruct the strongest version of the authors' or field's logic before criticizing it.
2. Name the concrete bottleneck and its proposed causal explanation.
3. Identify the key assumptions and their falsifiable predictions.
4. Trace `design -> changed information/constraint/optimization -> expected effect`.
5. Locate the decisive experiment, control, or ablation rather than relying on aggregate improvement alone.
6. Test whether a simpler alternative explanation remains viable.
7. Predict what should happen when a key module is removed, replaced, or minimized, and where the assumptions should fail.
8. Formulate the smallest credible alternative and the next experiment that would discriminate between explanations.

Keep `作者声称`, `实验支持`, `我们的推断`, and `尚未验证` distinct. Use this gate to decide whether the current output is only a summary or demonstrates actual understanding; do not expose it as a mandatory questionnaire or repeat the same headings in every document. Let `paper-card-delivery`, `paper-deep-dive`, and `survey-builder` compress the reasoning into their own artifacts and completion checks.

## Lab-Native Integration Principle

Personal lab skills own final deliverables. Downloaded / vendored skills are
method libraries unless the user explicitly asks to run them as standalone
workflows.

- For durable document work, final structure, hierarchy, images, captions, formulas, links, and verification are controlled by `research-doc-workflow`, its selected platform adapter, and the task-specific personal skill.
- For paper deep dives, route final delivery through `paper-deep-dive`. Borrow `nature-reader` ideas such as block-level source
  maps, original / Chinese correspondence, figure/table placement, terminology
  consistency, and uncertainty notes, but convert them into the required cross-platform package: main entry with `Paper Card`, `论文解析树`, and source-order `精读稿`, plus complete `英文原文稿` and `原文中译稿` artifacts; do not publish a partial or alternate reader as the finished deep dive.
- For surveys and literature organization, borrow `deep-research` ideas such as
  research-question clarification, source verification, contradiction checks,
  synthesis, and gap analysis, but convert them into the user's literature tree,
  challenge-insight tree, novelty tree, paper matrix, GitHub / Awesome resource
  map, and paper-card collection. Treat Awesome repositories, benchmark lists,
  and code-list repositories as active discovery sources: search for high-star
  and actively maintained repositories, open the repository README / lists /
  linked projects, and extract missing papers, datasets, code links, and field
  groupings before finalizing the survey. Do not use those repositories as a
  substitute for official paper-source verification.
- Do not let an external skill's default artifact format override the user's semantic contract or selected platform. External APA reports, alternate Markdown readers, PRISMA reports, or local asset bundles can be kept as intermediate/source artifacts only when useful and should be clearly labeled.

## 何时用哪个 skill

| 用户意图 | Skill |
|----------|-------|
| 中文科研文档、Notion/Obsidian/飞书页面、wiki 笔记、中文技术说明的语言规范 | [`chinese-technical-writing`](../chinese-technical-writing/SKILL.md) plus the task-specific skill below |
| 选择、迁移或写入 Feishu / Notion / Obsidian | [`research-doc-workflow`](../research-doc-workflow/SKILL.md) + matching `*-doc-workflow` + the task-specific content skill |
| 任意 paper card / 论文卡片生成、补全、审核、同步 | [`paper-card-delivery`](../paper-card-delivery/SKILL.md) plus the task-specific skill below |
| 精读 PDF、MinerU、中英笔记、paper card | [`paper-deep-dive`](../paper-deep-dive/SKILL.md) |
| 领域综述、taxonomy、文献树、challenge-insight | [`survey-builder`](../survey-builder/SKILL.md) |
| 引用核验、claim-citation 对齐 | [`cite-verify`](../cite-verify/SKILL.md) |
| 实验复现包、artifact、config/commit 归档 | [`repro-pack`](../repro-pack/SKILL.md) |
| 本仓库训练/实验代码与记录 | [`research-dev-standards`](../research-dev-standards/SKILL.md) |

Paper-card gate: this router only summarizes the gate. The binding contract lives in [`paper-card-delivery`](../paper-card-delivery/SKILL.md). Do not duplicate or override its source-verification, metadata, image, caption, bullet-slot, sorting, or validator rules here.

Deep-dive gate: this router only selects and composes skills. The binding contract lives in [`paper-deep-dive`](../paper-deep-dive/SKILL.md). Do not duplicate or override its hierarchy, manuscript, mind-map, close-reading, formula, figure, reference, or completion rules here.

## 推荐主线（不要孤立使用）

```
读文献 → 想问题 → 做实验 → 保真 → 写论文
  │         │         │        │        │
Paper RAG  Survey   Repro    Cite/    PaperSpine
Deep-dive  Builder   Pack    Stats    Nature/LaTeX
```

## 优先级（来自调研报告）

**立即吸收**：Paper RAG / local wiki、`survey-builder`、`cite-verify`、`repro-pack`、PaperSpine（有初稿时）

**中期**：Stats Sanity、LaTeX Writer、Nature-Skills

**按需**：Grant Writer、Academic Research Skills（流程较重，慎用）

## 与本仓库的衔接

- 实验与训练：始终叠加 `research-dev-standards`（Notion 实验记录、`RoadMap.md`、小步验证）与 `experiment-report-writing`
- `repro-pack` 产物应能支撑 Notion 实验页中的「可复制命令 + 产物路径」
- 文档同步：统一通过 `research-doc-workflow` 按用户链接/说明选择 Feishu、Notion 或 Obsidian，并叠加对应适配器：`feishu-doc-workflow`、`notion-doc-workflow`、`obsidian-doc-workflow`

## 阶段门（大型任务前自检）

1. Research question 是否明确？
2. 问题是否重要、可泛化、且下一步足够简单？
3. 用户自己的判断、导师/论文/趋势/AI 的输入是否已经区分清楚？
4. Literature / source list 是否足够，且是否读到原文、附录、限制而不只读摘要？
5. 是否能画出从瓶颈、假设、设计到预期效果的因果链，而不只是复述模块？
6. 关键 Claim 的决定性证据是什么，实验是否排除了相关替代解释？
7. 作者声称、实验支持、我们的推断和尚未验证的内容是否已经分开？
8. Citation 是否真实支撑，结论是否越过证据边界？
9. 统计/指标是否自洽，原始输出和失败样本是否与平均指标一致？
10. 实验是否可复现（commit、config、command）？
11. 是否已经写下反事实预测：删除、替换或简化关键设计后应发生什么？
12. 是否说明假设在何种数据、场景或监督变化下失效，以及下一个区分性实验是什么？

## 详细调研摘要

见 [references/survey-report.md](references/survey-report.md)
