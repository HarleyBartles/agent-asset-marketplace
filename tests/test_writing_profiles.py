from __future__ import annotations

import copy
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
CLARITY_ROOT = ROOT / "codex-marketplace" / "plugins" / "writing-pack" / "skills" / "writing-with-clarity"
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


def _mandatory_reference_paths(skill_path: Path, section_heading: str) -> set[str]:
    content = skill_path.read_text(encoding="utf-8")
    section = content.split(section_heading, maxsplit=1)[1].split("\n## ", maxsplit=1)[0]
    return set(re.findall(r"`(references/[^`]+)`", section))


def _walk_keys(value: Any) -> set[str]:
    if isinstance(value, dict):
        return set(value) | {key for child in value.values() for key in _walk_keys(child)}
    if isinstance(value, list):
        return {key for child in value for key in _walk_keys(child)}
    return set()


def _normalized_tokens(value: str) -> set[str]:
    snake_value = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", value)
    return set(re.findall(r"[a-z0-9]+", snake_value.lower()))


def _is_negative_boundary(sentence: str) -> bool:
    return bool(
        re.search(
            r"\b(?:do|does|must|should)\s+not\b|\bnot\s+an?\b|"
            r"\bwithout\s+(?:assigning|calculating|concluding|providing|reporting|returning)\b",
            sentence,
        )
    )


def _has_universal_restriction_scope(sentence: str, tokens: set[str]) -> bool:
    if re.search(r"\bwithout\s+(?:any\s+)?exceptions?\b", sentence):
        return True
    if re.search(r"\b(?:if|unless|when)\b", sentence):
        return False
    universal_markers = {"all", "always", "any", "each", "every", "never"}
    inherently_universal_actions = {
        "ban",
        "banned",
        "disallow",
        "disallowed",
        "forbid",
        "forbidden",
        "prohibit",
        "prohibited",
    }
    return bool(tokens & (universal_markers | inherently_universal_actions))


def _semantic_categories(tokens: set[str], *, universal_restriction: bool = True) -> set[str]:
    categories: set[str] = set()
    lexical_targets = {
        "occurrence",
        "occurrences",
        "phrase",
        "phrases",
        "term",
        "terms",
        "token",
        "tokens",
        "vocabulary",
        "word",
        "words",
    }
    restriction_actions = {
        "ban",
        "banned",
        "block",
        "blocked",
        "delete",
        "deleted",
        "disallow",
        "disallowed",
        "eliminate",
        "eliminated",
        "exclude",
        "excluded",
        "forbid",
        "forbidden",
        "omit",
        "omitted",
        "prohibit",
        "prohibited",
        "remove",
        "removed",
        "strip",
        "stripped",
    }
    origin_subjects = {"ai", "authorship", "detector", "evasion", "llm", "model"}
    score_measures = {"confidence", "likelihood", "probability", "rating", "score"}
    authorship_judgments = {
        "assertion",
        "claim",
        "classification",
        "conclusion",
        "decision",
        "judgment",
        "label",
        "result",
        "verdict",
    }

    restriction_action_present = bool(tokens & restriction_actions or {"never", "use"} <= tokens)
    if universal_restriction and tokens & lexical_targets and restriction_action_present:
        categories.add("universal_token_restriction")
    if tokens & origin_subjects and tokens & score_measures:
        categories.add("origin_or_detector_score")
    if "authorship" in tokens and tokens & authorship_judgments:
        categories.add("authorship_judgment")
    return categories


