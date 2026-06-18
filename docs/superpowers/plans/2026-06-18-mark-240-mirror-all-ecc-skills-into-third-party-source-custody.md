# MARK-240 ECC Full Source Mirror Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Mirror all 271 pinned upstream ECC skill directories into third-party source custody, record a manifest for every mirrored skill, and keep marketplace projection surfaces unchanged.

**Architecture:** Treat `sources/third_party/ecc/upstream` as retained third-party source custody. Pull the pinned ECC upstream commit into a temporary checkout, mirror every skill directory into `sources/third_party/ecc/upstream/skills/<skill>/` verbatim, then generate a custody manifest that records the upstream/local path pair, upstream commit, MARK-238 bucket, and future projection lane note for each skill. Keep the repo source note aligned with the mirrored root and validate the mirror against upstream before publishing.

**Tech Stack:** PowerShell, Git, Markdown, JSON, Python 3

---

### Task 1: Mirror the pinned ECC upstream snapshot

**Files:**
- Create: `sources/third_party/ecc/upstream/skills/**`
- Create: `.tmp/ecc-upstream/**` (temporary working checkout only)

- [ ] **Step 1: Fetch the pinned upstream commit into a temporary checkout**

Run the upstream clone from `https://github.com/affaan-m/ECC.git`, then check out `ceca28852e5b31edbbf66ebccc8fd163dd14208e` in `.tmp/ecc-upstream`.

- [ ] **Step 2: Mirror every upstream skill directory verbatim**

Copy all 271 directories from `.tmp/ecc-upstream/skills/` into `sources/third_party/ecc/upstream/skills/` without adapting the contents.

- [ ] **Step 3: Confirm the mirrored count and skip count**

Verify the custody root contains 271 mirrored skill directories and zero skipped directories.

### Task 2: Write the custody manifest and update the source note

**Files:**
- Create: `sources/third_party/ecc/upstream/manifest.json`
- Modify: `sources/third_party/ecc/upstream/source-custody.md`

- [ ] **Step 1: Generate the custody manifest**

Write a JSON manifest with `copied_skill_count: 271`, `skipped_skill_count: 0`, the pinned upstream commit, and one entry per mirrored skill containing:

```json
{
  "skill_name": "agentic-os",
  "upstream_source_path": "skills/agentic-os",
  "local_custody_path": "sources/third_party/ecc/upstream/skills/agentic-os",
  "upstream_commit": "ceca28852e5b31edbbf66ebccc8fd163dd14208e",
  "mark_238_bucket": "today",
  "future_projection_lane": "codex-cortex"
}
```

- [ ] **Step 2: Update the source-custody note**

Add a short note to `sources/third_party/ecc/upstream/source-custody.md` that points readers to the mirrored skill tree and the new manifest.

### Task 3: Prove verbatim mirroring and run repo validation

**Files:**
- Review: `sources/third_party/ecc/upstream/skills/**`
- Review: `sources/third_party/ecc/upstream/manifest.json`
- Review: `sources/third_party/ecc/upstream/source-custody.md`

- [ ] **Step 1: Compare every mirrored skill directory against upstream**

Use a deterministic directory comparison against the pinned upstream commit so the verification proves the mirrored directories are verbatim.

- [ ] **Step 2: Run the repo validation ladder**

Run:

```powershell
py -3 tools/validate_marketplace.py
py -3 tools/validate_repo_index.py
git diff --check
```

- [ ] **Step 3: Record the validation results**

Capture the command results and the exact verbatim-copy proof for the final return.

### Task 4: Create the implementation record and publish the branch

**Files:**
- Create: `docs/superpowers/records/2026-06-18-mark-240-mirror-all-ecc-skills-into-third-party-source-custody.md`

- [ ] **Step 1: Write the implementation record**

Document the mirror scope, the manifest path, the verbatim verification method, the validation results, and the publication state.

- [ ] **Step 2: Commit, push, and open a draft PR**

Commit the mirrored source custody changes on `harleydbartles/mark-240-drain-selected-ecc-skills-into-third-party-source-custody`, push the branch, and open a draft PR against `main`.
