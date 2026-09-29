from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
VALIDATOR = ROOT / "skills" / "repo-shape" / "scripts" / "validate_skill_scripts.py"


def test_validator_checks_an_explicit_canonical_skill_root(tmp_path: Path) -> None:
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    script = tmp_path / "skills" / "example" / "scripts" / "check.py"
    script.parent.mkdir(parents=True)
    script.write_text(
        '"""Example read-only command."""\n'
        "import argparse\n\n"
        "def main():\n"
        '    parser = argparse.ArgumentParser(description="Example (read-only)")\n'
        '    parser.add_argument("--check", action="store_true")\n'
        "    parser.parse_args()\n"
        "    return 0\n\n"
        'if __name__ == "__main__":\n'
        "    raise SystemExit(main())\n",
        encoding="utf-8",
    )

    result = subprocess.run(
        [sys.executable, str(VALIDATOR), "--root", "skills", "--check"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "skills/example/scripts/check.py" in result.stdout
    assert "CLI OK: 1" in result.stdout
