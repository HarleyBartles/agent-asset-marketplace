from __future__ import annotations
import json
import re
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
            "codex-marketplace/plugins/superpowers-plus/skills/systematic-debugging/tests/references/design-rationale.md",
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


class TestPressureRepairContracts:
    def test_pressure_repairs_are_owned_by_canonical_instruction_sources(self):
        bootstrap = _read(SKILLS / "using-superpowers-plus" / "SKILL.md")
        routing = _read(SKILLS / "using-superpowers-plus" / "references" / "bootstrap-routing.md")
        questions = _read(SKILLS / "asking-clarifying-questions" / "SKILL.md")
        brainstorming = _read(SKILLS / "brainstorming" / "SKILL.md")
        environment = _read(SKILLS / "inspecting-the-environment" / "SKILL.md")
        execution = _read(SKILLS / "executing-plans" / "SKILL.md")
        finishing = _read(SKILLS / "finishing-a-development-branch" / "SKILL.md")
        safety = _read(REPO_SKILLS / "risk-gates" / "references" / "gates" / "safety-gate.md")
        repo_worker = _read(REPO_SKILLS / "repo-worker-base" / "SKILL.md")
        assert "tiny_reversible_change" in routing
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
