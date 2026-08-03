# Remove the projection layer — Phase 1: Demolition

> **Status:** Executed and merged in PR #253 (`feat/remove-projection-layer`, `417e7f97b80803437f2d1a9966200874291d0021`) on 2026-08-01. This plan is now a historical record and lives in `.agents/plans/completed/`.

> **For agentic workers:** REQUIRED SUB-SKILL: Use `/subagent-driven-development` (recommended) or `/executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Delete the `sources/` custody tree, the custody-pack registry, and the tooling that exists only to project from custody into plugins. After this phase, `codex-marketplace/plugins/<plugin>/skills/<name>/` is the only canonical home for a skill.

**Architecture:** This phase removes `sources/first_party/`, `sources/third_party/`, `codex-marketplace/custody-pack-registry.json`, and the projection-only `tools/` scripts. The plugin manifests in `codex-marketplace/plugin-roots.json` and `codex-marketplace/plugins/<plugin>/.codex-plugin/plugin.json` remain as the marketplace source of truth. Existing plugin skill trees are already the vendored copies, so the repo keeps working once the registry is gone.

**Tech Stack:** Python 3.12, the existing `tools/run.py` / `tools/validate_marketplace.py` tooling, and `git`.

## Global Constraints

- CI must remain green after each task; run `py -3 tools/run.py ci --check` before every commit.
- No hand-editing of generated `codex-marketplace/plugins/<plugin>/skills/` trees; those are now the canonical source.
- Delete a file rather than adapt it if its only purpose was to service the removed custody/projection pipeline.
- Update `AGENTS.md` and runbook references in the same phase so doctrine does not drift.
- Create a `git tag` backup before demolition (`git tag pre-remove-projection-layer`) so the old state is trivially inspectable.

## Discovery findings (read-only pass, do not edit in this section)

### File/classification inventory

- `sources/first_party/` — 421 tracked references. The only non-generated/legitimate references are in `AGENTS.md`, `.agents/docs/AGENTS.md`, `docs/custody-and-projection-doctrine.md`, and the plan files. Everything else is generated or projection support.
- `sources/third_party/` — 142 tracked references. Same pattern: generated maps, bundle manifests, validators, and historical provenance notes.
- `codex-marketplace/custody-pack-registry.json` — 60 references. Referenced by `tools/generate_pack_manifests.py`, `tools/generate_plugin_root_inventory.py`, `tools/superpowers_source.py`, `tools/validate_marketplace.py`, several test files, and a handful of docs/runbooks.
- `projection` — 414 references. The bulk are in the generated `references/provenance-map.json`, `references/source-map.md`, `agents/openai.yaml` (`projection_plugin` metadata field), and `tools/validate_marketplace.py`.

### Tool fate

**Delete without replacement:**
- `tools/project_skills.py`
- `tools/skill_projection_helpers.py`
- `tools/generate_provenance_maps.py`
- `tools/generate_source_maps.py`
- `tools/update_skill_artifacts.py`
- `tools/generate_first_party_skill_catalog.py`
- `tools/normalize_first_party_skill_sources.py`
- `tools/update_superpowers_source.py`
- `tools/superpowers_source.py`
- `tools/check_superpowers_output_paths.py`

**Edit/retain:**
- `tools/generate_pack_manifests.py` — remove `custody-pack-registry.json` read; generate pack bundle manifests by scanning each plugin's `skills/` tree.
- `tools/generate_plugin_root_inventory.py` — remove `custody-pack-registry.json` read if present.
- `tools/marketplace_utils.py` — remove registry constants but keep marketplace manifest helpers.
- `tools/validate_marketplace.py` — delete the projection phase and all source-custody mirror checks (see function list in Task 4).
- `tools/validate_repo_index.py` — remove the `sources/third_party` zone check.
- `tools/validate_authority_assets.py` — remove `sources/first_party/skills` from discovery roots and `first_party_synthesis` from `CONTENT_MODES`.
- `tools/skill_validation.py` — remove path-based first-party detection.
- `tools/validate_agents_md.py` — remove the `sources/third_party/superpowers/obra-superpowers/v6.2.0/AGENTS.md` entry.
- `tools/run.py` — remove the `project` target and its `marketplace`/`ci` dependencies.

### `validate_marketplace.py` functions to remove

- `validate_projection_materializer`
- `validate_tree_mirror`
- `validate_tree_reconstruction`
- `_files_match_canonicalized`
- `_trees_match_canonicalized`
- `_validate_superpowers_provenance_map`
- `validate_superpowers_bundle_manifest`
- `validate_superpowers_projection`
- `validate_first_party_tree_mirror`
- `validate_third_party_tree_mirror`
- `_validate_verbatim_entry`
- `validate_verbatim_projections`
- `validate_normalised_projections`
- `validate_adapted_projections`
- `_validate_adapted_entry`
- `validate_projection_phase`

Simplify `validate_pack_manifests` and `check_phase` to remove projection handling.

### Skill copy verification

The plugin skill copies are **functionally** the same as `sources/first_party/skills/<name>/`, but **not byte-identical** in `agents/openai.yaml` because the projection added `projection_plugin` and `plugin` metadata fields to the plugin copy. The plugin copy is the richer/canonical one once `sources/` is deleted, but the `projection_plugin` field becomes dead metadata and should be stripped (see Task 7).

---

### Task 1: Remove the `sources/` tree

**Files:**
- Delete: `sources/first_party/` (entire tree)
- Delete: `sources/third_party/` (entire tree)
- Delete: `sources/INDEX.md`
- Delete: `sources/README.md`

**Interfaces:**
- Consumes: none
- Produces: a repo with no `sources/` directory

- [ ] **Step 1: Delete the `sources/` tree**

```bash
rm -r sources
rm sources/INDEX.md
rm sources/README.md
```

- [ ] **Step 2: Stage the deletion**

```bash
git add -A
git status
```

- [ ] **Step 3: Commit**

```bash
git commit -m "chore: remove sources/ custody tree

