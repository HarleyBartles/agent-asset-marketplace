#!/usr/bin/env python3
"""Focused tests for record_finding.py and record_resolution.py."""

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parent.parent
RECORD_FINDING = SKILL_DIR / "scripts" / "record_finding.py"
RECORD_RESOLUTION = SKILL_DIR / "scripts" / "record_resolution.py"
RECORD_ORCHESTRATOR_LOG = SKILL_DIR / "scripts" / "record_orchestrator_log.py"


def _write_state(scratch: Path) -> Path:
    p = scratch / "review-state.json"
    p.write_text(
        json.dumps(
            {
                "current_node": "setup",
                "previous_node": "",
                "round": 1,
                "max_fix_rounds": 4,
                "pr": {
                    "pr_number": 999,
                    "base": "main",
                    "branch": "test",
                    "head_sha": "abc123",
                },
                "scratch_dir": str(scratch),
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    return p


def _run(script: Path, state: Path, data: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["py", "-3", str(script), "--state", str(state), "--data", data],
        capture_output=True,
        text=True,
    )


class TestRecordFinding(unittest.TestCase):
    def test_record_finding_appends_object(self):
        with tempfile.TemporaryDirectory() as td:
            scratch = Path(td)
            state = _write_state(scratch)
            data = json.dumps(
                {
                    "finding_id": "f-001",
                    "lens": "scripts",
                    "discovered_at_node": "lens-dispatch",
                    "discovered_at_round": 1,
                    "severity": "minor",
                }
            )
            result = _run(RECORD_FINDING, state, data)
            self.assertEqual(result.returncode, 0)
            log = scratch / "findings.jsonl"
            self.assertTrue(log.exists())
            lines = log.read_text(encoding="utf-8").strip().splitlines()
            self.assertEqual(len(lines), 1)
            self.assertIn("f-001", lines[0])

    def test_record_finding_rejects_scalar(self):
        with tempfile.TemporaryDirectory() as td:
            scratch = Path(td)
            state = _write_state(scratch)
            result = _run(RECORD_FINDING, state, '"not-an-object"')
            self.assertEqual(result.returncode, 1)
            self.assertIn("must be a JSON object or array", result.stderr)

    def test_record_finding_rejects_array_of_scalars(self):
        with tempfile.TemporaryDirectory() as td:
            scratch = Path(td)
            state = _write_state(scratch)
            result = _run(RECORD_FINDING, state, '["a", "b"]')
            self.assertEqual(result.returncode, 1)
            self.assertIn("every --data item must be a JSON object", result.stderr)


class TestRecordResolution(unittest.TestCase):
    def test_record_resolution_appends_object(self):
        with tempfile.TemporaryDirectory() as td:
            scratch = Path(td)
            state = _write_state(scratch)
            data = json.dumps(
                {
                    "finding_id": "f-001",
                    "resolved_at_node": "finding-fix",
                    "resolved_at_round": 2,
                }
            )
            result = _run(RECORD_RESOLUTION, state, data)
            self.assertEqual(result.returncode, 0)
            log = scratch / "resolutions.jsonl"
            self.assertTrue(log.exists())
            lines = log.read_text(encoding="utf-8").strip().splitlines()
            self.assertEqual(len(lines), 1)
            self.assertIn("f-001", lines[0])

    def test_record_resolution_rejects_non_object(self):
        with tempfile.TemporaryDirectory() as td:
            scratch = Path(td)
            state = _write_state(scratch)
            result = _run(RECORD_RESOLUTION, state, "[1, 2]")
            self.assertEqual(result.returncode, 1)
            self.assertIn("every --data item must be a JSON object", result.stderr)


class TestRecordOrchestratorLog(unittest.TestCase):
    def test_record_orchestrator_log_check(self):
        result = subprocess.run(
            ["py", "-3", str(RECORD_ORCHESTRATOR_LOG), "--check"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0)

    def test_record_orchestrator_log_appends_with_apply(self):
        with tempfile.TemporaryDirectory() as td:
            scratch = Path(td)
            state = _write_state(scratch)
            result = subprocess.run(
                [
                    "py",
                    "-3",
                    str(RECORD_ORCHESTRATOR_LOG),
                    "--state",
                    str(state),
                    "--node",
                    "orchestrator-self-review",
                    "--data",
                    "test entry",
                    "--apply",
                ],
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0)
            log = scratch / "review-log-orchestrator-self-review.md"
            self.assertTrue(log.exists())
            self.assertIn("test entry", log.read_text(encoding="utf-8"))

    def test_record_orchestrator_log_appends_from_data_file(self):
        with tempfile.TemporaryDirectory() as td:
            scratch = Path(td)
            state = _write_state(scratch)
            data_file = scratch / "filled-template.md"
            data_file.write_text("file entry", encoding="utf-8")
            result = subprocess.run(
                [
                    "py",
                    "-3",
                    str(RECORD_ORCHESTRATOR_LOG),
                    "--state",
                    str(state),
                    "--node",
                    "orchestrator-self-review",
                    "--data-file",
                    str(data_file),
                    "--apply",
                ],
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0)
            log = scratch / "review-log-orchestrator-self-review.md"
            self.assertTrue(log.exists())
            self.assertIn("file entry", log.read_text(encoding="utf-8"))

    def test_record_orchestrator_log_rejects_missing_args(self):
        with tempfile.TemporaryDirectory() as td:
            scratch = Path(td)
            state = _write_state(scratch)
            result = subprocess.run(
                ["py", "-3", str(RECORD_ORCHESTRATOR_LOG), "--state", str(state), "--node", "orchestrator-self-review"],
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 2)
            self.assertIn("the following arguments are required", result.stderr)


if __name__ == "__main__":
    unittest.main()
