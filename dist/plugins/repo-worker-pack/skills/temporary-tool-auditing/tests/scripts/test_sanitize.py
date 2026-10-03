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
        ({"args": {"JSESSIONID": "java-session-SENTINEL"}}, "java-session-SENTINEL"),
        ({"args": {"sessionid": "plain-session-SENTINEL"}}, "plain-session-SENTINEL"),
        ({"args": {"sessionId": "camel-session-SENTINEL"}}, "camel-session-SENTINEL"),
        ({"args": {"sid": "short-session-SENTINEL"}}, "short-session-SENTINEL"),
        ({"args": {"session_id": "nested-session-SENTINEL"}}, "nested-session-SENTINEL"),
        ({"args": {"email": "person@example.test"}}, "person@example.test"),
        ({"args": {"credentials": "several credentials"}}, "several credentials"),
        ({"text": "contact person@example.test for access"}, "person@example.test"),
        ({"text": "AWS_SECRET_ACCESS_KEY=cloud-secret-SENTINEL"}, "cloud-secret-SENTINEL"),
        ({"args": {"ssn": "123-45-6789"}}, "123-45-6789"),
        ({"args": {"card_number": "4111 1111 1111 1111"}}, "4111 1111 1111 1111"),
        ({"args": {"cvv": "123"}}, "123"),
        ({"args": {"medical_record": "patient note"}}, "patient note"),
        ({"args": {"bank_account": "account-secret"}}, "account-secret"),
        ({"args": {"totp_secret": "second-factor-seed"}}, "second-factor-seed"),
        ({"Authorization": "Bearer bearer-SENTINEL"}, "bearer-SENTINEL"),
        ({"key": "sk-proj-abcdefghijklmnopqrstuvwxyz123456"}, "sk-proj-abcdefghijklmnopqrstuvwxyz123456"),
        ({"signature": "structured-signature-SENTINEL"}, "structured-signature-SENTINEL"),
        ({"sig": "structured-short-signature-SENTINEL"}, "structured-short-signature-SENTINEL"),
        (
            {"text": "id token eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjMifQ.signaturevalue"},
            "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjMifQ.signaturevalue",
        ),
        ({"text": "Authorization: Basic dXNlcjpwYXNz"}, "dXNlcjpwYXNz"),
        ({"text": "Authorization: ApiKey auth-SENTINEL"}, "auth-SENTINEL"),
        ({"text": "Proxy-Authorization: Digest proxy-SENTINEL"}, "proxy-SENTINEL"),
        ({"url": "https://example.test/?access_token=query-SENTINEL"}, "query-SENTINEL"),
        ({"url": "https://example.test/?password=query-password-SENTINEL"}, "query-password-SENTINEL"),
        ({"url": "https://health.example/patient?dob=dob-SENTINEL"}, "dob-SENTINEL"),
        ({"url": "https://travel.example/check?passport_number=passport-SENTINEL"}, "passport-SENTINEL"),
        ({"url": "https://bank.example/transfer?iban=iban-SENTINEL"}, "iban-SENTINEL"),
        ({"url": "https://health.example/patient?diagnosis=diagnosis-SENTINEL"}, "diagnosis-SENTINEL"),
        ({"url": "https://bank.example/transfer?account_number=account-SENTINEL"}, "account-SENTINEL"),
        ({"url": "https://health.example/patient?dateOfBirth=camel-dob-SENTINEL"}, "camel-dob-SENTINEL"),
        ({"url": "https://api.example/callback?%64ob=encoded-dob-SENTINEL"}, "encoded-dob-SENTINEL"),
        ({"url": "https://auth.example/callback?mfa_code=mfa-SENTINEL"}, "mfa-SENTINEL"),
        ({"url": "https://auth.example/callback?private_key=private-key-SENTINEL"}, "private-key-SENTINEL"),
        ({"url": "https://legacy.example/app?asp_net_session_id=asp-session-SENTINEL"}, "asp-session-SENTINEL"),
        (
            {"url": "https://example.test/callback?user%5Bpassword%5D=bracket-password-SENTINEL"},
            "bracket-password-SENTINEL",
        ),
        (
            {"url": "https://example.test/callback?oauth[access_token]=bracket-token-SENTINEL"},
            "bracket-token-SENTINEL",
        ),
        (
            {"url": "https://example.test/callback?oauth%5BaccessToken%5D=encoded-camel-token-SENTINEL"},
            "encoded-camel-token-SENTINEL",
        ),
        (
            {"url": "https://example.test/profile?customer.phoneNumber=camel-phone-SENTINEL"},
            "camel-phone-SENTINEL",
        ),
        ({"url": "https://example.test/profile?profile.email=dotted-email-SENTINEL"}, "dotted-email-SENTINEL"),
        ({"url": "https://example.test/maps?key=AIzaSyD-SENTINEL&zoom=3"}, "AIzaSyD-SENTINEL"),
        (
            {"url": "https://bucket.test/file?X-Amz-Signature=signature-SENTINEL&X-Amz-Security-Token=token-SENTINEL"},
            "signature-SENTINEL",
        ),
        ({"url": "https://bucket.test/file?%73ig=encoded-signature-SENTINEL"}, "encoded-signature-SENTINEL"),
        (
            {"url": "https://bucket.test/file?X%2dAmz%2dSignature=encoded-provider-signature-SENTINEL"},
            "encoded-provider-signature-SENTINEL",
        ),
        ({"url": "https://bucket.test/file?X-Goog-Signature=google-signature-SENTINEL"}, "google-signature-SENTINEL"),
        ({"url": "https://api.example/resource?jwt=jwt-bearer-SENTINEL"}, "jwt-bearer-SENTINEL"),
        ({"url": "https://example.test/callback?id_token=idtoken-SENTINEL"}, "idtoken-SENTINEL"),
        ({"url": "https://login.example/callback?code=oauth-code-SENTINEL"}, "oauth-code-SENTINEL"),
        ({"url": "https://api.example/items?auth_token=auth-bearer-SENTINEL&limit=5"}, "auth-bearer-SENTINEL"),
        ({"url": "https://example.test/#access_token=fragment-token-SENTINEL"}, "fragment-token-SENTINEL"),
        ({"url": "https://legacy.example/action?sessionid=session-SENTINEL&view=summary"}, "session-SENTINEL"),
        ({"url": "https://legacy.example/action?JSESSIONID=java-session-SENTINEL"}, "java-session-SENTINEL"),
        ({"url": "https://legacy.example/app?CFID=cfid-SENTINEL&CFTOKEN=cftoken-SENTINEL"}, "cftoken-SENTINEL"),
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
        ({"command": "tool --otp six-digit-SENTINEL"}, "six-digit-SENTINEL"),
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


