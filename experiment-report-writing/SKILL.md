---
name: experiment-report-writing
description: Write source-grounded research experiment reports and experiment-log entries for ML/vision/graphics/robotics projects. Use when the user asks to整理/撰写/补全/审查实验报告, 实验记录, 训练报告, 评测报告, ablation report, baseline report, reproduction report, docs/Experiment.md entries, or Feishu experiment summaries.
---

# Experiment Report Writing

## Core Contract

Treat an experiment report as a decision artifact, not a diary. It must help the reader decide whether to trust the run, what changed relative to baseline, what the evidence says, and what the next smallest action should be.

Never invent results, metrics, hyperparameters, commands, environments, datasets, checkpoints, or qualitative observations. If logs or artifacts are missing, write the report as incomplete and list the exact missing evidence. If the experiment has not been run yet, write an experiment plan / pre-registration report, not a completed experiment report.

The leading conclusion is user-owned. Preserve the user's conclusion callout if it exists, or leave a concise conclusion callout placeholder for the user to fill. Do not write final conclusions, decisions, or causal judgments for the user unless explicitly asked to draft them from inspected evidence.

Default language is Chinese. Keep method names, dataset names, model names, config keys, file paths, command lines, metric names, and paper/system names in their original form when needed.

Keep this skill focused on report writing. Tool-specific delivery rules, Feishu editing steps, repository operations, and project-specific paths belong in the relevant workflow or project skill.

If a project has an existing report style, preserve its generic writing conventions such as numbered sections, section order, table style, and caption style. Do not copy project-specific paths, run names, or one-off implementation details into this general skill.

## Evidence Intake

Before writing a completed report, inspect or request the evidence needed for the claims:

- goal / hypothesis / run plan;
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
> 用户填写。Codex 不默认代写结论；若用户已提供结论，只做格式整理和位置保留。

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
- 问题：
- 假设：
- 运行前预测：
- 成功标准：
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

Use a conclusion-first callout followed by numbered headings in formal reports. Omit `2. 预处理` only when the experiment has no meaningful preprocessing, pseudo-label generation, alignment, filtering, or data conversion step; then renumber later sections so the report remains continuous.

Use this compact entry when appending to `docs/Experiment.md` or a running experiment log:

```markdown
### YYYY-MM-DD｜实验标题
- 结论：用户填写；Codex 不默认代写
- 目的：
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
- 背景问题：
- 假设：
- 运行前预测：
- 最小实验设置：
- 对照 / baseline：
- 成功标准：
- 失败时如何解释：
- 命令草案：
- 预计产物：
- 复盘时间：
```

## Writing Rules

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
- leaving `待核验`, TODO, or guessed fields in a completed report.

## Verification Checklist

Before calling a report complete, verify:

- source evidence was inspected and cited by path, command, table, log, or artifact;
- actual project convention, dedicated skill, or repo guide was checked when the user names a specific project;
- command, config, environment, data, and output path are present or explicitly missing;
- branch/commit, dirty state, project path, and output root are recorded when relevant;
- hypothesis and run-before prediction are recorded;
- baseline / previous-run comparison is present or its absence is stated;
- metrics and qualitative/raw output observations are both included when available;
- metric table comparability, direction, precision, and mask/split口径 are explicit;
- qualitative images/videos are original-resolution sources, or any resized previews are clearly linked to original-resolution artifacts;
- visual artifacts were inspected and captions/media placement were verified when the report includes media;
- failure cases or negative evidence are included;
- user-provided conclusion callout is preserved, or an empty conclusion callout is left for the user instead of an invented final judgment;
- next step is the smallest useful action, not a vague research direction;
- reusable assets and document writeback targets are listed;
- no invented result, placeholder, unresolved `待核验`, or unsupported causal claim remains.
