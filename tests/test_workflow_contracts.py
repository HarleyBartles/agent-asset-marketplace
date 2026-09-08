from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "codex-marketplace" / "plugins" / "superpowers-plus" / "skills"
REPO_SKILLS = ROOT / "codex-marketplace" / "plugins" / "repo-worker-pack" / "skills"
DOCS = ROOT / "tests" / "pressure" / "workflow-contracts"
sys.path.insert(0, str(ROOT / "tools"))
import run_workflow_pressure_campaign as campaign_runner  # noqa: E402
import workflow_pressure_scan as pressure_scan  # noqa: E402


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class TestAuthorityBootstrapPortability:
    def test_superpowers_plus_version_matches_pinned_upstream_release(self):
        plugin = json.loads(_read(SKILLS.parent / ".codex-plugin" / "plugin.json"))
        bundle = json.loads(_read(SKILLS.parent / "references" / "bundle-manifest.json"))
        assert plugin["version"] == "6.3.0"
        assert bundle["bundle_version"] == "6.3.0"

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
        for root in (SKILLS, REPO_SKILLS):
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

    def test_verification_is_state_bound_not_message_bound(self):
        text = _read(SKILLS / "verification-before-completion" / "SKILL.md").lower()
        assert "tested state" in text
        assert "this message" not in text

    def test_branch_finish_reuses_valid_evidence_and_defaults_to_draft(self):
        text = _read(SKILLS / "finishing-a-development-branch" / "SKILL.md").lower()
        assert "reuse" in text and "evidence" in text
        assert "draft" in text

    def test_tdd_allows_transitive_coverage_for_glue(self):
        text = _read(SKILLS / "test-driven-development" / "SKILL.md").lower()
        assert "transitive" in text or "independent behavior" in text


class TestPlanningDelegationReview:
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
            REPO_SKILLS / "repo-standards" / "templates" / "pre-commit",
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
        assert "linear" in text and "owning" in text
        assert "touched surface" in text
        assert "product/architecture" in text


