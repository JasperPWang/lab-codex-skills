# Lab Codex Skills

This directory is the canonical source for the lab Codex skill bundle. It keeps
user-maintained skills and vendored/downloaded skills together so the same
workflow can be shared across the user's Macs and cloned by lab teammates.

Rules:

- Put every editable skill under `.tools/skills/<skill-name>/`.
- Treat `~/.codex/skills/<skill-name>` as a compatibility symlink only.
- Treat `.agents/skills/<skill-name>` as a compatibility symlink only when a
  loader still expects that path.
- Do not edit copied skill directories in multiple places. Edit the canonical
  Vault path, then let the symlink expose it to Codex.
- Keep system, bundled, plugin-cache, and runtime skills outside this
  repository. Vendored or downloaded third-party skill suites may live here when
  their provenance is recorded.
- After changing a skill, run the relevant validation script if the skill has
  one, or run the system skill validator when applicable.

Before publishing or sharing, review:

- `SKILL_MANIFEST.md`
- `THIRD_PARTY_NOTICES.md`
- `.gitignore`

## Copy-Paste Setup Prompt

For lab teammates, the easiest setup path is to paste this prompt into Codex on
their own machine. Codex should run the commands, validate the installation, and
report any missing prerequisites.

```text
请帮我配置 Human Centric Intelligence Lab 的 Codex skill bundle。

目标：
1. 从 GitHub 克隆公开仓库：https://github.com/JasperPWang/lab-codex-skills
2. 放到我本机一个稳定位置，例如 ~/lab-codex-skills；如果目录已存在，先 fetch/pull 更新，不要删除我的本地修改。
3. 运行 install.sh，把 skill 以 symlink 方式暴露到 ~/.codex/skills。
4. 运行 scripts/validate-all.sh，确认所有 skill 通过校验。
5. 检查 ~/.codex/skills 里是否能看到 paper-card-delivery、paper-deep-dive、feishu-doc-workflow、survey-builder、ai-research-workflow、chinese-technical-writing、feynman-learning 等常用入口。
6. 如果我要编辑飞书原生文档，请检查 ~/.local/bin/lark-cli doctor；如果没有安装或没有登录，只告诉我需要配置，不要猜测或写入任何 token / secret。
7. 最后用中文告诉我：安装目录、校验结果、可用的常用 prompt、以及 Feishu 原生编辑是否已就绪。

约束：
- 不要把任何 access token、refresh token、app secret、cookie、私有 Feishu 链接写进仓库或聊天输出。
- 如果遇到已有目录或已有 skill，同名普通目录先备份，不要直接覆盖；symlink 可以安全重建。
- 如果命令失败，先诊断并给出下一步，不要假装安装成功。
```

On a new Mac or a lab teammate's machine, run one of these:

```bash
# From this skill bundle directory after cloning it as a repository:
bash install.sh

# From the WorldModelVault root on this machine:
bash ".tools/skills/install.sh"
```

This recreates local compatibility symlinks under `~/.codex/skills` and
`.agents/skills` without copying skill content out of the iCloud-synced vault.

To validate all skills:

```bash
bash ".tools/skills/scripts/validate-all.sh"
```

To export a clean GitHub-ready copy without local archives or nested `.git`
metadata:

```bash
bash ".tools/skills/scripts/export-github-bundle.sh" /tmp/lab-codex-skills
```

## Feishu Native Editing Prerequisite

Feishu / Lark work in this bundle assumes the local `lark-cli` is installed and
authenticated. This is what lets Codex edit native Feishu documents instead of
flattening pages through browser copy-paste or generic Markdown.

Expected local command:

```bash
~/.local/bin/lark-cli doctor
```

Common checks:

```bash
~/.local/bin/lark-cli docs +fetch --help
~/.local/bin/lark-cli docs +update --help
~/.local/bin/lark-cli docs +media-insert --help
~/.local/bin/lark-cli wiki --help
```

Configuration is user-local under `~/.lark-cli/`. Do not commit app secrets,
tokens, refresh tokens, or local Feishu config into this repository.

## Integration Policy

Personal lab skills own final deliverables. Downloaded skills can provide
methods, checklists, and intermediate reasoning, but they should not override
the user's Feishu-native page structure or formatting.

- Deep dives may borrow `nature-reader`'s source-map and bilingual-reader
  methods, then convert them into the lab format: parent page plus `英文原文稿`,
  `原文译稿`, and `中文精读稿`.
- Literature reviews may borrow `deep-research`'s question clarification,
  source verification, synthesis, and gap-analysis methods, then convert them
  into literature trees, challenge-insight trees, novelty trees, matrices, and
  paper-card pages.
- Paper cards remain governed by `paper-card-delivery`.
- Feishu hierarchy, native images, captions, formulas, whiteboards, fetch
  before write, and fetch after write remain governed by `feishu-doc-workflow`.
