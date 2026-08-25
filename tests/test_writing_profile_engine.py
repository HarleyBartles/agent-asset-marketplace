from __future__ import annotations

import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "codex-marketplace" / "plugins" / "writing-pack" / "skills" / "writing-profile-engine"
STYLE = ROOT / "codex-marketplace" / "plugins" / "writing-pack" / "skills" / "writing-style"
PROFILE = STYLE / "references" / "profiles" / "fatigue" / "ai-prose-fatigue" / "patterns.json"
GOLDENS = PROFILE.with_name("goldens.json")
SCRIPTS = ENGINE / "scripts"
INSTALLED_ENGINE = ROOT / ".agents" / "skills" / "writing-profile-engine"
PROFILE_SCHEMA = ENGINE / "assets" / "schemas" / "writing-profile.schema.json"
SOURCE_AUTHORITY = ENGINE / "references" / "source-authority.json"


def _run_from(scripts: Path, script: str, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(scripts / script), *args],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=False,
    )


def _run(script: str, *args: str) -> subprocess.CompletedProcess[str]:
    return _run_from(SCRIPTS, script, *args)


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


@pytest.mark.parametrize("script", ["discover_profiles.py", "validate_profiles.py", "evaluate_profile.py"])
def test_read_only_cli_check_mode_is_available(script: str) -> None:
    result = _run(script, "--check")
    assert result.returncode in {0, 1}, result.stderr


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
    assert (
        payload["profiles"][0]["path"].replace("\\", "/").endswith("references/profiles/fatigue/sample/patterns.json")
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


def test_discovery_enumerates_malformed_candidates_and_validation_reports_them(tmp_path: Path) -> None:
    profile_root = tmp_path / "references" / "profiles" / "fatigue" / "broken"
    profile_root.mkdir(parents=True)
    malformed = profile_root / "patterns.json"
    malformed.write_text('{"profile_id": ', encoding="utf-8")

    discovered = _run("discover_profiles.py", "--root", str(tmp_path), "--json")
    assert discovered.returncode == 0, discovered.stderr
    profiles = json.loads(discovered.stdout)["profiles"]
    assert len(profiles) == 1
    assert profiles[0]["status"] == "invalid"
    assert profiles[0]["path"].replace("\\", "/").endswith("broken/patterns.json")

    validated = _run("validate_profiles.py", "--root", str(tmp_path), "--json")
    assert validated.returncode == 1
    errors = "\n".join(json.loads(validated.stdout)["errors"])
    assert str(malformed) in errors
    assert "invalid UTF-8 JSON" in errors


def test_validation_enforces_executable_rules_thresholds_and_golden_coverage(tmp_path: Path) -> None:
    profile_root = tmp_path / "references" / "profiles" / "fatigue" / "bad-contract"
    profile_root.mkdir(parents=True)
    document = json.loads(PROFILE.read_text(encoding="utf-8"))
    pattern = document["patterns"][0]
    pattern.pop("rules", None)
    pattern["status"] = "unknown"
    pattern["contextual_threshold"]["minimum_count"] = 0
    (profile_root / "patterns.json").write_text(json.dumps(document), encoding="utf-8")
    goldens = json.loads(GOLDENS.read_text(encoding="utf-8"))
    goldens["cases"] = [case for case in goldens["cases"] if case["expected_classification"] != "preserve"]
    (profile_root / "goldens.json").write_text(json.dumps(goldens), encoding="utf-8")

    result = _run("validate_profiles.py", "--root", str(tmp_path), "--json")
    assert result.returncode == 1
    errors = "\n".join(json.loads(result.stdout)["errors"])
    assert ".rules" in errors
    assert ".status" in errors
    assert "minimum_count" in errors
    assert "missing golden coverage" in errors


def test_profile_schema_accepts_canonical_data_and_rejects_missing_rules() -> None:
    schema = json.loads(PROFILE_SCHEMA.read_text(encoding="utf-8"))
    document = json.loads(PROFILE.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    assert not list(validator.iter_errors(document))

    document["patterns"][0].pop("rules")
    errors = list(validator.iter_errors(document))
    assert errors
    assert any("rules" in error.message for error in errors)


def test_bundled_source_authority_matches_the_canonical_research_register() -> None:
    bundled = json.loads(SOURCE_AUTHORITY.read_text(encoding="utf-8"))
    register = ROOT / "research" / "ai-prose-fatigue" / "source-register.json"
    canonical = json.loads(register.read_text(encoding="utf-8"))
    assert {item["id"] for item in bundled["sources"]} == {item["id"] for item in canonical["sources"]}


def test_validation_reports_nested_type_errors_without_traceback(tmp_path: Path) -> None:
    profile_root = tmp_path / "references" / "profiles" / "fatigue" / "bad-types"
    profile_root.mkdir(parents=True)
    document = json.loads(PROFILE.read_text(encoding="utf-8"))
    document["patterns"][0]["source_ids"] = [{"not": "a source id"}]
    document["patterns"][0]["rules"][0]["phrases"] = [{"not": "a phrase"}]
    (profile_root / "patterns.json").write_text(json.dumps(document), encoding="utf-8")
    (profile_root / "goldens.json").write_text(GOLDENS.read_text(encoding="utf-8"), encoding="utf-8")

    result = _run("validate_profiles.py", "--root", str(tmp_path), "--json")
    assert result.returncode == 1
    assert "Traceback" not in result.stderr
    errors = "\n".join(json.loads(result.stdout)["errors"])
    assert "source_ids" in errors
    assert "phrases" in errors


def test_installed_and_standalone_validation_are_self_contained(tmp_path: Path) -> None:
    installed = _run_from(INSTALLED_ENGINE / "scripts", "validate_profiles.py", "--json")
    assert installed.returncode == 0, installed.stderr
    assert json.loads(installed.stdout)["profiles_checked"] >= 1

    standalone_engine = tmp_path / "writing-profile-engine"
    shutil.copytree(ENGINE, standalone_engine)
    standalone_profiles = tmp_path / "references" / "profiles" / "fatigue" / "sample"
    standalone_profiles.mkdir(parents=True)
    shutil.copy2(PROFILE, standalone_profiles / "patterns.json")
    shutil.copy2(GOLDENS, standalone_profiles / "goldens.json")
    standalone = _run_from(
        standalone_engine / "scripts",
        "validate_profiles.py",
        "--root",
        str(tmp_path),
        "--json",
    )
    assert standalone.returncode == 0, standalone.stderr
    assert json.loads(standalone.stdout)["profiles_checked"] == 1


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
        set(finding)
        == {
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
    assert all(
        finding["type"] in {"observed", "candidate", "preserve", "repair", "abstain"} for finding in payload["findings"]
    )
    assert not ({"detector_score", "authorship", "ai_probability"} & set(payload))


def test_empty_input_abstains() -> None:
    evaluate = _load_module("evaluate_profile")
    payload = evaluate.evaluate_text(PROFILE, "", context=None, voice_card=None)
    assert payload["status"] == "abstained"
    assert payload["findings"][0]["type"] == "abstain"


def test_voice_card_presence_never_manufactures_divergence(tmp_path: Path) -> None:
    evaluate = _load_module("evaluate_profile")
    plain = "The maintenance window starts at 09:00. Staff should save their work before 08:55."
    unsupported_card = {"directness": "plain"}
    payload = evaluate.evaluate_text(
        PROFILE,
        plain,
        context="An operational notice for staff who need the time and action.",
        voice_card=unsupported_card,
    )
    voice = [item for item in payload["findings"] if item["pattern_id"] == "task-voice-convergence"]
    assert not any(item["type"] == "repair" for item in voice)
    assert voice and voice[0]["type"] == "abstain"


def test_unprovenanced_voice_tendencies_abstain_even_when_a_field_is_supported() -> None:
    evaluate = _load_module("evaluate_profile")
    partial_card = {"tendencies": {"directness": "high", "vocabulary_register": ["plain"]}}
    payload = evaluate.evaluate_text(
        PROFILE,
        "It is worth noting that our comprehensive approach unlocks meaningful value.",
        context="A staff notice requiring a direct, plain statement.",
        voice_card=partial_card,
    )
    voice = [item for item in payload["findings"] if item["pattern_id"] == "task-voice-convergence"]
    assert voice and voice[0]["type"] == "abstain"


def test_supported_voice_card_fields_are_compared_to_observable_prose() -> None:
    evaluate = _load_module("evaluate_profile")
    voice_card = json.loads(
        (STYLE / "references" / "profiles" / "voice" / "default-voice-card.json").read_text(encoding="utf-8")
    )
    voice_card["scope"]["task_boundary"] = "current_task"
    voice_card["derivation"].update(
        {
            "basis": "explicit_preferences",
            "authorization": "explicit_user_preference",
            "retention_boundary": "no_source_storage",
        }
    )
    voice_card["tendencies"]["directness"] = "high"
    voice_card["tendencies"]["vocabulary_register"] = ["plain"]
    text = "It is worth noting that our comprehensive approach unlocks meaningful value."
    payload = evaluate.evaluate_text(
        PROFILE,
        text,
        context="A staff notice requiring a direct, plain statement.",
        voice_card=voice_card,
    )
    voice = [item for item in payload["findings"] if item["pattern_id"] == "task-voice-convergence"]
    assert voice and voice[0]["type"] == "repair"
    assert "worth noting" in voice[0]["evidence"].lower()


def test_custom_profile_rules_drive_evaluation_without_known_pattern_ids(tmp_path: Path) -> None:
    document = json.loads(PROFILE.read_text(encoding="utf-8"))
    pattern = document["patterns"][0]
    pattern["id"] = "custom-data-driven-pattern"
    pattern["contextual_threshold"].update({"unit": "section", "minimum_count": 2, "minimum_distinct_signals": 2})
    pattern["rules"] = [
        {
            "id": "custom-phrases",
            "kind": "normalized_phrase_occurrence",
            "phrases": ["purple comet", "silver orchard"],
        }
    ]
    pattern["preserve_predicates"] = []
    document["patterns"] = [pattern]
    custom = tmp_path / "patterns.json"
    custom.write_text(json.dumps(document), encoding="utf-8")
    evaluate = _load_module("evaluate_profile")

    payload = evaluate.evaluate_text(
        custom,
        "A PURPLE   comet crossed the silver orchard.",
        context="A reader-facing section where ornamental repetition is not useful.",
        voice_card=None,
    )
    assert [(item["type"], item["pattern_id"]) for item in payload["findings"]] == [
        ("repair", "custom-data-driven-pattern")
    ]


def test_declared_paragraph_repetition_rule_drives_custom_profile(tmp_path: Path) -> None:
    document = json.loads(PROFILE.read_text(encoding="utf-8"))
    pattern = document["patterns"][0]
    pattern["id"] = "custom-paragraph-pattern"
    pattern["contextual_threshold"].update({"unit": "section", "minimum_count": 4, "minimum_distinct_signals": 2})
    pattern["contextual_threshold"].pop("window_words", None)
    pattern["rules"] = [
        {
            "id": "paragraph-shape",
            "kind": "paragraph_repetition",
            "minimum_paragraphs": 3,
            "opening_words": 2,
            "maximum_word_count_spread": 2,
        }
    ]
    pattern["preserve_predicates"] = []
    document["patterns"] = [pattern]
    custom = tmp_path / "patterns.json"
    custom.write_text(json.dumps(document), encoding="utf-8")
    evaluate = _load_module("evaluate_profile")
    text = "We ship updates today.\n\nWe ship reports today.\n\nWe ship notices today."

    payload = evaluate.evaluate_text(
        custom,
        text,
        context="A short reader-facing section whose hierarchy should be visible.",
        voice_card=None,
    )
    assert [(item["type"], item["pattern_id"]) for item in payload["findings"]] == [
        ("repair", "custom-paragraph-pattern")
    ]


def test_local_cluster_window_is_declared_data_not_a_pattern_id_shortcut(tmp_path: Path) -> None:
    document = json.loads(PROFILE.read_text(encoding="utf-8"))
    pattern = document["patterns"][0]
    pattern["id"] = "custom-local-cluster"
    pattern["contextual_threshold"].update(
        {"unit": "local_cluster", "minimum_count": 2, "minimum_distinct_signals": 2, "window_words": 5}
    )
    pattern["rules"] = [
        {
            "id": "cluster-phrases",
            "kind": "normalized_phrase_occurrence",
            "phrases": ["purple comet", "silver orchard"],
        }
    ]
    pattern["preserve_predicates"] = []
    document["patterns"] = [pattern]
    custom = tmp_path / "patterns.json"
    custom.write_text(json.dumps(document), encoding="utf-8")
    evaluate = _load_module("evaluate_profile")

    separated = evaluate.evaluate_text(
        custom,
        "Purple comet " + "word " * 12 + "silver orchard.",
        context="A reader-facing section.",
        voice_card=None,
    )
    clustered = evaluate.evaluate_text(
        custom,
        "Purple comet meets silver orchard.",
        context="A reader-facing section.",
        voice_card=None,
    )
    assert not separated["findings"]
    assert clustered["findings"][0]["type"] == "repair"


def test_preserve_requires_a_detected_signal_and_declared_predicate(tmp_path: Path) -> None:
    document = json.loads(PROFILE.read_text(encoding="utf-8"))
    pattern = document["patterns"][0]
    pattern["id"] = "custom-preserve-pattern"
    pattern["rules"] = [{"id": "term", "kind": "normalized_phrase_occurrence", "phrases": ["real"]}]
    pattern["preserve_predicates"] = [
        {
            "id": "precise-distinction",
            "kind": "all_phrases",
            "scope": "text_and_context",
            "phrases": ["real", "simulated"],
        }
    ]
    document["patterns"] = [pattern]
    custom = tmp_path / "patterns.json"
    custom.write_text(json.dumps(document), encoding="utf-8")
    evaluate = _load_module("evaluate_profile")

    without_signal = evaluate.evaluate_text(
        custom,
        "The environment uses generated fixtures.",
        context="Compare the real and simulated environments.",
        voice_card=None,
    )
    assert not without_signal["findings"]
    with_signal = evaluate.evaluate_text(
        custom,
        "The real environment uses records.",
        context="Compare the real and simulated environments.",
        voice_card=None,
    )
    assert with_signal["findings"][0]["type"] == "preserve"


def test_invalid_profile_fails_evaluation_without_traceback(tmp_path: Path) -> None:
    broken = tmp_path / "patterns.json"
    broken.write_text('{"profile_id": ', encoding="utf-8")
    source = tmp_path / "input.txt"
    source.write_text("Plain text.", encoding="utf-8")
    result = _run("evaluate_profile.py", "--profile", str(broken), "--input", str(source), "--json")
    assert result.returncode == 2
    assert str(broken) in result.stderr
    assert "Traceback" not in result.stderr


def test_all_goldens_return_the_declared_types_and_pattern_ids() -> None:
    evaluate = _load_module("evaluate_profile")
    goldens = json.loads(GOLDENS.read_text(encoding="utf-8"))
    for case in goldens["cases"]:
        payload = evaluate.evaluate_text(
            PROFILE,
            case["input"],
            context=case["context"],
            voice_card=case.get("voice_card"),
        )
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
