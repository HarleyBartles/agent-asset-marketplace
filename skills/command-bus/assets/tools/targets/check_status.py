#!/usr/bin/env python3
"""Sample read-only target that reports forwarded arguments."""

from __future__ import annotations

import json
import sys


def main() -> int:
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    arguments = sys.argv[2:]
    exit_code = 0
    if "--exit-code" in arguments:
        index = arguments.index("--exit-code")
        try:
            exit_code = int(arguments[index + 1])
        except (IndexError, ValueError):
            print("--exit-code requires an integer", file=sys.stderr)
            return 2
    print(json.dumps({"mode": mode, "arguments": arguments}))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
