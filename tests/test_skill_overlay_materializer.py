from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import sys


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from skill_overlay_materializer import (  # noqa: E402
    apply_overlay_tree,
    load_overlay_spec,
    stage_overlay_tree,
    validate_openai_agent_yaml,
)
from skill_validation import validate_skill_markdown_frontmatter  # noqa: E402


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _write_bytes(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)


class SkillOverlayMaterializerTests(unittest.TestCase):
    def test_stage_overlay_tree_applies_replacements_and_deletes(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            source_root = temp_root / "source"
            overlay_root = temp_root / "overlay"
            destination_root = temp_root / "destination"

            _write(source_root / "SKILL.md", "source skill\n")
            _write(source_root / "agents" / "openai.yaml", "version: 1\nmetadata: {skill_name: source}\n")
            _write(source_root / "notes.txt", "keep me\n")
            _write(source_root / "remove.txt", "delete me\n")

            _write(
                overlay_root / "overlay.yaml",
                "schema_version: 1\ndeletes:\n  - remove.txt\nmetadata:\n  note: adapted\n",
            )
            _write(overlay_root / "SKILL.md", "overlay skill\n")
            _write(overlay_root / "agents" / "openai.yaml", "version: 1\nmetadata: {skill_name: overlay}\n")

            expected_root, temp_handle = stage_overlay_tree(source_root, overlay_root)
            try:
                apply_overlay_tree(source_root, overlay_root, destination_root)
                self.assertEqual(
                    sorted(path.relative_to(expected_root).as_posix() for path in expected_root.rglob("*") if path.is_file()),
                    sorted(path.relative_to(destination_root).as_posix() for path in destination_root.rglob("*") if path.is_file()),
                )
                self.assertEqual(
                    (expected_root / "SKILL.md").read_text(encoding="utf-8"),
                    (destination_root / "SKILL.md").read_text(encoding="utf-8"),
                )
                self.assertFalse((destination_root / "overlay.yaml").exists())
                self.assertFalse((destination_root / "remove.txt").exists())
            finally:
                temp_handle.cleanup()

    def test_stage_overlay_tree_applies_line_edits_and_detects_drift(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            source_root = temp_root / "source"
            overlay_root = temp_root / "overlay"
            destination_root = temp_root / "destination"

            _write(
                source_root / "SKILL.md",
                "line 1\nline 2\nline 3\nline 4\nline 5\n",
            )
            _write(
                overlay_root / "overlay.yaml",
                (
                    "schema_version: 2\n"
                    "edits:\n"
                    "  - path: SKILL.md\n"
                    "    op: replace\n"
                    "    start_line: 2\n"
                    "    end_line: 3\n"
                    "    expected_lines:\n"
                    "      - line 2\n"
                    "      - line 3\n"
                    "    replace_lines:\n"
                    "      - swapped 2\n"
                    "      - swapped 3\n"
                    "  - path: SKILL.md\n"
                    "    op: insert_after\n"
                    "    line: 4\n"
                    "    anchor: line 4\n"
                    "    insert_lines:\n"
                    "      - inserted 4\n"
                    "      - inserted 5\n"
                ),
            )

            expected_root, temp_handle = stage_overlay_tree(source_root, overlay_root)
            try:
                apply_overlay_tree(source_root, overlay_root, destination_root)
                expected = "line 1\nswapped 2\nswapped 3\nline 4\ninserted 4\ninserted 5\nline 5\n"
                self.assertEqual((expected_root / "SKILL.md").read_text(encoding="utf-8"), expected)
                self.assertEqual((destination_root / "SKILL.md").read_text(encoding="utf-8"), expected)
            finally:
                temp_handle.cleanup()

            _write(source_root / "SKILL.md", "line 1\nline 2\nchanged 3\nline 4\nline 5\n")
            with self.assertRaises(ValueError):
                stage_overlay_tree(source_root, overlay_root)

    def test_stage_overlay_tree_applies_overlay_files_before_line_edits(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            source_root = temp_root / "source"
            overlay_root = temp_root / "overlay"
            destination_root = temp_root / "destination"

            _write(
                source_root / "SKILL.md",
                "line 1\nline 2\nline 3\n",
            )
            _write(
                overlay_root / "SKILL.md",
                "line 1\nline 2\nline 3\noverlay marker\n",
            )
            _write(
                overlay_root / "overlay.yaml",
                (
                    "schema_version: 2\n"
                    "edits:\n"
                    "  - path: SKILL.md\n"
                    "    op: replace\n"
                    "    start_line: 2\n"
                    "    end_line: 2\n"
                    "    expected_lines:\n"
                    "      - line 2\n"
                    "    replace_lines:\n"
                    "      - patched 2\n"
                ),
            )

            expected_root, temp_handle = stage_overlay_tree(source_root, overlay_root)
            try:
                apply_overlay_tree(source_root, overlay_root, destination_root)
                expected = "line 1\npatched 2\nline 3\noverlay marker\n"
                self.assertEqual((expected_root / "SKILL.md").read_text(encoding="utf-8"), expected)
                self.assertEqual((destination_root / "SKILL.md").read_text(encoding="utf-8"), expected)
            finally:
                temp_handle.cleanup()

    def test_stage_overlay_tree_preserves_existing_line_endings(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            source_root = temp_root / "source"
            overlay_root = temp_root / "overlay"
            destination_root = temp_root / "destination"

            _write_bytes(source_root / "SKILL.md", b"source skill\r\nsecond line\r\n")
            _write_bytes(source_root / "agents" / "openai.yaml", b"version: 1\r\nmetadata: {skill_name: source}\r\n")
            _write(overlay_root / "overlay.yaml", "schema_version: 1\nmetadata:\n  note: adapted\n")

            expected_root, temp_handle = stage_overlay_tree(source_root, overlay_root)
            try:
                apply_overlay_tree(source_root, overlay_root, destination_root)
                self.assertEqual(
                    (expected_root / "SKILL.md").read_bytes(),
                    b"source skill\r\nsecond line\r\n",
                )
                self.assertEqual(
                    (destination_root / "SKILL.md").read_bytes(),
                    b"source skill\r\nsecond line\r\n",
                )
                self.assertEqual(
                    (destination_root / "agents" / "openai.yaml").read_bytes(),
                    b"version: 1\r\nmetadata: {skill_name: source}\r\n",
                )
            finally:
                temp_handle.cleanup()

    def test_stage_overlay_tree_normalizes_examples_and_templates_into_references(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            source_root = temp_root / "source"
            overlay_root = temp_root / "overlay"
            destination_root = temp_root / "destination"

            _write(
                source_root / "SKILL.md",
                (
                    "---\n"
                    "name: sample-skill\n"
                    "description: Evaluate task outputs\n"
                    "---\n\n"
                    "See `examples/high-score-example.md` and `templates/evaluation-report.md`.\n"
                ),
            )
            _write(source_root / "examples" / "high-score-example.md", "# old example\n")
            _write(source_root / "templates" / "evaluation-report.md", "# old template\n")
            _write(source_root / "scripts" / "evaluate.py", "print('ok')\n")
            _write(source_root / "agents" / "openai.yaml", "version: 1\nmetadata: {skill_name: sample-skill}\n")

            _write(
                overlay_root / "overlay.yaml",
                (
                    "schema_version: 1\n"
                    "deletes:\n"
                    "  - examples/high-score-example.md\n"
                    "  - templates/evaluation-report.md\n"
                ),
            )
            _write(
                overlay_root / "SKILL.md",
                (
                    "---\n"
                    "name: sample-skill\n"
                    "description: Evaluate task outputs\n"
                    "---\n\n"
                    "See `references/examples/high-score-example.md` and `references/templates/evaluation-report.md`.\n"
                ),
            )
            _write(overlay_root / "references" / "examples" / "high-score-example.md", "# normalized example\n")
            _write(overlay_root / "references" / "templates" / "evaluation-report.md", "# normalized template\n")

            expected_root, temp_handle = stage_overlay_tree(source_root, overlay_root)
            try:
                apply_overlay_tree(source_root, overlay_root, destination_root)
                expected_files = sorted(path.relative_to(expected_root).as_posix() for path in expected_root.rglob("*") if path.is_file())
                destination_files = sorted(
                    path.relative_to(destination_root).as_posix() for path in destination_root.rglob("*") if path.is_file()
                )
                self.assertEqual(destination_files, expected_files)
                self.assertFalse((destination_root / "examples" / "high-score-example.md").exists())
                self.assertFalse((destination_root / "templates" / "evaluation-report.md").exists())
                self.assertTrue((destination_root / "references" / "examples" / "high-score-example.md").exists())
                self.assertTrue((destination_root / "references" / "templates" / "evaluation-report.md").exists())
                self.assertEqual(
                    (destination_root / "SKILL.md").read_text(encoding="utf-8"),
                    (expected_root / "SKILL.md").read_text(encoding="utf-8"),
                )
            finally:
                temp_handle.cleanup()

    def test_stage_overlay_tree_normalizes_security_review_companion_into_references(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            source_root = temp_root / "source"
            overlay_root = temp_root / "overlay"
            destination_root = temp_root / "destination"

            _write(
                source_root / "SKILL.md",
                (
                    "---\n"
                    "name: security-review\n"
                    "description: Review sensitive code paths\n"
                    "---\n\n"
                    "See `cloud-infrastructure-security.md` for the companion guide.\n"
                ),
            )
            _write(source_root / "cloud-infrastructure-security.md", "# old companion\n")

            _write(
                overlay_root / "overlay.yaml",
                "schema_version: 1\ndeletes:\n  - cloud-infrastructure-security.md\n",
            )
            _write(
                overlay_root / "SKILL.md",
                (
                    "---\n"
                    "name: security-review\n"
                    "description: Review sensitive code paths\n"
                    "---\n\n"
                    "See `references/cloud-infrastructure-security.md` for the companion guide.\n"
                ),
            )
            _write(
                overlay_root / "references" / "cloud-infrastructure-security.md",
                "# normalized companion\n",
            )

            expected_root, temp_handle = stage_overlay_tree(source_root, overlay_root)
            try:
                apply_overlay_tree(source_root, overlay_root, destination_root)
                self.assertFalse((destination_root / "cloud-infrastructure-security.md").exists())
                self.assertTrue((destination_root / "references" / "cloud-infrastructure-security.md").exists())
                self.assertEqual(
                    (destination_root / "SKILL.md").read_text(encoding="utf-8"),
                    (expected_root / "SKILL.md").read_text(encoding="utf-8"),
                )
            finally:
                temp_handle.cleanup()

    def test_overlay_yaml_rejects_unknown_keys_and_bad_delete_paths(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            overlay_root = temp_root / "overlay"

            _write(overlay_root / "overlay.yaml", "schema_version: 1\nunknown: value\n")
            with self.assertRaises(ValueError):
                load_overlay_spec(overlay_root)

            _write(
                overlay_root / "overlay.yaml",
                "schema_version: 1\ndeletes:\n  - ../escape.txt\n",
            )
            with self.assertRaises(ValueError):
                load_overlay_spec(overlay_root)

    def test_validate_openai_agent_yaml_requires_metadata_mapping(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            openai_yaml = temp_root / "agents" / "openai.yaml"

            _write(openai_yaml, "version: 1\nmetadata: {skill_name: using-superpowers}\n")
            validate_openai_agent_yaml(openai_yaml)

            _write(openai_yaml, "version: 2\nmetadata: {skill_name: using-superpowers}\n")
            with self.assertRaises(ValueError):
                validate_openai_agent_yaml(openai_yaml)

            _write(openai_yaml, "version: 1\nmetadata: not-a-mapping\n")
            with self.assertRaises(ValueError):
                validate_openai_agent_yaml(openai_yaml)

    def test_validate_openai_agent_yaml_accepts_rich_codex_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            openai_yaml = temp_root / "agents" / "openai.yaml"

            _write(
                openai_yaml,
                (
                    "version: 1\n"
                    "metadata:\n"
                    "  source_category: third_party\n"
                    "  upstream_name: sample-skill\n"
                    "  upstream_version: upstream\n"
                    "  adaptation_overlay: adapters/codex/game-studio/sample-skill\n"
                    "  projection_plugin: game-studio\n"
                    "  source-id: sample-skill\n"
                    "  source-path: sources/third_party/game-studio/upstream/skills/sample-skill/SKILL.md\n"
                    "  provenance-name: MARK-301 Agentic evaluation normalization skill\n"
                    "  origin: third_party\n"
                    "  source_author: OpenAI\n"
                    "  source_license: MIT\n"
                    "  source_repo: openai/plugins\n"
                    "  content_mode: normalised\n"
                    "  adapted_author: Harley Bartles\n"
                    "interface:\n"
                    "  display_name: Agentic Evaluation\n"
                    "  short_description: Route evaluation-heavy work to the dedicated game-studio pack.\n"
                    "  default_prompt: Use /sample-skill to keep evaluation assets internal.\n"
                    "policy:\n"
                    "  allow_implicit_invocation: true\n"
                    "  products:\n"
                    "    - chatgpt\n"
                    "    - codex\n"
                    "dependencies:\n"
                    "  tools:\n"
                    "    - type: mcp\n"
                    "      value: openaiDeveloperDocs\n"
                    "      description: OpenAI Docs MCP server\n"
                    "      transport: streamable_http\n"
                    "      url: https://developers.openai.com/mcp\n"
                ),
            )

            validate_openai_agent_yaml(openai_yaml)

    def test_validate_openai_agent_yaml_rejects_bad_rich_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            openai_yaml = temp_root / "agents" / "openai.yaml"

            _write(
                openai_yaml,
                (
                    "version: 1\n"
                    "metadata: {source_category: third_party, upstream_name: using-superpowers, upstream_version: v5.1.0}\n"
                    "interface: nope\n"
                ),
            )
            with self.assertRaises(ValueError):
                validate_openai_agent_yaml(openai_yaml)

            _write(
                openai_yaml,
                (
                    "version: 1\n"
                    "metadata: {source_category: third_party, upstream_name: using-superpowers, upstream_version: v5.1.0, adaptation_overlay: overlay, projection_plugin: superpowers-plus}\n"
                    "policy: {allow_implicit_invocation: maybe}\n"
                ),
            )
            with self.assertRaises(ValueError):
                validate_openai_agent_yaml(openai_yaml)

    def test_validate_skill_markdown_frontmatter_requires_metadata_for_projected_skills(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            skill_root = temp_root / "using-superpowers"
            skill_md = skill_root / "SKILL.md"

            _write(
                skill_md,
                (
                    "---\n"
                    "name: using-superpowers\n"
                    "description: route workflow-sensitive work\n"
                    "---\n"
                    "\n"
                    "body\n"
                ),
            )
            with self.assertRaises(ValueError):
                validate_skill_markdown_frontmatter(skill_root)

            _write(
                skill_md,
                (
                    "---\n"
                    "name: using-superpowers\n"
                    "description: route workflow-sensitive work\n"
                    "metadata:\n"
                    "  source_category: third_party\n"
                    "  upstream_name: using-superpowers\n"
                    "  upstream_version: v6.0.3\n"
                    "  adaptation_overlay: adapters/codex/superpowers-plus/using-superpowers\n"
                    "  projection_plugin: superpowers-plus\n"
                    "  source_author: Obra AI\n"
                    "  source_license: MIT\n"
                    "  source_repo: https://github.com/obra-ai/obra-superpowers\n"
                    "  content_mode: adapted\n"
                    "  adapted_author: Harley Bartles\n"
                    "---\n"
                    "\n"
                    "body\n"
                ),
            )
            validate_skill_markdown_frontmatter(skill_root)


if __name__ == "__main__":
    unittest.main()
