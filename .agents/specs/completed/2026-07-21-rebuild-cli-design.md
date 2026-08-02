# rebuild_marketplace.py CLI redesign

## Goal

Make `tools/rebuild_marketplace.py` the single agent-facing entry point for both full marketplace regeneration and non-mutating CI checks, so agents no longer call the individual generator/validator scripts directly. `tools/check_marketplace.py` becomes a thin wrapper around `rebuild_marketplace.py --check`.

## Non-goals

- Replace `tools/check_marketplace.py` as a separate file; it stays as a CI convenience wrapper.
- Add per-skill or per-plugin targeted rebuilds in this change (`--plugin` / `--skill`). `update_skill_artifacts.py` does not expose per-pack/per-skill projection today, so targeting requires a separate spec.
- Change the default full-rebuild behavior; `py -3 tools/rebuild_marketplace.py` with no flags continues to do the same work it does now.

## Motivation

Today `rebuild_marketplace.py` and `check_marketplace.py` are both linear orchestrators that call sibling scripts. Agents who want to run a partial phase (for example, re-project skills after a source edit without regenerating the full index mesh) must invoke `tools/project_skills.py`, `tools/generate_pack_manifests.py`, `tools/generate_repo_index.py`, etc. directly. This is error-prone and leaks the internal script names.

In addition, `tools/validate_marketplace.py` is a single monolithic validator. Rebuild phases generate output that `validate_marketplace.py` later re-validates, but there is no way to invoke only the validation relevant to a single phase. Each phase should end by validating the surface it just produced. `validate_marketplace.py` will be split into invocable phase-scoped functions and exposed through a `--phase` CLI so `rebuild_marketplace.py` can call it per phase.

## CLI contract

### Default behavior

```bash
py -3 tools/rebuild_marketplace.py
```

Runs the full marketplace rebuild and validation stack exactly as it does today.

### New flags

| Flag | Meaning |
|------|---------|
| `--check` | Non-mutating mode. Every script that supports `--check` receives it. Final gates ensure the working tree is clean and valid. |
| `--phase {inventory,heal,project,index,catalog,validate,all}` | Run only the named phase and its prerequisites. `all` is the default. |
| `--skip-install` | In `project` / `all`, skip `tools/install_agent_skills.py`. |
| `--skip-index` | In `index` / `all`, skip repo-index and index-mesh generation. |
| `--skip-validate` | In `validate` / `all`, skip the validator scripts. |
| `--skip-whitespace-check` | Skip `git diff --check` (whitespace-only lint of changed files). Does not skip `git diff --exit-code` in `--check` mode. |
| `--verbose` / `-v` | Print each sub-command before running it. |
| `--help` | Updated help describing phases and skip flags. |

Examples:

```bash
py -3 tools/rebuild_marketplace.py --check
py -3 tools/rebuild_marketplace.py --phase project
py -3 tools/rebuild_marketplace.py --phase validate --verbose
py -3 tools/rebuild_marketplace.py --phase project --skip-install
```

### Phase definitions

A phase is a logical unit that maps to one or more existing tools. In `--check` mode each writer tool gets its own `--check` flag where it supports one. At the end of each phase, the corresponding phase-scoped validation runs so a phase is self-checking.

1. **`inventory`**
   - `tools/generate_plugin_root_inventory.py`
   - In write mode only: `_prune_stale_projected_plugin_roots()`
   - Validate: `tools/validate_marketplace.py --phase inventory --skip-freshness-checks`

2. **`heal`**
   - `tools/heal_overlays.py`

3. **`project`**
   - `tools/update_skill_artifacts.py --all`
   - `tools/normalize_first_party_skill_sources.py --check`
   - `tools/install_agent_skills.py` (skipped if `--skip-install`)
   - Validate: `tools/validate_marketplace.py --phase project --skip-freshness-checks`

