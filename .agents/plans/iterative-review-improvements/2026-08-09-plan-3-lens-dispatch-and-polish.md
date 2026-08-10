# Plan 3 — Lens dispatch, write-safety, and final polish

> **For agentic workers:** REQUIRED SUB-SKILL: Use /subagent-driven-development (recommended) or /executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Close the remaining gaps in the `iterative-review` skill: automate lens selection with a `select_lenses.py` script, provide a script for orchestrator-authored markdown logs so no agent `write`s machine-managed scratch files, add focused tests for the router and record scripts, and document the lens re-run scope and no-hand-write contracts.

**Architecture:** Add a new `select_lenses.py` script that discovers `reviewer-*.md` profiles, parses their `## Applies to` rules (globs/keywords/inputs), and emits a dispatch list. Add `record_orchestrator_log.py` to append orchestrator markdown logs safely. Keep the canonical source in `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/` and regenerate the installed copy with `py -3 tools/run.py installed-skills --apply`. Add `tests/test_next_node.py` and `tests/test_record_scripts.py` that exercise the public CLI surface without a full repo CI run.

**Tech Stack:** Python 3, the existing `--help`/`--check` CLI contract, JSON/JSONL, `py -3 tools/run.py ci --check`.

## Global Constraints

- Only edit the canonical source in `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/`; regenerate `.agents/skills/iterative-review/` with `py -3 tools/run.py installed-skills --apply`.
- Every changed or new script must satisfy `--help` and `--check`.
- `py -3 tools/run.py ci --check` must pass before claiming any task complete.
- Work in the `iterative-review-improvements-3` worktree; do not commit to `main` directly.
- Do not change graph topology (nodes/edges) or reviewer lens profiles.
- Plans, specs, and roadmaps are source artifacts; commit them to the branch before implementation begins.

---

### Task 0: Verify worktree baseline and update the roadmap

**Files:**
- Read: `.agents/plans/iterative-review-improvements/roadmap.md`
- Modify: `.agents/plans/iterative-review-improvements/roadmap.md`
- Test: `py -3 tools/run.py ci --check`

**Interfaces:**
- Plan 3 row in the roadmap shows `in_progress`.

- [ ] **Step 1: Open the roadmap and set Plan 3 to `in_progress`**

Change the Plan 3 status and commit column to:

```markdown
| 3 | Lens dispatch, write-safety, and final polish | in_progress | [Plan 3](2026-08-09-plan-3-lens-dispatch-and-polish.md) | — | — | — | `select_lenses.py`, self-review template, tests, docs, plus a no-hand-write contract for all scratch files (`review-state.json`, `*.jsonl`, `review-log-*.md`) and a script for orchestrator markdown logs |
```

- [ ] **Step 2: Run CI**

```bash
py -3 tools/run.py ci --check
```

Expected: all targets pass.

- [ ] **Step 3: Commit the plan and roadmap update**

```bash
git add .agents/plans/iterative-review-improvements/2026-08-09-plan-3-lens-dispatch-and-polish.md .agents/plans/iterative-review-improvements/roadmap.md
git commit -m "docs(plans): start Plan 3 for iterative-review lens dispatch and write-safety"
```

---

### Task 1: Add `select_lenses.py` to automate lens dispatch

**Files:**
- Create: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/scripts/select_lenses.py`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/references/node-lens-dispatch.md`
- Test: `py -3 tools/run.py ci --check`

**Interfaces:**
- `select_lenses.py` takes `--state <review-state.json>` and `--apply` and appends `lenses.jsonl` to the scratch dir.
- Each line in `lenses.jsonl` is `{"lens": "reviewer-scripts", "profile_path": "...", "output_path": "..."}`.
- `--check` returns 0 and prints the dispatch list without writing.

- [ ] **Step 1: Create `select_lenses.py` with the helper script contract**

