# Iterative Review Experience Improvements

> **For agentic workers:** REQUIRED SUB-SKILL: Use `/executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the `iterative-review` graph cheap to follow, internally consistent, and honest about what work the branch actually implements.

**Architecture:** Introduce a `reviewer-fast` cheap pre-lens, harden recording scripts against hand-rolled helpers, make `scope-honesty` a concrete artifact, agree the graph across all node recipes, and keep scratch artifacts in sync with the working tree.

**Tech Stack:** Python 3, `codex-marketplace`/`superpowers-plus` skill source, `.agents/skills/iterative-review/scripts`

## Global Constraints
- All changes must be made in the plugin source under `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/` and regenerated to `.agents/skills/iterative-review/`.
- Canonical preflight `py -3 tools/run.py ci --check` must pass after every task that changes code, docs, or generated surfaces.
- Machine-managed scratch files are written only by the provided scripts; orchestrators may not hand-edit `review-state.json`, `findings.jsonl`, `resolutions.jsonl`, `regressions.jsonl`, `blockers.jsonl`, `lenses.jsonl`, or `review-metrics.json`.
- No emojis, no em-dashes.

---

### Task 1: Introduce `reviewer-fast` as a cheap pre-lens

**Files:**
- Create: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/references/reviewer-fast.md`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/references/review-state-graph.md`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/references/node-orchestrator-self-review.md` (re-purpose)
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/scripts/select_lenses.py`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/scripts/next_node.py`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/SKILL.md`

**Interfaces:**
- Consumes: the same `<diff_path>` and `<pr_description>` as other lenses.
- Produces: `review-log-reviewer-fast.md` ending with `reviewer-fast: clean` or `reviewer-fast: N issue(s)`.

- [x] **Step 1: Write `reviewer-fast.md` lens profile**

The profile is a cheap subagent prompt. It scans the diff for the most common mechanical issues that are currently in `orchestrator-self-review`: help text mismatches, dead CLI flags, stale `$-token` instructions, missing error handling, inconsistent exit codes, dead branches, and plan/spec drift. It should be told explicitly that it is a pre-filter, not a deep review, and must end with one status line.

- [x] **Step 2: Re-purpose `orchestrator-self-review` into `reviewer-fast`**

Delete the `orchestrator-self-review` node recipe. Rename it to `node-reviewer-fast.md`. The recipe becomes: dispatch `reviewer-fast` with the diff, capture its log, record any findings it produces, and route to `lens-dispatch` or `metrics-track`/`finding-fix` if it finds issues. Update `next_node.py` so the graph edge from `preflight` (or `scope-honesty`) points to `reviewer-fast`.

- [x] **Step 3: Update `select_lenses.py`**

`select_lenses.py` should always select `reviewer-fast` in addition to the other matching lenses. It should be first in `lenses.jsonl`. The `lens-dispatch` node can then dispatch it first and wait for it before dispatching others, or all can run in parallel and `lens-triage` treats `reviewer-fast` findings as cheap first-pass filter results.

- [x] **Step 4: Update `review-state-graph.md` and `SKILL.md`**

Replace `orchestrator-self-review` with `reviewer-fast` in the graph reference and quick start. Update `start_review.py` output and `next_node.py` help text.

- [x] **Step 5: Run `ci --check` and commit**

Run `py -3 tools/run.py ci --check`. If clean, commit with `git commit -m "feat(iterative-review): add reviewer-fast cheap pre-lens"`.

### Task 2: Make `scope-honesty` a concrete artifact

**Files:**
- Create: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/scripts/check_scope_honesty.py`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/scripts/normalize_review_inputs.py`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/references/node-scope-honesty.md`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/scripts/next_node.py`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/SKILL.md`

**Interfaces:**
- Consumes: `<pr_description>`, optional `<linear_issue_body>`, optional `<plan_path>`, optional `<spec_path>`, optional `<roadmap_paths>`, full branch `<diff_path>`.
- Produces: `review-log-scope-honesty.md` with a checklist and, if drift exists, a `scope-drift-NNN` finding that the orchestrator can fix.

