#!/usr/bin/env bash
# This script is repo-owned. The repo-standards skill only provides a starting
# scaffold. By default it regenerates the repo-wide INDEX.md mesh; pass --check
# to validate without writing.
#
# Available helpers from repo-standards:
#   bash .agents/skills/repo-standards/scripts/repo-standards.sh --check
#   bash .agents/skills/repo-standards/scripts/scaffold-all.sh --check
#   bash .agents/skills/generating-agent-mesh/scripts/generate-index-mesh.sh --check
#   bash .agents/skills/generating-agent-mesh/scripts/validate-agent-mesh.sh --check
#   bash .agents/skills/refreshing-installed-skills/scripts/refresh-installed-skills.sh --check
#
# Add repo-specific lint here, for example:
#   python -m ruff check <changed-python-files>
#
# Add repo-specific final CI checks here, for example:
#   python tools/rebuild_marketplace.py --phase inventory --check
#   python tools/rebuild_marketplace.py --phase project --check
#   python tools/rebuild_marketplace.py --phase validate --check
#
# See repo-standards/references/ci-validation-pipeline.md for the full contract.
set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
MODE="--apply"
ALLOW="--allow-shared-checkout"
if [ "${1:-}" = "--check" ]; then
    MODE="--check"
    ALLOW=""
fi

exec bash "$REPO_ROOT/.agents/skills/generating-agent-mesh/scripts/generate-index-mesh.sh" "$MODE" $ALLOW
