---
name: repo-bilingual-readme
description: Create, update, or repair English–Chinese paired README and other Markdown documents in GitHub repositories, including Awesome paper lists. Use for 仓库英中对照、README 英中对照、漏译修复 and associated paper-resource enrichment; not for Chinese-only translations, Notion paper cards, or general bilingual article archives.
---

# Repository English–Chinese Edition

## Scope and source preservation

Create a faithful English–Chinese reading edition in the repository, not a summary or a rewritten survey. These defaults capture this user's established preferences; explicit current instructions override them.

- Keep upstream English files unchanged by default. Create or maintain `README_zh-CN.md`; for another requested document use a sibling such as `not-good-ideas_zh-CN.md`, following its actual basename and existing repository convention. Inspect existing files before choosing names; do not duplicate an existing bilingual edition.
- Cover every document explicitly requested, including non-README Markdown files. Do not translate unrelated files just because they are in the repository.
- Resolve owner, repository, branch, path, and source revision from the actual repository. Inspect the current bilingual file, git status, and relevant diffs before editing; preserve user changes.
- Preserve English wording, technical meaning, links, images, citations, code, and licenses. Translate all reader-facing prose without omitting paragraphs or replacing them with summaries. Do not alter executable examples to make them bilingual.
- A separate bilingual file reduces collisions with upstream README edits, but does not automatically synchronize translations or eliminate all merge conflicts. For later updates, compare source revisions and reconcile changes into the bilingual edition; never blindly overwrite it.
- If the source revision used for an earlier edition is unknown, audit against the complete current source rather than assuming a partial diff proves completeness. Keep provenance in working notes or an existing maintenance convention, not intrusive metadata added without need.

## Layout defaults

Headings and contents entries use **English + exactly one ordinary ASCII space + Chinese** on the same line. Apply this to every heading depth, including tertiary taxonomy categories, not just the table of contents. Do not use `/`, `｜`, a dash, a line break, or a full-width space as the language separator. Preserve punctuation that genuinely belongs to the source title.

```markdown
## Taxonomy 分类体系
### Main Differences 主要区别

- [Taxonomy 分类体系](#taxonomy-分类体系)
```

Body text uses English first, then Chinese below it, without repeated `Original` / `Translation` / `原文` / `译文` labels:

```markdown
The method learns object-centric representations.

该方法学习以对象为中心的表征。

- **Instance-aware modeling**<br>**实例感知建模**
  - Each object is modeled independently.<br>每个对象均被独立建模。
```

- In tables and compact list items, use `<br>` for a real rendered line break inside the same cell/item; a plain source newline may collapse or break the table. Keep English and Chinese belonging to one item together.
- Short table headers may use `English 中文`; descriptive cells, taxonomy explanations, main differences, and paper titles need real English–Chinese pairing, not untranslated English or a repeated acronym masquerading as a translation.
- Preserve exact official English paper titles. Add faithful Chinese titles below them; retain method names/acronyms and translate the meaningful subtitle. Explain in working notes when a proper-name-only title legitimately needs no translation.
- Keep existing badges, images, HTML, equations, link destinations, and code fences functional. Translate meaningful prose in collapsible blocks, image alt text, captions, and footnotes; retain identifiers, commands, bibliographic names, and equations as appropriate.
- For Chinese prose use `chinese-technical-writing` when terminology decisions need its guidance; do not translate official model/dataset/method names mechanically.
- Rebuild or adjust contents anchors after heading translation. Verify actual GitHub-compatible anchors, including punctuation and duplicate headings. Do not assume English-only anchors still work; preserve explicit anchors where useful.

## Paper-list chronology

- Sort paper entries newest to oldest **within each existing category or subsection**. Preserve the source taxonomy unless the user asks to change it; do not flatten unrelated categories to create one global ranking.
- Reverse year groups where needed, then order dated entries within each group. Move the whole entry, including translation, links, notes, and associated figures.
- Use the source's declared date semantics consistently (e.g., publication year or release date). When dates are absent, prefer verified first-public dates from official metadata; do not mix latest arXiv revisions with first release dates or infer dates from list position.
- With only a year available, keep stable relative order within that year instead of inventing months/days. Undated entries remain a clearly separate tail within the category; record unresolved dates in working notes.

