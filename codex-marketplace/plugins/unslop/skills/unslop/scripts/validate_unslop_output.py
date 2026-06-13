#!/usr/bin/env python3
"""Validate an unslop-output directory."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


REQUIRED = [
    "manifest.json",
    "prompts.json",
]


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def forbidden_fragments() -> list[str]:
    return [
        "git " + "clone https://github.com/mshumer/unslop",
        "claude" + " -p",
        "requires " + "Claude Code",
    ]


def validate_prompts_only_manifest(manifest: dict, path: Path) -> list[str]:
    issues: list[str] = []
    if manifest.get("tool") != "asset-marketplace-unslop":
        issues.append("manifest tool mismatch")
    if manifest.get("output_contract") != "unslop-prompts-only/v1":
        issues.append("manifest output contract mismatch")
    domain = str(manifest.get("domain", ""))
    if not domain:
        issues.append("manifest domain is missing")
    if manifest.get("type") not in {"text", "visual"}:
        issues.append("manifest type is invalid")
    if manifest.get("upstream_provenance", {}).get("commit") != "edcb62386d129c65e4395f0cfcc9168eb1ba2148":
        issues.append("manifest missing pinned upstream commit")
    prompts = load_json(path / "prompts.json")
    prompt_count = manifest.get("prompts", {}).get("count")
    if not isinstance(prompt_count, int) or prompt_count != len(prompts):
        issues.append("prompt count does not match prompts.json")
    if manifest.get("validation", {}).get("passed") is not True:
        issues.append("manifest validation result is not passed")
    if manifest.get("validation", {}).get("issues") not in ([], None):
        issues.append("manifest validation issues must be empty for prompts-only output")
    if manifest.get("validation", {}).get("path") != "validation.md":
        issues.append("manifest validation path mismatch")
    if manifest.get("samples", {}).get("count") != 0:
        issues.append("prompts-only sample count must be zero")
    if manifest.get("visual_evidence", {}).get("status") not in {"not_requested", "skipped"}:
        issues.append("prompts-only visual evidence status must be not_requested or skipped")
    if path.joinpath("samples").exists() or path.joinpath("analysis.md").exists() or path.joinpath("skill.md").exists() or path.joinpath("validation.md").exists() or path.joinpath("before-after").exists():
        issues.append("prompts-only output should not create full-run support files")
    return issues


def validate(path: Path) -> list[str]:
    issues: list[str] = []
    for required in REQUIRED:
        if not (path / required).exists():
            issues.append(f"missing {required}")

    if issues:
        return issues

    manifest = load_json(path / "manifest.json")
    output_contract = str(manifest.get("output_contract", "unslop-output/v1"))
    prompts_only = output_contract == "unslop-prompts-only/v1"

    if prompts_only:
        if len(list(path.iterdir())) != 2:
            issues.append("prompts-only output should contain only manifest.json and prompts.json")
        issues.extend(validate_prompts_only_manifest(manifest, path))
        return issues

    if not (path / "samples").exists():
        issues.append("missing samples")
    if not (path / "analysis.md").exists():
        issues.append("missing analysis.md")
    if not (path / "skill.md").exists():
        issues.append("missing skill.md")
    if not (path / "validation.md").exists():
        issues.append("missing validation.md")
    if not (path / "before-after").exists():
        issues.append("missing before-after")
    if issues:
        return issues

    analysis = (path / "analysis.md").read_text(encoding="utf-8")
    skill = (path / "skill.md").read_text(encoding="utf-8")
    validation = (path / "validation.md").read_text(encoding="utf-8")

    domain = str(manifest.get("domain", ""))
    if not domain or domain.lower() not in analysis.lower():
        issues.append("analysis.md is not domain-specific")
    if manifest.get("tool") != "asset-marketplace-unslop":
        issues.append("manifest tool mismatch")
    if manifest.get("upstream_provenance", {}).get("commit") != "edcb62386d129c65e4395f0cfcc9168eb1ba2148":
        issues.append("manifest missing pinned upstream commit")
    sample_count = manifest.get("samples", {}).get("count")
    if not isinstance(sample_count, int) or sample_count < 2:
        issues.append("manifest sample count is too low")
    if len(list((path / "samples").iterdir())) != sample_count:
        issues.append("sample file count does not match manifest")
    if len(re.findall(r"\b\d+\b", analysis)) < 3:
        issues.append("analysis.md lacks counted evidence")
    avoid_count = len(re.findall(r"\b(do not|avoid|never)\b", skill.lower()))
    if avoid_count < 6:
        issues.append("skill.md is too generic or weak")
    if "Generated from local samples" not in skill:
        issues.append("skill.md does not identify itself as a draft from local samples")
    visual = manifest.get("visual_evidence", {})
    if manifest.get("type") == "visual" and visual.get("status") not in {"ran", "skipped"}:
        issues.append("visual evidence status is not cleanly recorded")
    manifest_validation = manifest.get("validation", {})
    if manifest_validation.get("path") != "validation.md":
        issues.append("manifest validation path mismatch")
    if manifest_validation.get("passed") is not True:
        issues.append("manifest validation result is not passed")
    if manifest_validation.get("issues") not in ([], None):
        issues.append("manifest validation issues must be empty for a passing run")
    if "Status: passed" not in validation:
        issues.append("validation.md does not record a passed state")
    if manifest_validation.get("passed") is True and "Status: passed" not in validation:
        issues.append("manifest and validation.md disagree on passed state")

    active_text = "\n".join(
        file.read_text(encoding="utf-8", errors="ignore")
        for file in path.rglob("*")
        if file.is_file()
        and "samples" not in file.relative_to(path).parts
        and file.suffix.lower() in {".md", ".json", ".txt"}
    )
    for forbidden in forbidden_fragments():
        if forbidden.lower() in active_text.lower():
            issues.append(f"forbidden runtime instruction found: {forbidden}")

    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path, help="Path to unslop-output directory.")
    args = parser.parse_args(argv)
    issues = validate(args.output)
    if issues:
        for issue in issues:
            print(f"ERROR: {issue}", file=sys.stderr)
        return 1
    print(f"OK: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
