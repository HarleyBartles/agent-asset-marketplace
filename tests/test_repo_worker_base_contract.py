import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest


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

MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
PRESSURE_ROOT = REPO_ROOT / "tests" / "pressure" / "repo-worker-base"
SDD_ROOT = REPO_ROOT / ".agents" / "superpowers" / "sdd"
SDD_SESSION = SDD_ROOT / "2026-07-18-repo-worker-base-hygiene-and-composition"


def _run_git(cwd: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(cwd), *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def _init_repository(path: Path) -> Path:
    subprocess.run(
        ["git", "init", "--initial-branch=main", str(path)],
        check=True,
        capture_output=True,
        text=True,
    )
    _run_git(path, "config", "user.email", "repo-worker-tests@example.invalid")
    _run_git(path, "config", "user.name", "Repo Worker Tests")
    (path / "README.md").write_text("fixture\n", encoding="utf-8", newline="\n")
    _run_git(path, "add", "README.md")
    _run_git(path, "commit", "-m", "test fixture")
    return path


def _resolve_worker_locations(start_path: Path, *, allow_shared_checkout: bool = False) -> dict[str, Path | str]:
    superproject = _run_git(start_path, "rev-parse", "--show-superproject-working-tree")
    if superproject:
        raise ValueError("submodule checkouts are rejected")
    current_checkout = Path(_run_git(start_path, "rev-parse", "--show-toplevel")).resolve()

    common_git = Path(
        _run_git(current_checkout, "rev-parse", "--path-format=absolute", "--git-common-dir")
    ).resolve()
    checkout_git = Path(
        _run_git(current_checkout, "rev-parse", "--path-format=absolute", "--git-dir")
    ).resolve()
    is_shared_checkout = os.path.normcase(str(checkout_git)) == os.path.normcase(str(common_git))
    if is_shared_checkout and not allow_shared_checkout:
        raise ValueError("shared checkout requires an explicit override")

    main_checkout = common_git.parent
    repository_name = main_checkout.name
    branch_name = _run_git(current_checkout, "branch", "--show-current")
    return {
        "current_checkout": current_checkout,
        "main_checkout": main_checkout,
        "external_worktree_root": main_checkout.parent / "_agent-worktrees" / repository_name,
        "external_scratch_root": main_checkout.parent / "_agent-scratch" / repository_name / branch_name,
    }


def _assert_local_markdown_links_resolve(path: Path) -> None:
    for raw_target in MARKDOWN_LINK.findall(path.read_text(encoding="utf-8")):
        clean_target = raw_target.split("#", 1)[0]
        if not clean_target or clean_target.startswith(("http://", "https://", "mailto:")):
            continue
        if clean_target.startswith((".agents/", "docs/", "sources/", "tools/")):
            resolved = (REPO_ROOT / clean_target).resolve()
        else:
            resolved = (path.parent / clean_target).resolve()
        assert resolved.exists(), f"broken local link in {path.relative_to(REPO_ROOT)}: {raw_target}"


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
        "rev-parse --show-toplevel",
        "rev-parse --path-format=absolute --git-common-dir",
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
        route_lines = [line for line in text.splitlines() if line.startswith(f"| `{route_name}` |")]
        assert len(route_lines) == 1, f"expected one {route_name} route-state entry, found {len(route_lines)}"
        assert handoff in route_lines[0], f"{route_name} bypasses the required base handoff"


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
    }
    for route_name, handoff in route_expectations.items():
        route_lines = [line for line in text.splitlines() if line.startswith(f"- `{route_name}` ->")]
        assert len(route_lines) == 1, f"expected one {route_name} routing-map entry, found {len(route_lines)}"
        assert handoff in route_lines[0], f"{route_name} routing map bypasses the required base handoff"

    github_routes = [line for line in text.splitlines() if line.startswith("- `github_proof` ->")]
    assert len(github_routes) == 1, f"expected one github_proof routing entry, found {len(github_routes)}"
    assert "repo-worker-base` + implementation or review baseline/local guide -> the repo/GitHub proof surface" in github_routes[0]


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

    assert not legacy.exists(), "the retired .agents/docs/guides home must not remain"
    missing = [name for name in STAGE_GUIDES if not (canonical / name).is_file()]
    assert not missing, f"missing canonical stage guides: {missing}"


