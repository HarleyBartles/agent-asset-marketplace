#!/usr/bin/env python3
"""Dependency-aware task runner for the agent-asset-marketplace tooling."""

from __future__ import annotations

import argparse
import json
import os
import shlex
import shutil
import subprocess
import sys
from dataclasses import dataclass, replace as dataclass_replace
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).resolve().parent.parent


PLUGIN_ROOTS_PATH = ROOT / "dist" / "plugins"
PLUGIN_ROOT_INVENTORY_PATH = ROOT / "dist" / "plugin-roots.json"
_MAX_CMD_CHARS = 28000


@dataclass(frozen=True)
class Ctx:
    mode: str
    base_ref: str | None
    verbose: bool
    diagnostics: bool = False
    files: tuple[Path, ...] = ()


@dataclass(frozen=True)
class Task:
    deps: tuple[str, ...] = ()
    apply: tuple[Callable[[Ctx], None], ...] = ()
    check: tuple[Callable[[Ctx], None], ...] = ()
    description: str = ""
    prerequisites: tuple[str, ...] = ()
    side_effects: str = ""


class ValidationFailure(Exception):
    def __init__(self, message: str, files: tuple[Path, ...] = ()):
        self.files = files
        super().__init__(message)


class CommandStartError(Exception):
    def __init__(self, command: list[str], original: OSError):
        self.command = command
        self.original = original
        super().__init__(
            f"Could not start command; confirm its executable and target prerequisites are available. {original}"
        )


class RunnerError(Exception):
    def __init__(
        self,
        target: str,
        repair: str,
        original: Exception | None = None,
        *,
        recheck: str = "",
        exit_code: int | None = None,
    ):
        self.target = target
        self.repair = repair
        self.original = original
        self.recheck = recheck
        if exit_code is not None:
            self.exit_code = exit_code
        elif isinstance(original, subprocess.CalledProcessError):
            self.exit_code = original.returncode or 1
        elif isinstance(original, ValidationFailure):
            self.exit_code = 1
        else:
            self.exit_code = 2
        detail = f"\n{original}" if original is not None else ""
        commands = f"\nRepair: {repair}" if repair else ""
        if recheck:
            commands += f"\nRecheck: {recheck}"
        super().__init__(f"[tools/run] check '{target}' failed.{detail}{commands}")


def _render_command(argv: list[str]) -> str:
    if os.name == "nt":

        def quote(value: str) -> str:
            return "'" + value.replace("'", "''") + "'"

        return "& " + " ".join(quote(part) for part in argv)
    return shlex.join(argv)


def _command_for(target: str, mode: str, ctx: Ctx) -> str:
    command = (["py", "-3"] if os.name == "nt" else ["python3"]) + ["tools/run.py", target, f"--{mode}"]
    if ctx.files:
        command.extend(["--files", *(str(path) for path in ctx.files)])
    return _render_command(command)


def _recheck_command(target: str, ctx: Ctx) -> str:
    return _command_for(target, "check", ctx)


def _run(cmd: list[str], ctx: Ctx, *, env: dict[str, str] | None = None) -> None:
    if ctx.verbose:
        print("+ " + " ".join(shlex.quote(part) for part in cmd))
    try:
        subprocess.run(cmd, cwd=ROOT, check=True, env=env)
    except OSError as exc:
        raise CommandStartError(cmd, exc) from exc


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
    return [path for path in _candidate_paths(base_ref) if path.suffix == ".py"]


def _git_paths(args: list[str]) -> list[Path]:
    result = subprocess.run(["git", *args, "-z"], cwd=ROOT, capture_output=True, check=True)
    return [Path(os.fsdecode(path)) for path in result.stdout.split(b"\0") if path]


def _candidate_paths(base_ref: str | None) -> list[Path]:
    paths: set[Path] = set()
    staged_snapshot = os.environ.get("REPO_STANDARDS_STAGED_SNAPSHOT") == "1"
    if base_ref is not None:
        paths.update(_git_paths(["diff", "--name-only", "--diff-filter=ACMR", f"{base_ref}...HEAD"]))
    paths.update(_git_paths(["diff", "--cached", "--name-only", "--diff-filter=ACMR"]))
    if not staged_snapshot:
        paths.update(_git_paths(["diff", "--name-only", "--diff-filter=ACMR"]))
    return sorted((path for path in paths if (ROOT / path).is_file()), key=lambda path: str(path))


