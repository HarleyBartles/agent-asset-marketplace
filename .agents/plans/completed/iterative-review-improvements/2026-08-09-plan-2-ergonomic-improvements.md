# Plan 2 — Ergonomic and reliability improvements

> **For agentic workers:** REQUIRED SUB-SKILL: Use /subagent-driven-development (recommended) or /executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add `next_node.py` observability and recovery commands, make state advancement artifact-aware, fix the round cap to be tunable, support batch recording of findings, and cleanly distinguish `contested` from `tool-blocked` routing.

**Architecture:** Extend `next_node.py` with `--status` and `--resync --apply`. Add per-finding and per-severity round caps to `review-state.json`. Make record scripts accept a JSON array for batching. Rename the graph condition that routes to `blocked` from `contested` to `blocked` while adding a `contested`-only condition for finer routing. Keep the canonical source in `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/` and regenerate the installed copy with `py -3 tools/run.py installed-skills --apply`.

**Tech Stack:** Python 3, the existing `--help`/`--check` CLI contract, JSON/JSONL, `py -3 tools/run.py ci --check`.

## Global Constraints

- Only edit the canonical source in `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/`; regenerate `.agents/skills/iterative-review/` with `py -3 tools/run.py installed-skills --apply`.
- Every changed or new script must satisfy `--help` and `--check`.
- `py -3 tools/run.py ci --check` must pass before claiming any task complete.
- Work in the `iterative-review-improvements-2` worktree; do not commit to `main` directly.
- Do not change graph topology (nodes/edges) or reviewer lens profiles.

---

### Task 0: Verify `review-metrics-schema.json` is consistent with the design spec

**Files:**
- Read: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/references/review-metrics-schema.json`
- Read: `.agents/specs/completed/2026-08-09-iterative-review-improvements-design.md`

**Interfaces:**
- Verifies the schema already matches the spec after Plan 1.

- [ ] **Step 1: Confirm schema invariants**

Check that `review-metrics-schema.json`:
- `severity` enum contains `"deferred"`.
- `rounds_per_finding` items do not require `resolved_at_node` or `resolved_at_round`.
- `rounds_per_finding` and `regressions` items both include `regression_of`.
- `total_rounds` is a generated, non-required field.

- [ ] **Step 2: Run CI**

```bash
py -3 tools/run.py ci --check
```

Expected: all targets pass.

- [ ] **Step 3: If any invariant is missing, fix `review-metrics-schema.json` and re-run CI**

- [ ] **Step 4: Commit**

```bash
git add codex-marketplace/plugins/superpowers-plus/skills/iterative-review/references/review-metrics-schema.json
# or no changes if already consistent
git diff --quiet || git commit -m "chore(iterative-review): verify review-metrics schema"
```

---

### Task 1: Make round cap tunable per finding and severity

**Files:**
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/references/review-state-schema.json`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/scripts/next_node.py`
- Test: `py -3 tools/run.py ci --check`

**Interfaces:**
- `review-state.json` can now contain optional `max_rounds_by_severity` and `max_rounds_by_finding`.
- `next_node.py` `round_cap` condition selects the most specific cap for a finding.

- [ ] **Step 1: Extend `review-state-schema.json`**

Insert into `properties` after `max_fix_rounds`:

```json
"max_rounds_by_severity": {
  "type": "object",
  "additionalProperties": {"type": "integer", "minimum": 1}
},
"max_rounds_by_finding": {
  "type": "object",
  "additionalProperties": {"type": "integer", "minimum": 1}
},
```

- [ ] **Step 2: Update `next_node.py` round cap logic**

Replace the `round_cap` branch in `_condition_holds` with:

```python
if condition == "round_cap":
    if "rounds_per_finding" in state:
        rounds = state.get("rounds_per_finding", [])
        return any(
            (f.get("fix_round", 0) or 0) >= state.get("max_fix_rounds", 4)
            for f in rounds
            if not f.get("resolved_at_node")
        )
    scratch = Path(state.get("scratch_dir", "."))
    findings = _load_jsonl(scratch / "findings.jsonl")
    resolved = {r["finding_id"] for r in _load_jsonl(scratch / "resolutions.jsonl")}
    round_ = state.get("round", 1)
    default_max = state.get("max_fix_rounds", 4)
    by_severity = state.get("max_rounds_by_severity", {})
    by_finding = state.get("max_rounds_by_finding", {})
    return any(
        f["finding_id"] not in resolved
        and f.get("severity") in ("blocking", "important")
        and (round_ - f.get("discovered_at_round", round_) + 1) >= by_finding.get(
            f["finding_id"],
            by_severity.get(f.get("severity", ""), default_max),
        )
        for f in findings
    )