Remove sources/first_party/ and sources/third_party/.
Skills now live directly in the vendored plugin trees."
```

---

### Task 2: Remove the custody-pack registry and generated provenance/source maps

**Files:**
- Delete: `codex-marketplace/custody-pack-registry.json`
- Delete: `codex-marketplace/plugins/*/references/provenance-map.json` (all)
- Delete: `codex-marketplace/plugins/*/references/source-map.md` (all)
- Delete: `provenance/first-party-skills.md`
- Delete: `provenance/unslop.md`
- Delete: `provenance/superpowers-plus.md`
- Modify: `provenance/INDEX.md` to remove entries for deleted provenance notes

**Interfaces:**
- Consumes: none
- Produces: a repo without custody-pack registry; plugin `references/` may be recreated later from plugin manifests

- [ ] **Step 1: Remove the registry and generated references**

```bash
rm codex-marketplace/custody-pack-registry.json
rm codex-marketplace/plugins/*/references/provenance-map.json
rm codex-marketplace/plugins/*/references/source-map.md
rm provenance/first-party-skills.md
rm provenance/unslop.md
rm provenance/superpowers-plus.md
```

- [ ] **Step 2: Edit `provenance/INDEX.md` to remove deleted provenance links**

Open `provenance/INDEX.md` and delete the list items that pointed to the removed files.

- [ ] **Step 3: Commit**

```bash
git add -A
git commit -m "chore: remove custody-pack registry and generated provenance/source maps

