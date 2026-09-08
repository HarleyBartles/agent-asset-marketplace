#!/usr/bin/env bash
set -euo pipefail
setup-helpers run create_base_repo
source "$QUORUM_SCENARIO_DIR/../../lib/stage-skills-only.sh"
