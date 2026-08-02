# Iterative Review Implementation Plan

> **Status:** Completed — implemented and merged via PR #255 (https://github.com/HarleyBartles/agent-asset-marketplace/pull/255).

> **For agentic workers:** REQUIRED SUB-SKILL: Use /subagent-driven-development (recommended) or /executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Create the `iterative-review` skill, update the `reviewer-fast` profile to a focused fix re-reviewer, wire both into the `superpowers-plus` bundle, and prove them with the repo's canonical marketplace and CI validation.

**Architecture:** Add a first-party skill under `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/`, update the `reviewer-fast` profile in `selecting-a-subagent/assets/`, add one `bundle-manifest.json` entry, then regenerate downstream installed surfaces and run CI.

**Tech Stack:** Markdown skill files, Codex plugin manifest (`codex-marketplace/plugins/superpowers-plus/references/bundle-manifest.json`), `py -3 tools/run.py`.

## Global Constraints

- Source edits only under `codex-marketplace/plugins/superpowers-plus/`. Generated `.agents/skills/` and `.agents/agents/` are regenerated, not hand-edited.
- `iterative-review` is a main-agent skill; it must not carry an `agent:` frontmatter.
- `iterative-review` does not modify files or PR state. It prepares review inputs, dispatches `reviewer-strong` and `reviewer-fast`, and reports "reviewer-clean" with any minor/deferred items.
- The PR stays in draft until the CI preflight (`py -3 tools/run.py ci --check`) passes.
- New skill must follow the existing `superpowers-plus` `SKILL.md` + `agents/openai.yaml` shape.
- `.agents/plans/completed/2026-08-02-iterative-review-plan.md` and `.agents/specs/completed/2026-08-02-iterative-review-design.md` are the provenance for this work.

---

## Task 1: Create `iterative-review` skill source

**Files:**
- Create: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/SKILL.md`
- Create: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/agents/openai.yaml`

**Interfaces:**
- Consumes: the design spec at `.agents/specs/completed/2026-08-02-iterative-review-design.md`
- Produces: the new `iterative-review` skill source, ready for bundling

- [x] **Step 1: Create the `iterative-review` directories**

  Run:
  ```powershell
  New-Item -ItemType Directory -Path 'codex-marketplace/plugins/superpowers-plus/skills/iterative-review', 'codex-marketplace/plugins/superpowers-plus/skills/iterative-review/agents'
  ```

- [x] **Step 2: Write `SKILL.md` with the exact content below**

  ```markdown
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
  2. Materialize inputs as files the subagents can read:
     - `<diff_path>`: the full branch diff (`git diff --no-color <base>...<branch>`) written to a file.
     - `<pr_description>`: the PR title, body, and any linked issue/spec context written to a file.
     - Optional `<issue_context>`: Linear/GitHub issue or spec text if linked, written to a file.
  3. Round 1 — dispatch `reviewer-strong` with the full diff, PR description, and any issue context. Capture its findings in a `review-log.md` with severity and file/line citations.
  4. For each finding, the orchestrator verifies it, fixes it, and commits. Then materialize the fix diff (`git diff <pre-fix-sha>...<post-fix-sha>`) and update `review-log.md`.
  5. Round 2 — dispatch `reviewer-fast` with:
     - the original finding,
     - the prepared fix diff,
     - relevant slices of the full diff that the fix touches.
     Its job is to confirm the fix resolves the finding and catch regressions in the touched area only.
  6. If `reviewer-fast` raises new issues, the orchestrator fixes them and returns to step 5.
  7. When `reviewer-fast` is clean, re-dispatch `reviewer-strong` with the whole branch diff, PR description, and the `review-log.md` of earlier issues and fixes. Its job is a full branch review with added context of what was already addressed.
  8. If the final `reviewer-strong` reports no blocking or important issues, the skill reports "reviewer-clean" and lists any minor/deferred items. The orchestrator then runs the repo's canonical CI preflight (`py -3 tools/run.py ci --check` here, or the consumer's equivalent) and flips the PR to ready only after a clean CI pass.

  ## Inputs the orchestrator must provide

  - `<base>` and `<branch>` (or `<head_sha>`)
  - `<pr_number>` or `<pr_description>`
  - Optional `<issue_context>` for Linear/GitHub issue or spec text

  ## Invariants

  - This skill does not modify files or PR state.
  - The orchestrator owns all fixes and the final decision to flip the PR to ready.
  - CI must pass before leaving draft.

  ## Common Mistakes

  - Letting `reviewer-fast` drift into a full branch review. Keep the dispatch prompt and the fix diff tightly scoped.
  - Blindly applying reviewer findings without verification. Use `receiving-code-review` for each finding.
  - Skipping CI after the reviewer loop. The reviewer "green" signal is not the draft/ready gate.
  ```

