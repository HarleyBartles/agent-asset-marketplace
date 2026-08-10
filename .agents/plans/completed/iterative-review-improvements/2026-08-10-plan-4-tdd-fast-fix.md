# Plan 4 - TDD and fast-fix churn reduction

> **For agentic workers:** REQUIRED SUB-SKILL: Use /subagent-driven-development (recommended) or /executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Reduce fast-fix churn by making `test-driven-development` the default discipline for implementer subagents and orchestrators, tightening the `finding-fix`/`reviewer-fixes` re-check loop so fixes are proven by failing tests and only the originating lens is re-run.

**Architecture:** Update the canonical `implementer` and `implementer-strong` subagent profiles and the `subagent-driven-development` implementer prompt to require RED/GREEN/REFACTOR evidence for any blocking/important finding. Add a TDD step to the `node-finding-fix.md` and `node-fast-fix.md` recipes. Add `findings_discovered_at_fix_nodes` and `regressions_introduced` to `review-metrics-schema.json` and `compile_metrics.py` so the review report can track churn. Keep all canonical edits in `codex-marketplace/plugins/superpowers-plus/skills/` and regenerate `.agents/skills/` with `py -3 tools/run.py installed-skills --apply`.

**Tech Stack:** Python 3, JSON/JSONL, Markdown profiles and prompts, `py -3 tools/run.py ci --check`.

## Global Constraints

- Only edit canonical source in `codex-marketplace/plugins/superpowers-plus/skills/`; regenerate `.agents/skills/` with `py -3 tools/run.py installed-skills --apply`.
- Every changed or new script must satisfy `--help` and `--check`.
- `py -3 tools/run.py ci --check` must pass before claiming any task complete.
- Work in the `2026-08-10-iterative-review-tdd` worktree; do not commit to `main` directly.
- Do not change graph topology (nodes/edges).
- Plans, specs, and roadmaps are source artifacts; commit them to the branch before implementation begins.

---

### Task 0: Update the roadmap and mark the plan in-flight

**Files:**
- Read: `.agents/plans/iterative-review-improvements/roadmap.md`
- Modify: `.agents/plans/iterative-review-improvements/roadmap.md`
- Modify: `../../../specs/2026-08-10-iterative-review-tdd-proposal.md` (status)
- Test: `py -3 tools/run.py ci --check`

**Interfaces:**
- Plan 3 status becomes `done`; Plan 4 row shows `in_progress` and links to this plan.
- The spec proposal status becomes `in-flight`.

- [x] **Step 1: Open the roadmap and update Plan 3 and Plan 4 rows**

Update the roadmap table to:

```markdown
| 3 | Lens dispatch, write-safety, and final polish | done | [Plan 3](../completed/iterative-review-improvements/2026-08-09-plan-3-lens-dispatch-and-polish.md) | df9a41b8 | #289 | 9/10 | `select_lenses.py`, self-review template, tests, docs, plus a no-hand-write contract for all scratch files (`review-state.json`, `*.jsonl`, `review-log-*.md`) and a script for orchestrator markdown logs |
| 4 | TDD and fast-fix churn reduction | in_progress | [Plan 4](2026-08-10-plan-4-tdd-fast-fix.md) | — | — | — | Enforce `test-driven-development` for implementers and orchestrators, add TDD to implementer profiles and subagent-driven-development prompts, and tighten the `finding-fix`/`reviewer-fixes`/`fast-fix` node recipes so fixes are proven by failing tests and re-run only the originating lens, not a full final branch review. |
```

- [x] **Step 2: Update the spec status**

In `../../../specs/2026-08-10-iterative-review-tdd-proposal.md`, change the status paragraph to:

```markdown
**Status:** In-flight for Plan 4 implementation.
**Source:** Design discussion after Plan 3 final branch review of PR #289.
```

- [x] **Step 3: Run CI**

```bash
py -3 tools/run.py ci --check
```

Expected: all targets pass.

- [x] **Step 4: Commit the plan and roadmap update**

```bash
git add .agents/plans/iterative-review-improvements/roadmap.md ../../../specs/2026-08-10-iterative-review-tdd-proposal.md .agents/plans/iterative-review-improvements/2026-08-10-plan-4-tdd-fast-fix.md
git commit -m "docs(plans): start Plan 4 - TDD and fast-fix churn reduction"
```

---

### Task 1: Require TDD evidence in implementer profiles and subagent prompt

**Files:**
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/selecting-a-subagent/assets/implementer.md`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/selecting-a-subagent/assets/implementer-strong.md`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/subagent-driven-development/implementer-prompt.md`
- Test: `py -3 tools/run.py ci --check`

**Interfaces:**
- `implementer.md` and `implementer-strong.md` now contain a `## Test-Driven Development` section.
- `implementer-prompt.md` instructs the subagent to report RED/GREEN commands and output for any blocking/important finding.
- The final `review-log-implementer-report.md` must include a `## TDD Evidence` section.

