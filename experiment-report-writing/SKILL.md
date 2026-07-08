---
name: experiment-report-writing
description: Write source-grounded research experiment reports and experiment-log entries for ML/vision/graphics/robotics projects. Use when the user asks to整理/撰写/补全/审查实验报告, 实验记录, 训练报告, 评测报告, ablation report, baseline report, reproduction report, docs/Experiment.md entries, or Feishu experiment summaries.
---

# Experiment Report Writing

## Core Contract

Treat an experiment report as a decision artifact, not a diary. It must help the reader decide whether to trust the run, what changed relative to baseline, what the evidence says, and what the next smallest action should be.

Never invent results, metrics, hyperparameters, commands, environments, datasets, checkpoints, or qualitative observations. If logs or artifacts are missing, write the report as incomplete and list the exact missing evidence. If the experiment has not been run yet, write an experiment plan / pre-registration report, not a completed experiment report.

Default language is Chinese. Keep method names, dataset names, model names, config keys, file paths, command lines, metric names, and paper/system names in their original form when needed.

When writing to Feishu, also use `feishu-doc-workflow` and local `lark-cli`; do not use browser operations. When documenting an experiment in a code repo, also follow `research-dev-standards`.

## Evidence Intake

Before writing a completed report, inspect or request the evidence needed for the claims:

- goal / hypothesis / run plan;
- exact command, script, config, branch, commit, seed, data split, checkpoint, and output directory;
- machine and environment: GPU, CUDA, driver, Docker image / Compose service / conda env, Python and key package versions when relevant;
- logs: stdout/stderr, TensorBoard/W&B tables, evaluation JSON/CSV, training curves, failure traces;
- artifacts: checkpoints, rendered images/videos, qualitative samples, figures, screenshots, meshes, point clouds, tables;
- baseline or prior run for comparison;
- known failure cases, raw outputs, and any manual filtering.

If evidence is too large, sample deterministically and say what was inspected. Prefer exact paths and commands over vague provenance.

## Required Structure

Use this structure for a full completed experiment report:

```markdown
# 实验标题

一句话结论：...

## 1. 实验语境
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

## 2. 问题与假设
- 问题：
- 假设：
- 运行前预测：
- 成功标准：

## 3. 实验设置
- 变量：
- 对照 / baseline：
- 固定条件：
- 指标：
- 评测流程：

## 4. 结果
| Run | 关键设置 | 指标 / 现象 | 产物 | 备注 |
|---|---|---|---|---|

## 5. 原始输出与失败样本观察
- 代表性成功样本：
- 代表性失败样本：
- 失败模式聚类：
- 日志 / 可视化异常：

## 6. 分析与判断
- 与预测是否一致：
- 相比 baseline / 上次运行：
- 可信结论：
- 仍不能下的结论：
- 最大混淆因素：

## 7. 结论与决策
- 决策：
- 理由：
- 风险：

## 8. 下一步最小动作
1. ...
2. ...
3. ...

## 9. 资产沉淀
- 可复用命令 / config：
- 可复用图表 / 样例：
- 需要写回的文档：
```

Use this compact entry when appending to `docs/Experiment.md` or a running experiment log:

```markdown
### YYYY-MM-DD｜实验标题
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
- Keep conclusions decision-oriented: `继续扩大`, `保留但复跑`, `需要 ablation`, `回滚`, `停止该路线`, or `只作为分析材料`.
- For generation, avatar, reconstruction, simulation, embodied, or graphics experiments, include visual artifact paths and inspect geometry/rendering/failure samples before concluding.
- For experiments relevant to simulation-ready / physical plausibility / deployment, explicitly state whether the run improves simulation-capable assets, geometry, dynamics, controllability, or evaluation readiness.
- For models that use pretrained or open-source bases, report base model, checkpoint, frozen/fine-tuned/LoRA/direct-use status, and source evidence.

## Environment And Reproducibility

Prefer Docker / Docker Compose for reproducible experiment environments and tmux for long-running jobs. If the run used conda or host Python, state that explicitly and explain whether it was a fallback.

Completed reports should include enough detail for a competent researcher to rerun or audit the result:

- exact command;
- config path and changed keys;
- commit hash / branch / dirty state if known;
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
- mixing multiple experiments into one vague conclusion;
- treating environment setup success as method success;
- declaring improvement without baseline or confidence about metric direction;
- hiding failed samples, NaNs, empty outputs, bad renderings, or partial checkpoints;
- leaving `待核验`, TODO, or guessed fields in a completed report.

## Verification Checklist

Before calling a report complete, verify:

- source evidence was inspected and cited by path, command, table, log, or artifact;
- command, config, environment, data, and output path are present or explicitly missing;
- hypothesis and run-before prediction are recorded;
- baseline / previous-run comparison is present or its absence is stated;
- metrics and qualitative/raw output observations are both included when available;
- failure cases or negative evidence are included;
- conclusions state what can and cannot be concluded;
- next step is the smallest useful action, not a vague research direction;
- reusable assets and document writeback targets are listed;
- no invented result, placeholder, unresolved `待核验`, or unsupported causal claim remains.