def _all_tracked_python_files() -> list[Path]:
    result = subprocess.run(["git", "ls-files", "-z", "--", "*.py"], cwd=ROOT, capture_output=True, check=True)
    return [Path(os.fsdecode(p)) for p in result.stdout.split(b"\0") if p and (ROOT / os.fsdecode(p)).is_file()]


def _validated_files(paths: tuple[Path, ...], *, text_only: bool = False) -> tuple[Path, ...]:
    result: list[Path] = []
    for path in paths:
        candidate = (ROOT / path).resolve() if not path.is_absolute() else path.resolve()
        try:
            relative = candidate.relative_to(ROOT.resolve())
        except ValueError as exc:
            raise ValueError(f"selected path is outside the repository: {path}") from exc
        if not candidate.is_file():
            raise ValueError(f"selected path is not a file: {path}")
        if text_only:
            data = candidate.read_bytes()
            if b"\0" in data:
                raise ValueError(f"selected path is binary and cannot be normalized: {relative}")
            try:
                data.decode("utf-8")
            except UnicodeDecodeError as exc:
                raise ValueError(f"selected path is not UTF-8 text: {relative}") from exc
        result.append(relative)
    return tuple(dict.fromkeys(result))


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


def _prune_stale_plugin_roots() -> None:
    active_names = _load_active_plugin_root_names()
    for child in sorted(PLUGIN_ROOTS_PATH.iterdir(), key=lambda path: path.name):
        if not child.is_dir() or child.name in active_names:
            continue
        if not (child / ".codex-plugin" / "plugin.json").is_file():
            continue
        shutil.rmtree(child)
        print(f"Pruned stale plugin root {child.relative_to(ROOT)}")


def _retained_verbatim_paths() -> set[str]:
    return set()


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
    _run([sys.executable, "tools/generate_plugin_root_inventory.py", "--apply"], ctx)
    _prune_stale_plugin_roots()
    _validate_marketplace_phase_step("inventory", ctx)


def _check_inventory(ctx: Ctx) -> None:
    _run([sys.executable, "tools/generate_plugin_root_inventory.py", "--check"], ctx)
    _validate_marketplace_phase_step("inventory", ctx)


def _run_validate(ctx: Ctx) -> None:
    _run([sys.executable, "tools/validate_authority_assets.py"], ctx)
    _run([sys.executable, "tools/validate_agents_md.py"], ctx)
    _run([sys.executable, "tools/validate_markdown_links.py", "--check"], ctx)
    _run([sys.executable, "tools/validate_tool_cli.py"], ctx)
    if ctx.mode == "check":
        _git_diff_check(ctx)


def _tracked_line_ending_offenders(paths: tuple[Path, ...] | None = None) -> list[Path]:
    command = ["git", "ls-files", "--eol", "-z"]
    if paths is not None:
        command.extend(["--", *(str(path) for path in paths)])
    result = subprocess.run(
        command,
        cwd=ROOT,
        capture_output=True,
        check=True,
    )
    selected = set(paths or ())
    offenders: list[Path] = []
    for entry in result.stdout.split(b"\0"):
        if not entry:
            continue
        state, path = entry.split(b"\t", maxsplit=1)
        relative = Path(os.fsdecode(path))
        if selected and relative not in selected:
            continue
        if b"eol=lf" not in state:
            continue
        if any(marker in state for marker in (b"i/crlf", b"i/mixed", b"w/crlf", b"w/mixed")):
            offenders.append(relative)
    return offenders


def _check_tracked_line_endings() -> None:
    """Catch text bytes that Git would silently normalize when committing."""
    offenders = _tracked_line_ending_offenders()
    if offenders:
        raise ValueError("tracked text must use LF line endings: " + ", ".join(map(str, offenders)))
    print("OK tracked text line endings: LF")