def _semantic_violations(value: Any, path: str = "$") -> list[str]:
    """Apply the profile contract's bounded semantic-category grammar recursively."""
    violations: list[str] = []

    if isinstance(value, dict):
        for key, child in value.items():
            snake_key = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", key)
            normalized_key = re.sub(r"[^a-z0-9]+", "_", snake_key.lower()).strip("_")
            if normalized_key in UNSAFE_FIELD_NAMES or _semantic_categories(_normalized_tokens(key)):
                violations.append(f"{path}.{key}: prohibited key semantics")
            violations.extend(_semantic_violations(child, f"{path}.{key}"))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            violations.extend(_semantic_violations(child, f"{path}[{index}]"))
    elif isinstance(value, str):
        sentences = re.split(r"(?<=[.!?;])\s+|\n+", value.lower())
        for sentence in sentences:
            tokens = _normalized_tokens(sentence)
            categories = _semantic_categories(
                tokens,
                universal_restriction=_has_universal_restriction_scope(sentence, tokens),
            )
            authorship_assertion = bool(
                tokens
                & {
                    "assert",
                    "asserted",
                    "classify",
                    "classified",
                    "conclude",
                    "concluded",
                    "determine",
                    "determined",
                    "label",
                    "labeled",
                }
                and tokens & {"ai", "authorship", "authored", "generated", "llm", "written"}
            )
            if not _is_negative_boundary(sentence) and (categories or authorship_assertion):
                violations.append(f"{path}: prohibited affirmative semantics")

    return violations


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
    if isinstance(value, int) and not isinstance(value, bool):
        if "minimum" in schema:
            assert value >= schema["minimum"], f"{path} is below minimum"
        if "maximum" in schema:
            assert value <= schema["maximum"], f"{path} is above maximum"
    if isinstance(value, str):
        if "minLength" in schema:
            assert len(value) >= schema["minLength"], f"{path} is too short"
        if "maxLength" in schema:
            assert len(value) <= schema["maxLength"], f"{path} is too long"
        if "pattern" in schema:
            assert re.fullmatch(schema["pattern"], value), f"{path} has invalid format"
    if isinstance(value, list):
        if "minItems" in schema:
            assert len(value) >= schema["minItems"], f"{path} has too few items"
        if "maxItems" in schema:
            assert len(value) <= schema["maxItems"], f"{path} has too many items"
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

    for index, subschema in enumerate(schema.get("allOf", [])):
        _assert_schema_value(subschema, value, f"{path}.allOf[{index}]")

    condition = schema.get("if")
    if condition is not None:
        try:
            _assert_schema_value(condition, value, path)
        except AssertionError:
            if "else" in schema:
                _assert_schema_value(schema["else"], value, path)
        else:
            if "then" in schema:
                _assert_schema_value(schema["then"], value, path)


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
        assert not _semantic_violations(document)


@pytest.mark.parametrize(
    "unsafe_fixture",
    [
        {"policy": {"never_use_tokens": ["delve"]}},
        {"policy": {"bannedWords": ["delve"]}},
        {"policy": {"forbidden_phrases": ["in conclusion"]}},
        {"policy": {"blocked_words": ["delve"]}},
        {"policy": {"disallowed_vocabulary": ["delve"]}},
        {"metrics": {"ai_likelihood": 0.92}},
        {"metrics": {"aiLikelihood": 0.92}},
        {"metrics": {"detector_confidence": 0.81}},
        {"metrics": {"llm_detection_score": 0.81}},
        {"result": {"authorship_verdict": "AI-generated"}},
        {"result": {"authorshipConclusion": "AI-authored"}},
        {"result": {"authorship_result": "AI-authored"}},
        {"rationale": "Conclude that this passage was written by AI."},
        {"rationale": "Label this draft as AI-authored."},
        {"rationale": "Report an authorship probability of 0.8."},
        {"repair_guidance": "Remove every occurrence of delve."},
        {"repair_guidance": "Words such as delve should always be removed."},
        {"repair_guidance": "Without exception, remove every occurrence of delve."},
        {"repair_guidance": "Without any exceptions, always delete the term delve."},
        {"repair_guidance": "Never use the term delve."},
    ],
)
def test_prohibited_semantic_aliases_are_rejected_recursively(unsafe_fixture: dict[str, Any]) -> None:
    assert _semantic_violations(unsafe_fixture)


