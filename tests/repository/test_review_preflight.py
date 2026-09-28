from pathlib import Path
import importlib.util

SPEC = importlib.util.spec_from_file_location("review_preflight", str(Path("tools/review_preflight.py").resolve()))
review_preflight = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(review_preflight)


def _fixture(path: str, content: str):
    return review_preflight.ROOT / path, content


def test_snowflake_with_context_is_flagged():
    path, content = _fixture(
        "skills/test/SKILL.md",
        "The main guild has guild_id 123456789012345678.\n",
    )
    findings = []
    review_preflight._scan_security(path, content, findings)
    assert any("possible real identifier" in f for f in findings)


def test_snowflake_without_context_is_not_flagged():
    path, content = _fixture(
        "README.md",
        "The count is 123456789012345678.\n",
    )
    findings = []
    review_preflight._scan_security(path, content, findings)
    assert not findings


def test_email_is_flagged():
    path, content = _fixture("README.md", "Contact admin@example.com.\n")
    findings = []
    review_preflight._scan_security(path, content, findings)
    assert any("email address" in f for f in findings)


def test_email_in_hash_pinned_reference_snapshot_is_not_flagged():
    path, content = _fixture(
        "codex-marketplace/plugins/example/skills/example/assets/authority/reference-source/upstream/source.txt",
        "Upstream contact: maintainer@example.com.\n",
    )
    findings = []
    review_preflight._scan_security(path, content, findings)
    assert not findings


def test_stale_subagent_path_is_flagged():
    path, content = _fixture(
        "skills/using-foo/SKILL.md",
        "Run `subagent-driven-development/scripts/sdd-workspace`.\n",
    )
    findings = []
    review_preflight._scan_stale_paths(path, content, findings)
    assert any("stale path" in f for f in findings)


def test_skill_license_nested_is_flagged():
    path, content = _fixture(
        "skills/using-foo/SKILL.md",
        "---\nname: using-foo\nmetadata:\n  license: MIT\n---\n",
    )
    findings = []
    review_preflight._scan_skill_frontmatter(path, content, findings)
    assert any("`license` is nested" in f for f in findings)


def test_markdown_table_missing_trailing_pipe():
    path, content = _fixture(
        "references/table.md",
        "| a | b\n| c | d |\n",
    )
    findings = []
    review_preflight._scan_markdown_tables(path, content, findings)
    assert any("does not end with" in f for f in findings)


def test_py_m_without_3_is_flagged():
    path, content = _fixture("README.md", "Run `py -m pytest`.\n")
    findings = []
    review_preflight._scan_py3_convention(path, content, findings)
    assert any("py -3 -m" in f for f in findings)


def test_new_plugin_default_enabled_true_is_flagged():
    path, content = _fixture(
        "tools/new_plugin.py",
        '    "enabled": True\n',
    )
    findings = []
    review_preflight._scan_new_plugin(path, content, findings)
    assert any("enabled: false" in f for f in findings)


def test_new_plugin_bogus_return_is_flagged():
    path, content = _fixture(
        "tools/new_plugin.py",
        "    return 0 if result is None or args.check else 1\n",
    )
    findings = []
    review_preflight._scan_new_plugin(path, content, findings)
    assert any("dry-run and validation-error exit codes" in f for f in findings)
