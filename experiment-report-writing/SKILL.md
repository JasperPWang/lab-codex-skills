---
name: experiment-report-writing
description: Write source-grounded research experiment reports and experiment-log entries for ML/vision/graphics/robotics projects. Default durable destination is Notion; Feishu/Lark or Obsidian/Markdown only when the user explicitly names them. Use when the user asks to整理/撰写/补全/审查实验报告, 实验记录, 训练报告, 评测报告, ablation report, baseline report, reproduction report, Notion experiment pages, or research-document experiment summaries.
---

# Experiment Report Writing

## Core Contract

Treat an experiment report as a decision artifact, not a diary. It must help the reader decide whether to trust the run, what changed relative to baseline, what the evidence says, and what the next smallest action should be.

Never invent results, metrics, hyperparameters, commands, environments, datasets, checkpoints, or qualitative observations. If logs or artifacts are missing, write the report as incomplete and list the exact missing evidence. If the experiment has not been run yet, write an experiment plan / pre-registration report, not a completed experiment report.

The leading conclusion callout is user-owned and has one fixed purpose: record the first question and its answer before the experiment runs. It must state what the minimum experiment is intended to verify and the precommitted success standard. Preserve the user's answer, or help make supplied intent falsifiable and measurable without inventing it. Do not rewrite this callout after seeing results; if the verification target or success standard changes, create a new experiment entry. Do not write final conclusions, decisions, or causal judgments for the user unless explicitly asked to draft them from inspected evidence.

Default language is Chinese. Keep method names, dataset names, model names, config keys, file paths, command lines, metric names, and paper/system names in their original form when needed.

Keep this skill focused on report writing. Durable experiment records are maintained in **Notion**, not `docs/Experiment.md` / root `Experiment.md` (those files are retired and must not be created or updated unless the user explicitly revives them). Use [`research-doc-workflow`](../research-doc-workflow/SKILL.md) plus [`notion-doc-workflow`](../notion-doc-workflow/SKILL.md) for delivery; switch to Feishu or Obsidian only when the user explicitly names that destination.

Section headings must use short numbered English labels in this fixed vocabulary: `1. Settings`, `2. Preprocess`, `3. Quantity`, `4. Quality`, `5. Next`, `6. Pause`, `7. Appendix`. Do not use Chinese heading titles for these sections. Body prose stays Chinese by default. If a project has other existing report conventions (table style, caption style), preserve those; do not copy project-specific paths, run names, or one-off implementation details into this general skill.

## Evidence Intake

Before writing a completed report, inspect or request the evidence needed for the claims:

- first question and answer: verification target plus a success standard fixed before the run;
- hypothesis / run plan;
- exact command, script, config, branch, commit, seed, data split, checkpoint, and output directory;
- machine and environment: GPU, CUDA, driver, Docker image / Compose service / conda env, Python and key package versions when relevant;
- code provenance: repo or project path, branch, commit, dirty state if known, and output root;
- logs: stdout/stderr, TensorBoard/W&B tables, evaluation JSON/CSV, training curves, failure traces;
- artifacts: checkpoints, original-resolution rendered images/videos, qualitative samples, figures, screenshots, meshes, point clouds, tables;
- baseline or prior run for comparison;
- known failure cases, raw outputs, and any manual filtering.

If evidence is too large, sample deterministically and say what was inspected. Prefer exact paths and commands over vague provenance.

## Required Structure

Use this structure for a full completed experiment report:

