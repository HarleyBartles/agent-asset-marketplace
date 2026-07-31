from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

# Superpowers upstream snapshot constants. Update these when the vendored
# superpowers source is refreshed to avoid hardcoding the version across tests.
SUPERPOWERS_VERSION = "v6.2.0"
SUPERPOWERS_COMMIT = "f2cbfbefebbfef77321e4c9abc9e949826bea9d7"
SUPERPOWERS_TAG_OBJECT = "ecbd610fce16d5faabcea997f17031129589b572"

import validate_marketplace  # noqa: E402
import superpowers_source  # noqa: E402
from skill_validation import validate_skill_markdown_frontmatter  # noqa: E402
from validate_marketplace import (  # noqa: E402
    _validate_projection_entry_provenance,
    _validate_repo_index_metadata,
    validate_skill_bundle_manifest,
    validate_superpowers_bundle_manifest,
)


def _touch(path: Path, content: str = "ok") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _first_party_projection_frontmatter(name: str, source_path: str, provenance_name: str, description: str) -> str:
    return (
        "---\n"
        f"name: {name}\n"
        f"description: {description}\n"
        "metadata:\n"
        f"  source-id: {name}\n"
        f"  source-path: {source_path}\n"
        f"  provenance-name: {provenance_name}\n"
        'license: "MIT"\n'
        "---\n"
    )


def _third_party_projection_frontmatter(name: str, upstream_name: str, overlay: str, description: str) -> str:
    return (
        "---\n"
        f"name: {name}\n"
        f"description: {description}\n"
        "metadata:\n"
        "  source_category: third_party\n"
        f"  upstream_name: {upstream_name}\n"
        f"  upstream_version: {SUPERPOWERS_VERSION}\n"
        f"  adaptation_overlay: {overlay}\n"
        "  projection_plugin: superpowers-plus\n"
        "---\n"
    )


def _write_superpowers_provenance_map(plugin_root: Path, bundle_manifest: dict) -> None:
    source_backed: list[dict[str, str]] = []
    adapted: list[dict[str, str]] = []
    for entry in bundle_manifest.get("entries", []):
        if not isinstance(entry, dict):
            continue
        record = {
            "canonical_name": entry["canonical_name"],
            "source_category": entry["source_category"],
            "content_mode": entry["content_mode"],
            "canonical_source_path": entry["canonical_source_path"],
            "local_path": f"codex-marketplace/plugins/superpowers-plus/{entry['local_path']}",
            "copy_expectation": entry["copy_expectation"],
            "provenance_note": entry["provenance_note"],
        }
        if entry.get("adaptation_overlay_path"):
            record["adaptation_overlay_path"] = entry["adaptation_overlay_path"]
        if entry.get("adaptation_note"):
            record["adaptation_note"] = entry["adaptation_note"]
        for field_name in ("source_path", "source_author", "source_license", "adapted_author"):
            if entry.get(field_name):
                record[field_name] = entry[field_name]
        if entry.get("source_category") == "first_party" or entry.get("content_mode") == "verbatim":
            source_backed.append(record)
        elif entry.get("content_mode") in ("adapted", "normalised"):
            adapted.append(record)

    provenance_map = {
        "bundle_name": "superpowers-plus",
        "bundle_version": "1.0.0",
        "upstream": {
            "repository": "https://github.com/obra/superpowers",
            "release_tag": SUPERPOWERS_VERSION,
            "release_commit": SUPERPOWERS_COMMIT,
            "tag_object": SUPERPOWERS_TAG_OBJECT,
            "license": "MIT",
        },
        "source_custody_root": f"sources/third_party/superpowers/obra-superpowers/{SUPERPOWERS_VERSION}",
        "active_projection_root": "codex-marketplace/plugins/superpowers-plus",
        "codex_surface": {
            "plugin_manifest": ".codex-plugin/plugin.json",
            "skills_root": "skills",
            "assets": [
                "assets/app-icon.png",
                "assets/superpowers-small.svg",
            ],
            "support_files": [
                "references/codex-marketplace-compatibility.md",
                "LICENSE",
                "SOURCE.md",
                "PROJECTION.md",
            ],
        },
        "source_backed_projections": source_backed,
        "adapted_projections": adapted,
        "source_only_surfaces": [
            {"path": ".claude-plugin", "reason": "Claude harness metadata stays in third-party source custody."},
            {"path": ".cursor-plugin", "reason": "Cursor harness metadata stays in third-party source custody."},
            {"path": ".opencode", "reason": "OpenCode harness metadata stays in third-party source custody."},
            {"path": "gemini-extension.json", "reason": "Gemini harness metadata stays in third-party source custody."},
            {"path": "CLAUDE.md", "reason": "Claude instructions stay in third-party source custody."},
            {"path": "GEMINI.md", "reason": "Gemini instructions stay in third-party source custody."},
            {"path": "hooks", "reason": "Hook definitions are source-only until Codex compatibility is proven."},
        ],
        "notes": [
            "The source custody root stays verbatim, the projection layer carries the "
            "Codex-marketplace adaptations, and the installation/export layer is "
            "regenerated from the projection.",
            "The active projection projects the first-party using-superpowers-plus "
            "workflow-selection entrypoint plus the compositional helper skills from "
            "first-party source custody.",
            "The harness-specific surfaces remain preserved in third-party source custody.",
            "The retained snapshot keeps the broader package boundary for provenance and review.",
        ],
    }
    _touch(plugin_root / "references" / "provenance-map.json", json.dumps(provenance_map, indent=2))


