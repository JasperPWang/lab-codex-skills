---
name: daily-research-review
description: Run the user's daily科研经营复盘 / Daily Research Operating Review. Use when the user says they want to start, continue, write, or organize a daily review, daily research review, 每日复盘, 科研复盘, 今日复盘, or asks to create/update the dated Feishu review page with reflection, project triage, AI ROI, simulation-ready research direction checks, and tomorrow's three key TODOs.
---

# Daily Research Review

## Core Contract

Treat the review as a personal research-company operating review, not a diary. The review must answer two questions:

1. Did today turn time, AI, papers, code, experiments, and communication into reusable research assets?
2. Did today make the user more like a researcher worth betting on: better at defining problems, testing hypotheses, building systems, and judging direction?

Default language is Chinese. Use English terms when they are the natural technical labels.

For reader-facing Chinese review prose and TODOs, also use [`chinese-technical-writing`](../chinese-technical-writing/SKILL.md): keep method names, acronyms, project names, and simulation terms when they are names, but translate ordinary technical concepts into Chinese instead of mixing raw English phrases into Chinese sentences.

## Feishu Placement

Use the `feishu-doc-workflow` skill for all Feishu reads/writes.

If the user brings a research-method article or web source into the review context and asks for `原文`, `提取原文`, or `英文原文与中文译文`, use [`bilingual-source-archive`](../bilingual-source-archive/SKILL.md) as a side path. Do not fold the source into the daily review as a summary unless the user explicitly asks for a review takeaway.

Stable hierarchy:

- Parent context page: `Entrepreneurial Research Mindset`
- Review hub: `科研经营复盘｜Daily Research Operating Review`
- Daily child pages under the hub: `YYYY-MM-DD 科研经营复盘`

Before writing, fetch the hub and child list. If today's child page exists, update it. If not, create it under the review hub. Verify after writing that:

- The document title and wiki node title are not `Untitled` / `无标题`.
- The page is under the review hub, not directly under the outer parent.
- The final page contains `明日三项关键 Todo`.

## Review Flow

Start by asking only the next useful questions. Do not ask the whole template at once if the user is already answering naturally.

Use this order:

1. Establish today's date and the user's current stage or context.
2. Capture project-level progress.
3. Capture assets created today.
4. Identify hypotheses validated, weakened, or still unknown.
5. Evaluate AI / GPT / Codex ROI.
6. Identify risks and bottlenecks.
7. Derive tomorrow's role-based TODOs, then reduce them to exactly three key TODOs.

If the user gives a long free-form answer, first reflect it back as structured notes, then ask for missing high-value information.

## Required Sections

Write each daily page with these sections:

```markdown
# YYYY-MM-DD 科研经营复盘

## 0. 今日语境
## 1. 今日最重要的推进
## 2. 今日资产沉淀
## 3. 今日假设验证
## 4. 项目经营判断
## 5. GPT / Codex / AI 投资回报
## 6. Simulation-Ready 方向检查
## 7. 当前最大风险
## 8. 明日角色化 Todo
## 9. 明日三项关键 Todo
```

Use `## 6. Simulation-Ready 方向检查` every day. The user has stated that simulation will be a future must-have capability, so projects should be reviewed for whether they move toward simulation-ready / simulation-capable outputs.

## Project Triage Lens

For every active project mentioned, record:

- Current priority: short-term critical / medium-term important / long-term thesis line / parked.
- Today's concrete movement.
- Next evidence needed.
- Whether it creates a reusable asset.
- Whether it improves simulation-readiness.

Current known project lines:

- `UniGAvatar`: short-term critical. Baseline experiment documentation, result analysis, geometry loss, semantic experiments.
- `3DGS4SMPL`: document and asset consolidation; needs deeper analysis.
- `GaussianAvatar`: July-August delivery line. Need to complete the SMPL-X pipeline and reuse mature ExAvatar components; tied to paper completion and submission.
- `Home-scene world model for SMPL-X planning`: long-term PhD thesis line. Needs sustained learning and literature grounding.
- `Single-pose simulation-ready avatar reconstruction`: emerging idea. Inspired by PGC-like thinking; multi-view single-pose reconstruction may be a better route to accurate simulation-ready meshes than monocular-video fitting.

These are context anchors, not fixed facts. Update them when the user corrects priorities.

## Hypothesis Language

Phrase hypotheses explicitly:

- `假设：...`
- `今日证据：支持 / 反驳 / 不确定`
- `下一步：继续 / 收缩 / 转向 / 停止`

Do not convert ideas into conclusions too early. For new ideas, preserve the user's intuition and mark what evidence is still missing.

## AI ROI Lens

Evaluate AI usage by outputs, not interaction volume:

- Time saved.
- Judgment improved.
- Assets created or cleaned.
- Experiments, code, papers, or Feishu pages advanced.
- Whether AI use became unproductive chatting.

## Role-Based TODOs

Use these roles to find blind spots:

- CEO: direction, priority, and strategic bet.
- CTO: technical route and module choices.
- Research Scientist: hypothesis and novelty.
- Research Engineer: smallest executable experiment or code step.
- PM: milestone, scope, and acceptance criteria.
- CFO: time, GPU, GPT, and attention ROI.
- Data / Infra: data, environment, logs, visualizations, failure cases.
- Reviewer: strongest attack on novelty, evaluation, claims, and baselines.
- Writer / Communicator: Feishu, wiki, paper, slides, mentor communication.
- AI Manager: what to delegate to AI and what judgment the user must own.

After role scanning, keep exactly three execution TODOs:

1. `CEO Todo`: the one action most affecting direction survival.
2. `Research / Engineering Todo`: the smallest experiment, code, paper, or analysis action.
3. `Asset Todo`: the one thing that must become a reusable research asset.

## Writing Style

Be concrete and decision-oriented. Avoid motivational fluff.

Good wording:

- `今天真正推进的是...`
- `这仍然不是结论，但它把下一步验证问题收缩为...`
- `明天的验收标准是...`

Avoid:

- Generic diary prose.
- Overconfident conclusions from weak evidence.
- Long project descriptions that do not end in an action or decision.
