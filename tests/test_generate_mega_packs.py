from __future__ import annotations

import json
import sys
import unittest
import tempfile
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import generate_mega_packs  # noqa: E402
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

    def test_generate_first_party_mega_pack_manifest_rebuilds_from_source_custody(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            source_root = temp_root / "sources" / "first_party" / "skills"
            active_alpha = source_root / "alpha-skill"
            active_beta = source_root / "beta-skill"
            active_alpha.mkdir(parents=True, exist_ok=True)
            active_beta.mkdir(parents=True, exist_ok=True)
            (active_alpha / "SKILL.md").write_text("# alpha\n", encoding="utf-8")
            (active_beta / "SKILL.md").write_text("# beta\n", encoding="utf-8")

            existing_manifest = {
                "bundle_name": "house-skills",
                "bundle_version": "1.0.0",
                "bundle_type": "projection-lane",
                "plugin_root": "codex-marketplace/plugins/house-skills",
                "is_mega_pack": True,
                "mega_pack_for": "first_party",
                "source_families": ["first_party"],
                "entries": [
                    {
                        "canonical_name": "alpha-skill",
                        "source_category": "first_party",
                        "content_mode": "verbatim",
                        "source_family": "first_party",
                        "canonical_source_path": "sources/first_party/skills/alpha-skill",
                        "local_path": "skills/alpha-skill",
                        "lane": "Base and control plane",
                        "provenance_note": "First-party skill projected verbatim into the house-skills mega-pack.",
                        "source_path": "sources/first_party/skills/alpha-skill/SKILL.md",
                        "source_author": "Harley Bartles",
                        "source_license": "MIT",
                        "source_repo": "https://github.com/HarleyBartles/agent-asset-marketplace",
                        "copy_expectation": "byte_identical",
                    },
                    {
                        "canonical_name": "linear-issue-compactor",
                        "source_category": "first_party",
                        "content_mode": "verbatim",
                        "source_family": "first_party",
                        "canonical_source_path": "sources/first_party/skills/linear-issue-compactor",
                        "local_path": "skills/linear-issue-compactor",
                        "lane": "Base and control plane",
                        "provenance_note": "First-party skill projected verbatim into the house-skills mega-pack.",
                        "source_path": "sources/first_party/skills/linear-issue-compactor/SKILL.md",
                        "source_author": "Harley Bartles",
                        "source_license": "MIT",
                        "source_repo": "https://github.com/HarleyBartles/agent-asset-marketplace",
                        "copy_expectation": "byte_identical",
                    },
                    {
                        "canonical_name": "game-playtest",
                        "source_category": "third_party",
                        "content_mode": "verbatim",
                        "source_family": "first_party",
                        "canonical_source_path": "sources/third_party/game-studio/upstream/skills/game-playtest",
                        "local_path": "skills/game-playtest",
                        "lane": "Base and control plane",
                        "provenance_note": "Copied verbatim from the retained game-studio upstream snapshot into the Wild Bunch pack.",
                        "copy_expectation": "byte_identical",
                    },
                ],
                "notes": ["existing"],
                "plugin_author": "Harley Bartles",
                "plugin_license": "MIT",
            }

            with (
                patch.object(generate_mega_packs, "ROOT", temp_root),
                patch.object(generate_mega_packs, "FIRST_PARTY_SOURCE_ROOT", source_root),
            ):
                manifest = generate_mega_packs.generate_first_party_mega_pack_manifest(
                    mega_pack_name="house-skills",
                    mega_pack_root="codex-marketplace/plugins/house-skills",
                    existing_manifest=existing_manifest,
                )

            names = [entry["canonical_name"] for entry in manifest["entries"]]
            self.assertEqual(names, ["alpha-skill", "beta-skill", "game-playtest"])
            self.assertNotIn("linear-issue-compactor", names)
            self.assertEqual(manifest["mega_pack_for"], "first_party")
            self.assertEqual(manifest["source_families"], ["first_party"])
            self.assertEqual(manifest["entries"][1]["source_path"], "sources/first_party/skills/beta-skill/SKILL.md")


if __name__ == "__main__":
    unittest.main()