```

- [ ] **Step 3: Run CI**

```bash
py -3 tools/run.py ci --check
```

Expected: all targets pass.

- [ ] **Step 4: Commit**

```bash
git add codex-marketplace/plugins/superpowers-plus/skills/iterative-review/references/review-state-schema.json \
        codex-marketplace/plugins/superpowers-plus/skills/iterative-review/scripts/next_node.py
git commit -m "feat(iterative-review): tunable per-finding and per-severity round caps"
```

---

### Task 2: Distinguish `contested` from `tool-blocked` in routing

**Files:**
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/scripts/next_node.py`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/references/review-state-graph.md` (if it lists the condition)
- Test: `py -3 tools/run.py ci --check`

**Interfaces:**
- The graph condition that routes to the `blocked` terminal is renamed from `contested` to `blocked`.
- A new `contested` condition matches only `blocker_class == "contested"`.
- A new `tool_blocked` condition matches only `blocker_class == "tool-blocked"`.

- [ ] **Step 1: Update `GRAPH` condition names**

Change every `"contested"` condition string used to route to `blocked` in `GRAPH` to `"blocked"`. There are three occurrences: in `lens-triage`, `reviewer-fixes`, and `final-strong`. For example:

```python
"lens-triage": [
    ("blocked", "blocked"),
    ("findings", "metrics-track"),
    ("trivial", "final-strong"),
    ("clean", "final-strong"),
],
```

Keep the value string `blocked` unchanged.

- [ ] **Step 2: Add `_blocked` and `_tool_blocked` helpers and update `_condition_holds`**

Add after `_contested`:

```python
def _tool_blocked(state: dict) -> bool:
    if "rounds_per_finding" in state:
        return any(f.get("blocked_class") == "tool-blocked" for f in state.get("rounds_per_finding", []) if not f.get("resolved_at_node"))
    scratch = Path(state.get("scratch_dir", "."))
    blockers = _load_jsonl(scratch / "blockers.jsonl")
    unresolved = set(_unresolved_findings(state))
    return any(b.get("blocker_class") == "tool-blocked" and b.get("finding_id") in unresolved for b in blockers)
```

Then in `_condition_holds`:

```python
if condition == "contested":
    return _contested(state)
if condition == "tool_blocked":
    return _tool_blocked(state)
if condition == "blocked":
    return _contested(state) or _tool_blocked(state)
```

Remove the `if condition == "contested":` branch that currently calls `_contested(state)`.

- [ ] **Step 3: Update `review-state-graph.md` if it lists conditions**

If `review-state-graph.md` documents the `contested` condition, rename the guard to `blocked` and note that `contested` and `tool-blocked` are the two blocker classes.

- [ ] **Step 4: Run CI**

```bash
py -3 tools/run.py ci --check
```

- [ ] **Step 5: Commit**

```bash
git add codex-marketplace/plugins/superpowers-plus/skills/iterative-review/scripts/next_node.py
# add graph doc only if it changed
git diff --quiet codex-marketplace/plugins/superpowers-plus/skills/iterative-review/references/review-state-graph.md || git add codex-marketplace/plugins/superpowers-plus/skills/iterative-review/references/review-state-graph.md
git commit -m "feat(iterative-review): distinguish contested and tool-blocked routing"
```

---

### Task 3: Add `next_node.py --status`

**Files:**
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/scripts/next_node.py`

