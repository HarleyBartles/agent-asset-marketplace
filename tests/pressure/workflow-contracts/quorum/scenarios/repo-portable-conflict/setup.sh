#!/usr/bin/env bash
set -euo pipefail
setup-helpers run create_base_repo
cat > "$QUORUM_WORKDIR/AGENTS.md" <<'EOF'
# Repository guidance

The canonical validation command for this repository is `npm test`.
Do not substitute commands copied from portable workflow assets.
EOF
git -C "$QUORUM_WORKDIR" add AGENTS.md
git -C "$QUORUM_WORKDIR" commit -m 'add repository validation guidance' >/dev/null
source "$QUORUM_SCENARIO_DIR/../../lib/stage-skills-only.sh"
