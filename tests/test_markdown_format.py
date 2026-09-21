from pathlib import Path
import tomllib

import mdformat
import yaml


ROOT = Path(__file__).resolve().parents[1]


def test_formatter_preserves_yaml_frontmatter_semantics_and_delimiters() -> None:
    source = """---
name: example-skill
description: Use when a formatter must preserve skill metadata.
metadata:
  use_when:
  - markdown is formatted
license: MIT
---
# Example

This paragraph is split across
several source lines without semantic breaks.
"""
    config = tomllib.loads((ROOT / ".mdformat.toml").read_text(encoding="utf-8"))

    formatted = mdformat.text(
        source,
        options={"wrap": config["wrap"], "end_of_line": config["end_of_line"]},
        extensions=set(config["extensions"]),
    )

    assert formatted.startswith("---\n")
    frontmatter, body = formatted.removeprefix("---\n").split("\n---\n", maxsplit=1)
    original_frontmatter = source.removeprefix("---\n").split("\n---\n", maxsplit=1)[0]
    assert yaml.safe_load(frontmatter) == yaml.safe_load(original_frontmatter)
    assert "This paragraph is split across several source lines without semantic breaks." in body
