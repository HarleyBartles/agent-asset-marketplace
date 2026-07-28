# Composable tooling (`tools/run`) implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

## Goal

Replace the flat `tools/rebuild_marketplace.py` and `scripts/ci-preflight` surfaces with a single dependency-aware `tools/run` task runner that composes the existing generator/validator scripts and unifies pre-commit, CI, and local regeneration.

## Architecture

- `tools/run.py` keeps an in-memory registry of named targets, their `--apply`/`--check` command sequences, dependencies, and fix messages.
- A resolver expands requested targets topologically, deduplicates them, and sorts them into a deterministic execution order.
- The runner executes each step with `subprocess.run`, forwards `--allow-shared-checkout` to scripts that require it, and prints a concrete repair command on failure.
- A tiny `tools/run` bash wrapper makes the surface discoverable and executable.
- The old entrypoints (`tools/rebuild_marketplace.py`, `scripts/ci-preflight.sh`, `scripts/ci-preflight.ps1`) and their test are deleted.
- `.git/hooks/pre-commit`, `.github/workflows/marketplace-validation.yml`, `tools/AGENTS.md`, `tools/README.md`, `tools/INDEX.md`, and the `repo-guide-policy.md` exceptions are updated to point at `tools/run`.

## Public interface

```text
tools/run <target>... [--check | --apply] [--base-ref <ref>] [--allow-shared-checkout] [--verbose]
tools/run.ps1 <target>... [--check | --apply] [--base-ref <ref>] [--allow-shared-checkout] [--verbose]
```

- On Linux/macOS/WSL/Git Bash: run `./tools/run`.
- On Windows PowerShell: run `./tools/run.ps1` (or `py -3 tools/run.py` / `python tools/run.py` as a fallback).
- Targets: `inventory`, `heal`, `project`, `installed-skills`, `repo-index`, `mesh`, `catalog`, `validate`, `marketplace`, `lint`, `repo-standards`, `ci`, `all`.
- `--check` is the default.
- `--allow-shared-checkout` is approved once with `shared_checkout.approve_mutation` and forwarded to child scripts that require explicit approval for writes in the main shared checkout.
- `--base-ref` defaults to `origin/main`; if unavailable, lint falls back to all tracked `.py` files with a warning.

## Global constraints

- All text files must be written with LF line endings (`newline="\n"`).
- `tools/run` must be importable and lintable as `tools/run.py`; the `tools/run` wrapper must `exec` the Python file and pass through exit codes.
- No external task runners (just/make/invoke).
- `tools/rebuild_marketplace.py`, `scripts/ci-preflight.sh`, `scripts/ci-preflight.ps1`, and `tests/test_rebuild_marketplace_cli.py` are deleted.
- `sources/first_party/skills/repo-standards/` and its generated marketplace projection are **not** modified; instead, `repo-guide-policy.md` exceptions are added for the removed surfaces.
- Do not rewrite historical specs/plans; only update active, tracked guidance that still advertises deleted canonical commands.

---

## Task 1: Create `tools/run.py`

**Files:** create `tools/run.py`
**Produces:** `main`, `resolve_targets`, `run_targets`, `Ctx`, `RunnerError`, `_TASKS`.

- [x] Step 1: Write `tools/run.py` with the following content.
- [x] Step 2: Run `python tools/run.py --help` and verify it exits 0.
- [x] Step 3: Commit.

```python
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

ROOT = Path(__file__).resolve().parent.parent
SCRIPT_NAME = "tools/run"

import shared_checkout
from superpowers_source import load_superpowers_bundle_manifest, superpowers_source_root


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
    return [
        Path(p)
        for p in diff.stdout.splitlines()
        if p.endswith(".py") and (ROOT / p).is_file()
    ]


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
```

Commit message:
```text
feat(tools): add dependency-aware task runner

Introduces tools/run.py and a tools/run wrapper that compose the
existing generator/validator scripts into named targets with --check
and --apply modes, dependency resolution, --allow-shared-checkout
forwarding, and concrete Fix: messages on failure.
```

---

## Task 2: Create `tools/run` and `tools/run.ps1` wrappers

**Files:** create `tools/run`, `tools/run.ps1`

- [x] Step 1: Write `tools/run` with the following content.
- [x] Step 2: Make `tools/run` executable.
- [x] Step 3: Write `tools/run.ps1` with the following content.
- [x] Step 4: Test `./tools/run --help` (or `bash tools/run --help` on Windows) and `.\tools\run.ps1 --help` in PowerShell and verify both print help.
- [x] Step 5: Commit.

```bash
#!/usr/bin/env bash
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

PYTHON=""
for bin in python3 python; do
    if command -v "$bin" >/dev/null 2>&1; then
        PYTHON="$bin"
        break
    fi
done

if [ -z "$PYTHON" ]; then
    echo "No Python interpreter found" >&2
    exit 1
fi

exec "$PYTHON" "$REPO_ROOT/tools/run.py" "$@"
```

