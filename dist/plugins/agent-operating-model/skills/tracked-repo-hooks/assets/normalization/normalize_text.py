#!/usr/bin/env python3
"""Normalize explicitly selected UTF-8 text files to a declared newline policy."""

from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from pathlib import Path


UTF8_BOM = b"\xef\xbb\xbf"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="report files that need normalization without writing")
    mode.add_argument("--apply", action="store_true", help="normalize selected files in place")
    parser.add_argument("--line-ending", choices=("lf", "crlf"), required=True)
    parser.add_argument("--final-newline", choices=("ensure", "forbid"), required=True)
    parser.add_argument("paths", nargs="+", type=Path, help="explicit UTF-8 text paths to inspect")
    return parser


def normalize(raw: bytes, *, line_ending: str, final_newline: str, path: Path) -> bytes:
    if b"\x00" in raw:
        raise ValueError(f"{path}: binary content contains a NUL byte")
    has_bom = raw.startswith(UTF8_BOM)
    payload = raw[len(UTF8_BOM) :] if has_bom else raw
    try:
        text = payload.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ValueError(f"{path}: content is not valid UTF-8: {error}") from error
    if any(unicodedata.category(character) == "Cc" and character not in "\t\n\r" for character in text):
        raise ValueError(f"{path}: binary/control content contains unsupported control characters")

    newline = "\n" if line_ending == "lf" else "\r\n"
    normalized = re.sub(r"\r\n|\r|\n", newline, text)
    if final_newline == "ensure":
        if not normalized.endswith(newline):
            normalized += newline
    else:
        while normalized.endswith(newline):
            normalized = normalized[: -len(newline)]

    encoded = normalized.encode("utf-8")
    return (UTF8_BOM if has_bom else b"") + encoded


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failed = False
    drifted = False
    for path in args.paths:
        if path.is_symlink() or not path.is_file():
            print(f"error: {path}: not a regular file", file=sys.stderr)
            failed = True
            continue
        try:
            original = path.read_bytes()
            result = normalize(
                original,
                line_ending=args.line_ending,
                final_newline=args.final_newline,
                path=path,
            )
            if result == original:
                print(f"already normalized: {path}")
            elif args.check:
                print(f"needs normalization: {path}")
                drifted = True
            else:
                path.write_bytes(result)
                print(f"normalized: {path}")
        except (OSError, ValueError) as error:
            print(f"error: {error}", file=sys.stderr)
            failed = True

    if failed:
        return 2
    if args.check and drifted:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
