# Shared-checkout gating design

## Context

This spec covers the shared-checkout gating changes for the same PR that fixes the `.gitignore` SDD rule drift. The `.gitignore` work is already implemented:

- Root `.gitignore` no longer contains `.agents/superpowers/sdd/**` or `!.agents/superpowers/sdd/.gitignore`.
- `.agents/superpowers/sdd/.gitignore` contains `*` and `!.gitignore`.
- `repo-standards/scripts/scaffold_gitignore.py` and `references/repository-shape-standard.md` are updated to enforce the local SDD `.gitignore` rule.

This spec reflects the final, simplified shared-checkout gating: a single runtime `--allow-shared-checkout` flag that is forwarded from parent scripts to child scripts, replacing the previous token-based two-step approval.

## Problem

The original `--allow-shared-checkout` flag only printed a warning and then immediately permitted mutation when combined with `--apply`/`--yes`. There was no clear, agent-visible approval step. The initial redesign introduced a token-based pre-approval step, but that was evaluated as overly complex because it required separate invocations, TTL tracking, and redundant script re-runs.

## Goals

1. A mutation script must not write files in a shared checkout unless the caller explicitly passes `--allow-shared-checkout`.
2. `--allow-shared-checkout` must be combined with `--apply` (or the default mutation mode) in the same invocation; it is rejected when used alone or with `--check`.
3. In a shared checkout, the script warns and, when running interactively, prompts for confirmation.
4. Parent scripts (`rebuild_marketplace.py`, `new_worktree.py`) must forward `--allow-shared-checkout` to any child mutation scripts they invoke.
5. No flags should default to mutating; `--apply` must be explicit.

## Out of scope

- Repo-specific tools that do not ship as skills (e.g., `heal_overlays.py`, `update_superpowers_source.py`) are not gated in this PR.
- `generate_index_mesh.py` is in scope because it ships as a skill and writes `INDEX.md` files.

## Mechanism

### Shared helper

`tools/shared_checkout.py` provides a single helper used by every gated script:

```python
def is_shared_checkout(repo_root: Path) -> bool
def prompt_for_approval(script_name: str) -> bool
def approve_mutation(repo_root: Path, script_name: str, flag_approved: bool) -> bool
```

- `is_shared_checkout` runs `git rev-parse --absolute-git-dir` and `git rev-parse --git-common-dir` and compares the resolved paths.
- `prompt_for_approval` returns `False` in a non-TTY and prompts `Allow <script-name> to apply changes in this shared checkout? (y/N)` when a TTY is available.
- `approve_mutation` returns `True` immediately for non-shared checkouts; in a shared checkout it requires `flag_approved=True` or a successful interactive prompt.

### Gated scripts

Each mutation script:

1. Adds `--allow-shared-checkout` to its argument parser.
2. Rejects `--allow-shared-checkout` unless `--apply` (or the mutation mode) is present.
3. Calls `shared_checkout.approve_mutation(ROOT, SCRIPT_NAME, args.allow_shared_checkout)` before writing files.
4. Prints a clear error telling the user to pass `--allow-shared-checkout` if the flag is missing in a shared checkout.

Scripts updated:

- `sources/first_party/skills/repo-standards/scripts/repo_standards.py`
- `sources/first_party/skills/refreshing-installed-skills/scripts/refresh_installed_skills.py`
- `sources/first_party/skills/generating-agent-mesh/scripts/generate_index_mesh.py`
- `tools/rebuild_marketplace.py`
- `adapters/codex/superpowers-plus/using-git-worktrees/scripts/new_worktree.py`

### Orchestrator forwarding

`tools/rebuild_marketplace.py` accepts `--allow-shared-checkout` and forwards it to:

- `refresh_installed_skills.py` during the `project` phase (when `--apply` is used).
- `generate_index_mesh.py` during the `index` phase (when `--apply` is used).

`new_worktree.py` accepts `--allow-shared-checkout` and forwards it to the `refresh_installed_skills.py` and `generate_index_mesh.py` scripts it discovers in the new worktree.

### No pre-approval tokens

The previous `tools/shared_checkout_approval.py` token helper and `<git-dir>/info/devin-shared-checkout-approval-*` token files are removed. Approval is per-run and explicit.

### Default behavior

All gated scripts default to check/no-op when called with no flags. `--apply` must be explicit.

## Changes

- Remove `tools/shared_checkout_approval.py`.
- Add `tools/shared_checkout.py` with `approve_mutation`, `is_shared_checkout`, and `prompt_for_approval`.
- Copy `shared_checkout.py` alongside each gated skill script so installed/projected skill trees are self-contained.
- Update `sources/first_party/skills/repo-standards/scripts/repo_standards.py`.
- Update `sources/first_party/skills/refreshing-installed-skills/scripts/refresh_installed_skills.py`.
- Update `sources/first_party/skills/generating-agent-mesh/scripts/generate_index_mesh.py`.
- Update `tools/rebuild_marketplace.py` to add `--allow-shared-checkout` and forward it to child scripts.
- Update `adapters/codex/superpowers-plus/using-git-worktrees/scripts/new_worktree.py` to add `--allow-shared-checkout` and forward it.
- Update `tools/AGENTS.md` to document the combined flag usage.
- Update `tests/test_shared_checkout.py` (renamed from `tests/test_shared_checkout_approval.py`) and `tests/test_repo_standards.py`, `tests/test_refresh_installed_skills.py`, `tests/test_worktree_scripts.py`.
- Regenerate marketplace projections and run `py -3 -m pytest` plus `py -3 tools/check_marketplace.py` before claiming done.

## Testing

- `tests/test_shared_checkout.py` covers `is_shared_checkout`, `prompt_for_approval`, and `approve_mutation`.
- `tests/test_repo_standards.py` covers:
  - `--apply --allow-shared-checkout` succeeds in a shared checkout.
  - `--allow-shared-checkout` alone and with `--check` are rejected.
  - `--apply` in a shared checkout fails without `--allow-shared-checkout`.
- `tests/test_refresh_installed_skills.py` patches `shared_checkout.approve_mutation` and continues to exercise install/refresh behavior.
- `tests/test_worktree_scripts.py` covers `new_worktree.py` `--allow-shared-checkout` forwarding.
- Full green path: `py -3 -m pytest` and `py -3 tools/check_marketplace.py`.
