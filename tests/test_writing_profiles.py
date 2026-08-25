from __future__ import annotations

import hashlib
import json
import re
from datetime import date
from pathlib import Path
from typing import Any

import pytest


ROOT = Path(__file__).resolve().parents[1]
STYLE_ROOT = ROOT / "codex-marketplace" / "plugins" / "writing-pack" / "skills" / "writing-style"
FATIGUE_ROOT = STYLE_ROOT / "references" / "profiles" / "fatigue" / "ai-prose-fatigue"
VOICE_ROOT = STYLE_ROOT / "references" / "profiles" / "voice"
SOURCE_REGISTER = ROOT / "research" / "ai-prose-fatigue" / "source-register.json"
BLINDED_ROOT = ROOT / "tests" / "pressure" / "writing" / "blinded"

STABLE_ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FINDING_TYPES = {"observed", "candidate", "preserve", "repair", "abstain"}
EVIDENCE_CLASSES = {
    "well_supported_reader_fatigue",
    "plausible_emerging",
    "author_specific_preference",
    "weak_or_folk_heuristic",
}
PATTERN_STATUSES = {"active", "retired", "rejected"}
REQUIRED_PATTERN_FIELDS = {
    "id",
    "family",
    "rationale",
    "evidence_class",
    "contextual_threshold",
    "preserve_conditions",
    "repair_guidance",
    "source_ids",
    "limitations",
    "version",
    "reviewed_at",
    "review_after",
    "status",
}
UNSAFE_FIELD_NAMES = {
    "authorship",
    "authorship_score",
    "ai_probability",
    "detector_score",
    "evasion_score",
    "exact_token_ban",
    "exact_token_bans",
    "banned_tokens",
    "forbidden_words",
}
REQUIRED_FAMILIES = {
    "low_information_affirmation",
    "synthetic_profundity",
    "manufactured_conversationality",
    "editorial_throat_clearing",
    "predictable_cadence",
    "synthetic_affect",
    "semantic_emptiness",
    "voice_flattening",
}


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _walk_keys(value: Any) -> set[str]:
    if isinstance(value, dict):
        return set(value) | {key for child in value.values() for key in _walk_keys(child)}
    if isinstance(value, list):
        return {key for child in value for key in _walk_keys(child)}
    return set()


def _assert_iso_date(value: str) -> date:
    parsed = date.fromisoformat(value)
    assert parsed.isoformat() == value
    return parsed


def _assert_schema_value(schema: dict[str, Any], value: Any, path: str = "$") -> None:
    expected_type = schema.get("type")
    type_checks = {
        "object": lambda item: isinstance(item, dict),
        "array": lambda item: isinstance(item, list),
        "string": lambda item: isinstance(item, str),
        "integer": lambda item: isinstance(item, int) and not isinstance(item, bool),
        "boolean": lambda item: isinstance(item, bool),
    }
    if expected_type:
        assert type_checks[expected_type](value), f"{path} must be {expected_type}"

    if "const" in schema:
        assert value == schema["const"], f"{path} must equal {schema['const']!r}"
    if "enum" in schema:
        assert value in schema["enum"], f"{path} must be one of {schema['enum']!r}"
    if isinstance(value, str):
        if "minLength" in schema:
            assert len(value) >= schema["minLength"], f"{path} is too short"
        if "pattern" in schema:
            assert re.fullmatch(schema["pattern"], value), f"{path} has invalid format"
    if isinstance(value, list):
        if "minItems" in schema:
            assert len(value) >= schema["minItems"], f"{path} has too few items"
        if schema.get("uniqueItems"):
            encoded = [json.dumps(item, sort_keys=True) for item in value]
            assert len(encoded) == len(set(encoded)), f"{path} contains duplicate items"
        for index, item in enumerate(value):
            _assert_schema_value(schema.get("items", {}), item, f"{path}[{index}]")
    if isinstance(value, dict):
        properties = schema.get("properties", {})
        missing = set(schema.get("required", [])) - set(value)
        assert not missing, f"{path} is missing {sorted(missing)}"
        if schema.get("additionalProperties") is False:
            extras = set(value) - set(properties)
            assert not extras, f"{path} has unsupported fields {sorted(extras)}"
        for key, child in value.items():
            if key in properties:
                _assert_schema_value(properties[key], child, f"{path}.{key}")


@pytest.fixture(scope="module")
def patterns_document() -> dict[str, Any]:
    return _load_json(FATIGUE_ROOT / "patterns.json")


@pytest.fixture(scope="module")
def goldens_document() -> dict[str, Any]:
    return _load_json(FATIGUE_ROOT / "goldens.json")


