#!/usr/bin/env bash
set -euo pipefail

marketplace_root=${MARK373_REPO_ROOT:?MARK373_REPO_ROOT is required}
evidence_head=${MARK373_EVIDENCE_HEAD:?MARK373_EVIDENCE_HEAD is required}
skills_source="$marketplace_root/.agents/skills"
skills_target="$QUORUM_WORKDIR/.agents/skills"

test -d "$skills_source"

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
printf '%s\n' "$evidence_head" > "$QUORUM_WORKDIR/.agents/mark373-evidence-head"
printf '%s\n' "$skills_sha256" > "$QUORUM_WORKDIR/.agents/mark373-skills-sha256"
