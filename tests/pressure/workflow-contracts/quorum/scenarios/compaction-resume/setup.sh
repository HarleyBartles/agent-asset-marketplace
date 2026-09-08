#!/usr/bin/env bash
set -euo pipefail
setup-helpers run create_base_repo
source "$QUORUM_SCENARIO_DIR/../../lib/stage-skills-only.sh"
checkpoint_head=$(git -C "$QUORUM_WORKDIR" rev-parse HEAD)
cat > "$QUORUM_WORKDIR/.agents/checkpoint.md" <<EOF
# Durable checkpoint

- HEAD: $checkpoint_head
- Dirty state: clean
EOF
printf '%s\n' 'resume drift' >> "$QUORUM_WORKDIR/README.md"
