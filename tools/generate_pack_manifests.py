#!/usr/bin/env python3
"""Generate deterministic pack bundle manifests.

This tool writes the bundle-manifest.json surfaces for the selected pack set.
The editable pack registry lives in `codex-marketplace/custody-pack-registry.json`
so the manifests can be regenerated from one source of truth instead of being
hand-edited.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from marketplace_utils import ROOT, load_json
from superpowers_source import load_superpowers_bundle_manifest, superpowers_source_ledger


PACK_REGISTRY_PATH = ROOT / "codex-marketplace/custody-pack-registry.json"


def _entry(
    canonical_name: str,
    *,
    source_category: str,
    source_family: str,
    canonical_source_path: str,
    local_path: str,
    content_mode: str = "verbatim",
    provenance_note: str,
    adaptation_overlay_path: str | None = None,
    adaptation_note: str | None = None,
    source_path: str | None = None,
    source_author: str | None = None,
    source_license: str | None = None,
    source_repo: str | None = None,
    adapted_author: str | None = None,
) -> dict[str, Any]:
    entry: dict[str, Any] = {
        "canonical_name": canonical_name,
        "source_category": source_category,
        "content_mode": content_mode,
        "source_family": source_family,
        "canonical_source_path": canonical_source_path,
        "local_path": local_path,
        "provenance_note": provenance_note,
    }
    if source_path is not None:
        entry["source_path"] = source_path
    if source_author is not None:
        entry["source_author"] = source_author
    if source_license is not None:
        entry["source_license"] = source_license
    if source_repo is not None:
        entry["source_repo"] = source_repo
    if adapted_author is not None:
        entry["adapted_author"] = adapted_author
    if adaptation_overlay_path is not None:
        entry["adaptation_overlay_path"] = adaptation_overlay_path
    if adaptation_note is not None:
        entry["adaptation_note"] = adaptation_note
    if content_mode == "verbatim":
        entry["copy_expectation"] = "byte_identical"
    elif content_mode == "normalised":
        entry["copy_expectation"] = "normalised_from_source"
    else:
        entry["copy_expectation"] = "adapted_from_source"
    return entry


def _repo_index(plugin_root: str, *, source_ledger: list[str], provenance_refs: list[str], agents_md: str | None = None) -> dict[str, Any]:
    return {
        "source_md": f"{plugin_root}/SOURCE.md",
        "source_ledger": source_ledger,
        "license_path": f"{plugin_root}/LICENSE",
        "bundle_manifest": f"{plugin_root}/references/bundle-manifest.json",
        "skills_path": f"{plugin_root}/skills",
        "provenance_refs": provenance_refs,
        "agents_md": agents_md,
        "registry_alignment": {
            "status": "aligned",
            "note": None,
        },
    }


def _superpowers_plus_pack() -> dict[str, Any]:
    bundle_manifest = load_superpowers_bundle_manifest()
    entries = [dict(entry) for entry in bundle_manifest.get("entries", []) if isinstance(entry, dict)]
    return {
        "bundle_name": "superpowers-plus",
        "plugin_root": "codex-marketplace/plugins/superpowers-plus",
        "bundle_version": "1.0.0",
        "bundle_type": "projection-lane",
        "is_mega_pack": False,
        "notes": [
            "Superpowers+ is the mixed projection-lane bundle for the retained Superpowers workflow skills.",
            "The bundle mixes first-party helpers, third-party verbatim skills, and adapter-backed projections.",
        ],
        "source_ledger": [
            *superpowers_source_ledger(),
        ],
        "provenance_refs": [
            "provenance/superpowers-plus.md",
            "codex-marketplace/plugins/superpowers-plus/references/source-map.md",
        ],
        "entries": entries,
    }


PACKS: list[dict[str, Any]] = [
    {
        "bundle_name": "repo-worker-pack",
        "plugin_root": "codex-marketplace/plugins/repo-worker-pack",
        "bundle_version": "1.0.0",
        "bundle_type": "projection-lane",
        "is_mega_pack": False,
        "notes": [
            "Repo worker pack combines first-party repo hygiene skills into a compositional baseline.",
            "The bundle stays first-party only and keeps the repo-worker entrypoint thin and complementary.",
        ],
        "source_ledger": [
            "sources/first_party/skills/repo-worker-base",
            "sources/first_party/skills/base-doctrine",
            "sources/first_party/skills/work-mode-router",
            "sources/first_party/skills/linear-issue-shaping",
            "sources/first_party/skills/using-linear",
            "sources/first_party/skills/boring-loop",
            "sources/first_party/skills/connector-safety",
            "sources/first_party/skills/github-operations",
            "sources/first_party/skills/unslop-plus",
            "sources/first_party/skills/context-safety",
        ],
        "provenance_refs": [
            "provenance/repo-worker-pack.md",
            "codex-marketplace/plugins/repo-worker-pack/references/source-map.md",
        ],
        "entries": [
            _entry(
                "repo-worker-base",
                source_category="first_party",
                source_family="first_party",
                canonical_source_path="sources/first_party/skills/repo-worker-base",
                local_path="skills/repo-worker-base",
                provenance_note="Projected verbatim from the first-party repo worker base skill.",
            ),
            _entry(
                "base-doctrine",
                source_category="first_party",
                source_family="first_party",
                canonical_source_path="sources/first_party/skills/base-doctrine",
                local_path="skills/base-doctrine",
                provenance_note="Projected verbatim from the first-party base-doctrine skill.",
            ),
            _entry(
                "work-mode-router",
                source_category="first_party",
                source_family="first_party",
                canonical_source_path="sources/first_party/skills/work-mode-router",
                local_path="skills/work-mode-router",
                provenance_note="Projected verbatim from the first-party work-mode-router skill.",
            ),
            _entry(
                "linear-issue-shaping",
                source_category="first_party",
                source_family="first_party",
                canonical_source_path="sources/first_party/skills/linear-issue-shaping",
                local_path="skills/linear-issue-shaping",
                provenance_note="Projected verbatim from the first-party linear-issue-shaping skill.",
            ),
            _entry(
                "using-linear",
                source_category="first_party",
                source_family="first_party",
                canonical_source_path="sources/first_party/skills/using-linear",
                local_path="skills/using-linear",
                provenance_note="Projected verbatim from the first-party using-linear skill.",
            ),
            _entry(
                "boring-loop",
                source_category="first_party",
                source_family="first_party",
                canonical_source_path="sources/first_party/skills/boring-loop",
                local_path="skills/boring-loop",
                provenance_note="Projected verbatim from the first-party boring-loop skill.",
            ),
            _entry(
                "connector-safety",
                source_category="first_party",
                source_family="first_party",
                canonical_source_path="sources/first_party/skills/connector-safety",
                local_path="skills/connector-safety",
                provenance_note="Projected verbatim from the first-party connector-safety skill.",
            ),
            _entry(
                "github-operations",
                source_category="first_party",
                source_family="first_party",
                canonical_source_path="sources/first_party/skills/github-operations",
                local_path="skills/github-operations",
                provenance_note="Projected verbatim from the first-party github-operations skill.",
            ),
            _entry(
                "unslop-plus",
                source_category="first_party",
                source_family="first_party",
                canonical_source_path="sources/first_party/skills/unslop-plus",
                local_path="skills/unslop-plus",
                provenance_note="Projected verbatim from the first-party unslop-plus skill.",
            ),
            _entry(
                "context-safety",
                source_category="first_party",
                source_family="first_party",
                canonical_source_path="sources/first_party/skills/context-safety",
                local_path="skills/context-safety",
                provenance_note="Projected verbatim from the first-party context-safety skill.",
            ),
        ],
    },
    _superpowers_plus_pack(),
    {
        "bundle_name": "security-pack",
        "plugin_root": "codex-marketplace/plugins/security-pack",
        "bundle_version": "1.0.0",
        "bundle_type": "projection-lane",
        "is_mega_pack": False,
        "notes": [
            "Security pack combines the retained Claude Cortex security foundations with the selected ECC safety and security-review skills.",
            "The bundle keeps the existing security foundations while adding the ECC security slice in the same topical home.",
        ],
        "source_ledger": [
            "sources/third_party/claude-cortex/upstream/skills/owasp-top-10",
            "sources/third_party/claude-cortex/upstream/skills/secure-coding-practices",
            "sources/third_party/claude-cortex/upstream/skills/security-testing-patterns",
            "sources/third_party/claude-cortex/upstream/skills/threat-modeling-techniques",
            "sources/third_party/ecc/upstream/source-custody.md",
        ],
        "provenance_refs": [
            "provenance/security-pack.md",
            "provenance/ecc-domain-packs.md",
            "codex-marketplace/plugins/security-pack/references/source-map.md",
        ],
        "entries": [
            _entry(
                "owasp-top-10",
                source_category="third_party",
                source_family="claude-cortex",
                canonical_source_path="sources/third_party/claude-cortex/upstream/skills/owasp-top-10",
                local_path="skills/owasp-top-10",
                content_mode="normalised",
                provenance_note="Normalised from the retained Claude Cortex snapshot with metadata and path rewrites.",
                adaptation_overlay_path="adapters/codex/security-pack/owasp-top-10",
                adaptation_note="Keep the skill body intact while adapting the projection metadata and path layout.",
                source_path="sources/third_party/claude-cortex/upstream/skills/owasp-top-10/SKILL.md",
                source_author="NickCrew",
                source_license="MIT",
                source_repo="https://github.com/NickCrew/Claude-Cortex",
                adapted_author="Harley Bartles",
            ),
            _entry(
                "secure-coding-practices",
                source_category="third_party",
                source_family="claude-cortex",
                canonical_source_path="sources/third_party/claude-cortex/upstream/skills/secure-coding-practices",
                local_path="skills/secure-coding-practices",
                content_mode="normalised",
                provenance_note="Normalised from the retained Claude Cortex snapshot with metadata and path rewrites.",
                adaptation_overlay_path="adapters/codex/security-pack/secure-coding-practices",
                adaptation_note="Keep the skill body intact while adapting the projection metadata and path layout.",
                source_path="sources/third_party/claude-cortex/upstream/skills/secure-coding-practices/SKILL.md",
                source_author="NickCrew",
                source_license="MIT",
                source_repo="https://github.com/NickCrew/Claude-Cortex",
                adapted_author="Harley Bartles",
            ),
            _entry(
                "security-testing-patterns",
                source_category="third_party",
                source_family="claude-cortex",
                canonical_source_path="sources/third_party/claude-cortex/upstream/skills/security-testing-patterns",
                local_path="skills/security-testing-patterns",
                content_mode="normalised",
                provenance_note="Normalised from the retained Claude Cortex snapshot with metadata and path rewrites.",
                adaptation_overlay_path="adapters/codex/security-pack/security-testing-patterns",
                adaptation_note="Keep the skill body intact while adapting the projection metadata and path layout.",
                source_path="sources/third_party/claude-cortex/upstream/skills/security-testing-patterns/SKILL.md",
                source_author="NickCrew",
                source_license="MIT",
                source_repo="https://github.com/NickCrew/Claude-Cortex",
                adapted_author="Harley Bartles",
            ),
            _entry(
                "threat-modeling-techniques",
                source_category="third_party",
                source_family="claude-cortex",
                canonical_source_path="sources/third_party/claude-cortex/upstream/skills/threat-modeling-techniques",
                local_path="skills/threat-modeling-techniques",
                content_mode="normalised",
                provenance_note="Normalised from the retained Claude Cortex snapshot with metadata and path rewrites.",
                adaptation_overlay_path="adapters/codex/security-pack/threat-modeling-techniques",
                adaptation_note="Keep the skill body intact while adapting the projection metadata and path layout.",
                source_path="sources/third_party/claude-cortex/upstream/skills/threat-modeling-techniques/SKILL.md",
                source_author="NickCrew",
                source_license="MIT",
                source_repo="https://github.com/NickCrew/Claude-Cortex",
                adapted_author="Harley Bartles",
            ),
            _entry(
                "safety-guard",
                source_category="third_party",
                source_family="ecc",
                canonical_source_path="sources/third_party/ecc/upstream/skills/safety-guard",
                local_path="skills/safety-guard",
                provenance_note="Projected verbatim from retained ECC custody as the safety guard complement to the existing security foundations.",
                source_path="sources/third_party/ecc/upstream/skills/safety-guard/SKILL.md",
                source_author="Affaan Mustafa",
                source_license="MIT",
                source_repo="https://github.com/affaan-m/ECC",
            ),
            _entry(
                "security-review",
                source_category="third_party",
                source_family="ecc",
                canonical_source_path="sources/third_party/ecc/upstream/skills/security-review",
                local_path="skills/security-review",
                content_mode="normalised",
                provenance_note="Normalised from retained ECC custody by moving the companion infrastructure guide under references/.",
                adaptation_overlay_path="adapters/codex/security-pack/security-review",
                adaptation_note="Move the loose cloud infrastructure companion into canonical references/ and keep the skill body pointed at the internal reference.",
                source_path="sources/third_party/ecc/upstream/skills/security-review/SKILL.md",
                source_author="ECC",
                source_license="MIT",
                source_repo="https://github.com/affaan-m/ECC",
                adapted_author="Harley Bartles",
            ),
        ],
    },
    {
        "bundle_name": "agentic-workflows",
        "plugin_root": "codex-marketplace/plugins/agentic-workflows",
        "bundle_version": "1.0.0",
        "bundle_type": "projection-lane",
        "is_mega_pack": False,
        "notes": [
            "Agentic workflows pack groups the selected ECC workflow mechanics into one topical home.",
            "The pack keeps the workflow-facing skills together so they can be projected as a complementary bundle instead of a superpowers-themed wrapper.",
        ],
        "source_ledger": [
            "sources/third_party/ecc/upstream/source-custody.md",
            "sources/third_party/ecc/upstream/manifest.json",
            "sources/third_party/ecc/upstream/LICENSE",
        ],
        "provenance_refs": [
            "provenance/ecc-domain-packs.md",
            "codex-marketplace/plugins/agentic-workflows/references/source-map.md",
        ],
        "entries": [
            _entry(
                "agent-harness-construction",
                source_category="third_party",
                source_family="ecc",
                canonical_source_path="sources/third_party/ecc/upstream/skills/agent-harness-construction",
                local_path="skills/agent-harness-construction",
                provenance_note="Projected verbatim from retained ECC custody into the agentic workflows pack.",
                source_path="sources/third_party/ecc/upstream/skills/agent-harness-construction/SKILL.md",
                source_author="Affaan Mustafa",
                source_license="MIT",
                source_repo="https://github.com/affaan-m/ECC",
            ),
            _entry(
                "autonomous-agent-harness",
                source_category="third_party",
                source_family="ecc",
                canonical_source_path="sources/third_party/ecc/upstream/skills/autonomous-agent-harness",
                local_path="skills/autonomous-agent-harness",
                provenance_note="Projected verbatim from retained ECC custody into the agentic workflows pack.",
                source_path="sources/third_party/ecc/upstream/skills/autonomous-agent-harness/SKILL.md",
                source_author="Affaan Mustafa",
                source_license="MIT",
                source_repo="https://github.com/affaan-m/ECC",
            ),
            _entry(
                "continuous-agent-loop",
                source_category="third_party",
                source_family="ecc",
                canonical_source_path="sources/third_party/ecc/upstream/skills/continuous-agent-loop",
                local_path="skills/continuous-agent-loop",
                provenance_note="Projected verbatim from retained ECC custody into the agentic workflows pack.",
                source_path="sources/third_party/ecc/upstream/skills/continuous-agent-loop/SKILL.md",
                source_author="Affaan Mustafa",
                source_license="MIT",
                source_repo="https://github.com/affaan-m/ECC",
            ),
            _entry(
                "dynamic-workflow-mode",
                source_category="third_party",
                source_family="ecc",
                canonical_source_path="sources/third_party/ecc/upstream/skills/dynamic-workflow-mode",
                local_path="skills/dynamic-workflow-mode",
                provenance_note="Projected verbatim from retained ECC custody into the agentic workflows pack.",
                source_path="sources/third_party/ecc/upstream/skills/dynamic-workflow-mode/SKILL.md",
                source_author="Affaan Mustafa",
                source_license="MIT",
                source_repo="https://github.com/affaan-m/ECC",
            ),
            _entry(
                "dmux-workflows",
                source_category="third_party",
                source_family="ecc",
                canonical_source_path="sources/third_party/ecc/upstream/skills/dmux-workflows",
                local_path="skills/dmux-workflows",
                provenance_note="Projected verbatim from retained ECC custody into the agentic workflows pack.",
                source_path="sources/third_party/ecc/upstream/skills/dmux-workflows/SKILL.md",
                source_author="Affaan Mustafa",
                source_license="MIT",
                source_repo="https://github.com/affaan-m/ECC",
            ),
            _entry(
                "agentic-os",
                source_category="third_party",
                source_family="ecc",
                canonical_source_path="sources/third_party/ecc/upstream/skills/agentic-os",
                local_path="skills/agentic-os",
                provenance_note="Projected verbatim from retained ECC custody into the agentic workflows pack.",
                source_path="sources/third_party/ecc/upstream/skills/agentic-os/SKILL.md",
                source_author="Affaan Mustafa",
                source_license="MIT",
                source_repo="https://github.com/affaan-m/ECC",
            ),
        ],
    },
    {
        "bundle_name": "agentic-evaluation",
        "plugin_root": "codex-marketplace/plugins/agentic-evaluation",
        "bundle_version": "1.0.0",
        "bundle_type": "projection-lane",
        "is_mega_pack": False,
        "notes": [
            "Agentic evaluation pack groups the scoring and audit skills that help decide whether an agent workflow is actually earning its keep.",
            "The pack keeps the evaluation rubric and the architectural audit surface together as a complementary home.",
        ],
        "source_ledger": [
            "sources/third_party/ecc/upstream/source-custody.md",
            "sources/third_party/ecc/upstream/manifest.json",
            "sources/third_party/ecc/upstream/LICENSE",
        ],
        "provenance_refs": [
            "provenance/ecc-domain-packs.md",
            "codex-marketplace/plugins/agentic-evaluation/references/source-map.md",
        ],
        "entries": [
            _entry(
                "agent-self-evaluation",
                source_category="third_party",
                source_family="ecc",
                canonical_source_path="sources/third_party/ecc/upstream/skills/agent-self-evaluation",
                local_path="skills/agent-self-evaluation",
                content_mode="normalised",
                provenance_note="Normalised from retained ECC custody by moving examples and templates into canonical references/ folders.",
                adaptation_overlay_path="adapters/codex/agentic-evaluation/agent-self-evaluation",
                adaptation_note="Move examples/ and templates/ into references/ and repoint the evaluation report template link to the internal references folder.",
                source_path="sources/third_party/ecc/upstream/skills/agent-self-evaluation/SKILL.md",
                source_author="ECC",
                source_license="MIT",
                source_repo="https://github.com/affaan-m/ECC",
                adapted_author="Harley Bartles",
            ),
            _entry(
                "agent-eval",
                source_category="third_party",
                source_family="ecc",
                canonical_source_path="sources/third_party/ecc/upstream/skills/agent-eval",
                local_path="skills/agent-eval",
                provenance_note="Projected verbatim from retained ECC custody into the agentic evaluation pack.",
                source_path="sources/third_party/ecc/upstream/skills/agent-eval/SKILL.md",
                source_author="Affaan Mustafa",
                source_license="MIT",
                source_repo="https://github.com/affaan-m/ECC",
            ),
            _entry(
                "agent-architecture-audit",
                source_category="third_party",
                source_family="ecc",
                canonical_source_path="sources/third_party/ecc/upstream/skills/agent-architecture-audit",
                local_path="skills/agent-architecture-audit",
                provenance_note="Projected verbatim from retained ECC custody into the agentic evaluation pack.",
                source_path="sources/third_party/ecc/upstream/skills/agent-architecture-audit/SKILL.md",
                source_author="Affaan Mustafa",
                source_license="MIT",
                source_repo="https://github.com/affaan-m/ECC",
            ),
        ],
    },
    {
        "bundle_name": "research-pack",
        "plugin_root": "codex-marketplace/plugins/research-pack",
        "bundle_version": "1.0.0",
        "bundle_type": "projection-lane",
        "is_mega_pack": False,
        "notes": [
            "Research pack keeps the evidence-first research workflow as its own domain home.",
            "The pack is intentionally small so it complements other workflow packs instead of duplicating them.",
        ],
        "source_ledger": [
            "sources/third_party/ecc/upstream/source-custody.md",
            "sources/third_party/ecc/upstream/manifest.json",
            "sources/third_party/ecc/upstream/LICENSE",
        ],
        "provenance_refs": [
            "provenance/ecc-domain-packs.md",
            "codex-marketplace/plugins/research-pack/references/source-map.md",
        ],
        "entries": [
            _entry(
                "research-ops",
                source_category="third_party",
                source_family="ecc",
                canonical_source_path="sources/third_party/ecc/upstream/skills/research-ops",
                local_path="skills/research-ops",
                provenance_note="Projected verbatim from retained ECC custody into the research pack.",
                source_path="sources/third_party/ecc/upstream/skills/research-ops/SKILL.md",
                source_author="Affaan Mustafa",
                source_license="MIT",
                source_repo="https://github.com/affaan-m/ECC",
            ),
        ],
    },
    {
        "bundle_name": "engineering-pack",
        "plugin_root": "codex-marketplace/plugins/engineering-pack",
        "bundle_version": "1.0.0",
        "bundle_type": "projection-lane",
        "is_mega_pack": False,
        "notes": [
            "Engineering pack groups the selected ECC implementation and deployment skills into a practical delivery home.",
            "The pack is narrow and complementary: it covers engineering execution without absorbing the broader workflow packs.",
        ],
        "source_ledger": [
            "sources/third_party/ecc/upstream/source-custody.md",
            "sources/third_party/ecc/upstream/manifest.json",
            "sources/third_party/ecc/upstream/LICENSE",
        ],
        "provenance_refs": [
            "provenance/ecc-domain-packs.md",
            "codex-marketplace/plugins/engineering-pack/references/source-map.md",
        ],
        "entries": [
            _entry(
                "ai-first-engineering",
                source_category="third_party",
                source_family="ecc",
                canonical_source_path="sources/third_party/ecc/upstream/skills/ai-first-engineering",
                local_path="skills/ai-first-engineering",
                provenance_note="Projected verbatim from retained ECC custody into the engineering pack.",
                source_path="sources/third_party/ecc/upstream/skills/ai-first-engineering/SKILL.md",
                source_author="Affaan Mustafa",
                source_license="MIT",
                source_repo="https://github.com/affaan-m/ECC",
            ),
            _entry(
                "deployment-patterns",
                source_category="third_party",
                source_family="ecc",
                canonical_source_path="sources/third_party/ecc/upstream/skills/deployment-patterns",
                local_path="skills/deployment-patterns",
                provenance_note="Projected verbatim from retained ECC custody into the engineering pack.",
                source_path="sources/third_party/ecc/upstream/skills/deployment-patterns/SKILL.md",
                source_author="Affaan Mustafa",
                source_license="MIT",
                source_repo="https://github.com/affaan-m/ECC",
            ),
        ],
    },
    {
        "bundle_name": "everything-codex-code",
        "plugin_root": "codex-marketplace/plugins/everything-codex-code",
        "bundle_version": "1.0.0",
        "bundle_type": "projection-lane",
        "is_mega_pack": True,
        "mega_pack_for": "ecc",
        "notes": [
            "Mega pack containing every selected ECC skill projected into the marketplace this issue.",
            "This pack exists as a reference bundle for the full selected ECC slice, not as a replacement for the topical packs.",
        ],
        "source_ledger": [
            "sources/third_party/ecc/upstream/source-custody.md",
            "sources/third_party/ecc/upstream/manifest.json",
            "sources/third_party/ecc/upstream/LICENSE",
        ],
        "provenance_refs": [
            "provenance/ecc-domain-packs.md",
            "codex-marketplace/plugins/everything-codex-code/references/source-map.md",
        ],
        "entries": [
            _entry(
                "agent-harness-construction",
                source_category="third_party",
                source_family="ecc",
                canonical_source_path="sources/third_party/ecc/upstream/skills/agent-harness-construction",
                local_path="skills/agent-harness-construction",
                provenance_note="Projected verbatim from retained ECC custody into the everything-codex-code mega pack.",
                source_path="sources/third_party/ecc/upstream/skills/agent-harness-construction/SKILL.md",
                source_author="Affaan Mustafa",
                source_license="MIT",
                source_repo="https://github.com/affaan-m/ECC",
            ),
            _entry(
                "autonomous-agent-harness",
                source_category="third_party",
                source_family="ecc",
                canonical_source_path="sources/third_party/ecc/upstream/skills/autonomous-agent-harness",
                local_path="skills/autonomous-agent-harness",
                provenance_note="Projected verbatim from retained ECC custody into the everything-codex-code mega pack.",
                source_path="sources/third_party/ecc/upstream/skills/autonomous-agent-harness/SKILL.md",
                source_author="Affaan Mustafa",
                source_license="MIT",
                source_repo="https://github.com/affaan-m/ECC",
            ),
            _entry(
                "continuous-agent-loop",
                source_category="third_party",
                source_family="ecc",
                canonical_source_path="sources/third_party/ecc/upstream/skills/continuous-agent-loop",
                local_path="skills/continuous-agent-loop",
                provenance_note="Projected verbatim from retained ECC custody into the everything-codex-code mega pack.",
                source_path="sources/third_party/ecc/upstream/skills/continuous-agent-loop/SKILL.md",
                source_author="Affaan Mustafa",
                source_license="MIT",
                source_repo="https://github.com/affaan-m/ECC",
            ),
            _entry(
                "dynamic-workflow-mode",
                source_category="third_party",
                source_family="ecc",
                canonical_source_path="sources/third_party/ecc/upstream/skills/dynamic-workflow-mode",
                local_path="skills/dynamic-workflow-mode",
                provenance_note="Projected verbatim from retained ECC custody into the everything-codex-code mega pack.",
                source_path="sources/third_party/ecc/upstream/skills/dynamic-workflow-mode/SKILL.md",
                source_author="Affaan Mustafa",
                source_license="MIT",
                source_repo="https://github.com/affaan-m/ECC",
            ),
            _entry(
                "dmux-workflows",
                source_category="third_party",
                source_family="ecc",
                canonical_source_path="sources/third_party/ecc/upstream/skills/dmux-workflows",
                local_path="skills/dmux-workflows",
                provenance_note="Projected verbatim from retained ECC custody into the everything-codex-code mega pack.",
                source_path="sources/third_party/ecc/upstream/skills/dmux-workflows/SKILL.md",
                source_author="Affaan Mustafa",
                source_license="MIT",
                source_repo="https://github.com/affaan-m/ECC",
            ),
            _entry(
                "agentic-os",
                source_category="third_party",
                source_family="ecc",
                canonical_source_path="sources/third_party/ecc/upstream/skills/agentic-os",
                local_path="skills/agentic-os",
                provenance_note="Projected verbatim from retained ECC custody into the everything-codex-code mega pack.",
                source_path="sources/third_party/ecc/upstream/skills/agentic-os/SKILL.md",
                source_author="Affaan Mustafa",
                source_license="MIT",
                source_repo="https://github.com/affaan-m/ECC",
            ),
            _entry(
                "agent-self-evaluation",
                source_category="third_party",
                source_family="ecc",
                canonical_source_path="sources/third_party/ecc/upstream/skills/agent-self-evaluation",
                local_path="skills/agent-self-evaluation",
                content_mode="normalised",
                provenance_note="Normalised from retained ECC custody by moving examples and templates into canonical references/ folders.",
                adaptation_overlay_path="adapters/codex/agentic-evaluation/agent-self-evaluation",
                adaptation_note="Move examples/ and templates/ into references/ and repoint the evaluation report template link to the internal references folder.",
                source_path="sources/third_party/ecc/upstream/skills/agent-self-evaluation/SKILL.md",
                source_author="ECC",
                source_license="MIT",
                source_repo="https://github.com/affaan-m/ECC",
                adapted_author="Harley Bartles",
            ),
            _entry(
                "agent-eval",
                source_category="third_party",
                source_family="ecc",
                canonical_source_path="sources/third_party/ecc/upstream/skills/agent-eval",
                local_path="skills/agent-eval",
                provenance_note="Projected verbatim from retained ECC custody into the everything-codex-code mega pack.",
                source_path="sources/third_party/ecc/upstream/skills/agent-eval/SKILL.md",
                source_author="Affaan Mustafa",
                source_license="MIT",
                source_repo="https://github.com/affaan-m/ECC",
            ),
            _entry(
                "agent-architecture-audit",
                source_category="third_party",
                source_family="ecc",
                canonical_source_path="sources/third_party/ecc/upstream/skills/agent-architecture-audit",
                local_path="skills/agent-architecture-audit",
                provenance_note="Projected verbatim from retained ECC custody into the everything-codex-code mega pack.",
                source_path="sources/third_party/ecc/upstream/skills/agent-architecture-audit/SKILL.md",
                source_author="Affaan Mustafa",
                source_license="MIT",
                source_repo="https://github.com/affaan-m/ECC",
            ),
            _entry(
                "research-ops",
                source_category="third_party",
                source_family="ecc",
                canonical_source_path="sources/third_party/ecc/upstream/skills/research-ops",
                local_path="skills/research-ops",
                provenance_note="Projected verbatim from retained ECC custody into the everything-codex-code mega pack.",
                source_path="sources/third_party/ecc/upstream/skills/research-ops/SKILL.md",
                source_author="Affaan Mustafa",
                source_license="MIT",
                source_repo="https://github.com/affaan-m/ECC",
            ),
            _entry(
                "ai-first-engineering",
                source_category="third_party",
                source_family="ecc",
                canonical_source_path="sources/third_party/ecc/upstream/skills/ai-first-engineering",
                local_path="skills/ai-first-engineering",
                provenance_note="Projected verbatim from retained ECC custody into the everything-codex-code mega pack.",
                source_path="sources/third_party/ecc/upstream/skills/ai-first-engineering/SKILL.md",
                source_author="Affaan Mustafa",
                source_license="MIT",
                source_repo="https://github.com/affaan-m/ECC",
            ),
            _entry(
                "deployment-patterns",
                source_category="third_party",
                source_family="ecc",
                canonical_source_path="sources/third_party/ecc/upstream/skills/deployment-patterns",
                local_path="skills/deployment-patterns",
                provenance_note="Projected verbatim from retained ECC custody into the everything-codex-code mega pack.",
                source_path="sources/third_party/ecc/upstream/skills/deployment-patterns/SKILL.md",
                source_author="Affaan Mustafa",
                source_license="MIT",
                source_repo="https://github.com/affaan-m/ECC",
            ),
            _entry(
                "search-first",
                source_category="third_party",
                source_family="ecc",
                canonical_source_path="sources/third_party/ecc/upstream/skills/search-first",
                local_path="skills/search-first",
                provenance_note="Projected verbatim from retained ECC custody into the everything-codex-code mega pack.",
                source_path="sources/third_party/ecc/upstream/skills/search-first/SKILL.md",
                source_author="Affaan Mustafa",
                source_license="MIT",
                source_repo="https://github.com/affaan-m/ECC",
            ),
            _entry(
                "safety-guard",
                source_category="third_party",
                source_family="ecc",
                canonical_source_path="sources/third_party/ecc/upstream/skills/safety-guard",
                local_path="skills/safety-guard",
                provenance_note="Projected verbatim from retained ECC custody into the everything-codex-code mega pack.",
                source_path="sources/third_party/ecc/upstream/skills/safety-guard/SKILL.md",
                source_author="Affaan Mustafa",
                source_license="MIT",
                source_repo="https://github.com/affaan-m/ECC",
            ),
            _entry(
                "security-review",
                source_category="third_party",
                source_family="ecc",
                canonical_source_path="sources/third_party/ecc/upstream/skills/security-review",
                local_path="skills/security-review",
                content_mode="normalised",
                provenance_note="Normalised from retained ECC custody by moving the companion infrastructure guide under references/.",
                adaptation_overlay_path="adapters/codex/security-pack/security-review",
                adaptation_note="Move the loose cloud infrastructure companion into canonical references/ and keep the skill body pointed at the internal reference.",
                source_path="sources/third_party/ecc/upstream/skills/security-review/SKILL.md",
                source_author="ECC",
                source_license="MIT",
                source_repo="https://github.com/affaan-m/ECC",
                adapted_author="Harley Bartles",
            ),
        ],
    },
]


def load_pack_registry() -> list[dict[str, Any]]:
    registry = load_json(PACK_REGISTRY_PATH)
    if registry.get("schema_version") != 1:
        raise ValueError(f"{PACK_REGISTRY_PATH}: schema_version must be 1")
    packs = registry.get("packs")
    if not isinstance(packs, list) or not packs:
        raise ValueError(f"{PACK_REGISTRY_PATH}: packs must be a non-empty list")
    normalized = [pack for pack in packs if isinstance(pack, dict)]
    if len(normalized) != len(packs):
        raise ValueError(f"{PACK_REGISTRY_PATH}: packs must contain objects")
    return normalized


def _bundle_manifest(pack: dict[str, Any]) -> dict[str, Any]:
    entries = sorted(pack["entries"], key=lambda item: item["canonical_name"])
    source_families = sorted({entry["source_family"] for entry in entries})
    manifest: dict[str, Any] = {
        "bundle_name": pack["bundle_name"],
        "bundle_version": pack["bundle_version"],
        "bundle_type": pack["bundle_type"],
        "plugin_root": pack["plugin_root"],
        "is_mega_pack": pack["is_mega_pack"],
        "source_families": source_families,
        "notes": pack["notes"],
        "provenance_refs": pack["provenance_refs"],
        "plugin_author": "Harley Bartles",
        "plugin_license": "MIT",
        "entries": entries,
    }
    if not pack.get("is_mega_pack"):
        manifest["repo_index"] = _repo_index(
            pack["plugin_root"],
            source_ledger=pack["source_ledger"],
            provenance_refs=pack["provenance_refs"],
        )
    if pack.get("mega_pack_for") is not None:
        manifest["mega_pack_for"] = pack["mega_pack_for"]
    return manifest


def _write_manifest(path: Path, manifest: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def generate(*, write: bool) -> None:
    for pack in load_pack_registry():
        if pack.get("is_mega_pack"):
            continue
        manifest = _bundle_manifest(pack)
        manifest_path = ROOT / pack["plugin_root"] / "references" / "bundle-manifest.json"
        if write:
            _write_manifest(manifest_path, manifest)
            print(f"WROTE {manifest_path.relative_to(ROOT)}")
            continue
        if not manifest_path.exists():
            raise FileNotFoundError(manifest_path)
        current = json.loads(manifest_path.read_text(encoding="utf-8"))
        if current != manifest:
            raise ValueError(f"{manifest_path.relative_to(ROOT)} is stale; run py -3 tools/generate_pack_manifests.py")
        print(f"OK   {manifest_path.relative_to(ROOT)}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate or validate the selected pack bundle manifests")
    parser.add_argument("--check", action="store_true", help="validate without writing")
    args = parser.parse_args()
    generate(write=not args.check)
    if args.check:
        print("OK pack manifests: current")
    else:
        print("OK pack manifests: generated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
