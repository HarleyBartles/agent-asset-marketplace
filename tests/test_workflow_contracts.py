from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

import pytest
import yaml


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "codex-marketplace" / "plugins" / "superpowers-plus" / "skills"
REPO_SKILLS = ROOT / "codex-marketplace" / "plugins" / "repo-worker-pack" / "skills"
OPERATING_SKILLS = ROOT / "codex-marketplace" / "plugins" / "agent-operating-model" / "skills"
DOCS = ROOT / "tests" / "pressure" / "workflow-contracts"
sys.path.insert(0, str(ROOT / "tools"))
import run_workflow_pressure_campaign as campaign_runner  # noqa: E402
import review_preflight  # noqa: E402
import skill_validation  # noqa: E402
import workflow_pressure_scan as pressure_scan  # noqa: E402


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _canonical_skill_names() -> set[str]:
    names = set()
    for path in (ROOT / "codex-marketplace" / "plugins").rglob("SKILL.md"):
        match = re.search(r"^name:\s*['\"]?([^\s'\"]+)", _read(path), re.MULTILINE)
        if match:
            names.add(match.group(1))
    return names


def _active_instruction_surfaces() -> list[Path]:
    local_roots = [
        ROOT / "AGENTS.md",
        ROOT / "CONTRIBUTING.md",
        ROOT / "REVIEW.md",
        ROOT / ".agents" / "doctrine",
        ROOT / ".agents" / "contracts",
        ROOT / ".agents" / "plans",
        ROOT / ".agents" / "runbooks",
        ROOT / ".agents" / "playbooks",
        ROOT / ".agents" / "skills",
        ROOT / ".devin" / "rules",
    ]
    paths = []
    for root in local_roots:
        if root.is_file():
            paths.append(root)
        elif root.is_dir():
            paths.extend(
                path
                for path in root.rglob("*")
                if path.is_file()
                and path.suffix.lower() in {"", ".md", ".json", ".yaml", ".yml"}
                and "completed" not in path.parts
            )
    plugin_root = ROOT / "codex-marketplace" / "plugins"
    paths.extend(
        path
        for path in plugin_root.rglob("*")
        if path.is_file() and path.suffix.lower() in {"", ".md", ".json", ".yaml", ".yml"}
    )
    return sorted(set(paths))


class TestAuthorityBootstrapPortability:
    def test_superpowers_plus_version_matches_pinned_upstream_release(self):
        plugin = json.loads(_read(SKILLS.parent / ".codex-plugin" / "plugin.json"))
        bundle = json.loads(_read(SKILLS.parent / "references" / "bundle-manifest.json"))
        source = _read(SKILLS.parent / "SOURCE.md")
        assert plugin["version"] == "6.4.1"
        assert bundle["bundle_version"] == "6.4.1"
        assert "5bf4e78011075bcfc0dc295f0724994cd123ee71" in source

    def test_superpowers_plus_retains_first_party_helper_inventory(self):
        bundle = json.loads(_read(SKILLS.parent / "references" / "bundle-manifest.json"))
        names = {entry["canonical_name"] for entry in bundle["entries"]}
        assert {
            "asking-clarifying-questions",
            "handoff-gates",
            "inspecting-the-environment",
            "iterative-review",
            "publishing-source",
            "selecting-a-subagent",
            "subagent-workspace",
            "writing-roadmaps",
        } <= names

    def test_superpowers_plus_bundles_session_diagnostics(self):
        bundle = json.loads(_read(SKILLS.parent / "references" / "bundle-manifest.json"))
        names = {entry["canonical_name"] for entry in bundle["entries"]}
        assert "diagnosing-superpowers" in names
        assert (SKILLS / "diagnosing-superpowers" / "SKILL.md").is_file()

    def test_operating_contract_declares_shared_authority(self):
        path = REPO_SKILLS / "base-doctrine" / "references" / "operating-contract.md"
        text = _read(path)
        lowered = text.lower()
        assert "explicit human instruction" in lowered
        assert "owning skill" in lowered
        assert "reversible" in lowered

    def test_bootstrap_classifies_before_loading_broad_doctrine(self):
        text = _read(SKILLS / "using-superpowers-plus" / "SKILL.md")
        lowered = text.lower()
        assert lowered.index("classify the request") < lowered.index("load only selected doctrine")
        assert "stop reading" in text.lower()

    def test_portable_roots_do_not_encode_machine_or_repo_commands(self):
        for path in (REPO_SKILLS / "base-doctrine" / "SKILL.md", REPO_SKILLS / "repo-worker-base" / "SKILL.md"):
            text = _read(path)
            assert "Z:\\" not in text
            assert "tools/run.py" not in text

    def test_owner_applicability_is_not_overridden_by_callers(self):
        text = _read(REPO_SKILLS / "base-doctrine" / "references" / "operating-contract.md")
        assert "cannot bypass" in text
        assert "applicability" in text

    def test_operating_contract_requires_authority_for_new_workflow_semantics(self):
        text = " ".join(_read(REPO_SKILLS / "base-doctrine" / "references" / "operating-contract.md").lower().split())
        for phrase in (
            "only authority can change what the workflow means",
            "implementation detail",
            "environment marker",
            "reproduced failure",
            "preserve the existing workflow semantics",
        ):
            assert phrase in text

    def test_bootstrap_stops_expansion_without_a_route_changing_question(self):
        text = _read(SKILLS / "using-superpowers-plus" / "SKILL.md").lower()
        assert "concrete unresolved question" in text
        assert "might be useful" in text

    def test_sdd_stops_for_human_owned_requirements_but_rules_technical_findings(self):
        text = _read(SKILLS / "subagent-driven-development" / "SKILL.md").lower()
        assert "human-owned requirements" in text
        assert "product/canon" in text
        assert "already authorized" in text
        assert "only reasons to stop are the four named below" not in text
        assert "unauthorized irreversible or destructive" in text

    def test_portable_skill_tree_has_no_absolute_machine_paths(self):
        machine_path = re.compile(r"(?<!\w)[A-Za-z]:[\\/]+[A-Za-z0-9_.-]")
        text_suffixes = {"", ".md", ".py", ".json", ".ps1", ".js", ".ts", ".yml", ".yaml", ".txt"}
        offenders = []
        for root in (SKILLS, REPO_SKILLS, OPERATING_SKILLS):
            for path in root.rglob("*"):
                if not path.is_file() or path.suffix.lower() not in text_suffixes or "__pycache__" in path.parts:
                    continue
                text = path.read_text(encoding="utf-8", errors="replace")
                if machine_path.search(text):
                    offenders.append(path.relative_to(ROOT).as_posix())
        assert offenders == []


