from __future__ import annotations

import subprocess
import sys
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[2] / "assets" / "check_agents_md.py"


def check(root: Path, *options: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--repo-root", str(root), "--check", *options],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )


def _write_agents(path: Path, lines: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join("router" for _ in range(lines)) + "\n", encoding="utf-8")


def test_default_boundaries_warn_above_55_and_fail_above_100(tmp_path: Path) -> None:
    for count in (54, 55, 56, 99, 100, 101):
        _write_agents(tmp_path / f"case-{count}" / "AGENTS.md", count)

    result = check(tmp_path)

    assert result.returncode == 1
    assert "case-54/AGENTS.md: 54 lines" not in result.stdout
    assert "case-55/AGENTS.md: 55 lines" not in result.stdout
    assert "case-56/AGENTS.md: 56 lines" in result.stdout
    assert "case-99/AGENTS.md: 99 lines" in result.stdout
    assert "case-100/AGENTS.md: 100 lines" in result.stdout
    assert "case-101/AGENTS.md: 101 lines" in result.stdout
    assert "warn above 55" in result.stdout and "error above 100" in result.stdout


def test_changed_budget_and_exclusions_are_repository_selected(tmp_path: Path) -> None:
    _write_agents(tmp_path / "AGENTS.md", 2)
    _write_agents(tmp_path / "nested/AGENTS.md", 4)
    _write_agents(tmp_path / "generated/AGENTS.md", 50)

    result = check(tmp_path, "--warn-lines", "1", "--error-lines", "3", "--exclude", "generated/**")

    assert result.returncode == 1
    assert "AGENTS.md: 2 lines" in result.stdout
    assert "nested/AGENTS.md: 4 lines" in result.stdout
    assert "generated/AGENTS.md" not in result.stdout
    assert "warn above 1" in result.stdout and "error above 3" in result.stdout


def test_router_count_alone_does_not_fail_and_untracked_files_are_scanned(tmp_path: Path) -> None:
    for index in range(25):
        _write_agents(tmp_path / f"domain-{index}" / "AGENTS.md", 1)

    result = check(tmp_path)

    assert result.returncode == 0, result.stdout + result.stderr
    assert "checked 25 agents.md file(s)" in result.stdout.lower()
