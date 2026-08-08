# tools

Small helper scripts belong here.

Agent-facing policy for this directory lives in [.devin/rules/tools.md](../.devin/rules/tools.md).

Canonical task runner:

- `tools/run <target>... [--check | --apply] [--base-ref <ref>] [--allow-shared-checkout] [--verbose]` — dependency-aware runner that composes the marketplace generators and validators. On Linux/macOS/WSL/Git Bash use `./tools/run`; on Windows PowerShell use `.\tools\run.ps1`. `py -3 tools/run.py` works as a cross-platform fallback. The individual `.py` files below are implementation details.

Useful targets:

- `tools/run ci --check` / `tools/run.ps1 ci --check` — full non-mutating CI gate (lint, repo-standards, marketplace).
- `tools/run marketplace --apply` / `tools/run.ps1 marketplace --apply` — regenerate all marketplace surfaces.
- `tools/run marketplace --apply --allow-shared-checkout` / `tools/run.ps1 marketplace --apply --allow-shared-checkout` — approve writes in the main shared checkout.
- `tools/run mesh --apply` / `tools/run.ps1 mesh --apply` — regenerate only the repo-wide `INDEX.md` mesh.
- `tools/run installed-skills mesh --apply` / `tools/run.ps1 installed-skills mesh --apply` — refresh installed skills and regenerate the mesh.

Keep tooling minimal and focused on validation or lightweight asset handling.

## CLI contract

Every `tools/*.py` file that is meant to be run directly (it has an `if __name__ == "__main__":` guard) must:

- respond to `--help` with a `usage:` line and a `read-only`, `mutating`, or `mixed` classification in its description;
- respond to `--check` as the default, read-only, idempotent mode;
- respond to `--apply` if it is classified `mixed` or `mutating`;
- support `--force` if it may overwrite an existing, drifted surface;
- support `--allow-shared-checkout` (which requires `--apply`) if it may write to a shared or main worktree.

`tools/validate_tool_cli.py --check` is the contract gate and is run by `tools/run.py ci --check`.