class TestValidationTddPublication:
    def test_repository_validation_contract_defines_the_evidence_sequence(self):
        text = _read(REPO_SKILLS / "repo-worker-base" / "references" / "repository-validation-contract.md")
        for phrase in ("focused slice", "hooked", "Draft", "Ready", "state-bound"):
            assert phrase in text

    def test_repository_validation_contract_keeps_one_cheap_commit_loop(self):
        text = " ".join(
            _read(REPO_SKILLS / "repo-worker-base" / "references" / "repository-validation-contract.md").lower().split()
        )
        for phrase in (
            "fix every reported failure",
            "normal hooked commit",
            "hosted confirmation",
            "do not add duplicate broad gates",
        ):
            assert phrase in text

    def test_debugging_rejects_unauthorized_semantic_expansion(self):
        text = " ".join(_read(SKILLS / "systematic-debugging" / "SKILL.md").lower().split())
        for phrase in (
            "new mode",
            "environment-sensitive branch",
            "identify its authority",
            "authorizes diagnosis and repair",
            "do not substitute a familiar adjacent failure",
        ):
            assert phrase in text

    def test_staged_snapshot_marker_does_not_change_consumer_semantics(self):
        text = " ".join(_read(OPERATING_SKILLS / "tracked-repo-hooks" / "SKILL.md").lower().split())
        for phrase in (
            "identifies the candidate tree",
            "does not alter consumer command semantics",
            "marketplace-source rolling",
            "explicitly declares otherwise",
        ):
            assert phrase in text

    def test_verification_is_state_bound_not_message_bound(self):
        text = _read(SKILLS / "verification-before-completion" / "SKILL.md").lower()
        assert "tested state" in text
        assert "this message" not in text

    def test_branch_finish_reuses_valid_evidence_and_defaults_to_draft(self):
        text = _read(SKILLS / "finishing-a-development-branch" / "SKILL.md").lower()
        assert "reuse" in text and "evidence" in text
        assert "draft" in text

    def test_branch_finish_owns_verified_post_merge_retirement(self):
        skill_root = SKILLS / "finishing-a-development-branch"
        raw = _read(skill_root / "SKILL.md")
        text = raw.lower()
        for phrase in (
            "merged externally",
            "recorded head sha",
            "expected base",
            "recorded merge result",
            "git branch -d",
        ):
            assert phrase in text
        assert "git branch -D" in raw
        helper = ".agents/skills/finishing-a-development-branch/scripts/remove_worktree.py"
        assert f"py -3 {helper} --check" in raw
        assert f"py -3 {helper} --apply" in raw
        assert text.index("after the worktree is gone") < text.index("verify the local branch ref no longer exists")

        frontmatter = yaml.safe_load(raw.split("---", 2)[1])
        assert "pr merged externally" in frontmatter["description"].lower()

        interface = yaml.safe_load(_read(skill_root / "agents" / "openai.yaml"))["interface"]
        assert "merged pr" in interface["short_description"].lower()
        assert "pr merged externally" in interface["default_prompt"].lower()

    def test_worktree_skill_routes_retirement_to_branch_finishing(self):
        text = _read(SKILLS / "using-git-worktrees" / "SKILL.md").lower()
        assert "finishing-a-development-branch" in text
        assert "remove_worktree.py" not in text

        old_scripts = SKILLS / "using-git-worktrees" / "scripts"
        owner_scripts = SKILLS / "finishing-a-development-branch" / "scripts"
        for filename in ("remove_worktree.py", "remove-worktree.ps1", "remove-worktree.sh"):
            assert not (old_scripts / filename).exists()
            assert (owner_scripts / filename).is_file()

    def test_planning_artifact_lifecycle_has_one_portable_owner(self):
        owner = REPO_SKILLS / "completing-planning-artifacts" / "SKILL.md"
        assert owner.is_file()
        text = _read(owner).lower()
        for phrase in (
            "committed, in-flight",
            "completed-awaiting-retirement",
            "squash",
            "next substantive slice",
            "first commit",
            "cleanup-only pr",
            "cleanup-custody",
            "<scratch-root>/<repo-name>/completed/<artifact-type>/",
            "repositories segregated",
            "canonical repository identity",
            "fully checked",
            "human-owned ready or merge actions",
            "explicitly declared incomplete",
        ):
            assert phrase in text

        planning = _read(SKILLS / "writing-plans" / "SKILL.md").lower()
        assert "plans are durable" not in planning
        assert "completing-planning-artifacts" in planning
        assert "human-owned post-handoff actions" in planning
        assert "unchecked plan items" in planning

        for publication_path in (
            OPERATING_SKILLS / "repo-shape" / "templates" / "pr.md",
            ROOT / ".agents" / "runbooks" / "pr.md",
        ):
            publication = _read(publication_path).lower()
            assert "commercial and ci posture" in publication
            assert "fully reviewable draft" in publication
            assert "explicitly declared incomplete" in publication
            assert "must not remain unchecked" in publication

        ingress = _read(REPO_SKILLS / "repo-worker-base" / "SKILL.md").lower()
        assert "completing-planning-artifacts" in ingress

        manifest_path = (
            ROOT / "codex-marketplace" / "plugins" / "repo-worker-pack" / "references" / "bundle-manifest.json"
        )
        manifest = json.loads(_read(manifest_path))
        declared = {entry["canonical_name"] for entry in manifest["entries"]}
        canonical = {path.name for path in REPO_SKILLS.iterdir() if (path / "SKILL.md").is_file()}
        assert declared == canonical

        completed_artifacts = _read(OPERATING_SKILLS / "repo-shape" / "templates" / "completed-artifacts.md").lower()
        assert "completion playbook" not in completed_artifacts
        assert "portable" in completed_artifacts
        assert "completion skill owns the lifecycle" in completed_artifacts

        runbook_standard = _read(
            OPERATING_SKILLS / "repo-shape" / "references" / "repository-runbook-standard.md"
        ).lower()
        shape_standard = _read(OPERATING_SKILLS / "repo-shape" / "references" / "repository-shape-standard.md").lower()
        for standard in (runbook_standard, shape_standard):
            assert "completing-planning-artifacts" not in standard
            assert "completed-awaiting-retirement" not in standard
            assert "next substantive slice" not in standard
            assert "two-slice lifecycle" not in standard
        assert "mandatory cross-repository capabilities belong in portable skills" in runbook_standard
        assert "routes to its current lifecycle owners" in shape_standard

    def test_tdd_allows_transitive_coverage_for_glue(self):
        text = _read(SKILLS / "test-driven-development" / "SKILL.md").lower()
        assert "transitive" in text or "independent behavior" in text

    def test_tdd_requires_the_consumer_complete_gate_before_completion(self):
        text = _read(SKILLS / "test-driven-development" / "SKILL.md").lower()
        assert "complete gate" in text
        assert "focused" in text
        assert "every failure" in text

    def test_bundled_scripts_are_invoked_through_their_interpreters(self):
        tracing = _read(SKILLS / "systematic-debugging" / "root-cause-tracing.md")
        authoring = _read(SKILLS / "writing-skills" / "SKILL.md")
        assert "bash ./find-polluter.sh" in tracing
        assert "node ./render-graphs.js" in authoring
        assert "Invoke bundled scripts through their interpreter" in authoring

    def test_subagent_workspace_uses_one_python_execution_engine(self):
        scripts = SKILLS / "subagent-workspace" / "scripts"
        assert {path.name for path in scripts.iterdir() if path.is_file()} == {
            "review_package.py",
            "task_brief.py",
            "workspace.py",
        }
        skill = _read(SKILLS / "subagent-workspace" / "SKILL.md")
        assert "default to read-only `--check`" in skill
        assert "--apply" in skill
        assert ".ps1" not in skill


