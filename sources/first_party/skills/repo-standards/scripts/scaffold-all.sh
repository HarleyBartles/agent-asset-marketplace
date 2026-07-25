#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

for script in scaffold-review scaffold-guides scaffold-contributing scaffold-gitignore; do
    echo "==> running ${script}"
    "${SCRIPT_DIR}/${script}.sh" "$@"
done
