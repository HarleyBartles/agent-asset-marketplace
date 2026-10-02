#!/usr/bin/env python3
"""Editable Codex/Devin declaration checker starter. Requires Python 3.11 or newer."""

from __future__ import annotations

import argparse
import json
import re
import sys
import tomllib
from pathlib import Path, PurePosixPath, PureWindowsPath
from urllib.parse import urlsplit


CATALOG_PATH = Path(".agents/plugins/marketplace.json")
CODEX_CONFIG_PATH = Path(".codex/config.toml")
DEVIN_CONFIG_PATH = Path(".devin/config.json")
IDENTIFIER = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
FULL_SHA = re.compile(r"^(?:[0-9a-fA-F]{40}|[0-9a-fA-F]{64})$")


def _git_url(value: object) -> bool:
    if not isinstance(value, str) or not value.strip() or any(char.isspace() for char in value):
        return False
    if re.fullmatch(r"[^@/\s]+@[^:/\s]+:.+", value):
        return True
    parsed = urlsplit(value)
    return parsed.scheme in {"https", "ssh", "git"} and bool(parsed.hostname and parsed.path)


def _relative_plugin_path(value: object, *, codex: bool) -> bool:
    if not isinstance(value, str) or not value.strip():
        return False
    path = value[2:] if codex and value.startswith("./") else value
    if codex and not value.startswith("./"):
        return False
    posix = PurePosixPath(path)
    windows = PureWindowsPath(path)
    return bool(
        posix.parts
        and not posix.is_absolute()
        and not windows.is_absolute()
        and not windows.drive
        and ".." not in posix.parts
        and ".." not in windows.parts
    )


def _selector_error(source: dict[str, object], label: str) -> str | None:
    present = [key for key in ("ref", "sha") if key in source]
    if len(present) != 1:
        return f"{label}: source must specify exactly one of ref or sha"
    key = present[0]
    value = source[key]
    if not isinstance(value, str) or not value.strip():
        return f"{label}: {key} must be a non-empty string"
    if key == "sha" and not FULL_SHA.fullmatch(value):
        return f"{label}: sha must be a full 40- or 64-character hexadecimal commit"
    return None


def _codex_catalog(path: Path, errors: list[str]) -> tuple[str | None, set[str]]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(value, dict):
            raise ValueError("catalog root must be an object")
        name = value.get("name")
        plugins = value.get("plugins")
        if not isinstance(name, str) or not IDENTIFIER.fullmatch(name):
            raise ValueError("catalog name must be a valid identifier")
        if not isinstance(plugins, list):
            raise ValueError("plugins must be an array")
        names: set[str] = set()
        for index, plugin in enumerate(plugins):
            label = f"{CATALOG_PATH.as_posix()}: plugins[{index}]"
            if not isinstance(plugin, dict):
                errors.append(f"{label} must be an object")
                continue
            plugin_name = plugin.get("name")
            source = plugin.get("source")
            if not isinstance(plugin_name, str) or not IDENTIFIER.fullmatch(plugin_name):
                errors.append(f"{label}.name must be a valid identifier")
            elif plugin_name in names:
                errors.append(f"{label}.name duplicates plugin {plugin_name!r}")
            else:
                names.add(plugin_name)
            if not isinstance(source, dict):
                errors.append(f"{label}.source must be an object")
                continue
            kind = source.get("source")
            if kind not in ("url", "git-subdir"):
                errors.append(f"{label}.source.source must be 'url' or 'git-subdir'")
            if not _git_url(source.get("url")):
                errors.append(f"{label}.source.url must be a Git URL")
            if kind == "git-subdir" and not _relative_plugin_path(source.get("path"), codex=True):
                errors.append(f"{label}.source.path must be a contained './' repository-relative plugin path")
            if kind == "url" and "path" in source:
                errors.append(f"{label}.source.path is only valid with 'git-subdir'")
            if error := _selector_error(source, label):
                errors.append(error)
        return name, names
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        errors.append(f"{CATALOG_PATH.as_posix()}: invalid catalog JSON/declaration: {exc}")
        return None, set()


