#!/usr/bin/env python3
"""GPT export manifest and staged overlay helpers for canonical skill zips."""

from __future__ import annotations

import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from marketplace_utils import load_json
from skill_overlay_materializer import stage_overlay_tree


ROOT = Path(__file__).resolve().parents[1]
GPT_OVERLAYS_ROOT = ROOT / "gpt-overlays"
GPT_EXPORT_MANIFEST_PATH = GPT_OVERLAYS_ROOT / "manifest.json"


@dataclass(frozen=True)
class GPTExportPolicy:
    export_mode: str
    reason: str | None = None
    overlay_path: str | None = None
    overlay_root: Path | None = None


def load_gpt_export_manifest() -> dict[str, Any]:
    if not GPT_EXPORT_MANIFEST_PATH.exists():
        raise FileNotFoundError(GPT_EXPORT_MANIFEST_PATH)
    return load_json(GPT_EXPORT_MANIFEST_PATH)


def _build_policy_index() -> tuple[str, dict[tuple[str, str], GPTExportPolicy]]:
    manifest = load_gpt_export_manifest()
    default_export_mode = str(manifest.get("default_export_mode", "direct"))
    policy_index: dict[tuple[str, str], GPTExportPolicy] = {}

    for pack_entry in manifest.get("packs", []):
        if not isinstance(pack_entry, dict):
            raise ValueError("gpt export manifest contains a malformed pack entry")
        pack_name = pack_entry.get("pack")
        if not isinstance(pack_name, str) or not pack_name:
            raise ValueError("gpt export manifest contains a pack without a name")
        for skill_entry in pack_entry.get("skills", []):
            if not isinstance(skill_entry, dict):
                raise ValueError(f"gpt export manifest pack {pack_name} contains a malformed skill entry")
            skill_name = skill_entry.get("skill")
            export_mode = skill_entry.get("export_mode")
            if not isinstance(skill_name, str) or not skill_name:
                raise ValueError(f"gpt export manifest pack {pack_name} contains a skill without a name")
            if export_mode not in {"direct", "overlay", "excluded"}:
                raise ValueError(
                    f"gpt export manifest pack {pack_name}/{skill_name} has an invalid export mode: {export_mode}"
                )

            overlay_path = skill_entry.get("overlay_path")
            reason = skill_entry.get("reason")
            overlay_root = None
            if export_mode == "overlay":
                if not isinstance(overlay_path, str) or not overlay_path:
                    raise ValueError(f"gpt export manifest pack {pack_name}/{skill_name} is missing overlay_path")
                overlay_root = (ROOT / overlay_path).resolve()
                if not overlay_root.exists():
                    raise FileNotFoundError(overlay_root)
            if export_mode == "excluded":
                if not isinstance(reason, str) or not reason:
                    raise ValueError(f"gpt export manifest pack {pack_name}/{skill_name} is missing an exclusion reason")
            policy_index[(pack_name, skill_name)] = GPTExportPolicy(
                export_mode=str(export_mode),
                reason=str(reason) if isinstance(reason, str) else None,
                overlay_path=str(overlay_path) if isinstance(overlay_path, str) else None,
                overlay_root=overlay_root,
            )

    return default_export_mode, policy_index


def resolve_gpt_export_policy(*, pack: str, skill: str) -> GPTExportPolicy:
    default_export_mode, policy_index = _build_policy_index()
    policy = policy_index.get((pack, skill))
    if policy is not None:
        return policy
    if pack == "superpowers":
        raise ValueError(f"gpt export manifest is missing a classification for {pack}/{skill}")
    return GPTExportPolicy(export_mode=default_export_mode)


def stage_skill_tree(source_root: Path, overlay_root: Path | None) -> tuple[Path, tempfile.TemporaryDirectory[str]]:
    return stage_overlay_tree(source_root, overlay_root)