- [x] **Step 3: Write `agents/openai.yaml` with the exact content below**

  ```yaml
  version: 1
  metadata:
    skill_name: iterative-review
    source_category: first_party
  interface:
    display_name: Iterative Review
    short_description: Use when a draft PR is ready for subagent review before being marked ready for CI and human review.
    default_prompt: Use /iterative-review when a draft PR is ready for subagent review before being marked ready for CI and human review.
  policy:
    products:
    - chatgpt
    - codex
    - api
    - atlas
    allow_implicit_invocation: true
  ```

- [x] **Step 4: Stage the skill files**

  Run:
  ```powershell
  git add codex-marketplace/plugins/superpowers-plus/skills/iterative-review/SKILL.md
  git add codex-marketplace/plugins/superpowers-plus/skills/iterative-review/agents/openai.yaml
  ```

---

## Task 2: Update `reviewer-fast` profile to fix re-reviewer scope

**Files:**
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/selecting-a-subagent/assets/reviewer-fast.md`

**Interfaces:**
- Consumes: the `iterative-review` design spec
- Produces: the updated `reviewer-fast` source asset, regenerated into `.agents/agents/reviewer-fast.md`

- [x] **Step 1: Read the current `assets/reviewer-fast.md` to locate `## Inputs` and `## Procedure`**

- [x] **Step 2: Append the fix re-review inputs to `## Inputs the orchestrator must provide`**

  Add the following bullet at the end of the input list, before the closing paragraph "Do not generate the diff yourself.":

  ```markdown
  - For a fix re-review, the orchestrator must also provide:
    - `<original_finding>` — the issue the fix is addressing.
    - `<fix_diff_path>` — the prepared fix diff (`git diff <pre-fix-sha>...<post-fix-sha>` output written to a file).
    - `<full_diff_slice_path>` — the relevant slices of the full branch diff that the fix touches.
  ```

- [x] **Step 3: Replace `## Procedure` steps 1 and 4 to match the two modes**

  Change the current step 1:

  ```markdown
  1. Read the prepared diff at `<diff_path>`.
  ```

  To:

  ```markdown
  1. Determine the mode. If this is a fix re-review, read the original finding at `<original_finding>`, then the prepared fix diff at `<fix_diff_path>` and the relevant full-branch slices at `<full_diff_slice_path>`; skip `<diff_path>`. If this is a general small re-review, read the prepared diff at `<diff_path>`.
  ```

  Then change the current step 4:

  ```markdown
  4. Do a lighter scan across the rest of the diff for regressions; do not deep-dive unless something looks off.
  ```

  To:

  ```markdown
  4. If this is a fix re-review, follow `## Fix re-review scope` below. If this is a general small re-review, do a lighter scan across the rest of the diff for regressions; do not deep-dive unless something looks off.
  ```

- [x] **Step 4: Insert `## Fix re-review scope` after `## Procedure`**

  ```markdown
  ## Fix re-review scope

  When this profile is used for a fix re-review, the orchestrator will provide the original finding, the prepared fix diff (`git diff <pre-fix-sha>...<post-fix-sha>`), and the relevant slices of the full branch diff the fix touches.

  Evaluate **only**:

  1. whether the fix diff resolves the listed finding,
  2. whether the fix introduces any obvious regressions in the code it touches,
  3. whether the fix is consistent with the immediate surrounding context.

  Do not broaden the review to the whole branch. Do not re-evaluate parts of the branch the fix does not touch. Keep findings brief, concrete, and actionable, with specific file and line citations.
  ```

- [x] **Step 5: Stage the modified file**

  Run:
  ```powershell
  git add codex-marketplace/plugins/superpowers-plus/skills/selecting-a-subagent/assets/reviewer-fast.md
  ```

---

## Task 3: Add `iterative-review` to the `superpowers-plus` bundle manifest

**Files:**
- Modify: `codex-marketplace/plugins/superpowers-plus/references/bundle-manifest.json`

