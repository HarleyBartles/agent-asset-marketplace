#!/usr/bin/env python3
"""Shared marketplace registry helpers."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MARKETPLACE_PATH = ROOT / ".agents/plugins/marketplace.json"
CODEX_MARKETPLACE_MANIFEST_PATH = ROOT / "codex-marketplace/manifest.json"
PLUGIN_MANIFEST_PATH = ROOT / "plugins/house-skills/.codex-plugin/plugin.json"
MARKETPLACE_FAMILY_PACK_PLUGIN_MANIFEST_PATH = ROOT / "codex-marketplace/plugins/marketplace-family-pack/.codex-plugin/plugin.json"
TESTING_SKILL_PACK_PLUGIN_MANIFEST_PATH = ROOT / "codex-marketplace/plugins/testing-skill-pack/.codex-plugin/plugin.json"
BUNDLE_MANIFEST_PATH = ROOT / "plugins/house-skills/skills/house-skills/references/bundle-manifest.json"
TESTING_BUNDLE_MANIFEST_PATH = ROOT / "codex-marketplace/plugins/testing-skill-pack/references/bundle-manifest.json"
SOURCE_MAP_PATH = ROOT / "plugins/house-skills/skills/house-skills/references/source-map.md"
PLUGIN_README_PATH = ROOT / "plugins/house-skills/README.md"
PLUGIN_SKILL_PATH = ROOT / "plugins/house-skills/skills/house-skills/SKILL.md"
SOURCE_DECISIONS_MD_PATH = ROOT / "sources/house-skills/decisions.md"
SOURCE_DECISIONS_JSON_PATH = ROOT / "sources/house-skills/decisions.json"
SOURCE_INTAKE_JSON_PATH = ROOT / "sources/house-skills/intake.json"
PROVENANCE_PATH = ROOT / "provenance/house-skills.md"

MARKETPLACE_NOTES = [
    "Canonical Codex marketplace source layout.",
    "Codex wrapper plugins mirror upstream Claude plugin packages with .codex-plugin manifests.",
]

MARKETPLACE_PLUGIN_SPECS = [
    {
        "name": "house-skills",
        "registry_path": "./plugins/house-skills",
        "plugin_root": "plugins/house-skills",
        "manifest_path": PLUGIN_MANIFEST_PATH,
    },
    {
        "name": "marketplace-family-pack",
        "registry_path": "./codex-marketplace/plugins/marketplace-family-pack",
        "plugin_root": "codex-marketplace/plugins/marketplace-family-pack",
        "manifest_path": MARKETPLACE_FAMILY_PACK_PLUGIN_MANIFEST_PATH,
    },
    {
        "name": "testing-skill-pack",
        "registry_path": "./codex-marketplace/plugins/testing-skill-pack",
        "plugin_root": "codex-marketplace/plugins/testing-skill-pack",
        "manifest_path": TESTING_SKILL_PACK_PLUGIN_MANIFEST_PATH,
    },
    {
        "name": "fullstack-starter-pack",
        "registry_path": "./codex-marketplace/plugins/fullstack-starter-pack",
        "plugin_root": "codex-marketplace/plugins/fullstack-starter-pack",
        "manifest_path": ROOT / "codex-marketplace/plugins/fullstack-starter-pack/.codex-plugin/plugin.json",
    },
    {
        "name": "ai-experiment-logger",
        "registry_path": "./codex-marketplace/plugins/ai-experiment-logger",
        "plugin_root": "codex-marketplace/plugins/ai-experiment-logger",
        "manifest_path": ROOT / "codex-marketplace/plugins/ai-experiment-logger/.codex-plugin/plugin.json",
    },
    {
        "name": "conversational-api-debugger",
        "registry_path": "./codex-marketplace/plugins/conversational-api-debugger",
        "plugin_root": "codex-marketplace/plugins/conversational-api-debugger",
        "manifest_path": ROOT / "codex-marketplace/plugins/conversational-api-debugger/.codex-plugin/plugin.json",
    },
    {
        "name": "design-to-code",
        "registry_path": "./codex-marketplace/plugins/design-to-code",
        "plugin_root": "codex-marketplace/plugins/design-to-code",
        "manifest_path": ROOT / "codex-marketplace/plugins/design-to-code/.codex-plugin/plugin.json",
    },
    {
        "name": "domain-memory-agent",
        "registry_path": "./codex-marketplace/plugins/domain-memory-agent",
        "plugin_root": "codex-marketplace/plugins/domain-memory-agent",
        "manifest_path": ROOT / "codex-marketplace/plugins/domain-memory-agent/.codex-plugin/plugin.json",
    },
    {
        "name": "lumera-agent-memory",
        "registry_path": "./codex-marketplace/plugins/lumera-agent-memory",
        "plugin_root": "codex-marketplace/plugins/lumera-agent-memory",
        "manifest_path": ROOT / "codex-marketplace/plugins/lumera-agent-memory/.codex-plugin/plugin.json",
    },
    {
        "name": "pr-to-spec",
        "registry_path": "./codex-marketplace/plugins/pr-to-spec",
        "plugin_root": "codex-marketplace/plugins/pr-to-spec",
        "manifest_path": ROOT / "codex-marketplace/plugins/pr-to-spec/.codex-plugin/plugin.json",
    },
    {
        "name": "project-health-auditor",
        "registry_path": "./codex-marketplace/plugins/project-health-auditor",
        "plugin_root": "codex-marketplace/plugins/project-health-auditor",
        "manifest_path": ROOT / "codex-marketplace/plugins/project-health-auditor/.codex-plugin/plugin.json",
    },
    {
        "name": "slack-channel",
        "registry_path": "./codex-marketplace/plugins/slack-channel",
        "plugin_root": "codex-marketplace/plugins/slack-channel",
        "manifest_path": ROOT / "codex-marketplace/plugins/slack-channel/.codex-plugin/plugin.json",
    },
    {
        "name": "workflow-orchestrator",
        "registry_path": "./codex-marketplace/plugins/workflow-orchestrator",
        "plugin_root": "codex-marketplace/plugins/workflow-orchestrator",
        "manifest_path": ROOT / "codex-marketplace/plugins/workflow-orchestrator/.codex-plugin/plugin.json",
    },
    {
        "name": "x-bug-triage-plugin",
        "registry_path": "./codex-marketplace/plugins/x-bug-triage-plugin",
        "plugin_root": "codex-marketplace/plugins/x-bug-triage-plugin",
        "manifest_path": ROOT / "codex-marketplace/plugins/x-bug-triage-plugin/.codex-plugin/plugin.json",
    },
]

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