def _check_codex(root: Path, errors: list[str], surfaces: list[str]) -> None:
    catalog_path = root / CATALOG_PATH
    config_path = root / CODEX_CONFIG_PATH
    if not catalog_path.is_file():
        surfaces.append("Codex: no repository Git plugin catalog present")
        return
    catalog_name, plugin_names = _codex_catalog(catalog_path, errors)
    if not config_path.is_file():
        errors.append(f"missing Codex project binding: {CODEX_CONFIG_PATH.as_posix()}")
        surfaces.append("Codex: catalog present, project binding missing")
        return
    try:
        config = tomllib.loads(config_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, tomllib.TOMLDecodeError) as exc:
        errors.append(f"{CODEX_CONFIG_PATH.as_posix()}: invalid TOML: {exc}")
        surfaces.append("Codex: configuration unreadable")
        return

    marketplaces = config.get("marketplaces", {})
    activations = config.get("plugins", {})
    if not isinstance(marketplaces, dict) or not isinstance(activations, dict):
        errors.append(f"{CODEX_CONFIG_PATH.as_posix()}: marketplaces and plugins must be TOML tables")
        surfaces.append("Codex: configuration parsed, binding tables invalid")
        return
    registration = marketplaces.get(catalog_name) if catalog_name else None
    if not isinstance(registration, dict) or registration.get("source_type") != "git":
        errors.append("Codex marketplace registration must match the catalog name and use source_type = 'git'")
    elif not _git_url(registration.get("source")):
        errors.append("Codex marketplace registration source must be a Git URL")
    elif "ref" in registration and (not isinstance(registration["ref"], str) or not registration["ref"].strip()):
        errors.append("Codex marketplace registration ref must be a non-empty string when provided")

    for key, config_value in activations.items():
        if not isinstance(key, str) or "@" not in key:
            continue
        plugin_name, marketplace_name = key.rsplit("@", 1)
        if marketplace_name != catalog_name:
            continue
        if plugin_name not in plugin_names:
            errors.append(f"{CODEX_CONFIG_PATH.as_posix()}: activation {key!r} has no matching catalog entry")
        elif not isinstance(config_value, dict) or not isinstance(config_value.get("enabled"), bool):
            errors.append(f"{CODEX_CONFIG_PATH.as_posix()}: activation {key!r} must set enabled to a boolean")
    surfaces.append("Codex: checked repository Git catalog, project registration, and local plugin activations")


def _devin_dependency(value: object, label: str, errors: list[str]) -> None:
    if not isinstance(value, dict):
        errors.append(f"{label} must be an object so it can record a ref or sha selector")
        return
    kind = value.get("source")
    if kind == "git-subdir":
        if not _git_url(value.get("url")):
            errors.append(f"{label}.url must be a Git URL")
        if not _relative_plugin_path(value.get("path"), codex=False):
            errors.append(f"{label}.path must be a contained repository-relative plugin path")
    elif kind == "url":
        if not _git_url(value.get("url")):
            errors.append(f"{label}.url must be a Git URL")
        if "path" in value:
            errors.append(f"{label}.path is only valid with source = 'git-subdir'")
    elif kind == "github":
        repo = value.get("repo")
        if not isinstance(repo, str) or not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repo):
            errors.append(f"{label}.repo must be owner/repository")
        if "path" in value:
            errors.append(f"{label}.path is only valid with source = 'git-subdir'")
    else:
        errors.append(f"{label}.source must be 'github', 'url', or 'git-subdir'")
    if error := _selector_error(value, label):
        errors.append(error)


def _check_devin(root: Path, errors: list[str], surfaces: list[str]) -> None:
    path = root / DEVIN_CONFIG_PATH
    if not path.exists():
        surfaces.append("Devin: not present")
        return
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(value, dict):
            raise ValueError("configuration root must be an object")
        for key in ("requiredPlugins", "optionalPlugins"):
            entries = value.get(key, [])
            if not isinstance(entries, list):
                errors.append(f"{DEVIN_CONFIG_PATH.as_posix()}: {key} must be an array")
                continue
            for index, entry in enumerate(entries):
                _devin_dependency(entry, f"{DEVIN_CONFIG_PATH.as_posix()}: {key}[{index}]", errors)
        forbidden = value.get("forbiddenPlugins", [])
        if not isinstance(forbidden, list) or any(not isinstance(item, str) for item in forbidden):
            errors.append(
                f"{DEVIN_CONFIG_PATH.as_posix()}: forbiddenPlugins must be an array of plugin identity strings"
            )
        surfaces.append("Devin: checked native repo plugin dependency declarations")
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        errors.append(f"{DEVIN_CONFIG_PATH.as_posix()}: invalid JSON/declaration: {exc}")
        surfaces.append("Devin: configuration unreadable")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Read-only Codex and Devin Git plugin declaration checks. Requires Python 3.11+ "
            "for standard-library TOML parsing; does not fetch or install plugins."
        )
    )
    parser.add_argument(
        "--repo-root", type=Path, default=Path("."), help="repository root (default: current directory)"
    )
    parser.add_argument("--check", action="store_true", help="check declarations without writing or fetching")
    args = parser.parse_args(argv)
    root = args.repo_root.resolve()
    if not root.is_dir():
        parser.error(f"repository root is not a directory: {root}")

    errors: list[str] = []
    surfaces: list[str] = []
    _check_codex(root, errors, surfaces)
    _check_devin(root, errors, surfaces)
    for surface in surfaces:
        print(surface)
    for error in errors:
        print(f"ERROR: {error}")
    print(
        "The checker does not fetch remote repositories. It cannot prove remote paths, access, "
        "authentication, trust, installation, or runtime loading."
    )
    if errors:
        return 1
    print("OK: local declarations are syntactically consistent")
    return 0


if __name__ == "__main__":
    sys.exit(main())