```markdown
# 实验标题

> [!结论]
> **第一问题：这个最小实验要验证什么？成功的标准是什么？**
> - 验证目标：<一句可证伪的陈述>
> - 成功标准：<预先确定的指标、阈值或明确的可观察条件>

## 1. Settings
1. <本实验相对 baseline / 旧设定改了什么：表示、监督、模块、训练协议等，一句一条>
2. <关键超参 / 权重 / 开关；必要坑点可作子条目>
3. 状态：运行中 / 已完成 / 失败 / 已暂停（失败或暂停时一句带过，细节放 `6. Pause`）
4. 实验metadata
   ```text
   分支 / worktree：
   实验名称 / run id：
   输出路径：
   数据 / 序列（如需要）：
   ```

## 2. Preprocess
- 数据清洗 / mask / 对齐 / 裁剪：
- 伪标签 / 中间产物：
- 过滤规则：
- 预处理对结果解释的影响：

## 3. Quantity
- 评测口径：
- 指标方向：
- 结果表：
- 相比 baseline / 上次运行：
- 定量分析：
- 统计或可比性 caveat：

## 4. Quality
- 代表性成功样本：
- 代表性失败样本：
- 原分辨率图像 / 视频：
- 图像原生图注：
- 可视化 / render / geometry / video 观察：
- 失败模式：
- 定性分析：

## 5. Next
1. ...
2. ...
3. ...

## 6. Pause
- 暂停或停止日期：
- 决策：已暂停 / 停止该路线 / 仅作分析材料
- 原因：用已检查证据说明为何不再继续，而不是只写“效果不好”
- 失败阶段 / 关键证据：日志、指标、可视化、坏 checkpoint、误判澄清
- 重启条件：满足什么才允许重开；若明确不再重启，写死“暂不重开”
- 未决项：还缺哪些证据、哪些改动被否决

## 7. Appendix
- 可复用命令 / config：
- 可复用图表 / 样例：
- 原始日志 / 指标文件 / 产物路径：
- 机器 / 环境 / commit 等 provenance（不宜塞进 Settings 的长清单）
- 需要写回的文档：
```

`1. Settings` is a short method card, not a provenance dump. Follow the lean style of pages like Var. Geometry Prior:

- Write only what changed in the experiment design: representation, losses/supervision, protocol, and critical weights or pitfalls.
- Put branch / run name / output path (and brief data/sequence ids if needed) under a single `实验metadata` item, preferably as a compact code/toggle block.
- Do **not** pack Settings with owner, machine/GPU inventory, full command lines, hypothesis essays, predictions, falsification conditions, resource limits, metric definitions, eval procedures, or pause narratives. Those belong in the gray conclusion callout, `3. Quantity` / `4. Quality`, `6. Pause`, or `7. Appendix`.
- If status is `失败` / `已暂停`, Settings may contain one short status line; the evidence-backed pause write-up stays in `6. Pause`.

Use the conclusion callout immediately after the title to preserve the first question and its user-owned answer. Keep the same Markdown report on every platform; only map the semantic callout marker to a native callout in Feishu or Notion when supported. The conclusion callout must use **gray** background (Notion: `gray_background`; Feishu: gray/neutral callout). Do not use yellow, blue, red, or green for this first-question callout. Create and freeze it before the run; do not replace it with a post-hoc result summary. Follow it with the numbered English headings above. Omit `2. Preprocess` only when the experiment has no meaningful preprocessing, pseudo-label generation, alignment, filtering, or data conversion step; then renumber later sections so the report remains continuous (`3. Quantity` becomes `2. Quantity`, and so on). Omit `6. Pause` only when status is not `失败` / `已暂停`; if omitted, renumber `7. Appendix` accordingly.

If the experiment failed, was aborted, or the route is deferred, `1. Settings` may note `状态：失败` / `已暂停` in one line, and the report must include `6. Pause`. Do not leave a failed or paused line looking like an unfinished success write-up. A later successful sub-run, guard check, or partial metric does not remove the pause record when the main route remains stopped.

Use this compact entry only for a short Notion page / database note when a full numbered report is unnecessary. Still deliver it to Notion; do not append to `Experiment.md`.

```markdown
### YYYY-MM-DD｜实验标题

> [!结论]
> **第一问题：这个最小实验要验证什么？成功的标准是什么？**
> - 验证目标：<一句可证伪的陈述>
> - 成功标准：<预先确定的指标、阈值或明确的可观察条件>

- 状态：运行中 / 已完成 / 失败 / 已暂停
- 假设 / 预测：
- 命令：
- 环境：
- 关键设置：
- 结果：
- 原始输出观察：
- 结论边界：
- 下一步：
- 产物：
- 暂停记录（失败 / 已暂停时必填）：日期、决策、原因、证据、重启条件
```

For an experiment that has not run yet, use a pre-registration form:

