#!/usr/bin/env python3
"""Validate canonical marketplace skill.zip artifacts and the registry."""

from __future__ import annotations

from skill_zip_artifacts import print_registry_receipt, validate_skill_zip_registry


def main() -> int:
    registry = validate_skill_zip_registry()
    print_registry_receipt(registry)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
