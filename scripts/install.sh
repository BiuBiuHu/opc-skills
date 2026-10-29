#!/usr/bin/env bash
# Shared entry for curl and the npm CLI. No editor settings or credentials are read.
set -euo pipefail
command -v git >/dev/null 2>&1 || { echo 'error: git is required.' >&2; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo 'error: Python 3.9+ is required.' >&2; exit 1; }
if [[ -n "${BASH_SOURCE[0]:-}" && -f "${BASH_SOURCE[0]}" ]]; then
  SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  if [[ -f "${SCRIPT_DIR}/sync-local-skills.py" ]]; then
    exec python3 "${SCRIPT_DIR}/sync-local-skills.py" "$@"
  fi
fi
# curl|bash has no adjacent helper. Bootstrap only into a task-owned temporary checkout.
bootstrap_dir="$(mktemp -d "${TMPDIR:-/tmp}/opc-bootstrap.XXXXXX")"
trap 'rm -rf "$bootstrap_dir"' EXIT
git clone --quiet --depth 1 https://github.com/BiuBiuHu/opc-skills.git "$bootstrap_dir/source"
python3 "$bootstrap_dir/source/scripts/sync-local-skills.py" "$@"
