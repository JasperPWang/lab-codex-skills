# Lab Agent Skills

This directory is the canonical source for the **Human Centric Intelligence Lab** skill bundle. It keeps user-maintained skills and vendored/downloaded skills together so the same research workflows can be shared across Macs and used by **any agent platform** that loads `SKILL.md` (Codex, Cursor, Antigravity, Claude Code, and similar).

Public GitHub mirror: [https://github.com/JasperPWang/lab-codex-skills](https://github.com/JasperPWang/lab-codex-skills)  
(The repository name is historical; the bundle is **not** Codex-only.)

## What This Bundle Supports

### Agent platforms

Skills are ordinary directories with a `SKILL.md`. Install scripts create **symlinks** into common discovery roots; you can also point any agent at this folder manually:

| Platform | Typical link target | Script |
| --- | --- | --- |
| Codex | `~/.codex/skills/` | `scripts/link-to-codex-skills.sh` |
| Cursor (project) | `<vault>/.cursor/skills/` | `scripts/link-to-cursor-skills.sh` |
| Antigravity / agent-local | `<vault>/.agents/skills/` | `scripts/link-to-antigravity-skills.sh` |
| Other agents | Set their skill root to this bundle or copy/symlink `SKILL.md` trees | — |

`bash install.sh` links Codex always; when run from WorldModelVault’s `.tools/skills/`, it also links Cursor and Antigravity.

### Note / document backends

Research **content** skills are Markdown-first and platform-neutral. [`research-doc-workflow`](research-doc-workflow/SKILL.md) routes the same structure to the destination you name (URL or explicit path). Thin adapters apply only format deltas:

| Backend | Adapter skill | Notes |
| --- | --- | --- |
| **Feishu / Lark** | [`feishu-doc-workflow`](feishu-doc-workflow/SKILL.md) | Native wiki/docs via `lark-cli`; whiteboards via `lark-whiteboard` when needed |
| **Notion** | [`notion-doc-workflow`](notion-doc-workflow/SKILL.md) | Native pages/databases, properties, equations, captions; re-fetch verification |
| **Obsidian / Markdown** | [`obsidian-doc-workflow`](obsidian-doc-workflow/SKILL.md) | Vault paths, callouts, frontmatter, wikilinks, relative assets; pair with `llm-wiki-skill` for wiki ingestion |

Resolve the backend from the user’s **link or explicit instruction**. Do not silently default to Feishu or redirect one backend to another. Preserve the platform of an existing document.

## Rules

- Put every editable skill under `.tools/skills/<skill-name>/` (or the root of this repo when cloned standalone).
- Treat `~/.codex/skills/<skill-name>`, `.cursor/skills/`, and `.agents/skills/` as **compatibility symlinks** only—edit the canonical copy here.
- Do not edit copied skill directories in multiple places.
- Keep system, bundled, plugin-cache, and runtime skills outside this repository. Vendored third-party suites may live here when provenance is recorded in `THIRD_PARTY_NOTICES.md`.
- After changing a skill, run its validator if present, or `scripts/validate-all.sh`.

Before publishing or sharing, review:

- `SKILL_MANIFEST.md`
- `THIRD_PARTY_NOTICES.md`
- `.gitignore`

## Copy-Paste Setup Prompt

Paste into Codex, Cursor, Antigravity, or another agent on a teammate’s machine:

```text
请帮我配置 Human Centric Intelligence Lab 的 agent skill bundle。

目标：
1. 从 GitHub 克隆公开仓库：https://github.com/JasperPWang/lab-codex-skills
2. 放到本机稳定位置，例如 ~/lab-codex-skills；若目录已存在，先 fetch/pull 更新，不要删除本地修改。
3. 运行 install.sh：链到 ~/.codex/skills；若在 Cursor/Antigravity 工作区使用，按 README 再链到 .cursor/skills 或 .agents/skills。
4. 运行 scripts/validate-all.sh，确认 skill 通过校验。
5. 确认能看到 research-doc-workflow、paper-card-delivery、paper-deep-dive、feishu-doc-workflow、notion-doc-workflow、obsidian-doc-workflow、survey-builder、ai-research-workflow、chinese-technical-writing 等常用入口。
6. 检查三类笔记后端：Obsidian/Markdown 是否可读写；Notion connector 是否已连接；若要编辑飞书原生文档，再检查 ~/.local/bin/lark-cli doctor。缺少后端时只说明需要配置，不要猜测或写入任何 token / secret。
7. 用中文总结：安装目录、校验结果、常用 prompt，以及 Feishu / Notion / Obsidian 是否就绪。

约束：
- 不要把 access token、refresh token、app secret、cookie、私有 Feishu 链接写进仓库或聊天。
- 同名普通目录先备份，不要直接覆盖；symlink 可以安全重建。
- 命令失败时先诊断，不要假装安装成功。
```

On a new machine:

```bash
# Standalone clone:
git clone https://github.com/JasperPWang/lab-codex-skills.git ~/lab-codex-skills
cd ~/lab-codex-skills
bash install.sh

# From WorldModelVault on this machine:
bash ".tools/skills/install.sh"
```

Standalone Cursor / Antigravity linking examples:

```bash
CURSOR_SKILL_ROOT=/path/to/project/.cursor/skills bash scripts/link-to-cursor-skills.sh
AGENT_SKILL_ROOT=/path/to/project/.agents/skills bash scripts/link-to-antigravity-skills.sh
```

Validate:

```bash
bash scripts/validate-all.sh
# or from the vault:
bash ".tools/skills/scripts/validate-all.sh"
```

Export a clean GitHub-ready copy:

```bash
bash scripts/export-github-bundle.sh /tmp/lab-codex-skills
```

## Document Backends (detail)

Common research-content skills stay Markdown-first. `research-doc-workflow` keeps headings, lists, tables, links, code, and LaTeX aligned across backends. Only callouts, captions, properties/frontmatter, hierarchy, editable diagrams, citation chrome, uploads, and verification use thin adapters:

- **Obsidian**: `obsidian-doc-workflow` (+ `llm-wiki-skill` when ingesting the Research Wiki).
- **Notion**: `notion-doc-workflow` (native properties, one-paragraph paper-card metadata with `<br>`, re-fetch).
- **Feishu/Lark**: `feishu-doc-workflow` + authenticated `lark-cli`.

### Feishu Native Editing Prerequisite

```bash
~/.local/bin/lark-cli doctor
```

Useful checks:

```bash
~/.local/bin/lark-cli docs +fetch --help
~/.local/bin/lark-cli docs +update --help
~/.local/bin/lark-cli docs +media-insert --help
~/.local/bin/lark-cli wiki --help
```

Configuration is user-local under `~/.lark-cli/`. Do not commit secrets into this repository.

## Integration Policy

Personal lab skills own final deliverables. Downloaded skills can provide methods and checklists, but must not override the user’s semantic content contract or the selected Feishu / Notion / Obsidian representation.

- Deep dives may borrow `nature-reader` methods, then deliver the lab package via `paper-deep-dive`.
- `paper-deep-dive` is the single canonical deep-dive delivery standard.
- Literature reviews may borrow `deep-research` methods, then deliver via `survey-builder`.
- Paper cards remain governed by `paper-card-delivery`.
- Cross-platform routing is governed by `research-doc-workflow`; each backend’s native blocks stay in its `*-doc-workflow` adapter.

## Research Workflow Skill Map

Use short daily prompts. The agent should select the skill stack and only ask when missing context would change the result.

| Research step | Daily prompt | Main skills |
| --- | --- | --- |
| Cross-platform page editing | `帮我整理/规范这个 Notion、Obsidian 或飞书页面` | `research-doc-workflow`, matching `*-doc-workflow`, `chinese-technical-writing` |
| Paper cards | `帮我补全这个页面/笔记的 paper card` | `paper-card-delivery`, `research-doc-workflow`, matching adapter |
| Single-paper deep dive | `帮我 deep dive 一下这篇论文，写到指定平台` | `paper-deep-dive`, `paper-card-delivery`, `research-doc-workflow`, matching adapter |
| Literature tree / survey | `帮我把这个方向整理成 literature tree` | `survey-builder`, `ai-research-workflow`, `deep-research` |
| Broad field exploration | `帮我调研这个方向，给我研究路线图` | `deep-research`, `academic-research-suite`, `nature-academic-search` |
| Concept learning | `帮我讲清楚这个概念/方法` | `feynman-learning` |
| Local wiki ingestion | `把这份材料纳入我的本地研究 wiki` | `llm-wiki-skill`, `obsidian-doc-workflow`, `chinese-technical-writing` |
| Manuscript planning/writing | `帮我搭论文框架/写引言/改摘要` | `nature-writing`, `paper-spine`, `academic-paper` |
| Manuscript polishing | `帮我润色这段英文论文文字` | `nature-polishing` |
| Citation verification | `帮我核验这些引用是否真的支撑论断` | `cite-verify`, `nature-citation` |
| Figures and plots | `帮我把这张图做成论文级图表` | `nature-figure` |
| Statistics sanity check | `帮我检查这些实验表格和 p 值是否一致` | `stats-sanity` |
| Experiment report / log | `帮我把这次运行整理成实验报告` | `experiment-report-writing`, `research-dev-standards` |
| Reproducibility / release | `帮我整理这个项目的复现包` | `repro-pack` |
| Mock review / rebuttal | `帮我从审稿人角度审一下/回审稿意见` | `academic-paper-reviewer`, `nature-reviewer`, `nature-response` |
| Grant / proposal | `帮我搭这个基金/博士课题 proposal` | `grant-writer` |
| Daily review | `帮我做今天的科研经营复盘` | `daily-research-review` |

## Downloaded Skills Worth Using

| Skill | Best use | Example prompt |
| --- | --- | --- |
| `deep-research` | Fuzzy new direction: questions, sources, synthesis, risks | `帮我调研 …，给我问题树、关键论文和研究空白。` |
| `academic-research-suite` | Heavier academic pipeline coordination | `帮我把这个方向整理成可写论文的 research plan。` |
| `nature-academic-search` | Multi-source search and BibTeX | `帮我检索 … 核心论文并导出 BibTeX。` |
| `cite-verify` | Claim–citation alignment | `帮我核验这些引用是否支持每一句 claim。` |
| `nature-reader` | Standalone bilingual reading; use `paper-deep-dive` for the lab package | `帮我做这篇论文的中英文对照精读。` |
| `nature-writing` / `nature-polishing` | Drafting and English polish | `帮我组织 introduction / 润色这段文字。` |
| `nature-figure` | Paper-grade figures | `用 Python 画论文级 figure。` |
| `stats-sanity` | Numeric consistency | `检查表与正文数字是否一致。` |
| `repro-pack` | Release / handoff | `整理成可复现包。` |
| `paper-spine` | End-to-end manuscript build | `基于这些材料搭完整论文草稿。` |
| `academic-paper-reviewer` / `nature-reviewer` / `nature-response` | Review and rebuttal | `从审稿人角度审 draft / 整理逐点回复。` |
| `grant-writer` | Proposals | `搭 proposal 的 aims 和 approach。` |
| `nature-paper2ppt` | Occasional PPTX from a paper | `做成 15 分钟组会 PPT。` |

## Common Prompts

### Daily Short Prompts

```text
帮我整理这个页面/笔记的 paper card：
<FEISHU_OR_NOTION_URL_OR_OBSIDIAN_PATH>
```

```text
帮我 deep dive 一下这篇论文：
<PDF_OR_ARXIV_OR_PROJECT_URL>
目标：<FEISHU_OR_NOTION_URL_OR_OBSIDIAN_PATH>
```

```text
帮我规范化这个研究页面/笔记，不要破坏已有图片和层级：
<FEISHU_OR_NOTION_URL_OR_OBSIDIAN_PATH>
```

```text
帮我把这个方向整理成 literature tree：
<RESEARCH_TOPIC_OR_PAGE_URL_OR_OBSIDIAN_PATH>
```

### Feishu / Lark

```text
读取这个飞书页面，修改前先 fetch，修改后再 fetch 验证。不要破坏已有图片、表格、画板或多图排版。
<FEISHU_OR_LARK_URL>
```

### Notion

```text
读取这个 Notion 页面或数据库记录，修改前先 fetch，修改后重新 fetch 验证。保留 properties、relations、原生 callout、公式、图片和 caption。
<NOTION_URL>
```

### Obsidian / Markdown

```text
读取这个 Obsidian 笔记及相邻约定，做局部修改并在写后检查 frontmatter、wikilinks、公式和相对资源路径。
<OBSIDIAN_PATH>
```

### Paper Cards / Deep Dive

```text
按照规范补全这个页面里的 paper card。必须先查看官方论文 HTML/PDF；中文 bullet 使用中文优先表达。
<FEISHU_OR_NOTION_URL_OR_OBSIDIAN_PATH>
```

```text
对这篇论文做完整 deep dive，必须满足 paper-deep-dive 交付标准：主入口 Paper Card、可编辑论文解析树、按原文顺序的精读稿；完整英文原文稿与原文中译稿；公式保留 LaTeX；参考文献与正文引用按 deep-dive 链接合同；目标平台用对应 *-doc-workflow 写入并回读验证。
<PDF_OR_ARXIV_OR_PROJECT_URL>
目标：<FEISHU_OR_NOTION_URL_OR_OBSIDIAN_PATH>
```

### Literature / Review / Wiki

```text
为这个方向建立 literature tree、novelty tree 和 challenge-insight tree。
主题：<RESEARCH_TOPIC>
```

```text
帮我做今天的科研经营复盘。最后写入当前 review 系统（Notion、Obsidian 或飞书），并输出明日三项关键 Todo。
```

```text
把这份材料纳入我的本地研究 wiki。保留来源锚点，生成中文正文与术语，并跑 lint/graph 检查。
<LOCAL_FILE_OR_SOURCE_URL>
```

## Compatibility Aliases

Install scripts also create:

- `feishu-cli` → `feishu-doc-workflow`
- `llm-wiki` → `llm-wiki-skill`
- `paper-to-slides` → `paper-to-slides-skill`
