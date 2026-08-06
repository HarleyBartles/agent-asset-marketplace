#!/usr/bin/env bash
# This script is repo-owned. The repo-standards skill only provides a starting
# scaffold. The pre-commit hook runs it to apply mechanical fixes, stage the
# resulting tracked changes, then verify the tree is clean before the commit.
# Run `tools/run ci --apply` manually to apply the same fixes outside of a commit.
set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
if ! pushd "$REPO_ROOT" >/dev/null; then
  exit 1
fi
trap 'popd >/dev/null 2>&1' EXIT

if command -v py >/dev/null 2>&1; then
  run_python() { py -3 "$@"; }
elif command -v python3 >/dev/null 2>&1; then
  run_python() { python3 "$@"; }
elif command -v python >/dev/null 2>&1; then
  run_python() { python "$@"; }
else
  echo "py, python3, or python not found" >&2
  exit 1
fi

run_python "$REPO_ROOT/tools/run.py" ci --apply --allow-shared-checkout
git add -u
run_python "$REPO_ROOT/tools/run.py" ci --check
