---
name: experiment-report-writing
description: Write source-grounded research experiment reports and experiment-log entries for ML/vision/graphics/robotics projects across Feishu/Lark, Notion, and Obsidian/Markdown. Use when the user asks to整理/撰写/补全/审查实验报告, 实验记录, 训练报告, 评测报告, ablation report, baseline report, reproduction report, docs/Experiment.md entries, or research-document experiment summaries.
---

# Experiment Report Writing

## Core Contract

Treat an experiment report as a decision artifact, not a diary. It must help the reader decide whether to trust the run, what changed relative to baseline, what the evidence says, and what the next smallest action should be.

Never invent results, metrics, hyperparameters, commands, environments, datasets, checkpoints, or qualitative observations. If logs or artifacts are missing, write the report as incomplete and list the exact missing evidence. If the experiment has not been run yet, write an experiment plan / pre-registration report, not a completed experiment report.

The leading conclusion callout is user-owned and has one fixed purpose: record the first question and its answer before the experiment runs. It must state what the minimum experiment is intended to verify and the precommitted success standard. Preserve the user's answer, or help make supplied intent falsifiable and measurable without inventing it. Do not rewrite this callout after seeing results; if the verification target or success standard changes, create a new experiment entry. Do not write final conclusions, decisions, or causal judgments for the user unless explicitly asked to draft them from inspected evidence.

Default language is Chinese. Keep method names, dataset names, model names, config keys, file paths, command lines, metric names, and paper/system names in their original form when needed.

Keep this skill focused on report writing. Also use [`research-doc-workflow`](../research-doc-workflow/SKILL.md) for platform selection and durable delivery to Feishu, Notion, or Obsidian. Tool-specific editing steps, repository operations, and project-specific paths belong in that workflow or the relevant project skill.

If a project has an existing report style, preserve its generic writing conventions such as numbered sections, section order, table style, and caption style. Do not copy project-specific paths, run names, or one-off implementation details into this general skill.

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

## 1. 实验设置
- 项目：
- 实验日期：
- 负责人 / 执行者：
- 代码版本：
- 机器 / GPU：
- 环境：
- 数据 / split：
- 配置 / checkpoint：
- 命令：
- 产物路径：
- 核心假设：
- 最高风险假设：
- 运行前预测：
- 反驳 / 无法判定条件：
- 资源上限：
- 变量：
- 对照 / baseline：
- 固定条件：
- 指标：
- 评测流程：

## 2. 预处理（如适用）
- 数据清洗 / mask / 对齐 / 裁剪：
- 伪标签 / 中间产物：
- 过滤规则：
- 预处理对结果解释的影响：

## 3. 定量实验
- 评测口径：
- 指标方向：
- 结果表：
- 相比 baseline / 上次运行：
- 定量分析：
- 统计或可比性 caveat：

## 4. 定性实验
- 代表性成功样本：
- 代表性失败样本：
- 原分辨率图像 / 视频：
- 图像原生图注：
- 可视化 / render / geometry / video 观察：
- 失败模式：
- 定性分析：

## 5. 下一步最小动作
1. ...
2. ...
3. ...

## 6. 附录
- 可复用命令 / config：
- 可复用图表 / 样例：
- 原始日志 / 指标文件 / 产物路径：
- 需要写回的文档：
```

Use the conclusion callout immediately after the title to preserve the first question and its user-owned answer. Keep the same Markdown report on every platform; only map the semantic callout marker to a native callout in Feishu or Notion when supported. Create and freeze it before the run; do not replace it with a post-hoc result summary. Follow it with numbered headings. Omit `2. 预处理` only when the experiment has no meaningful preprocessing, pseudo-label generation, alignment, filtering, or data conversion step; then renumber later sections so the report remains continuous.

Use this compact entry when appending to `docs/Experiment.md` or a running experiment log:

```markdown
### YYYY-MM-DD｜实验标题

> [!结论]
> **第一问题：这个最小实验要验证什么？成功的标准是什么？**
> - 验证目标：<一句可证伪的陈述>
> - 成功标准：<预先确定的指标、阈值或明确的可观察条件>

- 假设 / 预测：
- 命令：
- 环境：
- 关键设置：
- 结果：
- 原始输出观察：
- 结论边界：
- 下一步：
- 产物：
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

- Put the first question and answer in the first conclusion callout immediately after the title. Write and freeze it before execution; never retrofit the verification target or success threshold to match observed results.
- Keep both answers concrete: the verification target must be falsifiable, and the success standard must be a metric, threshold, or unambiguous observable condition. Treat `效果不错`, `看起来可行`, or equivalent wording as incomplete.
- Separate evidence from interpretation. Use phrases like `日志显示`, `指标表明`, `可视化显示`, and `我的判断是` to distinguish source-backed observation from analysis.
- Always compare against a baseline, previous run, or explicit expectation when possible. If no baseline exists, say so and propose the smallest baseline to add.
- Report both metrics and raw outputs. Do not conclude from aggregate metrics alone when qualitative artifacts exist.
- Include failed or ugly samples. A report with only cherry-picked images is not complete for research judgment.
- Record negative and inconclusive results clearly. A failed run can still be a useful report if it identifies a broken assumption, bad config, data issue, or next diagnostic.
- If the result is still running, write `状态：运行中` and include current evidence only; do not write final conclusions.
- If an experiment failed before producing metrics, report failure stage, error snippet, likely cause, and the next diagnostic command.
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

- the first conclusion callout answers what the minimum experiment verifies and what counts as success, and its wording was fixed before the run;
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
- the user-provided first-question callout is preserved without post-hoc rewriting, and no final judgment was invented for the user;
- next step is the smallest useful action, not a vague research direction;
- reusable assets and document writeback targets are listed;
- no invented result, placeholder, unresolved `待核验`, or unsupported causal claim remains.