```bash
chmod +x tools/run
git update-index --chmod=+x tools/run || true
```

```powershell
#Requires -Version 5.1
$ErrorActionPreference = 'Stop'

$RepoRoot = Split-Path -Parent $PSScriptRoot

$python = $null
$pythonArgs = @()
if (Get-Command py -ErrorAction SilentlyContinue) {
    $python = 'py'
    $pythonArgs += '-3'
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
    $python = 'python'
} elseif (Get-Command python3 -ErrorAction SilentlyContinue) {
    $python = 'python3'
} else {
    throw 'No Python interpreter found'
}

& $python @($pythonArgs + "$RepoRoot/tools/run.py") @args
exit $LASTEXITCODE
```

Commit message:
```text
feat(tools): add executable tools/run and tools/run.ps1 wrappers
```

---

## Task 3: Add `tests/test_run_cli.py`

**Files:** create `tests/test_run_cli.py`, delete `tests/test_rebuild_marketplace_cli.py` (Task 4).

- [x] Step 1: Write `tests/test_run_cli.py` with the following content.
- [x] Step 2: Run `py -3 -m pytest tests/test_run_cli.py -v`. Fix any failures.
- [x] Step 3: Commit.

```python
from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import run


def test_run_help_exposes_targets_and_flags():
    result = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "run.py"), "--help"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert "--check" in result.stdout
    assert "--apply" in result.stdout
    assert "--base-ref" in result.stdout
    assert "--allow-shared-checkout" in result.stdout
    assert "marketplace" in result.stdout
    assert "ci" in result.stdout


def test_apply_and_check_mutually_exclusive():
    result = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "run.py"), "inventory", "--apply", "--check"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 1
    assert "mutually exclusive" in result.stderr


def test_allow_shared_checkout_requires_apply():
    result = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "run.py"), "inventory", "--allow-shared-checkout"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 1
    assert "--allow-shared-checkout requires --apply" in result.stderr


def test_resolve_ci_order():
    targets = run.resolve_targets(["ci"])
    assert targets.index("lint") < targets.index("repo-standards") < targets.index("marketplace")
    assert targets.index("inventory") < targets.index("heal") < targets.index("project")
    assert targets.index("project") < targets.index("installed-skills")
    assert targets.index("installed-skills") < targets.index("repo-index")
    assert targets.index("repo-index") < targets.index("mesh")
    assert targets.index("mesh") < targets.index("catalog")
    assert targets.index("catalog") < targets.index("validate")
    assert targets[-1] == "ci"


def test_resolve_all_aliases_to_ci():
    assert run.resolve_targets(["all"]) == run.resolve_targets(["ci"])


def test_resolve_multiple_targets_deduped():
    targets = run.resolve_targets(["mesh", "installed-skills"])
    assert "mesh" in targets
    assert "installed-skills" in targets
    assert targets.index("project") < targets.index("installed-skills")
    assert targets.index("project") < targets.index("repo-index") < targets.index("mesh")


def test_runner_forwards_allow_shared_checkout(monkeypatch):
    calls = []
    def fake_run(cmd, ctx):
        calls.append(cmd)
    monkeypatch.setattr(run, "_run", fake_run)
    monkeypatch.setattr(run, "_prune_stale_projected_plugin_roots", lambda: None)
    monkeypatch.setattr(run, "_git_diff_check", lambda ctx: None)
    monkeypatch.setattr(run, "_git_diff_exit_code", lambda ctx: None)

    ctx = run.Ctx(mode="apply", base_ref=None, allow_shared=True, verbose=False)
    run.run_targets(["mesh"], ctx)

    mesh_cmd = next(
        (c for c in calls if "generate_index_mesh.py" in " ".join(c) and "--apply" in c),
        None,
    )
    assert mesh_cmd is not None
    assert "--allow-shared-checkout" in mesh_cmd


def test_runner_check_mode_no_allow_shared(monkeypatch):
    calls = []
    def fake_run(cmd, ctx):
        calls.append(cmd)
    monkeypatch.setattr(run, "_run", fake_run)
    monkeypatch.setattr(run, "_git_diff_check", lambda ctx: None)
    monkeypatch.setattr(run, "_git_diff_exit_code", lambda ctx: None)

    ctx = run.Ctx(mode="check", base_ref=None, allow_shared=True, verbose=False)
    run.run_targets(["repo-standards", "mesh"], ctx)

    for cmd in calls:
        assert "--allow-shared-checkout" not in " ".join(cmd)
        assert "--apply" not in " ".join(cmd)


def test_failure_prints_fix(monkeypatch):
    def boom(cmd, ctx):
        raise subprocess.CalledProcessError(1, cmd)
    monkeypatch.setattr(run, "_run", boom)

    ctx = run.Ctx(mode="check", base_ref=None, allow_shared=False, verbose=False)
    with pytest.raises(run.RunnerError) as exc_info:
        run.run_targets(["inventory"], ctx)
    assert "target 'inventory' failed" in str(exc_info.value)
    assert "Fix: tools/run inventory --apply" in str(exc_info.value)


def test_lint_fix_command_used_in_apply(monkeypatch):
    files = [Path("tools/run.py")]
    monkeypatch.setattr(run, "_changed_python_files", lambda base: files)

    calls = []
    def fake_run(cmd, ctx):
        calls.append(cmd)
    monkeypatch.setattr(run, "_run", fake_run)

    ctx = run.Ctx(mode="apply", base_ref="origin/main", allow_shared=False, verbose=False)
    run.run_targets(["lint"], ctx)

    check_cmd = [c for c in calls if c[1:4] == ["-m", "ruff", "check"]]
    assert check_cmd
    assert "--fix" in check_cmd[0]
    fmt_cmd = [c for c in calls if c[1:4] == ["-m", "ruff", "format"]]
    assert fmt_cmd
```

