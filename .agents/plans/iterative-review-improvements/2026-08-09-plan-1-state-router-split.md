# Plan 1 — State/router split and record scripts

> **For agentic workers:** REQUIRED SUB-SKILL: Use /subagent-driven-development (recommended) or /executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Split `iterative-review` so that `review-state.json` is the only router state and `review-metrics.json` is a generated evidence aggregate. Add the record scripts and `compile_metrics.py`, refactor `next_node.py`, and remove all hand-editing of `review-metrics.json` from the node recipes.

**Architecture:** The source of truth for routing moves from `review-metrics.json` to `review-state.json` plus an append-only log (`findings.jsonl`, `resolutions.jsonl`, `regressions.jsonl`, `blockers.jsonl`) in the off-repo scratch. `next_node.py` reads `review-state.json` and the logs. `compile_metrics.py` reads the same inputs and writes `review-metrics.json`. Node recipes call `record_*.py` instead of editing JSON.

**Tech Stack:** Python 3, the existing `iterative-review/scripts/` CLI contract (`--help`, `--check`, `--apply`), JSON/JSONL, and `tools/run.py` for CI and installed-skills regeneration.

## Global Constraints

- Only edit the canonical source in `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/`; regenerate `.agents/skills/iterative-review/` with `py -3 tools/run.py installed-skills --apply`.
- Every new script must satisfy the repo's `--help` / `--check` contract.
- `py -3 tools/run.py ci --check` must pass before claiming any task complete.
- Work in the `iterative-review-improvements` worktree; do not commit to `main` directly.
- Keep the graph topology unchanged; only the state and metrics surfaces change.

---

### Task 0: Create `review-state-schema.json`

**Files:**
- Create: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/references/review-state-schema.json`
- Test: `py -3 tools/run.py ci --check`

**Interfaces:**
- Produces: the JSON schema for `review-state.json`.

- [ ] **Step 1: Write the schema**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Iterative review router state",
  "description": "Canonical router state for the iterative-review skill. Written only by next_node.py --propose or setup.",
  "type": "object",
  "required": ["pr", "current_node", "previous_node", "round", "max_fix_rounds"],
  "properties": {
    "pr": {
      "type": "object",
      "required": ["branch", "base", "head_sha"],
      "properties": {
        "branch": {"type": "string"},
        "base": {"type": "string"},
        "head_sha": {"type": "string"},
        "pr_number": {"type": ["string", "integer"]}
      }
    },
    "current_node": {"type": "string"},
    "previous_node": {"type": "string"},
    "round": {"type": "integer", "minimum": 1},
    "max_fix_rounds": {"type": "integer", "minimum": 1},
    "non_trivial_fix": {"type": "boolean"},
    "contested": {"type": "boolean"},
    "blocked_class": {"type": "string", "enum": ["contested", "tool-blocked"]},
    "scratch_dir": {"type": "string"},
    "ledger_path": {"type": "string"}
  }
}
```

- [ ] **Step 2: Run CI**

```bash
py -3 tools/run.py ci --check
```

Expected: all targets pass.

- [ ] **Step 3: Commit**

```bash
git add codex-marketplace/plugins/superpowers-plus/skills/iterative-review/references/review-state-schema.json
git commit -m "feat(iterative-review): add review-state schema"
```

---

### Task 1: Create `record_finding.py`

