from __future__ import annotations

from pathlib import Path

import yaml


WORKFLOW = Path(__file__).resolve().parents[2] / "assets" / "workflows" / "github-actions-hosted-gate.yml"


def test_workflow_checks_out_and_runs_the_same_declared_commit_through_the_hook() -> None:
    workflow = yaml.load(WORKFLOW.read_text(encoding="utf-8"), Loader=yaml.BaseLoader)
    jobs = workflow["jobs"]
    gate = jobs["complete-gate"]
    steps = gate["steps"]
    checkout = next(step for step in steps if step.get("uses", "").startswith("actions/checkout@"))
    hosted = next(step for step in steps if step.get("name") == "Run the tracked complete gate")
    hosted_step = hosted["run"]

    assert checkout["with"]["ref"] == "${{ github.event.pull_request.head.sha || github.sha }}"
    assert gate["env"]["COMMIT_SHA"] == "${{ github.event.pull_request.head.sha || github.sha }}"
    assert 'bash githooks/pre-commit --hosted "$COMMIT_SHA"' in hosted_step
    assert "repository_gate.py" not in hosted_step
    assert "tools/run.py" not in hosted_step
    assert len([step for step in steps if step.get("uses", "").startswith("actions/checkout@")]) == 1
    assert not any("marketplace" in step.get("uses", "").lower() for step in steps)
