import pytest

from sanitize import sanitize
from record import record_event


@pytest.mark.parametrize(
    "value,secret",
    [
        ({"password": "pw-SENTINEL"}, "pw-SENTINEL"),
        ({"nested": {"access_token": "tok-SENTINEL"}}, "tok-SENTINEL"),
        ({"nested": {"apiKey": "camel-api-SENTINEL"}}, "camel-api-SENTINEL"),
        ({"clientSecret": "camel-secret-SENTINEL"}, "camel-secret-SENTINEL"),
        ({"text": '{"access_token":"json-token-SENTINEL"}'}, "json-token-SENTINEL"),
        ({"text": "X-API-Key: header-key-SENTINEL"}, "header-key-SENTINEL"),
        ({"Cookie": "sid=cookie-SENTINEL"}, "cookie-SENTINEL"),
        ({"Authorization": "Bearer bearer-SENTINEL"}, "bearer-SENTINEL"),
        ({"key": "sk-proj-abcdefghijklmnopqrstuvwxyz123456"}, "sk-proj-abcdefghijklmnopqrstuvwxyz123456"),
        ({"text": "Authorization: Basic dXNlcjpwYXNz"}, "dXNlcjpwYXNz"),
        ({"key": "-----BEGIN PRIVATE KEY-----\nprivate-SENTINEL\n-----END PRIVATE KEY-----"}, "private-SENTINEL"),
        ({"url": "https://user:url-SENTINEL@example.test/api"}, "url-SENTINEL"),
        ({"url": "postgres://user:db-SENTINEL@db.example.test/main"}, "db-SENTINEL"),
        ({"command": "tool --password=flag-SENTINEL"}, "flag-SENTINEL"),
        ({"command": "tool --api-key api-SENTINEL"}, "api-SENTINEL"),
    ],
)
def test_sanitise_removes_credential_values(value, secret):
    cleaned, redactions = sanitize(value)
    assert secret not in repr(cleaned)
    assert "[REDACTED]" in repr(cleaned)
    assert redactions


def test_sanitise_preserves_harmless_values_and_reports_paths():
    cleaned, redactions = sanitize({"tool": "Bash", "args": {"password": "p-SENTINEL", "count": 3}})
    assert cleaned["tool"] == "Bash"
    assert cleaned["args"]["count"] == 3
    assert cleaned["args"]["password"] == "[REDACTED]"
    assert redactions == ["$.args.password"]


def test_sanitise_handles_cyclic_input_without_echoing_values():
    value = {"token": "cycle-SENTINEL"}
    value["self"] = value
    cleaned, redactions = sanitize(value)
    assert "cycle-SENTINEL" not in repr(cleaned)
    assert redactions


@pytest.mark.parametrize("detail", ["status", "full-results"])
def test_recorder_never_persists_sentinels_from_json_or_header_strings(tmp_path, detail):
    import json

    from store import save_manifest

    save_manifest(
        tmp_path,
        {
            "run_id": "run-1",
            "runtime": "codex",
            "detail": detail,
            "expires_at": 1000,
            "armed": True,
            "registration_state": "installed",
        },
    )
    assert record_event(
        tmp_path,
        {
            "hook_event_name": "PostToolUse",
            "session_id": "s1",
            "tool_use_id": "call-1",
            "tool_name": "MCP",
            "tool_input": {
                "body": '{"api_key":"json-SENTINEL"}',
                "headers": "X-API-Key: header-SENTINEL",
            },
            "tool_response": {"body": '{"access_token":"result-SENTINEL"}'},
        },
        100,
    )
    persisted = (tmp_path / "events.jsonl").read_text(encoding="utf-8")
    for sentinel in ("json-SENTINEL", "header-SENTINEL", "result-SENTINEL"):
        assert sentinel not in persisted
    assert json.loads(persisted)["redactions"]
