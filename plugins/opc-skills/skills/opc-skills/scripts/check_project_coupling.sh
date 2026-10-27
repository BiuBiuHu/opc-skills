#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-$(cd "$(dirname "$0")/.." && pwd)}"
FAILED=0

scan() {
  local label="$1"
  local pattern="$2"
  local output
  local status

  set +e
  output="$(rg -n -i --hidden --glob '!.git/**' --glob '!LICENSE' --glob '!scripts/check_project_coupling.sh' "$pattern" "$ROOT")"
  status=$?
  set -e

  if [ "$status" -gt 1 ]; then
    printf 'Project coupling check could not run: %s\n' "$label" >&2
    FAILED=1
  elif [ "$status" -eq 0 ]; then
    printf 'Project coupling check failed: %s\n%s\n' "$label" "$output" >&2
    FAILED=1
  fi
}

scan "real email address" '[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}'
scan "user-specific absolute path" '/(Users|home)/[^/[:space:]]+/'
scan "deployment identifier" 'dpl_[A-Z0-9]+'
scan "database connection URL" '(postgres|postgresql|mysql|mongodb|redis)://[^[:space:]`]+'
scan "generated cloud deployment URL" 'https?://[^[:space:]`]+\.(vercel\.app|netlify\.app|run\.app)([/[:space:]`]|$)'

if [ -n "${OPC_PROJECT_TERMS:-}" ]; then
  scan "configured project-specific term" "$OPC_PROJECT_TERMS"
fi

if [ "$FAILED" -ne 0 ]; then
  exit 1
fi

echo "Project coupling check passed."
