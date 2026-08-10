# Iterative review skill — state/router split and ergonomic improvements

## Status

- Plan 1 (state/router split and record scripts) is implemented and ready to merge in PR #287, head `c1e59ac4`.
- The `iterative-review` skill was dogfooded on this PR and reached `reviewer-strong: clean`.

## Goal

Fix the `iterative-review` skill's core design flaw: `review-metrics.json` is both the router state and the generated metrics evidence file. This causes hand-editing contention and makes the graph fragile. After the split, add a small set of ergonomic improvements that make the skill easier for an orchestrator to follow and recover from mistakes.

## Problem

`review-metrics.json` currently holds:

- **Routing state**: `current_node`, `previous_node`, `non_trivial_fix`, `contested`, `fix_round`.
- **Metrics evidence**: `findings_by_node`, `rounds_per_finding`, `regressions`, `total_rounds`.

Node recipes are told to edit `review-metrics.json` directly to satisfy `next_node.py`. That is the write-contention path: a file that the agent must hand-edit is also the file that the mechanical router reads and writes. When the agent deviates, the only recovery is to hand-fix the same contested file.

In addition, the skill has accumulated ergonomic gaps: no `status` command, no resync, artifact-agnostic `--propose`, a stale `review-metrics-schema.json`, a hard 4-round cap, and manual lens selection.

## Design

### State vs. metrics split

Introduce two files with one writer each:

- **`review-state.json`** — the canonical router state. Written **only** by `next_node.py --propose` (or by `next_node.py` when bootstrapped from `setup`). It contains:
  - `current_node`, `previous_node`
  - `round`, `max_fix_rounds`
  - `non_trivial_fix`, `contested`, `blocked_class`
  - `pr` (branch, base, head_sha, pr_number)
  - `scratch_dir`, `ledger_path`
- **`review-metrics.json`** — a **generated** aggregate. No node recipe edits it. Built by `compile_metrics.py` from `review-state.json` and the log files.
- **Log files in `<scratch_dir>/`**:
  - `findings.jsonl` — one line per `record_finding.py` call.
  - `resolutions.jsonl` — one line per `record_resolution.py` call.
  - `regressions.jsonl` — one line per `record_regression.py` call.
  - `blockers.jsonl` — one line per `record_blocker.py` call.

`next_node.py` reads `review-state.json` and the log files to discover the allowed next node. `compile_metrics.py` reads the same inputs and writes `review-metrics.json` in a single, idempotent pass. `resolved_ledger.py` remains the evidence gate and writes `review-log-resolved-ledger.md` only.

### Record scripts

Node recipes stop editing JSON and call dedicated scripts:

| Script | Action | Appends to |
|---|---|---|
| `record_finding.py` | Records a newly discovered finding | `findings.jsonl` |
| `record_resolution.py` | Marks a finding resolved | `resolutions.jsonl` |
| `record_regression.py` | Records a regression tied to a fix | `regressions.jsonl` |
| `record_blocker.py` | Records a contested or load-bearing blocker | `blockers.jsonl` |

Each script takes a small JSON object, validates it against a tiny schema, and appends one line. They are idempotent and safe to call repeatedly.

### Record script CLI contract

All record scripts follow the repo's helper script contract (`--help`, `--check` exits 0). Each appends to the `.jsonl` file named in `review-state.json` (`scratch_dir`):

| Script | CLI | Appends to | JSON shape |
|---|---|---|---|
| `record_finding.py` | `--state <review-state.json> --data <json>` | `findings.jsonl` | `finding_id`, `lens`, `discovered_at_node`, `discovered_at_round`, `severity` |
| `record_resolution.py` | `--state <review-state.json> --data <json>` | `resolutions.jsonl` | `finding_id`, `resolved_at_node`, `resolved_at_round` |
| `record_regression.py` | `--state <review-state.json> --data <json>` | `regressions.jsonl` | `fix_for`, `new_finding`, `discovered_at_node`, `discovered_at_round`, `regression_class`, `severity` |
| `record_blocker.py` | `--state <review-state.json> --data <json>` | `blockers.jsonl` | `finding_id`, `blocker_class` (`contested` / `tool-blocked`) |
| `compile_metrics.py` | `--state <review-state.json> --metrics <review-metrics.json>` | — | Reads `review-state.json` + `.jsonl` logs and writes the aggregate `review-metrics.json` |