def test_worktree_policy_uses_git_anchored_absolute_resolution_and_preserves_gates():
    policy = (REPO_WORKER_BASE / "references" / "worktree-and-branch-policy.md").read_text(encoding="utf-8")
    implementation = (REPO_WORKER_BASE / "references" / "implementation-baseline.md").read_text(encoding="utf-8")

    for required in (
        "git -C <start-path> rev-parse --show-toplevel",
        "git -C <current-checkout> rev-parse --path-format=absolute --git-common-dir",
        "git -C <current-checkout> rev-parse --path-format=absolute --git-dir",
        "## Fresh-main gate",
        "## Worktree isolation and verification gate",
        "git worktree list",
        "## Branch and PR gate",
        "## Worktree stop signs",
    ):
        assert required in policy

    for forbidden in (
        "current_checkout / common_git",
        "Path(__file__).parent",
        "walk filesystem parents",
    ):
        assert forbidden not in policy

    for required in (
        "## Validation and publication gate",
        "## GREEN gate",
        "## Required return evidence",
        "## Stop signs",
    ):
        assert required in implementation


@pytest.mark.parametrize("nested", [False, True], ids=["root", "nested"])
def test_portable_resolution_from_shared_main_checkout_requires_override(tmp_path: Path, nested: bool):
    repository = _init_repository(tmp_path / "portable-repo")
    start_path = repository
    if nested:
        start_path = repository / "nested" / "path"
        start_path.mkdir(parents=True)

    with pytest.raises(ValueError, match="shared checkout"):
        _resolve_worker_locations(start_path)

    resolved = _resolve_worker_locations(start_path, allow_shared_checkout=True)
    assert resolved["current_checkout"] == repository.resolve()
    assert resolved["main_checkout"] == repository.resolve()
    assert resolved["external_worktree_root"] == tmp_path / "_agent-worktrees" / repository.name
    assert resolved["external_scratch_root"] == tmp_path / "_agent-scratch" / repository.name / "main"


@pytest.mark.parametrize("nested", [False, True], ids=["root", "nested"])
def test_portable_resolution_from_linked_worktree_finds_main_checkout(tmp_path: Path, nested: bool):
    repository = _init_repository(tmp_path / "portable-repo")
    linked = tmp_path / "linked-checkout"
    _run_git(repository, "worktree", "add", "-b", "feature/portable", str(linked))
    start_path = linked
    if nested:
        start_path = linked / "nested" / "path"
        start_path.mkdir(parents=True)

    resolved = _resolve_worker_locations(start_path)
    assert resolved["current_checkout"] == linked.resolve()
    assert resolved["main_checkout"] == repository.resolve()
    assert resolved["external_worktree_root"] == tmp_path / "_agent-worktrees" / repository.name
    assert resolved["external_scratch_root"] == tmp_path / "_agent-scratch" / repository.name / "feature" / "portable"