def _apply_marketplace(ctx: Ctx) -> None:
    _run([sys.executable, "tools/build_marketplace.py", "--apply"], ctx)
    _run([sys.executable, "tools/generate_marketplace.py", "--apply"], ctx)
    _run([sys.executable, "tools/validate_marketplace.py", "--phase", "all"], ctx)
    _run([sys.executable, "tools/deploy_vendor_profiles.py", "--apply"], ctx)


def _check_marketplace(ctx: Ctx) -> None:
    _run([sys.executable, "tools/build_marketplace.py", "--check"], ctx)
    _run([sys.executable, "tools/generate_marketplace.py", "--check"], ctx)
    _run([sys.executable, "tools/validate_marketplace.py", "--phase", "all"], ctx)


def _run_lint(ctx: Ctx) -> None:
    if ctx.files:
        files = [path for path in ctx.files if path.suffix == ".py"]
        if not files:
            print("No selected Python files to lint.")
            return
        command = [sys.executable, "-m", "ruff", "check"]
        if ctx.mode == "apply":
            command.append("--fix")
        _run([*command, *map(str, files)], ctx)
        return
    files = _changed_python_files(ctx.base_ref)
    if ctx.mode == "check" and not ctx.base_ref and os.environ.get("REPO_STANDARDS_STAGED_SNAPSHOT") != "1":
        files = _all_tracked_python_files()
    if not files:
        print("No changed Python files to lint.")
    elif ctx.mode == "check":
        if ctx.base_ref:
            _run([sys.executable, "tools/ruff_diff.py", "--changed-from", ctx.base_ref], ctx)
        else:
            _run([sys.executable, "-m", "ruff", "check", *map(str, files)], ctx)
    else:
        _run([sys.executable, "-m", "ruff", "check", "--fix", *map(str, files)], ctx)


def _run_format(ctx: Ctx) -> None:
    files = list(ctx.files) if ctx.files else _changed_python_files(ctx.base_ref)
    if not files:
        print("No changed Python files to format.")
        return
    command = [sys.executable, "-m", "ruff", "format"]
    if ctx.mode == "check":
        command.append("--check")
    _run([*command, *map(str, files)], ctx)


def _tracked_paths() -> list[Path]:
    result = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT, capture_output=True, check=True)
    return [Path(os.fsdecode(path)) for path in result.stdout.split(b"\0") if path]


def _normalize_text_files(ctx: Ctx) -> None:
    selected = _validated_files(ctx.files, text_only=True) if ctx.files else tuple(_tracked_paths())
    offenders = (
        [path for path in selected if b"\r" in (ROOT / path).read_bytes()]
        if ctx.files
        else _tracked_line_ending_offenders()
    )
    for path in offenders:
        absolute = ROOT / path
        data = absolute.read_bytes()
        data.decode("utf-8")
        if ctx.mode == "apply":
            absolute.write_bytes(data.replace(b"\r\n", b"\n").replace(b"\r", b"\n"))
    if offenders and ctx.mode == "check":
        rendered = ", ".join(str(path) for path in offenders)
        raise ValidationFailure(f"CRLF or bare CR line endings found: {rendered}", tuple(offenders))


def _run_normalize(ctx: Ctx) -> None:
    _normalize_text_files(ctx)


def _validate_skill_scripts(ctx: Ctx) -> None:
    _run(
        [
            sys.executable,
            "tools/validate_skill_scripts.py",
            "--root",
            "skills",
            "--check",
        ],
        ctx,
    )


def _run_repo_standards(ctx: Ctx) -> None:
    _run([sys.executable, "tools/check_agent_standards.py", "--check"], ctx)
    if ctx.mode == "check":
        _validate_skill_scripts(ctx)


def _check_review_preflight(ctx: Ctx) -> None:
    cmd = [sys.executable, "tools/review_preflight.py", "--check"]
    if ctx.base_ref:
        cmd.extend(["--base-ref", ctx.base_ref])
    _run(cmd, ctx)


def _apply_runtime_agents(ctx: Ctx) -> None:
    _run([sys.executable, "tools/sync_runtime_agents.py", "--apply"], ctx)


def _check_runtime_agents(ctx: Ctx) -> None:
    _run([sys.executable, "tools/sync_runtime_agents.py", "--check"], ctx)


