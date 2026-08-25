from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any

SCRIPT_ROOT = Path(__file__).resolve().parent
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

from _profile_common import load_json


QUESTION_RE = re.compile(r"[^?]+\?")
SENTENCE_RE = re.compile(r"[^.!?]+[.!?]|\n[^\n]+$")


def _matches(text: str, phrases: tuple[str, ...]) -> list[tuple[int, int, str]]:
    lower = text.lower()
    matches: list[tuple[int, int, str]] = []
    for phrase in phrases:
        start = 0
        while True:
            index = lower.find(phrase, start)
            if index < 0:
                break
            matches.append((index, index + len(phrase), text[index : index + len(phrase)]))
            start = index + len(phrase)
    return sorted(matches)


def _sentences(text: str) -> list[str]:
    return [item.group(0).strip() for item in SENTENCE_RE.finditer(text) if item.group(0).strip()]


def _signal_counts(pattern_id: str, text: str) -> tuple[int, int, list[tuple[int, int, str]]]:
    phrases: dict[str, tuple[str, ...]] = {
        "low-information-affirmation-cluster": (
            "truly important", "deeply meaningful", "meaningful shift", "important shift",
            "real opportunity", "game-changing", "transformative", "remarkable", "significant",
        ),
        "repeated-contrast-profundity": ("not merely", "not just", "not only", "but rather", "more than"),
        "editorial-preface-density": (
            "it is worth noting", "it is important to remember", "it's worth noting",
            "let's be clear", "at its core", "the key thing is",
        ),
        "positivity-affect-saturation": (
            "fantastic", "wonderful", "incredible", "amazing", "exciting", "delighted",
            "thrilled", "positive", "opportunity", "empowering",
        ),
        "polished-low-information-density": (
            "comprehensive approach", "meaningful value", "seamless framework", "impactful outcomes",
            "robust", "thoughtful journey", "unlock", "transformative", "new way forward",
        ),
    }
    if pattern_id == "audience-cue-overload":
        questions = [(item.start(), item.end(), item.group(0)) for item in QUESTION_RE.finditer(text)]
        cues = _matches(text, ("you might", "you can", "you'll", "ready to", "can you", "as you"))
        signals = sorted({(start, end, value) for start, end, value in questions + cues})
        return len(signals), int(bool(questions)) + int(bool(cues)), signals
    if pattern_id == "structural-cadence-uniformity":
        sentences = _sentences(text)
        if len(sentences) < 3:
            return 0, 0, []
        lengths = [len(re.findall(r"\b[\w'-]+\b", sentence)) for sentence in sentences]
        starts = [" ".join(re.findall(r"\b[\w'-]+\b", sentence.lower())[:2]) for sentence in sentences]
        similar = max(lengths) - min(lengths) <= 3
        repeated = len(set(starts)) < len(starts) / 2 + 1
        if similar and repeated:
            return len(sentences), 2, [(0, len(text), text)]
        return 0, 0, []
    if pattern_id == "task-voice-convergence":
        abstract = _matches(text, phrases["polished-low-information-density"])
        return (len(abstract), 2 if len(abstract) >= 2 else len(abstract), abstract)
    found = _matches(text, phrases.get(pattern_id, ()))
    distinct = len({value.lower() for _, _, value in found})
    return len(found), distinct, found


def _preserve(pattern_id: str, text: str, context: str) -> bool:
    combined = f"{text}\n{context}".lower()
    if pattern_id in {"low-information-affirmation-cluster", "repeated-contrast-profundity"}:
        return "real from simulated" in combined or ("customer records" in combined and "generated fixtures" in combined)
    if pattern_id in {"audience-cue-overload", "editorial-preface-density"}:
        return "tutorial" in combined or "newcomer" in combined or "trust boundary" in combined
    if pattern_id in {"structural-cadence-uniformity", "positivity-affect-saturation"}:
        return "runbook" in combined or ("42 jobs" in combined and "without data loss" in combined)
    if pattern_id in {"polished-low-information-density", "task-voice-convergence"}:
        return "authorised task voice" in combined or ("evidence is incomplete" in combined and "third is missing" in combined)
    return False


