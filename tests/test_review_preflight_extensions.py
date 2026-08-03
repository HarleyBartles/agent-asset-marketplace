from pathlib import Path
import importlib.util

SPEC = importlib.util.spec_from_file_location("review_preflight", str(Path("tools/review_preflight.py").resolve()))
review_preflight = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(review_preflight)


def _fixture(path: str, content: str):
    return review_preflight.ROOT / path, content


def test_snowflake_in_code_block_is_not_flagged():
    path, content = _fixture(
        "README.md",
        "```\nguild_id 123456789012345678\n```\n",
    )
    findings = []
    review_preflight._scan_security(path, content, findings)
    assert not findings


def test_skill_metadata_missing_is_not_flagged():
    path, content = _fixture(
        "skills/using-foo/SKILL.md",
        "---\nname: using-foo\n---\n",
    )
    findings = []
    review_preflight._scan_skill_metadata(path, content, findings)
    assert not findings


def test_skill_metadata_null_is_flagged():
    path, content = _fixture(
        "skills/using-foo/SKILL.md",
        "---\nname: using-foo\nmetadata: null\n---\n",
    )
    findings = []
    review_preflight._scan_skill_metadata(path, content, findings)
    assert any("present but null/empty" in f for f in findings)


def test_skill_metadata_empty_string_is_flagged():
    path, content = _fixture(
        "skills/using-foo/SKILL.md",
        "---\nname: using-foo\nmetadata: \n---\n",
    )
    findings = []
    review_preflight._scan_skill_metadata(path, content, findings)
    assert any("present but null/empty" in f for f in findings)


def test_skill_metadata_tilde_is_flagged():
    path, content = _fixture(
        "skills/using-foo/SKILL.md",
        "---\nname: using-foo\nmetadata: ~\n---\n",
    )
    findings = []
    review_preflight._scan_skill_metadata(path, content, findings)
    assert any("present but null/empty" in f for f in findings)


def test_skill_metadata_empty_dict_is_flagged():
    path, content = _fixture(
        "skills/using-foo/SKILL.md",
        "---\nname: using-foo\nmetadata: {}\n---\n",
    )
    findings = []
    review_preflight._scan_skill_metadata(path, content, findings)
    assert any("metadata: {}" in f for f in findings)


def test_skill_metadata_valid_is_not_flagged():
    path, content = _fixture(
        "skills/using-foo/SKILL.md",
        (
            "---\n"
            "name: using-foo\n"
            "metadata:\n"
            "  source-id: using-foo\n"
            "  source-path: skills/using-foo/SKILL.md\n"
            "  status: active\n"
            "---\n"
        ),
    )
    findings = []
    review_preflight._scan_skill_metadata(path, content, findings)
    assert not findings


def test_canonical_path_missing_is_flagged():
    path, content = _fixture(
        "skills/using-foo/SKILL.md",
        "Run `subagent-workspace/scripts/does-not-exist`.\n",
    )
    findings = []
    review_preflight._scan_canonical_paths(path, content, findings)
    assert any("does not exist" in f for f in findings)


def test_canonical_path_present_is_not_flagged():
    path, content = _fixture(
        "skills/using-foo/SKILL.md",
        "Run `subagent-workspace/scripts/sdd-workspace`.\n",
    )
    findings = []
    review_preflight._scan_canonical_paths(path, content, findings)
    assert not findings


def test_python_m_without_3_is_flagged():
    for command in ("python -m pytest", "python3 -m pytest"):
        path, content = _fixture("README.md", f"Run `{command}`.\n")
        findings = []
        review_preflight._scan_py3_convention(path, content, findings)
        assert any("py -3 -m" in f for f in findings)


def test_assume_unchanged_flag_is_flagged():
    findings = []
    review_preflight._scan_git_index_flags(
        findings,
        output="h .agents/skills/selecting-a-subagent/SKILL.md\n",
    )
    assert any("assume-unchanged" in f for f in findings)


def test_skip_worktree_flag_is_flagged():
    findings = []
    review_preflight._scan_git_index_flags(
        findings,
        output="S .agents/agents/reviewer-skills.md\n",
    )
    assert any("skip-worktree" in f for f in findings)


def test_normal_index_flag_is_not_flagged():
    findings = []
    review_preflight._scan_git_index_flags(
        findings,
        output="H .agents/skills/selecting-a-subagent/SKILL.md\n",
    )
    assert not findings
