# CI apply/pre-commit implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `/subagent-driven-development` (recommended) or `/executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make `tools/run ci --apply` the combined mechanical-fix + re-check command, make `ci --check` a strict pre-flight/PR gate that no longer fails on uncommitted changes, and update the pre-commit hook to apply mechanical fixes.

**Architecture:** In `tools/run.py`, import `dataclasses.replace` and change `run_targets` so `apply` mode runs the `apply` steps for every resolved target and then a `check` pass (with `mode="check"`) for every resolved target. Remove the working-tree cleanliness check from `_run_validate`, correct the `validate` `fix` string, and update the pre-commit hook to call `ci --apply --allow-shared-checkout`.

**Tech Stack:** Python 3, `tools/run.py`, `tools/run` bash wrapper, `.git/hooks/pre-commit`, `tests/test_run_cli.py`.

## Global Constraints

- All Python changes must pass `py -3 tools/run.py ci --check` before the PR is flipped to ready.
- Generated surfaces (`.agents/INDEX.md`, `repo-index/`, `codex-marketplace/manifest.json`, `.agents/plugins/marketplace.json`) are downstream outputs; only edit their source or the generators, not the generated files by hand.
- Pre-commit hooks are source-custody files in the shared `.git/hooks/`; they apply to all worktrees.
- The canonical CI gate is `py -3 tools/run.py ci --check`; it must be run on the staged tree before the final commit, then the pre-commit hook re-runs it.

---

### Task 1: Update `tools/run.py`

**Files:**
- Modify: `tools/run.py:12`, `tools/run.py:280-285`, `tools/run.py:404-409`, `tools/run.py:468-480`, `tools/run.py:483-491`

**Interfaces:**
- Consumes: existing `Task` dataclass, `run_targets`, `_run_validate`, `RunnerError`, `dataclasses.replace`.
- Produces: `run_targets` with `apply` then `check` passes, `_run_validate` without `_git_diff_exit_code`, `validate.fix` corrected to `tools/run validate --apply`.

- [ ] **Step 1.1: Import `replace` from `dataclasses`**

At `tools/run.py:12`, change:

```python
from dataclasses import dataclass, replace
```

No other changes to the `Ctx` or `Task` dataclasses are required.

- [ ] **Step 1.2: Remove the working-tree cleanliness check from `_run_validate`**

Replace `tools/run.py:280-285` with:

```python
def _run_validate(ctx: Ctx) -> None:
    _run([sys.executable, "tools/validate_authority_assets.py"], ctx)
    _run([sys.executable, "tools/validate_agents_md.py"], ctx)
    _git_diff_check(ctx)
```

`_git_diff_check(ctx)` remains; only the `_git_diff_exit_code(ctx)` guard is removed.

- [ ] **Step 1.3: Update the `validate` task `fix` string**

At `tools/run.py:404-409`, change `validate`:

```python
    "validate": Task(
        deps=("mesh",),
        apply=(_run_validate,),
        check=(_run_validate,),
        fix="tools/run validate --apply",
    ),
```

The `ci` task does not need a new flag; it keeps:

```python
    "ci": Task(
        deps=("lint", "repo-standards", "review-preflight", "validate", "archive-links"),
        fix="tools/run ci --apply",
    ),
```

- [ ] **Step 1.4: Update `run_targets` to run an `apply` pass followed by a `check` pass**

Replace `tools/run.py:468-480` with:

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

- [ ] **Step 1.5: Update the `argparse` epilog**

At `tools/run.py:483-491`, replace the `epilog` with:

```python
    parser = argparse.ArgumentParser(
        description="Dependency-aware task runner for the agent-asset-marketplace",
        epilog=(
            "Targets: " + ", ".join(_TASKS.keys()) + "\n"
            "ci --check is the full non-mutating CI/PR gate.\n"
            "ci --apply runs the same checks but applies mechanical fixes first.\n"
            "For a single target, run `tools/run <target> --apply`. See .devin/rules/tools.md."
        ),
    )
```

- [ ] **Step 1.6: Run `py -3 tools/run.py validate --check` with uncommitted changes**

Create a temporary whitespace-clean edit in a markdown file and run:

```bash
py -3 tools/run.py validate --check
```

Expected: passes (no longer fails because the working tree is uncommitted). Remove the temporary edit afterwards.