**Files:**
- Create: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/scripts/record_finding.py`
- Test: `py -3 -c` and `py -3 tools/run.py ci --check`

**Interfaces:**
- Consumes: `review-state.json` path and a JSON finding object.
- Produces: an append-only `findings.jsonl` event.

- [ ] **Step 1: Write the script**

```python
#!/usr/bin/env python3
"""record_finding.py — append a finding event to the review log. (mixed)"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REQUIRED = {"finding_id", "lens", "discovered_at_node", "discovered_at_round", "severity"}


def _load_state(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Record a new iterative-review finding. (mixed)"
    )
    parser.add_argument("--check", action="store_true", help="self-check; exits 0 if ready")
    parser.add_argument("--state", required=True, help="path to review-state.json")
    parser.add_argument("--data", required=True, help="JSON finding object")
    args = parser.parse_args(argv)

    if args.check:
        print("record_finding.py is ready")
        return 0

    state_path = Path(args.state)
    state = _load_state(state_path)
    finding = json.loads(args.data)

    missing = REQUIRED - finding.keys()
    if missing:
        print(f"ERROR: missing keys {missing}", file=sys.stderr)
        return 1

    scratch = Path(state["scratch_dir"])
    log = scratch / "findings.jsonl"
    log.parent.mkdir(parents=True, exist_ok=True)

    existing = set()
    if log.exists():
        for line in log.read_text(encoding="utf-8").splitlines():
            if line.strip():
                existing.add(json.loads(line).get("finding_id"))

    if finding["finding_id"] in existing:
        print("record_finding.py: finding already recorded; no change")
        return 0

    with log.open("a", encoding="utf-8") as f:
        f.write(json.dumps(finding, ensure_ascii=False) + "\n")

    print(f"record_finding.py: recorded {finding['finding_id']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
```

- [ ] **Step 2: Run a manual idempotency test**

```bash
py -3 codex-marketplace/plugins/superpowers-plus/skills/iterative-review/scripts/record_finding.py --check
```

Expected: `record_finding.py is ready` and exit 0.

- [ ] **Step 3: Commit**

```bash
git add codex-marketplace/plugins/superpowers-plus/skills/iterative-review/scripts/record_finding.py
git commit -m "feat(iterative-review): add record_finding.py"
```

---

### Task 2: Create the remaining record scripts

**Files:**
- Create: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/scripts/record_resolution.py`
- Create: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/scripts/record_regression.py`
- Create: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/scripts/record_blocker.py`
- Test: `py -3 -c` and `py -3 tools/run.py ci --check`

**Interfaces:**
- `record_resolution.py` — `--state <path> --data <json>` with keys `finding_id`, `resolved_at_node`, `resolved_at_round`.
- `record_regression.py` — `--state <path> --data <json>` with keys `fix_for`, `new_finding`, `discovered_at_node`, `discovered_at_round`, `regression_class`, `severity`.
- `record_blocker.py` — `--state <path> --data <json>` with keys `finding_id`, `blocker_class`.

- [ ] **Step 1: Write `record_resolution.py`**

Copy `record_finding.py` and change:
- `REQUIRED = {"finding_id", "resolved_at_node", "resolved_at_round"}`
- log file: `resolutions.jsonl`
- `if finding["finding_id"] in existing:` returns 0 without duplication

- [ ] **Step 2: Write `record_regression.py`**

Copy `record_finding.py` and change:
- `REQUIRED = {"fix_for", "new_finding", "discovered_at_node", "discovered_at_round", "regression_class", "severity"}`
- log file: `regressions.jsonl`
- `new_finding` uniqueness check instead of `finding_id`

- [ ] **Step 3: Write `record_blocker.py`**

Copy `record_finding.py` and change:
- `REQUIRED = {"finding_id", "blocker_class"}`
- log file: `blockers.jsonl`
- `blocker_class` enum: `{"contested", "tool-blocked"}`

- [ ] **Step 4: Run `--check` on each**

```bash
py -3 .../scripts/record_resolution.py --check
py -3 .../scripts/record_regression.py --check
py -3 .../scripts/record_blocker.py --check
```

Expected: each prints ready and exits 0.

- [ ] **Step 5: Commit**

```bash
git add codex-marketplace/plugins/superpowers-plus/skills/iterative-review/scripts/record_*.py
git commit -m "feat(iterative-review): add record resolution, regression, and blocker scripts"
```

---

### Task 3: Create `compile_metrics.py`

**Files:**
- Create: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/scripts/compile_metrics.py`
- Test: `py -3 -c` and `py -3 tools/run.py ci --check`

**Interfaces:**
- Consumes: `--state <review-state.json> --metrics <review-metrics.json>`.
- Produces: a `review-metrics.json` aggregate from state and logs.

- [ ] **Step 1: Write the script**

```python
#!/usr/bin/env python3
"""compile_metrics.py — generate review-metrics.json from state and logs. (mixed)"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _compile(state: dict, logs: dict) -> dict:
    findings = logs["findings"]
    resolutions = {r["finding_id"]: r for r in logs["resolutions"]}
    regressions = logs["regressions"]
    blockers = {b["finding_id"]: b for b in logs["blockers"]}

    rounds_per_finding: list[dict] = []
    findings_by_node: dict[str, int] = {}

    for f in findings:
        finding_id = f["finding_id"]
        r = resolutions.get(finding_id)
        b = blockers.get(finding_id)
        entry = {
            "finding_id": finding_id,
            "lens": f["lens"],
            "discovered_at_node": f["discovered_at_node"],
            "discovered_at_round": f["discovered_at_round"],
            "severity": f["severity"],
            "contested": b is not None and b["blocker_class"] == "contested",
        }
        if r:
            entry["resolved_at_node"] = r["resolved_at_node"]
            entry["resolved_at_round"] = r["resolved_at_round"]
        rounds_per_finding.append(entry)
        findings_by_node[f["discovered_at_node"]] = findings_by_node.get(f["discovered_at_node"], 0) + 1

    total_rounds = max(
        (f.get("discovered_at_round", 0) for f in findings),
        default=state.get("round", 1),
    )

    return {
        "pr": state.get("pr", {}),
        "findings_by_node": findings_by_node,
        "rounds_per_finding": rounds_per_finding,
        "regressions": regressions,
        "current_node": state.get("current_node"),
        "previous_node": state.get("previous_node"),
        "non_trivial_fix": state.get("non_trivial_fix", False),
        "total_rounds": total_rounds,
        "total_reviewer_subagent_dispatches": 0,
        "devin_auto_review_invocations": 0,
    }