def _write_superpowers_plugin_manifests(source_root: Path, plugin_root: Path) -> None:
    _touch(
        source_root / ".codex-plugin" / "plugin.json",
        json.dumps({"name": "superpowers", "interface": {"displayName": "Superpowers"}}, indent=2),
    )
    _touch(
        plugin_root / ".codex-plugin" / "plugin.json",
        json.dumps({"name": "superpowers-plus", "interface": {"displayName": "Superpowers+"}}, indent=2),
    )


SUPERPOWERS_PROJECTION_DOC = """# Projection

This root is the Codex-facing marketplace projection of the first-party
Superpowers+ workflow skills, including the `using-superpowers-plus`
workflow-selection entrypoint.

## Layer Model

This repository uses two distinct layers for the Superpowers+ bundle:

- Source custody keeps the first-party skills in `sources/first_party/skills/<name>/`.
- Projection layer holds the source-controlled marketplace copy.
- Installation/export layer is derived from the projection and is produced only by canonical tooling.
- The custody flow is `source custody -> projection layer -> installation/export layer`.
- The projected skills are materialized from `sources/first_party/skills/...`.
- Frontmatter contract: docs/contracts/skill-frontmatter.md
- OpenAI agent contract: docs/contracts/openai-agent-yaml.md
"""

SUPERPOWERS_COMPATIBILITY_DOC = """# Codex Marketplace Compatibility

## Projection contract

- The repo-specific adaptation text lives only in the projection layer; the
  first-party source custody root is the editable surface and is not folded
  into the retained upstream snapshot.
- Source custody remains a verbatim retained upstream snapshot for reference.
- Installation and export artifacts are derived from the projection layer.
- Frontmatter contract: docs/contracts/skill-frontmatter.md
- OpenAI agent contract: docs/contracts/openai-agent-yaml.md
"""


