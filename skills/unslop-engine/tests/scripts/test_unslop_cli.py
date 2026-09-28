from __future__ import annotations

import subprocess
import sys
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "unslop.py"


def _run(*arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, str(SCRIPT), *arguments], capture_output=True, text=True, check=False)


def test_default_check_does_not_create_output(tmp_path: Path) -> None:
    output = tmp_path / "unslop-output"
    result = _run("--domain", "fixture-domain", "--fixture-samples", "--output", str(output))

    assert result.returncode == 0, result.stderr
    assert not output.exists()


def test_apply_creates_output(tmp_path: Path) -> None:
    output = tmp_path / "unslop-output"
    result = _run("--apply", "--domain", "fixture-domain", "--fixture-samples", "--output", str(output))

    assert result.returncode == 0, result.stderr
    assert (output / "manifest.json").is_file()
