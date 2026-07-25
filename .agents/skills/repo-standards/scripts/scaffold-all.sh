#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

for script in scaffold-repo-guide-policy scaffold-guides scaffold-review scaffold-contributing scaffold-ci-preflight scaffold-gitignore scaffold-agents-md scaffold-marketplace-json; do
    echo "==> running ${script}"
    "${SCRIPT_DIR}/${script}.sh" "$@"
done
