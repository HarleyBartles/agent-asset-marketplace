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


def test_is_main_shared_checkout_true_for_main_worktree(monkeypatch, tmp_path: Path) -> None:
    git_dir = _fake_git_dir(tmp_path)
    monkeypatch.setattr(shared_checkout.subprocess, "run", _make_fake_run(git_dir, git_dir))
    assert shared_checkout.is_main_shared_checkout(tmp_path)


def test_is_main_shared_checkout_false_for_linked_worktree(monkeypatch, tmp_path: Path) -> None:
    git_dir = tmp_path / ".git" / "worktrees" / "feature"
    git_dir.mkdir(parents=True)
    (git_dir / "info").mkdir(parents=True)
    common_dir = tmp_path / ".git"
    monkeypatch.setattr(shared_checkout.subprocess, "run", _make_fake_run(git_dir, common_dir))
    assert not shared_checkout.is_main_shared_checkout(tmp_path)


def test_approve_mutation_allowed_in_normal_checkout(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(shared_checkout, "is_main_shared_checkout", lambda _root: False)
    assert shared_checkout.approve_mutation(tmp_path, "test", flag_approved=False)


def test_approve_mutation_allowed_with_flag_in_shared_checkout(monkeypatch, tmp_path: Path, capsys) -> None:
    monkeypatch.setattr(shared_checkout, "is_main_shared_checkout", lambda _root: True)
    assert shared_checkout.approve_mutation(tmp_path, "test", flag_approved=True)
    captured = capsys.readouterr()
    assert "--allow-shared-checkout supplied" in captured.err


def test_shared_checkout_on_other_branch_requires_flag(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(shared_checkout, "is_main_shared_checkout", lambda _root: True)
    monkeypatch.setattr(shared_checkout, "_current_branch", lambda _root: "feature", raising=False)
    assert not shared_checkout.approve_mutation(tmp_path, "test", flag_approved=False)


def test_interactive_shared_checkout_still_requires_flag(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(shared_checkout, "is_main_shared_checkout", lambda _root: True)
    monkeypatch.setattr(shared_checkout, "prompt_for_approval", lambda _name: True, raising=False)
    assert not shared_checkout.approve_mutation(tmp_path, "test", flag_approved=False)


def test_approve_mutation_denies_without_flag(monkeypatch, tmp_path: Path, capsys) -> None:
    monkeypatch.setattr(shared_checkout, "is_main_shared_checkout", lambda _root: True)
    assert not shared_checkout.approve_mutation(tmp_path, "test", flag_approved=False)
    captured = capsys.readouterr()
    assert "refusing to apply" in captured.err


def test_all_shared_checkout_copies_match_canonical() -> None:
    """Every vendored/projected copy of shared_checkout.py must be byte-identical to tools/shared_checkout.py."""
    repo_root = Path(__file__).resolve().parents[1]
    canonical = repo_root / "tools" / "shared_checkout.py"
    canonical_bytes = canonical.read_bytes()

    search_roots = [
        repo_root / "sources" / "first_party" / "skills",
        repo_root / "adapters",
        repo_root / ".agents" / "skills",
        repo_root / "codex-marketplace" / "plugins",
    ]
    copies = []
    for root in search_roots:
        if not root.is_dir():
            continue
        for candidate in root.rglob("shared_checkout.py"):
            if candidate.is_file() and candidate.resolve() != canonical.resolve():
                copies.append(candidate)

    mismatches = [str(c) for c in copies if c.read_bytes() != canonical_bytes]
    assert not mismatches, f"stale shared_checkout.py copies: {mismatches}"
