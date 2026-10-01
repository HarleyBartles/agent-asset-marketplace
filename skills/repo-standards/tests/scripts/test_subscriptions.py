from __future__ import annotations

import json
import subprocess
import importlib.util
import sys
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator


REPO = Path(__file__).resolve().parents[4]
SCRIPT = REPO / "skills/repo-standards/scripts/subscriptions.py"
SCHEMA_PATH = REPO / "skills/repo-standards/references/subscriptions.schema.json"
_SPEC = importlib.util.spec_from_file_location("subscriptions", SCRIPT)
assert _SPEC and _SPEC.loader
subscriptions = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(subscriptions)


def record(standard_id: str = "repo-private", commit: str = "a" * 40) -> dict:
    return {
        "version": 2,
        "standards": [
            {
                "id": standard_id,
                "source": {
                    "repository": "https://example.com/private.git",
                    "commit": commit,
                    "definition": "rules/standard.md",
                },
                "certification": ".agents/contracts/certification.md#private",
            }
        ],
    }


@pytest.fixture(scope="module")
def schema_validator() -> Draft202012Validator:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


def test_pinned_repo_owned_standard_does_not_need_current_catalog() -> None:
    assert subscriptions.validate_record(record()) == []


def test_floating_authority_is_rejected() -> None:
    assert subscriptions.validate_record(record(commit="main"))


def test_legacy_commands_are_not_v2_authority() -> None:
    raw = record()
    raw["standards"][0]["check"] = ["python", "sentinel.py"]
    assert subscriptions.validate_record(raw)


def test_full_64_character_commit_is_supported() -> None:
    assert subscriptions.validate_record(record(commit="b" * 64)) == []


def test_empty_selection_is_valid() -> None:
    assert subscriptions.validate_record({"version": 2, "standards": []}) == []


def test_integral_json_number_version_matches_schema(schema_validator: Draft202012Validator) -> None:
    raw = {"version": 2.0, "standards": []}
    assert schema_validator.is_valid(raw)
    assert subscriptions.validate_record(raw) == []


@pytest.mark.parametrize(
    "raw",
    [
        {"version": 2, "standards": [record()["standards"][0], record()["standards"][0]]},
        {"version": 2, "standards": [None]},
        {"version": 2, "standards": [{**record()["standards"][0], "source": None}]},
        {"version": 2, "standards": [record()["standards"][0], {"id": "other"}]},
        {"version": 2, "standards": [], "check": ["python", "run.py"]},
        {"version": 2, "standards": [{**record()["standards"][0], "certification": "a.md#"}]},
        {"version": 2, "standards": [{**record()["standards"][0], "id": "Upper-case"}]},
        {"version": True, "standards": []},
    ],
)
def test_invalid_records_match_schema_and_checker(raw: object, schema_validator: Draft202012Validator) -> None:
    assert subscriptions.validate_record(raw)
    assert not schema_validator.is_valid(raw)


@pytest.mark.parametrize(
    "relative",
    ["../escape.md", "folder/../escape.md", "C:relative.md", "C:/absolute.md", "\\\\server\\share\\file.md"],
)
def test_unsafe_paths_are_rejected(relative: str) -> None:
    assert subscriptions.validate_relative_path(relative)


@pytest.mark.parametrize(
    ("relative", "field"),
    [
        ("../escape.md", "definition"),
        ("folder/../escape.md", "definition"),
        ("C:relative.md", "definition"),
        ("C:/absolute.md", "definition"),
        ("\\\\server\\share\\file.md", "definition"),
        ("folder\\file.md", "definition"),
        ("folder//file.md", "definition"),
        ("folder/./file.md", "definition"),
        ("folder/", "definition"),
        ("/absolute.md", "definition"),
        ("folder:a.md", "definition"),
        ("cert.md#", "certification"),
        ("cert.md#part#other", "certification"),
    ],
)
def test_path_rules_match_schema_and_checker(relative: str, field: str, schema_validator: Draft202012Validator) -> None:
    raw = record()
    if field == "definition":
        raw["standards"][0]["source"]["definition"] = relative
        assert subscriptions.validate_relative_path(relative)
    else:
        raw["standards"][0]["certification"] = relative
        assert subscriptions.validate_relative_path(relative, allow_fragment=True)

    assert subscriptions.validate_record(raw)
    assert not schema_validator.is_valid(raw)