---

### Task 2: Update the pre-commit hook

**Files:**
- Modify: `.git/hooks/pre-commit`

**Interfaces:**
- Consumes: `tools/run ci --apply --allow-shared-checkout` and `tools/run ci --check`.
- Produces: a pre-commit that applies all mechanical fixes, re-stages, then validates.

- [ ] **Step 2.1: Replace the mesh-only pre-commit script**

Write `.git/hooks/pre-commit` as:

```bash
#!/usr/bin/env bash
set -euo pipefail
REPO_ROOT="$(git rev-parse --show-toplevel)"
cd "$REPO_ROOT"

"$REPO_ROOT/tools/run" ci --apply --allow-shared-checkout
git add -A

exec "$REPO_ROOT/tools/run" ci --check
```

- [ ] **Step 2.2: Make it executable**

```bash
git update-index --chmod=+x .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

- [ ] **Step 2.3: Smoke test in a disposable worktree**

Create a temporary worktree from the current branch, make a whitespace-clean edit that will cause `INDEX.md` staleness, and commit it. The new hook should regenerate the mesh and the commit should succeed. Then remove the worktree and the smoke branch.

```bash
SMOKE_BRANCH="smoke/ci-apply-precommit"
SMOKE_PATH="Z:\_agent-worktrees\agent-asset-marketplace\smoke-ci-apply-precommit"
git worktree add -b "$SMOKE_BRANCH" "$SMOKE_PATH" HEAD
cd "$SMOKE_PATH"

# Make a harmless whitespace-clean change to a tracked markdown file.
echo -e "\n<!-- smoke-test -->" >> .agents/runbooks/design.md
git add .agents/runbooks/design.md
git commit -m "smoke: verify pre-commit applies mesh fixes"
rc=$?

cd - > /dev/null
git worktree remove -f "$SMOKE_PATH"
git branch -D "$SMOKE_BRANCH"

[ $rc -eq 0 ] || exit 1
```

Expected: the pre-commit hook runs `ci --apply`, regenerates `INDEX.md` and related derived surfaces, re-stages them, and the `ci --check` final pass passes. The commit succeeds. The smoke branch and worktree are cleaned up after.

---

### Task 3: Update `tests/test_run_cli.py`

**Files:**
- Modify: `tests/test_run_cli.py`

**Interfaces:**
- Consumes: existing `test_run_cli.py` fixtures and `run` module functions.
- Produces: updated tests for `validate.fix`, `ci --apply` re-check behavior, and the absence of `_git_diff_exit_code` in `validate`.

- [ ] **Step 3.1: Add `test_validate_fix_message`**

Append to `tests/test_run_cli.py`:

```python
def test_validate_fix_message(monkeypatch):
    def boom(cmd, ctx):
        raise subprocess.CalledProcessError(1, cmd)

    monkeypatch.setattr(run, "_run", boom)

    ctx = run.Ctx(mode="check", base_ref=None, allow_shared=False, verbose=False)
    with pytest.raises(run.RunnerError) as exc_info:
        run.run_targets(["validate"], ctx)
    assert "target 'validate' failed" in str(exc_info.value)
    assert "Fix: tools/run validate --apply" in str(exc_info.value)
```

- [ ] **Step 3.2: Add `test_ci_apply_runs_review_preflight_check`**

Append to `tests/test_run_cli.py`:

```python
def test_ci_apply_runs_review_preflight_check(monkeypatch):
    calls = []

    def fake_run(cmd, ctx):
        calls.append(" ".join(cmd))

    monkeypatch.setattr(run, "_run", fake_run)
    monkeypatch.setattr(run, "_git_diff_check", lambda ctx: None)
    monkeypatch.setattr(run, "_git_diff_exit_code", lambda ctx: None)
    monkeypatch.setattr(run, "_prune_stale_projected_plugin_roots", lambda: None)

    ctx = run.Ctx(mode="apply", base_ref=None, allow_shared=True, verbose=False)
    run.run_targets(["ci"], ctx)

    review_preflight_calls = [c for c in calls if "tools/review_preflight.py" in c]
    assert review_preflight_calls
    assert "--check" in review_preflight_calls[0]
