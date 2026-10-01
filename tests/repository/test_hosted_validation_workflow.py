from __future__ import annotations

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = ROOT / ".github" / "workflows" / "marketplace-validation.yml"
PROPOSED_COMMIT = "${{ github.event.pull_request.head.sha || github.sha }}"


def test_hosted_gate_checks_out_and_validates_the_proposed_commit() -> None:
    workflow = yaml.load(WORKFLOW.read_text(encoding="utf-8"), Loader=yaml.BaseLoader)
    job = workflow["jobs"]["marketplace-validation"]
    checkout = next(step for step in job["steps"] if step.get("name") == "Checkout")
    parity = next(step for step in job["steps"] if step.get("name") == "Verify checked out commit for hosted parity")
    gate = next(step for step in job["steps"] if step.get("name") == "Validate tracked commit gate")

    assert checkout.get("with", {}).get("ref") == PROPOSED_COMMIT
    assert job.get("env", {}).get("REPO_STANDARDS_HOSTED_COMMIT") == PROPOSED_COMMIT
    assert 'test "$(git rev-parse HEAD)" = "$REPO_STANDARDS_HOSTED_COMMIT"' in parity["run"]
    assert 'test "$(git branch --show-current)" = ""' in parity["run"]
    assert gate.get("run", "").startswith("set -euo pipefail")