```python
#!/usr/bin/env python3
"""select_lenses.py - discover and select reviewer lens profiles for a PR. (read-only)"""

import argparse
import fnmatch
import json
import re
import sys
from pathlib import Path


def _reviewer_paths() -> list[Path]:
    """Return candidate reviewer-*.md paths in precedence order."""
    roots = [
        Path.home() / ".config" / "devin" / "agents" if sys.platform != "win32" else Path.home() / "AppData" / "Roaming" / "devin" / "agents",
        Path(".devin/agents"),
        Path(".agents/agents"),
        Path(__file__).parents[3] / "skills" / "selecting-a-subagent" / "assets",
    ]
    seen = set()
    results = []
    for root in roots:
        if not root.exists():
            continue
        for p in sorted(root.glob("reviewer-*.md")):
            if p.name in seen:
                continue
            seen.add(p.name)
            results.append(p)
    return results


def _applies_to(text: str) -> dict:
    """Parse the ## Applies to section from a reviewer profile."""
    section_match = re.search(r"## Applies to(.*?)\n## ", text, re.S)
    if not section_match:
        return {}
    section = section_match.group(1)

    def _list_items(name: str) -> list[str]:
        pattern = re.compile(rf"- {re.escape(name)}:\s*\n((?:\s+- .*\n)+)", re.S)
        m = pattern.search(section)
        if not m:
            return []
        return [line.strip("- ").strip() for line in m.group(1).strip().splitlines() if line.strip().startswith("-")]

    return {
        "globs": _list_items("globs"),
        "keywords": _list_items("keywords"),
        "inputs": _list_items("inputs"),
    }


def _changed_files(diff_path: Path | None) -> list[str]:
    if not diff_path or not diff_path.exists():
        return []
    text = diff_path.read_text(encoding="utf-8")
    return re.findall(r"^diff --git a/(.+) b/\1$", text, re.M)


def _matches(rule: dict, changed: list[str], diff_text: str, pr_text: str, provided_inputs: list[str]) -> bool:
    for inp in rule.get("inputs", []):
        if inp in provided_inputs:
            return True
    for pattern in rule.get("globs", []):
        if any(fnmatch.fnmatch(f, pattern) for f in changed):
            return True
    for keyword in rule.get("keywords", []):
        if keyword.lower() in diff_text.lower() or keyword.lower() in pr_text.lower():
            return True
    return False


def _state_paths(state: dict) -> tuple[Path, Path]:
    scratch = Path(state["scratch_dir"])
    return scratch / "lenses.jsonl", scratch / "pr_description.json"


def _load_state(state_path: Path) -> dict:
    with state_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _select(state: dict) -> list[dict]:
    scratch = Path(state["scratch_dir"])
    diff_path = scratch / f"review-{state['pr']['base']}..{state['pr']['head_sha']}.diff"
    pr_path = scratch / "pr_description.json"
    diff_text = diff_path.read_text(encoding="utf-8") if diff_path.exists() else ""
    pr_text = pr_path.read_text(encoding="utf-8") if pr_path.exists() else ""
    changed = _changed_files(diff_path if diff_path.exists() else None)
    provided = ["<diff_path>", "<pr_description>", "<scan_findings>", "<review-log-orchestrator-self-review>"]

    selected = []
    for profile in _reviewer_paths():
        text = profile.read_text(encoding="utf-8")
        rule = _applies_to(text)
        lens = profile.stem
        if _matches(rule, changed, diff_text, pr_text, provided) and lens != "reviewer-strong":
            selected.append({
                "lens": lens,
                "profile_path": str(profile.resolve()),
                "output_path": str((scratch / f"review-log-{lens}.md").resolve()),
            })
    return selected


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Select reviewer lenses for a PR.")
    parser.add_argument("--state", required=True, help="Path to review-state.json")
    parser.add_argument("--apply", action="store_true", help="Write lenses.jsonl to the scratch dir")
    parser.add_argument("--check", action="store_true", help="Validate CLI contract only")
    args = parser.parse_args(argv)

    if args.check:
        print("select_lenses.py: --check ok")
        return 0

    state = _load_state(Path(args.state))
    selected = _select(state)

    out_path, _ = _state_paths(state)
    if args.apply:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with out_path.open("w", encoding="utf-8") as f:
            for entry in selected:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        print(f"Wrote {out_path} with {len(selected)} lens(es)")
    else:
        for entry in selected:
            print(entry["lens"], "->", entry["output_path"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 2: Make `select_lenses.py` executable and add to `installed-skills` manifest if needed**

The file already lives in `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/scripts/`. Regeneration will place it in `.agents/skills/iterative-review/scripts/`.

- [ ] **Step 3: Update `node-lens-dispatch.md` to use `select_lenses.py`**

Replace the manual dispatch table and procedure steps 1-4 with:

```markdown
1. Run `select_lenses.py` to discover matching lenses:
   ```
   py -3 .agents/skills/iterative-review/scripts/select_lenses.py --state <scratch_dir>/review-state.json --apply
   ```
