#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
bash "$SCRIPT_DIR/scripts/link-to-codex-skills.sh"
if [[ "$SCRIPT_DIR" == */.tools/skills ]]; then
  bash "$SCRIPT_DIR/scripts/link-to-cursor-skills.sh"
fi

