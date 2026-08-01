# Refreshing Installed Skills — Provenance Rewrite Design

> Spec for making `refresh_installed_skills.py` rewrite `.agents/skills/.provenance.json` when the plugin list or local skill inventory changes, and for recording repo-local skills in provenance.

## Problem

`refresh_installed_skills.py` currently writes `.agents/skills/.provenance.json` only when marketplace skill files are copied or removed (`changes_made`). It does not:

1. Record repo-local skills that match `marketplace.json` `local_skill_prefixes`.
2. Rewrite provenance when only the installed plugin list, manifest SHA, or local skill inventory changes but no marketplace skill files are touched.

This forces consumers (e.g. `rooms-mostly`) to hand-edit `.provenance.json` after plugin or local-skill changes.

## Goals

1. Add a `localSkills` array to `.provenance.json` listing sorted, valid repo-local skill directory names.
2. Detect provenance drift in the non-temporal fields:
   - `manifestSha`
   - `syncedPlugins` (order matters)
   - `syncedSkills` (marketplace skill count)
   - `localSkills`
   - `localPlugins`
3. Rewrite `.provenance.json` in `--apply` mode whenever any of those fields drift, even if no marketplace skill files were copied.
4. Make `--check` return `1` when provenance would be rewritten, and `0` when the entire state (skills + provenance) is current.
5. Preserve the existing "byte-identical refresh is a no-diff operation" guarantee: if the state has not changed, do not rewrite provenance just to bump `syncedAt`.

## Constraints

- Source of truth for the skill is `sources/first_party/skills/refreshing-installed-skills/scripts/refresh_installed_skills.py`.
- Projected copies under `codex-marketplace/plugins/*/skills/refreshing-installed-skills/` and `.agents/skills/refreshing-installed-skills/` are generated outputs.
- `tools/run marketplace --apply` must regenerate all derived surfaces.
- `tools/run ci --check` must pass before the PR is called green.
- Tests live in `tests/test_refresh_installed_skills.py`.
- LF line endings; `newline="\n"` on writes.
- No third-party dependencies.

## Proposed Approaches

### Option A: Compare a rendered provenance snapshot

- Build the complete new provenance dict (including `syncedAt`) and compare it to the existing file content.
- Problem: `syncedAt` changes every run, so this would always rewrite provenance and churn generated files. Rejected.

### Option B: Compare only the fields that affect provenance meaning

- Compute a `provenance_state` dict of non-temporal fields (`manifestSha`, `syncedPlugins`, `syncedSkills`, `localSkills`, `localPlugins`).
- Compare it to the same fields in the existing provenance.
- If they differ, write a fresh provenance with a new `syncedAt`.
- This keeps the no-diff guarantee while catching plugin-list-only and local-skill-only changes.

### Option C: Separate provenance change from skill-file change

- Track `changes_made` for skill files as today.
- Add a separate `provenance_needs_update` flag.
- Rewrite provenance when either is true.
- This is the implementation shape of Option B; it preserves the existing `changes_made` semantics and adds the drift check.

**Recommendation:** Option C (Option B's logic, Option C's implementation structure). It is the smallest change that preserves existing behavior and adds the missing drift detection.

## Design Details

### New helper: `_discover_local_skills(prefixes: list[str]) -> list[str]`

- Iterate `AGENTS_SKILLS_PATH`.
- Include directory names that:
  - are directories,
  - match a local skill prefix,
  - have a `SKILL.md` whose frontmatter `name` matches the directory name.
- Return a sorted list of strings.
- Do not emit errors; validation is already handled by `_validate_local_skill_dirs`.
- If `AGENTS_SKILLS_PATH` does not exist, return `[]`.

### New helper: `_provenance_state(...)`

Inputs:
- `manifest_sha: str`
- `installed_plugins: list[dict]`
- `synced_skill_count: int` (marketplace skill count)
- `local_skills: list[str]`

Outputs a dict with the durable fields used by `_write_provenance`.

### New helper: `_provenance_needs_update(existing, new_state) -> bool`

- Return `True` if `existing` is missing any durable key or any value differs from `new_state`.
- Compare lists and dicts with normal equality.
- Ignore `syncedAt`.

### Updated `_write_provenance(...)`

- Accept `local_skills: list[str]`.
- Write `localSkills` to the provenance file.
- Keep all existing fields (`manifestSha`, `syncedAt`, `syncedPlugins`, `syncedSkills`, `marketplace`, `localPlugins`, `marketplaceFile`).

### Updated `main()`

1. Load config and validate local skills as today.
2. Compute:
   - `installed_plugins`
   - `manifest_sha`
   - `local_skills`
   - `synced_skill_count = len(_expected_marketplace_skill_inventory(installed_plugins, prefixes))`
   - `provenance_needs_update = _provenance_needs_update(existing, new_state)`
3. Early exit (no force, existing provenance, not needs update, marketplace inventory current) -> print current state and return `0`.
4. Continue with install/clean.
5. In `--check` mode, return `1` if `changes_made` or `provenance_needs_update`.
6. In `--apply` mode, write provenance if `changes_made` or `provenance_needs_update`.

### Test changes

- Update `test_force_refresh_with_no_skill_changes_is_a_no_diff_operation` to use the same `manifestSha`, same `syncedPlugins`, and same `syncedSkills` so the test actually tests a no-diff scenario.
- Add `test_provenance_rewritten_on_plugin_list_only_change`.
- Add `test_provenance_records_local_skills`.
- Add `test_check_fails_when_provenance_plugin_list_stale`.
- Add `test_provenance_rewritten_when_local_skill_added`.

## Files to Touch

- `sources/first_party/skills/refreshing-installed-skills/scripts/refresh_installed_skills.py`
- `sources/first_party/skills/refreshing-installed-skills/SKILL.md` (update Provenance section)
- `tests/test_refresh_installed_skills.py`
- Generated surfaces via `tools/run marketplace --apply`

## Verification

- `py -3 -m pytest tests/test_refresh_installed_skills.py -v`
- `tools/run ci --check`
- `tools/run marketplace --apply`
