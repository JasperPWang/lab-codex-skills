#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
VALIDATOR="${VALIDATOR:-$HOME/.codex/skills/.system/skill-creator/scripts/quick_validate.py}"

if [[ -f "$VALIDATOR" ]]; then
  tmp_log="$(mktemp)"
  if {
    count=0
    while IFS= read -r skill_md; do
      skill_dir="${skill_md%/SKILL.md}"
      python3 "$VALIDATOR" "$skill_dir" >/dev/null
      count=$((count + 1))
    done < <(find "$SKILL_ROOT" -mindepth 2 -maxdepth 2 -name SKILL.md -print | sort)
    echo "validated skills: $count"
  } 2>"$tmp_log"; then
    rm -f "$tmp_log"
    exit 0
  fi
  cat "$tmp_log" >&2
  rm -f "$tmp_log"
  echo "falling back to bundled standard-library validator" >&2
fi

python3 "$SCRIPT_DIR/simple-validate-skills.py" "$SKILL_ROOT"
