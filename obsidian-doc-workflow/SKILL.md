---
name: obsidian-doc-workflow
description: Obsidian/Markdown vault workflow for reading, editing, structuring, and verifying notes used by research skills (paper cards, deep dives, surveys, wiki pages, meeting notes). Use when the user gives a vault path or .md note, names Obsidian/WorldModelVault as the destination, or research-doc-workflow routes a durable write to local Markdown. Applies Obsidian-native format deltas so Feishu/Notion syntax does not leak into reader-facing notes.
---

# Obsidian Doc Workflow

## Overview

This skill is the Obsidian / local Markdown delivery adapter for research documents. Content contracts stay in task skills such as `paper-card-delivery`, `paper-deep-dive`, `survey-builder`, and `llm-wiki`. This skill owns vault path resolution, Markdown/callout/frontmatter/asset conventions, narrow file edits, and post-write verification.

Always use [`research-doc-workflow`](../research-doc-workflow/SKILL.md) as the platform router. Use this skill when the durable target is Obsidian or a vault Markdown path.

## Division Of Labor With `llm-wiki`

| Concern | Owner |
|---|---|
| Wiki layers (`raw/` / `wiki/`), ingestion, provenance, indexes, graph hygiene | [`llm-wiki`](../llm-wiki-skill/SKILL.md) |
| File write mechanics, callouts, frontmatter shape, relative assets, link hygiene, re-read verification | **this skill** |
| Paper-card fields and validators | [`paper-card-delivery`](../paper-card-delivery/SKILL.md) |

When writing Research-Wiki or vault learning notes, load `llm-wiki` for knowledge rules and this skill for format/write verification. Format conflicts: this skill wins for representation; `llm-wiki` wins for what belongs in the wiki.

## When To Use

- User supplies a vault-relative or absolute `.md` path, folder under WorldModelVault, or says Obsidian / 写到 vault.
- An existing durable note already lives in the vault and must be updated in place.

Do not silently redirect an Obsidian target to Feishu or Notion. Preserve the note's folder, naming, and neighboring conventions unless the user asks to move it.

## Shared Write Workflow

1. Read the task-specific content skill and keep its semantic contract unchanged.
2. Resolve the exact note path and folder conventions (frontmatter schema, asset dir, link style).
3. Read the current file (and nearby notes if hierarchy/MOC matters) before editing.
4. Prepare one canonical Markdown draft; keep Obsidian-native constructs listed below.
5. Make the narrowest safe edit. Prefer surgical section updates over rewriting an entire rich note that already has images and user annotations.
6. Re-read the written file and verify frontmatter, headings, links, image paths, formulas, and referenced assets. Run content-skill validators when present.

## Obsidian Format Deltas

| Concern | Obsidian rule |
|---|---|
| Hierarchy | Folders + MOC/index notes + `[[wikilinks]]`; do not invent Feishu wiki nodes or Notion database properties as body text |
| Callouts | Keep `> [!type]` (including `> [!paper]` when paper-card CSS/snippet applies) |
| Metadata | YAML frontmatter for stable queryable fields; do not paste Notion property dumps into the body |
| Paper-card metadata | Four **physical** Markdown lines after the title (not Notion `<br>`-joined single line) |
| Math | Keep `$...$` / `$$...$$` |
| Images | Relative paths under the vault asset convention; meaningful alt text or established caption convention; no absolute machine paths |
| Links | `[[wikilinks]]` when the vault expects them; relative Markdown links for portable assets; external PDFs as normal `[text](url)` |
| References | Plain `[n]` labels + original bibliography text + ` \| [url](url)` with display text equal to URL; never `1.` ordered lists for bibliography |
| Body citations | `[[n](pdf-url)]` with the same URL map as References |
| Editable trees | Mermaid, Canvas, or linked outline per vault convention—not Feishu whiteboard tokens |

## Forbidden Cross-Platform Residue

Reader-facing Obsidian notes must not contain:

- Notion paper-card `<br>` metadata tricks left as literal HTML when four physical lines are required
- Feishu Docx/XML, `block_id`, `docs +media-insert` instructions, or Lark whiteboard-only PlantUML as the primary tree
- Absolute paths like `/Users/...`, `.tools/tmp/...`, or MinerU scratch directories in reader-facing embeds
- Visible `EW_IMG_…` migration labels, `图像： assets/...` residue, or Feishu-only layout notes
- Database property tables copied from Notion as a substitute for frontmatter without converting fields

## Paper Cards in Obsidian

- Follow [`paper-card-delivery`](../paper-card-delivery/SKILL.md).
- Keep four physical metadata lines; relative image + Chinese caption in alt/vault convention; seven bullet slots.
- Validate local drafts when practical:

```bash
python .tools/skills/paper-card-delivery/scripts/validate_paper_card.py path/to/cards.md --target obsidian
```

## Deep Dives / Surveys / Meetings

- Completion standards come from `paper-deep-dive` / `survey-builder` / meeting conventions in `llm-wiki` or the content skill.
- Obsidian mapping: one main note plus linked manuscript notes in a stable folder; relative assets; LaTeX math; Mermaid/Canvas or outline for `论文解析树`.
- Do not require a Feishu mind map for vault deliveries.

## Workspace Hygiene

- Store extraction intermediates under `.tools/tmp/<task-slug>/`; delete after the durable note is re-read and verified.
- Durable figures belong under the note's `assets/` (or vault-established asset path) with semantic filenames—not the vault root.
- Do not leave opaque scratch files (`*_after.json`, one-off scripts) in `WorldModelVault` root.

## Acceptance Checklist

- Destination is Obsidian/vault Markdown from URL/path or explicit instruction.
- Content-skill contract passes.
- Frontmatter, headings, wikilinks/relative links, formulas, media paths, and captions verified by re-reading the file.
- No Feishu/Notion syntax residue in reader-facing content.
- Paper-card metadata (if any) uses four physical lines; validator run when a local draft exists.
- Response names Obsidian/path and the actual write/verify status.