Commit message:
```text
test(tools): add tests for tools/run CLI

Replaces tests/test_rebuild_marketplace_cli.py with tests/test_run_cli.py.
```

---

## Task 4: Delete obsolete entrypoints

**Files:** delete `tools/rebuild_marketplace.py`, `scripts/ci-preflight.sh`, `scripts/ci-preflight.ps1`, `tests/test_rebuild_marketplace_cli.py`.

- [x] Step 1: Delete the four files.
- [x] Step 2: Remove the `rebuild_marketplace.py` line from `tools/INDEX.md`.

Old block in `tools/INDEX.md`:
```markdown
- [README.md](tools/README.md)
- [rebuild_marketplace.py](tools/rebuild_marketplace.py)
- [ruff_diff.py](tools/ruff_diff.py)
```

New block:
```markdown
- [README.md](tools/README.md)
- [run](tools/run)
- [run.ps1](tools/run.ps1)
- [run.py](tools/run.py)
- [ruff_diff.py](tools/ruff_diff.py)
```

- [x] Step 3: Commit.

Commit message:
```text
chore(tools): remove obsolete rebuild_marketplace.py and ci-preflight scripts
```

---

## Task 5: Update `tools/update_skill_artifacts.py`

**Files:** overwrite `tools/update_skill_artifacts.py`

- [x] Step 1: Replace the entire file with the following content.
- [x] Step 2: Run `py -3 tools/update_skill_artifacts.py --help` and `py -3 tools/update_skill_artifacts.py --check` (read-only; should exit 0 if marketplace is current, otherwise it reports drift).
- [x] Step 3: Commit.

```python
#!/usr/bin/env python3
"""Worker-facing entrypoint for deterministic skill artifact updates.

This script orchestrates the core skill artifact pipeline:
generate mega-packs, generate pack manifests, project skills into plugin
trees and flat skill zips, and refresh the first-party skill catalog.

Use `tools/run marketplace --apply` for the canonical full regeneration and
validation gate. This script is an implementation detail invoked by the
`project` target.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from generate_mega_packs import generate_all_mega_packs
from generate_pack_manifests import generate as generate_pack_manifests
from generate_first_party_skill_catalog import generate as generate_first_party_skill_catalog
from project_skills import project_skills


def _run_tool(script_name: str, *args: str) -> None:
    script_path = Path(__file__).resolve().with_name(script_name)
    subprocess.run([sys.executable, str(script_path), *args], check=True)


def _run_full_regeneration_checks() -> None:
    """Run the repo-wide generated-surface checks for a full refresh."""
    _run_tool("generate_marketplace.py", "--check")
    _run_tool("generate_repo_index.py", "--check")
    generate_pack_manifests(write=False)
    generate_all_mega_packs(write=False)
    project_skills(write=False)
    _run_tool("generate_provenance_maps.py", "--check")
    _run_tool("generate_source_maps.py", "--check")
    generate_first_party_skill_catalog(write=False)


def _run_full_regeneration_writes() -> None:
    """Run every deterministic writer that participates in a full regen."""
    _run_tool("generate_marketplace.py")
    _run_tool("generate_repo_index.py")
    generate_pack_manifests(write=True)
    generate_all_mega_packs(write=True)
    project_skills(write=True)
    _run_tool("generate_provenance_maps.py")
    _run_tool("generate_source_maps.py")
    generate_first_party_skill_catalog(write=True)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Update or validate canonical skill artifacts")
    parser.add_argument("--all", action="store_true", help="regenerate every installable skill")
    parser.add_argument("--check", action="store_true", help="validate current generated artifacts without writing")
    args = parser.parse_args()
    if args.check and args.all:
        parser.error("--check cannot be combined with --all")
    if not args.check and not args.all:
        parser.error("choose --all or --check")
    return args


def main() -> int:
    args = _parse_args()
    if args.check:
        _run_full_regeneration_checks()
    else:
        _run_full_regeneration_writes()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

Commit message:
```text
refactor(tools): remove --skill and --pack from update_skill_artifacts.py

