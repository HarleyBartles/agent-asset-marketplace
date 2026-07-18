from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = REPO_ROOT / "sources" / "first_party" / "skills"
REPO_WORKER_BASE = SOURCE_ROOT / "repo-worker-base"
ROUTER = SOURCE_ROOT / "work-mode-router" / "SKILL.md"

REFERENCE_FILENAMES = (
    "worktree-and-branch-policy.md",
    "mutation-script-safety.md",
    "script-entrypoint-contract.md",
    "repository-layout-and-mesh.md",
    "stage-guide-contract.md",
    "design-baseline.md",
    "planning-baseline.md",
    "implementation-baseline.md",
    "code-review-baseline.md",
    "superpowers-composition.md",
)

STAGE_GUIDES = (
    "design-guide.md",
    "planning-guide.md",
    "implementing-guide.md",
    "code-review-guide.md",
)


def test_repo_worker_base_exposes_all_focused_references():
    references = REPO_WORKER_BASE / "references"
    missing = [name for name in REFERENCE_FILENAMES if not (references / name).is_file()]
    assert not missing, f"missing repo-worker-base references: {missing}"


def test_repo_worker_base_source_has_no_machine_specific_drive_assumptions():
    source_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in REPO_WORKER_BASE.rglob("*")
        if path.is_file() and path.suffix in {".md", ".yaml", ".yml"}
    )
    assert "Z:" not in source_text
    assert "C:" not in source_text


def test_worktree_policy_uses_portable_resolution_and_scratch_conventions():
    policy_path = REPO_WORKER_BASE / "references" / "worktree-and-branch-policy.md"
    assert policy_path.is_file(), f"missing worktree policy: {policy_path}"
    policy = policy_path.read_text(encoding="utf-8")
    for required in (
        "git rev-parse --show-toplevel",
        "git rev-parse --git-common-dir",
        "_agent-worktrees",
        "_agent-scratch",
    ):
        assert required in policy


def test_router_requires_base_before_downstream_lane():
    text = ROUTER.read_text(encoding="utf-8")
    assert "repo-worker-base" in text
    assert text.index("repo-worker-base") < text.index("using-superpowers")


def test_router_contract_covers_composition_ownership_and_non_recursion():
    text = ROUTER.read_text(encoding="utf-8")
    required = (
        "work-mode-router` -> `repo-worker-base` -> matching baseline reference and local `.agents/guides/` guide -> Superpowers lane",
        "The router owns first classification",
        "`repo-worker-base` owns portable repo hygiene, composition",
        "do not invoke `work-mode-router` recursively",
        "planning-baseline.md",
        "implementation-baseline.md",
        "code-review-baseline.md",
        ".agents/guides/design-guide.md",
        ".agents/guides/planning-guide.md",
        ".agents/guides/implementing-guide.md",
        ".agents/guides/code-review-guide.md",
        "source evidence",
        "publication",
        "review",
    )
    missing = [snippet for snippet in required if snippet not in text]
    assert not missing, f"router contract is missing: {missing}"


def test_router_routes_each_repo_worker_stage_to_the_downstream_superpowers_lane():
    text = ROUTER.read_text(encoding="utf-8")
    for lane in ("/brainstorming", "/writing-plans", "/executing-plans", "/subagent-driven-development", "/requesting-code-review"):
        assert lane in text, f"missing Superpowers lane route: {lane}"
    assert text.index("/repo-worker-base") < text.index("/writing-plans")
    assert text.index("/repo-worker-base") < text.index("/requesting-code-review")


def test_consuming_repository_stage_guides_use_canonical_agents_guides_home():
    canonical = REPO_ROOT / ".agents" / "guides"
    legacy = REPO_ROOT / ".agents" / "docs" / "guides"

    assert legacy.is_dir(), "the existing legacy guide home documents the RED baseline"
    missing = [name for name in STAGE_GUIDES if not (canonical / name).is_file()]
    assert not missing, f"missing canonical stage guides: {missing}"