- External formats such as APA reports, PRISMA reports, standalone Markdown
  readers, or local asset bundles are intermediate/source artifacts unless the
  user explicitly asks for them as final deliverables.

## Research Workflow Skill Map

Use natural daily prompts first. Codex should select the right skill stack and
only ask for more detail when the missing context would change the result.

| Research step | Daily prompt | Main skills |
| --- | --- | --- |
| Feishu page editing | `帮我整理/规范这个飞书页面` | `feishu-doc-workflow`, `chinese-technical-writing` |
| Paper cards | `帮我补全这个页面的 paper card` | `paper-card-delivery`, `feishu-doc-workflow` |
| Single-paper deep dive | `帮我 deep dive 一下这篇论文` | `paper-deep-dive`, `paper-card-delivery`, `feishu-doc-workflow` |
| Literature tree / survey | `帮我把这个方向整理成 literature tree` | `survey-builder`, `ai-research-workflow`, `deep-research` |
| Broad field exploration | `帮我调研这个方向，给我研究路线图` | `deep-research`, `academic-research-suite`, `nature-academic-search` |
| Concept learning | `帮我讲清楚这个概念/方法` | `feynman-learning` |
| Local wiki ingestion | `把这份材料纳入我的本地研究 wiki` | `llm-wiki-skill`, `chinese-technical-writing` |
| Manuscript planning/writing | `帮我搭论文框架/写引言/改摘要` | `nature-writing`, `paper-spine`, `academic-paper` |
| Manuscript polishing | `帮我润色这段英文论文文字` | `nature-polishing` |
| Citation verification | `帮我核验这些引用是否真的支撑论断` | `cite-verify`, `nature-citation` |
| Figures and plots | `帮我把这张图做成论文级图表` | `nature-figure` |
| Statistics sanity check | `帮我检查这些实验表格和 p 值是否一致` | `stats-sanity` |
| Reproducibility / release | `帮我整理这个项目的复现包` | `repro-pack` |
| Research code workflow | `按科研开发规范帮我改/跑/记录这个实验` | `research-dev-standards` |
| Mock review / rebuttal | `帮我从审稿人角度审一下/帮我回审稿意见` | `academic-paper-reviewer`, `nature-reviewer`, `nature-response` |
| Grant / proposal | `帮我搭这个基金/博士课题 proposal` | `grant-writer` |
| Daily review | `帮我做今天的科研经营复盘` | `daily-research-review` |

## Downloaded Skills Worth Using

These are not all daily defaults, but they are useful at specific pressure
points. Prefer short prompts; the skill carries the detailed protocol.

| Skill | Best use | Example prompt |
| --- | --- | --- |
| `deep-research` | A new direction is still fuzzy and needs question formulation, source search, synthesis, and risk checks. | `帮我调研 simulation-ready avatar reconstruction，给我问题树、关键论文和研究空白。` |
| `academic-research-suite` | Heavier academic research workflow: literature review, research question refinement, integrity checks, and writing pipeline coordination. | `帮我把这个方向整理成一个可写论文的 research plan。` |
| `nature-academic-search` | Systematic multi-source literature search, citation file conversion, deduplication, and reference management. | `帮我检索 2024-2026 simulation-ready reconstruction 的核心论文，并导出 BibTeX。` |
| `cite-verify` | Before a manuscript, proposal, or important Feishu knowledge page relies on citations. | `帮我核验这些引用是否真的支持每一句 claim。` |
| `nature-reader` | Standalone full-paper bilingual reading with source anchors; use `paper-deep-dive` when the deliverable must be the Feishu deep-dive package. | `帮我做这篇论文的中英文对照精读，不要只总结。` |
| `nature-writing` | Drafting or restructuring abstract, introduction, related work, method, experiments, or discussion. | `帮我把这些结果组织成一版论文 introduction 逻辑。` |
| `nature-polishing` | Publication-style English polishing and LaTeX layout cleanup. | `帮我润色这段 introduction，保留技术含义，不要过度改写。` |
| `nature-figure` | Paper-grade Python/R figures, multi-panel plots, export QA. | `用 Python 帮我把这个实验结果画成论文级 figure。` |
| `stats-sanity` | Numeric consistency for tables, metrics, p-values, confidence intervals, denominators, and figure-text drift. | `帮我检查这张实验表和正文里的数字是否一致。` |
| `repro-pack` | Before open-source release, paper artifact submission, or intern handoff. | `帮我把这个实验项目整理成可复现包。` |
| `paper-spine` | Heavy end-to-end manuscript/report build from materials or a rough draft. | `帮我基于这些材料搭一篇完整论文草稿。` |
| `academic-paper-reviewer` / `nature-reviewer` | Pre-submission critique, novelty/risk assessment, reviewer-perspective feedback. | `帮我从审稿人角度审一下这篇 draft。` |
| `nature-response` | Reviewer response and rebuttal letters. | `帮我把这些审稿意见整理成逐点回复。` |
| `grant-writer` | Project narratives, aims, milestones, risks, and reviewer-facing proposal strategy. | `帮我搭一个博士课题/基金 proposal 的 aims 和 approach。` |
| `nature-paper2ppt` | Occasional real PPTX deck from a paper. This is the preferred downloaded slide skill; `paper-to-slides-skill` is not a daily default. | `帮我把这篇论文做成 15 分钟组会 PPT。` |

