#!/usr/bin/env bash
# `agent-asset-marketplace` preflight script.
# This is a repo-owned mirror of the CI pipeline in
# `.github/workflows/marketplace-validation.yml`. It is read-only and prints
# the repair command for any failing check.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

PYTHON=""
for bin in python python3; do
    if command -v "$bin" >/dev/null 2>&1; then
        PYTHON="$bin"
        break
    fi
done
if [ -z "$PYTHON" ]; then
    echo "No Python interpreter found" >&2
    exit 1
fi

CHANGED_FROM=""
while [ $# -gt 0 ]; do
    case "$1" in
        --check) ;;  # accepted for compatibility; preflight is always read-only
        --changed-from)
            shift
            CHANGED_FROM="$1"
            ;;
        *) echo "unknown arg: $1" >&2; exit 1 ;;
    esac
    shift
done

# Determine the base ref for changed-line linting.
BASE_REF=""
if [ -n "$CHANGED_FROM" ]; then
    if git rev-parse --verify "$CHANGED_FROM" >/dev/null 2>&1; then
        BASE_REF="$CHANGED_FROM"
    else
        echo "warning: $CHANGED_FROM not found, no diff available to lint" >&2
    fi
elif git rev-parse --verify origin/main >/dev/null 2>&1; then
    BASE_REF="origin/main"
else
    echo "warning: origin/main not found, no diff available to lint" >&2
fi

echo "==> Lint changed Python files"
if ! "$PYTHON" tools/ruff_diff.py --changed-from "$BASE_REF"; then
    echo "Fix lint: $PYTHON -m ruff check --fix <changed-files> && $PYTHON -m ruff format <changed-files>" >&2
    exit 1
fi

echo "==> Repo standards"
if ! bash .agents/skills/repo-standards/scripts/repo-standards.sh --check; then
    echo "Fix repo standards: $PYTHON .agents/skills/repo-standards/scripts/repo_standards.py --apply --yes" >&2
    exit 1
fi

echo "==> Validate agent mesh"
if ! bash .agents/skills/generating-agent-mesh/scripts/validate-agent-mesh.sh --check; then
    echo "Fix agent mesh: $PYTHON .agents/skills/generating-agent-mesh/scripts/generate_index_mesh.py" >&2
    exit 1
fi

for phase in inventory heal project index catalog validate; do
    echo "==> Marketplace $phase"
    if ! "$PYTHON" tools/rebuild_marketplace.py --phase "$phase" --check; then
        echo "Fix marketplace: $PYTHON tools/rebuild_marketplace.py" >&2
        exit 1
    fi
done

echo "All preflight checks passed."
