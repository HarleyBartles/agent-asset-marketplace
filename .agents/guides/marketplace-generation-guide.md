# Marketplace Generation Guide

Use this reference when working with marketplace generation, validation, and regeneration in the agent-asset-marketplace repo. This guide covers the canonical tooling, when to regenerate, and what validation to run.

## Before You Begin: Read the Standards

- **[`docs/custody-and-projection-doctrine.md`](../../docs/custody-and-projection-doctrine.md)** — source custody rules, provenance modes, plugin curation rules
- **[`tools/AGENTS.md`](../../tools/AGENTS.md)** — marketplace generation and validation tooling

## Canonical Tooling

### Local Rebuild (Write Mode)
```bash
py -3 tools/rebuild_marketplace.py --apply
```

In a shared or git-worktree checkout, also pass `--allow-shared-checkout` to approve writes.

This is the canonical local rebuild and validation entrypoint. It:
- Regenerates all marketplace projections
- Refreshes installed skills
- Runs all validation checks
- Performs git diff checks on changed files

Use this when you have made changes to source custody, adapter files, projection plugin shapes, bundle manifests, source maps, provenance maps, or generated zips.

### What `rebuild_marketplace.py` does

`rebuild_marketplace.py` is the canonical **local full reconciliation** command. It writes derived marketplace surfaces and then validates them. Think of it as the single "refresh marketplace" call.

#### Editable inputs (do not edit the derived surfaces by hand)

- `codex-marketplace/custody-pack-registry.json` — which skills belong to which pack
- `codex-marketplace/plugin-roots.json` — discovered active plugin roots
- `sources/first_party/skills/<skill>/` — first-party skill source custody
- `sources/third_party/<upstream>/` — retained upstream source custody
- `adapters/codex/<pack>/<skill>/` — adaptation overlays for third-party skills

#### Execution flow

The script runs the generator/validator stack in order:

1. `generate_plugin_root_inventory.py` — refreshes `codex-marketplace/plugin-roots.json`.
2. Prune stale plugin roots — removes `codex-marketplace/plugins/<name>` directories that are no longer in the active inventory.
3. `heal_overlays.py` — auto-repairs `overlay.yaml` line-edit anchors after source normalization.
4. `update_skill_artifacts.py --all` — the core materialization stage:
   - `generate_marketplace.py` → `.agents/plugins/marketplace.json`, `codex-marketplace/manifest.json`
   - `generate_repo_index.py` → `repo-index/repo-index.json`
   - `generate_pack_manifests.py` → per-pack `references/bundle-manifest.json` and generated `README.md`/`SOURCE.md`/`PROJECTION.md` blocks
   - `generate_all_mega_packs.py` → mega-pack bundle manifests
   - `project_skills.py` → projected skill trees under `codex-marketplace/plugins/<pack>/skills/` and flat zips under `generated/skill-zips/<skill>.zip`
   - `generate_provenance_maps.py` → per-pack `references/provenance-map.json`
   - `generate_source_maps.py` → per-pack `references/source-map.md`
   - `generate_first_party_skill_catalog.py` → `provenance/first-party-skills.md`
5. `normalize_first_party_skill_sources.py --check` — verifies first-party source shape.
6. `refresh_installed_skills.py --apply` — refreshes `.agents/skills/` for plugins marked `INSTALLED_BY_DEFAULT`.
7. `generate_repo_index.py` — writes the final `repo-index/repo-index.json`.
8. `validate_marketplace.py --skip-freshness-checks` — structural validation of plugin trees, manifests, bundle manifests, and projections.
9. `generate_repo_index.py --check` — confirms `repo-index/repo-index.json` is current.
10. `generate_index_mesh.py` — regenerates repo-wide `INDEX.md` navigation mesh.
11. `generate_index_mesh.py --check` — confirms the mesh is current.
12. `generate_first_party_skill_catalog.py --check` — confirms the first-party catalog is current.
13. `validate_repo_index.py` — metadata alignment check.
14. `validate_skill_zips.py` — checks flat skill zip shape and contents.
15. `git diff --check` on changed paths — whitespace/formatting gate.

#### Key outputs

