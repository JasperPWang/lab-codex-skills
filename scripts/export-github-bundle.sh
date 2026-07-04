#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <output-directory>" >&2
  exit 1
fi

OUT_DIR="$1"
mkdir -p "$OUT_DIR"

if ! command -v rsync >/dev/null 2>&1; then
  echo "rsync is required" >&2
  exit 1
fi

rsync -a --delete \
  --exclude='.git/' \
  --exclude='.DS_Store' \
  --exclude='__pycache__/' \
  --exclude='*.pyc' \
  --exclude='.pytest_cache/' \
  --exclude='.mypy_cache/' \
  --exclude='.ruff_cache/' \
  --exclude='.venv/' \
  --exclude='venv/' \
  --exclude='node_modules/' \
  --exclude='.machine-local-archives/' \
  --exclude='.archive-before-consolidation-*/' \
  --exclude='.archive-before-vault-consolidation-*/' \
  --exclude='.archive-before-vault-link-*/' \
  "$SKILL_ROOT/" "$OUT_DIR/"

python3 "$SCRIPT_DIR/sanitize-public-export.py" "$OUT_DIR"

echo "exported clean bundle to: $OUT_DIR"
echo "next: cd \"$OUT_DIR\" && git init && git add ."
