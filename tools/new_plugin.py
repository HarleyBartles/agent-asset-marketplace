#!/usr/bin/env python3
"""Scaffold an inactive Codex product definition and its package assets."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import sys
from typing import Final

ROOT: Final[Path] = Path(__file__).resolve().parents[1]
DEFINITIONS: Final[Path] = ROOT / "src/plugin-definitions"
PLUGIN_ROOTS: Final[Path] = ROOT / "src/plugin-definitions/catalog.json"
TEMPLATE: Final[Path] = DEFINITIONS / "repo-worker-pack/files/assets/icon.svg"


def _display_name(name: str) -> str:
    return " ".join(part.capitalize() for part in name.replace("_", "-").split("-"))


def _license() -> str:
    return (ROOT / "LICENSE").read_text(encoding="utf-8")


def _validate(name: str, check: bool) -> Path | None:
    if not name or not name.replace("-", "").replace("_", "").isalnum():
        print("error: pack name must be alphanumeric with hyphens/underscores only", file=sys.stderr)
        return None
    definition = DEFINITIONS / name
    if definition.exists():
        print(f"error: product definition already exists: {definition}", file=sys.stderr)
        return None
    if not PLUGIN_ROOTS.is_file():
        print(f"error: plugin roots file not found: {PLUGIN_ROOTS}", file=sys.stderr)
        return None
    roots = json.loads(PLUGIN_ROOTS.read_text(encoding="utf-8"))
    if name in {row["name"] for row in roots.get("roots", [])}:
        print(f"error: pack already registered in {PLUGIN_ROOTS}", file=sys.stderr)
        return None
    if check:
        print(f"Would create inactive product definition {name!r} at {definition}")
    return definition


def _scaffold(definition: Path, name: str) -> None:
    display = _display_name(name)
    package_files = definition / "files"
    for directory in (package_files / "assets", package_files / "references"):
        directory.mkdir(parents=True, exist_ok=True)
    manifest = {
        "name": name,
        "version": "1.0.0",
        "description": f"{display} for Codex.",
        "author": {"name": "Harley Bartles"},
        "homepage": "https://github.com/HarleyBartles/agent-asset-marketplace",
        "repository": "https://github.com/HarleyBartles/agent-asset-marketplace",
        "license": "MIT",
        "keywords": ["codex", "marketplace", name],
        "skills": "./skills/",
        "interface": {
            "displayName": display,
            "shortDescription": f"{display} for Codex.",
            "longDescription": f"First-party Codex marketplace plugin for {name}.",
            "developerName": "Harley Bartles",
            "category": "Productivity",
            "capabilities": [],
            "defaultPrompt": f"Use {display} when the task is covered by its installed skills.",
            "brandColor": "#111827",
            "composerIcon": "./assets/icon.svg",
            "logo": "./assets/icon.svg",
        },
    }
    (definition / "plugin.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    (definition / "contents.json").write_text(
        json.dumps({"enabled": False, "skills": []}, indent=2) + "\n", encoding="utf-8"
    )
    bundle = {
        "bundle_name": name,
        "bundle_version": "1.0.0",
        "bundle_type": "plugin-pack",
        "marketplace_root": ".agents/plugins/marketplace.json",
        "plugin_root": f"dist/plugins/{name}",
        "source_families": ["first_party"],
        "notes": [f"{display} is assembled from first-party skill source."],
        "provenance_refs": [],
        "plugin_author": "Harley Bartles",
        "plugin_license": "MIT",
    }
    (definition / "bundle.json").write_text(json.dumps(bundle, indent=2) + "\n", encoding="utf-8")
    package = {
        "name": f"@harleybartles/{name}",
        "version": "1.0.0",
        "description": f"{display} for Codex.",
        "license": "MIT",
        "skills": "./skills/",
    }
    (package_files / "package.json").write_text(json.dumps(package, indent=2) + "\n", encoding="utf-8")
    (package_files / "LICENSE").write_text(_license(), encoding="utf-8")
    (package_files / "README.md").write_text(
        f"# {display}\n\nThis plugin is assembled from first-party sources declared in "
        f"`src/plugin-definitions/{name}/contents.json`.\n",
        encoding="utf-8",
    )
    (package_files / "SOURCE.md").write_text(
        "# Source\n\nThis product is first-party. Record adaptations, upstream attribution, and applicable "
        "license conditions in its source definitions.\n",
        encoding="utf-8",
    )
    if TEMPLATE.is_file():
        shutil.copyfile(TEMPLATE, package_files / "assets/icon.svg")
    _register_root(name)


def _register_root(name: str) -> None:
    data = json.loads(PLUGIN_ROOTS.read_text(encoding="utf-8"))
    roots = data.setdefault("roots", [])
    order = max((row.get("order", -1) for row in roots), default=-1) + 1
    roots.append(
        {
            "order": order,
            "name": name,
            "category": "Productivity",
            "registry_path": f"./dist/plugins/{name}",
            "plugin_root": f"dist/plugins/{name}",
            "manifest_path": f"dist/plugins/{name}/.codex-plugin/plugin.json",
            "enabled": False,
        }
    )
    PLUGIN_ROOTS.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Scaffold a source-first Codex plugin definition. (mutating)")
    parser.add_argument("name", nargs="?", help="Product name, e.g. 'mcp-usage-pack'")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="Report without writing")
    mode.add_argument("--apply", action="store_true", help="Create product definition and inactive inventory entry")
    args = parser.parse_args(argv)
    if args.name is None:
        print("error: product name is required", file=sys.stderr)
        return 1
    definition = _validate(args.name, args.check)
    if definition is None:
        return 1
    if args.check:
        return 0
    _scaffold(definition, args.name)
    print(f"Created product definition at {definition}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