def _main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Compile review-metrics.json from review-state and logs. (mixed)"
    )
    parser.add_argument("--check", action="store_true", help="self-check; exits 0 if ready")
    parser.add_argument("--state", required=True, help="path to review-state.json")
    parser.add_argument("--metrics", required=True, help="path to review-metrics.json")
    args = parser.parse_args(argv)

    if args.check:
        print("compile_metrics.py is ready")
        return 0

    state_path = Path(args.state)
    state = _load(state_path)
    scratch = Path(state["scratch_dir"])

    logs = {
        "findings": _load_jsonl(scratch / "findings.jsonl"),
        "resolutions": _load_jsonl(scratch / "resolutions.jsonl"),
        "regressions": _load_jsonl(scratch / "regressions.jsonl"),
        "blockers": _load_jsonl(scratch / "blockers.jsonl"),
    }

    metrics = _compile(state, logs)
    metrics_path = Path(args.metrics)
    metrics_path.write_text(json.dumps(metrics, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"compile_metrics.py: wrote {metrics_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
```

- [ ] **Step 2: Run a manual compile test**

Create a temporary scratch with a sample `review-state.json` and logs, then run:

```bash
py -3 codex-marketplace/plugins/superpowers-plus/skills/iterative-review/scripts/compile_metrics.py --state /tmp/review-state.json --metrics /tmp/review-metrics.json
py -3 -c "import json; print(json.load(open('/tmp/review-metrics.json'))['rounds_per_finding'])"
```

Expected: the generated `review-metrics.json` has a `rounds_per_finding` entry matching the input finding.

- [ ] **Step 3: Commit**

```bash
git add codex-marketplace/plugins/superpowers-plus/skills/iterative-review/scripts/compile_metrics.py
git commit -m "feat(iterative-review): add compile_metrics.py"
```

---

### Task 4: Refactor `next_node.py` to use `review-state.json`

**Files:**
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/scripts/next_node.py`
- Test: `py -3 tools/run.py ci --check` and the existing `next_node.py` synthetic walkthrough.

**Interfaces:**
- Consumes: `--state <review-state.json>`; logs from `scratch_dir`.
- Produces: single allowed next node and updated `review-state.json`.

- [ ] **Step 1: Add `--state` argument and `_load_state()`**

Add `--state` to the argument parser and make `--state` required when not using `--check`. Add:

```python
def _load_state(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except (json.JSONDecodeError, OSError):
        return {}
```

- [ ] **Step 2: Add log-driven unresolved checks**

Add helpers to read the JSONL logs:

```python
def _load_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
```

Replace `_unresolved_severities(metrics)` with `_unresolved_findings(state)`:

```python
def _unresolved_findings(state: dict) -> list[str]:
    scratch = Path(state.get("scratch_dir", "."))
    findings = _load_jsonl(scratch / "findings.jsonl")
    resolved = {r["finding_id"] for r in _load_jsonl(scratch / "resolutions.jsonl")}
    return [
        f["finding_id"]
        for f in findings
        if f["finding_id"] not in resolved and f.get("severity") in ("blocking", "important")
    ]
```

Replace the `regressions` and `contested` checks to read from `regressions.jsonl` and `blockers.jsonl`.

- [ ] **Step 3: Update `--propose` to write `review-state.json` instead of `review-metrics.json`**

In `main`, after a successful `--propose`, write the new `review-state.json`:

```python
state["previous_node"] = state.get("current_node", "")
state["current_node"] = node
state_path.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
```

Stop mutating `review-metrics.json` from `next_node.py`. The only persistent file `next_node.py` writes is `review-state.json`.

- [ ] **Step 4: Update the `--metrics` flag behavior**

`--metrics` may still be accepted for backward compatibility, but it becomes a read-only input used only for the fallback `compile_metrics.py` output. The canonical inputs are `--state` and the logs.

- [ ] **Step 5: Run CI**

```bash
py -3 tools/run.py ci --check
```

Expected: all targets pass.

- [ ] **Step 6: Commit**

```bash
git add codex-marketplace/plugins/superpowers-plus/skills/iterative-review/scripts/next_node.py
git commit -m "refactor(iterative-review): next_node.py uses review-state and logs"
```

---

### Task 5: Update `update_review_metrics.py` to be a compile wrapper

**Files:**
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/scripts/update_review_metrics.py`
- Test: `py -3 tools/run.py ci --check`

**Interfaces:**
- `update_review_metrics.py` remains an orchestrator-facing convenience, but now it calls `compile_metrics.py` with `--state` and `--metrics`.

- [ ] **Step 1: Replace the merge logic with `compile_metrics.py` invocation**

Change `main` so that `--apply` runs `compile_metrics.py` as a subprocess instead of merging JSON patches:

```python
import subprocess
import sys

def _compile(state_path: Path, metrics_path: Path) -> int:
    script = Path(__file__).resolve().parent / "compile_metrics.py"
    return subprocess.run(
        [sys.executable, str(script), "--state", str(state_path), "--metrics", str(metrics_path)],
        check=False,
    ).returncode
```

Update `main` so that `--apply --metrics <path>` calls `_compile(state_path, metrics_path)` where `state_path` is `<metrics_dir>/review-state.json` by default.

- [ ] **Step 2: Run CI**

```bash
py -3 tools/run.py ci --check
```

- [ ] **Step 3: Commit**

```bash
git add codex-marketplace/plugins/superpowers-plus/skills/iterative-review/scripts/update_review_metrics.py
git commit -m "refactor(iterative-review): update_review_metrics.py calls compile_metrics.py"
```

---

### Task 6: Update `references/review-metrics-schema.json`

**Files:**
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/references/review-metrics-schema.json`
- Test: `py -3 tools/run.py ci --check`

**Interfaces:**
- Fixes the schema to match the generated output shape.

- [ ] **Step 1: Remove `resolved_at_node` and `resolved_at_round` from required**

Change `rounds_per_finding` items so that `resolved_at_node` and `resolved_at_round` are not in `required`.

- [ ] **Step 2: Add `deferred` to the severity enum**

```json
"severity": {"type": "string", "enum": ["blocking", "important", "minor", "deferred"]}
```

- [ ] **Step 3: Add `regression_of` to `regressions` items**

```json
"regression_of": {"type": "string"}
```

- [ ] **Step 4: Make `total_rounds` optional**

It is generated by `compile_metrics.py` and should not be required on creation.

- [ ] **Step 5: Run CI and commit**

```bash
py -3 tools/run.py ci --check
```

```bash
git add codex-marketplace/plugins/superpowers-plus/skills/iterative-review/references/review-metrics-schema.json
git commit -m "fix(iterative-review): review-metrics schema for generated output"
```

---

### Task 7: Update node recipes to use record scripts

**Files:**
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/references/node-*.md`
- Test: `py -3 tools/run.py ci --check`

**Interfaces:**
- No node recipe edits `review-metrics.json` by hand. Each recipe appends events or calls `compile_metrics.py`.

- [ ] **Step 1: Update `node-lens-triage.md`**

Replace the instruction to append to `rounds_per_finding` in `review-metrics.json` with a `record_finding.py` call per classified finding:

```bash
py -3 .agents/skills/iterative-review/scripts/record_finding.py --state <scratch_dir>/review-state.json --data '<json>'
py -3 .agents/skills/iterative-review/scripts/compile_metrics.py --state <scratch_dir>/review-state.json --metrics <scratch_dir>/review-metrics.json
```

- [ ] **Step 2: Update `node-reviewer-fixes.md`**

On `PASS`, call `record_resolution.py` for the original finding. On `FAIL` with a new same-lens issue, call `record_finding.py` and `record_regression.py`.

- [ ] **Step 3: Update `node-regression-scan.md`**

On a new issue, call `record_finding.py` and `record_regression.py` with the appropriate `regression_class` and `regression_of`.

- [ ] **Step 4: Update `node-metrics-track.md`**

Remove the instruction to hand-edit `review-metrics.json`. It now only documents that `record_*.py` and `compile_metrics.py` produce the metrics file.

- [ ] **Step 5: Update `node-resolved-ledger.md`**

Ensure `resolved_ledger.py` is called after `record_resolution.py` has been used for all resolved findings and `compile_metrics.py` has regenerated `review-metrics.json`.

- [ ] **Step 6: Update `node-blocked.md`**

Use `record_blocker.py` to record the blocker class before routing to `blocked`.

- [ ] **Step 7: Update `node-setup.md`**

Create an empty `review-state.json` alongside the scratch workspace. The sample state should include `current_node: "setup"`, `round: 1`, `max_fix_rounds: 4`, `pr`, and `scratch_dir`.

- [ ] **Step 8: Run CI and commit**

```bash
py -3 tools/run.py ci --check
```

```bash
git add -A
git commit -m "docs(iterative-review): node recipes use record scripts and generated metrics"
```

---

### Task 8: Regenerate installed skills and final verification

**Files:**
- Generated: `.agents/skills/iterative-review/`
- Test: `py -3 tools/run.py installed-skills --apply` and `py -3 tools/run.py ci --check`

**Interfaces:**
- The installed copy of the skill mirrors the canonical source.

- [ ] **Step 1: Regenerate installed skills**

```bash
py -3 tools/run.py installed-skills --apply
```

- [ ] **Step 2: Run CI**

```bash
py -3 tools/run.py ci --check
```

Expected: all targets pass.

- [ ] **Step 3: Commit**

```bash
git add -A
git commit -m "regen(iterative-review): propagate state-router split to installed skills"
```

---

## Reference: old-to-new state mapping

| Old `review-metrics.json` field | New source | Source file |
|---|---|---|
| `current_node` | `current_node` | `review-state.json` |
| `previous_node` | `previous_node` | `review-state.json` |
| `non_trivial_fix` | `non_trivial_fix` | `review-state.json` |
| `contested` (per finding) | `blocker_class` in `blockers.jsonl` | `record_blocker.py` |
| `rounds_per_finding` | `findings.jsonl` - `resolutions.jsonl` | computed by `compile_metrics.py` |
| `findings_by_node` | `findings.jsonl` | computed by `compile_metrics.py` |
| `regressions` | `regressions.jsonl` | computed by `compile_metrics.py` |
| `total_rounds` | `max(discovered_at_round)` or `state["round"]` | computed by `compile_metrics.py` |
| `fix_round` per finding | `len(resolutions)` and `round` in `review-state.json` | computed at plan time |

## Reference: `next_node.py` hooks

Use these concrete hook points when editing `next_node.py`:

- Replace `_load_metrics(path)` with `_load_state(path)` and call it via `args.state`.
- Replace `_unresolved_severities(metrics)` with `_unresolved_findings(state)` that reads `findings.jsonl` and `resolutions.jsonl` from `state["scratch_dir"]`.
- Replace the `regressions` local in `_condition_holds` with `_load_jsonl(scratch / "regressions.jsonl")`.
- Replace the `contested` check in `_condition_holds` with a lookup in `blockers.jsonl` for the finding.
- Replace `_save_metrics` with `_save_state` that writes `review-state.json` and sets `previous_node = current_node` before updating `current_node`.
- Keep `GRAPH`, `_next_node`, and the CLI `--propose`/`--json` contract unchanged except for adding `--state` and removing `--metrics` as a write target.

## Plan handoff

After completing the plan, record the final plan-readiness rating from `handoff-gates` here and update the [roadmap](roadmap.md):

| Item | Status |
|---|---|
| Spec reviewed and approved | yes |
| Roadmap created | yes |
| Plan 1 written | yes |
| handoff-gates plan-readiness | 9/10 |
