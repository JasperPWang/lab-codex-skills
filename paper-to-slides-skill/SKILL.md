---
name: paper-to-slides
description: >-
  从论文 PDF Workflow：本地 MinerU 提取 Markdown，在 Cursor/Codex 会话内生成 Marp 幻灯（不使用额外 LLM/生图 API），再本地导出 pptx/PDF。Use when the user wants paper-to-slides, paper to PPT, thesis deck, or Marp export without OpenAI/Gemini/OpenRouter keys.
metadata:
  short-description: 论文 PDF → Marp（零额外交互 API）
  disable-model-invocation: true
---

# Paper → Slides（本地工具 + 会话内模型）

## 目标与硬约束

- **产出**：可演讲的幻灯片（优先 **Marp** 源文件 → 导出 **PPTX / PDF**）。
- **禁止**：为本工作流单独购买或配置 **OpenAI / Anthropic / Gemini / OpenRouter** 等**外部**推理或生图 API。  
  **允许且推荐**：在 **Cursor / Codex 已订阅的会话内**完成提纲、叙事、逐页文案与 Marp 生成（这不算「再买 API」）。
- **本地解析**：PDF → Markdown 使用 **MinerU** 包装脚本（`.tools/mineru-md.sh`）；脚本保存在 vault 内，Python 环境默认保存在本机 `~/Library/Application Support/WorldModelVault/envs/`，与 `Vault Setup.md` 一致。

不要使用 **HKUDS/Paper2Slides** 等默认依赖云端 Key 的一键工具，除非用户明确说已自行改为全本地后端（本 skill 不展开）。

## 何时启用

用户在做：组会幻灯、读书报告、论文分享、把项目中的 PDF 变成可讲 deck，且希望 **skill 化、可重复、不绑新 API**。

## 推荐目录（可按项目调整）

- **MinerU 输出**（中间产物）：`3-Projects/<项目>/assets/mineru-out/<论文短名>/` 或 `2-Learnings/EmbodiedWorld/assets/mineru-out/<短名>/`
- **Marp 源文件**：`3-Projects/<项目>/decks/YYYY-MM-DD-<论文短名>.md`（或同级 `decks/` 下）
- **导出 PPTX/PDF**：与 `.md` 同目录的 `exports/`，避免和 Obsidian 笔记 clutter

若用户已在 `3-Projects/.../Paper Cards.md` 有 paper card，可优先对齐其中的标题、链接与配图路径。

## 工作流（Agent 按顺序执行）

1. **确认输入**  
   PDF 路径；听众（导师/同门/外行）；时长或页数上限；语言（中文/英文）。

2. **本地提取**（若尚无可靠 Markdown）  
   在 vault 根执行：
   ```bash
   .tools/mineru-md.sh "/path/to/paper.pdf" "3-Projects/<项目>/assets/mineru-out/<短名>"
   ```
   在输出目录中找到主 Markdown（以 MinerU 实际结构为准，常为 `*.md` 或子目录中的 md）。

3. **在会话内理解论文**  
   阅读 MinerU md（与必要图片路径）；整理：问题、方法、实验、结论、限制；标出**必须在幻灯上出现的图**（用相对 Marp 文件的路径或复制/引用到 `decks/assets/`）。

4. **生成 Marp 文稿**  
   新建或更新 `decks/...md`，包含：
   - 顶部 YAML：`marp: true`、`theme`（若用户无偏好用 `default` 或 `gaia`）、`paginate: true`、`size: 16:9`
   - 每页用 `---` 分页；标题页、大纲、贡献/方法、实验、结论、备份页（可选）
   - 正文以 bullet 为主，避免长段粘贴；数字与主张需可在 md 中溯源
   - 图片：`![](相对路径)`，确保相对 Marp 文件可解析

5. **导出（用户本机，Agent 只给命令）**  
   - 已装 **Marp CLI** 时示例：
     ```bash
     marp decks/YYYY-MM-DD-foo.md --pptx -o exports/YYYY-MM-DD-foo.pptx
     marp decks/YYYY-MM-DD-foo.md --pdf  -o exports/YYYY-MM-DD-foo.pdf
     ```
   - 若仅用 **VS Code / Cursor 的 Marp 扩展**，说明用扩展导出即可。

6. **质量检查清单（口头提醒用户）**  
   字体是否嵌入、公式是否需截图、图是否模糊、是否需加一句「复现/数据来自原文表 X」。

## Marp 最小示例（写入真实文件时按论文替换）

```markdown
---
marp: true
theme: default
paginate: true
size: 16:9
---

# 论文标题
作者（会议 / arXiv） · 你的名字 · YYYY-MM-DD

---

# 我们在讲什么
- 问题：…
- 挑战：…

---

# 方法概览
- …

![width:600px](../assets/mineru-out/foo/figures/fig1.png)

---

# 实验与结论
- …
```

## 与 llm-wiki / paper card 的关系

- **Paper card**（`####` 标题块）：适合文献档案与精读笔记。  
- **本 skill**：面向**口述叙事**与**分页结构**，输出 Marp/PPTX。  
二者可链接同一批 `assets/` 图，但不要互相覆盖「唯一真源」：MinerU md 保持提取层；Marp 保持演讲层。

## 常见分叉

| 需求 | 做法 |
|------|------|
| 只要提纲、不要文件 | 仍按步骤 3 输出分页大纲，由用户贴进 Keynote |
| PDF 已是幻灯式逐页 | 考虑矢量保留的 pdf→pptx 工具；本 skill 仍以「论文全文」为主场景 |
| 公式很多 | Marp 有限；建议关键式一行展示，其余放附录页或截图 |

## Agent 自检

- 是否**避免**引导用户配置新的云端 API？
- 是否优先 **mineru-md.sh** 而非要求用户手抄 PDF？
- Marp 里图片路径是否**相对于 md 文件**可打开？
- 是否把**导出命令**写清楚，而不是假设用户已熟悉 Marp？