```markdown
# 实验计划｜实验标题

> [!结论]
> **第一问题：这个最小实验要验证什么？成功的标准是什么？**
> - 验证目标：<一句可证伪的陈述>
> - 成功标准：<预先确定的指标、阈值或明确的可观察条件>

- 背景问题：
- 假设：
- 运行前预测：
- 最小实验设置：
- 对照 / baseline：
- 失败时如何解释：
- 命令草案：
- 预计产物：
- 复盘时间：
```

## Writing Rules

- Put the first question and answer in the first conclusion callout immediately after the title, with gray background. Write and freeze it before execution; never retrofit the verification target or success threshold to match observed results.
- Keep both answers concrete: the verification target must be falsifiable, and the success standard must be a metric, threshold, or unambiguous observable condition. Treat `效果不错`, `看起来可行`, or equivalent wording as incomplete.
- Separate evidence from interpretation. Use phrases like `日志显示`, `指标表明`, `可视化显示`, and `我的判断是` to distinguish source-backed observation from analysis.
- Always compare against a baseline, previous run, or explicit expectation when possible. If no baseline exists, say so and propose the smallest baseline to add.
- Report both metrics and raw outputs. Do not conclude from aggregate metrics alone when qualitative artifacts exist.
- Include failed or ugly samples. A report with only cherry-picked images is not complete for research judgment.
- Record negative and inconclusive results clearly. A failed run can still be a useful report if it identifies a broken assumption, bad config, data issue, or next diagnostic.
- If the result is still running, write `状态：运行中` and include current evidence only; do not write final conclusions.
- If an experiment failed before producing metrics, report failure stage, error snippet, likely cause, and the next diagnostic command.
- Keep `1. Settings` lean: method deltas + compact `实验metadata` only. Do not turn Settings into an audit checklist of owner/GPU/commands/hypotheses/metrics.
- If the run or research route is failed, aborted, or deferred, put a one-line `状态：失败` / `已暂停` in Settings and keep the dedicated `6. Pause` section for decision, evidence-backed reason, and restart conditions or an explicit “暂不重开”. Do not bury the only pause note after a success-looking metric/render section without declaring status.
- When explicitly asked to draft conclusions, keep them decision-oriented: `继续扩大`, `保留但复跑`, `需要 ablation`, `回滚`, `停止该路线`, or `只作为分析材料`.
- For generation, avatar, reconstruction, simulation, embodied, or graphics experiments, include visual artifact paths and inspect geometry/rendering/failure samples before concluding.
- For qualitative figures or videos used to judge experimental quality, provide original-resolution source files by default. Scaled display in a document is acceptable, but thumbnails, compressed previews, cropped exports, or re-encoded low-resolution videos are not substitutes unless explicitly labeled as previews and linked to the original-resolution artifact.
- For experiments relevant to simulation-ready / physical plausibility / deployment, explicitly state whether the run improves simulation-capable assets, geometry, dynamics, controllability, or evaluation readiness.
- For models that use pretrained or open-source bases, report base model, checkpoint, frozen/fine-tuned/LoRA/direct-use status, and source evidence.

## Metrics, Tables, And Comparability

- Run or locate the actual evaluation output before writing metric claims.
- Round displayed scalar metrics consistently, normally to four decimal places unless the project standard differs.
- Keep raw run directory names, checkpoint paths, mask details, and command provenance outside metric cells when they make the table hard to read; put that provenance in the surrounding text or appendix.
- Mark metric direction explicitly when it matters, such as `PSNR ↑` or `LPIPS ↓`.
- Bold only the best value in each comparable metric column when the direction is known. Do not use background shading or bold method names unless the user asks.
- Do not mix incompatible masks, data splits, checkpoints, or evaluation scripts in one silent comparison. If mask or split differs, create a separate table or state the incompatibility directly.
- First-column identities such as method, subject, or sequence should be treated as row headers.
- If metrics are sensitive to foreground masks, cropping, alignment, frame selection, or pseudo-label quality, report that evaluation口径 next to the table.

## Visual And Artifact Rules