The targeted flags are no longer supported; the script now only accepts
--all and --check. It remains the implementation detail behind the
project/marketplace targets of tools/run.
```

---

## Task 6: Update tool callers and generated command metadata

**Files:** `tools/update_superpowers_source.py`, `tools/generate_repo_index.py`, `tools/validate_repo_index.py`

### 6a. `tools/update_superpowers_source.py`

Old block:
```python
    rebuild_args = [sys.executable, str(ROOT / "tools" / "rebuild_marketplace.py"), "--apply"]
    if allow_shared_checkout:
        rebuild_args.append("--allow-shared-checkout")
    _run(*rebuild_args)
```

New block:
```python
    regen_args = [sys.executable, str(ROOT / "tools" / "run.py"), "marketplace", "--apply"]
    if allow_shared_checkout:
        regen_args.append("--allow-shared-checkout")
    _run(*regen_args)
```

### 6b. `tools/generate_repo_index.py` default validation dict

Old block:
```python
        "marketplace": "py -3 tools/validate_marketplace.py",
        "repo_index": "py -3 tools/validate_repo_index.py",
        "skill_zips_update": "py -3 tools/update_skill_artifacts.py --skill <pack>/<skill>",
        "skill_zips_full_regeneration": "py -3 tools/update_skill_artifacts.py --all",
        "skill_zips_check": "py -3 tools/validate_skill_zips.py",
```

New block:
```python
        "marketplace": "py -3 tools/validate_marketplace.py",
        "repo_index": "py -3 tools/validate_repo_index.py",
        "skill_zips_update": "tools/run project --apply",
        "skill_zips_full_regeneration": "tools/run marketplace --apply",
        "skill_zips_check": "py -3 tools/validate_skill_zips.py",
```

### 6c. `tools/generate_repo_index.py` runtime validation update

Old block:
```python
    validation["marketplace_generate"] = "py -3 tools/generate_marketplace.py"
    validation["marketplace_check"] = "py -3 tools/generate_marketplace.py --check"
    validation["repo_index_generate"] = "py -3 tools/generate_repo_index.py"
    validation["repo_index_check"] = "py -3 tools/generate_repo_index.py --check"
    validation["skill_zips_check"] = "py -3 tools/validate_skill_zips.py"
    validation.pop("generated_drift", None)
```

New block:
```python
    validation["marketplace_generate"] = "py -3 tools/generate_marketplace.py"
    validation["marketplace_check"] = "py -3 tools/generate_marketplace.py --check"
    validation["repo_index_generate"] = "py -3 tools/generate_repo_index.py"
    validation["repo_index_check"] = "py -3 tools/generate_repo_index.py --check"
    validation["skill_zips_update"] = "tools/run project --apply"
    validation["skill_zips_full_regeneration"] = "tools/run marketplace --apply"
    validation["skill_zips_check"] = "py -3 tools/validate_skill_zips.py"
    validation.pop("generated_drift", None)
```

### 6d. `tools/validate_repo_index.py`

Old block:
```python
    if validation.get("skill_zips_update") != "py -3 tools/update_skill_artifacts.py --skill <pack>/<skill>":
        raise ValueError("repo-index skill_zips_update command mismatch")
    if validation.get("skill_zips_full_regeneration") != "py -3 tools/update_skill_artifacts.py --all":
        raise ValueError("repo-index skill_zips_full_regeneration command mismatch")
```

New block:
```python
    if validation.get("skill_zips_update") != "tools/run project --apply":
        raise ValueError("repo-index skill_zips_update command mismatch")
    if validation.get("skill_zips_full_regeneration") != "tools/run marketplace --apply":
        raise ValueError("repo-index skill_zips_full_regeneration command mismatch")
```

- [x] Step 1: Apply the four edits above.
- [x] Step 2: Commit.

Commit message:
```text
chore(tools): point tool callers and repo-index metadata at tools/run
```

---

## Task 7: Update CI, pre-commit, and repo-guide-policy exceptions

**Files:** `.github/workflows/marketplace-validation.yml`, `.git/hooks/pre-commit` (create), `.agents/docs/repo-guide-policy.md`

### 7a. `.github/workflows/marketplace-validation.yml`

Overwrite the entire file with:

```yaml
name: Marketplace validation

