from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import sys

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import heal_overlays  # noqa: E402


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def _make_overlay(spec: dict) -> str:
    import yaml

    return yaml.safe_dump(spec, sort_keys=False, allow_unicode=True, width=4096)


class FindContentTests(unittest.TestCase):
    def test_exact_match_at_original_location(self) -> None:
        source = ["a", "b", "c", "d"]
        result = heal_overlays._find_content(source, ["b", "c"], 2)
        self.assertEqual(result, (2, 3))

    def test_match_at_different_location(self) -> None:
        source = ["x", "a", "b", "c", "d"]
        result = heal_overlays._find_content(source, ["b", "c"], 1)
        self.assertEqual(result, (3, 4))

    def test_whitespace_insensitive_match(self) -> None:
        source = ["a", "b  ", "c"]
        result = heal_overlays._find_content(source, ["b", "c"], 1)
        self.assertEqual(result, (2, 3))

    def test_not_found(self) -> None:
        source = ["a", "b", "c"]
        result = heal_overlays._find_content(source, ["z"], 1)
        self.assertIsNone(result)

    def test_empty_expected(self) -> None:
        source = ["a", "b"]
        result = heal_overlays._find_content(source, [], 1)
        self.assertIsNone(result)


class HealOverlayTests(unittest.TestCase):
    def _setup(self, temp_dir: Path) -> tuple[Path, Path]:
        source_root = temp_dir / "source"
        overlay_path = temp_dir / "overlay" / "overlay.yaml"
        return source_root, overlay_path

    def test_line_number_shift_healing(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            temp = Path(td)
            source_root, overlay_path = self._setup(temp)
            # Source has 2 new lines inserted before the target content
            _write(source_root / "SKILL.md", "line1\nline2\nINSERTED_A\nINSERTED_B\ntarget\nafter\n")
            _write(
                overlay_path,
                _make_overlay({
                    "schema_version": 2,
                    "metadata": {"source_category": "third_party"},
                    "edits": [
                        {
                            "path": "SKILL.md",
                            "op": "replace",
                            "start_line": 3,
                            "end_line": 3,
                            "expected_lines": ["target"],
                            "replace_lines": ["REPLACED"],
                        }
                    ],
                }),
            )
            changes = heal_overlays._heal_overlay(overlay_path, source_root, write=True)
            self.assertTrue(any("lines healed" in c for c in changes))
            # Verify the overlay was updated
            import yaml

            spec = yaml.safe_load(overlay_path.read_text(encoding="utf-8"))
            self.assertEqual(spec["edits"][0]["start_line"], 5)
            self.assertEqual(spec["edits"][0]["end_line"], 5)

    def test_whitespace_healing_at_same_location(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            temp = Path(td)
            source_root, overlay_path = self._setup(temp)
            # Source has trailing whitespace stripped
            _write(source_root / "SKILL.md", "line1\nline2\ntarget\nline4\n")
            _write(
                overlay_path,
                _make_overlay({
                    "schema_version": 2,
                    "metadata": {"source_category": "third_party"},
                    "edits": [
                        {
                            "path": "SKILL.md",
                            "op": "replace",
                            "start_line": 3,
                            "end_line": 3,
                            "expected_lines": ["target  "],
                            "replace_lines": ["REPLACED"],
                        }
                    ],
                }),
            )
            changes = heal_overlays._heal_overlay(overlay_path, source_root, write=True)
            self.assertTrue(any("whitespace healed" in c for c in changes))
            import yaml

            spec = yaml.safe_load(overlay_path.read_text(encoding="utf-8"))
            self.assertEqual(spec["edits"][0]["expected_lines"], ["target"])

    def test_noop_removal(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            temp = Path(td)
            source_root, overlay_path = self._setup(temp)
            _write(source_root / "SKILL.md", "line1\nline2\ntarget\nline4\n")
            _write(
                overlay_path,
                _make_overlay({
                    "schema_version": 2,
                    "metadata": {"source_category": "third_party"},
                    "edits": [
                        {
                            "path": "SKILL.md",
                            "op": "replace",
                            "start_line": 3,
                            "end_line": 3,
                            "expected_lines": ["target  "],
                            "replace_lines": ["target"],
                        }
                    ],
                }),
            )
            changes = heal_overlays._heal_overlay(overlay_path, source_root, write=True)
            self.assertTrue(any("no-op" in c for c in changes))
            import yaml

            spec = yaml.safe_load(overlay_path.read_text(encoding="utf-8"))
            self.assertEqual(len(spec["edits"]), 0)

    def test_content_not_found(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            temp = Path(td)
            source_root, overlay_path = self._setup(temp)
            _write(source_root / "SKILL.md", "line1\nline2\nline3\n")
            _write(
                overlay_path,
                _make_overlay({
                    "schema_version": 2,
                    "metadata": {"source_category": "third_party"},
                    "edits": [
                        {
                            "path": "SKILL.md",
                            "op": "replace",
                            "start_line": 1,
                            "end_line": 1,
                            "expected_lines": ["DOES_NOT_EXIST"],
                            "replace_lines": ["REPLACED"],
                        }
                    ],
                }),
            )
            changes = heal_overlays._heal_overlay(overlay_path, source_root, write=True)
            self.assertTrue(any("NOT FOUND" in c for c in changes))
            # File should NOT be written when only a warning occurred
            import yaml

            spec = yaml.safe_load(overlay_path.read_text(encoding="utf-8"))
            # Edit should still be present (not healed)
            self.assertEqual(len(spec["edits"]), 1)
            self.assertEqual(spec["edits"][0]["start_line"], 1)

    def test_missing_source_file(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            temp = Path(td)
            source_root, overlay_path = self._setup(temp)
            _write(
                overlay_path,
                _make_overlay({
                    "schema_version": 2,
                    "metadata": {"source_category": "third_party"},
                    "edits": [
                        {
                            "path": "MISSING.md",
                            "op": "replace",
                            "start_line": 1,
                            "end_line": 1,
                            "expected_lines": ["x"],
                            "replace_lines": ["y"],
                        }
                    ],
                }),
            )
            changes = heal_overlays._heal_overlay(overlay_path, source_root, write=True)
            self.assertTrue(any("source file missing" in c for c in changes))

    def test_anchor_insert_healing(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            temp = Path(td)
            source_root, overlay_path = self._setup(temp)
            _write(source_root / "SKILL.md", "line1\nINSERTED\nanchor_line\nline4\n")
            _write(
                overlay_path,
                _make_overlay({
                    "schema_version": 2,
                    "metadata": {"source_category": "third_party"},
                    "edits": [
                        {
                            "path": "SKILL.md",
                            "op": "insert_after",
                            "line": 2,
                            "anchor": "anchor_line",
                            "insert_lines": ["NEW"],
                        }
                    ],
                }),
            )
            changes = heal_overlays._heal_overlay(overlay_path, source_root, write=True)
            self.assertTrue(any("anchor moved" in c for c in changes))
            import yaml

            spec = yaml.safe_load(overlay_path.read_text(encoding="utf-8"))
            self.assertEqual(spec["edits"][0]["line"], 3)

    def test_check_mode_does_not_write(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            temp = Path(td)
            source_root, overlay_path = self._setup(temp)
            _write(source_root / "SKILL.md", "INSERTED\ntarget\nafter\n")
            original_overlay = _make_overlay({
                "schema_version": 2,
                "metadata": {"source_category": "third_party"},
                "edits": [
                    {
                        "path": "SKILL.md",
                        "op": "replace",
                        "start_line": 1,
                        "end_line": 1,
                        "expected_lines": ["target"],
                        "replace_lines": ["REPLACED"],
                    }
                ],
            })
            _write(overlay_path, original_overlay)
            changes = heal_overlays._heal_overlay(overlay_path, source_root, write=False)
            self.assertTrue(len(changes) > 0)
            # File should be unchanged
            self.assertEqual(overlay_path.read_text(encoding="utf-8"), original_overlay)

    def test_edit_order_preserved(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            temp = Path(td)
            source_root, overlay_path = self._setup(temp)
            _write(source_root / "A.md", "x\ntarget_a\nz\n")
            _write(source_root / "B.md", "x\ntarget_b\nz\n")
            # Edits target B first, then A — order should be preserved
            _write(
                overlay_path,
                _make_overlay({
                    "schema_version": 2,
                    "metadata": {"source_category": "third_party"},
                    "edits": [
                        {
                            "path": "B.md",
                            "op": "replace",
                            "start_line": 1,
                            "end_line": 1,
                            "expected_lines": ["target_b"],
                            "replace_lines": ["RB"],
                        },
                        {
                            "path": "A.md",
                            "op": "replace",
                            "start_line": 1,
                            "end_line": 1,
                            "expected_lines": ["target_a"],
                            "replace_lines": ["RA"],
                        },
                    ],
                }),
            )
            heal_overlays._heal_overlay(overlay_path, source_root, write=True)
            import yaml

            spec = yaml.safe_load(overlay_path.read_text(encoding="utf-8"))
            # Order should be preserved: B first, A second
            self.assertEqual(spec["edits"][0]["path"], "B.md")
            self.assertEqual(spec["edits"][1]["path"], "A.md")

    def test_no_write_when_only_warnings(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            temp = Path(td)
            source_root, overlay_path = self._setup(temp)
            _write(source_root / "SKILL.md", "line1\nline2\nline3\n")
            original = _make_overlay({
                "schema_version": 2,
                "metadata": {"source_category": "third_party"},
                "edits": [
                    {
                        "path": "SKILL.md",
                        "op": "replace",
                        "start_line": 1,
                        "end_line": 1,
                        "expected_lines": ["DOES_NOT_EXIST"],
                        "replace_lines": ["REPLACED"],
                    }
                ],
            })
            _write(overlay_path, original)
            changes = heal_overlays._heal_overlay(overlay_path, source_root, write=True)
            self.assertTrue(any("NOT FOUND" in c for c in changes))
            # File should be unchanged — only a warning, no actual healing
            self.assertEqual(overlay_path.read_text(encoding="utf-8"), original)


class InferSourceRootTests(unittest.TestCase):
    def test_returns_none_for_short_path(self) -> None:
        # _infer_source_root expects paths under adapters/ — a path with
        # fewer than 3 parts relative to ADAPTERS_ROOT returns None.
        # We test the internal logic directly by mocking the relative_to call.
        with tempfile.TemporaryDirectory() as td:
            # Create a path that mimics adapters/codex/pack/skill/overlay.yaml
            # but in a temp dir, then patch ADAPTERS_ROOT
            fake_adapters = Path(td) / "adapters"
            overlay_path = fake_adapters / "codex" / "pack" / "skill" / "overlay.yaml"
            overlay_path.parent.mkdir(parents=True, exist_ok=True)
            overlay_path.write_text("schema_version: 2\n", encoding="utf-8")
            original_adapters = heal_overlays.ADAPTERS_ROOT
            original_root = heal_overlays.ROOT
            try:
                heal_overlays.ADAPTERS_ROOT = fake_adapters
                heal_overlays.ROOT = Path(td)
                result = heal_overlays._infer_source_root(overlay_path)
                # No sources/third_party dir exists, so should return None
                self.assertIsNone(result)
            finally:
                heal_overlays.ADAPTERS_ROOT = original_adapters
                heal_overlays.ROOT = original_root


if __name__ == "__main__":
    unittest.main()
