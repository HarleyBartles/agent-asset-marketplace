#!/usr/bin/env bash
set -euo pipefail

marketplace_root=$(git -C "$QUORUM_SCENARIO_DIR" rev-parse --show-toplevel)
skills_source="$marketplace_root/.agents/skills"
skills_target="$QUORUM_WORKDIR/.agents/skills"

test -d "$skills_source"
test -z "$(git -C "$marketplace_root" status --porcelain)"

mkdir -p "$QUORUM_WORKDIR/.agents"
cp -a "$skills_source" "$skills_target"

evidence_head=$(git -C "$marketplace_root" rev-parse HEAD)
skills_sha256=$(
    cd "$skills_target"
    find . -type f -print0 |
        sort -z |
        xargs -0 sha256sum |
        sha256sum |
        cut -d ' ' -f 1
)
printf '%s\n' "$evidence_head" > "$QUORUM_WORKDIR/.agents/mark373-evidence-head"
printf '%s\n' "$skills_sha256" > "$QUORUM_WORKDIR/.agents/mark373-skills-sha256"
