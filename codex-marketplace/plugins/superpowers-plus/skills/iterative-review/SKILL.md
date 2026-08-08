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

## Following the graph

Read `references/review-state-graph.md` and execute the graph. This section is an annotated walkthrough, not a replacement for the graph.

### `setup`

Collect the inputs above. The orchestrator owns the workspace.

After writing `scan_findings`, `pr_description`, and any optional `issue_context` files, run the UTF-8 backstop helper to normalize any inputs that shell redirects or `Tee-Object` may have emitted as UTF-16 or UTF-8-with-BOM:

```
py -3 .agents/skills/iterative-review/scripts/normalize_review_inputs.py --apply <scratch_dir>
```

Replace `<scratch_dir>` with the off-repo workspace path. This rewrites all `.md`, `.txt`, and `.json` files to plain UTF-8 in place.

### `next-node`

Before every `run_subagent` dispatch, call the routing validator to confirm the proposed node is allowed by the graph:

```
py -3 .agents/skills/iterative-review/scripts/next_node.py --propose <node> --metrics <scratch_dir>/review-metrics.json
```

- If it exits 0, dispatch is allowed.
- If it exits 1, the orchestrator must not dispatch the subagent and must route to the allowed node printed in the output.
- If no `--propose` is given, the script prints the single allowed next node.

The orchestrator may also call `next_node.py` without `--propose` at the start of each turn to discover the next node. The validator is the mechanical source of truth for the graph; do not override it.

### `preflight`

Run the consumer's canonical preflight on the branch. Do not proceed until `ci --check` or its equivalent is clean or its findings are converted to a `fast-fix` and re-checked.

### `fast-fix`

If the preflight reports deterministic findings, fix them and return to `preflight`. Preflight findings are the cheapest to catch and the cheapest to fix.

### `scope-honesty`

Compare the branch diff to the plan, spec, PR body, and linked issues. If the implemented scope has drifted, update the documents to match the real diff or fix the diff to match the documents. Commit the scope-honesty update. Reviewers must read an honest description of scope, not discover scope creep line-by-line.

### `orchestrator-self-review`

This is the cheapest non-deterministic review. For each relevant `reviewer-*.md` profile, read the `## Checklist` and the `## Applies to` section, then apply the checklist to the full diff mechanically. Use `## Applies to` only to decide relevance; the prediction pass still scans the full diff for checklist patterns. Fix what you can fix with high confidence. Record uncertain items in `review-log-orchestrator-self-review.md` in the off-repo scratch. Update `scan_findings` after the fixes.

**`orchestrator-self-review` is not a pass.** A clean orchestrator-self-review means the predictable issues are already fixed and the remaining known-unknowns are documented. It does **not** mean the PR is ready. Always proceed to `lens-dispatch` unless the PR has zero changed files or the consumer's CI preflight alone is the required gate for that PR.

### `lens-dispatch`

This node is mandatory. Dispatch only the lens reviewers whose `## Applies to` rules match the PR. Do not include the whole-branch `reviewer-strong` here; that is the `final-strong` pass after all `blocking/important` findings are resolved.

