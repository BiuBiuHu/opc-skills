#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "Usage: $0 <repo-root> <candidate-commit> [default-branch] [deployment-commit] [remote]" >&2
  echo "Checks production candidate ancestry, deployment mapping, and default-branch worktrees." >&2
  exit 2
}

[[ $# -ge 2 && $# -le 5 ]] || usage

ROOT="$1"
CANDIDATE="$2"
DEFAULT_BRANCH="${3:-}"
DEPLOYMENT_COMMIT="${4:-$CANDIDATE}"
REMOTE="${5:-origin}"

git_root="$(git -C "$ROOT" rev-parse --show-toplevel 2>/dev/null)" || {
  echo "FAIL: not a git repository: $ROOT" >&2
  exit 1
}

if [[ -z "$DEFAULT_BRANCH" ]]; then
  default_ref="$(git -C "$git_root" symbolic-ref --quiet --short "refs/remotes/$REMOTE/HEAD" 2>/dev/null || true)"
  DEFAULT_BRANCH="${default_ref#"$REMOTE/"}"
fi

[[ -n "$DEFAULT_BRANCH" ]] || {
  echo "FAIL: cannot determine default branch; pass it explicitly" >&2
  exit 1
}

remote_ref="$REMOTE/$DEFAULT_BRANCH"
remote_sha="$(git -C "$git_root" rev-parse --verify "$remote_ref" 2>/dev/null)" || {
  echo "FAIL: missing local remote-tracking ref: $remote_ref (fetch or update the project facts first)" >&2
  exit 1
}

candidate_sha="$(git -C "$git_root" rev-parse --verify "$CANDIDATE^{commit}" 2>/dev/null)" || {
  echo "FAIL: candidate commit does not resolve: $CANDIDATE" >&2
  exit 1
}

deployment_sha="$(git -C "$git_root" rev-parse --verify "$DEPLOYMENT_COMMIT^{commit}" 2>/dev/null)" || {
  echo "FAIL: deployment commit does not resolve: $DEPLOYMENT_COMMIT" >&2
  exit 1
}

if [[ "$candidate_sha" != "$deployment_sha" ]]; then
  echo "FAIL: deployment commit $deployment_sha does not match candidate $candidate_sha" >&2
  exit 1
fi

if ! git -C "$git_root" merge-base --is-ancestor "$candidate_sha" "$remote_sha"; then
  echo "FAIL: candidate $candidate_sha is not contained in $remote_ref ($remote_sha)" >&2
  exit 1
fi

if [[ -n "$(git -C "$git_root" status --porcelain)" ]]; then
  echo "FAIL: primary worktree is dirty; preserve changes before release reconciliation" >&2
  exit 1
fi

echo "PASS: repository=$git_root"
echo "PASS: default_branch=$DEFAULT_BRANCH remote_head=$remote_sha"
echo "PASS: candidate_commit=$candidate_sha deployment_commit=$deployment_sha"
echo "WORKTREES:"

failed=0
worktree_path=""
worktree_head=""
worktree_branch=""

check_worktree() {
  [[ -n "$worktree_path" ]] || return 0
  local state="clean"
  [[ -n "$(git -C "$worktree_path" status --porcelain 2>/dev/null || true)" ]] && state="dirty"
  local label="${worktree_branch:-detached}"
  if [[ "$state" != "clean" ]]; then
    echo "FAIL: worktree path=$worktree_path branch=$label head=$worktree_head state=$state; preserve changes before synchronization" >&2
    failed=1
    return 0
  fi
  if [[ "$worktree_branch" == "$DEFAULT_BRANCH" ]]; then
    if [[ "$worktree_head" != "$remote_sha" ]]; then
      echo "FAIL: default-branch worktree path=$worktree_path branch=$label head=$worktree_head state=$state expected_head=$remote_sha" >&2
      failed=1
    else
      echo "PASS: default-branch worktree path=$worktree_path branch=$label head=$worktree_head state=$state"
    fi
  else
    if ! git -C "$git_root" merge-base --is-ancestor "$candidate_sha" "$worktree_head" 2>/dev/null; then
      echo "FAIL: worktree path=$worktree_path branch=$label head=$worktree_head does not contain candidate $candidate_sha; sync before next development" >&2
      failed=1
    else
      echo "PASS: non-default worktree path=$worktree_path branch=$label head=$worktree_head contains_candidate=yes state=$state"
    fi
  fi
}

while IFS= read -r line || [[ -n "$line" ]]; do
  case "$line" in
    "worktree "*) check_worktree; worktree_path="${line#worktree }"; worktree_head=""; worktree_branch="" ;;
    "HEAD "*) worktree_head="${line#HEAD }" ;;
    "branch refs/heads/"*) worktree_branch="${line#branch refs/heads/}" ;;
    "") check_worktree; worktree_path=""; worktree_head=""; worktree_branch="" ;;
  esac
done < <(git -C "$git_root" worktree list --porcelain)
check_worktree

if [[ "$failed" -ne 0 ]]; then
  exit 1
fi

echo "PASS: release integrity checks completed."
