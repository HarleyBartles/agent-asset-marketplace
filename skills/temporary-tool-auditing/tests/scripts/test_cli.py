import pytest

from auditctl import main


def test_help_and_check_are_safe(capsys, tmp_path):
    with pytest.raises(SystemExit) as exit_code:
        main(["--help"])
    assert exit_code.value.code == 0
    assert "prepare" in capsys.readouterr().out
    with pytest.raises(SystemExit) as exit_code:
        main(["--help"])
    assert exit_code.value.code == 0
    assert "purge" in capsys.readouterr().out
    run = tmp_path / "missing"
    assert main(["status", "--run-dir", str(run), "--check"]) != 0
    output = capsys.readouterr().out
    assert "manifest-read-failed" in output
    assert not run.exists()


def test_ambiguous_devin_runtime_name_is_rejected(capsys, tmp_path):
    with pytest.raises(SystemExit) as exit_code:
        main(
            [
                "prepare",
                "--run-dir",
                str(tmp_path / "run"),
                "--runtime",
                "devin",
                "--project",
                str(tmp_path),
                "--question",
                "x",
                "--subject",
                "session:s1",
                "--detail",
                "status",
            ]
        )
    assert exit_code.value.code == 2
    assert "devin-desktop" in capsys.readouterr().err
    assert not (tmp_path / "run").exists()


def test_invalid_duration_returns_safe_error_and_does_not_write(tmp_path, capsys):
    code = main(
        [
            "prepare",
            "--run-dir",
            str(tmp_path / "run"),
            "--runtime",
            "codex",
            "--project",
            str(tmp_path),
            "--question",
            "x",
            "--subject",
            "session:s1",
            "--detail",
            "status",
            "--duration-minutes",
            "NaN",
            "--apply",
        ]
    )
    assert code != 0
    output = capsys.readouterr().out
    assert "invalid-duration" in output
    assert "NaN" not in output
    assert not (tmp_path / "run").exists()


def test_check_before_subcommand_cannot_be_overridden_into_apply(tmp_path, capsys):
    run = tmp_path / "run"
    code = main(
        [
            "--check",
            "prepare",
            "--run-dir",
            str(run),
            "--runtime",
            "codex",
            "--project",
            str(tmp_path / "project"),
            "--question",
            "prove calls",
            "--subject",
            "session:s1",
            "--detail",
            "status",
            "--apply",
        ]
    )
    assert code != 0
    assert "conflicting-modes" in capsys.readouterr().out
    assert not run.exists()


def test_verify_teardown_check_is_read_only(tmp_path, capsys, monkeypatch):
    from auditctl import execute
    from store import save_manifest

    run = tmp_path / "run"
    save_manifest(
        run,
        {
            "run_id": "run-1",
            "runtime": "codex",
            "project_root": str(tmp_path / "project"),
            "registration_state": "removed",
            "cleanup_required": True,
            "teardown_probe_started_at": 1,
            "teardown_probe_until": 100,
        },
    )

    def should_not_run(*args, **kwargs):
        raise AssertionError("check mode invoked recorder")

    monkeypatch.setattr("auditctl.subprocess.run", should_not_run)
    result = execute(
        {
            "operation": "verify-teardown",
            "run_dir": str(run),
            "check": True,
            "phase": "finish",
            "restart_confirmed": True,
            "canary_performed": True,
        },
        now=20,
    )
    assert result == {"applied": False, "operation": "verify-teardown"}
    assert '"cleanup_required":true' in (run / "manifest.json").read_text(encoding="utf-8")
