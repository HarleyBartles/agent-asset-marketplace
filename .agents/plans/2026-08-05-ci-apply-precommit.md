# CI apply/pre-commit implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `/subagent-driven-development` (recommended) or `/executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make `tools/run ci --apply` the combined mechanical-fix + re-check command, make `ci --check` a strict pre-flight/PR gate that no longer fails on uncommitted changes, and update the pre-commit hook to apply mechanical fixes.

**Architecture:** Add a `check_after_apply` flag to the `Task` dataclass in `tools/run.py`, use it only for the `ci` target so `ci --apply` runs `apply` then `check` for each dependency. Remove the working-tree cleanliness check from the `validate` task, fix its `fix` string, and update the pre-commit hook to call `ci --apply --allow-shared-checkout`.

**Tech Stack:** Python 3, `tools/run.py`, `tools/run` bash wrapper, `.git/hooks/pre-commit`, `tests/test_run_cli.py`.

## Global Constraints

- All Python changes must pass `py -3 tools/run.py ci --check` before the PR is flipped to ready.
- Generated surfaces (`.agents/INDEX.md`, `repo-index/`, `codex-marketplace/manifest.json`, `.agents/plugins/marketplace.json`) are downstream outputs; only edit their source or the generators, not the generated files by hand.
- Pre-commit hooks are source-custody files in the shared `.git/hooks/`; they apply to all worktrees.

---

### Task 1: Update `tools/run.py` for `ci` apply-then-check and `validate` correction

**Files:**
- Modify: `tools/run.py:36-40`, `tools/run.py:280-285`, `tools/run.py:404-409`, `tools/run.py:471-480`, `tools/run.py:483-491`

**Interfaces:**
- Consumes: existing `Task` dataclass, `run_targets`, `_run_validate`, `RunnerError`.
- Produces: `Task(check_after_apply=...)`, `_run_validate` without `_git_diff_exit_code`, corrected `validate.fix`, updated `run_targets` step selection.

- [ ] **Step 1.1: Add `check_after_apply` to `Task`**

```python
@dataclass(frozen=True)
class Task:
    deps: tuple[str, ...] = ()
    apply: tuple[Callable[[Ctx], None], ...] = ()
    check: tuple[Callable[[Ctx], None], ...] = ()
    fix: str = ""
    check_after_apply: bool = False
```

At `tools/run.py:36-40`.

- [ ] **Step 1.2: Remove the working-tree cleanliness check from `_run_validate`**

Replace `tools/run.py:280-285` with:

```python
def _run_validate(ctx: Ctx) -> None:
    _run([sys.executable, "tools/validate_authority_assets.py"], ctx)
    _run([sys.executable, "tools/validate_agents_md.py"], ctx)
    _git_diff_check(ctx)
```

`_git_diff_check(ctx)` remains; only the `_git_diff_exit_code(ctx)` guard is removed.

- [ ] **Step 1.3: Update the `validate` task `fix` string and set `check_after_apply=True` on `ci`**

At `tools/run.py:404-409`, change `validate`:

```python
    "validate": Task(
        deps=("mesh",),
        apply=(_run_validate,),
        check=(_run_validate,),
        fix="tools/run validate --apply",
    ),
```

At `tools/run.py:419-422`, update `ci`:

```python
    "ci": Task(
        deps=("lint", "repo-standards", "review-preflight", "validate", "archive-links"),
        fix="tools/run ci --apply",
        check_after_apply=True,
    ),
```

- [ ] **Step 1.4: Update `run_targets` to run `check` after `apply` when `check_after_apply=True`**

At `tools/run.py:471-480`, replace the body with:

