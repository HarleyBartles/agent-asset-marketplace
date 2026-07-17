#!/usr/bin/env python3
"""Generate the active first-party skill catalog from repo truth."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from marketplace_utils import ROOT, load_json, load_text, parse_top_markdown_table

SOURCE_ROOT = ROOT / "sources/first_party/skills"
CATALOG_PATH = ROOT / "provenance/first-party-skills.md"
PLUGIN_MANIFESTS_ROOT = ROOT / "codex-marketplace/plugins"
GENERATED_REGISTRY_PATH = ROOT / "generated/skill-zips/registry.json"

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


@dataclass(frozen=True)
class CatalogEntry:
    name: str
    source_root: str
    source_path: str
    source_id: str
    projected_in: tuple[str, ...]
    generated_refs: tuple[str, ...]
    repo_refs: tuple[str, ...]


def _parse_frontmatter(skill_md: Path) -> dict[str, Any]:
    raw = skill_md.read_text(encoding="utf-8")
    if raw.startswith("\ufeff"):
        raw = raw.lstrip("\ufeff")
    lines = raw.splitlines()
    if not lines or lines[0] != "---":
        raise ValueError(f"{skill_md.relative_to(ROOT)} must start with YAML frontmatter")

    end_index = None
    for index, line in enumerate(lines[1:], start=1):
        if line == "---":
            end_index = index
            break
    if end_index is None:
        raise ValueError(f"{skill_md.relative_to(ROOT)} is missing a closing YAML frontmatter delimiter")

    frontmatter_text = "\n".join(lines[1:end_index])

    def _extract(pattern: str) -> str | None:
        match = re.search(pattern, frontmatter_text, flags=re.MULTILINE)
        if match is None:
            return None
        value = match.group(1).strip()
        if len(value) >= 2 and ((value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'"))):
            value = value[1:-1]
        return value

    name = _extract(r"^name:\s*(.+)$")
    source_id = _extract(r"^\s+source-id:\s*(.+)$")
    source_path = _extract(r"^\s+source-path:\s*(.+)$")
    if source_path is None:
        source_path = _extract(r"^\s+source_path:\s*(.+)$")
    provenance_name = _extract(r"^\s+provenance-name:\s*(.+)$")
    if provenance_name is None:
        provenance_name = _extract(r"^\s+provenance_name:\s*(.+)$")

    if not isinstance(name, str) or not name:
        raise ValueError(f"{skill_md.relative_to(ROOT)} frontmatter must include a name")

    return {
        "name": name,
        "metadata": {
            "source-id": source_id or name,
            "source-path": source_path or skill_md.relative_to(ROOT).as_posix(),
            "provenance-name": provenance_name,
        },
    }


def _discover_active_skill_roots() -> list[Path]:
    roots: list[Path] = []
    if not SOURCE_ROOT.exists():
        return roots
    for child in sorted(SOURCE_ROOT.iterdir(), key=lambda path: path.name):
        if not child.is_dir():
            continue
        skill_md = child / "SKILL.md"
        if skill_md.is_file():
            roots.append(child)
    return roots


def _canonical_root_path(skill_root: Path) -> str:
    return skill_root.relative_to(ROOT).as_posix()


def _discover_projected_plugins(skill_name: str, source_root: str) -> tuple[str, ...]:
    plugin_roots: set[str] = set()
    for manifest_path in sorted(PLUGIN_MANIFESTS_ROOT.glob("*/references/bundle-manifest.json")):
        if not manifest_path.is_file():
            continue
        plugin_root = manifest_path.parent.parent
        manifest = load_json(manifest_path)
        entries = manifest.get("entries", [])
        if not isinstance(entries, list):
            continue
        for entry in entries:
            if not isinstance(entry, dict):
                continue
            canonical_name = entry.get("canonical_name")
            canonical_source_path = entry.get("canonical_source_path")
            source_path = entry.get("source_path")
            if canonical_name == skill_name or canonical_source_path == source_root or source_path == f"{source_root}/SKILL.md":
                plugin_roots.add(plugin_root.relative_to(ROOT).as_posix())
                break
    return tuple(sorted(plugin_roots))


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


def _discover_repo_refs(skill_name: str, source_path: str, source_root: str) -> tuple[str, ...]:
    refs: set[str] = set()
    needles = (skill_name, source_path, source_root)
    for ref in REFERENCE_SURFACES:
        if not ref.exists():
            continue
        text = ref.read_text(encoding="utf-8")
        if any(needle in text for needle in needles):
            refs.add(ref.relative_to(ROOT).as_posix())
    return tuple(sorted(refs))


def _build_entries() -> list[CatalogEntry]:
    entries: list[CatalogEntry] = []
    for skill_root in _discover_active_skill_roots():
        skill_md = skill_root / "SKILL.md"
        frontmatter = _parse_frontmatter(skill_md)
        skill_name = frontmatter.get("name") or skill_root.name
        if not isinstance(skill_name, str) or not skill_name.strip():
            raise ValueError(f"{skill_md.relative_to(ROOT)} frontmatter is missing a valid name")
        metadata = frontmatter.get("metadata", {})
        source_id = metadata.get("source-id") or skill_name
        if not isinstance(source_id, str) or not source_id.strip():
            raise ValueError(f"{skill_md.relative_to(ROOT)} metadata.source-id must be a nonblank string")
        source_path = metadata.get("source-path") or metadata.get("source_path") or skill_md.relative_to(ROOT).as_posix()
        if not isinstance(source_path, str) or not source_path.strip():
            raise ValueError(f"{skill_md.relative_to(ROOT)} metadata.source-path must be a nonblank string")
        source_root = _canonical_root_path(skill_root)
        projected_in = _discover_projected_plugins(skill_name, source_root)
        generated_refs = _discover_generated_refs(skill_name, projected_in)
        repo_refs = _discover_repo_refs(skill_name, source_path, source_root)
        entries.append(
            CatalogEntry(
                name=skill_name,
                source_root=source_root,
                source_path=source_path,
                source_id=source_id,
                projected_in=projected_in,
                generated_refs=generated_refs,
                repo_refs=repo_refs,
            )
        )
    return sorted(entries, key=lambda entry: entry.name)


def _format_refs(refs: tuple[str, ...]) -> str:
    if not refs:
        return ""
    return ", ".join(f"`{ref}`" for ref in refs)


def _render(entries: list[CatalogEntry]) -> str:
    lines: list[str] = []
    lines.append("# First-Party Skill Catalog")
    lines.append("")
    lines.append("Generated from the current active first-party skill roots under `sources/first_party/skills/`.")
    lines.append("Do not hand-edit this file.")
    lines.append("")
    lines.append(
        "| Skill | Source root | Source path | Source id | Projected in | Generated refs | Repo refs |"
    )
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    for entry in entries:
        lines.append(
            "| "
            + " | ".join(
                (
                    f"`{entry.name}`",
                    f"`{entry.source_root}`",
                    f"`{entry.source_path}`",
                    f"`{entry.source_id}`",
                    _format_refs(entry.projected_in),
                    _format_refs(entry.generated_refs),
                    _format_refs(entry.repo_refs),
                )
            )
            + " |"
        )
    lines.append("")
    return "\n".join(lines)


def _check_rows(expected: list[CatalogEntry], current_text: str) -> None:
    rows = parse_top_markdown_table(CATALOG_PATH) if CATALOG_PATH.exists() else []
    current_keys = [row.get("Skill", "").strip("`") for row in rows]
    expected_keys = [entry.name for entry in expected]
    if sorted(current_keys) != expected_keys:
        missing = sorted(set(expected_keys) - set(current_keys))
        extra = sorted(set(current_keys) - set(expected_keys))
        parts = []
        if missing:
            parts.append("missing: " + ", ".join(missing))
        if extra:
            parts.append("unexpected: " + ", ".join(extra))
        raise ValueError("first-party skill catalog row set mismatch; " + "; ".join(parts))

    existing_text = CATALOG_PATH.read_text(encoding="utf-8")
    if existing_text != current_text:
        raise ValueError("provenance/first-party-skills.md is stale; run py -3 tools/generate_first_party_skill_catalog.py")


def generate(*, write: bool) -> None:
    entries = _build_entries()
    rendered = _render(entries)
    if write:
        CATALOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        CATALOG_PATH.write_text(rendered, encoding="utf-8", newline="\n")
        print(f"WROTE {CATALOG_PATH.relative_to(ROOT)}")
        return
    if not CATALOG_PATH.exists():
        raise FileNotFoundError(CATALOG_PATH)
    _check_rows(entries, rendered)
    print(f"OK   {CATALOG_PATH.relative_to(ROOT)}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate or validate the first-party skill catalog")
    parser.add_argument("--check", action="store_true", help="validate without writing")
    args = parser.parse_args()
    generate(write=not args.check)
    if args.check:
        print("OK first-party skill catalog: current")
    else:
        print("OK first-party skill catalog: generated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
