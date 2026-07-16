# Superpowers Registry Prune Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make `codex-marketplace/custody-pack-registry.json` the single source of truth for projected plugin roots, prune stale projected roots deterministically, restore the active marketplace roots that were accidentally dropped from the registry, and remove the redundant `superpowers-mega-pack` projection while keeping `superpowers-plus` as the retained Superpowers projection-lane bundle.

**Architecture:** A small generator reconciles the editable plugin-root inventory against the pack registry, and the rebuild/check validators call that generator before any downstream surfaces are regenerated. The rebuild path also prunes obsolete projected plugin directories by comparing the active root inventory to the immediate children of `codex-marketplace/plugins/`, so removing a registry node is enough to remove the projected root cleanly. Documentation and bundle prose are updated to reflect that `superpowers-plus` is the retained mixed projection-lane bundle and there is no separate `superpowers-mega-pack` source of truth anymore.

**Tech Stack:** Python 3, existing marketplace generator scripts, GitHub PR branch workflow, PowerShell shell.

## Global Constraints

- Third-party source custody is immutable; changes to third-party behavior belong in adapters/overlays or generated projections, not in `sources/third_party/`.
- First-party source is mutable directly; no adapter layer is required for first-party custody.
- `codex-marketplace/custody-pack-registry.json` is the editable routing source of truth for pack/projection generation and must retain the active roots already present in the marketplace unless a task explicitly removes one.
- Generated surfaces must be regenerated, not hand-edited.
- Remove stale projected roots deterministically when the registry no longer declares them.
- Keep the existing PR and branch; do not open a new PR.

---

### Task 1: Add deterministic plugin-root reconciliation and pruning

**Files:**
- Create: `tools/generate_plugin_root_inventory.py`
- Modify: `tools/rebuild_marketplace.py`
- Modify: `tools/check_marketplace.py`
- Modify: `tools/validate_marketplace.py`

**Interfaces:**
- Consumes: `codex-marketplace/custody-pack-registry.json`, `codex-marketplace/plugin-roots.json`
- Produces: a reconciled `codex-marketplace/plugin-roots.json`, plus removal of projected plugin directories that are no longer listed in the registry

- [ ] **Step 1: Wire the generator into the full rebuild path**

Add a first-class call to `py -3 tools/generate_plugin_root_inventory.py` near the top of `tools/rebuild_marketplace.py` so the root inventory is reconciled before any downstream generators run.

- [ ] **Step 2: Wire the generator into the non-mutating check path**

Add `py -3 tools/generate_plugin_root_inventory.py --check` to `tools/check_marketplace.py` so CI fails when the editable root inventory has drifted from the registry.

- [ ] **Step 3: Make validation prove the inventory is current**

Call `py -3 tools/generate_plugin_root_inventory.py --check` from `tools/validate_marketplace.py` before it parses `codex-marketplace/plugin-roots.json`, so a syntactically valid but stale inventory still fails validation even when the JSON shape itself is valid.

- [ ] **Step 4: Prune stale projected plugin roots during rebuild**

Add a rebuild helper that loads the reconciled active root names and deletes immediate children of `codex-marketplace/plugins/` whose names are not present in that set. The helper must only remove projected plugin directories, must not recurse into source custody, and must leave non-plugin tracked files alone.

- [ ] **Step 5: Verify the new generator is deterministic**

Run:
`py -3 tools/generate_plugin_root_inventory.py --check`
Expected: `OK ... plugin root inventory: current` after the registry and inventory are aligned.

- [ ] **Step 6: Verify rebuild/check still pass after the hook is in place**

Run:
`py -3 tools/rebuild_marketplace.py`
`py -3 tools/check_marketplace.py`
Expected: both commands complete without leaving a stale projected plugin root behind, and the workspace diff shows no hand-edited generated residue for the removed pack.

### Task 2: Remove the redundant `superpowers-mega-pack` projection and update the source-of-truth prose

