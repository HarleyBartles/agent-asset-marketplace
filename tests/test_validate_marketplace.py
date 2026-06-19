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
import skill_zip_artifacts  # noqa: E402
from skill_zip_artifacts import validate_skill_markdown_frontmatter  # noqa: E402
from validate_marketplace import (  # noqa: E402
    _validate_projection_entry_provenance,
    _validate_repo_index_metadata,
    validate_everything_codex_code_bundle_manifest,
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
        "  upstream_version: v5.1.0\n"
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
        if entry.get("source_category") == "first_party":
            source_backed.append(record)
        elif entry.get("content_mode") == "adapted":
            adapted.append(record)

    provenance_map = {
        "bundle_name": "superpowers-plus",
        "bundle_version": "5.1.0",
        "upstream": {
            "repository": "https://github.com/obra/superpowers",
            "release_tag": "v5.1.0",
            "release_commit": "f2cbfbefebbfef77321e4c9abc9e949826bea9d7",
            "tag_object": "ecbd610fce16d5faabcea997f17031129589b572",
            "license": "MIT",
        },
        "source_custody_root": "sources/third_party/superpowers/obra-superpowers/v5.1.0",
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
            "The source custody root stays verbatim, the projection layer carries the Codex-marketplace adaptations, and the installation/export layer is regenerated from the projection plus overlays.",
            "The active projection adapts the using-superpowers and finishing-a-development-branch workflows for Codex marketplace precedence and publication rules, and adds the House Skills-backed linear-superpowers, github-superpowers, unslop-superpowers, and architecture-superpowers projections.",
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

This root is the Codex-facing marketplace projection of `obra/superpowers`
`v5.1.0`, plus the source-backed House Skills `linear-superpowers`,
`github-superpowers`, `unslop-superpowers`, and `architecture-superpowers`
skills.

## Layer Model

This repository uses three distinct layers for the Superpowers bundle:

- Source custody keeps the retained third-party snapshot verbatim.
- Projection layer holds the source-controlled marketplace copy and any
  Codex-marketplace adaptations.
- Installation/export layer is derived from the projection plus overlays and
  is produced only by canonical tooling.
- The custody flow is `source custody -> projection layer -> installation/export layer`.
- The adapted Superpowers skills are materialized from source custody plus
  `adapters/codex/superpowers-plus/...`.
- Frontmatter contract: docs/contracts/skill-frontmatter.md
- OpenAI agent contract: docs/contracts/openai-agent-yaml.md
"""

SUPERPOWERS_COMPATIBILITY_DOC = """# Codex Marketplace Compatibility

## Projection contract

- The repo-specific adaptation for `using-superpowers` and `finishing-a-development-branch` lives only in the projection layer and is source-controlled in `adapters/codex/superpowers-plus/...`.
- Source custody remains a verbatim upstream snapshot.
- Installation and export artifacts are derived from the projection layer plus overlays.
- Frontmatter contract: docs/contracts/skill-frontmatter.md
- OpenAI agent contract: docs/contracts/openai-agent-yaml.md
"""


class ValidateMarketplaceTests(unittest.TestCase):
    def test_superpowers_bundle_accepts_first_party_linear_superpowers_projection(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            source_root = temp_root / "sources" / "third_party" / "superpowers" / "obra-superpowers" / "v5.1.0"
            source_skill_root = temp_root / "sources" / "first_party" / "core" / "linear-superpowers"
            plugin_root = temp_root / "codex-marketplace" / "plugins" / "superpowers-plus"

            projected_skill_root = plugin_root / "skills" / "linear-superpowers"
            skill_md = _first_party_projection_frontmatter(
                "linear-superpowers",
                "sources/first_party/core/linear-superpowers/SKILL.md",
                "MARK-139 Linear Superpowers compositional skill",
                "Use when the Linear packet needs the smallest applicable Superpowers router.",
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
                "bundle_version": "5.1.0",
                "bundle_type": "third-party-codex-plugin-projection",
                "marketplace_root": ".agents/plugins/marketplace.json",
                "plugin_root": "codex-marketplace/plugins/superpowers-plus",
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
                "repo_index": {
                    "source_ledger": [
                        "sources/third_party/superpowers/obra-superpowers/v5.1.0/package.json",
                        "sources/third_party/superpowers/obra-superpowers/v5.1.0/README.md",
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
                        "canonical_name": "linear-superpowers",
                        "source_category": "first_party",
                        "content_mode": "verbatim",
                        "canonical_source_path": "sources/first_party/core/linear-superpowers",
                        "local_path": "skills/linear-superpowers",
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

            with patch("validate_marketplace.ROOT", temp_root):
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
                "source_ledger": ["sources/third_party/superpowers/obra-superpowers/v5.1.0/README.md"],
                "provenance_refs": ["provenance/superpowers-plus.md"],
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
                    "source_ledger": "nope",
                    "provenance_refs": ["provenance/superpowers-plus.md"],
                    "agents_md": None,
                    "registry_alignment": {"status": "aligned", "note": None},
                },
                bundle_name="superpowers-plus",
                plugin_root="codex-marketplace/plugins/superpowers-plus",
            )

    def test_validate_everything_codex_code_bundle_manifest_accepts_current_shape(self) -> None:
        bundle_manifest = json.loads(
            (ROOT / "codex-marketplace/plugins/everything-codex-code/references/bundle-manifest.json").read_text(
                encoding="utf-8"
            )
        )
        validate_everything_codex_code_bundle_manifest(
            bundle_manifest,
            plugin_root="codex-marketplace/plugins/everything-codex-code",
        )

    def test_validate_everything_codex_code_bundle_manifest_tracks_source_surfaces(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            plugin_root = temp_root / "codex-marketplace" / "plugins" / "everything-codex-code"
            source_root = temp_root / "codex-marketplace" / "plugins" / "superpowers-ecc" / "skills"

            selected_names = ["alpha-skill", "beta-skill"]
            for name in selected_names:
                source_skill_root = source_root / name
                local_skill_root = plugin_root / "skills" / name
                skill_md = _first_party_projection_frontmatter(
                    name,
                    f"codex-marketplace/plugins/superpowers-ecc/skills/{name}/SKILL.md",
                    f"{name} provenance",
                    f"{name} description",
                )
                _touch(source_skill_root / "SKILL.md", skill_md)
                _touch(local_skill_root / "SKILL.md", skill_md)

            _touch(
                plugin_root / "references" / "source-map.md",
                (
                    "# Everything Codex Code Source Map\n\n"
                    "This bundle projects the selected ECC Superpowers-style workflow skills into an installable Codex marketplace surface.\n\n"
                    "| Skill | Source projection root | Local path | Notes |\n"
                    "| --- | --- | --- | --- |\n"
                    "| alpha-skill | `codex-marketplace/plugins/superpowers-ecc/skills/alpha-skill/SKILL.md` | `codex-marketplace/plugins/everything-codex-code/skills/alpha-skill/SKILL.md` | Projected unchanged from the selected ECC slice. |\n"
                    "| beta-skill | `codex-marketplace/plugins/superpowers-ecc/skills/beta-skill/SKILL.md` | `codex-marketplace/plugins/everything-codex-code/skills/beta-skill/SKILL.md` | Projected unchanged from the selected ECC slice. |\n"
                ),
            )

            bundle_manifest = {
                "bundle_name": "everything-codex-code",
                "bundle_version": "1.0.0",
                "bundle_type": "project-scoped-codex-plugin-projection",
                "marketplace_root": ".agents/plugins/marketplace.json",
                "plugin_root": "codex-marketplace/plugins/everything-codex-code",
                "canonical_source_root": "codex-marketplace/plugins/superpowers-ecc/skills",
                "source_of_truth": [
                    "codex-marketplace/plugins/superpowers-ecc/references/bundle-manifest.json",
                    "codex-marketplace/plugins/superpowers-ecc/references/source-map.md",
                    "provenance/superpowers-ecc.md",
                ],
                "projection_policy": (
                    "Project the ECC workflow skills already selected into superpowers-ecc. "
                    "Keep this pack mirrored from that marketplace projection rather than upstream ECC custody."
                ),
                "repo_index": {
                    "source_ledger": [
                        "codex-marketplace/plugins/superpowers-ecc/references/bundle-manifest.json",
                        "codex-marketplace/plugins/superpowers-ecc/references/source-map.md",
                    ],
                    "provenance_refs": [
                        "provenance/everything-codex-code.md",
                        "codex-marketplace/plugins/everything-codex-code/references/source-map.md",
                    ],
                    "agents_md": None,
                    "registry_alignment": {"status": "aligned", "note": None},
                },
                "components": [
                    {
                        "canonical_name": name,
                        "source_path": f"codex-marketplace/plugins/superpowers-ecc/skills/{name}/SKILL.md",
                        "local_path": f"skills/{name}/SKILL.md",
                        "projection_status": "projected",
                    }
                    for name in selected_names
                ],
                "notes": [
                    "Installable aggregate projection over the dedicated superpowers-ecc pack.",
                    "This bundle does not mirror upstream ECC custody directly.",
                ],
            }

            with patch.object(validate_marketplace, "ROOT", temp_root):
                validate_everything_codex_code_bundle_manifest(
                    bundle_manifest,
                    plugin_root="codex-marketplace/plugins/everything-codex-code",
                )

    def test_validate_projection_entry_provenance_accepts_content_mode_matrix(self) -> None:
        _validate_projection_entry_provenance(
            {
                "canonical_name": "using-superpowers",
                "source_category": "third_party",
                "content_mode": "adapted",
                "canonical_source_path": "sources/third_party/superpowers/obra-superpowers/v5.1.0/skills/using-superpowers",
                "local_path": "skills/using-superpowers",
                "adaptation_overlay_path": "adapters/codex/superpowers-plus/using-superpowers",
                "adapted_author": "Harley Bartles",
                "provenance_note": "Adapted to remove any claim that Superpowers skills override repo instructions.",
                "adaptation_note": "Reworded instruction priority for Codex marketplace compatibility.",
            },
            bundle_name="superpowers-plus",
        )
        _validate_projection_entry_provenance(
            {
                "canonical_name": "ecc-superpowers",
                "source_category": "first_party",
                "content_mode": "adapted",
                "canonical_source_path": "sources/first_party/skills/ecc-superpowers",
                "local_path": "skills/ecc-superpowers",
                "source_path": "sources/first_party/skills/ecc-superpowers/SKILL.md",
                "source_author": "Harley Bartles",
                "source_license": "MIT",
                "adapted_author": "Harley Bartles",
                "provenance_note": "Projected from the repo-authored ECC Superpowers router skill.",
                "adaptation_note": "Added repo-authored wrapper attribution and explicit upstream author/license provenance.",
            },
            bundle_name="superpowers-plus",
        )

    def test_validate_projection_entry_provenance_rejects_missing_adapted_author(self) -> None:
        with self.assertRaises(ValueError):
            _validate_projection_entry_provenance(
                {
                    "canonical_name": "using-superpowers",
                    "source_category": "third_party",
                    "content_mode": "adapted",
                    "canonical_source_path": "sources/third_party/superpowers/obra-superpowers/v5.1.0/skills/using-superpowers",
                    "local_path": "skills/using-superpowers",
                    "adaptation_overlay_path": "adapters/codex/superpowers-plus/using-superpowers",
                    "provenance_note": "Adapted to remove any claim that Superpowers skills override repo instructions.",
                    "adaptation_note": "Reworded instruction priority for Codex marketplace compatibility.",
                },
                bundle_name="superpowers-plus",
            )

    def test_superpowers_bundle_accepts_first_party_github_superpowers_projection(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            source_root = temp_root / "sources" / "third_party" / "superpowers" / "obra-superpowers" / "v5.1.0"
            source_skill_root = temp_root / "sources" / "first_party" / "skills" / "github-superpowers"
            plugin_root = temp_root / "codex-marketplace" / "plugins" / "superpowers-plus"

            projected_skill_root = plugin_root / "skills" / "github-superpowers"
            skill_md = _first_party_projection_frontmatter(
                "github-superpowers",
                "sources/first_party/skills/github-superpowers/SKILL.md",
                "MARK-143 GitHub Superpowers compositional skill",
                "Use when GitHub-facing work needs the smallest applicable Superpowers router.",
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
                "bundle_version": "5.1.0",
                "bundle_type": "third-party-codex-plugin-projection",
                "marketplace_root": ".agents/plugins/marketplace.json",
                "plugin_root": "codex-marketplace/plugins/superpowers-plus",
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
                        "canonical_source_path": "sources/first_party/skills/github-superpowers",
                        "local_path": "skills/github-superpowers",
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

            with patch("validate_marketplace.ROOT", temp_root):
                try:
                    validate_superpowers_bundle_manifest(
                        bundle_manifest,
                        plugin_root="codex-marketplace/plugins/superpowers-plus",
                    )
                except ValueError as exc:  # pragma: no cover - exercised by the red test run
                    self.fail(f"validator rejected the first-party projection: {exc}")

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
            projected_skill_root = temp_root / "codex-marketplace" / "plugins" / "superpowers-plus" / "skills" / "architecture-superpowers"
            _touch(
                projected_skill_root / "SKILL.md",
                "---\nname: architecture-superpowers\ndescription: Use when shaping architecture decisions and review packets that need a compositional gate over Superpowers instead of a new doctrine surface.\n---\nBody.\n",
            )

            with patch("skill_zip_artifacts.ROOT", temp_root):
                with self.assertRaises(ValueError):
                    validate_skill_markdown_frontmatter(projected_skill_root)

            _touch(
                projected_skill_root / "SKILL.md",
                (
                    "---\n"
                    "name: architecture-superpowers\n"
                    "description: Use when shaping architecture decisions and review packets that need a compositional gate over Superpowers instead of a new doctrine surface.\n"
                    "metadata:\n"
                    "  source-id: architecture-superpowers\n"
                    "  source-path: sources/first_party/skills/architecture-superpowers/SKILL.md\n"
                    "  provenance-name: MARK-173 Architecture Superpowers compositional skill\n"
                    'license: "MIT"\n'
                    "---\n"
                    "Body.\n"
                ),
            )

            with patch("skill_zip_artifacts.ROOT", temp_root):
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

    def test_superpowers_bundle_accepts_first_party_unslop_superpowers_projection(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            source_root = temp_root / "sources" / "third_party" / "superpowers" / "obra-superpowers" / "v5.1.0"
            source_skill_root = temp_root / "sources" / "first_party" / "skills" / "unslop-superpowers"
            plugin_root = temp_root / "codex-marketplace" / "plugins" / "superpowers-plus"

            projected_skill_root = plugin_root / "skills" / "unslop-superpowers"
            skill_md = _first_party_projection_frontmatter(
                "unslop-superpowers",
                "sources/first_party/skills/unslop-superpowers/SKILL.md",
                "MARK-144 Unslop Superpowers compositional guard skill",
                "Use when repo-specific anti-slop controls need the smallest applicable Superpowers router.",
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
                "bundle_version": "5.1.0",
                "bundle_type": "third-party-codex-plugin-projection",
                "marketplace_root": ".agents/plugins/marketplace.json",
                "plugin_root": "codex-marketplace/plugins/superpowers-plus",
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
                        "canonical_source_path": "sources/first_party/skills/unslop-superpowers",
                        "local_path": "skills/unslop-superpowers",
                        "import_status": "imported",
                        "copy_expectation": "byte_identical",
                        "provenance_note": "Projected as a directory mirror from the canonical first-party source.",
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

            with patch("validate_marketplace.ROOT", temp_root):
                try:
                    validate_superpowers_bundle_manifest(
                        bundle_manifest,
                        plugin_root="codex-marketplace/plugins/superpowers-plus",
                    )
                except ValueError as exc:  # pragma: no cover - exercised by the red test run
                    self.fail(f"validator rejected the first-party projection: {exc}")

    def test_superpowers_bundle_rejects_adapted_third_party_entry_without_overlay_path(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            source_root = temp_root / "sources" / "third_party" / "superpowers" / "obra-superpowers" / "v5.1.0"
            source_skill_root = source_root / "skills" / "using-superpowers"
            plugin_root = temp_root / "codex-marketplace" / "plugins" / "superpowers-plus"
            projected_skill_root = plugin_root / "skills" / "using-superpowers"

            skill_md = _third_party_projection_frontmatter(
                "using-superpowers",
                "using-superpowers",
                "adapters/codex/superpowers-plus/using-superpowers",
                "Use when workflow-sensitive work needs Superpowers guidance.",
            )
            _touch(
                source_skill_root / "SKILL.md",
                skill_md,
            )
            _touch(source_skill_root / "agents" / "openai.yaml", "version: 1\nmetadata: {skill_name: using-superpowers}\n")
            _touch(projected_skill_root / "SKILL.md", skill_md)
            _touch(projected_skill_root / "agents" / "openai.yaml", "version: 1\nmetadata: {skill_name: using-superpowers}\n")

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
                "bundle_version": "5.1.0",
                "bundle_type": "third-party-codex-plugin-projection",
                "marketplace_root": ".agents/plugins/marketplace.json",
                "plugin_root": "codex-marketplace/plugins/superpowers-plus",
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
                        "canonical_name": "using-superpowers",
                        "source_category": "third_party",
                        "content_mode": "adapted",
                        "canonical_source_path": "sources/third_party/superpowers/obra-superpowers/v5.1.0/skills/using-superpowers",
                        "local_path": "skills/using-superpowers",
                        "import_status": "imported",
                        "copy_expectation": "adapted_from_source",
                        "provenance_note": "Adapted to remove any claim that Superpowers skills override system, developer, runtime, or repo instructions.",
                        "adapted_author": "Harley Bartles",
                        "adaptation_note": "Reworded instruction priority for Codex marketplace compatibility.",
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
            _touch(
                plugin_root / "references" / "provenance-map.json",
                json.dumps(
                    {
                        "bundle_name": "superpowers-plus",
                        "bundle_version": "5.1.0",
                        "upstream": {
                            "repository": "https://github.com/obra/superpowers",
                            "release_tag": "v5.1.0",
                            "release_commit": "f2cbfbefebbfef77321e4c9abc9e949826bea9d7",
                            "tag_object": "ecbd610fce16d5faabcea997f17031129589b572",
                            "license": "MIT",
                        },
                        "source_custody_root": "sources/third_party/superpowers/obra-superpowers/v5.1.0",
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
                                "canonical_name": "using-superpowers",
                                "source_category": "third_party",
                                "content_mode": "adapted",
                                "canonical_source_path": "sources/third_party/superpowers/obra-superpowers/v5.1.0/skills/using-superpowers",
                                "local_path": "codex-marketplace/plugins/superpowers-plus/skills/using-superpowers",
                                "copy_expectation": "adapted_from_source",
                                "provenance_note": "Adapted to remove any claim that Superpowers skills override system, developer, runtime, or repo instructions.",
                                "adaptation_note": "Reworded instruction priority for Codex marketplace compatibility.",
                                "adapted_author": "Harley Bartles",
                            }
                        ],
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
                            "The source custody root stays verbatim, the projection layer carries the Codex-marketplace adaptations, and the installation/export layer is regenerated from the projection plus overlays.",
                        ],
                    },
                    indent=2,
                ),
            )
            _touch(plugin_root / "references" / "bundle-manifest.json", json.dumps(bundle_manifest, indent=2))

            with patch("validate_marketplace.ROOT", temp_root):
                with self.assertRaisesRegex(
                    ValueError,
                    r"superpowers-plus adapted entry using-superpowers needs adapters/codex/superpowers-plus/using-superpowers",
                ):
                    validate_superpowers_bundle_manifest(bundle_manifest, plugin_root="codex-marketplace/plugins/superpowers-plus")


if __name__ == "__main__":
    unittest.main()
