#!/usr/bin/env python3
"""Shared marketplace registry helpers."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT_INVENTORY_PATH = ROOT / "codex-marketplace/plugin-roots.json"
MARKETPLACE_PATH = ROOT / ".agents/plugins/marketplace.json"
CODEX_MARKETPLACE_MANIFEST_PATH = ROOT / "codex-marketplace/manifest.json"
REPO_INDEX_PATH = ROOT / "repo-index/repo-index.json"
REPO_INDEX_README_PATH = ROOT / "repo-index/README.md"
PLUGIN_MANIFEST_PATH = ROOT / "codex-marketplace/plugins/house-skills/.codex-plugin/plugin.json"
BUNDLE_MANIFEST_PATH = ROOT / "codex-marketplace/plugins/house-skills/references/bundle-manifest.json"
REPO_LOCAL_MARKETPLACE_POLICY_PATH = ROOT / "codex-marketplace/repo-local-marketplace-policy.json"
ADVENTURES_PACK_BUNDLE_MANIFEST_PATH = ROOT / "codex-marketplace/plugins/adventures-pack/references/bundle-manifest.json"
ADVENTURES_PACK_SOURCE_MAP_PATH = ROOT / "codex-marketplace/plugins/adventures-pack/references/source-map.md"
ADVENTURES_PACK_SKILL_PATH = ROOT / "codex-marketplace/plugins/adventures-pack/skills/adventures-pack/SKILL.md"
SOURCE_MAP_PATH = ROOT / "codex-marketplace/plugins/house-skills/references/source-map.md"
PLUGIN_README_PATH = ROOT / "codex-marketplace/plugins/house-skills/README.md"
PLUGIN_SKILL_PATH = ROOT / "codex-marketplace/plugins/house-skills/skills/house-skills/SKILL.md"
PLUGIN_BUNDLE_AGENTS_PATH = ROOT / "codex-marketplace/plugins/house-skills/AGENTS.md"
SOURCE_INTAKE_JSON_PATH = ROOT / "sources/first_party/skills/house-skills/intake.json"
PROVENANCE_PATH = ROOT / "provenance/house-skills.md"

MARKETPLACE_NOTES = [
    "Canonical Codex marketplace source layout.",
    "Active marketplace plugins are limited to the protected plugin roots only.",
]


def load_repo_local_marketplace_policy() -> dict[str, Any]:
    policy = json.loads(REPO_LOCAL_MARKETPLACE_POLICY_PATH.read_text(encoding="utf-8"))
    if not isinstance(policy, dict):
        raise ValueError(f"{REPO_LOCAL_MARKETPLACE_POLICY_PATH}: policy must be a mapping")

    defaults = policy.get("defaults", {})
    if not isinstance(defaults, dict):
        raise ValueError(f"{REPO_LOCAL_MARKETPLACE_POLICY_PATH}: defaults must be a mapping")
    installation = defaults.get("installation", "AVAILABLE")
    authentication = defaults.get("authentication", "ON_INSTALL")
    if not isinstance(installation, str) or not installation:
        raise ValueError(f"{REPO_LOCAL_MARKETPLACE_POLICY_PATH}: defaults.installation must be a string")
    if not isinstance(authentication, str) or not authentication:
        raise ValueError(f"{REPO_LOCAL_MARKETPLACE_POLICY_PATH}: defaults.authentication must be a string")

    install_defaults = policy.get("install_defaults", [])
    if not isinstance(install_defaults, list):
        raise ValueError(f"{REPO_LOCAL_MARKETPLACE_POLICY_PATH}: install_defaults must be a list")
    category_overrides = policy.get("category_overrides", {})
    if not isinstance(category_overrides, dict):
        raise ValueError(f"{REPO_LOCAL_MARKETPLACE_POLICY_PATH}: category_overrides must be a mapping")
    exclusions = policy.get("exclusions", [])
    if not isinstance(exclusions, list):
        raise ValueError(f"{REPO_LOCAL_MARKETPLACE_POLICY_PATH}: exclusions must be a list")

    return {
        "marketplace_name": policy.get("marketplace_name", "agent-asset-marketplace"),
        "display_name": policy.get("display_name", "Agent Asset Marketplace"),
        "defaults": {
            "installation": installation,
            "authentication": authentication,
        },
        "install_defaults": tuple(str(item) for item in install_defaults if str(item).strip()),
        "category_overrides": {
            str(key): str(value)
            for key, value in category_overrides.items()
            if str(key).strip() and str(value).strip()
        },
        "exclusions": tuple(str(item) for item in exclusions if str(item).strip()),
    }


REPO_LOCAL_MARKETPLACE_POLICY = load_repo_local_marketplace_policy()


def _installation_policy_for_plugin(plugin_name: str) -> str:
    if plugin_name in REPO_LOCAL_MARKETPLACE_POLICY["install_defaults"]:
        return "INSTALLED_BY_DEFAULT"
    return REPO_LOCAL_MARKETPLACE_POLICY["defaults"]["installation"]

EXPECTED_PLUGIN_NAME = "house-skills"
EXPECTED_PLUGIN_VERSION = "1.0.0"
EXPECTED_PLUGIN_ROOT = "codex-marketplace/plugins/house-skills"
EXPECTED_MARKETPLACE_ROOT = ".agents/plugins/marketplace.json"
EXPECTED_SOURCE_OF_TRUTH = [
    "sources/first_party/skills/house-skills/intake.json",
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


def _normalize_plugin_root_inventory_entry(entry: dict[str, Any], *, index: int) -> dict[str, Any]:
    if not isinstance(entry, dict):
        raise ValueError(f"{PLUGIN_ROOT_INVENTORY_PATH}: root inventory entry {index} must be an object")

    required_fields = ("name", "category", "registry_path", "plugin_root", "manifest_path", "order")
    normalized: dict[str, Any] = {}
    for field in required_fields:
        value = entry.get(field)
        if field == "order":
            if not isinstance(value, int):
                raise ValueError(f"{PLUGIN_ROOT_INVENTORY_PATH}: root inventory entry {index} requires integer order")
            normalized[field] = value
            continue
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{PLUGIN_ROOT_INVENTORY_PATH}: root inventory entry {index} requires {field}")
        normalized[field] = value

    enabled = entry.get("enabled", True)
    if not isinstance(enabled, bool):
        raise ValueError(f"{PLUGIN_ROOT_INVENTORY_PATH}: root inventory entry {index} enabled must be a boolean")
    normalized["enabled"] = enabled
    return normalized


def load_plugin_root_inventory() -> tuple[dict[str, Any], ...]:
    inventory = load_json(PLUGIN_ROOT_INVENTORY_PATH)
    if inventory.get("schema_version") != 1:
        raise ValueError(f"{PLUGIN_ROOT_INVENTORY_PATH}: schema_version must be 1")
    roots = inventory.get("roots")
    if not isinstance(roots, list) or not roots:
        raise ValueError(f"{PLUGIN_ROOT_INVENTORY_PATH}: roots must be a non-empty list")

    normalized = [_normalize_plugin_root_inventory_entry(entry, index=index) for index, entry in enumerate(roots)]
    normalized.sort(key=lambda entry: entry["order"])

    orders = [entry["order"] for entry in normalized if entry["enabled"]]
    if orders != list(range(len(orders))):
        raise ValueError(f"{PLUGIN_ROOT_INVENTORY_PATH}: enabled root orders must be contiguous starting at zero")

    names = [entry["name"] for entry in normalized if entry["enabled"]]
    if len(names) != len(set(names)):
        raise ValueError(f"{PLUGIN_ROOT_INVENTORY_PATH}: enabled root names must be unique")
    plugin_roots = [entry["plugin_root"] for entry in normalized if entry["enabled"]]
    if len(plugin_roots) != len(set(plugin_roots)):
        raise ValueError(f"{PLUGIN_ROOT_INVENTORY_PATH}: enabled plugin roots must be unique")
    manifest_paths = [entry["manifest_path"] for entry in normalized if entry["enabled"]]
    if len(manifest_paths) != len(set(manifest_paths)):
        raise ValueError(f"{PLUGIN_ROOT_INVENTORY_PATH}: enabled manifest paths must be unique")

    return tuple(normalized)


PLUGIN_ROOT_INVENTORY = load_plugin_root_inventory()
MARKETPLACE_PLUGIN_SPECS = [
    {
        "name": entry["name"],
        "category": entry["category"],
        "registry_path": entry["registry_path"],
        "plugin_root": entry["plugin_root"],
        "manifest_path": ROOT / entry["manifest_path"],
        "order": entry["order"],
        "enabled": entry["enabled"],
    }
    for entry in PLUGIN_ROOT_INVENTORY
    if entry["enabled"]
]
PROTECTED_MARKETPLACE_PLUGIN_SPECS = tuple(MARKETPLACE_PLUGIN_SPECS)
PROTECTED_MARKETPLACE_PLUGIN_NAMES = tuple(spec["name"] for spec in MARKETPLACE_PLUGIN_SPECS)
PROTECTED_MARKETPLACE_PLUGIN_ROOTS = tuple(spec["plugin_root"] for spec in MARKETPLACE_PLUGIN_SPECS)
PROTECTED_MARKETPLACE_PLUGIN_MANIFESTS = tuple(spec["manifest_path"] for spec in MARKETPLACE_PLUGIN_SPECS)

EXPECTED_MARKETPLACE = {
    "name": REPO_LOCAL_MARKETPLACE_POLICY["marketplace_name"],
    "interface": {
        "displayName": REPO_LOCAL_MARKETPLACE_POLICY["display_name"],
    },
    "plugins": [
        {
            "name": spec["name"],
            "source": {
                "source": "local",
                "path": spec["registry_path"],
            },
            "policy": {
                "installation": _installation_policy_for_plugin(spec["name"]),
                "authentication": "ON_INSTALL",
            },
            "category": REPO_LOCAL_MARKETPLACE_POLICY["category_overrides"].get(spec["name"], spec["category"]),
        }
        for spec in MARKETPLACE_PLUGIN_SPECS
        if spec["name"] not in REPO_LOCAL_MARKETPLACE_POLICY["exclusions"]
    ],
    "notes": MARKETPLACE_NOTES,
}

EXPECTED_ACTIVE_MARKETPLACE_PLUGIN_SPECS = tuple(EXPECTED_MARKETPLACE["plugins"])
EXPECTED_ACTIVE_MARKETPLACE_PLUGIN_NAMES = tuple(plugin["name"] for plugin in EXPECTED_ACTIVE_MARKETPLACE_PLUGIN_SPECS)


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
        if plugin_name in REPO_LOCAL_MARKETPLACE_POLICY["exclusions"]:
            continue
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
                    "installation": _installation_policy_for_plugin(plugin_name),
                    "authentication": REPO_LOCAL_MARKETPLACE_POLICY["defaults"]["authentication"],
                },
                "category": REPO_LOCAL_MARKETPLACE_POLICY["category_overrides"].get(plugin_name, spec["category"]),
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
