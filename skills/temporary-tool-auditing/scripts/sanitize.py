"""Best-effort removal of common credentials from tool audit evidence."""

import json
import re
from typing import Any

_REDACTED = "[REDACTED]"
_SECRET_KEYS = re.compile(
    r"(?:^|[_-])(password|passwd|secret|token|api[_-]?key|access[_-]?key|"
    r"authorization|proxy[_-]?authorization|cookie|set[_-]?cookie|private[_-]?key)(?:$|[_-])",
    re.IGNORECASE,
)
_PATTERNS = [
    (re.compile(r"-----BEGIN [^-]*PRIVATE KEY-----.*?-----END [^-]*PRIVATE KEY-----", re.I | re.S), _REDACTED),
    (re.compile(r"(?i)\b(Bearer|Basic)\s+[A-Za-z0-9._~+/=-]+"), lambda m: f"{m.group(1)} {_REDACTED}"),
    (re.compile(r"(?i)([a-z][a-z0-9+.-]*://)[^/@\s:]+(?::[^/@\s]*)?@"), lambda m: f"{m.group(1)}{_REDACTED}@"),
    (
        re.compile(
            r"(?i)(\b(?:password|passwd|(?:access|refresh)[_-]?token|token|api[_-]?key|secret)\s*=\s*)([^\s;&]+)"
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
            r"(?i)(--(?:password|passwd|(?:access|refresh)[_-]?token|token|api[_-]?key|secret)(?:=|\s+))([^\s]+)"
        ),
        lambda m: f"{m.group(1)}{_REDACTED}",
    ),
    (re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{20,}\b"), _REDACTED),
    (re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b"), _REDACTED),
    (re.compile(r"\bAKIA[0-9A-Z]{16}\b"), _REDACTED),
    (re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b"), _REDACTED),
]


def _clean_text(value: str) -> tuple[str, bool]:
    cleaned = value
    changed = False
    for pattern, replacement in _PATTERNS:
        updated = pattern.sub(replacement, cleaned)
        changed = changed or updated != cleaned
        cleaned = updated
    return cleaned, changed


def sanitize(value: object) -> tuple[object, list[str]]:
    """Return a JSON-compatible copy and safe JSONPath-like redaction paths."""
    redactions: list[str] = []
    active: set[int] = set()

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