on:
  pull_request:
    types:
      - opened
      - synchronize
      - reopened
      - ready_for_review
  push:
    branches:
      - main
  workflow_dispatch:

permissions:
  contents: read

concurrency:
  group: marketplace-validation-${{ github.ref }}
  cancel-in-progress: true

jobs:
  marketplace-validation:
    name: marketplace-validation
    if: ${{ github.event_name != 'pull_request' || github.event.pull_request.draft == false }}
    runs-on: ubuntu-latest
    timeout-minutes: 20

    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Fetch origin/main
        run: git fetch origin main

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: CI gate
        shell: bash
        run: |
          set -euo pipefail
          tools/run ci --check
```

### 7b. `.git/hooks/pre-commit`

Create the local hook (not tracked by git):

```bash
#!/usr/bin/env bash
set -euo pipefail
REPO_ROOT="$(git rev-parse --show-toplevel)"
exec "$REPO_ROOT/tools/run" ci --check
```

```bash
cat << 'EOF' > .git/hooks/pre-commit
#!/usr/bin/env bash
set -euo pipefail
REPO_ROOT="$(git rev-parse --show-toplevel)"
exec "$REPO_ROOT/tools/run" ci --check
EOF
chmod +x .git/hooks/pre-commit
```

### 7c. `.agents/docs/repo-guide-policy.md`

Old block:
```markdown
## Exceptions

- `marketplace-source-submodule` — this repo is the marketplace source and does not vendor itself as a submodule.
```

New block:
```markdown
## Exceptions

- `marketplace-source-submodule` — this repo is the marketplace source and does not vendor itself as a submodule.
- `ci-preflight-ps1` — removed; replaced by `tools/run ci --check`.
- `ci-preflight-sh` — removed; replaced by `tools/run ci --check`.
- `pre-commit-hook` — local hook now calls `tools/run ci --check`; repo-standards should not overwrite it.
```

- [x] Step 1: Apply 7a, 7b, and 7c.
- [x] Step 2: Verify the workflow YAML is valid (`python -c "import yaml; yaml.safe_load(open('.github/workflows/marketplace-validation.yml'))"` if PyYAML is installed).
- [x] Step 3: Commit.

Commit message:
```text
chore(ci): use tools/run ci --check in workflow and pre-commit
```

---

## Task 8: Update canonical documentation

**Files:** `tools/AGENTS.md`, `tools/README.md`, `tools/INDEX.md` (already updated in Task 4). Also update remaining active guidance that still advertises the deleted canonical commands using the sweep script in this task.

### 8a. `tools/AGENTS.md`

Overwrite the entire file with:

```markdown
# AGENTS.md

Scope: `tools/`

This scope covers repository validation and generation scripts.

Defer to the repository root `AGENTS.md` for global doctrine, publication
rules, and upstream-drain policy.

The canonical task runner is `tools/run`. It composes the individual
generator and validator scripts into a dependency-aware task graph.

- `./tools/run ci --check` (or `.\tools\run.ps1 ci --check` on Windows PowerShell) is the full non-mutating CI gate (lint, repo-standards, marketplace).
- `./tools/run marketplace --apply` (or `.\tools\run.ps1 marketplace --apply` on Windows PowerShell) is the canonical local full regeneration and validation entrypoint.
- `tools/run <target> --apply` / `tools/run.ps1 <target> --apply` regenerates only the named target and its prerequisites.
- `tools/run <target> --check` / `tools/run.ps1 <target> --check` validates only the named target and its prerequisites without writing.
- `tools/run --help` / `tools/run.ps1 --help` lists all targets and flags.
- `py -3 tools/run.py` or `python tools/run.py` works on any platform as a fallback.

Targets are: `inventory`, `heal`, `project`, `installed-skills`, `repo-index`, `mesh`, `catalog`, `validate`, `marketplace`, `lint`, `repo-standards`, `ci`, `all`.

The underlying scripts are implementation details:

