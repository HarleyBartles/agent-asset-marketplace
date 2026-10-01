from __future__ import annotations

import subprocess
import sys
from pathlib import Path


NORMALIZER = Path(__file__).resolve().parents[2] / "assets" / "normalization" / "normalize_text.py"


def run_normalizer(
    mode: str,
    *paths: Path,
    line_ending: str = "lf",
    final_newline: str = "ensure",
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(NORMALIZER),
            f"--{mode}",
            "--line-ending",
            line_ending,
            "--final-newline",
            final_newline,
            *(str(path) for path in paths),
        ],
        cwd=NORMALIZER.parents[4],
        text=True,
        capture_output=True,
        check=False,
    )


def test_check_reports_line_ending_drift_without_changing_bytes(tmp_path: Path) -> None:
    source = tmp_path / "two lines.txt"
    source.write_bytes(b"first\r\nsecond\r")

    result = run_normalizer("check", source)

    assert result.returncode == 1
    assert "needs normalization" in result.stdout.lower()
    assert source.read_bytes() == b"first\r\nsecond\r"


def test_apply_normalizes_lf_and_required_final_newline_idempotently(tmp_path: Path) -> None:
    source = tmp_path / "mixed endings.txt"
    source.write_bytes(b"first\r\nsecond\rthird")

    applied = run_normalizer("apply", source)
    checked = run_normalizer("check", source)
    reapplied = run_normalizer("apply", source)

    assert applied.returncode == 0, applied.stderr
    assert source.read_bytes() == b"first\nsecond\nthird\n"
    assert checked.returncode == 0, checked.stdout + checked.stderr
    assert reapplied.returncode == 0, reapplied.stderr
    assert "already normalized" in reapplied.stdout.lower()


def test_apply_supports_crlf_and_forbidding_a_final_newline(tmp_path: Path) -> None:
    source = tmp_path / "no final ending.txt"
    source.write_bytes(b"first\nsecond\r\n\n")

    result = run_normalizer("apply", source, line_ending="crlf", final_newline="forbid")

    assert result.returncode == 0, result.stderr
    assert source.read_bytes() == b"first\r\nsecond"


def test_apply_preserves_utf8_bom_and_paths_not_selected(tmp_path: Path) -> None:
    selected = tmp_path / "selected file.txt"
    unselected = tmp_path / "unselected file.txt"
    selected.write_bytes(b"\xef\xbb\xbftext\r")
    unselected.write_bytes(b"untouched\r\n")

    result = run_normalizer("apply", selected)

    assert result.returncode == 0, result.stderr
    assert selected.read_bytes() == b"\xef\xbb\xbftext\n"
    assert unselected.read_bytes() == b"untouched\r\n"


def test_apply_rejects_binary_and_undecodable_files_without_changing_them(tmp_path: Path) -> None:
    binary = tmp_path / "binary.dat"
    undecodable = tmp_path / "undecodable.txt"
    binary.write_bytes(b"data\x00\r\n")
    undecodable.write_bytes(b"\xff\xfe\x80")

    result = run_normalizer("apply", binary, undecodable)

    assert result.returncode == 2
    assert "binary" in result.stderr.lower()
    assert "utf-8" in result.stderr.lower()
    assert binary.read_bytes() == b"data\x00\r\n"
    assert undecodable.read_bytes() == b"\xff\xfe\x80"


def test_missing_paths_fail_without_creating_them(tmp_path: Path) -> None:
    missing = tmp_path / "missing file.txt"

    result = run_normalizer("apply", missing)

    assert result.returncode == 2
    assert "not a regular file" in result.stderr.lower()
    assert not missing.exists()
