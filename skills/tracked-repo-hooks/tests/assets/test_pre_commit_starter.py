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


def _git_env() -> dict[str, str]:
    env = os.environ.copy()
    for name in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE"):
        env.pop(name, None)
    return env


def _git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        text=True,
        capture_output=True,
        check=False,
        env=_git_env(),
    )
    assert result.returncode == 0, result.stdout + result.stderr
    return result.stdout.strip()


def _shell_path(path: Path) -> str:
    if os.name == "nt":
        return f"/{path.drive[0].lower()}/" + "/".join(path.parts[1:])
    return str(path)


def _adapter(repo: Path, *, check_body: str, legacy_apply_body: str | None = None) -> None:
    adapter = repo / "tools" / "hook_gate_adapter.sh"
    adapter.parent.mkdir(parents=True, exist_ok=True)
    functions = ""
    if legacy_apply_body is not None:
        functions = "run_repository_apply_gate() {\n" + legacy_apply_body + "\n}\n\n"
    adapter.write_text(
        functions + "run_repository_check_gate() {\n" + check_body + "\n}\n",
        encoding="utf-8",
        newline="\n",
    )


def _repo(root: Path, *, check_body: str = "return 0", legacy_apply_body: str | None = None) -> Path:
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
    _adapter(root, check_body=check_body, legacy_apply_body=legacy_apply_body)
    (root / ".gitignore").write_text("build/\n.pytest_cache/\n", encoding="utf-8", newline="\n")
    (root / "notes file.txt").write_bytes(b"Header\nContent\nFooter\n")
    (root / "other.txt").write_bytes(b"Other base\n")
    _git(root, "add", ".")
    _git(root, "commit", "--quiet", "-m", "base")
    return root


def _run_hook(repo: Path, *args: str, scratch: Path | None = None) -> subprocess.CompletedProcess[str]:
    script = repo / "githooks" / "pre-commit"
    drive = script.drive.rstrip(":").lower()
    bash_script = f"/{drive}/" + "/".join(script.parts[1:])
    env = _git_env()
    if scratch is not None:
        scratch.mkdir(parents=True, exist_ok=True)
        env["TMPDIR"] = _shell_path(scratch)
    return subprocess.run(
        [str(_bash()), bash_script, *args],
        cwd=repo,
        text=True,
        capture_output=True,
        check=False,
        env=env,
    )


def _external(path: Path) -> str:
    return f'"{_shell_path(path)}"'


def test_local_gate_rejects_the_original_staged_candidate_without_losing_local_work(tmp_path: Path) -> None:
    apply_marker = tmp_path / "apply marker.txt"
    candidate_seen = tmp_path / "candidate seen.txt"
    repo = _repo(
        tmp_path / "reject unmodified candidate repo",
        legacy_apply_body=(
            f'printf "apply\\n" >> {_external(apply_marker)}; '
            'sed -i "s/Header staged/Header normalized/" "$REPO_ROOT/notes file.txt"'
        ),
        check_body=(
            f'cat "$REPO_ROOT/notes file.txt" > {_external(candidate_seen)}; '
            'if grep -q "Header staged" "$REPO_ROOT/notes file.txt"; then '
            'printf "format check rejected staged bytes\\n" >&2; return 17; fi'
        ),
    )
    notes = repo / "notes file.txt"
    notes.write_bytes(b"Header staged\nContent\nFooter\n")
    _git(repo, "add", "notes file.txt")
    candidate_tree = _git(repo, "write-tree")
    notes.write_bytes(b"Header unstaged repair\nContent\nFooter unstaged\n")
    (repo / ".git/info/exclude").write_text(".cache/\n", encoding="utf-8")
    ignored = repo / ".cache" / "protected local input.txt"
    ignored.parent.mkdir(parents=True)
    ignored.write_text("keep this ignored input", encoding="utf-8")
    untracked = repo / "untracked file.txt"
    untracked.write_text("keep this authored file", encoding="utf-8")
    other = repo / "other.txt"
    other.write_bytes(b"Other staged\n")
    _git(repo, "add", "other.txt")
    other.write_bytes(b"Other unstaged\n")
    candidate_tree = _git(repo, "write-tree")
    scratch = tmp_path / "isolated hook scratch"

    result = _run_hook(repo, scratch=scratch)

    assert result.returncode == 17, result.stdout + result.stderr
    assert "format check rejected staged bytes" in result.stderr
    assert _git(repo, "write-tree") == candidate_tree
    assert notes.read_bytes() == b"Header unstaged repair\nContent\nFooter unstaged\n"
    assert _git(repo, "show", ":notes file.txt") == "Header staged\nContent\nFooter"
    assert _git(repo, "show", ":other.txt") == "Other staged"
    assert other.read_bytes() == b"Other unstaged\n"
    assert untracked.read_text(encoding="utf-8") == "keep this authored file"
    assert ignored.read_text(encoding="utf-8") == "keep this ignored input"
    assert not apply_marker.exists()
    assert candidate_seen.read_bytes() == b"Header staged\nContent\nFooter\n"
    assert not list(scratch.iterdir())


