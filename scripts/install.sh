#!/usr/bin/env bash
# Install or update opc-skills into the Codex skills path.
#
# Safe to pipe:
#   curl -fsSL https://raw.githubusercontent.com/BiuBiuHu/opc-skills/main/scripts/install.sh | bash
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

require_git() {
  if ! command -v git >/dev/null 2>&1; then
    printf '%s\n' \
      'error: git is required to install opc-skills, but it was not found in PATH.' \
      '' \
      'Install git, then re-run:' \
      '  curl -fsSL https://raw.githubusercontent.com/BiuBiuHu/opc-skills/main/scripts/install.sh | bash' \
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
