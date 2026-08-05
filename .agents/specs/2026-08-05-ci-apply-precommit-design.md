# CI apply/pre-commit — design spec

> **Scope:** Make `ci --apply` the mechanical-fix command, make `ci --check` the strict pre-flight/PR gate, and make the pre-commit hook apply mechanical fixes instead of only regenerating the INDEX mesh.
> **Date:** 2026-08-05

## Problem

1. `tools/run.py ci --check` is supposed to tell an agent whether the pre-commit hook will pass, but it currently fails on any uncommitted working-tree change because `_run_validate` calls `git diff --exit-code`. That makes it useless as a pre-flight check.
2. The pre-commit hook only fixes a stale `INDEX.md` mesh. It does not apply other mechanical fixes such as `marketplace`, `repo-index`, `archive-links`, or `lint`.
3. `ci --apply` exists but does not run the non-mechanical checks that `ci --check` runs, so an agent who fixes mechanical problems with `ci --apply` still has to run `ci --check` to catch non-fixable issues.
4. The `validate` task's `fix` message is `tools/run marketplace --apply`, which is unrelated to the failure.

## Goals

1. `ci --check` is the canonical, strict, non-mutating PR and pre-flight gate. It fails on mechanical drift with a `Fix: tools/run <target> --apply` (or `tools/run ci --apply`) message and fails on non-mechanical issues with a manual remediation message.
2. `ci --apply` runs the same checks as `ci --check`, but for every check that is mechanically fixable it first runs the `apply` step and then re-checks. It still fails if a check has no mechanical fix.
3. The pre-commit hook runs `ci --apply --allow-shared-checkout`, stages all resulting changes, then runs `ci --check` to prove the commit is clean.
4. `validate` no longer treats an uncommitted working tree as an error. It only checks whitespace, authority-asset validity, and `AGENTS.md` / `INDEX.md` consistency.
5. `--allow-shared-checkout` is honored and passed down through `ci --apply` to the individual `apply` calls.

## Non-goals (out of scope for this phase)

- Changing the draft/ready PR policy or the `AGENTS.md` validation command list.
- Adding new `apply` logic to `review-preflight` (it remains a read-only check).
- Refactoring the `Task` model beyond the minimum needed for `apply-then-check`.

## Design

### `tools/run.py`

#### `Task` dataclass

Add `check_after_apply: bool = False`. When `mode == "apply"` and this flag is `True`, `run_targets` will run the `apply` steps followed by the `check` steps for that task.

Set `check_after_apply=True` only for the `ci` task. Individual `tools/run mesh --apply` remains apply-only; `ci --apply` is the only combined apply-then-check command.

#### `_run_validate`

Remove the `if ctx.mode == "check": _git_diff_exit_code(ctx)` block. Keep `_git_diff_check(ctx)` so whitespace errors in the current diff are still caught.

Update the `validate` task's `fix` string from `tools/run marketplace --apply` to `tools/run validate --apply` (which re-runs the validators; whitespace and authority errors are manual).

Update the `argparse` epilog to no longer tell users to avoid running `ci --check` on an uncommitted working tree. Instead, describe `ci --check` as the strict PR gate and `ci --apply` as the mechanical fix command.

#### `run_targets`

Change the step selection so that in `apply` mode, for a `Task` with `check_after_apply=True`, it runs `task.apply` then `task.check`. For all other tasks it runs only `task.apply`.

### `.git/hooks/pre-commit`

Replace the mesh-only conditional block with:

```bash
#!/usr/bin/env bash
set -euo pipefail
REPO_ROOT="$(git rev-parse --show-toplevel)"
cd "$REPO_ROOT"

"$REPO_ROOT/tools/run" ci --apply --allow-shared-checkout
git add -A
exec "$REPO_ROOT/tools/run" ci --check
```

This applies all mechanical fixes, stages the regenerated and formatted changes, then runs the strict `ci --check` to catch anything that cannot be auto-fixed.

### `tests/test_run_cli.py`

Update the `ci`/`validate` tests to match the new behavior:

- `ci --check` no longer fails merely because the working tree has uncommitted changes.
- `ci --apply` runs the `check` steps for all `ci` dependencies (or at least the `review-preflight` check, since it has no `apply`).
- The `validate` `fix` message is `tools/run validate --apply`.

## Interfaces and contracts

- `tools/run ci --check` — mutates nothing; returns non-zero on any drift or violation.
- `tools/run ci --apply` — mutates generated/derived surfaces; returns non-zero on any violation that cannot be mechanically fixed.
- `tools/run <target> --apply` (non-`ci`) — remains the existing apply-only command for the individual target.
- `validate` — no longer cares whether the working tree is committed; only validates content and whitespace.

## Cross-repo consumer considerations

None. This is a repo-local tooling change.

## Validation

- `py -3 tools/run.py ci --check` passes on a clean tree.
- `py -3 tools/run.py ci --apply` fixes a deliberately stale `INDEX.md` / `marketplace.json` and then passes.
- `py -3 tools/run.py validate --check` passes on a tree with uncommitted, whitespace-clean changes.
- A test commit with a stale `INDEX.md` causes the pre-commit hook to regenerate and include the fixed `INDEX.md`.
- `py -3 tools/run.py ci --check` still fails when a non-mechanical issue is present (e.g. a real `review-preflight` finding).

## Risks and tradeoffs

- `git add -A` in the pre-commit hook will stage any untracked file, not just generated ones. This is acceptable because the repo's `.gitignore` keeps scratch and temporary files out, and the doctrine is that the working tree should not hold intentionally untracked repo files.
- Running `ci --apply` on every commit is slower than the old mesh-only pre-commit. The tradeoff is that the agent never needs to manually run `marketplace --apply` or `lint --apply` before committing.
- `ci --apply` will run `lint --apply` (ruff fix/format) on every commit, which may auto-correct style. This is desirable mechanical behavior.
