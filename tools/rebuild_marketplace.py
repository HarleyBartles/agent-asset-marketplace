#!/usr/bin/env python3
"""Canonical full marketplace rebuild and validation entrypoint."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

import shared_checkout
from superpowers_source import load_superpowers_bundle_manifest, superpowers_source_root

ROOT = Path(__file__).resolve().parent.parent
PLUGIN_ROOTS_PATH = ROOT / "codex-marketplace/plugins"
PLUGIN_ROOT_INVENTORY_PATH = ROOT / "codex-marketplace/plugin-roots.json"

_SCRIPT_NAME = "rebuild-marketplace"


def _run_tool(script_name: str, *args: str, verbose: bool = False) -> None:
    script_path = Path(__file__).resolve().with_name(script_name)
    cmd = [sys.executable, str(script_path), *args]
    if verbose:
        print("+ " + " ".join(cmd))
    subprocess.run(cmd, check=True)


def _run_skill_script(skill_name: str, core_name: str, *args: str, verbose: bool = False) -> None:
    script_path = ROOT / "sources" / "first_party" / "skills" / skill_name / "scripts" / core_name
    if not script_path.is_file():
        script_path = ROOT / ".agents" / "skills" / skill_name / "scripts" / core_name
    if not script_path.is_file():
        raise FileNotFoundError(f"Skill script not found: {script_path}")
    cmd = [sys.executable, str(script_path), *args]
    if verbose:
        print("+ " + " ".join(cmd))
    subprocess.run(cmd, cwd=ROOT, check=True)


def _run_git(*args: str, verbose: bool = False) -> None:
    cmd = ["git", *args]
    if verbose:
        print("+ " + " ".join(cmd))
    subprocess.run(cmd, cwd=ROOT, check=True)


def _git_output(*args: str) -> str:
    completed = subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True, text=True)
    return completed.stdout


def _load_active_plugin_root_names() -> set[str]:
    inventory = json.loads(PLUGIN_ROOT_INVENTORY_PATH.read_text(encoding="utf-8"))
    roots = inventory.get("roots")
    if not isinstance(roots, list):
        raise ValueError(f"{PLUGIN_ROOT_INVENTORY_PATH}: roots must be a list")
    active_names: set[str] = set()
    for entry in roots:
        if not isinstance(entry, dict):
            raise ValueError(f"{PLUGIN_ROOT_INVENTORY_PATH}: roots must contain objects")
        if entry.get("enabled") is False:
            continue
        name = entry.get("name")
        if not isinstance(name, str) or not name.strip():
            raise ValueError(f"{PLUGIN_ROOT_INVENTORY_PATH}: enabled roots require a non-empty name")
        active_names.add(name)
    return active_names


def _prune_stale_projected_plugin_roots() -> None:
    active_names = _load_active_plugin_root_names()
    for child in sorted(PLUGIN_ROOTS_PATH.iterdir(), key=lambda path: path.name):
        if not child.is_dir() or child.name in active_names:
            continue
        if not (child / ".codex-plugin" / "plugin.json").is_file():
            continue
        shutil.rmtree(child)
        print(f"Pruned stale projected plugin root {child.relative_to(ROOT)}")


def _retained_verbatim_paths() -> set[str]:
    bundle_manifest = load_superpowers_bundle_manifest()
    source_root = superpowers_source_root(bundle_manifest).relative_to(ROOT).as_posix()
    skip_paths: set[str] = set()
    for entry in bundle_manifest.get("entries", []):
        if not isinstance(entry, dict):
            continue
        if entry.get("source_category") != "third_party" or entry.get("content_mode") != "verbatim":
            continue
        canonical_source_path = entry.get("canonical_source_path")
        if isinstance(canonical_source_path, str) and canonical_source_path.strip():
            skip_paths.add(canonical_source_path)
            skip_paths.add(f"{canonical_source_path}/SKILL.md")
        source_path = entry.get("source_path")
        if isinstance(source_path, str) and source_path.strip():
            skip_paths.add(source_path)
        local_path = entry.get("local_path")
        if isinstance(local_path, str) and local_path.strip():
            skip_paths.add(f"codex-marketplace/plugins/superpowers-plus/{local_path}")
            skip_paths.add(f"codex-marketplace/plugins/superpowers-plus/{local_path}/SKILL.md")
            # The .agents/skills/ install mirror copies the same verbatim bytes,
            # so pre-existing upstream trailing whitespace surfaces there too.
            skill_name = local_path.split("/")[-1]
            skip_paths.add(f".agents/skills/{skill_name}")
            skip_paths.add(f".agents/skills/{skill_name}/SKILL.md")
    skip_paths.add(source_root)
    skip_paths.add(f"{source_root}/AGENTS.md")
    return skip_paths


def _check_arg(check: bool) -> tuple[str, ...]:
    return ("--check",) if check else ()


def _run_inventory(*, check: bool, verbose: bool) -> None:
    _run_tool("generate_plugin_root_inventory.py", *_check_arg(check), verbose=verbose)
    if not check:
        _prune_stale_projected_plugin_roots()
    _run_tool("validate_marketplace.py", "--phase", "inventory", "--skip-freshness-checks", verbose=verbose)


def _run_heal(*, check: bool, verbose: bool) -> None:
    _run_tool("heal_overlays.py", *_check_arg(check), verbose=verbose)


def _run_project(*, check: bool, verbose: bool, skip_install: bool, allow_shared_checkout: bool) -> None:
    if check:
        _run_tool("update_skill_artifacts.py", "--check", verbose=verbose)
    else:
        _run_tool("update_skill_artifacts.py", "--all", verbose=verbose)
    _run_tool("normalize_first_party_skill_sources.py", *_check_arg(check), verbose=verbose)
    if not skip_install:
        refresh_args = [*_check_arg(check)]
        if not check:
            refresh_args.append("--apply")
            if allow_shared_checkout:
                refresh_args.append("--allow-shared-checkout")
        _run_skill_script("refreshing-installed-skills", "refresh_installed_skills.py", *refresh_args, verbose=verbose)
    _run_tool("validate_marketplace.py", "--phase", "project", "--skip-freshness-checks", verbose=verbose)


def _run_index(*, check: bool, verbose: bool, skip_index: bool, allow_shared_checkout: bool) -> None:
    if skip_index:
        return
    _run_tool("generate_repo_index.py", *_check_arg(check), verbose=verbose)
    mesh_args = ["--check"] if check else ["--apply"]
    if not check and allow_shared_checkout:
        mesh_args.append("--allow-shared-checkout")
    _run_skill_script("generating-agent-mesh", "generate_index_mesh.py", *mesh_args, verbose=verbose)
    if not check:
        _run_skill_script("generating-agent-mesh", "generate_index_mesh.py", "--check", verbose=verbose)
    _run_tool("validate_marketplace.py", "--phase", "index", "--skip-freshness-checks", verbose=verbose)


def _run_catalog(*, check: bool, verbose: bool) -> None:
    if check:
        _run_tool("generate_first_party_skill_catalog.py", "--check", verbose=verbose)
    else:
        _run_tool("generate_first_party_skill_catalog.py", verbose=verbose)
        _run_tool("generate_first_party_skill_catalog.py", "--check", verbose=verbose)


def _run_whitespace_check(*, verbose: bool, skip: bool) -> None:
    if skip:
        return
    changed_paths = [
        path
        for path in _git_output("diff", "--name-only", "HEAD").splitlines()
        if path and path not in _retained_verbatim_paths()
    ]
    if not changed_paths:
        return
    _MAX_CMD_CHARS = 28000
    batch: list[str] = []
    batch_len = 0
    for path in changed_paths:
        path_len = len(path) + 4  # path + space + 2 quotes + separator
        if batch and batch_len + path_len > _MAX_CMD_CHARS:
            _run_git("diff", "--check", "HEAD", "--", *batch, verbose=verbose)
            batch = []
            batch_len = 0
        batch.append(path)
        batch_len += path_len
    if batch:
        _run_git("diff", "--check", "HEAD", "--", *batch, verbose=verbose)


def _run_validate(
    *,
    check: bool,
    verbose: bool,
    skip_validate: bool,
    skip_whitespace_check: bool,
) -> None:
    if not skip_validate:
        _run_tool("validate_authority_assets.py", verbose=verbose)
    _run_whitespace_check(verbose=verbose, skip=skip_whitespace_check)
    if check:
        _run_git("diff", "--exit-code", verbose=verbose)


_PHASE_ORDER = ("inventory", "heal", "project", "index", "catalog", "validate")


def _parse_args() -> argparse.Namespace:
    epilog = (
        "This is the canonical 'refresh marketplace' command. It regenerates all derived\n"
        "marketplace surfaces and then validates them.\n\n"
        "Use --phase to run only one logical phase. Each phase is self-checking; earlier\n"
        "phases are not automatically regenerated unless you run --phase all (the default).\n\n"
        "Editable inputs (do not hand-edit derived outputs):\n"
        "  - codex-marketplace/custody-pack-registry.json\n"
        "  - sources/first_party/skills/<skill>/\n"
        "  - sources/third_party/<upstream>/\n"
        "  - adapters/codex/<pack>/<skill>/\n\n"
        "Key outputs:\n"
        "  - .agents/plugins/marketplace.json, codex-marketplace/manifest.json\n"
        "  - codex-marketplace/plugins/<pack>/skills/<skill>/\n"
        "  - codex-marketplace/plugins/<pack>/references/{bundle-manifest,source-map,provenance-map}.*\n"
        "  - generated/skill-zips/<skill>.zip\n"
        "  - provenance/first-party-skills.md\n"
        "  - repo-index/repo-index.json and repo-wide INDEX.md mesh\n"
        "  - .agents/skills/<skill>/ (installed skills)\n\n"
        "For the full step-by-step flow see .agents/guides/marketplace-generation-guide.md."
    )
    parser = argparse.ArgumentParser(
        description="Run the full marketplace rebuild and validation stack",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=epilog,
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Non-mutating check mode. Forwards --check to every writer script that supports it.",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Apply mode: regenerate derived surfaces (required for mutation)",
    )
    parser.add_argument(
        "--allow-shared-checkout",
        action="store_true",
        help="Approve applying changes in a shared or git-worktree checkout. "
             "Only pass this if you intend to mutate this checkout; it is forwarded to any child scripts.",
    )
    parser.add_argument(
        "--phase",
        choices=("inventory", "heal", "project", "index", "catalog", "validate", "all"),
        default="all",
        help="Run only the named phase. Default: all",
    )
    parser.add_argument(
        "--skip-install",
        action="store_true",
        help="Skip installing skills into .agents/skills/",
    )
    parser.add_argument(
        "--skip-index",
        action="store_true",
        help="Skip repo-index and index-mesh generation",
    )
    parser.add_argument(
        "--skip-validate",
        action="store_true",
        help="Skip validator scripts in the final validate phase",
    )
    parser.add_argument(
        "--skip-whitespace-check",
        action="store_true",
        help="Skip git diff --check (whitespace lint). Does not skip --exit-code in --check mode.",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Print each command before running it",
    )
    return parser.parse_args()


def main() -> int:
    args = _parse_args()

    if not args.check and not args.apply:
        args.check = True

    if args.apply and args.check:
        print("error: --apply and --check are mutually exclusive", file=sys.stderr)
        return 1

    if args.allow_shared_checkout and not args.apply:
        print("error: --allow-shared-checkout requires --apply", file=sys.stderr)
        return 1

    if args.apply and not shared_checkout.approve_mutation(ROOT, _SCRIPT_NAME, args.allow_shared_checkout):
        return 1

    # If mutation was approved interactively in a shared checkout, propagate that
    # approval to child scripts so they do not re-prompt.
    if args.apply and shared_checkout.is_shared_checkout(ROOT):
        args.allow_shared_checkout = True

    phase_runners = {
        "inventory": lambda: _run_inventory(check=args.check, verbose=args.verbose),
        "heal": lambda: _run_heal(check=args.check, verbose=args.verbose),
        "project": lambda: _run_project(
            check=args.check,
            verbose=args.verbose,
            skip_install=args.skip_install,
            allow_shared_checkout=args.allow_shared_checkout,
        ),
        "index": lambda: _run_index(
            check=args.check,
            verbose=args.verbose,
            skip_index=args.skip_index,
            allow_shared_checkout=args.allow_shared_checkout,
        ),
        "catalog": lambda: _run_catalog(check=args.check, verbose=args.verbose),
        "validate": lambda: _run_validate(
            check=args.check,
            verbose=args.verbose,
            skip_validate=args.skip_validate,
            skip_whitespace_check=args.skip_whitespace_check,
        ),
    }

    phases = _PHASE_ORDER if args.phase == "all" else (args.phase,)
    for phase in phases:
        phase_runners[phase]()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
