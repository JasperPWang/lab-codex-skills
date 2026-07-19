# Third-Party Notices

This bundle contains a mix of original lab-maintained skills and vendored or
adapted third-party skill suites. Do not treat the whole repository as a single
license unless each included upstream license has been reviewed.

## Academic Research Skills

Included skills:

- `academic-research-suite`
- `academic-research-skills`
- `academic-paper`
- `academic-paper-reviewer`
- `academic-pipeline`
- `deep-research`

Recorded sources:

- `https://github.com/Imbad0202/academic-research-skills.git`
  - commit: `96b82e82142dc95f117595c207d3e150b078e411`
- `https://github.com/Imbad0202/experiment-agent.git`
  - commit: `9b063fa895eaf1f63ac99ac03f924f8d31aa8d26`

License evidence in this bundle:

- `academic-research-suite/ars/LICENSE`: Creative Commons
  Attribution-NonCommercial 4.0 International.

Practical note:

- This is suitable for non-commercial lab/internal research sharing. Review the
  upstream license before public or commercial reuse.

## PaperSpine

Included skills:

- `paper-spine`
- `paper-spine-*`
- `paper-spine-update`

Recorded source:

- `https://github.com/WUBING2023/PaperSpine`
- local version manifest: `paper-spine-update/paperspine_version.json`
- recorded version: `3.3.0`

Practical note:

- Keep the PaperSpine version manifest and updater scripts together. Review the
  upstream repository license before publishing outside the lab.

## Nature-Style Academic Workflows

Included skills:

- `nature-*`

Recorded local metadata:

- Some skills record `author: Yuan1z skill, refactored into static/dynamic layers`.
- Some skills record `author: Community contribution, refactored into static/dynamic layers`.

Practical note:

- The active local files do not currently record a complete upstream URL. Before
  a public GitHub release, recover or verify the original upstream source and
  license. For private lab sharing, keep this notice with the bundle.

## Feynman Learning

Included active skill:

- `feynman-learning`

Recorded source:

- `https://github.com/JasperPWang/feynman-learning-skills.git`
- archived upstream container commit: `1faca50`
- references `https://github.com/pengsida/learning_research`.

License evidence:

- Archived upstream container includes an MIT license.

## LLM Wiki Skill

Included active skill:

- `llm-wiki-skill`

Recorded source:

- `https://github.com/JasperPWang/llm-wiki-skill.git`
- active local Git HEAD observed before bundling: `05c8fb6`

License evidence:

- `llm-wiki-skill/LICENSE`: MIT for original skill files.
- `llm-wiki-skill/external/llm_wiki/LICENSE`: GPL-3.0 for the vendored
  `nashsu/llm_wiki` app.

Practical note:

- The vendored GPL-3.0 component is not relicensed by this bundle. Preserve its
  license file and attribution.

## Draw.io Diagram Skills

Included skills:

- `drawio` — official jgraph skill-cli style workflow
- `drawio-diagram-builder` — Will-hxw research diagram builder (XML + browser preview loop)
- `drawio-skill` — Agents365-ai extended diagram toolkit

Recorded sources:

- `https://github.com/jgraph/drawio-mcp`
  - path: `plugins/claude-code/skills/drawio/` (identical to Codex plugin copy)
  - commit: `8b03f1e57fe3fbeb373e3dc459824f6624a86d0c`
  - lab note: `shared/{xml,mermaid,style}-reference.md` vendored under `drawio/shared/`;
    `SKILL.md` reference URLs rewritten to relative paths for offline / GPU use
- `https://github.com/Will-hxw/drawio-diagram-builder-skill`
  - path: `skills/drawio-diagram-builder/`
  - commit: `a922507ccd51815f4e8764846d640a65b5fb6f7e`
  - recorded skill version: `0.4.1`
- `https://github.com/Agents365-ai/drawio-skill`
  - path: `skills/drawio-skill/`
  - commit: `6f33563adce24450003d1cb61111ebbcc5579f28`
  - recorded skill version: `1.34.0`

License evidence in this bundle:

- `drawio/LICENSE`: Apache License 2.0
- `drawio-diagram-builder/LICENSE`: MIT
- `drawio-diagram-builder/assets/icons/tabler/LICENSE`: MIT (Tabler Icons)
- `drawio-skill/LICENSE`: MIT

Practical note:

- `drawio` and `drawio-skill` expect the native draw.io desktop CLI (`draw.io` /
  `drawio`) for PNG/SVG/PDF export. Agents365 `drawio-skill` optionally uses
  Graphviz (`dot`) for `scripts/autolayout.py`.
- `drawio-diagram-builder` primarily uses Python preview scripts plus a
  diagrams.net iframe (`embed.diagrams.net`); desktop CLI export is optional.
  Browser automation and internet access are required for the iterative preview
  loop. Review upstream licenses before commercial reuse.

## OpenAI, Plugin, And Runtime Skills

This repository does not vendor OpenAI bundled/runtime/plugin-cache skills such
as browser, Chrome, computer-use, Gmail, Google Drive, GitHub, Hugging Face,
Notion, Zotero, Data Analytics, documents, presentations, or spreadsheets.
Those remain managed by Codex/plugin installation.
