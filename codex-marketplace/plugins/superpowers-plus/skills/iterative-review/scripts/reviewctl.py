#!/usr/bin/env python3
"""reviewctl: the single version-2 review control plane.

This CLI is the only mutation authority for version-2 (schema_version 2)
review state. It is experimental until the cutover plan; version-1 reviews
continue through next_node.py. All commands except ``doctor`` take
``--state`` pointing at a review-state.json file.

Mutation commands (``init --apply``, ``dispatch``, ``complete``, ``block``,
``resume``) run only on the Devin Desktop runtime; on any other harness they
report ``unsupported-runtime`` and exit 1 without creating or mutating
state. ``status``, ``next``, ``validate``, and ``doctor`` are read-only and
run on any runtime; ``doctor`` exits 1 with ``verdict: inert`` off Devin
Desktop.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from review_core import engine, model, policy, store  # noqa: E402


USAGE_ERRORS = 2


def _fail(message: str, code: int = 1) -> int:
    print(message, file=sys.stderr)
    return code


def _emit(obj: dict, json_mode: bool) -> int:
    if json_mode:
        print(json.dumps(obj, indent=2, sort_keys=True))
    else:
        for key, value in obj.items():
            if isinstance(value, (dict, list)):
                value = json.dumps(value, sort_keys=True)
            print(f"{key}: {value}")
    return 0


def _decision_obj(result: engine.EngineResult) -> dict:
    d = result.decision
    obj = {
        "allowed": d.allowed,
        "action": d.action,
        "reason": d.reason,
        "missing": list(d.missing),
        "generation": result.generation,
        "state": str(result.state_path),
    }
    if d.status is not None:
        obj["status"] = d.status
    if d.recipe is not None:
        obj["recipe"] = {
            "dispatch_required": d.recipe.dispatch_required,
            "required_role": d.recipe.required_role,
            "minimum_capability_tier": d.recipe.minimum_capability_tier,
            "minimum_reasoning_floor": d.recipe.minimum_reasoning_floor,
            "preferred_profile": d.recipe.preferred_profile,
            "data_keys": list(d.recipe.data_keys),
            "evidence_kinds": list(d.recipe.evidence_kinds),
            "record_command": d.recipe.record_command,
        }
    return obj


def _schema_version_of(path: Path):
    """Read a state file's schema_version without imposing v2 validity."""
    try:
        raw = path.read_bytes()
    except OSError:
        return "missing"
    try:
        obj = model.strict_json_loads(raw, source=str(path))
    except Exception:
        return "unparseable"
    if isinstance(obj, dict):
        return obj.get("schema_version")
    return "unparseable"


def _require_v2_state(path: Path) -> int:
    """Exit 1 unless ``path`` holds a version-2 state; version-1 or legacy
    files are routed back to the legacy toolchain."""
    version = _schema_version_of(path)
    if version == model.SCHEMA_VERSION:
        return 0
    if version == "missing":
        return _fail(f"state-missing: no state file at {path}")
    if version == "unparseable":
        return _fail(f"state-invalid: {path} is not a JSON object")
    return _fail(f"state-version: {path} is a version-1 review state; version-2 control lives only in reviewctl")


def _runtime_gate() -> int:
    runtime = engine.detect_runtime()
    if runtime == engine.RUNTIME_DEVIN_DESKTOP:
        return 0
    return _fail(f"unsupported-runtime: version-2 mutations require devin-desktop (detected {runtime})")


def _sources() -> engine.WitnessSources:
    return engine.load_witness_sources()


def _parse_evidence_specs(specs) -> tuple:
    out = []
    for spec in specs or ():
        parts = spec.split("=", 2)
        if len(parts) != 3:
            raise model.StateValidationError(
                "bad-usage",
                "evidence-file",
                f"expected alias=kind=absolute-path, got {spec!r}",
            )
        alias, kind, path = parts
        if not path:
            raise model.StateValidationError("bad-usage", "evidence-file", f"empty path in {spec!r}")
        out.append(engine.EvidenceSource(alias=alias, kind=kind, path=Path(path)))
    return tuple(out)


def _cmd_doctor(args, json_mode: bool) -> int:
    runtime = engine.detect_runtime()
    supported = runtime == engine.RUNTIME_DEVIN_DESKTOP
    obj = {
        "runtime": runtime,
        "supported": supported,
        "verdict": "pass" if supported else "inert",
    }
    _emit(obj, json_mode)
    return 0 if supported else 1