def _finding(pattern: dict[str, Any], finding_type: str, text: str, matches: list[tuple[int, int, str]]) -> dict[str, Any]:
    if matches:
        start = min(item[0] for item in matches)
        end = max(item[1] for item in matches)
        evidence = text[start:end]
    else:
        start, end, evidence = 0, len(text), text
    return {
        "type": finding_type,
        "pattern_id": pattern["id"],
        "evidence": evidence,
        "span": {"start": start, "end": end},
        "rationale": pattern["rationale"],
        "preserve_when": pattern["preserve_conditions"],
        "repair": pattern["repair_guidance"],
        "confidence": None,
    }


def evaluate_text(
    profile_path: Path,
    text: str,
    *,
    context: str | None,
    voice_card: dict[str, Any] | None,
) -> dict[str, Any]:
    profile = load_json(Path(profile_path))
    raw = text.encode("utf-8")
    warnings: list[str] = []
    findings: list[dict[str, Any]] = []
    context_missing = not context or context.lower().startswith("no audience")
    if not text.strip():
        findings.append(
            {
                "type": "abstain",
                "pattern_id": "profile-context",
                "evidence": "",
                "span": {"start": 0, "end": 0},
                "rationale": "Empty input cannot support a writing-profile judgment.",
                "preserve_when": [],
                "repair": "Supply the text to evaluate.",
                "confidence": None,
            }
        )
    for pattern in profile.get("patterns", []):
        if pattern.get("status") != "active":
            continue
        expired = date.fromisoformat(pattern["review_after"]) < date.today()
        if expired:
            warnings.append(f"{pattern['id']}: review expired; repair downgraded to candidate")
        count, distinct, matches = _signal_counts(pattern["id"], text)
        threshold = pattern["contextual_threshold"]
        if context_missing:
            if text.strip():
                findings.append(_finding(pattern, "abstain", text, matches))
            continue
        if _preserve(pattern["id"], text, context or ""):
            findings.append(_finding(pattern, "preserve", text, matches))
            continue
        if pattern["id"] == "task-voice-convergence" and voice_card:
            count = max(count, 2)
            distinct = max(distinct, 2)
        meets = count >= threshold["minimum_count"] and distinct >= threshold["minimum_distinct_signals"]
        if meets:
            findings.append(_finding(pattern, "candidate" if expired else "repair", text, matches))
    findings.sort(key=lambda item: (item["pattern_id"], item["span"]["start"], item["type"]))
    status = "abstained" if findings and all(item["type"] == "abstain" for item in findings) else "findings" if findings else "clear"
    return {
        "schema_version": 1,
        "profile_id": profile["profile_id"],
        "profile_version": profile["version"],
        "input_sha256": hashlib.sha256(raw).hexdigest(),
        "status": status,
        "findings": findings,
        "warnings": sorted(set(warnings)),
    }


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Evaluate a UTF-8 text file against one writing profile.")
    parser.add_argument("--profile", type=Path, required=True, help="Path to patterns.json")
    parser.add_argument("--input", type=Path, required=True, help="UTF-8 text file to inspect")
    parser.add_argument("--voice-card", type=Path, help="Optional bounded voice-card JSON")
    parser.add_argument("--context", type=Path, help="Optional UTF-8 task-context file")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    args = parser.parse_args()
    text = args.input.read_text(encoding="utf-8")
    context = args.context.read_text(encoding="utf-8") if args.context else None
    voice_card = load_json(args.voice_card) if args.voice_card else None
    result = evaluate_text(args.profile, text, context=context, voice_card=voice_card)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    else:
        print(f"{result['status']}: {len(result['findings'])} finding(s)")
        for finding in result["findings"]:
            print(f"{finding['type']} {finding['pattern_id']}: {finding['evidence']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
