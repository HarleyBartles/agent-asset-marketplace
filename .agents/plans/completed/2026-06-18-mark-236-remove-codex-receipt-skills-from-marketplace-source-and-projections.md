# Remove Codex Receipt Skills From Marketplace Source and Projections Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remove `codex-repo-receipts` and `codex-receipts-superpowers` from marketplace source, projections, generated install surfaces, and stale receipt-pattern docs while preserving unrelated Superpowers skills.

**Architecture:** Treat this as a source/projection cleanup pass, not a redesign. Remove the two skill roots and their generated install artifacts, then update the remaining marketplace docs, manifests, validators, provenance notes, and plan files so they no longer advertise the removed skills or block future work on missing records.

**Tech Stack:** Markdown docs, marketplace manifests, generated skill zip registry, Python validation scripts, PowerShell/Git.

---

### Task 1: Inventory the affected surfaces

**Files:**
- Inspect: `codex-marketplace/plugins/house-skills/skills/codex-repo-receipts/`
- Inspect: `codex-marketplace/plugins/house-skills/skills/codex-receipts-superpowers/`
- Inspect: `codex-marketplace/plugins/repo-worker-base/skills/codex-repo-receipts/`
- Inspect: `codex-marketplace/plugins/superpowers/skills/codex-receipts-superpowers/`
- Inspect: `sources/first_party/core/codex-repo-receipts/`
- Inspect: `sources/first_party/skills/codex-receipts-superpowers/`
- Inspect: `docs/superpowers/plans/`
- Inspect: `docs/superpowers/records/`
- Inspect: `generated/skill-zips/registry.json`
- Inspect: `tools/validate_marketplace.py`
- Inspect: `provenance/house-skills.md`
- Inspect: `provenance/repo-worker-base.md`
- Inspect: `provenance/superpowers.md`

- [x] **Step 1: Read the current source and projection docs**

```powershell
Get-Content codex-marketplace/plugins/repo-worker-base/README.md
Get-Content codex-marketplace/plugins/repo-worker-base/SOURCE.md
Get-Content codex-marketplace/plugins/superpowers/SOURCE.md
Get-Content codex-marketplace/plugins/superpowers/PROJECTION.md
Get-Content codex-marketplace/plugins/house-skills/README.md
Get-Content codex-marketplace/plugins/house-skills/skills/codex-repo-receipts/SKILL.md
Get-Content codex-marketplace/plugins/house-skills/skills/codex-receipts-superpowers/SKILL.md
```

- [x] **Step 2: Enumerate the remaining record and plan files**

```powershell
Get-ChildItem docs/superpowers/records -File
Get-ChildItem docs/superpowers/plans -File
```

### Task 2: Remove the two receipt skills and their generated install surfaces

**Files:**
- Delete: `sources/first_party/core/codex-repo-receipts/`
- Delete: `sources/first_party/skills/codex-receipts-superpowers/`
- Delete: `codex-marketplace/plugins/house-skills/skills/codex-repo-receipts/`
- Delete: `codex-marketplace/plugins/house-skills/skills/codex-receipts-superpowers/`
- Delete: `codex-marketplace/plugins/repo-worker-base/skills/codex-repo-receipts/`
- Delete: `codex-marketplace/plugins/superpowers/skills/codex-receipts-superpowers/`
- Delete: any generated zips and registry entries for those two skills under `generated/skill-zips/`

- [x] **Step 1: Remove the source and projection trees**

- [x] **Step 2: Regenerate generated skill artifacts so deleted skills disappear from the zip corpus**

```powershell
py -3 tools/update_skill_artifacts.py --all
```

- [x] **Step 3: Verify the generated registry no longer advertises the removed skills**

```powershell
Select-String -Path generated/skill-zips/registry.json -Pattern 'codex-repo-receipts|codex-receipts-superpowers'
```

### Task 3: Backfill plans and remove implementation records

**Files:**
- Delete: all files under `docs/superpowers/records/`
- Modify: all files under `docs/superpowers/plans/` that still have completed work marked with unchecked boxes
- Modify: supporting workflow docs that still imply missing records or unchecked historical plans are future blockers

- [x] **Step 1: Remove the implementation record files**

```powershell
Get-ChildItem docs/superpowers/records -File | Remove-Item
```

- [x] **Step 2: Update surviving plan files so completed work is marked with `[x]`**

```powershell
Get-ChildItem docs/superpowers/plans -File | ForEach-Object {
  # Review each plan before editing so genuinely incomplete future work stays visible.
}
```

- [x] **Step 3: Remove stale record-path expectations from the remaining docs**

```powershell
Select-String -Path docs\**\*.md,provenance\*.md -Pattern 'docs/superpowers/records|implementation record|codex-repo-receipts|codex-receipts-superpowers'
```

### Task 4: Update the remaining marketplace docs and validators

**Files:**
- Modify: `codex-marketplace/plugins/repo-worker-base/README.md`
- Modify: `codex-marketplace/plugins/repo-worker-base/SOURCE.md`
- Modify: `codex-marketplace/plugins/superpowers/SOURCE.md`
- Modify: `codex-marketplace/plugins/superpowers/PROJECTION.md`
- Modify: `codex-marketplace/plugins/house-skills/README.md`
- Modify: `provenance/house-skills.md`
- Modify: `provenance/repo-worker-base.md`
- Modify: `provenance/superpowers.md`
- Modify: `tools/validate_marketplace.py`
- Modify: any other manifest, source-map, provenance-map, repo-index, or overlay file that still names the removed skills

- [x] **Step 1: Rewrite the surviving guidance so it no longer depends on the removed skills**

- [x] **Step 2: Remove validator allowlists and checks for the deleted skill surfaces**

- [x] **Step 3: Update or delete stale references in generated projection metadata that are source-controlled**

### Task 5: Validate the cleanup

**Files:**
- Inspect: working tree diff
- Inspect: generated artifacts

- [x] **Step 1: Run marketplace validation**

```powershell
py -3 tools/validate_marketplace.py
```

- [x] **Step 2: Run whitespace and diff sanity checks**

```powershell
git diff --check
```

- [x] **Step 3: Confirm the removed skills no longer appear anywhere in source-controlled install surfaces**

```powershell
rg -n "codex-repo-receipts|codex-receipts-superpowers" codex-marketplace sources generated docs provenance tools
```

- [x] **Step 4: Summarize the exact files removed, files edited, generated artifacts changed, and any intentional residual references**