def _cmd_init(args, json_mode: bool) -> int:
    gate = _runtime_gate()
    if gate:
        return gate
    if not args.apply:
        result = engine.init_review(
            Path(args.state),
            review_id=args.review_id,
            scratch_dir=Path(args.scratch_dir).resolve(),
            apply=False,
        )
        return _emit(_decision_obj(result), json_mode)
    result = engine.init_review(
        Path(args.state),
        review_id=args.review_id,
        scratch_dir=Path(args.scratch_dir).resolve(),
        apply=True,
    )
    return _emit(_decision_obj(result), json_mode)


def _cmd_status(args, json_mode: bool) -> int:
    bad = _require_v2_state(Path(args.state))
    if bad:
        return bad
    state = store.load_state(Path(args.state))
    findings = state["findings"]
    open_findings = sum(1 for f in findings.values() if f["disposition"] in ("open", "unassessed"))
    obj = {
        "schema_version": state["schema_version"],
        "review_id": state["review_id"],
        "generation": state["generation"],
        "status": state["status"],
        "stage": state["stage"],
        "counts": {
            "findings": len(findings),
            "open_findings": open_findings,
            "dispatches": len(state["dispatches"]),
            "active_blockers": sum(1 for b in state["blockers"].values() if b["active"]),
            "witness_records": len(state["witness_records"]),
            "checks": len(state["checks"]),
        },
        "green_seal": state["green_seal"] is not None,
        "ready_transition": (state["ready_transition"]["status"] if state["ready_transition"] else None),
        "state": str(Path(args.state)),
    }
    return _emit(obj, json_mode)


def _cmd_next(args, json_mode: bool) -> int:
    bad = _require_v2_state(Path(args.state))
    if bad:
        return bad
    result = engine.next_action_for(Path(args.state), policies=_sources().policies)
    return _emit(_decision_obj(result), json_mode)


def _cmd_dispatch(args, json_mode: bool) -> int:
    gate = _runtime_gate()
    if gate:
        return gate
    if not args.apply:
        return _fail(
            f"BLOCKED: dispatch --action {args.action} requires --apply to mutate version-2 state",
            USAGE_ERRORS,
        )
    bad = _require_v2_state(Path(args.state))
    if bad:
        return bad
    sources = _sources()
    registered = engine.register_dispatch_transaction(Path(args.state), action=args.action, sources=sources)
    if not registered.decision.allowed:
        _emit(_decision_obj(registered), json_mode)
        return 1
    state = store.load_state(Path(args.state))
    role = policy.action_recipe(args.action).required_role
    dispatch_id = engine.find_pending_dispatch_id(state, role)
    if dispatch_id is None:
        # A pending dispatch may already be launched; nothing left to do.
        return _emit(_decision_obj(registered), json_mode)
    launched = engine.launch_transaction(Path(args.state), dispatch_id=dispatch_id, sources=sources)
    _emit(_decision_obj(launched), json_mode)
    return 0 if launched.decision.allowed else 1


def _cmd_complete(args, json_mode: bool) -> int:
    gate = _runtime_gate()
    if gate:
        return gate
    if not args.apply:
        return _fail(
            f"BLOCKED: complete --action {args.action} requires --apply to mutate version-2 state",
            USAGE_ERRORS,
        )
    bad = _require_v2_state(Path(args.state))
    if bad:
        return bad
    caller_data = b"{}"
    if args.data_file:
        caller_data = Path(args.data_file).read_bytes()
    caller_evidence = _parse_evidence_specs(args.evidence_file)
    result = engine.complete_transaction(
        Path(args.state),
        action=args.action,
        caller_data_bytes=caller_data,
        caller_evidence=caller_evidence,
        sources=_sources(),
    )
    _emit(_decision_obj(result), json_mode)
    return 0 if result.decision.allowed else 1


def _cmd_block(args, json_mode: bool) -> int:
    gate = _runtime_gate()
    if gate:
        return gate
    if not args.apply:
        return _fail(
            "BLOCKED: block requires --apply to mutate version-2 state",
            USAGE_ERRORS,
        )
    bad = _require_v2_state(Path(args.state))
    if bad:
        return bad
    evidence = _parse_evidence_specs(args.evidence_file)
    result = engine.block_transaction(
        Path(args.state),
        blocker_class=args.blocker_class,
        reason=args.reason,
        evidence=evidence,
        sources=_sources(),
    )
    _emit(_decision_obj(result), json_mode)
    return 0 if result.decision.allowed else 1


