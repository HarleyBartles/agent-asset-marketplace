"""Assess bounded hook evidence without upgrading absence into universal proof."""

import json
import time
from pathlib import Path

from store import AuditStoreError, load_manifest


def _read_records(path: Path, limitations: set[str]) -> list[dict]:
    if not path.exists():
        return []
    records = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except Exception:
        limitations.add("record-log-unreadable")
        return []
    for line in lines:
        try:
            value = json.loads(line)
            if not isinstance(value, dict):
                raise ValueError
            records.append(value)
        except Exception:
            limitations.add("malformed-or-truncated-record")
    return records


def _selected(record: dict, subject: dict, runtime: str, limitations: set[str]) -> bool:
    if subject.get("agent_id") is not None:
        if runtime == "devin":
            return False
        if record.get("agent_id") is None:
            limitations.add("missing-agent-id")
            return False
        return record.get("agent_id") == subject["agent_id"]
    session_id = subject.get("session_id")
    if session_id is None:
        limitations.add("missing-subject-selector")
        return False
    return record.get("session_id") == session_id


def assess(run: Path, subject: dict) -> dict:
    limitations: set[str] = set()
    try:
        manifest = load_manifest(Path(run))
    except AuditStoreError:
        return {
            "claim_supported": False,
            "attempt_count": 0,
            "paired_count": 0,
            "limitations": ["manifest-unreadable"],
        }
    runtime = manifest.get("runtime", "")
    records = _read_records(Path(run) / "events.jsonl", limitations)
    health = _read_records(Path(run) / "health.jsonl", limitations)
    health.extend(item for item in manifest.get("health", []) if isinstance(item, dict))
    if health:
        limitations.add("recorder-health-failure")
    if not manifest.get("activation_verified"):
        limitations.add("activation-unverified")
    intervals = manifest.get("intervals", [])
    now = time.time()
    valid_intervals = [
        item
        for item in intervals
        if isinstance(item, dict)
        and isinstance(item.get("start"), (int, float))
        and isinstance(item.get("end"), (int, float))
        and item["end"] >= item["start"]
    ]
    if not valid_intervals:
        limitations.add("no-verified-coverage")
    completion_at = manifest.get("subject_completed_at")
    if isinstance(completion_at, (int, float)) and valid_intervals:
        if not any(item["start"] <= completion_at <= item["end"] for item in valid_intervals):
            limitations.add("completion-outside-coverage")
    if any(item.get("end") < now - 1 for item in valid_intervals) and manifest.get("coverage_gaps"):
        limitations.add("coverage-gap")
    if manifest.get("coverage_gaps"):
        limitations.add("coverage-gap")
    if not manifest.get("subject_completed_at"):
        limitations.add("subject-completion-unverified")

    control_ids = {
        item.get("call_id") for item in manifest.get("controls", []) if isinstance(item, dict) and item.get("call_id")
    }
    captured_control_ids = {
        item.get("call_id")
        for item in records
        if item.get("run_id") == manifest.get("run_id")
        and item.get("event") == "pre"
        and item.get("call_id") in control_ids
    }
    if not captured_control_ids:
        limitations.add("missing-positive-control")

    if runtime == "devin" and subject.get("kind") == "child":
        dispatches = manifest.get("dispatches", [])
        if not dispatches or any(
            not item.get("serialized") or not item.get("start") or not item.get("end") for item in dispatches
        ):
            limitations.add("devin-child-attribution-ambiguous")
            subject_records = []
        else:
            chosen = dispatches[-1]
            subject_records = [
                item
                for item in records
                if isinstance(item.get("received_at"), (int, float))
                and chosen["start"] <= item["received_at"] <= chosen["end"]
                and item.get("run_id") == manifest.get("run_id")
            ]
            if len(dispatches) > 1 and not manifest.get("unidentified_producers_excluded"):
                limitations.add("devin-child-attribution-ambiguous")
    else:
        subject_records = [
            item
            for item in records
            if item.get("run_id") == manifest.get("run_id") and _selected(item, subject, runtime, limitations)
        ]
    selected = [item for item in subject_records if item.get("call_id") not in control_ids]
    pres: dict[str, dict] = {}
    posts: dict[str, dict] = {}
    for item in selected:
        if item.get("redactions"):
            limitations.add("redactions-present")
        call_id = item.get("call_id")
        if not call_id:
            limitations.add("missing-call-id")
            continue
        if item.get("event") == "pre":
            if call_id in pres:
                limitations.add("duplicate-pre")
            pres[call_id] = item
        elif item.get("event") == "post":
            if call_id in posts:
                limitations.add("duplicate-post")
            posts[call_id] = item
    for call_id in pres.keys() - posts.keys():
        limitations.add("unmatched-pre")
    for call_id in posts.keys() - pres.keys():
        limitations.add("unmatched-post")
    attempts = len(pres)
    paired = len(pres.keys() & posts.keys())
    if attempts:
        limitations.add("tool-attempts-observed")
    supported = not limitations
    return {
        "claim_supported": supported,
        "claim_scope": "no observed tool attempts for the selected subject during verified coverage",
        "attempt_count": attempts,
        "paired_count": paired,
        "outcome_statuses": {
            call_id: posts[call_id].get("outcome_status", "observed-unknown") for call_id in pres.keys() & posts.keys()
        },
        "limitations": sorted(limitations),
    }
