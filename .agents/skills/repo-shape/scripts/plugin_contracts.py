#!/usr/bin/env python3
"""Validate consumer plugin prerequisites without inventorying plugin skills."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from surface_contracts import Finding


HARD_PREREQUISITES = ("agent-operating-model", "superpowers-plus", "repo-worker-pack")


@dataclass(frozen=True)
class ConsumerContract:
    surface_exceptions: tuple[str, ...]
    unslop_profile_roots: tuple[str, ...]


def load_consumer_contract(repo_root: Path) -> ConsumerContract:
    path = repo_root / ".agents/contracts/agent-operating-model.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    exceptions = data.get("surface_exceptions", [])
    roots = data.get("unslop_profile_roots", [])
    return ConsumerContract(
        surface_exceptions=tuple(item["id"] for item in exceptions if isinstance(item, dict) and "id" in item),
        unslop_profile_roots=tuple(item for item in roots if isinstance(item, str)),
    )


def load_legacy_surface_exceptions(repo_root: Path, known_surface_ids: set[str]) -> set[str]:
    """Read the explicit legacy contract used to derive a reviewable migration preview."""

    path = repo_root / ".agents/contracts/agent-operating-model.json"
    if not path.is_file():
        raise ValueError(
            "no authoritative legacy surface contract: .agents/contracts/agent-operating-model.json is missing"
        )
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"legacy operating-model contract cannot be read: {exc}") from exc
    if not isinstance(data, dict) or data.get("version") != 1:
        raise ValueError("legacy operating-model contract must be a version-1 object")
    exceptions = data.get("surface_exceptions")
    if not isinstance(exceptions, list):
        raise ValueError("legacy operating-model surface_exceptions must be a list")
    result: set[str] = set()
    for entry in exceptions:
        if not isinstance(entry, dict) or set(entry) != {"id", "reason"}:
            raise ValueError("legacy surface exceptions must contain exactly id and reason")
        surface_id, reason = entry.get("id"), entry.get("reason")
        if not isinstance(surface_id, str) or surface_id not in known_surface_ids:
            raise ValueError(f"legacy contract names unknown surface exception: {surface_id!r}")
        if not isinstance(reason, str) or not reason.strip():
            raise ValueError(f"legacy surface exception {surface_id} requires a reason")
        if surface_id in result:
            raise ValueError(f"legacy contract repeats surface exception: {surface_id}")
        result.add(surface_id)
    return result


def _installed_plugins(repo_root: Path) -> set[str]:
    path = repo_root / ".agents/plugins/marketplace.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return set()
    plugins = data.get("plugins", []) if isinstance(data, dict) else []
    return {
        item["name"]
        for item in plugins
        if isinstance(item, dict)
        and isinstance(item.get("name"), str)
        and isinstance(item.get("policy"), dict)
        and item["policy"].get("installation") == "INSTALLED_BY_DEFAULT"
    }


def check_plugin_contract(repo_root: Path, config: ConsumerContract) -> list[Finding]:
    installed = _installed_plugins(repo_root)
    findings: list[Finding] = []
    for plugin in HARD_PREREQUISITES:
        if plugin not in installed:
            findings.append(
                Finding(
                    severity="failure",
                    code="missing-prerequisite-plugin",
                    surface=plugin,
                    message=f"required plugin is not subscribed: {plugin}",
                    repair=f"subscribe to {plugin} with installation INSTALLED_BY_DEFAULT",
                )
            )
    if "writing-pack" not in installed:
        findings.append(
            Finding(
                severity="warning",
                code="missing-writing-pack",
                surface="writing-pack",
                message="expected writing-pack plugin is not subscribed",
                repair="subscribe to writing-pack when this repository should use the standard writing capabilities",
            )
        )
    has_profiles = any(
        (repo_root / root).is_dir() and any(path.is_file() for path in (repo_root / root).rglob("*"))
        for root in config.unslop_profile_roots
    )
    if has_profiles and "unslop-plus" not in installed:
        findings.append(
            Finding(
                severity="failure",
                code="missing-unslop-plus",
                surface="unslop-plus",
                message="governed unslop profiles exist but unslop-plus is not subscribed",
                repair="subscribe to unslop-plus or remove the governed unslop profiles",
            )
        )
    return findings
