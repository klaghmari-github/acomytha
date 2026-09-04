#!/usr/bin/env bash
# Add tout, commit, push la branche courante vers GitLab et GitHub.
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

if git remote get-url origin >/dev/null 2>&1; then
  git remote set-url origin "$GITLAB_URL"
else
  git remote add origin "$GITLAB_URL"
fi
if git remote get-url github >/dev/null 2>&1; then
  git remote set-url github "$GITHUB_URL"
else
  git remote add github "$GITHUB_URL"
fi

BRANCH="$(git branch --show-current)"
if [[ -z "$BRANCH" ]]; then
  echo "Pas de branche courante (HEAD détaché)." >&2
  exit 1
fi

git add -A

if git diff --cached --quiet; then
  echo "Rien à committer."
else
  git commit -m "$MSG"
fi

echo "→ GitLab ($BRANCH)"
git push -u origin "$BRANCH"
echo "→ GitHub ($BRANCH)"
git push github "$BRANCH"
echo "OK GitLab + GitHub"
