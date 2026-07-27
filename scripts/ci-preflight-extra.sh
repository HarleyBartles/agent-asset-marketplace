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
BASE_REF="${BASE%%...*}"

if ! git -C "$REPO_ROOT" rev-parse --verify --quiet "$BASE_REF" >/dev/null 2>&1; then
    echo "Base ref $BASE_REF not found; skipping Python lint." >&2
    exit 0
fi

mapfile -t files < <(git -C "$REPO_ROOT" diff --name-only --diff-filter=ACMR "$BASE" -- '*.py')
if [ ${#files[@]} -eq 0 ]; then
    echo "No changed Python files to lint."
    exit 0
fi

cd "$REPO_ROOT"
ruff check "${files[@]}"
