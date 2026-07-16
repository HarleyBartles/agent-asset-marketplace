# MARK-238 ECC Source Custody and Projection Findings Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Promote the committed ECC inventory into third-party source custody, move the projection findings into Linear, and keep the validator honest about structural JSON equality rather than brittle byte matching.

**Architecture:** Keep ECC as third-party source custody at `sources/third_party/ecc/upstream/source-custody.md`, remove the stale `docs/inventory/ecc-agent-first-workflow-skills.md` copy, preserve the Linear findings in the attached document, and keep the Superpowers projection validator comparing JSON structure for `plugin.json`.

**Tech Stack:** Markdown, Git, PowerShell, Python 3

---

### Task 1: Promote the ECC inventory into third-party source custody

**Files:**
- Add: `sources/third_party/ecc/upstream/source-custody.md`
- Modify: `sources/third_party/README.md`
- Modify: `repo-index/repo-index.json`

- [x] **Step 1: Move the committed ECC inventory into source custody**

Promote the MARK-235 inventory result from `docs/inventory/` into the third-party custody surface.

- [x] **Step 2: Refresh the repo-facing references**

Keep the source-custody guidance and repo index aligned with the new ECC custody root.

### Task 2: Preserve the Linear findings surface

**Files:**
- Update the attached Linear document for `MARK-238`

- [x] **Step 1: Move the projection and classification findings into Linear**

Record the leftovers, shortlist, and custody notes in the attached Linear document instead of a third repo surface.

- [x] **Step 2: Keep the slice narrow**

Do not add a third roadmap file or broaden the issue beyond the ECC custody and projection findings.

### Task 3: Clean up the stale inventory report

**Files:**
- Remove: `docs/inventory/ecc-agent-first-workflow-skills.md`

- [x] **Step 1: Remove the stale inventory report**

Delete the old `docs/inventory/` copy after the promoted custody surface is in place.

### Task 4: Repair the validator to compare structural content

**Files:**
- Modify: `tools/validate_marketplace.py`
- Add: `docs/superpowers/plans/2026-06-18-mark-238-promote-ecc-inventory-into-source-custody-and-projection-findings.md`

- [x] **Step 1: Compare the Superpowers `plugin.json` structurally**

Parse both JSON files and compare the resulting objects so formatting drift does not trigger a false failure.

- [x] **Step 2: Keep the remaining asset checks strict**

Continue byte-equality checks for the non-JSON assets where raw-content comparison is still appropriate.

### Task 5: Validate and publish

**Files:**
- Review: `tools/validate_marketplace.py`
- Review: `tools/validate_repo_index.py`
- Review: `git diff --check`

- [x] **Step 1: Run the validation ladder**

Run the repo index validator, the marketplace validator, and diff hygiene checks on the rebased branch.

- [x] **Step 2: Publish the branch**

Commit, push, and refresh the draft PR against `main` with the checked plan linked in the body.