class TestPlanningDelegationReview:
    def test_native_and_sdd_explain_their_distinct_review_costs(self):
        native = _read(SKILLS / "executing-plans" / "SKILL.md").lower()
        sdd = _read(SKILLS / "subagent-driven-development" / "SKILL.md").lower()
        assert "native inline execution" in native
        assert "one fresh whole-branch review" in native
        assert "fresh implementer" in sdd and "reviewer per task" in sdd
        assert "stay in this session?" not in sdd

    def test_native_execution_uses_shared_ledger_and_completion_owners(self):
        native = _read(SKILLS / "executing-plans" / "SKILL.md").lower()
        for phrase in (
            "workspace.py",
            "task_brief.py",
            "review focus",
            "ruling:",
            "handoff-gates",
            "completing-planning-artifacts",
            "finishing-a-development-branch",
        ):
            assert phrase in native
        assert "same host environment" in native
        assert "must not cross implicitly into wsl" in native
        assert "human-owned" in native

    def test_brainstorming_establishes_shared_intent_before_path_design(self):
        text = _read(SKILLS / "brainstorming" / "SKILL.md").lower()
        assert "establish shared understanding" in text
        assert "intended outcome" in text
        assert "who it is for" in text
        assert "what success looks like" in text
        assert "already supplies" in text
        assert "do not ask" in text

    def test_plans_pin_review_focus_to_owning_task_tests(self):
        text = _read(SKILLS / "writing-plans" / "SKILL.md").lower()
        assert "## review focus" in text
        assert "five" in text
        assert "failure modes" in text
        assert "owning task" in text
        assert "saved plan" in text

    def test_saved_plan_review_preserves_preselected_execution_method(self):
        plans = _read(SKILLS / "writing-plans" / "SKILL.md").lower()
        override = _read(SKILLS.parent / "references" / "execution-lane-override.md").lower()
        roadmaps = _read(SKILLS / "writing-roadmaps" / "SKILL.md").lower()
        assert "already explicitly supplied an execution method" in plans
        assert "preserve" in plans and "review the saved plan" in plans
        assert "native" in plans and "subagent-driven" in plans
        assert "execution cost" in override
        assert "review the saved plan" in roadmaps

    def test_review_uses_branch_base_and_reasonable_user_expectations(self):
        requesting = _read(SKILLS / "requesting-code-review" / "SKILL.md")
        reviewers = [
            _read(SKILLS / "requesting-code-review" / name).lower()
            for name in ("code-reviewer.md", "reviewer-prompt.md")
        ]
        assert "git merge-base origin/main HEAD" in requesting
        for reviewer in reviewers:
            assert "reasonable person" in reviewer
            assert "spec's silence is not permission" in reviewer
            assert "declined to judge" in reviewer
            assert "executor rules on each line" in reviewer

    def test_brainstorming_owns_spec_to_plan_handoff_review(self):
        brainstorming = _read(SKILLS / "brainstorming" / "SKILL.md").lower()
        brainstorming_flat = " ".join(brainstorming.split())
        handoff = _read(SKILLS / "handoff-gates" / "SKILL.md").lower()
        handoff_scope = _read(SKILLS / "handoff-gates" / "references" / "scope-notes.md").lower()
        handoff_wrapper = _read(SKILLS / "handoff-gates" / "agents" / "openai.yaml").lower()
        roadmaps = _read(SKILLS / "writing-roadmaps" / "SKILL.md").lower()
        design_runbook = _read(ROOT / ".agents" / "runbooks" / "design.md").lower()

        for phrase in (
            "planning-handoff review",
            "burden ledger",
            "exactly one branch",
            "total weighted burden is lower",
            "restore the preserved initial draft",
            "private review",
        ):
            assert phrase in brainstorming_flat

        assert "spec-readiness" not in handoff
        assert "spec-readiness" not in handoff_scope
        assert "spec" not in handoff_wrapper.split("short_description:", 1)[1].splitlines()[0]
        assert "spec-readiness" not in roadmaps
        assert "handoff-gates" not in design_runbook

    def test_design_scales_to_uncertainty_without_universal_approval(self):
        text = _read(SKILLS / "brainstorming" / "SKILL.md")
        assert "Three Paths" in text
        assert "ceremony scales" in text
        assert "approval gate never does" not in text

    def test_plans_are_recipient_relative(self):
        text = _read(SKILLS / "writing-plans" / "SKILL.md").lower()
        assert "recipient-relative" in text
        assert "exact implementation code" in text

    def test_review_can_make_evidence_backed_technical_rulings(self):
        text = _read(SKILLS / "subagent-driven-development" / "SKILL.md")
        assert "Ruling:" in text
        assert "before" in text[text.index("Ruling:") :].lower()

    def test_delegation_and_model_selection_remain_separate(self):
        text = _read(SKILLS / "selecting-a-subagent" / "SKILL.md").lower()
        assert "delegate" in text
        assert "model" in text
        assert "least" in text

    def test_no_nested_reviewer_dispatch(self):
        for name in (
            "code-reviewer.md",
            "implementer-prompt.md",
            "re-review-prompt.md",
            "task-reviewer-prompt.md",
        ):
            owner = "requesting-code-review" if name == "code-reviewer.md" else "subagent-driven-development"
            path = SKILLS / owner / name
            assert "do not dispatch subagents" in _read(path).lower()

    def test_bounded_and_spike_paths_do_not_require_ceremonial_approval(self):
        text = _read(SKILLS / "brainstorming" / "SKILL.md")
        lowered = text.lower()
        assert '"human approves?"' not in lowered
        assert "get a nod" not in lowered
        assert "bounded: after approval" not in lowered
        assert (
            "each task gets its own classification; a human decision is required only when that task "
            "contains a human-owned choice"
        ) in lowered

    def test_portable_surfaces_do_not_hardcode_marketplace_commands(self):
        for name in ("handoff-gates", "publishing-source"):
            text = _read(SKILLS / name / "SKILL.md")
            assert "tools/run" not in text
            assert "py -3" not in text

    def test_portable_superpowers_surfaces_do_not_encode_repo_command_bus(self):
        paths = [
            SKILLS / "using-git-worktrees" / "SKILL.md",
            SKILLS / "selecting-a-subagent" / "assets" / "reviewer-strong.md",
            *sorted((SKILLS / "iterative-review" / "references").glob("*.md")),
            *sorted(REPO_SKILLS.rglob("*.md")),
            *sorted(REPO_SKILLS.rglob("*.json")),
            *sorted(REPO_SKILLS.rglob("*.py")),
            *sorted(OPERATING_SKILLS.rglob("*.md")),
            *sorted(OPERATING_SKILLS.rglob("*.json")),
            *sorted(OPERATING_SKILLS.rglob("*.py")),
            OPERATING_SKILLS / "repo-shape" / "templates" / "pre-commit",
        ]
        for path in paths:
            text = _read(path).lower()
            assert "tools/run.py" not in text
            assert "tools/run ci" not in text
            assert "py -3 tools/run" not in text

    def test_sdd_implementer_defers_broad_proof_to_hooked_consumer_gate(self):
        text = _read(SKILLS / "subagent-driven-development" / "implementer-prompt.md").lower()
        assert "focused test" in text
        assert "full suite once before committing" not in text
        assert "consumer's canonical hooked gate" in text

    def test_executing_plans_rules_technical_concerns_before_human_escalation(self):
        text = _read(SKILLS / "executing-plans" / "SKILL.md").lower()
        assert "if concerns: raise them with your human partner before starting" not in text
        assert "falsifiable technical" in text
        assert "human-owned" in text
        assert "if a single missing fact blocks the next step" not in text
        assert "stop when blocked, don't guess" not in text

    def test_implementing_runbook_routes_linear_and_bounds_fix_while_here(self):
        text = _read(ROOT / ".agents" / "runbooks" / "implementing.md").lower()
        assert "linear issues must be updated" not in text
        assert "create a linear issue" not in text
        assert "under 10 minutes" not in text
        assert "## pr, linear, and plan honesty" not in text
        assert "fix-while-here is bounded" not in text