```

- [ ] **Step 3.3: Add `test_validate_does_not_call_git_diff_exit_code`**

Append to `tests/test_run_cli.py`:

```python
def test_validate_does_not_call_git_diff_exit_code(monkeypatch):
    calls = []

    def fake_git_diff_exit_code(ctx):
        calls.append("git_diff_exit_code")

    monkeypatch.setattr(run, "_git_diff_exit_code", fake_git_diff_exit_code)
    monkeypatch.setattr(run, "_git_diff_check", lambda ctx: None)
    monkeypatch.setattr(run, "_run", lambda cmd, ctx: None)

    ctx = run.Ctx(mode="check", base_ref=None, allow_shared=False, verbose=False)
    run._run_validate(ctx)

    assert "git_diff_exit_code" not in calls
```

- [ ] **Step 3.4: Run the test suite for `tools/run`**

```bash
py -3 -m pytest tests/test_run_cli.py -v
```

Expected: all tests pass, including the three new tests.

---

### Task 4: Regenerate surfaces, run `ci --check`, and commit

**Files:**
- Generated: `.agents/INDEX.md`, `.agents/skills/`, `codex-marketplace/manifest.json`, `.agents/plugins/marketplace.json`, `repo-index/repo-index.json`

**Interfaces:**
- Consumes: updated `tools/run.py`, pre-commit hook, and tests.
- Produces: a clean, regenerated repository surface on a passing commit.

- [ ] **Step 4.1: Run `ci --apply`**

```bash
py -3 tools/run.py ci --apply
```

Expected: regenerates any stale derived surfaces and passes. If it fails on a non-mechanical issue, fix the underlying problem before continuing.

- [ ] **Step 4.2: Stage and run the canonical `ci --check` on the staged tree**

```bash
git add -A
py -3 tools/run.py ci --check
```

Expected: passes on the staged tree. Do not commit before this passes.

- [ ] **Step 4.3: Commit the source and regenerated changes**

```bash
git commit -m "feat: make ci --apply the mechanical pre-commit fix and ci --check the strict gate"
```

Expected: the pre-commit hook runs and the commit succeeds.

- [ ] **Step 4.4: Run `ci --check` on the committed tree**

```bash
py -3 tools/run.py ci --check
```

Expected: passes.

---

### Task 5: Publish

**Files:**
- None (GitHub operations)

**Interfaces:**
- Consumes: local `feat/ci-apply-precommit` branch.
- Produces: pushed branch and updated draft PR.

- [ ] **Step 5.1: Push the branch**

```bash
git push origin feat/ci-apply-precommit
```

- [ ] **Step 5.2: Create or update the draft PR body**

Write `C:\Users\hbart\AppData\Local\Temp\pr-body.txt`:

```markdown
## Summary
- `tools/run <target> --apply` now runs `apply` then `check` for the target.
- `tools/run ci --apply` runs the same checks as `ci --check` after applying mechanical fixes.
- `ci --check` no longer fails on an uncommitted working tree.
- `validate` no longer treats an uncommitted working tree as an error.
- The pre-commit hook now runs `ci --apply --allow-shared-checkout` and re-stages the result before `ci --check`.

## Validation
- `py -3 tools/run.py ci --check` passes.
- `py -3 tools/run.py ci --apply` regenerates stale surfaces and passes.
- `py -3 -m pytest tests/test_run_cli.py` passes.
- Pre-commit hook smoke test in a disposable worktree passes.

Generated with [Devin](https://devin.ai)

Co-Authored-By: Devin <158243242+devin-ai-integration[bot]@users.noreply.github.com>
```

Then create the draft PR:

```bash
gh pr create --draft --title "ci: make ci --apply the mechanical pre-commit fix" --body-file "C:\Users\hbart\AppData\Local\Temp\pr-body.txt"
```

If the PR already exists, update its body with:

```bash
gh pr edit <number> --body-file "C:\Users\hbart\AppData\Local\Temp\pr-body.txt"
```

---

## Execution confidence: 9/10

The file paths, function names, and exact line numbers were verified against the current `tools/run.py` and `tests/test_run_cli.py`. The `run_targets` design is now implementable without the `ci` task needing new fields or steps. The pre-commit smoke test is isolated to a disposable worktree. Test code is provided verbatim and targeted. The only residual risk is the additional runtime of the second `check` pass in `--apply` mode, which is an accepted tradeoff documented in the spec.