`compile_metrics.py` is a pure compiler: it never mutates state or logs. A planning agent can run `compile_metrics.py` to refresh `review-metrics.json` without risk.

### `next_node.py` changes

- `--metrics` continues to read `review-metrics.json` for backward-compatible discovery, but the canonical state is now `review-state.json`.
- New `--state <path>` reads `review-state.json`.
- `--propose` validates both graph state and required artifacts, then writes the new `review-state.json`.
- New `--status` prints current node, next allowed, unresolved finding count, ledger status, and the last few log events without mutating state.
- New `--resync` compares the log files and state, reports drift, and offers to repair the state pointer if the actual work has run ahead.

### Schema cleanup

- Add `review-state-schema.json` for the new router file.
- Fix `review-metrics-schema.json`:
  - Add `deferred` to `severity` enum.
  - Remove `resolved_at_node` and `resolved_at_round` from required fields until resolution.
  - Add `regression_of` to `regressions` items.
  - Make `total_rounds` a generated field, not a hand-written one.

## Scope

This design is the umbrella for a **3-plan epic**:

### Plan 1 — State/router split and record scripts

- Create `review-state-schema.json`.
- Add `record_finding.py`, `record_resolution.py`, `record_regression.py`, `record_blocker.py`.
- Add `compile_metrics.py` to generate `review-metrics.json` from state and logs.
- Refactor `next_node.py` to use `review-state.json` and the log files.
- Update `update_review_metrics.py` to be a thin wrapper over `compile_metrics.py` for the orchestrator.
- Update every `references/node-*.md` recipe to call the record scripts instead of editing `review-metrics.json`.
- Regenerate `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/` and pass `py -3 tools/run.py ci --check`.

### Plan 2 — Ergonomic and reliability improvements

- Add `next_node.py --status`.
- Add `next_node.py --resync`.
- Make `--propose` artifact-aware (check required log files before state advance).
- Fix `review-metrics-schema.json` inconsistencies.
- Move `max_fix_rounds` into `review-state.json` and make round cap tunable per finding/severity.
- Allow `reviewer-fixes` to batch multiple findings from the same lens within the same blast radius.
- Distinguish `contested` from `tool-blocked` in `blockers.jsonl` and `next_node.py` routing.

### Plan 3 — Lens dispatch and final polish

- Add `select_lenses.py` to read `reviewer-*.md` profiles and diff, emit the lens dispatch list.
- Add `references/review-log-orchestrator-self-review-template.md`.
- Update `node-lens-dispatch.md` to use `select_lenses.py`.
- Add a focused test suite for `next_node.py` and the record scripts.
- Final documentation and skill surface refresh.

## Non-goals

- Do not change the graph topology (nodes/edges) or the reviewer lens profiles.
- Do not rewrite `reviewer-strong.md` or the `final-strong` guard contract.
- Do not change the `ci --check` contract for consumers.
- Do not remove `review-metrics.json`; it becomes a generated evidence file.

## Validation

- `py -3 tools/run.py ci --check` passes after each plan.
- A manual `next_node.py` walkthrough on a trivial synthetic `review-state.json` + logs advances through the expected nodes.
- No `review-metrics.json` hand-editing instructions remain in the node recipes.
- `compile_metrics.py` produces a `review-metrics.json` that matches the fixed schema.

## Out of scope

- Linear/Github issue automation.
- Changing the subagent profile format.
- New lenses or new graph nodes.

## Consumer check

The canonical source lives in `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/`. The installed copy in `.agents/skills/iterative-review/` is regenerated with `py -3 tools/run.py installed-skills --apply`. Record scripts and `next_node.py` must run from the installed layout, using paths relative to the script location and the consumer's `review-state.json` in the off-repo scratch workspace.
