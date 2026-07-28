from __future__ import annotations

import json
import sys
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import ruff_diff


class _FakeRun:
    """Configurable subprocess.run replacement for ruff_diff tests."""

    def __init__(self) -> None:
        self._responses: dict[tuple[str, ...], SimpleNamespace] = {}

    def add(self, cmd: tuple[str, ...], *, stdout: str = "", stderr: str = "", returncode: int = 0) -> None:
        self._responses[cmd] = SimpleNamespace(stdout=stdout, stderr=stderr, returncode=returncode)

    def __call__(self, cmd: list[str], *, check: bool = False) -> SimpleNamespace:
        key = tuple(cmd)
        if key in self._responses:
            return self._responses[key]
        if "ruff" in key:
            return SimpleNamespace(stdout="", stderr="", returncode=0)
        raise AssertionError(f"unexpected command: {cmd}")


def _run_with_git() -> _FakeRun:
    fake = _FakeRun()
    fake.add(("git", "rev-parse", "--verify", "origin/main"), returncode=0, stdout="abc123\n")
    return fake


def test_resolve_base_ref_uses_origin_main(monkeypatch) -> None:
    fake = _FakeRun()
    fake.add(("git", "rev-parse", "--verify", "origin/main"), returncode=0, stdout="abc123\n")
    monkeypatch.setattr(ruff_diff, "_run", fake)
    args = SimpleNamespace(changed_from="")
    assert ruff_diff._resolve_base_ref(args) == "origin/main"


def test_resolve_base_ref_uses_changed_from(monkeypatch) -> None:
    fake = _FakeRun()
    fake.add(("git", "rev-parse", "--verify", "feature"), returncode=0, stdout="def456\n")
    monkeypatch.setattr(ruff_diff, "_run", fake)
    args = SimpleNamespace(changed_from="feature")
    assert ruff_diff._resolve_base_ref(args) == "feature"


def test_resolve_base_ref_warns_when_changed_from_missing(monkeypatch, capsys) -> None:
    fake = _FakeRun()
    fake.add(("git", "rev-parse", "--verify", "missing"), returncode=1, stderr="fatal: not a valid object name")
    fake.add(("git", "rev-parse", "--verify", "origin/main"), returncode=1, stderr="fatal: not a valid object name")
    monkeypatch.setattr(ruff_diff, "_run", fake)
    args = SimpleNamespace(changed_from="missing")
    assert ruff_diff._resolve_base_ref(args) is None
    captured = capsys.readouterr()
    assert "missing not found" in captured.err


def test_changed_python_files_filters_and_exists(monkeypatch, tmp_path: Path) -> None:
    (tmp_path / "foo.py").write_text("x", encoding="utf-8")
    name_list = f"{tmp_path / 'foo.py'}\n{tmp_path / 'nope.md'}\n"
    fake = _run_with_git()
    fake.add(
        ("git", "diff", "--name-only", "--diff-filter=ACMR", "origin/main...HEAD"),
        stdout=name_list,
    )
    monkeypatch.setattr(ruff_diff, "_run", fake)
    files = ruff_diff._changed_python_files("origin/main")
    assert all(isinstance(p, Path) for p in files)
    assert (tmp_path / "foo.py") in files
    assert (tmp_path / "nope.md") not in files


def test_added_line_numbers_parse_added_and_context_lines(monkeypatch) -> None:
    diff = (
        "diff --git a/tools/foo.py b/tools/foo.py\n"
        "--- a/tools/foo.py\n"
        "+++ b/tools/foo.py\n"
        "@@ -10,3 +10,4 @@\n"
        " context0\n"
        "-removed\n"
        "+added1\n"
        "+added2\n"
        " context1\n"
    )
    path = Path("tools", "foo.py")
    fake = _run_with_git()
    fake.add(
        ("git", "diff", "--unified=0", "origin/main...HEAD", "--", str(path)),
        stdout=diff,
    )
    monkeypatch.setattr(ruff_diff, "_run", fake)
    added = ruff_diff._added_line_numbers("origin/main", path)
    # hunk starts at new line 10:
    # " context0" -> 11
    # "-removed" -> no advance
    # "+added1" -> add 11, advance to 12
    # "+added2" -> add 12, advance to 13
    # " context1" -> 14
    assert added == {11, 12}


