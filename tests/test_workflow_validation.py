from __future__ import annotations
import json
from pathlib import Path
import yaml


ROOT = Path(__file__).resolve().parents[1]

SKILLS = ROOT / "codex-marketplace" / "plugins" / "superpowers-plus" / "skills"

REPO_SKILLS = ROOT / "codex-marketplace" / "plugins" / "repo-worker-pack" / "skills"

OPERATING_SKILLS = ROOT / "codex-marketplace" / "plugins" / "agent-operating-model" / "skills"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


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
