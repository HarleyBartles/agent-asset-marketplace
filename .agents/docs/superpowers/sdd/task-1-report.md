# Task 1 Report

## What I implemented

- Added `tools/generate_plugin_root_inventory.py` as a standalone deterministic generator/checker for `codex-marketplace/plugin-roots.json`.
  - Reads `codex-marketplace/custody-pack-registry.json`.
  - Reconciles both projection-lane roots and mega-pack roots.
  - Derives each root's category from the live `.codex-plugin/plugin.json`.
  - Emits contiguous `order` values and a stable JSON shape.
- Updated `tools/rebuild_marketplace.py`.
  - Runs `py -3 tools/generate_plugin_root_inventory.py` before downstream generation.
  - Prunes immediate child directories under `codex-marketplace/plugins/` when they are no longer active roots and still look like plugin roots via `.codex-plugin/plugin.json`.
- Updated `tools/check_marketplace.py`.
  - Runs `py -3 tools/generate_plugin_root_inventory.py --check` at the top of the non-mutating check path.
- Updated `tools/validate_marketplace.py`.
  - Runs `py -3 tools/generate_plugin_root_inventory.py --check` before importing the marketplace helpers that parse `plugin-roots.json`.
  - Lazily bootstraps `marketplace_utils`, `validate_repo_index`, and `skill_zip_artifacts` after that pre-check so stale-but-valid inventory fails before validator parsing.

## What I tested and test results

- `py -3 -m py_compile tools/generate_plugin_root_inventory.py tools/rebuild_marketplace.py tools/check_marketplace.py tools/validate_marketplace.py`
  - Passed.
- `py -3 tools/generate_plugin_root_inventory.py --check`
  - Failed before the implementation was exercised against the stale inventory case.
- `py -3 tools/generate_plugin_root_inventory.py`
  - Wrote the reconciled inventory successfully.
- `py -3 tools/generate_plugin_root_inventory.py --check`
  - Passed after reconciliation with:
    - `OK codex-marketplace\plugin-roots.json`
    - `OK plugin root inventory: current`
- `py -3 tools/rebuild_marketplace.py`
  - Reached the new reconciliation and prune steps, then failed downstream because the current branch still has generators that expect plugin roots already removed from the active registry. The first concrete blocker was `generate_adventures_pack_manifest.py` raising `FileNotFoundError` for `codex-marketplace/plugins/adventures-pack/SOURCE.md` after the new prune step removed that stale root.
- `py -3 tools/check_marketplace.py`
  - Failed for the same downstream branch inconsistency via `update_skill_artifacts.py --check --full-regeneration`, again because `generate_adventures_pack_manifest.py --check` still expects `adventures-pack`.

## Files changed

- `tools/generate_plugin_root_inventory.py`
- `tools/rebuild_marketplace.py`
- `tools/check_marketplace.py`
- `tools/validate_marketplace.py`
- `.superpowers/sdd/task-1-report.md`

## Self-review findings

- The prune helper is deliberately narrow: it only deletes immediate child directories under `codex-marketplace/plugins/` that are not active roots and still contain `.codex-plugin/plugin.json`.
- `validate_marketplace.py` now performs the inventory freshness check before loading the helper modules that eagerly parse `plugin-roots.json`, which matches the task requirement instead of only failing later in validation.

## Any concerns or blockers

- Current branch state is not yet globally consistent with the new deterministic inventory/prune contract.
- `custody-pack-registry.json` no longer lists several legacy plugin roots, but downstream generators and checks still assume at least `adventures-pack` exists.
- Because another task owns the registry/docs cleanup lane, I restored all non-task verification residue and did not commit generated marketplace/tree changes outside this task's owned files.

---

## 2026-07-04 follow-up: registry-owned category reconciliation fix

### What I changed

- Updated `tools/generate_plugin_root_inventory.py` so inventory reconciliation no longer reads category from projected `.codex-plugin/plugin.json` files.
- Required `packs[*].category` directly on each active record in `codex-marketplace/custody-pack-registry.json`, including mega-pack records.
- Kept the emitted `plugin-roots.json` shape, ordering, and `manifest_path` field unchanged so the existing reconcile/check wiring still consumes the same inventory structure.
- Preserved clear registry-scoped failures by raising `ValueError` messages of the form:
  - `codex-marketplace/custody-pack-registry.json: packs[N].category must be a non-empty string`

### Tests run

- `py -3 tools/generate_plugin_root_inventory.py --check`
  - Result: failed as expected against the current live registry because `codex-marketplace/custody-pack-registry.json` does not yet include `packs[0].category`.
  - Error: `C:\WORK\repo-workspace\agent-asset-marketplace\.worktrees\codex-superpowers-powershell-adapter\codex-marketplace\custody-pack-registry.json: packs[0].category must be a non-empty string`
- Temporary inline Python verification using a copied registry with synthetic `category` values on every pack record
  - Result: passed.
  - Verified that `reconcile_plugin_root_inventory()` uses registry-owned category values directly and does not need projected plugin manifests to produce inventory rows.
- Temporary inline Python verification removing `category` from the first copied pack record
  - Result: passed.
  - Verified the missing-field failure path is explicit and names the registry temp path plus `packs[0].category`.

### Results

- Task-1 category reconciliation is now registry-owned inside the generator instead of being derived from generated plugin manifests.
- The current live worktree still cannot pass the inventory `--check` gate until the parallel registry repair lands, because the live `custody-pack-registry.json` in this branch is still missing the required `category` fields.

### Files changed

- `tools/generate_plugin_root_inventory.py`
- `.superpowers/sdd/task-1-report.md`

### Concerns

- I did not touch `codex-marketplace/custody-pack-registry.json`, per task instructions.
- The live branch still has pre-existing registry/inventory drift owned by the parallel worker, so only the focused generator checks are green right now.
