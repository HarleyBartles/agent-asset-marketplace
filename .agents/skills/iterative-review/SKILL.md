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

The canonical sequence, node responsibilities, and edge conditions are defined in `references/review-state-graph.md`. Read that file **before** you dispatch any subagent or decide which lenses apply. The body below is an annotated walkthrough, not a replacement for the graph. Most questions about ordering (e.g. which node runs before `lens-dispatch`, whether `strong-review` can be skipped, and what happens when a lens finds an issue) are answered by the graph.

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
- `references/review-log-orchestrator-self-review.md` for the prediction log template.
- `references/review-log-resolved-ledger.md` for the evidence file required by `final-strong`.
- The relevant `reviewer-*.md` lens profiles for the current repository.

The Devin Desktop agents search path is: user-global `~/.config/devin/agents/` (or `%APPDATA%\devin\agents\` on Windows), then `.devin/agents/`, then `.agents/agents/`. Discover `reviewer-*.md` files from that combined path; `.devin/agents/` and `.agents/agents/` take precedence over user-global.

## Setup

1. Determine `<base>` and `<branch>` (or `<head_sha>`) for the draft PR.
2. Resolve the off-repo scratch workspace by running `.agents/skills/subagent-workspace/scripts/sdd-workspace` with no plan file:
   - Bash: `bash .agents/skills/subagent-workspace/scripts/sdd-workspace`
   - PowerShell: `powershell .agents/skills/subagent-workspace/scripts/sdd-workspace.ps1`
   This prints a path like `<main-checkout>/../_agent-scratch/<branch>/`. Create an `iterative-review-<pr_number>` subdirectory inside it. All review inputs and logs live off-repo.
3. Materialize inputs in the off-repo `iterative-review-<pr_number>` directory:
   - `<diff_path>`: the full branch diff via `.agents/skills/subagent-workspace/scripts/review-package - <base> <branch> "$workspace/iterative-review-<pr_number>/review-<base7>..<head7>.diff"`.
   - `<pr_description>`: the PR title, body, and linked issue/spec context as a UTF-8 file.
   - Optional `<issue_context>`: Linear/GitHub issue or spec text as a UTF-8 file.
   - `<scan_findings>`: the consumer repo's canonical preflight output as a file. Use the command named in the consumer's `AGENTS.md` or `.devin/rules` and write the output to a UTF-8 file (e.g., `py -3 tools/run.py review-preflight --check` and `py -3 tools/run.py ci --check` for this repo).
4. Validate that every input file is valid UTF-8 (and, where applicable, without a BOM) before dispatching subagents. Subagents cannot read malformed inputs. If a file is not valid UTF-8, regenerate it from a known-UTF-8 source such as `review-package`/`review-package.ps1` rather than a raw shell redirect.
5. After `setup`, create an empty `review-metrics.json` in the off-repo scratch. At every `metrics-track`, `resolved-ledger`, and `blocked` node, update it. `next_node.py` and the `reviewer-strong` guard use this file as the source of truth for the graph state.



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
- The orchestrator owns the scope-honesty preflight, all verification, the `resolved-ledger`, and the final decision to flip the PR to ready. `implementer` subagents own the fix edits under the orchestrator's brief.
- All review inputs, logs, metrics, and fix-diffs are written to the off-repo scratch directory; they are never committed to the repo.
- CI must pass before leaving draft.

## Common Mistakes

- Treating the skill as a fixed list of rounds. Use the graph.
- Skipping `orchestrator-self-review` and dispatching lens reviewers immediately. That is the most expensive way to catch predictable issues.
- Using a clean `orchestrator-self-review` as an excuse to skip `lens-dispatch`, `lens-triage`, or `final-strong`. It is not a pass.
- Claiming subagents are unavailable and proceeding to `ready` without `lens-dispatch` or `final-strong`. If `run_subagent` cannot be used, the review is `blocked`.
- Skipping `re-preflight` after a fix. A fix can re-introduce deterministic issues.
- Skipping `regression-scan` for a non-trivial fix. A fix can cause a new issue in an adjacent area.
- Letting `reviewer-fixes` drift into a full branch review. Keep the input tightly scoped to the fix.
- Blindly applying reviewer findings without verification. Use `receiving-code-review` for each finding.
- Skipping CI after the reviewer loop. The reviewer "green" signal is not the draft/ready gate.
- Flipping a PR to ready without archiving the completed plan/spec/roadmap it implements. The ready state should represent the completed plan, including the moved planning artifacts.
