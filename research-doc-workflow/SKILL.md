---
name: research-doc-workflow
description: Route creation, editing, migration, and verification of research documents across Feishu/Lark, Notion, and Obsidian/Markdown while preserving content contracts, hierarchy, formulas, images, captions, links, and source provenance. Use whenever a task-specific research skill writes or normalizes paper cards, deep dives, surveys, experiment reports, bilingual source archives, daily reviews, meeting notes, or wiki pages, or whenever the user names Feishu, Notion, Obsidian, a wiki/page URL, or a local Markdown destination.
---

# Research Document Workflow

## Core Contract

Keep research content standards independent from storage platforms. Use one canonical Markdown-first document for the shared body: headings, paragraphs, lists, block quotes, links, tables, code blocks, and LaTeX formulas should remain the same unless the target demonstrably requires a small conversion. The task-specific skill owns what the document means and which sections are required; this skill selects the destination backend, applies only the necessary platform deltas, performs the write, and verifies the durable result.

Do not create separate Feishu, Notion, and Obsidian versions of the same content skill or template. Maintain one Markdown structure and three thin delivery adapters so field definitions, evidence standards, wording, and acceptance gates cannot drift.

Do not default a new research document to Feishu merely because an older workflow did. Preserve an existing document's platform. For a new document, infer the target from the user's URL, app mention, workspace, path, or explicit instruction. When no target is supplied:

- prefer Obsidian/Markdown for personal, local, versionable, file-based knowledge in the current vault;
- prefer Notion for collaborative pages, databases, property-driven collections, or material already connected to a Notion workspace;
- use Feishu when the user supplies a Feishu/Lark target, asks for a Feishu-native artifact, or the surrounding project explicitly requires it;
- ask one concise destination question only when both Notion and Obsidian are genuinely plausible and the choice changes the durable location.

Never silently migrate, duplicate, or delete an existing durable document. A platform change requires an explicit target or a user-approved migration task.

## Backend Router

### Feishu / Lark

- Also use `feishu-doc-workflow` for wiki resolution, fetch-before-write, narrow block edits, native images/captions/formulas/whiteboards, hierarchy preservation, and fetch-after-write verification.
- Preserve trusted blocks, image grids, captions, tables, formulas, and child-page relationships. Avoid whole-page replacement on rich documents.
- Use `lark-whiteboard` only when an editable Feishu whiteboard or mind map is required.

### Notion

- Use `notion-knowledge-capture` for structured knowledge pages and `notion-research-documentation` when the task requires searching or synthesizing existing Notion material.
- Search and fetch the destination before updating it. Resolve the exact parent page, database, or data source and inspect required properties before creating records.
- Prefer native Notion headings, callouts, equations, image captions, tables, page links, relations, and database properties. Do not paste Obsidian frontmatter or Feishu block artifacts into reader-facing Notion content.
- **Black-text preference**: do not create Notion rich-text with the inline `code` annotation unless the user explicitly requests literal inline code. Keep technical terms, model names, variables, configuration names, filenames, paths, and identifiers as ordinary black text. Write mathematical notation and short expressions as native inline equations; use display equations only for multi-line derivations or separately referenced formulas.
- Re-fetch the page after writing and verify title, parent/database, properties, section order, links, media, formulas, and content presence.
- If Notion tools are unavailable, report that the Notion app must be connected. Do not claim that a page was written and do not silently redirect the document to Feishu.

### Obsidian / Markdown

- Use `llm-wiki` when the task includes ingestion, source provenance, atomic notes, wikilinks, indexes, graph maintenance, or long-term Research-Wiki placement.
- Inspect the target folder, neighboring notes, frontmatter schema, attachment convention, and link style before editing. Preserve local conventions unless the user asks to change them.
- Use YAML frontmatter only for stable queryable metadata. Use `[[wikilinks]]` when the vault convention expects them, relative Markdown links for portable external assets, and `$...$` / `$$...$$` for formulas.
- Store durable assets beside the note or under the vault's established asset directory with semantic filenames. Do not leave temporary downloads, absolute machine paths, or scratch extraction directories in reader-facing notes.
- Read the written file back and verify frontmatter, headings, links, image paths, formulas, and referenced assets. Run the relevant local validator when the content skill provides one.

## Small Platform Deltas

Assume Markdown parity first. Convert only the features that are not represented consistently:

| Small delta | Feishu / Lark | Notion | Obsidian / Markdown |
|---|---|---|---|
| Parent/child hierarchy | Wiki node and child pages | Parent page, subpages, or database relations | Folder/MOC note plus links |
| Callout | Convert semantic callout marker to native callout when supported | Convert semantic callout marker to native callout when supported | Keep `> [!type]` callout |
| Inline/display math | Preserve `$...$` / `$$...$$` or map to native equation blocks without changing TeX | Preserve TeX or map to inline/block equations | Keep `$...$` / `$$...$$` |
| Image caption | Native image caption | Native image caption | Existing vault convention; otherwise meaningful Markdown alt text without a duplicate caption paragraph |
| Structured metadata | Compact native text/properties | Database/page properties | YAML frontmatter |
| Editable tree | Native whiteboard/mind map | Page/database hierarchy or embedded supported artifact | Mermaid, Canvas, or linked outline according to vault convention |
| Verification | Fetch Docx/wiki blocks | Re-fetch page/properties/blocks | Re-read files and validate links/assets |

Do not perform platform-specific rewrites merely for visual styling. Require semantic parity: the same Markdown body, source claims, fields, section order, captions, formulas, links, and completion status must survive; only the small deltas above may differ.

## Shared Write Workflow

1. Read the task-specific content skill and identify its non-negotiable semantic contract.
2. Resolve the target platform and exact destination. Preserve the current platform for existing documents.
3. Fetch or read the current document, hierarchy, properties/frontmatter, linked assets, and nearby conventions.
4. Prepare one canonical Markdown draft: title, metadata, sections, lists, tables, callouts, formulas, figures/captions, links, and child artifacts.
5. Preserve the Markdown directly where possible. Convert only unsupported callouts, captions, properties/frontmatter, hierarchy, diagrams, or upload references to native target primitives.
6. Make the narrowest safe update. Preserve user notes and trusted existing media unless replacement is requested.
7. Re-fetch or re-read the durable result. Run content and platform validators, then report the actual destination and any unsupported native feature.

## Migration Rules

- Treat migration as copy-and-verify by default. Do not delete the source document unless the user explicitly asks after the destination passes verification.
- Preserve source URLs, original creation context, authorship, dates, citations, captions, formulas, attachments, and child-page relationships.
- Convert platform-only constructs explicitly. Examples: Feishu whiteboard to an exported image plus editable outline for Notion, Notion database properties to Obsidian frontmatter, or Obsidian wikilinks to Notion page links.
- Record any lossy conversion. Do not call a migration complete when formulas, figures, captions, tables, or child documents were silently dropped.

## Acceptance Checklist

Before declaring a document complete:

- the chosen platform matches the user's target or the existing document;
- the task-specific content contract passes without platform-specific omissions;
- title, hierarchy, metadata/properties/frontmatter, section order, links, formulas, media, and captions were verified in the durable destination;
- user-authored notes and trusted assets were preserved;
- no syntax from another platform remains as reader-facing residue;
- temporary files were cleaned only after the durable copy was verified;
- the response names the platform and actual write status instead of implying a write that did not occur.
