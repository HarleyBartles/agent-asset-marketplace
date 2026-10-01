from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[2]
BUS = SKILL_ROOT / "assets" / "tools" / "run.py"


def run_bus(*args: str) -> subprocess.CompletedProcess[str]:
    command = [sys.executable, str(BUS), *args]
    if not BUS.is_file():
        return subprocess.CompletedProcess(command, 127, "", "command bus starter is not present")
    return subprocess.run(command, cwd=SKILL_ROOT, text=True, capture_output=True, check=False)


def test_bare_invocation_lists_targets_without_running_them() -> None:
    result = run_bus()

    assert result.returncode == 0, result.stderr
    assert "check_status" in result.stdout
    assert "apply_change" in result.stdout
    assert "preview_change" in result.stdout


def test_top_level_help_lists_usage_without_running_targets() -> None:
    result = run_bus("--help")

    assert result.returncode == 0, result.stderr
    assert "usage: run.py" in result.stdout.lower()
    assert "check_status" in result.stdout


def test_target_help_describes_modes_and_side_effects_without_running_target() -> None:
    result = run_bus("apply_change", "--help")

    assert result.returncode == 0, result.stderr
    assert "--apply" in result.stdout
    assert "writes" in result.stdout.lower()
    assert "usage: apply_change.py" not in result.stdout.lower()


def test_check_target_forwards_arguments_and_returns_exact_exit_status() -> None:
    result = run_bus("check_status", "--check", "--", "two words", "--apply", "17", "--exit-code", "17")

    assert result.returncode == 17
    assert json.loads(result.stdout) == {
        "mode": "--check",
        "arguments": ["two words", "--apply", "17", "--exit-code", "17"],
    }


def test_target_stderr_and_failure_status_are_preserved() -> None:
    result = run_bus("check_status", "--check", "--", "--exit-code")

    assert result.returncode == 2
    assert "--exit-code requires an integer" in result.stderr


def test_apply_target_performs_its_documented_change(tmp_path: Path) -> None:
    destination = tmp_path / "maintained.txt"
    result = run_bus("apply_change", "--apply", "--", "--path", str(destination), "--content", "updated")

    assert result.returncode == 0, result.stderr
    assert destination.read_text(encoding="utf-8") == "updated\n"


def test_dry_run_reports_proposed_change_without_mutating(tmp_path: Path) -> None:
    destination = tmp_path / "maintained.txt"
    destination.write_text("before\n", encoding="utf-8")
    result = run_bus("preview_change", "--dry-run", "--", "--path", str(destination), "--content", "after")

    assert result.returncode == 0, result.stderr
    assert "would update" in result.stdout.lower()
    assert destination.read_text(encoding="utf-8") == "before\n"


def test_selected_target_without_mode_fails_without_running_it(tmp_path: Path) -> None:
    destination = tmp_path / "maintained.txt"
    result = run_bus("apply_change", "--", "--path", str(destination), "--content", "bad")

    assert result.returncode != 0
    assert "mode" in result.stderr.lower()
    assert "usage:" in result.stderr.lower()
    assert not destination.exists()


def test_conflicting_modes_fail_before_target_work(tmp_path: Path) -> None:
    destination = tmp_path / "maintained.txt"
    result = run_bus("apply_change", "--check", "--apply", "--", "--path", str(destination), "--content", "bad")

    assert result.returncode != 0
    assert "mode" in result.stderr.lower()
    assert not destination.exists()


def test_unknown_target_fails_before_work() -> None:
    result = run_bus("missing_target", "--check")

    assert result.returncode != 0
    assert "unknown target" in result.stderr.lower()


def test_unsupported_mode_fails_before_target_work(tmp_path: Path) -> None:
    destination = tmp_path / "maintained.txt"
    result = run_bus("check_status", "--apply", "--", "--exit-code", "0", str(destination))

    assert result.returncode != 0
    assert "does not support" in result.stderr.lower()
    assert not destination.exists()


def test_invalid_target_metadata_is_rejected_before_dispatch() -> None:
    spec = importlib.util.spec_from_file_location("command_bus_starter", BUS)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    try:
        module.validate_target(
            "bad_target",
            {
                "command": [],
                "description": "Bad sample.",
                "supported_modes": ["delete"],
                "prerequisites": [],
                "side_effects": "None.",
                "argument_help": "No arguments.",
            },
        )
    except ValueError as error:
        assert "bad_target" in str(error)
    else:
        raise AssertionError("invalid target metadata was accepted")


def test_help_and_rejected_requests_never_launch_a_target(tmp_path: Path, capsys: object) -> None:
    spec = importlib.util.spec_from_file_location("command_bus_invocation_probe", BUS)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    target = tmp_path / "record_invocation.py"
    marker = tmp_path / "launched.txt"
    target.write_text(
        f"from pathlib import Path\nPath({str(marker)!r}).write_text('started', encoding='utf-8')\n",
        encoding="utf-8",
    )
    module.TARGETS["probe"] = {
        "command": [sys.executable, str(target)],
        "description": "Records whether dispatch launched this target.",
        "supported_modes": ["check"],
        "prerequisites": [],
        "side_effects": "Writes the requested test marker.",
        "argument_help": "--marker PATH",
    }
    assert module.main(["probe", "--check"]) == 0
    assert marker.read_text(encoding="utf-8") == "started"
    marker.unlink()

    requests = (
        ("target help", ["probe", "--help"], 0),
        ("missing mode", ["probe"], 2),
        ("conflicting modes", ["probe", "--check", "--apply"], 2),
        ("unknown target", ["missing", "--check"], 2),
        ("unsupported mode", ["probe", "--apply"], 2),
    )

    for label, arguments, expected_status in requests:
        assert module.main(arguments) == expected_status, label
        assert not marker.exists(), f"{label} launched the target"
        capsys.readouterr()  # Keep each request's expected diagnostic local.

    assert module.main(["--help"]) == 0
    assert not marker.exists()
