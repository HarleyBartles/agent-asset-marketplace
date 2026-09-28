from __future__ import annotations
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

SKILLS = ROOT / "codex-marketplace" / "plugins" / "superpowers-plus" / "skills"

REPO_SKILLS = ROOT / "codex-marketplace" / "plugins" / "repo-worker-pack" / "skills"

OPERATING_SKILLS = ROOT / "codex-marketplace" / "plugins" / "agent-operating-model" / "skills"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


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
