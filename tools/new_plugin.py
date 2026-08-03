"""Scaffold a new Codex marketplace plugin pack.

This is a repo-local scaffolder. It creates the minimum pack source files
required for `tools/run.py marketplace --apply` to finish the generated
indexes and bundle manifests.

Usage:
    py -3 tools/new_plugin.py --check <pack-name>
    py -3 tools/new_plugin.py --apply <pack-name>
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import sys
from typing import Any, Final

import shared_checkout
import yaml


REPO_ROOT: Final[Path] = Path(__file__).resolve().parent.parent
PLUGINS_DIR: Final[Path] = REPO_ROOT / "codex-marketplace" / "plugins"
PLUGIN_ROOTS: Final[Path] = REPO_ROOT / "codex-marketplace" / "plugin-roots.json"
TEMPLATE_PACK: Final[str] = "repo-worker-pack"
DISPLAY_PREFIX: Final[str] = " ".join(part.capitalize() for part in TEMPLATE_PACK.split("-"))


def _title_case(name: str) -> str:
    return " ".join(part.capitalize() for part in name.replace("_", "-").split("-"))


def _validate(name: str, check: bool) -> tuple[Path, Path] | None:
    if not name or not name.replace("-", "").replace("_", "").isalnum():
        print("error: pack name must be alphanumeric with hyphens/underscores only", file=sys.stderr)
        return None

    pack_dir = PLUGINS_DIR / name
    if pack_dir.exists():
        print(f"error: pack already exists: {pack_dir}", file=sys.stderr)
        return None

    if not PLUGIN_ROOTS.is_file():
        print(f"error: plugin roots file not found: {PLUGIN_ROOTS}", file=sys.stderr)
        return None

    with PLUGIN_ROOTS.open("r", encoding="utf-8") as f:
        roots = json.load(f)

    existing = {r["name"] for r in roots.get("roots", [])}
    if name in existing:
        print(f"error: pack already registered in {PLUGIN_ROOTS}", file=sys.stderr)
        return None

    if check:
        print(f"Would create pack {name!r} at {pack_dir}")

    return pack_dir, PLUGIN_ROOTS


def _plugin_json(name: str, pack_dir: Path) -> str:
    display = _title_case(name)
    return f"""{{
    "name": "{name}",
    "version": "1.0.0",
    "description": "{display} for Codex.",
    "author": {{
        "name": "Harley Bartles"
    }},
    "homepage": "https://github.com/HarleyBartles/agent-asset-marketplace",
    "repository": "https://github.com/HarleyBartles/agent-asset-marketplace",
    "license": "MIT",
    "keywords": [
        "codex",
        "marketplace",
        "{name}"
    ],
    "skills": "./skills/",
    "interface": {{
        "displayName": "{display}",
        "shortDescription": "{display} for Codex.",
        "longDescription": "First-party Codex marketplace plugin for {name}.",
        "developerName": "Harley Bartles",
        "category": "Productivity",
        "capabilities": [],
        "defaultPrompt": "Use {display} when the task is covered by the {name} skills.",
        "brandColor": "#111827",
        "composerIcon": "./assets/icon.svg",
        "logo": "./assets/icon.svg"
    }}
}}
"""


def _package_json(name: str) -> str:
    display = _title_case(name)
    return f"""{{
  "name": "@harleybartles/{name}",
  "version": "1.0.0",
  "description": "{display} for Codex.",
  "author": {{
    "name": "Harley Bartles"
  }},
  "homepage": "https://github.com/HarleyBartles/agent-asset-marketplace",
  "repository": {{
    "type": "git",
    "url": "git+https://github.com/HarleyBartles/agent-asset-marketplace.git",
    "directory": "codex-marketplace/plugins/{name}"
  }},
  "license": "MIT",
  "rights": "First-party Harley-authored marketplace plugin.",
  "keywords": [
    "codex",
    "marketplace",
    "{name}"
  ],
  "skills": "./skills/",
  "interface": {{
    "type": "cli",
    "displayName": "{display}",
    "shortDescription": "{display} for Codex.",
    "longDescription": "First-party Codex marketplace plugin for {name}.",
    "developerName": "Harley Bartles",
    "category": "Productivity",
    "capabilities": [],
    "defaultPrompt": "Use {display} when the task is covered by the {name} skills.",
    "brandColor": "#111827",
    "composerIcon": "./assets/icon.svg",
    "logo": "./assets/icon.svg"
  }}
}}
"""


def _readme(name: str) -> str:
    display = _title_case(name)
    return f"""# {display}

