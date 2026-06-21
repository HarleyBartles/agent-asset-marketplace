from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from tree_canonicalization import canonicalize_tree_bytes, canonicalize_tree  # noqa: E402


class TreeCanonicalizationTests(unittest.TestCase):
    def test_canonicalizes_crlf_to_lf_for_text_files(self) -> None:
        result = canonicalize_tree_bytes(Path("SKILL.md"), b"line1\r\nline2\r\n")
        self.assertEqual(result, b"line1\nline2\n")

    def test_canonicalizes_cr_to_lf_for_text_files(self) -> None:
        result = canonicalize_tree_bytes(Path("SKILL.md"), b"line1\rline2\r")
        self.assertEqual(result, b"line1\nline2\n")

    def test_preserves_binary_files(self) -> None:
        result = canonicalize_tree_bytes(Path("icon.png"), b"\x89PNG\r\n\x1a\n")
        self.assertEqual(result, b"\x89PNG\r\n\x1a\n")

    def test_canonicalizes_json(self) -> None:
        result = canonicalize_tree_bytes(Path("manifest.json"), b'{"a":1}\r\n')
        self.assertEqual(result, b'{"a":1}\n')

    def test_canonicalizes_yaml(self) -> None:
        result = canonicalize_tree_bytes(Path("openai.yaml"), b"name: test\r\n")
        self.assertEqual(result, b"name: test\n")


if __name__ == "__main__":
    unittest.main()
