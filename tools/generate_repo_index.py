#!/usr/bin/env python3
"""Regenerate the repo navigation index from marketplace registry surfaces."""

from __future__ import annotations

import json
from pathlib import Path

from marketplace_utils import MARKETPLACE_PATH, REPO_INDEX_PATH, load_json


ROOT = Path(__file__).resolve().parents[1]
REPO_WORKER_BASE_ENTRY = {
    "name": "repo-worker-base",
    "plugin_root": "codex-marketplace/plugins/repo-worker-base",
    "plugin_manifest": "codex-marketplace/plugins/repo-worker-base/.codex-plugin/plugin.json",
    "source_md": "codex-marketplace/plugins/repo-worker-base/SOURCE.md",
    "source_ledger": [],
    "license_path": "codex-marketplace/plugins/repo-worker-base/LICENSE",
    "bundle_manifest": None,
    "skills_path": "codex-marketplace/plugins/repo-worker-base/skills",
    "provenance_refs": ["provenance/repo-worker-base.md"],
    "agents_md": None,
    "registry_path": "./codex-marketplace/plugins/repo-worker-base",
    "registry_alignment": {
        "status": "aligned",
        "note": None,
    },
}


def build_repo_index() -> dict:
    marketplace = load_json(MARKETPLACE_PATH)
    repo_index = load_json(REPO_INDEX_PATH)
    registry_plugins = {plugin["name"]: plugin for plugin in marketplace.get("plugins", [])}

    current_plugins = {entry["name"]: entry for entry in repo_index.get("marketplace_plugins", [])}
    ordered_plugins: list[dict] = []
    for plugin in marketplace.get("plugins", []):
        name = plugin.get("name")
        if not isinstance(name, str) or not name:
            raise ValueError("marketplace registry contains a malformed plugin name")

        if name in current_plugins:
            ordered_plugins.append(current_plugins[name])
            continue
        if name == "repo-worker-base":
            ordered_plugins.append(dict(REPO_WORKER_BASE_ENTRY))
            continue
        raise ValueError(f"repo-index generator does not know how to synthesize marketplace plugin {name}")

    repo_index["marketplace_plugins"] = ordered_plugins
    validation = dict(repo_index.get("validation", {}))
    validation["repo_index_generate"] = "py -3 tools/generate_repo_index.py"
    repo_index["validation"] = validation
    return repo_index


def main() -> int:
    repo_index = build_repo_index()
    rendered = json.dumps(repo_index, indent=2, ensure_ascii=False)
    REPO_INDEX_PATH.write_text(rendered + "\n", encoding="utf-8")
    print(f"Wrote {REPO_INDEX_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