class ValidateMarketplaceTests(unittest.TestCase):
    def setUp(self) -> None:
        # Bootstrap lazy imports so individual validator functions can be
        # called directly without running the full validate_marketplace flow.
        validate_marketplace._bootstrap_marketplace_dependencies()

    def test_validate_marketplace_runs_projection_materializer_check(self) -> None:
        with patch.object(
            validate_marketplace.subprocess,
            "run",
            return_value=subprocess.CompletedProcess(["py"], 0),
        ) as run_mock:
            validate_marketplace.validate_projection_materializer()
            run_mock.assert_called_once()
            self.assertEqual(
                run_mock.call_args.args[0],
                [sys.executable, "tools/project_skills.py", "--check"],
            )

    def test_validate_marketplace_runs_pack_manifest_check(self) -> None:
        with patch.object(
            validate_marketplace.subprocess,
            "run",
            return_value=subprocess.CompletedProcess(["py"], 0),
        ) as run_mock:
            validate_marketplace.validate_pack_manifests()
            run_mock.assert_called_once()
            self.assertEqual(
                run_mock.call_args.args[0],
                [sys.executable, "tools/generate_pack_manifests.py", "--check"],
            )

    def test_superpowers_bundle_accepts_first_party_inspecting_the_environment_projection(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            source_root = temp_root / "sources" / "third_party" / "superpowers" / "obra-superpowers" / "v6.2.0"
            source_skill_root = temp_root / "sources" / "first_party" / "skills" / "using-superpowers-plus"
            plugin_root = temp_root / "codex-marketplace" / "plugins" / "superpowers-plus"

            projected_skill_root = plugin_root / "skills" / "using-superpowers-plus"
            skill_md = _first_party_projection_frontmatter(
                "using-superpowers-plus",
                "sources/first_party/skills/using-superpowers-plus/SKILL.md",
                "Superpowers+ first-party workflow-selection entrypoint",
                "Use when starting workflow-sensitive work that may need a Superpowers workflow skill.",
            )
            _touch(
                source_skill_root / "SKILL.md",
                skill_md,
            )
            _touch(source_skill_root / "agents" / "openai.yaml", "model: gpt-5\n")
            _touch(projected_skill_root / "SKILL.md", skill_md)
            _touch(projected_skill_root / "agents" / "openai.yaml", "model: gpt-5\n")

            for rel_path in (
                "LICENSE",
                "SOURCE.md",
                "PROJECTION.md",
                "references/codex-marketplace-compatibility.md",
                "references/bundle-manifest.json",
                "references/provenance-map.json",
                "assets/app-icon.png",
                "assets/superpowers-small.svg",
            ):
                _touch(plugin_root / rel_path)
            _touch(plugin_root / "PROJECTION.md", SUPERPOWERS_PROJECTION_DOC)
            _touch(
                plugin_root / "references" / "codex-marketplace-compatibility.md",
                SUPERPOWERS_COMPATIBILITY_DOC,
            )

            for rel_path in (
                ".codex-plugin/plugin.json",
                "LICENSE",
                "README.md",
                "AGENTS.md",
                "package.json",
                "assets/app-icon.png",
                "assets/superpowers-small.svg",
            ):
                _touch(source_root / rel_path)

            for rel_path in (
                ".claude-plugin",
                ".cursor-plugin",
                ".opencode",
                "gemini-extension.json",
                "CLAUDE.md",
                "GEMINI.md",
                "hooks",
            ):
                target = source_root / rel_path
                if rel_path == "hooks":
                    target.mkdir(parents=True, exist_ok=True)
                else:
                    _touch(target)

            _write_superpowers_plugin_manifests(source_root, plugin_root)

            bundle_manifest = {
                "bundle_name": "superpowers-plus",
                "bundle_version": "1.0.0",
                "bundle_type": "third-party-codex-plugin-projection",
                "marketplace_root": ".agents/plugins/marketplace.json",
                "plugin_root": "codex-marketplace/plugins/superpowers-plus",
                "canonical_source_root": "sources/third_party/superpowers/obra-superpowers/v6.2.0",
                "source_tag": "v6.2.0",
                "source_commit": "f2cbfbefebbfef77321e4c9abc9e949826bea9d7",
                "license": "MIT",
                "plugin_author": "Harley Bartles",
                "plugin_license": "MIT",
                "projection_policy": (
                    "Project only the Codex-facing plugin surface. Keep the upstream "
                    "harness-specific metadata, docs, scripts, and hooks in third-party "
                    "source custody."
                ),
                "source_of_truth": [
                    "sources/third_party/superpowers/obra-superpowers/v6.2.0/.codex-plugin/plugin.json",
                    "sources/third_party/superpowers/obra-superpowers/v6.2.0/LICENSE",
                    "sources/third_party/superpowers/obra-superpowers/v6.2.0/README.md",
                    "sources/third_party/superpowers/obra-superpowers/v6.2.0/AGENTS.md",
                    "sources/third_party/superpowers/obra-superpowers/v6.2.0/package.json",
                ],
                "repo_index": {
                    "source_ledger": [
                        "sources/third_party/superpowers/obra-superpowers/v6.2.0/package.json",
                        "sources/third_party/superpowers/obra-superpowers/v6.2.0/README.md",
                    ],
                    "provenance_refs": [
                        "provenance/superpowers-plus.md",
                    ],
                    "agents_md": None,
                    "registry_alignment": {
                        "status": "aligned",
                        "note": None,
                    },
                },
                "candidate_count": 1,
                "imported_count": 1,
                "skipped_count": 0,
                "blocked_count": 0,
                "entries": [
                    {
                        "canonical_name": "using-superpowers-plus",
                        "source_category": "first_party",
                        "content_mode": "verbatim",
                        "canonical_source_path": "sources/first_party/skills/using-superpowers-plus",
                        "local_path": "skills/using-superpowers-plus",
                        "import_status": "imported",
                        "copy_expectation": "byte_identical",
                        "provenance_note": "Projected from the canonical first-party source.",
                    }
                ],
                "excluded": [
                    {"path": ".claude-plugin", "reason": "Claude harness metadata stays in third-party source custody."},
                    {"path": ".cursor-plugin", "reason": "Cursor harness metadata stays in third-party source custody."},
                    {"path": ".opencode", "reason": "OpenCode harness metadata stays in third-party source custody."},
                    {"path": "gemini-extension.json", "reason": "Gemini harness metadata stays in third-party source custody."},
                    {"path": "CLAUDE.md", "reason": "Claude instructions stay in third-party source custody."},
                    {"path": "GEMINI.md", "reason": "Gemini instructions stay in third-party source custody."},
                    {"path": "hooks", "reason": "Hook definitions are source-only until Codex compatibility is proven."},
                ],
            }
            _write_superpowers_provenance_map(plugin_root, bundle_manifest)

            with patch("validate_marketplace.ROOT", temp_root), patch("superpowers_source.ROOT", temp_root):
                try:
                    validate_superpowers_bundle_manifest(
                        bundle_manifest,
                        plugin_root="codex-marketplace/plugins/superpowers-plus",
                    )
                except ValueError as exc:  # pragma: no cover - exercised by the red test run
                    self.fail(f"validator rejected the first-party projection: {exc}")

    def test_validate_repo_index_metadata_accepts_current_shape(self) -> None:
        _validate_repo_index_metadata(
            {
                "source_md": "codex-marketplace/plugins/superpowers-plus/SOURCE.md",
                "bundle_manifest": "codex-marketplace/plugins/superpowers-plus/references/bundle-manifest.json",
                "skills_path": "codex-marketplace/plugins/superpowers-plus/skills",
                "agents_md": None,
                "registry_alignment": {"status": "aligned", "note": None},
            },
            bundle_name="superpowers-plus",
            plugin_root="codex-marketplace/plugins/superpowers-plus",
        )

    def test_validate_repo_index_metadata_rejects_bad_shape(self) -> None:
        with self.assertRaises(ValueError):
            _validate_repo_index_metadata(
                {
                    "source_md": "codex-marketplace/plugins/superpowers-plus/SOURCE.md",
                    "bundle_manifest": "codex-marketplace/plugins/superpowers-plus/references/bundle-manifest.json",
                    "skills_path": "codex-marketplace/plugins/superpowers-plus/skills",
                    "agents_md": "",
                    "registry_alignment": {"status": "aligned", "note": None},
                },
                bundle_name="superpowers-plus",
                plugin_root="codex-marketplace/plugins/superpowers-plus",
            )

    def test_validate_repo_index_metadata_rejects_bad_registry_alignment(self) -> None:
        with self.assertRaises(ValueError):
            _validate_repo_index_metadata(
                {
                    "source_md": "codex-marketplace/plugins/superpowers-plus/SOURCE.md",
                    "bundle_manifest": "codex-marketplace/plugins/superpowers-plus/references/bundle-manifest.json",
                    "skills_path": "codex-marketplace/plugins/superpowers-plus/skills",
                    "agents_md": None,
                    "registry_alignment": {"status": "intentional-delta", "note": ""},
                },
                bundle_name="superpowers-plus",
                plugin_root="codex-marketplace/plugins/superpowers-plus",
            )

    def test_context_safety_skill_requires_target_2000_and_limit_4000(self) -> None:
        source_skill = ROOT / "sources" / "first_party" / "skills" / "context-safety" / "SKILL.md"
        projected_skill = (
            ROOT
            / "codex-marketplace"
            / "plugins"
            / "repo-worker-pack"
            / "skills"
            / "context-safety"
            / "SKILL.md"
        )
        source_agent = ROOT / "sources" / "first_party" / "skills" / "context-safety" / "agents" / "openai.yaml"
        projected_agent = (
            ROOT
            / "codex-marketplace"
            / "plugins"
            / "repo-worker-pack"
            / "skills"
            / "context-safety"
            / "agents"
            / "openai.yaml"
        )

        for skill_path in (source_skill, projected_skill):
            text = skill_path.read_text(encoding="utf-8")
            self.assertIn("target 2,000 lines per chunk", text)
            self.assertIn("absolute red limit max 4,000 lines per chunk", text)
            self.assertIn("1,500 lines or more", text)

        for agent_path in (source_agent, projected_agent):
            text = agent_path.read_text(encoding="utf-8")
            self.assertIn("2,000 lines per chunk as the target", text)
            self.assertIn("4,000 lines per chunk as the absolute red limit", text)
            self.assertIn("1,500 lines or more", text)

    def test_superpowers_script_adapters_project_scripts_at_the_skill_root(self) -> None:
        cases = {
            "brainstorming": ["start-server.ps1", "stop-server.ps1"],
            "systematic-debugging": ["find-polluter.ps1"],
            "subagent-driven-development": [
                "AGENTS.md",
                "review-package",
                "review-package.ps1",
                "sdd-workspace",
                "sdd-workspace.ps1",
                "task-brief",
                "task-brief.ps1",
            ],
        }

        for skill_name, expected_files in cases.items():
            source_script_root = (
                ROOT / "sources" / "first_party" / "skills" / skill_name / "scripts"
            )
            projected_skill_root = (
                ROOT
                / "codex-marketplace"
                / "plugins"
                / "superpowers-plus"
                / "skills"
                / skill_name
            )
            projected_script_root = projected_skill_root / "scripts"

            self.assertTrue(source_script_root.is_dir(), skill_name)
            self.assertTrue(projected_script_root.is_dir(), skill_name)
            self.assertFalse((source_script_root / "skills").exists(), skill_name)
            self.assertFalse((projected_skill_root / "skills").exists(), skill_name)

            for rel_path in expected_files:
                self.assertTrue((source_script_root / rel_path).is_file(), f"{skill_name}/{rel_path}")
                self.assertTrue((projected_script_root / rel_path).is_file(), f"{skill_name}/{rel_path}")

    def test_validate_skill_bundle_manifest_normalizes_line_endings_for_verbatim_entries(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            plugin_root = temp_root / "codex-marketplace" / "plugins" / "sample-pack"
            source_root = temp_root / "sources" / "first_party"
            projected_skill_dir = plugin_root / "skills"

            source_file = source_root / "skills" / "line-ending-note.txt"
            projected_file = plugin_root / "docs" / "line-endings.txt"

            source_file.parent.mkdir(parents=True, exist_ok=True)
            projected_file.parent.mkdir(parents=True, exist_ok=True)
            projected_skill_dir.mkdir(parents=True, exist_ok=True)

            source_file.write_bytes(b"alpha\r\nbeta\r\n")
            projected_file.write_bytes(b"alpha\nbeta\n")

            bundle_manifest = {
                "bundle_name": "sample-pack",
                "bundle_version": "1.0.0",
                "bundle_type": "third-party-codex-plugin-projection",
                "plugin_root": "codex-marketplace/plugins/sample-pack",
                "upstream_repo": "first-party",
                "pinned_commit": "ignored-for-first-party-root",
                "source_root": "skills",
                "plugin_author": "Harley Bartles",
                "plugin_license": "MIT",
                "repo_index": {
                    "source_ledger": ["sources/first_party/skills/line-ending-note.txt"],
                    "provenance_refs": ["provenance/sample-pack.md"],
                    "agents_md": None,
                    "registry_alignment": {"status": "aligned", "note": None},
                },
                "entries": [
                    {
                        "canonical_name": "line-ending-note",
                        "source_category": "first_party",
                        "content_mode": "verbatim",
                        "import_status": "imported",
                        "snapshot_path": "skills/line-ending-note.txt",
                        "local_path": "docs/line-endings.txt",
                    }
                ],
                "candidate_count": 1,
                "imported_count": 1,
                "skipped_count": 0,
                "blocked_count": 0,
            }

            with patch.object(validate_marketplace, "ROOT", temp_root), patch.object(superpowers_source, "ROOT", temp_root):
                validate_skill_bundle_manifest(
                    bundle_manifest,
                    bundle_name="sample-pack",
                    plugin_root="codex-marketplace/plugins/sample-pack",
                )

    def test_validate_projection_entry_provenance_accepts_content_mode_matrix(self) -> None:
        _validate_projection_entry_provenance(
            {
                "canonical_name": "using-superpowers-plus",
                "source_category": "third_party",
                "content_mode": "adapted",
                "canonical_source_path": (
                    "sources/third_party/superpowers/obra-superpowers/v6.2.0/skills/using-superpowers"
                ),
                "local_path": "skills/using-superpowers-plus",
                "source_path": (
                    "sources/third_party/superpowers/obra-superpowers/v6.2.0/skills/using-superpowers/SKILL.md"
                ),
                "source_author": "obra",
                "source_license": "MIT",
                "source_repo": "https://github.com/obra/superpowers",
                "adaptation_overlay_path": "adapters/codex/superpowers-plus/using-superpowers-plus",
                "adapted_author": "Harley Bartles",
                "provenance_note": "Adapted to remove any claim that Superpowers skills override repo instructions.",
                "adaptation_note": "Reworded instruction priority for Codex marketplace compatibility.",
            },
            bundle_name="superpowers-plus",
        )
        _validate_projection_entry_provenance(
            {
                "canonical_name": "sample-skill",
                "source_category": "third_party",
                "content_mode": "normalised",
                "canonical_source_path": "sources/third_party/game-studio/upstream/skills/sample-skill",
                "local_path": "skills/sample-skill",
                "source_path": "sources/third_party/game-studio/upstream/skills/sample-skill/SKILL.md",
                "source_author": "OpenAI",
                "source_license": "MIT",
                "source_repo": "openai/plugins",
                "adapted_author": "Harley Bartles",
                "adaptation_overlay_path": "adapters/codex/game-studio/sample-skill",
                "provenance_note": "Projected from the retained Game Studio sample skill.",
                "adaptation_note": "Moved examples into canonical references/ folders.",
            },
            bundle_name="game-studio",
        )

    def test_validate_projection_entry_provenance_rejects_missing_adapted_author(self) -> None:
        with self.assertRaises(ValueError):
            _validate_projection_entry_provenance(
                {
                    "canonical_name": "using-superpowers-plus",
                    "source_category": "third_party",
                    "content_mode": "adapted",
                    "canonical_source_path": (
                        "sources/third_party/superpowers/obra-superpowers/v6.2.0/skills/using-superpowers"
                    ),
                    "local_path": "skills/using-superpowers-plus",
                    "adaptation_overlay_path": "adapters/codex/superpowers-plus/using-superpowers-plus",
                    "provenance_note": "Adapted to remove any claim that Superpowers skills override repo instructions.",
                    "adaptation_note": "Reworded instruction priority for Codex marketplace compatibility.",
                },
                bundle_name="superpowers-plus",
            )

    def test_validate_skill_markdown_frontmatter_accepts_simple_headers(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            skill_root = Path(temp_dir) / "example-skill"
            skill_root.mkdir(parents=True, exist_ok=True)
            _touch(
                skill_root / "SKILL.md",
                "---\nname: example-skill\ndescription: Use when something simple is needed.\n---\nBody.\n",
            )

            validate_skill_markdown_frontmatter(skill_root)

    def test_validate_skill_markdown_frontmatter_accepts_nested_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            skill_root = Path(temp_dir) / "example-skill"
            skill_root.mkdir(parents=True, exist_ok=True)
            _touch(
                skill_root / "SKILL.md",
                (
                    "---\n"
                    "name: example-skill\n"
                    "description: Use when something simple is needed.\n"
                    "metadata:\n"
                    "  keywords:\n"
                    "    - alpha\n"
                    "    - beta\n"
                    "  owner: docs\n"
                    "---\n"
                    "Body.\n"
                ),
            )

            validate_skill_markdown_frontmatter(skill_root)

    def test_validate_skill_markdown_frontmatter_requires_metadata_for_projected_skills(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            projected_skill_root = (
                temp_root / "codex-marketplace" / "plugins" / "superpowers-plus"
                / "skills" / "using-superpowers-plus"
            )
            _touch(
                projected_skill_root / "SKILL.md",
                "---\nname: using-superpowers-plus\ndescription: Use when workflow-sensitive work needs Superpowers guidance.\n---\nBody.\n",  # noqa: E501
            )

            with patch("skill_validation.ROOT", temp_root):
                with self.assertRaises(ValueError):
                    validate_skill_markdown_frontmatter(projected_skill_root)

            _touch(
                projected_skill_root / "SKILL.md",
                (
                    "---\n"
                    "name: using-superpowers-plus\n"
                    "description: Use when workflow-sensitive work needs Superpowers guidance.\n"
                    "metadata:\n"
                    "  source-id: using-superpowers-plus\n"
                    "  source-path: sources/first_party/skills/using-superpowers-plus/SKILL.md\n"
                    "  provenance-name: Superpowers+ first-party workflow-selection entrypoint\n"
                    'license: "MIT"\n'
                    "---\n"
                    "Body.\n"
                ),
            )

            with patch("skill_validation.ROOT", temp_root):
                validate_skill_markdown_frontmatter(projected_skill_root)

    def test_validate_skill_markdown_frontmatter_rejects_invalid_headers(self) -> None:
        cases = {
            "bom": b"\xef\xbb\xbf---\nname: example-skill\ndescription: ok\n---\n",
            "collapsed": b"--- name: example-skill description: ok ---\n",
            "missing_closing_delimiter": b"---\nname: example-skill\ndescription: ok\n",
            "missing_name": b"---\ndescription: ok\n---\n",
            "missing_description": b"---\nname: example-skill\n---\n",
            "blank_name": b"---\nname:   \ndescription: ok\n---\n",
            "blank_description": b"---\nname: example-skill\ndescription:   \n---\n",
            "metadata_not_mapping": b"---\nname: example-skill\ndescription: ok\nmetadata: nope\n---\n",
            "duplicate_name": b"---\nname: first\nname: second\ndescription: ok\n---\n",
        }

        for label, raw in cases.items():
            with self.subTest(label=label):
                with tempfile.TemporaryDirectory() as temp_dir:
                    skill_root = Path(temp_dir) / "example-skill"
                    skill_root.mkdir(parents=True, exist_ok=True)
                    (skill_root / "SKILL.md").write_bytes(raw)
                    with self.assertRaises(ValueError):
                        validate_skill_markdown_frontmatter(skill_root)

    def test_superpowers_bundle_rejects_adapted_third_party_entry_without_overlay_path(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            source_root = temp_root / "sources" / "third_party" / "superpowers" / "obra-superpowers" / "v6.2.0"
            source_skill_root = source_root / "skills" / "using-superpowers"
            plugin_root = temp_root / "codex-marketplace" / "plugins" / "superpowers-plus"
            projected_skill_root = plugin_root / "skills" / "using-superpowers-plus"

            skill_md = _third_party_projection_frontmatter(
                "using-superpowers-plus",
                "using-superpowers",
                "adapters/codex/superpowers-plus/using-superpowers-plus",
                "Use when workflow-sensitive work needs Superpowers guidance.",
            )
            _touch(
                source_skill_root / "SKILL.md",
                skill_md,
            )
            _touch(
                source_skill_root / "agents" / "openai.yaml",
                "version: 1\nmetadata: {skill_name: using-superpowers-plus}\n",
            )
            _touch(projected_skill_root / "SKILL.md", skill_md)
            _touch(
                projected_skill_root / "agents" / "openai.yaml",
                "version: 1\nmetadata: {skill_name: using-superpowers-plus}\n",
            )

            for rel_path in (
                "LICENSE",
                "SOURCE.md",
                "PROJECTION.md",
                "references/codex-marketplace-compatibility.md",
                "references/bundle-manifest.json",
                "references/provenance-map.json",
                "assets/app-icon.png",
                "assets/superpowers-small.svg",
            ):
                _touch(plugin_root / rel_path)
            _touch(plugin_root / "PROJECTION.md", SUPERPOWERS_PROJECTION_DOC)
            _touch(plugin_root / "references" / "codex-marketplace-compatibility.md", SUPERPOWERS_COMPATIBILITY_DOC)

            for rel_path in (
                ".codex-plugin/plugin.json",
                "LICENSE",
                "README.md",
                "AGENTS.md",
                "package.json",
                "assets/app-icon.png",
                "assets/superpowers-small.svg",
            ):
                _touch(source_root / rel_path)

            for rel_path in (
                ".claude-plugin",
                ".cursor-plugin",
                ".opencode",
                "gemini-extension.json",
                "CLAUDE.md",
                "GEMINI.md",
                "hooks",
            ):
                target = source_root / rel_path
                if rel_path == "hooks":
                    target.mkdir(parents=True, exist_ok=True)
                else:
                    _touch(target)

            _write_superpowers_plugin_manifests(source_root, plugin_root)

            bundle_manifest = {
                "bundle_name": "superpowers-plus",
                "bundle_version": "1.0.0",
                "bundle_type": "third-party-codex-plugin-projection",
                "marketplace_root": ".agents/plugins/marketplace.json",
                "plugin_root": "codex-marketplace/plugins/superpowers-plus",
                "canonical_source_root": "sources/third_party/superpowers/obra-superpowers/v6.2.0",
                "source_tag": "v6.2.0",
                "source_commit": "f2cbfbefebbfef77321e4c9abc9e949826bea9d7",
                "license": "MIT",
                "plugin_author": "Harley Bartles",
                "plugin_license": "MIT",
                "projection_policy": (
                    "Project only the Codex-facing plugin surface. Keep the upstream "
                    "harness-specific metadata, docs, scripts, and hooks in third-party "
                    "source custody."
                ),
                "source_of_truth": [
                    "sources/third_party/superpowers/obra-superpowers/v6.2.0/.codex-plugin/plugin.json",
                    "sources/third_party/superpowers/obra-superpowers/v6.2.0/LICENSE",
                    "sources/third_party/superpowers/obra-superpowers/v6.2.0/README.md",
                    "sources/third_party/superpowers/obra-superpowers/v6.2.0/AGENTS.md",
                    "sources/third_party/superpowers/obra-superpowers/v6.2.0/package.json",
                ],
                "candidate_count": 1,
                "imported_count": 1,
                "skipped_count": 0,
                "blocked_count": 0,
                "entries": [
                    {
                        "canonical_name": "using-superpowers-plus",
                        "source_category": "third_party",
                        "content_mode": "adapted",
                        "canonical_source_path": (
                            "sources/third_party/superpowers/obra-superpowers/v6.2.0/skills/using-superpowers"
                        ),
                        "local_path": "skills/using-superpowers-plus",
                        "import_status": "imported",
                        "copy_expectation": "adapted_from_source",
                        "provenance_note": "Adapted to remove any claim that Superpowers skills override system, developer, runtime, or repo instructions.",
                        "adapted_author": "Harley Bartles",
                        "adaptation_note": "Reworded instruction priority for Codex marketplace compatibility.",
                    }
                ],
                "excluded": [
                    {"path": ".claude-plugin", "reason": "Claude harness metadata stays in third-party source custody."},  # noqa: E501
                    {"path": ".cursor-plugin", "reason": "Cursor harness metadata stays in third-party source custody."},  # noqa: E501
                    {"path": ".opencode", "reason": "OpenCode harness metadata stays in third-party source custody."},
                    {"path": "gemini-extension.json", "reason": "Gemini harness metadata stays in third-party source custody."},
                    {"path": "CLAUDE.md", "reason": "Claude instructions stay in third-party source custody."},
                    {"path": "GEMINI.md", "reason": "Gemini instructions stay in third-party source custody."},
                    {"path": "hooks", "reason": "Hook definitions are source-only until Codex compatibility is proven."},  # noqa: E501
                ],
            }
            _touch(
                plugin_root / "references" / "provenance-map.json",
                json.dumps(
                    {
                        "bundle_name": "superpowers-plus",
                        "bundle_version": "1.0.0",
                        "upstream": {
                            "repository": "https://github.com/obra/superpowers",
                            "release_tag": "v6.2.0",
                            "release_commit": "f2cbfbefebbfef77321e4c9abc9e949826bea9d7",
                            "tag_object": "ecbd610fce16d5faabcea997f17031129589b572",
                            "license": "MIT",
                        },
                        "source_custody_root": "sources/third_party/superpowers/obra-superpowers/v6.2.0",
                        "active_projection_root": "codex-marketplace/plugins/superpowers-plus",
                        "codex_surface": {
                            "plugin_manifest": ".codex-plugin/plugin.json",
                            "skills_root": "skills",
                            "assets": [
                                "assets/app-icon.png",
                                "assets/superpowers-small.svg",
                            ],
                            "support_files": [
                                "references/codex-marketplace-compatibility.md",
                                "LICENSE",
                                "SOURCE.md",
                                "PROJECTION.md",
                            ],
                        },
                        "source_backed_projections": [],
                        "adapted_projections": [
                            {
                                "canonical_name": "using-superpowers-plus",
                                "source_category": "third_party",
                                "content_mode": "adapted",
                                "canonical_source_path": (
                                    "sources/third_party/superpowers/obra-superpowers/v6.2.0/skills/using-superpowers"
                                ),
                                "local_path": (
                                    "codex-marketplace/plugins/superpowers-plus/skills/using-superpowers-plus"
                                ),
                                "copy_expectation": "adapted_from_source",
                                "provenance_note": "Adapted to remove any claim that Superpowers skills override system, developer, runtime, or repo instructions.",
                                "adaptation_note": "Reworded instruction priority for Codex marketplace compatibility.",
                                "adapted_author": "Harley Bartles",
                            }
                        ],
                        "source_only_surfaces": [
                            {"path": ".claude-plugin", "reason": "Claude harness metadata stays in third-party source custody."},  # noqa: E501
                            {"path": ".cursor-plugin", "reason": "Cursor harness metadata stays in third-party source custody."},  # noqa: E501
                            {"path": ".opencode", "reason": "OpenCode harness metadata stays in third-party source custody."},  # noqa: E501
                            {"path": "gemini-extension.json", "reason": "Gemini harness metadata stays in third-party source custody."},  # noqa: E501
                            {"path": "CLAUDE.md", "reason": "Claude instructions stay in third-party source custody."},
                            {"path": "GEMINI.md", "reason": "Gemini instructions stay in third-party source custody."},
                            {"path": "hooks", "reason": "Hook definitions are source-only until Codex compatibility is proven."},  # noqa: E501
                        ],
                        "notes": [
                            "The source custody root stays verbatim, the projection "
                            "layer carries the Codex-marketplace adaptations, and the "
                            "installation/export layer is regenerated from the projection.",
                        ],
                    },
                    indent=2,
                ),
            )
            _touch(plugin_root / "references" / "bundle-manifest.json", json.dumps(bundle_manifest, indent=2))

            with patch("validate_marketplace.ROOT", temp_root), patch("superpowers_source.ROOT", temp_root):
                with self.assertRaisesRegex(
                    ValueError,
                    r"superpowers-plus adapted entry using-superpowers-plus needs an adaptation_overlay_path",
                ):
                    validate_superpowers_bundle_manifest(bundle_manifest, plugin_root="codex-marketplace/plugins/superpowers-plus")


if __name__ == "__main__":
    unittest.main()
