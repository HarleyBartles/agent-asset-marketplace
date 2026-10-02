from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

import pytest


HOOK = Path(__file__).resolve().parents[2] / "assets" / "hooks" / "pre-commit"


def _bash() -> Path:
    git = shutil.which("git")
    if git:
        git_root = Path(git).resolve().parent.parent
        for candidate in (git_root / "bin/bash.exe", git_root / "usr/bin/bash.exe"):
            if candidate.is_file():
                return candidate
    discovered = shutil.which("bash")
    if discovered:
        return Path(discovered)
    pytest.fail("Git Bash is required for this hook test; install Git for Windows or make bash available on PATH")


def _git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    return result.stdout.strip()


def _write_adapter(repo: Path, *, apply_body: str, check_body: str) -> None:
    adapter = repo / "tools" / "hook_gate_adapter.sh"
    adapter.parent.mkdir(parents=True, exist_ok=True)
    adapter.write_text(
        "run_repository_apply_gate() {\n"
        + apply_body
        + "\n}\n\nrun_repository_check_gate() {\n"
        + check_body
        + "\n}\n",
        encoding="utf-8",
        newline="\n",
    )


def _repo(
    root: Path,
    *,
    apply_body: str = 'printf "apply\\n" >> "$REPO_ROOT/.git/gate-calls"',
    check_body: str = 'printf "check\\n" >> "$REPO_ROOT/.git/gate-calls"',
) -> Path:
    root.mkdir()
    _git(root, "init", "--quiet")
    for key, value in (
        ("user.name", "Hook Test"),
        ("user.email", "hook-test@example.invalid"),
        ("core.autocrlf", "false"),
        ("core.filemode", "false"),
    ):
        _git(root, "config", key, value)
    hooks = root / "githooks"
    hooks.mkdir()
    shutil.copyfile(HOOK, hooks / "pre-commit")
    if os.name != "nt":
        (hooks / "pre-commit").chmod(0o755)
    _write_adapter(root, apply_body=apply_body, check_body=check_body)
    (root / "notes file.txt").write_bytes(b"Header\nContent\nFooter\n")
    (root / "other.txt").write_bytes(b"Other base\n")
    _git(root, "add", "githooks/pre-commit", "tools/hook_gate_adapter.sh", "notes file.txt", "other.txt")
    _git(root, "commit", "--quiet", "-m", "base")
    return root


