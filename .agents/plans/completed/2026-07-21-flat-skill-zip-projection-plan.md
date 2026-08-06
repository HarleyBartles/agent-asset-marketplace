# `flat-skill-zip-projection` Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: `superpowers:executing-plans` (or `superpowers:subagent-driven-development`). Steps use checkbox syntax for tracking.

**Goal:** Replace the per-pack `generated/skill-zips/<pack>/<skill>/skill.zip` + `registry.json` pipeline with a single `tools/project_skills.py` generator/validator that projects every non-skipped/non-blocked bundle entry into all plugin skill trees and writes one flat, deterministic `generated/skill-zips/<canonical_name>.zip` per unique `canonical_name`. Delete the `adapters/gpt/` tree and the obsolete projection/zip/GPT-export tools.

**Architecture:** `project_skills.py` becomes the only place that stages overlays, copies staged trees to `codex-marketplace/plugins/<pack>/skills/<skill>`, writes flat zips, and prunes stale plugin skill dirs and generated zip artifacts. `update_skill_artifacts.py` orchestrates `generate_mega_packs`, `generate_pack_manifests`, `project_skills`, and `generate_first_party_skill_catalog`. `validate_marketplace.py` calls `tools/project_skills.py --check` and performs flat-zip assertions. `tools/skill_validation.py` holds the moved `validate_skill_markdown_frontmatter` helper.

**Tech Stack:** Python 3.13-compatible standard library, PyYAML, existing `marketplace_utils`, `skill_overlay_materializer`, `tree_canonicalization`.

## Global Constraints

- One zip per unique `canonical_name` (currently 94); no `registry.json`; no per-pack zip subdirectories.
- `generated/skill-zips/` must contain only `<skill>.zip` files and no other files after regeneration.
- Deterministic zip bytes: `1980-01-01 00:00:00`, `0644`, `ZIP_DEFLATED`.
- `--check` compares plugin trees with `tree_canonicalization.compare_trees_canonicalized` and verifies zip shape/namelist without byte-comparing existing zips.
- All generated text files written with LF (`newline="\n"`).
- Generated surfaces remain derived; docs/AGENTS/README surfaces must not claim `adapters/gpt/`, `registry.json`, or per-pack zip paths are current.

### Count reconciliation

A live scan of current bundle manifests shows **168 active entries** across all plugin roots and **94 unique `canonical_name` values**:

```text
py -3 -c "import json, pathlib, collections; R=pathlib.Path('Z:/agent-asset-marketplace'); E=[]; [E.extend(json.loads(p.read_text()).get('entries',[])) for p in (R/'codex-marketplace/plugins').glob('*/references/bundle-manifest.json')]; A=[e for e in E if e.get('import_status') not in {'skipped','blocked','out_of_scope'} and e.get('content_mode') not in {'blocked','skipped'}]; print('active entries:', len(A)); print('unique canonical names:', len({e['canonical_name'] for e in A})); print('import_status', collections.Counter(e.get('import_status') for e in E)); print('content_mode', collections.Counter(e.get('content_mode') for e in E))"
```

The implementation target is **94 flat zips**, one per unique `canonical_name`. Verify the exact count in Task 8.

## File Structure

| File | Responsibility |
| --- | --- |
| `tools/project_skills.py` | New single generator/validator for projection trees and flat zips. |
| `tools/skill_validation.py` | Moved `validate_skill_markdown_frontmatter` and supporting constants/helpers. |
| `tools/update_skill_artifacts.py` | Orchestrates `generate_mega_packs`, `generate_pack_manifests`, `project_skills`, `generate_first_party_skill_catalog`. |
| `tools/validate_marketplace.py` | Calls `tools/project_skills.py --check`; flat-zip assertions; imports `validate_skill_markdown_frontmatter` from `skill_validation`. |
| `tools/validate_skill_zips.py` | Rewritten as thin wrapper over `project_skills --check`. |
| `tools/rebuild_marketplace.py` | Calls `update_skill_artifacts.py --all` (no `--base`). |
| `tools/check_marketplace.py` | Calls `update_skill_artifacts.py --check` (no obsolete flags). |
| `tools/generate_pack_manifests.py` | `SOURCE.md` generated block uses flat zip path. |
| `tools/generate_repo_index.py` | Removes `generated_drift` validation key; updates `superpowers-plus-marketplace` key_validation_scripts. |
| `tools/validate_repo_index.py` | Drops `generated_drift` check; updates `skill_zips_check` command. |
| `tools/generate_first_party_skill_catalog.py` | Uses flat `generated/skill-zips/<skill>.zip` instead of `registry.json`. |
| `tools/install_agent_skills.py` | Imports `validate_skill_markdown_frontmatter` from `skill_validation`. |
| `tests/test_generator_check_modes.py` | `project_skills` tests; updated `update_skill_artifacts` check test; removed `validate_generated_drift` test. |
| `tests/test_validate_marketplace.py` | Updated projection-materializer command; `skill_validation` imports. |
| `tests/test_skill_overlay_materializer.py` | `skill_validation` import. |
| `tools/AGENTS.md`, `codex-marketplace/AGENTS.md`, `codex-marketplace/plugins/AGENTS.md`, `docs/custody-and-projection-doctrine.md`, `docs/overlay-adapter-policy.md`, `.agents/docs/unslop/profile.md`, `README.md`, `codex-marketplace/README.md`, `repo-index/README.md`, `.agents/guides/marketplace-generation-guide.md`, `provenance/house-skills.md`, `tools/README.md` | Remove `adapters/gpt/`, per-pack zip path, `registry.json`, obsolete tool references. |
| `adapters/gpt/` | Deleted entirely. |
| `tools/materialize_projection.py`, `tools/skill_zip_artifacts.py`, `tools/skill_gpt_exports.py`, `tools/export_skill_zips.py`, `tools/validate_export_skill_zips.py`, `tools/validate_generated_drift.py`, `tools/package_skill_zips.py` | Deleted after moving function. |

## Task 1: Create `tools/skill_validation.py` and repoint `install_agent_skills.py`

**Files:**
- Add `tools/skill_validation.py`
- Modify `tools/install_agent_skills.py:16`

**Expected interim state:** `tools/skill_validation.py` exists and `validate_skill_markdown_frontmatter` can be imported from it. `tools/skill_zip_artifacts.py` still exists but is no longer imported for frontmatter. `validate_marketplace.py` will be repointed in Task 5.

**Step 1: Create `tools/skill_validation.py` by moving code from `tools/skill_zip_artifacts.py`**

No logic changes. Move the following unchanged blocks from `tools/skill_zip_artifacts.py` into a new `tools/skill_validation.py`:

- imports: `import os`, `from pathlib import Path`, `import yaml`, `from yaml.nodes import MappingNode, ScalarNode, SequenceNode`
- `ROOT = Path(__file__).resolve().parents[1]`
- `PROJECTED_SKILL_METADATA_REQUIRED_NAMES = {"using-superpowers"}`
- `_as_windows_long_path` (lines 89-96)
- `_projected_skill_requires_metadata` (lines 116-117)
- `validate_skill_markdown_frontmatter` (lines 120-231)

The new module should look like:

```python
#!/usr/bin/env python3
"""Canonical skill frontmatter validation helpers."""

from __future__ import annotations

import os
from pathlib import Path

import yaml
from yaml.nodes import MappingNode, ScalarNode, SequenceNode


ROOT = Path(__file__).resolve().parents[1]
PROJECTED_SKILL_METADATA_REQUIRED_NAMES = {"using-superpowers"}


def _as_windows_long_path(path: Path) -> str:
    resolved = path.resolve(strict=False)
    text = str(resolved)
    if os.name != "nt" or text.startswith("\\\\?\\"):
        return text
    if text.startswith("\\\\"):
        return "\\\\?\\UNC\\" + text[2:]
    return "\\\\?\\" + text


def _projected_skill_requires_metadata(skill_root: Path) -> bool:
    return skill_root.name in PROJECTED_SKILL_METADATA_REQUIRED_NAMES


def validate_skill_markdown_frontmatter(skill_root: Path) -> None:
    skill_md = skill_root / "SKILL.md"
    if not skill_md.is_file():
        raise FileNotFoundError(skill_md)

    raw = Path(_as_windows_long_path(skill_md)).read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        raise ValueError(f"{skill_md} begins with a UTF-8 BOM")

    text = raw.decode("utf-8")
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        raise ValueError(f"{skill_md} must start with a standalone YAML frontmatter delimiter")

    end_index = None
    for index, line in enumerate(lines[1:], start=1):
        if line == "---":
            end_index = index
            break
    if end_index is None:
        raise ValueError(f"{skill_md} is missing a closing YAML frontmatter delimiter")

    frontmatter_text = "\n".join(lines[1:end_index])
    parsed_frontmatter = yaml.safe_load(frontmatter_text)
    if not isinstance(parsed_frontmatter, dict):
        raise ValueError(f"{skill_md} frontmatter must be a mapping")

    frontmatter_node = yaml.compose(frontmatter_text, Loader=yaml.SafeLoader)
    if not isinstance(frontmatter_node, MappingNode):
        raise ValueError(f"{skill_md} frontmatter must be a mapping")

    def ensure_unique_keys(node: MappingNode | SequenceNode) -> None:
        if isinstance(node, MappingNode):
            seen_keys: set[str] = set()
            for key_node, value_node in node.value:
                if not isinstance(key_node, ScalarNode):
                    raise ValueError(f"{skill_md} frontmatter keys must be simple scalars")
                key = key_node.value
                if key in seen_keys:
                    raise ValueError(f"{skill_md} frontmatter contains duplicate key {key!r}")
                seen_keys.add(key)
                ensure_unique_keys(value_node)
            return
        if isinstance(node, SequenceNode):
            for child in node.value:
                ensure_unique_keys(child)

    ensure_unique_keys(frontmatter_node)

    name = parsed_frontmatter.get("name")
    description = parsed_frontmatter.get("description")
    if not isinstance(name, str) or not name.strip():
        raise ValueError(f"{skill_md} frontmatter must include nonblank name")
    if not isinstance(description, str) or not description.strip():
        raise ValueError(f"{skill_md} frontmatter must include nonblank description")
    metadata = parsed_frontmatter.get("metadata")
    if _projected_skill_requires_metadata(skill_root) and not isinstance(metadata, dict):
        raise ValueError(f"{skill_md} frontmatter metadata must be a mapping")
    if metadata is not None and not isinstance(metadata, dict):
        raise ValueError(f"{skill_md} frontmatter metadata must be a mapping when present")
    if isinstance(metadata, dict):
        def require_string(field_names: tuple[str, ...], *, allow_empty: bool = False) -> None:
            for field_name in field_names:
                if field_name not in metadata:
                    continue
                value = metadata.get(field_name)
                if not isinstance(value, str) or (not allow_empty and not value.strip()):
                    raise ValueError(
                        f"{skill_md} frontmatter metadata {field_name} must be a "
                        f"{'string' if allow_empty else 'nonblank string'}"
                    )

        require_string(
            (
                "source_category",
                "upstream_name",
                "upstream_version",
                "adaptation_overlay",
                "projection_plugin",
                "source-id",
                "source_path",
                "source-path",
                "provenance-name",
                "provenance_name",
                "origin",
                "content_mode",
                "source_author",
                "source_license",
                "source_repo",
                "adapted_author",
            )
        )
        if metadata.get("source_category") and metadata["source_category"] not in {"first_party", "third_party"}:
            raise ValueError(f"{skill_md} frontmatter metadata source_category must be first_party or third_party")
        if metadata.get("content_mode") and metadata["content_mode"] not in {"verbatim", "normalised", "adapted"}:
            raise ValueError(f"{skill_md} frontmatter metadata content_mode must be verbatim, normalised, or adapted")
        if metadata.get("source_category") == "third_party":
            for field_name in ("upstream_name", "upstream_version", "adaptation_overlay", "projection_plugin"):
                require_string((field_name,))
        if metadata.get("content_mode") == "adapted":
            require_string(("adapted_author",))
            if "source_author" not in metadata or "source_license" not in metadata:
                raise ValueError(
                    f"{skill_md} frontmatter metadata adapted projections must declare source_author and source_license"
                )
            require_string(("source_author", "source_license"))
        elif metadata.get("content_mode") == "normalised":
            if metadata.get("adapted_author") or metadata.get("adaptation_note"):
                raise ValueError(
                    f"{skill_md} frontmatter metadata normalised projections must not declare adapted_author or adaptation_note"
                )
```

