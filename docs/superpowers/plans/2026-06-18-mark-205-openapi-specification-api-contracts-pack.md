# openapi-specification Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Project Claude-Cortex `openapi-specification` into `api-contracts-pack` as the narrower OpenAPI companion slice while preserving retained Codex Cortex custody and publishable marketplace artifacts.

**Architecture:** Keep `sources/third_party/codex-cortex/upstream/skills/openapi-specification/` as the retained source snapshot, mirror that slice into `codex-marketplace/plugins/codex-cortex/skills/openapi-specification/` as the custody projection, and adapt `codex-marketplace/plugins/api-contracts-pack/skills/openapi-specification/` to compose with `api-design-patterns` rather than duplicate its broader contract doctrine. Update bundle manifests, source maps, ledgers, and generated skill zips so the new slice is discoverable in both the custody surface and the installable pack.

**Tech Stack:** Markdown skill sources, JSON manifests, provenance ledgers, repo index metadata, `py -3 tools/update_skill_artifacts.py`, `py -3 tools/validate_marketplace.py`, `py -3 tools/validate_repo_index.py`, `git diff --check`

---

### Task 1: Retain the upstream OpenAPI source under Codex Cortex custody

**Files:**
- Create: `sources/third_party/codex-cortex/upstream/skills/openapi-specification/SKILL.md`
- Create: `sources/third_party/codex-cortex/upstream/skills/openapi-specification/references/spec-patterns.md`
- Create: `sources/third_party/codex-cortex/upstream/skills/openapi-specification/validation/rubric.yaml`
- Modify: `sources/first_party/skills/codex-cortex/intake.json`
- Modify: `sources/first_party/skills/codex-cortex/decisions.json`
- Modify: `sources/first_party/skills/codex-cortex/decisions.md`
- Modify: `provenance/codex-cortex.md`

- [x] **Step 1: Copy the retained upstream skill into third-party custody**

Keep the upstream OpenAPI skill, reference, and validation rubric under the retained Claude-Cortex custody path.

- [x] **Step 2: Record the import ledger entry**

Add the MARK-205 intake and decision entries for `openapi-specification` and the boundary note that it stays focused on the OpenAPI-specific companion slice.

### Task 2: Project the OpenAPI companion slice into the installable pack

**Files:**
- Modify: `codex-marketplace/plugins/codex-cortex/README.md`
- Modify: `codex-marketplace/plugins/codex-cortex/SOURCE.md`
- Modify: `codex-marketplace/plugins/codex-cortex/references/source-map.md`
- Modify: `codex-marketplace/plugins/codex-cortex/references/bundle-manifest.json`
- Create: `codex-marketplace/plugins/codex-cortex/skills/openapi-specification/SKILL.md`
- Create: `codex-marketplace/plugins/codex-cortex/skills/openapi-specification/references/spec-patterns.md`
- Create: `codex-marketplace/plugins/codex-cortex/skills/openapi-specification/validation/rubric.yaml`
- Modify: `codex-marketplace/plugins/api-contracts-pack/README.md`
- Modify: `codex-marketplace/plugins/api-contracts-pack/SOURCE.md`
- Modify: `codex-marketplace/plugins/api-contracts-pack/references/source-map.md`
- Modify: `codex-marketplace/plugins/api-contracts-pack/references/bundle-manifest.json`
- Modify: `codex-marketplace/plugins/api-contracts-pack/.codex-plugin/plugin.json`
- Create: `codex-marketplace/plugins/api-contracts-pack/skills/openapi-specification/SKILL.md`
- Create: `codex-marketplace/plugins/api-contracts-pack/skills/openapi-specification/references/spec-patterns.md`
- Create: `codex-marketplace/plugins/api-contracts-pack/skills/openapi-specification/validation/rubric.yaml`

- [x] **Step 1: Mirror the custody surface**

Project the OpenAPI slice into `codex-cortex` so the custody plugin retains the imported source for downstream projection.

- [x] **Step 2: Build the installable pack projection**

Adapt the `api-contracts-pack` OpenAPI slice so it composes with `api-design-patterns` instead of duplicating its broader contract doctrine.

### Task 3: Update ledgers, docs, and discoverability surfaces

**Files:**
- Modify: `README.md`
- Modify: `codex-marketplace/README.md`
- Modify: `sources/README.md`
- Modify: `sources/third_party/README.md`
- Modify: `repo-index/repo-index.json`

- [x] **Step 1: Refresh repo-facing docs**

Update the repo, marketplace, and source-custody guidance so they name the MARK-205 OpenAPI companion slice.

- [x] **Step 2: Refresh structured navigation metadata**

Keep the repo index aligned with the new source custody and projection notes.

### Task 4: Regenerate and validate artifacts

**Files:**
- Modify: `generated/skill-zips/registry.json`
- Modify: `generated/skill-zips/api-contracts-pack/openapi-specification/skill.zip`
- Modify: `generated/skill-zips/codex-cortex/openapi-specification/skill.zip`

- [ ] **Step 1: Regenerate the targeted skill zips**

Run: `py -3 tools/update_skill_artifacts.py --skill api-contracts-pack/openapi-specification`
Expected: new deterministic zips for the `api-contracts-pack` and `codex-cortex` OpenAPI slices plus the matching registry entries.

- [ ] **Step 2: Validate the marketplace and repo index**

Run:

```powershell
py -3 tools/validate_marketplace.py
py -3 tools/validate_repo_index.py
git diff --check
```

Expected: all commands pass with no unexpected drift.

- [ ] **Step 3: Capture publication evidence**

Record the branch name, final head SHA, changed files, generated zip paths, validation output, and the exact composition note showing that `openapi-specification` stays narrower than `api-design-patterns`.