1. Discover every `reviewer-*.md` file in the Devin Desktop agents search path (`~/.config/devin/agents/` / `%APPDATA%\devin\agents\`, `.devin/agents/`, and `.agents/agents/`). This set is the portable profiles shipped by the marketplace pack plus any user or repo-local `reviewer-*.md` overrides.
2. For each lens profile, read its `## Applies to` section. Match the rules in this order:
   - If an `inputs` entry is provided by the orchestrator (e.g. `<plan_path>` for `reviewer-plans`), dispatch the lens.
   - If a `globs` pattern matches a changed file in the diff, dispatch the lens.
   - If a `keywords` string appears in the diff or in `<pr_description>`, dispatch the lens.
3. Build the input package for each matching lens: full branch `<diff_path>`, `<pr_description>`, `<scan_findings>`, `review-log-orchestrator-self-review.md`, and any lens-specific inputs (`<plan_path>`, `<spec_path>`, `<roadmap_path>` for `reviewer-plans`). Assign each lens a concrete `<log_path>` such as `$scratch/review-log-<lens>.md`.
4. Use `run_subagent` to dispatch each selected lens. Read the corresponding `reviewer-*.md` profile and use its content as the subagent task. Pass the `<log_path>` in the subagent `task` so the reviewer writes to that exact file. Set the off-repo workspace as the subagent's working directory.

If no lens matches the PR, still continue to `lens-triage` with the orchestrator-self-review log; `final-strong` will then perform the first whole-branch review.

If you cannot run subagents (e.g. `run_subagent` is unavailable, fails, or is explicitly stopped), this is a `blocked` node — do not proceed to `ready` and do not claim the review is complete. Record the blocker and hand to a human.

Lens reviewers should use the prediction log as the primary checklist and not re-flag what the orchestrator already fixed. Each lens writes `review-log-<lens>.md`.

### `lens-triage`

After all lens subagents complete, run the UTF-8 backstop helper on the scratch directory to ensure every lens report is plain UTF-8:

```
py -3 .agents/skills/iterative-review/scripts/normalize_review_inputs.py --apply <scratch_dir>
```

Then classify every finding from the lens reports:
- `blocking/important` — enter the fast fix loop: go to `metrics-track` then `finding-fix`.
- `trivial/deferred` — the fix is optional or cosmetic; leave it for `final-strong` and go to `final-strong` now.
- `contested` or `load-bearing` — the orchestrator cannot resolve it safely; go to `blocked`.
- `clean` (no lens findings) — go to `final-strong`.

The orchestrator does not dispatch a subagent at `lens-triage`. It is a routing decision based on the lens logs and the `## Checklist` severity language in each `review-log-<lens>.md`.

### `metrics-track`

For each finding, record the node that discovered it, the round, the lens, and the severity in `review-metrics.json`. This is an evidence checkpoint, not a gate. It does not block.

### `finding-fix`

For each finding, the orchestrator first uses `receiving-code-review` to verify it. Then it builds a task brief and dispatches an `implementer` subagent:

- `original_finding` — the exact finding text and severity, with file and line citations.
- `lens` — the originating `reviewer-*.md` lens, e.g. `reviewer-security`.
- `lens_checklist` — the `## Checklist` section from that lens profile.
- `diff_slice` — the relevant slice of the full branch diff that the finding touches.
- `fix_constraints` — what not to break, which tests to run, and the consumer's `ci --check` command.

The `implementer` edits, runs the consumer's preflight, and commits. The orchestrator verifies the commit and the report, then moves to `re-preflight`.

Use `implementer` for rounds 1–3. If a finding fails `reviewer-fixes` three times, escalate to `implementer-strong` for round 4. If it still fails, route to `blocked`.

### `re-preflight`

Re-run the consumer's canonical preflight over the post-fix range. If it reports new deterministic issues, go to `fast-fix`. If it is clean, go to `reviewer-fixes`.

### `reviewer-fixes`

Before spending a full whole-branch `reviewer-strong` pass, dispatch `reviewer-fixes` with the following lens-aware package and a concrete `<log_path>` (e.g. `$scratch/review-log-fixes.md`):
- `original_finding` — the issue the fix is addressing.
- `fix_diff_path` — the prepared fix diff (`git diff <pre-fix-sha>...<post-fix-sha>`).
- `full_diff_slice_path` — the relevant slices of the full branch diff that the fix touches (the blast radius).
- `lens` — the originating `reviewer-*.md` lens.
- `lens_checklist` — the `## Checklist` from that lens.
- `<log_path>` where `reviewer-fixes` must use the `write` tool to write its report.

`reviewer-fixes` verifies the original finding is resolved and applies the originating lens's `## Checklist` to the blast radius only. It is not a whole-branch review.

Confirm the original finding is resolved. Then:
- If the original finding is fixed and `reviewer-fixes` is clean, go to `resolved-ledger`.
- If the original finding is not fixed, go back to `finding-fix` for the same finding.
- If `reviewer-fixes` finds a new same-lens/blast-radius issue, record it in `metrics-track` with `regression_class: same-lens-blast-radius`.
- If the fix is non-trivial (multi-file, generated surfaces, security/tooling boundary, public interface change), go to `regression-scan` even if `reviewer-fixes` is clean.

### `regression-scan`

For non-trivial or cross-cutting fixes, widen the scope to the fix and immediate surrounding area. Dispatch `reviewer-strong` on the touched area with `<log_path>` set to `$scratch/review-log-strong.md`. Its job is to confirm and classify any new issue the fix introduced.

If `reviewer-strong` on the touched area is clean, go to `resolved-ledger`. If it finds a new issue, classify it:
- `same-lens-blast-radius` if the issue is in the same lens and in the blast radius.
- `cross-lens-blast-radius` if the issue is in a different lens and in the blast radius.
- `outside-blast-radius` if the issue is outside the blast radius.

Record the new finding in `metrics-track` with `regression_class` and `regression_of` set to the original finding, then return to `finding-fix`.

### `resolved-ledger`

This is an orchestrator bookkeeping node, not a subagent dispatch. When `reviewer-fixes` or `regression-scan` is clean, mark the original finding `resolved` and record the `resolved_at_node` and `resolved_at_round` in `review-metrics.json`.

When the queue is empty, run the resolved-ledger evidence gate before proceeding to `final-strong`:

```
py -3 .agents/skills/iterative-review/scripts/resolved_ledger.py --apply --metrics <scratch_dir>/review-metrics.json
```

This command writes `review-log-resolved-ledger.md` only when every `important`/`blocking` finding has a `resolved_at_node` and `regressions` is empty. If the command exits 1, do not proceed to `final-strong` and return to `finding-fix` or `regression-scan`.

If more findings remain in the queue, choose the next one and go to `finding-fix`. If the queue is empty, go to `resolved-ledger` then `final-strong`.

### `final-strong`

Run one whole-branch `reviewer-strong` pass after all `blocking/important` findings are resolved. It also covers any `trivial/deferred` findings the `lens-triage` decided to defer. Its job is to confirm there are no remaining gaps, contradictions, or design issues.

Before dispatching `reviewer-strong`, run the `next_node` validator with the exact node you intend to dispatch:

```
py -3 .agents/skills/iterative-review/scripts/next_node.py --propose final-strong --metrics <scratch_dir>/review-metrics.json
```

If it exits 1, the orchestrator must not dispatch `reviewer-strong` and must route to the allowed node instead. If it exits 0, build the `reviewer-strong` input package with the full branch diff, PR description, all lens logs, `review-log-resolved-ledger.md`, `review-metrics.json`, and `<log_path>`.

If `reviewer-strong` reports `reviewer-strong: clean` and the preflight is clean, go to `closeout`. If it reports findings, go to `metrics-track` to start a new fix loop. If it reports a contested or load-bearing finding, go to `blocked`.

### `closeout`

After `reviewer-strong: clean`, decide whether the PR closes the plan/spec/roadmap it set out to implement. If it does, archive the completed planning artifacts per `.agents/runbooks/completing-plans.md` before flipping the PR to ready:

1. Identify the plan and spec named in the PR body, linked issues, or the branch's `.agents/plans/` and `.agents/specs/` files.
2. Confirm the plan is complete: every top-level checkbox is checked or the plan records the implementation PR.
3. `git mv .agents/plans/<plan-name>.md .agents/plans/completed/`
4. If the plan lists a spec: `git mv .agents/specs/<spec-name>.md .agents/specs/completed/`
5. Move any related roadmaps or research files referenced by the plan.
6. Run `py -3 tools/heal_archive_links.py --apply` and `py -3 tools/check_archive_links.py`.
7. Run `py -3 tools/run.py mesh --apply` and `py -3 tools/run.py marketplace --apply`.
8. Run `py -3 tools/run.py ci --check`. Do not proceed if it fails.
9. Commit the archive with `git commit -m "archive: complete <plan-name>"`.

If the PR does not close any plan/spec/roadmap, skip the move and go to `ready`.

### `ready`

After `closeout` (with or without archive moves):

1. Run `py -3 tools/run.py ci --check` (or the consumer's equivalent). Do not proceed if it fails.
2. Flip the PR from draft to ready with `gh pr ready <pr_number>`.
3. Wait for remote CI to pass. Use `gh pr checks <pr_number> --watch` or the equivalent consumer command. Do not merge until the PR is green.

### `blocked`

Use only when the orchestrator cannot resolve a contested or load-bearing finding. Record the blocker in `review-metrics.json` and hand to a human. The human may say "carry on"; if so, resume from `metrics-track`.

If `next_node.py` or `resolved_ledger.py` returns a `BLOCKED` result, treat that as a graph error: do not override it, do not dispatch `final-strong` out of order, and do not claim the review is complete. Resume from the allowed node.

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
