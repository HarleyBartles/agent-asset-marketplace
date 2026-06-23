from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import generate_marketplace  # noqa: E402
import generate_repo_index  # noqa: E402


class GeneratorCheckModeTests(unittest.TestCase):
    def test_generate_marketplace_check_detects_stale_registry_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            decisions_path = temp_root / "sources" / "first_party" / "skills" / "house-skills" / "decisions.json"
            intake_path = temp_root / "sources" / "first_party" / "skills" / "house-skills" / "intake.json"
            plugin_manifest_path = temp_root / "codex-marketplace" / "plugins" / "demo" / ".codex-plugin" / "plugin.json"
            marketplace_path = temp_root / ".agents" / "plugins" / "marketplace.json"
            codex_manifest_path = temp_root / "codex-marketplace" / "manifest.json"

            decisions_path.parent.mkdir(parents=True, exist_ok=True)
            intake_path.parent.mkdir(parents=True, exist_ok=True)
            plugin_manifest_path.parent.mkdir(parents=True, exist_ok=True)
            marketplace_path.parent.mkdir(parents=True, exist_ok=True)
            codex_manifest_path.parent.mkdir(parents=True, exist_ok=True)

            decisions_path.write_text('[{"source_id":"demo","import_state":"imported"}]\n', encoding="utf-8")
            intake_path.write_text('{"imports":[{"source_id":"demo"}]}\n', encoding="utf-8")
            plugin_manifest_path.write_text('{"name":"demo","skills":"skills"}\n', encoding="utf-8")

            expected_manifest = {
                "name": "agent-asset-marketplace",
                "interface": {"displayName": "Agent Asset Marketplace"},
                "plugins": [
                    {
                        "name": "demo",
                        "source": {"source": "local", "path": "./demo"},
                        "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
                        "category": "demo",
                    }
                ],
                "notes": ["generated"],
            }
            rendered = json.dumps(expected_manifest, indent=2) + "\n"
            marketplace_path.write_text(rendered, encoding="utf-8")
            codex_manifest_path.write_text(rendered, encoding="utf-8")

            with (
                patch.object(generate_marketplace, "ROOT", temp_root),
                patch.object(generate_marketplace, "SOURCE_DECISIONS_JSON_PATH", decisions_path),
                patch.object(generate_marketplace, "SOURCE_INTAKE_JSON_PATH", intake_path),
                patch.object(generate_marketplace, "MARKETPLACE_PATH", marketplace_path),
                patch.object(generate_marketplace, "CODEX_MARKETPLACE_MANIFEST_PATH", codex_manifest_path),
                patch.object(
                    generate_marketplace,
                    "MARKETPLACE_PLUGIN_SPECS",
                    ({"manifest_path": plugin_manifest_path},),
                ),
                patch.object(generate_marketplace, "build_marketplace_manifest", return_value=expected_manifest),
                patch.object(generate_marketplace, "EXPECTED_MARKETPLACE", expected_manifest),
                patch.object(sys, "argv", ["generate_marketplace.py", "--check"]),
            ):
                self.assertEqual(generate_marketplace.main(), 0)

            marketplace_path.write_text(rendered.replace("generated", "stale"), encoding="utf-8")
            with (
                patch.object(generate_marketplace, "ROOT", temp_root),
                patch.object(generate_marketplace, "SOURCE_DECISIONS_JSON_PATH", decisions_path),
                patch.object(generate_marketplace, "SOURCE_INTAKE_JSON_PATH", intake_path),
                patch.object(generate_marketplace, "MARKETPLACE_PATH", marketplace_path),
                patch.object(generate_marketplace, "CODEX_MARKETPLACE_MANIFEST_PATH", codex_manifest_path),
                patch.object(
                    generate_marketplace,
                    "MARKETPLACE_PLUGIN_SPECS",
                    ({"manifest_path": plugin_manifest_path},),
                ),
                patch.object(generate_marketplace, "build_marketplace_manifest", return_value=expected_manifest),
                patch.object(generate_marketplace, "EXPECTED_MARKETPLACE", expected_manifest),
                patch.object(sys, "argv", ["generate_marketplace.py", "--check"]),
            ):
                with self.assertRaises(ValueError):
                    generate_marketplace.main()

    def test_generate_repo_index_check_detects_stale_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            repo_index_path = temp_root / "repo-index" / "repo-index.json"
            repo_index_path.parent.mkdir(parents=True, exist_ok=True)

            expected_repo_index = {
                "schema_version": 1,
                "repo_name": "agent-asset-marketplace",
                "description": "Navigation metadata for the agent asset marketplace.",
                "marketplace_root_inventory_path": "codex-marketplace/plugin-roots.json",
                "marketplace_registry_path": ".agents/plugins/marketplace.json",
                "codex_marketplace_manifest_path": "codex-marketplace/manifest.json",
                "validation": {
                    "marketplace": "py -3 tools/validate_marketplace.py",
                    "marketplace_generate": "py -3 tools/generate_marketplace.py",
                    "marketplace_check": "py -3 tools/generate_marketplace.py --check",
                    "repo_index": "py -3 tools/validate_repo_index.py",
                    "repo_index_generate": "py -3 tools/generate_repo_index.py",
                    "repo_index_check": "py -3 tools/generate_repo_index.py --check",
                },
                "zones": [],
                "marketplace_plugins": [],
            }
            rendered = json.dumps(expected_repo_index, indent=2, ensure_ascii=False) + "\n"
            repo_index_path.write_text(rendered, encoding="utf-8")

            with (
                patch.object(generate_repo_index, "ROOT", temp_root),
                patch.object(generate_repo_index, "REPO_INDEX_PATH", repo_index_path),
                patch.object(generate_repo_index, "build_repo_index", return_value=expected_repo_index),
                patch.object(sys, "argv", ["generate_repo_index.py", "--check"]),
            ):
                self.assertEqual(generate_repo_index.main(), 0)

            repo_index_path.write_text(rendered.replace("Navigation metadata", "stale"), encoding="utf-8")
            with (
                patch.object(generate_repo_index, "ROOT", temp_root),
                patch.object(generate_repo_index, "REPO_INDEX_PATH", repo_index_path),
                patch.object(generate_repo_index, "build_repo_index", return_value=expected_repo_index),
                patch.object(sys, "argv", ["generate_repo_index.py", "--check"]),
            ):
                with self.assertRaises(ValueError):
                    generate_repo_index.main()


if __name__ == "__main__":
    unittest.main()