def test_all_profile_json_parses_and_profile_ids_are_unique_and_stable() -> None:
    json_paths = sorted((STYLE_ROOT / "references" / "profiles").rglob("*.json"))
    assert json_paths

    documents = {path: _load_json(path) for path in json_paths}
    profile_ids = [document["profile_id"] for document in documents.values() if "profile_id" in document]

    assert profile_ids
    assert len(profile_ids) == len(set(profile_ids))
    assert all(STABLE_ID.fullmatch(profile_id) for profile_id in profile_ids)


def test_fatigue_patterns_follow_the_contextual_evidence_contract(patterns_document: dict[str, Any]) -> None:
    assert patterns_document["schema_version"] == 1
    assert patterns_document["profile_id"] == "ai-prose-fatigue"
    assert STABLE_ID.fullmatch(patterns_document["profile_id"])

    patterns = patterns_document["patterns"]
    pattern_ids = [pattern["id"] for pattern in patterns]
    assert len(pattern_ids) == len(set(pattern_ids))
    assert all(STABLE_ID.fullmatch(pattern_id) for pattern_id in pattern_ids)

    source_ids = {source["id"] for source in _load_json(SOURCE_REGISTER)["sources"]}
    for pattern in patterns:
        assert REQUIRED_PATTERN_FIELDS <= set(pattern)
        assert pattern["evidence_class"] in EVIDENCE_CLASSES
        assert pattern["status"] in PATTERN_STATUSES
        assert pattern["rationale"].strip()
        assert pattern["limitations"].strip()
        assert pattern["repair_guidance"].strip()
        assert pattern["preserve_conditions"] and all(item.strip() for item in pattern["preserve_conditions"])
        assert pattern["source_ids"] and set(pattern["source_ids"]) <= source_ids

        threshold = pattern["contextual_threshold"]
        assert set(threshold) == {"unit", "minimum_count", "minimum_distinct_signals", "decision_rule"}
        assert threshold["unit"] in {"draft", "paragraph", "section", "local_cluster"}
        assert threshold["minimum_count"] >= 1
        assert threshold["minimum_distinct_signals"] >= 1
        assert threshold["decision_rule"].strip()

        reviewed_at = _assert_iso_date(pattern["reviewed_at"])
        review_after = _assert_iso_date(pattern["review_after"])
        assert reviewed_at < review_after

    active_families = {pattern["family"] for pattern in patterns if pattern["status"] == "active"}
    assert REQUIRED_FAMILIES <= active_families


def test_profile_data_rejects_exact_token_bans_and_detector_scores(
    patterns_document: dict[str, Any], goldens_document: dict[str, Any]
) -> None:
    schema = _load_json(VOICE_ROOT / "voice-card.schema.json")
    default_voice = _load_json(VOICE_ROOT / "default-voice-card.json")

    for document in (patterns_document, goldens_document, schema, default_voice):
        assert not (_walk_keys(document) & UNSAFE_FIELD_NAMES)

    serialized = json.dumps((patterns_document, goldens_document, schema, default_voice)).lower()
    assert "ban every occurrence" not in serialized
    assert "detector evasion" not in serialized


def test_goldens_name_expected_finding_types_and_pattern_ids(
    patterns_document: dict[str, Any], goldens_document: dict[str, Any]
) -> None:
    pattern_ids = {pattern["id"] for pattern in patterns_document["patterns"]}
    case_ids: set[str] = set()

    for case in goldens_document["cases"]:
        assert STABLE_ID.fullmatch(case["id"])
        assert case["id"] not in case_ids
        case_ids.add(case["id"])
        assert case["expected_findings"]
        for finding in case["expected_findings"]:
            assert finding["type"] in FINDING_TYPES
            assert set(finding["pattern_ids"]) <= pattern_ids
            assert finding["pattern_ids"] or finding["type"] == "abstain"


def test_goldens_cover_clusters_preservation_boundaries_clarity_and_voice(
    patterns_document: dict[str, Any], goldens_document: dict[str, Any]
) -> None:
    active_ids = {pattern["id"] for pattern in patterns_document["patterns"] if pattern["status"] == "active"}
    coverage = {
        pattern_id: {
            finding["type"]
            for case in goldens_document["cases"]
            for finding in case["expected_findings"]
            if pattern_id in finding["pattern_ids"]
        }
        for pattern_id in active_ids
    }

    for pattern_id, finding_types in coverage.items():
        assert "repair" in finding_types, f"{pattern_id} lacks a positive cluster/repair case"
        assert "preserve" in finding_types, f"{pattern_id} lacks a legitimate-device preserve case"
        assert "abstain" in finding_types, f"{pattern_id} lacks a contextual boundary case"

    tags = {tag for case in goldens_document["cases"] for tag in case["tags"]}
    assert {"pattern-cluster", "legitimate-device", "clarity-protection", "author-voice-protection"} <= tags

    repair_cases = [
        case
        for case in goldens_document["cases"]
        if any(finding["type"] == "repair" for finding in case["expected_findings"])
    ]
    assert repair_cases
    assert all(case["expected_repair_principle"].strip() for case in repair_cases)


