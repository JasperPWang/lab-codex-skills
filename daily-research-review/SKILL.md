---
name: daily-research-review
description: Run the user's daily科研经营复盘 / Daily Research Operating Review and persist it in Feishu/Lark, Notion, or Obsidian/Markdown. Use when the user says they want to start, continue, write, or organize a daily review, daily research review, 每日复盘, 科研复盘, 今日复盘, or asks to create/update a dated review page with reflection, project triage, AI ROI, simulation-ready research direction checks, and tomorrow's three key TODOs.
---

# Daily Research Review

## Core Contract

Treat the review as a personal research-company operating review, not a diary. The review must answer two questions:

1. Did today turn time, AI, papers, code, experiments, and communication into reusable research assets?
2. Did today make the user more like a researcher worth betting on: better at defining problems, testing hypotheses, building systems, and judging direction?

Default language is Chinese. Use English terms when they are the natural technical labels.

For reader-facing Chinese review prose and TODOs, also use [`chinese-technical-writing`](../chinese-technical-writing/SKILL.md): keep method names, acronyms, project names, and simulation terms when they are names, but translate ordinary technical concepts into Chinese instead of mixing raw English phrases into Chinese sentences.

## Platform Placement

Use [`research-doc-workflow`](../research-doc-workflow/SKILL.md) for destination selection and durable writes. Preserve an existing review hub's platform; do not create a parallel Feishu copy when the active review system is Notion or Obsidian.

If the user brings a research-method article or web source into the review context and asks for `原文`, `提取原文`, or `英文原文与中文译文`, use [`bilingual-source-archive`](../bilingual-source-archive/SKILL.md) as a side path. Do not fold the source into the daily review as a summary unless the user explicitly asks for a review takeaway.

Keep this logical hierarchy on every platform:

- Parent context page: `Entrepreneurial Research Mindset`
- Review hub: `科研经营复盘｜Daily Research Operating Review`
- Dated entries under or linked from the hub: `YYYY-MM-DD 科研经营复盘`

Map it natively:

- Feishu/Lark: wiki parent, review hub, and dated child page through `feishu-doc-workflow`.
- Notion: review hub plus dated subpage or database record with date/status properties.
- Obsidian: review MOC/index plus dated Markdown note in the established review folder, with frontmatter and links following neighboring notes.

Before writing, fetch or read the hub/index and dated entries. If today's entry exists, update it; otherwise create it in the same system. Verify after writing that:

- The title is not `Untitled` / `无标题` and the date is correct.
- The entry is linked to or contained by the review hub, not left orphaned.
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

## Good Research Loop Lens

Use the review to train research taste, not just record activity. When relevant, extract these signals and place them into the existing required sections:

- Problem ownership: did the user choose the problem from their own reasoning, or merely absorb an advisor's task, a trend, or a paper's framing?
- Important and attackable: is the current question both worth solving and small enough to test with the next concrete action?
- Forecast before result: what did the user expect before reading a paper, asking for advice, running an experiment, or seeing a metric?
- Belief update: after the result, what changed in the user's model of the project, method, baseline, data, or evaluation?
- Loop speed: how quickly did the user discover they were wrong, and what tooling, command, config, plot, or AI workflow could shorten that loop tomorrow?
- Output inspection: did the user inspect raw outputs, failure cases, visualizations, transcripts, samples, or geometry artifacts instead of only trusting aggregate metrics?
- Failure clustering: what is the largest pile of failures, and what is the smallest attack on that pile?
- Input quality: did today's reading include primary papers, appendices, limitations, old or underpriced sources, and not only social summaries?
- Focus versus exploration: did the user protect the main project line while giving exploratory ideas a bounded budget?
- Generous asset: did today's work produce something reusable for future self, collaborators, public writing, code, Notion/Obsidian/Feishu documentation, or paper writing?

Map these signals into the template rather than adding new daily sections. For example, forecast and belief update belong in `今日假设验证`; loop speed and output inspection belong in `今日资产沉淀`, `GPT / Codex / AI 投资回报`, or `当前最大风险`; problem ownership and importance belong in `项目经营判断`.

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
- `预测：...`
- `结果：...`
- `更新后的判断：...`

Do not convert ideas into conclusions too early. For new ideas, preserve the user's intuition and mark what evidence is still missing.

## AI ROI Lens

Evaluate AI usage by outputs, not interaction volume:

- Time saved.
- Judgment improved.
- Assets created or cleaned.
- Experiments, code, papers, or durable research pages advanced.
- Whether AI use became unproductive chatting.
- Whether AI shortened the research loop by making experiments, plots, comparisons, source reading, or failure inspection faster.
- Whether the user kept ownership of the key judgment instead of outsourcing taste, problem choice, or claims to AI.

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
- Writer / Communicator: Notion/Obsidian/Feishu documentation, paper, slides, mentor communication.
- AI Manager: what to delegate to AI and what judgment the user must own.
- Research Taste Coach: forecast before seeing answers, compare with reality, and convert the gap into a sharper next experiment or reading question.

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
