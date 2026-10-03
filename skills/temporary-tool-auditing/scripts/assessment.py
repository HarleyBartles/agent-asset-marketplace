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
        if record.get("event") not in {"pre", "post"}:
            return False
        if record.get("agent_id") is None:
            limitations.add("missing-agent-id")
            return False
        return record.get("agent_id") == subject["agent_id"]
    session_id = subject.get("session_id")
    if session_id is None:
        limitations.add("missing-subject-selector")
        return False
    if record.get("event") in {"pre", "post"} and not record.get("session_id"):
        limitations.add("missing-session-id")
        return False
    return record.get("session_id") == session_id


def assess(run: Path, subject: dict, parent_idle_confirmed: bool = False) -> dict:
    limitations: set[str] = set()
    try:
        manifest = load_manifest(Path(run))
    except AuditStoreError:
        return {
            "claim_supported": False,
            "claim_scope": "no observed tool attempts for the selected subject during verified coverage",
            "subject": subject,
            "detail": None,
            "intervals": [],
            "unresolved_count": 0,
            "coverage": {"verified": False, "gaps": [], "interval_count": 0},
            "health": [],
            "redactions": [],
            "attempt_count": 0,
            "paired_count": 0,
            "limitations": ["manifest-unreadable"],
        }
    runtime = manifest.get("runtime", "")
    records = _read_records(Path(run) / "events.jsonl", limitations)
    health = _read_records(Path(run) / "health.jsonl", limitations)
    extra_controls = _read_records(Path(run) / "controls.jsonl", limitations)
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
    completion_source = manifest.get("subject_completion_source")
    if runtime == "devin" and subject.get("kind") == "child":
        if not parent_idle_confirmed:
            limitations.add("devin-parent-idle-unconfirmed")
        dispatch_id = subject.get("dispatch_call_id")
        matching_dispatch_post = next(
            (
                item
                for item in records
                if item.get("run_id") == manifest.get("run_id")
                and item.get("call_id") == dispatch_id
                and item.get("event") == "post"
            ),
            None,
        )
        completion_at = matching_dispatch_post.get("received_at") if matching_dispatch_post else None
        completion_source = "matched-dispatch-post" if matching_dispatch_post else None
    elif subject.get("agent_id") is not None:
        matching_stop = next(
            (
                item
                for item in records
                if item.get("run_id") == manifest.get("run_id")
                and item.get("agent_id") == subject.get("agent_id")
                and item.get("event") == "subagentstop"
            ),
            None,
        )
        completion_at = matching_stop.get("received_at") if matching_stop else None
        completion_source = "matched-subagent-stop" if matching_stop else None
    if isinstance(completion_at, (int, float)) and valid_intervals:
        if not any(item["start"] <= completion_at <= item["end"] for item in valid_intervals):
            limitations.add("completion-outside-coverage")
    if any(item.get("end") < now - 1 for item in valid_intervals) and manifest.get("coverage_gaps"):
        limitations.add("coverage-gap")
    if manifest.get("coverage_gaps"):
        limitations.add("coverage-gap")
    if not isinstance(completion_at, (int, float)):
        limitations.add("subject-completion-unverified")

    manifest_controls = [item for item in manifest.get("controls", []) if isinstance(item, dict)]
    lifecycle_controls = [
        {
            "call_id": item.get("call_id"),
            "session_id": item.get("session_id"),
            "agent_id": item.get("agent_id"),
            "role": "lifecycle",
        }
        for item in records
        if item.get("control_operation") and item.get("call_id")
    ]
    all_controls = manifest_controls + extra_controls + lifecycle_controls

    def identity(item):
        return item.get("call_id"), item.get("session_id"), item.get("agent_id")

    control_identities = {identity(item) for item in all_controls if item.get("call_id") and item.get("session_id")}
    captured_control_identities = {
        key
        for key in control_identities
        if any(record.get("event") == "pre" and identity(record) == key for record in records)
    }
    positive_control_identities = {
        identity(item)
        for item in all_controls
        if item.get("call_id") and item.get("session_id") and item.get("role", "positive") == "positive"
    }
    if not (captured_control_identities & positive_control_identities):
        limitations.add("missing-positive-control")

    def is_control(item):
        return identity(item) in control_identities

    if runtime == "devin" and subject.get("kind") == "child":
        dispatch_id = subject.get("dispatch_call_id")
        dispatches = [
            item
            for item in records
            if item.get("run_id") == manifest.get("run_id")
            and str(item.get("tool_name", "")).lower() in {"run_subagent", "run subagent", "subagent_dispatch"}
            and item.get("call_id")
        ]
        start = next(
            (item for item in dispatches if item.get("call_id") == dispatch_id and item.get("event") == "pre"),
            None,
        )
        end = next(
            (item for item in dispatches if item.get("call_id") == dispatch_id and item.get("event") == "post"),
            None,
        )
        start_at = start.get("received_at") if start else None
        end_at = end.get("received_at") if end else None
        overlapping = any(
            item.get("call_id") != dispatch_id
            and item.get("event") == "pre"
            and isinstance(item.get("received_at"), (int, float))
            and isinstance(end_at, (int, float))
            and start_at <= item["received_at"] <= end_at
            for item in dispatches
        )
        if (
            not start
            or not end
            or not isinstance(start_at, (int, float))
            or not isinstance(end_at, (int, float))
            or overlapping
        ):
            limitations.add("devin-child-attribution-ambiguous")
            subject_records = []
        else:
            subject_records = [
                item
                for item in records
                if isinstance(item.get("received_at"), (int, float))
                and start_at <= item["received_at"] <= end_at
                and item.get("call_id") != dispatch_id
                and item.get("run_id") == manifest.get("run_id")
            ]
    else:
        subject_records = [
            item
            for item in records
            if item.get("run_id") == manifest.get("run_id")
            and not is_control(item)
            and _selected(item, subject, runtime, limitations)
        ]
    for item in subject_records:
        if item.get("event") in {"pre", "post"} and not item.get("session_id"):
            limitations.add("missing-session-id")
        if runtime == "devin" and item.get("event") in {"pre", "post"} and not item.get("turn_id"):
            limitations.add("missing-turn-id")
    selected = [item for item in subject_records if not is_control(item) and not item.get("control_operation")]
    pres: dict[str, dict] = {}
    posts: dict[str, dict] = {}
    interval_bounds = [(item["start"], item["end"]) for item in valid_intervals]

    def in_coverage(timestamp):
        return isinstance(timestamp, (int, float)) and any(start <= timestamp <= end for start, end in interval_bounds)

    for item in selected:
        if item.get("redactions"):
            limitations.add("redactions-present")
        call_id = item.get("call_id")
        if not call_id:
            limitations.add("missing-call-id")
            continue
        if item.get("event") == "pre":
            if not in_coverage(item.get("received_at")):
                continue
            if call_id in pres:
                limitations.add("duplicate-pre")
            pres[call_id] = item
        elif item.get("event") == "post":
            if not in_coverage(item.get("received_at")) and call_id not in pres:
                continue
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
    unresolved_count = len(pres.keys() - posts.keys()) + len(posts.keys() - pres.keys())
    redactions = sorted(
        {marker for item in subject_records for marker in item.get("redactions", []) if isinstance(marker, str)}
    )
    gaps = manifest.get("coverage_gaps", [])
    coverage_verified = bool(valid_intervals) and not gaps and "completion-outside-coverage" not in limitations
    return {
        "claim_supported": supported,
        "claim_scope": "no observed tool attempts for the selected subject during verified coverage",
        "attribution_assumptions": ["orchestrator-self-attested-idleness"]
        if runtime == "devin" and subject.get("kind") == "child" and parent_idle_confirmed
        else [],
        "completion_source": completion_source,
        "subject": subject,
        "detail": manifest.get("detail"),
        "intervals": valid_intervals,
        "unresolved_count": unresolved_count,
        "coverage": {"verified": coverage_verified, "gaps": gaps, "interval_count": len(valid_intervals)},
        "health": health,
        "redactions": redactions,
        "parent_idle_attestation": "orchestrator-self-attested"
        if runtime == "devin" and subject.get("kind") == "child" and parent_idle_confirmed
        else None,
        "attempt_count": attempts,
        "paired_count": paired,
        "outcome_statuses": {
            call_id: posts[call_id].get("outcome_status", "observed-unknown") for call_id in pres.keys() & posts.keys()
        },
        "limitations": sorted(limitations),
    }