- [x] **Step 1: Append a TDD section to `implementer.md` and `implementer-strong.md`**

Insert after the `## What not to do` section in each file:

```markdown

## Test-Driven Development

For any blocking or important finding, or when the task is a non-trivial bug fix, follow RED/GREEN/REFACTOR:

1. RED - Before changing source code, write or identify a failing test that reproduces the issue.
   - Run it and capture the failing output. Confirm the failure is the one you expect.
2. GREEN - Write the minimal change that makes the test pass.
   - Run the same test and the consumer's focused test suite. Confirm it passes.
3. REFACTOR - Clean up the implementation while keeping the test green.

For trivial one-liners, documentation-only changes, or pure configuration, a failing test is not required, but the existing test suite must still pass before reporting DONE.

## TDD evidence format

When `test-driven-development` is required, end `review-log-implementer-report.md` with a `## TDD Evidence` section containing:

- RED command and the relevant failing output.
- GREEN command and the relevant passing output.
- The test file path and the production file path changed.
```

- [x] **Step 2: Update `implementer-prompt.md` to require TDD evidence for blocking/important work**

In the `## Your Job` block, insert the TDD step before the Commit step and renumber Commit/Self-review/Report to 5/6/7:

```markdown
4. If the task is a blocking/important bug fix or non-trivial behavior change, follow `test-driven-development`:
   - RED: write or identify a failing test that reproduces the bug and run it. Capture the failing output in `review-log-implementer-report.md`.
   - GREEN: implement the minimal fix, run the same test until it passes.
   - REFACTOR: clean up only after green. Do not add behavior.
5. Commit your work once the targeted tests and the consumer's preflight pass.
```

In the `## Report Format` block, expand the TDD evidence bullet to:

```markdown
- **TDD Evidence** (required when `test-driven-development` was used, otherwise note "not required"):
  - RED: command, failing output, and why the failure was expected
  - GREEN: command, passing output, and the minimal change that made it pass
  - The test file path and the production file path changed
```

- [x] **Step 3: Run CI**

```bash
py -3 tools/run.py ci --check
```

Expected: all targets pass.

- [x] **Step 4: Commit**

```bash
git add codex-marketplace/plugins/superpowers-plus/skills/selecting-a-subagent/assets/implementer.md codex-marketplace/plugins/superpowers-plus/skills/selecting-a-subagent/assets/implementer-strong.md codex-marketplace/plugins/superpowers-plus/skills/subagent-driven-development/implementer-prompt.md
git commit -m "feat(selecting-a-subagent,subagent-driven-development): mandate TDD evidence in implementer profiles and prompts"
```

---

### Task 2: Add TDD to `finding-fix` and `fast-fix` recipes

**Files:**
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/references/node-finding-fix.md`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/references/node-fast-fix.md`
- Test: `py -3 tools/run.py ci --check`

**Interfaces:**
- `node-finding-fix.md` requires the implementer/orchestrator to produce RED/GREEN evidence before recording a resolution.
- `node-fast-fix.md` requires the preflight command to pass and a failing-then-passing test for the top finding, if one exists in the preflight output.

- [x] **Step 1: Insert TDD requirements into `node-finding-fix.md` before step 5**

Add a new step 4.5 after the fix is applied and before step 5:

```markdown
4.5. If the finding severity is `blocking` or `important`, or if `non_trivial_fix` is `true`, the fix must be proven with a failing-then-passing test:
   - **RED:** Create or identify a test that reproduces the bug. Run it and capture the failing output in the implementer report or inline log.
   - **GREEN:** Apply the minimal fix. Re-run the same test until it passes.
   - The test must be added or updated in the permanent test suite. `compile_metrics.py` and the consumer's preflight must pass.
   - For inline/orchestrator fixes, record the RED/GREEN commands and output in `review-log-finding-fix.md`.
```

Then renumber the existing step 5 onwards to 6, etc.

- [x] **Step 2: Update `node-fast-fix.md` to require a reproducer for the top finding**

Replace the recipe section with:

```markdown
## Recipe
1. Read the deterministic findings from `<scan_findings>`.
2. Choose the cheapest fix for the top finding.
3. If the top finding has an existing test, run that test and confirm it fails (RED). If there is no test, write the minimal test that reproduces the finding.
4. Apply the minimal fix and re-run the test until it passes (GREEN).
5. Return to `preflight` to re-run the consumer's canonical preflight.
```

