#!/usr/bin/env bash
# Copy the canonical root skill into the Agent Plugin payload.
#
# Source of truth: repository root (SKILL.md, agents/, references/,
# templates/, selected scripts/ and docs/). Do not edit
# plugins/opc-skills/skills/opc-skills/ by hand.
#
# Usage:
#   scripts/sync-plugin-skill.sh          # rewrite the plugin payload
#   scripts/sync-plugin-skill.sh --check  # fail if the payload drifted

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PLUGIN_ROOT="${ROOT}/plugins/opc-skills"
PAYLOAD="${PLUGIN_ROOT}/skills/opc-skills"
PLUGIN_JSON="${PLUGIN_ROOT}/plugin.json"
VERSION_FILE="${ROOT}/VERSION"

FILES=(
  SKILL.md
  VERSION
  LICENSE
)

DIRS=(
  agents
  references
  templates
)

DOC_FILES=(
  docs/subagent-optimization-plan.md
  docs/subagent-runtime-invocation-design.md
)

SCRIPT_FILES=(
  scripts/check_project_coupling.sh
  scripts/check_release_integrity.sh
  scripts/prepare_post_release_content.sh
  scripts/start_rnd.sh
)

die() {
  printf 'error: %s\n' "$*" >&2
  exit 1
}

read_version() {
  tr -d '[:space:]' < "$VERSION_FILE"
}

copy_payload() {
  local dest="$1"

  rm -rf "$dest"
  mkdir -p "$dest"

  local rel
  for rel in "${FILES[@]}"; do
    cp -a "${ROOT}/${rel}" "${dest}/${rel}"
  done

  for rel in "${DIRS[@]}"; do
    mkdir -p "${dest}/${rel}"
    cp -a "${ROOT}/${rel}/." "${dest}/${rel}/"
  done

  for rel in "${DOC_FILES[@]}" "${SCRIPT_FILES[@]}"; do
    mkdir -p "${dest}/$(dirname "$rel")"
    cp -a "${ROOT}/${rel}" "${dest}/${rel}"
  done
}

sync_plugin_version() {
  local version
  version="$(read_version)"
  [[ -n "$version" ]] || die "VERSION is empty"

  python3 - "$PLUGIN_JSON" "$version" <<'PY'
import json
import sys

path, version = sys.argv[1], sys.argv[2]
with open(path, encoding="utf-8") as fh:
    data = json.load(fh)
data["version"] = version
with open(path, "w", encoding="utf-8") as fh:
    json.dump(data, fh, indent=2, ensure_ascii=False)
    fh.write("\n")
PY
}

validate_manifests() {
  local version
  version="$(read_version)"

  python3 - "$PLUGIN_JSON" "${ROOT}/.agents/plugins/marketplace.json" "$version" "$PLUGIN_ROOT" "$PAYLOAD" <<'PY'
import json
import sys
from pathlib import Path

plugin_path, market_path, version, plugin_root, payload = sys.argv[1:]

plugin = json.loads(Path(plugin_path).read_text(encoding="utf-8"))
errors = []

if plugin.get("$schema") != "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json":
    errors.append("plugin.json $schema must be the Agent Plugins 1.0.0 schema")
if plugin.get("name") != "opc-skills":
    errors.append("plugin.json name must be opc-skills")
if plugin.get("version") != version:
    errors.append(f"plugin.json version {plugin.get('version')!r} != VERSION {version!r}")
if "mcpServers" in plugin:
    errors.append("skills-only plugin.json must not declare mcpServers")
if "apps" in plugin:
    errors.append("skills-only plugin.json must not declare apps")

iface = plugin.get("extensions", {}).get("com.openai", {}).get("interface", {})
for field in ("displayName", "shortDescription", "category", "developerName", "websiteURL"):
    if not iface.get(field):
        errors.append(f"extensions.com.openai.interface.{field} is required")
if iface.get("category") not in {"Productivity", "Developer Tools"}:
    errors.append("interface.category should be Productivity or Developer Tools")
if len(iface.get("displayName", "")) > 30:
    errors.append("interface.displayName exceeds 30 characters")
if len(iface.get("shortDescription", "")) > 30:
    errors.append("interface.shortDescription exceeds 30 characters")

if plugin.get("extensions", {}).get("com.openai", {}).get("apps"):
    errors.append("skills-only plugin must omit extensions.com.openai.apps")

skill_md = Path(payload) / "SKILL.md"
if not skill_md.is_file():
    errors.append(f"missing plugin skill payload: {skill_md}")

market = json.loads(Path(market_path).read_text(encoding="utf-8"))
if market.get("name") != "opc-skills":
    errors.append("marketplace.json name must be opc-skills")
plugins = market.get("plugins") or []
if len(plugins) != 1:
    errors.append("marketplace.json must list exactly one plugin")
else:
    entry = plugins[0]
    if entry.get("name") != "opc-skills":
        errors.append("marketplace plugin name must be opc-skills")
    source = entry.get("source") or {}
    if source.get("source") != "local" or source.get("path") != "./plugins/opc-skills":
        errors.append("marketplace source.path must be ./plugins/opc-skills")
    policy = entry.get("policy") or {}
    if policy.get("installation") != "AVAILABLE":
        errors.append("marketplace policy.installation must be AVAILABLE")
    if policy.get("authentication") != "ON_INSTALL":
        errors.append("marketplace policy.authentication must be ON_INSTALL")
    if not entry.get("category"):
        errors.append("marketplace category is required")

if not Path(plugin_root, "plugin.json").is_file():
    errors.append("plugin root is missing plugin.json")

if errors:
    print("plugin packaging check failed:", file=sys.stderr)
    for item in errors:
        print(f"  - {item}", file=sys.stderr)
    sys.exit(1)
PY
}

cmd="${1:-sync}"
case "$cmd" in
  sync|"")
    [[ -f "$PLUGIN_JSON" ]] || die "missing ${PLUGIN_JSON}"
    copy_payload "$PAYLOAD"
    sync_plugin_version
    validate_manifests
    printf 'synced plugin skill payload -> %s\n' "$PAYLOAD"
    ;;
  --check|check)
    [[ -d "$PAYLOAD" ]] || die "plugin payload missing; run scripts/sync-plugin-skill.sh"
    tmp="$(mktemp -d "${TMPDIR:-/tmp}/opc-plugin-skill.XXXXXX")"
    trap 'rm -rf "$tmp"' EXIT
    copy_payload "$tmp"
    if ! diff -rq "$tmp" "$PAYLOAD" >/dev/null; then
      printf 'error: plugins/opc-skills/skills/opc-skills drifted from the root skill.\n' >&2
      printf 'Run: scripts/sync-plugin-skill.sh\n' >&2
      diff -rq "$tmp" "$PAYLOAD" >&2 || true
      exit 1
    fi
    validate_manifests
    printf 'plugin skill payload is in sync with the repository root.\n'
    ;;
  help|-h|--help)
    cat <<EOF
Usage: scripts/sync-plugin-skill.sh [--check]

  (default)  Copy root skill files into plugins/opc-skills/skills/opc-skills
  --check    Fail if the plugin payload drifted from the root skill

Canonical skill files live at the repository root so curl / npx /
\$skill-installer keep cloning this repo into ~/.codex/skills/opc-skills.
The Agent Plugin host loads a copy under plugins/opc-skills/skills/opc-skills/.
EOF
    ;;
  *)
    die "unknown command: $cmd

Run scripts/sync-plugin-skill.sh --help"
    ;;
esac
