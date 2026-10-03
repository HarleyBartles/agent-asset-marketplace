"""Runtime-specific hook payload normalization and registration templates."""

import shlex
import os
import subprocess
import sys
from pathlib import Path


def _first(payload: dict, *names: str):
    for name in names:
        value = payload.get(name)
        if value is not None:
            return value
    return None


def normalize_event(
    runtime: str,
    payload: dict,
    detail: str,
    run_dir: str | Path | None = None,
    lifecycle_cli_path: str | Path | None = None,
) -> dict:
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
        if runtime == "devin" and "success" in result and isinstance(result["success"], bool):
            if result.get("error"):
                status = "failure"
            else:
                status = "success" if result["success"] else "failure"
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
    control_operation = _auditctl_operation(arguments, run_dir, lifecycle_cli_path)
    if control_operation:
        normalized["control_operation"] = control_operation
    return normalized


def _auditctl_operation(
    arguments: object, run_dir: str | Path | None = None, helper_path: str | Path | None = None
) -> str | None:
    if run_dir is None or helper_path is None:
        return None
    values = []

    def collect(value):
        if isinstance(value, dict):
            for child in value.values():
                collect(child)
        elif isinstance(value, (list, tuple)):
            for child in value:
                collect(child)
        elif isinstance(value, str):
            values.append(value)

    collect(arguments)
    allowed = {
        "prepare",
        "install",
        "status",
        "verify",
        "start",
        "stop",
        "renew",
        "assess",
        "disarm",
        "remove",
        "verify-teardown",
    }
    expected_run = os.path.normcase(os.path.realpath(os.path.normpath(str(run_dir))))
    expected_helper = os.path.normcase(os.path.realpath(os.path.normpath(str(helper_path))))

    def unquote(value: str) -> str:
        return value[1:-1] if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'} else value

    for value in values:
        try:
            tokens = [unquote(token) for token in shlex.split(value, posix=False)]
        except ValueError:
            continue
        for index, token in enumerate(tokens[:-2]):
            if os.path.normcase(os.path.realpath(os.path.normpath(token))) != expected_helper:
                continue
            if index == 0:
                continue
            interpreter = tokens[index - 1].replace("\\", "/").rsplit("/", 1)[-1].lower()
            python_names = {"py", "py.exe", "python", "python.exe", "python3", "python3.exe"}
            if interpreter not in python_names:
                launcher = tokens[index - 2].replace("\\", "/").rsplit("/", 1)[-1].lower() if index >= 2 else ""
                if not (interpreter.startswith("-") and launcher in {"py", "py.exe"}):
                    continue
            operation = tokens[index + 1].lower()
            if operation not in allowed:
                continue
            try:
                run_index = tokens.index("--run-dir", index + 2)
                candidate_run = os.path.normcase(os.path.normpath(tokens[run_index + 1]))
            except (ValueError, IndexError):
                continue
            if os.path.normcase(os.path.realpath(os.path.normpath(candidate_run))) == expected_run:
                return operation
    return None


def render_handlers(runtime: str, recorder: Path) -> dict:
    """Render project-local handlers using this active Python interpreter."""
    runtime = runtime.lower()
    recorder = Path(recorder).resolve()
    run_dir = recorder.parent.parent if recorder.parent.name == "scripts" else recorder.parent
    argv = [sys.executable, str(recorder), "--run-dir", str(run_dir)]
    posix_command = shlex.join(argv)
    windows_command = subprocess.list2cmdline(argv)
    if runtime == "codex":
        hooks = {}
        for event in (
            "PreToolUse",
            "PostToolUse",
            "SubagentStart",
            "SubagentStop",
            "SessionStart",
            "SessionEnd",
        ):
            handler = {"type": "command", "command": posix_command, "commandWindows": windows_command}
            if event == "SessionEnd":
                handler["timeout"] = 3
            hooks[event] = [{"matcher": "", "hooks": [handler]}]
        return hooks
    if runtime == "devin":
        command = windows_command if sys.platform == "win32" else posix_command
        return {
            "version": 1,
            "hooks": {
                event: [{"matcher": "", "hooks": [{"type": "command", "command": command}]}]
                for event in ("PreToolUse", "PostToolUse", "SessionStart", "SessionEnd")
            },
        }
    raise ValueError("unsupported-runtime")