def _run_hook(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    script = repo / "githooks/pre-commit"
    drive = script.drive.rstrip(":").lower()
    bash_script = f"/{drive}/" + "/".join(script.parts[1:])
    return subprocess.run(
        [str(_bash()), bash_script, *args],
        cwd=repo,
        text=True,
        capture_output=True,
        check=False,
        env=os.environ.copy(),
    )


def test_local_hook_checks_the_staged_candidate_and_restores_other_work(tmp_path: Path) -> None:
    repo = _repo(
        tmp_path / "consumer repo",
        apply_body=(
            'printf "apply\\n" >> "$REPO_ROOT/.git/gate-calls"; '
            'sed -i "1s/^Header$/Header normalized/" "$REPO_ROOT/notes file.txt"'
        ),
        check_body=(
            'printf "check\\n" >> "$REPO_ROOT/.git/gate-calls"; '
            'cat "$REPO_ROOT/notes file.txt" > "$REPO_ROOT/.git/candidate-seen"; '
            'cat "$REPO_ROOT/other.txt" > "$REPO_ROOT/.git/other-seen"'
        ),
    )
    notes = repo / "notes file.txt"
    notes.write_bytes(b"Header\nContent staged\nFooter\n")
    _git(repo, "add", "notes file.txt")
    notes.write_bytes(b"Header\nContent staged\nFooter unstaged\n")
    (repo / "other.txt").write_bytes(b"Other staged\n")
    _git(repo, "add", "other.txt")
    (repo / "other.txt").write_bytes(b"Other unstaged\n")
    (repo / "untracked file.txt").write_bytes(b"Keep me\n")

    result = _run_hook(repo)

    assert result.returncode == 0, result.stdout + result.stderr
    assert _git(repo, "show", ":notes file.txt") == "Header normalized\nContent staged\nFooter"
    assert notes.read_bytes() == b"Header normalized\nContent staged\nFooter unstaged\n"
    assert _git(repo, "show", ":other.txt") == "Other staged"
    assert (repo / "other.txt").read_bytes() == b"Other unstaged\n"
    assert (repo / "untracked file.txt").read_bytes() == b"Keep me\n"
    assert (repo / ".git/candidate-seen").read_bytes() == b"Header normalized\nContent staged\nFooter\n"
    assert (repo / ".git/other-seen").read_bytes() == b"Other staged\n"
    assert (repo / ".git/gate-calls").read_text(encoding="utf-8").splitlines() == ["apply", "check"]


def test_local_hook_loads_the_adapter_from_the_staged_candidate(tmp_path: Path) -> None:
    repo = _repo(tmp_path / "adapter candidate repo")

    _write_adapter(repo, apply_body="return 17", check_body="return 17")
    _git(repo, "add", "tools/hook_gate_adapter.sh")
    _write_adapter(
        repo,
        apply_body='printf "unstaged adapter ran\\n" >> "$REPO_ROOT/.git/adapter-calls"',
        check_body='printf "unstaged adapter ran\\n" >> "$REPO_ROOT/.git/adapter-calls"',
    )

    result = _run_hook(repo)

    assert result.returncode != 0
    assert not (repo / ".git/adapter-calls").exists()
    assert _git(repo, "status", "--short") == "MM tools/hook_gate_adapter.sh"


def test_commit_only_validates_git_temporary_index_candidate(tmp_path: Path) -> None:
    repo = _repo(tmp_path / "path limited commit repo")
    _write_adapter(
        repo,
        apply_body='git write-tree > "$REPO_ROOT/.git/apply-tree"',
        check_body='git write-tree > "$REPO_ROOT/.git/check-tree"',
    )
    _git(repo, "add", "tools/hook_gate_adapter.sh")
    _git(repo, "commit", "--quiet", "-m", "record candidate observer")
    _git(repo, "config", "core.hooksPath", "githooks")

    (repo / "notes file.txt").write_text("Only-path commit\n", encoding="utf-8")
    (repo / "other.txt").write_text("Keep separately staged\n", encoding="utf-8")
    _git(repo, "add", "other.txt")
    result = subprocess.run(
        ["git", "commit", "--only", "-m", "path limited", "--", "notes file.txt"],
        cwd=repo,
        text=True,
        capture_output=True,
        check=False,
        env=os.environ.copy(),
    )

    assert result.returncode == 0, result.stdout + result.stderr
    committed_tree = _git(repo, "rev-parse", "HEAD^{tree}")
    assert (repo / ".git/check-tree").read_text(encoding="utf-8").strip() == committed_tree
    assert _git(repo, "show", "HEAD:notes file.txt") == "Only-path commit"
    assert _git(repo, "show", "HEAD:other.txt") == "Other base"
    assert _git(repo, "show", ":other.txt") == "Keep separately staged"


def test_apply_failure_restores_staged_and_unstaged_work(tmp_path: Path) -> None:
    repo = _repo(
        tmp_path / "apply failure repo",
        apply_body=(
            'printf "apply\\n" >> "$REPO_ROOT/.git/gate-calls"; '
            'printf "broken\\n" > "$REPO_ROOT/notes file.txt"; return 17'
        ),
        check_body='printf "check\\n" >> "$REPO_ROOT/.git/gate-calls"',
    )
    notes = repo / "notes file.txt"
    notes.write_bytes(b"Header staged\nContent\nFooter\n")
    _git(repo, "add", "notes file.txt")
    notes.write_bytes(b"Header staged\nContent\nFooter unstaged\n")
    (repo / "untracked file.txt").write_bytes(b"Keep me\n")

    result = _run_hook(repo)

    assert result.returncode == 17
    assert _git(repo, "show", ":notes file.txt") == "Header staged\nContent\nFooter"
    assert notes.read_bytes() == b"Header staged\nContent\nFooter unstaged\n"
    assert (repo / "untracked file.txt").read_bytes() == b"Keep me\n"
    assert (repo / ".git/gate-calls").read_text(encoding="utf-8").splitlines() == ["apply"]


def test_check_failure_keeps_the_applied_candidate_and_restores_other_work(tmp_path: Path) -> None:
    repo = _repo(
        tmp_path / "check failure repo",
        apply_body='sed -i "1s/^Header staged/Header normalized/" "$REPO_ROOT/notes file.txt"',
        check_body=(
            'printf "check\\n" >> "$REPO_ROOT/.git/gate-calls"; '
            'printf "callback corruption\\n" > "$REPO_ROOT/notes file.txt"; '
            'git add -- "notes file.txt"; return 23'
        ),
    )
    notes = repo / "notes file.txt"
    notes.write_bytes(b"Header staged\nContent\nFooter\n")
    _git(repo, "add", "notes file.txt")
    (repo / "other.txt").write_bytes(b"Other staged\n")
    _git(repo, "add", "other.txt")
    notes.write_bytes(b"Header staged\nContent\nFooter unstaged\n")
    (repo / "untracked file.txt").write_bytes(b"Keep me\n")

    result = _run_hook(repo)

    assert result.returncode == 23
    assert _git(repo, "show", ":notes file.txt").startswith("Header normalized")
    assert notes.read_bytes().startswith(b"Header normalized\n")
    assert notes.read_bytes().endswith(b"Footer unstaged\n")
    assert (repo / "untracked file.txt").read_bytes() == b"Keep me\n"


def test_hosted_mode_checks_only_a_clean_detached_committed_tree(tmp_path: Path) -> None:
    repo = _repo(tmp_path / "hosted repo")
    head = _git(repo, "rev-parse", "HEAD")
    _git(repo, "checkout", "--quiet", "--detach", head)
    before_tree = _git(repo, "write-tree")

    result = _run_hook(repo, "--hosted", head)

    assert result.returncode == 0, result.stdout + result.stderr
    assert _git(repo, "write-tree") == before_tree
    assert (repo / ".git/gate-calls").read_text(encoding="utf-8").splitlines() == ["check"]


def test_hosted_mode_rejects_dirty_or_attached_checkouts_before_running_gate(tmp_path: Path) -> None:
    repo = _repo(tmp_path / "dirty hosted repo")
    head = _git(repo, "rev-parse", "HEAD")
    _git(repo, "checkout", "--quiet", "--detach", head)
    (repo / "other.txt").write_bytes(b"dirty\n")

    dirty_result = _run_hook(repo, "--hosted", head)

    assert dirty_result.returncode != 0
    assert "clean" in dirty_result.stderr.lower()
    assert not (repo / ".git/gate-calls").exists()

    (repo / "other.txt").write_bytes(b"Other base\n")
    _git(repo, "checkout", "--quiet", "--force", "-B", "main", head)
    attached_result = _run_hook(repo, "--hosted", head)

    assert attached_result.returncode != 0
    assert "detached" in attached_result.stderr.lower()
    assert not (repo / ".git/gate-calls").exists()


def test_hook_fails_closed_when_the_repo_gate_adapter_is_missing(tmp_path: Path) -> None:
    repo = _repo(tmp_path / "no adapter repo")
    (repo / "tools/hook_gate_adapter.sh").unlink()
    _git(repo, "add", "-u", "tools/hook_gate_adapter.sh")

    result = _run_hook(repo)

    assert result.returncode != 0
    assert "not configured" in result.stderr.lower()