4. **`index`**
   - `tools/generate_repo_index.py`
   - `tools/generate_index_mesh.py` (write + `--check`) (skipped if `--skip-index`)
   - Validate: `tools/validate_marketplace.py --phase index --skip-freshness-checks`

5. **`catalog`**
   - `tools/generate_first_party_skill_catalog.py` (write + `--check`)

6. **`validate`** (final gate)
   - `tools/validate_authority_assets.py` (skipped if `--skip-validate`)
   - `git diff --check` on changed paths, excluding retained verbatim third-party paths (skipped if `--skip-whitespace-check`)
   - In `--check` mode: `git diff --exit-code` to enforce a clean working tree

7. **`all`** (default)
   - Run `inventory`, `heal`, `project`, `index`, `catalog`, `validate` in order.

### `check_marketplace.py` wrapper

`tools/check_marketplace.py` is reduced to:

```python
def main() -> int:
    return subprocess.run(
        [sys.executable, str(ROOT / "tools" / "rebuild_marketplace.py"), "--check"]
    ).returncode
```

It keeps its own `--help` and epilog explaining it is the canonical non-mutating CI gate.

### `validate_marketplace.py` phase API

`tools/validate_marketplace.py` is refactored into invocable functions and a minimal CLI:

```python
def validate_inventory(*, skip_freshness: bool = False) -> None: ...
def validate_project(*, skip_freshness: bool = False) -> None: ...
def validate_index(*, skip_freshness: bool = False) -> None: ...
def validate_all(*, skip_freshness: bool = False) -> None: ...
```

The CLI gains:

```bash
py -3 tools/validate_marketplace.py                 # default: --phase all
py -3 tools/validate_marketplace.py --phase project --skip-freshness-checks
```

- `--phase {inventory,project,index,all}` selects the function to run. Default is `all`.
- `--skip-freshness-checks` suppresses `generate_plugin_root_inventory.py --check`, `validate_projection_materializer()`, and `validate_pack_manifests()` so `rebuild_marketplace.py` can call validation at the end of a phase that already ran the writer/checker.
- `validate_all` runs the three phase validators in order.

### `validate_marketplace.py` phase-to-call mapping

`main` is split so each phase function is self-contained (it loads the JSON/text surfaces it needs). `validate_all` loads no shared state; it simply calls the phase functions in order.

**`validate_inventory(skip_freshness)`**
- If `not skip_freshness`: `generate_plugin_root_inventory.py --check`
- For each `spec` in `MARKETPLACE_PLUGIN_SPECS`:
  - `check_json(spec["manifest_path"])`
  - `validate_plugin_manifest(plugin_manifest, spec)`
- `validate_active_plugin_tree()`
- `check_json(PLUGIN_ROOT_INVENTORY_PATH)`

**`validate_project(skip_freshness)`**
- `intake = check_json(SOURCE_INTAKE_JSON_PATH)`
- For each `spec` in `MARKETPLACE_PLUGIN_SPECS`:
  - `check_json(spec["manifest_path"])`
  - `validate_plugin_manifest(plugin_manifest, spec)`
- `registry = check_json(MARKETPLACE_PATH)`
- `bundle_manifest = check_json(BUNDLE_MANIFEST_PATH)`
- `validate_marketplace_registry(registry, plugin_manifests)`
- If `not skip_freshness`:
  - `validate_projection_materializer()`
  - `validate_pack_manifests()`
- `codex_manifest = check_json(CODEX_MARKETPLACE_MANIFEST_PATH)`
- Assert `codex_manifest == registry`
- `validate_bundle_manifest(bundle_manifest, intake)`
- For each `spec` in `MARKETPLACE_PLUGIN_SPECS` (skipping `house-skills`):
  - Required file checks (`README.md`/`SOURCE.md`/`LICENSE`, `package.json` if present, `assets/icon.svg`, superpowers assets)
  - `check_json(plugin_root / "references/bundle-manifest.json")`
  - `validate_superpowers_bundle_manifest`, `validate_projection_pack_manifest`, or `validate_skill_bundle_manifest` as appropriate
