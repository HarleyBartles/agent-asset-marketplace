from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PLUGIN_SOURCE = ROOT / "dist/plugins/agent-operating-model"
SKILL_NAME = "tracked-repo-hooks"


def _files(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file() and not {"__pycache__", "evaluator-only"}.intersection(path.parts)
    }


def _copy_asset_tree(source: Path, destination: Path, relative: str) -> None:
    shutil.copytree(source / relative, destination / relative, dirs_exist_ok=True)


def test_tracked_hook_skill_is_packaged_byte_identically_with_optional_assets() -> None:
    canonical = ROOT / "skills" / SKILL_NAME
    generated = PLUGIN_SOURCE / "skills" / SKILL_NAME
    manifest = json.loads((PLUGIN_SOURCE / "references/bundle-manifest.json").read_text(encoding="utf-8"))
    entries = {entry["canonical_name"] for entry in manifest["entries"]}

    assert SKILL_NAME in entries
    assert _files(canonical) == _files(generated)
    for relative in (
        "assets/hooks/pre-commit",
        "assets/normalization/normalize_text.py",
        "assets/normalization/gitattributes.example",
        "assets/targets/repository_gate.py",
        "assets/workflows/github-actions-hosted-gate.yml",
    ):
        assert (generated / relative).is_file(), relative
    assert not (generated / "tests/evaluator-only").exists()


def test_generated_package_assets_run_from_an_isolated_consumer(tmp_path: Path) -> None:
    installed_plugin = tmp_path / "isolated-install/agent-operating-model"
    shutil.copytree(PLUGIN_SOURCE, installed_plugin)
    installed_skill = installed_plugin / "skills" / SKILL_NAME
    consumer = tmp_path / "consumer"
    test_skill = consumer / "skills" / SKILL_NAME
    consumer.mkdir()

    for relative in ("assets/normalization", "assets/hooks", "assets/targets", "assets/workflows", "tests/assets"):
        _copy_asset_tree(installed_skill, test_skill, relative)

    deployed = {
        "tools/normalize_text.py": "assets/normalization/normalize_text.py",
        "githooks/pre-commit": "assets/hooks/pre-commit",
        "tools/targets/repository_gate.py": "assets/targets/repository_gate.py",
        ".github/workflows/hosted-gate.yml": "assets/workflows/github-actions-hosted-gate.yml",
    }
    for destination, source in deployed.items():
        target = consumer / destination
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(test_skill / source, target)

    sample = consumer / "selected text.txt"
    sample.write_bytes(b"line one\r\nline two\r")
    env = os.environ.copy()
    env.pop("PYTHONPATH", None)
    for name in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE"):
        env.pop(name, None)
    normalized = subprocess.run(
        [
            sys.executable,
            str(consumer / "tools/normalize_text.py"),
            "--apply",
            "--line-ending",
            "lf",
            "--final-newline",
            "ensure",
            str(sample),
        ],
        cwd=consumer,
        env=env,
        capture_output=True,
        check=False,
    )
    assert normalized.returncode == 0, normalized.stdout.decode() + normalized.stderr.decode()
    assert sample.read_bytes() == b"line one\nline two\n"

    behavior_tests = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", str(test_skill / "tests/assets")],
        cwd=consumer,
        env=env,
        capture_output=True,
        check=False,
    )
    output = behavior_tests.stdout.decode(errors="replace") + behavior_tests.stderr.decode(errors="replace")
    assert behavior_tests.returncode == 0, output
    assert (consumer / "githooks/pre-commit").is_file()
    assert (consumer / "tools/targets/repository_gate.py").is_file()
