---
name: paper-pdf2zh-notion-import
description: Import a paper's original and pdf2zh Chinese PDFs into Notion as a correctly nested child-page package, then repair the Chinese manuscript against the deep-dive standard. Use when the user gives an arXiv PDF URL or paper title and asks to pdf2zh, import the Chinese paper into Notion, or place translated paper PDFs in a Notion page.
---

# Paper PDF2ZH to Notion Import

This is the canonical workflow for importing a paper PDF and its `pdf2zh` Chinese translation into Notion. It is a delivery workflow, not merely a file upload. The imported PDF page is a draft until the Chinese manuscript has passed two independent repair/read-back rounds.

Use [`paper-deep-dive`](../paper-deep-dive/SKILL.md) for source fidelity, formulas, figures, tables, references, and the final Chinese manuscript standard. Use [`notion-doc-workflow`](../notion-doc-workflow/SKILL.md) for Notion page verification. Use [`pdf`](../pdf/SKILL.md) and the local MinerU/pdf2zh tooling for extraction and translation.

## Trigger

Use this skill when the user provides any of the following:

- an arXiv PDF URL;
- an arXiv identifier or paper title;
- a request to download a paper, run `pdf2zh`, and import the Chinese paper into Notion;
- a request to repair a previously imported `pdf2zh` Chinese paper page.

The default target is the Notion page explicitly supplied by the user. If no target is supplied, stop and ask for the target page before uploading anything.

## Canonical Notion Hierarchy

Import directly into the exact Notion page supplied by the user:

```text
User-specified Notion destination
└── Chinese PDF child page
```

Do not create an intermediate Paper container page, staging page, or extra wrapper page. The native Notion PDF importer creates the child page automatically when the import location is set to the supplied destination. Do not move the imported page afterward merely to introduce another hierarchy layer.

The original English PDF is normally kept local for source verification and is not imported. Import additional PDF variants only when the user explicitly requests them.

## File Naming

Rename the imported PDF pages after import, or rename the local PDFs before import when Notion preserves the filename:

- Original English PDF: the verified original English paper title exactly, without `.pdf` in the Notion page title.
- Chinese PDF: the verified Chinese paper title exactly, without `.pdf` in the Notion page title.
- Optional bilingual PDF: `English Title｜中英对照` only when the user explicitly asks to retain it.

Do not use `D4RT.pdf`, `D4RT.zh.mono.pdf`, `paper.pdf`, `translated.pdf`, `BabelDOC`, or temporary filenames as reader-facing Notion titles.

## End-to-End Procedure

### 1. Resolve and verify the source

1. Resolve the paper from the supplied arXiv URL, identifier, or title.
2. Download the latest arXiv PDF and save all `pdf2zh` outputs directly under `/Users/wangpu/Downloads/`. Use a task-specific subdirectory such as `/Users/wangpu/Downloads/<task-slug>/` to avoid collisions. Do not save paper conversion outputs under the vault or `.tools/tmp/`.
3. Record the verified English title, Chinese title, authors, arXiv ID/version, and source URL.
4. Resolve and archive the official arXiv HTML and LaTeX source when available. They are the semantic and structural authority for the repair, not optional spot-check material. Use the rendered PDF as the authority for visual order, page completeness, figure/table placement, and layout only. Treat `pdf2zh`, OCR, MinerU, and the imported Notion blocks strictly as a draft to be reconciled against those official sources.
5. Before editing, build a source map that inventories every source section, subsection, natural paragraph, display equation, inline formula span, figure/caption, table/title/note, algorithm, footnote, appendix/supplement item, citation, and reference. Assign stable source IDs and map each existing Notion block to one or more source IDs. Record missing, duplicated, split, fused, reordered, or corrupted blocks explicitly.
6. If official HTML and LaTeX disagree with extracted PDF text, prefer LaTeX for logical structure, paragraph boundaries, formulas, citations, labels, and captions; use official HTML as the rendered semantic cross-check; use the PDF to resolve visual placement and completeness. Never infer a source paragraph boundary from Chinese punctuation or adjacent Notion blocks when HTML/LaTeX is available.
5. Do not infer identity from a filename alone. If the title cannot be verified, stop before importing.

### 2. Run pdf2zh

1. Run the local `pdf2zh` workflow on the downloaded original PDF. Prefer the established local script/toolchain; do not invent a second translation tool.
2. Retain the original PDF and the translated Chinese PDF until Notion import and verification are complete.
3. If both mono and dual outputs exist, choose the variant according to the user's request. Default to the Chinese mono PDF for the Chinese manuscript page. The original English PDF is used for verification and is not imported unless the user explicitly requests it.
4. Treat all pdf2zh output as draft material. It is not compliant merely because the PDF opens or the translation is readable.

