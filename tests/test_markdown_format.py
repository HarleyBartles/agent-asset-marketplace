from pathlib import Path
import json
import tomllib

import mdformat
import yaml


ROOT = Path(__file__).resolve().parents[1]


def test_repository_uses_portable_markdown_formatter_wiring() -> None:
    requirements = (ROOT / "requirements.txt").read_text(encoding="utf-8")
    runner = (ROOT / "tools/run.py").read_text(encoding="utf-8")
    commands = json.loads((ROOT / ".agents/contracts/repo-standards-commands.json").read_text(encoding="utf-8"))

    assert "-r .agents/skills/markdown-formatting/requirements.txt" in requirements
    assert "mdformat==" not in requirements
    assert "_all_tracked_markdown_files" not in runner
    assert "_run_mdformat" not in runner
    assert commands["apply"][0] == [
        "@python",
        ".agents/skills/markdown-formatting/scripts/format_markdown.py",
        "--apply",
    ]
    assert commands["check"][0] == [
        "@python",
        ".agents/skills/markdown-formatting/scripts/format_markdown.py",
        "--check",
    ]


def test_installed_markdown_formatter_matches_canonical_source() -> None:
    canonical = ROOT / "codex-marketplace/plugins/agent-operating-model/skills/markdown-formatting"
    installed = ROOT / ".agents/skills/markdown-formatting"
    canonical_files = {
        path.relative_to(canonical)
        for path in canonical.rglob("*")
        if path.is_file() and "__pycache__" not in path.parts
    }
    installed_files = {
        path.relative_to(installed)
        for path in installed.rglob("*")
        if path.is_file() and "__pycache__" not in path.parts
    }

    assert installed_files == canonical_files
    for relative in canonical_files:
        assert (installed / relative).read_bytes() == (canonical / relative).read_bytes()


def test_aggregate_markdown_producers_use_scoped_checks() -> None:
    owners = [
        ROOT / "codex-marketplace/plugins/repo-worker-pack/skills/generating-agent-mesh/scripts/generate_index_mesh.py",
        ROOT / "tools/new_plugin.py",
        ROOT / "codex-marketplace/plugins/agent-operating-model/skills/repo-shape/scripts/repo_standards.py",
        ROOT / "tools/sync_skill_shared_references.py",
    ]

    for owner in owners:
        source = owner.read_text(encoding="utf-8")
        assert "_check_markdown_outputs" in source
        assert '"--check-files"' in source


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


def test_formatter_writes_visible_consecutive_ordered_list_numbers() -> None:
    source = """# Checks

1. First
1. Second
1. Third
"""
    config = tomllib.loads((ROOT / ".mdformat.toml").read_text(encoding="utf-8"))

    formatted = mdformat.text(
        source,
        options={
            "wrap": config["wrap"],
            "end_of_line": config["end_of_line"],
            "number": config["number"],
        },
        extensions=set(config["extensions"]),
    )

    assert "1. First\n2. Second\n3. Third" in formatted