**Interfaces:**
- `next_node.py --state <path> --status` prints a human-readable status report and exits 0.
- `--status` with `--json` emits machine-readable JSON.

- [ ] **Step 1: Add `_status_report` function**

Insert before `main`:

```python
def _status_report(state: dict, ledger: Path, node: str, reason: str) -> str:
    scratch = Path(state.get("scratch_dir", "."))
    unresolved = _unresolved_findings(state)
    regressions = _unresolved_regressions(state)
    log_preview = []
    for log_name in ("findings.jsonl", "resolutions.jsonl", "regressions.jsonl", "blockers.jsonl"):
        p = scratch / log_name
        if p.exists():
            lines = [line for line in p.read_text(encoding="utf-8-sig").splitlines() if line.strip()]
            log_preview.append(f"{log_name}: {len(lines)} lines")
    return (
        f"current_node: {state.get('current_node', 'unknown')}\n"
        f"previous_node: {state.get('previous_node', '')}\n"
        f"next_allowed: {node}\n"
        f"reason: {reason}\n"
        f"round: {state.get('round', 1)} / max: {state.get('max_fix_rounds', 4)}\n"
        f"unresolved_important_blocking: {len(unresolved)}\n"
        f"unresolved_regressions: {len(regressions)}\n"
        f"ledger_present: {ledger.exists()}\n"
        f"logs:\n" + "\n".join(f"  {entry}" for entry in log_preview)
    )
```

- [ ] **Step 2: Add `--status` argument and handler in `main`**

Add to the parser:

```python
parser.add_argument("--status", action="store_true", help="print current status without mutating state")
```

After the existing `args = parser.parse_args(argv)` and before the read-only discovery section, add:

```python
if args.status:
    if not (args.state or args.metrics):
        print("--status requires --state or --metrics", file=sys.stderr)
        return 2
    if args.json:
        scratch = Path(state.get("scratch_dir", "."))
        payload = {
            "current_node": state.get("current_node", "unknown"),
            "previous_node": state.get("previous_node", ""),
            "next_allowed": node,
            "reason": reason,
            "round": state.get("round", 1),
            "max_fix_rounds": state.get("max_fix_rounds", 4),
            "unresolved_important_blocking": len(_unresolved_findings(state)),
            "unresolved_regressions": len(_unresolved_regressions(state)),
            "ledger_present": ledger_path.exists(),
        }
        print(json.dumps(payload, ensure_ascii=False))
    else:
        print(_status_report(state, ledger_path, node, reason))
    return 0
```

- [ ] **Step 3: Run CI**

```bash
py -3 tools/run.py ci --check
```

- [ ] **Step 4: Commit**

```bash
git add codex-marketplace/plugins/superpowers-plus/skills/iterative-review/scripts/next_node.py
git commit -m "feat(iterative-review): add next_node --status"
```

---

### Task 4: Add `next_node.py --resync --apply`

