#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
CODEX_SKILL_ROOT="${CODEX_SKILL_ROOT:-$HOME/.codex/skills}"
STAMP="$(date +%Y%m%d-%H%M%S)"

mkdir -p "$CODEX_SKILL_ROOT"

link_skill() {
  local name="$1"
  local target="$2"
  local link="$3"
  local archive_root="$4"

  if [[ ! -d "$target" || ! -f "$target/SKILL.md" ]]; then
    echo "skip missing skill: $name" >&2
    return 0
  fi

  if [[ -L "$link" ]]; then
    rm "$link"
  elif [[ -e "$link" ]]; then
    mkdir -p "$archive_root/.archive-before-vault-link-$STAMP"
    mv "$link" "$archive_root/.archive-before-vault-link-$STAMP/$name"
  fi

  ln -s "$target" "$link"
  echo "linked $name"
}

while IFS= read -r skill_md; do
  skill_dir="${skill_md%/SKILL.md}"
  name="${skill_dir##*/}"
  link_skill "$name" "$skill_dir" "$CODEX_SKILL_ROOT/$name" "$CODEX_SKILL_ROOT"
done < <(find "$SKILL_ROOT" -mindepth 2 -maxdepth 2 -name SKILL.md -print | sort)

# Backward-compatible aliases for renamed skills.
link_skill "feishu-cli" "$SKILL_ROOT/feishu-doc-workflow" "$CODEX_SKILL_ROOT/feishu-cli" "$CODEX_SKILL_ROOT"
link_skill "llm-wiki" "$SKILL_ROOT/llm-wiki-skill" "$CODEX_SKILL_ROOT/llm-wiki" "$CODEX_SKILL_ROOT"
link_skill "paper-to-slides" "$SKILL_ROOT/paper-to-slides-skill" "$CODEX_SKILL_ROOT/paper-to-slides" "$CODEX_SKILL_ROOT"

# Compatibility path for loaders that still discover agent-local skills. Only
# auto-create the Vault-local .agents path when this bundle is running from the
# WorldModelVault .tools/skills layout. In a standalone GitHub clone, set
# AGENT_SKILL_ROOT explicitly if this compatibility path is needed.
if [[ -n "${AGENT_SKILL_ROOT:-}" ]]; then
  mkdir -p "$AGENT_SKILL_ROOT"
  link_skill "lark-whiteboard" "$SKILL_ROOT/lark-whiteboard" "$AGENT_SKILL_ROOT/lark-whiteboard" "$AGENT_SKILL_ROOT"
elif [[ "$SKILL_ROOT" == */.tools/skills ]]; then
  VAULT_ROOT="$(cd "$SKILL_ROOT/../.." && pwd)"
  AGENT_SKILL_ROOT="$VAULT_ROOT/.agents/skills"
  mkdir -p "$AGENT_SKILL_ROOT"
  link_skill "lark-whiteboard" "$SKILL_ROOT/lark-whiteboard" "$AGENT_SKILL_ROOT/lark-whiteboard" "$AGENT_SKILL_ROOT"
fi

echo "done"
