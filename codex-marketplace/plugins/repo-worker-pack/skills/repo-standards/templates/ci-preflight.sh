#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

find_skill_script() {
    local skill="$1" core="$2"
    local installed="$REPO_ROOT/.agents/skills/$skill/scripts/$core.sh"
    if [ -f "$installed" ]; then echo "$installed"; return; fi

    local mp_source="$REPO_ROOT/.agents/plugins/marketplace-source/codex-marketplace/plugins"
    if [ -d "$mp_source" ]; then
        local found
        found=$(find "$mp_source" -path "*/skills/$skill/scripts/$core.sh" -maxdepth 4 -print -quit 2>/dev/null)
        if [ -n "$found" ]; then echo "$found"; return; fi
    fi
    echo "$skill $core wrapper not found" >&2; exit 1
}

CHECK=""
FULL=""
while [ $# -gt 0 ]; do
    case "$1" in
        --check) CHECK="--check" ;;
        --full) FULL="1" ;;
        *) echo "unknown arg: $1" >&2; exit 1 ;;
    esac
    shift
done

MESH=$(find_skill_script generating-index-mesh generate-index-mesh)
REFRESH=$(find_skill_script refreshing-installed-skills refresh-installed-skills)

MESH_ARGS=()
[ -n "$CHECK" ] && MESH_ARGS+=("--check")
"$MESH" "${MESH_ARGS[@]}"

REFRESH_ARGS=()
[ -n "$CHECK" ] && REFRESH_ARGS+=("--check")
"$REFRESH" "${REFRESH_ARGS[@]}"

DOCTRINE="$SCRIPT_DIR/validate_agent_mesh.sh"
if [ -f "$DOCTRINE" ]; then
    DOCTRINE_ARGS=()
    [ -n "$CHECK" ] && DOCTRINE_ARGS+=("--check")
    "$DOCTRINE" "${DOCTRINE_ARGS[@]}"
fi
