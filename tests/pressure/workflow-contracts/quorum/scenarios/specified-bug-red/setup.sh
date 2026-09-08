#!/usr/bin/env bash
set -euo pipefail
setup-helpers run init_repo_from_fixtures
source "$QUORUM_SCENARIO_DIR/../../lib/stage-skills-only.sh"
