"""Best-effort removal of common credentials from tool audit evidence."""

import json
import re
from typing import Any
from urllib.parse import unquote_plus

_REDACTED = "[REDACTED]"
_SECRET_KEYS = re.compile(
    r"(?:^|[_-])(password|passwd|pwd|passphrase|secret|token|credential|credentials|api[_-]?key|access[_-]?key|"
    r"session(?:[_-]?id)?|sid|phpsessid|jsessionid|asp(?:\.|[_-])net[_-]?session[_-]?id|cfid|cftoken|"
    r"email|e[_-]?mail|phone|mobile|telephone|ssn|social[_-]?security(?:[_-]?number)?|"
    r"national[_-]?(?:id|identifier)|passport(?:[_-]?(?:number|no))?|date[_-]?of[_-]?birth|dob|"
    r"address|postal[_-]?code|zip[_-]?code|first[_-]?name|last[_-]?name|full[_-]?name|username|"
    r"medical[_-]?record|health[_-]?record|health[_-]?data|patient[_-]?id|diagnosis|medical[_-]?history|"
    r"genetic[_-]?data|bank[_-]?account|account[_-]?number|routing[_-]?number|iban|swift|"
    r"signature|sig|"
    r"pan|card[_-]?(?:number|no)|cardholder|credit[_-]?card|cvv|cvc|security[_-]?code|pin|track[_-]?data|"
    r"totp[_-]?(?:secret|seed)|otp[_-]?secret|mfa[_-]?secret|two[_-]?factor[_-]?(?:secret|code|seed)|"
    r"otp|one[_-]?time[_-]?(?:password|code)|mfa[_-]?code|recovery[_-]?code|backup[_-]?code|"
    r"authorization|proxy[_-]?authorization|cookie|set[_-]?cookie|private[_-]?key)(?:$|[_-])",
    re.IGNORECASE,
)
_EMAIL = re.compile(r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,63}\b")
_URL_PARAMETER = re.compile(r"(?i)([?&#;])([^=&#;\s\"'<>]+)(=)([^&#;\s\"'<>]+)")
_US_SSN = re.compile(r"(?<!\d)(?!000|666|9\d\d)\d{3}[- ](?!00)\d{2}[- ](?!0000)\d{4}(?!\d)")
_JWT = re.compile(r"\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\b")
_PAN = re.compile(r"(?<!\d)(?:\d[ -]?){12,18}\d(?!\d)")
_PATTERNS = [
    (re.compile(r"-----BEGIN [^-]*PRIVATE KEY-----.*?-----END [^-]*PRIVATE KEY-----", re.I | re.S), _REDACTED),
    (re.compile(r"(?i)\b(Bearer|Basic)\s+[A-Za-z0-9._~+/=-]+"), lambda m: f"{m.group(1)} {_REDACTED}"),
    (re.compile(r"(?i)([a-z][a-z0-9+.-]*://)[^/@\s:]+(?::[^/@\s]*)?@"), lambda m: f"{m.group(1)}{_REDACTED}@"),
    (
        re.compile(
            r"(?i)([?&#](?:key|api[_-]?key|access[_-]?key|auth[_-]?token|refresh[_-]?token|token|jwt|id[_-]?token|"
            r"session(?:[_-]?id)?|sid|phpsessid|jsessionid|asp(?:\.|[_-])net[_-]?session[_-]?id|cfid|cftoken|"
            r"oauth[_-]?token|code|password|passwd|pwd|credential|credentials|client[_-]?secret|"
            r"email|e[_-]?mail|phone|mobile|telephone|ssn|social[_-]?security(?:[_-]?number)?|"
            r"national[_-]?(?:id|identifier)|passport(?:[_-]?(?:number|no))?|date[_-]?of[_-]?birth|dob|"
            r"address|postal[_-]?code|zip[_-]?code|first[_-]?name|last[_-]?name|full[_-]?name|username|"
            r"medical[_-]?record|health[_-]?record|health[_-]?data|patient[_-]?id|diagnosis|medical[_-]?history|"
            r"genetic[_-]?data|bank[_-]?account|account[_-]?number|routing[_-]?number|iban|swift|"
            r"pan|card[_-]?(?:number|no)|cardholder|credit[_-]?card|cvv|cvc|security[_-]?code|pin|track[_-]?data|"
            r"(?:x-amz-|x-goog-)?(?:signature|sig)|"
            r"x-amz-security-token|x-amz-credential)=)[^&#\s\"'<>]+"
        ),
        lambda m: f"{m.group(1)}{_REDACTED}",
    ),
    (
        re.compile(
            r"""(?i)(\b[A-Z0-9_.-]*(?:PASSWORD|PASSWD|PWD|PASSPHRASE|SECRET|TOKEN|CREDENTIALS?|API[_-]?KEY|ACCESS[_-]?KEY)[A-Z0-9_.-]*\s*=\s*)("(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*'|\{[^}]*\}|[^\s;&]+)""",
        ),
        lambda m: f"{m.group(1)}{_REDACTED}",
    ),
    (
        re.compile(
            r"""(?i)(\b(?:password|passwd|pwd|(?:access|refresh)[_-]?token|token|api[_-]?key|secret)\s*=\s*)("(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*'|\{[^}]*\}|[^\s;&]+)""",
        ),
        lambda m: f"{m.group(1)}{_REDACTED}",
    ),
    (
        re.compile(
            r"(?i)(\b(?:x-)?(?:password|passwd|token|access[_-]?token|refresh[_-]?token|api[_-]?key|secret|set-cookie|cookie|proxy-authorization|authorization)\s*:\s*)([^\r\n]+)"
        ),
        lambda m: f"{m.group(1)}{_REDACTED}",
    ),
    (
        re.compile(
            r"""(?i)(--(?:password|passwd|pwd|passphrase|(?:access|refresh)[_-]?token|token|api[_-]?key|secret|credential|client[_-]?secret|otp|mfa[_-]?code)(?:=|\s+))("(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*'|[^\s]+)""",
        ),
        lambda m: f"{m.group(1)}{_REDACTED}",
    ),
    (re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{20,}\b"), _REDACTED),
    (re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b"), _REDACTED),
    (re.compile(r"\bAKIA[0-9A-Z]{16}\b"), _REDACTED),
    (re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b"), _REDACTED),
    (re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b"), _REDACTED),
    (re.compile(r"\b(?:sk|rk)_live_[0-9A-Za-z]{16,}\b"), _REDACTED),
    (_EMAIL, _REDACTED),
    (_US_SSN, _REDACTED),
    (_JWT, _REDACTED),
    (
        _PAN,
        lambda match: _REDACTED if _passes_luhn(match.group(0)) else match.group(0),
    ),
]


def _passes_luhn(value: str) -> bool:
    digits = [int(character) for character in value if character.isdigit()]
    if not 13 <= len(digits) <= 19:
        return False
    checksum = 0
    parity = len(digits) % 2
    for index, digit in enumerate(digits):
        if index % 2 == parity:
            digit *= 2
            if digit > 9:
                digit -= 9
        checksum += digit
    return checksum % 10 == 0


def _clean_text(value: str) -> tuple[str, bool]:
    cleaned = value
    changed = False
    for pattern, replacement in _PATTERNS:
        updated = pattern.sub(replacement, cleaned)
        changed = changed or updated != cleaned
        cleaned = updated

    def redact_sensitive_parameter(match: re.Match) -> str:
        key = unquote_plus(match.group(2))
        camel_normalized = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", key)
        normalized_key = re.sub(r"[^a-z0-9]+", "_", camel_normalized.lower()).strip("_")
        signature_key = normalized_key in {"sig", "signature", "x_amz_signature", "x_goog_signature"}
        if _SECRET_KEYS.search(normalized_key) or signature_key:
            return f"{match.group(1)}{match.group(2)}{match.group(3)}{_REDACTED}"
        return match.group(0)

    updated = _URL_PARAMETER.sub(redact_sensitive_parameter, cleaned)
    changed = changed or updated != cleaned
    cleaned = updated
    return cleaned, changed


def sanitize(value: object, *, safe_session_paths: set[str] | None = None) -> tuple[object, list[str]]:
    """Return a JSON-compatible copy and safe JSONPath-like redaction paths."""
    redactions: list[str] = []
    active: set[int] = set()
    safe_session_paths = safe_session_paths or set()

    def visit(item: Any, path: str, depth: int) -> Any:
        if depth > 40:
            redactions.append(path)
            return _REDACTED
        if isinstance(item, dict):
            identity = id(item)
            if identity in active:
                redactions.append(path)
                return _REDACTED
            active.add(identity)
            result = {}
            for index, (key, child) in enumerate(item.items()):
                raw_key = str(key)[:256]
                safe_key, key_changed = _clean_text(raw_key)
                if key_changed:
                    safe_key = f"[REDACTED_KEY_{index}]"
                child_path = f"{path}.{safe_key}"
                normalized_key = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", safe_key).replace(" ", "_")
                if key_changed:
                    result[safe_key] = _REDACTED
                    redactions.append(child_path)
                elif safe_key == "session_id" and child_path in safe_session_paths:
                    result[safe_key] = visit(child, child_path, depth + 1)
                elif _SECRET_KEYS.search(normalized_key):
                    result[safe_key] = _REDACTED
                    redactions.append(child_path)
                else:
                    result[safe_key] = visit(child, child_path, depth + 1)
            active.remove(identity)
            return result
        if isinstance(item, (list, tuple)):
            identity = id(item)
            if identity in active:
                redactions.append(path)
                return _REDACTED
            active.add(identity)
            result = [visit(child, f"{path}[{index}]", depth + 1) for index, child in enumerate(item)]
            active.remove(identity)
            return result
        if isinstance(item, str):
            stripped = item.lstrip()
            if stripped.startswith(("{", "[")):
                try:
                    parsed = json.loads(item)
                except (json.JSONDecodeError, RecursionError):
                    parsed = None
                if isinstance(parsed, (dict, list)):
                    cleaned = visit(parsed, path, depth + 1)
                    if cleaned != parsed:
                        return json.dumps(cleaned, ensure_ascii=False, separators=(",", ":"))
            cleaned, changed = _clean_text(item)
            if changed:
                redactions.append(path)
            return cleaned
        if item is None or isinstance(item, (bool, int, float)):
            return item
        return f"[UNSUPPORTED:{type(item).__name__}]"

    return visit(value, "$", 0), redactions