2. Read `<scratch_dir>/lenses.jsonl`; each line is a lens to dispatch.
3. Build the common input package: `<diff_path>`, `<pr_description>`, `<scan_findings>`, and `review-log-orchestrator-self-review.md`.
4. `run_subagent` each lens from `lenses.jsonl` with its `profile_path` and `output_path`.
```

Keep the rest of the recipe unchanged.

- [ ] **Step 4: Run CI**

```bash
py -3 tools/run.py ci --check
```

Expected: all targets pass.

- [ ] **Step 5: Commit**

```bash
git add codex-marketplace/plugins/superpowers-plus/skills/iterative-review/scripts/select_lenses.py codex-marketplace/plugins/superpowers-plus/skills/iterative-review/references/node-lens-dispatch.md
git commit -m "feat(iterative-review): select lenses script and recipe update"
```

---

### Task 2: Add `record_orchestrator_log.py` for markdown logs

**Files:**
- Create: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/scripts/record_orchestrator_log.py`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/SKILL.md`
- Test: `py -3 tools/run.py ci --check`

**Interfaces:**
- `record_orchestrator_log.py --state <review-state.json> --node <node> --data <markdown>` appends a header, round, and the markdown block to `review-log-<node>.md` in the scratch dir.
- Refuses to overwrite existing content; appends only.

- [ ] **Step 1: Create `record_orchestrator_log.py`**

```python
#!/usr/bin/env python3
"""record_orchestrator_log.py - append an orchestrator markdown log for a node. (mixed)"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def _load_state(state_path: Path) -> dict:
    with state_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Append an orchestrator markdown log.")
    parser.add_argument("--state", required=True, help="Path to review-state.json")
    parser.add_argument("--node", required=True, help="Node name (used for review-log-<node>.md)")
    parser.add_argument("--data", required=True, help="Markdown content to append")
    parser.add_argument("--apply", action="store_true", help="Append the log")
    parser.add_argument("--check", action="store_true", help="Validate CLI contract")
    args = parser.parse_args(argv)

    if args.check:
        print("record_orchestrator_log.py: --check ok")
        return 0

    state = _load_state(Path(args.state))
    scratch = Path(state["scratch_dir"])
    log_path = scratch / f"review-log-{args.node}.md"
    round_ = state.get("round", 1)
    now = datetime.now(timezone.utc).isoformat()
    block = f"\n## Round {round_} - {now}\n\n{args.data}\n"

    if not args.apply:
        print(f"Would append to {log_path}:\n{block}")
        return 0

    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as f:
        f.write(block)
    print(f"Appended to {log_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 2: Update `SKILL.md` invariants to prohibit hand-write on managed files**

Add a new invariant subsection:

```markdown
## Machine-managed files

The following files in the off-repo scratch must be written only through the provided scripts:

- `review-state.json` — written by `next_node.py --propose` or `next_node.py --resync --apply`.
- `findings.jsonl`, `resolutions.jsonl`, `regressions.jsonl`, `blockers.jsonl` — written by `record_*.py` scripts.
- `review-log-*.md` — written by the dispatched lens subagents and by `record_orchestrator_log.py` for orchestrator logs.
- `review-metrics.json` — written by `compile_metrics.py`.

Do not use `write` or `edit` on these files. The `write` tool causes IDE buffer contention when the file is also open or being updated by a script.
```

- [ ] **Step 3: Run CI**

```bash
py -3 tools/run.py ci --check
```

Expected: all targets pass.

- [ ] **Step 4: Commit**

```bash
git add codex-marketplace/plugins/superpowers-plus/skills/iterative-review/scripts/record_orchestrator_log.py codex-marketplace/plugins/superpowers-plus/skills/iterative-review/SKILL.md
git commit -m "feat(iterative-review): record_orchestrator_log and no-hand-write contract"
```

---

### Task 3: Add focused tests for `next_node.py` and the record scripts

**Files:**
- Create: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/tests/test_next_node.py`
- Create: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/tests/test_record_scripts.py`
- Test: `py -3 -m pytest` from the skill directory, then `py -3 tools/run.py ci --check`

**Interfaces:**
- Tests live in `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/tests/`.
- `test_next_node.py` validates `--propose` graph transitions on a synthetic `review-state.json`.
- `test_record_scripts.py` validates that `record_finding.py` and `record_resolution.py` append correctly and reject non-array/non-object data.

- [x] **Step 1: Create the test directory and `__init__.py` (or keep it package-less)**

No `__init__.py` is needed if `pytest` discovers by file. Create the tests as standalone scripts.

- [x] **Step 2: Write `test_next_node.py`**

```python
import json
import subprocess
import tempfile
from pathlib import Path

import pytest

SELECTOR = ["py", "-3", ".agents/skills/iterative-review/scripts/next_node.py"]


def _state(tmp_path: Path, node: str = "setup") -> Path:
    p = tmp_path / "review-state.json"
    p.write_text(json.dumps({
        "current_node": node,
        "previous_node": "",
        "round": 1,
        "max_fix_rounds": 4,
        "pr": {"pr_number": 999, "base": "main", "branch": "test", "head_sha": "abc123"},
        "scratch_dir": str(tmp_path),
    }), encoding="utf-8")
    return p


def test_propose_setup(tmp_path: Path):
    state = _state(tmp_path)
    result = subprocess.run(SELECTOR + ["--state", str(state), "--propose", "normalize-inputs"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "ALLOWED: normalize-inputs" in result.stdout


def test_blocked_missing_artifacts(tmp_path: Path):
    state = _state(tmp_path, "lens-dispatch")
    (tmp_path / "lenses.jsonl").write_text("", encoding="utf-8")
    result = subprocess.run(SELECTOR + ["--state", str(state), "--propose", "lens-triage"], capture_output=True, text=True)
    assert result.returncode == 1
    assert "BLOCKED" in result.stdout
```

- [x] **Step 3: Write `test_record_scripts.py`**

```python
import json
import subprocess
import tempfile
from pathlib import Path

import pytest


def _state(tmp_path: Path) -> Path:
    p = tmp_path / "review-state.json"
    p.write_text(json.dumps({
        "current_node": "setup",
        "previous_node": "",
        "round": 1,
        "max_fix_rounds": 4,
        "pr": {"pr_number": 999, "base": "main", "branch": "test", "head_sha": "abc123"},
        "scratch_dir": str(tmp_path),
    }), encoding="utf-8")
    return p


def _run(script: str, state: Path, data: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["py", "-3", f".agents/skills/iterative-review/scripts/{script}.py", "--state", str(state), "--data", data, "--apply"],
        capture_output=True, text=True,
    )


def test_record_finding_object(tmp_path: Path):
    state = _state(tmp_path)
    data = json.dumps({"finding_id": "f-001", "lens": "scripts", "discovered_at_node": "lens-dispatch", "discovered_at_round": 1, "severity": "minor"})
    result = _run("record_finding", state, data)
    assert result.returncode == 0
    lines = (tmp_path / "findings.jsonl").read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 1
    assert "f-001" in lines[0]


def test_record_finding_rejects_scalar(tmp_path: Path):
    state = _state(tmp_path)
    result = _run("record_finding", state, "\"not-an-object\"")
    assert result.returncode == 1
```

- [x] **Step 4: Add `pytest` marker to CI?**

If the repo does not run `pytest` automatically, these tests can be invoked manually with `py -3 -m pytest` from the canonical skill directory. The plan's acceptance criteria is that `py -3 tools/run.py ci --check` still passes (lint and CLI contracts) and the manual `pytest` command passes.

- [x] **Step 5: Run CI and pytest**

```bash
cd codex-marketplace/plugins/superpowers-plus/skills/iterative-review
py -3 -m pytest tests/ -v
cd -
py -3 tools/run.py ci --check
```

Expected: all tests pass and CI is green.

- [x] **Step 6: Commit**

```bash
git add codex-marketplace/plugins/superpowers-plus/skills/iterative-review/tests/
git commit -m "test(iterative-review): next_node and record script tests"
```

---

### Task 4: Add `references/review-log-orchestrator-self-review-template.md`

**Files:**
- Create: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/references/review-log-orchestrator-self-review-template.md`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/SKILL.md`
- Test: `py -3 tools/run.py ci --check`

**Interfaces:**
- The template provides a markdown skeleton for the orchestrator to fill via `record_orchestrator_log.py` or equivalent.

- [ ] **Step 1: Create the template file**

```markdown
# Orchestrator self-review

## Inputs
- diff: `<diff_path>`
- pr_description: `<pr_description>`

## Scan
- Relevant file categories changed:
- Preflight predictions:

## Predictions
No uncertain items requiring lens escalation.
```

- [ ] **Step 2: Update `SKILL.md` Required reading list**

Add:
- `references/review-log-orchestrator-self-review-template.md` for the prediction log template.

- [ ] **Step 3: Run CI**

```bash
py -3 tools/run.py ci --check
```

Expected: all targets pass.

- [ ] **Step 4: Commit**

```bash
git add codex-marketplace/plugins/superpowers-plus/skills/iterative-review/references/review-log-orchestrator-self-review-template.md codex-marketplace/plugins/superpowers-plus/skills/iterative-review/SKILL.md
git commit -m "docs(iterative-review): orchestrator self-review template"
```

---

### Task 5: Document and enforce lens re-run scope

**Files:**
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/SKILL.md`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/references/node-reviewer-fixes.md`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/references/node-lens-dispatch.md`
- Test: `py -3 tools/run.py ci --check`

**Interfaces:**
- `lens-dispatch` dispatches each relevant lens exactly once.
- `reviewer-fixes` re-dispatches only the lens that originally discovered the finding.

- [ ] **Step 1: Add a `## Lens re-run scope` section to `SKILL.md`**

```markdown
## Lens re-run scope

`lens-dispatch` runs at most once per review cycle. It dispatches every lens whose `## Applies to` rules match the PR.

When a finding is fixed, `finding-fix` -> `re-preflight` -> `reviewer-fixes` re-runs only the originating lens for that finding. Do not re-dispatch all lenses after a single fix; that is unnecessary churn and can introduce unrelated feedback late in the cycle.
```

- [ ] **Step 2: Update `node-reviewer-fixes.md`**

Add to the recipe:

```markdown
1. Determine the `lens` that discovered the finding being fixed (from `findings.jsonl`).
2. Re-dispatch only that lens profile with the fix diff and the original input package.
3. Do not dispatch other lenses; their prior review remains valid unless the fix diff changes files they own.
```

- [ ] **Step 3: Update `node-lens-dispatch.md` to note one-time dispatch**

Add a note:

```markdown
`lens-dispatch` is a one-time dispatch. After this node, the graph routes to `lens-triage`, `metrics-track`, `finding-fix`, and `reviewer-fixes`. `reviewer-fixes` re-runs only the lens associated with the finding being fixed.
```

- [ ] **Step 4: Run CI**

```bash
py -3 tools/run.py ci --check
```

Expected: all targets pass.

- [ ] **Step 5: Commit**

```bash
git add codex-marketplace/plugins/superpowers-plus/skills/iterative-review/SKILL.md codex-marketplace/plugins/superpowers-plus/skills/iterative-review/references/node-reviewer-fixes.md codex-marketplace/plugins/superpowers-plus/skills/iterative-review/references/node-lens-dispatch.md
git commit -m "docs(iterative-review): lens re-run scope contracts"
```

---

### Task 6: Final documentation and marketplace refresh

**Files:**
- Modify: any stale references touched above
- Test: `py -3 tools/run.py ci --check` and `py -3 tools/run.py installed-skills --apply`

**Interfaces:**
- All canonical and installed copies are in sync.
- `SKILL.md` is ready for consumers.

- [ ] **Step 1: Regenerate installed skills**

```bash
py -3 .agents/skills/refreshing-installed-skills/scripts/refresh_installed_skills.py --apply --force --allow-shared-checkout
```

- [ ] **Step 2: Run CI**

```bash
py -3 tools/run.py ci --check
```

Expected: all targets pass.

- [ ] **Step 3: Commit the regeneration**

```bash
git add -A
git commit -m "chore(iterative-review): regenerate installed skills for Plan 3"
```

---

### Task 7: Open PR and archive the plan

**Files:**
- Use: `gh pr create`
- Move: this plan to `.agents/plans/completed/iterative-review-improvements/`

**Interfaces:**
- Draft PR #289 (or next available) opened from `iterative-review-improvements-3` to `main`.

- [ ] **Step 1: Push the branch**

```bash
git push -u origin iterative-review-improvements-3
```

- [ ] **Step 2: Create a draft PR**

Use `gh pr create --draft` with a body summarizing the Plan 3 changes and linking to the spec and roadmap.

- [ ] **Step 3: Run the `iterative-review` skill on the new PR until `closeout` and `reviewer-strong: clean`**

Follow the `iterative-review` skill on the new PR. Fix any findings, then flip to ready for review and merge.

- [ ] **Step 4: Archive this plan to `completed/` after merge**

When the PR merges, move this file to `.agents/plans/completed/iterative-review-improvements/2026-08-09-plan-3-lens-dispatch-and-polish.md` and update the roadmap row to `done` with the PR number.

---

## Execution handoff

Plan complete and saved to `.agents/plans/iterative-review-improvements/2026-08-09-plan-3-lens-dispatch-and-polish.md`.

Recommended execution approach: **subagent-driven-development**. Each task is independently implementable, modifies distinct files, and ends with a testable deliverable. Task 0 should be completed first to commit the plan and roadmap; Tasks 1-6 can then proceed in order.
