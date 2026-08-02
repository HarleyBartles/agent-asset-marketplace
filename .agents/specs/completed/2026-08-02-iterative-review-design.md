# Iterative Review — PR Review Loop Design

> **Status:** Completed — implemented and merged via PR #255 (https://github.com/HarleyBartles/agent-asset-marketplace/pull/255), head SHA `46a2ece5`.

> Spec for adding an `iterative-review` skill to `superpowers-plus` that runs a multi-round subagent review loop on a draft PR, and for tightening the `reviewer-fast` profile so it becomes a focused fix re-reviewer.

## Problem

`requesting-code-review` is a single-round dispatch skill: it prepares a diff, dispatches a reviewer, and returns the findings. There is no canonical skill that runs a controlled feedback/fix/re-review loop before a draft PR is marked ready. Meanwhile, the `reviewer-fast` profile exists but is lightly used and lacks an explicit narrow scope; without that, a "fast" re-review of a fix can drift into a full branch review, defeating the cost/timing separation.

## Goals

1. Add first-party `iterative-review` skill to the `superpowers-plus` pack.
2. Update the `reviewer-fast` profile so it is explicitly a fix-diff re-reviewer.
3. Declare the new skill in `codex-marketplace/plugins/superpowers-plus/references/bundle-manifest.json`.
4. Regenerate downstream installed surfaces with `py -3 tools/run.py marketplace --apply`.
5. Pass `py -3 tools/run.py ci --check`.

## Constraints

- `iterative-review` is a main-agent skill: it prepares inputs, dispatches reviewers, and reports. It does not modify files or change PR state.
- The repo's draft/ready policy keeps a PR in draft until `py -3 tools/run.py ci --check` passes. The skill reports "reviewer-clean" and leaves the CI run and the draft-to-ready flip to the orchestrator.
- The skill must reuse the existing `requesting-code-review` prepared-diff pattern and the `selecting-a-subagent` profile-selection rules.
- First-party source is edited under `codex-marketplace/plugins/superpowers-plus/` only; installed `.agents/skills/` and `.agents/agents/` surfaces are regenerated downstream.

## Non-goals

- Adding a new custom subagent profile. The loop uses existing `reviewer-strong` and the updated `reviewer-fast`.
- Auto-applying fixes. The orchestrator applies fixes using its own judgement.
- Shipping the skill in any pack other than `superpowers-plus` for this iteration.

## Proposed Approaches

### Option A: New `iterative-review` skill + `reviewer-fast` scoping (recommended)

- Create `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/`.
- Update `codex-marketplace/plugins/superpowers-plus/skills/selecting-a-subagent/assets/reviewer-fast.md` to scope it to fix re-review.
- Add one bundle-manifest entry and regenerate.
- Pros: clean, single-purpose, uses existing packs/profiles, easy to discover via `using-superpowers-plus`.
- Cons: adds one more skill to the `superpowers-plus` namespace.

### Option B: Extend `requesting-code-review` with an iterative mode

- Add a loop flag or extra section to `requesting-code-review`.
- Pros: one skill to maintain.
- Cons: the single-round dispatch contract of `requesting-code-review` becomes unclear; the loop needs more orchestrator state than a dispatch skill should own.

### Option C: Repo-local `.agents/skills/iterative-review/` only

- Create the skill under `.agents/skills/` and edit the installed `.agents/agents/reviewer-fast.md` directly.
- Pros: fastest local landing.
- Cons: not in the marketplace pack, not versioned as first-party source, and the `reviewer-fast` source in `codex-marketplace/plugins/` still needs changing anyway.

**Recommendation: Option A.**

## Design Details

### `iterative-review` first-party skill

