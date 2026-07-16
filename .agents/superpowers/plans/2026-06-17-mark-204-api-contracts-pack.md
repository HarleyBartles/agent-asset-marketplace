# api-contracts-pack Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Project Claude-Cortex `api-design-patterns` into a new installable `api-contracts-pack` while preserving retained `codex-cortex` custody, provenance, and generated skill zip outputs.

**Architecture:** Keep the upstream custody tree under `sources/third_party/codex-cortex/upstream/` as the source record, add a matching `codex-cortex` import/projection slice for `api-design-patterns`, and mirror that slice into a new `api-contracts-pack` plugin root with a bundle manifest and source map. Update the marketplace registry, plugin-root inventory, generated skill zips, provenance, and repo index so the new pack is discoverable without expanding into `openapi-specification`.

**Tech Stack:** Markdown skill sources, JSON manifests, provenance ledgers, repo index metadata, `py -3 tools/update_skill_artifacts.py`, `py -3 tools/validate_marketplace.py`, `py -3 tools/validate_repo_index.py`, `git diff --check`

---

### Task 1: Vendor the retained Claude-Cortex `api-design-patterns` source and record the import decision

**Files:**
- Create: `sources/third_party/codex-cortex/upstream/skills/api-design-patterns/SKILL.md`
- Create: `sources/third_party/codex-cortex/upstream/skills/api-design-patterns/references/design-process.md`
- Create: `sources/third_party/codex-cortex/upstream/skills/api-design-patterns/validation/rubric.yaml`
- Modify: `sources/first_party/skills/codex-cortex/intake.json`
- Modify: `sources/first_party/skills/codex-cortex/decisions.json`
- Modify: `sources/first_party/skills/codex-cortex/decisions.md`
- Modify: `provenance/codex-cortex.md`

- [x] **Step 1: Copy the retained upstream skill into third-party custody**

Use the upstream Claude-Cortex `api-design-patterns` files as the retained source basis, keeping the upstream skill, its design-process reference, and its validation rubric intact under `sources/third_party/codex-cortex/upstream/`.

- [x] **Step 2: Record the import ledger entry**

Add a first-party intake/decision record for `MARK-204` that names the retained source path, the upstream repo and pinned commit, the imported public name, and the explicit boundary that `openapi-specification` stays out of this issue.

- [x] **Step 3: Update the provenance note**

Extend `provenance/codex-cortex.md` so the new custody surface and its rights trail are visible alongside the earlier Codex Cortex imports.

### Task 2: Build the installable `api-contracts-pack` projection

**Files:**
- Create: `codex-marketplace/plugins/api-contracts-pack/.codex-plugin/plugin.json`
- Create: `codex-marketplace/plugins/api-contracts-pack/README.md`
- Create: `codex-marketplace/plugins/api-contracts-pack/SOURCE.md`
- Create: `codex-marketplace/plugins/api-contracts-pack/LICENSE`
- Create: `codex-marketplace/plugins/api-contracts-pack/assets/icon.svg`
- Create: `codex-marketplace/plugins/api-contracts-pack/references/bundle-manifest.json`
- Create: `codex-marketplace/plugins/api-contracts-pack/references/source-map.md`
- Create: `codex-marketplace/plugins/api-contracts-pack/skills/api-design-patterns/SKILL.md`
- Create: `codex-marketplace/plugins/api-contracts-pack/skills/api-design-patterns/references/design-process.md`
- Create: `codex-marketplace/plugins/api-contracts-pack/skills/api-design-patterns/validation/rubric.yaml`
- Modify: `codex-marketplace/plugins/codex-cortex/SOURCE.md`
- Modify: `codex-marketplace/plugins/codex-cortex/references/source-map.md`
- Modify: `codex-marketplace/plugins/codex-cortex/references/bundle-manifest.json`

- [x] **Step 1: Author the new pack shell**

Define `api-contracts-pack` as the installable plugin and point its metadata back to the retained `codex-cortex` custody surface.

- [x] **Step 2: Project the `api-design-patterns` skill**

Mirror the upstream skill into the new pack root as the umbrella contract-doctrine slice, keeping the skill narrow to contract-first API design, contract seams, generated-client expectations, and validation posture.

- [x] **Step 3: Wire bundle metadata**

Record the source/provenance split and the single projected skill in the new bundle manifest and source map, and update the `codex-cortex` bundle metadata to show the retained import now includes `api-design-patterns`.

### Task 3: Register the new surfaces in marketplace and repo metadata

**Files:**
- Modify: `codex-marketplace/plugin-roots.json`
- Modify: `codex-marketplace/manifest.json`
- Modify: `.agents/plugins/marketplace.json`
- Modify: `codex-marketplace/README.md`
- Modify: `README.md`
- Modify: `codex-marketplace/plugins/AGENTS.md`
- Modify: `sources/README.md`
- Modify: `sources/third_party/README.md`
- Modify: `repo-index/repo-index.json`
- Modify: `tools/generate_repo_index.py` if the new pack or custody zone is not already represented by existing generators
- Modify: `tools/validate_marketplace.py` if the new pack needs explicit path or custody checks

- [x] **Step 1: Add the new marketplace root**

Insert `api-contracts-pack` into the protected marketplace inventory and keep the registry/export surfaces aligned.

- [x] **Step 2: Add the repo-index and human-facing references**

Teach the repo index and repo navigation surfaces about the new pack and the retained `codex-cortex` custody addition so discovery stays deterministic.

- [x] **Step 3: Refresh the active-root documentation**

Update the repo docs and scoped AGENTS guidance so the active marketplace root lists reflect the current protected set instead of the pre-MARK-204 inventory.

### Task 4: Generate and validate the installable artifact

**Files:**
- Modify: `generated/skill-zips/registry.json`
- Create or modify: `generated/skill-zips/api-contracts-pack/api-design-patterns/skill.zip`

- [x] **Step 1: Regenerate the projected skill zip**

Run: `py -3 tools/update_skill_artifacts.py --skill api-contracts-pack/api-design-patterns`
Expected: one deterministic `skill.zip` under `generated/skill-zips/api-contracts-pack/api-design-patterns/` and a matching registry entry.

- [x] **Step 2: Validate the marketplace and repo index**

Run:

```powershell
py -3 tools/validate_marketplace.py
py -3 tools/validate_repo_index.py
git diff --check
```

Expected: all commands pass with no unexpected drift.

- [x] **Step 3: Capture publication evidence**

Record the branch name, final head SHA, changed files, generated zip path, validation output, and the explicit boundary that `openapi-specification` was left for MARK-205.
