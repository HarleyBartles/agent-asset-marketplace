#!/usr/bin/env python3
"""Focused tests for select_lenses.py helpers."""

import importlib.util
import subprocess
import tempfile
import unittest
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parent.parent
SELECT_LENSES = SKILL_DIR / "scripts" / "select_lenses.py"


def _load_select_lenses():
    spec = importlib.util.spec_from_file_location("select_lenses", SELECT_LENSES)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TestSelectLensesCLI(unittest.TestCase):
    def test_select_lenses_check(self):
        result = subprocess.run(
            ["py", "-3", str(SELECT_LENSES), "--check"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0)


class TestSelectLensesHelpers(unittest.TestCase):
    def test_applies_to_parses_globs_inputs_keywords_and_strips_backticks(self):
        module = _load_select_lenses()
        text = """# reviewer-test

## Applies to

- globs:
  - `**/scripts/**`
  - `tools/*.py`
- inputs:
  - `<diff_path>`
- keywords:
  - refactor

## Checklist

- C1
"""
        rule = module._applies_to(text)
        self.assertEqual(rule["globs"], ["**/scripts/**", "tools/*.py"])
        self.assertEqual(rule["inputs"], ["<diff_path>"])
        self.assertEqual(rule["keywords"], ["refactor"])

    def test_applies_to_matches_last_section(self):
        module = _load_select_lenses()
        text = """# reviewer-test

## Checklist

- C1

## Applies to

- globs:
  - `tests/**`
"""
        rule = module._applies_to(text)
        self.assertEqual(rule["globs"], ["tests/**"])

    def test_changed_files_captures_renamed_files(self):
        module = _load_select_lenses()
        with tempfile.TemporaryDirectory() as td:
            diff_path = Path(td) / "test.diff"
            diff_path.write_text(
                "diff --git a/old_name.py b/new_name.py\n"
                "--- a/old_name.py\n"
                "+++ b/new_name.py\n"
                "@@ -1 +1 @@\n"
                "diff --git a/unchanged.py b/unchanged.py\n"
            )
            files = module._changed_files(diff_path)
            self.assertIn("old_name.py", files)
            self.assertIn("new_name.py", files)


if __name__ == "__main__":
    unittest.main()