The custody-pack-registry.json and the generated provenance/source maps
only made sense when skills were projected from a separate custody layer.
They are no longer needed."
```

---

### Task 3: Delete projection-only tools

**Files to delete:**
- `tools/project_skills.py`
- `tools/skill_projection_helpers.py`
- `tools/generate_provenance_maps.py`
- `tools/generate_source_maps.py`
- `tools/update_skill_artifacts.py`
- `tools/generate_first_party_skill_catalog.py`
- `tools/normalize_first_party_skill_sources.py`
- `tools/update_superpowers_source.py`
- `tools/superpowers_source.py`
- `tools/check_superpowers_output_paths.py`

**Files to modify:**
- `tools/INDEX.md` — remove deleted tool links
- `tools/run.py` — remove the `project` target and its call chain

**Interfaces:**
- Consumes: plugin manifests from `codex-marketplace/plugin-roots.json`
- Produces: a smaller `tools/` tree whose remaining tools read directly from `codex-marketplace/plugins/`

- [ ] **Step 1: Inspect each tool and delete if projection-only**

For each of the scripts above, read the first 30 lines. If the docstring or imports reference `sources/first_party`, `sources/third_party`, `custody-pack-registry`, or `projection`, delete the file.

```bash
git rm tools/generate_first_party_skill_catalog.py
git rm tools/normalize_first_party_skill_sources.py
# ... repeat for each identified projection-only script
```

- [ ] **Step 2: Remove `tools/INDEX.md` links for deleted scripts**

Open `tools/INDEX.md` and delete the bullet items that point at removed files.

- [ ] **Step 3: Remove dead tool targets from `tools/run.py`**

Open `tools/run.py` and delete the `click` / `subprocess` invocations that call the removed scripts. If a `tools/run` target no longer has a backing script, delete the target.

- [ ] **Step 4: Commit**

```bash
git add -A
git commit -m "chore: remove projection-only tools

Delete scripts that generated or validated the custody-to-plugin
projection pipeline."
```

---

### Task 4: Simplify `tools/validate_marketplace.py`

**Files:**
- Modify: `tools/validate_marketplace.py`

**Interfaces:**
- Consumes: `codex-marketplace/plugin-roots.json` and plugin `.codex-plugin/plugin.json` manifests
- Produces: a validator that checks plugin shape and skill metadata but does not enforce `sources/first_party` or `custody-pack-registry.json`

- [ ] **Step 1: Read the current validator and identify custody/projection assertions**

Look for:
- references to `sources/first_party/`
- references to `sources/third_party/`
- `custody-pack-registry.json`
- `first_party`/`third_party` source-category validation
- orphan detection

- [ ] **Step 2: Delete the projection functions**

Delete these functions in `tools/validate_marketplace.py`:

```python
validate_projection_materializer
validate_tree_mirror
validate_tree_reconstruction
_files_match_canonicalized
_trees_match_canonicalized
_validate_superpowers_provenance_map
validate_superpowers_bundle_manifest
validate_superpowers_projection
validate_first_party_tree_mirror
validate_third_party_tree_mirror
_validate_verbatim_entry
validate_verbatim_projections
validate_normalised_projections
validate_adapted_projections
_validate_adapted_entry
validate_projection_phase
```

Simplify `validate_pack_manifests` and `check_phase` to only check:
- each plugin has a valid `.codex-plugin/plugin.json`
- each declared plugin root in `codex-marketplace/plugin-roots.json` exists
- each `skills/<name>/SKILL.md` has valid YAML front matter
- `source_category` and `content_mode` are allowed values

- [ ] **Step 3: Commit**

```bash
git add -A
git commit -m "chore: simplify marketplace validator