def _run_steps(
    target: str,
    task: Task,
    steps: tuple[Callable[[Ctx], None], ...],
    run_ctx: Ctx,
) -> None:
    if not steps:
        return
    print(f"[tools/run] === {target} ({run_ctx.mode})")
    for step in steps:
        try:
            step(run_ctx)
        except RunnerError:
            raise
        except Exception as exc:
            repair_ctx = run_ctx
            if isinstance(exc, ValidationFailure) and exc.files and not run_ctx.files:
                repair_ctx = dataclass_replace(run_ctx, files=exc.files)
            if target in {"lint", "format", "normalize"}:
                repair = _command_for(target, "apply", repair_ctx)
            elif task.apply:
                repair = _command_for(target, "apply", repair_ctx)
            else:
                repair = f"No automatic repair is available for {target}; review the reported failure."
            recheck = _recheck_command(target, repair_ctx)
            failed_command = ""
            if isinstance(exc, subprocess.CalledProcessError):
                failed_command = (
                    f"\nFailed command: {_render_command([str(part) for part in exc.cmd])} (exit {exc.returncode})"
                )
            elif isinstance(exc, CommandStartError):
                failed_command = f"\nFailed command: {_render_command(exc.command)}"
            wrapped = RunnerError(target, repair, exc, recheck=recheck)
            if failed_command:
                wrapped.args = (str(wrapped) + failed_command,)
            raise wrapped from exc


def _resolve_ci_deps() -> list[str]:
    # The `ci` meta-target uses the same dependency set but resolves them
    # through the normal DAG so transitive dependencies are included.
    return resolve_targets(list(_TASKS["ci"].deps))


def _run_ci(ctx: Ctx) -> None:
    """Run the `ci` meta-target.

    In `--apply` mode each dependency is run in apply mode only.
    In `--check` mode each dependency is run in check mode; with `--diagnostics`
    every failing target is collected and reported before the command exits.
    """
    deps = _resolve_ci_deps()
    if ctx.mode == "apply":
        for target in deps:
            task = _TASKS[target]
            _run_steps(target, task, task.apply, Ctx("apply", ctx.base_ref, ctx.verbose, False))
        return
    failures: list[RunnerError] = []
    for target in deps:
        task = _TASKS[target]
        try:
            _run_steps(
                target,
                task,
                task.check,
                Ctx("check", ctx.base_ref, ctx.verbose, ctx.diagnostics),
            )
        except RunnerError as exc:
            if ctx.diagnostics:
                failures.append(exc)
            else:
                raise
    if failures:
        fixes = "\n".join(f"  {exc.target}: {exc.repair}\n  Recheck: {exc.recheck}" for exc in failures)
        raise RunnerError(
            "ci",
            f"one or more ci checks failed\n{fixes}",
            exit_code=failures[0].exit_code,
        )


def _run_python_tests(ctx: Ctx, suite: str) -> None:
    test_env = os.environ.copy()
    test_env.pop("REPO_STANDARDS_STAGED_SNAPSHOT", None)
    test_env.pop("REPO_STANDARDS_HOSTED_COMMIT", None)
    _run([sys.executable, "-m", "pytest", "-q", f"tests/{suite}"], ctx, env=test_env)


def _run_build_tests(ctx: Ctx) -> None:
    _run_python_tests(ctx, "build")


def _run_repository_tests(ctx: Ctx) -> None:
    _run_python_tests(ctx, "repository")


def _run_shipping_tests(ctx: Ctx) -> None:
    _run_python_tests(ctx, "shipping")


