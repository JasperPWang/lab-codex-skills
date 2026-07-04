---
name: research-dev-standards
description: Enforces evidence-based reasoning, test-driven development, strict step order, small incremental changes, and pre-completion review (tensor shapes and core logic). Maintains RoadMap.md, docs/Experiment.md, and Q&A archives. Use when working on this repository’s research/training code, running or documenting experiments, or when the user mentions 科研开发规范 or similar workflow rules.
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
- 建议包含：实验目的、**完整或可复制命令**、关键超参与环境说明、主要结果（指标/现象）、**产物路径**（检查点、日志、图表、视频等）。

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
- [ ] 完成前是否核对维度与形状与核心逻辑？
- [ ] 是否更新了 `RoadMap.md` / `docs/Experiment.md` / Q&A 归档（如适用）？

## 附加资源

- 仓库内若存在根目录 `skills.md` 与本文重复时，以 **`.cursor/skills/research-dev-standards/SKILL.md`** 为代理侧权威副本；可择机将 `skills.md` 改为指向本 skill 的简短说明以避免双源漂移。
