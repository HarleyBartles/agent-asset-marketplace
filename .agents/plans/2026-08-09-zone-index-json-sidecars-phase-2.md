# Zone-level INDEX.json sidecars — Phase 2 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use /subagent-driven-development (recommended) or /executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Convert the remaining directory zones from inline root `INDEX.json` entries to per-zone `INDEX.json` sidecars, so the root becomes a pure registry.

**Architecture:** Extend `tools/generate_repo_index.py` with sidecar defaults for every remaining directory zone and refactor `build_zone_indexes()` to produce all sidecars. `tools/validate_marketplace.py` checks every `index_json` referenced in the root. `tools/validate_repo_index.py` `merged_repo_index()` must rebuild the `zones` list from the loaded sidecars and expand the per-key skip set to avoid collision with the root registry's local fields (e.g. `purpose`, `surface_kind`, `nearest_scoped_agents_md`, `key_validation_scripts`).

**Tech Stack:** Python 3, `pathlib`, `json`, existing `tools/run.py` targets.

## Global Constraints

- Keep `INDEX.md` mesh untouched.
- `INDEX.json` sidecars are generated, read-only, and live at zone root directories.
- Schema version remains `2`.
- `py -3 tools/run.py ci --check` must pass before claiming any task is complete.
- No new metadata fields beyond what the spec requires.
- If a sidecar would duplicate only what `INDEX.md` already covers, that zone does not get a sidecar.
- All commits must go through the local pre-commit hook (`git commit`, not `--no-verify`).

---

### Task 1: Refactor `tools/generate_repo_index.py` for all directory zones

**Files:**
- Modify: `tools/generate_repo_index.py`
- Test: `py -3 tools/generate_repo_index.py --apply`

**Interfaces:**
- Consumes: existing `build_root_index()`, `DEFAULT_CODEX_MARKETPLACE_INDEX`, `zone_index_path`.
- Produces: `DEFAULT_ZONE_INDEXES` list, an updated `DEFAULT_ROOT_INDEX` with only registry entries, and a `build_zone_indexes()` that returns sidecars for all directory zones.

- [x] **Step 1: Replace `DEFAULT_ROOT_INDEX` zones with registry-only entries**

All zones that get a sidecar must only have `name`, `path`, and `index_json` in the root. Single-file surfaces (`marketplace-root-inventory`, `docs-unslop-profile`) stay inline because they are not directories and their metadata belongs to their parent.

```python
    "zones": [
        {
            "name": "runtime-registry",
            "path": ".agents/plugins",
            "index_json": ".agents/plugins/INDEX.json",
        },
        {
            "name": "codex-marketplace-root",
            "path": "codex-marketplace",
            "index_json": "codex-marketplace/INDEX.json",
        },
        {
            "name": "marketplace-root-inventory",
            "path": "codex-marketplace/plugin-roots.json",
            "purpose": "Editable active marketplace plugin root inventory for manifest and validator generation.",
            "surface_kind": "hand-authored",
            "nearest_scoped_agents_md": None,
            "key_validation_scripts": [
                "tools/validate_marketplace.py",
                "tools/validate_repo_index.py",
            ],
        },
        {
            "name": "codex-marketplace-plugins",
            "path": "codex-marketplace/plugins",
            "index_json": "codex-marketplace/plugins/INDEX.json",
        },
        {
            "name": "docs-unslop-profile",
            "path": ".agents/docs/unslop/profile.md",
            "purpose": "Canonical repo unslop profile for anti-slop custody and discovery.",
            "surface_kind": "hand-authored",
            "nearest_scoped_agents_md": ".devin/rules/docs.md",
            "key_validation_scripts": [
                "tools/validate_repo_index.py",
            ],
        },
        {
            "name": "superpowers-plans",
            "path": ".agents/plans",
            "index_json": ".agents/plans/INDEX.json",
        },
        {
            "name": "superpowers-specs",
            "path": ".agents/specs",
            "index_json": ".agents/specs/INDEX.json",
        },
        {
            "name": "tools",
            "path": "tools",
            "index_json": "tools/INDEX.json",
        },
    ],
```

- [x] **Step 2: Add `DEFAULT_ZONE_INDEXES` for the new sidecars**

Insert the sidecar data structure after `DEFAULT_CODEX_MARKETPLACE_INDEX`:

```python
DEFAULT_ZONE_INDEXES: list[dict[str, Any]] = [
    {
        "schema_version": 2,
        "name": "runtime-registry",
        "path": ".agents/plugins",
        "purpose": "Runtime-facing plugin registry consumed by Codex tooling.",
        "surface_kind": "runtime-facing",
        "nearest_scoped_agents_md": None,
        "key_validation_scripts": [
            "tools/validate_marketplace.py",
            "tools/validate_repo_index.py",
        ],
    },
    {
        "schema_version": 2,
        "name": "codex-marketplace-plugins",
        "path": "codex-marketplace/plugins",
        "purpose": "Protected active Codex marketplace plugin pack roots and their packaging metadata.",
        "surface_kind": "runtime-facing",
        "nearest_scoped_agents_md": ".devin/rules/codex-plugins.md",
        "key_validation_scripts": [
            "tools/validate_marketplace.py",
            "tools/validate_repo_index.py",
        ],
    },
    {
        "schema_version": 2,
        "name": "superpowers-plans",
        "path": ".agents/plans",
        "purpose": "Superpowers plan drafts and execution plans.",
        "surface_kind": "hand-authored",
        "nearest_scoped_agents_md": ".devin/rules/plans.md",
        "key_validation_scripts": [
            "tools/validate_repo_index.py",
        ],
    },
    {
        "schema_version": 2,
        "name": "superpowers-specs",
        "path": ".agents/specs",
        "purpose": "Superpowers design specs. Specs are repo-resident, tracked, and indexed alongside plans.",
        "surface_kind": "hand-authored",
        "nearest_scoped_agents_md": ".agents/runbooks/design.md",
        "key_validation_scripts": [
            "tools/validate_repo_index.py",
        ],
    },
    {
        "schema_version": 2,
        "name": "tools",
        "path": "tools",
        "purpose": "Repository validation and generation scripts.",
        "surface_kind": "hand-authored",
        "nearest_scoped_agents_md": ".devin/rules/tools.md",
        "key_validation_scripts": [
            "tools/validate_marketplace.py",
            "tools/validate_repo_index.py",
        ],
    },
]
```

