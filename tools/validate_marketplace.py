#!/usr/bin/env python3
"""Validate the private Codex plugin marketplace baseline."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MARKETPLACE = ROOT / ".agents" / "plugins" / "marketplace.json"
AUDIT = ROOT / "reports" / "mark-2-marketplace-audit.md"


class ValidationError(Exception):
    pass


def load_json(path: Path) -> Any:
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except json.JSONDecodeError as exc:
        raise ValidationError(f"{path.relative_to(ROOT)} is not valid JSON: {exc}") from exc


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def inside_repo(path: Path) -> bool:
    try:
        path.resolve().relative_to(ROOT.resolve())
        return True
    except ValueError:
        return False


def resolve_repo_relative(raw_path: str, owner: Path = ROOT) -> Path:
    require(raw_path.startswith("./"), f"path must be local and repo-relative: {raw_path}")
    path = (owner / raw_path).resolve()
    require(inside_repo(path), f"path escapes repository: {raw_path}")
    return path


def validate_marketplace() -> list[str]:
    messages: list[str] = []
    marketplace = load_json(MARKETPLACE)
    messages.append(f"parsed {MARKETPLACE.relative_to(ROOT)}")

    require(marketplace.get("name"), "marketplace missing name")
    require(marketplace.get("interface", {}).get("displayName"), "marketplace missing interface.displayName")
    plugins = marketplace.get("plugins")
    require(isinstance(plugins, list) and plugins, "marketplace.plugins must be a non-empty list")

    asset_catalog_refs: list[str] = []
    legacy_asset_catalog = marketplace.get("assetCatalog")
    if legacy_asset_catalog is not None:
        require(isinstance(legacy_asset_catalog, str), "marketplace assetCatalog must be a string when present")
        asset_catalog_refs.append(legacy_asset_catalog)

    asset_catalogs = marketplace.get("assetCatalogs", [])
    require(isinstance(asset_catalogs, list), "marketplace assetCatalogs must be a list when present")
    for asset_catalog in asset_catalogs:
        require(isinstance(asset_catalog, str), "marketplace assetCatalogs entries must be strings")
        if asset_catalog not in asset_catalog_refs:
            asset_catalog_refs.append(asset_catalog)

    require(asset_catalog_refs, "marketplace missing assetCatalog or assetCatalogs")

    catalog_projection_ids: set[str] = set()
    catalog_asset_ids: set[str] = set()
    for asset_catalog in asset_catalog_refs:
        asset_catalog_path = resolve_repo_relative(asset_catalog)
        catalog = load_json(asset_catalog_path)
        assets = catalog.get("assets")
        projections = catalog.get("projections")
        require(isinstance(assets, list) and assets, f"asset catalog {asset_catalog} missing assets")
        require(isinstance(projections, list) and projections, f"asset catalog {asset_catalog} missing projections")
        for asset in assets:
            asset_id = asset.get("assetId")
            require(asset_id, f"catalog {asset_catalog} asset missing assetId")
            require(asset.get("license"), f"catalog asset {asset_id} missing license")
            require(asset.get("quality", {}).get("productionGradeMetadata") is True, f"catalog asset {asset_id} missing production-grade quality metadata")
            require("translationNeeded" in asset.get("localization", {}), f"catalog asset {asset_id} missing localization posture")
            catalog_asset_ids.add(asset_id)
        for projection in projections:
            projection_id = projection.get("projectionId")
            require(projection_id, f"catalog {asset_catalog} projection missing projectionId")
            require(projection.get("pluginName"), f"catalog projection {projection_id} missing pluginName")
            require(isinstance(projection.get("assetIds"), list) and projection.get("assetIds"), f"catalog projection {projection_id} missing assetIds")
            for asset_id in projection.get("assetIds"):
                require(asset_id in catalog_asset_ids, f"catalog projection {projection_id} references unknown assetId {asset_id}")
            catalog_projection_ids.add(projection_id)
        messages.append(f"parsed {asset_catalog_path.relative_to(ROOT)}")

    installable_seen = False
    for entry in plugins:
        name = entry.get("name")
        require(isinstance(name, str) and name, "plugin entry missing name")
        source = entry.get("source")
        require(isinstance(source, dict), f"{name} missing source")
        require(source.get("source") == "local", f"{name} source.source must be local")
        source_path_raw = source.get("path")
        require(isinstance(source_path_raw, str), f"{name} missing source.path")
        require(source_path_raw.startswith("./plugins/"), f"{name} source.path must be under ./plugins")
        plugin_dir = resolve_repo_relative(source_path_raw)
        require(plugin_dir.exists() and plugin_dir.is_dir(), f"{name} source path does not exist: {source_path_raw}")
        require(plugin_dir.name == name, f"{name} source path folder must match plugin name")

        policy = entry.get("policy")
        require(isinstance(policy, dict), f"{name} missing policy")
        require(policy.get("installation") in {"AVAILABLE", "NOT_AVAILABLE", "INSTALLED_BY_DEFAULT"}, f"{name} has invalid policy.installation")
        require(policy.get("authentication") in {"ON_INSTALL", "ON_USE"}, f"{name} has invalid policy.authentication")
        require(entry.get("category"), f"{name} missing category")

        manifest_path = plugin_dir / ".codex-plugin" / "plugin.json"
        require(manifest_path.exists(), f"{name} missing .codex-plugin/plugin.json")
        manifest = load_json(manifest_path)
        messages.append(f"parsed {manifest_path.relative_to(ROOT)}")
        require(manifest.get("name") == name, f"{name} manifest name mismatch")
        require(manifest.get("interface", {}).get("displayName"), f"{name} manifest missing interface.displayName")

        skills = manifest.get("skills")
        if skills is not None:
            require(isinstance(skills, str), f"{name} manifest skills must be a string when present")
            skills_path = resolve_repo_relative(skills, manifest_path.parent.parent)
            require(skills_path.exists() and skills_path.is_dir(), f"{name} declared skills path does not exist: {skills}")
            messages.append(f"verified {name} skills path {skills_path.relative_to(ROOT)}")

        license_meta = entry.get("license")
        provenance_meta = entry.get("provenance")
        quality_meta = entry.get("quality")
        localization_meta = entry.get("localization")
        projection_meta = entry.get("projection")
        require(isinstance(projection_meta, dict) and projection_meta.get("projectionId"), f"{name} missing projection metadata")
        require(projection_meta.get("projectionId") in catalog_projection_ids, f"{name} projectionId not found in asset catalogs")
        for asset_id in projection_meta.get("assetIds", []):
            require(asset_id in catalog_asset_ids, f"{name} projection references unknown assetId {asset_id}")
        require(isinstance(quality_meta, dict) and quality_meta.get("status"), f"{name} missing quality metadata")
        require(isinstance(localization_meta, dict) and "translationNeeded" in localization_meta, f"{name} missing localization metadata")

        if policy.get("installation") in {"AVAILABLE", "INSTALLED_BY_DEFAULT"}:
            installable_seen = True
            require(isinstance(license_meta, dict) and license_meta.get("clearance"), f"{name} installable projection missing license clearance")
            require(isinstance(provenance_meta, dict) and provenance_meta.get("sourceRecord"), f"{name} installable projection missing provenance sourceRecord")
            require(manifest.get("provenance", {}).get("mirroredThirdPartyContent") is False, f"{name} must declare no mirrored third-party content or add clearance")
            require(projection_meta.get("installToDo"), f"{name} installable projection must answer install this to do X")

        for rel_key in ("sourceRecord", "licenseRecord"):
            if isinstance(provenance_meta, dict) and rel_key in provenance_meta:
                ref_path = resolve_repo_relative(provenance_meta[rel_key])
                require(ref_path.exists(), f"{name} provenance {rel_key} does not exist")
                if ref_path.suffix == ".json":
                    load_json(ref_path)
                    messages.append(f"parsed {ref_path.relative_to(ROOT)}")

    require(installable_seen, "at least one installable projection is required")
    require(AUDIT.exists(), f"audit artifact missing: {AUDIT.relative_to(ROOT)}")
    messages.append(f"found audit artifact {AUDIT.relative_to(ROOT)}")

    # Guard against accidental copied upstream license/source blobs in plugin payloads without explicit clearance.
    suspicious_markers = [
        "Copyright (c) 2025 Jesse Vincent",
        "THE SOFTWARE IS PROVIDED \"AS IS\"",
    ]
    for plugin_file in (ROOT / "plugins").rglob("*"):
        if not plugin_file.is_file():
            continue
        text = plugin_file.read_text(encoding="utf-8", errors="ignore")
        for marker in suspicious_markers:
            require(marker not in text, f"potential mirrored upstream content marker found in {plugin_file.relative_to(ROOT)}")
    messages.append("verified no blocked upstream license/source markers in plugin payloads")

    return messages


def main() -> int:
    try:
        messages = validate_marketplace()
    except ValidationError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1

    print("Marketplace validation passed")
    for message in messages:
        print(f"- {message}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
