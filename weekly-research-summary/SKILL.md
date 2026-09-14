---
name: weekly-research-summary
description: Create, update, or normalize the user's weekly research summary under the Week Summary hub (GPT weekly picks, paper notes, progress/plans, reflection). Use when the user asks for 周总结, 周报, weekly summary, GPT Weekly Pick, weekly paper pick, or to repair/normalize a dated Week Summary child page that contains GPT paste, broken formulas, or flat heading hierarchy.
---

# Weekly Research Summary

## Core Contract

Treat each week page as a **research taste + literature operating note**, not a diary and not a daily review.

It must answer:

1. Which papers this week are worth reading for the user's current lines, and why?
2. What progress / plans / reflections should survive into next week as reusable judgment?

Default language is Chinese. Keep method names, paper titles, acronyms, datasets, and code names in English when they are names.

Also use:

- [`chinese-technical-writing`](../chinese-technical-writing/SKILL.md) for reader-facing Chinese prose
- [`research-doc-workflow`](../research-doc-workflow/SKILL.md) + matching `*-doc-workflow` for durable writes
- Do **not** fold this into [`daily-research-review`](../daily-research-review/SKILL.md); daily = operating loop, weekly = literature + mid-horizon judgment

## Platform Placement

Current durable hub is Notion:

- Hub: `Week Summary` — `https://app.notion.com/p/3b5cdd0459b5801bb537f64f5ce4889d`
- Dated children: `Aug 1st`, `Sep 2nd`, … (month abbreviation + ordinal; match neighboring titles)

Preserve this Notion hub by default. Do not silently migrate to Feishu/Obsidian. If the user later moves hubs, follow the new platform and keep the same logical hierarchy.

Before writing:

1. Fetch the hub and the target week page (or create a child under the hub).
2. Inspect sibling week pages for section naming and toggle style.
3. If the week page exists, update in place; otherwise create it under `Week Summary`.

After writing, verify:

- title is not `Untitled` / `无标题` and matches the intended week label;
- page sits under `Week Summary`, not orphaned;
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

Group by GPT/session theme when the week has multiple reading threads:

```markdown
## GPT Weekly Pick {toggle="true"}
	### 会话一：<主题> {toggle="true"}
		#### 1. <Paper Title> — <year or venue>
		...
	### 会话二：<主题> {toggle="true"}
		...
```

If there is only one thread, paper `####` headings may sit directly under `GPT Weekly Pick`.

For each recommended paper, prefer this slot order when the source material supports it:

1. **一句话核心创新**
2. **建模的物理** / 关键建模对象（若相关）
3. **关键方法**
4. **物理有效性验证** / 实验证据（若相关）
5. **为什么值得读**
6. **对你的启发**
7. Clean resource links: arXiv abs/html + Project Page/Code when available

End a session or the whole pick block with a short **本周优先级** when multiple papers compete: which to read first for which research line.

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
2. **Headings**: lift flat dumps into the required toggle hierarchy; split multi-session pastes into `会话一/二/三`.
3. **Links**: strip `?utm_source=chatgpt.com` and similar trackers; replace proxy/anonymous viewers with canonical `https://arxiv.org/abs/...` or `/html/...`.
4. **Media**: preserve existing images/captions when doing narrow edits. If a full-page replace is required and an image cannot be safely reattached, say so after write.
5. **Residue**: remove ChatGPT chrome, “Anonymous View” wrappers, and cross-platform Markdown fences from reader-facing text.
6. **Narrowest write**: prefer targeted updates; use full-page replace only when formula/heading corruption is pervasive (as with dense GPT paste).

## Writing Flow

1. Resolve the week label and target page under `Week Summary`.
2. Collect inputs: GPT paste, arXiv links, user notes, sibling conventions.
3. Draft one Markdown body with the required sections.
4. Write through `notion-doc-workflow` (default) and re-fetch.
5. Report: page URL, which sections were filled/left empty, any media loss, and the week's top reading priority if present.

## Acceptance Checklist

- Hub child placement and week title are correct
- `GPT Weekly Pick` / `Paper Notes` / `Progress & Plans` / `Reflection` exist as toggles
- Paper slots are skim-friendly and end in a decision or priority when multiple picks exist
- Native equations; no GPT TeX residue
- Clean arXiv/project links; no ChatGPT tracking or proxy URLs
- Chinese prose follows `chinese-technical-writing`
- Response names the actual Notion write status
