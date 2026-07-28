#!/usr/bin/env python3
"""Dependency-aware task runner for the agent-asset-marketplace tooling."""

from __future__ import annotations

import argparse
import json
import shlex
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import shared_checkout
from superpowers_source import load_superpowers_bundle_manifest, superpowers_source_root

ROOT = Path(__file__).resolve().parent.parent
SCRIPT_NAME = "tools/run"


PLUGIN_ROOTS_PATH = ROOT / "codex-marketplace" / "plugins"
PLUGIN_ROOT_INVENTORY_PATH = ROOT / "codex-marketplace" / "plugin-roots.json"
_MAX_CMD_CHARS = 28000


@dataclass(frozen=True)
class Ctx:
    mode: str
    base_ref: str | None
    allow_shared: bool
    verbose: bool


@dataclass(frozen=True)
class Task:
    deps: tuple[str, ...] = ()
    apply: tuple[Callable[[Ctx], None], ...] = ()
    check: tuple[Callable[[Ctx], None], ...] = ()
    fix: str = ""


class RunnerError(Exception):
    def __init__(self, target: str, fix: str, original: Exception | None = None):
        self.target = target
        self.fix = fix
        self.original = original
        super().__init__(f"[tools/run] target '{target}' failed.\nFix: {fix}")


def _run(cmd: list[str], ctx: Ctx) -> None:
    if ctx.verbose:
        print("+ " + " ".join(shlex.quote(part) for part in cmd))
    subprocess.run(cmd, cwd=ROOT, check=True)


def _ref_exists(ref: str) -> bool:
    return (
        subprocess.run(
            ["git", "rev-parse", "--verify", ref],
            cwd=ROOT,
            capture_output=True,
        ).returncode
        == 0
    )


def _resolve_base_ref(args: argparse.Namespace) -> str | None:
    if args.base_ref:
        if _ref_exists(args.base_ref):
            return args.base_ref
        print(f"warning: {args.base_ref} not found, no diff available to lint", file=sys.stderr)
        return None
    if _ref_exists("origin/main"):
        return "origin/main"
    print("warning: origin/main not found, no diff available to lint", file=sys.stderr)
    return None


