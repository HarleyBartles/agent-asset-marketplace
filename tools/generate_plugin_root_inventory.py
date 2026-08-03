#!/usr/bin/env python3
"""Reconcile the editable plugin-root inventory against the plugin tree."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOTS_PATH = ROOT / "codex-marketplace" / "plugins"
PLUGIN_ROOT_INVENTORY_PATH = ROOT / "codex-marketplace" / "plugin-roots.json"


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _require_nonblank_string(value: Any, *, path: Path, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{path}: {field_name} must be a non-empty string")
    return value


def _scan_plugin_roots() -> list[dict[str, Any]]:
    roots: list[dict[str, Any]] = []
    seen_names: set[str] = set()
    seen_plugin_roots: set[str] = set()
    plugin_dirs = sorted(p for p in PLUGIN_ROOTS_PATH.iterdir() if p.is_dir())
    for index, plugin_path in enumerate(plugin_dirs):
        manifest_path = plugin_path / ".codex-plugin" / "plugin.json"
        if not manifest_path.is_file():
            continue
        manifest = load_json(manifest_path)
        name = _require_nonblank_string(
            manifest.get("name"),
            path=manifest_path,
            field_name="name",
        )
        category = _require_nonblank_string(
            manifest.get("interface", {}).get("category"),
            path=manifest_path,
            field_name="interface.category",
        )
        plugin_root = f"codex-marketplace/plugins/{plugin_path.name}"
        if name in seen_names:
            raise ValueError(f"{manifest_path}: duplicate active root name {name}")
        if plugin_root in seen_plugin_roots:
            raise ValueError(f"{manifest_path}: duplicate active plugin root {plugin_root}")
        seen_names.add(name)
        seen_plugin_roots.add(plugin_root)
        roots.append({
            "order": index,
            "name": name,
            "category": category,
            "registry_path": f"./{plugin_root}",
            "plugin_root": plugin_root,
            "manifest_path": f"{plugin_root}/.codex-plugin/plugin.json",
            "enabled": True,
        })
    return roots


def reconcile_plugin_root_inventory() -> list[dict[str, Any]]:
    scanned = _scan_plugin_roots()
    existing: dict[str, dict[str, Any]] = {}
    if PLUGIN_ROOT_INVENTORY_PATH.exists():
        current = load_json(PLUGIN_ROOT_INVENTORY_PATH)
        for root in current.get("roots", []):
            existing[root.get("name")] = root
    for root in scanned:
        if root["name"] in existing:
            root["enabled"] = existing[root["name"]].get("enabled", root["enabled"])
            root["order"] = existing[root["name"]].get("order", root["order"])
    return scanned


def _render_inventory(roots: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "description": "Editable inventory for the active Codex marketplace plugin roots.",
        "roots": roots,
    }


def _write_inventory(path: Path, inventory: dict[str, Any]) -> None:
    path.write_text(json.dumps(inventory, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate or validate the active marketplace plugin-root inventory")
    parser.add_argument("--check", action="store_true", help="validate without writing")
    args = parser.parse_args()

    expected = _render_inventory(reconcile_plugin_root_inventory())
    if args.check:
        if not PLUGIN_ROOT_INVENTORY_PATH.exists():
            raise FileNotFoundError(PLUGIN_ROOT_INVENTORY_PATH)
        current = load_json(PLUGIN_ROOT_INVENTORY_PATH)
        if current != expected:
            raise ValueError(
                f"{PLUGIN_ROOT_INVENTORY_PATH.relative_to(ROOT)} is stale; "
                "run py -3 tools/generate_plugin_root_inventory.py"
            )
        print(f"OK {PLUGIN_ROOT_INVENTORY_PATH.relative_to(ROOT)}")
        print("OK plugin root inventory: current")
        return 0

    _write_inventory(PLUGIN_ROOT_INVENTORY_PATH, expected)
    print(f"Wrote {PLUGIN_ROOT_INVENTORY_PATH.relative_to(ROOT)}")
    print("OK plugin root inventory: generated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
