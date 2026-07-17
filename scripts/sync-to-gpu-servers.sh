#!/usr/bin/env bash
# Sync lab-codex-skills to GPU SSH hosts (3090 / 4090 / A800 / A6000).
# Prefer git pull on hosts that can reach GitHub; fall back to rsync from this machine for 3090.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

HOSTS=("$@")
if [[ ${#HOSTS[@]} -eq 0 ]]; then
  HOSTS=(3090 4090 A800 A6000)
fi

SSH=(ssh -o BatchMode=yes -o ConnectTimeout=15)
RSYNC_SSH="ssh -o BatchMode=yes -o ConnectTimeout=15"

can_reach_github() {
  local host="$1"
  "${SSH[@]}" "$host" 'curl -sI -m 8 https://github.com >/dev/null 2>&1'
}

sync_via_git() {
  local host="$1"
  echo "========== $host (git pull) =========="
  "${SSH[@]}" "$host" 'bash -s' <<'REMOTE'
set -euo pipefail
cd "$HOME/lab-codex-skills"
if [ -n "$(git status --porcelain 2>/dev/null || true)" ]; then
  git stash push -u -m "auto-stash before skill sync $(date +%Y%m%d-%H%M%S)" || true
fi
git fetch origin
git checkout main
git pull --ff-only origin main
echo "HEAD=$(git rev-parse --short HEAD)"
bash install.sh
REMOTE
}

sync_via_rsync() {
  local host="$1"
  local export_dir
  export_dir="$(mktemp -d /tmp/lab-codex-skills-rsync-XXXXXX)"
  echo "========== $host (rsync fallback) =========="
  bash "$SKILL_ROOT/scripts/export-github-bundle.sh" "$export_dir"
  rsync -az --delete --exclude='.git/' --exclude='.DS_Store' \
    -e "$RSYNC_SSH" \
    "$export_dir/" "$host:lab-codex-skills/"
  rm -rf "$export_dir"
  "${SSH[@]}" "$host" 'bash -s' <<'REMOTE'
set -euo pipefail
cd "$HOME/lab-codex-skills"
bash install.sh
for s in notion-doc-workflow obsidian-doc-workflow research-doc-workflow; do
  test -e "$HOME/.codex/skills/$s" && echo "OK $s" || echo "MISSING $s"
done
REMOTE
}

for host in "${HOSTS[@]}"; do
  if can_reach_github "$host"; then
    sync_via_git "$host"
  else
    echo "WARN: $host cannot reach GitHub; using rsync from this machine"
    sync_via_rsync "$host"
  fi
  echo
done

echo "GPU skill sync complete."
