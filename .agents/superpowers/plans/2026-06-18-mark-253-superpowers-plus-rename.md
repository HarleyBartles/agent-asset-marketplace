# Superpowers+ Rename Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rename the Asset Marketplace Superpowers projection to `Superpowers+` / `superpowers-plus` and keep the adapted `using-superpowers` router aligned with the marketplace wrapper front doors.

**Architecture:** Treat this as a breaking marketplace rename, not a content rewrite. Move the plugin identity, registry, repo index, generated zips, and projection/provenance references onto the new slug, then preserve the adapted workflow router and wrapper routing in the new projection. Keep third-party custody separate from the active marketplace projection and regenerate derived artifacts instead of hand-editing them.

**Tech Stack:** PowerShell, repository Python validators, marketplace manifest/registry generation, skill artifact packaging, Markdown/YAML/JSON projections.

---

### Task 1: Rename the active marketplace projection surface

**Files:**
- Modify: `codex-marketplace/plugins/superpowers/.codex-plugin/plugin.json`
- Modify: `codex-marketplace/plugins/superpowers/PROJECTION.md`
- Modify: `codex-marketplace/plugins/superpowers/SOURCE.md`
- Modify: `codex-marketplace/plugins/superpowers/skills/using-superpowers/SKILL.md`
- Modify: `codex-marketplace/plugins/superpowers/skills/*`
- Modify: `codex-marketplace/plugins/superpowers/references/*`
- Rename: `codex-marketplace/plugins/superpowers` -> `codex-marketplace/plugins/superpowers-plus`

- [x] **Step 1: Inspect the current projection tree and confirm every active-surface path that still names `superpowers`.**
- [x] **Step 2: Rename the plugin root to `superpowers-plus` and update the plugin metadata so the user-facing display name is `Superpowers+`.**
- [x] **Step 3: Update the adapted `using-superpowers` router so it still chooses the smallest fitting workflow, but routes directly to repo-specific wrapper skills where they own the front door.**
- [x] **Step 4: Rewrite local projection/provenance references from the old projection identity to the new one without changing the retained third-party custody snapshot.**

### Task 2: Reconcile the marketplace registry, repo index, and generated skill exports

**Files:**
- Modify: `codex-marketplace/plugin-roots.json`
- Modify: `codex-marketplace/manifest.json`
- Modify: `.agents/plugins/marketplace.json`
- Modify: `repo-index/repo-index.json`
- Modify: `generated/skill-zips/registry.json`
- Modify: `generated/skill-zips/superpowers-plus/*`
- Remove: `generated/skill-zips/superpowers/*` if the generator no longer treats the old slug as active

- [x] **Step 1: Regenerate the marketplace manifest/registry inputs so the active plugin inventory points at `superpowers-plus`.**
- [x] **Step 2: Regenerate the repo index so the plugin root, source ledger, and provenance references reflect `Superpowers+`.**
- [x] **Step 3: Regenerate the skill zip corpus and registry so `superpowers` is no longer a live install/export target.**
- [x] **Step 4: Verify that any retained `superpowers` references are historical custody only, not installable marketplace identity.**

### Task 3: Update validation and publication evidence

**Files:**
- Modify: any affected docs or notes that point at the old active projection name

- [x] **Step 1: Run the repo validation ladder for marketplace and repo-index consistency, plus the generated artifact checks needed for the rename.**
- [x] **Step 2: Capture a targeted stale-reference search proving the old name is gone from active surfaces and only survives in custody/provenance where expected.**
- [ ] **Step 3: Commit, push, and open a draft PR on the required branch so the publication surface is visible before final return.**

### Non-goals

- Do not rename the retained third-party custody snapshot under `sources/third_party/superpowers/obra-superpowers/v5.1.0/`.
- Do not broaden the change into unrelated marketplace plugins or first-party skills.
- Do not preserve the old `superpowers` install/export identity as a second active market-facing plugin.