def test_portable_resolution_rejects_submodule_even_with_shared_override(tmp_path: Path):
    child = _init_repository(tmp_path / "child-repo")
    superproject = _init_repository(tmp_path / "superproject")
    subprocess.run(
        [
            "git",
            "-c",
            "protocol.file.allow=always",
            "-C",
            str(superproject),
            "submodule",
            "add",
            str(child),
            "modules/child",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    submodule = superproject / "modules" / "child"

    with pytest.raises(ValueError, match="submodule"):
        _resolve_worker_locations(submodule, allow_shared_checkout=True)


def test_moved_guides_and_mesh_agent_references_have_resolvable_local_targets():
    guide_root = REPO_ROOT / ".agents" / "guides"
    link_surfaces = [
        *sorted(guide_root.glob("*.md")),
        REPO_ROOT / ".agents" / "INDEX.md",
        REPO_ROOT / ".agents" / "AGENTS.md",
        REPO_ROOT / ".agents" / "docs" / "INDEX.md",
        REPO_ROOT / ".agents" / "docs" / "AGENTS.md",
        guide_root / "AGENTS.md",
        REPO_ROOT / "tools" / "AGENTS.md",
    ]
    for path in link_surfaces:
        _assert_local_markdown_links_resolve(path)

    routed_targets = {
        REPO_ROOT / ".agents" / "AGENTS.md": (
            REPO_ROOT / ".agents" / "docs" / "mesh-policy.md",
            REPO_ROOT / ".agents" / "docs" / "INDEX.md",
            guide_root / "AGENTS.md",
        ),
        REPO_ROOT / ".agents" / "docs" / "AGENTS.md": (
            REPO_ROOT / ".agents" / "docs" / "mesh-policy.md",
            guide_root / "AGENTS.md",
        ),
        guide_root / "AGENTS.md": (
            REPO_ROOT / ".agents" / "docs" / "mesh-policy.md",
            guide_root / "INDEX.md",
        ),
        REPO_ROOT / "tools" / "AGENTS.md": tuple(guide_root / name for name in STAGE_GUIDES),
    }
    for router, targets in routed_targets.items():
        assert router.is_file(), f"missing router: {router.relative_to(REPO_ROOT)}"
        missing = [target.relative_to(REPO_ROOT) for target in targets if not target.exists()]
        assert not missing, f"{router.relative_to(REPO_ROOT)} routes to missing targets: {missing}"


def test_marketplace_generation_guide_uses_supported_mesh_check_mode():
    guide = REPO_ROOT / ".agents" / "guides" / "marketplace-generation-guide.md"
    text = guide.read_text(encoding="utf-8")
    assert "generate_index_mesh.py --validate" not in text
    assert text.count("generate_index_mesh.py --check") >= 2


def test_local_guides_cannot_override_the_mandatory_superpowers_mapping():
    text = ROUTER.read_text(encoding="utf-8")
    assert "the repo guide takes precedence" not in text
    assert "Local guides cannot override or bypass this canonical mapping" in text
    assert "paths, commands, exclusions, CI, and exceptions" in text


def test_portable_resolution_checks_submodule_status_from_supplied_start_path_first(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    repository = _init_repository(tmp_path / "portable-repo")
    start_path = repository / "nested" / "path"
    start_path.mkdir(parents=True)
    calls: list[tuple[Path, tuple[str, ...]]] = []
    real_run_git = _run_git

    def recording_run_git(path: Path, *args: str) -> str:
        calls.append((Path(path), args))
        return real_run_git(path, *args)

    monkeypatch.setattr(sys.modules[__name__], "_run_git", recording_run_git)
    _resolve_worker_locations(start_path, allow_shared_checkout=True)

    assert calls[0] == (start_path, ("rev-parse", "--show-superproject-working-tree"))
    assert calls[1] == (start_path, ("rev-parse", "--show-toplevel"))


def test_sdd_mesh_respects_gitignore_for_session_directories():
    gitignore = SDD_ROOT / ".gitignore"
    child_index = SDD_SESSION / "INDEX.md"
    assert gitignore.is_file()
    assert not child_index.is_file(), "generated INDEX.md must not be created inside gitignored SDD sessions"

    relative_gitignore = gitignore.relative_to(REPO_ROOT).as_posix()
    tracked = subprocess.run(
        ["git", "ls-files", "--error-unmatch", relative_gitignore],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert tracked.returncode == 0, f"SDD .gitignore scaffold is absent from Git HEAD: {relative_gitignore}"

    ignored = subprocess.run(
        ["git", "check-ignore", "-q", child_index.relative_to(REPO_ROOT).as_posix()],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert ignored.returncode == 0, "SDD session INDEX.md path must be ignored"

    ignored_session_artifact = SDD_SESSION / "task-2-brief.md"
    ignored = subprocess.run(
        ["git", "check-ignore", "-q", ignored_session_artifact.relative_to(REPO_ROOT).as_posix()],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert ignored.returncode == 0, "ordinary SDD session artifacts must remain ignored"


def test_pressure_campaign_is_structured_for_red_green_refactor_execution():
    fixture_path = PRESSURE_ROOT / "campaign.json"
    assert fixture_path.is_file(), "missing structured repo-worker-base pressure campaign"
    campaign = json.loads(fixture_path.read_text(encoding="utf-8"))

    assert campaign["schema_version"] == 1
    runtime_results = campaign["runtime_results"]
    assert len(runtime_results) == 11
    assert campaign["runtime_execution"]["scenario_context_count"] == 6
    assert campaign["runtime_execution"]["independent_micro_test_context_count"] == 5
    assert sum(result["context_kind"] == "scenario" for result in runtime_results) == 6
    assert sum(result["context_kind"] == "independent_micro_test" for result in runtime_results) == 5
    assert all(result["fresh_codex_subagent_context"] for result in runtime_results)
    assert all(result["source_rollout"] and result["raw_response_excerpt"] for result in runtime_results)
    assert set(campaign["evidence_shape"]) == {"RED", "GREEN", "REFACTOR"}
    for phase, required_fields in campaign["evidence_shape"].items():
        assert required_fields, f"{phase} evidence shape must declare required fields"

    scenarios = campaign["combined_pressure_scenarios"]
    assert len(scenarios) >= 3
    assert len({scenario["id"] for scenario in scenarios}) == len(scenarios)
    for scenario in scenarios:
        assert len(scenario["pressures"]) >= 3
        assert scenario["no_guidance_control"]["prompt"]
        assert scenario["guided_variant"]["prompt"]
        assert scenario["expected_behavior"]

    micro_tests = campaign["micro_tests"]
    assert len(micro_tests) >= 5
    assert len({case["id"] for case in micro_tests}) == len(micro_tests)
    for case in micro_tests:
        assert case["no_guidance_control"]["prompt"]
        assert case["guided_variant"]["prompt"]
        assert case["expected_behavior"]

    assert not (PRESSURE_ROOT / "repo-backed-superpowers-lane.md").exists()
    assert not (PRESSURE_ROOT / "worktree-resolution.md").exists()
