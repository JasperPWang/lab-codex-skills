#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

if [[ "$SKILL_ROOT" == */.tools/skills ]]; then
  VAULT_ROOT="$(cd "$SKILL_ROOT/../.." && pwd)"
  AGENT_SKILL_ROOT="${AGENT_SKILL_ROOT:-$VAULT_ROOT/.agents/skills}"
else
  AGENT_SKILL_ROOT="${AGENT_SKILL_ROOT:-$SKILL_ROOT/.agents/skills}"
fi

STAMP="$(date +%Y%m%d-%H%M%S)"

mkdir -p "$AGENT_SKILL_ROOT"

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
    mkdir -p "$archive_root/.archive-before-agent-link-$STAMP"
    mv "$link" "$archive_root/.archive-before-agent-link-$STAMP/$name"
  fi

  ln -sfn "$target" "$link"
  echo "linked antigravity skill: $name"
}

while IFS= read -r skill_md; do
  skill_dir="${skill_md%/SKILL.md}"
  name="${skill_dir##*/}"
  link_skill "$name" "$skill_dir" "$AGENT_SKILL_ROOT/$name" "$AGENT_SKILL_ROOT"
done < <(find "$SKILL_ROOT" -mindepth 2 -maxdepth 2 -name SKILL.md -print | sort)

# Compatibility aliases
link_skill "feishu-cli" "$SKILL_ROOT/feishu-doc-workflow" "$AGENT_SKILL_ROOT/feishu-cli" "$AGENT_SKILL_ROOT"
link_skill "llm-wiki" "$SKILL_ROOT/llm-wiki-skill" "$AGENT_SKILL_ROOT/llm-wiki" "$AGENT_SKILL_ROOT"
link_skill "paper-to-slides" "$SKILL_ROOT/paper-to-slides-skill" "$AGENT_SKILL_ROOT/paper-to-slides" "$AGENT_SKILL_ROOT"

echo "Antigravity skills linked under: $AGENT_SKILL_ROOT"