def test_voice_card_schema_is_bounded_and_default_card_conforms() -> None:
    schema = _load_json(VOICE_ROOT / "voice-card.schema.json")
    default_voice = _load_json(VOICE_ROOT / "default-voice-card.json")

    assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
    assert schema["additionalProperties"] is False
    assert set(schema["required"]) == {
        "schema_version",
        "profile_id",
        "version",
        "scope",
        "derivation",
        "tendencies",
        "choices",
        "limitations",
    }

    properties = set(schema["properties"])
    assert not (properties & {"source_text", "source_prose", "corpus", "identity", "personality", "demographics"})
    assert {"prefer", "avoid"} <= set(schema["properties"]["choices"]["properties"])

    tendency_properties = set(schema["properties"]["tendencies"]["properties"])
    assert {
        "sentence_range",
        "directness",
        "vocabulary_register",
        "tolerated_fragments",
        "rhetorical_devices",
        "formatting_norms",
    } <= tendency_properties

    _assert_schema_value(schema, default_voice)
    assert default_voice["derivation"]["source_retained"] is False
    assert default_voice["derivation"]["basis"] in {"current_task_text", "explicit_preferences", "synthetic_default"}
    assert not (_walk_keys(default_voice) & {"source_text", "source_prose", "corpus", "identity", "personality"})


def test_blinded_campaign_is_frozen_and_hides_the_judge_rubric_from_workers() -> None:
    campaign = _load_json(BLINDED_ROOT / "campaign.json")
    stimulus = BLINDED_ROOT / "stimulus.md"
    rubric = BLINDED_ROOT / "hidden-rubric.md"

    assert campaign["status"] == "frozen_unrun"
    assert campaign["repetitions_per_arm"] >= 3
    assert campaign["trial_route"]["fresh_context_per_trial"] is True
    assert campaign["trial_route"]["identical_across_arms"] is True
    assert campaign["artifacts"]["stimulus"]["sha256"] == _sha256(stimulus)
    assert campaign["artifacts"]["hidden_rubric"]["sha256"] == _sha256(rubric)
    assert campaign["artifacts"]["stimulus"]["worker_visible"] is True
    assert campaign["artifacts"]["hidden_rubric"]["worker_visible"] is False

    forbidden_worker_reads = {
        "tests/pressure/writing/blinded/hidden-rubric.md",
        "tests/pressure/writing/blinded/campaign.json",
        "tests/pressure/writing/blinded/results.md",
    }
    arms = {arm["id"]: arm for arm in campaign["arms"]}
    assert set(arms) == {"control-no-writing-style", "treatment-writing-style"}
    assert all(not (set(arm["worker_allowed_reads"]) & forbidden_worker_reads) for arm in arms.values())
    assert arms["control-no-writing-style"]["worker_allowed_reads"] == [
        "tests/pressure/writing/blinded/stimulus.md"
    ]
    assert arms["treatment-writing-style"]["writing_style_available"] is True
    assert arms["treatment-writing-style"]["writing_style_invoked"] is True

    thresholds = campaign["predeclared_thresholds"]
    assert thresholds["baseline_red"]["minimum_material_failures"] >= 2
    assert thresholds["baseline_red"]["out_of_trials"] == campaign["repetitions_per_arm"]
    assert thresholds["treatment_green"]["minimum_material_passes"] >= 2
    assert thresholds["treatment_green"]["out_of_trials"] == campaign["repetitions_per_arm"]
    assert thresholds["treatment_green"]["maximum_treatment_to_control_median_family_count_ratio"] <= 0.5
    assert thresholds["treatment_green"]["maximum_treatment_hard_factual_failures"] == 0


def test_blinded_stimulus_does_not_reveal_hidden_pattern_or_scoring_names() -> None:
    stimulus = (BLINDED_ROOT / "stimulus.md").read_text(encoding="utf-8").lower()

    hidden_names = REQUIRED_FAMILIES | {
        "low-information-affirmation-cluster",
        "repeated-contrast-profundity",
        "audience-cue-overload",
        "editorial-preface-density",
        "structural-cadence-uniformity",
        "positivity-affect-saturation",
        "polished-low-information-density",
        "task-voice-convergence",
        "hidden rubric",
        "pass threshold",
        "pattern score",
    }
    assert not {name for name in hidden_names if name.lower() in stimulus}
