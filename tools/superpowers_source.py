#!/usr/bin/env python3
"""Shared helpers for the active superpowers source custody snapshot."""

from __future__ import annotations

from pathlib import Path
from typing import Any
import re

from marketplace_utils import load_json


ROOT = Path(__file__).resolve().parents[1]
SUPERPOWERS_FAMILY_ROOT = ROOT / "sources/third_party/superpowers/obra-superpowers"
SUPERPOWERS_BUNDLE_MANIFEST_PATH = ROOT / "codex-marketplace/plugins/superpowers-plus/references/bundle-manifest.json"
SUPERPOWERS_CUSTODY_REGISTRY_PATH = ROOT / "codex-marketplace/custody-pack-registry.json"
SUPERPOWERS_PROVENANCE_PATH = ROOT / "provenance/superpowers-plus.md"
SUPERPOWERS_SOURCE_MD_PATH = ROOT / "codex-marketplace/plugins/superpowers-plus/SOURCE.md"
SUPERPOWERS_ADAPTER_OVERLAY_PATH = ROOT / "adapters/codex/superpowers-plus/using-superpowers/overlay.yaml"
SUPERPOWERS_ADAPTER_OPENAI_PATH = ROOT / "adapters/codex/superpowers-plus/using-superpowers/agents/openai.yaml"


def load_superpowers_bundle_manifest() -> dict[str, Any]:
    bundle_manifest = load_json(SUPERPOWERS_BUNDLE_MANIFEST_PATH)
    if not isinstance(bundle_manifest, dict):
        raise ValueError(f"{SUPERPOWERS_BUNDLE_MANIFEST_PATH}: bundle manifest must be a mapping")
    return bundle_manifest


def superpowers_custody_root_from_registry() -> str:
    registry = load_json(SUPERPOWERS_CUSTODY_REGISTRY_PATH)
    if not isinstance(registry, dict):
        raise ValueError(f"{SUPERPOWERS_CUSTODY_REGISTRY_PATH}: registry must be a mapping")
    for mapping in registry.get("packs", []):
        if not isinstance(mapping, dict) or not mapping.get("is_mega_pack"):
            continue
        if mapping.get("source_family") == "superpowers":
            custody_root = mapping.get("custody_root")
            if isinstance(custody_root, str) and custody_root.strip():
                return custody_root
    raise ValueError("could not determine superpowers custody root from registry")


def _bundle_manifest_source_root(bundle_manifest: dict[str, Any]) -> str | None:
    canonical_source_root = bundle_manifest.get("canonical_source_root")
    if isinstance(canonical_source_root, str) and canonical_source_root.strip():
        return canonical_source_root
    for entry in bundle_manifest.get("entries", []):
        if not isinstance(entry, dict):
            continue
        if entry.get("source_category") != "third_party":
            continue
        canonical_source_path = entry.get("canonical_source_path")
        if isinstance(canonical_source_path, str) and "/skills/" in canonical_source_path:
            return canonical_source_path.split("/skills/", 1)[0]
        source_path = entry.get("source_path")
        if isinstance(source_path, str) and "/skills/" in source_path:
            return source_path.rsplit("/", 1)[0].rsplit("/", 1)[0]
    return None


def superpowers_source_tag(bundle_manifest: dict[str, Any] | None = None) -> str:
    manifest = bundle_manifest or load_superpowers_bundle_manifest()
    source_tag = manifest.get("source_tag")
    if isinstance(source_tag, str) and source_tag.strip():
        return source_tag
    source_root = superpowers_source_root(manifest)
    return source_root.name


def superpowers_source_root(bundle_manifest: dict[str, Any] | None = None) -> Path:
    manifest = bundle_manifest or load_superpowers_bundle_manifest()
    canonical_source_root = manifest.get("canonical_source_root")
    if not isinstance(canonical_source_root, str) or not canonical_source_root.strip():
        canonical_source_root = _bundle_manifest_source_root(manifest) or superpowers_custody_root_from_registry()
    return ROOT / canonical_source_root


def superpowers_source_commit(bundle_manifest: dict[str, Any] | None = None) -> str:
    manifest = bundle_manifest or load_superpowers_bundle_manifest()
    source_commit = manifest.get("source_commit")
    if isinstance(source_commit, str) and source_commit.strip():
        return source_commit
    if SUPERPOWERS_PROVENANCE_PATH.exists():
        match = re.search(r"Release commit:\s*`([0-9a-f]{40})`", SUPERPOWERS_PROVENANCE_PATH.read_text(encoding="utf-8"))
        if match:
            return match.group(1)
    raise ValueError("could not determine superpowers-plus source commit")


def superpowers_source_ledger() -> list[str]:
    source_root = superpowers_source_root()
    return [
        (source_root / "package.json").relative_to(ROOT).as_posix(),
        (source_root / "README.md").relative_to(ROOT).as_posix(),
        (source_root / "LICENSE").relative_to(ROOT).as_posix(),
        (source_root / "AGENTS.md").relative_to(ROOT).as_posix(),
    ]