This bundle projects the first-party {name} skills.

## Bundle contents

### Documentation
- provenance and source mapping in `SOURCE.md`
- bundle inventory in `references/bundle-manifest.json`

## Boundary
- The first-party {name} skills stay bundled together as a focused {display} set.
- The bundle stays first-party only and does not absorb unrelated workflow packs.

## Install shape

Skills are installed from the Codex plugin roots under `codex-marketplace/plugins/<pack>/skills/<skill>/`.
"""


def _source(name: str) -> str:
    display = _title_case(name)
    return f"""# Source

This plugin projects the first-party {name} skills.

## Boundary
- The first-party {name} skills stay bundled together as a focused {display} set.
- The bundle stays first-party only and aligns to the current marketplace manifest.
"""


def _license() -> str:
    return """MIT License

Copyright (c) 2026 Harley Bartles

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


def _bundle_manifest(name: str) -> str:
    return f"""{{
  "bundle_name": "{name}",
  "bundle_version": "1.0.0",
  "bundle_type": "plugin-pack",
  "marketplace_root": ".agents/plugins/marketplace.json",
  "plugin_root": "codex-marketplace/plugins/{name}",
  "source_families": [
    "first_party"
  ],
  "notes": [
    "{name} combines first-party {name} skills."
  ],
  "provenance_refs": [],
  "plugin_author": "Harley Bartles",
  "plugin_license": "MIT",
  "entries": []
}}
"""


def _icon_svg() -> str:
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"'
        ' stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>'
        '<line x1="12" y1="8" x2="12" y2="16"></line>'
        '<line x1="8" y1="12" x2="16" y2="12"></line>'
        "</svg>"
    )


def _scaffold(pack_dir: Path, name: str) -> None:
    pack_dir.mkdir(parents=True, exist_ok=False)
    (pack_dir / ".codex-plugin").mkdir()
    (pack_dir / "assets").mkdir()
    (pack_dir / "references").mkdir()
    (pack_dir / "skills").mkdir()

    (pack_dir / ".codex-plugin" / "plugin.json").write_text(_plugin_json(name, pack_dir), encoding="utf-8")
    (pack_dir / "package.json").write_text(_package_json(name), encoding="utf-8")
    (pack_dir / "README.md").write_text(_readme(name), encoding="utf-8")
    (pack_dir / "SOURCE.md").write_text(_source(name), encoding="utf-8")
    (pack_dir / "LICENSE").write_text(_license(), encoding="utf-8")
    (pack_dir / "references" / "bundle-manifest.json").write_text(_bundle_manifest(name), encoding="utf-8")
    (pack_dir / "skills" / ".gitkeep").write_text("", encoding="utf-8")
    (pack_dir / "references" / ".gitkeep").write_text("", encoding="utf-8")

    template_icon = PLUGINS_DIR / TEMPLATE_PACK / "assets" / "icon.svg"
    if template_icon.is_file():
        shutil.copy(template_icon, pack_dir / "assets" / "icon.svg")
    else:
        (pack_dir / "assets" / "icon.svg").write_text(_icon_svg(), encoding="utf-8")


def _register_root(name: str) -> None:
    with PLUGIN_ROOTS.open("r", encoding="utf-8") as f:
        data = json.load(f)

    max_order = max((r.get("order", 0) for r in data.get("roots", [])), default=-1)
    data["roots"].append(
        {
            "order": max_order + 1,
            "name": name,
            "category": "Productivity",
            "registry_path": f"./codex-marketplace/plugins/{name}",
            "plugin_root": f"codex-marketplace/plugins/{name}",
            "manifest_path": f"codex-marketplace/plugins/{name}/.codex-plugin/plugin.json",
            "enabled": False,
        }
    )

    data["roots"].sort(key=lambda r: r["order"])

    with PLUGIN_ROOTS.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


