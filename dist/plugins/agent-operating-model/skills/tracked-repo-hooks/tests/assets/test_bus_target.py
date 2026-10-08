from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


TARGET = Path(__file__).resolve().parents[2] / "assets" / "targets" / "repository_gate.py"


def _copy_target(destination: Path) -> Path:
    copied = destination / "repository_gate.py"
    shutil.copyfile(TARGET, copied)
    return copied


def test_target_forwards_the_repo_check_command_output_and_exit_status(tmp_path: Path) -> None:
    target = _copy_target(tmp_path)
    command = tmp_path / "repo check.py"
    command.write_text(
        "import sys\nprint(repr(sys.argv[1:]))\nprint('check stderr', file=sys.stderr)\nraise SystemExit(19)\n",
        encoding="utf-8",
    )

    result = subprocess.run(
        [sys.executable, str(target), "--check", "--", sys.executable, str(command), "space arg"],
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 19
    assert result.stdout == "['space arg']\n"
    assert result.stderr == "check stderr\n"


def test_target_help_declares_check_only_support_and_no_default_operation(tmp_path: Path) -> None:
    target = _copy_target(tmp_path)
    help_result = subprocess.run([sys.executable, str(target), "--help"], text=True, capture_output=True, check=False)
    bare_result = subprocess.run([sys.executable, str(target)], text=True, capture_output=True, check=False)
    apply_result = subprocess.run(
        [sys.executable, str(target), "--apply", "--", sys.executable],
        text=True,
        capture_output=True,
        check=False,
    )

    assert help_result.returncode == 0
    assert "Supported modes: --check" in help_result.stdout
    assert "repository-owned complete candidate-preserving check command" in help_result.stdout
    assert bare_result.returncode != 0
    assert "explicit --check" in bare_result.stderr
    assert apply_result.returncode != 0
    assert "does not support --apply" in apply_result.stderr