### 3. Import directly into the specified Notion page

Use **Notion desktop**, not a browser tab, Notion API, CLI, or Markdown import, for the PDF import operation. The user specifically expects Notion's native PDF importer to create child pages.

1. Open the user-specified destination in the Notion desktop app.
2. Use that page's `Actions` menu → `Import` → `PDF`.
3. Confirm the import location is exactly the user-specified destination page. Do not create an intermediate container page.

### 4. Import the PDF as a child page

Import only the Chinese pdf2zh PDF into the user-specified destination page. Notion will create the paper as a child page. Do not import the original English PDF unless explicitly requested; English source material is only for verification.

For each file:

1. Select the file in the native macOS file picker.
2. Confirm the Notion dialog says `Import location: <user-specified destination page>`.
3. Continue the import and wait until Notion reports `Import complete`.
4. Return to the supplied destination page and verify the new child link exists.
5. Rename the child page to the verified Chinese title.

Do not paste the PDF into the body of the destination page. Do not use a browser upload control if the Notion desktop importer is available. Do not report completion while Notion still says `Import in progress`.

### 5. Repair the Chinese imported page: two mandatory rounds

The imported Chinese page is only a draft. Perform two distinct repair rounds, with a fresh read-back between them.

**Write-back safety requirement.** Never use the raw serialized text returned by a Notion connector as page content. If a connector response wraps the page in JSON, parse the outer JSON first, then extract only the content between the actual `<content>` markers. Before any write, verify that the extracted string starts with the page's paper content rather than connector metadata or another app's accessibility tree.

**Hard no-whole-page-rebuild rule.** An already imported PDF page is a structured document, not a Markdown reconstruction target. Unless the user explicitly authorizes destructive replacement, never use `replace_content`, whole-page Markdown replacement, or a full-page delete-and-recreate operation. Default to native block edits or targeted replacements by known block ID/span. Before each repair batch, save a recovery snapshot of page properties and the complete block tree, including block types, images, equations, tables, captions, links, and text. Keep each batch small and re-fetch immediately after writing. If block counts, heading levels, image/equation/table counts, captions, or untouched block IDs change unexpectedly, stop and report the mismatch; do not continue writing. If the available tool can only perform a whole-page replacement, stop and report the blocker instead of using it.

#### Round 1: structural and source-fidelity repair

Compare the imported page with the original PDF and official HTML/LaTeX. Repair:

- verified Chinese page-property title and opening English title/author/resource block; the English title is an ordinary paragraph, not a heading; do not place a Chinese title under the English title;
- manuscript-only scope: do not add `精读稿`, `精读部分`, a Paper Card, `论文解析树`, close reading, or mechanism synthesis; leave an existing `精读稿` untouched unless the user asks to remove or revise it;
- heading hierarchy and source order;
- broken paragraph joins, duplicate headers/footers, and conversion residue;
- all figures, figure images, complete translated captions, and figure placement;
- all tables, table titles/notes, cell boundaries, and missing table images;
- inline and display formulas, equation numbers, symbols, superscripts, subscripts, and tags;
- references and body citations, with citation labels as plain `[n]` chrome and only `n` as the link text when linked;
- appendices, supplementary sections, algorithms, and reference lists;
- author emails as ordinary visible text, not intentionally linked or code-formatted.

**Mandatory paragraph-boundary reconstruction.** Reconstruct the manuscript against the official HTML/LaTeX source map paragraph by paragraph. Each source natural paragraph must correspond to one coherent target paragraph unless a native figure, table, algorithm, or display-equation block necessarily interrupts it. Merge PDF column/page-break fragments; split falsely fused source paragraphs; remove repeated overlap introduced by page headers, footers, captions, or column extraction; and preserve the original paragraph order. Chinese grammar, paragraph length, punctuation, and visual adjacency are only anomaly detectors and may not serve as the final authority. Do not preserve a `pdf2zh` block boundary merely because it already exists in Notion.

**Mandatory full-content reconciliation.** Apply the same source map to headings, prose, inline and display math, figures/captions, tables/titles/notes, algorithms, footnotes, appendices/supplements, citations, and References. A repair that validates only block counts or selected formulas is incomplete. For every source ID, record exactly one of: mapped and verified; intentionally excluded by the user; or unresolved with an explicit reason.

Use HTML/LaTeX to correct formulas, captions, references, and structure; use the PDF to verify visual placement and page completeness. Preserve images already present unless the source comparison proves they are wrong or missing. Never remove an image just to simplify formatting.

#### Round 2: independent audit and correction

Read the repaired page again as a separate QA pass. Do not assume Round 1 fixed everything. Sample:

