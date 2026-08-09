# Zone-level INDEX.json sidecars

## Problem

The repository currently keeps all machine-readable index metadata in a single `INDEX.json` at the repo root (formerly `repo-index/repo-index.json`). This one file is responsible for:

- the zone registry
- the marketplace plugin inventory and registry alignment
- the repo-wide validation command map
- cross-zone invariants

That violates the same locality principle the `INDEX.md` mesh follows: navigation and authority should live as close as possible to the thing they describe.

## Goal

Distribute the monolithic root `INDEX.json` into per-zone `INDEX.json` sidecars while keeping the `INDEX.md` mesh unchanged. The root `INDEX.json` becomes a thin registry of zones. Each zone sidecar owns its own metadata and any zone-specific data. The result is a machine-readable mesh that mirrors the `INDEX.md` navigation mesh but at a coarser, more meaningful granularity.

## Design

### Keep INDEX.md untouched

The per-directory `INDEX.md` mesh remains the primary human/agent navigation surface. It lists children, provides routing, and stays lightweight.

### What is a zone root

A zone root is a top-level responsibility boundary in the repository. It is a directory (or, in the case of a single-file surface, the file's parent) that has its own `AGENTS.md`/`.devin/rules/` guidance, its own `surface_kind`, and at least one validation or generation command that applies specifically to it. Zone roots are coarser than the per-directory `INDEX.md` mesh. They are the directories where a tool or agent first enters the repo and needs to know which rule set applies.

### Add INDEX.json at zone roots

A `INDEX.json` file is added at each zone root. It is generated, read-only, and carries structured metadata that the `INDEX.md` mesh does not currently express:

- `name` — zone name
- `path` — zone path relative to repo root
- `surface_kind` — `hand-authored`, `generated`, `runtime-facing`, `provenance`, etc.
- `purpose` — one-line description of the zone
- `nearest_scoped_agents_md` — path to the nearest `AGENTS.md` or `null`
- `key_validation_scripts` — list of validation/generation scripts that matter to the zone
- zone-specific data (e.g., `marketplace_plugins` in `codex-marketplace/INDEX.json`)

### Root INDEX.json becomes a registry

Root `INDEX.json` only lists zones and points to their sidecars. It also keeps the repo-wide `validation` command map because many commands are cross-zone.

```json
{
  "schema_version": 2,
  "repo_name": "agent-asset-marketplace",
  "description": "Registry of zone INDEX.json sidecars.",
  "validation": {
    "marketplace": "py -3 tools/validate_marketplace.py",
    "repo_index": "py -3 tools/validate_repo_index.py",
    "repo_index_generate": "py -3 tools/generate_repo_index.py --apply",
    "marketplace_generate": "py -3 tools/generate_marketplace.py --apply",
    "marketplace_check": "py -3 tools/generate_marketplace.py --check",
    "repo_index_check": "py -3 tools/generate_repo_index.py --check"
  },
  "zones": [
    {
      "name": "codex-marketplace",
      "path": "codex-marketplace",
      "index_json": "codex-marketplace/INDEX.json"
    }
  ]
}
```

### Zone sidecar example

`codex-marketplace/INDEX.json`:

```json
{
  "name": "codex-marketplace",
  "path": "codex-marketplace",
  "purpose": "Codex marketplace source root and export manifest surface.",
  "surface_kind": "runtime-facing",
  "nearest_scoped_agents_md": ".devin/rules/codex-marketplace.md",
  "key_validation_scripts": [
    "tools/validate_marketplace.py",
    "tools/validate_repo_index.py"
  ],
  "marketplace_plugins": [
    {
      "name": "agentic-evaluation",
      "plugin_root": "codex-marketplace/plugins/agentic-evaluation",
      ...
    }
  ]
}
```

### Tooling changes

- `tools/marketplace_utils.py`
  - `REPO_INDEX_PATH` stays at `ROOT / "INDEX.json"`.
  - Add `load_zone_indexes()` or `merged_repo_index()` helper.

- `tools/generate_repo_index.py`
  - After building the aggregate, writes root `INDEX.json` and one `INDEX.json` per zone root.
  - May split into a `ZoneIndexBuilder` and `RepoIndexBuilder` later.

- `tools/validate_repo_index.py`
  - Read root `INDEX.json`.
  - For each zone, load `<zone>/INDEX.json`, validate the sidecar schema.
  - Merge zone sidecars into an aggregate and run the same invariants as today (plugin list matches registry, alignment, no duplicates, etc.).

- `tools/validate_marketplace.py`
  - `validate_index()` now checks the root `INDEX.json` and the zone sidecars.
  - During Phase 1 and 2, keep `check_text(REPO_INDEX_README_PATH)` for `repo-index/README.md`.
  - During Phase 3, remove `REPO_INDEX_README_PATH` and the stale `repo-index/` directory once its guidance has moved.

### Zones to start with

Use the existing `zones` list from the current root `INDEX.json` as the jumping-off point. For each zone, generate an `INDEX.json` and prove it earns its keep. If a zone has no structured metadata that the `INDEX.md` mesh does not already cover, that zone does not get a sidecar.

Candidate initial zones:

- `.agents/plugins` — runtime registry
- `codex-marketplace` — marketplace root and plugin inventory
- `codex-marketplace/plugin-roots.json` — hand-authored inventory surface
- `codex-marketplace/plugins` — protected plugin packs
- `tools` — validation and generation scripts
- `repo-index` or repo root — to be retired/merged

### Tooling ownership

- `tools/run.py` `repo-index` target remains the generator and validator of `INDEX.json` sidecars.
- `tools/run.py` `mesh` target continues to own the per-directory `INDEX.md` mesh and does not generate `INDEX.json`.
- `tools/run.py` `marketplace` target consumes the merged zone sidecars through `validate_repo_index.py`.

### Schema version and transition

- Root and zone `INDEX.json` files use `schema_version: 2`.
- `validate_repo_index.py` only needs to support `schema_version: 2` once the change lands; there is no v1/v2 compatibility requirement because this is a single PR that regenerates the files.
- `generate_repo_index.py` produces the new schema and writes both root and zone sidecars in one pass.

### Migration

Phase 1: Pilot zone
1. Update `tools/marketplace_utils.py` `REPO_INDEX_PATH` to root `INDEX.json` (already spiked).
2. Refactor `generate_repo_index.py` to write the root `INDEX.json` registry and the `codex-marketplace/INDEX.json` sidecar.
3. Refactor `validate_repo_index.py` to load the root registry and merge the `codex-marketplace` sidecar.
4. Run `py -3 tools/run.py ci --check`. Keep the `repo-index/README.md` surface untouched during the pilot.

Phase 2: Remaining zones
5. Add sidecars for the other existing zones one at a time, proving each sidecar carries non-duplicative metadata.
6. For each new sidecar, run `py -3 tools/run.py ci --check` before committing it.

Phase 3: Retire repo-index/
7. Move or merge `repo-index/README.md` guidance into `.agents/docs/repo-index.md` or a short section in the root `README.md`.
8. Remove the `repo-index/` directory and any generated `repo-index/INDEX.md`.
9. Run `py -3 tools/run.py mesh --apply` and `py -3 tools/run.py ci --check`.

## Success criteria

- `py -3 tools/run.py ci --check` passes.
- `INDEX.json` at the root is a thin registry and no longer a monolithic data dump.
- Each zone sidecar contains metadata that `INDEX.md` does not already provide.
- `validate_repo_index.py` and `validate_marketplace.py` still enforce the same invariants without regressions.

## Out of scope

- Replacing `INDEX.md` with `INDEX.json` in the per-directory mesh.
- Adding new metadata fields beyond what is already required for validation.
- Changing the marketplace registry format or plugin manifests.

## Risks and mitigations

| Risk | Mitigation |
|------|------------|
| Zone sidecar becomes a duplicate of `INDEX.md` | Require each sidecar to carry at least one structured field not in `INDEX.md`; excise failures. |
| `validate_repo_index.py` becomes complex | Split loading/merging into a helper; keep validation logic unchanged. |
| Marketplace plugin validation breaks | Move `marketplace_plugins` to `codex-marketplace/INDEX.json` and validate the merged aggregate. |
| `repo-index/` README becomes stale | Retire or redirect the README in the same change. |