def test_added_line_numbers_skips_no_newline_marker(monkeypatch) -> None:
    diff = (
        "diff --git a/tools/foo.py b/tools/foo.py\n"
        "--- a/tools/foo.py\n"
        "+++ b/tools/foo.py\n"
        "@@ -5 +5,2 @@\n"
        " context\n"
        "+added\n"
        "\\ No newline at end of file\n"
    )
    path = Path("tools", "foo.py")
    fake = _run_with_git()
    fake.add(
        ("git", "diff", "--unified=0", "origin/main...HEAD", "--", str(path)),
        stdout=diff,
    )
    monkeypatch.setattr(ruff_diff, "_run", fake)
    added = ruff_diff._added_line_numbers("origin/main", path)
    # hunk starts at new line 5:
    # " context" -> 6
    # "+added" -> add 6
    # "\ No newline" -> ignored, not a file line
    assert added == {6}


def test_added_line_numbers_pure_deletion_returns_empty(monkeypatch) -> None:
    diff = (
        "diff --git a/tools/foo.py b/tools/foo.py\n"
        "--- a/tools/foo.py\n"
        "+++ b/tools/foo.py\n"
        "@@ -5,3 +0,0 @@\n"
        "-line1\n"
        "-line2\n"
        "-line3\n"
    )
    path = Path("tools", "foo.py")
    fake = _run_with_git()
    fake.add(
        ("git", "diff", "--unified=0", "origin/main...HEAD", "--", str(path)),
        stdout=diff,
    )
    monkeypatch.setattr(ruff_diff, "_run", fake)
    added = ruff_diff._added_line_numbers("origin/main", path)
    assert added == set()


def test_lint_file_filters_findings_to_changed_lines(monkeypatch) -> None:
    diff = (
        "diff --git a/tools/foo.py b/tools/foo.py\n"
        "--- a/tools/foo.py\n"
        "+++ b/tools/foo.py\n"
        "@@ -2,0 +3,2 @@\n"
        "+bad = 1\n"
        "+old = unused\n"
    )
    ruff_json = [
        {
            "filename": "tools/foo.py",
            "location": {"row": 3, "column": 1},
            "end_location": {"row": 3, "column": 3},
            "code": "F841",
            "message": "local variable `bad` is assigned to but never used",
        },
        {
            "filename": "tools/foo.py",
            "location": {"row": 10, "column": 1},
            "end_location": {"row": 10, "column": 3},
            "code": "F841",
            "message": "pre-existing",
        },
    ]
    path = Path("tools", "foo.py")
    fake = _run_with_git()
    fake.add(
        ("git", "diff", "--unified=0", "origin/main...HEAD", "--", str(path)),
        stdout=diff,
    )
    fake.add(
        (sys.executable, "-m", "ruff", "check", "--output-format=json", str(path)),
        stdout=json.dumps(ruff_json),
        returncode=1,
    )
    monkeypatch.setattr(ruff_diff, "_run", fake)
    findings = ruff_diff._lint_file("origin/main", path)
    assert len(findings) == 1
    assert "bad" in findings[0]


def test_lint_file_reports_ruff_failure(monkeypatch) -> None:
    diff = (
        "diff --git a/tools/foo.py b/tools/foo.py\n"
        "--- a/tools/foo.py\n"
        "+++ b/tools/foo.py\n"
        "@@ -1 +1 @@\n"
        "+x\n"
    )
    path = Path("tools", "foo.py")
    fake = _run_with_git()
    fake.add(
        ("git", "diff", "--unified=0", "origin/main...HEAD", "--", str(path)),
        stdout=diff,
    )
    fake.add(
        (sys.executable, "-m", "ruff", "check", "--output-format=json", str(path)),
        stderr="ruff: invalid syntax at line 1\n",
        returncode=2,
    )
    monkeypatch.setattr(ruff_diff, "_run", fake)
    findings = ruff_diff._lint_file("origin/main", path)
    assert len(findings) == 1
    assert "ruff failed" in findings[0]


def test_lint_file_reports_invalid_ruff_output(monkeypatch) -> None:
    diff = (
        "diff --git a/tools/foo.py b/tools/foo.py\n"
        "--- a/tools/foo.py\n"
        "+++ b/tools/foo.py\n"
        "@@ -1 +1 @@\n"
        "+x\n"
    )
    path = Path("tools", "foo.py")
    fake = _run_with_git()
    fake.add(
        ("git", "diff", "--unified=0", "origin/main...HEAD", "--", str(path)),
        stdout=diff,
    )
    fake.add(
        (sys.executable, "-m", "ruff", "check", "--output-format=json", str(path)),
        stdout="not-json",
        returncode=1,
    )
    monkeypatch.setattr(ruff_diff, "_run", fake)
    findings = ruff_diff._lint_file("origin/main", path)
    assert len(findings) == 1
    assert "invalid ruff output" in findings[0]