- [x] **Step 3: Run CI**

```bash
py -3 tools/run.py ci --check
```

Expected: all targets pass.

- [x] **Step 4: Commit**

```bash
git add codex-marketplace/plugins/superpowers-plus/skills/iterative-review/references/node-finding-fix.md codex-marketplace/plugins/superpowers-plus/skills/iterative-review/references/node-fast-fix.md
git commit -m "docs(iterative-review): require TDD evidence in finding-fix and fast-fix recipes"
```

---

### Task 3: Add `findings_discovered_at_fix_nodes` and `regressions_introduced` to review metrics

**Files:**
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/scripts/compile_metrics.py`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/references/review-metrics-schema.json`
- Create: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/tests/test_compile_metrics.py`
- Test: `py -3 -m pytest codex-marketplace/plugins/superpowers-plus/skills/iterative-review/tests/test_compile_metrics.py -q`
- Test: `py -3 tools/run.py ci --check`

**Interfaces:**
- `compile_metrics.py` returns `findings_discovered_at_fix_nodes` (count of findings whose first discovery node is `finding-fix` or `fast-fix`) and `regressions_introduced` (count of `regressions` items).
- `review-metrics-schema.json` declares both fields as `integer` with `minimum: 0`.

- [x] **Step 1: Update `_compile` in `compile_metrics.py` to compute the new fields**

Add the two computed values to the returned metrics dict. After `total_rounds`:

```python
    fix_nodes = {"finding-fix", "fast-fix"}
    findings_discovered_at_fix_nodes = sum(
        1 for f in findings if f.get("discovered_at_node") in {"finding-fix", "fast-fix"}
    )
    regressions_introduced = len(regressions)

    return {
        "pr": state.get("pr", {}),
        "findings_by_node": findings_by_node,
        "rounds_per_finding": rounds_per_finding,
        "regressions": regressions,
        "current_node": state.get("current_node"),
        "previous_node": state.get("previous_node"),
        "non_trivial_fix": state.get("non_trivial_fix", False),
        "total_rounds": total_rounds,
        "findings_discovered_at_fix_nodes": findings_discovered_at_fix_nodes,
        "regressions_introduced": regressions_introduced,
    }
```

- [x] **Step 2: Add the schema properties**

In `review-metrics-schema.json`, after `devin_auto_review_invocations` (the current last property), add:

```json
    "findings_discovered_at_fix_nodes": {"type": "integer", "minimum": 0},
    "regressions_introduced": {"type": "integer", "minimum": 0},
```

- [x] **Step 3: Write a failing test for `compile_metrics.py`**

Create `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/tests/test_compile_metrics.py`:

```python
#!/usr/bin/env python3
"""Tests for compile_metrics.py."""

import importlib.util
import json
import tempfile
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
COMPILE_METRICS = SKILL_DIR / "scripts" / "compile_metrics.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("compile_metrics", COMPILE_METRICS)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_compile_metrics_includes_churn_fields():
    module = _load_module()
    state = {
        "pr": {"branch": "test", "base": "main", "head_sha": "abc"},
        "current_node": "resolved-ledger",
        "previous_node": "regression-scan",
        "round": 3,
        "non_trivial_fix": True,
    }
    with tempfile.TemporaryDirectory() as td:
        scratch = Path(td)
        (scratch / "findings.jsonl").write_text(
            "{\"finding_id\": \"f-1\", \"lens\": \"security\", \"discovered_at_node\": \"finding-fix\", \"discovered_at_round\": 2, \"severity\": \"important\"}\n",
            encoding="utf-8",
        )
        (scratch / "resolutions.jsonl").write_text(
            "{\"finding_id\": \"f-1\", \"resolved_at_node\": \"reviewer-fixes\", \"resolved_at_round\": 3}\n",
            encoding="utf-8",
        )
        (scratch / "regressions.jsonl").write_text(
            "{\"fix_for\": \"f-1\", \"new_finding\": \"f-2\", \"discovered_at_node\": \"reviewer-fixes\", \"discovered_at_round\": 3, \"regression_class\": \"same-lens-blast-radius\", \"severity\": \"important\"}\n",
            encoding="utf-8",
        )
        (scratch / "blockers.jsonl").write_text("", encoding="utf-8")
        state["scratch_dir"] = str(scratch)

        logs = {
            "findings": module._load_jsonl(scratch / "findings.jsonl"),
            "resolutions": module._load_jsonl(scratch / "resolutions.jsonl"),
            "regressions": module._load_jsonl(scratch / "regressions.jsonl"),
            "blockers": module._load_jsonl(scratch / "blockers.jsonl"),
        }
        metrics = module._compile(state, logs)

        assert metrics["findings_discovered_at_fix_nodes"] == 1
        assert metrics["regressions_introduced"] == 1
        assert metrics["non_trivial_fix"] is True


