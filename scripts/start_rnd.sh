#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-.}"
FEATURE_NAME="${2:-}"

if [ -z "$FEATURE_NAME" ]; then
  echo "Usage: $0 <project-root> <feature-name>"
  echo "Example: $0 example-monitoring-platform evidence-review-workflow"
  exit 1
fi

DOCS="$ROOT/docs/$FEATURE_NAME"

mkdir -p \
  "$DOCS/01-product" \
  "$DOCS/02-ui" \
  "$DOCS/03-architecture" \
  "$DOCS/04-engineering" \
  "$DOCS/05-testing" \
  "$DOCS/06-ops"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TEMPLATES_DIR="$(cd "$SCRIPT_DIR/../templates" && pwd)"

seed_from_template() {
  local target="$1"
  local template="$2"
  if [ ! -s "$target" ]; then
    cp "$template" "$target"
  fi
}

seed_from_template "$DOCS/01-product/PRD.md" "$TEMPLATES_DIR/prd-template.md"
seed_from_template "$DOCS/02-ui/markdown-prototype.md" "$TEMPLATES_DIR/ui-prototype-template.md"
seed_from_template "$DOCS/03-architecture/architecture.md" "$TEMPLATES_DIR/architecture-template.md"
seed_from_template "$DOCS/04-engineering/implementation-plan.md" "$TEMPLATES_DIR/implementation-plan-template.md"
seed_from_template "$DOCS/04-engineering/backlog.md" "$TEMPLATES_DIR/backlog-template.md"
seed_from_template "$DOCS/05-testing/test-strategy.md" "$TEMPLATES_DIR/test-strategy-template.md"
seed_from_template "$DOCS/06-ops/ops-runbook.md" "$TEMPLATES_DIR/ops-runbook-template.md"

echo "OPC Skills 工作区已初始化：$DOCS"
