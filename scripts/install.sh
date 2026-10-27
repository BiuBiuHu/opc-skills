#!/usr/bin/env bash
# Install or update opc-skills into the Codex skills path.
#
# Safe to pipe (default command is install):
#   curl -fsSL https://raw.githubusercontent.com/BiuBiuHu/opc-skills/main/scripts/install.sh | bash
#
# Subcommands (also used by the npm CLI):
#   install.sh install|update|doctor|path|help
#
# Always installs ~/.codex/skills/opc-skills.
# If ~/.cursor/skills or ~/.claude/skills already exists, also symlink there.
# Those extra parent dirs are never created from scratch, and no editor
# config or secrets are read.

set -euo pipefail

REPO_URL="https://github.com/BiuBiuHu/opc-skills.git"
REPO_SLUG="BiuBiuHu/opc-skills"
SKILL_NAME="opc-skills"
CODEX_PARENT="${HOME}/.codex/skills"
CODEX_TARGET="${CODEX_PARENT}/${SKILL_NAME}"
CURL_FALLBACK="curl -fsSL https://raw.githubusercontent.com/BiuBiuHu/opc-skills/main/scripts/install.sh | bash"

# Extra skill parents are used only when they already exist.
OPTIONAL_SKILL_PARENTS=(
  "${HOME}/.cursor/skills"
  "${HOME}/.claude/skills"
)

die() {
  printf 'error: %s\n' "$*" >&2
  exit 1
}

info() {
  printf '%s\n' "$*"
}

print_kv() {
  printf '  %-12s %s\n' "$1" "$2"
}

usage() {
  cat <<EOF
Usage: install.sh [install|update|doctor|path|help]

  install, update  Clone or fast-forward ~/.codex/skills/opc-skills
  doctor           Check install paths, git identity, VERSION, and symlinks
  path             Print the primary Codex install path
  help             Show this help

Always installs ${CODEX_TARGET}.
If ~/.cursor/skills or ~/.claude/skills already exists, also symlink there.
Those extra parent dirs are never created. git is required for install/update/doctor.

One-liner:
  ${CURL_FALLBACK}

npm CLI (same rules):
  npx opc-skills install
EOF
}

require_git() {
  if ! command -v git >/dev/null 2>&1; then
    printf '%s\n' \
      'error: git is required to install opc-skills, but it was not found in PATH.' \
      '' \
      'Install git, then re-run:' \
      "  ${CURL_FALLBACK}" \
      '  npx opc-skills install' \
      >&2
    exit 1
  fi
}

is_this_repo() {
  local dir="$1"
  local url
  url="$(git -C "$dir" remote get-url origin 2>/dev/null || true)"
  [[ "$url" == *"${REPO_SLUG}"* ]]
}

is_git_checkout() {
  local dir="$1"
  git -C "$dir" rev-parse --is-inside-work-tree >/dev/null 2>&1
}

origin_url() {
  git -C "$1" remote get-url origin 2>/dev/null || true
}

read_version() {
  local dir="$1"
  if [[ -f "${dir}/VERSION" ]]; then
    tr -d '[:space:]' < "${dir}/VERSION"
  else
    printf 'missing'
  fi
}

clone_fresh() {
  local dest="$1"
  info "Cloning ${REPO_SLUG} into ${dest}"
  GIT_TERMINAL_PROMPT=0 git clone --quiet "$REPO_URL" "$dest" </dev/null
}

update_checkout() {
  local dest="$1"
  if ! is_this_repo "$dest"; then
    die "${dest} is a git checkout, but origin is not ${REPO_SLUG}. Refusing to overwrite it."
  fi
  info "Updating ${dest} (git pull --ff-only)"
  GIT_TERMINAL_PROMPT=0 git -C "$dest" pull --ff-only --quiet </dev/null
}

install_or_update() {
  local dest="$1"

  mkdir -p "$(dirname "$dest")"

  if [[ -L "$dest" ]]; then
    local resolved
    resolved="$(readlink "$dest")"
    if [[ -d "$dest/.git" ]]; then
      update_checkout "$dest"
      return
    fi
    info "Replacing symlink ${dest} -> ${resolved} with a git checkout"
    rm "$dest"
    clone_fresh "$dest"
    return
  fi

  if [[ -d "$dest/.git" ]]; then
    update_checkout "$dest"
    return
  fi

  if [[ -e "$dest" ]]; then
    local bak="${dest}.bak.$(date +%Y%m%d%H%M%S)"
    info "${dest} exists but is not a git checkout. Moving it to ${bak}"
    mv "$dest" "$bak"
  fi

  clone_fresh "$dest"
}

link_optional_skill_dir() {
  local parent="$1"
  local dest="${parent}/${SKILL_NAME}"

  if [[ ! -d "$parent" ]]; then
    return 0
  fi

  if [[ -L "$dest" ]]; then
    local current
    current="$(readlink "$dest")"
    if [[ "$current" == "$CODEX_TARGET" ]]; then
      info "Already linked ${dest} -> ${CODEX_TARGET}"
      return 0
    fi
    info "Updating symlink ${dest} -> ${CODEX_TARGET}"
    rm "$dest"
    ln -s "$CODEX_TARGET" "$dest"
    return 0
  fi

  if [[ -d "$dest/.git" ]]; then
    update_checkout "$dest"
    return 0
  fi

  if [[ -e "$dest" ]]; then
    info "Skipping ${dest}: path exists and is not a symlink to the Codex install."
    return 0
  fi

  ln -s "$CODEX_TARGET" "$dest"
  info "Linked ${dest} -> ${CODEX_TARGET}"
}