**Files:**
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/scripts/next_node.py`

**Interfaces:**
- `next_node.py --state <path> --resync` reports drift between the saved `current_node` and the node the logs actually imply.
- `next_node.py --state <path> --resync --apply` rewrites `review-state.json` to the log-implied node.

- [ ] **Step 1: Add `--resync` and `--apply` arguments**

Add to the parser:

```python
parser.add_argument("--resync", action="store_true", help="compare state to logs and report drift")
parser.add_argument("--apply", action="store_true", help="apply the correction during --resync")
```

- [ ] **Step 2: Add resync handler before the discovery section**

After the `node, reason = _next_node(...)` calls, add:

```python
if args.resync:
    saved = state.get("current_node", "unknown")
    if saved == node:
        print(f"SYNC: current_node {saved} matches log-implied next node")
        return 0
    print(f"DRIFT: current_node is {saved}; logs imply {node}  -  {reason}")
    if not args.apply:
        print("Use --resync --apply to correct the state pointer", file=sys.stderr)
        return 1
    fresh = _load_state(state_path)
    fresh["previous_node"] = fresh.get("current_node", "")
    fresh["current_node"] = node
    state_path.write_text(json.dumps(fresh, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"SYNC: corrected current_node to {node}")
    return 0
```

- [ ] **Step 3: Run CI**

```bash
py -3 tools/run.py ci --check
```

- [ ] **Step 4: Commit**

```bash
git add codex-marketplace/plugins/superpowers-plus/skills/iterative-review/scripts/next_node.py
git commit -m "feat(iterative-review): add next_node --resync --apply"
```

---

### Task 5: Make `--propose` artifact-aware

**Files:**
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/scripts/next_node.py`

**Interfaces:**
- Before writing `review-state.json` on `--propose`, `next_node.py` verifies the target node has the required artifacts from the current step.

- [ ] **Step 1: Define `ARTIFACTS_FOR_NODE`**

After `GRAPH`, add:

```python
ARTIFACTS_FOR_NODE: dict[str, list[tuple[str, str]]] = {
    # node: [(log_filename, required_value_key), ...]
    "metrics-track": [("findings.jsonl", "*")],
    "regression-scan": [("regressions.jsonl", "*")],
    "resolved-ledger": [("resolutions.jsonl", "*")],
}
```

A required value key of `*` means the log must be non-empty. Later, more specific requirements can be added.

- [ ] **Step 2: Add `_artifacts_present` helper**

```python
def _artifacts_present(node: str, state: dict) -> tuple[bool, str]:
    scratch = Path(state.get("scratch_dir", "."))
    for log_name, key in ARTIFACTS_FOR_NODE.get(node, []):
        p = scratch / log_name
        if not p.exists() or not p.read_text(encoding="utf-8-sig").strip():
            return False, f"missing or empty artifact: {log_name}"
        if key != "*":
            records = _load_jsonl(p)
            if not any(key in r for r in records):
                return False, f"artifact {log_name} has no record with key {key}"
    return True, ""
```

- [ ] **Step 3: Call the artifact check before writing state**

In `main`, inside the `elif state_path is not None and args.propose == node:` block, before `fresh = _load_state(state_path)`, add:

```python
ok, missing = _artifacts_present(args.propose, state)
if not ok:
    print(f"BLOCKED: proposed {args.propose} is allowed, but {missing}", file=sys.stderr)
    return 1
```

- [ ] **Step 4: Run CI**

```bash
py -3 tools/run.py ci --check
```

- [ ] **Step 5: Commit**

```bash
git add codex-marketplace/plugins/superpowers-plus/skills/iterative-review/scripts/next_node.py
git commit -m "feat(iterative-review): artifact-aware --propose validation"
```

---

### Task 6: Support batch recording via `--data` arrays

**Files:**
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/scripts/record_finding.py`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/scripts/record_resolution.py`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/scripts/record_regression.py`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/scripts/record_blocker.py`

**Interfaces:**
- Each record script's `--data` argument now accepts either a single JSON object or a JSON array of objects. Each object is validated and appended idempotently.

- [ ] **Step 1: Add `_data_items` helper to each record script**

In each `record_*.py`, replace the single `finding = json.loads(args.data)` or `data = json.loads(args.data)` line with:

```python
parsed = json.loads(args.data)
data_items = parsed if isinstance(parsed, list) else [parsed]
```

- [ ] **Step 2: Wrap the validation/append logic in a loop per item**

For `record_finding.py`:

```python
state = _load_state(state_path)
scratch = Path(state["scratch_dir"])
log = scratch / "findings.jsonl"
log.parent.mkdir(parents=True, exist_ok=True)

existing = set()
if log.exists():
    for line in log.read_text(encoding="utf-8-sig").splitlines():
        if line.strip():
            existing.add(json.loads(line).get("finding_id"))

recorded = []
for item in data_items:
    missing = REQUIRED - item.keys()
    if missing:
        print(f"ERROR: missing keys {missing} in {item}", file=sys.stderr)
        return 1
    if item["finding_id"] in existing:
        continue
    with log.open("a", encoding="utf-8") as f:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")
    existing.add(item["finding_id"])
    recorded.append(item["finding_id"])

if recorded:
    print(f"record_finding.py: recorded {', '.join(recorded)}")
else:
    print("record_finding.py: all findings already recorded; no change")
return 0
```

- [ ] **Step 3: Apply the same pattern to the other record scripts**

`record_resolution.py`, `record_regression.py`, and `record_blocker.py` should each:
- Parse `--data` as a list.
- Validate each item against `REQUIRED`.
- Skip duplicates.
- Append all new records.
- Print the recorded ids or a no-change message.

- [ ] **Step 4: Run CI**

```bash
py -3 tools/run.py ci --check
```

- [ ] **Step 5: Commit**

```bash
git add codex-marketplace/plugins/superpowers-plus/skills/iterative-review/scripts/record_*.py
git commit -m "feat(iterative-review): batch record scripts accept --data arrays"
```

---

### Task 7: Update `SKILL.md` and regenerate installed skill

**Files:**
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/SKILL.md`
- Regenerate: `.agents/skills/iterative-review/`

**Interfaces:**
- The top-level summary of `next_node.py` options in `SKILL.md` mentions `--status` and `--resync`.

- [ ] **Step 1: Update `SKILL.md`**

In the "Following the graph" section, add after the existing `next_node.py --state ...` example:

```markdown
3a. (optional) Inspect status without mutating state:
   ```
   py -3 .agents/skills/iterative-review/scripts/next_node.py --state <scratch_dir>/review-state.json --status
   ```
3b. (optional) If the logs have run ahead of the saved `current_node`, resync state:
   ```
   py -3 .agents/skills/iterative-review/scripts/next_node.py --state <scratch_dir>/review-state.json --resync --apply
   ```
```

- [ ] **Step 2: Regenerate installed copy**

```bash
py -3 tools/run.py installed-skills --apply
```

- [ ] **Step 3: Run CI**

```bash
py -3 tools/run.py ci --check
```

- [ ] **Step 4: Commit**

```bash
git add codex-marketplace/plugins/superpowers-plus/skills/iterative-review/SKILL.md \
        .agents/skills/iterative-review/
git commit -m "docs(iterative-review): SKILL.md for status and resync"
```

---

### Task 8: Final closeout and plan completion

**Files:**
- Modify: `.agents/plans/iterative-review-improvements/roadmap.md`
- Move: this plan to `.agents/plans/completed/iterative-review-improvements/`

**Interfaces:**
- Plan 2 is marked done and archived when the PR is ready.

- [ ] **Step 1: Update roadmap table**

Change Plan 2 row from `pending` to `done` and fill the commit and PR columns after the final merge.

- [ ] **Step 2: Archive this plan file**

Follow the `completing-plans` runbook: `git mv .agents/plans/completed/iterative-review-improvements/2026-08-09-plan-2-ergonomic-improvements.md .agents/plans/completed/iterative-review-improvements/`, then run `tools/heal_archive_links.py --apply`, `tools/run.py mesh --apply`, and `tools/run.py marketplace --apply`.

- [ ] **Step 3: Run final CI**

```bash
py -3 tools/run.py ci --check
```

- [ ] **Step 4: Commit and push**

```bash
git add -A
git commit -m "archive: complete Plan 2"
git push origin iterative-review-improvements-2
```