## Common Prompts

Daily prompts should stay short. The agent should choose the matching skill and
apply the detailed rules internally; only name a skill when you want to force a
specific workflow.

### Daily Short Prompts

```text
帮我整理这个页面的 paper card：
<FEISHU_OR_LARK_URL>
```

```text
帮我补全这个页面下子页的 paper card，按时间新到旧：
<FEISHU_OR_LARK_URL>
```

```text
帮我 deep dive 一下这篇论文：
<PDF_OR_ARXIV_OR_PROJECT_URL>
```

```text
帮我规范化这个飞书页面，不要动已有图片布局：
<FEISHU_OR_LARK_URL>
```

```text
帮我把这个方向整理成 literature tree：
<RESEARCH_TOPIC_OR_FEISHU_URL>
```

Use the longer prompts below only when you need to pin a specific constraint.

### Feishu / Lark Documents

```text
读取这个飞书页面，修改前先 fetch，修改后再 fetch 验证。不要破坏已有图片、表格、画板或多图排版。
<FEISHU_OR_LARK_URL>
```

```text
帮我规范这个页面的结构。只做必要的局部修改，不要整页重写；如果页面里有图片，请保持原有图片顺序、大小、caption 和并排关系。
<FEISHU_OR_LARK_URL>
```

### Paper Cards

```text
按照规范补全这个页面里的 paper card。必须先查看官方论文 HTML/PDF，不要只依据网页摘要；Dataset 只写数据集名称，中文 bullet 使用中文优先表达。
<FEISHU_OR_LARK_URL>
```

```text
请审核这个 paper card 是否符合规范：官方原文核验、元信息、Dataset、Simulation、方法一句话总结加两个核心创新、作者原文结论总结、中文图注和图片布局保护。
<FEISHU_OR_LARK_URL>
```

### Paper Deep Dive

```text
对这篇论文做完整 deep dive：父页面只放 paper card 和摘要；子页面包括英文原文稿、完整中文译稿、中文精读稿。公式必须保留 LaTeX，图片使用中文图注。
<PDF_OR_ARXIV_OR_PROJECT_URL>
```

```text
请用 paper-deep-dive 检查这篇论文的 deep dive 是否完整：英文原文、中文译稿、中文精读稿、公式、参考文献、图表 caption、paper card 和 Feishu 层级都要核验。
<FEISHU_OR_LARK_URL>
```

### Literature Review / Survey

```text
为这个方向建立 literature tree、novelty tree 和 challenge-insight tree，并给出阅读顺序、方法对比表和 research gap。涉及 paper card 时按 paper card 规范处理。
主题：<RESEARCH_TOPIC>
已有论文或页面：<PAPERS_OR_FEISHU_URLS>
```

```text
请把这些论文按 Type 1/2/3/4 novelty 分类，构建一个能服务创新判断的 literature tree，而不是普通相关工作列表。
<PAPER_LIST_OR_FOLDER>
```

### Bilingual Source Archive

```text
把这篇文章保存为英文原文与中文译文。不要总结，不要改写；按原文顺序保留段落结构。
<SOURCE_URL_OR_TEXT>
```

### Daily Research Review

```text
帮我做今天的科研经营复盘。先问我最少量的关键问题；最后写成 Feishu 页面，并输出明日三项关键 Todo。
```

```text
这是我今天的复盘原文，请整理成科研经营复盘，重点检查 simulation-ready 方向、AI 投资回报、资产沉淀和明日三项关键 Todo。
<TODAY_NOTES>
```

### Chinese Technical Writing

```text
修改下面这段中文技术文字。中文优先表达，必要英文术语用 中文（English term），不要留下不必要的英文短语。
<TEXT>
```

### Learning / Explanation

```text
帮我讲清楚这个概念。先用直觉解释，再给正式定义、最小例子、常见误区、和我研究方向的连接。
<CONCEPT_OR_PAPER>
```

### Local Wiki

```text
把这份材料纳入我的本地研究 wiki。保留来源锚点，生成中文正文、中文（English term）术语、LaTeX 公式，并跑 lint/graph 检查。
<LOCAL_FILE_OR_SOURCE_URL>
```

### PDF QA

```text
检查这个 PDF 的版式、页码、图片和公式渲染，并指出需要修复的页面。
<PDF_PATH>
```

Current compatibility aliases:

- `~/.codex/skills/feishu-cli` points to `.tools/skills/feishu-doc-workflow`
  for backward compatibility after the Feishu workflow skill rename.
- `~/.codex/skills/llm-wiki` points to `.tools/skills/llm-wiki-skill`.
