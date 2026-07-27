# Shared-checkout approval gating design

## Context

This spec covers the shared-checkout gating changes for the same PR that fixes the `.gitignore` SDD rule drift. The `.gitignore` work is already implemented:

- Root `.gitignore` no longer contains `.agents/superpowers/sdd/**` or `!.agents/superpowers/sdd/.gitignore`.
- `.agents/superpowers/sdd/.gitignore` contains `*` and `!.gitignore`.
- `repo-standards/scripts/scaffold_gitignore.py` and `references/repository-shape-standard.md` are updated to enforce the local SDD `.gitignore` rule.

This spec focuses on making `--allow-shared-checkout` an authoritative, two-step approval gate across the mutation scripts that ship as skills (and the repo-local `rebuild_marketplace.py` orchestrator).

## Problem

Today `--allow-shared-checkout` prints a warning but then immediately permits mutation when combined with `--apply`/`--yes`. An agent can read the warning only after the mutation has already happened. The flag must be split into a separate approval step so the agent sees the warning, decides whether they have permission, and then explicitly runs `--apply`.

## Goals

1. No mutation script may apply changes in a shared checkout without a separate approval step.
2. `--allow-shared-checkout` must be usable only as an approval step; it must reject mutation flags in the same invocation.
3. The approval must be short-lived (10 minutes) and consumed on first use.
4. The approval must be stored in the git metadata directory so it is never committed.
5. Parent scripts like `rebuild_marketplace.py` may pre-approve child scripts that are part of the same approved operation.
6. No flags should default to mutating; `--apply` must be explicit.

## Out of scope

- Repo-specific tools that do not ship as skills (e.g., `heal_overlays.py`, `update_superpowers_source.py`) are not gated in this PR.
- `generate_index_mesh.py` is in scope because it ships as a skill and writes `INDEX.md` files.

## Mechanism

### Token storage

A shared helper, `tools/shared_checkout_approval.py`, provides script-specific tokens:

```text
<git-dir>/info/devin-shared-checkout-approval-<script-name>
```

Each token file contains an ISO-8601 UTC timestamp. Tokens are valid for 10 minutes and are consumed (deleted) on first use.

### Token helper API

```python
approval_path(repo_root: Path, script_name: str) -> Path
is_valid(repo_root: Path, script_name: str) -> bool
write(repo_root: Path, script_name: str) -> Path
consume(repo_root: Path, script_name: str) -> bool
```

All functions operate with `newline="\n"` and UTC ISO-8601 timestamps.

### Prompt behavior

When `--allow-shared-checkout` is invoked and `sys.stdin.isatty()` is True, the script prints the warning and prompts:

```text
Record shared-checkout approval for <script-name>? (y/N)
```

Only a response starting with `y` or `Y` writes the token; anything else exits 1.

### Approval flow

1. `repo_standards --allow-shared-checkout`
   - Writes the `repo-standards` token.
   - Prints a warning that human approval is required.
   - Optionally prompts in a TTY.
   - Exits 0.
   - Errors if combined with `--apply` or `--check`.

2. `repo_standards --apply --yes`
   - In a shared checkout, consumes the `repo-standards` token.
   - If no valid token, errors with "run --allow-shared-checkout first".
   - If not a shared checkout, proceeds normally.

3. `refresh_installed_skills.py --allow-shared-checkout`
   - Writes the `refresh-installed-skills` token and the `generate-index-mesh` token (because it calls `generate_index_mesh.py`).
   - Prints warning, optionally prompts, exits.
   - Errors if combined with `--apply`/`--check`.

4. `refresh_installed_skills.py --apply`
   - In a shared checkout, consumes the `refresh-installed-skills` token.
   - Before calling `generate_index_mesh.py`, that script consumes its own token.

5. `generate_index_mesh.py --allow-shared-checkout`
   - Writes the `generate-index-mesh` token.
   - Prints warning, optionally prompts, exits.

6. `generate_index_mesh.py --apply`
   - In a shared checkout, consumes the `generate-index-mesh` token before writing any `INDEX.md` files.

7. `rebuild_marketplace.py --allow-shared-checkout`
   - Writes tokens for `rebuild-marketplace`, `refresh-installed-skills`, and `generate-index-mesh`.
   - Prints warning, optionally prompts, exits.

8. `rebuild_marketplace.py --apply`
   - In a shared checkout, consumes the `rebuild-marketplace` token.
   - Calls `refresh_installed_skills.py` and `generate_index_mesh.py` without `--allow-shared-checkout`; those scripts consume their pre-written tokens.
   - `rebuild_marketplace.py` also consumes any unconsumed tokens at the end of the run (e.g., when `--skip-install` is used).

### Default behavior

All four scripts default to check/no-op when called with no flags. `--apply` must be explicit.

## Changes

- Add `tools/shared_checkout_approval.py` with token read/write/consume helpers.
- Update `sources/first_party/skills/repo-standards/scripts/repo_standards.py`.
- Update `sources/first_party/skills/refreshing-installed-skills/scripts/refresh_installed_skills.py`.
- Update `sources/first_party/skills/generating-agent-mesh/scripts/generate_index_mesh.py`.
- Update `tools/rebuild_marketplace.py` to add `--apply`, `--allow-shared-checkout`, and token orchestration.
- Update `tests/test_repo_standards.py` and `tests/test_refresh_installed_skills.py`.
- Regenerate marketplace projections.
- Run `tools/rebuild_marketplace.py` and `py -3 -m pytest` before claiming done.

## Testing

- Add tests that `--allow-shared-checkout` rejects `--apply` in the same invocation.
- Add tests that mutation in a shared checkout fails without a pre-existing token.
- Add tests that the approval step writes a token and the apply step consumes it.
- Add tests that expired or missing tokens are rejected.
- Add tests for `rebuild_marketplace.py` token orchestration.
- Run the full `pytest` suite and `tools/check_marketplace.py`.
