#!/usr/bin/env python3
"""Reconcile the editable plugin-root inventory against the pack registry."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PACK_REGISTRY_PATH = ROOT / "codex-marketplace/custody-pack-registry.json"
PLUGIN_ROOT_INVENTORY_PATH = ROOT / "codex-marketplace/plugin-roots.json"


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _require_nonblank_string(value: Any, *, path: Path, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{path}: {field_name} must be a non-empty string")
    return value


def load_pack_registry() -> list[dict[str, Any]]:
    registry = load_json(PACK_REGISTRY_PATH)
    if registry.get("schema_version") != 1:
        raise ValueError(f"{PACK_REGISTRY_PATH}: schema_version must be 1")
    packs = registry.get("packs")
    if not isinstance(packs, list) or not packs:
        raise ValueError(f"{PACK_REGISTRY_PATH}: packs must be a non-empty list")
    if any(not isinstance(pack, dict) for pack in packs):
        raise ValueError(f"{PACK_REGISTRY_PATH}: packs must contain only objects")
    return packs


def _registry_root_record(pack: dict[str, Any], *, index: int) -> tuple[str, str, str]:
    name = _require_nonblank_string(pack.get("bundle_name"), path=PACK_REGISTRY_PATH, field_name=f"packs[{index}].bundle_name")
    plugin_root = _require_nonblank_string(
        pack.get("plugin_root"),
        path=PACK_REGISTRY_PATH,
        field_name=f"packs[{index}].plugin_root",
    )
    category = _require_nonblank_string(
        pack.get("category"),
        path=PACK_REGISTRY_PATH,
        field_name=f"packs[{index}].category",
    )
    return name, plugin_root, category


def reconcile_plugin_root_inventory() -> list[dict[str, Any]]:
    roots: list[dict[str, Any]] = []
    seen_names: set[str] = set()
    seen_plugin_roots: set[str] = set()
    for index, pack in enumerate(load_pack_registry()):
        name, plugin_root, category = _registry_root_record(pack, index=index)
        if name in seen_names:
            raise ValueError(f"{PACK_REGISTRY_PATH}: duplicate active root name {name}")
        if plugin_root in seen_plugin_roots:
            raise ValueError(f"{PACK_REGISTRY_PATH}: duplicate active plugin root {plugin_root}")
        seen_names.add(name)
        seen_plugin_roots.add(plugin_root)
        roots.append(
            {
                "order": index,
                "name": name,
                "category": category,
                "registry_path": f"./{plugin_root}",
                "plugin_root": plugin_root,
                "manifest_path": f"{plugin_root}/.codex-plugin/plugin.json",
                "enabled": True,
            }
        )
    return roots


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
            raise ValueError(f"{PLUGIN_ROOT_INVENTORY_PATH.relative_to(ROOT)} is stale; run py -3 tools/generate_plugin_root_inventory.py")
        print(f"OK {PLUGIN_ROOT_INVENTORY_PATH.relative_to(ROOT)}")
        print("OK plugin root inventory: current")
        return 0

    _write_inventory(PLUGIN_ROOT_INVENTORY_PATH, expected)
    print(f"Wrote {PLUGIN_ROOT_INVENTORY_PATH.relative_to(ROOT)}")
    print("OK plugin root inventory: generated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
