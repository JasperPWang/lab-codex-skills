---
name: ai-research-workflow
description: Orchestrates AI research agent workflows (paper deep-dive, survey builder, cite verify, repro pack) per the team's Feishu wiki survey. Use when the user asks for literature workflows, paper cards, survey/taxonomy, citation verification, reproducibility packages, or mentions AI Research Skills / 科研 skill 工作流.
---

# AI Research Workflow

基于飞书 Wiki 调研报告组织的科研工作流入口。源文档：
<FEISHU_OR_LARK_URL>

## Canonical Paper Card Gate

Whenever a workflow will create, normalize, audit, or sync paper cards, first use [`paper-card-delivery`](../paper-card-delivery/SKILL.md). That skill is the canonical source for paper-card verification, fixed format, image/caption rules, and validation. This router must not finalize a paper card from its local summary rules alone.

## Canonical Chinese Technical Writing Gate

Whenever a workflow will produce Chinese reader-facing research notes, Feishu pages, wiki pages, paper-card prose, deep-dive notes, survey summaries, or meeting/daily-review text, also use [`chinese-technical-writing`](../chinese-technical-writing/SKILL.md). Keep English for names, acronyms, code, formulas, datasets, and exact source text; translate ordinary technical concepts into Chinese.

## Good Research Operating Loop Gate

For research planning, paper reading, survey work, experiments, reproduction, and writing, treat the workflow as a loop that improves judgment:

1. Problem choice: state why the problem matters, why it generalizes beyond one narrow trick, and why the next attack is simple enough to test.
2. Ownership: distinguish the user's own reasoning from advisor framing, paper framing, social-media framing, and AI-generated framing.
3. Forecast: before reading the result, asking a mentor, or running an experiment, write the expected outcome and the reason.
4. Correction: after evidence arrives, write what belief changed and what remains unknown.
5. Speed: prefer the path that discovers wrong assumptions fastest: one-command run, one-command plot, reproducible config, small data slice, or single-batch overfit check.
6. Output inspection: inspect raw outputs, failure cases, visual samples, logs, transcripts, geometry, and qualitative artifacts before trusting an aggregate metric.
7. Baseline pressure: tune baselines, run ablations, and compare against the simplest strong alternative before claiming novelty.
8. Research notebook compression: preserve experiment findings, insights, code progress, failed runs, and next steps in a form that can be compressed weekly or reused in Feishu/wiki/paper assets.
9. Focus budget: protect the main research line; give wandering, new fields, and speculative ideas a bounded exploration budget unless evidence justifies a pivot.
10. Communication asset: convert useful understanding into an explanation, tool, code snippet, paper card, Feishu page, or draft paragraph.

Do not turn this gate into a long questionnaire. Use it to catch missing reasoning before choosing a downstream skill.

## Lab-Native Integration Principle

Personal lab skills own final deliverables. Downloaded / vendored skills are
method libraries unless the user explicitly asks to run them as standalone
workflows.

- For Feishu work, final structure, hierarchy, native images, native captions,
  formula handling, fetch-before-write, and fetch-after-write verification are
  controlled by `feishu-doc-workflow` and the task-specific personal skill.
- For paper deep dives, borrow `nature-reader` ideas such as block-level source
  maps, original / Chinese correspondence, figure/table placement, terminology
  consistency, and uncertainty notes, but convert them into the required Feishu
  parent page with `Paper Card`, native `论文解析树`, and source-order `精读稿`,
  plus child pages `英文原文稿` and `原文中译稿`.
- For surveys and literature organization, borrow `deep-research` ideas such as
  research-question clarification, source verification, contradiction checks,
  synthesis, and gap analysis, but convert them into the user's literature tree,
  challenge-insight tree, novelty tree, paper matrix, and paper-card collection.
- Do not let an external skill's default artifact format override the user's
  Feishu-native conventions. External APA reports, Markdown readers, PRISMA
  reports, or local asset bundles can be kept as intermediate/source artifacts
  only when useful and should be clearly labeled.

## 何时用哪个 skill

| 用户意图 | Skill |
|----------|-------|
| 中文科研文档、飞书页面、wiki 笔记、中文技术说明的语言规范 | [`chinese-technical-writing`](../chinese-technical-writing/SKILL.md) plus the task-specific skill below |
| 任意 paper card / 论文卡片生成、补全、审核、同步 | [`paper-card-delivery`](../paper-card-delivery/SKILL.md) plus the task-specific skill below |
| 精读 PDF、MinerU、中英笔记、paper card | [`paper-deep-dive`](../paper-deep-dive/SKILL.md) |
| 领域综述、taxonomy、文献树、challenge-insight | [`survey-builder`](../survey-builder/SKILL.md) |
| 引用核验、claim-citation 对齐 | [`cite-verify`](../cite-verify/SKILL.md) |
| 实验复现包、artifact、config/commit 归档 | [`repro-pack`](../repro-pack/SKILL.md) |
| 本仓库训练/实验代码与记录 | [`research-dev-standards`](../research-dev-standards/SKILL.md) |

Paper-card gate: this router only summarizes the gate. The binding contract lives in [`paper-card-delivery`](../paper-card-delivery/SKILL.md). Do not duplicate or override its source-verification, metadata, image, caption, bullet-slot, sorting, or validator rules here.

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

- 实验与训练：始终叠加 `research-dev-standards`（`Experiment.md`、`RoadMap.md`、小步验证）
- `repro-pack` 产物应能支撑 `Experiment.md` 中的「可复制命令 + 产物路径」
- 飞书同步：使用 `feishu-doc-workflow` 和本地 `lark-cli`；创建或更新文档优先 `--as user` 放入用户云文档

## 阶段门（大型任务前自检）

1. Research question 是否明确？
2. 问题是否重要、可泛化、且下一步足够简单？
3. 用户自己的判断、导师/论文/趋势/AI 的输入是否已经区分清楚？
4. Literature / source list 是否足够，且是否读到原文、附录、限制而不只读摘要？
5. Claim 是否有 evidence？
6. Citation 是否真实支撑？
7. 统计/指标是否自洽？
8. 实验是否可复现（commit、config、command）？
9. 是否已经写下预测、结果和更新后的判断？
10. 是否检查过原始输出和失败样本，而不只看平均指标？

## 详细调研摘要

见 [references/survey-report.md](references/survey-report.md)