def test_lint_file_reports_unexpected_ruff_output(monkeypatch) -> None:
    diff = (
        "diff --git a/tools/foo.py b/tools/foo.py\n"
        "--- a/tools/foo.py\n"
        "+++ b/tools/foo.py\n"
        "@@ -1 +1 @@\n"
        "+x\n"
    )
    path = Path("tools", "foo.py")
    fake = _run_with_git()
    fake.add(
        ("git", "diff", "--unified=0", "origin/main...HEAD", "--", str(path)),
        stdout=diff,
    )
    fake.add(
        (sys.executable, "-m", "ruff", "check", "--output-format=json", str(path)),
        stdout=json.dumps({"error": "unexpected"}),
        returncode=1,
    )
    monkeypatch.setattr(ruff_diff, "_run", fake)
    findings = ruff_diff._lint_file("origin/main", path)
    assert len(findings) == 1
    assert "unexpected ruff output" in findings[0]


def test_main_returns_zero_when_no_findings(monkeypatch, tmp_path: Path, capsys) -> None:
    path = tmp_path / "foo.py"
    path.write_text("x = 1\n", encoding="utf-8")
    diff = (
        "diff --git a/foo.py b/foo.py\n"
        "--- a/foo.py\n"
        "+++ b/foo.py\n"
        "@@ -1 +1 @@\n"
        "-x\n"
        "+y\n"
    )
    fake = _run_with_git()
    fake.add(
        ("git", "diff", "--name-only", "--diff-filter=ACMR", "origin/main...HEAD"),
        stdout=f"{path}\n",
    )
    fake.add(
        ("git", "diff", "--unified=0", "origin/main...HEAD", "--", str(path)),
        stdout=diff,
    )
    fake.add(
        (sys.executable, "-m", "ruff", "check", "--output-format=json", str(path)),
        stdout="[]",
        returncode=0,
    )
    monkeypatch.setattr(ruff_diff, "_run", fake)
    assert ruff_diff.main(["--changed-from", "origin/main"]) == 0
    captured = capsys.readouterr()
    assert "No new lint findings" in captured.out


def test_main_returns_one_when_findings_on_changed_lines(monkeypatch, tmp_path: Path, capsys) -> None:
    path = tmp_path / "foo.py"
    path.write_text("y = 1\n", encoding="utf-8")
    diff = (
        "diff --git a/foo.py b/foo.py\n"
        "--- a/foo.py\n"
        "+++ b/foo.py\n"
        "@@ -1 +1,2 @@\n"
        "-y\n"
        "+unused = 1\n"
        "+z = 2\n"
    )
    ruff_json = [
        {
            "filename": str(path),
            "location": {"row": 1, "column": 1},
            "end_location": {"row": 1, "column": 7},
            "code": "F841",
            "message": "local variable `unused` is assigned to but never used",
        }
    ]
    fake = _run_with_git()
    fake.add(
        ("git", "diff", "--name-only", "--diff-filter=ACMR", "origin/main...HEAD"),
        stdout=f"{path}\n",
    )
    fake.add(
        ("git", "diff", "--unified=0", "origin/main...HEAD", "--", str(path)),
        stdout=diff,
    )
    fake.add(
        (sys.executable, "-m", "ruff", "check", "--output-format=json", str(path)),
        stdout=json.dumps(ruff_json),
        returncode=1,
    )
    monkeypatch.setattr(ruff_diff, "_run", fake)
    assert ruff_diff.main(["--changed-from", "origin/main"]) == 1
    captured = capsys.readouterr()
    assert "Found 1 new lint finding" in captured.err


def test_main_returns_zero_when_no_python_files_changed(monkeypatch, capsys) -> None:
    fake = _run_with_git()
    fake.add(
        ("git", "diff", "--name-only", "--diff-filter=ACMR", "origin/main...HEAD"),
        stdout="README.md\n",
    )
    monkeypatch.setattr(ruff_diff, "_run", fake)
    assert ruff_diff.main(["--changed-from", "origin/main"]) == 0
    captured = capsys.readouterr()
    assert "No changed Python files" in captured.out
