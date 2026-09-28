from __future__ import annotations
import json
import subprocess
import sys
from pathlib import Path
import pytest


ROOT = Path(__file__).resolve().parents[1]

DOCS = ROOT / "tests" / "pressure" / "workflow-contracts"


sys.path.insert(0, str(ROOT / "tools"))


import run_workflow_pressure_campaign as campaign_runner  # noqa: E402
import workflow_pressure_scan as pressure_scan  # noqa: E402


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


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
