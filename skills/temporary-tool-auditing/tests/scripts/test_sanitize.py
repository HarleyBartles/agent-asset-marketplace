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
        ({"text": "Cookie: sessionid=cookie-header-SENTINEL"}, "cookie-header-SENTINEL"),
        ({"text": "Set-Cookie: sid=setter-cookie-SENTINEL; Secure"}, "setter-cookie-SENTINEL"),
        ({"Cookie": "sid=cookie-SENTINEL"}, "cookie-SENTINEL"),
        ({"Authorization": "Bearer bearer-SENTINEL"}, "bearer-SENTINEL"),
        ({"key": "sk-proj-abcdefghijklmnopqrstuvwxyz123456"}, "sk-proj-abcdefghijklmnopqrstuvwxyz123456"),
        ({"text": "Authorization: Basic dXNlcjpwYXNz"}, "dXNlcjpwYXNz"),
        ({"text": "Authorization: ApiKey auth-SENTINEL"}, "auth-SENTINEL"),
        ({"text": "Proxy-Authorization: Digest proxy-SENTINEL"}, "proxy-SENTINEL"),
        ({"url": "https://example.test/?access_token=query-SENTINEL"}, "query-SENTINEL"),
        ({"url": "https://example.test/maps?key=AIzaSyD-SENTINEL&zoom=3"}, "AIzaSyD-SENTINEL"),
        (
            {"url": "https://bucket.test/file?X-Amz-Signature=signature-SENTINEL&X-Amz-Security-Token=token-SENTINEL"},
            "signature-SENTINEL",
        ),
        ({"url": "https://bucket.test/file?X-Goog-Signature=google-signature-SENTINEL"}, "google-signature-SENTINEL"),
        ({"command": "tool --access-token cli-SENTINEL"}, "cli-SENTINEL"),
        ({"command": "tool --refresh_token=refresh-SENTINEL"}, "refresh-SENTINEL"),
        ({"command": 'tool --password "example-secret has spaces"'}, "example-secret has spaces"),
        ({"command": "tool --access-token='quoted token value'"}, "quoted token value"),
        ({"text": 'password="assignment secret with spaces"'}, "assignment secret with spaces"),
        ({"key": "-----BEGIN PRIVATE KEY-----\nprivate-SENTINEL\n-----END PRIVATE KEY-----"}, "private-SENTINEL"),
        ({"url": "https://user:url-SENTINEL@example.test/api"}, "url-SENTINEL"),
        ({"url": "postgres://user:db-SENTINEL@db.example.test/main"}, "db-SENTINEL"),
        ({"command": "tool --password=flag-SENTINEL"}, "flag-SENTINEL"),
        ({"command": "tool --api-key api-SENTINEL"}, "api-SENTINEL"),
        ({"connection": "Server=db;User Id=example;Pwd=SENTINEL-password"}, "SENTINEL-password"),
        ({"connection": 'Server=db;Password="quoted;password"'}, "quoted;password"),
        ({"connection": "Server=db;Pwd={braced password}"}, "braced password"),
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
                "headers": (
                    "X-API-Key: header-SENTINEL\nAuthorization: ApiKey auth-SENTINEL\n"
                    "Proxy-Authorization: Digest proxy-SENTINEL"
                ),
                "url": "https://example.test/?access_token=query-SENTINEL",
                "maps_url": "https://example.test/maps?key=AIzaSyD-persisted-SENTINEL&zoom=3",
                "signed_url": "https://bucket.test/file?X-Amz-Signature=aws-signature-persisted-SENTINEL",
                "connection_string": "Server=db;User Id=example;Pwd=connection-SENTINEL",
                "command": (
                    "tool --access-token cli-SENTINEL --refresh_token=refresh-SENTINEL "
                    '--password "example-secret has spaces" password="assignment secret with spaces"'
                ),
            },
            "tool_response": {"body": '{"access_token":"result-SENTINEL"}'},
        },
        100,
    )
    persisted = (tmp_path / "events.jsonl").read_text(encoding="utf-8")
    for sentinel in (
        "json-SENTINEL",
        "header-SENTINEL",
        "auth-SENTINEL",
        "proxy-SENTINEL",
        "query-SENTINEL",
        "AIzaSyD-persisted-SENTINEL",
        "aws-signature-persisted-SENTINEL",
        "cli-SENTINEL",
        "refresh-SENTINEL",
        "result-SENTINEL",
        "connection-SENTINEL",
    ):
        assert sentinel not in persisted
    assert json.loads(persisted)["redactions"]