- the opening pages and abstract;
- at least one formula-heavy middle section;
- every figure/table-heavy section;
- the final discussion/conclusion;
- every appendix/supplement section;
- the full reference list and several body citations.

Search specifically for `Invalid equation`, malformed `$`, duplicated `$$`, `[n` used as link text, missing `]`, `待补`, `TODO`, `EW_IMG_`, raw `file://`, MinerU paths, duplicate captions, broken table pipes, untranslated generic technical terms, and page-order jumps. Correct every confirmed issue against the source. If a visual or formula cannot be reliably represented natively, keep the exact source LaTeX or an official PDF/HTML image as the fallback and label the fallback.

Before any Notion Markdown write that inserts or rewrites numeric body citations, escape the outer bracket (Notion always turns the first cite into link text `[n` otherwise):

```bash
python3 ".tools/skills/notion-doc-workflow/scripts/prepare-notion-citation-markdown.py" draft.md -o notion-ready.md
# then write notion-ready.md (contains \[[n](url)] / \[[n](url), [m](url)])
```

After the write, run the rich_text fixer as a safety net before claiming Round 2 complete:

```bash
python3 ".tools/skills/notion-doc-workflow/scripts/fix-notion-citation-rich-text.py" <chinese-page-id-or-url>
python3 ".tools/skills/notion-doc-workflow/scripts/fix-notion-citation-rich-text.py" <chinese-page-id-or-url> --check-only
```

`--check-only` must exit 0. Do not trust Markdown export alone for link ranges.

Two rounds means two full source/read-back cycles, not two passes over the same stale export.

Round 2 must independently re-run the source-map coverage and paragraph-boundary comparison from fresh official HTML/LaTeX and fresh Notion blocks. A heuristic scan for short blocks, unfinished Chinese sentences, or unchanged media counts is insufficient. The completion record must include source-paragraph count, mapped target-paragraph count, split/fused/duplicate/reordered mismatch counts, and unresolved source IDs; all mismatch and unresolved counts must be zero unless the user explicitly accepted a documented exception.

### 6. Verify the package

Before delivery, verify all of the following in Notion:

- destination page contains the intended Chinese PDF child page directly under it;
- child page titles use paper titles, not temporary filenames;
- Chinese page has complete source-order content, not only a summary or selected sections;
- figures and captions are present and in the correct relative positions;
- tables are present and readable;
- inline formulas render as inline formulas; display formulas are centered/native where supported and preserve numbering;
- body citations use plain outer brackets and digit-only link text (Blocks API / `fix-notion-citation-rich-text.py --check-only` must pass; do not trust Markdown export alone);
- references are numbered paragraphs, not accidental bullet lists;
- appendix and supplementary content is present;
- no raw local paths, temporary filenames, or migration artifacts remain;
- the page was re-read after the second repair round.
- no whole-page replacement or delete-and-recreate operation was used without explicit user authorization;
- each repair batch had a pre-write recovery snapshot and a post-write block-level re-fetch;
- untouched sections retained their block types, hierarchy, media, formulas, tables, captions, and links.
- an official HTML/LaTeX-derived source map exists and covers the complete source package;
- every source natural paragraph has been reconciled to the target page, with zero unexplained split, fused, duplicated, omitted, or reordered paragraphs;
- completion was not inferred from Chinese sentence heuristics, block-count preservation, or PDF text extraction alone.

If any item fails, report the package as incomplete and continue repairing. Do not call the initial PDF import the final result.

### 7. Clean up local artifacts

Only after Notion import and the second repair/read-back pass succeed:

1. Delete pdf2zh intermediate output, MinerU Markdown, page images, and temporary conversion files.
2. Keep the original source PDF only if the user explicitly wants a local copy; otherwise delete it too.
3. Never delete the Notion pages or their uploaded content as part of local cleanup.
4. Report which local artifacts were removed and which, if any, were retained.

## Failure Handling

- If Notion desktop is unavailable, do not silently substitute browser/API/CLI import. Report the blocker.
- If the native file picker is open, re-query the current app state before every click; element indices change after selection and upload progress.
- If an import is still processing, wait and poll until `Import complete` or an explicit error.
- If the wrong page was selected as import location, stop and correct the location before uploading the next file.
- If a paper title, arXiv version, or Chinese translation cannot be verified, stop before renaming or delivery.
- If a paper is too difficult to repair in one task, leave the draft clearly marked as incomplete and list the unresolved source-grounded issues; never present a partial page as compliant.

## Compact Completion Report

The final response should state:

- source paper and arXiv version;
- Notion destination and direct Chinese child-page link;
- English source PDF path used for verification, when retained locally;
- confirmation that the Chinese page passed two repair rounds;
- local pdf2zh/MinerU cleanup status;
- any remaining verified limitations.
