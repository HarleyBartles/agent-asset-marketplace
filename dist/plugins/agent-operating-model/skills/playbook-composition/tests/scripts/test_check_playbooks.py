from __future__ import annotations

import subprocess
import sys
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "check_playbooks.py"


def run_checker(root: Path, *args: str, include_check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--repo-root", str(root), *args] + (["--check"] if include_check else []),
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )


def test_accepts_standalone_concern_guide_without_fixed_headings(tmp_path: Path) -> None:
    (tmp_path / "security.md").write_text(
        "Review trust boundaries, minimize exposed data, and record any accepted risk.\n", encoding="utf-8"
    )
    (tmp_path / "AGENTS.md").write_text(
        "For security-sensitive changes, read [security](security.md).\n", encoding="utf-8"
    )

    result = run_checker(tmp_path, "--document", "security.md", "--route-source", "AGENTS.md")

    assert result.returncode == 0, result.stdout + result.stderr
    assert "semantic usefulness" in result.stdout.lower()


def test_check_mode_is_default_when_flag_is_omitted(tmp_path: Path) -> None:
    (tmp_path / "security.md").write_text("A cross-stage concern guide.\n", encoding="utf-8")

    result = run_checker(tmp_path, "--document", "security.md", include_check=False)

    assert result.returncode == 0, result.stdout + result.stderr


def test_resolves_angle_bracket_route_with_parenthesized_target(tmp_path: Path) -> None:
    (tmp_path / "security (concern).md").write_text("A cross-stage concern guide.\n", encoding="utf-8")
    (tmp_path / "AGENTS.md").write_text(
        "For security concerns, read [security](<security (concern).md>).\n", encoding="utf-8"
    )

    result = run_checker(tmp_path, "--document", "security (concern).md", "--route-source", "AGENTS.md")

    assert result.returncode == 0, result.stdout + result.stderr


def test_rejects_broken_local_link(tmp_path: Path) -> None:
    (tmp_path / "testing.md").write_text("See [policy](missing.md).\n", encoding="utf-8")

    result = run_checker(tmp_path, "--document", "testing.md")

    assert result.returncode == 1
    assert "missing.md" in result.stdout


def test_rejects_undefined_reference_style_link(tmp_path: Path) -> None:
    (tmp_path / "testing.md").write_text(
        "- [x] Run checks.\n\nThe [testing term] is local.\n\nSee [policy][missing] and ![diagram][image-missing].\n",
        encoding="utf-8",
    )

    result = run_checker(tmp_path, "--document", "testing.md")

    assert result.returncode == 1
    assert "undefined markdown reference: [missing]" in result.stdout.lower()
    assert "undefined markdown reference: [image-missing]" in result.stdout.lower()


def test_ignores_link_shaped_text_inside_fenced_markdown_examples(tmp_path: Path) -> None:
    (tmp_path / "testing.md").write_text(
        "A cross-stage concern guide.\n\n`[inline example](missing.md)`\n\n"
        "~~~markdown\n[example](missing.md)\n![example][missing]\n~~~\n",
        encoding="utf-8",
    )

    result = run_checker(tmp_path, "--document", "testing.md")

    assert result.returncode == 0, result.stdout + result.stderr


def test_rejects_document_missing_from_route_and_bad_route_source(tmp_path: Path) -> None:
    (tmp_path / "testing.md").write_text("Run tests before publication.\n", encoding="utf-8")
    (tmp_path / "AGENTS.md").write_text("Repository orientation.\n", encoding="utf-8")

    result = run_checker(
        tmp_path, "--document", "testing.md", "--route-source", "AGENTS.md", "--route-source", "absent.md"
    )

    assert result.returncode == 1
    assert "testing.md" in result.stdout and "absent.md" in result.stdout


def test_selected_concern_can_route_from_one_stage_without_all_to_all_links(tmp_path: Path) -> None:
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs/design.md").write_text(
        "Shape the solution and use [testing guidance](testing.md) when evidence is needed.\n", encoding="utf-8"
    )
    (tmp_path / "docs/implementation.md").write_text("Build the approved solution.\n", encoding="utf-8")
    (tmp_path / "docs/testing.md").write_text("Run focused checks and the full gate.\n", encoding="utf-8")
    (tmp_path / "docs/security.md").write_text("Review trust boundaries when applicable.\n", encoding="utf-8")

    playbook = run_checker(tmp_path, "--document", "docs/testing.md", "--route-source", "docs/design.md")

    assert playbook.returncode == 0, playbook.stdout + playbook.stderr
