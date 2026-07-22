#!/usr/bin/env python3
"""Validate the canonical flat skill.zip surface."""

from __future__ import annotations

from project_skills import project_skills


def main() -> int:
    project_skills(write=False)
    print("OK skill-zips: all expected flat zips present and valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
