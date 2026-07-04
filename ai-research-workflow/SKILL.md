---
name: ai-research-workflow
description: Orchestrates AI research agent workflows (paper deep-dive, survey builder, cite verify, repro pack) per the team's Feishu wiki survey. Use when the user asks for literature workflows, paper cards, survey/taxonomy, citation verification, reproducibility packages, or mentions AI Research Skills / 科研 skill 工作流.
---

# AI Research Workflow

基于飞书 Wiki 调研报告组织的科研工作流入口。源文档：
<FEISHU_OR_LARK_URL>

## 何时用哪个 skill

| 用户意图 | Skill |
|----------|-------|
| 精读 PDF、MinerU、中英笔记、paper card | [`paper-deep-dive`](../paper-deep-dive/SKILL.md) |
| 领域综述、taxonomy、文献树、challenge-insight | [`survey-builder`](../survey-builder/SKILL.md) |
| 引用核验、claim-citation 对齐 | [`cite-verify`](../cite-verify/SKILL.md) |
| 实验复现包、artifact、config/commit 归档 | [`repro-pack`](../repro-pack/SKILL.md) |
| 本仓库训练/实验代码与记录 | [`research-dev-standards`](../research-dev-standards/SKILL.md) |

Paper-card gate: whenever this router leads to a Feishu paper card, survey card, meeting paper card, or deep-dive card, a finished card requires official full-paper verification first. Do not promote cards based only on abstracts, project pages, README files, slides, screenshots, snippets, or secondary summaries. Use `candidate / 待核验`, `Not reported`, or an explicit verification TODO until the official paper has been read or searched end to end.

Paper-card image gate: the main image should be the official core method/process figure when available, such as method, pipeline, framework, system overview, architecture, data flow, benchmark construction, or score/loss/computation flow. Do not let a teaser, qualitative showcase, result collage, demo gallery, or visual example grid be the only card image when a core method/process figure exists. Teasers may only be supplementary second images with explicit teaser/result captions.

Paper-card caption gate: every selected figure needs the complete Chinese translation of the official source figure caption. A caption such as `图｜GS-IR overview`, `图｜pipeline`, `图｜teaser`, a local filename, or a self-written summary is incomplete. If the original caption has not been found and translated in full, leave `图注待补` and keep the card incomplete.

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
- 飞书同步：用 `lark-doc` / `lark-drive`；创建文档优先 `--as user` 放入用户云文档

## 阶段门（大型任务前自检）

1. Research question 是否明确？
2. Literature / source list 是否足够？
3. Claim 是否有 evidence？
4. Citation 是否真实支撑？
5. 统计/指标是否自洽？
6. 实验是否可复现（commit、config、command）？

## 详细调研摘要

见 [references/survey-report.md](references/survey-report.md)
