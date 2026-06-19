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


if __name__ == "__main__":
    unittest.main()
