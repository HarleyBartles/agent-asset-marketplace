"""Runtime-specific hook payload normalization and registration templates."""

import shlex
import subprocess
import sys
from pathlib import Path


def _first(payload: dict, *names: str):
    for name in names:
        value = payload.get(name)
        if value is not None:
            return value
    return None


def normalize_event(runtime: str, payload: dict, detail: str) -> dict:
    runtime = runtime.lower()
    if runtime not in {"codex", "devin"}:
        raise ValueError("unsupported-runtime")
    raw_event = str(_first(payload, "hook_event_name", "event", "event_name") or "unknown").lower()
    if "pre" in raw_event or raw_event in {"before_tool_use", "tool_start"}:
        event = "pre"
    elif "post" in raw_event or raw_event in {"after_tool_use", "tool_end"}:
        event = "post"
    else:
        event = raw_event
    if runtime == "codex":
        arguments = _first(payload, "tool_input", "arguments")
        result = _first(payload, "tool_response", "tool_output", "result")
        session_id = _first(payload, "session_id")
        agent_id = _first(payload, "agent_id", "subagent_id")
        turn_id = _first(payload, "turn_id")
        call_id = _first(payload, "tool_use_id", "call_id")
        tool_name = _first(payload, "tool_name", "tool")
    else:
        arguments = _first(payload, "arguments", "tool_input", "input")
        result = _first(payload, "result", "tool_response", "tool_output")
        session_id = _first(payload, "session_id", "sessionId")
        agent_id = _first(payload, "agent_id", "agentId", "child_agent_id")
        turn_id = _first(payload, "prompt_id", "turn_id", "turnId")
        call_id = _first(payload, "tool_call_id", "call_id", "tool_use_id")
        tool_name = _first(payload, "tool", "tool_name", "name")

    status = "observed-unknown"
    if event == "post" and isinstance(result, dict):
        candidate = str(_first(result, "status", "outcome", "state") or "").lower()
        if candidate in {"success", "succeeded", "completed"}:
            status = "success"
        elif candidate in {"failure", "failed", "error"}:
            status = "failure"
        elif candidate in {"rejected", "denied"}:
            status = "rejected"
    normalized = {
        "event": event,
        "session_id": session_id,
        "agent_id": agent_id,
        "turn_id": turn_id,
        "call_id": call_id,
        "tool_name": tool_name,
        "arguments": arguments,
        "outcome_status": status,
    }
    if detail == "full-results" and event == "post" and result is not None:
        normalized["result"] = result
    return normalized


def render_handlers(runtime: str, recorder: Path) -> dict:
    """Render project-local handlers using this active Python interpreter."""
    runtime = runtime.lower()
    recorder = Path(recorder).resolve()
    argv = [sys.executable, str(recorder), "--run-dir", str(recorder.parent)]
    command = subprocess.list2cmdline(argv) if sys.platform == "win32" else shlex.join(argv)
    if runtime == "codex":
        return {
            event: [{"matcher": "", "hooks": [{"type": "command", "command": command}]}]
            for event in ("PreToolUse", "PostToolUse", "SubagentStart", "SubagentStop", "SessionStart", "SessionEnd")
        }
    if runtime == "devin":
        return {event: {"command": command} for event in ("PreToolUse", "PostToolUse", "SessionStart", "SessionEnd")}
    raise ValueError("unsupported-runtime")
