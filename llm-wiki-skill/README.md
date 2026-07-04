# LLM Wiki Skill

A Codex-native skill for maintaining a personal Markdown / Obsidian research
wiki without running a separate app, API server, or local model service.

This skill helps Codex ingest curated sources, create and update durable wiki
notes, answer questions with citations, lint knowledge gaps, analyze a Markdown
knowledge graph, and manage review or deep-research queues.

## Install

Clone this repository and link the skill into Codex:

```bash
git clone --recurse-submodules https://github.com/WangPu1999/llm-wiki-skill.git
mkdir -p ~/.codex/skills
ln -sfn "$PWD/llm-wiki-skill" ~/.codex/skills/llm-wiki
```

If you cloned without submodules:

```bash
git submodule update --init --recursive
```

## Structure

```text
.
├── SKILL.md
├── agents/
├── assets/
├── external/
│   └── llm_wiki/          # Git submodule: nashsu/llm_wiki
├── references/
└── scripts/
```

## External References

This skill is inspired by:

- [Andrej Karpathy's LLM Wiki gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
- [nashsu/llm_wiki](https://github.com/nashsu/llm_wiki), a GPL-3.0 desktop app
  implementation of the LLM Wiki idea

`external/llm_wiki` is a Git submodule pinned to the upstream
`nashsu/llm_wiki` repository. It is not relicensed by this repository.

## License

The original skill files in this repository are released under the MIT License.

Third-party references keep their own upstream licenses and attribution:

- `external/llm_wiki`: GPL-3.0, copyright and license belong to
  [nashsu/llm_wiki](https://github.com/nashsu/llm_wiki).
- `references/karpathy-llm-wiki-note.md`: an attributed learning note based on
  Andrej Karpathy's public LLM Wiki gist; it is included for reference and is
  not a copy of the upstream gist.
