# MARK-310 Context-Safety Rename Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rename the first-party `safe-large-file-writing` skill to `context-safety`, broaden it from large-write protection into context-window and large-data-flow safety, and keep the original large-file write mechanics intact.

**Architecture:** Treat this as a full identity rename, not a compatibility alias. The canonical source moves first, the repo-worker baseline and local skill index are updated to point at the new name, and the marketplace generators are then rerun so every projection, source map, provenance map, zip, and registry entry converges on `context-safety`. In parallel, add a repo-resident provenance catalog for all first-party skills so future renames have one place to check canonical locations, projection surfaces, generated outputs, and stale-reference validation paths. Any stale `safe-large-file-writing` reference that remains after regeneration must be an explicit historical artifact, not an active surface.

**Tech Stack:** Markdown skill source, YAML frontmatter, JSON inventories/manifests, Python marketplace generators, generated skill zips.

## Global Constraints

- Preserve the existing safe temp-file, chunked append, validation, and atomic replace mechanics.
- Add context-pressure guidance that stops large context streaming before it starts, and keep `/compact` phrased as runtime-specific boundary tooling rather than a universal rescue button.
- Do not hand-edit generated zips, source maps, provenance maps, bundle manifests, or registry files when tooling can regenerate them.
- Keep provenance and marketplace source identity intact across the rename.
- Prefer a full rename to `context-safety`; do not leave a long-lived compatibility alias unless source inspection exposes a blocker that makes that unavoidable.
- Add a durable first-party skill catalog instead of a narrow rename note so future first-party skill updates do not require another spelunking pass.
- Active surfaces must be renamed. Historical planning documents may still mention the old name, but they are not part of the active skill surface.

---

### Task 1: Rename and broaden the canonical first-party skill

**Files:**
- Move: `sources/first_party/skills/safe-large-file-writing/SKILL.md` -> `sources/first_party/skills/context-safety/SKILL.md`
- Move: `sources/first_party/skills/safe-large-file-writing/agents/openai.yaml` -> `sources/first_party/skills/context-safety/agents/openai.yaml`
- Modify: `sources/first_party/skills/repo-worker-base/SKILL.md`
- Modify: `sources/first_party/skills/repo-worker-base/agents/openai.yaml`
- Modify: `.agents/skills/AGENTS.md`
- Modify: `.agents/skills/INDEX.md`

**Interfaces:**
- Consumes: the current `safe-large-file-writing` skill body, its agent prompt, and the repo-worker support references that still point at the old skill name.
- Produces: a canonical `context-safety` skill source, updated repo-worker guidance, and a local skill index that resolves the new public name.

- [x] **Step 1: Rewrite the canonical skill metadata and body**

Rename the skill identity to `context-safety` in frontmatter and update the body so it leads with context safety, not only large-file safety. Keep the existing large-file write sequence, but add explicit guidance for:

- avoiding giant inline context streams;
- chunked inspection and composition for large inputs;
- tool-call boundaries as the place to pause and checkpoint;
- `/compact` only at deliberate phase boundaries after durable state has been preserved;
- large-file writing as a subsection of the broader context-safety posture.
- Apply the same richer canonical metadata shape to every active first-party skill under `sources/first_party/skills/*`, not just the renamed skill, so the repo does not keep a grab bag of metadata formats.

- [x] **Step 2: Update repo-worker support references**

Replace the old support-skill mentions in `sources/first_party/skills/repo-worker-base/SKILL.md`, `sources/first_party/skills/repo-worker-base/agents/openai.yaml`, `.agents/skills/AGENTS.md`, and `.agents/skills/INDEX.md` so they point at `/context-safety` and the renamed source path instead of `safe-large-file-writing`.

- [x] **Step 3: Keep the active skill surface free of stale identity**

Make sure the active source tree and local skill index present `context-safety` as the public name and do not leave a second active first-party name behind.

### Task 2: Update marketplace source inventory and generator inputs

**Files:**
- Modify: `tools/generate_pack_manifests.py`
- Modify: `sources/first_party/skills/house-skills/intake.json`
- Modify: `sources/first_party/skills/house-skills/decisions.json`
- Modify: `sources/first_party/skills/house-skills/decisions.md`

**Interfaces:**
- Consumes: the renamed canonical source path and the existing house-skills source inventory for MARK-302.
- Produces: generator input that points at `context-safety`, plus source-led inventory records that no longer advertise the old name as active.

- [x] **Step 1: Move the pack manifest inputs to the renamed source**

Update `tools/generate_pack_manifests.py` so the house-skills and repo-worker-pack entries reference `sources/first_party/skills/context-safety` and the `context-safety` canonical name instead of the old path/name pair.

- [x] **Step 2: Update the first-party source inventory records**

Adjust the house-skills intake and decisions ledgers so the active source inventory records the new public name and source path, while keeping the historical MARK-302 provenance intact.

- [x] **Step 3: Preserve the rename decision in source-facing metadata**

Make sure the source-facing metadata reflects that this is a broadened safety skill, not a brand-new unrelated import.

### Task 3: Regenerate projections, zips, and registry surfaces

