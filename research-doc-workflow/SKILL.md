---
name: research-doc-workflow
description: Route creation, editing, migration, and verification of research documents across Feishu/Lark, Notion, and Obsidian/Markdown while preserving content contracts, hierarchy, formulas, images, captions, links, and source provenance. Use whenever a task-specific research skill writes or normalizes paper cards, deep dives, surveys, experiment reports, bilingual source archives, daily reviews, meeting notes, or wiki pages, or whenever the user names Feishu, Notion, Obsidian, a wiki/page URL, or a local Markdown destination. Routes to feishu-doc-workflow, notion-doc-workflow, or obsidian-doc-workflow.
---

# Research Document Workflow

## Core Contract

Keep research content standards independent from storage platforms. Use one canonical Markdown-first document for the shared body: headings, paragraphs, lists, block quotes, links, tables, code blocks, and LaTeX formulas should remain the same unless the target demonstrably requires a small conversion. The task-specific skill owns what the document means and which sections are required; this skill selects the destination backend, loads the matching platform adapter, applies only the necessary platform deltas, performs the write, and verifies the durable result.

Do not create separate Feishu, Notion, and Obsidian versions of the same **content** skill or template. Maintain one Markdown structure and three thin delivery adapters (`feishu-doc-workflow`, `notion-doc-workflow`, `obsidian-doc-workflow`) so field definitions, evidence standards, wording, and acceptance gates cannot drift.

## Platform Resolution

Resolve the target in this order:

1. Explicit user instruction (`写到飞书` / `写到 Notion` / `写到 Obsidian/vault`).
2. URL or path in the request (`feishu.cn` / `larksuite.com` → Feishu; `notion.so` → Notion; vault `.md` path / WorldModelVault folder → Obsidian).
3. Platform of an **existing** durable document being updated (never silently migrate).

The user normally supplies a link or an explicit destination. If none of the above resolves a single platform, ask one concise destination question. Do **not** default to Feishu (or any other platform) and do not silently duplicate across platforms.

Never silently migrate, duplicate, or delete an existing durable document. A platform change requires an explicit target or a user-approved migration task.

## Backend Router

After resolving the platform, also load the matching adapter:

### Feishu / Lark → [`feishu-doc-workflow`](../feishu-doc-workflow/SKILL.md)

- Wiki resolution, fetch-before-write, narrow block edits, native images/captions/formulas/whiteboards, hierarchy preservation, and fetch-after-write verification.
- Use `lark-whiteboard` only when an editable Feishu whiteboard or mind map is required.

### Notion → [`notion-doc-workflow`](../notion-doc-workflow/SKILL.md)

- Search/fetch the destination before updating. Resolve the exact parent page, database, or data source and inspect required properties before creating records.
- Prefer native Notion headings, callouts, equations, image captions, tables, page links, relations, and database properties.
- Do not paste Obsidian frontmatter, Obsidian callout fences, Feishu block artifacts, or absolute vault paths into reader-facing Notion content.
- If Notion tools are unavailable, report that Notion must be connected. Do not claim that a page was written and do not silently redirect to Feishu or Obsidian.

### Obsidian / Markdown → [`obsidian-doc-workflow`](../obsidian-doc-workflow/SKILL.md)

- Inspect the target folder, neighboring notes, frontmatter schema, attachment convention, and link style before editing.
- Use YAML frontmatter, `> [!type]` callouts, `[[wikilinks]]`, relative assets, and `$...$` / `$$...$$` as required by the vault.
- Also use [`llm-wiki`](../llm-wiki-skill/SKILL.md) when the task includes wiki ingestion, provenance, atomic notes, indexes, or Research-Wiki placement. Format/write verification still belongs to `obsidian-doc-workflow`.

## Small Platform Deltas

Assume Markdown parity first. Convert only the features that are not represented consistently:

| Small delta | Feishu / Lark | Notion | Obsidian / Markdown |
|---|---|---|---|
| Parent/child hierarchy | Wiki node and child pages | Parent page, subpages, or database relations | Folder/MOC note plus links |
| Callout | Native callout when supported | Native callout when supported | Keep `> [!type]` callout |
| Inline/display math | Map to native equation blocks without changing TeX | Map to inline/block equations | Keep `$...$` / `$$...$$` |
| Image caption | Native image caption | Native image caption | Vault convention or meaningful Markdown alt text; avoid duplicate caption paragraph |
| Structured metadata | Compact native text/properties | Database/page properties | YAML frontmatter |
| Paper-card metadata | One native text block with four hard-break lines | One paragraph with exactly three `<br>` hard breaks | Four physical Markdown lines |
| References | `[n]` plain text + ` \| [url](url)` (display = URL); no `1.` lists | Same semantic form in rich text; no ordered-list renumbering | Same Markdown form |
| Body citations | Number links to the same PDF URL as References | Same | `[[n](pdf-url)]` |
| Editable tree | Native whiteboard/mind map | Page/database hierarchy or supported embed | Mermaid, Canvas, or linked outline |
| Cross-platform residue | Strip Notion `<br>` tricks and Obsidian `![[` / frontmatter fences from reader text | Strip Feishu XML/block chrome and Obsidian callout fences | Strip Feishu tokens and Notion `<br>` metadata HTML |
| Verification | Fetch Docx/wiki blocks | Re-fetch page/properties/blocks | Re-read files and validate links/assets |

Do not perform platform-specific rewrites merely for visual styling. Require semantic parity: the same Markdown body, source claims, fields, section order, captions, formulas, links, and completion status must survive; only the small deltas above may differ.

## Shared Write Workflow

1. Read the task-specific content skill and identify its non-negotiable semantic contract.
2. Resolve the target platform and exact destination. Preserve the current platform for existing documents.
3. Load the matching `*-doc-workflow` adapter.
4. Fetch or read the current document, hierarchy, properties/frontmatter, linked assets, and nearby conventions.
5. Prepare one canonical Markdown draft: title, metadata, sections, lists, tables, callouts, formulas, figures/captions, links, and child artifacts.
6. Preserve the Markdown directly where possible. Convert only unsupported callouts, captions, properties/frontmatter, hierarchy, diagrams, citation chrome, or upload references to native target primitives.
7. Make the narrowest safe update. Preserve user notes and trusted existing media unless replacement is requested.
8. Re-fetch or re-read the durable result. Run content and platform validators, then report the actual destination and any unsupported native feature.

## Migration Rules

- Treat migration as copy-and-verify by default. Do not delete the source document unless the user explicitly asks after the destination passes verification.
- Preserve source URLs, original creation context, authorship, dates, citations, captions, formulas, attachments, and child-page relationships.
- Convert platform-only constructs explicitly. Examples: Feishu whiteboard to an exported image plus editable outline for Notion/Obsidian, Notion database properties to Obsidian frontmatter, or Obsidian wikilinks to Notion page links.
- Record any lossy conversion. Do not call a migration complete when formulas, figures, captions, tables, or child documents were silently dropped.

## Acceptance Checklist

Before declaring a document complete:

- the chosen platform matches the user's target or the existing document;
- the matching `*-doc-workflow` adapter was used;
- the task-specific content contract passes without platform-specific omissions;
- title, hierarchy, metadata/properties/frontmatter, section order, links, formulas, media, and captions were verified in the durable destination;
- user-authored notes and trusted assets were preserved;
- no syntax from another platform remains as reader-facing residue;
- temporary files were cleaned only after the durable copy was verified;
- the response names the platform and actual write status instead of implying a write that did not occur.
