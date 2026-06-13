#!/usr/bin/env python3
"""Shared marketplace registry helpers."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MARKETPLACE_PATH = ROOT / ".agents/plugins/marketplace.json"
CODEX_MARKETPLACE_MANIFEST_PATH = ROOT / "codex-marketplace/manifest.json"
REPO_INDEX_PATH = ROOT / "repo-index/repo-index.json"
REPO_INDEX_README_PATH = ROOT / "repo-index/README.md"
PLUGIN_MANIFEST_PATH = ROOT / "codex-marketplace/plugins/house-skills/.codex-plugin/plugin.json"
BUNDLE_MANIFEST_PATH = ROOT / "codex-marketplace/plugins/house-skills/skills/house-skills/references/bundle-manifest.json"
ADVENTURES_PACK_BUNDLE_MANIFEST_PATH = ROOT / "codex-marketplace/plugins/adventures-pack/references/bundle-manifest.json"
ADVENTURES_PACK_SOURCE_MAP_PATH = ROOT / "codex-marketplace/plugins/adventures-pack/references/source-map.md"
ADVENTURES_PACK_SKILL_PATH = ROOT / "codex-marketplace/plugins/adventures-pack/skills/adventures-pack/SKILL.md"
SOURCE_MAP_PATH = ROOT / "codex-marketplace/plugins/house-skills/skills/house-skills/references/source-map.md"
PLUGIN_README_PATH = ROOT / "codex-marketplace/plugins/house-skills/README.md"
PLUGIN_SKILL_PATH = ROOT / "codex-marketplace/plugins/house-skills/skills/house-skills/SKILL.md"
PLUGIN_BUNDLE_AGENTS_PATH = ROOT / "codex-marketplace/plugins/house-skills/AGENTS.md"
SOURCE_DECISIONS_MD_PATH = ROOT / "sources/house-skills/decisions.md"
SOURCE_DECISIONS_JSON_PATH = ROOT / "sources/house-skills/decisions.json"
SOURCE_INTAKE_JSON_PATH = ROOT / "sources/house-skills/intake.json"
PROVENANCE_PATH = ROOT / "provenance/house-skills.md"

MARKETPLACE_NOTES = [
    "Canonical Codex marketplace source layout.",
    "Active marketplace plugins are limited to the protected plugin roots only.",
]

PROTECTED_MARKETPLACE_PLUGIN_SPECS: tuple[dict[str, str | Path], ...] = (
    {
        "name": "house-skills",
        "registry_path": "./codex-marketplace/plugins/house-skills",
        "plugin_root": "codex-marketplace/plugins/house-skills",
        "manifest_path": PLUGIN_MANIFEST_PATH,
    },
    {
        "name": "adventures-pack",
        "registry_path": "./codex-marketplace/plugins/adventures-pack",
        "plugin_root": "codex-marketplace/plugins/adventures-pack",
        "manifest_path": ROOT / "codex-marketplace/plugins/adventures-pack/.codex-plugin/plugin.json",
    },
    {
        "name": "unslop",
        "registry_path": "./codex-marketplace/plugins/unslop",
        "plugin_root": "codex-marketplace/plugins/unslop",
        "manifest_path": ROOT / "codex-marketplace/plugins/unslop/.codex-plugin/plugin.json",
    },
    {
        "name": "game-studio",
        "registry_path": "./codex-marketplace/plugins/game-studio",
        "plugin_root": "codex-marketplace/plugins/game-studio",
        "manifest_path": ROOT / "codex-marketplace/plugins/game-studio/.codex-plugin/plugin.json",
    },
)

MARKETPLACE_PLUGIN_SPECS = list(PROTECTED_MARKETPLACE_PLUGIN_SPECS)
PROTECTED_MARKETPLACE_PLUGIN_NAMES = tuple(spec["name"] for spec in PROTECTED_MARKETPLACE_PLUGIN_SPECS)
PROTECTED_MARKETPLACE_PLUGIN_ROOTS = tuple(spec["plugin_root"] for spec in PROTECTED_MARKETPLACE_PLUGIN_SPECS)

EXPECTED_MARKETPLACE = {
    "name": "agent-asset-marketplace",
    "interface": {
        "displayName": "Agent Asset Marketplace",
    },
    "plugins": [
        {
            "name": spec["name"],
            "source": {
                "source": "local",
                "path": spec["registry_path"],
            },
            "policy": {
                "installation": "AVAILABLE",
                "authentication": "ON_INSTALL",
            },
            "category": "Productivity",
        }
        for spec in MARKETPLACE_PLUGIN_SPECS
    ],
    "notes": MARKETPLACE_NOTES,
}

EXPECTED_PLUGIN_NAME = "house-skills"
EXPECTED_PLUGIN_VERSION = "1.0.0"
EXPECTED_PLUGIN_ROOT = "codex-marketplace/plugins/house-skills"
EXPECTED_MARKETPLACE_ROOT = ".agents/plugins/marketplace.json"
EXPECTED_SOURCE_OF_TRUTH = [
    "sources/house-skills/decisions.json",
    "sources/house-skills/decisions.md",
    "sources/house-skills/intake.json",
    "provenance/house-skills.md",
]

EXPECTED_COMPONENT_LANE_ORDER = {
    "base/control-plane": 0,
    "Adventures": 1,
    "Rooms": 2,
}


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_top_markdown_table(path: Path) -> list[dict[str, str]]:
    lines = load_text(path).splitlines()
    header: list[str] | None = None
    rows: list[dict[str, str]] = []
    in_table = False

    for line in lines:
        stripped = line.strip()
        if not stripped:
            if in_table:
                break
            continue
        if not stripped.startswith("|"):
            if in_table:
                break
            continue

        cells = [_normalize_markdown_cell(cell) for cell in stripped.strip("|").split("|")]
        if header is None:
            header = cells
            in_table = True
            continue

        if all(_is_separator_cell(cell) for cell in cells):
            continue

        if len(cells) != len(header):
            raise ValueError(f"{path}: malformed table row: {line}")

        rows.append(dict(zip(header, cells, strict=True)))

    if header is None:
        raise ValueError(f"{path}: no table found")

    return rows


def _is_separator_cell(cell: str) -> bool:
    cleaned = cell.replace("-", "").replace(":", "").strip()
    return cleaned == ""


def _normalize_markdown_cell(cell: str) -> str:
    value = cell.strip()
    if len(value) >= 2 and value.startswith("`") and value.endswith("`"):
        return value[1:-1]
    return value


def normalize_decision_record(record: dict[str, Any]) -> dict[str, Any]:
    if "source_id" in record:
        return {
            "issue": record.get("issue", ""),
            "source_id": record.get("source_id", ""),
            "source_path": record.get("source_path", ""),
            "public_name": record.get("public_name", ""),
            "provenance_name": record.get("provenance_name", ""),
            "import_state": record.get("import_state", ""),
            "scope": record.get("scope", ""),
            "notes": record.get("notes", ""),
        }

    return {
        "issue": record.get("issue", ""),
        "id": record.get("id", ""),
        "status": record.get("status", ""),
        "import_state": record.get("import_state", ""),
        "decision": record.get("decision", ""),
        "imported_source_paths": tuple(record.get("imported_source_paths", [])),
    }


def normalize_decision_row(row: dict[str, str]) -> dict[str, Any]:
    if row.get("source_id"):
        return {
            "issue": row.get("issue", ""),
            "source_id": row.get("source_id", ""),
            "source_path": row.get("source_path", ""),
            "public_name": row.get("public_name", ""),
            "provenance_name": row.get("provenance_name", ""),
            "import_state": row.get("import_state", ""),
            "scope": row.get("scope", ""),
            "notes": row.get("notes", ""),
        }

    return {
        "issue": row.get("issue", ""),
        "id": row.get("id", ""),
        "status": row.get("status", ""),
        "import_state": row.get("import_state", ""),
        "decision": row.get("decision", ""),
        "imported_source_paths": tuple(
            item.strip()
            for item in row.get("imported_source_paths", "").split(",")
            if item.strip()
        ),
    }


def build_marketplace_manifest(plugin_manifests: list[dict[str, Any]]) -> dict[str, Any]:
    plugin_manifest_by_name = {}
    for plugin_manifest in plugin_manifests:
        plugin_name = plugin_manifest.get("name")
        if not isinstance(plugin_name, str) or not plugin_name:
            raise ValueError("Unsupported plugin manifest without a valid name")
        if plugin_name in plugin_manifest_by_name:
            raise ValueError(f"Duplicate plugin manifest supplied for {plugin_name}")
        plugin_manifest_by_name[plugin_name] = plugin_manifest

    plugins: list[dict[str, Any]] = []
    registry_paths = {spec["name"]: spec["registry_path"] for spec in MARKETPLACE_PLUGIN_SPECS}
    for spec in MARKETPLACE_PLUGIN_SPECS:
        plugin_name = spec["name"]
        plugin_manifest = plugin_manifest_by_name.get(plugin_name)
        if not plugin_manifest:
            raise ValueError(f"Missing plugin manifest for protected marketplace root {plugin_name}")
        plugin_path = registry_paths.get(plugin_name)
        if not plugin_path:
            raise ValueError(f"Unsupported plugin manifest {plugin_name!r}")

        plugins.append(
            {
                "name": plugin_name,
                "source": {
                    "source": "local",
                    "path": plugin_path,
                },
                "policy": {
                    "installation": "AVAILABLE",
                    "authentication": "ON_INSTALL",
                },
                "category": plugin_manifest["interface"]["category"],
            }
        )

    return {
        "name": "agent-asset-marketplace",
        "interface": {
            "displayName": "Agent Asset Marketplace",
        },
        "plugins": plugins,
        "notes": MARKETPLACE_NOTES,
    }
