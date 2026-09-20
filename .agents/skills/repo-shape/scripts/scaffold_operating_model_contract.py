#!/usr/bin/env python3
"""Create or validate the consumer-owned operating-model contract."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
from pathlib import Path

import surface_contracts


def _repo_root() -> Path:
    env = os.environ.copy()
    for name in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE"):
        env.pop(name, None)
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True, env=env
    )
    return Path(result.stdout.strip())


def _validate(data: object) -> list[str]:
    if not isinstance(data, dict):
        return ["contract must be a JSON object"]
    findings: list[str] = []
    if set(data) != {"version", "surface_exceptions", "unslop_profile_roots"}:
        findings.append("contract must contain only version, surface_exceptions, and unslop_profile_roots")
    if data.get("version") != 1:
        findings.append("contract version must be 1")
    manifest = surface_contracts.load_manifest(
        Path(__file__).resolve().parent.parent / "references" / "repository-shape-manifest.json"
    )
    known_ids = {surface.id for surface in manifest.surfaces}
    exceptions = data.get("surface_exceptions")
    if not isinstance(exceptions, list):
        findings.append("surface_exceptions must be a list")
    else:
        seen: set[str] = set()
        for entry in exceptions:
            if not isinstance(entry, dict) or set(entry) != {"id", "reason"}:
                findings.append("each surface exception must contain exactly id and reason")
                continue
            surface_id, reason = entry.get("id"), entry.get("reason")
            if not isinstance(surface_id, str) or surface_id not in known_ids:
                findings.append(f"unknown surface exception: {surface_id!r}")
            elif surface_id in seen:
                findings.append(f"duplicate surface exception: {surface_id}")
            else:
                seen.add(surface_id)
            if not isinstance(reason, str) or not reason.strip():
                findings.append(f"surface exception {surface_id!r} requires a reason")
    roots = data.get("unslop_profile_roots")
    if not isinstance(roots, list) or not roots or not all(isinstance(item, str) and item for item in roots):
        findings.append("unslop_profile_roots must be a non-empty list of paths")
    elif any(Path(item).is_absolute() or ".." in Path(item).parts for item in roots):
        findings.append("unslop_profile_roots must contain repository-relative paths")
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Scaffold or validate .agents/contracts/agent-operating-model.json. (mixed)"
    )
    parser.add_argument("--check", action="store_true", help="Report drift without writing")
    args = parser.parse_args(argv)
    root = _repo_root()
    target = root / ".agents" / "contracts" / "agent-operating-model.json"
    template = Path(__file__).resolve().parent.parent / "templates" / "agent-operating-model.json"
    if not target.is_file():
        if args.check:
            print("DRIFT: .agents/contracts/agent-operating-model.json missing")
            return 1
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(template.read_bytes())
        print("wrote .agents/contracts/agent-operating-model.json")
        return 0
    try:
        data = json.loads(target.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        findings = [f"contract cannot be read: {exc}"]
    else:
        findings = _validate(data)
    if findings:
        for finding in findings:
            print(f"DRIFT: {finding}")
        return 1
    print("OK .agents/contracts/agent-operating-model.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
