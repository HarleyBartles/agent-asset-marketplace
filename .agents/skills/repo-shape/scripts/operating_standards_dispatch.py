#!/usr/bin/env python3
"""Validate and execute only the consumer-declared operating standards."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Callable

import operating_standards_catalog


_RUN = Callable[..., subprocess.CompletedProcess]


def _resolve_repo_path(repo_root: Path, value: str, *, label: str) -> Path:
    candidate = (repo_root / value).resolve()
    try:
        candidate.relative_to(repo_root.resolve())
    except ValueError as exc:
        raise ValueError(f"{label} escapes repository: {value}") from exc
    return candidate


def _command_vector(repo_root: Path, vector: tuple[str, ...], standard_id: str) -> list[str]:
    command = list(vector)
    if command[0] == "@python":
        command[0] = sys.executable
    elif not (Path(command[0]).is_file() if Path(command[0]).is_absolute() else shutil.which(command[0])):
        raise ValueError(f"standard {standard_id} command executable is unavailable: {command[0]}")
    for argument in command[1:]:
        if argument.endswith(".py") and not argument.startswith("-"):
            candidate = _resolve_repo_path(repo_root, argument, label=f"standard {standard_id} command path")
            if not candidate.is_file():
                raise ValueError(f"standard {standard_id} command file is missing: {argument}")
    return command


def dispatch(
    repo_root: Path,
    catalog: operating_standards_catalog.StandardsCatalog,
    contract_path: Path,
    *,
    mode: str,
    standard_id: str | None = None,
    run: _RUN = subprocess.run,
) -> list[str]:
    """Validate the complete declaration and preflight every selected command before execution."""
    if mode not in {"check", "apply"}:
        raise ValueError(f"unsupported operating standards dispatch mode: {mode}")
    try:
        composition = json.loads(contract_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"operating-standards contract cannot be read: {exc}") from exc
    operating_standards_catalog.validate_composition(composition, catalog)
    entries = composition["standards"]
    by_id = {entry["id"]: entry for entry in entries}
    if standard_id is None:
        roots = [entry["id"] for entry in entries]
    elif standard_id in by_id:
        roots = [standard_id]
    else:
        raise ValueError(f"standard is not declared in this repository: {standard_id}")

    ordered_ids: list[str] = []
    visited: set[str] = set()

    def include_with_dependencies(current_id: str) -> None:
        if current_id in visited:
            return
        for dependency in by_id[current_id]["requires"]:
            include_with_dependencies(dependency)
        visited.add(current_id)
        ordered_ids.append(current_id)

    for root_id in roots:
        include_with_dependencies(root_id)
    selected = [by_id[current_id] for current_id in ordered_ids]

    commands: list[tuple[str, list[str]]] = []
    for entry in selected:
        implementation_root = _resolve_repo_path(
            repo_root, entry["implementation_root"], label=f"standard {entry['id']} implementation root"
        )
        if not implementation_root.is_dir():
            raise ValueError(f"standard {entry['id']} implementation root is missing: {entry['implementation_root']}")
        vector = entry["check"] if mode == "check" else entry["apply"]
        if not vector:
            continue
        commands.append((entry["id"], _command_vector(repo_root, tuple(vector), entry["id"])))

    completed: list[str] = []
    for selected_id, command in commands:
        result = run(command, cwd=repo_root, check=False)
        if result.returncode:
            raise ValueError(f"standard {selected_id} {mode} command failed with exit code {result.returncode}")
        completed.append(selected_id)
    return completed


def load_catalog(script_path: Path) -> operating_standards_catalog.StandardsCatalog:
    skill_root = script_path.resolve().parent.parent
    source_root = skill_root.parent.parent
    return operating_standards_catalog.load_catalog(
        skill_root / "references/operating-standards-catalog.json",
        skill_root / "references/repository-shape-manifest.json",
        source_root,
    )
