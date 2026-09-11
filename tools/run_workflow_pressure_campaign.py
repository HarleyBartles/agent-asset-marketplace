#!/usr/bin/env python3
"""Run isolated, observable Codex pressure trials for MARK-373 (mixed)."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import time
from typing import Any, Callable


MODEL_MATRIX = {
    "luna": "gpt-5.6-luna",
    "terra": "gpt-5.6-terra",
    "sol": "gpt-5.6-sol",
    "astra": "gpt-6-astra",
}
ALLOWED_SANDBOXES = {"read-only", "workspace-write"}
REQUIRED_CAPABILITIES = {
    "exec",
    "--ephemeral",
    "--json",
    "--model",
    "--sandbox",
    "--output-last-message",
    "--ignore-user-config",
    "-c",
}
PROJECT_CONFIG_PATHS = (
    Path(".codex") / "config.toml",
    Path(".codex") / "config.json",
    Path(".codex") / "mcp.json",
    Path(".mcp.json"),
)
EXTERNAL_SURFACE_COMMANDS = (
    ("mcp", "list"),
    ("plugin", "list"),
)
EXTERNAL_WRITE_MARKERS = re.compile(r"(?i)(?:mcp|connector|github|linear|external|\bpush\b|dispatch|write)")
MODEL_UNAVAILABLE_MARKERS = (
    "not available",
    "unavailable",
    "unsupported model",
    "unknown model",
    "model not found",
    "does not exist",
    "do not have access",
    "don't have access",
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def classify_trial_availability(requested_model: str, returncode: int, stdout: str, stderr: str) -> str:
    """Classify only explicit requested-model absence as model-unavailable."""
    if returncode == 0:
        return "ok"
    combined = f"{stdout}\n{stderr}".lower()
    model = requested_model.lower()
    if model in combined and any(marker in combined for marker in MODEL_UNAVAILABLE_MARKERS):
        return "model-unavailable"
    return "trial-error"


def sanitize_argv(argv: list[str], worktree: Path, run_dir: Path) -> list[str]:
    """Remove machine-local trial paths while preserving the exact invocation shape."""
    worktree_value = str(worktree)
    final_value = str((run_dir / "final.txt").resolve())
    return [
        "<worktree>" if item == worktree_value else "<run-dir>/final.txt" if item == final_value else item
        for item in argv
    ]


def _current_head() -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return result.stdout.strip()


def build_codex_argv(worktree: Path, model: str, sandbox: str, final_path: Path) -> list[str]:
    if sandbox not in ALLOWED_SANDBOXES:
        raise ValueError(f"unsupported campaign sandbox: {sandbox}")
    return [
        "codex",
        "exec",
        "-C",
        str(worktree),
        "--ephemeral",
        "--json",
        "--ignore-user-config",
        "--model",
        model,
        "-c",
        'model_reasoning_effort="medium"',
        "-c",
        "hide_agent_reasoning=true",
        "-c",
        'web_search="disabled"',
        "-c",
        "features.apps=false",
        "--sandbox",
        sandbox,
        "--output-last-message",
        str(final_path.resolve()),
        "-",
    ]


def validate_campaign(campaign: dict[str, Any]) -> None:
    if campaign.get("schema_version") != 1:
        raise ValueError("campaign schema_version must be 1")
    if campaign.get("model_matrix") != MODEL_MATRIX:
        raise ValueError("campaign model matrix does not match the fixed baseline")
    scenarios = campaign.get("scenarios")
    if not isinstance(scenarios, list) or not scenarios:
        raise ValueError("campaign must contain scenarios")
    for scenario in scenarios:
        if scenario.get("sandbox") not in ALLOWED_SANDBOXES:
            raise ValueError(f"scenario has forbidden sandbox: {scenario.get('id')}")
        if scenario.get("external_effect") != "none":
            raise ValueError(f"scenario permits external effect: {scenario.get('id')}")
        if not scenario.get("rubric"):
            raise ValueError(f"scenario has no rubric: {scenario.get('id')}")


def extract_mechanical_metrics(
    events_jsonl: str, final_text: str, elapsed_ms: int | str = "unobservable"
) -> dict[str, int | str]:
    events = []
    for line in events_jsonl.splitlines():
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return {
        "question_count": sum(1 for line in final_text.splitlines() if "?" in line),
        "tool_call_count": sum(1 for event in events if event.get("type") in {"tool_call", "function_call"}),
        "verification_count": sum(
            1
            for event in events
            if "test" in json.dumps(event, sort_keys=True).lower()
            or "verify" in json.dumps(event, sort_keys=True).lower()
        ),
        "reads_before_useful_action": "unobservable",
        "elapsed_ms": elapsed_ms,
    }


def inspect_project_config(worktree: Path) -> dict[str, Any]:
    present: list[str] = []
    external_write_surfaces: list[str] = []
    for relative_path in PROJECT_CONFIG_PATHS:
        path = worktree / relative_path
        if not path.is_file():
            continue
        present.append(relative_path.as_posix())
        text = path.read_text(encoding="utf-8", errors="replace")
        if EXTERNAL_WRITE_MARKERS.search(text):
            external_write_surfaces.append(relative_path.as_posix())
    return {
        "project_config_paths": present,
        "external_write_surfaces": external_write_surfaces,
    }


def inspect_external_tool_surfaces(
    executable: str,
    run: Callable[..., subprocess.CompletedProcess[str]],
) -> dict[str, Any]:
    inventory: dict[str, Any] = {}
    for command in EXTERNAL_SURFACE_COMMANDS:
        help_result = run(
            [executable, *command, "--help"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        help_text = (help_result.stdout or "") + (help_result.stderr or "")
        if help_result.returncode != 0 or "--json" not in help_text:
            return {
                "status": "harness-blocked",
                "reason": "effective MCP/plugin tool inventory is unavailable",
                "inventory": inventory,
                "inventory_command": list(command),
            }
        result = run(
            [executable, *command, "--json"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        output = (result.stdout or "") + (result.stderr or "")
        record = {
            "command": list(command),
            "exit_code": result.returncode,
            "output_sha256": sha256_text(output),
        }
        if result.returncode != 0:
            return {
                "status": "harness-blocked",
                "reason": "effective MCP/plugin tool inventory failed",
                "inventory": {**inventory, command[0]: record},
            }
        try:
            payload = json.loads(result.stdout or "null")
        except json.JSONDecodeError:
            return {
                "status": "harness-blocked",
                "reason": "effective MCP/plugin tool inventory was not valid JSON",
                "inventory": {**inventory, command[0]: record},
            }
        exposed = bool(payload)
        record["exposed"] = exposed
        inventory[command[0]] = record
        if exposed:
            return {
                "status": "harness-blocked",
                "reason": "effective MCP/plugin tool inventory is not empty",
                "inventory": inventory,
            }
    return {"status": "inventory-clear", "inventory": inventory}


def preflight(
    resolve: Callable[[str], str | None] = shutil.which,
    run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    worktree: Path | None = None,
) -> dict[str, Any]:
    executable = resolve("codex")
    if not executable:
        return {"status": "harness-unavailable", "reason": "codex executable not found on PATH"}
    version = run(
        [executable, "--version"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    help_result = run(
        [executable, "exec", "--help"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    help_text = (help_result.stdout or "") + (help_result.stderr or "")
    missing = sorted(capability for capability in REQUIRED_CAPABILITIES if capability not in help_text)
    if version.returncode != 0 or help_result.returncode != 0 or missing:
        return {
            "status": "harness-incompatible",
            "version": (version.stdout or version.stderr).strip(),
            "missing_capabilities": missing,
        }
    smoke_worktree = worktree or Path.cwd()
    project_config = inspect_project_config(smoke_worktree)
    if project_config["external_write_surfaces"]:
        return {
            "status": "harness-blocked",
            "version": (version.stdout or version.stderr).strip(),
            "reason": "project-scoped configuration exposes external write surfaces",
            **project_config,
        }
    external_tools = inspect_external_tool_surfaces(executable, run)
    if external_tools["status"] != "inventory-clear":
        return {
            "status": external_tools["status"],
            "reason": external_tools["reason"],
            "inventory": external_tools["inventory"],
            "version": (version.stdout or version.stderr).strip(),
            **project_config,
        }
    with tempfile.TemporaryDirectory(prefix="mark-373-harness-smoke-") as smoke_dir:
        smoke_final = Path(smoke_dir) / "final.txt"
        smoke = run(
            build_codex_argv(smoke_worktree, MODEL_MATRIX["luna"], "read-only", smoke_final),
            input=(
                "MARK-373 harness smoke: perform no repository changes and respond with SMOKE_OK. "
                "Run one read-only command that prints the repository root, then respond with SMOKE_OK. "
                "Do not use connectors, web access, or publication."
            ),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=60,
        )
        smoke_text = smoke_final.read_text(encoding="utf-8", errors="replace") if smoke_final.is_file() else ""
        smoke_sha256 = sha256_file(smoke_final) if smoke_final.is_file() else None
    if smoke.returncode != 0:
        return {
            "status": "harness-blocked",
            "version": (version.stdout or version.stderr).strip(),
            "reason": "read-only smoke invocation failed",
            "smoke_exit_code": smoke.returncode,
            "smoke_stderr": (smoke.stderr or "")[-500:],
            "smoke_final_sha256": smoke_sha256,
            "inventory": external_tools["inventory"],
            **project_config,
        }
    if "SMOKE_OK" not in smoke_text:
        return {
            "status": "harness-blocked",
            "version": (version.stdout or version.stderr).strip(),
            "reason": "read-only smoke invocation did not complete expected response",
            "smoke_exit_code": smoke.returncode,
            "smoke_final_sha256": smoke_sha256,
            **external_tools,
            **project_config,
        }
    return {
        "status": "preflight-ready",
        "version": (version.stdout or version.stderr).strip(),
        "smoke_exit_code": smoke.returncode,
        "smoke_final_sha256": smoke_sha256,
        "inventory": external_tools["inventory"],
        **project_config,
    }


def preflight_at_head(
    head: str,
    preflight_fn: Callable[..., dict[str, Any]] = preflight,
    git_run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
) -> dict[str, Any]:
    """Run preflight from a clean disposable worktree at exactly ``head``."""
    worktree = Path(tempfile.mkdtemp(prefix="mark-373-preflight-"))
    added = False
    try:
        git_run(
            ["git", "worktree", "add", "--detach", str(worktree), head],
            check=True,
            capture_output=True,
            text=True,
        )
        added = True
        resolved = git_run(
            ["git", "-C", str(worktree), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        status = git_run(
            ["git", "-C", str(worktree), "status", "--porcelain"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        if resolved != head:
            return {
                "status": "harness-blocked",
                "reason": "preflight worktree resolved to a different head",
                "requested_head": head,
                "preflight_head": resolved,
            }
        if status:
            return {
                "status": "harness-blocked",
                "reason": "preflight worktree is not clean",
                "requested_head": head,
                "preflight_head": resolved,
                "preflight_worktree_status": status,
            }
        result = preflight_fn(worktree=worktree)
        return {
            **result,
            "requested_head": head,
            "preflight_head": resolved,
            "preflight_worktree_status": "clean",
        }
    except (OSError, subprocess.CalledProcessError) as error:
        return {
            "status": "harness-blocked",
            "reason": "could not materialize immutable preflight worktree",
            "requested_head": head,
            "details": str(error),
        }
    except Exception as error:  # fail closed if a runtime integration is malformed
        return {
            "status": "harness-blocked",
            "reason": "immutable preflight raised an unexpected runtime error",
            "requested_head": head,
            "details": f"{type(error).__name__}: {error}",
        }
    finally:
        if added:
            git_run(
                ["git", "worktree", "remove", "--force", str(worktree)],
                capture_output=True,
                text=True,
            )
        if worktree.exists():
            shutil.rmtree(worktree, ignore_errors=True)


def _load_campaign(path: Path) -> dict[str, Any]:
    campaign = json.loads(path.read_text(encoding="utf-8"))
    validate_campaign(campaign)
    return campaign


def _write_trial_evidence(
    run_dir: Path,
    *,
    events_text: str,
    stderr_text: str,
    final_text: str,
    meta: dict[str, Any],
) -> None:
    events_path = run_dir / "events.jsonl"
    stderr_path = run_dir / "stderr.txt"
    final_path = run_dir / "final.txt"
    meta_path = run_dir / "meta.json"
    metrics_path = run_dir / "metrics.json"
    hashes_path = run_dir / "hashes.json"

    events_path.write_text(events_text, encoding="utf-8")
    stderr_path.write_text(stderr_text, encoding="utf-8")
    final_path.write_text(final_text, encoding="utf-8")
    metrics_path.write_text(
        json.dumps(extract_mechanical_metrics(events_text, final_text, meta["elapsed_ms"]), indent=2) + "\n",
        encoding="utf-8",
    )
    meta_path.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    hashes_path.write_text(
        json.dumps(
            {
                "events_jsonl_sha256": sha256_file(events_path),
                "stderr_sha256": sha256_file(stderr_path),
                "final_sha256": sha256_file(final_path),
                "meta_sha256": sha256_file(meta_path),
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def _run_trial(
    campaign_path: Path,
    campaign: dict[str, Any],
    head_root: Path,
    head: str,
    controlling_head: str,
    codex_version: str,
    current_family: str,
    scenario: dict[str, Any],
) -> tuple[str, bool]:
    """Run one isolated trial and always leave durable local evidence."""
    run_dir = head_root / current_family / scenario["id"]
    run_dir.mkdir(parents=True, exist_ok=True)
    worktree = Path(tempfile.mkdtemp(prefix=f"mark-373-{current_family}-"))
    added = False
    cleanup: dict[str, Any] = {"status": "not-needed"}
    error: dict[str, str] | None = None
    events_text = ""
    stderr_text = ""
    final_text = ""
    exit_code: int | None = None
    availability = "trial-error"
    sanitized_argv: list[str] = []
    started = time.time()

    try:
        add_result = subprocess.run(
            ["git", "worktree", "add", "--detach", str(worktree), head],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        if add_result.returncode != 0:
            error = {
                "kind": "worktree-add",
                "message": ((add_result.stderr or add_result.stdout) or "git worktree add failed")[-1000:],
            }
            stderr_text = add_result.stderr or add_result.stdout or ""
        else:
            added = True
            prompt = (
                campaign["prompt_prefix"]
                + "\n\n"
                + (campaign_path.parent / "prompts" / scenario["prompt"]).read_text(encoding="utf-8")
            )
            final_path = run_dir / "final.txt"
            argv = build_codex_argv(worktree, MODEL_MATRIX[current_family], scenario["sandbox"], final_path)
            sanitized_argv = sanitize_argv(argv, worktree, run_dir)
            try:
                result = subprocess.run(
                    argv,
                    input=prompt,
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                )
                exit_code = result.returncode
                events_text = result.stdout or ""
                stderr_text = result.stderr or ""
                if final_path.is_file():
                    final_text = final_path.read_text(encoding="utf-8", errors="replace")
                availability = classify_trial_availability(
                    MODEL_MATRIX[current_family], result.returncode, events_text, stderr_text
                )
            except Exception as exc:
                error = {"kind": type(exc).__name__, "message": str(exc)}
                stderr_text = f"{type(exc).__name__}: {exc}\n"
                availability = "trial-error"
    except Exception as exc:
        error = {"kind": type(exc).__name__, "message": str(exc)}
        stderr_text = f"{type(exc).__name__}: {exc}\n"
        availability = "trial-error"

    elapsed_ms = round((time.time() - started) * 1000)
    preliminary_meta = {
        "schema_version": 1,
        "scenario": scenario["id"],
        "family": current_family,
        "requested_model": MODEL_MATRIX[current_family],
        "observed_model": "unobservable",
        "requested_reasoning_effort": "medium",
        "observed_reasoning_effort": "unobservable",
        "api_reasoning_mode": "unobservable",
        "codex_version": codex_version,
        "sanitized_argv": sanitized_argv,
        "sandbox": scenario["sandbox"],
        "trial_head": head,
        "controlling_head": controlling_head,
        "started_at": started,
        "finished_at": time.time(),
        "elapsed_ms": elapsed_ms,
        "exit_code": exit_code,
        "availability": availability,
        "cleanup": {"status": "pending" if added else "not-needed"},
    }
    if error is not None:
        preliminary_meta["error"] = error

    # Preserve raw trial evidence before cleanup. Cleanup outcome is then folded
    # into the final meta and hashes without risking the trial trace itself.
    _write_trial_evidence(
        run_dir,
        events_text=events_text,
        stderr_text=stderr_text,
        final_text=final_text,
        meta=preliminary_meta,
    )

    if added:
        try:
            cleanup_result = subprocess.run(
                ["git", "worktree", "remove", "--force", str(worktree)],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
            )
            if cleanup_result.returncode == 0:
                cleanup = {"status": "ok"}
                if worktree.exists():
                    shutil.rmtree(worktree)
            else:
                cleanup = {
                    "status": "failed",
                    "exit_code": cleanup_result.returncode,
                    "details": ((cleanup_result.stderr or cleanup_result.stdout) or "cleanup failed")[-1000:],
                    "worktree_retained": worktree.exists(),
                }
        except Exception as exc:
            cleanup = {
                "status": "failed",
                "details": f"{type(exc).__name__}: {exc}",
                "worktree_retained": worktree.exists(),
            }
    elif worktree.exists():
        shutil.rmtree(worktree, ignore_errors=True)

    final_meta = {**preliminary_meta, "cleanup": cleanup}
    _write_trial_evidence(
        run_dir,
        events_text=events_text,
        stderr_text=stderr_text,
        final_text=final_text,
        meta=final_meta,
    )
    return availability, cleanup.get("status") == "failed"


def run_campaign(
    campaign_path: Path,
    output_root: Path,
    head: str,
    family: str | None = None,
    scenario_id: str | None = None,
) -> int:
    campaign = _load_campaign(campaign_path)
    if family is not None and family not in MODEL_MATRIX:
        print(f"error: unknown model family: {family}", file=sys.stderr)
        return 2
    scenarios = [s for s in campaign["scenarios"] if not scenario_id or s["id"] == scenario_id]
    if scenario_id and not scenarios:
        print(f"error: unknown campaign scenario: {scenario_id}", file=sys.stderr)
        return 2

    output_root.mkdir(parents=True, exist_ok=True)
    head_root = output_root / head
    try:
        controlling_head = _current_head()
    except (OSError, subprocess.CalledProcessError) as error:
        preflight_result = {
            "status": "harness-blocked",
            "reason": "could not resolve controlling repository head",
            "requested_head": head,
            "details": str(error),
        }
    else:
        try:
            preflight_result = preflight_at_head(head)
        except BaseException as error:  # campaign metadata must record every fail-closed preflight outcome
            preflight_result = {
                "status": "harness-blocked",
                "reason": "preflight orchestration failed",
                "requested_head": head,
                "details": f"{type(error).__name__}: {error}",
            }
    (head_root / "_harness").mkdir(parents=True, exist_ok=True)
    (head_root / "_harness" / "campaign-meta.json").write_text(
        json.dumps(
            {
                "schema_version": 1,
                "evaluation_head": head,
                "controlling_head": locals().get("controlling_head", "unobservable"),
                **preflight_result,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    if preflight_result["status"] != "preflight-ready":
        return 2

    families = [family] if family else list(MODEL_MATRIX)
    had_trial_error = False
    for current_family in families:
        for scenario in scenarios:
            availability, cleanup_failed = _run_trial(
                campaign_path,
                campaign,
                head_root,
                head,
                controlling_head,
                str(preflight_result.get("version", "unobservable")),
                current_family,
                scenario,
            )
            if availability == "trial-error" or cleanup_failed:
                had_trial_error = True
    return 2 if had_trial_error else 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Run isolated, observable Codex pressure trials for MARK-373. (mixed)")
    parser.add_argument(
        "--check",
        action="store_true",
        help="validate the CLI contract without running a campaign (read-only)",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="run the campaign and write its local evidence (mixed)",
    )
    parser.add_argument("--campaign", type=Path)
    parser.add_argument("--output-root", type=Path)
    parser.add_argument("--head")
    parser.add_argument("--family", choices=sorted(MODEL_MATRIX))
    parser.add_argument("--scenario")
    args = parser.parse_args()
    if args.check and not any((args.campaign, args.output_root, args.head)):
        print("OK pressure campaign runner: CLI contract available")
        return 0
    missing = [
        name
        for name, value in (
            ("--campaign", args.campaign),
            ("--output-root", args.output_root),
            ("--head", args.head),
        )
        if not value
    ]
    if missing:
        parser.error("missing required arguments: " + ", ".join(missing))
    return run_campaign(args.campaign, args.output_root, args.head, args.family, args.scenario)


if __name__ == "__main__":
    raise SystemExit(main())