def test_gate_allows_disposable_ignored_outputs_without_importing_author_ignored_files(tmp_path: Path) -> None:
    build_seen = tmp_path / "build output seen.txt"
    repo = _repo(
        tmp_path / "disposable output repo",
        check_body=(
            'test ! -e "$REPO_ROOT/.cache/protected local input.txt" || return 31; '
            'mkdir -p "$REPO_ROOT/build"; '
            'printf "built\\n" > "$REPO_ROOT/build/report.txt"; '
            f'printf "output\\n" >> {_external(build_seen)}'
        ),
    )
    (repo / ".git/info/exclude").write_text(".cache/\n", encoding="utf-8")
    protected = repo / ".cache" / "protected local input.txt"
    protected.parent.mkdir(parents=True)
    protected.write_text("author cache", encoding="utf-8")
    scratch = tmp_path / "disposable output scratch"

    result = _run_hook(repo, scratch=scratch)

    assert result.returncode == 0, result.stdout + result.stderr
    assert build_seen.read_text(encoding="utf-8").splitlines() == ["output"]
    assert protected.read_text(encoding="utf-8") == "author cache"
    assert not (repo / "build/report.txt").exists()
    assert not list(scratch.iterdir())


def test_failed_check_that_mutates_candidate_preserves_status_and_original_index(tmp_path: Path) -> None:
    repo = _repo(
        tmp_path / "mutating callback repo",
        check_body=(
            'printf "corruption\\n" > "$REPO_ROOT/notes file.txt"; '
            'git add -- "notes file.txt"; '
            'printf "named check failed\\n" >&2; return 23'
        ),
    )
    notes = repo / "notes file.txt"
    notes.write_bytes(b"Header staged\nContent\nFooter\n")
    _git(repo, "add", "notes file.txt")
    candidate_tree = _git(repo, "write-tree")
    notes.write_bytes(b"Header unstaged\nContent\nFooter unstaged\n")
    untracked = repo / "untracked file.txt"
    untracked.write_text("preserve", encoding="utf-8")
    (repo / ".git/info/exclude").write_text(".cache/\n", encoding="utf-8")
    protected = repo / ".cache" / "protected.txt"
    protected.parent.mkdir(parents=True)
    protected.write_text("preserve ignored input", encoding="utf-8")
    scratch = tmp_path / "mutating callback scratch"

    result = _run_hook(repo, scratch=scratch)

    assert result.returncode == 23, result.stdout + result.stderr
    assert "named check failed" in result.stderr
    assert "changed" in result.stderr.lower()
    assert _git(repo, "write-tree") == candidate_tree
    assert _git(repo, "show", ":notes file.txt") == "Header staged\nContent\nFooter"
    assert notes.read_bytes() == b"Header unstaged\nContent\nFooter unstaged\n"
    assert untracked.read_text(encoding="utf-8") == "preserve"
    assert protected.read_text(encoding="utf-8") == "preserve ignored input"
    assert not list(scratch.iterdir())


def test_local_hook_loads_check_adapter_from_the_staged_candidate(tmp_path: Path) -> None:
    adapter_calls = tmp_path / "adapter calls.txt"
    repo = _repo(tmp_path / "adapter candidate repo")
    _adapter(repo, check_body=f'printf "staged\\n" >> {_external(adapter_calls)}; return 19')
    _git(repo, "add", "tools/hook_gate_adapter.sh")
    _adapter(repo, check_body=f'printf "unstaged\\n" >> {_external(adapter_calls)}; return 0')
    scratch = tmp_path / "adapter candidate scratch"

    result = _run_hook(repo, scratch=scratch)

    assert result.returncode == 19
    assert adapter_calls.read_text(encoding="utf-8").splitlines() == ["staged"]
    assert _git(repo, "status", "--short") == "MM tools/hook_gate_adapter.sh"
    assert not list(scratch.iterdir())


