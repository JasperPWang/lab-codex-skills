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

## Common Prompts

Skill names are optional, but naming the intended skill is the most reliable way
to trigger the right workflow. Copy one of these prompts and replace the
placeholders.

### Feishu / Lark Documents

```text
请使用 feishu-doc-workflow 读取这个飞书页面，并在修改前先 fetch、修改后再 fetch 验证。不要破坏已有图片、表格、画板或多图排版。
<FEISHU_OR_LARK_URL>
```

```text
请使用 feishu-doc-workflow 帮我规范这个页面的结构。只做必要的局部修改，不要整页重写；如果页面里有图片，请保持原有图片顺序、大小、caption 和并排关系。
<FEISHU_OR_LARK_URL>
```

### Paper Cards

```text
请使用 paper-card-delivery 和 feishu-doc-workflow，按照规范补全这个页面里的 paper card。必须先查看官方论文 HTML/PDF，不要只依据网页摘要；Dataset 只写数据集名称，中文 bullet 使用中文优先表达。
<FEISHU_OR_LARK_URL>
```

```text
请审核这个 paper card 是否符合规范：官方原文核验、元信息、Dataset、Simulation、方法一句话总结加两个核心创新、作者原文结论总结、中文图注和图片布局保护。
<FEISHU_OR_LARK_URL>
```

### Paper Deep Dive

```text
请使用 paper-deep-dive 对这篇论文做完整深读包：父页面只放 paper card 和摘要；子页面包括英文原文稿、完整中文译稿、中文精读稿。公式必须保留 LaTeX，图片使用中文图注。
<PDF_OR_ARXIV_OR_PROJECT_URL>
```

```text
请用 paper-deep-dive 检查这篇论文的 deep dive 是否完整：英文原文、中文译稿、中文精读稿、公式、参考文献、图表 caption、paper card 和 Feishu 层级都要核验。
<FEISHU_OR_LARK_URL>
```

### Literature Review / Survey

```text
请使用 survey-builder 为这个方向建立 literature tree、novelty tree 和 challenge-insight tree，并给出阅读顺序、方法对比表和 research gap。涉及 paper card 时同时使用 paper-card-delivery。
主题：<RESEARCH_TOPIC>
已有论文或页面：<PAPERS_OR_FEISHU_URLS>
```

```text
请把这些论文按 Type 1/2/3/4 novelty 分类，构建一个能服务创新判断的 literature tree，而不是普通相关工作列表。
<PAPER_LIST_OR_FOLDER>
```

### Bilingual Source Archive

```text
请使用 bilingual-source-archive 和 feishu-doc-workflow，把这篇文章保存为英文原文与中文译文。不要总结，不要改写；按原文顺序保留段落结构。
<SOURCE_URL_OR_TEXT>
```

### Daily Research Review

```text
请使用 daily-research-review 帮我做今天的科研经营复盘。先问我最少量的关键问题；最后写成 Feishu 页面，并输出明日三项关键 Todo。
```

```text
这是我今天的复盘原文，请使用 daily-research-review 整理成科研经营复盘，重点检查 simulation-ready 方向、AI 投资回报、资产沉淀和明日三项关键 Todo。
<TODAY_NOTES>
```

### Chinese Technical Writing

```text
请使用 chinese-technical-writing 修改下面这段中文技术文字。中文优先表达，必要英文术语用 中文（English term），不要留下不必要的英文短语。
<TEXT>
```

### Learning / Explanation

```text
请使用 feynman-learning 帮我讲清楚这个概念。先用直觉解释，再给正式定义、最小例子、常见误区、和我研究方向的连接。
<CONCEPT_OR_PAPER>
```

### Local Wiki

```text
请使用 llm-wiki-skill 把这份材料纳入我的本地研究 wiki。保留来源锚点，生成中文正文、中文（English term）术语、LaTeX 公式，并跑 lint/graph 检查。
<LOCAL_FILE_OR_SOURCE_URL>
```

### Slides / PDF

```text
请使用 paper-to-slides-skill 把这篇论文做成组会 Marp 幻灯。先提炼故事线，再选择必要图表，不要做成逐段摘要。
<PDF_PATH_OR_URL>
```

```text
请使用 pdf 检查这个 PDF 的版式、页码、图片和公式渲染，并指出需要修复的页面。
<PDF_PATH>
```

Current compatibility aliases:

- `~/.codex/skills/feishu-cli` points to `.tools/skills/feishu-doc-workflow`
  for backward compatibility after the Feishu workflow skill rename.
- `~/.codex/skills/llm-wiki` points to `.tools/skills/llm-wiki-skill`.
- `~/.codex/skills/paper-to-slides` points to
  `.tools/skills/paper-to-slides-skill`.