class TestRepositoryCallersAndPressure:
    def test_skill_tests_ship_with_skills_but_test_results_do_not(self):
        policy = " ".join(_read(ROOT / ".agents" / "doctrine" / "skill-standards-policy.md").lower().split())
        contract = " ".join(_read(ROOT / ".agents" / "contracts" / "skill-tests.md").lower().split())
        skills_doctrine = " ".join(_read(ROOT / ".agents" / "doctrine" / "skills.md").lower().split())
        pressure = _read(ROOT / "tests" / "pressure" / "README.md").lower()

        assert ".agents/contracts/skill-tests.md" in policy
        assert "skills are code" in contract
        assert "code ships with its tests" in contract
        assert "skills do not ship test results" in contract
        assert "tests/" in contract and "maintainer" in contract
        assert "ordinary skill invocation" in contract
        for responsibility in (
            "complete lightweight fixture trees",
            "materialization helpers",
            "assets/",
            "references/",
            "scripts/",
            "transcripts",
            "scores",
            "verdicts",
            "generated repositories",
        ):
            assert responsibility in contract

        for local_skill_policy in (policy, skills_doctrine):
            assert "repo.local_skills" in local_skill_policy
            assert "prefixes are optional" in local_skill_policy
            assert ".agents/skills/mark-*" not in local_skill_policy

        assert "skill-root `tests/`" in pressure
        assert "assets/pressure-tests.md" not in pressure

    def test_skill_test_material_uses_the_tests_directory(self):
        skill_roots = []
        for bundle_path in sorted((ROOT / "codex-marketplace" / "plugins").glob("*/references/bundle-manifest.json")):
            bundle = json.loads(_read(bundle_path))
            for entry in bundle["entries"]:
                skill_roots.append(ROOT / entry["canonical_source_path"])

        misplaced = []
        for skill_root in skill_roots:
            candidates = [
                skill_root / "assets" / "pressure-tests.md",
                skill_root / "CREATION-LOG.md",
                *skill_root.glob("test-*.md"),
            ]
            misplaced.extend(path.relative_to(ROOT).as_posix() for path in candidates if path.is_file())

        assert misplaced == []
        expected = (
            "codex-marketplace/plugins/mcp-usage-pack/skills/using-playwright-mcp/tests/pressure-tests.md",
            "codex-marketplace/plugins/superpowers-plus/skills/systematic-debugging/tests/scenarios/academic.md",
            "codex-marketplace/plugins/superpowers-plus/skills/systematic-debugging/tests/scenarios/pressure-1.md",
            "codex-marketplace/plugins/superpowers-plus/skills/systematic-debugging/tests/scenarios/pressure-2.md",
            "codex-marketplace/plugins/superpowers-plus/skills/systematic-debugging/tests/scenarios/pressure-3.md",
            "codex-marketplace/plugins/superpowers-plus/skills/systematic-debugging/tests/evidence/creation-log.md",
        )
        assert all((ROOT / path).is_file() for path in expected)

    def test_skill_language_contract_assigns_one_role_per_field(self):
        frontmatter = _read(ROOT / ".agents" / "contracts" / "skill-frontmatter.md")
        wrapper = _read(ROOT / ".agents" / "contracts" / "openai-agent-yaml.md")
        policy = _read(ROOT / ".agents" / "doctrine" / "skill-standards-policy.md")
        for field in ("description", "metadata.scope", "metadata.use_when[]", "metadata.do_not_use_when[]"):
            assert f"`{field}`" in frontmatter
        for field in ("short_description", "default_prompt"):
            assert f"`{field}`" in wrapper
        assert "do not impose description-style `Use when` phrasing" in policy

    def test_review_preflight_accepts_relationship_metadata_fields(self):
        source = _read(ROOT / "tools" / "review_preflight.py")
        for field in ("use_before", "use_after", "use_with", "use_instead"):
            assert f'"{field}"' in source

    def test_review_preflight_reports_workflow_like_description_for_adjudication(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ):
        path = tmp_path / "SKILL.md"
        content = "---\nname: sample\ndescription: Use when a task is blocked. Then run the fixer.\n---\n"
        findings = []
        monkeypatch.setattr(review_preflight, "ROOT", tmp_path)
        review_preflight._scan_skill_language(path, content, findings)
        assert findings and "workflow-like clause" in findings[0]

    def test_repo_contracts_have_one_home(self):
        contracts = ROOT / ".agents" / "contracts"
        assert (contracts / "openai-agent-yaml.md").is_file()
        assert (contracts / "skill-frontmatter.md").is_file()
        assert (contracts / "repo-standards-commands.json").is_file()
        assert not (ROOT / ".agents" / "docs" / "contracts").exists()
        assert not (ROOT / ".agents" / "doctrine" / "repo-standards-commands.json").exists()

    def test_repo_unslop_profile_has_contract_custody(self):
        assert (ROOT / ".agents" / "contracts" / "unslop" / "repository.md").is_file()
        assert not (ROOT / ".agents" / "docs" / "unslop").exists()
        standard = _read(OPERATING_SKILLS / "repo-shape" / "references" / "repository-shape-standard.md")
        assert ".agents/contracts/unslop/" in standard
        assert "<scope>/.agents/contracts/unslop/" in standard

    def test_superpowers_provenance_does_not_claim_a_retained_snapshot(self):
        source = _read(ROOT / "codex-marketplace" / "plugins" / "superpowers-plus" / "SOURCE.md")
        assert "5bf4e78011075bcfc0dc295f0724994cd123ee71" in source
        assert "Retained snapshot" not in source
        offenders = []
        plugin = ROOT / "codex-marketplace" / "plugins" / "superpowers-plus"
        for path in plugin.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in {".md", ".json", ".yaml", ".yml"}:
                continue
            text = _read(path).lower()
            stale_claims = (
                "upstream snapshot is retained",
                "snapshot retained in",
                "retained upstream snapshot",
                "snapshot is recorded in `source.md`",
            )
            if any(claim in text for claim in stale_claims):
                offenders.append(path.relative_to(plugin).as_posix())
        assert offenders == []

    def test_completed_artifact_guidance_does_not_require_archival(self):
        owners = (
            ROOT / ".agents" / "doctrine" / "plans.md",
            ROOT / ".agents" / "runbooks" / "AGENTS.md",
            ROOT / ".agents" / "runbooks" / "code-review.md",
            ROOT
            / "codex-marketplace"
            / "plugins"
            / "repo-worker-pack"
            / "skills"
            / "linear-issue-shaping"
            / "SKILL.md",
            ROOT / "codex-marketplace" / "plugins" / "superpowers-plus" / "skills" / "writing-plans" / "SKILL.md",
            ROOT
            / "codex-marketplace"
            / "plugins"
            / "superpowers-plus"
            / "skills"
            / "iterative-review"
            / "references"
            / "review-state-graph.md",
        )
        stale_phrases = ("archive-and-removal", "off-repo archive", "plan archival", "archiving a plan")
        offenders = [
            path.relative_to(ROOT).as_posix()
            for path in owners
            if any(phrase in _read(path).lower() for phrase in stale_phrases)
        ]
        assert offenders == []

    def test_portable_clarification_trigger_is_consumer_neutral(self):
        skill = _read(SKILLS / "asking-clarifying-questions" / "SKILL.md")
        description = " ".join(skill.split("---", 2)[1].lower().split())
        assert "one human answer" in description
        assert "taste" not in description
        assert "premium" not in description
        assert "before source inspection" not in description

    def test_runbooks_keep_generic_method_in_skills(self):
        design = _read(ROOT / ".agents" / "runbooks" / "design.md")
        review = _read(ROOT / ".agents" / "runbooks" / "code-review.md")
        implementing = _read(ROOT / ".agents" / "runbooks" / "implementing.md")
        security = _read(ROOT / ".agents" / "playbooks" / "security.md")
        skill_authoring = _read(ROOT / ".agents" / "playbooks" / "skill-authoring.md")
        assert "## Spec Self-Review" not in design
        assert "Apply three core lenses to every review" not in review
        assert "## Repo Improvement Check" not in review
        assert "## PR, Linear, and Plan Honesty" not in implementing
        assert "No secrets committed" not in implementing
        assert "## When to use" not in security
        assert "## Publication handoff" not in skill_authoring

    def test_local_runbooks_delegate_skill_composition_to_bootstrap(self):
        surfaces = [
            ROOT / "AGENTS.md",
            ROOT / "CONTRIBUTING.md",
            ROOT / "REVIEW.md",
            *sorted((ROOT / ".agents" / "doctrine").glob("*.md")),
            *sorted((ROOT / ".agents" / "runbooks").glob("*.md")),
            *sorted((ROOT / ".agents" / "playbooks").glob("*.md")),
        ]
        skill_names = "|".join(map(re.escape, sorted(_canonical_skill_names(), key=len, reverse=True)))
        imperative_skill = re.compile(
            rf"(?:\b(?:invoke|route to|handoff to)\s+`?"
            rf"|\buse\s+(?:the\s+)?(?:first-party\s+)?(?:\[`?)?"
            rf"|\bapply\b[^\n]{{0,60}}?\bfrom\s+`?)"
            rf"({skill_names})\b",
            re.IGNORECASE,
        )
        for path in surfaces:
            text = _read(path).lower()
            assert "skills to invoke" not in text
            assert "routing to skills" not in text
            targets = imperative_skill.findall(text)
            assert set(targets) <= {"using-superpowers-plus"}, (path, targets)

    def test_active_prose_uses_skill_identifiers_not_slash_invocations(self):
        skill_names = sorted(_canonical_skill_names(), key=len, reverse=True)
        slash_skill = re.compile(
            r"(?<![A-Za-z0-9._~*\-])/(?:" + "|".join(map(re.escape, skill_names)) + r")(?![a-z0-9-])"
        )
        offenders = []
        for path in _active_instruction_surfaces():
            for line_number, line in enumerate(_read(path).splitlines(), start=1):
                if slash_skill.search(line):
                    offenders.append(f"{path.relative_to(ROOT).as_posix()}:{line_number}")
        assert offenders == []

    def test_vendored_skill_prose_uses_plain_identifiers_not_client_sigils(self):
        skill_names = sorted(_canonical_skill_names(), key=len, reverse=True)
        sigilled_skill = re.compile(
            r"(?<![A-Za-z0-9._~*\-])[/\$](?:" + "|".join(map(re.escape, skill_names)) + r")(?![a-z0-9-])"
        )
        offenders = []
        for path in (ROOT / "codex-marketplace" / "plugins").rglob("*"):
            if path.is_file() and (path.name == "SKILL.md" or path.as_posix().endswith("/agents/openai.yaml")):
                for line_number, line in enumerate(_read(path).splitlines(), start=1):
                    if sigilled_skill.search(line):
                        offenders.append(f"{path.relative_to(ROOT).as_posix()}:{line_number}")
        assert offenders == []

    def test_superpowers_plus_uses_its_own_namespace(self):
        offenders = []
        for path in (ROOT / "codex-marketplace" / "plugins" / "superpowers-plus").rglob("*"):
            if not path.is_file() or path.suffix.lower() not in {".md", ".json", ".yaml", ".yml"}:
                continue
            if re.search(r"\bsuperpowers:[a-z][a-z0-9-]+", _read(path)):
                offenders.append(path.relative_to(ROOT).as_posix())
        assert offenders == []

    def test_vendored_skill_metadata_uses_field_relative_language(self):
        offenders = []
        for skill_md in (ROOT / "codex-marketplace" / "plugins").rglob("SKILL.md"):
            if "templates" in skill_md.parts:
                continue
            skill_validation.validate_skill_markdown_frontmatter(skill_md.parent)
            text = _read(skill_md)
            _, frontmatter, _ = text.split("---", 2)
            data = yaml.safe_load(frontmatter)
            metadata = data.get("metadata") or {}
            description = data.get("description", "")
            if not description.startswith("Use when "):
                offenders.append(f"{skill_md.relative_to(ROOT)}: description")
            scope = metadata.get("scope")
            if isinstance(scope, str) and scope.lower().startswith("use when"):
                offenders.append(f"{skill_md.relative_to(ROOT)}: scope")
            for field, prefix in (("use_when", "use "), ("do_not_use_when", "do not use")):
                for value in metadata.get(field, []):
                    if value.lower().startswith(prefix):
                        offenders.append(f"{skill_md.relative_to(ROOT)}: {field}")
        assert offenders == []

    def test_openai_wrappers_use_capability_copy_and_direct_prompts(self):
        offenders = []
        skill_names = "|".join(map(re.escape, sorted(_canonical_skill_names(), key=len, reverse=True)))
        client_sigil = re.compile(rf"(?<![A-Za-z0-9._~*\-])[/$](?:{skill_names})(?![a-z0-9-])")
        for path in (ROOT / "codex-marketplace" / "plugins").rglob("agents/openai.yaml"):
            data = yaml.safe_load(_read(path))
            interface = data.get("interface") or {}
            skill_name = (data.get("metadata") or {}).get("skill_name")
            short = interface.get("short_description", "")
            prompt = interface.get("default_prompt", "")
            if short.lower().startswith("use when"):
                offenders.append(f"{path.relative_to(ROOT)}: short_description")
            if re.search(r"\bto use when\b|^use when\b", prompt, re.IGNORECASE):
                offenders.append(f"{path.relative_to(ROOT)}: default_prompt grammar")
            if client_sigil.search(prompt):
                offenders.append(f"{path.relative_to(ROOT)}: client sigil")
            if skill_name and not re.search(rf"\b{re.escape(skill_name)}\b", prompt):
                offenders.append(f"{path.relative_to(ROOT)}: missing skill identity")
        assert offenders == []

    def test_repo_standards_routes_to_focused_operating_model_skills(self):
        router = _read(OPERATING_SKILLS / "repo-standards" / "SKILL.md").lower()
        for skill in (
            "repo-shape",
            "repo-composition",
            "command-bus",
            "repository-validation",
            "tracked-repo-hooks",
            "repo-agent-assets",
            "python",
        ):
            assert skill in router
        assert "repo-worker-base" in router
        assert "worktrees" in router
        assert "publication" in router

    def test_operating_model_consumer_surface_contract_is_durable(self):
        audit_path = OPERATING_SKILLS / "repo-shape" / "references" / "consumer-surface-audit.md"
        schema = OPERATING_SKILLS / "repo-shape" / "references" / "repository-shape-manifest.schema.json"
        coordinator = _read(OPERATING_SKILLS / "repo-shape" / "scripts" / "repo_standards.py")
        audit = _read(audit_path)
        assert "Mandatory invariants" in audit
        assert "consumer-authored" in audit
        assert schema.is_file()
        assert 'surface.get("check_content", True)' not in coordinator

    def test_workflow_inventory_covers_every_tracked_workflow(self):
        inventory = _read(DOCS / "workflow-inventory.md")
        workflows = list((ROOT / ".github" / "workflows").glob("*.y*ml"))
        for workflow in workflows:
            assert workflow.as_posix().replace(ROOT.as_posix() + "/", "") in inventory.replace("\\", "/")

    def test_ci_parity_and_draft_anti_bypass_are_explicit(self):
        text = _read(DOCS / "ci-parity.md").lower()
        assert "canonical ci registry" in text
        assert "draft" in text
        assert "feature branch" in text

    def test_scanner_defects_are_classified(self):
        roots = [SKILLS, REPO_SKILLS, OPERATING_SKILLS, ROOT / ".agents" / "runbooks", ROOT / ".agents" / "playbooks"]
        files = [path for root in roots for path in root.rglob("*")]
        findings = pressure_scan.scan_paths(files, ROOT)
        classified = json.loads(_read(DOCS / "pressure-scan-decisions.json"))
        assert isinstance(findings, list)
        assert all({"path", "line", "pattern", "context"} <= set(item) for item in findings)
        assert all(item["classification"] in {"intended", "repo-local"} for item in classified)
        assert all(item["classification"] != "defect" for item in classified)

    def test_pressure_scan_has_one_owned_disposition_per_candidate(self):
        roots = [SKILLS, REPO_SKILLS, OPERATING_SKILLS, ROOT / ".agents" / "runbooks", ROOT / ".agents" / "playbooks"]
        files = [path for root in roots for path in root.rglob("*")]
        findings = pressure_scan.scan_paths(files, ROOT)
        dispositions = json.loads(_read(DOCS / "pressure-scan-decisions.json"))
        assert len(dispositions) == len(findings)
        assert all(
            {"path", "line", "pattern", "classification", "owner", "reason"} <= set(item) for item in dispositions
        )
        assert all(item["classification"] in {"intended", "repo-local"} for item in dispositions)
        assert all(item["owner"] and item["reason"] for item in dispositions)
        assert {(item["path"], item["line"], item["pattern"]) for item in dispositions} == {
            (item["path"], item["line"], item["pattern"]) for item in findings
        }
        assert all(item["classification"] != "defect" for item in dispositions)


