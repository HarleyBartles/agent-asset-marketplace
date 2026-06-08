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
UPSTREAM_VENDOR_ROOT = ROOT / "sources/vendor/jeremylongshore/claude-code-plugins-plus-skills/e773501f1dfb409fc71fccdaf6ac2898fedf66d6"
PLUGIN_MANIFEST_PATH = ROOT / "plugins/house-skills/.codex-plugin/plugin.json"
MARKETPLACE_FAMILY_PACK_PLUGIN_MANIFEST_PATH = ROOT / "codex-marketplace/plugins/marketplace-family-pack/.codex-plugin/plugin.json"
TESTING_SKILL_PACK_PLUGIN_MANIFEST_PATH = ROOT / "codex-marketplace/plugins/testing-skill-pack/.codex-plugin/plugin.json"
SUPABASE_PLATFORM_PACK_PLUGIN_MANIFEST_PATH = ROOT / "codex-marketplace/plugins/supabase-platform-pack/.codex-plugin/plugin.json"
VERCEL_PACK_PLUGIN_MANIFEST_PATH = ROOT / "codex-marketplace/plugins/vercel-pack/.codex-plugin/plugin.json"
SENTRY_PACK_PLUGIN_MANIFEST_PATH = ROOT / "codex-marketplace/plugins/sentry-pack/.codex-plugin/plugin.json"
OPENROUTER_PACK_PLUGIN_MANIFEST_PATH = ROOT / "codex-marketplace/plugins/openrouter-pack/.codex-plugin/plugin.json"
CURSOR_PACK_PLUGIN_MANIFEST_PATH = ROOT / "codex-marketplace/plugins/cursor-pack/.codex-plugin/plugin.json"
COHERE_PACK_PLUGIN_MANIFEST_PATH = ROOT / "codex-marketplace/plugins/cohere-pack/.codex-plugin/plugin.json"
DATABRICKS_PACK_PLUGIN_MANIFEST_PATH = ROOT / "codex-marketplace/plugins/databricks-pack/.codex-plugin/plugin.json"
FLYIO_PACK_PLUGIN_MANIFEST_PATH = ROOT / "codex-marketplace/plugins/flyio-pack/.codex-plugin/plugin.json"
ADVENTURES_PACK_PLUGIN_MANIFEST_PATH = ROOT / "codex-marketplace/plugins/adventures-pack/.codex-plugin/plugin.json"
BUNDLE_MANIFEST_PATH = ROOT / "plugins/house-skills/skills/house-skills/references/bundle-manifest.json"
TESTING_BUNDLE_MANIFEST_PATH = ROOT / "codex-marketplace/plugins/testing-skill-pack/references/bundle-manifest.json"
SUPABASE_BUNDLE_MANIFEST_PATH = ROOT / "codex-marketplace/plugins/supabase-platform-pack/references/bundle-manifest.json"
VERCEL_BUNDLE_MANIFEST_PATH = ROOT / "codex-marketplace/plugins/vercel-pack/references/bundle-manifest.json"
SENTRY_BUNDLE_MANIFEST_PATH = ROOT / "codex-marketplace/plugins/sentry-pack/references/bundle-manifest.json"
OPENROUTER_BUNDLE_MANIFEST_PATH = ROOT / "codex-marketplace/plugins/openrouter-pack/references/bundle-manifest.json"
CURSOR_BUNDLE_MANIFEST_PATH = ROOT / "codex-marketplace/plugins/cursor-pack/references/bundle-manifest.json"
COHERE_BUNDLE_MANIFEST_PATH = ROOT / "codex-marketplace/plugins/cohere-pack/references/bundle-manifest.json"
DATABRICKS_BUNDLE_MANIFEST_PATH = ROOT / "codex-marketplace/plugins/databricks-pack/references/bundle-manifest.json"
FLYIO_BUNDLE_MANIFEST_PATH = ROOT / "codex-marketplace/plugins/flyio-pack/references/bundle-manifest.json"
ADVENTURES_PACK_BUNDLE_MANIFEST_PATH = ROOT / "codex-marketplace/plugins/adventures-pack/references/bundle-manifest.json"
ADVENTURES_PACK_SOURCE_MAP_PATH = ROOT / "codex-marketplace/plugins/adventures-pack/references/source-map.md"
ADVENTURES_PACK_SKILL_PATH = ROOT / "codex-marketplace/plugins/adventures-pack/skills/adventures-pack/SKILL.md"
SOURCE_MAP_PATH = ROOT / "plugins/house-skills/skills/house-skills/references/source-map.md"
PLUGIN_README_PATH = ROOT / "plugins/house-skills/README.md"
PLUGIN_SKILL_PATH = ROOT / "plugins/house-skills/skills/house-skills/SKILL.md"
PLUGIN_BUNDLE_AGENTS_PATH = ROOT / "plugins/house-skills/AGENTS.md"
SOURCE_DECISIONS_MD_PATH = ROOT / "sources/house-skills/decisions.md"
SOURCE_DECISIONS_JSON_PATH = ROOT / "sources/house-skills/decisions.json"
SOURCE_INTAKE_JSON_PATH = ROOT / "sources/house-skills/intake.json"
PROVENANCE_PATH = ROOT / "provenance/house-skills.md"

MARKETPLACE_NOTES = [
    "Canonical Codex marketplace source layout.",
    "Codex wrapper plugins mirror upstream Claude plugin packages with .codex-plugin manifests.",
]

def discover_marketplace_plugin_specs() -> list[dict[str, str | Path]]:
    specs: list[dict[str, str | Path]] = [
        {
            "name": "house-skills",
            "registry_path": "./plugins/house-skills",
            "plugin_root": "plugins/house-skills",
            "manifest_path": PLUGIN_MANIFEST_PATH,
        },
    ]

    marketplace_plugins_root = ROOT / "codex-marketplace/plugins"
    if marketplace_plugins_root.exists():
        for plugin_dir in sorted(marketplace_plugins_root.iterdir(), key=lambda path: path.name):
            if not plugin_dir.is_dir():
                continue
            manifest_path = plugin_dir / ".codex-plugin" / "plugin.json"
            if not manifest_path.exists():
                continue
            specs.append(
                {
                    "name": plugin_dir.name,
                    "registry_path": f"./codex-marketplace/plugins/{plugin_dir.name}",
                    "plugin_root": f"codex-marketplace/plugins/{plugin_dir.name}",
                    "manifest_path": manifest_path,
                }
            )

    return specs


MARKETPLACE_PLUGIN_SPECS = discover_marketplace_plugin_specs()

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
EXPECTED_PLUGIN_ROOT = "plugins/house-skills"
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
    plugins: list[dict[str, Any]] = []
    registry_paths = {spec["name"]: spec["registry_path"] for spec in MARKETPLACE_PLUGIN_SPECS}
    for plugin_manifest in plugin_manifests:
        plugin_name = plugin_manifest["name"]
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
