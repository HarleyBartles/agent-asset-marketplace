"""Verify disposable fixture custody and distinct review revisions."""

import importlib.util
import subprocess
from pathlib import Path

import pytest


fixture_path = Path(__file__).parents[1] / "pressure" / "fixtures" / "review_case.py"
spec = importlib.util.spec_from_file_location("review_case", fixture_path)
review_case = importlib.util.module_from_spec(spec)
spec.loader.exec_module(review_case)


def git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, text=True).stdout.strip()


def test_rejects_populated_root_without_touching_existing_content(tmp_path):
    retained = tmp_path / "retained.txt"
    retained.write_text("caller-owned", encoding="utf-8")
    with pytest.raises(ValueError, match="absent or empty"):
        review_case.materialize(tmp_path)
    assert retained.read_text(encoding="utf-8") == "caller-owned"
    assert list(tmp_path.iterdir()) == [retained]


def test_rejects_relative_root_before_creating_anything():
    with pytest.raises(ValueError, match="absolute"):
        review_case.materialize(Path("relative-fixture"))


def test_fix_checkout_has_actual_fix_and_independent_revision(tmp_path):
    outputs = review_case.materialize(tmp_path)
    changed = outputs["repo"]
    fixed = outputs["fix_repo"]
    assert git(changed, "rev-parse", "HEAD") != git(fixed, "rev-parse", "HEAD")
    assert git(changed, "status", "--porcelain") == ""
    assert git(fixed, "status", "--porcelain") == ""
    assert (changed / "REVIEW.md").is_file()
    assert not (fixed / "REVIEW.md").exists()
    changed_source = (changed / "labels.py").read_text(encoding="utf-8")
    fixed_source = (fixed / "labels.py").read_text(encoding="utf-8")
    scope = {"__name__": "fixture_labels"}
    exec(changed_source, scope)
    assert scope["render_label"]("<b>&") == "<p><b>&</p>"
    exec(fixed_source, scope)
    assert scope["render_label"]("<b>&") == "<p>&lt;b&gt;&amp;</p>"
    assert "label_or_empty" in scope
    assert outputs["fix_diff"].read_text(encoding="utf-8") == (
        git(fixed, "diff", "--no-color", git(changed, "rev-parse", "HEAD"), "HEAD") + "\n"
    )
