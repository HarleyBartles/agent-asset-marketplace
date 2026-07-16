# MARK-285: Normalize marketplace projection custody and drift tooling

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fully normalize all 20 marketplace plugin manifests to directory-level `entries[]` projection-lane shape, add mega-pack auto-inclusion from custody roots, add first-party orphan and drift detection, generate proof surfaces from manifests, and eliminate the house-skills self-hosted exception — so any worker can add/remove/reshape/replace/merge/override/hybridize assets deterministically without inventing mechanisms or exceptions.

**Architecture:** A custody→mega-pack registry drives a generator that derives mega-pack manifests from the union of plugin entries by custody root. A shared canonicalization helper fixes the validator-disagreement bug. All 20 manifests migrate to directory-level `entries[]` with `canonical_name`/`source_category`/`content_mode`/`canonical_source_path`/`local_path`/`source_family`. First-party custody collapses to a single `sources/first_party/skills/` tree. Proof surfaces (provenance-map.json, source-map.md) are generated from manifests and validated-current.

**Tech Stack:** Python 3 (`py -3`), stdlib only (json, pathlib, argparse, shutil, tempfile, unittest). No external dependencies.

---

## Verified state before implementation

- **Worktree:** `C:/WORK/Devin/agent-asset-marketplace/.worktrees/mark-285-normalize-projection-custody`
- **Branch:** `harleydbartles/mark-285-normalize-marketplace-projection-custody-and-drift-tooling`
- **Base:** `0841fc82` (PR #147 landed)
- **Worktree clean:** yes, zero commits ahead of main

### Manifest shape classification (verified by direct inspection)

| Shape | Count | Plugins |
|---|---|---|
| projection-lane (dir-level entries[], no suffix on csp) | 2 | `superpowers-plus` (20 entries), `house-skills` (57 entries, nested manifest, self-hosted exception) |
| components-legacy (components[] with file-level source_path) | 2 | `adventures-pack` (17 components), `everything-codex-code` (14 components) |
| hybrid-filelevel (entries[] with new-schema fields but file-level csp) | 1 | `wild-bunch-project-pack` (11 entries) |
| entries-legacy (snapshot_path/local_path file-level, no canonical_name) | 14 | `api-contracts-pack` (5), `architecture-pack` (30), `codex-cortex` (98), `data-platform-pack` (11), `dotnet-kit` (6), `frontend-pack` (16), `game-studio` (9), `language-patterns-pack` (63), `media-content-pack` (10), `ops-connectors-pack` (9), `planning-pack` (31), `security-pack` (56), `superpowers-ecc` (14), `unslop-plus` (19) |
| skills-legacy (skills[] array) | 1 | `repo-worker-base` (47 skills) |

### First-party custody (verified)

- `sources/first_party/skills/`: 56 dirs, 52 with SKILL.md, 4 without (governance: codex-cortex, dotnet-kit, frontend-pack, house-skills)
- `sources/first_party/core/`: 9 dirs, all with SKILL.md
- **Total real first-party skills: 61** (52 + 9)

### Custody→mega-pack mapping (locked in)

| Custody root | source_family | Mega-pack | Current state |
|---|---|---|---|
| `sources/first_party/skills` | `first_party` | `house-skills` | projection-lane (57 entries), self-hosted exception |
| `sources/third_party/claude-cortex/upstream` | `claude-cortex` | `codex-cortex` | legacy (98 entries), missing cross-plugin projections |
| `sources/third_party/ecc/upstream` | `ecc` | `everything-codex-code` | components-legacy (14), missing cross-plugin projections |
| `sources/third_party/superpowers/obra-superpowers/v5.1.0` | `superpowers` | `superpowers-plus` | projection-lane (20 entries), working |
| `sources/third_party/game-studio/upstream` | `game-studio` | `game-studio` | legacy (9 entries) |
| `sources/third_party/dotnet-claude-kit/upstream` | `dotnet-claude-kit` | `dotnet-kit` | legacy (6 entries) |
| `sources/third_party/unslop/upstream` | `unslop` | `unslop-plus` | legacy (19 entries) |

### Validator-disagreement bug (confirmed)

`materialize_projection.py --check` fails on `brainstorming` (raw-byte comparison) while `validate_marketplace.py` passes (CRLF-canonicalized). Fix: shared canonicalization helper.

### Key file locations

- Canonicalization helper: `tools/validate_marketplace.py:90` (`_canonicalize_tree_bytes`)
- Tree mirror validator: `tools/validate_marketplace.py:115` (`validate_tree_mirror`)
- Materializer: `tools/materialize_projection.py` (raw bytes at line 122)
- Plugin root inventory: `codex-marketplace/plugin-roots.json`
- House-skills manifest (nested): `codex-marketplace/plugins/house-skills/skills/house-skills/references/bundle-manifest.json`
- Superpowers provenance map: `codex-marketplace/plugins/superpowers-plus/references/provenance-map.json`
- Tests: `tests/test_validate_marketplace.py`, `tests/test_skill_overlay_materializer.py`
- Doctrine: `docs/custody-and-projection-doctrine.md`

---

## Normalized entry schema (target for all 20 manifests)

Every entry in every `entries[]` array must have:

```json
{
  "canonical_name": "skill-name",
  "source_category": "first_party|third_party",
  "content_mode": "verbatim|normalised|adapted|blocked|skipped",
  "source_family": "first_party|claude-cortex|ecc|superpowers|game-studio|dotnet-claude-kit|unslop",
  "canonical_source_path": "sources/first_party/skills/skill-name",
  "local_path": "skills/skill-name",
  "provenance_note": "..."
}
```

Rules:
- `canonical_source_path` must be a **directory** (no file suffix). Active `verbatim`/`normalised`/`adapted` entries point at directory-level source custody.
- `local_path` is a directory within the plugin root (e.g. `skills/skill-name`).
- `blocked`/`skipped` entries may have non-materialized paths but must be explicit.
- `source_family` drives mega-pack auto-inclusion.
- Third-party `normalised`/`adapted` entries must also have `adaptation_overlay_path`.
- Optional fields: `adaptation_overlay_path`, `source_path`, `source_author`, `source_license`, `source_repo`, `adaptation_note`, `adapted_author`, `copy_expectation`, `lane`.

### Manifest top-level schema (target)

```json
{
  "bundle_name": "plugin-name",
  "bundle_version": "1.0.0",
  "bundle_type": "projection-lane",
  "plugin_root": "codex-marketplace/plugins/plugin-name",
  "is_mega_pack": false,
  "mega_pack_for": null,
  "source_families": ["family-name"],
  "entries": [...],
  "notes": ["..."],
  "plugin_author": "Harley Bartles",
  "plugin_license": "MIT"
}
```

Mega-pack manifests set `"is_mega_pack": true` and `"mega_pack_for": "family-name"`. Mega-pack manifests are **generated**, not hand-edited.

---

## Phase 1: Foundation — shared canonicalization and custody cleanup

### Task 1: Fix the validator-disagreement bug with shared canonicalization

**Files:**
- Create: `tools/tree_canonicalization.py`
- Modify: `tools/validate_marketplace.py` (replace `_canonicalize_tree_bytes` with import)
- Modify: `tools/materialize_projection.py` (use shared canonicalization in check mode)
- Test: `tests/test_tree_canonicalization.py`

- [ ] **Step 1: Write the failing test**

Create `tests/test_tree_canonicalization.py`:

```python
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from tree_canonicalization import canonicalize_tree_bytes, canonicalize_tree  # noqa: E402


class TreeCanonicalizationTests(unittest.TestCase):
    def test_canonicalizes_crlf_to_lf_for_text_files(self) -> None:
        result = canonicalize_tree_bytes(Path("SKILL.md"), b"line1\r\nline2\r\n")
        self.assertEqual(result, b"line1\nline2\n")

    def test_canonicalizes_cr_to_lf_for_text_files(self) -> None:
        result = canonicalize_tree_bytes(Path("SKILL.md"), b"line1\rline2\r")
        self.assertEqual(result, b"line1\nline2\n")

    def test_preserves_binary_files(self) -> None:
        result = canonicalize_tree_bytes(Path("icon.png"), b"\x89PNG\r\n\x1a\n")
        self.assertEqual(result, b"\x89PNG\r\n\x1a\n")

    def test_canonicalizes_json(self) -> None:
        result = canonicalize_tree_bytes(Path("manifest.json"), b'{"a":1}\r\n')
        self.assertEqual(result, b'{"a":1}\n')

    def test_canonicalizes_yaml(self) -> None:
        result = canonicalize_tree_bytes(Path("openai.yaml"), b"name: test\r\n")
        self.assertEqual(result, b"name: test\n")


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `py -3 tests/test_tree_canonicalization.py`
Expected: FAIL with `ModuleNotFoundError: No module named 'tree_canonicalization'`

- [ ] **Step 3: Create the shared canonicalization module**

Create `tools/tree_canonicalization.py`:

```python
#!/usr/bin/env python3
"""Shared tree canonicalization helpers for projection and validation tools."""

from __future__ import annotations

from pathlib import Path

TEXT_FILENAMES = {"SKILL.md", "openai.yaml", "AGENTS.md", "README.md", "LICENSE", "SOURCE.md", "PROJECTION.md"}
TEXT_SUFFIXES = {".md", ".json", ".yaml", ".yml", ".txt", ".py", ".sh", ".toml", ".cfg", ".ini"}


def canonicalize_tree_bytes(path: Path, raw: bytes) -> bytes:
    """Normalize CRLF/CR to LF for text files. Binary files are returned as-is."""
    if path.name in TEXT_FILENAMES or path.suffix.lower() in TEXT_SUFFIXES:
        return raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return raw


def canonicalize_tree(root: Path) -> dict[str, bytes]:
    """Read all files under root and return a dict of rel-path -> canonicalized bytes."""
    result: dict[str, bytes] = {}
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(root).as_posix()
        result[rel] = canonicalize_tree_bytes(path, path.read_bytes())
    return result


def compare_trees_canonicalized(expected_root: Path, actual_root: Path) -> None:
    """Compare two directory trees after canonicalization. Raises ValueError on mismatch."""
    expected = canonicalize_tree(expected_root)
    actual = canonicalize_tree(actual_root)
    if set(expected.keys()) != set(actual.keys()):
        missing = set(expected.keys()) - set(actual.keys())
        extra = set(actual.keys()) - set(expected.keys())
        parts = []
        if missing:
            parts.append(f"missing files: {sorted(missing)}")
        if extra:
            parts.append(f"extra files: {sorted(extra)}")
        raise ValueError(f"file inventory mismatch: {', '.join(parts)}")
    for rel in sorted(expected.keys()):
        if expected[rel] != actual[rel]:
            raise ValueError(f"content differs at {rel}")
```

- [ ] **Step 4: Run test to verify it passes**

Run: `py -3 tests/test_tree_canonicalization.py`
Expected: PASS (all 5 tests)

- [ ] **Step 5: Update validate_marketplace.py to import from shared module**

In `tools/validate_marketplace.py`:
- Remove the `_canonicalize_tree_bytes` function (lines ~90-93) and the `TEXT_FILENAMES`/`TEXT_SUFFIXES` constants if they exist at module level.
- Add import at top: `from tree_canonicalization import canonicalize_tree_bytes as _canonicalize_tree_bytes, compare_trees_canonicalized`
- Update `validate_tree_mirror` to use `_canonicalize_tree_bytes` (now imported) — the call sites stay the same since the function signature is identical.
- Alternatively, replace `validate_tree_mirror` body with a call to `compare_trees_canonicalized`.

- [ ] **Step 6: Update materialize_projection.py to use shared canonicalization**

In `tools/materialize_projection.py`, in `_materialize_entry` (check mode, lines ~112-125):
- Replace the raw-byte comparison with canonicalized comparison.
- Add import: `from tree_canonicalization import compare_trees_canonicalized`
- Replace the check-mode block with:

```python
    # check mode: stage reconstruction and compare (canonicalized, not raw bytes)
    if not destination_root.exists():
        raise FileNotFoundError(f"projection missing for {entry['canonical_name']}: {destination_root}")
    expected_root, tempdir = stage_overlay_tree(source_root, overlay_root)
    try:
        compare_trees_canonicalized(expected_root, destination_root)
    finally:
        tempdir.cleanup()
```

- [ ] **Step 7: Verify the brainstorming drift is now fixed**

Run: `py -3 tools/materialize_projection.py --check`
Expected: `OK projection: all projection-lane plugins validated` (no more brainstorming failure)

- [ ] **Step 8: Run existing tests to verify no regression**

Run: `py -3 tests/test_validate_marketplace.py` and `py -3 tests/test_skill_overlay_materializer.py`
Expected: All tests pass.

- [ ] **Step 9: Commit**

```bash
git add tools/tree_canonicalization.py tools/validate_marketplace.py tools/materialize_projection.py tests/test_tree_canonicalization.py
git commit -m "fix: shared tree canonicalization fixes validator-disagreement drift bug

materialize_projection.py compared raw bytes while validate_marketplace.py
canonicalized CRLF->LF. This caused brainstorming to fail materialize_projection
--check while passing validate_marketplace. Extract canonicalization into a
shared module (tools/tree_canonicalization.py) and use it in both validators."
```

---

### Task 2: Move house-skills control-plane source to first-party custody

**Files:**
- Move: `codex-marketplace/plugins/house-skills/skills/house-skills/SKILL.md` → `sources/first_party/skills/house-skills/SKILL.md`
- Move: `codex-marketplace/plugins/house-skills/skills/house-skills/agents/` → `sources/first_party/skills/house-skills/agents/`
- Keep: `codex-marketplace/plugins/house-skills/skills/house-skills/references/` (projection-local references)
- Move: `codex-marketplace/plugins/house-skills/skills/house-skills/references/bundle-manifest.json` → `codex-marketplace/plugins/house-skills/references/bundle-manifest.json` (de-nest)
- Modify: `codex-marketplace/plugins/house-skills/references/bundle-manifest.json` (update house-skills entry canonical_source_path)
- Modify: `tools/materialize_projection.py` (remove self-hosted skip)
- Modify: `tools/marketplace_utils.py` (update BUNDLE_MANIFEST_PATH)
- Modify: `docs/custody-and-projection-doctrine.md` (remove self-hosted exception section)

- [ ] **Step 1: Move the control-plane skill source to first-party custody**

```bash
# Create the first-party source dir
mkdir -p sources/first_party/skills/house-skills
# Move SKILL.md and agents/
git mv codex-marketplace/plugins/house-skills/skills/house-skills/SKILL.md sources/first_party/skills/house-skills/SKILL.md
git mv codex-marketplace/plugins/house-skills/skills/house-skills/agents sources/first_party/skills/house-skills/agents
# Move governance metadata (decisions/intake) — these stay as governance, will be ejected in Task 3
# For now, move them alongside since house-skills governance IS the house-skills skill's governance
```

Note: The existing `sources/first_party/skills/house-skills/` dir already has `decisions.json`, `decisions.md`, `intake.json` (governance metadata). The SKILL.md and agents/ move in alongside them.

- [ ] **Step 2: De-nest the house-skills bundle manifest**

```bash
mkdir -p codex-marketplace/plugins/house-skills/references
git mv codex-marketplace/plugins/house-skills/skills/house-skills/references/bundle-manifest.json codex-marketplace/plugins/house-skills/references/bundle-manifest.json
git mv codex-marketplace/plugins/house-skills/skills/house-skills/references/source-map.md codex-marketplace/plugins/house-skills/references/source-map.md
```

- [ ] **Step 3: Update the house-skills entry in the bundle manifest**

In `codex-marketplace/plugins/house-skills/references/bundle-manifest.json`, find the entry with `"canonical_name": "house-skills"` and change:

```json
{
  "canonical_name": "house-skills",
  "source_category": "first_party",
  "content_mode": "verbatim",
  "canonical_source_path": "sources/first_party/skills/house-skills",
  "local_path": "skills/house-skills",
  ...
}
```

(Change `canonical_source_path` from `codex-marketplace/plugins/house-skills/skills/house-skills` to `sources/first_party/skills/house-skills`.)

- [ ] **Step 4: Remove the self-hosted skip from materialize_projection.py**

In `tools/materialize_projection.py`, remove the `source_root == destination_root` block (lines ~95-98) in `_materialize_entry`. The house-skills entry now has a real source custody path that differs from the projection path.

- [ ] **Step 5: Update marketplace_utils.py BUNDLE_MANIFEST_PATH**

In `tools/marketplace_utils.py`, change:
```python
BUNDLE_MANIFEST_PATH = ROOT / "codex-marketplace/plugins/house-skills/skills/house-skills/references/bundle-manifest.json"
```
to:
```python
BUNDLE_MANIFEST_PATH = ROOT / "codex-marketplace/plugins/house-skills/references/bundle-manifest.json"
```
Also update `SOURCE_MAP_PATH` similarly.

- [ ] **Step 6: Update doctrine — remove self-hosted exception**

In `docs/custody-and-projection-doctrine.md`, remove the entire "### Self-hosted control-plane exception" section (lines ~76-89). The exception no longer exists.

- [ ] **Step 7: Verify materializer now handles house-skills**

Run: `py -3 tools/materialize_projection.py --check`
Expected: `OK projection: all projection-lane plugins validated`

- [ ] **Step 8: Run full validation**

Run: `py -3 tools/validate_marketplace.py`
Expected: `Marketplace validation passed.`

- [ ] **Step 9: Commit**

```bash
git add -A
git commit -m "feat: move house-skills control-plane source to first-party custody

Eliminates the self-hosted control-plane exception. The house-skills
SKILL.md and agents/ now live under sources/first_party/skills/house-skills/
alongside their governance metadata. The bundle manifest is de-nested from
skills/house-skills/references/ to the standard references/ location. The
materializer's source_root == destination_root skip is removed."
```

---

### Task 3: Fold core/ into skills/ and eject governance dirs

**Files:**
- Move: `sources/first_party/core/*` → `sources/first_party/skills/` (9 dirs)
- Delete: `sources/first_party/core/` (after moving)
- Move: `sources/first_party/skills/{codex-cortex,dotnet-kit,frontend-pack}/` governance metadata → `provenance/{plugin}-governance/`
- Modify: `codex-marketplace/plugins/house-skills/references/bundle-manifest.json` (add 9 core skills as entries, update paths)
- Modify: `sources/first_party/README.md` (update to reflect single skills/ tree)
- Modify: `docs/custody-and-projection-doctrine.md` (update custody section if it references core/)

- [ ] **Step 1: Move core/ skills into skills/**

```bash
for skill in bootstrap-router boring-loop cleanup-custody connector-safety github-operations linear-superpowers skill-installer skill-packager skill-validator; do
  git mv sources/first_party/core/$skill sources/first_party/skills/$skill
done
rmdir sources/first_party/core
```

- [ ] **Step 2: Eject governance dirs to provenance/**

```bash
for plugin in codex-cortex dotnet-kit frontend-pack; do
  mkdir -p provenance/$plugin-governance
  git mv sources/first_party/skills/$plugin/decisions.json provenance/$plugin-governance/decisions.json
  git mv sources/first_party/skills/$plugin/decisions.md provenance/$plugin-governance/decisions.md
  git mv sources/first_party/skills/$plugin/intake.json provenance/$plugin-governance/intake.json
  rmdir sources/first_party/skills/$plugin
done
```

Note: `sources/first_party/skills/house-skills/` keeps its governance metadata because it IS a real skill now (SKILL.md moved there in Task 2).

- [ ] **Step 3: Add the 9 core skills to the house-skills bundle manifest**

In `codex-marketplace/plugins/house-skills/references/bundle-manifest.json`, add 9 new entries for the core skills. Each entry follows the same pattern as existing first-party entries:

```json
{
  "canonical_name": "bootstrap-router",
  "source_category": "first_party",
  "content_mode": "verbatim",
  "canonical_source_path": "sources/first_party/skills/bootstrap-router",
  "local_path": "skills/bootstrap-router",
  "lane": "Core worker machinery",
  "provenance_note": "First-party skill projected verbatim into the house-skills mega-pack.",
  "source_path": "sources/first_party/skills/bootstrap-router/SKILL.md",
  "source_author": "Harley Bartles",
  "source_license": "MIT"
}
```

Repeat for: boring-loop, cleanup-custody, connector-safety, github-operations, linear-superpowers, skill-installer, skill-packager, skill-validator.

Also update any existing entries that referenced `sources/first_party/core/` paths to use `sources/first_party/skills/` instead.

- [ ] **Step 4: Update sources/first_party/README.md**

Update the README to reflect the single `skills/` tree (no more `core/`).

- [ ] **Step 5: Verify first-party custody is clean**

Run: `py -3 -c "import pathlib; root = pathlib.Path('.'); skills = sorted(d.name for d in (root / 'sources/first_party/skills').iterdir() if d.is_dir()); without = [d for d in skills if not (root / 'sources/first_party/skills' / d / 'SKILL.md').exists()]; print(f'total: {len(skills)}, without SKILL.md: {without}')"`
Expected: `total: 61, without SKILL.md: []` (all 61 dirs have SKILL.md, zero governance-only dirs)

- [ ] **Step 6: Run validation**

Run: `py -3 tools/validate_marketplace.py` and `py -3 tools/materialize_projection.py --check`
Expected: Both pass.

- [ ] **Step 7: Commit**

```bash
git add -A
git commit -m "feat: fold core/ into skills/ and eject governance dirs to provenance/

First-party custody is now a single sources/first_party/skills/ tree with 61
real skills (52 existing + 9 from core/ + house-skills control-plane moved in).
Governance metadata for codex-cortex, dotnet-kit, frontend-pack moves to
provenance/<plugin>-governance/. Zero non-skill dirs remain under skills/."
```

---

## Phase 2: Custody→mega-pack registry and mega-pack tooling

### Task 4: Create the custody→mega-pack registry

**Files:**
- Create: `codex-marketplace/custody-mega-pack-registry.json`

- [ ] **Step 1: Create the registry**

Create `codex-marketplace/custody-mega-pack-registry.json`:

```json
{
  "schema_version": 1,
  "description": "Maps source custody roots to mega-pack plugins. Drives mega-pack manifest generation.",
  "mappings": [
    {
      "source_family": "first_party",
      "custody_root": "sources/first_party/skills",
      "mega_pack": "house-skills",
      "mega_pack_root": "codex-marketplace/plugins/house-skills"
    },
    {
      "source_family": "claude-cortex",
      "custody_root": "sources/third_party/claude-cortex/upstream",
      "mega_pack": "codex-cortex",
      "mega_pack_root": "codex-marketplace/plugins/codex-cortex"
    },
    {
      "source_family": "ecc",
      "custody_root": "sources/third_party/ecc/upstream",
      "mega_pack": "everything-codex-code",
      "mega_pack_root": "codex-marketplace/plugins/everything-codex-code"
    },
    {
      "source_family": "superpowers",
      "custody_root": "sources/third_party/superpowers/obra-superpowers/v5.1.0",
      "mega_pack": "superpowers-plus",
      "mega_pack_root": "codex-marketplace/plugins/superpowers-plus"
    },
    {
      "source_family": "game-studio",
      "custody_root": "sources/third_party/game-studio/upstream",
      "mega_pack": "game-studio",
      "mega_pack_root": "codex-marketplace/plugins/game-studio"
    },
    {
      "source_family": "dotnet-claude-kit",
      "custody_root": "sources/third_party/dotnet-claude-kit/upstream",
      "mega_pack": "dotnet-kit",
      "mega_pack_root": "codex-marketplace/plugins/dotnet-kit"
    },
    {
      "source_family": "unslop",
      "custody_root": "sources/third_party/unslop/upstream",
      "mega_pack": "unslop-plus",
      "mega_pack_root": "codex-marketplace/plugins/unslop-plus"
    }
  ]
}
```

- [ ] **Step 2: Commit**

```bash
git add codex-marketplace/custody-mega-pack-registry.json
git commit -m "feat: add custody-to-mega-pack registry

Declares the 7-row mapping from source custody roots to mega-pack plugins.
Drives mega-pack manifest generation and auto-inclusion validation."
```

---

### Task 5: Build the mega-pack manifest generator

**Files:**
- Create: `tools/generate_mega_packs.py`
- Test: `tests/test_generate_mega_packs.py`

- [ ] **Step 1: Write the failing test**

Create `tests/test_generate_mega_packs.py`:

```python
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from generate_mega_packs import collect_entries_by_family, generate_mega_pack_manifest  # noqa: E402


class GenerateMegaPacksTests(unittest.TestCase):
    def test_collect_entries_by_family_groups_by_source_family(self) -> None:
        plugin_manifests = [
            {
                "bundle_name": "security-pack",
                "entries": [
                    {"canonical_name": "owasp-top-10", "source_category": "third_party", "source_family": "claude-cortex", "content_mode": "normalised", "canonical_source_path": "sources/third_party/claude-cortex/upstream/skills/owasp-top-10", "local_path": "skills/owasp-top-10"},
                    {"canonical_name": "ecc-security", "source_category": "third_party", "source_family": "ecc", "content_mode": "normalised", "canonical_source_path": "sources/third_party/ecc/upstream/skills/ecc-security", "local_path": "skills/ecc-security"},
                ],
            },
            {
                "bundle_name": "architecture-pack",
                "entries": [
                    {"canonical_name": "cqrs", "source_category": "third_party", "source_family": "claude-cortex", "content_mode": "normalised", "canonical_source_path": "sources/third_party/claude-cortex/upstream/skills/cqrs", "local_path": "skills/cqrs"},
                ],
            },
        ]
        by_family = collect_entries_by_family(plugin_manifests)
        self.assertIn("claude-cortex", by_family)
        self.assertIn("ecc", by_family)
        self.assertEqual(len(by_family["claude-cortex"]), 2)
        self.assertEqual(len(by_family["ecc"]), 1)

    def test_generate_mega_pack_manifest_produces_correct_shape(self) -> None:
        entries = [
            {"canonical_name": "owasp-top-10", "source_category": "third_party", "source_family": "claude-cortex", "content_mode": "normalised", "canonical_source_path": "sources/third_party/claude-cortex/upstream/skills/owasp-top-10", "local_path": "skills/owasp-top-10"},
            {"canonical_name": "cqrs", "source_category": "third_party", "source_family": "claude-cortex", "content_mode": "normalised", "canonical_source_path": "sources/third_party/claude-cortex/upstream/skills/cqrs", "local_path": "skills/cqrs"},
        ]
        manifest = generate_mega_pack_manifest(
            mega_pack_name="codex-cortex",
            mega_pack_root="codex-marketplace/plugins/codex-cortex",
            source_family="claude-cortex",
            entries=entries,
        )
        self.assertEqual(manifest["bundle_name"], "codex-cortex")
        self.assertTrue(manifest["is_mega_pack"])
        self.assertEqual(manifest["mega_pack_for"], "claude-cortex")
        self.assertEqual(len(manifest["entries"]), 2)
        # Mega-pack local_path should be relative to the mega-pack root
        for entry in manifest["entries"]:
            self.assertTrue(entry["local_path"].startswith("skills/"))


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `py -3 tests/test_generate_mega_packs.py`
Expected: FAIL with `ModuleNotFoundError`

- [ ] **Step 3: Create the mega-pack generator**

Create `tools/generate_mega_packs.py`:

```python
#!/usr/bin/env python3
"""Generate mega-pack manifests from the union of plugin entries by custody root."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from marketplace_utils import ROOT, load_plugin_root_inventory, load_json

REGISTRY_PATH = ROOT / "codex-marketplace/custody-mega-pack-registry.json"
SKIP_CONTENT_MODES = {"blocked", "skipped"}


def load_mega_pack_registry() -> list[dict[str, Any]]:
    registry = load_json(REGISTRY_PATH)
    if registry.get("schema_version") != 1:
        raise ValueError(f"{REGISTRY_PATH}: schema_version must be 1")
    mappings = registry.get("mappings")
    if not isinstance(mappings, list) or not mappings:
        raise ValueError(f"{REGISTRY_PATH}: mappings must be a non-empty list")
    return mappings


def _load_plugin_manifest(plugin_root: Path) -> dict[str, Any] | None:
    manifest_path = plugin_root / "references" / "bundle-manifest.json"
    if not manifest_path.exists():
        return None
    manifest = load_json(manifest_path)
    if not isinstance(manifest, dict):
        return None
    if "entries" not in manifest:
        return None
    return manifest


def collect_entries_by_family(plugin_manifests: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    """Collect all active entries from all plugin manifests, grouped by source_family."""
    by_family: dict[str, list[dict[str, Any]]] = {}
    for manifest in plugin_manifests:
        entries = manifest.get("entries", [])
        if not isinstance(entries, list):
            continue
        for entry in entries:
            if not isinstance(entry, dict):
                continue
            if entry.get("content_mode") in SKIP_CONTENT_MODES:
                continue
            family = entry.get("source_family")
            if not family:
                continue
            by_family.setdefault(family, []).append(entry)
    return by_family


def generate_mega_pack_manifest(
    *, mega_pack_name: str, mega_pack_root: str, source_family: str, entries: list[dict[str, Any]]
) -> dict[str, Any]:
    """Generate a mega-pack manifest from collected entries."""
    # Deduplicate by canonical_name (an entry may appear in multiple plugins)
    seen: dict[str, dict[str, Any]] = {}
    for entry in entries:
        name = entry.get("canonical_name")
        if not name:
            continue
        if name not in seen:
            # Mega-pack local_path is relative to the mega-pack root
            mega_entry = dict(entry)
            mega_entry["local_path"] = f"skills/{name}"
            seen[name] = mega_entry
    return {
        "bundle_name": mega_pack_name,
        "bundle_version": "1.0.0",
        "bundle_type": "projection-lane",
        "plugin_root": mega_pack_root,
        "is_mega_pack": True,
        "mega_pack_for": source_family,
        "source_families": [source_family],
        "entries": sorted(seen.values(), key=lambda e: e["canonical_name"]),
        "notes": [
            f"Auto-generated mega-pack manifest for the {source_family} custody root.",
            "Do not hand-edit. Regenerate with: py -3 tools/generate_mega_packs.py",
        ],
        "plugin_author": "Harley Bartles",
        "plugin_license": "MIT",
    }


def generate_all_mega_packs(*, write: bool) -> None:
    registry = load_mega_pack_registry()
    inventory = load_plugin_root_inventory()

    # Load all non-mega-pack plugin manifests
    plugin_manifests: list[dict[str, Any]] = []
    mega_pack_names = {m["mega_pack"] for m in registry}
    for spec in inventory:
        plugin_root = ROOT / spec["plugin_root"]
        manifest = _load_plugin_manifest(plugin_root)
        if manifest is None:
            continue
        if spec["name"] in mega_pack_names:
            continue  # Skip mega-packs themselves
        plugin_manifests.append(manifest)

    by_family = collect_entries_by_family(plugin_manifests)

    for mapping in registry:
        family = mapping["source_family"]
        mega_name = mapping["mega_pack"]
        mega_root = mapping["mega_pack_root"]
        entries = by_family.get(family, [])
        manifest = generate_mega_pack_manifest(
            mega_pack_name=mega_name,
            mega_pack_root=mega_root,
            source_family=family,
            entries=entries,
        )
        manifest_path = ROOT / mega_root / "references" / "bundle-manifest.json"
        if write:
            manifest_path.parent.mkdir(parents=True, exist_ok=True)
            with manifest_path.open("w", encoding="utf-8", newline="\n") as f:
                json.dump(manifest, f, indent=2)
                f.write("\n")
            print(f"Wrote {manifest_path.relative_to(ROOT)}")
        else:
            if not manifest_path.exists():
                raise FileNotFoundError(f"mega-pack manifest missing: {manifest_path}")
            existing = load_json(manifest_path)
            if existing != manifest:
                raise ValueError(
                    f"mega-pack manifest stale: {manifest_path}\n"
                    f"Run: py -3 tools/generate_mega_packs.py"
                )
            print(f"OK mega-pack manifest current: {manifest_path.relative_to(ROOT)}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate or validate mega-pack manifests")
    parser.add_argument("--check", action="store_true", help="validate without writing")
    args = parser.parse_args()
    generate_all_mega_packs(write=not args.check)
    if args.check:
        print("OK mega-packs: all mega-pack manifests validated")
    else:
        print("OK mega-packs: all mega-pack manifests generated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Run test to verify it passes**

Run: `py -3 tests/test_generate_mega_packs.py`
Expected: PASS (all 2 tests)

- [ ] **Step 5: Commit**

```bash
git add tools/generate_mega_packs.py tests/test_generate_mega_packs.py
git commit -m "feat: add mega-pack manifest generator

Derives mega-pack manifests from the union of plugin entries by custody root.
A worker adding an entry to any plugin manifest with the right source_family
gets mega-pack inclusion automatically on regeneration. --check mode fails
on stale mega-pack manifests."
```

---

## Phase 3: Normalize all 20 manifests

### Task 6: Normalize the 14 entries-legacy manifests (batch 1: claude-cortex family)

This task normalizes plugins whose entries come from the `claude-cortex` and `ecc` source families. These share the same legacy shape: `snapshot_path`/`local_path` file-level entries with `source_family`/`source_path`/`source_author`/`source_license`/`source_repo` fields.

**Plugins in this batch:** `api-contracts-pack` (5), `architecture-pack` (30), `frontend-pack` (16), `language-patterns-pack` (63), `planning-pack` (31), `security-pack` (56), `codex-cortex` (98)

**Transformation contract:**

For each legacy entry:
```json
{
  "snapshot_path": "skills/cqrs-event-sourcing/SKILL.md",
  "local_path": "skills/cqrs-event-sourcing/SKILL.md",
  "import_status": "imported",
  "content_mode": "normalised",
  "source_family": "claude-cortex",
  "source_path": "skills/cqrs-event-sourcing/SKILL.md",
  "source_author": "NickCrew",
  "source_license": "MIT",
  "source_repo": "https://github.com/NickCrew/Claude-Cortex"
}
```

Transform to:
```json
{
  "canonical_name": "cqrs-event-sourcing",
  "source_category": "third_party",
  "content_mode": "normalised",
  "source_family": "claude-cortex",
  "canonical_source_path": "sources/third_party/claude-cortex/upstream/skills/cqrs-event-sourcing",
  "local_path": "skills/cqrs-event-sourcing",
  "adaptation_overlay_path": "adapters/codex/<plugin>/skills/cqrs-event-sourcing",
  "provenance_note": "Projected from claude-cortex custody.",
  "source_path": "skills/cqrs-event-sourcing/SKILL.md",
  "source_author": "NickCrew",
  "source_license": "MIT",
  "source_repo": "https://github.com/NickCrew/Claude-Cortex"
}
```

Key transformations:
1. `canonical_name` = dir name extracted from `snapshot_path` (e.g. `cqrs-event-sourcing` from `skills/cqrs-event-sourcing/SKILL.md`)
2. `source_category` = `"third_party"` (all these are third-party)
3. `canonical_source_path` = custody root + dir path (e.g. `sources/third_party/claude-cortex/upstream/skills/cqrs-event-sourcing`)
4. `local_path` = dir path within plugin (e.g. `skills/cqrs-event-sourcing`, no SKILL.md suffix)
5. `adaptation_overlay_path` = path under `adapters/codex/<plugin>/` if the entry has adaptations; `null` or omitted if verbatim
6. `import_status` → if not `"imported"`, set `content_mode` to `"blocked"` or `"skipped"` and keep the entry explicit

**Important:** The `source_family` field on each entry determines which custody root it belongs to. For entries with `source_family: "ecc"`, the `canonical_source_path` prefix is `sources/third_party/ecc/upstream/`. For `source_family: "claude-cortex"`, it's `sources/third_party/claude-cortex/upstream/`.

- [ ] **Step 1: Write a migration helper script**

Create a temporary `tools/_tmp_migrate_legacy_manifest.py` that:
1. Reads a plugin's legacy bundle-manifest.json
2. Transforms each entry per the contract above
3. Writes the normalized manifest back
4. Prints a summary of what changed

The script should:
- Extract `canonical_name` from the directory name in `snapshot_path` (strip `SKILL.md` suffix)
- Map `source_family` to the correct custody root prefix
- Set `source_category` to `"third_party"` for all entries in these plugins
- Preserve `content_mode`, `source_author`, `source_license`, `source_repo`, `source_path`
- Set `local_path` to the directory (strip `SKILL.md`)
- Set `canonical_source_path` to `custody_root + "/" + snapshot_path_dir`
- Add `adaptation_overlay_path` only if `content_mode` is `normalised` or `adapted` (point to `adapters/codex/<plugin>/<skill-dir>` — the overlay may not exist yet for some, in which case use `null`)
- Convert `import_status: "skipped"`/`"blocked"` to `content_mode: "skipped"`/`"blocked"`

- [ ] **Step 2: Run the migration on each plugin in this batch**

For each plugin: `api-contracts-pack`, `architecture-pack`, `frontend-pack`, `language-patterns-pack`, `planning-pack`, `security-pack`, `codex-cortex`:

```bash
py -3 tools/_tmp_migrate_legacy_manifest.py --plugin <plugin-name>
```

Inspect the output. Verify:
- Every entry has `canonical_name`, `source_category`, `content_mode`, `source_family`, `canonical_source_path` (directory, no suffix), `local_path` (directory, no suffix)
- `canonical_source_path` points at a real directory under `sources/third_party/`
- No `snapshot_path` or `import_status` fields remain

- [ ] **Step 3: Update manifest top-level fields for each plugin**

For each normalized manifest, update the top-level fields:
- Add `"bundle_type": "projection-lane"`
- Add `"is_mega_pack": false` (except codex-cortex which gets `"is_mega_pack": true, "mega_pack_for": "claude-cortex"` — but codex-cortex's manifest is generated by the mega-pack generator, so it should NOT be hand-edited. Instead, the mega-pack generator will produce it from the union of claude-cortex entries across all plugins.)
- Remove legacy fields: `upstream_repo`, `pinned_commit`, `source_root`, `path_semantics`, `candidate_count`, `imported_count`, `skipped_count`, `blocked_count`
- Keep `source_families` as a list of family names
- Add `"plugin_author"` and `"plugin_license"` if missing

**For codex-cortex specifically:** Since it's a mega-pack, its manifest will be **generated** by `tools/generate_mega_packs.py`, not hand-edited. After normalizing all the topical plugins (api-contracts, architecture, frontend, language-patterns, planning, security), run the mega-pack generator to produce codex-cortex's manifest. Delete the hand-edited codex-cortex manifest and let the generator create it.

- [ ] **Step 4: Verify each manifest's entries point at real directories**

```bash
py -3 -c "
import json, pathlib
root = pathlib.Path('.')
for plugin in ['api-contracts-pack', 'architecture-pack', 'frontend-pack', 'language-patterns-pack', 'planning-pack', 'security-pack']:
    bm = json.loads((root / f'codex-marketplace/plugins/{plugin}/references/bundle-manifest.json').read_text(encoding='utf-8'))
    for e in bm.get('entries', []):
        if e.get('content_mode') in ('blocked', 'skipped'): continue
        csp = root / e.get('canonical_source_path', '')
        if not csp.is_dir():
            print(f'MISSING: {plugin}/{e.get(\"canonical_name\")}: {csp}')
print('done')
"
```
Expected: `done` with no MISSING lines.

- [ ] **Step 5: Run materializer check**

Run: `py -3 tools/materialize_projection.py --check`
Expected: Passes (or fails with clear projection mismatches that need fixing — fix by running `py -3 tools/materialize_projection.py` to write the projection)

- [ ] **Step 6: Run validation and fix any issues**

Run: `py -3 tools/validate_marketplace.py`
Fix any validation failures. The plugin-specific validators (`validate_skill_bundle_manifest`, etc.) may need updating to handle the new schema. See Task 10 for validator updates.

- [ ] **Step 7: Clean up the temporary migration script**

```bash
rm tools/_tmp_migrate_legacy_manifest.py
```

- [ ] **Step 8: Commit**

```bash
git add -A
git commit -m "feat: normalize claude-cortex and ecc family manifests to projection-lane shape

Migrates api-contracts-pack, architecture-pack, frontend-pack,
language-patterns-pack, planning-pack, security-pack from legacy
snapshot_path/local_path file-level entries to directory-level entries[]
with canonical_name/source_category/content_mode/canonical_source_path/
local_path/source_family. codex-cortex becomes a generated mega-pack."
```

---

### Task 7: Normalize the ecc-only and other third-party manifests (batch 2)

**Plugins in this batch:** `data-platform-pack` (11), `media-content-pack` (10), `ops-connectors-pack` (9), `superpowers-ecc` (14), `game-studio` (9), `dotnet-kit` (6), `unslop-plus` (19)

These follow the same transformation contract as Task 6, but with different custody roots:
- `ecc` family → `sources/third_party/ecc/upstream/`
- `game-studio` family → `sources/third_party/game-studio/upstream/` (or `openai/plugins` — verify the actual custody path)
- `dotnet-claude-kit` family → `sources/third_party/dotnet-claude-kit/upstream/`
- `unslop` family → `sources/third_party/unslop/upstream/`

For `unslop-plus`, note it has a hybrid `first-party-profiles` family. Those entries have `source_category: "first_party"` and `source_family: "first_party"` — they should be treated as first-party entries that also appear in `house-skills`.

- [ ] **Step 1: Run the migration helper on each plugin**

Use the same `tools/_tmp_migrate_legacy_manifest.py` script from Task 6. For each plugin, verify the custody root prefix is correct for its source_family.

- [ ] **Step 2: Handle unslop-plus first-party-profiles entries**

For `unslop-plus` entries with `source_family: "first-party-profiles"`:
- Set `source_category: "first_party"`, `source_family: "first_party"`
- Set `canonical_source_path` to `sources/first_party/skills/<skill-name>`
- These entries will also appear in `house-skills` via mega-pack auto-inclusion

- [ ] **Step 3: Verify all entries point at real directories**

Same verification as Task 6 Step 4.

- [ ] **Step 4: Run materializer and validation**

Run: `py -3 tools/materialize_projection.py --check` and `py -3 tools/validate_marketplace.py`
Fix any issues.

- [ ] **Step 5: Clean up and commit**

```bash
rm tools/_tmp_migrate_legacy_manifest.py
git add -A
git commit -m "feat: normalize ecc, game-studio, dotnet-kit, unslop manifests to projection-lane shape"
```

---

### Task 8: Normalize the components-legacy and hybrid manifests

**Plugins in this batch:** `adventures-pack` (17 components), `everything-codex-code` (14 components), `wild-bunch-project-pack` (11 entries)

These use `components[]` or hybrid `entries[]` with file-level paths.

**Transformation for adventures-pack:**
- Convert `components[]` to `entries[]`
- Each component has `canonical_name`, `source_path` (file-level), `local_path` (file-level), `projection_status`
- Transform `source_path` → `canonical_source_path` (directory, strip SKILL.md)
- Transform `local_path` → directory (strip SKILL.md)
- Set `source_category: "first_party"`, `content_mode: "verbatim"`, `source_family: "first_party"`
- `canonical_source_path` = `sources/first_party/skills/<name>`

**Transformation for everything-codex-code:**
- This is the mega-pack for `ecc`. After Task 7 normalizes the ecc topical plugins, this manifest is **generated** by `tools/generate_mega_packs.py`. Delete the hand-edited manifest and let the generator produce it.

**Transformation for wild-bunch-project-pack:**
- Already has `entries[]` with new-schema field names but file-level `canonical_source_path`
- Transform: strip SKILL.md suffix from `canonical_source_path` and `local_path`
- Set `source_family` based on the entry's source (first_party for wild-bunch skills, game-studio for game-studio skills)

- [ ] **Step 1: Normalize adventures-pack**

Convert components[] to entries[] with directory-level paths. All adventures-pack entries are first-party.

- [ ] **Step 2: Delete hand-edited everything-codex-code manifest**

```bash
# The mega-pack generator will create it
py -3 tools/generate_mega_packs.py
```

- [ ] **Step 3: Normalize wild-bunch-project-pack**

Strip file suffixes from `canonical_source_path` and `local_path`. Set `source_family` per entry.

- [ ] **Step 4: Run materializer and validation**

Run: `py -3 tools/materialize_projection.py --check` and `py -3 tools/validate_marketplace.py`

- [ ] **Step 5: Commit**

```bash
git add -A
git commit -m "feat: normalize adventures-pack, everything-codex-code, wild-bunch manifests"
```

---

### Task 9: Normalize repo-worker-base (skills-legacy shape)

**Plugin:** `repo-worker-base` (47 skills[] entries)

This is the only `skills[]`-shape plugin. Each skill has `name`, `lane`, `path`, optional `content_mode`, `upstream_author`, `upstream_license`.

**Investigation needed:** Determine whether these 47 skills have source custody under `sources/first_party/skills/` or are repo-internal worker skills without custody. The prior session flagged this as a candidate red blocker.

- [ ] **Step 1: Inspect repo-worker-base skills**

Check which of the 47 skill names have corresponding dirs under `sources/first_party/skills/`:

```bash
py -3 -c "
import json, pathlib
root = pathlib.Path('.')
bm = json.loads((root / 'codex-marketplace/plugins/repo-worker-base/references/bundle-manifest.json').read_text(encoding='utf-8'))
skills = bm.get('skills', [])
for s in skills:
    name = s.get('name')
    fp = root / 'sources/first_party/skills' / name
    has_custody = fp.is_dir() and (fp / 'SKILL.md').exists()
    if not has_custody:
        print(f'NO CUSTODY: {name}')
print(f'total: {len(skills)}, checked')
"
```

- [ ] **Step 2: Based on inspection, normalize or record a red blocker**

**If all 47 skills have first-party custody:** Convert `skills[]` to `entries[]` with the standard schema. Each entry gets `source_category: "first_party"`, `content_mode: "verbatim"`, `source_family: "first_party"`, `canonical_source_path: "sources/first_party/skills/<name>"`, `local_path: "skills/<name>"`.

**If some skills lack custody:** For skills without custody, either:
(a) Create first-party custody dirs for them under `sources/first_party/skills/` (copy the SKILL.md from the projection to custody), or
(b) Record a red blocker with: why they can't be normalized, the exact green condition (custody dirs created), and the actions to reach green.

Based on the prior session's analysis, `repo-worker-base` has a SKILL.md in `sources/first_party/skills/repo-worker-base/` (it appeared in the "with SKILL.md" list). This suggests the repo-worker-base skill itself has custody, but the 47 skills *within* the plugin may be sub-skills or references. Inspect carefully.

- [ ] **Step 3: Run validation and commit**

```bash
git add -A
git commit -m "feat: normalize repo-worker-base from skills[] to entries[] projection-lane shape"
```

---

## Phase 4: Orphan and drift detection

### Task 10: Add first-party orphan detection

**Files:**
- Modify: `tools/validate_marketplace.py` (add orphan detection function, wire into main)
- Test: `tests/test_validate_marketplace.py` (add orphan detection tests)

- [ ] **Step 1: Write the failing test**

Add to `tests/test_validate_marketplace.py`:

```python
class FirstPartyOrphanDetectionTests(unittest.TestCase):
    def test_detects_orphaned_first_party_skill(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            # Create a first-party skill with no manifest entry
            orphan_dir = temp_root / "sources" / "first_party" / "skills" / "orphan-skill"
            orphan_dir.mkdir(parents=True)
            (orphan_dir / "SKILL.md").write_text("---\nname: orphan-skill\n---\nbody", encoding="utf-8")
            # Create a plugin with no entries referencing it
            plugin_root = temp_root / "codex-marketplace" / "plugins" / "some-pack"
            (plugin_root / "references").mkdir(parents=True)
            (plugin_root / "references" / "bundle-manifest.json").write_text(
                json.dumps({"bundle_name": "some-pack", "entries": []}), encoding="utf-8"
            )

            with patch("validate_marketplace.ROOT", temp_root):
                from validate_marketplace import detect_first_party_orphans
                orphans = detect_first_party_orphans()
                self.assertIn("orphan-skill", orphans)

    def test_no_orphans_when_all_skills_projected(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            skill_dir = temp_root / "sources" / "first_party" / "skills" / "projected-skill"
            skill_dir.mkdir(parents=True)
            (skill_dir / "SKILL.md").write_text("---\nname: projected-skill\n---\nbody", encoding="utf-8")
            plugin_root = temp_root / "codex-marketplace" / "plugins" / "house-skills"
            (plugin_root / "references").mkdir(parents=True)
            (plugin_root / "references" / "bundle-manifest.json").write_text(
                json.dumps({
                    "bundle_name": "house-skills",
                    "entries": [
                        {"canonical_name": "projected-skill", "source_category": "first_party",
                         "content_mode": "verbatim", "source_family": "first_party",
                         "canonical_source_path": "sources/first_party/skills/projected-skill",
                         "local_path": "skills/projected-skill"}
                    ],
                }),
                encoding="utf-8",
            )

            with patch("validate_marketplace.ROOT", temp_root):
                from validate_marketplace import detect_first_party_orphans
                orphans = detect_first_party_orphans()
                self.assertEqual(orphans, [])
```

- [ ] **Step 2: Run test to verify it fails**

Run: `py -3 tests/test_validate_marketplace.py`
Expected: FAIL with `ImportError: cannot import name 'detect_first_party_orphans'`

- [ ] **Step 3: Implement orphan detection**

Add to `tools/validate_marketplace.py`:

```python
def detect_first_party_orphans() -> list[str]:
    """Detect first-party skill dirs with SKILL.md that have no projection entry."""
    skills_root = ROOT / "sources" / "first_party" / "skills"
    if not skills_root.is_dir():
        return []
    # Collect all first-party skill dirs that have a SKILL.md
    custody_skills: set[str] = set()
    for d in skills_root.iterdir():
        if d.is_dir() and (d / "SKILL.md").exists():
            custody_skills.add(d.name)
    # Collect all canonical_names from first_party entries across all manifests
    projected_names: set[str] = set()
    for spec in PROTECTED_MARKETPLACE_PLUGIN_SPECS:
        plugin_root = ROOT / spec["plugin_root"]
        manifest_path = plugin_root / "references" / "bundle-manifest.json"
        if not manifest_path.exists():
            continue
        manifest = load_json(manifest_path)
        for entry in manifest.get("entries", []):
            if isinstance(entry, dict) and entry.get("source_category") == "first_party":
                name = entry.get("canonical_name")
                if name:
                    projected_names.add(name)
    orphans = sorted(custody_skills - projected_names)
    return orphans
```

- [ ] **Step 4: Wire orphan detection into main()**

In `main()`, add after the existing validation steps:

```python
    orphans = detect_first_party_orphans()
    if orphans:
        raise ValueError(
            f"first-party orphan skills detected (have SKILL.md in custody but no projection entry): {orphans}\n"
            f"Fix: add manifest entries for these skills and regenerate."
        )
    print(f"OK first-party orphan check: {len(custody_skills)} skills, 0 orphans")
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `py -3 tests/test_validate_marketplace.py`
Expected: PASS

- [ ] **Step 6: Run full validation**

Run: `py -3 tools/validate_marketplace.py`
Expected: Passes (if all 61 first-party skills are now in manifests) or reports orphans (fix by adding manifest entries).

- [ ] **Step 7: Commit**

```bash
git add tools/validate_marketplace.py tests/test_validate_marketplace.py
git commit -m "feat: add first-party orphan detection to marketplace validation

Detects first-party skill dirs with SKILL.md that have no projection entry
in any plugin manifest. Fails validation with a clear message listing the
orphans and how to fix them."
```

---

### Task 11: Add mega-pack inclusion validation

**Files:**
- Modify: `tools/validate_marketplace.py` (add mega-pack inclusion check)
- Test: `tests/test_validate_marketplace.py`

- [ ] **Step 1: Write the failing test**

Add a test that verifies mega-pack inclusion: a first-party entry in a topical plugin must also appear in `house-skills`. An ecc entry in a topical plugin must also appear in `everything-codex-code`.

- [ ] **Step 2: Run test to verify it fails**

- [ ] **Step 3: Implement mega-pack inclusion validation**

Add to `tools/validate_marketplace.py`:

```python
def validate_mega_pack_inclusion() -> None:
    """Validate that every entry in a topical plugin also appears in its mega-pack."""
    from generate_mega_packs import load_mega_pack_registry, collect_entries_by_family, _load_plugin_manifest
    registry = load_mega_pack_registry()
    mega_pack_names = {m["mega_pack"] for m in registry}
    inventory = load_plugin_root_inventory()

    # Collect entries from topical (non-mega-pack) plugins
    topical_manifests = []
    for spec in inventory:
        if spec["name"] in mega_pack_names:
            continue
        plugin_root = ROOT / spec["plugin_root"]
        manifest = _load_plugin_manifest(plugin_root)
        if manifest:
            topical_manifests.append(manifest)

    by_family = collect_entries_by_family(topical_manifests)

    for mapping in registry:
        family = mapping["source_family"]
        mega_name = mapping["mega_pack"]
        mega_root = ROOT / mapping["mega_pack_root"]
        mega_manifest_path = mega_root / "references" / "bundle-manifest.json"
        if not mega_manifest_path.exists():
            raise ValueError(f"mega-pack manifest missing for {family}: {mega_manifest_path}")
        mega_manifest = load_json(mega_manifest_path)
        mega_names = {
            e.get("canonical_name") for e in mega_manifest.get("entries", [])
            if isinstance(e, dict) and e.get("content_mode") not in ("blocked", "skipped")
        }
        topical_names = {
            e.get("canonical_name") for e in by_family.get(family, [])
        }
        missing = sorted(topical_names - mega_names)
        if missing:
            raise ValueError(
                f"mega-pack {mega_name} is missing entries that appear in topical plugins: {missing}\n"
                f"Fix: run py -3 tools/generate_mega_packs.py"
            )
    print("OK mega-pack inclusion: all topical entries appear in their mega-packs")
```

- [ ] **Step 4: Wire into main()**

Add `validate_mega_pack_inclusion()` call in `main()`.

- [ ] **Step 5: Run tests and validation**

Run: `py -3 tests/test_validate_marketplace.py` and `py -3 tools/validate_marketplace.py`

- [ ] **Step 6: Commit**

```bash
git add tools/validate_marketplace.py tests/test_validate_marketplace.py
git commit -m "feat: add mega-pack inclusion validation

Validates that every entry in a topical plugin also appears in its
mega-pack. Fails if the mega-pack manifest is stale. Points the worker
to run the mega-pack generator."
```

---

### Task 12: Add projection drift detection for skipped plugins

**Files:**
- Modify: `tools/validate_marketplace.py` (add drift detection that catches entries green-passing because a plugin is skipped as legacy/hybrid)

- [ ] **Step 1: Add a validation that no plugin manifest is silently skipped**

After all manifests are normalized, the materializer's `_load_bundle_manifest` skip logic (which returns `None` for legacy/hybrid shapes) should no longer skip any plugin. Add a check:

```python
def validate_no_legacy_manifest_shapes() -> None:
    """Validate that no plugin manifest uses a legacy shape that the materializer would skip."""
    for spec in PROTECTED_MARKETPLACE_PLUGIN_SPECS:
        plugin_root = ROOT / spec["plugin_root"]
        manifest_path = plugin_root / "references" / "bundle-manifest.json"
        if not manifest_path.exists():
            continue
        manifest = load_json(manifest_path)
        entries = manifest.get("entries")
        if not isinstance(entries, list):
            raise ValueError(
                f"{spec['name']}: manifest must have entries[] array (legacy skills[] or components[] not allowed)"
            )
        if not entries:
            continue
        first = entries[0]
        if not isinstance(first, dict):
            raise ValueError(f"{spec['name']}: first entry must be an object")
        if "canonical_name" not in first or "canonical_source_path" not in first:
            raise ValueError(
                f"{spec['name']}: entries must have canonical_name and canonical_source_path (legacy shape)"
            )
        csp = first.get("canonical_source_path", "")
        if isinstance(csp, str) and Path(csp).suffix:
            raise ValueError(
                f"{spec['name']}: canonical_source_path must be directory-level (legacy file-level path: {csp})"
            )
    print("OK manifest shape: all plugins use projection-lane directory-level entries[]")
```

- [ ] **Step 2: Wire into main() and commit**

```bash
git add tools/validate_marketplace.py
git commit -m "feat: add manifest shape validation that rejects legacy/hybrid shapes

Ensures no plugin manifest can green-pass the materializer by using a
legacy or hybrid shape. All manifests must use directory-level entries[]
with canonical_name and canonical_source_path."
```

---

## Phase 5: Manifest-driven proof surfaces

### Task 13: Generate provenance-map.json from manifests

**Files:**
- Create: `tools/generate_provenance_maps.py`
- Modify: `codex-marketplace/plugins/superpowers-plus/references/provenance-map.json` (will be regenerated)
- Modify: `codex-marketplace/plugins/wild-bunch-project-pack/references/provenance-map.json` (will be regenerated)

- [ ] **Step 1: Create the provenance-map generator**

Create `tools/generate_provenance_maps.py` that:
1. Reads each plugin's bundle-manifest.json
2. Generates a provenance-map.json from the manifest entries
3. Has `--check` mode that fails on drift

The generator produces `source_backed_projections` (first_party verbatim entries) and `adapted_projections` (third-party adapted/normalised entries) from the manifest's `entries[]`.

- [ ] **Step 2: Run the generator**

```bash
py -3 tools/generate_provenance_maps.py
```

- [ ] **Step 3: Verify the generated maps match the existing hand-maintained ones**

If they don't match, inspect the differences. The generator is the new source of truth; the hand-maintained map is retired.

- [ ] **Step 4: Add --check mode and wire into validation**

- [ ] **Step 5: Commit**

```bash
git add tools/generate_provenance_maps.py codex-marketplace/plugins/*/references/provenance-map.json
git commit -m "feat: generate provenance-map.json from bundle manifests

Provenance maps are now generated from manifest entries, not hand-maintained.
The generator produces source_backed_projections and adapted_projections from
the manifest's entries[] array. --check mode fails on drift."
```

---

### Task 14: Generate source-map.md from manifests

**Files:**
- Create: `tools/generate_source_maps.py`
- Modify: all 19 `source-map.md` files (will be regenerated)

- [ ] **Step 1: Create the source-map generator**

Create `tools/generate_source_maps.py` that:
1. Reads each plugin's bundle-manifest.json
2. Generates a source-map.md markdown table from the manifest entries
3. Has `--check` mode that fails on drift

The table columns: `Skill | Source category | Content mode | Canonical source path | Local path | Notes`

- [ ] **Step 2: Run the generator and verify**

```bash
py -3 tools/generate_source_maps.py
py -3 tools/generate_source_maps.py --check
```

- [ ] **Step 3: Commit**

```bash
git add tools/generate_source_maps.py codex-marketplace/plugins/*/references/source-map.md
git commit -m "feat: generate source-map.md from bundle manifests

Source maps are now generated from manifest entries. --check mode fails
on drift."
```

---

## Phase 6: Update validators and doctrine

### Task 15: Update plugin-specific validators for new schema

**Files:**
- Modify: `tools/validate_marketplace.py` (update `validate_skill_bundle_manifest`, `validate_superpowers_bundle_manifest`, `validate_wild_bunch_bundle_manifest`, `validate_project_bundle_manifest`, `validate_everything_codex_code_bundle_manifest`, `validate_bundle_manifest`)

The existing plugin-specific validators were written for the legacy shapes. After normalization, they need to handle the new directory-level `entries[]` schema. Many of these validators can be replaced by a single generic validator that checks:
1. Every entry has the required fields (`canonical_name`, `source_category`, `content_mode`, `source_family`, `canonical_source_path`, `local_path`)
2. `canonical_source_path` is directory-level (no suffix) for active entries
3. `canonical_source_path` exists as a directory (for active entries)
4. First-party entries are `verbatim` with no overlay
5. Third-party `normalised`/`adapted` entries have `adaptation_overlay_path`
6. `blocked`/`skipped` entries are explicit

- [ ] **Step 1: Write a generic manifest validator**

Add `validate_projection_lane_manifest(bundle_manifest, plugin_root)` to `tools/validate_marketplace.py` that validates the normalized schema.

- [ ] **Step 2: Replace plugin-specific validators with calls to the generic validator**

For each plugin-specific validator, either:
- Replace it entirely with a call to `validate_projection_lane_manifest` (if the plugin has no special rules), or
- Keep it but have it call `validate_projection_lane_manifest` first, then apply plugin-specific checks

- [ ] **Step 3: Update tests**

Update `tests/test_validate_marketplace.py` to test the new generic validator.

- [ ] **Step 4: Run validation and commit**

```bash
git add tools/validate_marketplace.py tests/test_validate_marketplace.py
git commit -m "refactor: replace plugin-specific manifest validators with generic projection-lane validator

All 20 plugin manifests now use the same directory-level entries[] schema,
so plugin-specific validators are replaced by a single generic validator
that checks the normalized shape."
```

---

### Task 16: Update doctrine and AGENTS files

**Files:**
- Modify: `docs/custody-and-projection-doctrine.md`
- Modify: `AGENTS.md` (if needed)
- Modify: `tools/AGENTS.md` (if needed)
- Modify: `codex-marketplace/AGENTS.md` (if needed)

- [ ] **Step 1: Update doctrine**

In `docs/custody-and-projection-doctrine.md`:
- Remove the "Self-hosted control-plane exception" section (already done in Task 2, verify)
- Add a "Mega-pack auto-inclusion" section documenting the custody→mega-pack registry and generator
- Update "First-party orphan detection" section to describe the implemented detection
- Update "Source custody" section to reflect the single `sources/first_party/skills/` tree (no more `core/`)
- Add "Proof surface generation" section documenting that provenance-map.json and source-map.md are generated

- [ ] **Step 2: Update AGENTS files**

Update any AGENTS.md files that reference the old manifest shapes, the self-hosted exception, or the `core/` directory.

- [ ] **Step 3: Commit**

```bash
git add docs/custody-and-projection-doctrine.md AGENTS.md tools/AGENTS.md codex-marketplace/AGENTS.md
git commit -m "docs: update doctrine and AGENTS files for normalized projection-lane shape

Removes self-hosted exception, documents mega-pack auto-inclusion,
orphan detection, and proof-surface generation. Updates custody section
for single skills/ tree."
```

---

## Phase 7: Regenerate, validate, and publish

### Task 17: Regenerate all derived surfaces

- [ ] **Step 1: Regenerate mega-pack manifests**

```bash
py -3 tools/generate_mega_packs.py
```

- [ ] **Step 2: Regenerate provenance maps**

```bash
py -3 tools/generate_provenance_maps.py
```

- [ ] **Step 3: Regenerate source maps**

```bash
py -3 tools/generate_source_maps.py
```

- [ ] **Step 4: Regenerate repo index**

```bash
py -3 tools/generate_repo_index.py
```

- [ ] **Step 5: Regenerate marketplace manifests**

```bash
py -3 tools/generate_marketplace.py
```

- [ ] **Step 6: Regenerate skill zips**

```bash
py -3 tools/update_skill_artifacts.py --all
```

- [ ] **Step 7: Commit**

```bash
git add -A
git commit -m "feat: regenerate all derived surfaces from normalized manifests

Mega-pack manifests, provenance maps, source maps, repo index, marketplace
manifests, and skill zips all regenerated from the normalized projection-lane
manifests."
```

---

### Task 18: Run full validation suite

- [ ] **Step 1: Run marketplace validation**

```bash
py -3 tools/validate_marketplace.py
```
Expected: `Marketplace validation passed.`

- [ ] **Step 2: Run materializer check**

```bash
py -3 tools/materialize_projection.py --check
```
Expected: `OK projection: all projection-lane plugins validated`

- [ ] **Step 3: Run mega-pack check**

```bash
py -3 tools/generate_mega_packs.py --check
```
Expected: `OK mega-packs: all mega-pack manifests validated`

- [ ] **Step 4: Run drift validation**

```bash
py -3 tools/validate_generated_drift.py --base origin/main
```
Expected: Passes (or requires `--full-regeneration` flag since this is a full regen)

- [ ] **Step 5: Run artifact check**

```bash
py -3 tools/update_skill_artifacts.py --check
```
Expected: Passes

- [ ] **Step 6: Run all tests**

```bash
py -3 tests/test_validate_marketplace.py
py -3 tests/test_skill_overlay_materializer.py
py -3 tests/test_tree_canonicalization.py
py -3 tests/test_generate_mega_packs.py
```
Expected: All tests pass

- [ ] **Step 7: Run git diff check**

```bash
git diff --check HEAD~1 HEAD
```
Expected: No whitespace errors

- [ ] **Step 8: Create the inventory/classification report**

Create `docs/marketplace-projection-normalization-report.md` documenting:
- The before/after classification of all 20 plugins
- The custody→mega-pack mapping
- The proof surfaces that are now generated
- The orphan detection and drift detection that is now enforced
- Any red blockers with green conditions and actions

- [ ] **Step 9: Commit**

```bash
git add docs/marketplace-projection-normalization-report.md
git commit -m "docs: add marketplace projection normalization report"
```

---

### Task 19: Push and create PR

- [ ] **Step 1: Push the branch**

```bash
git push -u origin harleydbartles/mark-285-normalize-marketplace-projection-custody-and-drift-tooling
```

- [ ] **Step 2: Create the PR**

```bash
gh pr create --title "MARK-285: Normalize marketplace projection custody and drift tooling" --body "$(cat <<'EOF'
## Summary

- Fixes validator-disagreement drift bug with shared tree canonicalization
- Eliminates house-skills self-hosted exception by moving control-plane source to first-party custody
- Folds `sources/first_party/core/` into `sources/first_party/skills/` (single tree, 61 real skills)
- Ejects governance metadata dirs to `provenance/<plugin>-governance/`
- Adds custody→mega-pack registry and mega-pack manifest generator with auto-inclusion
- Normalizes all 20 plugin manifests to directory-level `entries[]` projection-lane shape
- Adds first-party orphan detection and mega-pack inclusion validation
- Generates provenance-map.json and source-map.md from manifests (no more hand-maintained mirrors)
- Replaces plugin-specific validators with a generic projection-lane validator
- Updates doctrine and AGENTS files

## Changed files grouped by lane

**Manifests:**
- All 20 plugin bundle-manifest.json files normalized to projection-lane shape
- `codex-marketplace/custody-mega-pack-registry.json` (new)

**Validators/generators:**
- `tools/tree_canonicalization.py` (new — shared canonicalization)
- `tools/generate_mega_packs.py` (new — mega-pack manifest generator)
- `tools/generate_provenance_maps.py` (new — provenance map generator)
- `tools/generate_source_maps.py` (new — source map generator)
- `tools/validate_marketplace.py` (orphan detection, mega-pack inclusion, shape validation, generic validator)
- `tools/materialize_projection.py` (shared canonicalization, self-hosted skip removed)
- `tools/marketplace_utils.py` (updated paths)

**Doctrine/docs:**
- `docs/custody-and-projection-doctrine.md` (self-hosted exception removed, mega-pack auto-inclusion documented)
- `docs/marketplace-projection-normalization-report.md` (new — inventory/classification report)
- `AGENTS.md`, `tools/AGENTS.md`, `codex-marketplace/AGENTS.md` (updated references)

**Custody:**
- `sources/first_party/skills/house-skills/` (control-plane source moved here)
- `sources/first_party/core/` (deleted — 9 skills folded into skills/)
- `provenance/<plugin>-governance/` (governance metadata ejected from skills/)

**Projections/generated outputs:**
- All projection directories regenerated via materializer
- `generated/skill-zips/` regenerated via `update_skill_artifacts.py --all`
- `repo-index/repo-index.json` regenerated
- All `provenance-map.json` and `source-map.md` files regenerated

#### Test plan

- [ ] `py -3 tools/validate_marketplace.py` passes
- [ ] `py -3 tools/materialize_projection.py --check` passes
- [ ] `py -3 tools/generate_mega_packs.py --check` passes
- [ ] `py -3 tools/validate_generated_drift.py --base origin/main` passes
- [ ] `py -3 tools/update_skill_artifacts.py --check` passes
- [ ] All unit tests pass
- [ ] `git diff --check HEAD~1 HEAD` passes
- [ ] No first-party orphans detected
- [ ] All mega-pack manifests current

Generated with [Devin](https://devin.ai)
EOF
)"
```

- [ ] **Step 3: Verify PR is mergeable**

Check the PR status on GitHub. If not mergeable, resolve conflicts.

- [ ] **Step 4: Report completion on Linear**

Comment on MARK-285 with:
- PR URL and branch
- Changed files grouped by lane
- Validation command results
- Before/after statement for orphan detection and drift detection
- Any follow-up issues created

---

## Self-Review

### Spec coverage

1. ✅ Inventory/classification report — Task 18 Step 8
2. ✅ Custody→mega-pack registry — Task 4
3. ✅ Mega-pack generator + validator — Task 5, Task 11
4. ✅ First-party orphan + projection drift detection — Task 10, Task 12
5. ✅ Normalize all 20 manifests — Tasks 6, 7, 8, 9
6. ✅ Manifest-driven proof surfaces — Tasks 13, 14
7. ✅ Regenerate + validate + publish — Tasks 17, 18, 19
8. ✅ house-skills self-hosted exception eliminated — Task 2
9. ✅ Validator-disagreement bug fixed — Task 1
10. ✅ core/ folded into skills/ — Task 3
11. ✅ Governance dirs ejected — Task 3
12. ✅ Doctrine updated — Task 16

### Placeholder scan

- Tasks 6-9 (manifest normalization) use a transformation contract + migration helper script rather than writing out all 300+ entry transformations. This is intentional — the migration is mechanical and the helper script encodes the contract. The executor must verify each manifest after migration.
- Task 9 (repo-worker-base) has an investigation step because the prior session flagged it as a candidate red blocker. The executor must inspect before deciding normalize vs red-blocker.
- Task 15 (validator updates) is intentionally high-level because the exact changes depend on what the plugin-specific validators currently enforce. The generic validator contract is specified.

### Type consistency

- `canonical_name`, `source_category`, `content_mode`, `source_family`, `canonical_source_path`, `local_path` — used consistently across all tasks
- `is_mega_pack`, `mega_pack_for` — used in mega-pack manifests (Tasks 5, 8)
- `detect_first_party_orphans` — defined in Task 10, used in Task 18
- `validate_mega_pack_inclusion` — defined in Task 11, used in Task 18
- `validate_no_legacy_manifest_shapes` — defined in Task 12, used in Task 18
