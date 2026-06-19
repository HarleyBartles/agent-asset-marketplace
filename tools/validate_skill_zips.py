#!/usr/bin/env python3
"""Validate GPT-ready canonical marketplace skill.zip artifacts and the registry."""

from __future__ import annotations

import zipfile

from skill_zip_artifacts import print_registry_receipt, validate_skill_zip_registry
from skill_zip_artifacts import ROOT, load_registry


def _assert_overlay_export_present(registry: dict) -> None:
    artifact = next(
        record
        for record in registry["artifacts"]
        if record["pack"] == "superpowers-plus" and record["skill"] == "finishing-a-development-branch"
    )
    if artifact["export_mode"] != "overlay":
        raise AssertionError("expected finishing-a-development-branch to be an overlay export")
    if artifact["overlay_path"] != "adapters/gpt/superpowers-plus/finishing-a-development-branch":
        raise AssertionError("expected finishing-a-development-branch overlay path to match adapters/gpt")

    zip_path = ROOT / artifact["zip_path"]
    with zipfile.ZipFile(zip_path) as archive:
        skill_md = archive.read("finishing-a-development-branch/SKILL.md").decode("utf-8")
    if "Use when implementation is done and the work needs a clean closeout path." not in skill_md:
        raise AssertionError("overlay skill zip does not contain the GPT-ready closeout guidance")
    if "Codex Marketplace Note" in skill_md:
        raise AssertionError("overlay skill zip still contains raw Codex-specific guidance")


def _assert_excluded_skill_present(registry: dict) -> None:
    excluded = next(
        record
        for record in registry["excluded"]
        if record["pack"] == "superpowers-plus" and record["skill"] == "dispatching-parallel-agents"
    )
    if excluded["export_mode"] != "excluded":
        raise AssertionError("expected dispatching-parallel-agents to be excluded")
    if "subagents" not in excluded["reason"]:
        raise AssertionError("excluded skill should explain the subagent limitation")


def main() -> int:
    registry = load_registry()
    _assert_overlay_export_present(registry)
    _assert_excluded_skill_present(registry)
    registry = validate_skill_zip_registry()
    print_registry_receipt(registry)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