def test_path_limited_commit_checks_git_temporary_index_and_preserves_separately_staged_work(tmp_path: Path) -> None:
    repo = _repo(tmp_path / "path limited commit repo")
    seen_tree = tmp_path / "candidate tree.txt"
    _adapter(repo, check_body=f"git write-tree > {_external(seen_tree)}")
    _git(repo, "add", "tools/hook_gate_adapter.sh")
    _git(repo, "commit", "--quiet", "-m", "record candidate observer")
    _git(repo, "config", "core.hooksPath", "githooks")
    _git(repo, "config", "user.name", "Hook Test")
    _git(repo, "config", "user.email", "hook-test@example.invalid")
    scratch = tmp_path / "path limited scratch"
    env = _git_env()
    scratch.mkdir()
    env["TMPDIR"] = _shell_path(scratch)
    (repo / "notes file.txt").write_text("Only-path commit\n", encoding="utf-8")
    (repo / "other.txt").write_text("Keep separately staged\n", encoding="utf-8")
    _git(repo, "add", "other.txt")
    result = subprocess.run(
        ["git", "commit", "--only", "-m", "path limited", "--", "notes file.txt"],
        cwd=repo,
        text=True,
        capture_output=True,
        check=False,
        env=env,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    committed_tree = _git(repo, "rev-parse", "HEAD^{tree}")
    assert seen_tree.read_text(encoding="utf-8").strip() == committed_tree
    assert _git(repo, "show", "HEAD:notes file.txt") == "Only-path commit"
    assert _git(repo, "show", "HEAD:other.txt") == "Other base"
    assert _git(repo, "show", ":other.txt") == "Keep separately staged"
    assert not list(scratch.iterdir())


def test_hosted_and_local_modes_check_the_same_tree_without_mutating_the_checkout(tmp_path: Path) -> None:
    seen_trees = tmp_path / "seen trees.txt"
    repo = _repo(tmp_path / "hosted repo", check_body=f"git write-tree >> {_external(seen_trees)}")
    head = _git(repo, "rev-parse", "HEAD")
    _git(repo, "checkout", "--quiet", "--detach", head)
    before_tree = _git(repo, "write-tree")
    scratch = tmp_path / "hosted scratch"

    local_result = _run_hook(repo, scratch=scratch)
    hosted_result = _run_hook(repo, "--hosted", head, scratch=scratch)

    assert local_result.returncode == 0, local_result.stdout + local_result.stderr
    assert hosted_result.returncode == 0, hosted_result.stdout + hosted_result.stderr
    assert _git(repo, "write-tree") == before_tree
    assert seen_trees.read_text(encoding="utf-8").splitlines() == [before_tree, before_tree]
    assert not list(scratch.iterdir())


def test_hosted_mode_rejects_dirty_or_attached_checkouts_before_gate_execution(tmp_path: Path) -> None:
    calls = tmp_path / "hosted calls.txt"
    repo = _repo(tmp_path / "dirty hosted repo", check_body=f'printf "called\\n" >> {_external(calls)}')
    head = _git(repo, "rev-parse", "HEAD")
    _git(repo, "checkout", "--quiet", "--detach", head)
    scratch = tmp_path / "hosted rejected scratch"
    (repo / "other.txt").write_bytes(b"dirty\n")

    dirty_result = _run_hook(repo, "--hosted", head, scratch=scratch)

    assert dirty_result.returncode != 0
    assert "clean" in dirty_result.stderr.lower()
    assert not calls.exists()
    assert not list(scratch.iterdir())

    (repo / "other.txt").write_bytes(b"Other base\n")
    _git(repo, "checkout", "--quiet", "--force", "-B", "main", head)
    attached_result = _run_hook(repo, "--hosted", head, scratch=scratch)

    assert attached_result.returncode != 0
    assert "detached" in attached_result.stderr.lower()
    assert not calls.exists()
    assert not list(scratch.iterdir())


def test_missing_candidate_adapter_fails_closed(tmp_path: Path) -> None:
    repo = _repo(tmp_path / "no adapter repo")
    (repo / "tools/hook_gate_adapter.sh").unlink()
    _git(repo, "add", "-u", "tools/hook_gate_adapter.sh")
    scratch = tmp_path / "no adapter scratch"

    result = _run_hook(repo, scratch=scratch)

    assert result.returncode == 2
    assert "adapter" in result.stderr.lower()
    assert "not configured" in result.stderr.lower()
    assert not list(scratch.iterdir())


def test_candidate_with_unavailable_staged_submodule_object_fails_without_fetching(tmp_path: Path) -> None:
    calls = tmp_path / "submodule gate calls.txt"
    repo = _repo(tmp_path / "missing submodule object repo", check_body=f'printf "called\\n" >> {_external(calls)}')
    module_path = repo / "modules" / "child"
    module_path.mkdir(parents=True)
    _git(module_path, "init", "--quiet")
    _git(module_path, "config", "user.name", "Hook Test")
    _git(module_path, "config", "user.email", "hook-test@example.invalid")
    (module_path / "source.txt").write_text("local source", encoding="utf-8")
    _git(module_path, "add", "source.txt")
    _git(module_path, "commit", "--quiet", "-m", "local source")
    unavailable = _git(repo, "rev-parse", "HEAD")
    (repo / ".gitmodules").write_text(
        '[submodule "child"]\n\tpath = modules/child\n\turl = https://example.invalid/missing.git\n',
        encoding="utf-8",
    )
    _git(repo, "add", ".gitmodules")
    _git(repo, "update-index", "--add", "--cacheinfo", f"160000,{unavailable},modules/child")
    source_status = _git(module_path, "status", "--porcelain")
    scratch = tmp_path / "missing submodule scratch"

    result = _run_hook(repo, scratch=scratch)

    assert result.returncode == 2, result.stdout + result.stderr
    assert "submodule" in result.stderr.lower()
    assert unavailable in result.stderr
    assert not calls.exists()
    assert _git(module_path, "status", "--porcelain") == source_status
    assert not list(scratch.iterdir())


def test_unborn_root_candidate_can_be_materialized_and_checked(tmp_path: Path) -> None:
    checked_tree = tmp_path / "root tree.txt"
    repo = tmp_path / "root candidate repo"
    repo.mkdir()
    _git(repo, "init", "--quiet")
    _git(repo, "config", "user.name", "Hook Test")
    _git(repo, "config", "user.email", "hook-test@example.invalid")
    (repo / "githooks").mkdir()
    shutil.copyfile(HOOK, repo / "githooks/pre-commit")
    if os.name != "nt":
        (repo / "githooks/pre-commit").chmod(0o755)
    (repo / "tools").mkdir()
    _adapter(repo, check_body=f"git write-tree > {_external(checked_tree)}")
    (repo / "initial.txt").write_text("root candidate", encoding="utf-8")
    _git(repo, "add", ".")
    source_tree = _git(repo, "write-tree")
    scratch = tmp_path / "root candidate scratch"

    result = _run_hook(repo, scratch=scratch)

    assert result.returncode == 0, result.stdout + result.stderr
    assert checked_tree.read_text(encoding="utf-8").strip() == source_tree
    head_check = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "--verify", "HEAD"],
        text=True,
        capture_output=True,
        check=False,
        env=_git_env(),
    )
    assert head_check.returncode != 0
    assert _git(repo, "write-tree") == source_tree
    assert not list(scratch.iterdir())