def test_sanitise_preserves_only_root_and_audit_manifest_session_metadata():
    value = {
        "session_id": "runtime-session",
        "arguments": {"session_id": "nested-session-secret"},
        "subject": {"session_id": "selected-session"},
        "controls": [{"session_id": "control-session"}],
    }
    cleaned, redactions = sanitize(
        value,
        safe_session_paths={"$.session_id", "$.subject.session_id", "$.controls[0].session_id"},
    )
    assert cleaned["session_id"] == "runtime-session"
    assert cleaned["subject"]["session_id"] == "selected-session"
    assert cleaned["controls"][0]["session_id"] == "control-session"
    assert cleaned["arguments"]["session_id"] == "[REDACTED]"
    assert "$.arguments.session_id" in redactions


def test_sanitise_redacts_session_id_without_an_explicit_metadata_path():
    cleaned, redactions = sanitize({"session_id": "untrusted-session-secret"})
    assert cleaned["session_id"] == "[REDACTED]"
    assert redactions == ["$.session_id"]


def test_free_text_card_number_redaction_checks_luhn():
    valid, valid_redactions = sanitize("payment 4111 1111 1111 1111 submitted")
    invalid, invalid_redactions = sanitize("reference 4111 1111 1111 1112")
    assert valid == "payment [REDACTED] submitted"
    assert valid_redactions
    assert invalid == "reference 4111 1111 1111 1112"
    assert not invalid_redactions


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
                "oauth_callback": "https://login.example/callback?code=oauth-persisted-SENTINEL",
                "auth_url": "https://api.example/items?auth_token=auth-persisted-SENTINEL",
                "fragment_url": "https://example.test/#access_token=fragment-persisted-SENTINEL",
                "session_url": "https://legacy.example/action?sessionid=session-persisted-SENTINEL",
                "coldfusion_url": "https://legacy.example/app?CFID=cfid-persisted&CFTOKEN=cftoken-persisted-SENTINEL",
                "connection_string": "Server=db;User Id=example;Pwd=connection-SENTINEL",
                "JSESSIONID": "java-session-persisted-SENTINEL",
                "sessionid": "plain-session-persisted-SENTINEL",
                "sessionId": "camel-session-persisted-SENTINEL",
                "sid": "short-session-persisted-SENTINEL",
                "session_id": "nested-session-persisted-SENTINEL",
                "email": "person@example.test",
                "ssn": "123-45-6789",
                "card_number": "4111 1111 1111 1111",
                "cvv": "123",
                "medical_record": "patient-record-SENTINEL",
                "bank_account": "bank-account-SENTINEL",
                "environment": "AWS_SECRET_ACCESS_KEY=env-secret-SENTINEL",
                "credential_url": "https://example.test/?password=query-password-SENTINEL",
                "dob_url": "https://health.example/patient?dob=dob-persisted-SENTINEL&next=summary",
                "passport_url": "https://travel.example/check?passport_number=passport-persisted-SENTINEL",
                "iban_url": "https://bank.example/transfer?iban=iban-persisted-SENTINEL",
                "diagnosis_url": "https://health.example/patient?diagnosis=diagnosis-persisted-SENTINEL",
                "account_url": "https://bank.example/transfer?account_number=account-persisted-SENTINEL",
                "mfa_url": "https://auth.example/callback?mfa_code=mfa-persisted-SENTINEL",
                "private_key_url": "https://auth.example/callback?private_key=private-key-persisted-SENTINEL",
                "asp_session_url": "https://legacy.example/app?asp_net_session_id=asp-session-persisted-SENTINEL",
                "nested_sensitive_url": (
                    "https://example.test/callback?user%5Bpassword%5D=nested-password-persisted-SENTINEL"
                    "&oauth[access_token]=nested-token-persisted-SENTINEL&profile.email=nested-email-persisted-SENTINEL"
                    "&view=summary"
                ),
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
        "oauth-persisted-SENTINEL",
        "auth-persisted-SENTINEL",
        "fragment-persisted-SENTINEL",
        "session-persisted-SENTINEL",
        "cftoken-persisted-SENTINEL",
        "cli-SENTINEL",
        "refresh-SENTINEL",
        "result-SENTINEL",
        "connection-SENTINEL",
        "java-session-persisted-SENTINEL",
        "plain-session-persisted-SENTINEL",
        "camel-session-persisted-SENTINEL",
        "short-session-persisted-SENTINEL",
        "nested-session-persisted-SENTINEL",
        "person@example.test",
        "123-45-6789",
        "4111 1111 1111 1111",
        "patient-record-SENTINEL",
        "bank-account-SENTINEL",
        "env-secret-SENTINEL",
        "query-password-SENTINEL",
        "dob-persisted-SENTINEL",
        "passport-persisted-SENTINEL",
        "iban-persisted-SENTINEL",
        "diagnosis-persisted-SENTINEL",
        "account-persisted-SENTINEL",
        "mfa-persisted-SENTINEL",
        "private-key-persisted-SENTINEL",
        "asp-session-persisted-SENTINEL",
        "nested-password-persisted-SENTINEL",
        "nested-token-persisted-SENTINEL",
        "nested-email-persisted-SENTINEL",
    ):
        assert sentinel not in persisted
    persisted_event = json.loads(persisted)
    assert persisted_event["session_id"] == "s1"
    assert "view=summary" in persisted_event["arguments"]["nested_sensitive_url"]
    assert persisted_event["redactions"]
