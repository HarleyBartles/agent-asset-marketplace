# Flat skill zip projection design

## Goal

Replace the current per-pack, GPT-overlay zip pipeline with a single shared projection stage that emits one flat `generated/skill-zips/<skill>.zip` per unique vendored skill, using the same source + codex-adapter projection that populates `codex-marketplace/plugins/`.

## Scope

- Create `tools/project_skills.py` as the single generator/validator for plugin tree and skill zip outputs.
- `project_skills.py` discovers the 22 active plugin roots from `codex-marketplace/plugin-roots.json`, loads each `references/bundle-manifest.json`, collects entries by `canonical_name`, validates cross-pack conflicts, stages each unique skill once, then:
  - copies the staged tree to every plugin pack destination `codex-marketplace/plugins/<pack>/skills/<skill>`;
  - writes `generated/skill-zips/<skill>.zip` with one top-level `<skill>/` folder and deterministic 1980-01-01 timestamps / 0644 permissions.
- Remove the GPT export lane entirely by deleting the `adapters/gpt/` tree (`manifest.json`, `AGENTS.md`, `README.md`, `INDEX.md`, and `superpowers-plus/` overlays).
- Drop `generated/skill-zips/registry.json` and the old per-pack zip layout `generated/skill-zips/<pack>/<skill>/skill.zip` (174 per-pack artifact records -> 99 unique skill zips).
- Remove obsolete tooling:
  - `tools/skill_gpt_exports.py`
  - `tools/export_skill_zips.py`
  - `tools/validate_export_skill_zips.py`
  - `tools/validate_generated_drift.py`
  - `tools/package_skill_zips.py`
  - `tools/materialize_projection.py`
  - `tools/skill_zip_artifacts.py` after moving `validate_skill_markdown_frontmatter`
- Refactor `tools/update_skill_artifacts.py` to orchestrate `generate_mega_packs`, `generate_pack_manifests`, `project_skills`, and `generate_first_party_skill_catalog`.
- Update `tools/rebuild_marketplace.py`, `tools/check_marketplace.py`, and `tools/validate_marketplace.py` to call `project_skills.py` instead of the old projection/zip stack.
- Update `tools/generate_pack_manifests.py` generated `SOURCE.md` install-units block to point to `generated/skill-zips/<skill>.zip`.
- Update `tools/generate_repo_index.py` validation metadata and the `superpowers-plus-marketplace` key validation scripts list.
- Move `validate_skill_markdown_frontmatter` from `tools/skill_zip_artifacts.py` to a new `tools/skill_validation.py` and update imports in `tools/validate_marketplace.py` and `tools/install_agent_skills.py`.
- Update AGENTS.md and docs surfaces:
  - `AGENTS.md`
  - `tools/AGENTS.md`
  - `codex-marketplace/AGENTS.md`
  - `codex-marketplace/plugins/AGENTS.md`
  - `docs/custody-and-projection-doctrine.md`
  - `docs/overlay-adapter-policy.md`
  - `codex-marketplace/README.md`
  - `README.md`
  - `tools/README.md`
- Update tests to match the new pipeline:
  - `tests/test_generator_check_modes.py`
  - `tests/test_validate_marketplace.py`
  - `tests/test_skill_overlay_materializer.py`

## Non-goals

- No per-pack zip output; a skill that appears in multiple packs must have identical `canonical_source_path` and `adaptation_overlay_path` or the build fails.
- No GPT-safe adaptation layer; zips are exact copies of the Codex projection.
- No registry of per-zip hashes; validation checks existence and archive shape/inventory only.
- No new first-party skills or marketplace packs.
- No changes to third-party source custody under `sources/third_party/`.

## Contract

### Shared projection stage

- `project_skills.py` loads `codex-marketplace/plugin-roots.json` and, for each enabled root, loads `codex-marketplace/plugins/<pack>/references/bundle-manifest.json`.
- It collects all `entries` whose `import_status` is not `skipped` or `blocked` and groups them by `canonical_name`.
- If any group contains entries with different `canonical_source_path` or `adaptation_overlay_path` values, the tool fails with a message listing the conflicting packs and the diverging paths.
- For each unique `canonical_name`, it materializes the skill once with `skill_overlay_materializer.stage_overlay_tree(canonical_source_path, codex_overlay_root)` into a temporary directory.

### Plugin tree output

- In the second pass, the staged tree is copied to `codex-marketplace/plugins/<pack>/skills/<skill>` for every manifest entry, after removing any existing destination directory.
- After all copies, any plugin `skills/<skill>` directory not in the expected set is deleted.

### Zip output

- For each unique `canonical_name`, write `generated/skill-zips/<skill>.zip` with a single top-level `<skill>/` folder.
- File timestamps, permissions, and compression follow the same deterministic rules currently used by `tools/skill_zip_artifacts.py` (1980-01-01 00:00:00, 0644, `ZIP_DEFLATED`).
- After all zips are written, any file in `generated/skill-zips/` that is not an expected `<skill>.zip` is deleted and empty parent directories are removed.

### Validation

- `project_skills.py --check` re-stages every unique skill and:
  - compares each plugin tree to the staged tree using `tree_canonicalization.compare_trees_canonicalized`;
  - verifies every expected zip exists, has exactly one top-level folder named `<skill>`, contains `<skill>/SKILL.md`, and its namelist matches the staged file list.
- It does **not** re-create and byte-compare zips.

### Orchestrator

- `tools/update_skill_artifacts.py` keeps its existing CLI surface as an alias for the full canonical pipeline:
  - `generate_mega_packs()`
  - `generate_pack_manifests()`
  - `project_skills()`
  - `generate_first_party_skill_catalog()`
- `--check` runs the same stages in check mode.

## Validation

- `py -3 tools/project_skills.py --check` passes with no plugin tree drift and all expected zips present with correct shape.
- `py -3 tools/rebuild_marketplace.py` passes after a full regeneration.
- `py -3 tools/check_marketplace.py` passes.
- `git diff --check` passes.
- After regeneration, `generated/skill-zips/` contains only `<skill>.zip` files (99 expected) and no `registry.json` or per-pack subdirectories.
- `adapters/gpt/` is removed and no active AGENTS.md or docs surface references it.

## Tradeoffs / risks

- `--check` only compares zip file inventories, not file contents. Content-only source changes that do not add or remove files will not fail `--check` if the zip is stale; the safeguard is running `py -3 tools/rebuild_marketplace.py` and committing regenerated zips.
- Removing `tools/materialize_projection.py` and `tools/skill_zip_artifacts.py` changes the tool surface. This repo's own `validate_marketplace.py` and tests are updated in scope; no external consumers are expected.
- The first regeneration collapses 174 per-pack zip records into 99 unique zips. The diff will be large but is purely derived output.

## Handoff confidence

9/10. The file targets, counts, and contract rules have been verified against the live repo. The planner will need to derive exact function signatures and cleanup helpers for `project_skills.py` from the existing `materialize_projection.py` and `skill_zip_artifacts.py` implementations, which are concrete and in place.
