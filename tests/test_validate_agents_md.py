from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "validate_agents_md.py"
SPEC = importlib.util.spec_from_file_location("validate_agents_md_under_test", SCRIPT)
validate_agents_md = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(validate_agents_md)


def _text_with_lines(count: int) -> str:
    return "\n".join(f"line {number}" for number in range(count))


def test_root_agents_line_count_is_quiet_at_55_lines() -> None:
    assert validate_agents_md._root_line_count_finding(_text_with_lines(55)) is None


def test_root_agents_line_count_warns_above_55_lines() -> None:
    assert validate_agents_md._root_line_count_finding(_text_with_lines(56)) == (
        "warning",
        "Root AGENTS.md has 56 lines; consider routing detail after 55 lines",
    )


def test_root_agents_line_count_fails_above_100_lines() -> None:
    assert validate_agents_md._root_line_count_finding(_text_with_lines(101)) == (
        "error",
        "Root AGENTS.md exceeds 100 lines (found 101)",
    )