_TASKS: dict[str, Task] = {
    "normalize": Task(
        check=(_run_normalize,),
        apply=(_run_normalize,),
        description="Check or normalize tracked text line endings.",
        side_effects="Apply rewrites selected UTF-8 text line endings; check preserves maintained files.",
    ),
    "lint": Task(
        apply=(_run_lint,),
        check=(_run_lint,),
        description="Check changed Python lines or apply Ruff lint fixes.",
        side_effects="Apply may rewrite selected Python files.",
    ),
    "format": Task(
        apply=(_run_format,),
        check=(_run_format,),
        description="Check or apply Ruff formatting to changed Python files.",
        side_effects="Apply may rewrite selected Python files.",
    ),
    "validate": Task(
        check=(_run_validate,),
        description="Run repository authority, documentation, and CLI validators.",
        side_effects="Check preserves maintained repository files.",
    ),
    "repo-standards": Task(
        check=(_run_repo_standards,),
        description="Validate adopted repository operating standards and skill scripts.",
        side_effects="Check preserves maintained repository files.",
    ),
    "tests-build": Task(
        check=(_run_build_tests,),
        description="Run build-focused tests.",
        prerequisites=("Python test dependencies are installed.",),
        side_effects="May create disposable ignored test outputs.",
    ),
    "tests-repository": Task(
        check=(_run_repository_tests,),
        description="Run repository behavior tests.",
        prerequisites=("Python test dependencies are installed.",),
        side_effects="May create disposable ignored test outputs.",
    ),
    "tests-shipping": Task(
        check=(_run_shipping_tests,),
        description="Run packaged asset tests.",
        prerequisites=("Python test dependencies are installed.",),
        side_effects="May create disposable ignored test outputs.",
    ),
    "inventory": Task(
        apply=(_apply_inventory,),
        check=(_check_inventory,),
        description="Regenerate and validate the plugin-root inventory.",
        side_effects="Apply updates generated inventory and prunes stale generated plugin roots.",
    ),
    "marketplace": Task(
        deps=("inventory",),
        apply=(_apply_marketplace,),
        check=(_check_marketplace,),
        description="Build, generate, and validate Marketplace distributions.",
        prerequisites=("Marketplace build dependencies are installed.",),
        side_effects="Apply regenerates Marketplace distribution and vendor profile outputs.",
    ),
    "review-preflight": Task(
        check=(_check_review_preflight,),
        description="Check review readiness and required evidence.",
        side_effects="Check preserves maintained repository files.",
    ),
    # runtime-agents is intentionally excluded from `ci`; it stages profiles
    # into the main checkout for the local runtime.
    "runtime-agents": Task(
        apply=(_apply_runtime_agents,),
        check=(_check_runtime_agents,),
        description="Synchronize repository profiles into the local agent runtime.",
        side_effects="Apply writes local runtime profile files.",
    ),
    "ci": Task(
        deps=(
            "normalize",
            "lint",
            "format",
            "validate",
            "repo-standards",
            "inventory",
            "marketplace",
            "tests-build",
            "tests-repository",
            "tests-shipping",
        ),
        apply=(_run_ci,),
        check=(_run_ci,),
        description="Run the complete fail-fast repository gate in cheap-first order.",
        prerequisites=("Declared repository gate prerequisites are installed.",),
        side_effects="Check may create disposable ignored build/test outputs; apply runs mutative target operations.",
    ),
    "all": Task(
        check=(_run_ci,),
        apply=(_run_ci,),
        deps=("ci",),
        description="Alias for the complete CI gate.",
        side_effects="Same as ci.",
    ),
}


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
        # `ci` is a meta-target; it resolves and runs its own dependencies.
        if name != "ci":
            for dep in _TASKS[name].deps:
                visit(dep)
        visiting.remove(name)
        seen.add(name)
        order.append(name)

    for name in requested:
        visit(name)

    return order


def _supported_modes(task: Task) -> tuple[str, ...]:
    return tuple(mode for mode, steps in (("check", task.check), ("apply", task.apply)) if steps)


def _print_target_help(target: str) -> int:
    task = _TASKS[target]
    print(f"Target: {target}\n{task.description or 'Repository-owned task.'}")
    print("Supported modes: " + (", ".join(f"--{mode}" for mode in _supported_modes(task)) or "none"))
    print("Prerequisites: " + (" ".join(task.prerequisites) if task.prerequisites else "none"))
    print("Side effects: " + (task.side_effects or "none declared"))
    if target in {"lint", "format", "normalize"}:
        print("Arguments: --files PATH [PATH ...] scopes work to repository files; paths with spaces are supported.")
    return 0


