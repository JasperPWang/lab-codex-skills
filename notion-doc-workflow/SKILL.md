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
6. **Notion body citations — write-time escape (required):** canonical drafts still use `[[n](url)]` / `[[n](url), [m](url)]`. Immediately before any Notion Markdown write (`ntn pages create|edit`, MCP markdown update), escape the outer opening bracket so the first cite is not stored as link text `[n`:
   ```bash
   python3 ".tools/skills/notion-doc-workflow/scripts/prepare-notion-citation-markdown.py" draft.md -o notion-ready.md
   # writes \[[n](url)] / \[[n](url), [m](url)] — verified: link text is digits only
   ```
   Do **not** write bare `[[n](url)]` into Notion: single or multi cluster, the importer always absorbs the first `[` into the first link.
7. **Mandatory after any Markdown write that contains numeric body citations:** run the citation rich_text fixer as a safety net (covers older pages and any write that skipped step 6):
   ```bash
   python3 ".tools/skills/notion-doc-workflow/scripts/fix-notion-citation-rich-text.py" <page-id-or-url>
   ```
   Do not treat Markdown re-fetch alone as proof that link ranges are correct; verify via Blocks API / this script (`--check-only` must exit 0).
8. Re-fetch native blocks/properties and verify. Run any content-skill validator that applies to Notion drafts when available.

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
| Body citations | Reader goal: plain outer `[]`, digit-only link text (`6`, not `[6`). Canonical draft: `[[n](pdf-url)]` / `[[n](url), [m](url)]`. **Notion write form:** escape the outer `[` → `\[[n](url)]` / `\[[n](url), [m](url)]` via `scripts/prepare-notion-citation-markdown.py` (single and multi: the first cite is always the one Notion corrupts). After write, still run `scripts/fix-notion-citation-rich-text.py <page>` until `--check-only` exits 0. The fixer splits `text.content` >2000 and sanitizes nested/overlong `link.url`. Rare mangled blobs (`[[[[9](url)](url)…`) may need a one-block manual rewrite. |
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

### Manually Imported `pdf2zh-next` Pages

Treat a manually imported translated PDF as a draft. For a deep-dive translation page:

For the `pdf2zh-next` imported-page repair path, the existing Chinese manuscript page is the primary deliverable. Do not require or create `英文原文稿` and `精读稿` child pages unless the user explicitly requests them. Apply the source-fidelity, formula, figure/caption, table, appendix, reference/citation, and read-back checks to the Chinese page itself. This exception does not change the requirements for new Notion deep dives created from source materials.

- rename the page to the verified Chinese paper title; keep the official English title in the opening block;
- add the latest arXiv PDF, Project Page, and Code links above the abstract when those resources exist; do not add child-artifact links by default on this imported-page repair path;
- restore heading levels from the source paper, repair PDF-induced paragraph splits and duplicate headers/footers, and inspect all major sections;
- normalize numbered headings at every depth from their prefixes rather than imported font levels: `N` is a top-level heading, `N.M` a subsection, `N.M.K` a sub-subsection, and the same component-count rule continues deeper. Convert full-width heading punctuation `．` to ASCII `.` before parsing, so `4．2．方法` becomes `4.2. 方法`. In ordinary structural text, convert `／` to `/`, `－` to `-`, and citation/list brackets `［］` to `[]`; protect formulas, code, URLs, paths, and backslash-escaped sequences before cleanup and restore them exactly. Preserve unrelated Chinese punctuation in prose. Use one punctuation style throughout, defaulting to `N. Title` / `N.M. Subtitle` unless the source consistently uses `N Title` / `N.M Subtitle`;
- convert inline/display formulas to native Notion equations where possible, preserving exact TeX when native conversion is unavailable;
- use native image captions for complete translated figure captions and do not leave duplicate caption paragraphs;
- before writing native image captions, sanitize parser-sensitive escaped citation markers such as `\[33\]` inside the caption only (use ordinary visible parentheses if required); keep the manuscript body citations unchanged and verify the caption survives fetch/read-back;
- keep author email addresses as non-link text; because Notion auto-links bare email addresses, use inline code or another visible non-link representation when the user requests plain text;
- keep author emails as ordinary visible text; do not intentionally add Markdown/`mailto:` links or code formatting. Notion may auto-link a bare email during rendering;
- for the opening resource block of a deep-dive Chinese manuscript only, omit a standalone `来源` label and make each link's visible text equal to its URL; do not apply this rule to English manuscripts or general Notion documents;
- keep table cells in English, translate only table titles/notes, and preserve an original screenshot when an imported table is visually unreliable;
- audit imported tables for garbled cells, broken row/column boundaries, duplicated pipe-table remnants, fused captions, and repeated table data. Keep one authoritative native table, repair it against the official PDF/HTML, and use an official table screenshot when the editable extraction cannot be trusted;
- in References, allow the cited paper title to be translated, but keep authors, venue, year, pages, identifiers, URLs, and other metadata in the source language; restore one reference per paragraph and the shared body-citation PDF URL map.

After repair, fetch the page again and verify title, links, headings, formulas, captions, tables, references, and citation URLs. Do not report the import as a completed deep dive until this read-back passes.

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
