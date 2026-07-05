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
  parent page plus `英文原文稿`, `原文译稿`, and `中文精读稿`.
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
2. Literature / source list 是否足够？
3. Claim 是否有 evidence？
4. Citation 是否真实支撑？
5. 统计/指标是否自洽？
6. 实验是否可复现（commit、config、command）？

## 详细调研摘要

见 [references/survey-report.md](references/survey-report.md)
