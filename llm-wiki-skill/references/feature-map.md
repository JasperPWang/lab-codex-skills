# 功能映射

这个文件说明如何把 LLM Wiki 原始思路和 `nashsu/llm_wiki` 的功能，映射成 Codex 原生 skill。

## 可以完整支持

- 原始资料 → 生成 wiki → schema/purpose 的三层架构。
- 外层资料池 → 精选 `raw` 证据库 → 编译后 `wiki` 理解层的边界。
- `2-Learnings/EmbodiedWorld/`、`2-Learnings/Courses/`、`0-Daily/`、`1-Meetings/` 作为宽输入池，`4-Research-Wiki/raw/` 作为精选输入层。
- Ingest / Query / Lint 三个核心操作。
- `index.md`、`overview.md`、只追加的 `log.md`。
- Obsidian 兼容 Markdown 和 `[[wikilinks]]`。
- 带页面类型、状态、日期、来源、标签的 YAML frontmatter。
- 来源可追溯。
- 两步摄入：先分析，再生成 wiki。
- 文件夹导入：把资料放到 `raw/sources/` 即可。
- SHA256 manifest：用于增量检测和跳过未变化文件。
- `wiki/reviews.md` 人工审核队列。
- `wiki/research.md` 深度研究队列。
- 查询答案可保存到 `wiki/queries/`。
- 基于链接和共享来源的知识图谱分析。
- Lint 检查：缺 frontmatter、断链、孤立页面、source 引用问题。

## 可以用替代方案支持

- Activity panel：用 `wiki/log.md` 和 `.llm-wiki/queue.json` 替代。
- 知识图谱 UI：用 `.llm-wiki/graph.json`、Markdown 表格和 Mermaid 替代。
- Louvain 社区检测：默认用 connected components 和 cohesion 启发式；如果以后接入图算法库再增强。
- 图谱洞察：从 `graph` 输出生成 Markdown 洞察列表。
- 向量语义搜索：默认用关键词搜索 + 图谱扩展；用户愿意时再接 qmd、embedding 或向量库。
- 多聊天会话：把有长期价值的回答保存到 `wiki/queries/`；实时对话使用当前 Codex 会话。
- 浏览器剪藏：把网页剪藏或 Markdown 笔记保存到 `raw/sources/`；需要时让 Codex 联网浏览并归档。
- Source 文件夹监听：通过运行 `manifest` 显式检测新增、修改、删除。
- 多格式文档：Codex 使用本地可用工具提取文本；如果提取失败，写入 review item。

## Skill 不能原生提供

- 桌面 App 窗口、侧边栏、可拖动面板、实时预览面板。
- 由 App 控制的实时流式聊天 UI 和聊天 JSON 持久化。
- Chrome 扩展和本地 HTTP bridge。
- Tauri 文件选择器和 OS 级应用行为。
- Codex 不运行时的后台自动队列执行。
- 内嵌 LanceDB 向量索引，除非另外实现或接入外部工具。

## 实用原则

当某个功能不能作为常驻 App 功能实现时，保留它的信息效果：

- UI 状态 → Markdown/JSON 状态。
- 实时事件 → 显式同步命令。
- 可视化图谱 → 图谱报告。
- App 设置 → `schema.md`。
- 人机协作弹窗 → review queue。

摄入边界原则：

- 外层资料池可以宽，`4-Research-Wiki/raw` 必须精选，`4-Research-Wiki/wiki` 必须编译。
- 没有 property/frontmatter 的原始文档也可以被选入 `raw`；property 不是准入门槛。
- 生成的 wiki 页面必须有 frontmatter，因为它们是长期维护对象。
- 判断材料是否进入 wiki，看它是否能生成或更新 concept、claim、question、synthesis 或 research-practice。
