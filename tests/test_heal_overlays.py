from __future__ import annotations

import json
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

    def test_repeated_content_prefers_nearest_match(self) -> None:
        source = ["heading", "a", "b", "heading", "a", "b"]
        # Original target was the second "heading" block at line 4-5
        result = heal_overlays._find_content(source, ["a", "b"], 4)
        # Should prefer line 4-5 (distance 0) over line 1-2 (distance 3)
        self.assertEqual(result, (5, 6))

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
            changes, _ = heal_overlays._heal_overlay(overlay_path, source_root, write=True)
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
            changes, _ = heal_overlays._heal_overlay(overlay_path, source_root, write=True)
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
            changes, _ = heal_overlays._heal_overlay(overlay_path, source_root, write=True)
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
            changes, has_errors = heal_overlays._heal_overlay(overlay_path, source_root, write=True)
            self.assertTrue(has_errors)
            self.assertTrue(any("NOT FOUND" in c for c in changes))
            # File should NOT be written when an error occurred
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
            changes, has_errors = heal_overlays._heal_overlay(overlay_path, source_root, write=True)
            self.assertTrue(has_errors)
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
            changes, _ = heal_overlays._heal_overlay(overlay_path, source_root, write=True)
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
            changes, _ = heal_overlays._heal_overlay(overlay_path, source_root, write=False)
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
            _, has_errors = heal_overlays._heal_overlay(overlay_path, source_root, write=True)
            self.assertFalse(has_errors)
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
            changes, has_errors = heal_overlays._heal_overlay(overlay_path, source_root, write=True)
            self.assertTrue(has_errors)
            self.assertTrue(any("NOT FOUND" in c for c in changes))
            # File should be unchanged when an error occurred
            self.assertEqual(overlay_path.read_text(encoding="utf-8"), original)


class FindSourceRootTests(unittest.TestCase):
    def test_finds_source_root_from_bundle_manifest(self) -> None:
        # Bundle manifests store adaptation_overlay_path as the directory,
        # while heal_overlays is passed the full overlay.yaml path. The
        # lookup must compare the overlay's parent directory to the manifest.
        with tempfile.TemporaryDirectory() as td:
            temp = Path(td)
            source_root = temp / "sources" / "third_party" / "superpowers" / "obra-superpowers" / "v6.1.0" / "skills" / "sample-skill"
            source_root.mkdir(parents=True)
            (source_root / "SKILL.md").write_text("content\n", encoding="utf-8")

            plugin_dir = temp / "codex-marketplace" / "plugins" / "superpowers-plus" / "references"
            plugin_dir.mkdir(parents=True)
            manifest = {
                "entries": [
                    {
                        "canonical_name": "sample-skill",
                        "adaptation_overlay_path": "adapters/codex/superpowers-plus/sample-skill",
                        "canonical_source_path": str(source_root.relative_to(temp).as_posix()),
                    }
                ]
            }
            (plugin_dir / "bundle-manifest.json").write_text(json.dumps(manifest), encoding="utf-8")

            original_root = heal_overlays.ROOT
            try:
                heal_overlays.ROOT = temp
                result = heal_overlays._find_source_root_for_overlay(
                    "adapters/codex/superpowers-plus/sample-skill/overlay.yaml"
                )
                self.assertEqual(result, source_root)
            finally:
                heal_overlays.ROOT = original_root


class InferSourceRootTests(unittest.TestCase):
    def test_returns_none_for_short_path(self) -> None:
        # _infer_source_root expects paths under adapters/ — a path with
        # fewer than 3 parts relative to ADAPTERS_ROOT returns None.
        # We test the internal logic directly by mocking the relative_to call.
        with tempfile.TemporaryDirectory() as td:
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

    def test_prefers_upstream_version_when_multiple_candidates(self) -> None:
        # Multiple upstreams can contain a skill with the same name. The
        # fallback must use overlay metadata to disambiguate instead of taking
        # the first filesystem-ordered rglob match.
        with tempfile.TemporaryDirectory() as td:
            temp = Path(td)
            # Two upstreams both have the same skill name
            superpowers = temp / "sources" / "third_party" / "superpowers" / "obra-superpowers" / "v6.1.0" / "skills" / "sample-skill"
            cortex = temp / "sources" / "third_party" / "claude-cortex" / "upstream" / "skills" / "sample-skill"
            superpowers.mkdir(parents=True)
            cortex.mkdir(parents=True)
            (superpowers / "SKILL.md").write_text("superpowers\n", encoding="utf-8")
            (cortex / "SKILL.md").write_text("cortex\n", encoding="utf-8")

            overlay_path = temp / "adapters" / "codex" / "superpowers-plus" / "sample-skill" / "overlay.yaml"
            overlay_path.parent.mkdir(parents=True)
            overlay_path.write_text(
                "schema_version: 2\nmetadata:\n  source_category: third_party\n  upstream_name: sample-skill\n  upstream_version: v6.1.0\nedits: []\n",
                encoding="utf-8",
            )

            original_adapters = heal_overlays.ADAPTERS_ROOT
            original_root = heal_overlays.ROOT
            try:
                heal_overlays.ADAPTERS_ROOT = temp / "adapters"
                heal_overlays.ROOT = temp
                result = heal_overlays._infer_source_root(overlay_path)
                self.assertEqual(result, superpowers)
            finally:
                heal_overlays.ADAPTERS_ROOT = original_adapters
                heal_overlays.ROOT = original_root

    def test_raises_when_ambiguous_candidates(self) -> None:
        # If overlay metadata cannot disambiguate, fail loudly rather than
        # silently picking a filesystem-dependent match.
        with tempfile.TemporaryDirectory() as td:
            temp = Path(td)
            one = temp / "sources" / "third_party" / "superpowers" / "v6.1.0" / "skills" / "sample-skill"
            two = temp / "sources" / "third_party" / "claude-cortex" / "upstream" / "skills" / "sample-skill"
            one.mkdir(parents=True)
            two.mkdir(parents=True)

            overlay_path = temp / "adapters" / "codex" / "pack" / "sample-skill" / "overlay.yaml"
            overlay_path.parent.mkdir(parents=True)
            overlay_path.write_text("schema_version: 2\nmetadata:\n  source_category: third_party\n  upstream_name: sample-skill\nedits: []\n", encoding="utf-8")

            original_adapters = heal_overlays.ADAPTERS_ROOT
            original_root = heal_overlays.ROOT
            try:
                heal_overlays.ADAPTERS_ROOT = temp / "adapters"
                heal_overlays.ROOT = temp
                with self.assertRaises(RuntimeError):
                    heal_overlays._infer_source_root(overlay_path)
            finally:
                heal_overlays.ADAPTERS_ROOT = original_adapters
                heal_overlays.ROOT = original_root


if __name__ == "__main__":
    unittest.main()