def test_compile_metrics_cli_writes_metrics_with_churn_fields():
    module = _load_module()
    with tempfile.TemporaryDirectory() as td:
        scratch = Path(td)
        state_path = scratch / "review-state.json"
        metrics_path = scratch / "review-metrics.json"
        state = {
            "pr": {"branch": "test", "base": "main", "head_sha": "abc"},
            "current_node": "resolved-ledger",
            "previous_node": "regression-scan",
            "round": 1,
            "non_trivial_fix": False,
            "scratch_dir": str(scratch),
        }
        state_path.write_text(json.dumps(state), encoding="utf-8")
        (scratch / "findings.jsonl").write_text("", encoding="utf-8")
        (scratch / "resolutions.jsonl").write_text("", encoding="utf-8")
        (scratch / "regressions.jsonl").write_text("", encoding="utf-8")
        (scratch / "blockers.jsonl").write_text("", encoding="utf-8")
        rc = module._main(["--state", str(state_path), "--metrics", str(metrics_path)])
        assert rc == 0
        written = json.loads(metrics_path.read_text(encoding="utf-8"))
        assert "findings_discovered_at_fix_nodes" in written
        assert "regressions_introduced" in written
        assert written["findings_discovered_at_fix_nodes"] == 0
        assert written["regressions_introduced"] == 0
```

- [x] **Step 4: Run the focused tests and expect failure (RED)**

```bash
py -3 -m pytest codex-marketplace/plugins/superpowers-plus/skills/iterative-review/tests/test_compile_metrics.py -q
```

Expected: tests fail because the new fields are not yet in `compile_metrics.py`.

- [x] **Step 5: Implement the metric changes in `compile_metrics.py` and the schema**

Make the code and schema changes shown in Step 1 and Step 2.

- [x] **Step 6: Run the focused tests and expect pass (GREEN)**

```bash
py -3 -m pytest codex-marketplace/plugins/superpowers-plus/skills/iterative-review/tests/test_compile_metrics.py -q
```

Expected: 2 passed.

- [x] **Step 7: Run full CI**

```bash
py -3 tools/run.py ci --check
```

Expected: all targets pass.

- [x] **Step 8: Commit**

```bash
git add codex-marketplace/plugins/superpowers-plus/skills/iterative-review/scripts/compile_metrics.py codex-marketplace/plugins/superpowers-plus/skills/iterative-review/references/review-metrics-schema.json codex-marketplace/plugins/superpowers-plus/skills/iterative-review/tests/test_compile_metrics.py
git commit -m "feat(iterative-review): track findings_discovered_at_fix_nodes and regressions_introduced in review metrics"
```

---

### Task 4: Regenerate installed skills and final CI

**Files:**
- All canonical skill source in `codex-marketplace/plugins/superpowers-plus/skills/`
- Generated: `.agents/skills/`
- Test: `py -3 tools/run.py ci --check`

**Interfaces:**
- `.agents/skills/` mirrors the canonical source.
- Marketplace indexes are current.

- [x] **Step 1: Regenerate installed skills and indexes**

```bash
py -3 tools/run.py installed-skills --apply
py -3 tools/run.py marketplace --apply
py -3 tools/run.py ci --check
```

Expected: all targets pass.

- [x] **Step 2: Stage and commit the regenerated copies**

```bash
git add -A
git commit -m "chore: regenerate installed skills and marketplace for Plan 4 TDD changes"
```

- [x] **Step 3: Push the branch and open a draft PR**

```bash
git push origin 2026-08-10-iterative-review-tdd
gh pr create --draft --title "Plan 4: TDD and fast-fix churn reduction" --body "See .agents/plans/iterative-review-improvements/2026-08-10-plan-4-tdd-fast-fix.md"
```

Report the PR URL.

---

### Task 5: Mark the spec as implemented

**Files:**
- Read: `../../../specs/2026-08-10-iterative-review-tdd-proposal.md`
- Modify: `../../../specs/2026-08-10-iterative-review-tdd-proposal.md`

**Interfaces:**
- The spec proposal status reflects that the work is complete and points to this plan and PR #290.

- [x] **Step 1: Update the spec status paragraph**

```markdown
**Status:** Implemented in Plan 4 / PR #290.
**Source:** Design discussion after Plan 3 final branch review of PR #289.
```

- [x] **Step 2: Commit the spec status update**

```bash
git add ../../../specs/2026-08-10-iterative-review-tdd-proposal.md
git commit -m "docs(spec): mark iterative-review TDD proposal as implemented in Plan 4"
```
