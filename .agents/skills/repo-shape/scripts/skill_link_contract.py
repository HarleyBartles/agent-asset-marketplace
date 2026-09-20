#!/usr/bin/env python3
"""Resolve workflow skill links against the consumer-visible namespace."""

from __future__ import annotations

import json
import re
from pathlib import Path

from surface_contracts import Finding


def _visible_skills(root: Path) -> set[str]:
    skills = root / ".agents/skills"
    visible: set[str] = set()
    for path in skills.iterdir() if skills.is_dir() else ():
        if not path.is_dir() or not (path / "SKILL.md").is_file():
            continue
        visible.add(path.name)
        match = re.search(r"(?im)^name:\s*['\"]?([^'\"\n]+)", (path / "SKILL.md").read_text(encoding="utf-8"))
        if match:
            visible.add(match.group(1).strip())
    try:
        data = json.loads((root / ".agents/plugins/marketplace.json").read_text(encoding="utf-8"))
        for name in data.get("repo", {}).get("local_skills", []):
            if isinstance(name, str):
                visible.add(name)
    except (OSError, json.JSONDecodeError, AttributeError):
        pass
    return visible


def check_skill_links(repo_root: Path) -> list[Finding]:
    visible = _visible_skills(repo_root)
    findings: list[Finding] = []
    for directory, heading, composition in (
        ("runbooks", "Required skills", "Composition"),
        ("playbooks", "Required skills", "Composition"),
    ):
        for path in (
            sorted((repo_root / ".agents" / directory).glob("*.md"))
            if (repo_root / ".agents" / directory).is_dir()
            else ()
        ):
            text = path.read_text(encoding="utf-8")
            sections = re.split(r"(?m)^##\s+", text)
            required = next((part for part in sections if part.startswith(heading)), "")
            comp = next((part for part in sections if part.startswith(composition)), "")
            required_names = set(re.findall(r"`([A-Za-z0-9][A-Za-z0-9_.+-]*)`", required))
            comp_names = set(re.findall(r"`([A-Za-z0-9][A-Za-z0-9_.+-]*)`", comp))
            comp_names -= {"main", "HEAD", "completed-awaiting-retirement", "Composition"}
            for skill in sorted(required_names | comp_names):
                if skill in {"runbooks", "playbooks", "Composition"} or "/" in skill:
                    continue
                if skill not in visible:
                    findings.append(
                        Finding(
                            "failure",
                            "dead-skill-link",
                            path.relative_to(repo_root).as_posix(),
                            f"workflow references missing skill: {skill}",
                            "install a provider plugin or declare a repo-local skill",
                        )
                    )
                elif skill in comp_names and skill not in required_names:
                    findings.append(
                        Finding(
                            "failure",
                            "unlisted-composition-skill",
                            path.relative_to(repo_root).as_posix(),
                            f"Composition invokes skill not listed in Required skills: {skill}",
                            "add the exact skill to Required skills",
                        )
                    )
    return findings
