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

# Iterative Review

Run the review state graph on a draft PR before it is marked ready for CI and human review.

## When to Use

Use when a draft PR exists and needs an automated subagent review loop before being marked ready for CI and human review.

## Core Pattern

Follow the `review-state-graph.md` reference. The graph routes the orchestrator through deterministic preflight, orchestrator prediction, parallel lens review, `reviewer-strong` whole-branch review, fix, re-preflight, targeted re-review, and conditional regression-scan. Every finding records the node and round that discovered it. There are no fixed "Round N" steps.

## Required reading

- `selecting-a-subagent` skill for choosing lens profiles.
- `references/review-state-graph.md` for the canonical graph, node table, and edge conditions.
- `references/review-metrics-schema.json` for the metrics to collect.
- `references/review-log-orchestrator-self-review.md` for the prediction log template.
- The relevant `.agents/agents/reviewer-*.md` lens profiles for the current repository.

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

## Following the graph

Read `references/review-state-graph.md` and execute the graph. This section is an annotated walkthrough, not a replacement for the graph.

### `setup`

Collect the inputs above. The orchestrator owns the workspace.

After writing `scan_findings`, `pr_description`, and any optional `issue_context` files, run the UTF-8 backstop helper to normalize any inputs that shell redirects or `Tee-Object` may have emitted as UTF-16 or UTF-8-with-BOM:

```
py -3 .agents/skills/iterative-review/scripts/normalize_review_inputs.py --apply <scratch_dir>
```

Replace `<scratch_dir>` with the off-repo workspace path. This rewrites all `.md`, `.txt`, and `.json` files to plain UTF-8 in place.

### `preflight`

Run the consumer's canonical preflight on the branch. Do not proceed until `ci --check` or its equivalent is clean or its findings are converted to a `fast-fix` and re-checked.

### `fast-fix`

If the preflight reports deterministic findings, fix them and return to `preflight`. Preflight findings are the cheapest to catch and the cheapest to fix.

### `scope-honesty`

Compare the branch diff to the plan, spec, PR body, and linked issues. If the implemented scope has drifted, update the documents to match the real diff or fix the diff to match the documents. Commit the scope-honesty update. Reviewers must read an honest description of scope, not discover scope creep line-by-line.

### `orchestrator-self-review`

This is the cheapest non-deterministic review. For each relevant `.agents/agents/reviewer-*.md` profile, read the `## Checklist` and the `## Applies to` section, then apply the checklist to the full diff mechanically. Use `## Applies to` only to decide relevance; the prediction pass still scans the full diff for checklist patterns. Fix what you can fix with high confidence. Record uncertain items in `review-log-orchestrator-self-review.md` in the off-repo scratch. Update `scan_findings` after the fixes.

**`orchestrator-self-review` is not a pass.** A clean orchestrator-self-review means the predictable issues are already fixed and the remaining known-unknowns are documented. It does **not** mean the PR is ready. Always proceed to `lens-dispatch` unless the PR has zero changed files or the consumer's CI preflight alone is the required gate for that PR.

### `lens-dispatch`

This node is mandatory. Dispatch only the lens reviewers whose `## Applies to` rules match the PR, plus the mandatory `reviewer-strong` whole-branch pass.

1. Discover every `.agents/agents/reviewer-*.md` file in the consumer repo. This set is the portable profiles shipped by the marketplace pack plus any repo-local `.agents/agents/reviewer-*.md` overrides.
2. For each lens profile, read its `## Applies to` section. Match the rules in this order:
   - If an `inputs` entry is provided by the orchestrator (e.g. `<plan_path>` for `reviewer-plans`), dispatch the lens.
   - If a `globs` pattern matches a changed file in the diff, dispatch the lens.
   - If a `keywords` string appears in the diff or in `<pr_description>`, dispatch the lens.
3. Build the input package for each matching lens: full branch `<diff_path>`, `<pr_description>`, `<scan_findings>`, `review-log-orchestrator-self-review.md`, and any lens-specific inputs (`<plan_path>`, `<spec_path>`, `<roadmap_path>` for `reviewer-plans`).
4. Use `run_subagent` to dispatch each selected lens. Read the corresponding `.agents/agents/reviewer-*.md` profile and use its content as the subagent task. Set the off-repo workspace as the subagent's working directory.
5. `reviewer-strong` always runs after the lens reviews with the full diff, PR description, and all `review-log-<lens>.md` files.

If no lens matches the PR, still dispatch `reviewer-strong` for the whole-branch pass.

If you cannot run subagents (e.g. `run_subagent` is unavailable, fails, or is explicitly stopped), this is a `blocked` node — do not proceed to `ready` and do not claim the review is complete. Record the blocker and hand to a human.

Lens reviewers should use the prediction log as the primary checklist and not re-flag what the orchestrator already fixed. Each lens writes `review-log-<lens>.md`.

### `strong-review`

This node is mandatory. Before dispatching `reviewer-strong`, re-run the UTF-8 backstop helper on the scratch directory to ensure every lens report is plain UTF-8:

```
py -3 .agents/skills/iterative-review/scripts/normalize_review_inputs.py --apply <scratch_dir>
```

Then dispatch `reviewer-strong` with the full diff, PR description, `issue_context`, `scan_findings`, `review-log-orchestrator-self-review.md`, and all `review-log-*.md` files. Its job is to combine lens findings, look for gaps and contradictions, and review design/scope. It writes `review-log-strong.md`.

