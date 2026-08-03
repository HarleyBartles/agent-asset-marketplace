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
license: MIT
---

## Provenance

This skill is a first-party skill authored for this repository. It is not derived from an upstream snapshot.

# Iterative Review

Run a multi-round subagent review loop on a draft PR before it is marked ready for CI and human review.

## When to Use

Use when a draft PR exists and needs an automated subagent review loop before being marked ready for CI and human review.

## Core Pattern

Strong review of the full branch, then a fast re-review of each fix, then a final strong re-review of the full branch with knowledge of earlier issues and fixes. The orchestrator applies all fixes and uses its own judgement on when the branch is green enough.

## Procedure

1. Determine the base ref (`<base>`) and the branch/head (`<branch>` or `<head_sha>`) for the draft PR.
2. **Scope-honesty preflight.** Before the reviewer sees the code, compare the actual branch diff to the plan, any linked spec, and the PR title/body. If the implemented scope has expanded beyond what those documents describe, update them to match the real diff. Commit and push the scope-honesty update. The reviewer should read an honest description of scope, not discover scope creep line-by-line in the code.
3. Resolve the off-repo scratch workspace by running `subagent-workspace/scripts/sdd-workspace` with no plan file:
   - Bash: `bash .agents/skills/subagent-workspace/scripts/sdd-workspace`
   - PowerShell: `powershell .agents/skills/subagent-workspace/scripts/sdd-workspace.ps1`
   This prints a path like `<main-checkout>/../_agent-scratch/<branch>/` (on Windows, `Z:\_agent-scratch\<branch>\`). Create an `iterative-review-<pr_number>` subdirectory inside it. All review inputs and logs live in that off-repo directory so they are never committed.
4. Materialize inputs as files the subagents can read in the off-repo `iterative-review-<pr_number>` directory:
   - `<diff_path>`: the full branch diff (`git diff --no-color <base>...<branch>`) written to a file. Write it as UTF-8. On PowerShell, the `>` operator can emit UTF-16; pipe through `Out-File -Encoding utf8NoBOM` or a Python one-liner to keep the file UTF-8 so `read` can open it.
   - `<pr_description>`: the PR title, body, and any linked issue/spec context written to a file.
   - Optional `<issue_context>`: Linear/GitHub issue or spec text if linked, written to a file.
5. Round 1 — dispatch `reviewer-strong` with the full diff, PR description, and any issue context. Capture its findings in a `review-log.md` with severity and file/line citations.
6. For each finding, the orchestrator verifies it, fixes it, and commits. Then materialize the fix diff (`git diff <pre-fix-sha>...<post-fix-sha>`) in the same off-repo `iterative-review-<pr_number>` directory and update `review-log.md`.
7. Round 2 — dispatch `reviewer-fast` with:
   - the original finding,
   - the prepared fix diff,
   - relevant slices of the full diff that the fix touches.
   Its job is to confirm the fix resolves the finding and catch regressions in the touched area only.
8. If `reviewer-fast` raises new issues, the orchestrator fixes them and returns to step 7.
9. When `reviewer-fast` is clean, re-dispatch `reviewer-strong` with the whole branch diff, PR description, and the `review-log.md` of earlier issues and fixes. Its job is a full branch review with added context of what was already addressed.
10. If the final `reviewer-strong` reports no blocking or important issues, the skill reports "reviewer-clean" and lists any minor/deferred items. The orchestrator then runs the repo's canonical CI preflight (`py -3 tools/run.py ci --check` here, or the consumer's equivalent) and flips the PR to ready only after a clean CI pass.

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

- Naming subagent dispatch prompts `final`, `final final`, `final final final`, etc. Use `Round N` for every round, including the last one (e.g., `Round 3 — strong re-review of full branch`).
- Letting `reviewer-fast` drift into a full branch review. Keep the dispatch prompt and the fix diff tightly scoped.
- Blindly applying reviewer findings without verification. Use `receiving-code-review` for each finding.
- Skipping CI after the reviewer loop. The reviewer "green" signal is not the draft/ready gate.