#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

if ! command -v ruff &> /dev/null; then
    echo "ruff not found; skipping Python lint (install with: pip install ruff==0.9.0)"
    exit 0
fi

CHANGED_FROM=""
while [ $# -gt 0 ]; do
    case "$1" in
        --check) ;;
        --changed-from)
            shift
            CHANGED_FROM="$1"
            ;;
        *) echo "unknown arg: $1" >&2; exit 1 ;;
    esac
    shift
done

BASE="${CHANGED_FROM:-origin/main...HEAD}"
mapfile -t files < <(git -C "$REPO_ROOT" diff --name-only "$BASE" -- '*.py' || true)
if [ ${#files[@]} -eq 0 ]; then
    echo "No changed Python files to lint."
    exit 0
fi

cd "$REPO_ROOT"
ruff check "${files[@]}"
