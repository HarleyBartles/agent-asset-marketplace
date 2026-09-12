#!/usr/bin/env python3
"""PreToolUse policy gate for the iterative-review hooks pack.

Denies file and exec tool calls that touch a configured deny root (the
review's state, witness, evidence, and acquire directories). Emits a
``{"decision": "block", "reason": ...}`` object on stdout when a call crosses
a deny root; silent success otherwise. Always exits 0 - hook failure must not
abort the session; the state kernel remains the enforcer.
"""

import json
import os
import sys
from pathlib import Path

_PATH_KEYS = ("file_path", "path", "notebook_path", "target_file", "workdir")


def _env() -> dict:
    env_path = os.environ.get("IR_HOOK_ENV") or str(Path(__file__).parent / "hook-env.json")
    try:
        return json.loads(Path(env_path).read_text(encoding="utf-8"))
    except Exception:
        return {}


def _norm(text: str) -> str:
    return text.replace("\\", "/").rstrip("/").lower()


def _deny_roots(env: dict) -> list[str]:
    return [_norm(str(r)) for r in env.get("deny_roots") or [] if str(r).strip()]


def _payload() -> dict | None:
    raw = sys.stdin.read()
    if not raw.strip() and len(sys.argv) > 1:
        raw = sys.argv[1]
    if not raw.strip():
        return None
    try:
        parsed = json.loads(raw)
    except Exception:
        return None
    return parsed if isinstance(parsed, dict) else None


def _extract_paths(tool_input: dict) -> list[str]:
    out = []
    for key in _PATH_KEYS:
        value = tool_input.get(key)
        if isinstance(value, str) and value.strip():
            out.append(value)
    return out


def _touches_deny(text: str, deny_roots: list[str]) -> str | None:
    normed = _norm(text)
    for root in deny_roots:
        if normed == root or normed.startswith(root + "/") or root in normed:
            return root
    return None


def main() -> int:
    env = _env()
    deny_roots = _deny_roots(env)
    if not deny_roots:
        return 0
    payload = _payload()
    if payload is None:
        return 0
    tool_input = payload.get("tool_input")
    if not isinstance(tool_input, dict):
        return 0
    hit = None
    for candidate in _extract_paths(tool_input):
        hit = _touches_deny(candidate, deny_roots)
        if hit:
            break
    if hit is None:
        command = tool_input.get("command")
        if isinstance(command, str):
            hit = _touches_deny(command, deny_roots)
    if hit is not None:
        print(
            json.dumps(
                {
                    "decision": "block",
                    "reason": f"iterative-review: path under sealed review root {hit}",
                },
                separators=(",", ":"),
            )
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