- [x] **Step 1: Extend `normalize_review_inputs.py` to gather scope inputs**

If `pr_description` mentions a Linear issue, or if `gh pr view` returns linked issues, fetch the issue body and save it as `linear_issue.txt`. If `.agents/plans/` has a plan whose name matches the PR title or branch, save its path. If a spec or roadmap file is referenced, save those paths. If none exist, the script still runs and the `scope-honesty` check only uses the PR body.

- [x] **Step 2: Write `check_scope_honesty.py`**

The script reads the PR body, issue body, plan, spec, and roadmaps (if present). It extracts the claimed in-scope and out-of-scope items. It then compares the actual branch `diff_path` to those items and produces `review-log-scope-honesty.md`. It records drift findings with `record_finding.py` and exits 0 when no drift. It must not require the orchestrator to hand-edit the log.

- [x] **Step 3: Update `node-scope-honesty.md` recipe**

The recipe becomes: run `check_scope_honesty.py --apply` with the state. If it exits 0, proceed to `reviewer-fast`. If it produces drift, the orchestrator either updates the PR/Linear/plan/spec to match the diff or updates the diff to match the documents, then re-runs scope-honesty before continuing.

- [x] **Step 4: Update `next_node.py` and `SKILL.md`**

Make the graph edge from `preflight` to `scope-honesty` to `reviewer-fast`. Update skill docs.

- [x] **Step 5: Run `ci --check` and commit**

Run `py -3 tools/run.py ci --check`. If clean, commit with `git commit -m "feat(iterative-review): make scope-honesty a concrete check"`.

### Task 3: Harden `record_*.py` scripts so hand-rolled helpers are unnecessary

**Files:**
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/scripts/record_finding.py`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/scripts/record_resolution.py`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/scripts/record_regression.py`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/scripts/record_blocker.py`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/SKILL.md` (examples)

**Interfaces:**
- Each script accepts either `--data '<json>'` or `--data-file <path>`.
- Each script validates the JSON schema before appending and prints a one-line confirmation.

- [x] **Step 1: Add `--data-file <path>` support to all four scripts**

Allow a JSON file (single object or array) to be passed instead of a raw `--data` string. Keep `--data` for backwards compatibility, but the help examples should show `--data-file`. The script reads the file, validates required keys, and appends to `findings.jsonl`/`resolutions.jsonl`/`regressions.jsonl`/`blockers.jsonl`.

- [x] **Step 2: Improve `--help` output to show the required schema**

`record_finding.py --help` should print the required keys, allowed severity values, and an example JSON. Same for the others. No hand-rolling should be required because the schema is discoverable.

- [x] **Step 3: Update `SKILL.md` examples**

Replace the inline JSON examples with `--data-file <path>` examples and a small example file.

- [x] **Step 4: Run `ci --check` and commit**

Run `py -3 tools/run.py ci --check`. If clean, commit with `git commit -m "fix(iterative-review): accept --data-file in record scripts and expose schema"`.

### Task 4: Reconcile the graph across all `node-*.md` recipes and `next_node.py`

**Files:**
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/references/node-*.md`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/scripts/next_node.py`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/SKILL.md`

- [x] **Step 1: Audit every `node-*.md` recipe**

For each node, verify:
- the `next_node.py` command examples use `--state` consistently (remove stray `--metrics`)
- the routing described in the recipe matches the edge in `next_node.py`
- the output artifact names and paths match the machine-managed file list
- there are no duplicate or conflicting instructions

- [x] **Step 2: Fix the `reviewer-fixes` vs `resolved-ledger` resolution recording conflict**

Pick one authority. `record_resolution.py` should be called once at `resolved-ledger` after the originating lens confirms the fix. Update both `node-reviewer-fixes.md` and `node-resolved-ledger.md` to say the same thing.

- [x] **Step 3: Fix the `new_issue` -> `metrics-track` routing bug**