- `generate_marketplace.py` regenerates `.agents/plugins/marketplace.json` and `codex-marketplace/manifest.json` from the local plugin bundle and source ledger, and `--check` compares both files without writing.
- `update_skill_artifacts.py` is the canonical generator orchestrator for full regeneration. Use `--all` to regenerate every installable skill artifact, or `--check` to validate without writing.
- `project_skills.py` stages overlays, materializes plugin skill trees under `codex-marketplace/plugins/<pack>/skills/`, and writes flat deterministic `generated/skill-zips/<skill>.zip` archives. `--check` validates projected trees and zip shape without writing.
- `validate_skill_zips.py` checks the canonical flat `skill.zip` surface and fails on stale, missing, or malformed artifacts.
- `validate_marketplace.py` checks the marketplace export, plugin manifest, bundle manifest, source ledger, repo index, local path references, projection materialization, and selected pack bundle-manifest freshness for the protected marketplace shape.
- `validate_repo_index.py` checks that the repo index stays aligned with the current marketplace and scoped guidance surfaces, but it is not the freshness proof for `repo-index/repo-index.json`.
- `generate_repo_index.py` regenerates `repo-index/repo-index.json` and `--check` compares the rendered file without writing.
- `generate_pack_manifests.py` regenerates the selected pack bundle-manifest surfaces and `--check` compares them without writing.
- `heal_overlays.py` adjusts `overlay.yaml` line-edit entries when source normalization shifts line numbers or whitespace. It runs in the `heal` target.
- `normalize_first_party_skill_sources.py` normalizes first-party `SKILL.md` and `agents/openai.yaml` content.
- `generate_first_party_skill_catalog.py` regenerates `provenance/first-party-skills.md`.
- `tools/ruff_diff.py` reports ruff findings only on added or modified lines when given `--changed-from <ref>`.
- `tools/run` uses `ruff_diff.py` for `lint --check` and runs `ruff check --fix` / `ruff format` for `lint --apply`.
- `python .agents/skills/repo-standards/scripts/repo_standards.py --check` checks repo shape; `python .agents/skills/repo-standards/scripts/repo_standards.py --apply --yes` applies missing surfaces.
- `python .agents/skills/refreshing-installed-skills/scripts/refresh_installed_skills.py --apply` refreshes skills in `.agents/skills` based on plugins with `INSTALLED_BY_DEFAULT` policy. In the main shared checkout, pass `--apply --allow-shared-checkout` to approve; linked worktrees do not need the flag.
- `python .agents/skills/generating-agent-mesh/scripts/generate_index_mesh.py --apply` regenerates repo-wide `INDEX.md` files; `--check` validates them.
- `python .agents/skills/generating-agent-mesh/scripts/validate_agent_mesh.py --check` validates mesh link reachability and doctrine.

Codex plugin first; generated GPT-safe skill zips second.

Current scope note: `generated/skill-zips/` is the flat GPT-ready export surface
for skill zips. It is a deterministic copy of the staged Codex projection.

Common worker commands:

```bash
# Full local regeneration and validation (Linux/macOS/WSL/Git Bash)
./tools/run marketplace --apply

# Full CI gate (read-only) (Linux/macOS/WSL/Git Bash)
./tools/run ci --check

# Regenerate only the mesh (Linux/macOS/WSL/Git Bash)
./tools/run mesh --apply
```

```powershell
# Full local regeneration and validation (Windows PowerShell)
.\tools\run.ps1 marketplace --apply

# Full CI gate (read-only) (Windows PowerShell)
.\tools\run.ps1 ci --check

# Regenerate only the mesh (Windows PowerShell)
.\tools\run.ps1 mesh --apply
```

Use `--check` to validate the current generated surface without rewriting it.
`--allow-shared-checkout` is approved once by `tools/run` and forwarded to child
scripts that require explicit approval to write in the main shared checkout
(`generate_index_mesh.py`, `refresh_installed_skills.py`, `repo_standards.py`).
It is not needed in a linked worktree. `--allow-shared-checkout` alone is
rejected by those scripts.

`py -3 tools/generate_pack_manifests.py --check` also verifies any
manifest-declared generated inventory blocks in pack `README.md`, `SOURCE.md`,
and `PROJECTION.md` surfaces.

## Routing pointers

- `../.agents/docs/mesh-policy.md` before changing generator or validator behavior
- `../.agents/guides/planning-guide.md` before planning tool changes
- `../.agents/guides/implementing-guide.md` before implementing tool changes
- `../.agents/guides/marketplace-generation-guide.md` before changing marketplace regeneration behavior
- `../.agents/guides/code-review-guide.md` before reviewing tooling changes

Policy for agent work:

- Any change to source custody, adapter files, projection plugin shapes, bundle manifests,
  source maps, provenance maps, or generated zips requires a full market regeneration
  followed by validation before a PR may be called green.
- The canonical completion path is the full regeneration stack, not a partial refresh.
- Partial regeneration paths are fallback-only repair tools and should not be
  advertised as a normal completion route.
- The expected local green-path proof is `tools/run marketplace --apply`.
- The expected CI green-path proof is `tools/run ci --check`.
- Both commands must be aligned so check mode fails if regeneration would be
  needed and write mode still performs the actual regeneration locally.
- If a worker cannot run the full stack, it must say so explicitly instead of
  assuming CI will catch the missing regeneration.