- [x] **Step 3: Rewrite `build_zone_indexes()` to generate all sidecars**

```python
def build_zone_indexes() -> list[tuple[Path, dict[str, Any]]]:
    sidecars: list[tuple[Path, dict[str, Any]]] = []

    codex = dict(DEFAULT_CODEX_MARKETPLACE_INDEX)
    codex["marketplace_plugins"] = [_plugin_entry(spec) for spec in MARKETPLACE_PLUGIN_SPECS]
    sidecars.append((zone_index_path("codex-marketplace"), codex))

    for zone in DEFAULT_ZONE_INDEXES:
        data = dict(zone)
        sidecars.append((zone_index_path(data["path"]), data))

    return sidecars
```

- [x] **Step 4: Run the generator**

```bash
py -3 tools/generate_repo_index.py --apply
```

Expected:

```
Wrote INDEX.json
Wrote codex-marketplace\INDEX.json
Wrote .agents\plugins\INDEX.json
Wrote codex-marketplace\plugins\INDEX.json
Wrote .agents\plans\INDEX.json
Wrote .agents\specs\INDEX.json
Wrote tools\INDEX.json
OK repo index: generated
```

- [x] **Step 5: Verify the generator check**

```bash
py -3 tools/generate_repo_index.py --check
```

Expected: `OK repo index: current`.

- [x] **Step 6: Commit**

```bash
git add tools\generate_repo_index.py INDEX.json codex-marketplace\INDEX.json codex-marketplace\plugins\INDEX.json .agents\plugins\INDEX.json .agents\plans\INDEX.json .agents\specs\INDEX.json tools\INDEX.json
git commit -m "feat: generate INDEX.json sidecars for all directory zones"
```

> **Note:** `tools/validate_repo_index.py` `merged_repo_index()` was also updated to rebuild the `zones` list from the sidecars and expand the key skip set so that per-zone fields (`purpose`, `surface_kind`, `nearest_scoped_agents_md`, `key_validation_scripts`) do not collide with the merged aggregate.

---

### Task 2: Update `tools/validate_marketplace.py` to validate all sidecars

**Files:**
- Modify: `tools/validate_marketplace.py`
- Test: `py -3 tools/validate_marketplace.py`

**Interfaces:**
- Consumes: root `INDEX.json`.
- Produces: `validate_index()` iterates `zones` and calls `check_json` on each `index_json`.

- [x] **Step 1: Replace `validate_index()`**

```python
def validate_index(*, skip_freshness: bool = False) -> None:
    _ = skip_freshness
    check_text(REPO_INDEX_README_PATH)
    root = check_json(REPO_INDEX_PATH)
    for zone in root.get("zones", []):
        index_json = zone.get("index_json")
        if index_json:
            check_json(ROOT / index_json)
    validate_repo_index()
    print("OK validate_marketplace: index")
```

- [x] **Step 2: Run the marketplace validator**

```bash
py -3 tools/validate_marketplace.py
```

Expected: `OK validate_marketplace: index` at the end.

- [x] **Step 3: Commit**

```bash
git add tools\validate_marketplace.py
git commit -m "feat: validate all zone INDEX.json sidecars"
```

---

### Task 3: Regenerate surfaces and CI gate

**Files:**
- All generated surfaces may be touched by `tools/run.py`.

**Interfaces:**
- Consumes: changes from Tasks 1-2.
- Produces: a passing `ci --check` and a clean branch.

- [x] **Step 1: Regenerate all derived surfaces**

```bash
py -3 tools/run.py ci --apply
```

- [x] **Step 2: Verify with check**

```bash
py -3 tools/run.py ci --check
```

Expected: `[tools/run] all requested targets passed.`

- [x] **Step 3: Commit any generated changes**

```bash
git add -A
git commit -m "chore: regenerate derived surfaces after sidecar expansion"
```

- [x] **Step 4: Push**

```bash
git push
```

---

## Interim state notes

- Tasks 1 and 2 must be committed in order; `generate_repo_index.py` must be updated and applied before `validate_marketplace.py` can find the new sidecars.
- Do not run `ci --check` between Task 1 and Task 2 because the marketplace validator will expect the new sidecar files but `validate_marketplace.py` has not yet been told to look for them.

## Test summary

| Step | Command | Expected |
|------|---------|----------|
| Task 1 | `py -3 tools/generate_repo_index.py --apply` | writes all sidecar `INDEX.json` files |
| Task 1 | `py -3 tools/generate_repo_index.py --check` | `OK repo index: current` |
| Task 2 | `py -3 tools/validate_marketplace.py` | `OK validate_marketplace: index` |
| Task 3 | `py -3 tools/run.py ci --check` | all targets pass |

## Out of scope for this plan

- Converting single-file surface zones (`marketplace-root-inventory`, `docs-unslop-profile`) to sidecars.
- Retiring `repo-index/` and its `README.md` (Phase 3).
- Moving zone-specific `nearest_scoped_agents_md` into sidecars that already have it.
- Updating the design spec; it already covers this work.
