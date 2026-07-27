from __future__ import annotations

import sys
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import shared_checkout


def _fake_git_dir(tmp_path: Path) -> Path:
    git_dir = tmp_path / ".git"
    git_dir.mkdir()
    (git_dir / "info").mkdir(parents=True)
    return git_dir


def _make_fake_run(git_dir: Path, common_dir: Path | None = None) -> object:
    """Return a subprocess.run replacement that reports the requested git dirs."""
    common = common_dir or git_dir

    def fake_run(cmd, **kwargs):
        if "--absolute-git-dir" in cmd:
            return SimpleNamespace(stdout=str(git_dir), returncode=0, stderr="")
        if "--git-common-dir" in cmd:
            return SimpleNamespace(stdout=str(common), returncode=0, stderr="")
        return SimpleNamespace(stdout="", returncode=0, stderr="")

    return fake_run


def test_is_shared_checkout_false_for_main_worktree(monkeypatch, tmp_path: Path) -> None:
    git_dir = _fake_git_dir(tmp_path)
    monkeypatch.setattr(shared_checkout.subprocess, "run", _make_fake_run(git_dir, git_dir))
    assert not shared_checkout.is_shared_checkout(tmp_path)


def test_is_shared_checkout_true_for_linked_worktree(monkeypatch, tmp_path: Path) -> None:
    git_dir = tmp_path / ".git" / "worktrees" / "feature"
    git_dir.mkdir(parents=True)
    (git_dir / "info").mkdir(parents=True)
    common_dir = tmp_path / ".git"
    monkeypatch.setattr(shared_checkout.subprocess, "run", _make_fake_run(git_dir, common_dir))
    assert shared_checkout.is_shared_checkout(tmp_path)


def test_approve_mutation_allowed_in_normal_checkout(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(shared_checkout, "is_shared_checkout", lambda _root: False)
    assert shared_checkout.approve_mutation(tmp_path, "test", flag_approved=False)


def test_approve_mutation_allowed_with_flag_in_shared_checkout(monkeypatch, tmp_path: Path, capsys) -> None:
    monkeypatch.setattr(shared_checkout, "is_shared_checkout", lambda _root: True)
    assert shared_checkout.approve_mutation(tmp_path, "test", flag_approved=True)
    captured = capsys.readouterr()
    assert "--allow-shared-checkout supplied" in captured.err


def test_approve_mutation_prompts_in_shared_checkout_and_approves(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(shared_checkout, "is_shared_checkout", lambda _root: True)
    monkeypatch.setattr(shared_checkout, "prompt_for_approval", lambda _name: True)
    assert shared_checkout.approve_mutation(tmp_path, "test", flag_approved=False)


def test_approve_mutation_denies_when_prompt_rejects(monkeypatch, tmp_path: Path, capsys) -> None:
    monkeypatch.setattr(shared_checkout, "is_shared_checkout", lambda _root: True)
    monkeypatch.setattr(shared_checkout, "prompt_for_approval", lambda _name: False)
    assert not shared_checkout.approve_mutation(tmp_path, "test", flag_approved=False)
    captured = capsys.readouterr()
    assert "refusing to apply" in captured.err


def test_prompt_for_approval_returns_false_when_non_tty(monkeypatch) -> None:
    monkeypatch.setattr(sys.stdin, "isatty", lambda: False)
    assert not shared_checkout.prompt_for_approval("test")


def test_prompt_for_approval_reads_y(monkeypatch) -> None:
    monkeypatch.setattr(sys.stdin, "isatty", lambda: True)
    monkeypatch.setattr("builtins.input", lambda _prompt: "y")
    assert shared_checkout.prompt_for_approval("test")


def test_prompt_for_approval_reads_n(monkeypatch) -> None:
    monkeypatch.setattr(sys.stdin, "isatty", lambda: True)
    monkeypatch.setattr("builtins.input", lambda _prompt: "n")
    assert not shared_checkout.prompt_for_approval("test")
