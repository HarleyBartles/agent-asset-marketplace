---
name: iterative-review
description: Use when a draft PR is ready for subagent review before being marked ready for CI and human review.
metadata:
  source-id: iterative-review
  source-path: codex-marketplace/plugins/superpowers-plus/skills/iterative-review/SKILL.md
  provenance-name: Iterative Review first-party skill
  source-category: first_party
  status: active
  owner: Harley Bartles
  scope: Use when a draft PR is ready for subagent review before being marked ready for CI and human review.
  use_when:
  - Use when a draft PR is ready for subagent review before being marked ready for CI and human review.
  do_not_use_when:
  - Do not use when the PR has no changes to review.
  - Do not use as a substitute for the repo's canonical CI preflight.
  related_skills:
  - requesting-code-review
  - receiving-code-review
  - handoff-gates
  - selecting-a-subagent
  - dispatching-parallel-agents
license: MIT
---

## Provenance

This skill is a first-party skill authored for this repository. It is not derived from an upstream snapshot.

## Before you start

Read `references/review-state-graph.md` first; it defines the canonical graph and routing. Then run the orchestrator below one node at a time.

# Iterative Review

Run the review state graph on a draft PR before it is marked ready for CI and human review.

## When to Use

Use when a draft PR exists and needs an automated subagent review loop before being marked ready for CI and human review.

## Core Pattern

Follow the `review-state-graph.md` reference. The graph routes the orchestrator through deterministic preflight, `orchestrator-self-review`, parallel `lens-dispatch`, `lens-triage`, fast `finding-fix` by an `implementer` for `blocking/important` lens findings, `re-preflight`, lens-aware `reviewer-fixes`, `resolved-ledger`, conditional `regression-scan`, and a final `reviewer-strong` `final-strong` pass. `trivial/deferred` findings are left for `final-strong` instead of forcing an early whole-branch review. Every finding records the node and round that discovered it. There are no fixed "Round N" steps.

## Required reading

- `selecting-a-subagent` skill for choosing lens profiles.
- `references/review-state-graph.md` for the canonical graph, node table, and edge conditions.
- `references/review-metrics-schema.json` for the metrics to collect.
- `references/review-log-orchestrator-self-review.md` for the filled orchestrator self-review log.
- `references/review-log-orchestrator-self-review-template.md` for the skeleton/template for that log.
- `references/review-log-resolved-ledger.md` for the evidence file required by `final-strong`.
- `references/node-*.md` for the per-node recipes. Do not read ahead; open only the `references/node-<node>.md` file named by `next_node.py`.
- The relevant `reviewer-*.md` lens profiles for the current repository.

