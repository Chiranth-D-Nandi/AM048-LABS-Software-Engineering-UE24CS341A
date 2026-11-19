#!/usr/bin/env bash
# Replays the four Lab 4 task changes as four separate commits.
# Run from the ROOT of your cloned/forked repo (the folder containing main.py),
# on a clean working tree:   bash /path/to/apply_patches.sh
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

[ -f main.py ] && [ -d game ] || { echo "Run this from the root of the platformer repo."; exit 1; }
[ -z "$(git status --porcelain --untracked-files=no)" ] || { echo "Working tree not clean - commit or stash first."; exit 1; }

for p in "$HERE"/patches/*.patch; do
  msg="$(git mailinfo /dev/null /dev/null < "$p" | sed -n 's/^Subject: //p' | head -1)"
  git apply --index "$p"
  git commit -q -m "$msg"  
  echo "committed: $msg"
done
echo "Done. Review with: git log --oneline"
