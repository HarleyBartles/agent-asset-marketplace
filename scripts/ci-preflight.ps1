# This script is repo-owned. The repo-standards skill only provides a starting
# scaffold. The pre-commit hook runs the .sh version; this .ps1 can be used
# directly on Windows to apply mechanical fixes and stage the resulting changes.
$ErrorActionPreference = 'Stop'

$repoRoot = (git rev-parse --show-toplevel)
Set-Location "$repoRoot"

py -3 tools/run.py ci --apply --allow-shared-checkout
git add -A
