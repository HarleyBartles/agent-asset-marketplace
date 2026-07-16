# MARK-264 Repair Upstream Source Custody Gaps Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Normalize the frontend-pack custody references onto the retained `claude-cortex` source root so the active projection points at the repo's honest retained upstream snapshot.

**Architecture:** Keep the change narrow and documentation-first. Update the frontend-pack source/provenance surfaces to point at the normalized third-party custody root that already contains the retained frontend skill slice, then record the repair and run validation without reshaping pack membership.

**Tech Stack:** Markdown, JSON, repository validation scripts, `py -3`.

---

### Task 1: Normalize frontend-pack custody pointers

**Files:**
- Modify: `codex-marketplace/plugins/frontend-pack/README.md`
- Modify: `codex-marketplace/plugins/frontend-pack/SOURCE.md`
- Modify: `codex-marketplace/plugins/frontend-pack/references/source-map.md`
- Modify: `provenance/frontend-pack.md`

- [x] **Step 1: Update the failing source-custody references**

Replace the wrong `codex-cortex` custody-root references with the honest `claude-cortex` custody-root references in the frontend pack documentation and source map, while keeping the pack boundary and projected skills unchanged.

- [x] **Step 2: Verify the updated wording**

Run: `rg -n "claude-cortex|codex-cortex" codex-marketplace/plugins/frontend-pack provenance/frontend-pack.md`
Expected: `codex-cortex` remains only where the repo intentionally keeps other family naming, and the frontend-pack custody references point at `claude-cortex`.

### Task 2: Record the repair

**Files:**
- Create: `docs/superpowers/records/2026-06-19-mark-264-repair-upstream-source-custody-gaps.md`

- [x] **Step 1: Write the implementation record**

Capture the narrow repair, the inspected repo surfaces, the custody normalization decision, the validation commands, and the publication details once the branch is pushed.

- [x] **Step 2: Keep the record aligned with the repo state**

Ensure the record only claims the change that actually lands in the repository and notes any unresolved blocker explicitly instead of inventing a broader custody expansion.

### Task 3: Validate and publish

**Files:**
- Modify: `docs/superpowers/plans/2026-06-19-mark-264-repair-upstream-source-custody-gaps.md`

- [x] **Step 1: Run the relevant validators**

Run:
`py -3 tools/validate_marketplace.py`
`py -3 tools/validate_repo_index.py`
`py -3 tools/validate_skill_zips.py`
`git diff --check`

- [x] **Step 2: Mark completed plan steps**

Change completed steps to `[x]` in this plan so the record reflects the work actually done.

- [x] **Step 3: Publish the branch**

Commit the scoped changes, push `harleydbartles/mark-264-repair-upstream-source-custody-gaps`, and open a draft PR without broadening scope.