**Step 2: Update `tools/install_agent_skills.py`**

old_string:
```python
from skill_zip_artifacts import validate_skill_markdown_frontmatter
```

new_string:
```python
from skill_validation import validate_skill_markdown_frontmatter
```

**Verification:**

```text
py -3 -c "from skill_validation import validate_skill_markdown_frontmatter; print('OK')"
py -3 -c "from install_agent_skills import validate_skill_markdown_frontmatter; print('OK')"
```

**Commit message:** `refactor: move validate_skill_markdown_frontmatter to tools/skill_validation.py`

## Task 2: Create `tools/project_skills.py`

**Files:**
- Add `tools/project_skills.py`

**Expected interim state:** The new `project_skills` module imports cleanly, but `tools/project_skills.py --check` will not yet pass because other tooling and generated surfaces are still stale. That is expected until Task 8.

**Step 1: Add `tools/project_skills.py`**

```python
#!/usr/bin/env python3
"""Project marketplace skills into Codex plugin trees and flat skill zips."""

from __future__ import annotations

import argparse
import os
import shutil
import zipfile
from pathlib import Path
from typing import Any, Iterable

from marketplace_utils import ROOT, load_json, load_plugin_root_inventory
from skill_overlay_materializer import stage_overlay_tree
from tree_canonicalization import compare_trees_canonicalized


GENERATED_SKILL_ZIPS_ROOT = ROOT / "generated/skill-zips"

VALID_SOURCE_CATEGORIES = {"first_party", "third_party"}
VALID_CONTENT_MODES = {"verbatim", "normalised", "adapted"}
SKIP_CONTENT_MODES = {"blocked", "skipped"}
SKIP_STATUSES = {"skipped", "blocked", "out_of_scope"}

# Deterministic packaging constants copied from tools/skill_zip_artifacts.py
SKIP_DIR_NAMES = {
    ".git",
    ".hg",
    ".svn",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".cache",
    "node_modules",
    "dist",
    "build",
    "coverage",
    "tmp",
    "temp",
    "generated",
    "logs",
    "worker-output",
}
FORBIDDEN_FILE_NAMES = {
    "skill.zip",
    "package-evidence.json",
    "package-run-receipt.json",
}
TEXT_SUFFIXES = {
    ".md",
    ".txt",
    ".jsonl",
    ".yaml",
    ".yml",
    ".json",
    ".toml",
    ".py",
    ".sh",
    ".svg",
    ".xml",
    ".html",
    ".css",
    ".js",
    ".cjs",
    ".mjs",
    ".cts",
    ".mts",
    ".dot",
    ".upstream",
    ".ts",
    ".tsx",
}
TEXT_FILENAMES = {"SKILL.md", "openai.yaml"}
CANONICAL_ZIP_TIMESTAMP = (1980, 1, 1, 0, 0, 0)
CANONICAL_ZIP_PERMISSIONS = 0o644

def _as_windows_long_path(path: Path) -> str:
    resolved = path.resolve(strict=False)
    text = str(resolved)
    if os.name != "nt" or text.startswith("\\\\?\\"):
        return text
    if text.startswith("\\\\"):
        return "\\\\?\\UNC\\" + text[2:]
    return "\\\\?\\" + text


def _relative_path(path: Path, root: Path) -> str:
    path_text = _as_windows_long_path(path)
    root_text = _as_windows_long_path(root)
    if os.name == "nt":
        if not path_text.startswith("\\\\?\\"):
            path_text = "\\\\?\\" + path_text
        if not root_text.startswith("\\\\?\\"):
            root_text = "\\\\?\\" + root_text
        prefix = root_text + "\\"
        if path_text.startswith(prefix):
            return path_text[len(prefix) :].replace("\\", "/")
    try:
        return path.resolve(strict=False).relative_to(root.resolve(strict=False)).as_posix()
    except ValueError:
        return str(path).replace("\\", "/")


def _is_text_file(path: Path, raw: bytes | None = None) -> bool:
    return path.name in TEXT_FILENAMES or path.suffix.lower() in TEXT_SUFFIXES or (
        raw is not None and raw.startswith(b"#!")
    )


def _canonicalize_text_bytes(raw: bytes) -> bytes:
    return raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def _read_canonical_file_bytes(path: Path) -> bytes:
    raw = Path(_as_windows_long_path(path)).read_bytes()
    if _is_text_file(path, raw):
        raw.decode("utf-8")
        if raw.startswith(b"\xef\xbb\xbf"):
            raw = raw[3:]
        return _canonicalize_text_bytes(raw)
    return raw


def _zip_info_for_arcname(arcname: str) -> zipfile.ZipInfo:
    info = zipfile.ZipInfo(arcname, date_time=CANONICAL_ZIP_TIMESTAMP)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.create_system = 3
    info.external_attr = (0o100000 | CANONICAL_ZIP_PERMISSIONS) << 16
    return info


def _write_canonical_zip_tree(
    archive: zipfile.ZipFile,
    files: Iterable[Path],
    *,
    root: Path,
    archive_root_name: str,
) -> None:
    for file_path in files:
        rel = _relative_path(file_path, root)
        archive.writestr(_zip_info_for_arcname(f"{archive_root_name}/{rel}"), _read_canonical_file_bytes(file_path))


def _is_packaging_ignored(rel: Path) -> bool:
    if any(part.startswith(".") for part in rel.parts):
        return True
    if any(part in SKIP_DIR_NAMES for part in rel.parts):
        return True
    if rel.suffix.lower() == ".log":
        return True
    return False


def scan_skill_tree(skill_root: Path) -> tuple[list[Path], list[str]]:
    skill_root = skill_root.resolve()
    if not skill_root.exists():
        raise FileNotFoundError(skill_root)
    if not skill_root.is_dir():
        raise NotADirectoryError(skill_root)
    skill_root_str = _as_windows_long_path(skill_root)

    packaged_files: list[Path] = []
    forbidden_paths: list[str] = []
    for current, dirnames, filenames in os.walk(skill_root_str):
        current_path = Path(current)
        dirnames.sort()
        filenames.sort()
        for dirname in list(dirnames):
            candidate = current_path / dirname
            rel = Path(str(candidate)[len(skill_root_str) + 1 :])
            if candidate.is_symlink():
                forbidden_paths.append(rel.as_posix())

        for filename in filenames:
            candidate = current_path / filename
            rel = Path(str(candidate)[len(skill_root_str) + 1 :])
            if candidate.is_symlink():
                forbidden_paths.append(rel.as_posix())
                continue
            if rel.name in FORBIDDEN_FILE_NAMES:
                forbidden_paths.append(rel.as_posix())
                continue
            if _is_packaging_ignored(rel):
                continue
            packaged_files.append(candidate)

    packaged_files.sort(key=lambda path: str(path)[len(skill_root_str) + 1 :])
    forbidden_paths = sorted(dict.fromkeys(forbidden_paths))
    return packaged_files, forbidden_paths


def _load_bundle_manifest(plugin_root: Path) -> dict[str, Any] | None:
    """Load a projection-lane bundle manifest or return None for legacy/empty plugins."""
    manifest_path = plugin_root / "references" / "bundle-manifest.json"
    if not manifest_path.exists():
        return None
    manifest = load_json(manifest_path)
    if not isinstance(manifest, dict):
        raise ValueError(f"{manifest_path} must contain a JSON object")
    entries = manifest.get("entries")
    if not isinstance(entries, list):
        return None
    if entries:
        first = entries[0]
        if not isinstance(first, dict):
            return None
        if "canonical_name" not in first or "canonical_source_path" not in first:
            return None
        csp = first.get("canonical_source_path", "")
        if isinstance(csp, str) and Path(csp).suffix:
            return None
    return manifest


def _validate_entry(entry: dict[str, Any]) -> bool:
    """Validate a bundle entry and return True if it should be projected."""
    canonical_name = entry.get("canonical_name")
    if not isinstance(canonical_name, str) or not canonical_name:
        raise ValueError(f"entry missing canonical_name: {entry}")
    source_category = entry.get("source_category")
    if source_category not in VALID_SOURCE_CATEGORIES:
        raise ValueError(f"entry {canonical_name} invalid source_category: {source_category}")
    import_status = entry.get("import_status")
    content_mode = entry.get("content_mode")
    if import_status in SKIP_STATUSES or content_mode in SKIP_CONTENT_MODES:
        return False
    if content_mode not in VALID_CONTENT_MODES:
        raise ValueError(f"entry {canonical_name} invalid content_mode: {content_mode}")
    for field in ("canonical_source_path", "local_path"):
        if not isinstance(entry.get(field), str) or not entry[field]:
            raise ValueError(f"entry {canonical_name} missing {field}")
    overlay_path = entry.get("adaptation_overlay_path")
    if source_category == "first_party":
        if content_mode != "verbatim":
            raise ValueError(f"first-party entry {canonical_name} must be verbatim")
        if overlay_path is not None:
            raise ValueError(f"first-party entry {canonical_name} must not declare adaptation_overlay_path")
    else:
        if content_mode == "verbatim":
            if overlay_path is not None:
                raise ValueError(f"verbatim entry {canonical_name} must not declare adaptation_overlay_path")
        else:
            if not isinstance(overlay_path, str) or not overlay_path:
                raise ValueError(f"third-party {content_mode} entry {canonical_name} requires adaptation_overlay_path")
    return True


def _collect_skill_groups(*, plugin_name: str | None = None) -> dict[str, list[dict[str, Any]]]:
    """Group active bundle entries by canonical_name across all enabled plugin roots."""
    groups: dict[str, list[dict[str, Any]]] = {}
    for spec in load_plugin_root_inventory():
        if not spec.get("enabled", True):
            continue
        if plugin_name and spec["name"] != plugin_name:
            continue
        plugin_root = ROOT / spec["plugin_root"]
        manifest = _load_bundle_manifest(plugin_root)
        if manifest is None:
            continue
        for entry in manifest.get("entries", []):
            if not isinstance(entry, dict):
                continue
            if not _validate_entry(entry):
                continue
            canonical_name = entry["canonical_name"]
            enriched = {
                **entry,
                "plugin_root": spec["plugin_root"],
                "pack_name": spec["name"],
            }
            groups.setdefault(canonical_name, []).append(enriched)

    for canonical_name, entries in groups.items():
        reference = (entries[0]["canonical_source_path"], entries[0].get("adaptation_overlay_path"))
        for entry in entries[1:]:
            candidate = (entry["canonical_source_path"], entry.get("adaptation_overlay_path"))
            if candidate != reference:
                conflicting = [
                    f"{e['pack_name']}: source={e['canonical_source_path']}, overlay={e.get('adaptation_overlay_path')}"
                    for e in entries
                ]
                raise ValueError(
                    f"cross-pack conflict for {canonical_name}: diverging canonical_source_path or adaptation_overlay_path; "
                    f"packs: {conflicting}"
                )
    return groups


def _expected_plugin_roots(groups: dict[str, list[dict[str, Any]]]) -> dict[str, set[str]]:
    """Map plugin_root -> set of expected skill directory names."""
    expected: dict[str, set[str]] = {}
    for entries in groups.values():
        for entry in entries:
            local_path = entry["local_path"]
            parts = Path(local_path).parts
            if len(parts) >= 2 and parts[0] == "skills":
                expected.setdefault(entry["plugin_root"], set()).add(parts[1])
    return expected


def _copy_staged_tree(staged_root: Path, destination_root: Path) -> None:
    """Replace a plugin skill tree with the freshly staged tree."""
    if destination_root.exists():
        shutil.rmtree(_as_windows_long_path(destination_root))
    destination_root.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(_as_windows_long_path(staged_root), _as_windows_long_path(destination_root))


def _write_skill_zip(canonical_name: str, staged_root: Path, packaged_files: list[Path]) -> None:
    """Atomically write a deterministic flat skill zip."""
    GENERATED_SKILL_ZIPS_ROOT.mkdir(parents=True, exist_ok=True)
    zip_path = GENERATED_SKILL_ZIPS_ROOT / f"{canonical_name}.zip"
    tmp_path = zip_path.parent / f".{zip_path.name}.{os.getpid()}.tmp"
    try:
        with zipfile.ZipFile(tmp_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            _write_canonical_zip_tree(
                archive,
                packaged_files,
                root=staged_root,
                archive_root_name=canonical_name,
            )
        os.replace(str(_as_windows_long_path(tmp_path)), str(_as_windows_long_path(zip_path)))
    except Exception:
        if tmp_path.exists():
            tmp_path.unlink()
        raise


def _check_skill_zip(canonical_name: str, staged_root: Path, packaged_files: list[Path]) -> None:
    """Validate an existing flat skill zip matches the staged tree."""
    zip_path = GENERATED_SKILL_ZIPS_ROOT / f"{canonical_name}.zip"
    if not zip_path.exists():
        raise FileNotFoundError(f"expected zip missing: {zip_path}")
    with zipfile.ZipFile(zip_path) as archive:
        bad = archive.testzip()
        if bad:
            raise ValueError(f"{zip_path} zip integrity failure at {bad}")
        names = sorted(name for name in archive.namelist() if not name.endswith("/"))
        roots = sorted({name.split("/", 1)[0] for name in names})
        if len(roots) != 1 or roots[0] != canonical_name:
            raise ValueError(f"{zip_path} must contain exactly one top-level folder named {canonical_name}")
        if f"{canonical_name}/SKILL.md" not in names:
            raise ValueError(f"{zip_path} missing {canonical_name}/SKILL.md")
        expected_names = sorted(f"{canonical_name}/{_relative_path(path, staged_root)}" for path in packaged_files)
        if names != expected_names:
            raise ValueError(f"{zip_path} namelist mismatch: expected {expected_names}, got {names}")


def _cleanup_generated_skill_zips(expected_names: set[str]) -> None:
    """Remove stale root-level zips and any leftover per-pack subdirectories or registry files."""
    if not GENERATED_SKILL_ZIPS_ROOT.exists():
        return
    for path in sorted(GENERATED_SKILL_ZIPS_ROOT.rglob("*"), key=lambda p: len(p.parts), reverse=True):
        if path.is_dir():
            if path.resolve() == GENERATED_SKILL_ZIPS_ROOT.resolve():
                continue
            try:
                next(path.iterdir())
            except StopIteration:
                path.rmdir()
            continue
        if path.name in expected_names and path.parent == GENERATED_SKILL_ZIPS_ROOT:
            continue
        path.unlink()
        print(f"Pruned stale generated zip {path.relative_to(ROOT)}")


def _validate_generated_skill_zips(expected_names: set[str]) -> None:
    """Fail if any unexpected files linger under generated/skill-zips/."""
    if not GENERATED_SKILL_ZIPS_ROOT.is_dir():
        raise FileNotFoundError(GENERATED_SKILL_ZIPS_ROOT)
    missing = sorted(name for name in expected_names if not (GENERATED_SKILL_ZIPS_ROOT / name).is_file())
    extra = [
        str(path.relative_to(ROOT))
        for path in GENERATED_SKILL_ZIPS_ROOT.rglob("*")
        if path.is_file() and (path.name not in expected_names or path.parent != GENERATED_SKILL_ZIPS_ROOT)
    ]
    if missing or extra:
        raise ValueError(f"generated skill zips mismatch: missing {missing}, extra {extra}")


def project_skills(*, write: bool = True, plugin_name: str | None = None) -> None:
    """Project every active skill into plugin trees and flat skill zips."""
    groups = _collect_skill_groups(plugin_name=plugin_name)
    expected_zip_names = {f"{name}.zip" for name in groups}

    for canonical_name, entries in sorted(groups.items()):
        source_path = entries[0]["canonical_source_path"]
        overlay_path = entries[0].get("adaptation_overlay_path")
        source_root = ROOT / source_path
        overlay_root = ROOT / overlay_path if overlay_path else None

        if not source_root.is_dir():
            raise ValueError(f"entry {canonical_name} canonical_source_path must be a directory: {source_root}")

        staged_root, tempdir = stage_overlay_tree(source_root, overlay_root)
        try:
            packaged_files, forbidden_paths = scan_skill_tree(staged_root)
            if forbidden_paths:
                raise ValueError(f"{canonical_name} staged tree contains forbidden paths: {forbidden_paths}")

            if write:
                for entry in entries:
                    destination_root = ROOT / entry["plugin_root"] / entry["local_path"]
                    _copy_staged_tree(staged_root, destination_root)
                _write_skill_zip(canonical_name, staged_root, packaged_files)
            else:
                for entry in entries:
                    destination_root = ROOT / entry["plugin_root"] / entry["local_path"]
                    if not destination_root.exists():
                        raise FileNotFoundError(f"projection missing for {canonical_name} in {entry['pack_name']}: {destination_root}")
                    compare_trees_canonicalized(staged_root, destination_root)
                _check_skill_zip(canonical_name, staged_root, packaged_files)
        finally:
            tempdir.cleanup()

    expected_roots = _expected_plugin_roots(groups)
    for spec in load_plugin_root_inventory():
        if not spec.get("enabled", True):
            continue
        plugin_root = spec["plugin_root"]
        skills_root = ROOT / plugin_root / "skills"
        if not skills_root.is_dir():
            continue
        roots = expected_roots.get(plugin_root, set())
        for child in sorted(skills_root.iterdir()):
            if not child.is_dir():
                continue
            if child.name in roots:
                continue
            if write:
                shutil.rmtree(_as_windows_long_path(child))
                print(f"Pruned stale projected skill root {child.relative_to(ROOT)}")
            else:
                raise ValueError(f"{plugin_root} has stale projected skill roots: {child.name}")

    if write:
        _cleanup_generated_skill_zips(expected_zip_names)
        print(f"OK project skills: materialized {len(groups)} unique skills")
    else:
        _validate_generated_skill_zips(expected_zip_names)
        print(f"OK project skills: validated {len(groups)} unique skills and zips")


def expected_skill_names(*, plugin_name: str | None = None) -> set[str]:
    """Return the set of canonical skill names that should produce flat zips."""
    return set(_collect_skill_groups(plugin_name=plugin_name).keys())


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Project skills into plugin trees and flat skill zips")
    parser.add_argument("--check", action="store_true", help="validate without writing")
    parser.add_argument("--plugin", help="target one plugin by name")
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    project_skills(write=not args.check, plugin_name=args.plugin)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

**Verification:**

```text
py -3 -c "from project_skills import project_skills; print('OK')"
```

**Commit message:** `feat: add tools/project_skills.py for flat skill zip projection`

## Task 3: Refactor `tools/update_skill_artifacts.py`

**Files:**
- Rewrite `tools/update_skill_artifacts.py`

**Expected interim state:** `update_skill_artifacts.py --check` now calls the new four-function pipeline. It may still fail on stale `SOURCE.md` blocks or repo-index validation until Task 4.

**Step 1: Rewrite `tools/update_skill_artifacts.py`**

```python
#!/usr/bin/env python3
"""Worker-facing entrypoint for deterministic skill artifact updates.

This script orchestrates the core skill artifact pipeline:
generate mega-packs, generate pack manifests, project skills into plugin
trees and flat skill zips, and refresh the first-party skill catalog.

Use `tools/rebuild_marketplace.py` for the canonical full regeneration and
validation gate. The partial update modes in this script are repair-oriented
fallbacks.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from generate_mega_packs import generate_all_mega_packs
from generate_pack_manifests import generate as generate_pack_manifests
from generate_first_party_skill_catalog import generate as generate_first_party_skill_catalog
from project_skills import project_skills


def _selected_pack(args: argparse.Namespace) -> str | None:
    if args.pack:
        return args.pack
    if args.skill:
        return args.skill.split("/", 1)[0]
    return None


def _run_tool(script_name: str, *args: str) -> None:
    """Run a sibling generator script with the current Python interpreter."""
    script_path = Path(__file__).resolve().with_name(script_name)
    subprocess.run([sys.executable, str(script_path), *args], check=True)


def _run_full_regeneration_checks() -> None:
    """Run the repo-wide generated-surface checks for a full refresh."""
    _run_tool("generate_marketplace.py", "--check")
    _run_tool("generate_repo_index.py", "--check")
    generate_pack_manifests(write=False)
    generate_all_mega_packs(write=False)
    project_skills(write=False)
    _run_tool("generate_provenance_maps.py", "--check")
    _run_tool("generate_source_maps.py", "--check")
    generate_first_party_skill_catalog(write=False)


def _run_full_regeneration_writes() -> None:
    """Run every deterministic writer that participates in a full regen."""
    _run_tool("generate_marketplace.py")
    _run_tool("generate_repo_index.py")
    generate_pack_manifests(write=True)
    generate_all_mega_packs(write=True)
    project_skills(write=True)
    _run_tool("generate_provenance_maps.py")
    _run_tool("generate_source_maps.py")
    generate_first_party_skill_catalog(write=True)


def _run_targeted_writes(selected_pack: str) -> None:
    """Deprecated alias that runs the full skill artifact pipeline."""
    _ = selected_pack  # kept for CLI compatibility
    _run_full_regeneration_writes()


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Update or validate canonical skill artifacts")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--skill", help="deprecated alias that runs the full pipeline; ignored")
    group.add_argument("--pack", help="deprecated alias that runs the full pipeline; ignored")
    group.add_argument("--all", action="store_true", help="regenerate every installable skill")
    parser.add_argument("--check", action="store_true", help="validate current generated artifacts without writing")
    args = parser.parse_args()

    update_selected = any((args.skill, args.pack, args.all))
    if args.check and update_selected:
        parser.error("--check cannot be combined with update flags")
    if not args.check and not update_selected:
        parser.error("choose one of --skill, --pack, --all, or use --check")
    return args


def main() -> int:
    args = _parse_args()
    selected_pack = _selected_pack(args)

    if args.check:
        _run_full_regeneration_checks()
        return 0

    if args.all:
        _run_full_regeneration_writes()
    else:
        assert selected_pack is not None
        _run_targeted_writes(selected_pack)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

**Verification:**

```text
py -3 -c "from update_skill_artifacts import main; print('OK')"
py -3 tools/update_skill_artifacts.py --check
```

The `--check` run is expected to fail at this point because Task 4 surfaces are still stale.

**Commit message:** `refactor: update_skill_artifacts orchestrates flat skill zip pipeline`

## Task 4: Update generated-surface generators and repo-index metadata

**Files:**
- Modify `tools/generate_pack_manifests.py:186-190`
- Modify `tools/generate_first_party_skill_catalog.py:15-36` and `_discover_generated_refs`
- Modify `tools/generate_repo_index.py:24-35` and `build_repo_index`
- Modify `tools/validate_repo_index.py:122-125`

**Expected interim state:** Pack `SOURCE.md` blocks, first-party catalog generated refs, and repo-index validation metadata now point to the new flat zip layout. `generated/skill-zips/` contents are still old until Task 8 runs a full regeneration.

**Step 1: Update `tools/generate_pack_manifests.py` SOURCE.md block**

old_string:
```python
        lines.extend(["", "## Generated install units"])
        lines.extend(
            f"- `generated/skill-zips/{pack['bundle_name']}/{entry['canonical_name']}/skill.zip`"
            for entry in entries
        )
```

new_string:
```python
        lines.extend(["", "## Generated install units"])
        lines.extend(
            f"- `generated/skill-zips/{entry['canonical_name']}.zip`"
            for entry in entries
        )
```

**Step 2: Update `tools/generate_first_party_skill_catalog.py`**

old_string:
```python
GENERATED_REGISTRY_PATH = ROOT / "generated/skill-zips/registry.json"
```

new_string:
```python
GENERATED_SKILL_ZIPS_ROOT = ROOT / "generated/skill-zips"
```

old_string:
```python
REFERENCE_SURFACES = (
    ROOT / "sources/first_party/skills/house-skills/intake.json",
    ROOT / "codex-marketplace/plugins/repo-worker-pack/README.md",
    ROOT / "codex-marketplace/plugins/repo-worker-pack/SOURCE.md",
    ROOT / "codex-marketplace/plugins/repo-worker-pack/PROJECTION.md",
    ROOT / "codex-marketplace/plugins/repo-worker-pack/references/source-map.md",
    ROOT / "codex-marketplace/plugins/repo-worker-pack/references/provenance-map.json",
    ROOT / "codex-marketplace/plugins/house-skills/README.md",
    ROOT / "codex-marketplace/plugins/house-skills/SOURCE.md",
    ROOT / "codex-marketplace/plugins/house-skills/PROJECTION.md",
    ROOT / "codex-marketplace/plugins/house-skills/references/source-map.md",
    ROOT / "codex-marketplace/plugins/house-skills/references/provenance-map.json",
    ROOT / "provenance/repo-worker-pack.md",
    ROOT / "provenance/house-skills.md",
    ROOT / "repo-index/repo-index.json",
    GENERATED_REGISTRY_PATH,
)
```

new_string:
```python
REFERENCE_SURFACES = (
    ROOT / "sources/first_party/skills/house-skills/intake.json",
    ROOT / "codex-marketplace/plugins/repo-worker-pack/README.md",
    ROOT / "codex-marketplace/plugins/repo-worker-pack/SOURCE.md",
    ROOT / "codex-marketplace/plugins/repo-worker-pack/PROJECTION.md",
    ROOT / "codex-marketplace/plugins/repo-worker-pack/references/source-map.md",
    ROOT / "codex-marketplace/plugins/repo-worker-pack/references/provenance-map.json",
    ROOT / "codex-marketplace/plugins/house-skills/README.md",
    ROOT / "codex-marketplace/plugins/house-skills/SOURCE.md",
    ROOT / "codex-marketplace/plugins/house-skills/PROJECTION.md",
    ROOT / "codex-marketplace/plugins/house-skills/references/source-map.md",
    ROOT / "codex-marketplace/plugins/house-skills/references/provenance-map.json",
    ROOT / "provenance/repo-worker-pack.md",
    ROOT / "provenance/house-skills.md",
    ROOT / "repo-index/repo-index.json",
)
```

old_string:
```python
def _discover_generated_refs(skill_name: str, projected_in: tuple[str, ...]) -> tuple[str, ...]:
    refs: set[str] = set()
    if GENERATED_REGISTRY_PATH.exists():
        registry = load_json(GENERATED_REGISTRY_PATH)
        for artifact in registry.get("artifacts", []):
            if not isinstance(artifact, dict):
                continue
            if artifact.get("skill") == skill_name:
                zip_path = artifact.get("zip_path")
                if isinstance(zip_path, str) and zip_path:
                    refs.add(zip_path)
        if refs:
            refs.add("generated/skill-zips/registry.json")

    for plugin_root in projected_in:
        refs.add(f"{plugin_root}/references/bundle-manifest.json")
        refs.add(f"{plugin_root}/references/source-map.md")
        refs.add(f"{plugin_root}/references/provenance-map.json")
    return tuple(sorted(refs))
```

new_string:
```python
def _discover_generated_refs(skill_name: str, projected_in: tuple[str, ...]) -> tuple[str, ...]:
    refs: set[str] = set()
    zip_path = GENERATED_SKILL_ZIPS_ROOT / f"{skill_name}.zip"
    if zip_path.exists():
        refs.add(zip_path.relative_to(ROOT).as_posix())

    for plugin_root in projected_in:
        refs.add(f"{plugin_root}/references/bundle-manifest.json")
        refs.add(f"{plugin_root}/references/source-map.md")
        refs.add(f"{plugin_root}/references/provenance-map.json")
    return tuple(sorted(refs))
```

**Step 3: Update `tools/generate_repo_index.py`**

old_string (DEFAULT_REPO_INDEX validation block):
```python
    "validation": {
        "marketplace": "py -3 tools/validate_marketplace.py",
        "repo_index": "py -3 tools/validate_repo_index.py",
        "skill_zips_update": "py -3 tools/update_skill_artifacts.py --skill <pack>/<skill>",
        "skill_zips_full_regeneration": "py -3 tools/update_skill_artifacts.py --all",
        "skill_zips_check": "py -3 tools/validate_skill_zips.py",
        "generated_drift": "py -3 tools/validate_generated_drift.py --base origin/main",
        "repo_index_generate": "py -3 tools/generate_repo_index.py",
        "marketplace_generate": "py -3 tools/generate_marketplace.py",
        "marketplace_check": "py -3 tools/generate_marketplace.py --check",
        "repo_index_check": "py -3 tools/generate_repo_index.py --check",
    },
```

new_string:
```python
    "validation": {
        "marketplace": "py -3 tools/validate_marketplace.py",
        "repo_index": "py -3 tools/validate_repo_index.py",
        "skill_zips_update": "py -3 tools/update_skill_artifacts.py --skill <pack>/<skill>",
        "skill_zips_full_regeneration": "py -3 tools/update_skill_artifacts.py --all",
        "skill_zips_check": "py -3 tools/validate_skill_zips.py",
        "repo_index_generate": "py -3 tools/generate_repo_index.py",
        "marketplace_generate": "py -3 tools/generate_marketplace.py",
        "marketplace_check": "py -3 tools/generate_marketplace.py --check",
        "repo_index_check": "py -3 tools/generate_repo_index.py --check",
    },
```

old_string (superpowers-plus-marketplace zone):
```python
        {
            "name": "superpowers-plus-marketplace",
            "path": "codex-marketplace/plugins/superpowers-plus",
            "purpose": "Codex-facing projection of the upstream Superpowers release snapshot, renamed to Superpowers+.",
            "surface_kind": "runtime-facing",
            "nearest_scoped_agents_md": "codex-marketplace/plugins/AGENTS.md",
            "key_validation_scripts": [
                "tools/validate_marketplace.py",
                "tools/validate_repo_index.py",
                "tools/package_skill_zips.py",
            ],
        },
```

new_string:
```python
        {
            "name": "superpowers-plus-marketplace",
            "path": "codex-marketplace/plugins/superpowers-plus",
            "purpose": "Codex-facing projection of the upstream Superpowers release snapshot, renamed to Superpowers+.",
            "surface_kind": "runtime-facing",
            "nearest_scoped_agents_md": "codex-marketplace/plugins/AGENTS.md",
            "key_validation_scripts": [
                "tools/validate_marketplace.py",
                "tools/validate_repo_index.py",
                "tools/project_skills.py",
            ],
        },
```

In `build_repo_index`, after `validation = dict(repo_index.get("validation", {}))` and the four marketplace/repo_index assignments, add:

```python
    validation["skill_zips_check"] = "py -3 tools/validate_skill_zips.py"
    validation.pop("generated_drift", None)
```

Add the following loop just before `repo_index["validation"] = validation` to normalize stale key_validation_scripts entries:

```python
    for zone in repo_index.get("zones", []):
        scripts = zone.get("key_validation_scripts", [])
        if "tools/package_skill_zips.py" in scripts:
            zone["key_validation_scripts"] = [
                "tools/project_skills.py" if s == "tools/package_skill_zips.py" else s
                for s in scripts
            ]
```

**Step 4: Update `tools/validate_repo_index.py`**

old_string:
```python
    if validation.get("skill_zips_check") != "py -3 tools/validate_skill_zips.py":
        raise ValueError("repo-index skill_zips_check command mismatch")
    if validation.get("generated_drift") != "py -3 tools/validate_generated_drift.py --base origin/main":
        raise ValueError("repo-index generated_drift command mismatch")
```

new_string:
```python
    if validation.get("skill_zips_check") != "py -3 tools/validate_skill_zips.py":
        raise ValueError("repo-index skill_zips_check command mismatch")
    if "generated_drift" in validation:
        raise ValueError("repo-index validation block contains obsolete generated_drift command")
```

**Verification:**

```text
py -3 tools/generate_pack_manifests.py --check
py -3 tools/validate_repo_index.py
```

Both are expected to fail until Task 8 regenerates the checked-in files.

**Commit message:** `refactor: point generated-surface metadata at flat skill zips`

## Task 5: Update marketplace validators and entrypoints

**Files:**
- Modify `tools/validate_marketplace.py:16-55`, `92-93`, `1432-1500`, `1503-1527`, `1417-1428`
- Rewrite `tools/validate_skill_zips.py`
- Modify `tools/rebuild_marketplace.py:93-108`
- Modify `tools/check_marketplace.py:23-37`

**Expected interim state:** `validate_marketplace.py` no longer references `skill_zip_artifacts`; `validate_skill_zips.py` wraps `project_skills --check`; `rebuild_marketplace.py` and `check_marketplace.py` use the simplified `update_skill_artifacts` CLI.

**Step 1: Update `tools/validate_marketplace.py`**

Add imports after the existing top imports:

```python
import project_skills
from skill_validation import validate_skill_markdown_frontmatter
```

old_string (`_bootstrap_marketplace_dependencies`):
```python
    globals()["validate_repo_index"] = importlib.import_module("validate_repo_index").validate_repo_index
    skill_zip_artifacts = importlib.import_module("skill_zip_artifacts")
    globals()["validate_skill_markdown_frontmatter"] = skill_zip_artifacts.validate_skill_markdown_frontmatter
    globals()["validate_skill_zip_registry"] = skill_zip_artifacts.validate_skill_zip_registry
    globals()["load_registry"] = skill_zip_artifacts.load_registry
    globals()["SKILL_ZIP_ROOT"] = skill_zip_artifacts.ROOT
```

new_string:
```python
    globals()["validate_repo_index"] = importlib.import_module("validate_repo_index").validate_repo_index
```

old_string:
```python
def validate_projection_materializer() -> None:
    _run_tool_check([sys.executable, "tools/materialize_projection.py", "--check"], "projection materializer check")
```

new_string:
```python
def validate_projection_materializer() -> None:
    _run_tool_check([sys.executable, "tools/project_skills.py", "--check"], "project skills check")
```

old_string (`_parse_args` help):
```python
            "Skip freshness checks already covered by an upstream step "
            "(generate_plugin_root_inventory --check, projection materializer, "
            "pack manifests, and skill zip registry). Metadata validation "
            "(validate_repo_index) still runs."
```

new_string:
```python
            "Skip freshness checks already covered by an upstream step "
            "(generate_plugin_root_inventory --check, project_skills.py --check, "
            "and pack manifests). Metadata validation (validate_repo_index) still runs."
```

old_string (`main` freshness block):
```python
    if not args.skip_freshness_checks:
        validate_skill_zip_registry()
        validate_projection_materializer()
        validate_pack_manifests()
```

new_string:
```python
    if not args.skip_freshness_checks:
        validate_projection_materializer()
        validate_pack_manifests()
```

old_string (`validate_skill_zip_assertions`):
```python
def validate_skill_zip_assertions() -> None:
    """Assert skill-zip registry invariants that are not covered elsewhere.

    These three checks previously lived in the standalone
    ``validate_skill_zips.py`` step. They are cheap metadata assertions
    (no zip materialization), so they run regardless of
    ``--skip-freshness-checks``.
    """
    import zipfile

    registry = load_registry()

    # finishing-a-development-branch must be a direct (verbatim) export.
    verbatim = next(
        (
            record
            for record in registry["artifacts"]
            if record["pack"] == "superpowers-plus" and record["skill"] == "finishing-a-development-branch"
        ),
        None,
    )
    if verbatim is None:
        raise ValueError("expected finishing-a-development-branch artifact in registry but found none")
    if verbatim["export_mode"] != "direct":
        raise AssertionError("expected finishing-a-development-branch to be a direct export")
    if verbatim.get("overlay_path") is not None:
        raise AssertionError("expected finishing-a-development-branch to have a null overlay path")
    with zipfile.ZipFile(SKILL_ZIP_ROOT / verbatim["zip_path"]) as archive:
        skill_md = archive.read("finishing-a-development-branch/SKILL.md").decode("utf-8")
    if "Use when implementation is complete, all tests pass, and you need to decide how to integrate the work - guides completion of development work by presenting structured options for merge, PR, or cleanup" not in skill_md:
        raise AssertionError("direct skill zip does not contain the retained upstream guidance")
    if "Codex Marketplace Note" in skill_md:
        raise AssertionError("direct skill zip still contains raw Codex-specific guidance")

    # dispatching-parallel-agents must be excluded.
    excluded = next(
        (
            record
            for record in registry["excluded"]
            if record["pack"] == "superpowers-plus" and record["skill"] == "dispatching-parallel-agents"
        ),
        None,
    )
    if excluded is None:
        raise ValueError("expected dispatching-parallel-agents excluded record in registry but found none")
    if excluded["export_mode"] != "excluded":
        raise AssertionError("expected dispatching-parallel-agents to be excluded")
    if "subagents" not in excluded["reason"]:
        raise AssertionError("excluded skill should explain the subagent limitation")

    # worker-verification must export as an installable zip and must not be
    # re-added to wild-bunch-project-pack.
    worker_verification = next(
        (
            record
            for record in registry["artifacts"]
            if record["pack"] == "house-skills" and record["skill"] == "worker-verification"
        ),
        None,
    )
    if worker_verification is None:
        raise ValueError("expected house-skills/worker-verification artifact in registry but found none")
    if worker_verification["export_mode"] not in {"direct", "overlay"}:
        raise AssertionError("house-skills/worker-verification should export as an installable zip")
    if any(
        record["skill"] == "worker-verification" and record["pack"] == "wild-bunch-project-pack"
        for record in registry["artifacts"]
    ):
        raise AssertionError("worker-verification must not be re-added to wild-bunch-project-pack")
```

new_string:
```python
def validate_skill_zip_assertions() -> None:
    """Assert flat skill-zip invariants that are not covered elsewhere.

    These checks previously lived in the standalone ``validate_skill_zips.py``
    step. They are cheap metadata assertions (no zip materialization), so they
    run regardless of ``--skip-freshness-checks``.
    """
    import zipfile

    groups = project_skills._collect_skill_groups()
    if "finishing-a-development-branch" not in groups:
        raise AssertionError("expected finishing-a-development-branch projection")

    worker_packs = {entry["pack_name"] for entry in groups.get("worker-verification", [])}
    if "wild-bunch-project-pack" in worker_packs:
        raise AssertionError("worker-verification must not be re-added to wild-bunch-project-pack")

    finishing = project_skills.GENERATED_SKILL_ZIPS_ROOT / "finishing-a-development-branch.zip"
    if not finishing.exists():
        raise FileNotFoundError(f"expected flat zip: {finishing}")
    with zipfile.ZipFile(finishing) as archive:
        skill_md = archive.read("finishing-a-development-branch/SKILL.md").decode("utf-8")
    if "Use when implementation is complete, all tests pass, and you need to decide how to integrate the work - guides completion of development work by presenting structured options for merge, PR, or cleanup" not in skill_md:
        raise AssertionError("direct skill zip does not contain the retained upstream guidance")
    if "Codex Marketplace Note" in skill_md:
        raise AssertionError("direct skill zip still contains raw Codex-specific guidance")
```

**Step 2: Rewrite `tools/validate_skill_zips.py`**

```python
#!/usr/bin/env python3
"""Validate the canonical flat skill.zip surface."""

from __future__ import annotations

from project_skills import project_skills


def main() -> int:
    project_skills(write=False)
    print("OK skill-zips: all expected flat zips present and valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

**Step 3: Update `tools/rebuild_marketplace.py`**

old_string:
```python
def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the full marketplace rebuild and validation stack")
    parser.add_argument("--base", default="origin/main", help="git revision used for generated drift validation")
    return parser.parse_args()
```

new_string:
```python
def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the full marketplace rebuild and validation stack")
    return parser.parse_args()
```

old_string:
```python
    _run_tool("update_skill_artifacts.py", "--all", "--base", args.base)
```

new_string:
```python
    _run_tool("update_skill_artifacts.py", "--all")
```

**Step 4: Update `tools/check_marketplace.py`**

old_string:
```python
def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the non-mutating marketplace check stack")
    parser.add_argument("--base", default="origin/main", help="git revision used for generated drift validation")
    return parser.parse_args()
```

new_string:
```python
def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the non-mutating marketplace check stack")
    return parser.parse_args()
```

old_string:
```python
    _run_tool("update_skill_artifacts.py", "--check", "--full-regeneration", "--base", args.base, "--skip-zip-content-validation")
```

new_string:
```python
    _run_tool("update_skill_artifacts.py", "--check")
```

**Verification:**

```text
py -3 -c "from validate_marketplace import validate_projection_materializer, validate_skill_zip_assertions; print('OK')"
py -3 -c "from validate_skill_zips import main; print('OK')"
```

**Commit message:** `refactor: point validators and entrypoints at project_skills`

## Task 6: Delete obsolete files and update docs/AGENTS/README surfaces

**Files:**
- Delete `adapters/gpt/` recursively.
- Delete `tools/materialize_projection.py`, `tools/skill_zip_artifacts.py`, `tools/skill_gpt_exports.py`, `tools/export_skill_zips.py`, `tools/validate_export_skill_zips.py`, `tools/validate_generated_drift.py`, `tools/package_skill_zips.py`.
- Modify `tools/AGENTS.md:10-24`, `tools/AGENTS.md:103-115`
- Modify `codex-marketplace/AGENTS.md:21-24`, `codex-marketplace/AGENTS.md:96-103`
- Modify `codex-marketplace/plugins/AGENTS.md:21-23`
- Modify `docs/custody-and-projection-doctrine.md:106-116`, `123-146`, `171-175`, `184-200`
- Modify `docs/overlay-adapter-policy.md:31-65`
- Modify `.agents/docs/unslop/profile.md:14`
- Modify `README.md:18-31`
- Modify `codex-marketplace/README.md:34-47`
- Modify `repo-index/README.md:48-54`
- Modify `.agents/guides/marketplace-generation-guide.md:73`, `92`, `98`
- Modify `provenance/house-skills.md:25`
- Rewrite `tools/README.md`

**Expected interim state:** Obsolete tooling is gone. `tools/INDEX.md` and `adapters/INDEX.md` are stale until `generate_index_mesh.py` regenerates them in Task 8.

**Step 1: Delete obsolete files and directories**

```text
rm -rf adapters/gpt
del tools/materialize_projection.py tools/skill_zip_artifacts.py tools/skill_gpt_exports.py tools/export_skill_zips.py tools/validate_export_skill_zips.py tools/validate_generated_drift.py tools/package_skill_zips.py
```

On Windows, use:

```text
Remove-Item -Recurse -Force adapters\gpt
Remove-Item tools\materialize_projection.py, tools\skill_zip_artifacts.py, tools\skill_gpt_exports.py, tools\export_skill_zips.py, tools\validate_export_skill_zips.py, tools\validate_generated_drift.py, tools\package_skill_zips.py
```

**Step 2: Update `tools/AGENTS.md`**

old_string:
```markdown
The skill-update path is now worker-facing through
`py -3 tools/update_skill_artifacts.py --skill <pack>/<skill>`. The root
inventory that drives marketplace plugin ownership is
`codex-marketplace/plugin-roots.json`, GPT overlay sources live under
`adapters/gpt/`, and drift validation lives in
`tools/validate_generated_drift.py`.
The marketplace freshness proof is `py -3 tools/generate_marketplace.py --check`
for `.agents/plugins/marketplace.json` and
`codex-marketplace/manifest.json`, plus `py -3 tools/generate_repo_index.py
--check` for `repo-index/repo-index.json`. Projection-lane freshness is
proven by `py -3 tools/materialize_projection.py --check`, and the selected
pack bundle-manifest surfaces are proven by `py -3 tools/generate_pack_manifests.py
--check`.
```

new_string:
```markdown
The skill-update path is now worker-facing through
`py -3 tools/update_skill_artifacts.py --all` for a full regeneration. The
`--skill` and `--pack` flags remain as backwards-compatible aliases that also
run the full pipeline. The root inventory that drives marketplace plugin
ownership is `codex-marketplace/plugin-roots.json`.
The marketplace freshness proof is `py -3 tools/generate_marketplace.py --check`
for `.agents/plugins/marketplace.json` and
`codex-marketplace/manifest.json`, plus `py -3 tools/generate_repo_index.py
--check` for `repo-index/repo-index.json`. Projection-lane and flat skill-zip
freshness are proven by `py -3 tools/project_skills.py --check`, and the selected
pack bundle-manifest surfaces are proven by `py -3 tools/generate_pack_manifests.py
--check`.
```

old_string:
```markdown
- Flag GPT export manifests that allow raw Codex-specific assumptions to leak
  into generated skill zips instead of using an overlay or exclusion.
```

new_string:
```markdown
- Flag flat skill.zip artifacts that do not match the staged Codex projection
  or that contain stale adapter, gpt, or per-pack zip references.
```

**Step 3: Update `codex-marketplace/AGENTS.md`**

old_string:
```markdown
The marketplace plugin roots are the canonical install surface. Generated
`skill.zip` files under `generated/skill-zips/` are downstream GPT exports, and
`adapters/gpt/manifest.json` decides whether each one is `direct`, `overlay`,
or `excluded`.
```

new_string:
```markdown
The marketplace plugin roots are the canonical install surface. Generated
`skill.zip` files under `generated/skill-zips/` are downstream GPT-ready exports
produced as flat, deterministic archives named `generated/skill-zips/<skill>.zip`.
There is no per-pack subdirectory and no `registry.json`.
```

old_string:
```markdown
- Flag generated-export mismatches that would let the registry or bundle source
  drift silently from the tracked marketplace source tree or GPT overlay source.
- Flag any `skill.zip` found inside a source skill tree; canonical install
  archives belong only under `generated/skill-zips/` and must be written by the
  package tool, not by hand.
- Flag stale or unregistered canonical skill.zip artifacts under
  `generated/skill-zips/`, including missing overlay derivation metadata or
  excluded GPT-export records.
```

new_string:
```markdown
- Flag generated-export mismatches that would let the bundle source drift
  silently from the tracked marketplace source tree or Codex overlay source.
- Flag any `skill.zip` found inside a source skill tree; canonical install
  archives belong only under `generated/skill-zips/` as flat `<skill>.zip`
  files and must be written by `tools/project_skills.py`, not by hand.
- Flag stale or unregistered canonical skill.zip artifacts under
  `generated/skill-zips/`, including leftover per-pack subdirectories or
  `registry.json`.
```

**Step 4: Update `codex-marketplace/plugins/AGENTS.md`**

old_string:
```markdown
Treat these plugin roots as the canonical install surface. Generated
`skill.zip` artifacts are downstream GPT exports; `adapters/gpt/manifest.json`
controls whether a skill is exported direct, via overlay, or excluded.
Everything else in this tree is support custody or historical source material,
not part of the active marketplace inventory for the normalized root pass.
```

new_string:
```markdown
Treat these plugin roots as the canonical install surface. Generated
`skill.zip` artifacts are downstream flat GPT-ready exports named
`generated/skill-zips/<skill>.zip`. Everything else in this tree is support
custody or historical source material, not part of the active marketplace
inventory for the normalized root pass.
```

**Step 5: Update `docs/custody-and-projection-doctrine.md`**

old_string:
```markdown
2. **Projection** — `codex-marketplace/plugins/` vendored bundles, generated
   from custody plus manifest entries.
3. **Install / export** — `codex-marketplace/plugins/` is the canonical install
   surface; `generated/skill-zips/` is the derived GPT export corpus.
```

new_string:
```markdown
2. **Projection** — `codex-marketplace/plugins/` vendored bundles, generated
   from custody plus manifest entries.
3. **Install / export** — `codex-marketplace/plugins/` is the canonical install
   surface; `generated/skill-zips/<skill>.zip` is the derived flat GPT-ready
   export corpus with no per-pack subdirectories and no registry file.
```

old_string:
```markdown
4. **Add GPT decision** — record the GPT export lane decision (see below).
5. **Run one tool** — regenerate the projection with the designated tooling
   (e.g. `py -3 tools/update_skill_artifacts.py --skill <pack>/<skill>`).
6. **Regenerate proof surfaces** — run
   `py -3 tools/generate_provenance_maps.py` and
   `py -3 tools/generate_source_maps.py`.
7. **Validate** — run `py -3 tools/validate_marketplace.py` and
   `py -3 tools/materialize_projection.py --check` to confirm the projection
   matches custody and manifest.
```

new_string:
```markdown
4. **Run one tool** — regenerate the projection with the designated tooling
   (`py -3 tools/update_skill_artifacts.py --all`), which also refreshes the
   flat `generated/skill-zips/<skill>.zip` artifacts.
5. **Regenerate proof surfaces** — run
   `py -3 tools/generate_provenance_maps.py` and
   `py -3 tools/generate_source_maps.py`.
6. **Validate** — run `py -3 tools/validate_marketplace.py` and
   `py -3 tools/project_skills.py --check` to confirm the projection and flat
   zips match custody and manifest.
```

old_string:
```markdown
All 20 plugin manifests must use the directory-level `entries[]` projection-lane
shape.
```

new_string:
```markdown
All 21 plugin manifests must use the directory-level `entries[]` projection-lane
shape.
```

old_string:
```markdown
## Zip projection lanes

When projecting from marketplace source to GPT-ready zips under
`generated/skill-zips/`, each entry falls into one lane:

- **`direct`** — already GPT-safe. Verbatim passthrough from projection to
  zip. No overlay needed.
- **`overlay`** — codex-safe but not GPT-safe. Needs GPT adaptation declared
  under `adapters/gpt/` to become installable as a raw GPT package. The
  overlay makes the export safe without weakening Codex-native plugin
  behavior.
- **`excluded`** — not exportable as a raw GPT package. The entry is
  intentionally omitted from the zip corpus. Exclusion is explicit, not
  silent.

The lane is a per-entry decision recorded alongside the manifest entry. It
drives export behavior, not projection behavior.
```

new_string:
```markdown
## Zip projection

`generated/skill-zips/<skill>.zip` is a flat, deterministic archive of the
staged Codex projection for each active `canonical_name`. The archive contains
exactly one top-level folder named `<skill>/`, including `<skill>/SKILL.md`.
There is no per-pack subdirectory and no `registry.json`. The projection is the
same byte content installed into `codex-marketplace/plugins/<pack>/skills/<skill>/`;
GPT-readiness is a property of the Codex projection itself, not a separate lane.
```

**Step 6: Update `docs/overlay-adapter-policy.md`**

old_string:
```markdown
If a third-party skill needs a content change, the path is:
1. Add an overlay adapter under `adapters/codex/<plugin>/<skill>/` or `adapters/gpt/<plugin>/<skill>/`.
2. Set `content_mode` to `normalised` or `adapted` in the bundle manifest.
3. Record the adaptation note in the manifest entry.
4. Regenerate the projection.

Do not edit the third-party source tree to fix a skill. Edit at the adapter layer.

## When to add an overlay adapter

Overlay adapters live under `adapters/codex/` (for Codex projection changes) or `adapters/gpt/` (for GPT export changes).

### Add a Codex overlay adapter when:

- A third-party skill references harness-specific features (Claude hooks, Cursor plugins, etc.) that need repointing for Codex compatibility.
- A third-party skill's frontmatter needs normalization to marketplace schema without changing the instruction body.
- A third-party skill's internal links point to moved files that need repointing.

This is the `normalised` mode. The skill body stays unchanged beyond link repointing.

### Add a GPT overlay adapter when:

- A Codex-safe skill is not GPT-safe and needs adaptation to become installable as a raw GPT package.
- The overlay makes the export safe without weakening Codex-native plugin behavior.

This is the GPT export lane (`overlay` mode in `adapters/gpt/manifest.json`).

## When NOT to add an overlay adapter

**Usually, do not add an overlay.** Most skills are either:
- Already GPT-safe as-is → `direct` export, no overlay needed.
- Not exportable as a raw GPT package → `excluded` from the zip corpus.

Add an overlay only when the skill is Codex-safe but not GPT-safe AND can be made GPT-safe without weakening Codex behavior. If the skill cannot be made GPT-safe without weakening it, exclude it.
```

new_string:
```markdown
If a third-party skill needs a content change, the path is:
1. Add a Codex overlay adapter under `adapters/codex/<plugin>/<skill>/`.
2. Set `content_mode` to `normalised` or `adapted` in the bundle manifest.
3. Record the adaptation note in the manifest entry.
4. Regenerate the projection.

Do not edit the third-party source tree to fix a skill. Edit at the adapter layer.

## When to add a Codex overlay adapter

- A third-party skill references harness-specific features (Claude hooks, Cursor plugins, etc.) that need repointing for Codex compatibility.
- A third-party skill's frontmatter needs normalization to marketplace schema without changing the instruction body.
- A third-party skill's internal links point to moved files that need repointing.

This is the `normalised` mode. The skill body stays unchanged beyond link repointing.

## When NOT to add an overlay adapter

**Usually, do not add an overlay.** The flat `generated/skill-zips/<skill>.zip` is
exactly the staged Codex projection. If a skill is not suitable as a raw GPT
package, it should not be projected at all (set `import_status` or
`content_mode` to `skipped`/`blocked` in the bundle manifest).
```

**Step 7: Update `.agents/docs/unslop/profile.md`**

old_string:
```markdown
- `gpt-overlays/` describes projection behavior, not source doctrine.
```

new_string:
```markdown
- `adapters/codex/` describes Codex projection behavior, not source doctrine.
```

**Step 8: Update `README.md` generated zip paragraph**

old_string:
```markdown
Canonical repo-resident `skill.zip` artifacts, when present, live under
`generated/skill-zips/<pack-or-plugin>/<skill-name>/skill.zip` with a registry at
`generated/skill-zips/registry.json`. The package tooling is the normal writer
for that surface.

That generated surface is the GPT-ready export surface. It is built from the
marketplace source tree plus any repo-owned GPT overlay declared under
`adapters/gpt/`. Direct exports stay direct when the source is already
GPT-safe; overlay exports apply the overlay before packaging; excluded skills
are recorded in the registry with a reason instead of being exported raw.

Treat the marketplace plugin roots under `codex-marketplace/plugins/` as the
canonical install surface. Treat `generated/skill-zips/` as a generated GPT
export corpus, not canonical source.
```

new_string:
```markdown
Canonical repo-resident `skill.zip` artifacts, when present, live as flat files
under `generated/skill-zips/<skill-name>.zip`. The package tooling is the normal
writer for that surface.

That generated surface is the GPT-ready export surface. It is built as a
deterministic copy of the staged Codex projection. Treat the marketplace plugin
roots under `codex-marketplace/plugins/` as the canonical install surface.
Treat `generated/skill-zips/` as a generated GPT export corpus, not canonical
source.
```

**Step 8b: Update `README.md` worker command**

old_string:
```markdown
`py -3 tools/update_skill_artifacts.py --skill <pack>/<skill>` for a targeted
refresh. Use `--all` only for an explicit full regeneration.
```

new_string:
```markdown
`py -3 tools/update_skill_artifacts.py --all` for a full regeneration. The
`--skill` and `--pack` flags remain as backwards-compatible aliases.
```

**Step 9: Update `codex-marketplace/README.md` generated zip paragraph**

old_string:
```markdown
Repo-resident canonical `skill.zip` artifacts are published separately under
`generated/skill-zips/<pack-or-plugin>/<skill-name>/skill.zip`, with
`generated/skill-zips/registry.json` mapping each archive back to the source
skill tree that produced it.

That generated surface is the GPT-ready export surface. It packages the source
skill tree plus any repo-owned GPT overlay declared under `adapters/gpt/`.
Direct exports stay direct when the source is already GPT-safe; overlay exports
apply the overlay before packaging; excluded skills are recorded in the
registry with a reason instead of being exported raw.

The marketplace plugin roots are the canonical install surface. `adapters/gpt/`
exists to keep generated exports GPT-safe without changing Codex plugin
behavior.
```

new_string:
```markdown
Repo-resident canonical `skill.zip` artifacts are published as flat files under
`generated/skill-zips/<skill-name>.zip`. There is no per-pack subdirectory and
no `registry.json`.

That generated surface is the GPT-ready export surface. It is a deterministic
copy of the staged Codex projection.

The marketplace plugin roots are the canonical install surface.
```

**Step 10: Update `repo-index/README.md` validation list**

old_string:
```markdown
- `py -3 tools/update_skill_artifacts.py --skill <pack>/<skill>`
- `py -3 tools/validate_generated_drift.py --base origin/main`
```

new_string:
```markdown
- `py -3 tools/update_skill_artifacts.py --all`
- `py -3 tools/project_skills.py --check`
```

**Step 11: Update `.agents/guides/marketplace-generation-guide.md`**

old_string:
```markdown
- Adapter files under `adapters/codex/` or `adapters/gpt/`
```

new_string:
```markdown
- Adapter files under `adapters/codex/`
```

old_string:
```markdown
If a skillset pack or projection lane lacks a manifest-driven generator/validator path, add one to `tools/` and wire it into the standard update/check entrypoints. Do not hand-edit projected skill trees, source maps, provenance maps, registry surfaces, or zip artifacts.
```

new_string:
```markdown
If a skillset pack or projection lane lacks a manifest-driven generator/validator path, add one to `tools/` and wire it into the standard update/check entrypoints. Do not hand-edit projected skill trees, source maps, provenance maps, or zip artifacts.
```

old_string:
```markdown
- Adapter/overlay trees under `adapters/`
```

new_string:
```markdown
- Adapter/overlay trees under `adapters/codex/`
```

**Step 12: Update `provenance/house-skills.md`**

old_string:
```markdown
- Notes: Retired legacy skill helper. Skill packaging is now handled by `tools/package_skill_zips.py` and the deterministic marketplace generation pipeline. This record exists only for provenance audit of the retired source path.
```

new_string:
```markdown
- Notes: Retired legacy skill helper. Skill packaging is now handled by `tools/project_skills.py` and the deterministic marketplace generation pipeline. This record exists only for provenance audit of the retired source path.
```

**Step 13: Rewrite `tools/README.md`**

Replace the file with:

```markdown
# tools

Small helper scripts belong here.

Agent-facing policy for this directory lives in [AGENTS.md](AGENTS.md).

Current marketplace flow:

- `generate_marketplace.py` regenerates `.agents/plugins/marketplace.json` and `codex-marketplace/manifest.json` from the local plugin bundle and source ledger, and `--check` compares both files without writing.
- `update_skill_artifacts.py` is the canonical generator orchestrator for targeted skill updates, pack updates, and explicit full regeneration. Full regeneration runs the marketplace manifest, repo index, pack-manifest, mega-pack, projection, proof-map, first-party-catalog, and flat skill-zip generators in one deterministic pass.
- `project_skills.py` stages overlays, materializes plugin skill trees under `codex-marketplace/plugins/<pack>/skills/`, and writes flat deterministic `generated/skill-zips/<skill>.zip` archives. `--check` validates projected trees and zip shape without writing.
- `validate_skill_zips.py` checks the canonical flat `skill.zip` surface and fails on stale, missing, or malformed artifacts.
- `validate_marketplace.py` checks the marketplace export, plugin manifest, bundle manifest, source ledger, repo index, local path references, projection materialization, and selected pack bundle-manifest freshness for the protected marketplace shape.
- `validate_repo_index.py` checks that the repo index stays aligned with the current marketplace and scoped guidance surfaces, but it is not the freshness proof for `repo-index/repo-index.json`.
- `generate_repo_index.py` regenerates `repo-index/repo-index.json` and `--check` compares the rendered file without writing.
- `generate_pack_manifests.py` regenerates the selected pack bundle-manifest surfaces and `--check` compares them without writing.
- `rebuild_marketplace.py` is the canonical local full reconciliation and validation entrypoint. It runs the full generator stack and the matching validators before a worker should return green.
- `check_marketplace.py` is the canonical CI gate. It runs the non-mutating checks and fails if the committed tree would need regeneration.

Codex plugin first; generated GPT-safe skill zips second.

Current scope note: `generated/skill-zips/` is the flat GPT-ready export surface
for skill zips. It is a deterministic copy of the staged Codex projection.
`py -3 tools/rebuild_marketplace.py` is the canonical local full reconciliation
and validation entrypoint. `py -3 tools/check_marketplace.py` is the canonical
CI gate.

Common worker update command:

```bash
py -3 tools/update_skill_artifacts.py --all
```

Use `--check` to validate the current generated surface without rewriting it.
The `--skill` and `--pack` flags remain as backwards-compatible aliases that
run the full pipeline.

Keep tooling minimal and focused on validation or lightweight asset handling.
```

**Verification:**

```text
git status --short
```

Expected: deleted files listed; no unexpected changes.

**Commit message:** `docs: remove gpt/per-pack zip references and obsolete tool docs`

## Task 7: Update tests

**Files:**
- Modify `tests/test_skill_overlay_materializer.py:21`
- Modify `tests/test_validate_marketplace.py:24-32`, `199-204`, `624`, `644`
- Modify `tests/test_generator_check_modes.py` top imports and replace/remove relevant tests.

**Expected interim state:** Test imports no longer reference deleted modules. `test_generator_check_modes.py` tests the new `project_skills` pipeline.

**Step 1: Update `tests/test_skill_overlay_materializer.py`**

old_string:
```python
from skill_zip_artifacts import validate_skill_markdown_frontmatter  # noqa: E402
```

new_string:
```python
from skill_validation import validate_skill_markdown_frontmatter  # noqa: E402
```

**Step 2: Update `tests/test_validate_marketplace.py`**

old_string:
```python
import validate_marketplace  # noqa: E402
import superpowers_source  # noqa: E402
import skill_zip_artifacts  # noqa: E402
from skill_zip_artifacts import validate_skill_markdown_frontmatter  # noqa: E402
from validate_marketplace import (  # noqa: E402
    _validate_projection_entry_provenance,
    _validate_repo_index_metadata,
    validate_skill_bundle_manifest,
    validate_superpowers_bundle_manifest,
)
```

new_string:
```python
import validate_marketplace  # noqa: E402
import superpowers_source  # noqa: E402
import project_skills  # noqa: E402
from skill_validation import validate_skill_markdown_frontmatter  # noqa: E402
from validate_marketplace import (  # noqa: E402
    _validate_projection_entry_provenance,
    _validate_repo_index_metadata,
    validate_skill_bundle_manifest,
    validate_superpowers_bundle_manifest,
)
```

old_string:
```python
            self.assertEqual(
                run_mock.call_args.args[0],
                [sys.executable, "tools/materialize_projection.py", "--check"],
            )
```

new_string:
```python
            self.assertEqual(
                run_mock.call_args.args[0],
                [sys.executable, "tools/project_skills.py", "--check"],
            )
```

old_string:
```python
            with patch("skill_zip_artifacts.ROOT", temp_root):
                with self.assertRaises(ValueError):
                    validate_skill_markdown_frontmatter(projected_skill_root)
```

new_string:
```python
            with patch("skill_validation.ROOT", temp_root):
                with self.assertRaises(ValueError):
                    validate_skill_markdown_frontmatter(projected_skill_root)
```

old_string:
```python
            with patch("skill_zip_artifacts.ROOT", temp_root):
                validate_skill_markdown_frontmatter(projected_skill_root)
```

new_string:
```python
            with patch("skill_validation.ROOT", temp_root):
                validate_skill_markdown_frontmatter(projected_skill_root)
```

**Step 3: Update `tests/test_generator_check_modes.py`**

old_string:
```python
import generate_pack_manifests
import generate_repo_index
import materialize_projection
import update_skill_artifacts
import validate_generated_drift
from generate_pack_manifests import PACKS
from skill_zip_artifacts import (
    FORBIDDEN_FILE_NAMES,
    SKIP_DIR_NAMES,
    TEXT_SUFFIXES,
    compute_source_fingerprint,
    scan_skill_tree,
    sha256_file,
)
```

new_string:
```python
import generate_pack_manifests
import generate_repo_index
import project_skills
import update_skill_artifacts
from generate_pack_manifests import PACKS
```

old_string:
```python
@dataclass
class SkillArtifact:
    pack: str
    skill: str
    export_mode: str
    source_path: str
    overlay_path: str | None
    zip_path: str
    source_file_count: int
    source_bytes: int
    source_sha256: str
    overlay_file_count: int
    overlay_bytes: int
    overlay_sha256: str | None
    zip_size_bytes: int
    zip_sha256: str
```

Remove the `SkillArtifact` dataclass and `artifact_to_record` helper entirely (no replacement needed).

Replace the three `test_materialize_projection_*` tests with the following:

```python
    def test_project_skills_check_detects_stale_projection(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            source_root = temp_root / "sources" / "third_party" / "ecc" / "upstream" / "skills" / "sample-skill"
            projected_root = temp_root / "codex-marketplace" / "plugins" / "sample-pack" / "skills" / "sample-skill"
            manifest_path = temp_root / "codex-marketplace" / "plugins" / "sample-pack" / "references" / "bundle-manifest.json"

            source_root.mkdir(parents=True, exist_ok=True)
            projected_root.mkdir(parents=True, exist_ok=True)
            manifest_path.parent.mkdir(parents=True, exist_ok=True)

            (source_root / "SKILL.md").write_text("---\nname: sample-skill\ndescription: sample\n---\n\nbody\n", encoding="utf-8")
            (projected_root / "SKILL.md").write_text("---\nname: sample-skill\ndescription: sample\n---\n\nbody\n", encoding="utf-8")

            manifest = {
                "bundle_name": "sample-pack",
                "bundle_version": "1.0.0",
                "bundle_type": "projection-lane",
                "plugin_root": "codex-marketplace/plugins/sample-pack",
                "is_mega_pack": False,
                "source_families": ["ecc"],
                "notes": ["generated"],
                "provenance_refs": ["provenance/sample-pack.md"],
                "plugin_author": "Harley Bartles",
                "plugin_license": "MIT",
                "entries": [
                    {
                        "canonical_name": "sample-skill",
                        "source_category": "third_party",
                        "content_mode": "verbatim",
                        "source_family": "ecc",
                        "canonical_source_path": "sources/third_party/ecc/upstream/skills/sample-skill",
                        "local_path": "skills/sample-skill",
                        "provenance_note": "Projected verbatim from retained ECC custody.",
                        "source_path": "sources/third_party/ecc/upstream/skills/sample-skill/SKILL.md",
                        "source_author": "ECC",
                        "source_license": "MIT",
                        "source_repo": "https://github.com/affaan-m/ECC",
                        "copy_expectation": "byte_identical",
                        "import_status": "imported",
                    }
                ],
                "repo_index": {
                    "source_md": "codex-marketplace/plugins/sample-pack/SOURCE.md",
                    "bundle_manifest": "codex-marketplace/plugins/sample-pack/references/bundle-manifest.json",
                    "skills_path": "codex-marketplace/plugins/sample-pack/skills",
                    "agents_md": None,
                    "registry_alignment": {"status": "aligned", "note": None},
                },
            }
            manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

            with (
                patch.object(project_skills, "ROOT", temp_root),
                patch.object(project_skills, "GENERATED_SKILL_ZIPS_ROOT", temp_root / "generated/skill-zips"),
                patch.object(
                    project_skills,
                    "load_plugin_root_inventory",
                    return_value=[{"name": "sample-pack", "plugin_root": "codex-marketplace/plugins/sample-pack", "enabled": True}],
                ),
            ):
                project_skills.project_skills(write=True)

            (projected_root / "SKILL.md").write_text(
                "---\nname: sample-skill\ndescription: stale\n---\n\nbody\n",
                encoding="utf-8",
            )
            with (
                patch.object(project_skills, "ROOT", temp_root),
                patch.object(project_skills, "GENERATED_SKILL_ZIPS_ROOT", temp_root / "generated/skill-zips"),
                patch.object(
                    project_skills,
                    "load_plugin_root_inventory",
                    return_value=[{"name": "sample-pack", "plugin_root": "codex-marketplace/plugins/sample-pack", "enabled": True}],
                ),
            ):
                with self.assertRaises(ValueError):
                    project_skills.project_skills(write=False)

    def test_project_skills_check_fails_on_stale_skill_roots(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            source_root = temp_root / "sources" / "third_party" / "ecc" / "upstream" / "skills" / "sample-skill"
            projected_root = temp_root / "codex-marketplace" / "plugins" / "sample-pack" / "skills" / "sample-skill"
            stale_root = temp_root / "codex-marketplace" / "plugins" / "sample-pack" / "skills" / "retired-skill"
            manifest_path = temp_root / "codex-marketplace" / "plugins" / "sample-pack" / "references" / "bundle-manifest.json"

            source_root.mkdir(parents=True, exist_ok=True)
            projected_root.mkdir(parents=True, exist_ok=True)
            stale_root.mkdir(parents=True, exist_ok=True)
            manifest_path.parent.mkdir(parents=True, exist_ok=True)

            (source_root / "SKILL.md").write_text("---\nname: sample-skill\ndescription: sample\n---\n\nbody\n", encoding="utf-8")
            (projected_root / "SKILL.md").write_text("---\nname: sample-skill\ndescription: sample\n---\n\nbody\n", encoding="utf-8")
            (stale_root / "SKILL.md").write_text("---\nname: retired-skill\ndescription: stale\n---\n\nbody\n", encoding="utf-8")

            manifest = {
                "bundle_name": "sample-pack",
                "bundle_version": "1.0.0",
                "bundle_type": "projection-lane",
                "plugin_root": "codex-marketplace/plugins/sample-pack",
                "is_mega_pack": False,
                "source_families": ["ecc"],
                "notes": ["generated"],
                "provenance_refs": ["provenance/sample-pack.md"],
                "plugin_author": "Harley Bartles",
                "plugin_license": "MIT",
                "entries": [
                    {
                        "canonical_name": "sample-skill",
                        "source_category": "third_party",
                        "content_mode": "verbatim",
                        "source_family": "ecc",
                        "canonical_source_path": "sources/third_party/ecc/upstream/skills/sample-skill",
                        "local_path": "skills/sample-skill",
                        "provenance_note": "Projected verbatim from retained ECC custody.",
                        "source_path": "sources/third_party/ecc/upstream/skills/sample-skill/SKILL.md",
                        "source_author": "ECC",
                        "source_license": "MIT",
                        "source_repo": "https://github.com/affaan-m/ECC",
                        "copy_expectation": "byte_identical",
                        "import_status": "imported",
                    }
                ],
                "repo_index": {
                    "source_md": "codex-marketplace/plugins/sample-pack/SOURCE.md",
                    "source_ledger": ["sources/third_party/ecc/upstream/source-custody.md"],
                    "license_path": "codex-marketplace/plugins/sample-pack/LICENSE",
                    "bundle_manifest": "codex-marketplace/plugins/sample-pack/references/bundle-manifest.json",
                    "skills_path": "codex-marketplace/plugins/sample-pack/skills",
                    "provenance_refs": ["provenance/sample-pack.md"],
                    "agents_md": None,
                    "registry_alignment": {"status": "aligned", "note": None},
                },
            }
            manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

            with (
                patch.object(project_skills, "ROOT", temp_root),
                patch.object(project_skills, "GENERATED_SKILL_ZIPS_ROOT", temp_root / "generated/skill-zips"),
                patch.object(
                    project_skills,
                    "load_plugin_root_inventory",
                    return_value=[{"name": "sample-pack", "plugin_root": "codex-marketplace/plugins/sample-pack", "enabled": True}],
                ),
            ):
                project_skills.project_skills(write=True)

            with (
                patch.object(project_skills, "ROOT", temp_root),
                patch.object(project_skills, "GENERATED_SKILL_ZIPS_ROOT", temp_root / "generated/skill-zips"),
                patch.object(
                    project_skills,
                    "load_plugin_root_inventory",
                    return_value=[{"name": "sample-pack", "plugin_root": "codex-marketplace/plugins/sample-pack", "enabled": True}],
                ),
            ):
                with self.assertRaises(ValueError) as ctx:
                    project_skills.project_skills(write=False)

            self.assertIn("retired-skill", str(ctx.exception))

    def test_project_skills_write_prunes_stale_skill_roots(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            source_root = temp_root / "sources" / "third_party" / "ecc" / "upstream" / "skills" / "sample-skill"
            projected_root = temp_root / "codex-marketplace" / "plugins" / "sample-pack" / "skills" / "sample-skill"
            stale_root = temp_root / "codex-marketplace" / "plugins" / "sample-pack" / "skills" / "retired-skill"
            manifest_path = temp_root / "codex-marketplace" / "plugins" / "sample-pack" / "references" / "bundle-manifest.json"

            source_root.mkdir(parents=True, exist_ok=True)
            projected_root.mkdir(parents=True, exist_ok=True)
            stale_root.mkdir(parents=True, exist_ok=True)
            manifest_path.parent.mkdir(parents=True, exist_ok=True)

            (source_root / "SKILL.md").write_text("---\nname: sample-skill\ndescription: sample\n---\n\nbody\n", encoding="utf-8")
            (projected_root / "SKILL.md").write_text("---\nname: sample-skill\ndescription: sample\n---\n\nbody\n", encoding="utf-8")
            (stale_root / "SKILL.md").write_text("---\nname: retired-skill\ndescription: stale\n---\n\nbody\n", encoding="utf-8")

            manifest = {
                "bundle_name": "sample-pack",
                "bundle_version": "1.0.0",
                "bundle_type": "projection-lane",
                "plugin_root": "codex-marketplace/plugins/sample-pack",
                "is_mega_pack": False,
                "source_families": ["ecc"],
                "notes": ["generated"],
                "provenance_refs": ["provenance/sample-pack.md"],
                "plugin_author": "Harley Bartles",
                "plugin_license": "MIT",
                "entries": [
                    {
                        "canonical_name": "sample-skill",
                        "source_category": "third_party",
                        "content_mode": "verbatim",
                        "source_family": "ecc",
                        "canonical_source_path": "sources/third_party/ecc/upstream/skills/sample-skill",
                        "local_path": "skills/sample-skill",
                        "provenance_note": "Projected verbatim from retained ECC custody.",
                        "source_path": "sources/third_party/ecc/upstream/skills/sample-skill/SKILL.md",
                        "source_author": "ECC",
                        "source_license": "MIT",
                        "source_repo": "https://github.com/affaan-m/ECC",
                        "copy_expectation": "byte_identical",
                        "import_status": "imported",
                    }
                ],
                "repo_index": {
                    "source_md": "codex-marketplace/plugins/sample-pack/SOURCE.md",
                    "source_ledger": ["sources/third_party/ecc/upstream/source-custody.md"],
                    "license_path": "codex-marketplace/plugins/sample-pack/LICENSE",
                    "bundle_manifest": "codex-marketplace/plugins/sample-pack/references/bundle-manifest.json",
                    "skills_path": "codex-marketplace/plugins/sample-pack/skills",
                    "provenance_refs": ["provenance/sample-pack.md"],
                    "agents_md": None,
                    "registry_alignment": {"status": "aligned", "note": None},
                },
            }
            manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

            with (
                patch.object(project_skills, "ROOT", temp_root),
                patch.object(project_skills, "GENERATED_SKILL_ZIPS_ROOT", temp_root / "generated/skill-zips"),
                patch.object(
                    project_skills,
                    "load_plugin_root_inventory",
                    return_value=[{"name": "sample-pack", "plugin_root": "codex-marketplace/plugins/sample-pack", "enabled": True}],
                ),
            ):
                project_skills.project_skills(write=True)

            self.assertTrue(projected_root.exists())
            self.assertFalse(stale_root.exists())
            self.assertTrue((temp_root / "generated/skill-zips/sample-skill.zip").exists())
```

Replace `test_update_skill_artifacts_check_runs_mega_pack_generation_first` with:

```python
    def test_update_skill_artifacts_check_runs_skill_artifact_pipeline(self) -> None:
        calls: list[tuple[str, dict[str, object]]] = []

        def record(name: str, result: object | None = None):
            def _inner(**kwargs):
                calls.append((name, dict(kwargs)))
                return result
            return _inner

        with (
            patch.object(update_skill_artifacts, "generate_all_mega_packs", side_effect=record("generate_all_mega_packs")),
            patch.object(update_skill_artifacts, "generate_pack_manifests", side_effect=record("generate_pack_manifests")),
            patch.object(update_skill_artifacts, "project_skills", side_effect=record("project_skills")),
            patch.object(update_skill_artifacts, "generate_first_party_skill_catalog", side_effect=record("generate_first_party_skill_catalog")),
            patch.object(update_skill_artifacts, "_run_tool") as run_tool_mock,
            patch.object(sys, "argv", ["update_skill_artifacts.py", "--check"]),
        ):
            self.assertEqual(update_skill_artifacts.main(), 0)

        self.assertEqual(
            calls,
            [
                ("generate_pack_manifests", {"write": False}),
                ("generate_all_mega_packs", {"write": False}),
                ("project_skills", {"write": False}),
                ("generate_first_party_skill_catalog", {"write": False}),
            ],
        )
        run_tool_mock.assert_called()
```

Remove `test_validate_generated_drift_allows_rename_paths_for_generated_artifacts` entirely.

**Verification:**

```text
py -3 -m pytest tests/test_skill_overlay_materializer.py tests/test_validate_marketplace.py tests/test_generator_check_modes.py -q
```

Some tests in `test_validate_marketplace.py` may still fail until `project_skills` is fully wired and the flat zips exist. Run the subset for the changed tests to confirm import-level issues are resolved.

**Commit message:** `test: update tests for flat skill zip projection`

## Task 8: Regenerate, validate, and verify counts

**Files:**
- All generated surfaces under `codex-marketplace/plugins/`, `generated/skill-zips/`, `repo-index/repo-index.json`, `.agents/plugins/marketplace.json`, `codex-marketplace/manifest.json`, pack SOURCE/README/PROJECTION docs, index mesh `INDEX.md` files.

**Expected interim state:** All generated surfaces are consistent with the flat zip layout. `project_skills.py --check`, `check_marketplace.py`, and the targeted pytest subset pass.

**Step 1: Run the full regeneration**

```text
py -3 tools/rebuild_marketplace.py
```

This will:
- Regenerate marketplace manifests (`generate_marketplace.py`)
- Regenerate the repo index (`generate_repo_index.py`)
- Regenerate pack manifests (`generate_pack_manifests.py`)
- Regenerate mega-packs (`generate_mega_packs.py`)
- Project all skills and write flat zips (`project_skills.py`)
- Regenerate provenance and source maps
- Regenerate the first-party skill catalog
- Regenerate the index mesh (`tools/INDEX.md`, `adapters/INDEX.md`, etc.)
- Run validators

**Step 2: Verify the flat zip layout**

```text
# Confirm only flat <skill>.zip files exist and count them
python - <<'PY'
import pathlib
root = pathlib.Path('generated/skill-zips')
files = sorted(p for p in root.iterdir() if p.is_file())
print('zip count:', len(files))
print('unexpected:', [p.name for p in files if not p.name.endswith('.zip')])
PY

# Confirm unique active canonical_name count matches
python -c "import json, pathlib; entries=[]; [entries.extend(json.loads(p.read_text()).get('entries',[])) for p in pathlib.Path('codex-marketplace/plugins').glob('*/references/bundle-manifest.json')]; active=[e for e in entries if e.get('import_status') not in {'skipped','blocked'} and e.get('content_mode') not in {'skipped','blocked'}]; print('unique canonical names:', len({e['canonical_name'] for e in active}))"
```

The two numbers must be equal (currently expected: 94).

**Step 3: Run validation gates**

```text
py -3 tools/project_skills.py --check
py -3 tools/validate_skill_zips.py
py -3 tools/validate_marketplace.py
py -3 tools/validate_repo_index.py
py -3 tools/check_marketplace.py
```

**Step 4: Run tests**

```text
py -3 -m pytest tests/test_generator_check_modes.py tests/test_validate_marketplace.py tests/test_skill_overlay_materializer.py -q
```

**Step 5: Verify no stale references remain**

```text
rg -l "adapters/gpt|skill_zip_artifacts|materialize_projection|skill_gpt_exports|export_skill_zips|validate_export_skill_zips|validate_generated_drift|package_skill_zips|registry\.json|generated/skill-zips/[a-z0-9-]+/[a-z0-9-]+/skill\.zip" tools/ codex-marketplace/ .agents/ docs/ repo-index/ README.md || true
```

Any remaining hits should be in `provenance/` or archive docs; active tooling, AGENTS, README, and generated surfaces must be clean. If unexpected hits remain, reopen the relevant task.

**Verification:**

All commands in Steps 2-5 pass with zero errors.

**Commit message:** `regenerate: flat skill zips and updated generated surfaces`

---

## Test Plan

- Unit: `tests/test_skill_overlay_materializer.py` confirms frontmatter validation still works after the module move.
- Unit: `tests/test_validate_marketplace.py` confirms `validate_marketplace.py` calls `tools/project_skills.py --check` and accepts the new `validate_skill_zip_assertions` shape.
- Unit: `tests/test_generator_check_modes.py` confirms `project_skills` check/write/prune behavior and `update_skill_artifacts --check` orchestration order.
- Integration: `tools/project_skills.py --check` validates projection trees and flat zips against the staged source.
- Integration: `tools/rebuild_marketplace.py` regenerates all surfaces without error.
- Integration: `tools/check_marketplace.py` passes on the regenerated tree.
- Count: `generated/skill-zips/` contains one `<skill>.zip` per unique active `canonical_name` (currently 94).

## Expected Interim State Summary

After each task:

1. `skill_validation.py` exists and is importable.
2. `project_skills.py` exists and is importable.
3. `update_skill_artifacts.py` orchestrates the new four-function pipeline.
4. Generated-surface generators and repo-index metadata point to flat zip paths.
5. Validators and entrypoints use `project_skills` / `update_skill_artifacts --check`.
6. Obsolete files deleted; docs/AGENTS/README surfaces no longer mention `adapters/gpt/`, `registry.json`, or per-pack zip paths.
7. Tests updated; `validate_generated_drift` test removed.
8. Full regeneration produces 94 flat zips and all gates pass.

## Commit Sequence

1. `refactor: move validate_skill_markdown_frontmatter to tools/skill_validation.py`
2. `feat: add tools/project_skills.py for flat skill zip projection`
3. `refactor: update_skill_artifacts orchestrates flat skill zip pipeline`
4. `refactor: point generated-surface metadata at flat skill zips`
5. `refactor: point validators and entrypoints at project_skills`
6. `docs: remove gpt/per-pack zip references and obsolete tool docs`
7. `test: update tests for flat skill zip projection`
8. `regenerate: flat skill zips and updated generated surfaces`

These can be squashed into a single PR or kept as a logical sequence for easier review.

## SDD Confidence Rating

**8/10**

**Rationale:**
- All source files, call sites, generated-surface consumers, AGENTS/docs/README references, and tests have been inventoried.
- The new `project_skills.py` design preserves the existing deterministic zip conventions and projection materialization behavior by reusing helper bodies from `tools/skill_zip_artifacts.py` and `tools/materialize_projection.py`.
- `update_skill_artifacts.py`, `validate_marketplace.py`, `rebuild_marketplace.py`, and `check_marketplace.py` are reduced to a single `project_skills` call path, removing the previous split between `materialize_projection` and `skill_zip_artifacts`.
- The design spec and plan counts have been reconciled to the current `origin/main` after rebase: 168 active bundle-manifest entries collapse into 94 unique flat zips. The previous 174/99 numbers reflected the pre-rebase state.
- The `--skill` and `--pack` flags in `update_skill_artifacts.py` are kept as backwards-compatible aliases that run the full pipeline; they do not limit projection to a single pack. This avoids cross-pack consistency issues at the cost of always regenerating all surfaces.

## Open Questions / Follow-up

1. Counts have been reconciled against the current `origin/main` after rebase (168 active entries, 94 unique `canonical_name`). Re-verify after Task 8 regeneration.
2. Decide whether `tools/validate_skill_zips.py` should be kept as a thin wrapper or deleted. This plan keeps it because `repo-index/README.md` and `validate_repo_index.py` reference it as the canonical skill-zip check; deleting it would require additional doc/validator edits.
3. After implementation, verify `tools/generate_index_mesh.py --check` passes and that `tools/INDEX.md` and `adapters/INDEX.md` no longer list deleted scripts or the `adapters/gpt` tree.

---

## Plan Completion Checklist

- [x] Read design spec, planning guide, and source files
- [x] Inventory all call sites and generated-surface consumers
- [x] Draft implementation plan with required sections and exact code snippets
- [x] Write plan to target path
- [ ] Approve plan before implementation
- [ ] Execute tasks 1-8
- [ ] Run full validation and regenerate surfaces
- [ ] Open PR with publication proof