**Interfaces:**
- Consumes: the `iterative-review` source tree
- Produces: a bundle entry that projects the skill into `.agents/skills/iterative-review/`

- [x] **Step 1: Insert the following object in the `bundle-manifest.json` `entries` array in alphabetical order by `canonical_name` (after `inspecting-the-environment`, before `publishing-source`)**

  ```json
  {
    "canonical_name": "iterative-review",
    "source_category": "first_party",
    "content_mode": "verbatim",
    "source_family": "first_party",
    "canonical_source_path": "codex-marketplace/plugins/superpowers-plus/skills/iterative-review",
    "local_path": "skills/iterative-review",
    "provenance_note": "First-party helper skill bundled verbatim; not derived from the obra/superpowers upstream snapshot.",
    "copy_expectation": "byte_identical"
  }
  ```

- [x] **Step 2: Stage the modified manifest**

  Run:
  ```powershell
  git add codex-marketplace/plugins/superpowers-plus/references/bundle-manifest.json
  ```

---

## Task 4: Regenerate and validate

**Files:**
- Derived: `.agents/skills/iterative-review/`, `.agents/agents/reviewer-fast.md`, bundle manifests, source maps, and indexes

**Interfaces:**
- Consumes: staged source edits and manifest entry
- Produces: a clean CI preflight and regenerated installed surfaces

- [x] **Step 1: Run marketplace generation to project source into installed surfaces**

  Run:
  ```powershell
  py -3 tools/run.py marketplace --apply
  git add -A
  ```

  This will create `.agents/skills/iterative-review/` and refresh `.agents/agents/reviewer-fast.md` and other derived files.

  **Expected interim state:** `tools/run.py marketplace --apply` should exit 0. If it fails, fix the source or manifest error before proceeding.

- [x] **Step 2: Spot-check the generated installed surfaces**

  Run:
  ```powershell
  Select-String -Pattern "iterative-review" -Path .agents/skills/iterative-review/SKILL.md
  Select-String -Pattern "Fix re-review scope" -Path .agents/agents/reviewer-fast.md
  Select-String -Pattern "fix_diff_path" -Path .agents/agents/reviewer-fast.md
  Select-String -Pattern "full_diff_slice_path" -Path .agents/agents/reviewer-fast.md
  ```

  **Expected result:** the first command finds the `iterative-review` name in the installed skill; the second finds `Fix re-review scope` in the installed agent profile.

- [x] **Step 3: Run the CI preflight on the staged tree**

  Run:
  ```powershell
  py -3 tools/run.py ci --check
  ```

  **Expected result:** all targets pass. If any fail, fix the source or derived files and re-run.

- [x] **Step 4: Commit the source and regenerated changes**

  Run:
  ```powershell
  git commit -m "feat: add iterative-review skill and scope reviewer-fast`n`nGenerated with [Devin](https://devin.ai)`nCo-Authored-By: Devin <158243242+devin-ai-integration[bot]@users.noreply.github.com>"
  ```

  The pre-commit hook will re-run `py -3 tools/run.py ci --check` and should pass.

---

## Task 5: Push and verify the PR

**Files:**
- None (GitHub surface)

**Interfaces:**
- Consumes: the local commit on `spec-pr-review-iteration`
- Produces: an updated draft PR with the new commit

- [x] **Step 1: Push the branch**

  Run:
  ```powershell
  git push origin spec-pr-review-iteration
  ```

- [x] **Step 2: Verify the PR for the current branch**

  Run:
  ```powershell
  gh pr view --json headRefOid,url,state,mergeable
  ```

  **Expected result:** `state` is `OPEN`, `mergeable` is `MERGEABLE`, and `headRefOid` matches the latest commit on `spec-pr-review-iteration`.

- [x] **Step 3: Confirm the PR remains draft**

  The PR is intentionally left in draft. Flip to ready only after self-review and a green preflight. It is already green, but final draft/ready decision is the author's.

---

## SDD Confidence Rating

**9/10** — exact file paths, file contents, manifest entry, and validation commands are specified. The `SKILL.md` frontmatter, `agents/openai.yaml`, and `reviewer-fast` input and scope updates are now concrete and transcribable.

---

## Completion Notes

- PR #255 was created from branch `spec-pr-review-iteration` and merged to `main`.
- Head SHA at merge: `46a2ece5`.
- All CI preflight checks (`py -3 tools/run.py ci --check`) passed before merge.
- This plan was moved to `.agents/plans/completed/` on `main`.
