# Codex Cortex / Architecture Pack Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Seed `codex-cortex` as the retained Claude-Cortex-derived custody surface for `cqrs-event-sourcing`, then project that skill into the installable `architecture-pack` plugin and its generated skill zip.

**Architecture:** Keep the third-party custody and first-party import decisions under `codex-cortex` and `sources/first_party/skills/codex-cortex/`. Project only the single adapted `cqrs-event-sourcing` skill into `codex-marketplace/plugins/architecture-pack/`, with the plugin manifest and bundle metadata pointing back to the custody surface. Update the marketplace inventory and repo index so the new custody and projection surfaces are discoverable without broadening into later Claude-Cortex candidates.

**Tech Stack:** Markdown skill sources, JSON manifests, source/provenance ledgers, marketplace validation scripts, repo-index generation, `py -3 tools/update_skill_artifacts.py`.

---

### Task 1: Create the `codex-cortex` custody surface for the imported Claude-Cortex slice

**Files:**
- Create: `sources/third_party/codex-cortex/upstream/README.md`
- Create: `sources/third_party/codex-cortex/upstream/LICENSE`
- Create: `sources/third_party/codex-cortex/upstream/skills/cqrs-event-sourcing/SKILL.md`
- Create: `sources/third_party/codex-cortex/upstream/skills/cqrs-event-sourcing/references/cqrs-patterns.md`
- Create: `sources/third_party/codex-cortex/upstream/skills/cqrs-event-sourcing/references/event-sourcing.md`
- Create: `sources/third_party/codex-cortex/upstream/skills/cqrs-event-sourcing/references/event-store-tech.md`
- Create: `sources/third_party/codex-cortex/upstream/skills/cqrs-event-sourcing/references/consistency-patterns.md`
- Create: `sources/third_party/codex-cortex/upstream/skills/cqrs-event-sourcing/references/best-practices.md`
- Create: `sources/first_party/skills/codex-cortex/intake.json`
- Create: `sources/first_party/skills/codex-cortex/decisions.json`
- Create: `sources/first_party/skills/codex-cortex/decisions.md`
- Create: `provenance/codex-cortex.md`

- [ ] **Step 1: Write the custody snapshot**

Capture only the retained Claude-Cortex evidence needed for `cqrs-event-sourcing`: upstream license, the skill source, and the five reference files that the skill links to. Keep later Claude-Cortex candidates out of the custody tree.

- [ ] **Step 2: Record the import decision**

Write the first-party intake and decision ledger for `cqrs-event-sourcing`, including the pinned upstream repo, commit, license, import boundary, and the explicit non-goal that later Claude-Cortex candidates are not imported.

- [ ] **Step 3: Record the provenance note**

Write `provenance/codex-cortex.md` so the custody surface has a durable source anchor and reviewable rights trail separate from the installable projection.

### Task 2: Build the installable `architecture-pack` projection

**Files:**
- Create: `codex-marketplace/plugins/architecture-pack/.codex-plugin/plugin.json`
- Create: `codex-marketplace/plugins/architecture-pack/README.md`
- Create: `codex-marketplace/plugins/architecture-pack/SOURCE.md`
- Create: `codex-marketplace/plugins/architecture-pack/LICENSE`
- Create: `codex-marketplace/plugins/architecture-pack/assets/icon.svg`
- Create: `codex-marketplace/plugins/architecture-pack/references/bundle-manifest.json`
- Create: `codex-marketplace/plugins/architecture-pack/references/source-map.md`
- Create: `codex-marketplace/plugins/architecture-pack/skills/cqrs-event-sourcing/SKILL.md`
- Create: `codex-marketplace/plugins/architecture-pack/skills/cqrs-event-sourcing/references/cqrs-patterns.md`
- Create: `codex-marketplace/plugins/architecture-pack/skills/cqrs-event-sourcing/references/event-sourcing.md`
- Create: `codex-marketplace/plugins/architecture-pack/skills/cqrs-event-sourcing/references/event-store-tech.md`
- Create: `codex-marketplace/plugins/architecture-pack/skills/cqrs-event-sourcing/references/consistency-patterns.md`
- Create: `codex-marketplace/plugins/architecture-pack/skills/cqrs-event-sourcing/references/best-practices.md`

- [ ] **Step 1: Author the plugin shell**

Define `architecture-pack` as the installable plugin, keep its skill root at `./skills/`, and point the metadata back to the retained `codex-cortex` custody surface.

- [ ] **Step 2: Adapt the seed skill**

Rewrite `cqrs-event-sourcing` for Codex installability: keep CQRS/event-sourcing guidance, strip Claude-Cortex-specific command or runtime assumptions, and keep the skill narrow to the single seed slice.

- [ ] **Step 3: Wire the bundle manifest and source map**

Record the source/provenance split, the retained upstream files, the first-party intake/decision records, and the single adapted skill entry in the bundle metadata.

### Task 3: Register the new surfaces in marketplace and repo-index metadata

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
- Modify: `tools/generate_repo_index.py`
- Modify: `tools/validate_marketplace.py` if new path checks or source custody checks are needed

- [ ] **Step 1: Add the new marketplace root**

Insert `architecture-pack` into the protected marketplace root inventory and regenerate the marketplace manifest surfaces.

- [ ] **Step 2: Add the new repo-index entries**

Teach the repo-index generator about the new `architecture-pack` marketplace plugin and the `sources/third_party/codex-cortex` custody zone so index regeneration stays deterministic.

- [ ] **Step 3: Update the human-facing root lists**

Refresh the active-root descriptions in the repo docs and scoped AGENTS files so they describe the current protected marketplace set instead of the pre-MARK-172 inventory.

### Task 4: Generate and validate the installable artifact

**Files:**
- Modify: `generated/skill-zips/registry.json`
- Create or modify: `generated/skill-zips/architecture-pack/cqrs-event-sourcing/skill.zip`

- [ ] **Step 1: Regenerate the seed skill zip**

Run: `py -3 tools/update_skill_artifacts.py --skill architecture-pack/cqrs-event-sourcing`
Expected: one deterministic `skill.zip` under `generated/skill-zips/architecture-pack/cqrs-event-sourcing/` and a matching registry entry.

- [ ] **Step 2: Validate the marketplace and generated surfaces**

Run:

```powershell
py -3 tools/validate_marketplace.py
py -3 tools/generate_repo_index.py
py -3 tools/validate_repo_index.py
py -3 tools/validate_skill_zips.py
py -3 tools/validate_generated_drift.py --base origin/main
git diff --check
```

Expected: pass, with any failure pointing directly to the new custody, projection, registry, or generated-artifact surface.

- [ ] **Step 3: Capture publication evidence**

Record the branch name, final head SHA, changed files, generated zip path, validation output, and a clear statement that no later Claude-Cortex candidates were imported.
