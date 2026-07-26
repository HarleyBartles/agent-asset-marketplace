#!/usr/bin/env python3
"""Deterministically update the retained upstream superpowers snapshot."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

from superpowers_source import (
    ROOT,
    SUPERPOWERS_ADAPTER_OPENAI_PATH,
    SUPERPOWERS_ADAPTER_OVERLAY_PATH,
    SUPERPOWERS_BUNDLE_MANIFEST_PATH,
    SUPERPOWERS_CUSTODY_REGISTRY_PATH,
    SUPERPOWERS_FAMILY_ROOT,
    SUPERPOWERS_PROVENANCE_PATH,
    SUPERPOWERS_SOURCE_MD_PATH,
    load_superpowers_bundle_manifest,
    superpowers_source_commit,
    superpowers_source_root,
    superpowers_source_tag,
)


UPSTREAM_REPO = "https://github.com/obra/superpowers"
def _run(*args: str, cwd: Path | None = None) -> None:
    subprocess.run([*args], cwd=cwd or ROOT, check=True)


def _git_ls_remote(tag: str) -> tuple[str, str]:
    result = subprocess.run(
        ["git", "ls-remote", "--tags", UPSTREAM_REPO, f"refs/tags/{tag}", f"refs/tags/{tag}^{{}}"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    tag_object = ""
    commit = ""
    for line in result.stdout.splitlines():
        if not line.strip():
            continue
        sha, ref = line.split("\t", 1)
        if ref.endswith("^{}"):
            commit = sha
        elif ref.endswith(tag):
            tag_object = sha
    if not commit:
        raise ValueError(f"could not resolve commit for {tag}")
    if not tag_object:
        tag_object = commit
    return tag_object, commit


def _clone_release(tag: str, destination: Path) -> Path:
    if destination.exists():
        shutil.rmtree(destination)
    subprocess.run(
        ["git", "clone", "--depth", "1", "--branch", tag, UPSTREAM_REPO, str(destination)],
        cwd=ROOT,
        check=True,
    )
    return destination


def _replace_text(path: Path, replacements: list[tuple[str, str]]) -> None:
    content = path.read_text(encoding="utf-8")
    original = content
    for old, new in replacements:
        content = content.replace(old, new)
    if content != original:
        path.write_text(content, encoding="utf-8", newline="\n")


def _copy_source_snapshot(source_checkout: Path, target_root: Path) -> None:
    if target_root.exists():
        shutil.rmtree(target_root)
    shutil.copytree(
        source_checkout,
        target_root,
        ignore=shutil.ignore_patterns(".git"),
    )


def _remove_old_source_versions(keep_version: str) -> None:
    if not SUPERPOWERS_FAMILY_ROOT.exists():
        return
    for child in SUPERPOWERS_FAMILY_ROOT.iterdir():
        if child.is_dir() and child.name.startswith("v") and child.name != keep_version:
            shutil.rmtree(child)


def _update_custody_registry(
    *,
    old_root: str,
    old_version: str,
    new_root: str,
    new_version: str,
) -> None:
    registry = json.loads(SUPERPOWERS_CUSTODY_REGISTRY_PATH.read_text(encoding="utf-8"))
    changed = False
    for pack in registry.get("packs", []):
        if not isinstance(pack, dict):
            continue
        if pack.get("bundle_name") != "superpowers-plus":
            continue

        source_ledger = pack.get("source_ledger", [])
        for i, ledger_path in enumerate(source_ledger):
            if not isinstance(ledger_path, str):
                continue
            updated = ledger_path.replace(old_root, new_root).replace(old_version, new_version)
            if updated != ledger_path:
                source_ledger[i] = updated
                changed = True

        for entry in pack.get("entries", []):
            if not isinstance(entry, dict):
                continue
            if entry.get("source_family") != "superpowers":
                continue
            for field in (
                "canonical_source_path",
                "source_path",
                "provenance_note",
                "adaptation_note",
            ):
                value = entry.get(field)
                if isinstance(value, str):
                    updated = value.replace(old_root, new_root).replace(old_version, new_version)
                    if updated != value:
                        entry[field] = updated
                        changed = True
            if entry.get("source_repo") != UPSTREAM_REPO:
                entry["source_repo"] = UPSTREAM_REPO
                changed = True

        break  # superpowers-plus is unique

    if changed:
        SUPERPOWERS_CUSTODY_REGISTRY_PATH.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8", newline="\n")


def _update_bundle_manifest(new_version: str, new_commit: str) -> None:
    bundle_manifest = load_superpowers_bundle_manifest()
    old_root = superpowers_source_root(bundle_manifest).relative_to(ROOT).as_posix()
    new_root = f"sources/third_party/superpowers/obra-superpowers/{new_version}"
    old_version = superpowers_source_tag(bundle_manifest)

    for entry in bundle_manifest.get("entries", []):
        if not isinstance(entry, dict):
            continue
        if entry.get("source_category") != "third_party":
            continue
        for field in ("canonical_source_path", "source_path", "provenance_note", "adaptation_note"):
            value = entry.get(field)
            if isinstance(value, str):
                updated = value.replace(old_root, new_root).replace(old_version, new_version)
                entry[field] = updated
        entry["source_repo"] = UPSTREAM_REPO

    SUPERPOWERS_BUNDLE_MANIFEST_PATH.write_text(
        json.dumps(bundle_manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def _tag_object_from_provenance() -> str:
    if not SUPERPOWERS_PROVENANCE_PATH.exists():
        return ""
    match = re.search(r"Tag object:\s*`([0-9a-f]{40})`", SUPERPOWERS_PROVENANCE_PATH.read_text(encoding="utf-8"))
    return match.group(1) if match else ""


def _update_provenance_and_source_md(
    *,
    old_root: str,
    old_version: str,
    old_commit: str,
    old_tag_object: str,
    new_version: str,
    new_commit: str,
    new_tag_object: str,
) -> None:
    _replace_text(
        SUPERPOWERS_SOURCE_MD_PATH,
        [
            (old_root, f"sources/third_party/superpowers/obra-superpowers/{new_version}"),
            (old_version, new_version),
        ],
    )
    provenance_replacements = [
        (old_version, new_version),
        (old_commit, new_commit),
        (old_root, f"sources/third_party/superpowers/obra-superpowers/{new_version}"),
    ]
    if old_tag_object and new_tag_object:
        provenance_replacements.insert(0, (old_tag_object, new_tag_object))
    _replace_text(SUPERPOWERS_PROVENANCE_PATH, provenance_replacements)


def _adapter_staleness() -> list[str]:
    issues: list[str] = []
    bundle_manifest = load_superpowers_bundle_manifest()
    target_version = superpowers_source_tag(bundle_manifest)
    target_root = superpowers_source_root(bundle_manifest).relative_to(ROOT).as_posix()

    overlay_text = SUPERPOWERS_ADAPTER_OVERLAY_PATH.read_text(encoding="utf-8")
    openai_doc = yaml.safe_load(SUPERPOWERS_ADAPTER_OPENAI_PATH.read_text(encoding="utf-8"))
    if f"upstream_version: {target_version}" not in overlay_text:
        issues.append(f"{SUPERPOWERS_ADAPTER_OVERLAY_PATH.relative_to(ROOT)} still points at an older upstream version")
    if target_root not in overlay_text:
        issues.append(f"{SUPERPOWERS_ADAPTER_OVERLAY_PATH.relative_to(ROOT)} still references an older source root")
    if not re.search(rf"source_repo:\s*['\"]?{re.escape(UPSTREAM_REPO)}['\"]?", overlay_text):
        issues.append(f"{SUPERPOWERS_ADAPTER_OVERLAY_PATH.relative_to(ROOT)} still points at an older upstream repository")
    if not isinstance(openai_doc, dict) or openai_doc.get("metadata", {}).get("upstream_version") != target_version:
        issues.append(f"{SUPERPOWERS_ADAPTER_OPENAI_PATH.relative_to(ROOT)} still points at an older upstream version")
    return issues


def _print_adapter_guidance() -> None:
    print("Adapter guidance:")
    print(f"- If {SUPERPOWERS_ADAPTER_OVERLAY_PATH.relative_to(ROOT)} exists, update it before regen when the upstream version changes.")
    print(f"- If {SUPERPOWERS_ADAPTER_OPENAI_PATH.relative_to(ROOT)} exists, keep its upstream_version in lockstep with the overlay.")


def _prepare(tag: str) -> None:
    bundle_manifest = load_superpowers_bundle_manifest()
    old_root = superpowers_source_root(bundle_manifest).relative_to(ROOT).as_posix()
    old_version = superpowers_source_tag(bundle_manifest)
    old_commit = superpowers_source_commit(bundle_manifest)

    tag_object, commit = _git_ls_remote(tag)
    print(f"Resolved {tag}: tag object {tag_object}, commit {commit}")
    old_tag_object = _tag_object_from_provenance()

    target_root = SUPERPOWERS_FAMILY_ROOT / tag
    checkout_root = Path(tempfile.mkdtemp(prefix="superpowers-upstream-"))
    try:
        _clone_release(tag, checkout_root)
        _remove_old_source_versions(tag)
        _copy_source_snapshot(checkout_root, target_root)
    finally:
        shutil.rmtree(checkout_root, ignore_errors=True)

    _update_custody_registry(
        old_root=old_root,
        old_version=old_version,
        new_root=target_root.relative_to(ROOT).as_posix(),
        new_version=tag,
    )
    _update_bundle_manifest(tag, commit)
    _update_provenance_and_source_md(
        old_root=old_root,
        old_version=old_version,
        old_commit=old_commit,
        old_tag_object=old_tag_object,
        new_version=tag,
        new_commit=commit,
        new_tag_object=tag_object,
    )
    _print_adapter_guidance()

    issues = _adapter_staleness()
    if issues:
        print("Adapter drift detected before regeneration:")
        for issue in issues:
            print(f"- {issue}")
        print("Update the adapter manually, then rerun this script with --regen.")
    else:
        print("Adapter surfaces are already aligned with the new upstream version.")


def _regen() -> None:
    issues = _adapter_staleness()
    if issues:
        print("Adapter drift detected; regenerate is blocked until the adapter is updated:")
        for issue in issues:
            print(f"- {issue}")
        raise SystemExit(2)
    _run(sys.executable, str(ROOT / "tools" / "rebuild_marketplace.py"))


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Update the retained upstream superpowers snapshot")
    parser.add_argument("--tag", required=True, help="upstream release tag to retain, for example v6.1.0")
    parser.add_argument("--prepare", action="store_true", help="refresh source custody and supporting source docs")
    parser.add_argument("--regen", action="store_true", help="run the canonical marketplace rebuild after the adapter is updated")
    args = parser.parse_args()
    if not args.prepare and not args.regen:
        parser.error("choose at least one of --prepare or --regen")
    return args


def main() -> int:
    args = _parse_args()
    if args.prepare:
        _prepare(args.tag)
    if args.regen:
        _regen()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
