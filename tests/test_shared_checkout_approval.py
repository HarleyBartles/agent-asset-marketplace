from __future__ import annotations

import datetime
import sys
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import shared_checkout_approval


def _fake_git_dir(tmp_path: Path) -> Path:
    git_dir = tmp_path / ".git"
    git_dir.mkdir()
    (git_dir / "info").mkdir(parents=True)
    return git_dir


def test_approval_path_returns_expected_path(monkeypatch, tmp_path: Path) -> None:
    git_dir = _fake_git_dir(tmp_path)

    def fake_run(cmd, **kwargs):
        assert cmd == ["git", "rev-parse", "--git-dir"]
        return SimpleNamespace(stdout=str(git_dir), returncode=0, stderr="")

    monkeypatch.setattr(shared_checkout_approval.subprocess, "run", fake_run)
    path = shared_checkout_approval.approval_path(tmp_path, "test-script")
    assert path == git_dir / "info" / "devin-shared-checkout-approval-test-script"


def test_write_and_is_valid_round_trip(monkeypatch, tmp_path: Path) -> None:
    git_dir = _fake_git_dir(tmp_path)

    def fake_run(cmd, **kwargs):
        return SimpleNamespace(stdout=str(git_dir), returncode=0, stderr="")

    monkeypatch.setattr(shared_checkout_approval.subprocess, "run", fake_run)

    shared_checkout_approval.write(tmp_path, "test-script")
    assert shared_checkout_approval.is_valid(tmp_path, "test-script")


def test_consume_deletes_valid_token(monkeypatch, tmp_path: Path) -> None:
    git_dir = _fake_git_dir(tmp_path)

    def fake_run(cmd, **kwargs):
        return SimpleNamespace(stdout=str(git_dir), returncode=0, stderr="")

    monkeypatch.setattr(shared_checkout_approval.subprocess, "run", fake_run)

    shared_checkout_approval.write(tmp_path, "test-script")
    assert shared_checkout_approval.consume(tmp_path, "test-script")
    assert not shared_checkout_approval.is_valid(tmp_path, "test-script")
    assert not (git_dir / "info" / "devin-shared-checkout-approval-test-script").exists()


def test_consume_returns_false_for_missing_token(monkeypatch, tmp_path: Path) -> None:
    git_dir = _fake_git_dir(tmp_path)

    def fake_run(cmd, **kwargs):
        return SimpleNamespace(stdout=str(git_dir), returncode=0, stderr="")

    monkeypatch.setattr(shared_checkout_approval.subprocess, "run", fake_run)

    assert not shared_checkout_approval.consume(tmp_path, "test-script")


def test_is_valid_false_for_expired_token(monkeypatch, tmp_path: Path) -> None:
    git_dir = _fake_git_dir(tmp_path)

    def fake_run(cmd, **kwargs):
        return SimpleNamespace(stdout=str(git_dir), returncode=0, stderr="")

    monkeypatch.setattr(shared_checkout_approval.subprocess, "run", fake_run)

    shared_checkout_approval.write(tmp_path, "test-script")
    token_path = shared_checkout_approval.approval_path(tmp_path, "test-script")
    old = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(seconds=661)
    token_path.write_text(old.isoformat() + "\n", encoding="utf-8", newline="\n")

    assert not shared_checkout_approval.is_valid(tmp_path, "test-script")
    assert not shared_checkout_approval.consume(tmp_path, "test-script")


def test_consume_cleans_up_invalid_token(monkeypatch, tmp_path: Path) -> None:
    git_dir = _fake_git_dir(tmp_path)

    def fake_run(cmd, **kwargs):
        return SimpleNamespace(stdout=str(git_dir), returncode=0, stderr="")

    monkeypatch.setattr(shared_checkout_approval.subprocess, "run", fake_run)

    shared_checkout_approval.write(tmp_path, "test-script")
    token_path = shared_checkout_approval.approval_path(tmp_path, "test-script")
    token_path.write_text("not-a-timestamp", encoding="utf-8", newline="\n")

    assert not shared_checkout_approval.consume(tmp_path, "test-script")
    assert not token_path.exists()
