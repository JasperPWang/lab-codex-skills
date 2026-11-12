---
name: weekly-research-summary
description: Create, update, or normalize the user's weekly research summary under Weekly Research Progress (formerly Week Summary), including the source-grounded GPT Weekly Pick template. Use for 周总结, 周报, weekly summary, GPT Weekly Pick, weekly paper picks, or repairs to dated weekly pages with GPT paste, broken formulas, or flat headings.
---

# Weekly Research Summary

## Core Contract

Treat each week page as a **research taste + literature operating note**, not a diary and not a daily review.

It must answer:

1. Which papers this week are worth reading for the user's current lines, and why?
2. What progress / plans / reflections should survive into next week as reusable judgment?

Default language is Chinese. Keep method names, paper titles, acronyms, datasets, and code names in English when they are names.

`GPT Weekly Pick` is a source-grounded research guide centered on problems, insights, implementation, evidence, and research judgment. It is a distinct deliverable from a Paper Abstract Card (abstract translation + figures + resources) and a Paper Card (the seven-field index). Do not substitute either card schema for the weekly-pick template.

Also use:

- [`chinese-technical-writing`](../chinese-technical-writing/SKILL.md) for reader-facing Chinese prose
- [`research-doc-workflow`](../research-doc-workflow/SKILL.md) + matching `*-doc-workflow` for durable writes
- Do **not** fold this into [`daily-research-review`](../daily-research-review/SKILL.md); daily = operating loop, weekly = literature + mid-horizon judgment

## Platform Placement

Current durable hub is Notion:

- Hub: `Weekly Research Progress` (formerly `Week Summary`) — `https://app.notion.com/p/3b5cdd0459b5801bb537f64f5ce4889d`
- Dated children: `Aug 1st`, `Sep 2nd`, … (month abbreviation + ordinal; match neighboring titles)

Preserve this Notion hub by default. Do not silently migrate to Feishu/Obsidian. If the user later moves hubs, follow the new platform and keep the same logical hierarchy.

Before writing:

1. Fetch the hub and the target week page (or create a child under the hub).
2. Inspect sibling week pages for section naming and toggle style.
3. If the week page exists, update in place; otherwise create it under the hub.

Resolve the reporting period separately from paper publication dates. Labels such as `Oct 4th` name a weekly child; do not interpret the ordinal as a calendar day. Record actual coverage dates when known, and never shift content to a neighboring week merely to match publication dates. Mature work may be selected; explain why it is relevant now.

After writing, verify:

- title is not `Untitled` / `无标题` and matches the intended week label;
- page sits under the hub, not orphaned;
- required sections exist as toggle headings;
- formulas are native Notion equations, not GPT double-escaped TeX;
- no ChatGPT tracking params or proxy arXiv links remain.

## Required Sections

Write each week page with these top-level toggle headings (Notion):

```markdown
## GPT Weekly Pick {toggle="true"}
## Paper Notes {toggle="true"}
## Progress & Plans {toggle="true"}
## Reflection {toggle="true"}
```

Optional when the user has method/meta reading that week:

```markdown
## Recent Readings {toggle="true"}
```

Do not invent extra top-level sections unless the user asks. Empty required sections may keep `<empty-block/>` so the skeleton remains stable.

### `GPT Weekly Pick`

`GPT Weekly Pick` always contains these **four fixed tracks**, in this order and with these exact heading titles:

```markdown
## GPT Weekly Pick {toggle="true"}
	### 每周论文推荐：上游方法 {toggle="true"}
	### 每周论文推荐：人场景联合重建 {toggle="true"}
	### 每周论文推荐：人体交互生成 {toggle="true"}
	### 每周论文推荐：物理AI {toggle="true"}
```

Do not rename, reorder, merge, or drop these four tracks. If a track has no worthy paper that week, keep the toggle and write a one-line negative finding (e.g. 本周无达到阅读阈值的新工作), rather than deleting the section.

Map GPT paste / multi-session dumps into these tracks by topic. Legacy sibling pages that used `会话一/二/三` should be normalized to the four tracks when repairing.

