from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HOOK = ROOT / "githooks" / "pre-commit"


def _git(repo: Path, *args: str) -> str:
    env = os.environ.copy()
    for name in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE"):
        env.pop(name, None)
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        text=True,
        capture_output=True,
        check=False,
        env=env,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    return result.stdout.strip()


def test_path_limited_commit_hook_validates_git_temporary_index(tmp_path: Path) -> None:
    repo = tmp_path / "path-limited-repo"
    repo.mkdir()
    _git(repo, "init", "--quiet")
    _git(repo, "config", "user.name", "Hook Test")
    _git(repo, "config", "user.email", "hook-test@example.invalid")
    _git(repo, "config", "core.autocrlf", "false")

    (repo / "selected.txt").write_text("base selected\n", encoding="utf-8")
    (repo / "unrelated.txt").write_text("base unrelated\n", encoding="utf-8")
    contracts = repo / ".agents" / "contracts"
    contracts.mkdir(parents=True)
    tools = repo / "tools"
    tools.mkdir()
    observer = tools / "observe_index.py"
    observer.write_text(
        "import subprocess, sys\n"
        "tree = subprocess.run(['git', 'write-tree'], check=True, capture_output=True, text=True).stdout.strip()\n"
        "with open(sys.argv[2], 'a', encoding='utf-8') as stream:\n"
        "    stream.write(f'{sys.argv[1]}:{tree}\\n')\n",
        encoding="utf-8",
    )
    observations = tmp_path / "observed-trees.txt"
    declaration = {
        "apply": ["@python", "tools/observe_index.py", "--apply", str(observations)],
        "check": ["@python", "tools/observe_index.py", "--check", str(observations)],
        "generated_paths": [],
    }
    (contracts / "repo-standards-commands.json").write_text(json.dumps(declaration), encoding="utf-8")
    hooks = repo / "githooks"
    hooks.mkdir()
    hook = hooks / "pre-commit"
    shutil.copyfile(HOOK, hook)
    if os.name != "nt":
        hook.chmod(0o755)

    _git(repo, "add", ".")
    _git(repo, "commit", "--quiet", "-m", "fixture base")
    _git(repo, "config", "core.hooksPath", "githooks")

    (repo / "unrelated.txt").write_text("separately staged\n", encoding="utf-8")
    _git(repo, "add", "unrelated.txt")
    (repo / "selected.txt").write_text("path-limited candidate\n", encoding="utf-8")
    commit_env = {
        name: value for name, value in os.environ.items() if name not in {"GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE"}
    }
    result = subprocess.run(
        ["git", "commit", "--only", "-m", "commit selected path", "--", "selected.txt"],
        cwd=repo,
        text=True,
        capture_output=True,
        check=False,
        env=commit_env,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    committed_tree = _git(repo, "rev-parse", "HEAD^{tree}")
    observed = [line.split(":", 1)[1] for line in observations.read_text(encoding="utf-8").splitlines()]
    assert observed == [committed_tree, committed_tree]
    assert _git(repo, "show", "HEAD:selected.txt") == "path-limited candidate"
    assert _git(repo, "show", "HEAD:unrelated.txt") == "base unrelated"
    assert _git(repo, "show", ":unrelated.txt") == "separately staged"