The Devin Desktop agents search path is: user-global `~/.config/devin/agents/` (or `%APPDATA%\devin\agents\` on Windows), then `.devin/agents/`, then `.agents/agents/`. Discover `reviewer-*.md` files from that combined path; `.devin/agents/` and `.agents/agents/` take precedence over user-global.

## Following the graph

1. Determine `<base>` and `<branch>` (or `<head_sha>`) for the draft PR.
2. Create the off-repo scratch workspace and seed `review-state.json` in it (see `references/node-setup.md`).
3. Run the mechanical next-node discovery (read-only):
   ```
   py -3 .agents/skills/iterative-review/scripts/next_node.py --state <scratch_dir>/review-state.json
   ```
   Capture the first line of output as `<node>`.
4. (Optional) Inspect current status without mutating state:
   ```
   py -3 .agents/skills/iterative-review/scripts/next_node.py --state <scratch_dir>/review-state.json --status
   ```
5. (Optional) If the logs have run ahead of the saved `current_node`, resync state:
   ```
   py -3 .agents/skills/iterative-review/scripts/next_node.py --state <scratch_dir>/review-state.json --resync --apply
   ```
6. Validate and advance the router to the discovered node before running its recipe:
   ```
   py -3 .agents/skills/iterative-review/scripts/next_node.py --propose <node> --state <scratch_dir>/review-state.json
   ```
7. Open `references/node-<node>.md` for the just-proposed node and follow it exactly.
8. Return to step 3 after the node is done.
9. Stop when `next_node.py` prints `ready` or `blocked`.

## Recording `review-metrics.json`

At every `metrics-track` and at `ready`, `resolved-ledger`, or `blocked`, write or update `review-metrics.json` in the off-repo scratch. The schema is in `references/review-metrics-schema.json`. This file is evidence for:

- **Fast catch**: `findings_by_node.preflight` should dominate.
- **Early catch**: most lens/strong findings should appear at low `discovered_at_round` values.
- **No sloppy fixes**: `regressions` should be low relative to `rounds_per_finding`.
- **Tunable regressions**: the `regression_class` distribution tells us whether late findings are due to weak lens review (`outside-blast-radius`), shoddy same-lens fixes (`same-lens-blast-radius`), or cross-cutting regressions (`cross-lens-blast-radius`).

For every post-fix finding, set `regression_class` from the decision table in the design spec (`## Concrete regression_class assignment`). Also set `regression_of` on the `rounds_per_finding` entry for the new finding.

## Inputs the orchestrator must provide

- `<base>` and `<branch>` (or `<head_sha>`)
- `<pr_number>` or `<pr_description>`
- Optional `<issue_context>` for Linear/GitHub issue or spec text

## Invariants

- Follow the graph in `references/review-state-graph.md`. Do not follow a round list.
- The `final-strong` pass is reachable only through `lens-triage` or after all `blocking/important` findings are resolved; there is no edge from `setup`, `preflight`, `fast-fix`, or `orchestrator-self-review` directly to `final-strong`. If `lens-dispatch` is skipped, unavailable, or produces no logs, the review is `blocked`.
- This skill does not modify review files or PR state beyond the scope-honesty preflight.
- The orchestrator owns the scope-honesty preflight, the `orchestrator-self-review` pass, all verification, the `resolved-ledger`, and the final decision to flip the PR to ready. `implementer` subagents own the fix edits under the orchestrator's brief. `orchestrator-self-review` is orchestrator-only; no `reviewer-*`, `implementer`, or `subagent_explore` may be dispatched to perform it.
- All review inputs, logs, metrics, and fix-diffs are written to the off-repo scratch directory; they are never committed to the repo.
- CI must pass before leaving draft.

## Lens re-run scope

`lens-dispatch` runs at most once per review cycle. It dispatches every lens whose `## Applies to` rules match the PR.

When a finding is fixed, `finding-fix` -> `re-preflight` -> `reviewer-fixes` re-runs only the originating lens for that finding. Do not re-dispatch all lenses after a single fix; that is unnecessary churn and can introduce unrelated feedback late in the cycle.

## Machine-managed files

The following files in the off-repo scratch must be written only through the provided scripts. The orchestrator must not use `write` or `edit` on them:

- `review-state.json` - written by `next_node.py --propose` or `next_node.py --resync --apply`.
- `findings.jsonl`, `resolutions.jsonl`, `regressions.jsonl`, `blockers.jsonl` - written by `record_*.py` scripts.
- `lenses.jsonl` - written by `select_lenses.py --apply`.
- `review-log-orchestrator-self-review.md` - written by `record_orchestrator_log.py`.
- `review-metrics.json` - written by `compile_metrics.py`.

Lens subagents write their own `review-log-<lens>.md` files with `write` and end them with a one-line status. The `write` tool warning applies to orchestrator-authored files; it causes IDE buffer contention when a file is also open or being updated by a script.

## Common Mistakes

- Treating the skill as a fixed list of rounds. Use the graph.
- Skipping `orchestrator-self-review` and dispatching lens reviewers immediately. That is the most expensive way to catch predictable issues.
- Using a clean `orchestrator-self-review` as an excuse to skip `lens-dispatch`, `lens-triage`, or `final-strong`. It is not a pass.
- Delegating `orchestrator-self-review` to a subagent. This is an orchestrator-only, cheap mechanical pass. If the diff is too large to scan quickly, narrow to checklist patterns or proceed to `lens-dispatch` with a minimal prediction log; do not call a subagent.
- Claiming subagents are unavailable and proceeding to `ready` without `lens-dispatch` or `final-strong`. If `run_subagent` cannot be used, the review is `blocked`.
- Skipping `re-preflight` after a fix. A fix can re-introduce deterministic issues.
- Skipping `regression-scan` for a non-trivial fix. A fix can cause a new issue in an adjacent area.
- Letting `reviewer-fixes` drift into a full branch review. Keep the input tightly scoped to the fix.
- Blindly applying reviewer findings without verification. Use `receiving-code-review` for each finding.
- Skipping CI after the reviewer loop. The reviewer "green" signal is not the draft/ready gate.
- Flipping a PR to ready without archiving the completed plan/spec/roadmap it implements. The ready state should represent the completed plan, including the moved planning artifacts.