- Inspect representative images, videos, meshes, point clouds, or render outputs before writing qualitative conclusions.
- Use original-resolution image and video artifacts for qualitative judgment; if the report embeds a resized preview, include the path or link to the original-resolution file.
- Use the target platform's caption representation: native image captions in Feishu/Lark and Notion; the established vault convention in Obsidian, or meaningful Markdown alt text when no visible-caption convention exists. Do not duplicate the same caption as a separate paragraph.
- Present paired subjects, conditions, or before/after variants side by side when the report is making a visual comparison and the page format supports it.
- Use stable, stated column order for comparison grids. Include ground truth, baseline, current method, residuals/deltas, depth, normal, mask, or canonical views only when they are actually available and relevant.
- Use consistent color semantics for residual or delta maps and state the meaning of colors if the figure is not self-explanatory.
- Distinguish ambiguous artifacts explicitly, for example input mesh, canonical base mesh, refined mesh, posed mesh, Gaussian render, depth map, normal map, and novel-pose video. Do not substitute a generic visualization for a requested project-specific artifact.
- Preserve existing trusted images, videos, captions, and user-visible generated assets unless the user asks to replace them or they are clearly temporary.

## Environment And Reproducibility

Prefer Docker / Docker Compose for reproducible experiment environments and tmux for long-running jobs. If the run used conda or host Python, state that explicitly and explain whether it was a fallback.

Completed reports should include enough detail for a competent researcher to rerun or audit the result:

- exact command;
- config path and changed keys;
- commit hash / branch / dirty state if known;
- project/repo path and output root;
- container image or environment name;
- GPU model and count;
- seed and deterministic settings when relevant;
- data paths or dataset version;
- output/checkpoint/log paths.

Do not claim reproducibility if these are missing. Instead write a reproducibility gap and the smallest action to close it.

## Common Failure Modes

Avoid these:

- writing a polished story before reading logs or artifacts;
- explaining a result only after seeing it, without recording the prior prediction;
- reporting only the best metric or best image;
- omitting command/config/output paths;
- using run names as proof of settings without checking config, command, checkpoint, or logs;
- mixing multiple experiments into one vague conclusion;
- mixing incompatible masks, splits, stale runs, or non-comparable outputs as if they were directly comparable;
- treating environment setup success as method success;
- declaring improvement without baseline or confidence about metric direction;
- hiding failed samples, NaNs, empty outputs, bad renderings, or partial checkpoints;
- using thumbnails, downsampled images, or compressed videos as the only qualitative evidence;
- using standalone text paragraphs as Feishu image captions instead of native image captions;
- leaving `待核验`, TODO, or guessed fields in a completed report.

## Verification Checklist

Before calling a report complete, verify:

- the first conclusion callout answers what the minimum experiment verifies and what counts as success, its wording was fixed before the run, and its background is gray;
- source evidence was inspected and cited by path, command, table, log, or artifact;
- actual project convention, dedicated skill, or repo guide was checked when the user names a specific project;
- command, config, environment, data, and output path are present or explicitly missing;
- branch/commit, dirty state, project path, and output root are recorded when relevant;
- hypothesis and run-before prediction are recorded;
- baseline / previous-run comparison is present or its absence is stated;
- metrics and qualitative/raw output observations are both included when available;
- metric table comparability, direction, precision, and mask/split口径 are explicit;
- qualitative images/videos are original-resolution sources, or any resized previews are clearly linked to original-resolution artifacts;
- image captions use the target platform's native or established representation, with no duplicate standalone caption paragraphs;
- visual artifacts were inspected and captions/media placement were verified when the report includes media;
- failure cases or negative evidence are included;
- `1. Settings` is lean (method deltas + metadata only), not a full provenance questionnaire;
- if status is `失败` or `已暂停`, Settings metadata declares that status and a `6. Pause` section exists with decision, reason, evidence, and restart conditions;
- section headings use the short numbered English labels (`1. Settings` … `7. Appendix`), not Chinese titles;
- the user-provided first-question callout is preserved without post-hoc rewriting, and no final judgment was invented for the user;
- next step is the smallest useful action, not a vague research direction;
- reusable assets and document writeback targets are listed;
- no invented result, placeholder, unresolved `待核验`, or unsupported causal claim remains.
