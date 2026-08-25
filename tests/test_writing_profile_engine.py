from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "codex-marketplace" / "plugins" / "writing-pack" / "skills" / "writing-profile-engine"
STYLE = ROOT / "codex-marketplace" / "plugins" / "writing-pack" / "skills" / "writing-style"
PROFILE = STYLE / "references" / "profiles" / "fatigue" / "ai-prose-fatigue" / "patterns.json"
GOLDENS = PROFILE.with_name("goldens.json")
SCRIPTS = ENGINE / "scripts"


def _run(script: str, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPTS / script), *args],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=False,
    )


def _load_module(name: str):
    path = SCRIPTS / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize("script", ["discover_profiles.py", "validate_profiles.py", "evaluate_profile.py"])
def test_cli_help_is_available(script: str) -> None:
    result = _run(script, "--help")
    assert result.returncode == 0, result.stderr
    assert "usage:" in result.stdout.lower()


def test_discovery_is_lawful_recursive_stable_and_json_serializable(tmp_path: Path) -> None:
    lawful = tmp_path / "references" / "profiles" / "fatigue" / "sample"
    lawful.mkdir(parents=True)
    (lawful / "patterns.json").write_text(
        json.dumps({"profile_id": "sample-profile", "profile_kind": "fatigue", "version": "1.2.3", "patterns": []}),
        encoding="utf-8",
    )
    (tmp_path / "outside.json").write_text(
        json.dumps({"profile_id": "outside", "profile_kind": "fatigue", "version": "1.0.0", "patterns": []}),
        encoding="utf-8",
    )

    result = _run("discover_profiles.py", "--root", str(tmp_path), "--json")
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert [(item["id"], item["kind"], item["version"]) for item in payload["profiles"]] == [
        ("sample-profile", "fatigue", "1.2.3")
    ]
    assert payload["profiles"][0]["path"].replace("\\", "/").endswith(
        "references/profiles/fatigue/sample/patterns.json"
    )


def test_discovery_rejects_symlink_escape_when_supported(tmp_path: Path) -> None:
    profiles = tmp_path / "references" / "profiles"
    profiles.mkdir(parents=True)
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "patterns.json").write_text(
        json.dumps({"profile_id": "escaped", "profile_kind": "fatigue", "version": "1.0.0", "patterns": []}),
        encoding="utf-8",
    )
    link = profiles / "escape"
    try:
        link.symlink_to(outside, target_is_directory=True)
    except OSError:
        pytest.skip("directory symlinks are unavailable")

    result = _run("discover_profiles.py", "--root", str(tmp_path), "--json")
    assert result.returncode != 0
    assert "escape" in result.stderr.lower()


def test_default_validation_is_read_only_and_machine_readable() -> None:
    before = hashlib.sha256(PROFILE.read_bytes()).hexdigest()
    result = _run("validate_profiles.py", "--json")
    after = hashlib.sha256(PROFILE.read_bytes()).hexdigest()
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["status"] == "valid"
    assert before == after


def test_validation_reports_actionable_cross_reference_and_unsafe_field_errors(tmp_path: Path) -> None:
    profile_root = tmp_path / "references" / "profiles" / "fatigue" / "bad"
    profile_root.mkdir(parents=True)
    document = json.loads(PROFILE.read_text(encoding="utf-8"))
    document["patterns"][0]["source_ids"] = ["missing-source"]
    document["patterns"][0]["detector_score"] = 0.9
    (profile_root / "patterns.json").write_text(json.dumps(document), encoding="utf-8")
    (profile_root / "goldens.json").write_text(GOLDENS.read_text(encoding="utf-8"), encoding="utf-8")

    result = _run("validate_profiles.py", "--root", str(tmp_path), "--json")
    assert result.returncode != 0
    payload = json.loads(result.stdout)
    joined = "\n".join(payload["errors"])
    assert "patterns[0].source_ids" in joined
    assert "detector_score" in joined


def test_evaluator_is_deterministic_utf8_safe_read_only_and_typed(tmp_path: Path) -> None:
    source = tmp_path / "draft.txt"
    source.write_text(
        "It is worth noting that the café opens. It is important to remember that the café closes.",
        encoding="utf-8",
    )
    before = source.read_bytes()
    args = ("--profile", str(PROFILE), "--input", str(source), "--json")
    first = _run("evaluate_profile.py", *args)
    second = _run("evaluate_profile.py", *args)
    assert first.returncode == second.returncode == 0, first.stderr
    assert first.stdout == second.stdout
    payload = json.loads(first.stdout)
    assert payload["schema_version"] == 1
    assert payload["profile_id"] == "ai-prose-fatigue"
    assert payload["input_sha256"] == hashlib.sha256(before).hexdigest()
    assert payload["status"] in {"findings", "abstained", "clear"}
    assert source.read_bytes() == before
    assert all(
        set(finding) == {
            "type",
            "pattern_id",
            "evidence",
            "span",
            "rationale",
            "preserve_when",
            "repair",
            "confidence",
        }
        for finding in payload["findings"]
    )
    assert all(finding["type"] in {"observed", "candidate", "preserve", "repair", "abstain"} for finding in payload["findings"])
    assert not ({"detector_score", "authorship", "ai_probability"} & set(payload))


def test_empty_input_abstains() -> None:
    evaluate = _load_module("evaluate_profile")
    payload = evaluate.evaluate_text(PROFILE, "", context=None, voice_card=None)
    assert payload["status"] == "abstained"
    assert payload["findings"][0]["type"] == "abstain"


def test_all_goldens_return_the_declared_types_and_pattern_ids() -> None:
    evaluate = _load_module("evaluate_profile")
    goldens = json.loads(GOLDENS.read_text(encoding="utf-8"))
    for case in goldens["cases"]:
        payload = evaluate.evaluate_text(PROFILE, case["input"], context=case["context"], voice_card=None)
        actual = {(finding["type"], finding["pattern_id"]) for finding in payload["findings"]}
        expected = {
            (finding["type"], pattern_id)
            for finding in case["expected_findings"]
            for pattern_id in finding["pattern_ids"]
        }
        assert expected <= actual, case["id"]


def test_expired_profiles_downgrade_repair_to_candidate(tmp_path: Path) -> None:
    document = json.loads(PROFILE.read_text(encoding="utf-8"))
    for pattern in document["patterns"]:
        pattern["review_after"] = "2020-01-01"
    expired = tmp_path / "patterns.json"
    expired.write_text(json.dumps(document), encoding="utf-8")
    evaluate = _load_module("evaluate_profile")
    goldens = json.loads(GOLDENS.read_text(encoding="utf-8"))
    case = goldens["cases"][0]
    payload = evaluate.evaluate_text(expired, case["input"], context=case["context"], voice_card=None)
    assert {finding["type"] for finding in payload["findings"]} == {"candidate"}
    assert payload["warnings"]


def test_overlapping_findings_are_stably_ordered_and_spans_are_bounded() -> None:
    evaluate = _load_module("evaluate_profile")
    goldens = json.loads(GOLDENS.read_text(encoding="utf-8"))
    case = goldens["cases"][0]
    payload = evaluate.evaluate_text(PROFILE, case["input"], context=case["context"], voice_card=None)
    ids = [finding["pattern_id"] for finding in payload["findings"]]
    assert ids == sorted(ids)
    for finding in payload["findings"]:
        assert 0 <= finding["span"]["start"] <= finding["span"]["end"] <= len(case["input"])