- Marketplace manifests: `.agents/plugins/marketplace.json`, `codex-marketplace/manifest.json`
- Plugin roots: `codex-marketplace/plugins/<pack>/skills/<skill>/`
- Bundle manifests: `codex-marketplace/plugins/<pack>/references/bundle-manifest.json`
- Source/provenance maps: `codex-marketplace/plugins/<pack>/references/source-map.md`, `provenance-map.json`
- Skill zips: `generated/skill-zips/<skill>.zip`
- First-party catalog: `provenance/first-party-skills.md`
- Repo index: `repo-index/repo-index.json`
- Index mesh: `INDEX.md` files throughout the repo
- Installed skills: `.agents/skills/<skill>/`

#### When it fails

- A missing `README.md`/`SOURCE.md`/`LICENSE` in a plugin root usually means a hand-maintained pack doc was deleted during a merge.
- A `project_skills` or `validate_skill_zips` failure usually means a source/overlay mismatch or a stale zip.
- A `validate_marketplace.py` failure usually means a bundle manifest or plugin manifest is out of sync with the registry.
- `heal_overlays.py` or `normalize_first_party_skill_sources.py` failures usually mean source files have drifted from the expected shape.

Run the same command again after fixing the underlying source; do not hand-edit derived outputs.

### CI Check (Read-Only Mode)
```bash
bash scripts/ci-preflight.sh --check
```

This is the canonical non-mutating CI gate. It:
- Checks if marketplace regeneration is needed
- Validates current marketplace state
- Checks installed skills freshness
- Performs git diff checks

Use this in CI to verify the committed state is current.

### Skills Installation
```bash
py -3 sources/first_party/skills/refreshing-installed-skills/scripts/refresh_installed_skills.py --apply
```

In a shared or git-worktree checkout, also pass `--allow-shared-checkout`.

Refreshes installed skills from marketplace plugins. Use this when:
- Skills have been modified in source
- Plugin configuration has changed
- You need to refresh without a full marketplace rebuild

Check mode:
```bash
py -3 sources/first_party/skills/refreshing-installed-skills/scripts/refresh_installed_skills.py --check
```

### Index Mesh Generation
```bash
py -3 sources/first_party/skills/generating-agent-mesh/scripts/generate_index_mesh.py --apply
```

In a shared or git-worktree checkout, also pass `--allow-shared-checkout`.

Regenerates the repo-wide INDEX.md mesh. Use this when:
- Files have been added or removed
- Directories have been added or removed
- You need to update navigation

Check mode:
```bash
py -3 sources/first_party/skills/generating-agent-mesh/scripts/generate_index_mesh.py --check
```

## When to Regenerate

You must run the full marketplace regeneration (`rebuild_marketplace.py --apply`) after any change to:

- Source custody under `sources/first_party/` or `sources/third_party/`
- Codex adapter/overlay files under `adapters/codex/`
- Projection plugin shapes under `codex-marketplace/plugins/`
- Bundle manifests in plugin references
- Source maps or provenance maps
- Generated skill zips

Partial regeneration is a fallback-only repair path and should not be used as a normal completion route.

## Validation Standards

After regeneration, verify:

1. **All validation checks pass** — `rebuild_marketplace.py --apply` runs validation automatically
2. **No git diff errors** — whitespace and formatting checks pass
3. **Installed skills are current** — `refresh_installed_skills.py --check` passes
4. **Index mesh is current** — `sources/first_party/skills/generating-agent-mesh/scripts/generate_index_mesh.py --check` passes

## Deterministic Pack Rule

If a skillset pack or projection lane lacks a manifest-driven generator/validator path, add one to `tools/` and wire it into the standard update/check entrypoints. Do not hand-edit projected skill trees, source maps, provenance maps, or zip artifacts.

## Editable Custody Inputs

The editable custody inputs for marketplace generation are:
- Source trees under `sources/`
- Codex overlay/adapter trees under `adapters/codex/`
- Pack registry under `codex-marketplace/custody-pack-registry.json`

Generated surfaces (manifests, projection trees, source maps, provenance maps, zip artifacts) must stay derived from these inputs.

## Source-of-Truth Split

GitHub and the repository tree prove file state, landed assets, manifests, source snapshots, provenance notes, validation scripts, and playbooks.

Linear remains the control plane for issue state, worker state, review posture, and closeout decisions. Do not treat a Linear note, worker report, or chat summary as repo truth until the repository state or an explicit follow-up issue preserves the consequence.

Generated artifacts are downstream outputs unless the repo explicitly says otherwise.