Source tree: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/`

- `SKILL.md`
  - Frontmatter:
    ```yaml
    ---
    name: iterative-review
    description: Use when a draft PR is ready for subagent review before being marked ready for CI and human review.
    ---
    ```
  - No `agent:` frontmatter; the skill runs on the main orchestrator.
  - Body instructs the orchestrator to:
    1. Determine the base ref and the branch/head for the draft PR.
    2. Materialize inputs as files:
       - `<diff_path>`: the full branch diff (`git diff --no-color <base>...<branch>`).
       - `<pr_description>`: the PR title, body, and any linked issue/spec context.
       - Optional `<issue_context>`: Linear/GitHub issue or spec text if linked.
    3. Round 1 — dispatch `reviewer-strong` with the full diff, PR description, and any issue context. Capture its findings in a `review-log.md` with severity and file/line citations.
    4. For each finding, the orchestrator verifies, fixes, and commits. It then materializes the fix diff and updates `review-log.md`.
    5. Round 2 — dispatch `reviewer-fast` with:
       - the original finding,
       - the prepared fix diff (`git diff <pre-fix-sha>...<post-fix-sha>`),
       - relevant slices of the full diff that the fix touches.
       Its job is to confirm the fix resolves the finding and catches regressions in the touched area only.
    6. If `reviewer-fast` raises new issues, the orchestrator fixes them and returns to step 5.
    7. When `reviewer-fast` is clean, re-dispatch `reviewer-strong` with the whole branch diff, PR description, and the `review-log.md` of earlier issues and fixes. Its job is a full branch review with added context of what was already addressed.
    8. If the final `reviewer-strong` reports no blocking or important issues, the skill reports "reviewer-clean" and lists any minor/deferred items. The orchestrator then runs `py -3 tools/run.py ci --check` and flips the PR to ready only after a clean CI pass.

- `agents/openai.yaml`
  - `skill_name: iterative-review`
  - `source_category: first_party`
  - `display_name: Iterative Review`
  - `short_description: Use when a draft PR is ready for subagent review before being marked ready for CI and human review.`
  - `default_prompt: Use /iterative-review when a draft PR is ready for subagent review before being marked ready for CI and human review.`
  - `policy.allow_implicit_invocation: true`

### `reviewer-fast` profile update

Source file: `codex-marketplace/plugins/superpowers-plus/skills/selecting-a-subagent/assets/reviewer-fast.md`

- Keep the existing `model: swe-1-6` and allowed tools.
- Add an explicit `## Fix re-review scope` section that instructs the subagent to:
  - review only the provided fix diff,
  - evaluate how that diff addresses the listed prior finding,
  - look at the full branch diff only where the fix touches it,
  - keep findings brief and not broaden the review to the whole branch.

### Marketplace wiring

- `codex-marketplace/plugins/superpowers-plus/references/bundle-manifest.json`
  - Add a first-party `verbatim` entry for `iterative-review` following the existing skill-entry shape:
    ```json
    {
      "canonical_name": "iterative-review",
      "source_category": "first_party",
      "content_mode": "verbatim",
      "source_family": "first_party",
      "canonical_source_path": "codex-marketplace/plugins/superpowers-plus/skills/iterative-review",
      "local_path": "skills/iterative-review",
      "provenance_note": "First-party helper skill bundled verbatim.",
      "copy_expectation": "byte_identical"
    }
    ```
- `py -3 tools/run.py marketplace --apply` will:
  - project the new skill into `codex-marketplace/plugins/superpowers-plus/`,
  - install the skill to `.agents/skills/iterative-review/`,
  - refresh `.agents/agents/reviewer-fast.md` from the updated source asset,
  - regenerate bundle manifests, source maps, provenance maps, and indexes.

## Files to Touch

- `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/SKILL.md` (new)
- `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/agents/openai.yaml` (new)
- `codex-marketplace/plugins/superpowers-plus/skills/selecting-a-subagent/assets/reviewer-fast.md` (edit)
- `codex-marketplace/plugins/superpowers-plus/references/bundle-manifest.json` (edit)
- Derived surfaces under `.agents/skills/`, `.agents/agents/`, and `codex-marketplace/plugins/` (regenerated)

## Verification

- `py -3 tools/run.py marketplace --apply`
- `py -3 tools/run.py ci --check`
- Spot-check the installed `.agents/skills/iterative-review/SKILL.md` and `.agents/agents/reviewer-fast.md` for the new content.

## Completion Notes

- PR #255 created from `spec-pr-review-iteration` and merged to `main`.
- All five goals above were met.
- `py -3 tools/run.py ci --check` passed before merge.
- This spec was moved to `.agents/specs/completed/` on `main`.