**Files:**
- Regenerated: `codex-marketplace/plugins/house-skills/skills/context-safety/SKILL.md`
- Regenerated: `codex-marketplace/plugins/house-skills/skills/context-safety/agents/openai.yaml`
- Regenerated: `codex-marketplace/plugins/repo-worker-pack/skills/context-safety/SKILL.md`
- Regenerated: `codex-marketplace/plugins/repo-worker-pack/skills/context-safety/agents/openai.yaml`
- Regenerated: `codex-marketplace/plugins/house-skills/references/bundle-manifest.json`
- Regenerated: `codex-marketplace/plugins/house-skills/references/source-map.md`
- Regenerated: `codex-marketplace/plugins/house-skills/references/provenance-map.json`
- Regenerated: `codex-marketplace/plugins/repo-worker-pack/references/bundle-manifest.json`
- Regenerated: `codex-marketplace/plugins/repo-worker-pack/references/source-map.md`
- Regenerated: `codex-marketplace/plugins/repo-worker-pack/references/provenance-map.json`
- Regenerated: `generated/skill-zips/house-skills/context-safety/skill.zip`
- Regenerated: `generated/skill-zips/repo-worker-pack/context-safety/skill.zip`
- Regenerated: `generated/skill-zips/registry.json`
- Regenerated: `codex-marketplace/manifest.json`
- Regenerated: `.agents/plugins/marketplace.json`
- Regenerated: `repo-index/repo-index.json`

**Interfaces:**
- Consumes: the renamed canonical source and the updated pack-manifest generator inputs.
- Produces: fully regenerated marketplace projections, matching generated zips, and a registry/index set that exposes `context-safety` as the active skill identity.

- [x] **Step 1: Regenerate from source instead of patching projections**

Run the repo tooling so the projected skill trees, bundle manifests, source maps, provenance maps, and skill zips are rebuilt from the renamed source and generator inputs.

- [x] **Step 2: Verify the old name is gone from active projections**

Confirm the regenerated `house-skills` and `repo-worker-pack` surfaces no longer expose `safe-large-file-writing` as an active skill entry, zip path, or registry item.

- [x] **Step 3: Confirm marketplace and repo-index freshness**

Ensure the generated marketplace manifest, plugin marketplace registry, and repo index all stay in sync with the rename.

### Task 4: Create the durable first-party skill catalog

**Files:**
- Create: `provenance/first-party-skills.md`
- Create: `tools/generate_first_party_skill_catalog.py`
- Modify: `.github/workflows/marketplace-validation.yml`

**Interfaces:**
- Consumes: the active first-party source tree, the renamed `context-safety` surfaces, the generated pack/projection inventory already validated in this repo, and the repo references discoverable from manifests, maps, registry surfaces, and docs.
- Produces: tooling that generates a durable repo-resident map of all first-party skills with canonical source locations, active projection or vendoring surfaces, generated artifacts, manifest/source-map touch points, workflow/doc references, and the validation path that should catch stale references after a rename.

- [x] **Step 1: Build the catalog generator from repo truth, not memory**

Implement a catalog generator that derives every first-party skill row from repo truth:

- canonical source location;
- projection or vendoring surfaces in plugins/packs;
- generated artifacts that should not be hand-edited;
- manifests, registries, and source maps that mention the skill;
- repo docs, prompts, workflow text, or skill references that use the skill by name;
- the command or validation path that should catch stale references after a rename.

- [x] **Step 2: Keep the catalog bounded and useful**

Group the generated entries so the file is easy to scan, but do not collapse it into a vague inventory dump. If a field cannot be derived reliably yet, either omit it, mark it as unresolved from inspected source, or place it in a clearly separated bounded notes section. The catalog should make future first-party renames boring without requiring another wide search.

- [x] **Step 3: Check the catalog against the active first-party tree**

The generator/check mode must verify catalog completeness by comparing discovered `sources/first_party/skills/*` entries against the generated catalog. `--check` fails if any active first-party skill is missing, stale, or has mismatched generated rows.

- [x] **Step 4: Add write and check modes for the catalog**

Add a write mode that refreshes `provenance/first-party-skills.md` from the current repo truth, and a `--check` mode that fails if the committed catalog is stale.

- [x] **Step 5: Put the catalog check in CI**

Add the catalog generator check to `.github/workflows/marketplace-validation.yml` so the same validator that guards the PR also runs in CI. If any additional validator or catalog-related check is introduced for this issue, wire it into that workflow as well.

- [x] **Step 6: Normalize all active first-party skill sources**

Add a repo tool that rewrites every active first-party `SKILL.md` and existing `agents/openai.yaml` to the canonical rich metadata shape, then run it across the active first-party skill tree. The tool must have a `--check` mode, and that check must also run in CI.

### Task 5: Validate cleanup and publish the plan-only branch

**Files:**
- Check: `generated/skill-zips/registry.json`
- Check: `codex-marketplace/plugins/house-skills/references/bundle-manifest.json`
- Check: `codex-marketplace/plugins/repo-worker-pack/references/bundle-manifest.json`
- Check: `repo-index/repo-index.json`
- Check: `codex-marketplace/manifest.json`
- Check: `.agents/plugins/marketplace.json`

**Interfaces:**
- Consumes: the regenerated outputs from Task 3.
- Produces: validation evidence that the rename is coherent and the stale-name cleanup is real.

- [x] **Step 1: Run the repo's marketplace and zip validations**

Run:

```powershell
py -3 tools/normalize_first_party_skill_sources.py --check
py -3 tools/update_skill_artifacts.py --check
py -3 tools/generate_first_party_skill_catalog.py --check
py -3 tools/generate_marketplace.py --check
py -3 tools/generate_repo_index.py --check
py -3 tools/validate_marketplace.py
py -3 tools/materialize_projection.py --check
py -3 tools/generate_mega_packs.py --check
py -3 tools/generate_provenance_maps.py --check
py -3 tools/generate_source_maps.py --check
py -3 tools/validate_repo_index.py
py -3 tools/validate_skill_zips.py
git diff --check
```

Expected result: the active surfaces validate, the generated zips and registries agree, the provenance and source maps are current, and `safe-large-file-writing` is absent from the active rename surfaces.

- [x] **Step 2: Keep any remaining old-name text quarantined**

If `safe-large-file-writing` still appears, it must be in historical plan text or other intentionally archival surfaces, not in the active skill tree, manifest, registry, or repo-worker baseline.