## Paper, Project, and Code links

For paper-list creation or enrichment, place verified Paper, Project, and Code links together in the paper cell/item, using the same compact link style already used for Paper. For translation-only or format-only repairs, preserve existing resources and do not broaden the task into a new link investigation unless requested.

```markdown
| Paper 论文 | Year 年份 |
| --- | --- |
| Exact English Paper Title<br>准确的中文论文标题<br>[Paper](https://example.org/paper.pdf) [Project](https://example.org/project/) [Code](https://github.com/example/repository) | 2026 |
```

The URLs above are schematic examples, never deliverable links. Retain valid original Paper links unless repair is required. Add optional resources only when confirmed; do not insert empty placeholders or fabricate predictable URLs. Do not create Notion cards or backfill Notion card links as part of this workflow.

To reduce missed resources, use an entry-by-entry search ledger in working notes, not a spot check:

1. Inspect the existing README links, official abstract/proceedings page, and available official paper text for project/code links.
2. Follow the official project page to its Code/GitHub links; inspect official author/lab pages and repositories where relevant.
3. For still-missing resources, search the exact paper title and method name with `project`, `code`, `GitHub`, and author/lab identifiers. Resolve title collisions against authors and paper identifiers.
4. Revisit every missing Project/Code slot in a second pass through remaining official routes. An empty slot after one search is not a completed check.
5. Record each slot as verified, searched-but-not-found, or blocked, with source evidence. Do not claim a blocked search proves no resource exists, or promise that no future/undiscoverable link can be missed.

A working URL alone is insufficient: confirm that it belongs to this paper and is official or author-maintained. Do not substitute a third-party reproduction. Follow redirects and ensure a project URL is paper-specific rather than a generic lab homepage. If an official repository only contains a project website or promises future code, do not label it as released Code; use it as Project when appropriate. Clearly preserve access restrictions when an official code route is gated.

## Completeness and rendering gate

Before editing, inventory source units: headings at every depth, paragraphs, list items, table rows/cells, paper entries, captions, footnotes, and meaningful HTML sections. Maintain a source-to-target correspondence as working notes for long documents. Sorting changes position, not coverage.

Before delivery:

- Compare every source unit with its target counterpart. Check for missing, duplicated, shortened, or stale English text and missing Chinese translations. Review headings, tertiary categories, “main differences” cells, and the entire late portion of long paper lists explicitly.
- Check that each Chinese block actually translates its paired English block; mere presence of Chinese characters does not establish completeness. Proper names, code, and source-preserved bibliographic fields are documented exemptions, not excuses for missing prose.
- Compare paper-entry identifiers and counts within categories; verify dates are descending and that an entry's links/translation moved with it. Do not deduplicate distinct source entries automatically.
- Verify heading language separators, contents destinations, relative paths, escaped table pipes, `<br>` rendering, balanced code fences, and existing images/HTML. Inspect a rendered preview when available, especially for tables and nested lists. Do not claim visual validation when only source checks were possible.
- Review the final diff: original English source files and unrelated content must remain unchanged unless explicitly in scope. Re-read the saved target; after any authorized remote write, read the remote result back too.

Automated detection of English-only lines, row counts, or Chinese characters can flag candidates but cannot certify translation coverage. Pair structural checks with semantic review, and fix findings rather than only reporting totals.

## Delivery and authorization

For this user's GitHub repositories, publishing the bilingual edition is the default close-out: after the completeness gate, commit the bilingual Markdown on the current branch and `git push` to `origin`. Do not force-push. Do not rewrite English source files to add a language switcher unless that repo already has one. Put `[English](README.md)` (or the matching English sibling) at the top of the bilingual file. After push, read the remote file back and report the commit URL.

Do not interpret this skill as permission to sync unrelated upstream remotes, merge branches, open PRs, or edit other repositories. Never force-push as a routine synchronization step. If write access is missing, stop and state the blocker.

For partial work, missing source access, or unresolved write permissions, state exactly what remains; do not present an incomplete bilingual file as finished. Keep the final handoff brief with a file/page link and actual write/verification status. The user's default is to receive the updated document, not search statistics or a long audit report; surface only material limitations.
