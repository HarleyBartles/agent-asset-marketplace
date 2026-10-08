#!/usr/bin/env bash
set -euo pipefail

if command -v py >/dev/null 2>&1; then
  HOOK_PYTHON=(py -3)
elif command -v python3 >/dev/null 2>&1; then
  HOOK_PYTHON=(python3)
elif command -v python >/dev/null 2>&1; then
  HOOK_PYTHON=(python)
else
  printf 'hook gate prerequisite missing: py, python3, or python is required\n' >&2
  return 2
fi

run_repository_check_gate() {
  "${HOOK_PYTHON[@]}" - "$REPO_ROOT" <<'PY'
import json
import subprocess
import sys
from pathlib import Path

repo_root = Path(sys.argv[1])
declaration_path = repo_root / ".agents/contracts/repo-standards-commands.json"
try:
    declaration = json.loads(declaration_path.read_text(encoding="utf-8"))
except (OSError, UnicodeError, json.JSONDecodeError) as error:
    print(f"hook gate configuration failed: {declaration_path}: {error}", file=sys.stderr)
    raise SystemExit(2)

if not isinstance(declaration, dict) or set(declaration) != {"check"}:
    print("hook gate configuration must contain only the check command", file=sys.stderr)
    raise SystemExit(2)
commands = declaration.get("check")
expected = ["@python", "tools/run.py", "ci", "--check"]
if not isinstance(commands, list) or commands != [expected]:
    print("hook gate check must be exactly @python tools/run.py ci --check", file=sys.stderr)
    raise SystemExit(2)

for declared in commands:
    if not isinstance(declared, list) or not all(isinstance(part, str) and part for part in declared):
        print("hook gate check command must be a non-empty string vector", file=sys.stderr)
        raise SystemExit(2)
    if "--apply" in declared or "--diagnostics" in declared:
        print("hook gate check rejects apply and aggregate diagnostics commands", file=sys.stderr)
        raise SystemExit(2)
    argv = [sys.executable, *declared[1:]] if declared[0] == "@python" else declared
    try:
        result = subprocess.run(argv, cwd=repo_root, check=False)
    except OSError as error:
        print(f"hook gate could not start {argv[0]}: {error}", file=sys.stderr)
        raise SystemExit(2)
    if result.returncode:
        raise SystemExit(result.returncode)
PY
}