Use `run_subagent` with the `.agents/agents/reviewer-strong.md` profile. `reviewer-strong` must always see the lens logs; do not let it run on the diff alone.

If `reviewer-strong` reports `reviewer-strong: clean` and the preflight is clean, proceed to `ready`. Otherwise, proceed to `metrics-track`.

If you cannot run `reviewer-strong` or any lens did not complete, this is `blocked`; do not proceed to `ready`.

### `metrics-track`

For each finding, record the node that discovered it, the round, the lens, and the severity in `review-metrics.json`. This is an evidence checkpoint, not a gate. It does not block.

### `finding-fix`

For each finding, use `receiving-code-review` to verify it, then fix it. Commit the fix. The fix should be narrow.

### `re-preflight`

Re-run the consumer's canonical preflight over the post-fix range. If it reports new deterministic issues, go to `fast-fix`. If it is clean, go to `targeted-re-review`.

### `targeted-re-review`

Before spending a full whole-branch `reviewer-strong` pass, dispatch `reviewer-fast` with a tight scope:
- the original finding,
- the fix diff (e.g. `HEAD~N..HEAD` or `origin/main..HEAD` if the fixes are the latest commits),
- the relevant slice of the full branch diff.

Use `reviewer-fast` to verify the original finding is resolved and to look for obvious new issues in the fix. Do not broaden into a whole-branch review here.

Confirm the original finding is resolved. Then:
- If the fix is trivial (single file, same concern, no cross-cutting impact) and `reviewer-fast` is clean, go to `strong-review`.
- If the fix is non-trivial (multi-file, generated surfaces, security/tooling boundary, public interface change) or `reviewer-fast` finds any new issue, go to `regression-scan`.

### `regression-scan`

Widen the scope to the fix and immediate surrounding area. First dispatch `reviewer-fast` on that widened diff to catch cheap regressions. If `reviewer-fast` is clean, go to `strong-review` for the final whole-branch pass. If `reviewer-fast` finds a new issue, dispatch `reviewer-strong` on the touched area to confirm and classify it; then return to `metrics-track` so it is recorded as a regression.

### `ready`

When `strong-review` reports `reviewer-strong: clean` and the preflight is clean:

1. Run `py -3 tools/run.py ci --check` (or the consumer's equivalent). Do not proceed if it fails.
2. If the PR completes the plan/spec/roadmap it set out to implement, archive the completed planning artifacts per `.agents/runbooks/completing-plans.md`:
   - `git mv .agents/plans/<plan-name>.md .agents/plans/completed/`
   - `git mv .agents/specs/<spec-name>.md .agents/specs/completed/`
   - Move any related roadmaps or research files referenced by the plan.
   - Run `py -3 tools/heal_archive_links.py --apply`, `py -3 tools/run.py mesh --apply`, and `py -3 tools/run.py marketplace --apply`.
   - Re-run `py -3 tools/run.py ci --check` after the archive step.
   - Commit the archive with `git commit -m "archive: complete <plan-name>"`.
3. Only then flip the PR from draft to ready.

### `blocked`

Use only when the orchestrator cannot resolve a contested or load-bearing finding. Record the blocker in `review-metrics.json` and hand to a human. The human may say "carry on"; if so, resume from `metrics-track`.

## Recording `review-metrics.json`

At every `metrics-track` and at `ready` or `blocked`, write or update `review-metrics.json` in the off-repo scratch. The schema is in `references/review-metrics-schema.json`. This file is evidence for:

- **Fast catch**: `findings_by_node.preflight` should dominate.
- **Early catch**: most lens/strong findings should appear at low `discovered_at_round` values.
- **No sloppy fixes**: `regressions` should be low relative to `rounds_per_finding`.

## Inputs the orchestrator must provide

- `<base>` and `<branch>` (or `<head_sha>`)
- `<pr_number>` or `<pr_description>`
- Optional `<issue_context>` for Linear/GitHub issue or spec text

## Invariants

- Follow the graph in `references/review-state-graph.md`. Do not follow a round list.
- This skill does not modify review files or PR state beyond the scope-honesty preflight.
- The orchestrator owns the scope-honesty preflight, all fixes, and the final decision to flip the PR to ready.
- All review inputs, logs, metrics, and fix-diffs are written to the off-repo scratch directory; they are never committed to the repo.
- CI must pass before leaving draft.

## Common Mistakes

- Treating the skill as a fixed list of rounds. Use the graph.
- Skipping `orchestrator-self-review` and dispatching lens reviewers immediately. That is the most expensive way to catch predictable issues.
- Using a clean `orchestrator-self-review` as an excuse to skip `lens-dispatch` or `strong-review`. It is not a pass.
- Claiming subagents are unavailable and proceeding to `ready` without `lens-dispatch` or `strong-review`. If `run_subagent` cannot be used, the review is `blocked`.
- Skipping `re-preflight` after a fix. A fix can re-introduce deterministic issues.
- Skipping `regression-scan` for a non-trivial fix. A fix can cause a new issue in an adjacent area.
- Letting `reviewer-fast` or `targeted-re-review` drift into a full branch review. Keep the input tightly scoped to the fix.
- Blindly applying reviewer findings without verification. Use `receiving-code-review` for each finding.
- Skipping CI after the reviewer loop. The reviewer "green" signal is not the draft/ready gate.
- Flipping a PR to ready without archiving the completed plan/spec/roadmap it implements. The ready state should represent the completed plan, including the moved planning artifacts.