class TestRepositoryCallersAndPressure:
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
        findings = json.loads(_read(DOCS / "pressure-scan.json"))
        classified = _read(DOCS / "pressure-scan.md")
        assert isinstance(findings, list)
        assert all({"path", "line", "pattern", "context"} <= set(item) for item in findings)
        assert "classification" in classified
        assert all(label in classified for label in ("intended", "repo-local"))
        assert "deferred" not in classified
        assert "| defect |" not in classified

    def test_pressure_scan_has_one_owned_disposition_per_candidate(self):
        findings = json.loads(_read(DOCS / "pressure-scan.json"))
        dispositions = json.loads(_read(DOCS / "pressure-scan-dispositions.json"))
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
        assert len(campaign["scenarios"]) == 13
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

    def test_raw_runs_are_ignored_and_scores_are_durable(self):
        result = __import__("subprocess").run(
            ["git", "check-ignore", "tests/pressure/workflow-contracts/runs/probe/events.jsonl"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "scores/<head>/<family>/<scenario-id>.json" in _read(
            ROOT / ".agents" / "plans" / "2026-09-06-mark-373-operating-system.md"
        )

    def test_committed_campaign_meta_and_scores_are_self_contained(self):
        meta = json.loads(_read(DOCS / "campaign-meta.json"))
        assert meta["schema_version"] == 1
        assert meta["evaluation_head"] == "8f6280aa5dad59b33124f50af37b7f7150ea2afa"
        assert meta["status"] == "harness-blocked"
        assert meta["completed_trials"] == 0
        assert meta["superseded_diagnostic_trials"] == 52
        assert meta["score_validity"] == "superseded-diagnostic-only"
        assert meta["requested_head"] == meta["evaluation_head"]
        assert meta["preflight_head"] == meta["evaluation_head"]
        assert meta["preflight_worktree_status"] == "clean"
        assert meta["inventory"]["mcp"]["exposed"] is True
        assert meta["smoke_status"] == "not-run"
        score_paths = sorted((DOCS / "scores").glob("*/*/*.json"))
        assert len(score_paths) == 52
        for path in score_paths:
            score = json.loads(_read(path))
            assert score["schema_version"] == 1
            assert score["trial"]["status"] == "ok"
            assert score["judge"] == {
                "kind": "executor-inline",
                "family": "luna",
                "model": "gpt-5.6-luna",
                "reasoning_effort": "medium",
                "separate_codex_exec": False,
            }
            assert score["raw_evidence"]["committed"] is False
            assert all(
                len(score["raw_evidence"][name]) == 64
                for name in (
                    "events_jsonl_sha256",
                    "stderr_sha256",
                    "final_sha256",
                    "meta_sha256",
                )
            )
            assert score["mechanical"]["reads_before_useful_action"] == "unobservable"
            assert score["criteria"]
            assert score["overall_verdict"] in {"pass", "fail"}
            assert score["failure_class"] in {
                "none",
                "instruction-composition",
                "harness-capability",
                "model-behavior",
            }

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


class TestQuorumExamScaffolding:
    def test_mark373_quorum_exam_has_one_scenario_for_each_campaign_cell(self):
        exam = DOCS / "quorum"
        expected = {
            "trivial-docs",
            "specified-bug-red",
            "genuine-ambiguity",
            "wrong-reviewer",
            "authorized-draft-pr",
            "compaction-resume",
            "unauthorized-destructive",
            "bounded-parallel",
            "small-reversible",
            "repo-portable-conflict",
            "tiny-no-approval-design",
            "branch-finish-evidence",
            "no-independent-behavior-helper",
        }
        scenarios = exam / "scenarios"
        assert scenarios.is_dir()
        assert {path.name for path in scenarios.iterdir() if path.is_dir()} == expected
        for scenario in sorted(expected):
            path = scenarios / scenario
            story = _read(path / "story.md")
            setup = _read(path / "setup.sh")
            checks = _read(path / "checks.sh")
            codex_config = _read(path / "codex.config.toml")
            assert f"id: {scenario}" in story
            assert "## Acceptance Criteria" in story
            assert "read `HOWTO.md`" in story
            assert "Never type a bare `codex` command" in story
            assert "setup-helpers run" in setup
            assert "stage-skills-only.sh" in setup
            assert "pre()" in checks and "post()" in checks
            assert "$QUORUM_WORKDIR" not in checks
            assert "[features]" not in codex_config
            assert "features.plugins = false" in codex_config
            assert "features.apps = false" in codex_config

    def test_mark373_quorum_launcher_projects_windows_codex_auth_into_wsl(self):
        launcher = _read(DOCS / "quorum" / "run-mark373-quorum.ps1")
        assert "wsl.exe" in launcher
        assert "openai_responses_56luna" in launcher
        assert "--no-superpowers" in launcher
        assert "status --porcelain" in launcher
        assert "--git-dir" in launcher
        assert "--work-tree" in launcher
        assert 'mkdir -p "results/mark373/$evidence_head"' in launcher
        assert 'export PATH="$quorum_bin:$PATH"' in launcher
        assert "OPENAI_API_KEY" in launcher
        assert "--grader-model gpt-5.4" in launcher
        assert '--gauntlet-bin "$quorum_bin/gauntlet"' in launcher
        assert 'export ANTHROPIC_API_KEY="$OPENAI_API_KEY"' in launcher
        assert "Quorum OpenAI grader requires OPENAI_API_KEY" in launcher
        assert "[switch]$Preflight" in launcher

        gauntlet = DOCS / "quorum" / "bin" / "gauntlet"
        shim = _read(gauntlet)
        assert "evals/gauntlet" in shim
        assert "export OPENAI_API_KEY=${ANTHROPIC_API_KEY:" in shim
        assert "unset ANTHROPIC_API_KEY" in shim
        assert "npx --yes bun run" in shim

    def test_skills_only_stage_copies_the_exact_composed_stack(self):
        stage = _read(DOCS / "quorum" / "lib" / "stage-skills-only.sh")
        assert ".agents/skills" in stage
        assert "wslpath -a" in stage
        assert '--git-dir="$marketplace_git_dir"' in stage
        assert '--work-tree="$marketplace_root"' in stage
        assert "rev-parse HEAD" in stage
        assert "sha256sum" in stage
        assert "cp -a" in stage

    def test_local_quorum_clone_is_excluded_from_repo_mesh_traversal(self):
        mesh = _read(REPO_SKILLS / "generating-agent-mesh" / "scripts" / "generate_index_mesh.py")
        assert '"evals"' in mesh