```python
def run_targets(targets: list[str], ctx: Ctx) -> None:
    for target in targets:
        task = _TASKS[target]
        if ctx.mode == "apply":
            apply_steps = task.apply
            if task.check_after_apply:
                steps = apply_steps + task.check
            else:
                steps = apply_steps
        else:
            steps = task.check
        if not steps:
            continue
        print(f"[tools/run] === {target} ({ctx.mode})")
        for step in steps:
            try:
                step(ctx)
            except Exception as exc:
                fix = _lint_fix(ctx) if target == "lint" else task.fix
                raise RunnerError(target, fix, exc) from exc
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

Expected: passes (no longer fails because the working tree is uncommitted).

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

- [ ] **Step 2.3: Smoke test by making a whitespace-clean, generated-stale change**

Stage a deliberate `INDEX.md` staleness by editing a tracked markdown file, then:

```bash
git add -A
git commit -m "test: verify pre-commit applies mesh fixes"
```

Expected: hook regenerates `INDEX.md`, re-stages it, and the commit succeeds. The `INDEX.md` regeneration will be part of the test commit; this is the test commit.

---

### Task 3: Update `tests/test_run_cli.py`

**Files:**
- Modify: `tests/test_run_cli.py` (exact line numbers to be confirmed by the implementer)

**Interfaces:**
- Consumes: existing `test_run_cli.py` fixtures and assertions about `Fix: tools/run ...`.
- Produces: updated tests for `validate.fix` and `ci` apply-then-check behavior.

- [ ] **Step 3.1: Update the `validate` fix assertion**

Search `tests/test_run_cli.py` for the `validate` task `Fix:` assertion and update it to `tools/run validate --apply`.

- [ ] **Step 3.2: Add a test for `ci --apply` running `review-preflight` check**

`review-preflight` has no `apply` step. Add a test that `tools/run ci --apply` still invokes `review-preflight --check` (e.g., by patching `_check_review_preflight` and asserting it is called).

- [ ] **Step 3.3: Add a test for `validate` not failing on uncommitted changes**

Patch `_git_diff_check` to return cleanly and assert that `_git_diff_exit_code` is not called when `ctx.mode == "check"`. This guards against accidental re-introduction of the working-tree cleanliness check.

- [ ] **Step 3.4: Run the test suite for `tools/run`**

```bash
py -3 -m pytest tests/test_run_cli.py -v
```

Expected: all tests pass.

---

### Task 4: Regenerate marketplace/mesh surfaces and run `ci --check`

**Files:**
- Generated: `.agents/INDEX.md`, `.agents/skills/`, `codex-marketplace/manifest.json`, `.agents/plugins/marketplace.json`, `repo-index/repo-index.json`

**Interfaces:**
- Consumes: updated `tools/run.py` and pre-commit hook.
- Produces: a clean, regenerated repository surface.

- [ ] **Step 4.1: Run `ci --apply`**

```bash
py -3 tools/run.py ci --apply
```

Expected: regenerates any stale derived surfaces and passes. If it fails on a non-mechanical issue, fix the underlying problem before continuing.

- [ ] **Step 4.2: Stage and commit the source changes and regenerated surfaces**

```bash
git add -A
git commit -m "feat: make ci --apply the mechanical pre-commit fix and ci --check the strict gate"
```

Expected: the pre-commit hook runs and the commit succeeds.

- [ ] **Step 4.3: Run `ci --check` on the committed tree**

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
- Produces: open draft PR.

- [ ] **Step 5.1: Push the branch**

```bash
git push -u origin feat/ci-apply-precommit
```

- [ ] **Step 5.2: Open a draft PR**

```bash
gh pr create --draft --title "ci: make ci --apply the mechanical pre-commit fix" --body "$(cat <<'EOF'
## Summary
- `ci --apply` now runs `apply` then `check` for every `ci` dependency, applying mechanical fixes while still failing on non-mechanical issues.
- `ci --check` no longer fails on an uncommitted working tree.
- `validate` no longer treats an uncommitted working tree as an error.
- The pre-commit hook now runs `ci --apply --allow-shared-checkout` and re-stages the result before `ci --check`.

## Validation
- `py -3 tools/run.py ci --check` passes.
- `py -3 tools/run.py ci --apply` regenerates stale surfaces and passes.
- `py -3 -m pytest tests/test_run_cli.py` passes.
- Pre-commit hook smoke test passes.

Generated with [Devin](https://devin.ai)

Co-Authored-By: Devin <158243242+devin-ai-integration[bot]@users.noreply.github.com>
EOF
)"
```

---

## Execution confidence: 8/10

The design is clear, the file paths and functions are known, and the test surface is small. The main residual risk is the exact interaction between `git add -A` in the hook and any untracked, non-`.gitignore` files in the working tree; the plan documents this as an accepted tradeoff under existing repo doctrine.
