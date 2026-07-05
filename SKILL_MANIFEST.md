# Skill Manifest

This repository is a lab skill bundle. It intentionally keeps user-maintained
skills and vendored/downloaded skills in one place so teammates can clone one
repository and expose the skills to Codex with `scripts/link-to-codex-skills.sh`.

## Canonical Location

The canonical working copy on this machine is:

`WorldModelVault/.tools/skills`

`~/.codex/skills` should contain symlinks to this directory, not independent
copies.

## User-Maintained Lab Skills

- `ai-research-workflow`
- `bilingual-source-archive`
- `chinese-technical-writing`
- `daily-research-review`
- `feishu-doc-workflow`
- `intern-interview-intake`
- `lark-whiteboard`
- `obsidian-clipping-ai-summary`
- `paper-card-delivery`
- `paper-deep-dive`
- `paper-rag`
- `paper-to-slides-skill`
- `pdf`
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
- `feynman-learning`
- `grant-writer`
- `latex-writer`
- `llm-wiki-skill`
- `repro-pack`
- `research-dev-standards`
- `stats-sanity`

## Compatibility Aliases

The install script creates these compatibility aliases in `~/.codex/skills`:

- `feishu-cli` -> `feishu-doc-workflow`
- `llm-wiki` -> `llm-wiki-skill`
- `paper-to-slides` -> `paper-to-slides-skill`

## Excluded From Publication

Hidden migration archives are kept locally for recovery but excluded from Git:

- `.machine-local-archives/`
- `.archive-before-consolidation-*/`
- `.archive-before-vault-consolidation-*/`
- `.archive-before-vault-link-*/`