Under each track, use paper-level headings:

```markdown
#### 1. <Paper Title> — <year or venue>
```

Number papers consecutively as `1.`, `2.`, `3.` within each track, restarting at `1.` in the next track. Every paper title in `GPT Weekly Pick` must be an H4 heading with this numbering, including late additions. Do not mix H4 headings with unnumbered titles, circled numerals (`①`), bulleted items, or numbered-list blocks as paper titles. Keep meaningful tags such as `【新机制】` after the Arabic numeral rather than dropping them. Reserve H4 for papers: comparison notes and entry labels are bold paragraphs, not competing H4 headings. If a legacy list item owns images, equations, or other child blocks, convert it in place and verify the children remain present and correctly placed; never rebuild or delete media merely to normalize a title.

For any creation, substantive update, or content-completeness audit of `GPT Weekly Pick`, read and apply [the final weekly-pick template](references/gpt-weekly-pick-template.md). This is the authoritative field order and content standard, shared by all four tracks:

1. **论文信息**: complete English and Chinese titles; dates; venue/status; institutions; core authors and their roles; PDF / Project / Code plus inspected reproduction availability.
2. **一句话核心创新**.
3. **任务定义**, including inputs, outputs, conditions, and key assumptions.
4. **问题与核心 insight**: prior bottleneck → insight → why the proposed route should help.
5. **原文主要贡献**.
6. **关键方法与具体实现**, including training/inference flow and compute.
7. **关键实验证据**, including relevant baselines, decisive results/ablations, source figure/table anchors, and evidence boundaries.
8. **原文声称的局限性**.
9. **为什么值得读**.
10. **对我的启发**.
11. **最小验证与我的判断**: a concrete proposed check and a source-grounded assessment, clearly distinguished from reported results.

Do not add `本周优先级`, ranking tables, or reading-priority sections by default; the user removed this field. Keep the mechanism explanation substantive and adapt field lengths to the paper rather than imposing equal word counts. If a request is only a formatting repair, preserve scope: report missing substantive fields rather than inventing content or silently undertaking a full literature rewrite.

#### Paper Images and Copy Residue

Place each paper's important verified figures directly in its paper section as native images: teaser with the task, motivation with the problem/insight, pipeline with the method, and decisive experiment figures with the evidence. Select by explanatory value; a single figure may serve several roles, and not every paper has all three figure types. Use the official paper HTML/PDF or project page; verify that the images belong to the exact paper. When HTML splits a figure into components or omits diagram elements, obtain the complete figure through the matching document/PDF workflow. If a paper has no teaser or standard pipeline, use its actual method illustration or relevant experiment figure without inventing or mislabeling one.

Remove standalone copy/paste scaffolding such as `原论文 Figure 1 / Figure 2`, `查看原图`, `查看官方原图`, `相关图像与来源`, `概览原图`, `流程原图`, and `Teaser 原图 / Pipeline 原图` link lists. These are copying residue, not research content: do not rename, bold, merge, or preserve them as new prose labels. Remove copied favicon/source badges, `+1` counters, and unrelated web-image/search-result credits as well. Keep real paper, project, and code resource links; when a mixed resource paragraph also contains image-view links, remove only the image scaffolding.

Every selected paper figure must carry the **complete Chinese translation of its original caption**, including figure number, subfigure labels, symbols, conditions, and qualifications. Keep official method/model/dataset names. A brief summary cannot replace the full caption. Use the native image-caption field, with no duplicate caption or image-introduction paragraph above/below the image. If a project-only image has no original caption, identify that fact and use a source-grounded explanatory caption rather than inventing an original caption. Preserve correct existing figures, formulas, tables, and user-supplied table screenshots. Replace a copied wrong-paper or proxy image only after verifying the corresponding official figure, then re-fetch to confirm the replacement is present under the intended paper.

### `Paper Notes`

Short personal notes on papers the user actually read or skimmed this week. Prefer insight over re-summary. Link deep-dive / paper-card pages when they exist.

### `Progress & Plans`

Concrete movement and next evidence for active lines. Keep decision-oriented; avoid motivational fluff.

