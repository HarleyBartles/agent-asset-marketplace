# Enforce iterative-review graph so `final-strong` cannot run before `finding-fix`

> **For agentic workers:** REQUIRED SUB-SKILL: Use /subagent-driven-development (recommended) or /executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add hard gates to the `iterative-review` skill so the whole-branch `final-strong` (portable `reviewer-strong` without `<regression_diff_path>`) cannot be invoked until `lens-triage` has completed, every `important`/`blocking` finding has been resolved through `finding-fix` → `reviewer-fixes`, and `review-metrics.json` shows an empty `regressions` list.

**Architecture:** Introduce two small mechanical validators in `iterative-review/scripts/` plus a guard at the top of the `reviewer-strong` subagent profile. `resolved_ledger.py` is the evidence gate that writes `review-log-resolved-ledger.md` only when the ledger is clean. `next_node.py` is the routing validator the orchestrator calls before every `run_subagent` dispatch. The `reviewer-strong` profile starts with an unconditional `BLOCKED` check so the subagent itself refuses an out-of-order dispatch. Update `iterative-review/SKILL.md` and `review-state-graph.md` to make the new gate part of the canonical graph.

**Tech Stack:** Python 3, the existing `iterative-review/scripts/` CLI convention (`--help` and `--check` must respond; `--apply` for mutating steps), and the existing portable `reviewer-*.md` subagent profile format.

## Global Constraints

- Only edit the `codex-marketplace/plugins/superpowers-plus/skills/` canonical source. Regenerate `.agents/skills/` with `py -3 tools/run.py installed-skills --apply`.
- New scripts must follow the repo's `--help` / `--check` contract used by `repo-standards`.
- The `reviewer-strong` subagent profile must keep its hard contract line (`reviewer-strong: N issue(s)` or `reviewer-strong: clean`); add a new allowed final line `reviewer-strong: blocked` for guard failures.
- All changes must pass `py -3 tools/run.py ci --check` before the PR is flipped to ready.

---

### Task 1: Create `resolved_ledger.py` evidence-gate script

**Files:**
- **Create:** `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/scripts/resolved_ledger.py`
- **Modify:** `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/SKILL.md` (the `resolved-ledger` and `final-strong` sections)
- **Modify:** `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/references/review-state-graph.md` (add the evidence file as an output of `resolved-ledger`)

**Interfaces:**
- **Consumes:** `<review-metrics.json>` path (`--metrics`), optional output ledger path (`--ledger`, default `<scratch_dir>/review-log-resolved-ledger.md`).
- **Produces:** `review-log-resolved-ledger.md` (only when allowed).

