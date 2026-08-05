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
2. `ci --apply` runs the same checks as `ci --check` by performing an `apply` pass for every `ci` dependency, then a `check` pass with the same `Ctx` but `mode="check"`. It still fails if a check has no mechanical fix.
3. The pre-commit hook runs `ci --apply --allow-shared-checkout`, stages all resulting changes, then runs `ci --check` to prove the commit is clean.
4. `validate` no longer treats an uncommitted working tree as an error. It only checks whitespace, authority-asset validity, and `AGENTS.md` / `INDEX.md` consistency.
5. `--allow-shared-checkout` is honored and passed down through `ci --apply` to the individual `apply` calls.

## Non-goals (out of scope for this phase)

- Changing the draft/ready PR policy or the `AGENTS.md` validation command list.
- Adding new `apply` logic to `review-preflight` (it remains a read-only check).
- Refactoring `tools/run.py` beyond the minimum needed for the apply-then-check pass.

## Design

### `tools/run.py`

#### `dataclasses.replace` import

Update `from dataclasses import dataclass` to `from dataclasses import dataclass, replace` so `run_targets` can build a `mode="check"` context from the `apply` context for the re-check pass.

#### `_run_validate`

Remove the `if ctx.mode == "check": _git_diff_exit_code(ctx)` block. Keep `_git_diff_check(ctx)` so whitespace errors in the current diff are still caught. After this change `_run_validate` behaves identically in `apply` and `check` modes and no longer considers whether the working tree is committed.

#### `validate` task

Update the `fix` string from `tools/run marketplace --apply` to `tools/run validate --apply`.

#### `run_targets`

Change the function so that when `ctx.mode == "apply"` it first runs the `apply` steps for every target in the resolved list, then creates a new `Ctx(..., mode="check")` with `dataclasses.replace` and runs the `check` steps for every target. When `ctx.mode == "check"` it runs only the `check` pass.

This makes `tools/run <target> --apply` re-check the same target, and it makes `tools/run ci --apply` run the exact same checks as `tools/run ci --check` after applying fixes.

```python
def run_targets(targets: list[str], ctx: Ctx) -> None:
    def _run_steps(target: str, task: Task, steps: tuple[Callable[[Ctx], None], ...], run_ctx: Ctx) -> None:
        if not steps:
            return
        print(f"[tools/run] === {target} ({run_ctx.mode})")
        for step in steps:
            try:
                step(run_ctx)
            except Exception as exc:
                fix = _lint_fix(run_ctx) if target == "lint" else task.fix
                raise RunnerError(target, fix, exc) from exc

    for target in targets:
        task = _TASKS[target]
        _run_steps(target, task, task.apply, ctx)
    if ctx.mode == "apply":
        check_ctx = replace(ctx, mode="check")
        for target in targets:
            task = _TASKS[target]
            _run_steps(target, task, task.check, check_ctx)
```

#### `argparse` epilog

Replace the epilog to describe `ci --check` as the strict non-mutating CI/PR gate and `ci --apply` as the mechanical-fix command, and remove the warning about not running `ci --check` on an uncommitted working tree.

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

Add or update tests to match the new behavior:

1. `test_validate_fix_message` — assert a `validate` failure prints `Fix: tools/run validate --apply`.
2. `test_ci_apply_runs_review_preflight_check` — assert `tools/run ci --apply` eventually invokes `tools/review_preflight.py --check` (the non-mechanical `review-preflight` has no `apply` step, so the re-check pass must run it).
3. `test_validate_does_not_call_git_diff_exit_code` — assert `_run_validate(ctx)` with `mode="check"` never calls `_git_diff_exit_code`, guarding against accidental re-introduction of the working-tree cleanliness check.

## Interfaces and contracts

- `tools/run ci --check` — mutates nothing; returns non-zero on any drift or violation.
- `tools/run ci --apply` — mutates generated/derived surfaces and then re-checks them; returns non-zero on any violation that cannot be mechanically fixed.
- `tools/run <target> --apply` — runs the `apply` steps for the target and then its `check` steps. `review-preflight` only runs the `check` step because it has no `apply`.
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
- `ci --apply` is slower than the old mesh-only pre-commit because it runs a full `apply` pass followed by a full `check` pass. The tradeoff is that the agent never needs to manually run `marketplace --apply` or `lint --apply` before committing and `ci --apply` is now a faithful preview of `ci --check`.
- `ci --apply` will run `lint --apply` (ruff fix/format) on every commit, which may auto-correct style. This is desirable mechanical behavior.