- `source_map = check_text(SOURCE_MAP_PATH)`; `validate_source_map(source_map)`
- `check_text(ROOT / "codex-marketplace/README.md")`
- `check_text(ROOT / "codex-marketplace/plugins/README.md")`
- `check_text(PLUGIN_README_PATH)`
- `check_text(PLUGIN_SKILL_PATH)`
- `check_text(PLUGIN_BUNDLE_AGENTS_PATH)`
- `check_text(PROVENANCE_PATH)`
- `check_text(ROOT / "provenance/MARK-99-unslop.md")`
- `validate_no_legacy_manifest_shapes()`
- `orphans = detect_first_party_orphans()`; fail if non-empty
- `validate_mega_pack_inclusion()`
- `validate_skill_zip_assertions()`

**`validate_index(skip_freshness)`**
- `_bootstrap_marketplace_dependencies()` (so `validate_repo_index` is importable)
- `check_text(REPO_INDEX_README_PATH)`
- `check_json(REPO_INDEX_PATH)`
- `validate_repo_index()`

**`validate_all(skip_freshness)`**
- `validate_inventory(skip_freshness)`
- `validate_project(skip_freshness)`
- `validate_index(skip_freshness)`

## Design decisions

- **Flag-based, not subcommand-based.** The existing `rebuild_marketplace.py` is a single command with no subcommands; adding `--phase` keeps the learning curve low and avoids breaking existing muscle memory.
- **Phases are coarse-grained.** Each phase matches a step in the current full-rebuild sequence. Finer granularity (per-script) would leak the same internal names the CLI is trying to hide.
- **Each phase validates its own output.** `rebuild_marketplace.py` calls `validate_marketplace.py --phase <phase>` at the end of `inventory`, `project`, and `index`. This makes partial runs self-checking.
- **Skip flags only affect the relevant phase.** `--skip-install` only applies to the `project` phase, so `--phase index --skip-install` is a no-op rather than an error.
- **`--check` is the global mode switch.** Individual scripts already support `--check`; `rebuild_marketplace.py` forwards it consistently. This makes `check_marketplace.py` a true wrapper.
- **Final `git diff --exit-code` is only in `--check` mode.** A full write run is expected to produce changes, so exit-code enforcement would be wrong there.

## Validation

- `py -3 tools/rebuild_marketplace.py` still passes (full rebuild, no diff errors).
- `py -3 tools/rebuild_marketplace.py --check` passes on a clean tree.
- `py -3 tools/check_marketplace.py` still passes (wrapper over `--check`).
- `py -3 tools/rebuild_marketplace.py --phase <each-phase>` runs the expected writer + validator subset and exits 0.
- `py -3 tools/validate_marketplace.py --phase <inventory|project|index>` runs only that validator subset and exits 0.
- `py -3 -m pytest tests` still passes after changes.

## Files touched

- `tools/rebuild_marketplace.py` — add argument parser, phase dispatch, `--check` plumbing, skip flags, verbose output.
- `tools/validate_marketplace.py` — split `main` into `validate_inventory`, `validate_project`, `validate_index`, `validate_all`; add `--phase` and `--skip-freshness-checks` CLI.
- `tools/check_marketplace.py` — rewrite as a thin wrapper.
- `tools/AGENTS.md` — update documented commands if the description of `rebuild_marketplace.py`, `check_marketplace.py`, or `validate_marketplace.py` needs alignment.

## Out of scope

- `--plugin` / `--skill` targeted projection. Adding it requires extending `update_skill_artifacts.py` and `project_skills.py` wiring; a separate spec should handle that once this CLI refactor lands.
- Changing the sequence or responsibility of the underlying generator/validator scripts.

## Handoff confidence

9/10. The CLI contract, phase dispatch, skip-flag semantics, and the exact partition of `validate_marketplace.py` `main` into phase functions are specified. The remaining implementation work is mechanical transcription of existing calls into the new structure.
