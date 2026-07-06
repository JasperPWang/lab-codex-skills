---
name: research-dev-standards
description: Enforces evidence-based reasoning, test-driven development, tmux-first long-running sessions, Docker-first reproducible experiment environments, strict step order, small incremental changes, and pre-completion review (tensor shapes and core logic). Maintains RoadMap.md, docs/Experiment.md, and Q&A archives. Use when working on research/training code, configuring GPU/server experiment environments, running or documenting experiments, or when the user mentions 科研开发规范, 代码规范, 实验环境, Docker first, tmux first, Docker, tmux, or similar workflow rules.
---

# 科研开发规范（UniGAvatar）

在协助本仓库科研与开发时，默认遵循以下规范；与用户明确指令冲突时，以用户指令为准。

## 一、基础原则

### 基于证据

- 分析、结论、方案须建立在**实际代码、运行输出、实验指标或数据**之上。
- 在缺少可核验证据时，不臆测、不过度自信；应说明假设、建议如何验证（读代码、跑测试、小规模实验）。

### 测试驱动开发

- **先**有可执行的验证手段（单元测试、脚本断言、或约定的可视化/数值检查），**再**扩展实现。
- 功能到位后，用可视化与数据核对效果，再合并或宣称完成。

### 顺序执行

- 按约定步骤推进，**不擅自跳过**某一步。
- 若某步受阻：先说明阻塞原因与可选方案，与用户沟通后再继续；**仅**在用户明确授权时可临时跳过。

### 小步迭代

- 避免单次提交中堆叠大量未验证的模块、损失项或配置分叉。
- 优先小范围改动 → 验证 → 再下一处。

### 研究循环

- 每个重要实验或分析都应写成一个可校正循环：`假设 / 设置 / 预测 / 结果 / 更新后的判断 / 下一步最小动作`。
- 在运行前写下预测，训练对模型、数据、baseline、损失项和指标的品味；不要只在看到结果后解释。
- 优先缩短发现错误的时间：单命令运行、单命令画图、可复现 config、小数据切片、单 batch 过拟合检查。
- 看指标前后都要检查原始输出：可视化、失败样本、日志、几何结果、视频、渲染图或数据样例。
- 对失败样本做聚类：先攻击最大的失败堆，再决定是否扩大实验规模。
- 任何新增方法结论都要经受 baseline 调参、最小 ablation、数据/评价边界检查。

### 实验环境优先级：tmux first + Docker first

- 默认路线：**tmux first** 保证长任务不中断，**Docker first** / Docker Compose 保证环境可复现。
- 需要在服务器上跑实验、训练、下载数据、编译或长时间配置环境时，先进入 `tmux` 会话，再启动命令；不要把长任务裸跑在普通 SSH shell 里。
- 宿主机只保持最小稳定层：SSH、tmux、NVIDIA Driver、Docker、Docker Compose、NVIDIA Container Toolkit、存储挂载。
- 项目依赖默认进入容器：CUDA runtime、Python、PyTorch、系统库、编译依赖、项目包版本。
- 配新服务器或新项目环境时，先检查：
  - 项目是否已有 `Dockerfile` / `docker-compose.yml` / `.devcontainer`；
  - 服务器是否通过 `nvidia-smi`、`docker --version`、`docker compose version`；
  - `docker run --rm --gpus all ... nvidia-smi` 是否能看到 GPU；
  - 代码、数据、cache、checkpoints、outputs 是否挂载到稳定目录。
- 只有 Docker 不可用、权限不足或临时救急时，才用 conda / pip-on-host / system package 作为 fallback，并在结果中说明原因。
- 不静默接受 Anaconda Terms of Service，不随意修改全局 conda channels，不把项目依赖散装到宿主机。
- 环境完成的最低标准：容器内跑通项目最小验证命令，例如 `nvidia-smi`、核心 Python import、单 batch overfit、dry run 或 smoke test。

### 完成前审查

- 在宣称功能完成前，做一次针对性审查，重点包括：
  - **关键张量/数组的维度变换**是否与数据管线一致；
  - **输入输出形状**与 API 契约；
  - **分支与边界**下的逻辑是否正确。

---

## 二、文档维护（仓库根目录相对路径）

### 路线图：`RoadMap.md`

- 在讨论与实现功能过程中**同步更新**。
- 记录：当前分支相关功能、已知问题、待办与优先级（简明、可执行）。

### 实验记录：`docs/Experiment.md`（根目录 `Experiment.md` 为入口）

- 每次重要实验结束后**补充条目**。
- 建议包含：实验目的、**完整或可复制命令**、Docker 镜像/Compose 文件/容器入口、关键超参与环境说明、运行前预测、主要结果（指标/现象）、失败样本/原始输出观察、更新后的判断、下一步最小动作、**产物路径**（检查点、日志、图表、视频等）。

### Q&A 归档

- 对用户问题在基于代码与数据给出可靠解答后，将**问题摘要 + 结论要点 + 必要时引用路径/命令**写入归档。
- 默认归档文件：若不存在则创建 `docs/Q&A.md`（若项目已另有约定文件，则写入约定处并在此 skill 中保持一致）。

---

## 执行清单（代理自检）

开始复杂任务前可快速对照：

- [ ] 结论是否有代码/运行/实验依据？
- [ ] 是否有测试或可重复验证步骤？
- [ ] 是否按步骤执行，未擅自跳步？
- [ ] 改动是否小步、可回滚？
- [ ] 实验/分析是否写下 `假设 / 设置 / 预测 / 结果 / 更新后的判断 / 下一步最小动作`？
- [ ] 长任务是否先进入 `tmux` 会话，而不是裸跑在 SSH shell？
- [ ] 实验环境是否优先走 Docker/Compose，而不是散装到宿主机？
- [ ] 是否验证了容器内 GPU、核心 import、smoke test 或单 batch 运行？
- [ ] 是否检查了原始输出和失败样本，而不只看平均指标？
- [ ] 是否有单命令运行、画图、config 或小数据验证来缩短发现错误的时间？
- [ ] 完成前是否核对维度与形状与核心逻辑？
- [ ] 是否更新了 `RoadMap.md` / `docs/Experiment.md` / Q&A 归档（如适用）？

## 附加资源

- 仓库内若存在根目录 `skills.md` 与本文重复时，以 **`.cursor/skills/research-dev-standards/SKILL.md`** 为代理侧权威副本；可择机将 `skills.md` 改为指向本 skill 的简短说明以避免双源漂移。