### `Reflection`

Method / taste / process lessons that should change next week's behavior. Prefer reformulation rules over generic encouragement.

### `Recent Readings` (optional)

Non-paper research-method notes, mentor advice pages, or meta readings. Use callouts sparingly and keep takeaways actionable.

## GPT Paste / Normalization Rules

When the user pastes GPT weekly picks or asks to repair an existing week page:

1. **Formulas**: convert mangled plain+escaped TeX (`\\\\rightarrow`, `\\\\text\\{...\\}`, doubled `MMμ\\\\mu`) into Notion `$`…`$` / `$$…$$`.
2. **Headings**: lift flat dumps into the required toggle hierarchy; map multi-session pastes into the four fixed tracks (`上游方法` / `人场景联合重建` / `人体交互生成` / `物理AI`). Normalize every paper title to a consecutively numbered H4 within its track; do not leave a mixture of numbered, circled, unnumbered, or list-style titles.
3. **Links**: strip `?utm_source=chatgpt.com` and similar trackers; replace proxy/anonymous viewers with canonical sources. The metadata `PDF` link must open the official full PDF (prefer `https://arxiv.org/pdf/...` when available); abs/html links may be additional resources, not substitutes for PDF.
4. **Media**: follow **Paper Images and Copy Residue** above: show important teaser/motivation/pipeline/evidence figures directly as native images with complete Chinese captions, preserve trusted media, and verify any wrong-paper image replacement.
5. **Residue**: remove ChatGPT chrome, “Anonymous View” wrappers, cross-platform Markdown fences, and image-view scaffolding; do not turn copying residue into reader-facing prose.
6. **Narrowest write**: prefer targeted updates and snapshot existing content before structural changes. Rebuild only the affected subtree when necessary; whole-page replacement requires the user's explicit authorization. Formatting corruption alone does not authorize replacing unrelated sections.

## Writing Flow

1. Resolve the week label and target page under the hub.
2. Collect inputs: GPT paste, official paper links, user notes, sibling conventions. For weekly-pick content, read the linked template and inspect official full-paper sources, selected captions, and resource/code availability sufficiently to support all fields.
3. Draft with the required sections and the weekly-pick template. Keep author claims, experimental support, and our analysis distinct. Missing facts are resolved from sources or honestly marked as not reported; never fill by plausibility.
4. Write through `notion-doc-workflow` (default) and re-fetch.
5. Report: page URL, actual sections updated, verification outcome, and any unresolved source-access or delivery issues.

## Acceptance Checklist

- Hub child placement and week title are correct
- `GPT Weekly Pick` / `Paper Notes` / `Progress & Plans` / `Reflection` exist as toggles
- `GPT Weekly Pick` contains all four fixed tracks with the exact titles above
- Each track's paper titles are H4 headings numbered `1.`, `2.`, ... without gaps or mixed title styles; non-paper notes do not use H4
- After structural edits, existing images, captions, equations, tables, and child pages are still present and attached to the intended content
- Entries follow the linked final template, including complete Chinese titles, dates, institutions/core authors, and PDF / Project / Code availability
- Task, key assumptions, problem/insight, author contributions, implementation and training/inference compute are source-grounded; unreported details are not guessed
- Key experimental evidence identifies relevant comparisons, decisive results/ablations and figure/table anchors, with evidence boundaries
- Author-stated limitations are separate from our own judgment; proposed minimal validation is not presented as an executed experiment
- Important verified teaser/motivation/pipeline/evidence figures are displayed directly with complete Chinese original-caption translations; alternatives are accurately identified
- No standalone `查看原图`, `相关图像与来源`, `原论文 Figure 1 / Figure 2`, duplicate image introductions, or copied source badges remain; actual paper/project/code links are preserved
- Why-read, user-specific inspiration, and minimal-validation/judgment fields are substantive and paper-specific; no default weekly ranking or priority field
- Native equations; no GPT TeX residue
- Clean arXiv/project links; no ChatGPT tracking or proxy URLs
- Chinese prose follows `chinese-technical-writing`
- Response names the actual Notion write status
