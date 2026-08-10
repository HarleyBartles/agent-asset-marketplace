#!/usr/bin/env python3
"""Focused tests for next_node.py --propose graph transitions."""

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parent.parent
NEXT_NODE = SKILL_DIR / "scripts" / "next_node.py"


def _write_state(scratch: Path, *, current: str = "setup", previous: str = "") -> Path:
    p = scratch / "review-state.json"
    p.write_text(
        json.dumps(
            {
                "current_node": current,
                "previous_node": previous,
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


def _propose(state: Path, node: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["py", "-3", str(NEXT_NODE), "--state", str(state), "--propose", node],
        capture_output=True,
        text=True,
    )


class TestNextNodePropose(unittest.TestCase):
    def test_propose_setup_allows_normalize_inputs(self):
        with tempfile.TemporaryDirectory() as td:
            scratch = Path(td)
            state = _write_state(scratch)
            result = _propose(state, "normalize-inputs")
            self.assertEqual(result.returncode, 0)
            self.assertIn("ALLOWED: normalize-inputs", result.stdout)

    def test_propose_blocked_for_missing_artifact(self):
        with tempfile.TemporaryDirectory() as td:
            scratch = Path(td)
            # With no unresolved findings and no regressions, reviewer-fixes is
            # ready for the resolved-ledger node, which requires resolutions.jsonl.
            state = _write_state(scratch, current="reviewer-fixes", previous="regression-scan")
            (scratch / "findings.jsonl").write_text("", encoding="utf-8")
            (scratch / "regressions.jsonl").write_text("", encoding="utf-8")
            result = _propose(state, "resolved-ledger")
            self.assertEqual(result.returncode, 1)
            self.assertIn("BLOCKED", result.stderr)
            self.assertIn("resolutions.jsonl", result.stderr)


if __name__ == "__main__":
    unittest.main()
