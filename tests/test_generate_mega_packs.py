from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from generate_mega_packs import collect_entries_by_family, generate_mega_pack_manifest  # noqa: E402


class GenerateMegaPacksTests(unittest.TestCase):
    def test_collect_entries_by_family_groups_by_source_family(self) -> None:
        plugin_manifests = [
            {
                "bundle_name": "security-pack",
                "entries": [
                    {"canonical_name": "owasp-top-10", "source_category": "third_party", "source_family": "claude-cortex", "content_mode": "normalised", "canonical_source_path": "sources/third_party/claude-cortex/upstream/skills/owasp-top-10", "local_path": "skills/owasp-top-10"},
                    {"canonical_name": "ecc-security", "source_category": "third_party", "source_family": "ecc", "content_mode": "normalised", "canonical_source_path": "sources/third_party/ecc/upstream/skills/ecc-security", "local_path": "skills/ecc-security"},
                ],
            },
            {
                "bundle_name": "architecture-pack",
                "entries": [
                    {"canonical_name": "cqrs", "source_category": "third_party", "source_family": "claude-cortex", "content_mode": "normalised", "canonical_source_path": "sources/third_party/claude-cortex/upstream/skills/cqrs", "local_path": "skills/cqrs"},
                ],
            },
        ]
        by_family = collect_entries_by_family(plugin_manifests)
        self.assertIn("claude-cortex", by_family)
        self.assertIn("ecc", by_family)
        self.assertEqual(len(by_family["claude-cortex"]), 2)
        self.assertEqual(len(by_family["ecc"]), 1)

    def test_generate_mega_pack_manifest_produces_correct_shape(self) -> None:
        entries = [
            {"canonical_name": "owasp-top-10", "source_category": "third_party", "source_family": "claude-cortex", "content_mode": "normalised", "canonical_source_path": "sources/third_party/claude-cortex/upstream/skills/owasp-top-10", "local_path": "skills/owasp-top-10"},
            {"canonical_name": "cqrs", "source_category": "third_party", "source_family": "claude-cortex", "content_mode": "normalised", "canonical_source_path": "sources/third_party/claude-cortex/upstream/skills/cqrs", "local_path": "skills/cqrs"},
        ]
        manifest = generate_mega_pack_manifest(
            mega_pack_name="codex-cortex",
            mega_pack_root="codex-marketplace/plugins/codex-cortex",
            source_family="claude-cortex",
            entries=entries,
        )
        self.assertEqual(manifest["bundle_name"], "codex-cortex")
        self.assertTrue(manifest["is_mega_pack"])
        self.assertEqual(manifest["mega_pack_for"], "claude-cortex")
        self.assertEqual(len(manifest["entries"]), 2)
        # Mega-pack local_path should be relative to the mega-pack root
        for entry in manifest["entries"]:
            self.assertTrue(entry["local_path"].startswith("skills/"))


if __name__ == "__main__":
    unittest.main()