Investigate why a clean `reviewer-fixes` pass routed to `metrics-track` in the #296 dogfood. The likely cause is `next_node.py` treating a resolved-but-still-in-queue finding as `new_issue` because the resolution had not yet been recorded in `rounds_per_finding`. The fix is to record the resolution at `reviewer-fixes` before `next_node.py` discovers the next node, or to make the routing look at `resolutions.jsonl` as well as `findings.jsonl`.

- [x] **Step 4: Run `ci --check` and commit**

Run `py -3 tools/run.py ci --check`. If clean, commit with `git commit -m "fix(iterative-review): reconcile node recipes and routing"`.

### Task 5: Keep scratch artifacts in sync with the working tree

**Files:**
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/scripts/start_review.py`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/scripts/normalize_review_inputs.py`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/scripts/next_node.py`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/scripts/compile_metrics.py`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/SKILL.md`

- [x] **Step 1: Add a `--resync` flag to `next_node.py` and/or `start_review.py`**

When called with `--resync --apply --state <path>`, the script re-reads the current `HEAD`, updates `review-state.json` `head_sha` and `pr.head_sha`, regenerates the full branch diff at `review-<base>..<head>.diff`, and re-runs `normalize_review_inputs`.

- [x] **Step 2: Make `compile_metrics.py` derive `head_sha` from `review-state.json` and `review-metrics.json`**

If `review-state.json` has been resynced, `compile_metrics.py` must use the new `head_sha` and not the stale one from `start_review.py`.

- [x] **Step 3: Update `SKILL.md` quick-start and node recipes**

Document when to use `next_node.py --resync --apply` (after rebases, after fix commits, after checking out an updated branch).

- [x] **Step 4: Run `ci --check` and commit**

Run `py -3 tools/run.py ci --check`. If clean, commit with `git commit -m "feat(iterative-review): resync scratch artifacts after working-tree changes"`.

### Task 6: Clean up `reviewer-fixes` re-dispatch and output

**Files:**
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/references/node-reviewer-fixes.md`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/references/reviewer-*.md`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/scripts/select_lenses.py`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/SKILL.md`

- [x] **Step 1: Standardize the `reviewer-fixes` output file and status line**

Each `reviewer-*.md` profile should, when run as a `reviewer-fixes` pass, write to `review-log-reviewer-<lens>-fixes.md` and end with the standard `reviewer-<lens>: clean` or `reviewer-<lens>: N issue(s)` status line. The `node-reviewer-fixes.md` recipe should explicitly reference `review-log-reviewer-<lens>-fixes.md` and interpret any non-`clean` result as a fail.

- [x] **Step 2: Make `select_lenses.py` (or a helper) re-select the originating lens for `reviewer-fixes`**

The `reviewer-fixes` node should be able to ask the tooling which lens to re-dispatch for a given `finding_id`. Avoid the orchestrator guessing.

- [x] **Step 3: Run `ci --check` and commit**

Run `py -3 tools/run.py ci --check`. If clean, commit with `git commit -m "fix(iterative-review): clean up reviewer-fixes re-dispatch and output"`.

### Task 7: Regenerate installed copies and dogfood on PR #295

**Files:**
- All modified `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/` files

- [x] **Step 1: Regenerate installed skill copies**

Run `py -3 .agents/skills/refreshing-installed-skills/scripts/refresh_installed_skills.py --apply` and `py -3 tools/run.py ci --check`.

- [x] **Step 2: Commit the regenerated installed copies and provenance**

Commit with the canonical pre-commit hooks.

- [x] **Step 3: Run `iterative-review` on PR #295 again from the new worktree**

Use `py -3 .agents/skills/iterative-review/scripts/start_review.py --pr 295 --apply` and follow the updated graph. Verify it reaches `ready` with fewer manual steps and no stale artifacts.

- [x] **Step 4: Push and flip to ready**

Push the branch and, if PR #295 is the target, flip it to ready.
