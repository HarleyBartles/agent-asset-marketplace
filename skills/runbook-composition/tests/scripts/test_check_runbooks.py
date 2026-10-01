from __future__ import annotations

import subprocess
import sys
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "check_runbooks.py"


def run_checker(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--repo-root", str(root), *args, "--check"],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )


def test_accepts_minimal_stage_guide_without_prescribed_headings(tmp_path: Path) -> None:
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs/design.md").write_text(
        "Explore options, choose one, and record the decision.\n", encoding="utf-8"
    )
    (tmp_path / "AGENTS.md").write_text("For design work, read [the guide](docs/design.md).\n", encoding="utf-8")

    result = run_checker(tmp_path, "--document", "docs/design.md", "--route-source", "AGENTS.md")

    assert result.returncode == 0, result.stdout + result.stderr
    assert "semantic usefulness" in result.stdout.lower()


def test_resolves_reference_route_with_angle_bracket_target_spaces_and_parentheses(tmp_path: Path) -> None:
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs/design guide (decision).md").write_text("A lifecycle stage guide.\n", encoding="utf-8")
    (tmp_path / "AGENTS.md").write_text(
        "For design, read [the guide][design].\n\n[design]: <docs/design guide (decision).md>\n", encoding="utf-8"
    )

    result = run_checker(tmp_path, "--document", "docs/design guide (decision).md", "--route-source", "AGENTS.md")

    assert result.returncode == 0, result.stdout + result.stderr


def test_rejects_broken_local_link(tmp_path: Path) -> None:
    (tmp_path / "design.md").write_text("Consult [missing](absent.md).\n", encoding="utf-8")

    result = run_checker(tmp_path, "--document", "design.md")

    assert result.returncode == 1
    assert "absent.md" in result.stdout


def test_rejects_undefined_reference_style_link(tmp_path: Path) -> None:
    (tmp_path / "design.md").write_text(
        "- [x] Record the decision.\n\nThe [design term] needs definition.\n\nConsult [the guide][missing].\n",
        encoding="utf-8",
    )

    result = run_checker(tmp_path, "--document", "design.md")

    assert result.returncode == 1
    assert "undefined markdown reference: [missing]" in result.stdout.lower()


def test_rejects_selected_document_without_supplied_route(tmp_path: Path) -> None:
    (tmp_path / "design.md").write_text("Useful stage guidance.\n", encoding="utf-8")
    (tmp_path / "AGENTS.md").write_text("General orientation.\n", encoding="utf-8")

    result = run_checker(tmp_path, "--document", "design.md", "--route-source", "AGENTS.md")

    assert result.returncode == 1
    assert "no supplied route source links" in result.stdout.lower()


def test_rejects_missing_empty_and_empty_selection(tmp_path: Path) -> None:
    (tmp_path / "empty.md").write_text("  \n", encoding="utf-8")

    missing = run_checker(tmp_path, "--document", "missing.md")
    empty = run_checker(tmp_path, "--document", "empty.md")
    no_selection = run_checker(tmp_path)

    assert missing.returncode == 1 and "missing.md" in missing.stdout
    assert empty.returncode == 1 and "empty" in empty.stdout.lower()
    assert no_selection.returncode == 1 and "at least one --document" in no_selection.stdout
