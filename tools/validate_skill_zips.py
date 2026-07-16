#!/usr/bin/env python3
"""Validate GPT-ready canonical marketplace skill.zip artifacts and the registry."""

from __future__ import annotations

import zipfile

from skill_zip_artifacts import print_registry_receipt, validate_skill_zip_registry
from skill_zip_artifacts import ROOT, load_registry


def _assert_verbatim_export_present(registry: dict) -> None:
    artifact = next(
        record
        for record in registry["artifacts"]
        if record["pack"] == "superpowers-plus" and record["skill"] == "finishing-a-development-branch"
    )
    if artifact["export_mode"] != "direct":
        raise AssertionError("expected finishing-a-development-branch to be a direct export")
    if artifact.get("overlay_path") is not None:
        raise AssertionError("expected finishing-a-development-branch to have a null overlay path")

    zip_path = ROOT / artifact["zip_path"]
    with zipfile.ZipFile(zip_path) as archive:
        skill_md = archive.read("finishing-a-development-branch/SKILL.md").decode("utf-8")
    if "Use when implementation is complete, all tests pass, and you need to decide how to integrate the work - guides completion of development work by presenting structured options for merge, PR, or cleanup" not in skill_md:
        raise AssertionError("direct skill zip does not contain the retained upstream guidance")
    if "Codex Marketplace Note" in skill_md:
        raise AssertionError("direct skill zip still contains raw Codex-specific guidance")


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


def _assert_house_skills_exports_present(registry: dict) -> None:
    worker_verification = next(
        record
        for record in registry["artifacts"]
        if record["pack"] == "house-skills" and record["skill"] == "worker-verification"
    )
    crew = next(
        record
        for record in registry["artifacts"]
        if record["pack"] == "house-skills" and record["skill"] == "crew"
    )

    if worker_verification["export_mode"] not in {"direct", "overlay"}:
        raise AssertionError("house-skills/worker-verification should export as an installable zip")
    if crew["export_mode"] not in {"direct", "overlay"}:
        raise AssertionError("house-skills/crew should export as an installable zip")

    if any(
        record["skill"] == "worker-verification" and record["pack"] == "wild-bunch-project-pack"
        for record in registry["artifacts"]
    ):
        raise AssertionError("worker-verification must not be re-added to wild-bunch-project-pack")
    if any(record["skill"] == "crew" and record["pack"] == "wild-bunch-project-pack" for record in registry["artifacts"]):
        raise AssertionError("crew must not be exposed through wild-bunch-project-pack")


def main() -> int:
    registry = load_registry()
    _assert_verbatim_export_present(registry)
    _assert_excluded_skill_present(registry)
    _assert_house_skills_exports_present(registry)
    registry = validate_skill_zip_registry()
    print_registry_receipt(registry)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
