from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REBUILD = [sys.executable, str(ROOT / "tools" / "rebuild_marketplace.py")]
VALIDATE = [sys.executable, str(ROOT / "tools" / "validate_marketplace.py")]


def test_rebuild_cli_help_exposes_new_flags():
    result = subprocess.run(
        [*REBUILD, "--help"],
        capture_output=True,
        text=True,
        check=True,
    )
    text = result.stdout
    assert "--phase" in text, "expected --phase in help"
    assert "--check" in text, "expected --check in help"
    assert "--apply" in text, "expected --apply in help"
    assert "--allow-shared-checkout" in text, "expected --allow-shared-checkout in help"
    assert "--skip-install" in text, "expected --skip-install in help"
    assert "--verbose" in text, "expected --verbose in help"


def test_validate_marketplace_phase_cli_exists():
    result = subprocess.run(
        [*VALIDATE, "--help"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert "--phase" in result.stdout, "expected --phase in validate_marketplace.py help"
