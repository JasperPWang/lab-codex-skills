# Lab Codex Skills

This directory is the canonical source for the lab Codex skill bundle. It keeps
user-maintained skills and vendored/downloaded skills together so the same
workflow can be shared across the user's Macs and cloned by lab teammates.

Rules:

- Put every editable skill under `.tools/skills/<skill-name>/`.
- Treat `~/.codex/skills/<skill-name>` as a compatibility symlink only.
- Treat `.agents/skills/<skill-name>` as a compatibility symlink only when a
  loader still expects that path.
- Do not edit copied skill directories in multiple places. Edit the canonical
  Vault path, then let the symlink expose it to Codex.
- Keep system, bundled, plugin-cache, and runtime skills outside this
  repository. Vendored or downloaded third-party skill suites may live here when
  their provenance is recorded.
- After changing a skill, run the relevant validation script if the skill has
  one, or run the system skill validator when applicable.

Before publishing or sharing, review:

- `SKILL_MANIFEST.md`
- `THIRD_PARTY_NOTICES.md`
- `.gitignore`

On a new Mac or a lab teammate's machine, run one of these:

```bash
# From this skill bundle directory after cloning it as a repository:
bash install.sh

# From the WorldModelVault root on this machine:
bash ".tools/skills/install.sh"
```

This recreates local compatibility symlinks under `~/.codex/skills` and
`.agents/skills` without copying skill content out of the iCloud-synced vault.

To validate all skills:

```bash
bash ".tools/skills/scripts/validate-all.sh"
```

To export a clean GitHub-ready copy without local archives or nested `.git`
metadata:

```bash
bash ".tools/skills/scripts/export-github-bundle.sh" /tmp/lab-codex-skills
```

Current compatibility aliases:

- `~/.codex/skills/feishu-cli` points to `.tools/skills/feishu-doc-workflow`
  for backward compatibility after the Feishu workflow skill rename.
- `~/.codex/skills/llm-wiki` points to `.tools/skills/llm-wiki-skill`.
- `~/.codex/skills/paper-to-slides` points to
  `.tools/skills/paper-to-slides-skill`.
