---
name: lark-whiteboard
description: >
  飞书画板：查询和编辑飞书云文档中的画板。支持导出画板为预览图片、导出原始节点结构、使用多种格式更新画板内容。
  当用户需要查看画板内容、导出画板图片、编辑画板时使用此 skill。不负责：飞书云文档正文编辑、文档层级、图片/表格布局保护，这些统一交给 feishu-doc-workflow。
---

# Local Requirements

- Skill version: `1.0.0`.
- Required CLI: `lark-cli`.
- Useful help command: `lark-cli whiteboard --help`.

> [!IMPORTANT]
> - 运行 `lark-cli --version`，确认可用，无需询问用户。
> - 运行 `npx -y @larksuite/whiteboard-cli@^0.2.11 -v`，确认可用，无需询问用户。

**CRITICAL — 如果任务涉及飞书文档/知识库 URL、在文档中创建画板、或需要保护正文/图片/表格/层级，先使用 [`feishu-doc-workflow`](../feishu-doc-workflow/SKILL.md)。本 skill 只负责画板 token 级别的查询与更新。**

---

## 快速决策

**身份**：画板操作默认使用 `--as user`。仅当需要以应用身份上传时使用 `--as bot`。

**Feishu mind-map bilingual rule**: when creating or repairing a Feishu native mind map for the user's research-map / literature-review pages, every visible node must be bilingual in this exact form: English on the first line, Chinese on the second line. Do not deliver all-English mind maps. If PlantUML `\n` imports as a literal backslash-n string, or `<br/>` breaks the preview, query `--output_as raw`, patch each native `mind_map` node's `text.text` to contain an actual newline character, write back with `+update --input_format raw --overwrite`, and export an image preview to verify the two-line English/Chinese rendering.

| 用户需求                                    | 行动                                                                                            |
|-----------------------------------------|-----------------------------------------------------------------------------------------------|
| 查看画板内容 / 导出图片                           | [`+query --output_as image`](references/lark-whiteboard-query.md)                             |
| 获取画板的 Mermaid/PlantUML 代码               | [`+query --output_as code`](references/lark-whiteboard-query.md)                              |
| 检查画板是否由代码绘制                             | [`+query --output_as code`](references/lark-whiteboard-query.md)                              |
| 修改节点文字/颜色（简单改动）                         | `+query --output_as raw` → 手动改 JSON → `+update --input_format raw`                            |
| 用户**已提供** Mermaid/PlantUML 代码，或明确指定用该格式 | 自己生成/使用代码 → [`+update --input_format mermaid/plantuml`](references/lark-whiteboard-update.md) |
| 新建/创作复杂图表（架构/流程/组织等）                    | → **[§ 创作 Workflow](references/lark-whiteboard-workflow.md#创作-workflow)**                     |
| 修改/重绘已有画板                               | → **[§ 修改 Workflow](references/lark-whiteboard-workflow.md#修改-workflow)**                     |

## Shortcuts

| Shortcut | 说明 |
|---|---|
| [`+query`](references/lark-whiteboard-query.md) | 查询画板，导出为预览图片、代码或原始节点结构 |
| [`+update`](references/lark-whiteboard-update.md) | 更新画板，支持 PlantUML、Mermaid 或 OpenAPI 原生格式 |

---

## 不在本 skill 范围
- 文档内容编辑、文档层级、正文图片/表格布局保护、在文档中创建画板 → [`feishu-doc-workflow`](../feishu-doc-workflow/SKILL.md)
- 表格 / Base 操作不由本 skill 处理；若画板任务涉及这些内容，先明确数据来源和目标文档，再由合适的表格或飞书文档工作流接管。
