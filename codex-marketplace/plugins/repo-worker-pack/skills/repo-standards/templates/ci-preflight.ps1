# This script is repo-owned. The repo-standards skill only provides a starting
# scaffold. The pre-commit hook runs the .sh version; this .ps1 can be used
# directly on Windows to apply mechanical fixes, stage the resulting tracked
# changes, then verify the tree is clean before the commit.
$ErrorActionPreference = 'Stop'

$repoRoot = (git rev-parse --show-toplevel)
Push-Location "$repoRoot"
try {
  py -3 tools/run.py ci --apply --allow-shared-checkout
  git add -u
  py -3 tools/run.py ci --check
} finally {
  Pop-Location
}
