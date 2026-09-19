from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "codex-marketplace/plugins/superpowers-plus/skills/subagent-workspace/scripts"


def _git(cwd: Path, *args: str) -> str:
    result = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, check=True)
    return result.stdout.strip()


def _repo(tmp_path: Path) -> Path:
    repo = tmp_path / "example repo"
    repo.mkdir(parents=True)
    _git(repo, "init")
    _git(repo, "config", "user.email", "test@example.invalid")
    _git(repo, "config", "user.name", "Test User")
    (repo / "seed.txt").write_text("seed\n", encoding="utf-8")
    _git(repo, "add", "seed.txt")
    _git(repo, "commit", "-m", "seed")
    return repo


def _run(script: str, cwd: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPTS / script), *args],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=check,
    )


def test_workspace_disambiguates_same_basename_by_canonical_plan_identity(tmp_path: Path):
    repo = _repo(tmp_path)
    first = repo / "plans" / "one" / "upgrade.md"
    second = repo / "plans" / "two" / "upgrade.md"
    first.parent.mkdir(parents=True)
    second.parent.mkdir(parents=True)
    first.write_text("# First\n", encoding="utf-8")
    second.write_text("# Second\n", encoding="utf-8")

    first_workspace = Path(_run("workspace.py", repo, "--apply", str(first)).stdout.strip())
    second_workspace = Path(_run("workspace.py", repo, "--apply", str(second)).stdout.strip())

    assert first_workspace != second_workspace
    assert first_workspace.parent == second_workspace.parent
    assert (first_workspace / ".plan-identity").read_text(encoding="utf-8") == str(first.resolve())
    assert (second_workspace / ".plan-identity").read_text(encoding="utf-8") == str(second.resolve())


def test_workspace_adopts_markerless_legacy_candidate_once(tmp_path: Path):
    repo = _repo(tmp_path)
    plan_one = repo / "a" / "upgrade.md"
    plan_two = repo / "b" / "upgrade.md"
    plan_one.parent.mkdir()
    plan_two.parent.mkdir()
    plan_one.write_text("# One\n", encoding="utf-8")
    plan_two.write_text("# Two\n", encoding="utf-8")

    preview = Path(_run("workspace.py", repo, str(plan_one)).stdout.strip())
    preview.mkdir(parents=True)
    (preview / "legacy.txt").write_text("keep\n", encoding="utf-8")

    adopted = Path(_run("workspace.py", repo, "--apply", str(plan_one)).stdout.strip())
    disambiguated = Path(_run("workspace.py", repo, "--apply", str(plan_two)).stdout.strip())

    assert adopted == preview
    assert (adopted / "legacy.txt").is_file()
    assert disambiguated != adopted
    assert not (disambiguated / "legacy.txt").exists()


def test_workspace_sanitizes_repo_and_branch_and_defaults_to_check(tmp_path: Path):
    repo = _repo(tmp_path)
    _git(repo, "checkout", "-b", "feature/slash")
    plan = repo / "plan.md"
    plan.write_text("# Plan\n", encoding="utf-8")

    workspace = Path(_run("workspace.py", repo, str(plan)).stdout.strip())

    assert any(part.startswith("feature-slash-") for part in workspace.parts)
    assert workspace.parts[-4] == "_agent-scratch"
    assert not workspace.exists()


def test_workspace_identity_segments_resist_sanitization_collisions(tmp_path: Path):
    first_repo = _repo(tmp_path / "one")
    second_repo = _repo(tmp_path / "two")
    first_plan = first_repo / "plan.md"
    second_plan = second_repo / "plan.md"
    first_plan.write_text("# Plan\n", encoding="utf-8")
    second_plan.write_text("# Plan\n", encoding="utf-8")
    _git(first_repo, "checkout", "-b", "feature/slash")
    _git(second_repo, "checkout", "-b", "feature-slash")

    first = Path(_run("workspace.py", first_repo, "--apply", str(first_plan)).stdout.strip())
    second = Path(_run("workspace.py", second_repo, "--apply", str(second_plan)).stdout.strip())

    assert first != second
    assert (first.parent / ".workspace-identity").is_file()
    assert (second.parent / ".workspace-identity").is_file()