**Files:**
- Modify: `codex-marketplace/custody-pack-registry.json`
- Modify: `codex-marketplace/plugin-roots.json`
- Modify: `codex-marketplace/AGENTS.md`
- Modify: `codex-marketplace/README.md`
- Modify: `docs/custody-and-projection-doctrine.md`
- Modify: `codex-marketplace/plugins/superpowers-plus/README.md`
- Modify: `codex-marketplace/plugins/superpowers-plus/PROJECTION.md`
- Modify: `codex-marketplace/plugins/superpowers-plus/SOURCE.md`

**Interfaces:**
- Consumes: the registry-led projection model from Task 1
- Produces: docs and registry state that describe `superpowers-plus` as the retained mixed projection-lane bundle without claiming a separate `superpowers-mega-pack`

- [ ] **Step 1: Remove the `superpowers-mega-pack` pack node from the registry**

Delete the `superpowers-mega-pack` entry from `codex-marketplace/custody-pack-registry.json` so the registry no longer requests that projected root.

- [ ] **Step 2: Restore the active marketplace roots that were accidentally dropped**

Re-add the missing live marketplace roots that still exist in `codex-marketplace/plugins/` and were present in the prior shape of the marketplace, including their stable routing metadata such as category, so the registry keeps the broad plugin output stable while only the redundant `superpowers-mega-pack` root is removed.

- [ ] **Step 3: Reconcile the active plugin-root inventory**

Regenerate `codex-marketplace/plugin-roots.json` so the removed registry node disappears from the active root list instead of being hand-edited.

- [ ] **Step 4: Update marketplace guidance to describe the actual final shape**

Rewrite the repo guidance and the `superpowers-plus` bundle prose so they say:
`superpowers-plus` is the mixed projection-lane bundle over retained Superpowers source,
`superpowers-mega-pack` is not a maintained projection surface,
and the registry determines which roots are projected.

- [ ] **Step 5: Keep the wording consistent across the projection surfaces**

Make the `README.md`, `PROJECTION.md`, and `SOURCE.md` for `superpowers-plus` say the same thing about the retained bundle shape and avoid any phrase that implies a separate pure-third-party mega pack still exists.

- [ ] **Step 6: Regenerate the docs sanity checks by inspection**

Re-read the updated files and confirm there is no remaining prose that names `superpowers-mega-pack` as an active bundle or describes `superpowers-plus` as a mega pack.

### Task 3: Regenerate the whole marketplace and validate the branch

**Files:**
- Generated marketplace outputs under `codex-marketplace/plugins/`
- Generated registry and manifest surfaces under `.agents/plugins/`, `codex-marketplace/manifest.json`, `repo-index/repo-index.json`, and the index mesh

**Interfaces:**
- Consumes: the reconciled registry and updated docs from Tasks 1 and 2
- Produces: a clean generated tree with no stale `superpowers-mega-pack` projection and with `superpowers-plus` still present

- [ ] **Step 1: Rebuild the marketplace from the edited registry**

Run `py -3 tools/rebuild_marketplace.py` from the branch root so the registry, manifests, projected plugin trees, and generated surfaces are all refreshed in one deterministic pass.

- [ ] **Step 2: Run the non-mutating checks**

Run `py -3 tools/check_marketplace.py` and `py -3 tools/generate_index_mesh.py --check` to confirm the working tree is clean after regeneration and the generated index mesh stayed in sync.

- [ ] **Step 3: Confirm the stale mega-pack root is gone**

Verify `codex-marketplace/plugins/superpowers-mega-pack/` no longer exists and that `codex-marketplace/plugin-roots.json` does not reintroduce it.

- [ ] **Step 4: Publish the updated existing PR**

Commit the regenerated tree on the existing branch, push the branch, and update the current PR body if needed so it accurately describes the narrower final state: registry-led projection, deterministic pruning, and removal of the redundant mega pack.