cmd_install() {
  require_git

  info "Installing opc-skills"
  install_or_update "$CODEX_TARGET"

  if [[ ! -f "${CODEX_TARGET}/SKILL.md" ]]; then
    die "clone finished, but ${CODEX_TARGET}/SKILL.md is missing. Partial install aborted."
  fi

  for parent in "${OPTIONAL_SKILL_PARENTS[@]}"; do
    link_optional_skill_dir "$parent"
  done

  cat <<EOF

opc-skills is ready.

Install path: ${CODEX_TARGET}

In Codex (or Cursor / Claude, if those skill dirs already existed), say:

  启动 OPC Skills
  Start OPC Skills

EOF
}

cmd_path() {
  printf '%s\n' "$CODEX_TARGET"
}

cmd_doctor() {
  require_git

  local failed=0

  info "opc-skills doctor"
  info ""

  if ! check_primary; then
    failed=1
  fi
  info ""

  local parent
  for parent in "${OPTIONAL_SKILL_PARENTS[@]}"; do
    if ! check_optional "$parent"; then
      failed=1
    fi
    info ""
  done

  if [[ "$failed" -ne 0 ]]; then
    info "doctor: broken install"
    exit 1
  fi
  info "doctor: ok"
}

check_primary() {
  local broken=0

  info "Primary (Codex)"
  print_kv "path" "$CODEX_TARGET"

  if [[ -L "$CODEX_TARGET" ]]; then
    print_kv "symlink" "$(readlink "$CODEX_TARGET")"
    if [[ ! -e "$CODEX_TARGET" ]]; then
      print_kv "status" "broken symlink"
      return 1
    fi
  elif [[ ! -e "$CODEX_TARGET" ]]; then
    print_kv "status" "missing"
    return 1
  fi

  if [[ ! -d "$CODEX_TARGET" ]]; then
    print_kv "status" "not a directory"
    return 1
  fi

  if [[ -f "${CODEX_TARGET}/SKILL.md" ]]; then
    print_kv "SKILL.md" "yes"
  else
    print_kv "SKILL.md" "missing"
    broken=1
  fi

  local version
  version="$(read_version "$CODEX_TARGET")"
  print_kv "VERSION" "$version"
  if [[ "$version" == "missing" ]]; then
    broken=1
  fi

  if is_git_checkout "$CODEX_TARGET"; then
    local url
    url="$(origin_url "$CODEX_TARGET")"
    print_kv "git" "yes"
    print_kv "origin" "${url:-missing}"
    if is_this_repo "$CODEX_TARGET"; then
      print_kv "repo" "$REPO_SLUG"
    else
      print_kv "repo" "not ${REPO_SLUG}"
      broken=1
    fi
  else
    print_kv "git" "no"
    print_kv "repo" "not a git checkout of ${REPO_SLUG}"
    broken=1
  fi

  if [[ "$broken" -ne 0 ]]; then
    print_kv "status" "broken"
    return 1
  fi
  print_kv "status" "ok"
  return 0
}

check_optional() {
  local parent="$1"
  local dest="${parent}/${SKILL_NAME}"

  info "Optional (${dest})"

  if [[ ! -d "$parent" ]]; then
    print_kv "parent" "missing (not created; skipped)"
    print_kv "status" "n/a"
    return 0
  fi

  print_kv "parent" "exists"
  print_kv "path" "$dest"

  if [[ -L "$dest" ]]; then
    local current
    current="$(readlink "$dest")"
    print_kv "symlink" "$current"
    if [[ ! -e "$dest" ]]; then
      print_kv "healthy" "no (dangling)"
      print_kv "status" "broken"
      return 1
    fi
    if [[ "$current" == "$CODEX_TARGET" ]]; then
      print_kv "healthy" "yes"
      print_kv "VERSION" "$(read_version "$dest")"
      print_kv "status" "ok"
      return 0
    fi
    print_kv "healthy" "no (does not point at ${CODEX_TARGET})"
    print_kv "status" "broken"
    return 1
  fi

  if [[ ! -e "$dest" ]]; then
    print_kv "linked" "no"
    print_kv "status" "not linked"
    return 0
  fi

  if is_git_checkout "$dest"; then
    print_kv "git" "yes"
    print_kv "origin" "$(origin_url "$dest")"
    print_kv "VERSION" "$(read_version "$dest")"
    if is_this_repo "$dest"; then
      print_kv "repo" "$REPO_SLUG"
      print_kv "status" "ok (independent checkout)"
      return 0
    fi
    print_kv "repo" "not ${REPO_SLUG}"
    print_kv "status" "unmanaged"
    return 0
  fi

  print_kv "status" "unmanaged (exists, not a symlink to Codex)"
  return 0
}

if [[ $# -gt 1 ]]; then
  die "unexpected arguments: $*

$(usage)"
fi

cmd="${1:-install}"
case "$cmd" in
  install|update)
    cmd_install
    ;;
  doctor)
    cmd_doctor
    ;;
  path)
    cmd_path
    ;;
  help|-h|--help)
    usage
    ;;
  *)
    die "unknown command: ${cmd}

$(usage)"
    ;;
esac
