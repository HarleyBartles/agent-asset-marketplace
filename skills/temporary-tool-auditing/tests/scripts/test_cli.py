import pytest

from auditctl import main


def test_help_and_check_are_safe(capsys, tmp_path):
    with pytest.raises(SystemExit) as exit_code:
        main(["--help"])
    assert exit_code.value.code == 0
    assert "prepare" in capsys.readouterr().out
    run = tmp_path / "missing"
    assert main(["status", "--run-dir", str(run), "--check"]) != 0
    output = capsys.readouterr().out
    assert "manifest-read-failed" in output
    assert not run.exists()


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
