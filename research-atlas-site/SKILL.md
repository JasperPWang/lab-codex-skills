---
name: research-atlas-site
description: Design, build, revise, or audit durable academic research atlas websites that combine project-style introductions, searchable paper collections, multidimensional taxonomies, datasets, assets, and statistics. Use for standalone research knowledge websites; do not use for ordinary Notion, Feishu, or Obsidian page formatting.
---

# Research Atlas Site

Build the site as a durable research interface rather than a visually enhanced document. Preserve the user's subject taxonomy, bilingual conventions, metadata requirements, and preferred deployment platform.

## Default architecture

Prefer a static, data-driven pipeline unless the requested collaboration or access-control model requires a backend:

1. Keep canonical research records in structured YAML, JSON, or Markdown frontmatter with stable IDs.
2. Normalize, enrich, and validate records during the build.
3. Generate pages, search indexes, statistics, and reusable exports from the same source of truth.
4. Deploy through version control and CI to static hosting such as GitHub Pages or Cloudflare Pages.

Avoid maintaining the same metadata independently in page markup, tables, and bibliography files. Cache remote enrichment such as abstracts and PDF thumbnails so builds remain reproducible and do not depend on every upstream service being available.

## Information architecture

When appropriate, provide these complementary views rather than one long document:

- Overview: scope, research map, key resources, and recent updates.
- Papers: searchable cards ordered newest to oldest by default.
- Taxonomy: multidimensional research classification, not only a folder tree.
- Datasets and Benchmarks.
- Assets and Tools, including projects, code, models, and demos.
- Statistics derived from canonical records.

Treat a paper card as a core reusable unit. Support title, Chinese title when requested, publication date, venue, authors, abstract or summary, thumbnail, taxonomy fields, and only the resource links that actually exist: Paper, Project, Code, Dataset, Model, Demo, BibTeX, and internal notes.

## Data and quality rules

- Use stable identifiers and controlled vocabularies for taxonomy fields.
- Represent cross-cutting concepts with multiple orthogonal fields rather than duplicating a paper across directories.
- Sort dated scholarly records from new to old unless the user requests otherwise.
- Keep Chinese and English as distinct fields so layouts can render them consistently.
- Validate required fields, dates, URLs, duplicate DOI/arXiv IDs, taxonomy values, and build output in CI.
- Distinguish source-backed metadata from editorial summaries and personal reading state.
- Keep Notion, Feishu, or Obsidian links optional and secondary; the website's canonical records must remain platform-neutral unless the user explicitly chooses otherwise.

## Implementation choices

For a new personal or small-team atlas, prefer Astro with TypeScript and structured content files. Plain HTML, CSS, and JavaScript are acceptable for a narrow single-topic collection. Introduce a database or server only when live multi-user editing, private access, or transactional workflows justify it.

Reuse the reference site's architectural principles and interaction patterns, not its copyrighted code, text, or images. Public source without an explicit license is not permission to copy it directly.

## Reference

For analysis, redesign, or implementation inspired by the Digital Humans survey site, read [references/digital-humans-reference.md](references/digital-humans-reference.md). It records the source URLs, observed pipeline, reusable patterns, and adaptation guidance.