def test_valid_records_match_schema_and_checker(schema_validator: Draft202012Validator) -> None:
    assert schema_validator.is_valid(record())
    assert subscriptions.validate_record(record()) == []
    empty = {"version": 2, "standards": []}
    assert schema_validator.is_valid(empty)
    assert subscriptions.validate_record(empty) == []


def test_checker_rejects_repeated_id_even_when_source_rows_differ(schema_validator: Draft202012Validator) -> None:
    raw = record()
    duplicate = dict(raw["standards"][0])
    duplicate["certification"] = ".agents/contracts/another.md#private"
    raw["standards"].append(duplicate)

    assert subscriptions.validate_record(raw)
    # Standard JSON Schema compares entire array values; the checker adds ID-level uniqueness.
    assert schema_validator.is_valid(raw)


def test_selected_standards_require_root_agents_and_certification(tmp_path: Path) -> None:
    path = tmp_path / ".agents/contracts/operating-standards.json"
    path.parent.mkdir(parents=True)
    path.write_text(json.dumps(record()), encoding="utf-8")

    findings = subscriptions.check_repository(tmp_path)

    assert any("AGENTS.md" in finding for finding in findings)
    assert any("certification.md" in finding for finding in findings)


def test_empty_selection_needs_no_root_agents_or_certificate(tmp_path: Path) -> None:
    path = tmp_path / ".agents/contracts/operating-standards.json"
    path.parent.mkdir(parents=True)
    path.write_text(json.dumps({"version": 2, "standards": []}), encoding="utf-8")

    assert subscriptions.check_repository(tmp_path) == []


def test_legacy_record_is_reported_without_rewriting(tmp_path: Path) -> None:
    path = tmp_path / ".agents/contracts/operating-standards.json"
    path.parent.mkdir(parents=True)
    before = b'{"version":1,"standards":[]}'
    path.write_bytes(before)

    findings = subscriptions.check_repository(tmp_path)

    assert any("legacy" in finding.lower() for finding in findings)
    assert path.read_bytes() == before


def test_malformed_json_is_a_diagnostic(tmp_path: Path) -> None:
    path = tmp_path / ".agents/contracts/operating-standards.json"
    path.parent.mkdir(parents=True)
    path.write_text("{", encoding="utf-8")

    assert subscriptions.check_repository(tmp_path)


@pytest.mark.parametrize(
    ("raw", "valid"),
    [(record(), True), (record(commit="main"), False), ({"version": 2, "standards": []}, True)],
)
def test_schema_and_checker_have_matching_authority_rules(
    raw: object, valid: bool, schema_validator: Draft202012Validator
) -> None:
    assert schema_validator.is_valid(raw) is valid
    assert bool(subscriptions.validate_record(raw)) is (not valid)


def _snapshot(root: Path) -> dict[str, bytes]:
    return {path.relative_to(root).as_posix(): path.read_bytes() for path in root.rglob("*") if path.is_file()}


@pytest.mark.parametrize("mode", ["valid", "missing", "legacy"])
def test_cli_never_mutates_consumer_or_executes_declared_commands(tmp_path: Path, mode: str) -> None:
    consumer = tmp_path / "consumer"
    consumer.mkdir()
    sentinel = tmp_path / "executed.txt"
    command = [sys.executable, "-c", f"from pathlib import Path; Path({str(sentinel)!r}).write_text('ran')"]

    if mode != "missing":
        contract = consumer / ".agents/contracts/operating-standards.json"
        contract.parent.mkdir(parents=True)
        if mode == "valid":
            (consumer / "AGENTS.md").write_text("route", encoding="utf-8")
            certificate = consumer / ".agents/contracts/certification.md"
            certificate.write_text("certification", encoding="utf-8")
            raw = record()
            raw["standards"][0]["certification"] = ".agents/contracts/certification.md#private"
        else:
            raw = {"version": 1, "standards": [], "check": command}
        contract.write_text(json.dumps(raw), encoding="utf-8")

    before = _snapshot(consumer)
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--repo-root", str(consumer), "--check"],
        capture_output=True,
        text=True,
        check=False,
    )

    if mode == "valid":
        assert result.returncode == 0, result.stdout + result.stderr
        assert "semantic certification is not assessed" in result.stdout.lower()
    else:
        assert result.returncode == 1
    assert _snapshot(consumer) == before
    assert not sentinel.exists()


def test_bare_check_uses_current_directory_and_returns_one_for_missing_record(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)

    assert subscriptions.main(["--check"]) == 1
