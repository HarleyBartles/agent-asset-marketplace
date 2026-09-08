#!/usr/bin/env bash
set -euo pipefail

marketplace_root=$(realpath "$QUORUM_SCENARIO_DIR/../../../../../..")
marketplace_git_dir=$(sed -n 's/^gitdir: //p' "$marketplace_root/.git")
marketplace_git_dir=$(wslpath -a "$marketplace_git_dir")
skills_source="$marketplace_root/.agents/skills"
skills_target="$QUORUM_WORKDIR/.agents/skills"

test -d "$skills_source"
test -z "$(git --git-dir="$marketplace_git_dir" --work-tree="$marketplace_root" status --porcelain)"

mkdir -p "$QUORUM_WORKDIR/.agents"
cp -a "$skills_source" "$skills_target"

skills_sha256=$(
    cd "$skills_target"
    find . -type f -print0 |
        sort -z |
        xargs -0 sha256sum |
        sha256sum |
        cut -d ' ' -f 1
)
evidence_head=$(git --git-dir="$marketplace_git_dir" --work-tree="$marketplace_root" rev-parse HEAD)
printf '%s\n' "$evidence_head" > "$QUORUM_WORKDIR/.agents/mark373-evidence-head"
printf '%s\n' "$skills_sha256" > "$QUORUM_WORKDIR/.agents/mark373-skills-sha256"