def test_fail_fast_adapter_preserves_first_failure_and_does_not_start_expensive_check(tmp_path: Path) -> None:
    calls = tmp_path / "ordered checks.txt"
    expensive = tmp_path / "expensive marker.txt"
    repo = _repo(
        tmp_path / "fail fast repo",
        check_body=(
            f'printf "cheap\\n" >> {_external(calls)}; '
            'printf "cheap validation failed\\nRepair: python repair.py --file \\"notes file.txt\\"\\n'
            'Recheck: python validate.py --file \\"notes file.txt\\"\\n" >&2; '
            "false || return 17; "
            f'printf "expensive\\n" >> {_external(expensive)}'
        ),
    )
    scratch = tmp_path / "fail fast scratch"

    result = _run_hook(repo, scratch=scratch)
    head = _git(repo, "rev-parse", "HEAD")
    _git(repo, "checkout", "--quiet", "--detach", head)
    hosted_result = _run_hook(repo, "--hosted", head, scratch=scratch)

    assert result.returncode == 17
    assert hosted_result.returncode == 17, hosted_result.stdout + hosted_result.stderr
    assert "cheap validation failed" in result.stderr
    assert 'Repair: python repair.py --file "notes file.txt"' in result.stderr
    assert 'Recheck: python validate.py --file "notes file.txt"' in result.stderr
    assert calls.read_text(encoding="utf-8").splitlines() == ["cheap", "cheap"]
    assert not expensive.exists()
    assert not list(scratch.iterdir())