@pytest.mark.parametrize(
    "legitimate_fixture",
    [
        {"rationale": "This is not an authorship claim."},
        {"limitations": "Do not provide detector scores, authorship conclusions, or exact-token bans."},
        {"repair_guidance": "Preserve the word when it carries precise meaning."},
        {"repair_guidance": "Use precise words when facts permit."},
        {"repair_guidance": "Remove repeated words only when they obscure meaning."},
        {"repair_guidance": "Use specific terms if evidence supports them."},
        {"repair_guidance": "Remove repeated phrases when they obscure the point."},
        {"repair_guidance": "Omit repeated terms only if the sentence stays clear."},
        {"repair_guidance": "Always use precise words."},
        {"repair_guidance": "Use any precise term that the facts support."},
    ],
)
def test_prohibited_semantic_check_preserves_legitimate_boundary_prose(
    legitimate_fixture: dict[str, Any],
) -> None:
    assert not _semantic_violations(legitimate_fixture)


def test_profile_contract_documents_bounded_universal_restriction_scope() -> None:
    contract = " ".join((STYLE_ROOT / "references" / "profile-contract.md").read_text(encoding="utf-8").lower().split())

    assert "without exception" in contract
    assert "contextual qualifiers such as `if`, `when`, and `unless`" in contract


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


def test_voice_card_schema_couples_synthetic_default_provenance() -> None:
    schema = _load_json(VOICE_ROOT / "voice-card.schema.json")
    default_voice = _load_json(VOICE_ROOT / "default-voice-card.json")

    invalid_cards = []
    for path, invalid_value in (
        (("scope", "task_boundary"), "current_task"),
        (("derivation", "authorization"), "current_task_user"),
        (("derivation", "sample_count"), 1),
        (("derivation", "retention_boundary"), "task_memory_only"),
    ):
        card = copy.deepcopy(default_voice)
        card[path[0]][path[1]] = invalid_value
        invalid_cards.append(card)

    for card in invalid_cards:
        with pytest.raises(AssertionError):
            _assert_schema_value(schema, card)


def test_voice_card_schema_couples_current_task_text_provenance() -> None:
    schema = _load_json(VOICE_ROOT / "voice-card.schema.json")
    default_voice = _load_json(VOICE_ROOT / "default-voice-card.json")
    current_task_card = copy.deepcopy(default_voice)
    current_task_card["profile_id"] = "current-task-voice"
    current_task_card["scope"]["task_boundary"] = "current_task"
    current_task_card["derivation"].update(
        {
            "basis": "current_task_text",
            "authorization": "current_task_user",
            "sample_count": 1,
            "source_retained": False,
            "retention_boundary": "no_source_storage",
        }
    )
    _assert_schema_value(schema, current_task_card)

    invalid_cards = []
    for path, invalid_value in (
        (("scope", "task_boundary"), "synthetic_example"),
        (("derivation", "authorization"), "synthetic_fixture"),
        (("derivation", "sample_count"), 0),
        (("derivation", "retention_boundary"), "task_memory_only"),
    ):
        card = copy.deepcopy(current_task_card)
        card[path[0]][path[1]] = invalid_value
        invalid_cards.append(card)

    for card in invalid_cards:
        with pytest.raises(AssertionError):
            _assert_schema_value(schema, card)


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
    assert arms["control-no-writing-style"]["worker_allowed_reads"] == ["tests/pressure/writing/blinded/stimulus.md"]
    assert arms["treatment-writing-style"]["writing_style_available"] is True
    assert arms["treatment-writing-style"]["writing_style_invoked"] is True

    thresholds = campaign["predeclared_thresholds"]
    assert thresholds["baseline_red"]["minimum_material_failures"] >= 2
    assert thresholds["baseline_red"]["out_of_trials"] == campaign["repetitions_per_arm"]
    assert thresholds["treatment_green"]["minimum_material_passes"] >= 2
    assert thresholds["treatment_green"]["out_of_trials"] == campaign["repetitions_per_arm"]
    assert thresholds["treatment_green"]["maximum_treatment_to_control_median_family_count_ratio"] <= 0.5
    assert thresholds["treatment_green"]["maximum_treatment_hard_factual_failures"] == 0