Deterministic pack rule: if a skillset pack or projection lane lacks a
manifest-driven generator/validator path, add one to `tools/` and wire it into
the standard update/check entrypoints. Do not paper over missing pipeline
support with a pack-specific one-off script or a hand-edited output surface.
The editable source custody for marketplace generation is the trio of source
trees, adapters/overlays, and `codex-marketplace/custody-pack-registry.json`.
Treat generated manifests, projection trees, source maps, provenance maps, and
zip artifacts as derived outputs only. If a convention can be expressed in the
registry and generator, do that instead of hand-rolling per-pack output
conventions in the generated surfaces.

## Line-ending policy for generated files

This repo normalizes to LF. `core.autocrlf` is `false` so git does not
translate line endings. Generators and agents that write text files must
write LF explicitly, not the platform default (CRLF on Windows).

When writing text files, prefer `open("w")` with `newline="\n"`:
```python
with path.open("w", encoding="utf-8", newline="\n") as f:
    f.write(content)
```

Do not pass `newline=` to `Path.read_text()` in scripts that must run under
Python 3.12; the `newline` keyword for `Path.read_text()` was added in Python
3.13. For consistent LF-only reads and writes across `Path.read_text()` and
`Path.write_text()`, prefer `Path.open(..., newline="\n")` or the built-in
`open(..., newline="\n")` (or `newline=""` if the text already contains explicit
`\n` and you want no translation) instead.

Without the explicit `newline` parameter, Python translates `\n` to
`os.linesep` (CRLF on Windows), which `git diff --check` flags as trailing
whitespace and which churns every generated file on every rebuild.

Do not add CRLF detection or preservation logic to generators. Always
write LF.

## Review guidelines

- Flag validators that can pass while indexed paths, plugin manifests, or
  registry entries have already drifted.
- Flag generator changes that are not paired with matching validation updates.
- Flag JSON or path parsing that could silently skip missing files, stale
  references, or unsupported plugin entries.
- Flag tooling changes that do not keep the marketplace export, repo index,
  and validation command documentation aligned.
- Flag targeted skill-update helpers that rewrite unrelated generated state or
  that hide full-regeneration behavior behind an ordinary update path.
- Flag flat skill.zip artifacts that do not match the staged Codex projection
  or that contain stale adapter, gpt, or per-pack zip references.

## Maintenance responsibility

This file must stay aligned with the repo's validation and generation tooling.
When tooling paths change, new validation scripts are added, or worker-facing
commands evolve, review and update this file to reflect current expectations.
The skill-update path, marketplace inventory source, and drift validation
references must stay accurate—when those change, this file should be updated
to prevent drift.
```

### 8b. `tools/README.md`

Overwrite the entire file with:

```markdown
# tools

Small helper scripts belong here.

Agent-facing policy for this directory lives in [AGENTS.md](AGENTS.md).

Canonical task runner:

- `tools/run <target>... [--check | --apply] [--base-ref <ref>] [--allow-shared-checkout] [--verbose]` — dependency-aware runner that composes the marketplace generators and validators. On Linux/macOS/WSL/Git Bash use `./tools/run`; on Windows PowerShell use `.\tools\run.ps1`. `py -3 tools/run.py` works as a cross-platform fallback. The individual `.py` files below are implementation details.

Useful targets:

- `tools/run ci --check` / `tools/run.ps1 ci --check` — full non-mutating CI gate (lint, repo-standards, marketplace).
- `tools/run marketplace --apply` / `tools/run.ps1 marketplace --apply` — regenerate all marketplace surfaces.
- `tools/run marketplace --apply --allow-shared-checkout` / `tools/run.ps1 marketplace --apply --allow-shared-checkout` — approve writes in the main shared checkout.
- `tools/run mesh --apply` / `tools/run.ps1 mesh --apply` — regenerate only the repo-wide `INDEX.md` mesh.
- `tools/run installed-skills mesh --apply` / `tools/run.ps1 installed-skills mesh --apply` — refresh installed skills and regenerate the mesh.

