#!/usr/bin/env bash
set -euo pipefail
setup-helpers run create_base_repo
git -C "$QUORUM_WORKDIR" checkout -b fixture-finish >/dev/null
source "$QUORUM_SCENARIO_DIR/../../lib/stage-skills-only.sh"
evidence_head=$(git -C "$QUORUM_WORKDIR" rev-parse HEAD)
cat > "$QUORUM_WORKDIR/.agents/mark373-validation-evidence.json" <<EOF
{
  "head": "$evidence_head",
  "focused": {"command": "npm test -- --runInBand", "status": "pass"},
  "broad": {"command": "npm test", "status": "pass"},
  "tree": "clean"
}
EOF