def _changed_python_files(base_ref: str | None) -> list[Path]:
    if base_ref is None:
        return _all_tracked_python_files()
    diff = subprocess.run(
        ["git", "diff", "--name-only", "--diff-filter=ACMR", f"{base_ref}...HEAD"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    return [Path(p) for p in diff.stdout.splitlines() if p.endswith(".py") and (ROOT / p).is_file()]


def _all_tracked_python_files() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "--", "*.py"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    return [Path(p) for p in result.stdout.splitlines() if (ROOT / p).is_file()]


def _run_ruff(files: list[Path], ctx: Ctx, *, fix: bool = False) -> None:
    if not files:
        return
    file_args = [str(f) for f in files]
    check_cmd = [sys.executable, "-m", "ruff", "check"]
    if fix:
        check_cmd.append("--fix")
    check_cmd.extend(file_args)
    _run(check_cmd, ctx)
    fmt_cmd = [sys.executable, "-m", "ruff", "format", *file_args]
    _run(fmt_cmd, ctx)


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
            skill_name = local_path.split("/")[-1]
            skip_paths.add(f".agents/skills/{skill_name}")
            skip_paths.add(f".agents/skills/{skill_name}/SKILL.md")
    skip_paths.add(source_root)
    skip_paths.add(f"{source_root}/AGENTS.md")
    return skip_paths


def _git_diff_check(ctx: Ctx) -> None:
    retained = _retained_verbatim_paths()
    changed_paths = [
        path
        for path in subprocess.run(
            ["git", "diff", "--name-only", "HEAD"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.splitlines()
        if path and path not in retained
    ]
    if not changed_paths:
        return
    batch: list[str] = []
    batch_len = 0
    for path in changed_paths:
        path_len = len(path) + 4
        if batch and batch_len + path_len > _MAX_CMD_CHARS:
            _run(["git", "diff", "--check", "HEAD", "--", *batch], ctx)
            batch = []
            batch_len = 0
        batch.append(path)
        batch_len += path_len
    if batch:
        _run(["git", "diff", "--check", "HEAD", "--", *batch], ctx)


def _git_diff_exit_code(ctx: Ctx) -> None:
    _run(["git", "diff", "--exit-code"], ctx)


def _validate_marketplace_phase_step(phase: str, ctx: Ctx) -> None:
    _run(
        [
            sys.executable,
            "tools/validate_marketplace.py",
            "--phase",
            phase,
            "--skip-freshness-checks",
        ],
        ctx,
    )


def _apply_inventory(ctx: Ctx) -> None:
    _run([sys.executable, "tools/generate_plugin_root_inventory.py"], ctx)
    _prune_stale_projected_plugin_roots()
    _validate_marketplace_phase_step("inventory", ctx)


def _check_inventory(ctx: Ctx) -> None:
    _run([sys.executable, "tools/generate_plugin_root_inventory.py", "--check"], ctx)
    _validate_marketplace_phase_step("inventory", ctx)


def _apply_heal(ctx: Ctx) -> None:
    _run([sys.executable, "tools/heal_overlays.py"], ctx)


def _check_heal(ctx: Ctx) -> None:
    _run([sys.executable, "tools/heal_overlays.py", "--check"], ctx)


def _apply_project(ctx: Ctx) -> None:
    _run([sys.executable, "tools/update_skill_artifacts.py", "--all"], ctx)
    _run([sys.executable, "tools/normalize_first_party_skill_sources.py"], ctx)
    _validate_marketplace_phase_step("project", ctx)


def _check_project(ctx: Ctx) -> None:
    _run([sys.executable, "tools/update_skill_artifacts.py", "--check"], ctx)
    _run([sys.executable, "tools/normalize_first_party_skill_sources.py", "--check"], ctx)
    _validate_marketplace_phase_step("project", ctx)


def _apply_installed_skills(ctx: Ctx) -> None:
    cmd = [
        sys.executable,
        ".agents/skills/refreshing-installed-skills/scripts/refresh_installed_skills.py",
        "--apply",
    ]
    if ctx.allow_shared:
        cmd.append("--allow-shared-checkout")
    _run(cmd, ctx)


def _check_installed_skills(ctx: Ctx) -> None:
    _run(
        [
            sys.executable,
            ".agents/skills/refreshing-installed-skills/scripts/refresh_installed_skills.py",
            "--check",
        ],
        ctx,
    )


def _apply_repo_index(ctx: Ctx) -> None:
    _run([sys.executable, "tools/generate_repo_index.py"], ctx)
    _validate_marketplace_phase_step("index", ctx)


def _check_repo_index(ctx: Ctx) -> None:
    _run([sys.executable, "tools/generate_repo_index.py", "--check"], ctx)
    _validate_marketplace_phase_step("index", ctx)


def _apply_mesh(ctx: Ctx) -> None:
    cmd = [
        sys.executable,
        ".agents/skills/generating-agent-mesh/scripts/generate_index_mesh.py",
        "--apply",
    ]
    if ctx.allow_shared:
        cmd.append("--allow-shared-checkout")
    _run(cmd, ctx)
    _run(
        [sys.executable, ".agents/skills/generating-agent-mesh/scripts/generate_index_mesh.py", "--check"],
        ctx,
    )
    _run(
        [
            sys.executable,
            ".agents/skills/generating-agent-mesh/scripts/validate_agent_mesh.py",
            "--check",
        ],
        ctx,
    )


def _check_mesh(ctx: Ctx) -> None:
    _run(
        [
            sys.executable,
            ".agents/skills/generating-agent-mesh/scripts/generate_index_mesh.py",
            "--check",
        ],
        ctx,
    )
    _run(
        [
            sys.executable,
            ".agents/skills/generating-agent-mesh/scripts/validate_agent_mesh.py",
            "--check",
        ],
        ctx,
    )


def _apply_catalog(ctx: Ctx) -> None:
    _run([sys.executable, "tools/generate_first_party_skill_catalog.py"], ctx)
    _run([sys.executable, "tools/generate_first_party_skill_catalog.py", "--check"], ctx)


def _check_catalog(ctx: Ctx) -> None:
    _run([sys.executable, "tools/generate_first_party_skill_catalog.py", "--check"], ctx)


def _run_validate(ctx: Ctx) -> None:
    _run([sys.executable, "tools/validate_authority_assets.py"], ctx)
    _git_diff_check(ctx)
    if ctx.mode == "check":
        _git_diff_exit_code(ctx)


def _run_lint(ctx: Ctx) -> None:
    if ctx.mode == "check":
        if ctx.base_ref:
            _run([sys.executable, "tools/ruff_diff.py", "--changed-from", ctx.base_ref], ctx)
        else:
            print(
                "warning: no base ref available for lint; linting all tracked .py files",
                file=sys.stderr,
            )
            _run_ruff(_all_tracked_python_files(), ctx)
    else:
        files = _changed_python_files(ctx.base_ref)
        if not files:
            print("No changed Python files to lint.")
            return
        _run_ruff(files, ctx, fix=True)


def _run_repo_standards(ctx: Ctx) -> None:
    if ctx.mode == "check":
        _run(
            [
                sys.executable,
                ".agents/skills/repo-standards/scripts/repo_standards.py",
                "--check",
            ],
            ctx,
        )
    else:
        cmd = [
            sys.executable,
            ".agents/skills/repo-standards/scripts/repo_standards.py",
            "--apply",
            "--yes",
        ]
        if ctx.allow_shared:
            cmd.append("--allow-shared-checkout")
        _run(cmd, ctx)


_TASKS: dict[str, Task] = {
    "lint": Task(apply=(_run_lint,), check=(_run_lint,), fix="tools/run lint --apply"),
    "repo-standards": Task(
        apply=(_run_repo_standards,),
        check=(_run_repo_standards,),
        fix="tools/run repo-standards --apply",
    ),
    "inventory": Task(
        apply=(_apply_inventory,),
        check=(_check_inventory,),
        fix="tools/run inventory --apply",
    ),
    "heal": Task(
        deps=("inventory",),
        apply=(_apply_heal,),
        check=(_check_heal,),
        fix="tools/run heal --apply",
    ),
    "project": Task(
        deps=("heal",),
        apply=(_apply_project,),
        check=(_check_project,),
        fix="tools/run project --apply",
    ),
    "installed-skills": Task(
        deps=("project",),
        apply=(_apply_installed_skills,),
        check=(_check_installed_skills,),
        fix="tools/run installed-skills --apply",
    ),
    "repo-index": Task(
        deps=("installed-skills",),
        apply=(_apply_repo_index,),
        check=(_check_repo_index,),
        fix="tools/run repo-index --apply",
    ),
    "mesh": Task(
        deps=("repo-index",),
        apply=(_apply_mesh,),
        check=(_check_mesh,),
        fix="tools/run mesh --apply",
    ),
    "catalog": Task(
        deps=("mesh",),
        apply=(_apply_catalog,),
        check=(_check_catalog,),
        fix="tools/run catalog --apply",
    ),
    "validate": Task(
        deps=("catalog",),
        apply=(_run_validate,),
        check=(_run_validate,),
        fix="tools/run marketplace --apply",
    ),
    "marketplace": Task(
        deps=("validate",),
        fix="tools/run marketplace --apply",
    ),
    "ci": Task(
        deps=("lint", "repo-standards", "marketplace"),
        fix="tools/run ci --apply",
    ),
    "all": Task(
        deps=("ci",),
        fix="tools/run ci --apply",
    ),
}

_TARGET_ORDER = (
    "lint",
    "repo-standards",
    "inventory",
    "heal",
    "project",
    "installed-skills",
    "repo-index",
    "mesh",
    "catalog",
    "validate",
    "marketplace",
    "ci",
    "all",
)


def resolve_targets(requested: list[str]) -> list[str]:
    if not requested:
        raise ValueError("at least one target is required")

    seen: set[str] = set()
    visiting: set[str] = set()
    order: list[str] = []

    def visit(name: str) -> None:
        if name == "all":
            name = "ci"
        if name in visiting:
            raise ValueError(f"circular dependency detected involving {name}")
        if name in seen:
            return
        if name not in _TASKS:
            raise ValueError(f"unknown target: {name}")
        visiting.add(name)
        for dep in _TASKS[name].deps:
            visit(dep)
        visiting.remove(name)
        seen.add(name)
        order.append(name)

    for name in requested:
        visit(name)

    return sorted(order, key=lambda n: _TARGET_ORDER.index(n))


def _lint_fix(ctx: Ctx) -> str:
    files = _changed_python_files(ctx.base_ref)
    if not files:
        return "tools/run lint --apply"
    file_str = " ".join(str(f) for f in files)
    return f"{sys.executable} -m ruff check --fix {file_str} && {sys.executable} -m ruff format {file_str}"


def run_targets(targets: list[str], ctx: Ctx) -> None:
    for target in targets:
        task = _TASKS[target]
        steps = task.apply if ctx.mode == "apply" else task.check
        if not steps:
            continue
        print(f"[tools/run] === {target} ({ctx.mode})")
        for step in steps:
            try:
                step(ctx)
            except subprocess.CalledProcessError as exc:
                fix = _lint_fix(ctx) if target == "lint" else task.fix
                raise RunnerError(target, fix, exc) from exc


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Dependency-aware task runner for the agent-asset-marketplace",
        epilog=f"Targets: {', '.join(_TASKS.keys())}",
    )
    parser.add_argument(
        "targets",
        nargs="+",
        choices=tuple(_TASKS.keys()),
        help="target(s) to run",
    )
    parser.add_argument("--check", action="store_true", help="non-mutating validation (default)")
    parser.add_argument("--apply", action="store_true", help="regenerate outputs")
    parser.add_argument(
        "--base-ref",
        default=None,
        help="base ref for changed-line linting (default: origin/main)",
    )
    parser.add_argument(
        "--allow-shared-checkout",
        action="store_true",
        help="approve writes in the main shared checkout (requires --apply)",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="print each sub-command before executing it",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    if not args.check and not args.apply:
        args.check = True
    if args.apply and args.check:
        print("error: --apply and --check are mutually exclusive", file=sys.stderr)
        return 1
    if args.allow_shared_checkout and not args.apply:
        print("error: --allow-shared-checkout requires --apply", file=sys.stderr)
        return 1
    if args.apply:
        if not shared_checkout.approve_mutation(ROOT, SCRIPT_NAME, args.allow_shared_checkout):
            return 1
        if shared_checkout.is_main_shared_checkout(ROOT):
            args.allow_shared_checkout = True
    base_ref = _resolve_base_ref(args)
    ctx = Ctx(
        mode="apply" if args.apply else "check",
        base_ref=base_ref,
        allow_shared=args.allow_shared_checkout,
        verbose=args.verbose,
    )
    try:
        targets = resolve_targets(args.targets)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    try:
        run_targets(targets, ctx)
    except RunnerError as exc:
        print(exc, file=sys.stderr)
        return 1
    print("[tools/run] all requested targets passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