Keep tooling minimal and focused on validation or lightweight asset handling.
```

### 8c. Doc sweep for remaining active guidance

Run the following script from the repo root. It updates command references in
`codex-marketplace/AGENTS.md`, `.agents/guides/*.md`, and
`docs/skill-standards-policy.md` to use `tools/run`.

```python
from pathlib import Path

ROOT = Path.cwd()

FILES = [
    ROOT / ".agents/guides/testing-guide.md",
    ROOT / ".agents/guides/skill-authoring-guide.md",
    ROOT / ".agents/guides/pr-guide.md",
    ROOT / ".agents/guides/implementing-guide.md",
    ROOT / ".agents/guides/code-review-guide.md",
    ROOT / ".agents/guides/planning-guide.md",
    ROOT / ".agents/guides/marketplace-generation-guide.md",
    ROOT / "codex-marketplace/AGENTS.md",
    ROOT / "docs/skill-standards-policy.md",
]

REPLACEMENTS = [
    ("py -3 sources/first_party/skills/refreshing-installed-skills/scripts/refresh_installed_skills.py --apply", "tools/run installed-skills --apply"),
    ("py -3 sources/first_party/skills/refreshing-installed-skills/scripts/refresh_installed_skills.py --check", "tools/run installed-skills --check"),
    ("py -3 sources/first_party/skills/generating-agent-mesh/scripts/generate_index_mesh.py --apply", "tools/run mesh --apply"),
    ("py -3 sources/first_party/skills/generating-agent-mesh/scripts/generate_index_mesh.py --check", "tools/run mesh --check"),
    ("py -3 tools/install_agent_skills.py", "tools/run installed-skills --apply"),
    ("py -3 tools/generate_index_mesh.py", "tools/run mesh --apply"),
    ("py -3 tools/rebuild_marketplace.py --apply", "tools/run marketplace --apply"),
    ("py -3 tools/rebuild_marketplace.py --check", "tools/run marketplace --check"),
    ("py -3 tools/rebuild_marketplace.py", "tools/run marketplace --apply"),
    ("tools/rebuild_marketplace.py --apply", "tools/run marketplace --apply"),
    ("tools/rebuild_marketplace.py --check", "tools/run marketplace --check"),
    ("tools/rebuild_marketplace.py", "tools/run"),
    ("rebuild_marketplace.py --apply", "tools/run marketplace --apply"),
    ("rebuild_marketplace.py --check", "tools/run marketplace --check"),
    ("rebuild_marketplace.py", "tools/run"),
    ("bash scripts/ci-preflight.sh --check", "tools/run ci --check"),
    ("scripts/ci-preflight.sh --check", "tools/run ci --check"),
    ("scripts/ci-preflight.sh", "tools/run ci --check"),
]

for path in FILES:
    if not path.is_file():
        continue
    text = path.read_text(encoding="utf-8")
    for old, new in REPLACEMENTS:
        text = text.replace(old, new)
    path.write_text(text, encoding="utf-8", newline="\n")
```

After running it, inspect `git diff` and `tools/run ci --check` output.

- [x] Step 1: Write `tools/AGENTS.md`, `tools/README.md`, update `tools/INDEX.md`.
- [x] Step 2: Run the doc-sweep script.
- [x] Step 3: Review the diff for obviously broken replacements.
- [x] Step 4: Commit.

Commit message:
```text
docs(tools): document tools/run and retire rebuild_marketplace/ci-preflight references
```

---

## Task 9: Final regeneration and verification

- [x] Step 1: Run lint apply to fix any ruff issues in the new files.
  ```bash
  tools/run lint --apply
  ```
- [x] Step 2: Regenerate the full marketplace.
  ```bash
  tools/run marketplace --apply --allow-shared-checkout
  ```
- [x] Step 3: Stage and commit the generated drift.
  ```bash
  git add -A
  git commit -m "chore: regenerate marketplace with tools/run"
  ```
- [x] Step 4: Run the CI gate.
  ```bash
  tools/run ci --check
  ```
- [x] Step 5: Run the focused and full test suites.
  ```bash
  py -3 -m pytest tests/test_run_cli.py -v
  py -3 -m pytest
  ```
- [x] Step 6: If any step fails, fix the underlying source (not the generated outputs) and repeat from Step 2.
- [x] Step 7: Commit any final fixes and report completion.

---

## Plan-readiness self-review

| Lane | Check | Status |
|------|-------|--------|
| Spec coverage | All required surfaces (tools/run.py, tools/run wrapper, --check/--apply, --allow-shared-checkout forwarding, dependency graph, Fix messages, CI/pre-commit/docs updates) are represented. | Pass |
| No placeholders | Every task gives exact file content or exact old-string/new-string edits. The doc-sweep script lists exact files and exact replacements. | Pass |
| Dependency order | Target graph matches the spec: marketplace = inventory → heal → project → installed-skills → repo-index → mesh → catalog → validate; ci = lint → repo-standards → marketplace; all = ci. | Pass |
| Validation alignment | `tools/run ci --check` runs lint, repo-standards, and marketplace checks; `marketplace --apply` regenerates; `marketplace --check` includes `git diff --exit-code`. | Pass |
| Risk | The doc-sweep script may over-replace prose; the implementer must review `git diff` after running it. A fallback is to manually fix any awkward replacements. | Noted |
| Deletion safety | `rebuild_marketplace.py`, `ci-preflight.sh/.ps1`, and `tests/test_rebuild_marketplace_cli.py` are removed; `repo-guide-policy.md` exceptions prevent `repo-standards` drift. | Pass |

**Plan-readiness rating:** 9/10

The plan is concrete enough for a competent implementer to transcribe without designing in flight. The main residual risk is the generic doc-sweep script over-replacing prose, which is mitigated by the explicit instruction to review `git diff` after running it.