```python
#!/usr/bin/env python3
"""resolved_ledger.py — write review-log-resolved-ledger.md only when the fix queue is clean.

Contract:
- --help   prints usage and exits 0
- --check  reports whether the script is in a runnable state and exits 0
- --apply  writes the ledger if and only if the metrics file shows no unresolved
           important/blocking findings and no regressions.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def _load_metrics(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _is_ledger_clean(metrics: dict) -> tuple[bool, str]:
    if not metrics:
        return False, "review-metrics.json not found"
    rounds = metrics.get("rounds_per_finding", [])
    for f in rounds:
        severity = f.get("severity", "")
        resolved = f.get("resolved_at_node")
        if severity in ("blocking", "important") and not resolved:
            return False, f"unresolved {severity} finding: {f.get('finding_id')}"
    regressions = metrics.get("regressions", [])
    if regressions:
        return False, f"{len(regressions)} unresolved regression(s)"
    return True, "ledger clean"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Produce the resolved-ledger evidence file for iterative-review."
    )
    parser.add_argument("--check", action="store_true", help="self-check; exits 0 if ready")
    parser.add_argument("--apply", action="store_true", help="write the ledger if allowed")
    parser.add_argument("--metrics", required=True, help="path to review-metrics.json")
    parser.add_argument("--ledger", help="path to review-log-resolved-ledger.md")
    args = parser.parse_args(argv)

    if args.check:
        print("resolved_ledger.py is ready")
        return 0

    metrics_path = Path(args.metrics)
    if not args.ledger:
        ledger_path = metrics_path.parent / "review-log-resolved-ledger.md"
    else:
        ledger_path = Path(args.ledger)

    metrics = _load_metrics(metrics_path)
    clean, reason = _is_ledger_clean(metrics)

    if not clean:
        print(f"BLOCKED: {reason}", file=sys.stderr)
        return 1

    if not args.apply:
        print("resolved-ledger allowed")
        return 0

    pr = metrics.get("pr", {})
    lines = [
        "# Resolved ledger",
        "",
        f"- branch: {pr.get('branch', '<unknown>')}",
        f"- base: {pr.get('base', '<unknown>')}",
        f"- head_sha: {pr.get('head_sha', '<unknown>')}",
        "",
        "All `blocking` and `important` findings recorded in `review-metrics.json` have a `resolved_at_node`.",
        f"Total findings: {len(metrics.get('rounds_per_finding', []))}",
        f"Unresolved important/blocking: 0",
        f"Regressions: {len(metrics.get('regressions', []))}",
        "",
        "resolved-ledger: ready for final-strong",
    ]
    ledger_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {ledger_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

**Steps:**
1. [ ] Create `resolved_ledger.py` in the source path above.
2. [ ] Make it executable or ensure `repo-standards` sees it as a helper script (it is a `.py` in `scripts/`).
3. [ ] Run `py -3 resolved_ledger.py --help` and `py -3 resolved_ledger.py --check` from the source scripts dir; both should exit 0.
4. [ ] Update `SKILL.md` `resolved-ledger` section to say:
   > "When the queue is empty, run `py -3 .agents/skills/iterative-review/scripts/resolved_ledger.py --apply --metrics <scratch_dir>/review-metrics.json`. This writes `review-log-resolved-ledger.md` only when every `important`/`blocking` finding has a `resolved_at_node` and `regressions` is empty. If the command exits 1, do not proceed to `final-strong` and return to `finding-fix` or `regression-scan`."
5. [ ] Update `SKILL.md` `final-strong` section to list `review-log-resolved-ledger.md` as a required input.
6. [ ] Update `review-state-graph.md` `resolved-ledger` node row to add: "Produces `review-log-resolved-ledger.md` evidence file."
7. [ ] Commit: `git add ...; git commit -m "Add resolved_ledger.py evidence gate"`.

---

### Task 2: Create `next_node.py` routing validator

**Files:**
- **Create:** `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/scripts/next_node.py`
- **Modify:** `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/SKILL.md` (add a `next-node` subsection under `Following the graph` and require it before `run_subagent`)

**Interfaces:**
- **Consumes:** `--metrics <path>`, optional `--propose <node>`, optional `--ledger <path>`.
- **Produces:** stdout with the allowed next node (default) or an exit 0/1 validation of a proposed node.

```python
#!/usr/bin/env python3
"""next_node.py — mechanical next-node validator for the iterative-review graph.

Contract:
- --help                  prints usage
- --check                 self-check; exits 0
- --metrics <path>        path to review-metrics.json
- --ledger <path>         path to review-log-resolved-ledger.md (default: <metrics-parent>/review-log-resolved-ledger.md)
- --propose <node>        if given, exits 0 only if <node> is the allowed next node

The orchestrator must call this before every run_subagent dispatch and must not
proceed if it exits 1.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def _load_metrics(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _unresolved_severities(metrics: dict) -> list[str]:
    rounds = metrics.get("rounds_per_finding", [])
    return [f.get("finding_id", "?") for f in rounds if f.get("severity") in ("blocking", "important") and not f.get("resolved_at_node")]


def _next_node(metrics: dict, ledger: Path) -> tuple[str, str]:
    if not metrics:
        return "setup", "no review-metrics.json yet"
    unresolved = _unresolved_severities(metrics)
    regressions = metrics.get("regressions", [])
    if unresolved:
        return "finding-fix", f"unresolved important/blocking: {', '.join(unresolved)}"
    if regressions:
        return "regression-scan", f"{len(regressions)} unresolved regression(s)"
    if not ledger.exists():
        return "resolved-ledger", "resolved-ledger evidence file is missing"
    return "final-strong", "all important findings resolved and ledger evidence present"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Return or validate the allowed next node for iterative-review."
    )
    parser.add_argument("--check", action="store_true", help="self-check; exits 0 if ready")
    parser.add_argument("--metrics", required=True, help="path to review-metrics.json")
    parser.add_argument("--ledger", help="path to review-log-resolved-ledger.md")
    parser.add_argument("--propose", help="proposed next node to validate")
    args = parser.parse_args(argv)

    if args.check:
        print("next_node.py is ready")
        return 0

    metrics_path = Path(args.metrics)
    ledger_path = Path(args.ledger) if args.ledger else metrics_path.parent / "review-log-resolved-ledger.md"
    metrics = _load_metrics(metrics_path)
    node, reason = _next_node(metrics, ledger_path)

    if not args.propose:
        print(f"{node}\n# {reason}")
        return 0

    if args.propose == node:
        print(f"ALLOWED: {args.propose} — {reason}")
        return 0

    print(f"BLOCKED: proposed {args.propose}; allowed next node is {node} — {reason}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
```

**Steps:**
1. [ ] Create `next_node.py` in the source path above.
2. [ ] Verify `py -3 next_node.py --help` and `py -3 next_node.py --check` exit 0.
3. [ ] Update `SKILL.md` to add a `next-node` subsection:
   > "Before each `run_subagent` call, run `py -3 .agents/skills/iterative-review/scripts/next_node.py --propose <node> --metrics <scratch_dir>/review-metrics.json`. If it exits 1, the orchestrator must not dispatch the subagent and must route to the allowed node instead. If it exits 0, dispatch is allowed."
4. [ ] Commit.

---

### Task 3: Add the `reviewer-strong` unconditional guard

**Files:**
- **Modify:** `codex-marketplace/plugins/superpowers-plus/skills/selecting-a-subagent/assets/reviewer-strong.md`

**Interfaces:**
- **Consumes:** existing inputs plus `<review-log-resolved-ledger.md>` (required for `final-strong`) and `<review-metrics.json>` (required for `final-strong`).
- **Produces:** `reviewer-strong: blocked` (new allowed final line) plus a `BLOCKED: ...` report at `<log_path>` when the guard trips.

**Changes:**
1. [ ] After the frontmatter, add a new top section before `## Checklist`:
   ```markdown
   ## Precondition — `final-strong` is only lawful when the ledger is clean

   Read this section before any other inputs.

   This profile is used for two purposes:
   - `regression-scan`: when `<regression_diff_path>` is provided, this is a touched-area re-check.
   - `final-strong`: when `<regression_diff_path>` is *not* provided, this is the whole-branch final review.

   When `<regression_diff_path>` is *not* provided, perform these checks in order. If any check fails, use the `write` tool to write `<log_path>` with the exact single line `BLOCKED: <reason>` and respond with the single line `reviewer-strong: blocked`. Do not read `<diff_path>`, do not produce a normal report, and do not output any other text.

   1. `<review-log-resolved-ledger.md>` must be a readable file. If it is missing, write `BLOCKED: missing review-log-resolved-ledger.md; run resolved-ledger before final-strong`.
   2. `<review-metrics.json>` must be a readable file. If it is missing, write `BLOCKED: missing review-metrics.json`.
   3. No `rounds_per_finding` entry may have `severity` of `blocking` or `important` and an empty/absent `resolved_at_node`.
   4. The `regressions` array must be empty.

   Only if all four pass, proceed to `## Checklist`.
   ```
2. [ ] In `## Inputs`, add:
   ```markdown
   - `<review-log-resolved-ledger.md>` (required for `final-strong`): evidence that all `important`/`blocking` findings are resolved and `regressions` is empty. Produced by `resolved_ledger.py --apply`.
   - `<review-metrics.json>` (required for `final-strong`): the review ledger; used to verify no unresolved `important`/`blocking` findings or regressions remain.
   ```
3. [ ] In the `## Final response (hard contract)` section, expand the allowed lines to include:
   > `reviewer-strong: blocked` — allowed only when the `## Precondition` block has already been violated and the report has been written with `BLOCKED: ...`.
4. [ ] Commit.

---

### Task 4: Update `iterative-review/SKILL.md` orchestrator instructions

**Files:**
- **Modify:** `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/SKILL.md`

**Changes:**
1. [ ] In `## Required reading`, add `references/review-log-resolved-ledger.md` (create a minimal template reference; see Task 5).
2. [ ] In the `### setup` section, add:
   > "After creating the off-repo workspace, the orchestrator must keep `review-metrics.json` current at every `metrics-track`, `resolved-ledger`, and `blocked` node. This file is the single source of truth for `next_node.py` and `resolved_ledger.py`."
3. [ ] In the `### resolved-ledger` section (already updated in Task 1), add the explicit `resolved_ledger.py` command.
4. [ ] In the `### final-strong` section, require the orchestrator to call `next_node.py --propose final-strong` immediately before `run_subagent` for `reviewer-strong`, and require passing `review-log-resolved-ledger.md` and `review-metrics.json` as inputs to the subagent.
5. [ ] In the `### blocked` section, add:
   > "If `next_node.py` or `resolved_ledger.py` returns a `BLOCKED` result, treat the result as a graph error: do not override it, do not dispatch `final-strong`, and do not claim the review is complete. Resume from the allowed node."
6. [ ] Commit.

---

### Task 5: Update graph reference and add resolved-ledger template

**Files:**
- **Create:** `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/references/review-log-resolved-ledger.md`
- **Modify:** `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/references/review-state-graph.md`
- **Modify:** `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/references/review-metrics-schema.json` (only if `resolved-ledger` needs a tracking field)

**Changes:**
1. [ ] Create `review-log-resolved-ledger.md` reference template:
   ```markdown
   # Resolved ledger

   - branch: `<branch>`
   - base: `<base>`
   - head_sha: `<head_sha>`

   All `blocking` and `important` findings recorded in `review-metrics.json` have a `resolved_at_node`.
   Total findings: `<count>`
   Unresolved important/blocking: 0
   Regressions: 0

   resolved-ledger: ready for final-strong
   ```
2. [ ] In `review-state-graph.md`, update the `resolved-ledger` node row to include: "Produces `review-log-resolved-ledger.md` as the evidence file required by `final-strong`."
3. [ ] Optionally add `resolved-ledger` to the `findings_by_node` enum in `review-metrics-schema.json` if the schema is updated to record this node; otherwise leave the schema as-is and use the existing `resolved_at_node` field.
4. [ ] Commit.

---

### Task 6: Regenerate installed skills, run CI, and publish

**Files:**
- **Modify:** `.agents/skills/` (regenerated by `tools/run.py`)
- **Modify:** `.agents/skills/.provenance.json`

**Steps:**
1. [ ] Run `py -3 tools/run.py installed-skills --apply` in the worktree.
2. [ ] Run `py -3 tools/run.py ci --check` and expect it to pass.
3. [ ] Run `git status` and confirm only the expected source and `.agents/skills/` surfaces changed.
4. [ ] Commit with the conventional format:
   ```bash
   git add -A
   git commit -m "Enforce iterative-review graph before final-strong

   - Add resolved_ledger.py to produce review-log-resolved-ledger.md
   - Add next_node.py to validate the allowed next node before dispatch
   - Add unconditional guard at the top of reviewer-strong.md
   - Update SKILL.md and review-state-graph.md for the new gates

   Generated with [Devin](https://devin.ai)

   Co-Authored-By: Devin <158243242+devin-ai-integration[bot]@users.noreply.github.com>"
   ```
5. [ ] Push to `origin feat/enforce-iterative-review-graph`.
6. [ ] Open a draft PR with `gh pr create --draft`.
7. [ ] Run `py -3 .agents/skills/selecting-a-subagent/scripts/install_profiles.py --apply` to refresh the user-global `reviewer-strong.md` for local dogfooding.
8. [ ] Run the new `iterative-review` skill against the new PR or a test PR to verify the guard blocks `final-strong` when `review-log-resolved-ledger.md` is missing.

---

## Spec coverage check

| Brief requirement | Task |
|---|---|
| `final-strong` cannot be invoked before `lens-triage` is complete | Task 1 (resolved-ledger evidence), Task 2 (next_node), Task 3 (reviewer-strong guard) |
| `final-strong` cannot run while any `important`/`blocking` finding is unresolved | Task 1, Task 2, Task 3 |
| `final-strong` cannot run while `regressions` is non-empty | Task 1, Task 2, Task 3 |
| The orchestrator has a clear, mechanical way to know which node is next | Task 2 (`next_node.py`) |
| The fix is published to the asset marketplace and refreshes into `Rooms-Mostly` | Task 6 (commit, push, draft PR; marketplace pack source is in `superpowers-plus`) |

## Placeholder scan

No `TBD`, `TODO`, `implement later`, or references to undefined types. All proposed filenames, function names, and CLI flags are explicitly named.