def _validate_invocation(targets: list[str], ctx: Ctx, *, diagnostics: bool) -> Ctx:
    scoped_targets = {"lint", "format", "normalize"}
    if ctx.files and any(target not in scoped_targets for target in targets):
        raise ValueError("--files is supported only by lint, format, and normalize")
    for target in targets:
        task = _TASKS[target]
        if ctx.mode not in _supported_modes(task):
            supported = ", ".join(f"--{mode}" for mode in _supported_modes(task)) or "none"
            raise ValueError(f"target {target} does not support --{ctx.mode}; supported: {supported}")
    if diagnostics and (ctx.mode != "check" or targets != ["ci"]):
        raise ValueError("--diagnostics is accepted only with ci/all --check")
    if ctx.files:
        files = _validated_files(ctx.files, text_only=False)
        if any(path.suffix != ".py" for path in files if "normalize" not in targets):
            raise ValueError("lint and format --files selections must be Python files")
        if "normalize" in targets:
            _validated_files(files, text_only=True)
        ctx = dataclass_replace(ctx, files=files)
    return ctx


def run_targets(targets: list[str], ctx: Ctx) -> None:
    ctx = _validate_invocation(targets, ctx, diagnostics=ctx.diagnostics)
    for target in targets:
        task = _TASKS[target]
        if ctx.mode == "apply":
            _run_steps(target, task, task.apply, ctx)
        else:
            _run_steps(target, task, task.check, ctx)


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Repository command bus. Checks may create disposable ignored build/test outputs "
            "while preserving maintained files."
        ),
        epilog=(
            "Targets: " + ", ".join(_TASKS.keys()) + "\n"
            "ci --check is the full fail-fast gate in cheap-first order.\n"
            "ci --check --diagnostics explicitly collects independent failures.\n"
            "Use explicit apply targets for preparation and maintained-file repairs.\n"
            "For a single target, run `py -3 tools/run.py <target> --check` or `--apply` when supported."
        ),
    )
    parser.add_argument(
        "targets",
        nargs="*",
        choices=tuple(_TASKS.keys()),
        help="target(s) to run; omit targets to discover available commands",
    )
    parser.add_argument("--check", action="store_true", help="run candidate-preserving checks")
    parser.add_argument("--apply", action="store_true", help="run documented mutative operations")
    parser.add_argument("--files", nargs="+", type=Path, help="scope lint, format, or normalize to selected paths")
    parser.add_argument(
        "--base-ref",
        default=None,
        help="base ref for changed-line linting (default: origin/main)",
    )
    parser.add_argument(
        "--diagnostics",
        action="store_true",
        help="collect all independent check failures before rejecting (ci --check only)",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="print each sub-command before executing it",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    arguments = list(sys.argv[1:] if argv is None else argv)
    if len(arguments) == 2 and arguments[0] in _TASKS and arguments[1] == "--help":
        return _print_target_help(arguments[0])
    args = _parse_args(arguments)
    if not args.targets:
        if args.check or args.apply or args.files or args.diagnostics:
            print("error: select a target with an explicit mode", file=sys.stderr)
            return 2
        print("Available targets: " + ", ".join(_TASKS))
        print("Use tools/run.py <target> --help for target details.")
        return 0
    if not args.check and not args.apply:
        print("error: selected targets require an explicit --check, --apply, or --help mode", file=sys.stderr)
        return 2
    if args.apply and args.check:
        print("error: --apply and --check are mutually exclusive", file=sys.stderr)
        return 2
    if args.diagnostics and args.apply:
        print("error: --diagnostics requires --check", file=sys.stderr)
        return 2
    ctx = Ctx(
        mode="apply" if args.apply else "check",
        base_ref=None,
        verbose=args.verbose,
        diagnostics=args.diagnostics,
        files=tuple(args.files or ()),
    )
    try:
        targets = resolve_targets(args.targets)
        ctx = _validate_invocation(targets, ctx, diagnostics=args.diagnostics)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    ctx = dataclass_replace(ctx, base_ref=_resolve_base_ref(args))
    try:
        run_targets(targets, ctx)
    except RunnerError as exc:
        print(exc, file=sys.stderr)
        return exc.exit_code
    print("[tools/run] all requested targets passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
