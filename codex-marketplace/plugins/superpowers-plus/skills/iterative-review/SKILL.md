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

Run a multi-round subagent review loop on a draft PR before it is marked ready for CI and human review.

## When to Use

Use when a draft PR exists and needs an automated subagent review loop before being marked ready for CI and human review.

## Core Pattern

Parallel lens reviews of the full branch, then a `reviewer-strong` whole-branch design pass, then targeted `reviewer-fast` re-reviews of each fix, then a final `reviewer-strong` pass with all logs. The orchestrator applies all fixes and uses its own judgement on when the branch is green enough.

## Procedure

1. Determine the base ref (`<base>`) and the branch/head (`<branch>` or `<head_sha>`) for the draft PR.
2. **Scope-honesty preflight.** Before the reviewers see the code, compare the actual branch diff to the plan, any linked spec, and the PR title/body. If the implemented scope has expanded beyond what those documents describe, update them to match the real diff. Commit and push the scope-honesty update. The reviewers should read an honest description of scope, not discover scope creep line-by-line in the code.
3. Resolve the off-repo scratch workspace by running `.agents/skills/subagent-workspace/scripts/sdd-workspace` with no plan file:
   - Bash: `bash .agents/skills/subagent-workspace/scripts/sdd-workspace`
   - PowerShell: `powershell .agents/skills/subagent-workspace/scripts/sdd-workspace.ps1`
   This prints a path like `<main-checkout>/../_agent-scratch/<branch>/` (on Windows, `Z:\_agent-scratch\<branch>\`). Create an `iterative-review-<pr_number>` subdirectory inside it. All review inputs and logs live in that off-repo directory so they are never committed.
4. Materialize inputs as files the subagents can read in the off-repo `iterative-review-<pr_number>` directory:
   - `<diff_path>`: the review package from `.agents/skills/subagent-workspace/scripts/review-package - <base> <branch> "$workspace/iterative-review-<pr_number>/review-<base7>..<head7>.diff"` (use `-` for no plan file). The script writes it as UTF-8 with no BOM.
   - `<pr_description>`: the PR title, body, and any linked issue/spec context written to a file as UTF-8.
   - Optional `<issue_context>`: Linear/GitHub issue or spec text if linked, written to a file as UTF-8.
   - `<scan_findings>` (optional but strongly recommended): the output of the consumer repo's canonical preflight, written to a file. Do not hardcode the preflight command; use the command(s) named in the consumer repo's `AGENTS.md` or `.devin/rules`. Examples:
     - In this repo: `py -3 tools/run.py review-preflight --check --base-ref <base>` followed by `py -3 tools/run.py ci --check`.
     - In rooms-mostly: `scripts/ci-preflight.ps1 -Check` and the checks listed in its `AGENTS.md`.
     Capture the output so the lens reviewers can cross-check rather than rediscover the findings.
5. **Round 0 — orchestrator pre-emptive review.** Before dispatching subagent reviewers, the orchestrator performs a self-review of the full diff against the known-finding classes and lens profiles:
   - Read `.agents/skills/selecting-a-subagent/assets/reviewer-known-findings.md` (or the consumer repo's equivalent known-findings catalog) and the relevant `.agents/agents/reviewer-*.md` lens profiles.
   - For each lens, scan the diff and ask: *What would this lens flag that I can fix now with high confidence?*
   - Apply the predictable fixes and commit them. Record the predicted/fixed classes and the rationale in `review-log-orchestrator-prediction.md` in the off-repo scratch; this log is an input to the lens reviewers.
   - Re-run the consumer's canonical preflight and update `scan_findings` so the fixed classes are no longer in the report.
   - If no uncertain issues remain, the orchestrator may skip Round 1 and proceed directly to `handoff-gates` or CI. Otherwise, dispatch reviewers only for the classes the orchestrator could not resolve.
6. **Round 1 — parallel lens review.** Dispatch the lens reviewers in parallel, each with the full diff, PR description, `scan_findings`, and `review-log-orchestrator-prediction.md`:
   - `reviewer-security` writes `review-log-security.md`.
   - `reviewer-skills` (portable) writes `review-log-skills.md`.
   - `reviewer-marketplace` (repo-local) writes `review-log-marketplace.md`.
   - Any repo-specific lens profiles declared in the consumer's `AGENTS.md` or found as `.agents/agents/reviewer-*.md` overrides write `review-log-<lens>.md`.
   - In their prompts, explicitly instruct the reviewers to respect the `review-log-orchestrator-prediction.md` and not re-flag classes the orchestrator has already fixed; their value is in the classes the orchestrator marked as uncertain.
8. **Round 2 — `reviewer-strong` whole-branch pass.** Dispatch `reviewer-strong` with the full diff, PR description, `issue_context`, `scan_findings`, `review-log-orchestrator-prediction.md`, and all `review-log-*.md` files. It should combine the lens findings, look for gaps or contradictions, and review design/scope. It writes `review-log-strong-1.md`.
9. Merge the lens and strong logs into a single `review-log.md` with severity and file/line citations.
10. For each finding, the orchestrator verifies it, fixes it, and commits. Then re-run the consumer repo's canonical preflight over the post-fix range, materialize the fix review package (`.agents/skills/subagent-workspace/scripts/review-package - <pre-fix-sha> <post-fix-sha> "$workspace/iterative-review-<pr_number>/review-<pre-fix7>..<post-fix7>.diff"`), and update the relevant `review-log-*.md` with any new preflight hits.
11. **Round 3 — `reviewer-fast` re-review of the fix.** For each lens that raised the finding, dispatch `reviewer-fast` with the original finding, the prepared fix diff, and relevant slices of the full branch diff that the fix touches. Confirm the fix resolves the finding and catch regressions in the touched area only.
12. If `reviewer-fast` raises new issues, the orchestrator fixes them and returns to step 11.
13. **Round 4 — final `reviewer-strong` re-review.** Re-dispatch `reviewer-strong` with the whole branch diff, PR description, `review-log-orchestrator-prediction.md`, and the updated `review-log-*.md` files. Its job is a full branch review with added context of what was already addressed. It writes `review-log-strong-2.md`.
14. If the final `reviewer-strong` reports no blocking or important issues, the skill reports "reviewer-clean" and lists any minor/deferred items. The orchestrator then runs the repo's canonical CI preflight (`py -3 tools/run.py ci --check` here, or the consumer's equivalent) and flips the PR to ready only after a clean CI pass.

## Inputs the orchestrator must provide

- `<base>` and `<branch>` (or `<head_sha>`)
- `<pr_number>` or `<pr_description>`
- Optional `<issue_context>` for Linear/GitHub issue or spec text

## Invariants

- This skill does not modify review files or PR state beyond the scope-honesty preflight.
- The orchestrator owns the scope-honesty preflight, all fixes, and the final decision to flip the PR to ready.
- All review inputs, logs, and fix-diffs are written to the SDD off-repo scratch directory; they are never committed to the repo.
- CI must pass before leaving draft.

## Common Mistakes

- Naming subagent dispatch prompts `final`, `final final`, `final final final`, etc. Use `Round N` for every round, including the last one (e.g., `Round 4 — strong re-review of full branch`).
- Letting `reviewer-fast` drift into a full branch review. Keep the dispatch prompt and the fix diff tightly scoped.
- Blindly applying reviewer findings without verification. Use `receiving-code-review` for each finding.
- Skipping CI after the reviewer loop. The reviewer "green" signal is not the draft/ready gate.
- Forgetting to re-run the consumer's preflight after each fix. A fix can re-introduce a pattern the preflight catches.
