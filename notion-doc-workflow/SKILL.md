---
name: notion-doc-workflow
description: Notion document and database workflow for reading, editing, structuring, and verifying pages used by research skills (paper cards, deep dives, surveys, meeting notes, bilingual archives). Use when the user provides a notion.so URL, names Notion as the destination, asks to create or update a Notion page/database, or research-doc-workflow routes a durable write to Notion. Applies Notion-native format deltas so Feishu/Obsidian syntax does not leak into reader-facing content.
---

# Notion Doc Workflow

## Overview

This skill is the Notion delivery adapter for research documents. Content contracts (what sections mean, what counts as complete) stay in task skills such as `paper-card-delivery`, `paper-deep-dive`, `survey-builder`. This skill owns Notion destination resolution, native block representation, narrow writes, and post-write verification.

Always use [`research-doc-workflow`](../research-doc-workflow/SKILL.md) as the platform router. Use this skill only when the durable target is Notion.

## When To Use

- User supplies a `notion.so` / `www.notion.so` URL or Notion page/database ID.
- User explicitly says write to Notion / 写到 Notion.
- An existing durable document already lives in Notion and must be updated in place.

Do not silently redirect a Notion target to Feishu or Obsidian. If Notion tools/MCP/connectors are unavailable, report that Notion must be connected and stop; do not claim a write succeeded elsewhere.

## Tooling

Prefer the available Notion connector / MCP / API tools in the current agent environment:

1. Search or resolve the destination page or database.
2. Fetch the current page (and parent / data source / required properties when creating database rows).
3. Apply the narrowest update that preserves trusted blocks.
4. Re-fetch and verify title, parent/database, properties, section order, links, media, formulas, and content presence.

If the environment exposes no Notion write path, state the blocker explicitly.

## Shared Write Workflow

1. Read the task-specific content skill and keep its semantic contract unchanged.
2. Confirm the Notion destination from the user's URL or explicit instruction.
3. Fetch the current page/database state before editing.
4. Prepare one canonical Markdown draft for the shared body, then convert only Notion-required deltas below.
5. Write with the smallest safe change. Prefer appending or replacing a known span over rebuilding the whole page.
6. Re-fetch native blocks/properties and verify. Run any content-skill validator that applies to Notion drafts when available.

## Notion Format Deltas

Assume Markdown parity first. Convert only what Notion cannot represent the same way as Obsidian or Feishu:

| Concern | Notion rule |
|---|---|
| Hierarchy | Parent page + subpages, or database relations; do not invent Feishu wiki tokens |
| Callouts | Native Notion callout blocks; do not leave Obsidian `> [!type]` as reader-facing text |
| Metadata | Database/page properties for queryable fields; no YAML frontmatter in reader-facing body |
| Paper-card metadata | One paragraph with four logical rows joined by exactly three `<br>` tags so Notion imports one paragraph with three hard breaks; never four physical Markdown lines |
| Math | Native inline/block equations from TeX; keep `$...$` / `$$...$$` only in the intermediate Markdown if the importer maps them to equations |
| Inline code | For paths, filenames, commands, config keys: Notion inline `code` with default/black color (`annotations.color="default"`); do not color code gray/brown/red |
| Images | Native image blocks + native captions; no duplicate caption paragraph after a successful native caption |
| Wikilinks | Convert `[[Note]]` to Notion page links or plain titles; do not leave Obsidian wikilink chrome |
| References | Keep `[n]` plain labels; append `. URL [url](url)` (or ` URL [url](url)` after an existing period) with display text equal to URL; do not turn References into numbered `1.` lists |
| Body citations | Goal form is `[[n](pdf-url)]` / `[[n](url), [m](url)]`: only the **digits** are links; outer `[]` and commas stay plain chrome. Notion’s Markdown importer often absorbs the opening `[` into the link text (`[6` linked) and may treat adjacent `[[` as a wikilink—after Markdown write-back, verify via the Blocks API and PATCH `rich_text` so linked segments are digit-only (`6`, not `[6`) |
| Editable trees | Nested headings/toggles, linked subpages, or supported embeds; not Feishu whiteboard tokens |

## Forbidden Cross-Platform Residue

Reader-facing Notion pages must not contain:

- Feishu Docx/XML fragments, `block_id`, `docs +media-insert` scratch, or Feishu whiteboard PlantUML dumps meant only for Lark boards
- Obsidian `> [!paper]` / other callout fences left as literal Markdown when a native callout was intended
- YAML frontmatter fences (`---\nkey:`) as visible body text
- Absolute machine paths, `.tools/tmp/`, MinerU scratch directories, `EW_IMG_…`, or `![[wikilink-image]]` vault embeds
- Paper-card metadata split into four separate Notion paragraphs

## Paper Cards on Notion

Content and field rules: [`paper-card-delivery`](../paper-card-delivery/SKILL.md). This skill only maps them to Notion:

- Title as Notion heading; metadata as one hard-break paragraph; native image + caption; then seven bullet slots.
- After write, re-fetch and confirm the metadata region is **one** paragraph containing three newline/hard-break characters.
- Verify no Obsidian asset-path labels remain in visible text.

## Deep Dives / Surveys / Meetings

- Structure and completion standards come from `paper-deep-dive`, `survey-builder`, or the relevant content skill.
- Notion mapping: one parent page plus required subpages or database entries; native equations/images; editable outline or supported embed for trees—not Feishu mind-map boards unless the user explicitly wants an export image.
- Preserve existing Notion layout and media unless the user asks to restructure.

## Workspace Hygiene

- Keep downloads, MinerU outputs, and fetch dumps under `.tools/tmp/<task-slug>/` (or system temp), not the vault root.
- Delete task-local scratch after the Notion page is re-fetched and verified, unless the user asks to keep audit artifacts under `.tools/outputs/<task-slug>/`.

## Acceptance Checklist

- Destination is Notion (URL or explicit instruction), not a silent redirect.
- Content-skill contract passes without Notion-specific omissions.
- Title, parent/database, properties, section order, links, formulas, media, and captions verified via re-fetch.
- No Feishu/Obsidian syntax residue in reader-facing content.
- Paper-card metadata (if any) is one paragraph with three hard breaks.
- Response names Notion and the actual write/verify status.