Remove source-custody and projection checks from validate_marketplace.py.
Validation is now plugin-root and plugin-manifest shape only."
```

---

### Task 5: Simplify `tools/validate_repo_index.py`

**Files:**
- Modify: `tools/validate_repo_index.py`

**Interfaces:**
- Consumes: repo-index entries
- Produces: a validator that no longer requires `sources/third_party` AGENTS or custody rules

- [ ] **Step 1: Remove `sources/third_party` AGENTS check**

Open `tools/validate_repo_index.py` and delete the block that validates the `sources/third_party` scoped AGENTS.md guidance.

- [ ] **Step 2: Commit**

```bash
git add -A
git commit -m "chore: remove sources/third_party AGENTS check from repo-index validator"
```

---

### Task 6: Remove or rewrite the custody and projection doctrine

**Files:**
- Delete: `docs/custody-and-projection-doctrine.md`
- Modify: `AGENTS.md` — remove source-custody language
- Modify: `.agents/docs/AGENTS.md` — remove `sources/first_party` and `sources/third_party` review guidance
- Modify: `.agents/runbooks/AGENTS.md` — remove `completing-plans`? (no, keep; unrelated)

**Interfaces:**
- Consumes: the repo's new shape
- Produces: documentation that matches the new no-projection, no-custody model

- [ ] **Step 1: Delete `docs/custody-and-projection-doctrine.md`**

```bash
git rm docs/custody-and-projection-doctrine.md
```

- [ ] **Step 2: Update `AGENTS.md`**

Open `AGENTS.md` and replace custody/projection language with the simpler statement that the repo's source of truth is `codex-marketplace/plugins/`.

- [ ] **Step 3: Update `.agents/docs/AGENTS.md`**

Open `.agents/docs/AGENTS.md` and remove the bullet that says "Treat `sources/first_party/**` as mutable source custody" and "Treat `sources/third_party/**` as immutable custody."

- [ ] **Step 4: Commit**

```bash
git add -A
git commit -m "chore: remove custody-and-projection doctrine

Delete the doctrine doc and update AGENTS files to reflect that
vendored plugin trees are the canonical source."
```

---

### Task 7: Strip dead `projection_plugin` metadata from plugin skills

**Files:**
- Modify: `codex-marketplace/plugins/<plugin>/skills/<name>/agents/openai.yaml` (all)

**Interfaces:**
- Consumes: the canonical plugin skill tree
- Produces: `openai.yaml` files that no longer reference the removed projection layer

- [ ] **Step 1: Remove `projection_plugin` keys from every `agents/openai.yaml`**

For each `openai.yaml` under `codex-marketplace/plugins/*/skills/`, delete the `projection_plugin` field. Keep the `plugin` field if it is used by consumers.

```python
import re
from pathlib import Path

for path in Path("codex-marketplace/plugins").glob("*/skills/*/agents/openai.yaml"):
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"^\s*projection_plugin:.*\n", "", text, flags=re.MULTILINE)
    path.write_text(text, encoding="utf-8", newline="\n")
```

- [ ] **Step 2: Commit**

```bash
git add -A
git commit -m "chore: strip projection_plugin metadata from plugin skills"
```

---

### Task 8: Regenerate the marketplace and repo index from plugin roots only

**Files:**
- Modify: `tools/run.py` — keep only `marketplace`, `repo-index`, `mesh`, `catalog`, `lint`, `repo-standards`
- Modify: `tools/marketplace_utils.py` — remove `first_party`/`third_party` and custody references
- Run: `py -3 tools/run.py marketplace --apply`
- Run: `py -3 tools/run.py ci --check`

**Interfaces:**
- Consumes: `codex-marketplace/plugin-roots.json` and plugin manifests
- Produces: regenerated `.agents/plugins/marketplace.json`, `codex-marketplace/manifest.json`, `repo-index/repo-index.json`, and mesh indexes

- [ ] **Step 1: Update `tools/marketplace_utils.py` to not reference `sources/`**

Open `tools/marketplace_utils.py` and remove any constants, helpers, or validation that reference `sources/first_party` or `sources/third_party`.

- [ ] **Step 2: Regenerate**

```bash
py -3 tools/run.py marketplace --apply
```

- [ ] **Step 3: Validate**

```bash
py -3 tools/run.py ci --check
```

- [ ] **Step 4: Commit**

```bash
git add -A
git commit -m "chore: regenerate marketplace from plugin roots only

Remove custody references from marketplace_utils.py and regenerate
all derived surfaces."
```

---

## SDD Confidence / Plan-Readiness Rating

**Rating: 8/10**

The discovery pass produced an exact inventory of files to delete, the exact `tools/` scripts that are projection-only, and the exact `validate_marketplace.py` functions to remove. The two remaining uncertainties are:

1. `tools/generate_pack_manifests.py` will need a small implementation (scan plugin `skills/` and emit `bundle-manifest.json` entries) rather than a one-line edit. The plan does not provide that implementation.
2. `tools/validate_marketplace.py` deletions may leave unused helper imports; the implementer must run `py -3 tools/run.py ci --check` after each task to catch them.

Both are manageable with the validation-first workflow, so the plan is ready for execution.
