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
import generate_pack_manifests  # noqa: E402
import generate_repo_index  # noqa: E402
import project_skills  # noqa: E402
import update_skill_artifacts  # noqa: E402


class GeneratorCheckModeTests(unittest.TestCase):
    @unittest.skip("skill zips and mega-packs removed")
    def test_generate_marketplace_check_detects_stale_registry_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            intake_path = temp_root / "sources" / "first_party" / "skills" / "house-skills" / "intake.json"
            plugin_manifest_path = temp_root / "codex-marketplace" / "plugins" / "demo" / ".codex-plugin" / "plugin.json"
            marketplace_path = temp_root / ".agents" / "plugins" / "marketplace.json"
            codex_manifest_path = temp_root / "codex-marketplace" / "manifest.json"

            intake_path.parent.mkdir(parents=True, exist_ok=True)
            plugin_manifest_path.parent.mkdir(parents=True, exist_ok=True)
            marketplace_path.parent.mkdir(parents=True, exist_ok=True)
            codex_manifest_path.parent.mkdir(parents=True, exist_ok=True)

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

    def test_generate_pack_manifests_check_detects_stale_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            manifest_path = temp_root / "codex-marketplace" / "plugins" / "sample-pack" / "references" / "bundle-manifest.json"
            manifest_path.parent.mkdir(parents=True, exist_ok=True)

            pack = {
                "bundle_name": "sample-pack",
                "plugin_root": "codex-marketplace/plugins/sample-pack",
                "bundle_version": "1.0.0",
                "bundle_type": "projection-lane",
                "is_mega_pack": False,
                "notes": ["generated"],
                "source_ledger": ["sources/third_party/game-studio/upstream/source-custody.md"],
                "provenance_refs": ["provenance/sample-pack.md"],
                "entries": [
                    {
                        "canonical_name": "sample-skill",
                        "source_category": "third_party",
                        "source_family": "game-studio",
                        "canonical_source_path": "sources/third_party/game-studio/upstream/skills/sample-skill",
                        "local_path": "skills/sample-skill",
                        "provenance_note": "Projected verbatim from retained Game Studio custody.",
                        "source_path": "sources/third_party/game-studio/upstream/skills/sample-skill/SKILL.md",
                        "source_author": "OpenAI",
                        "source_license": "MIT",
                        "source_repo": "openai/plugins",
                    }
                ],
            }
            expected_manifest = generate_pack_manifests._bundle_manifest(pack)
            manifest_path.write_text(json.dumps(expected_manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

            with (
                patch.object(generate_pack_manifests, "ROOT", temp_root),
                patch.object(generate_pack_manifests, "PACKS", [pack]),
                patch.object(sys, "argv", ["generate_pack_manifests.py", "--check"]),
            ):
                self.assertEqual(generate_pack_manifests.main(), 0)

            manifest_path.write_text(
                json.dumps({**expected_manifest, "notes": ["stale"]}, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
            with (
                patch.object(generate_pack_manifests, "ROOT", temp_root),
                patch.object(generate_pack_manifests, "PACKS", [pack]),
                patch.object(sys, "argv", ["generate_pack_manifests.py", "--check"]),
            ):
                with self.assertRaises(ValueError):
                    generate_pack_manifests.main()

    def test_generate_pack_manifests_refreshes_and_checks_generated_pack_docs(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            plugin_root = temp_root / "codex-marketplace" / "plugins" / "sample-pack"
            manifest_path = plugin_root / "references" / "bundle-manifest.json"
            manifest_path.parent.mkdir(parents=True, exist_ok=True)
            for doc_name, marker in (
                ("README.md", "bundle-contents"),
                ("SOURCE.md", "pack-inventory"),
                ("PROJECTION.md", "projection-contract"),
            ):
                (plugin_root / doc_name).write_text(
                    f"# Sample\n<!-- BEGIN GENERATED: {marker} -->\nstale\n<!-- END GENERATED: {marker} -->\n",
                    encoding="utf-8",
                )

            pack = {
                "bundle_name": "sample-pack",
                "plugin_root": "codex-marketplace/plugins/sample-pack",
                "bundle_version": "1.0.0",
                "bundle_type": "projection-lane",
                "is_mega_pack": False,
                "notes": ["generated"],
                "provenance_refs": ["provenance/sample-pack.md"],
                "generated_doc_surfaces": ["README.md", "SOURCE.md", "PROJECTION.md"],
                "entries": [
                    {
                        "canonical_name": "sample-skill",
                        "source_category": "third_party",
                        "source_family": "game-studio",
                        "canonical_source_path": "sources/third_party/game-studio/upstream/skills/sample-skill",
                        "local_path": "skills/sample-skill",
                        "provenance_note": "Projected verbatim from retained Game Studio custody.",
                    }
                ],
            }

            with (
                patch.object(generate_pack_manifests, "ROOT", temp_root),
                patch.object(generate_pack_manifests, "PACKS", [pack]),
            ):
                generate_pack_manifests.generate(write=True)

            for doc_name in ("README.md", "SOURCE.md", "PROJECTION.md"):
                rendered = (plugin_root / doc_name).read_text(encoding="utf-8")
                self.assertIn("sample-skill", rendered)
                self.assertNotIn("stale", rendered)

            readme_path = plugin_root / "README.md"
            readme_path.write_text(
                readme_path.read_text(encoding="utf-8").replace("sample-skill", "retired-skill"),
                encoding="utf-8",
            )
            with (
                patch.object(generate_pack_manifests, "ROOT", temp_root),
                patch.object(generate_pack_manifests, "PACKS", [pack]),
            ):
                with self.assertRaises(ValueError):
                    generate_pack_manifests.generate(write=False)

    @unittest.skip("skill zips and mega-packs removed")
    def test_project_skills_check_detects_stale_projection(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            source_root = temp_root / "sources" / "third_party" / "game-studio" / "upstream" / "skills" / "sample-skill"
            projected_root = temp_root / "codex-marketplace" / "plugins" / "sample-pack" / "skills" / "sample-skill"
            manifest_path = temp_root / "codex-marketplace" / "plugins" / "sample-pack" / "references" / "bundle-manifest.json"

            source_root.mkdir(parents=True, exist_ok=True)
            projected_root.mkdir(parents=True, exist_ok=True)
            manifest_path.parent.mkdir(parents=True, exist_ok=True)

            (source_root / "SKILL.md").write_text("---\nname: sample-skill\ndescription: sample\n---\n\nbody\n", encoding="utf-8")
            (projected_root / "SKILL.md").write_text("---\nname: sample-skill\ndescription: sample\n---\n\nbody\n", encoding="utf-8")

            manifest = {
                "bundle_name": "sample-pack",
                "bundle_version": "1.0.0",
                "bundle_type": "projection-lane",
                "plugin_root": "codex-marketplace/plugins/sample-pack",
                "is_mega_pack": False,
                "source_families": ["game-studio"],
                "notes": ["generated"],
                "provenance_refs": ["provenance/sample-pack.md"],
                "plugin_author": "Harley Bartles",
                "plugin_license": "MIT",
                "entries": [
                    {
                        "canonical_name": "sample-skill",
                        "source_category": "third_party",
                        "content_mode": "verbatim",
                        "source_family": "game-studio",
                        "canonical_source_path": "sources/third_party/game-studio/upstream/skills/sample-skill",
                        "local_path": "skills/sample-skill",
                        "provenance_note": "Projected verbatim from retained Game Studio custody.",
                        "source_path": "sources/third_party/game-studio/upstream/skills/sample-skill/SKILL.md",
                        "source_author": "OpenAI",
                        "source_license": "MIT",
                        "source_repo": "openai/plugins",
                        "copy_expectation": "byte_identical",
                        "import_status": "imported",
                    }
                ],
                "repo_index": {
                    "source_md": "codex-marketplace/plugins/sample-pack/SOURCE.md",
                    "bundle_manifest": "codex-marketplace/plugins/sample-pack/references/bundle-manifest.json",
                    "skills_path": "codex-marketplace/plugins/sample-pack/skills",
                    "agents_md": None,
                    "registry_alignment": {"status": "aligned", "note": None},
                },
            }
            manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

            with (
                patch.object(project_skills, "ROOT", temp_root),
                patch.object(project_skills, "GENERATED_SKILL_ZIPS_ROOT", temp_root / "generated/skill-zips"),
                patch.object(
                    project_skills,
                    "load_plugin_root_inventory",
                    return_value=[{"name": "sample-pack", "plugin_root": "codex-marketplace/plugins/sample-pack", "enabled": True}],
                ),
            ):
                project_skills.project_skills(write=True)

            (projected_root / "SKILL.md").write_text(
                "---\nname: sample-skill\ndescription: stale\n---\n\nbody\n",
                encoding="utf-8",
            )
            with (
                patch.object(project_skills, "ROOT", temp_root),
                patch.object(project_skills, "GENERATED_SKILL_ZIPS_ROOT", temp_root / "generated/skill-zips"),
                patch.object(
                    project_skills,
                    "load_plugin_root_inventory",
                    return_value=[{"name": "sample-pack", "plugin_root": "codex-marketplace/plugins/sample-pack", "enabled": True}],
                ),
            ):
                with self.assertRaises(ValueError):
                    project_skills.project_skills(write=False)

    @unittest.skip("skill zips and mega-packs removed")
    def test_project_skills_check_fails_on_stale_skill_roots(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            source_root = temp_root / "sources" / "third_party" / "game-studio" / "upstream" / "skills" / "sample-skill"
            projected_root = temp_root / "codex-marketplace" / "plugins" / "sample-pack" / "skills" / "sample-skill"
            stale_root = temp_root / "codex-marketplace" / "plugins" / "sample-pack" / "skills" / "retired-skill"
            manifest_path = temp_root / "codex-marketplace" / "plugins" / "sample-pack" / "references" / "bundle-manifest.json"

            source_root.mkdir(parents=True, exist_ok=True)
            projected_root.mkdir(parents=True, exist_ok=True)
            stale_root.mkdir(parents=True, exist_ok=True)
            manifest_path.parent.mkdir(parents=True, exist_ok=True)

            (source_root / "SKILL.md").write_text("---\nname: sample-skill\ndescription: sample\n---\n\nbody\n", encoding="utf-8")
            (projected_root / "SKILL.md").write_text("---\nname: sample-skill\ndescription: sample\n---\n\nbody\n", encoding="utf-8")
            (stale_root / "SKILL.md").write_text("---\nname: retired-skill\ndescription: stale\n---\n\nbody\n", encoding="utf-8")

            manifest = {
                "bundle_name": "sample-pack",
                "bundle_version": "1.0.0",
                "bundle_type": "projection-lane",
                "plugin_root": "codex-marketplace/plugins/sample-pack",
                "is_mega_pack": False,
                "source_families": ["game-studio"],
                "notes": ["generated"],
                "provenance_refs": ["provenance/sample-pack.md"],
                "plugin_author": "Harley Bartles",
                "plugin_license": "MIT",
                "entries": [
                    {
                        "canonical_name": "sample-skill",
                        "source_category": "third_party",
                        "content_mode": "verbatim",
                        "source_family": "game-studio",
                        "canonical_source_path": "sources/third_party/game-studio/upstream/skills/sample-skill",
                        "local_path": "skills/sample-skill",
                        "provenance_note": "Projected verbatim from retained Game Studio custody.",
                        "source_path": "sources/third_party/game-studio/upstream/skills/sample-skill/SKILL.md",
                        "source_author": "OpenAI",
                        "source_license": "MIT",
                        "source_repo": "openai/plugins",
                        "copy_expectation": "byte_identical",
                        "import_status": "imported",
                    }
                ],
                "repo_index": {
                    "source_md": "codex-marketplace/plugins/sample-pack/SOURCE.md",
                    "source_ledger": ["sources/third_party/game-studio/upstream/source-custody.md"],
                    "license_path": "codex-marketplace/plugins/sample-pack/LICENSE",
                    "bundle_manifest": "codex-marketplace/plugins/sample-pack/references/bundle-manifest.json",
                    "skills_path": "codex-marketplace/plugins/sample-pack/skills",
                    "provenance_refs": ["provenance/sample-pack.md"],
                    "agents_md": None,
                    "registry_alignment": {"status": "aligned", "note": None},
                },
            }
            manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

            with (
                patch.object(project_skills, "ROOT", temp_root),
                patch.object(project_skills, "GENERATED_SKILL_ZIPS_ROOT", temp_root / "generated/skill-zips"),
                patch.object(
                    project_skills,
                    "load_plugin_root_inventory",
                    return_value=[{"name": "sample-pack", "plugin_root": "codex-marketplace/plugins/sample-pack", "enabled": True}],
                ),
            ):
                project_skills.project_skills(write=True)

            stale_root.mkdir(parents=True, exist_ok=True)
            (stale_root / "SKILL.md").write_text("---\nname: retired-skill\ndescription: stale\n---\n\nbody\n", encoding="utf-8")

            with (
                patch.object(project_skills, "ROOT", temp_root),
                patch.object(project_skills, "GENERATED_SKILL_ZIPS_ROOT", temp_root / "generated/skill-zips"),
                patch.object(
                    project_skills,
                    "load_plugin_root_inventory",
                    return_value=[{"name": "sample-pack", "plugin_root": "codex-marketplace/plugins/sample-pack", "enabled": True}],
                ),
            ):
                with self.assertRaises(ValueError) as ctx:
                    project_skills.project_skills(write=False)

            self.assertIn("retired-skill", str(ctx.exception))

    @unittest.skip("skill zips and mega-packs removed")
    def test_project_skills_write_prunes_stale_skill_roots(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            source_root = temp_root / "sources" / "third_party" / "game-studio" / "upstream" / "skills" / "sample-skill"
            projected_root = temp_root / "codex-marketplace" / "plugins" / "sample-pack" / "skills" / "sample-skill"
            stale_root = temp_root / "codex-marketplace" / "plugins" / "sample-pack" / "skills" / "retired-skill"
            manifest_path = temp_root / "codex-marketplace" / "plugins" / "sample-pack" / "references" / "bundle-manifest.json"

            source_root.mkdir(parents=True, exist_ok=True)
            projected_root.mkdir(parents=True, exist_ok=True)
            stale_root.mkdir(parents=True, exist_ok=True)
            manifest_path.parent.mkdir(parents=True, exist_ok=True)

            (source_root / "SKILL.md").write_text("---\nname: sample-skill\ndescription: sample\n---\n\nbody\n", encoding="utf-8")
            (projected_root / "SKILL.md").write_text("---\nname: sample-skill\ndescription: sample\n---\n\nbody\n", encoding="utf-8")
            (stale_root / "SKILL.md").write_text("---\nname: retired-skill\ndescription: stale\n---\n\nbody\n", encoding="utf-8")

            manifest = {
                "bundle_name": "sample-pack",
                "bundle_version": "1.0.0",
                "bundle_type": "projection-lane",
                "plugin_root": "codex-marketplace/plugins/sample-pack",
                "is_mega_pack": False,
                "source_families": ["game-studio"],
                "notes": ["generated"],
                "provenance_refs": ["provenance/sample-pack.md"],
                "plugin_author": "Harley Bartles",
                "plugin_license": "MIT",
                "entries": [
                    {
                        "canonical_name": "sample-skill",
                        "source_category": "third_party",
                        "content_mode": "verbatim",
                        "source_family": "game-studio",
                        "canonical_source_path": "sources/third_party/game-studio/upstream/skills/sample-skill",
                        "local_path": "skills/sample-skill",
                        "provenance_note": "Projected verbatim from retained Game Studio custody.",
                        "source_path": "sources/third_party/game-studio/upstream/skills/sample-skill/SKILL.md",
                        "source_author": "OpenAI",
                        "source_license": "MIT",
                        "source_repo": "openai/plugins",
                        "copy_expectation": "byte_identical",
                        "import_status": "imported",
                    }
                ],
                "repo_index": {
                    "source_md": "codex-marketplace/plugins/sample-pack/SOURCE.md",
                    "source_ledger": ["sources/third_party/game-studio/upstream/source-custody.md"],
                    "license_path": "codex-marketplace/plugins/sample-pack/LICENSE",
                    "bundle_manifest": "codex-marketplace/plugins/sample-pack/references/bundle-manifest.json",
                    "skills_path": "codex-marketplace/plugins/sample-pack/skills",
                    "provenance_refs": ["provenance/sample-pack.md"],
                    "agents_md": None,
                    "registry_alignment": {"status": "aligned", "note": None},
                },
            }
            manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

            with (
                patch.object(project_skills, "ROOT", temp_root),
                patch.object(project_skills, "GENERATED_SKILL_ZIPS_ROOT", temp_root / "generated/skill-zips"),
                patch.object(
                    project_skills,
                    "load_plugin_root_inventory",
                    return_value=[{"name": "sample-pack", "plugin_root": "codex-marketplace/plugins/sample-pack", "enabled": True}],
                ),
            ):
                project_skills.project_skills(write=True)

            self.assertTrue(projected_root.exists())
            self.assertFalse(stale_root.exists())
            self.assertTrue((temp_root / "generated/skill-zips/sample-skill.zip").exists())

    @unittest.skip("skill zips and mega-packs removed")
    def test_update_skill_artifacts_check_runs_skill_artifact_pipeline(self) -> None:
        calls: list[tuple[str, dict[str, object]]] = []

        def record(name: str, result: object | None = None):
            def _inner(**kwargs):
                calls.append((name, dict(kwargs)))
                return result
            return _inner

        with (
            patch.object(update_skill_artifacts, "generate_all_mega_packs", side_effect=record("generate_all_mega_packs")),
            patch.object(update_skill_artifacts, "generate_pack_manifests", side_effect=record("generate_pack_manifests")),
            patch.object(update_skill_artifacts, "project_skills", side_effect=record("project_skills")),
            patch.object(update_skill_artifacts, "generate_first_party_skill_catalog", side_effect=record("generate_first_party_skill_catalog")),
            patch.object(update_skill_artifacts, "_run_tool") as run_tool_mock,
            patch.object(sys, "argv", ["update_skill_artifacts.py", "--check"]),
        ):
            self.assertEqual(update_skill_artifacts.main(), 0)

        self.assertEqual(
            calls,
            [
                ("generate_pack_manifests", {"write": False}),
                ("generate_all_mega_packs", {"write": False}),
                ("project_skills", {"write": False}),
                ("generate_first_party_skill_catalog", {"write": False}),
            ],
        )
        run_tool_mock.assert_called()


if __name__ == "__main__":
    unittest.main()
