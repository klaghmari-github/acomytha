#!/usr/bin/env bash
# Un dossier local → GitLab (origin) + GitHub (github).
# Usage :
#   ./gitpush.sh
#   ./gitpush.sh -m "feat(F-XXX): …"
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

MSG="checkpoint"
if [[ "${1:-}" == "-m" ]]; then
  if [[ -z "${2:-}" ]]; then
    echo "usage: $0 [-m \"message\"]" >&2
    exit 1
  fi
  MSG="$2"
elif [[ $# -gt 0 ]]; then
  echo "usage: $0 [-m \"message\"]" >&2
  exit 1
fi

GITLAB_URL="git@gitlab.com:klaghmari-group/akomytha.git"
GITHUB_URL="git@github.com:klaghmari-github/acomytha.git"

ensure_remote() {
  local name="$1" url="$2"
  if git remote get-url "$name" >/dev/null 2>&1; then
    git remote set-url "$name" "$url"
  else
    git remote add "$name" "$url"
  fi
}

ensure_remote origin "$GITLAB_URL"
ensure_remote github "$GITHUB_URL"

if [[ "$(git branch --show-current)" != "main" ]]; then
  echo "→ checkout main"
  git checkout main
fi

echo "→ fetch GitLab + GitHub"
git fetch origin
git fetch github || true

tip() {
  git rev-parse -q --verify "$1" 2>/dev/null || true
}

ff_to() {
  local ref="$1"
  [[ -z "$ref" ]] && return 0
  git rev-parse -q --verify "$ref" >/dev/null 2>&1 || return 0
  if git merge-base --is-ancestor HEAD "$ref"; then
    if [[ "$(git rev-parse HEAD)" != "$(git rev-parse "$ref")" ]]; then
      echo "→ fast-forward vers $ref"
      git merge --ff-only "$ref"
    fi
  elif git merge-base --is-ancestor "$ref" HEAD; then
    :
  else
    echo "→ $ref a divergé, fusion dans main"
    git merge --no-edit "$ref"
  fi
}

ff_to origin/main
ff_to github/main

git add -A
if git diff --cached --quiet; then
  echo "Rien à committer."
else
  git commit -m "$MSG"
fi

echo "→ push GitLab"
git push -u origin main
echo "→ push GitHub"
git push github main

echo "OK  local = GitLab = GitHub  $(git rev-parse --short HEAD)"