def test_workspace_reuses_matching_suffixed_identity_after_lower_slot_removed(tmp_path: Path):
    repo = _repo(tmp_path)
    first_plan = repo / "a" / "upgrade.md"
    second_plan = repo / "b" / "upgrade.md"
    first_plan.parent.mkdir()
    second_plan.parent.mkdir()
    first_plan.write_text("# First\n", encoding="utf-8")
    second_plan.write_text("# Second\n", encoding="utf-8")
    first = Path(_run("workspace.py", repo, "--apply", str(first_plan)).stdout.strip())
    second = Path(_run("workspace.py", repo, "--apply", str(second_plan)).stdout.strip())

    for child in first.iterdir():
        child.unlink()
    first.rmdir()

    assert Path(_run("workspace.py", repo, "--apply", str(second_plan)).stdout.strip()) == second


def test_task_brief_extracts_one_task_as_utf8_without_bom(tmp_path: Path):
    repo = _repo(tmp_path)
    plan = repo / "plan.md"
    plan.write_text("# Plan\n\n### Task 1: One\nbody\n\n### Task 2: Two\nother\n", encoding="utf-8")

    result = _run("task_brief.py", repo, "--apply", str(plan), "1")
    output = Path(result.stdout.strip().split("wrote ", 1)[1].split(": ", 1)[0])

    assert output.read_bytes().startswith(b"### Task 1")
    assert not output.read_bytes().startswith(b"\xef\xbb\xbf")
    assert "Task 2" not in output.read_text(encoding="utf-8")


def test_review_package_rejects_empty_and_non_descendant_ranges(tmp_path: Path):
    repo = _repo(tmp_path)
    base = _git(repo, "rev-parse", "HEAD")

    empty = _run("review_package.py", repo, "--apply", "-", base, base, check=False)
    assert empty.returncode == 3
    assert "empty review range" in empty.stderr

    _git(repo, "checkout", "--orphan", "unrelated")
    _git(repo, "rm", "-rf", ".")
    (repo / "other.txt").write_text("other\n", encoding="utf-8")
    _git(repo, "add", "other.txt")
    _git(repo, "commit", "-m", "other")
    head = _git(repo, "rev-parse", "HEAD")

    unrelated = _run("review_package.py", repo, "--apply", "-", base, head, check=False)
    assert unrelated.returncode == 3
    assert "not a descendant" in unrelated.stderr


def test_review_package_contains_commits_stat_and_context_diff(tmp_path: Path):
    repo = _repo(tmp_path)
    base = _git(repo, "rev-parse", "HEAD")
    (repo / "seed.txt").write_text("seed\nchanged\n", encoding="utf-8")
    _git(repo, "add", "seed.txt")
    _git(repo, "commit", "-m", "change")
    head = _git(repo, "rev-parse", "HEAD")

    result = _run("review_package.py", repo, "--apply", "-", base, head)
    output = Path(result.stdout.strip().split("wrote ", 1)[1].split(": ", 1)[0])
    content = output.read_text(encoding="utf-8")

    assert not output.read_bytes().startswith(b"\xef\xbb\xbf")
    assert "## Commits" in content and "change" in content
    assert "## Files changed" in content and "seed.txt" in content
    assert "## Diff" in content and "@@" in content


def test_review_package_decodes_utf8_diff_on_windows(tmp_path: Path):
    repo = _repo(tmp_path)
    base = _git(repo, "rev-parse", "HEAD")
    (repo / "unicode.txt").write_text("Native → review\n", encoding="utf-8")
    _git(repo, "add", "unicode.txt")
    _git(repo, "commit", "-m", "add unicode")
    head = _git(repo, "rev-parse", "HEAD")

    result = _run("review_package.py", repo, "--apply", "-", base, head)
    output = Path(result.stdout.strip().split("wrote ", 1)[1].split(": ", 1)[0])

    assert "Native → review" in output.read_text(encoding="utf-8")


def test_python_helpers_expose_help_and_default_to_read_only(tmp_path: Path):
    repo = _repo(tmp_path)
    plan = repo / "plan.md"
    plan.write_text("### Task 1: One\nbody\n", encoding="utf-8")
    base = _git(repo, "rev-parse", "HEAD")

    for script in ("workspace.py", "task_brief.py", "review_package.py"):
        help_result = _run(script, repo, "--help")
        assert help_result.returncode == 0
        assert "mixed:" in help_result.stdout
        assert _run(script, repo, "--check").returncode == 0

    brief = _run("task_brief.py", repo, str(plan), "1")
    assert "would write" in brief.stdout
    review = _run("review_package.py", repo, "-", base, base, check=False)
    assert review.returncode == 3
    assert not list(tmp_path.rglob("review-*.diff"))
