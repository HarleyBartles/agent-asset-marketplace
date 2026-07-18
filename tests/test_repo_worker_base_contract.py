from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = REPO_ROOT / "sources" / "first_party" / "skills"
REPO_WORKER_BASE = SOURCE_ROOT / "repo-worker-base"
ROUTER = SOURCE_ROOT / "work-mode-router" / "SKILL.md"
ROUTER_PROMPT = SOURCE_ROOT / "work-mode-router" / "agents" / "openai.yaml"

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


def test_router_route_states_cannot_bypass_repo_worker_base():
    text = ROUTER.read_text(encoding="utf-8")
    route_expectations = {
        "worktree_isolation_needed": "repo-worker-base` -> `worktree-and-branch-policy.md` -> local repository policy -> `/using-git-worktrees`",
        "design_needed": "repo-worker-base` -> `design-baseline.md` + local `.agents/guides/design-guide.md` -> `/brainstorming`",
        "planning_needed": "repo-worker-base` -> `planning-baseline.md` + local `.agents/guides/planning-guide.md` -> `/writing-plans`",
        "approved_plan_execution_ready": "repo-worker-base` -> matching baseline + local `.agents/guides/` guide -> `/using-superpowers`",
        "implementation_in_progress": "repo-worker-base` -> `implementation-baseline.md` + local `.agents/guides/implementing-guide.md` -> implementing lane skills",
        "code_review_needed": "repo-worker-base` -> `code-review-baseline.md` + local `.agents/guides/code-review-guide.md` -> `/requesting-code-review`",
        "preflight_needed": "repo-worker-base` -> `planning-baseline.md` + local `.agents/guides/planning-guide.md` -> `/using-superpowers`",
        "preflight_complete_pending_approval": "repo-worker-base` verifies the planning baseline and local `.agents/guides/planning-guide.md`",
        "stale_plan_repair_needed": "repo-worker-base` -> `implementation-baseline.md` + local `.agents/guides/implementing-guide.md` -> `/using-superpowers`",
    }
    for route_name, handoff in route_expectations.items():
        route_line = next(line for line in text.splitlines() if line.startswith(f"| `{route_name}` |"))
        assert handoff in route_line, f"{route_name} bypasses the required base handoff"


def test_router_routing_map_cannot_bypass_repo_worker_base():
    text = ROUTER.read_text(encoding="utf-8")
    route_expectations = {
        "worktree_isolation_needed": "repo-worker-base` + worktree policy/local repository policy -> `/using-git-worktrees`",
        "design_needed": "repo-worker-base` + `design-baseline.md` + local `.agents/guides/design-guide.md` -> `/brainstorming`",
        "planning_needed": "repo-worker-base` + `planning-baseline.md` + local `.agents/guides/planning-guide.md` -> `/writing-plans`",
        "approved_plan_execution_ready": "repo-worker-base` + matching baseline/local guide -> `/using-superpowers`",
        "implementation_in_progress": "repo-worker-base` + `implementation-baseline.md` + local `.agents/guides/implementing-guide.md` -> `/executing-plans`",
        "code_review_needed": "repo-worker-base` + `code-review-baseline.md` + local `.agents/guides/code-review-guide.md` -> `/requesting-code-review`",
        "repo_worker_coding": "repo-worker-base` + matching baseline/local guide -> `/using-superpowers`",
        "repo_or_source_evidence": "repo-worker-base` + baseline for the active stage/local guide -> the evidence or implementation lane",
        "github_proof": "repo-worker-base` + implementation or review baseline/local guide -> the GitHub proof surface",
    }
    for route_name, handoff in route_expectations.items():
        route_line = next(line for line in text.splitlines() if line.startswith(f"- `{route_name}` ->"))
        assert handoff in route_line, f"{route_name} routing map bypasses the required base handoff"


def test_router_prompt_metadata_uses_the_mandatory_handoff():
    router_text = ROUTER.read_text(encoding="utf-8")
    frontmatter = router_text.split("---", 2)[1]
    assert "routing repository-backed work through /repo-worker-base" in frontmatter
    assert "routing normal coding work to /using-superpowers" not in frontmatter

    text = ROUTER_PROMPT.read_text(encoding="utf-8")
    assert "routing repository-backed work through /repo-worker-base" in text
    assert "baseline and local .agents/guides/ guide, then /using-superpowers" in text
    assert "Do not recursively" in text
    assert "/work-mode-router after classification" in text
    assert "routing normal coding work to /using-superpowers" not in text


def test_router_phase_table_and_guide_discovery_use_canonical_guide_home():
    text = ROUTER.read_text(encoding="utf-8")
    phase_table = text.split("## Working Mode Phases", 1)[1].split("## Superpowers Workflow Mapping", 1)[0]
    assert ".agents/guides/design-guide.md" in phase_table
    assert ".agents/guides/planning-guide.md" in phase_table
    assert ".agents/guides/implementing-guide.md" in phase_table
    assert ".agents/guides/code-review-guide.md" in phase_table
    assert ".agents/docs/guides/" not in phase_table

    guide_discovery = text.split("## Workflow Enforcement", 1)[1].split("## Golden-gate reminder", 1)[0]
    assert "When a repo has guides in `.agents/guides/`, reference them explicitly" in guide_discovery
    assert ".agents/docs/guides/" not in guide_discovery


def test_consuming_repository_stage_guides_use_canonical_agents_guides_home():
    canonical = REPO_ROOT / ".agents" / "guides"
    legacy = REPO_ROOT / ".agents" / "docs" / "guides"

    assert legacy.is_dir(), "the existing legacy guide home documents the RED baseline"
    missing = [name for name in STAGE_GUIDES if not (canonical / name).is_file()]
    assert not missing, f"missing canonical stage guides: {missing}"
