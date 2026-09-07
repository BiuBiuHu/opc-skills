#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "Usage: $0 <project-root> <feature-name> <base-commit> <head-commit> [output-dir]" >&2
  echo "Prepare a local source manifest for optional post-release article production." >&2
  exit 2
}

[[ $# -ge 4 && $# -le 5 ]] || usage

ROOT="$1"
FEATURE_NAME="$2"
BASE_COMMIT="$3"
HEAD_COMMIT="$4"
OUTPUT_DIR="${5:-$ROOT/docs/$FEATURE_NAME/07-content}"

[[ "$FEATURE_NAME" =~ ^[A-Za-z0-9][A-Za-z0-9._-]*$ ]] || {
  echo "FAIL: feature-name must be a simple kebab-case path segment: $FEATURE_NAME" >&2
  exit 1
}

git_root="$(git -C "$ROOT" rev-parse --show-toplevel 2>/dev/null)" || {
  echo "FAIL: not a git repository: $ROOT" >&2
  exit 1
}

base_sha="$(git -C "$git_root" rev-parse --verify "$BASE_COMMIT^{commit}" 2>/dev/null)" || {
  echo "FAIL: base commit does not resolve: $BASE_COMMIT" >&2
  exit 1
}

head_sha="$(git -C "$git_root" rev-parse --verify "$HEAD_COMMIT^{commit}" 2>/dev/null)" || {
  echo "FAIL: head commit does not resolve: $HEAD_COMMIT" >&2
  exit 1
}

mkdir -p "$OUTPUT_DIR"
target="$OUTPUT_DIR/release-source-manifest.md"
generated_at="$(date '+%Y-%m-%d %H:%M:%S %z')"

{
  printf '%s\n\n' "# 发布后文章素材清单"
  printf '%s\n\n' "> 此文件由 scripts/prepare_post_release_content.sh 生成。发布文章前必须人工检查敏感信息和事实准确性。"
  printf '%s\n\n' "## 基本信息"
  printf '%s\n' "- 生成时间：$generated_at"
  printf '%s\n' "- 项目根目录：\`<PROJECT_ROOT>\`"
  printf '%s\n' "- Feature：$FEATURE_NAME"
  printf '%s\n' "- Base commit：\`$base_sha\`"
  printf '%s\n\n' "- Head commit：\`$head_sha\`"
  printf '%s\n\n' "## 提交记录"
  git -C "$git_root" log --no-merges --date=short --format='- %h %ad %s' "$base_sha..$head_sha" || true
  printf '\n%s\n\n' "## 变更统计"
  git -C "$git_root" diff --stat "$base_sha...$head_sha" || true
  printf '\n%s\n\n' "## 变更文件"
  git -C "$git_root" diff --name-status "$base_sha...$head_sha" || true
  printf '\n%s\n\n' "## 写作前检查"
  printf '%s\n' "- [ ] 已读取 PRD、变更影响、测试报告、联调报告、发布方案和 evidence manifest"
  printf '%s\n' "- [ ] 数字、版本、时间线和根因均已回到 Git/代码/证据核实"
  printf '%s\n' "- [ ] 已移除账号、token、secret、内部域名、deployment、数据库 host/schema 和客户数据"
  printf '%s\n' "- [ ] 已区分预发、生产、smoke、线上回归和观察窗口结论"
  printf '%s\n' "- [ ] 已确定文章输出目录、语言版本、slug、frontmatter 和配图计划"
} > "$target"

echo "Post-release content source manifest created: $target"
