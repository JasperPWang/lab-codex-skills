# Skill Manifest

This repository is a lab **agent skill** bundle (Codex, Cursor, Antigravity, and any loader that reads `SKILL.md`). It keeps user-maintained skills and vendored/downloaded skills in one place so teammates can clone one repository and expose skills via the install / link scripts.

## Canonical Location

On the maintainer machine the working copy is:

`WorldModelVault/.tools/skills`

Agent discovery paths (`~/.codex/skills`, project `.cursor/skills`, project `.agents/skills`, etc.) should contain **symlinks** to this directory, not independent copies.

## Document Backends

Content skills are Markdown-first. Route durable writes with `research-doc-workflow`, then the matching adapter:

| Backend | Adapter |
| --- | --- |
| Feishu / Lark | `feishu-doc-workflow` |
| Notion | `notion-doc-workflow` |
| Obsidian / Markdown | `obsidian-doc-workflow` |

## User-Maintained Lab Skills

- `ai-research-workflow`
- `bilingual-source-archive`
- `chinese-technical-writing`
- `daily-research-review`
- `experiment-report-writing`
- `feishu-doc-workflow`
- `notion-doc-workflow`
- `obsidian-doc-workflow`
- `intern-interview-intake`
- `lark-whiteboard`
- `obsidian-clipping-ai-summary`
- `paper-card-delivery`
- `paper-deep-dive`
- `paper-rag`
- `paper-to-slides-skill`
- `pdf`
- `research-doc-workflow`
- `survey-builder`

## Vendored Or Downloaded Skills

Academic Research Skills:

- `academic-research-suite`
- `academic-research-skills`
- `academic-paper`
- `academic-paper-reviewer`
- `academic-pipeline`
- `deep-research`

PaperSpine:

- `paper-spine`
- `paper-spine-audit`
- `paper-spine-build`
- `paper-spine-citation`
- `paper-spine-humanize`
- `paper-spine-intake`
- `paper-spine-latex`
- `paper-spine-research`
- `paper-spine-rewrite`
- `paper-spine-translate`
- `paper-spine-ui`
- `paper-spine-update`

Nature-style academic workflows:

- `nature-academic-search`
- `nature-citation`
- `nature-data`
- `nature-figure`
- `nature-paper-to-patent`
- `nature-paper2ppt`
- `nature-polishing`
- `nature-reader`
- `nature-response`
- `nature-reviewer`
- `nature-skills`
- `nature-writing`

Other research/workflow skills:

- `cite-verify`
- `drawio`
- `drawio-skill`
- `feynman-learning`
- `grant-writer`
- `latex-writer`
- `llm-wiki-skill`
- `repro-pack`
- `research-dev-standards`
- `stats-sanity`

## Compatibility Aliases

The install / link scripts create these aliases in each discovery root:

- `feishu-cli` -> `feishu-doc-workflow`
- `llm-wiki` -> `llm-wiki-skill`
- `paper-to-slides` -> `paper-to-slides-skill`

## Excluded From Publication

Hidden migration archives are kept locally for recovery but excluded from Git:

- `.machine-local-archives/`
- `.archive-before-consolidation-*/`
- `.archive-before-vault-consolidation-*/`
- `.archive-before-vault-link-*/`