def test_blinded_campaign_pins_intervention_and_goldens_before_output() -> None:
    campaign = _load_json(BLINDED_ROOT / "campaign.json")
    assert campaign["campaign_version"] == "1.3.0"
    assert campaign["prospective_freeze"] == {
        "correction_round": 3,
        "correction_scope": "pre_output_review_findings",
        "worker_outputs_existed_before_refreeze": False,
        "arms_run_before_refreeze": False,
    }
    treatment = next(arm for arm in campaign["arms"] if arm["id"] == "treatment-writing-style")
    intervention_paths = set(treatment["worker_allowed_reads"]) - {"tests/pressure/writing/blinded/stimulus.md"}
    pinned_intervention = {artifact["path"]: artifact["sha256"] for artifact in campaign["treatment_artifacts"]}

    assert set(pinned_intervention) == intervention_paths
    for path, expected_hash in pinned_intervention.items():
        assert _sha256(ROOT / path) == expected_hash

    goldens = campaign["evaluator_goldens"]
    assert goldens["path"] == (
        "codex-marketplace/plugins/writing-pack/skills/writing-style/"
        "references/profiles/fatigue/ai-prose-fatigue/goldens.json"
    )
    assert _sha256(ROOT / goldens["path"]) == goldens["sha256"]

    verification = campaign["pre_output_verification"]
    assert verification["required"] is True
    assert verification["algorithm"] == "sha256"
    assert verification["timing"] == "before_any_worker_output"
    assert verification["on_mismatch"] == "abort_without_running_trials"


def test_treatment_campaign_pins_complete_mandatory_clarity_route() -> None:
    campaign = _load_json(BLINDED_ROOT / "campaign.json")
    treatment = next(arm for arm in campaign["arms"] if arm["id"] == "treatment-writing-style")
    allowed_reads = set(treatment["worker_allowed_reads"])
    pinned_reads = {artifact["path"] for artifact in campaign["treatment_artifacts"]}
    route = campaign["clarity_recheck"]

    writing_style_skill = STYLE_ROOT / "SKILL.md"
    assert "$writing-with-clarity" in writing_style_skill.read_text(encoding="utf-8")

    clarity_skill_relative = "codex-marketplace/plugins/writing-pack/skills/writing-with-clarity/SKILL.md"
    mandatory_references = _mandatory_reference_paths(CLARITY_ROOT / "SKILL.md", "## Read in bounded layers")
    routed_primary = route["primary_reference"]
    assert Path(routed_primary).name in (CLARITY_ROOT / "references" / "routing.md").read_text(encoding="utf-8")
    assert route["routing_reference"] == "references/routing.md"
    assert route["final_edit_reference"] == "references/final-edit.md"

    required_reads = {clarity_skill_relative} | {
        f"codex-marketplace/plugins/writing-pack/skills/writing-with-clarity/{path}"
        for path in mandatory_references | {routed_primary}
    }
    assert required_reads <= allowed_reads
    assert required_reads <= pinned_reads
    assert route["optional_secondary_reference"] is None


def test_hidden_rubric_requires_output_evidence_without_excluding_unsupported_signals() -> None:
    rubric = " ".join((BLINDED_ROOT / "hidden-rubric.md").read_text(encoding="utf-8").lower().split())

    assert "a signal is supported only when tied to a supplied fact or direct concrete consequence" not in rubric
    assert "quote evidence from the output" in rubric
    assert "assess its support against the supplied facts" in rubric
    assert "unsupported or unearned language can satisfy" in rubric


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