def _read_skill_frontmatter(skill_path: Path) -> dict[str, Any] | None:
    text = skill_path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        return None
    try:
        end = lines.index("---", 1)
    except ValueError:
        return None
    try:
        return yaml.safe_load("\n".join(lines[1:end])) or {}
    except yaml.YAMLError:
        return None


def _skill_bundle_entry(skill_dir: Path, pack_name: str) -> dict[str, Any] | None:
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        return None

    front = _read_skill_frontmatter(skill_md)
    if not front:
        return None

    name = front.get("name")
    if not isinstance(name, str) or not name.strip():
        return None

    metadata = front.get("metadata") or {}
    source_category = metadata.get("source-category") or metadata.get("source_category") or "first_party"
    content_mode = metadata.get("content_mode") or "verbatim"
    source_path = (
        metadata.get("source-path")
        or metadata.get("source_path")
        or f"codex-marketplace/plugins/{pack_name}/skills/{name}/SKILL.md"
    )
    provenance_name = metadata.get("provenance-name") or metadata.get("provenance_name") or f"{name} first-party skill"

    source_family = source_category if source_category in {"first_party", "third_party"} else "first_party"
    family_display = "first-party" if source_family == "first_party" else "third-party"
    provenance_note = (
        metadata.get("provenance-note")
        or metadata.get("provenance_note")
        or f"Canonical {family_display} {name} skill. ({provenance_name})"
    )

    return {
        "canonical_name": name,
        "source_category": source_category,
        "content_mode": content_mode,
        "source_family": source_family,
        "canonical_source_path": f"codex-marketplace/plugins/{pack_name}/skills/{name}",
        "local_path": f"skills/{name}",
        "source_path": source_path,
        "copy_expectation": "byte_identical",
        "provenance_note": provenance_note,
    }


def _sync_bundle_manifest(pack_name: str) -> None:
    pack_dir = PLUGINS_DIR / pack_name
    bundle_path = pack_dir / "references" / "bundle-manifest.json"
    if not bundle_path.is_file():
        raise FileNotFoundError(bundle_path)

    with bundle_path.open("r", encoding="utf-8") as f:
        bundle = json.load(f)

    existing_entries = {e["canonical_name"]: e for e in bundle.get("entries", []) if "canonical_name" in e}

    entries: list[dict[str, Any]] = []
    skills_dir = pack_dir / "skills"
    if skills_dir.is_dir():
        for child in sorted(skills_dir.iterdir()):
            if child.is_dir() and not child.name.startswith("."):
                entry = _skill_bundle_entry(child, pack_name)
                if not entry:
                    continue
                old = existing_entries.get(entry["canonical_name"], {})
                provenance = old.get("provenance_note", entry["provenance_note"])
                # Preserve maintainer overrides for any field while still adding
                # newly discovered skills and derived defaults.
                entry = {**entry, **old, "provenance_note": provenance}
                entries.append(entry)

    bundle["entries"] = entries

    with bundle_path.open("w", encoding="utf-8") as f:
        json.dump(bundle, f, indent=2)
        f.write("\n")

    print(f"Synced bundle manifest for {pack_name}: {len(entries)} skill(s)")


def main() -> int:
    parser = argparse.ArgumentParser(description="Scaffold a new Codex marketplace plugin pack.")
    parser.add_argument("name", help="Pack name, e.g. 'mcp-usage-pack'")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--check", action="store_true", help="Dry-run report only")
    group.add_argument("--apply", action="store_true", help="Actually create the pack and register it")
    group.add_argument("--sync", action="store_true", help="Regenerate references/bundle-manifest.json from skills/")
    parser.add_argument(
        "--allow-shared-checkout", action="store_true", help="Allow scaffolding from a shared main checkout"
    )
    args = parser.parse_args()

    if (args.apply or args.sync) and not shared_checkout.approve_mutation(
        REPO_ROOT, "new_plugin.py", args.allow_shared_checkout
    ):
        return 1

    if args.sync:
        try:
            _sync_bundle_manifest(args.name)
            return 0
        except FileNotFoundError as e:
            print(f"error: pack not found: {e}", file=sys.stderr)
            return 1

    result = _validate(args.name, args.check)
    if result is None:
        return 1
    if args.check:
        return 0

    pack_dir, _ = result
    _scaffold(pack_dir, args.name)
    _register_root(args.name)
    print(f"Created pack at {pack_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