class TestEvaluationCampaign:
    def test_campaign_schema_and_fixed_matrix(self):
        campaign = json.loads(_read(DOCS / "campaign.json"))
        campaign_runner.validate_campaign(campaign)
        assert len(campaign["scenarios"]) == 16
        assert all(s["external_effect"] == "none" for s in campaign["scenarios"])

    def test_pressure_prompts_do_not_leak_rubric_decisions(self):
        leaked_imperatives = (
            "do not ask again",
            "reuse unchanged evidence",
            "do not dispatch another reviewer",
            "without a universal design-approval pause",
            "do not run an unrelated full matrix",
            "ceremonial direct test",
            "follow repository canon",
            "least adequate bounded worker",
            "stop before deletion",
            "ask exactly the one human-owned question",
            "run focused verification before reporting",
            "without asking for a ceremonial design approval",
        )
        for scenario in json.loads(_read(DOCS / "campaign.json"))["scenarios"]:
            prompt = _read(DOCS / "prompts" / scenario["prompt"]).lower()
            assert not any(fragment in prompt for fragment in leaked_imperatives), scenario["id"]

    def test_raw_runs_are_ignored_and_historical_result_artifacts_are_absent(self):
        result = __import__("subprocess").run(
            ["git", "check-ignore", "tests/pressure/workflow-contracts/runs/probe/events.jsonl"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        discarded = (
            "campaign-meta.json",
            "scores",
            "results.md",
            "red-baseline.md",
            "pressure-scan.json",
            "pressure-scan.md",
        )
        for name in discarded:
            assert not (DOCS / name).exists()

    def test_pressure_fixtures_do_not_retain_run_results(self):
        pressure_root = ROOT / "tests" / "pressure"
        contract_path = ROOT / ".agents" / "contracts" / "pressure-artifacts.json"
        contract = json.loads(_read(contract_path))

        required_transient_artifacts = {
            "model_outputs",
            "grader_outputs",
            "scores",
            "verdicts",
            "transcripts",
            "runtime_identities",
            "run_metadata",
        }
        required_transient_fields = {
            "runtime_results",
            "runtime_execution",
            "raw_response",
            "raw_response_excerpt",
            "source_rollout",
            "score",
            "scores",
            "verdict",
            "judgment",
            "transcript",
        }
        assert required_transient_artifacts <= set(contract["transient_artifacts"])
        assert required_transient_fields <= set(contract["transient_result_fields"])
        assert contract["transient_run_location"] == "tests/pressure/<campaign>/runs/"

        tracked = (
            __import__("subprocess")
            .run(
                ["git", "ls-files", "tests/pressure"],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=True,
            )
            .stdout.splitlines()
        )
        forbidden_names = set(contract["forbidden_tracked_basenames"])
        retained = [path for path in tracked if Path(path).name in forbidden_names or "/runs/" in path]
        assert retained == []

        transient_fields = required_transient_fields

        def find_transient_fields(value):
            if isinstance(value, dict):
                return (set(value) & transient_fields) | set().union(
                    *(find_transient_fields(child) for child in value.values()), set()
                )
            if isinstance(value, list):
                return set().union(*(find_transient_fields(child) for child in value), set())
            return set()

        for fixture in pressure_root.rglob("*.json"):
            assert find_transient_fields(json.loads(_read(fixture))) == set(), fixture

        forbidden_stem_tokens = {"result", "results", "score", "scores", "verdict", "transcript", "response"}
        for path in tracked:
            tokens = set(__import__("re").split(r"[-_.]", Path(path).stem.lower()))
            assert not (tokens & forbidden_stem_tokens), path

    def test_every_pressure_run_directory_is_ignored(self):
        probes = (
            "tests/pressure/workflow-contracts/runs/probe.json",
            "tests/pressure/writing/blinded/runs/probe.json",
            "tests/pressure/asking-clarifying-questions/runs/probe.json",
        )
        result = __import__("subprocess").run(
            ["git", "check-ignore", *probes],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert set(result.stdout.splitlines()) == set(probes)

    def test_trial_argv_has_exact_controls_and_least_privilege(self, tmp_path: Path):
        argv = campaign_runner.build_codex_argv(tmp_path, "gpt-5.6-luna", "read-only", tmp_path / "final.txt")
        assert argv[:2] == ["codex", "exec"]
        assert "--ephemeral" in argv and "--json" in argv and "--ignore-user-config" in argv
        assert "--model" in argv and "gpt-5.6-luna" in argv
        assert "--sandbox" in argv and "read-only" in argv
        assert "features.apps=false" in argv and 'web_search="disabled"' in argv
        with pytest.raises(ValueError):
            campaign_runner.build_codex_argv(tmp_path, "gpt-5.6-luna", "danger-full-access", tmp_path / "final.txt")

    def test_preflight_distinguishes_missing_harness_and_missing_capability(self):
        missing = campaign_runner.preflight(resolve=lambda _: None)
        assert missing["status"] == "harness-unavailable"

        class Result:
            returncode = 0
            stdout = "Codex 1.0"
            stderr = ""

        def fake_run(argv, **kwargs):
            return Result()

        incompatible = campaign_runner.preflight(resolve=lambda _: "codex", run=fake_run)
        assert incompatible["status"] == "harness-incompatible"

    def test_preflight_runs_read_only_smoke_and_checks_project_config(self, tmp_path: Path):
        calls = []

        class Result:
            returncode = 0
            stdout = "Codex 1.0"
            stderr = ""

        def fake_run(argv, **kwargs):
            calls.append((argv, kwargs))
            result = Result()
            if argv[-1] == "--help":
                result.stdout = (
                    "exec --ephemeral --json --model --sandbox --output-last-message --ignore-user-config -c"
                )
            if argv[:3] == ["codex", "mcp", "list"] or argv[:3] == ["codex", "plugin", "list"]:
                if argv[-1] == "--help":
                    result.stdout = "list --json"
                else:
                    result.stdout = "[]"
            if "--output-last-message" in argv:
                final_path = Path(argv[argv.index("--output-last-message") + 1])
                final_path.write_text("SMOKE_OK\n", encoding="utf-8")
            return result

        ready = campaign_runner.preflight(resolve=lambda _: "codex", run=fake_run, worktree=tmp_path)
        assert ready["status"] == "preflight-ready"
        assert len(calls) == 7
        assert "--sandbox" in calls[-1][0] and "read-only" in calls[-1][0]
        assert calls[-1][1]["input"].startswith("MARK-373 harness smoke")
        assert "read-only command" in calls[-1][1]["input"]

        config = tmp_path / ".codex" / "config.toml"
        config.parent.mkdir()
        config.write_text("mcp_servers = { github = { command = 'connector' } }\n", encoding="utf-8")
        blocked = campaign_runner.preflight(resolve=lambda _: "codex", run=fake_run, worktree=tmp_path)
        assert blocked["status"] == "harness-blocked"
        assert "external" in blocked["reason"]

        config.unlink()
        calls.clear()
        plugin_payload = '[{"name":"external-plugin"}]'

        def fake_plugin_run(argv, **kwargs):
            result = fake_run(argv, **kwargs)
            if argv[:3] == ["codex", "plugin", "list"] and argv[-1] == "--json":
                result.stdout = plugin_payload
            return result

        plugin_blocked = campaign_runner.preflight(resolve=lambda _: "codex", run=fake_plugin_run, worktree=tmp_path)
        assert plugin_blocked["status"] == "harness-blocked"
        assert "MCP/plugin" in plugin_blocked["reason"]
        assert not any("--output-last-message" in argv for argv, _ in calls)

    def test_campaign_preflight_is_bound_to_requested_immutable_head(self):
        head = "a" * 40
        calls = []

        class Result:
            returncode = 0
            stdout = ""
            stderr = ""

        def fake_git(argv, **kwargs):
            calls.append((argv, kwargs))
            result = Result()
            if "rev-parse" in argv:
                result.stdout = head + "\n"
            return result

        def fake_preflight(*, worktree):
            calls.append(("preflight", worktree))
            return {"status": "preflight-ready", "version": "codex-cli test"}

        result = campaign_runner.preflight_at_head(head, preflight_fn=fake_preflight, git_run=fake_git)
        assert result["status"] == "preflight-ready"
        assert result["preflight_head"] == head
        add_call = next(
            argv for argv, _ in calls if isinstance(argv, list) and argv[:4] == ["git", "worktree", "add", "--detach"]
        )
        assert add_call[-1] == head
        preflight_call = next(item for item in calls if item[0] == "preflight")
        assert str(preflight_call[1]) != str(Path.cwd())

    def test_run_campaign_passes_head_to_bound_preflight(self, tmp_path: Path, monkeypatch):
        head = "b" * 40
        requested = []

        def fake_preflight_at_head(value):
            requested.append(value)
            return {"status": "harness-blocked", "reason": "test block"}

        monkeypatch.setattr(campaign_runner, "preflight_at_head", fake_preflight_at_head)
        result = campaign_runner.run_campaign(DOCS / "campaign.json", tmp_path, head)
        assert result == 2
        assert requested == [head]
        meta = json.loads(_read(tmp_path / head / "_harness" / "campaign-meta.json"))
        assert meta["evaluation_head"] == head

    def test_unknown_scenario_fails_before_preflight(self, tmp_path: Path, monkeypatch):
        calls = []

        def fake_preflight_at_head(value):
            calls.append(value)
            return {"status": "preflight-ready", "version": "codex-cli test"}

        monkeypatch.setattr(campaign_runner, "preflight_at_head", fake_preflight_at_head)
        result = campaign_runner.run_campaign(
            DOCS / "campaign.json",
            tmp_path,
            "c" * 40,
            scenario_id="does-not-exist",
        )
        assert result == 2
        assert calls == []

    def test_trial_availability_classification_is_specific_to_requested_model(self):
        assert campaign_runner.classify_trial_availability("gpt-6-astra", 0, "", "") == "ok"
        assert (
            campaign_runner.classify_trial_availability(
                "gpt-6-astra",
                1,
                "",
                "Error: requested model gpt-6-astra is not available for this account",
            )
            == "model-unavailable"
        )
        assert (
            campaign_runner.classify_trial_availability(
                "gpt-6-astra",
                1,
                "",
                "authentication failed while starting provider",
            )
            == "trial-error"
        )

    def test_successful_trial_writes_reproducible_evidence(self, tmp_path: Path, monkeypatch):
        head = "d" * 40
        controlling_head = "e" * 40
        monkeypatch.setattr(
            campaign_runner,
            "preflight_at_head",
            lambda value: {
                "status": "preflight-ready",
                "version": "codex-cli 0.test",
                "requested_head": value,
                "preflight_head": value,
                "preflight_worktree_status": "clean",
            },
        )

        def fake_run(argv, **kwargs):
            if argv[:3] == ["git", "rev-parse", "HEAD"]:
                return subprocess.CompletedProcess(argv, 0, controlling_head + "\n", "")
            if argv[:4] == ["git", "worktree", "add", "--detach"]:
                return subprocess.CompletedProcess(argv, 0, "", "")
            if argv[:4] == ["git", "worktree", "remove", "--force"]:
                return subprocess.CompletedProcess(argv, 0, "", "")
            if argv[:2] == ["codex", "exec"]:
                final = Path(argv[argv.index("--output-last-message") + 1])
                final.write_text("Completed bounded change.\n", encoding="utf-8")
                return subprocess.CompletedProcess(argv, 0, '{"type":"tool_call","name":"read"}\n', "")
            raise AssertionError(argv)

        monkeypatch.setattr(campaign_runner.subprocess, "run", fake_run)
        result = campaign_runner.run_campaign(
            DOCS / "campaign.json",
            tmp_path,
            head,
            family="luna",
            scenario_id="trivial-docs",
        )
        assert result == 0
        run_dir = tmp_path / head / "luna" / "trivial-docs"
        meta = json.loads(_read(run_dir / "meta.json"))
        metrics = json.loads(_read(run_dir / "metrics.json"))
        hashes = json.loads(_read(run_dir / "hashes.json"))
        assert meta["codex_version"] == "codex-cli 0.test"
        assert meta["controlling_head"] == controlling_head
        assert meta["availability"] == "ok"
        assert meta["cleanup"]["status"] == "ok"
        assert "<worktree>" in meta["sanitized_argv"]
        assert "<run-dir>/final.txt" in meta["sanitized_argv"]
        assert metrics["tool_call_count"] == 1
        for name in ("events_jsonl_sha256", "stderr_sha256", "final_sha256", "meta_sha256"):
            assert len(hashes[name]) == 64

    def test_trial_exception_and_cleanup_failure_leave_durable_evidence(self, tmp_path: Path, monkeypatch):
        head = "f" * 40
        controlling_head = "a" * 40
        monkeypatch.setattr(
            campaign_runner,
            "preflight_at_head",
            lambda value: {"status": "preflight-ready", "version": "codex-cli 0.test"},
        )

        def fake_run(argv, **kwargs):
            if argv[:3] == ["git", "rev-parse", "HEAD"]:
                return subprocess.CompletedProcess(argv, 0, controlling_head + "\n", "")
            if argv[:4] == ["git", "worktree", "add", "--detach"]:
                return subprocess.CompletedProcess(argv, 0, "", "")
            if argv[:4] == ["git", "worktree", "remove", "--force"]:
                return subprocess.CompletedProcess(argv, 1, "", "cleanup refused")
            if argv[:2] == ["codex", "exec"]:
                raise OSError("provider launch exploded")
            raise AssertionError(argv)

        monkeypatch.setattr(campaign_runner.subprocess, "run", fake_run)
        result = campaign_runner.run_campaign(
            DOCS / "campaign.json",
            tmp_path,
            head,
            family="luna",
            scenario_id="trivial-docs",
        )
        assert result == 2
        run_dir = tmp_path / head / "luna" / "trivial-docs"
        meta = json.loads(_read(run_dir / "meta.json"))
        assert meta["availability"] == "trial-error"
        assert meta["error"]["kind"] == "OSError"
        assert meta["cleanup"]["status"] == "failed"
        assert (run_dir / "hashes.json").is_file()

    def test_model_unavailable_trial_is_recorded_without_becoming_harness_failure(self, tmp_path: Path, monkeypatch):
        head = "1" * 40
        monkeypatch.setattr(
            campaign_runner,
            "preflight_at_head",
            lambda value: {"status": "preflight-ready", "version": "codex-cli 0.test"},
        )

        def fake_run(argv, **kwargs):
            if argv[:3] == ["git", "rev-parse", "HEAD"]:
                return subprocess.CompletedProcess(argv, 0, "2" * 40 + "\n", "")
            if argv[:4] == ["git", "worktree", "add", "--detach"]:
                return subprocess.CompletedProcess(argv, 0, "", "")
            if argv[:4] == ["git", "worktree", "remove", "--force"]:
                return subprocess.CompletedProcess(argv, 0, "", "")
            if argv[:2] == ["codex", "exec"]:
                return subprocess.CompletedProcess(
                    argv,
                    1,
                    "",
                    "Error: requested model gpt-6-astra is not available for this account",
                )
            raise AssertionError(argv)

        monkeypatch.setattr(campaign_runner.subprocess, "run", fake_run)
        result = campaign_runner.run_campaign(
            DOCS / "campaign.json",
            tmp_path,
            head,
            family="astra",
            scenario_id="trivial-docs",
        )
        assert result == 0
        meta = json.loads(_read(tmp_path / head / "astra" / "trivial-docs" / "meta.json"))
        assert meta["availability"] == "model-unavailable"

    def test_metrics_use_unobservable_for_unprovable_values(self):
        metrics = campaign_runner.extract_mechanical_metrics('{"type":"tool_call"}\n', "Need clarification?\n")
        assert metrics["question_count"] == 1
        assert metrics["reads_before_useful_action"] == "unobservable"

    def test_scanner_is_candidate_only(self, tmp_path: Path):
        path = tmp_path / "sample.md"
        path.write_text("Run the full test suite.\n", encoding="utf-8")
        hits = pressure_scan.scan_paths([path], tmp_path)
        assert hits and hits[0]["pattern"] == "full-test-suite"

    def test_scanner_includes_extensionless_shebang_templates(self, tmp_path: Path):
        path = tmp_path / "pre-commit"
        path.write_text("#!/usr/bin/env bash\ntools/run.py ci --check\n", encoding="utf-8")
        hits = pressure_scan.scan_paths([path], tmp_path)
        assert hits and hits[0]["pattern"] == "portable-repo-command"

    def test_scanner_detects_generic_windows_drive_root_paths(self, tmp_path: Path):
        path = tmp_path / "portable.md"
        path.write_text(r"Use Z:\\_agent-scratch\\branch\\plan for temporary work." + "\n", encoding="utf-8")
        hits = pressure_scan.scan_paths([path], tmp_path)
        assert any(hit["pattern"] == "personal-path" for hit in hits)


class TestPressureRepairContracts:
    def test_pressure_repairs_are_owned_by_canonical_instruction_sources(self):
        bootstrap = _read(SKILLS / "using-superpowers-plus" / "SKILL.md")
        routing = _read(SKILLS / "using-superpowers-plus" / "references" / "bootstrap-routing.md")
        routing_flat = " ".join(routing.split())
        questions = _read(SKILLS / "asking-clarifying-questions" / "SKILL.md")
        brainstorming = _read(SKILLS / "brainstorming" / "SKILL.md")
        environment = _read(SKILLS / "inspecting-the-environment" / "SKILL.md")
        execution = _read(SKILLS / "executing-plans" / "SKILL.md")
        finishing = _read(SKILLS / "finishing-a-development-branch" / "SKILL.md")
        safety = _read(REPO_SKILLS / "risk-gates" / "references" / "gates" / "safety-gate.md")
        repo_worker = _read(REPO_SKILLS / "repo-worker-base" / "SKILL.md")
        assert "tiny_reversible_change" in routing
        assert ".agents/playbooks/INDEX.md" in routing
        assert ".agents/runbooks/INDEX.md" in routing
        assert "session start, resume, and whenever the active concern changes" in routing_flat
        assert "independently of runbook selection" in routing_flat
        assert "Tiny reversible fast path" in bootstrap
        assert "Taste ambiguity stop" in bootstrap
        assert "Checkpoint-first resume exception" in bootstrap
        assert "Destructive-authority stop" in bootstrap
        assert "taste words" in questions
        assert "before source inspection" not in questions.split("---", 2)[1]
        assert "decision remains human-owned" in questions
        assert "invites collaboration" in questions
        assert "unresolved human-owned taste" in brainstorming.split("---", 2)[1]
        assert "technical assumption" in brainstorming and "focused proof" in brainstorming
        assert "Tiny bounded sketch" in brainstorming
        assert "missing destructive authority" in environment.split("---", 2)[1]
        assert "read that checkpoint before this skill or any" in bootstrap
        assert "read the committed in-flight checkpoint before live repository inspection" in execution
        assert "committed in-flight checkpoint before live repository inspection" in execution
        assert "inspect the current branch and status" in finishing
        assert "find .agents -maxdepth 2 -type f -iname '*evidence*'" in finishing
        assert "first response" in safety and "reversible alternative" in safety
        assert "recoverability does not grant authority" in safety.lower()
        assert "git switch --orphan" in safety
        assert "stop and wait" in " ".join(safety.lower().split())
        assert "portable suggestion conflicts" in repo_worker.split("---", 2)[1]
        assert "repository guidance" in bootstrap and "owner gate" in bootstrap
