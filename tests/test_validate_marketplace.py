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

import validate_marketplace  # noqa: E402
from validate_marketplace import validate_superpowers_bundle_manifest  # noqa: E402


def _touch(path: Path, content: str = "ok") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


class ValidateMarketplaceTests(unittest.TestCase):
    def test_codex_receipts_superpowers_uses_canonical_cross_plugin_reference(self) -> None:
        source_text = (
            ROOT
            / "codex-marketplace"
            / "plugins"
            / "house-skills"
            / "skills"
            / "codex-receipts-superpowers"
            / "SKILL.md"
        ).read_text(encoding="utf-8")

        self.assertIn("repo-worker-base:codex-repo-receipts", source_text)
        self.assertNotIn("@codex-repo-receipts", source_text)

    def test_validate_marketplace_rejects_bare_cross_plugin_receipt_reference(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            source_roots = (
                temp_root / "codex-marketplace" / "plugins" / "house-skills" / "skills" / "codex-receipts-superpowers",
                temp_root / "codex-marketplace" / "plugins" / "superpowers" / "skills" / "codex-receipts-superpowers",
                temp_root / "sources" / "first_party" / "skills" / "house-skills",
            )

            for source_root in source_roots:
                source_root.mkdir(parents=True, exist_ok=True)

            _touch(
                source_roots[0] / "SKILL.md",
                "---\nname: codex-receipts-superpowers\n---\nUse `@codex-repo-receipts`.\n",
            )
            _touch(
                source_roots[1] / "SKILL.md",
                "---\nname: codex-receipts-superpowers\n---\nUse `repo-worker-base:codex-repo-receipts`.\n",
            )
            _touch(
                source_roots[2] / "decisions.md",
                "| MARK-162 | codex-receipts-superpowers-v1 | `codex-marketplace/plugins/house-skills/skills/codex-receipts-superpowers` | codex-receipts-superpowers | MARK-162 | imported | scope | Composes `repo-worker-base:codex-repo-receipts`. |\n",
            )
            _touch(
                source_roots[2] / "decisions.json",
                json.dumps(
                    [
                        {
                            "issue": "MARK-162",
                            "source_id": "codex-receipts-superpowers-v1",
                            "source_path": "codex-marketplace/plugins/house-skills/skills/codex-receipts-superpowers",
                            "public_name": "codex-receipts-superpowers",
                            "provenance_name": "MARK-162",
                            "scope": "scope",
                            "notes": "Composes repo-worker-base:codex-repo-receipts.",
                            "import_state": "imported",
                        }
                    ],
                    indent=2,
                ),
            )
            _touch(
                source_roots[2] / "intake.json",
                json.dumps(
                    [
                        {
                            "issue": "MARK-162",
                            "source_id": "codex-receipts-superpowers-v1",
                            "source_path": "codex-marketplace/plugins/house-skills/skills/codex-receipts-superpowers",
                            "public_name": "codex-receipts-superpowers",
                            "provenance_name": "MARK-162",
                            "scope": "scope",
                            "notes": "Composes repo-worker-base:codex-repo-receipts.",
                            "import_state": "imported",
                        }
                    ],
                    indent=2,
                ),
            )

            with patch("validate_marketplace.ROOT", temp_root):
                with self.assertRaisesRegex(
                    ValueError,
                    r"codex-receipts-superpowers[\\/]+SKILL\.md must use repo-worker-base:codex-repo-receipts",
                ):
                    validate_marketplace.validate_canonical_cross_plugin_skill_references()

    def test_superpowers_bundle_accepts_first_party_linear_superpowers_projection(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            source_root = temp_root / "sources" / "third_party" / "superpowers" / "obra-superpowers" / "v5.1.0"
            house_skill_root = (
                temp_root / "codex-marketplace" / "plugins" / "house-skills" / "skills" / "linear-superpowers"
            )
            plugin_root = temp_root / "codex-marketplace" / "plugins" / "superpowers"

            projected_skill_root = plugin_root / "skills" / "linear-superpowers"
            _touch(house_skill_root / "SKILL.md", "---\nname: linear-superpowers\n---\n")
            _touch(house_skill_root / "agents" / "openai.yaml", "model: gpt-5\n")
            _touch(projected_skill_root / "SKILL.md", "---\nname: linear-superpowers\n---\n")
            _touch(projected_skill_root / "agents" / "openai.yaml", "model: gpt-5\n")

            for rel_path in (
                ".codex-plugin/plugin.json",
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

            bundle_manifest = {
                "bundle_name": "superpowers",
                "bundle_version": "5.1.0",
                "bundle_type": "third-party-codex-plugin-projection",
                "marketplace_root": ".agents/plugins/marketplace.json",
                "plugin_root": "codex-marketplace/plugins/superpowers",
                "canonical_source_root": "sources/third_party/superpowers/obra-superpowers/v5.1.0",
                "source_tag": "v5.1.0",
                "source_commit": "f2cbfbefebbfef77321e4c9abc9e949826bea9d7",
                "license": "MIT",
                "projection_policy": "Project only the Codex-facing plugin surface. Keep the upstream harness-specific metadata, docs, scripts, and hooks in third-party source custody.",
                "source_of_truth": [
                    "sources/third_party/superpowers/obra-superpowers/v5.1.0/.codex-plugin/plugin.json",
                    "sources/third_party/superpowers/obra-superpowers/v5.1.0/LICENSE",
                    "sources/third_party/superpowers/obra-superpowers/v5.1.0/README.md",
                    "sources/third_party/superpowers/obra-superpowers/v5.1.0/AGENTS.md",
                    "sources/third_party/superpowers/obra-superpowers/v5.1.0/package.json",
                ],
                "candidate_count": 1,
                "imported_count": 1,
                "skipped_count": 0,
                "blocked_count": 0,
                "entries": [
                    {
                        "canonical_name": "linear-superpowers",
                        "source_category": "first_party",
                        "content_mode": "verbatim",
                        "canonical_source_path": "codex-marketplace/plugins/house-skills/skills/linear-superpowers",
                        "local_path": "skills/linear-superpowers",
                        "import_status": "imported",
                        "copy_expectation": "byte_identical",
                        "provenance_note": "Projected from House Skills as the canonical first-party source.",
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

            with patch("validate_marketplace.ROOT", temp_root):
                try:
                    validate_superpowers_bundle_manifest(
                        bundle_manifest,
                        plugin_root="codex-marketplace/plugins/superpowers",
                    )
                except ValueError as exc:  # pragma: no cover - exercised by the red test run
                    self.fail(f"validator rejected the first-party projection: {exc}")

    def test_superpowers_bundle_accepts_first_party_github_superpowers_projection(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            source_root = temp_root / "sources" / "third_party" / "superpowers" / "obra-superpowers" / "v5.1.0"
            house_skill_root = (
                temp_root / "codex-marketplace" / "plugins" / "house-skills" / "skills" / "github-superpowers"
            )
            plugin_root = temp_root / "codex-marketplace" / "plugins" / "superpowers"

            projected_skill_root = plugin_root / "skills" / "github-superpowers"
            _touch(house_skill_root / "SKILL.md", "---\nname: github-superpowers\n---\n")
            _touch(house_skill_root / "agents" / "openai.yaml", "model: gpt-5\n")
            _touch(projected_skill_root / "SKILL.md", "---\nname: github-superpowers\n---\n")
            _touch(projected_skill_root / "agents" / "openai.yaml", "model: gpt-5\n")

            for rel_path in (
                ".codex-plugin/plugin.json",
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

            bundle_manifest = {
                "bundle_name": "superpowers",
                "bundle_version": "5.1.0",
                "bundle_type": "third-party-codex-plugin-projection",
                "marketplace_root": ".agents/plugins/marketplace.json",
                "plugin_root": "codex-marketplace/plugins/superpowers",
                "canonical_source_root": "sources/third_party/superpowers/obra-superpowers/v5.1.0",
                "source_tag": "v5.1.0",
                "source_commit": "f2cbfbefebbfef77321e4c9abc9e949826bea9d7",
                "license": "MIT",
                "projection_policy": "Project only the Codex-facing plugin surface. Keep the upstream harness-specific metadata, docs, scripts, and hooks in third-party source custody.",
                "source_of_truth": [
                    "sources/third_party/superpowers/obra-superpowers/v5.1.0/.codex-plugin/plugin.json",
                    "sources/third_party/superpowers/obra-superpowers/v5.1.0/LICENSE",
                    "sources/third_party/superpowers/obra-superpowers/v5.1.0/README.md",
                    "sources/third_party/superpowers/obra-superpowers/v5.1.0/AGENTS.md",
                    "sources/third_party/superpowers/obra-superpowers/v5.1.0/package.json",
                ],
                "candidate_count": 1,
                "imported_count": 1,
                "skipped_count": 0,
                "blocked_count": 0,
                "entries": [
                    {
                        "canonical_name": "github-superpowers",
                        "source_category": "first_party",
                        "content_mode": "verbatim",
                        "canonical_source_path": "codex-marketplace/plugins/house-skills/skills/github-superpowers",
                        "local_path": "skills/github-superpowers",
                        "import_status": "imported",
                        "copy_expectation": "byte_identical",
                        "provenance_note": "Projected from House Skills as the canonical first-party source.",
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

            with patch("validate_marketplace.ROOT", temp_root):
                try:
                    validate_superpowers_bundle_manifest(
                        bundle_manifest,
                        plugin_root="codex-marketplace/plugins/superpowers",
                    )
                except ValueError as exc:  # pragma: no cover - exercised by the red test run
                    self.fail(f"validator rejected the first-party projection: {exc}")

    def test_superpowers_bundle_accepts_first_party_unslop_superpowers_projection(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            source_root = temp_root / "sources" / "third_party" / "superpowers" / "obra-superpowers" / "v5.1.0"
            house_skill_root = (
                temp_root / "codex-marketplace" / "plugins" / "house-skills" / "skills" / "unslop-superpowers"
            )
            plugin_root = temp_root / "codex-marketplace" / "plugins" / "superpowers"

            projected_skill_root = plugin_root / "skills" / "unslop-superpowers"
            _touch(house_skill_root / "SKILL.md", "---\nname: unslop-superpowers\n---\n")
            _touch(house_skill_root / "agents" / "openai.yaml", "model: gpt-5\n")
            _touch(projected_skill_root / "SKILL.md", "---\nname: unslop-superpowers\n---\n")
            _touch(projected_skill_root / "agents" / "openai.yaml", "model: gpt-5\n")

            for rel_path in (
                ".codex-plugin/plugin.json",
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

            bundle_manifest = {
                "bundle_name": "superpowers",
                "bundle_version": "5.1.0",
                "bundle_type": "third-party-codex-plugin-projection",
                "marketplace_root": ".agents/plugins/marketplace.json",
                "plugin_root": "codex-marketplace/plugins/superpowers",
                "canonical_source_root": "sources/third_party/superpowers/obra-superpowers/v5.1.0",
                "source_tag": "v5.1.0",
                "source_commit": "f2cbfbefebbfef77321e4c9abc9e949826bea9d7",
                "license": "MIT",
                "projection_policy": "Project only the Codex-facing plugin surface. Keep the upstream harness-specific metadata, docs, scripts, and hooks in third-party source custody.",
                "source_of_truth": [
                    "sources/third_party/superpowers/obra-superpowers/v5.1.0/.codex-plugin/plugin.json",
                    "sources/third_party/superpowers/obra-superpowers/v5.1.0/LICENSE",
                    "sources/third_party/superpowers/obra-superpowers/v5.1.0/README.md",
                    "sources/third_party/superpowers/obra-superpowers/v5.1.0/AGENTS.md",
                    "sources/third_party/superpowers/obra-superpowers/v5.1.0/package.json",
                ],
                "candidate_count": 1,
                "imported_count": 1,
                "skipped_count": 0,
                "blocked_count": 0,
                "entries": [
                    {
                        "canonical_name": "unslop-superpowers",
                        "source_category": "first_party",
                        "content_mode": "verbatim",
                        "canonical_source_path": "codex-marketplace/plugins/house-skills/skills/unslop-superpowers",
                        "local_path": "skills/unslop-superpowers",
                        "import_status": "imported",
                        "copy_expectation": "byte_identical",
                        "provenance_note": "Projected as a directory mirror from House Skills as the canonical first-party source.",
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

            with patch("validate_marketplace.ROOT", temp_root):
                try:
                    validate_superpowers_bundle_manifest(
                        bundle_manifest,
                        plugin_root="codex-marketplace/plugins/superpowers",
                    )
                except ValueError as exc:  # pragma: no cover - exercised by the red test run
                    self.fail(f"validator rejected the first-party projection: {exc}")


if __name__ == "__main__":
    unittest.main()
