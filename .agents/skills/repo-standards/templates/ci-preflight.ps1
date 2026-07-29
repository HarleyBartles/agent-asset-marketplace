# This script is repo-owned. The repo-standards skill only provides a starting
# scaffold. By default it regenerates the repo-wide INDEX.md mesh; pass --check
# to validate without writing.
#
# Available helpers from repo-standards:
#   . .agents/skills/repo-standards/scripts/repo-standards.ps1 --check
#   . .agents/skills/repo-standards/scripts/scaffold-all.ps1 --check
#   . .agents/skills/generating-agent-mesh/scripts/generate-index-mesh.ps1 --check
#   . .agents/skills/generating-agent-mesh/scripts/validate-agent-mesh.ps1 --check
#   . .agents/skills/refreshing-installed-skills/scripts/refresh-installed-skills.ps1 --check
#
# Add repo-specific lint here, for example:
#   ruff check <changed-python-files>
#
# Add repo-specific final CI checks here, for example:
#   py -3 tools/rebuild_marketplace.py --phase inventory --check
#   py -3 tools/rebuild_marketplace.py --phase project --check
#   py -3 tools/rebuild_marketplace.py --phase validate --check
#
# See repo-standards/references/ci-validation-pipeline.md for the full contract.
$ErrorActionPreference = 'Stop'

$repoRoot = (git rev-parse --show-toplevel)
$mode = "--apply"
$allow = "--allow-shared-checkout"
if ($args -contains "--check") {
    $mode = "--check"
    & "$repoRoot/.agents/skills/generating-agent-mesh/scripts/generate-index-mesh.ps1" $mode
} else {
    & "$repoRoot/.agents/skills/generating-agent-mesh/scripts/generate-index-mesh.ps1" $mode $allow
}
