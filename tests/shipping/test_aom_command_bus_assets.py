from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PLUGIN_SOURCE = ROOT / "dist/plugins/agent-operating-model"
SKILL_SOURCE = ROOT / "skills/command-bus"


def _run(bus: Path, cwd: Path, *args: str) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env.pop("PYTHONPATH", None)
    return subprocess.run(
        [sys.executable, str(bus), *args],
        cwd=cwd,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )


def test_optional_python_starter_works_after_copy_to_consumer_tools(tmp_path: Path) -> None:
    installed_plugin = tmp_path / "installed/agent-operating-model"
    shutil.copytree(PLUGIN_SOURCE, installed_plugin)
    consumer = tmp_path / "consumer"
    consumer_tools = consumer / "tools"
    consumer_tools.mkdir(parents=True)
    shutil.copytree(
        installed_plugin / "skills/command-bus/assets/tools",
        consumer_tools,
        dirs_exist_ok=True,
    )
    bus = consumer_tools / "run.py"

    help_result = _run(bus, consumer)
    assert help_result.returncode == 0, help_result.stderr
    assert "check_status" in help_result.stdout
    assert "apply_change" in help_result.stdout
    assert "preview_change" in help_result.stdout

    check_result = _run(bus, consumer, "check_status", "--check", "--", "two words", "--apply", "--exit-code", "7")
    assert check_result.returncode == 7
    assert '"arguments": ["two words", "--apply", "--exit-code", "7"]' in check_result.stdout

    destination = consumer / "maintained.txt"
    apply_result = _run(
        bus,
        consumer,
        "apply_change",
        "--apply",
        "--",
        "--path",
        str(destination),
        "--content",
        "consumer-owned",
    )
    assert apply_result.returncode == 0, apply_result.stderr
    assert destination.read_text(encoding="utf-8") == "consumer-owned\n"

    preview_result = _run(
        bus,
        consumer,
        "preview_change",
        "--dry-run",
        "--",
        "--path",
        str(destination),
        "--content",
        "preview-only",
    )
    assert preview_result.returncode == 0, preview_result.stderr
    assert "would update" in preview_result.stdout.lower()
    assert destination.read_text(encoding="utf-8") == "consumer-owned\n"

    assert not (installed_plugin / "skills/command-bus/tests/evaluator-only").exists()
