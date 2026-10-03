import sys

from runtime import normalize_event, render_handlers


def test_codex_pre_event_keeps_call_and_child_identity():
    event = normalize_event(
        "codex",
        {
            "hook_event_name": "PreToolUse",
            "session_id": "session-1",
            "agent_id": "agent-2",
            "turn_id": "turn-3",
            "tool_use_id": "call-4",
            "tool_name": "Bash",
            "tool_input": {"command": "pwd"},
        },
        "status",
    )
    assert event["event"] == "pre"
    assert event["session_id"] == "session-1"
    assert event["agent_id"] == "agent-2"
    assert event["call_id"] == "call-4"
    assert "arguments" not in event


def test_full_results_detail_includes_sanitizable_arguments():
    event = normalize_event(
        "codex",
        {"hook_event_name": "PreToolUse", "tool_name": "Bash", "tool_input": {"command": "pwd"}},
        "full-results",
    )
    assert event["arguments"] == {"command": "pwd"}


def test_codex_main_identity_is_not_manufactured():
    event = normalize_event(
        "codex",
        {"hook_event_name": "PreToolUse", "session_id": "s", "tool_name": "Bash", "tool_input": {}},
        "status",
    )
    assert event["agent_id"] is None
    assert event["turn_id"] is None


def test_codex_post_text_response_does_not_imply_success():
    event = normalize_event(
        "codex",
        {
            "hook_event_name": "PostToolUse",
            "tool_name": "Bash",
            "tool_use_id": "call-1",
            "tool_response": "some output",
        },
        "status",
    )
    assert event["outcome_status"] == "observed-unknown"
    assert "result" not in event


def test_devin_structured_outcome_and_prompt_correlation():
    event = normalize_event(
        "devin-desktop",
        {
            "event": "post_tool_use",
            "session_id": "s1",
            "prompt_id": "prompt-2",
            "tool_call_id": "call-3",
            "tool": "Bash",
            "arguments": {"command": "false"},
            "result": {"status": "failure", "error": "exit code 1"},
        },
        "full-results",
    )
    assert event["turn_id"] == "prompt-2"
    assert event["call_id"] == "call-3"
    assert event["outcome_status"] == "failure"
    assert event["result"]["status"] == "failure"


def test_devin_structured_success_and_error_fields_are_used():
    success = normalize_event(
        "devin-desktop",
        {
            "event": "post_tool_use",
            "tool": "read",
            "tool_call_id": "c1",
            "tool_response": {"success": True, "error": None},
        },
        "status",
    )
    failure = normalize_event(
        "devin-desktop",
        {
            "event": "post_tool_use",
            "tool": "read",
            "tool_call_id": "c2",
            "tool_response": {"success": False, "error": "failed"},
        },
        "status",
    )
    assert success["outcome_status"] == "success"
    assert failure["outcome_status"] == "failure"


def test_devin_missing_correlation_fields_remain_null():
    event = normalize_event("devin-desktop", {"event": "pre_tool_use", "tool": "Bash"}, "status")
    assert event["session_id"] is None
    assert event["call_id"] is None
    assert event["outcome_status"] == "observed-unknown"


def test_handlers_use_absolute_interpreter_script_command(tmp_path):
    handlers = render_handlers("codex", tmp_path / "record.py")
    hook = handlers["PreToolUse"][0]["hooks"][0]
    command = hook["commandWindows"] if sys.platform == "win32" else hook["command"]
    assert sys.executable in command
    assert "-B" in command
    assert str((tmp_path / "record.py").resolve()) in command


def test_devin_handlers_use_observed_v1_event_shape(tmp_path):
    handlers = render_handlers("devin-desktop", tmp_path / "record.py")
    assert handlers["version"] == 1
    entry = handlers["hooks"]["PreToolUse"][0]
    assert entry["matcher"] == ""
    assert entry["hooks"][0]["type"] == "command"
    assert "-B" in entry["hooks"][0]["command"]
    assert str((tmp_path / "record.py").resolve()) in entry["hooks"][0]["command"]


def test_auditctl_lifecycle_commands_are_marked_as_controls():
    event = normalize_event(
        "codex",
        {
            "hook_event_name": "PreToolUse",
            "tool_name": "Bash",
            "tool_use_id": "control-call",
            "tool_input": {"command": "py -3 C:/skills/auditctl.py stop --apply --run-dir C:/repo/.audit/run"},
        },
        "status",
        run_dir="C:/repo/.audit/run",
        lifecycle_cli_path="C:/skills/auditctl.py",
    )
    assert event["control_operation"] == "stop"


def test_purge_command_is_a_lifecycle_control():
    event = normalize_event(
        "codex",
        {
            "hook_event_name": "PreToolUse",
            "tool_name": "Bash",
            "tool_use_id": "purge-call",
            "tool_input": {"command": "py -3 C:/skills/auditctl.py purge --apply --run-dir C:/repo/.audit/run"},
        },
        "status",
        run_dir="C:/repo/.audit/run",
        lifecycle_cli_path="C:/skills/auditctl.py",
    )
    assert event["control_operation"] == "purge"


def test_auditctl_reference_in_shell_text_is_not_a_control():
    event = normalize_event(
        "codex",
        {
            "hook_event_name": "PreToolUse",
            "tool_name": "Bash",
            "tool_use_id": "ordinary-call",
            "tool_input": {"command": "Get-Content auditctl.py; Write-Output start"},
        },
        "status",
        run_dir="C:/repo/.audit/run",
        lifecycle_cli_path="C:/skills/auditctl.py",
    )
    assert "control_operation" not in event


def test_auditctl_text_embedded_in_command_or_non_shell_payload_is_not_control():
    lifecycle = "py -3 C:/skills/auditctl.py stop --apply --run-dir C:/repo/.audit/run"
    command_text = normalize_event(
        "codex",
        {
            "hook_event_name": "PreToolUse",
            "tool_name": "PowerShell",
            "tool_use_id": "ordinary-shell",
            "tool_input": {"command": f"Write-Output '{lifecycle}'"},
        },
        "status",
        run_dir="C:/repo/.audit/run",
        lifecycle_cli_path="C:/skills/auditctl.py",
    )
    nested_payload = normalize_event(
        "devin-desktop",
        {
            "event": "pre_tool_use",
            "tool": "browser",
            "tool_call_id": "ordinary-browser",
            "arguments": {"url": f"https://example.test/?q={lifecycle}"},
        },
        "status",
        run_dir="C:/repo/.audit/run",
        lifecycle_cli_path="C:/skills/auditctl.py",
    )
    assert "control_operation" not in command_text
    assert "control_operation" not in nested_payload


def test_auditctl_lifecycle_command_in_mixed_shell_command_is_not_control():
    event = normalize_event(
        "codex",
        {
            "hook_event_name": "PreToolUse",
            "tool_name": "Bash",
            "tool_use_id": "mixed-call",
            "tool_input": {
                "command": "py -3 C:/skills/auditctl.py status --run-dir C:/repo/.audit/run && curl https://example.test"
            },
        },
        "status",
        run_dir="C:/repo/.audit/run",
        lifecycle_cli_path="C:/skills/auditctl.py",
    )
    assert "control_operation" not in event
