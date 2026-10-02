import pytest

from sanitize import sanitize


@pytest.mark.parametrize(
    "value,secret",
    [
        ({"password": "pw-SENTINEL"}, "pw-SENTINEL"),
        ({"nested": {"access_token": "tok-SENTINEL"}}, "tok-SENTINEL"),
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
