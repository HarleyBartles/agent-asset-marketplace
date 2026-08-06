#!/usr/bin/env bash
# This script is repo-owned. The repo-standards skill only provides a starting
# scaffold. The pre-commit hook runs it to apply mechanical fixes and stage the
# resulting changes in the same commit. Run `tools/run ci --apply` manually to
# apply the same fixes outside of a commit.
set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
cd "$REPO_ROOT"

"$REPO_ROOT/tools/run" ci --apply --allow-shared-checkout
git add -A