def _cmd_resume(args, json_mode: bool) -> int:
    gate = _runtime_gate()
    if gate:
        return gate
    if not args.apply:
        return _fail(
            "BLOCKED: resume requires --apply to mutate version-2 state",
            USAGE_ERRORS,
        )
    bad = _require_v2_state(Path(args.state))
    if bad:
        return bad
    evidence = _parse_evidence_specs(args.evidence_file)
    result = engine.resume_transaction(
        Path(args.state),
        blocker_id=args.blocker_id,
        resolution_evidence=evidence,
        sources=_sources(),
    )
    _emit(_decision_obj(result), json_mode)
    return 0 if result.decision.allowed else 1


def _cmd_validate(args, json_mode: bool) -> int:
    bad = _require_v2_state(Path(args.state))
    if bad:
        return bad
    try:
        result = engine.validate_state_file(Path(args.state))
    except (model.StateValidationError, store.StoreError) as exc:
        _emit(
            {"valid": False, "error": str(exc), "state": str(Path(args.state))},
            json_mode,
        )
        return 1
    _emit(
        {
            "valid": True,
            "generation": result.generation,
            "state": str(result.state_path),
        },
        json_mode,
    )
    return 0


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="reviewctl",
        description=(
            "version-2 review control plane (experimental until cutover). "
            "The only mutation authority for schema_version-2 review state. "
            "(mixed)"
        ),
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help=(
            "self-check: parse arguments and exit 0 without touching files; "
            "subcommand arguments are validated at the parser level only, "
            "handlers are not run"
        ),
    )
    parser.add_argument("--json", action="store_true", help="emit one JSON object per command")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("doctor", help="report runtime detection and surface verdict")

    p = sub.add_parser("init", help="create a generation-0 intake state")
    p.add_argument("--state", required=True)
    p.add_argument("--review-id", required=True)
    p.add_argument("--scratch-dir", required=True)
    p.add_argument("--apply", action="store_true")

    p = sub.add_parser("status", help="read current state summary")
    p.add_argument("--state", required=True)

    p = sub.add_parser("next", help="report the next lawful action and recipe")
    p.add_argument("--state", required=True)

    p = sub.add_parser("dispatch", help="register and launch a reviewer dispatch")
    p.add_argument("--state", required=True)
    p.add_argument("--action", required=True)
    p.add_argument("--apply", action="store_true")

    p = sub.add_parser("complete", help="record completion of a lawful action")
    p.add_argument("--state", required=True)
    p.add_argument("--action", required=True)
    p.add_argument("--data-file")
    p.add_argument("--evidence-file", action="append", default=[])
    p.add_argument("--apply", action="store_true")

    p = sub.add_parser("block", help="open a blocker on the review")
    p.add_argument("--state", required=True)
    p.add_argument("--class", dest="blocker_class", required=True)
    p.add_argument("--reason", required=True)
    p.add_argument("--evidence-file", action="append", default=[])
    p.add_argument("--apply", action="store_true")

    p = sub.add_parser("resume", help="resolve the active blocker")
    p.add_argument("--state", required=True)
    p.add_argument("--blocker-id", required=True)
    p.add_argument("--evidence-file", action="append", default=[])
    p.add_argument("--apply", action="store_true")

    p = sub.add_parser("validate", help="validate a version-2 state file")
    p.add_argument("--state", required=True)

    return parser


_HANDLERS = {
    "doctor": _cmd_doctor,
    "init": _cmd_init,
    "status": _cmd_status,
    "next": _cmd_next,
    "dispatch": _cmd_dispatch,
    "complete": _cmd_complete,
    "block": _cmd_block,
    "resume": _cmd_resume,
    "validate": _cmd_validate,
}


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    json_mode = "--json" in argv
    if json_mode:
        argv = [a for a in argv if a != "--json"]
    parser = _build_parser()
    args = parser.parse_args(argv)
    if args.check:
        return 0
    if args.command is None:
        parser.print_help()
        return USAGE_ERRORS
    handler = _HANDLERS[args.command]
    try:
        return handler(args, json_mode)
    except model.StateValidationError as exc:
        return _fail(f"{exc.code}: {exc}")
    except store.StoreError as exc:
        return _fail(str(exc))
    except OSError as exc:
        return _fail(f"io-error: {exc}")


if __name__ == "__main__":
    sys.exit(main())
