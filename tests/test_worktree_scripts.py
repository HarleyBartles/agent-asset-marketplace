import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
NEW_WORKTREE = (
    REPO_ROOT / "adapters" / "codex" / "superpowers-plus" / "using-git-worktrees" / "scripts" / "new_worktree.py"
)
REMOVE_WORKTREE = (
    REPO_ROOT / "adapters" / "codex" / "superpowers-plus" / "using-git-worktrees" / "scripts" / "remove_worktree.py"
)


def _make_repo(tmp_path: Path, name: str) -> Path:
    repo = tmp_path / name
    repo.mkdir()
    subprocess.run(["git", "init"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@test"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=repo, check=True, capture_output=True)
    (repo / "README.md").write_text("# test\n", encoding="utf-8")
    subprocess.run(["git", "add", "-A"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "init"], cwd=repo, check=True, capture_output=True)
    return repo


def _make_repo_with_bundled_refresh(tmp_path: Path, name: str) -> Path:
    """Create a fake repo with enough marketplace structure for new-worktree to auto-refresh skills."""
    repo = _make_repo(tmp_path, name)
    pack = repo / "codex-marketplace" / "plugins" / "repo-worker-pack" / "skills"
    pack.mkdir(parents=True)
    source_refresh = REPO_ROOT / "sources" / "first_party" / "skills" / "refreshing-installed-skills"
    source_mesh = REPO_ROOT / "sources" / "first_party" / "skills" / "generating-agent-mesh"
    shutil.copytree(source_refresh, pack / "refreshing-installed-skills")
    shutil.copytree(source_mesh, pack / "generating-agent-mesh")
    (repo / ".agents" / "plugins").mkdir(parents=True)
    marketplace = {
        "plugins": [
            {
                "name": "repo-worker-pack",
                "source": {"source": "local", "path": "./codex-marketplace/plugins/repo-worker-pack"},
                "policy": {"installation": "INSTALLED_BY_DEFAULT", "authentication": "ON_INSTALL"},
            }
        ]
    }
    (repo / ".agents" / "plugins" / "marketplace.json").write_text(
        json.dumps(marketplace, indent=2) + "\n", encoding="utf-8"
    )
    subprocess.run(["git", "add", "-A"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "add refresh scaffolding"], cwd=repo, check=True, capture_output=True)
    return repo


def _stripped_env():
    env = os.environ.copy()
    env.pop("GIT_DIR", None)
    env.pop("GIT_WORK_TREE", None)
    env.pop("GIT_INDEX_FILE", None)
    return env


def test_new_help_exits_zero() -> None:
    result = subprocess.run([sys.executable, str(NEW_WORKTREE), "--help"], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert "branch" in result.stdout.lower()


def test_remove_help_exits_zero() -> None:
    result = subprocess.run([sys.executable, str(REMOVE_WORKTREE), "--help"], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert "worktree" in result.stdout.lower()


def test_new_and_remove_create_cycle(tmp_path: Path) -> None:
    repo = _make_repo(tmp_path, "cycle-repo")
    worktree_root = tmp_path / "_agent-worktrees" / "cycle-repo" / "feature"
    result = subprocess.run(
        [sys.executable, str(NEW_WORKTREE), "feature", "--no-skill-refresh"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert worktree_root.is_dir()

    result = subprocess.run(
        [sys.executable, str(REMOVE_WORKTREE), "feature"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert not worktree_root.exists()


def test_new_worktree_base_ref(tmp_path: Path) -> None:
    repo = _make_repo(tmp_path, "base-ref-repo")
    marker = "base-marker.txt"
    (repo / marker).write_text("from-base", encoding="utf-8")
    subprocess.run(["git", "add", "-A"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "base"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "tag", "v1-base"], cwd=repo, check=True, capture_output=True)

    worktree_root = tmp_path / "_agent-worktrees" / "base-ref-repo" / "feature"
    result = subprocess.run(
        [sys.executable, str(NEW_WORKTREE), "feature", "--base-ref", "v1-base", "--no-skill-refresh"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert worktree_root.is_dir()
    assert (worktree_root / marker).read_text(encoding="utf-8") == "from-base"


def test_new_worktree_defaults_to_origin_main(tmp_path: Path) -> None:
    remote = tmp_path / "origin-main-remote"
    remote.mkdir()
    subprocess.run(["git", "init", "--bare"], cwd=remote, check=True, capture_output=True)

    repo = _make_repo(tmp_path, "origin-main-local")
    subprocess.run(["git", "branch", "-m", "main"], cwd=repo, check=True, capture_output=True)
    subprocess.run(
        ["git", "remote", "add", "origin", str(remote)],
        cwd=repo,
        check=True,
        capture_output=True,
    )
    # Push the initial commit; this also pins repo's local origin/main to that commit.
    subprocess.run(["git", "push", "origin", "main"], cwd=repo, check=True, capture_output=True)

    # Add a second commit to the remote from a separate clone so that repo's
    # origin/main becomes stale. new_worktree.py must fetch before it can base
    # the new worktree branch on the latest origin/main tip.
    upstream = tmp_path / "upstream"
    subprocess.run(
        ["git", "clone", "--branch", "main", str(remote), str(upstream)],
        check=True,
        capture_output=True,
    )
    subprocess.run(["git", "config", "user.email", "test@test"], cwd=upstream, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=upstream, check=True, capture_output=True)

    marker = "origin-main-marker.txt"
    (upstream / marker).write_text("from-origin-main", encoding="utf-8")
    subprocess.run(["git", "add", "-A"], cwd=upstream, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "marker"], cwd=upstream, check=True, capture_output=True)
    subprocess.run(["git", "push", "origin", "main"], cwd=upstream, check=True, capture_output=True)

    expected_sha = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=upstream,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()

    worktree_root = tmp_path / "_agent-worktrees" / "origin-main-local" / "feature"
    result = subprocess.run(
        [sys.executable, str(NEW_WORKTREE), "feature", "--no-skill-refresh"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert worktree_root.is_dir()

    worktree_head = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=worktree_root,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    assert worktree_head == expected_sha
    assert (worktree_root / marker).read_text(encoding="utf-8") == "from-origin-main"


def test_remove_worktree_resolves_by_full_ref_and_directory(tmp_path: Path) -> None:
    repo = _make_repo(tmp_path, "resolve-repo")

    # Full ref match
    worktree_full = tmp_path / "_agent-worktrees" / "resolve-repo" / "feature-full"
    result = subprocess.run(
        [sys.executable, str(NEW_WORKTREE), "feature-full", "--no-skill-refresh"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert worktree_full.is_dir()

    result = subprocess.run(
        [sys.executable, str(REMOVE_WORKTREE), "refs/heads/feature-full"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert not worktree_full.exists()

    # Trailing segment / directory name match
    worktree_dir = tmp_path / "_agent-worktrees" / "resolve-repo" / "feature-dir"
    result = subprocess.run(
        [sys.executable, str(NEW_WORKTREE), "feature-dir", "--no-skill-refresh"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert worktree_dir.is_dir()

    result = subprocess.run(
        [sys.executable, str(REMOVE_WORKTREE), "feature-dir"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert not worktree_dir.exists()


def test_new_worktree_fails_when_target_path_already_exists(tmp_path: Path) -> None:
    repo = _make_repo(tmp_path, "exists-repo")
    worktree_root = tmp_path / "_agent-worktrees" / "exists-repo" / "feature"
    worktree_root.parent.mkdir(parents=True, exist_ok=True)

    # Existing file
    worktree_root.write_text("existing file", encoding="utf-8")
    result = subprocess.run(
        [sys.executable, str(NEW_WORKTREE), "feature", "--no-skill-refresh"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "file" in result.stderr.lower()

    # Existing directory
    worktree_root.unlink()
    worktree_root.mkdir(parents=True)
    result = subprocess.run(
        [sys.executable, str(NEW_WORKTREE), "feature", "--no-skill-refresh"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "directory" in result.stderr.lower()


def test_new_worktree_runs_refresh_installed_skills(tmp_path: Path) -> None:
    repo = _make_repo_with_bundled_refresh(tmp_path, "refresh-repo")
    worktree_root = tmp_path / "_agent-worktrees" / "refresh-repo" / "feature"
    result = subprocess.run(
        [sys.executable, str(NEW_WORKTREE), "feature"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert worktree_root.is_dir()
    assert "Worktree ready" in result.stdout
    assert "Installed skill" in result.stdout
    assert "index mesh" in result.stdout


def test_remove_worktree_resolves_branch_namespace(tmp_path: Path) -> None:
    repo = _make_repo(tmp_path, "namespace-repo")

    team_root = tmp_path / "_agent-worktrees" / "namespace-repo" / "team" / "feature"
    result = subprocess.run(
        [sys.executable, str(NEW_WORKTREE), "team/feature", "--no-skill-refresh"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert team_root.is_dir()

    personal_root = tmp_path / "_agent-worktrees" / "namespace-repo" / "personal" / "feature"
    result = subprocess.run(
        [sys.executable, str(NEW_WORKTREE), "personal/feature", "--no-skill-refresh"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert personal_root.is_dir()

    # Resolve by full ref
    result = subprocess.run(
        [sys.executable, str(REMOVE_WORKTREE), "refs/heads/team/feature"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert not team_root.exists()
    assert personal_root.is_dir()

    # Resolve by branch leaf (ambiguous, should remove the remaining one)
    result = subprocess.run(
        [sys.executable, str(REMOVE_WORKTREE), "feature"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert not personal_root.exists()


def test_new_worktree_rejects_path_traversal(tmp_path: Path) -> None:
    repo = _make_repo(tmp_path, "traversal-repo")
    for branch in ["../evil", "evil/../other"]:
        result = subprocess.run(
            [sys.executable, str(NEW_WORKTREE), branch, "--no-skill-refresh"],
            cwd=repo,
            env=_stripped_env(),
            capture_output=True,
            text=True,
        )
        assert result.returncode != 0, branch
        assert any(
            word in result.stderr.lower()
            for word in ["canonical", "outside", "invalid branch"]
        ), branch


def test_new_worktree_rejects_absolute_branch(tmp_path: Path) -> None:
    repo = _make_repo(tmp_path, "absolute-repo")
    outside = (tmp_path / "outside").resolve()
    result = subprocess.run(
        [sys.executable, str(NEW_WORKTREE), str(outside), "--no-skill-refresh"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert any(
        word in result.stderr.lower()
        for word in ["canonical", "outside", "invalid branch"]
    )


def test_remove_worktree_rejects_ambiguous_leaf(tmp_path: Path) -> None:
    repo = _make_repo(tmp_path, "ambiguous-repo")

    team_root = tmp_path / "_agent-worktrees" / "ambiguous-repo" / "team" / "feature"
    subprocess.run(
        [sys.executable, str(NEW_WORKTREE), "team/feature", "--no-skill-refresh"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        check=True,
    )
    assert team_root.is_dir()

    personal_root = tmp_path / "_agent-worktrees" / "ambiguous-repo" / "personal" / "feature"
    subprocess.run(
        [sys.executable, str(NEW_WORKTREE), "personal/feature", "--no-skill-refresh"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        check=True,
    )
    assert personal_root.is_dir()

    result = subprocess.run(
        [sys.executable, str(REMOVE_WORKTREE), "feature"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "ambiguous" in result.stderr.lower()
    assert team_root.is_dir()
    assert personal_root.is_dir()


def test_remove_worktree_rejects_unregistered_absolute_path(tmp_path: Path) -> None:
    repo = _make_repo(tmp_path, "unregistered-repo")
    outside = tmp_path / "outside"
    outside.mkdir()
    result = subprocess.run(
        [sys.executable, str(REMOVE_WORKTREE), str(outside)],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "not a registered worktree" in result.stderr.lower()


def test_new_worktree_accepts_full_ref(tmp_path: Path) -> None:
    repo = _make_repo(tmp_path, "full-ref-repo")
    worktree_root = tmp_path / "_agent-worktrees" / "full-ref-repo" / "feature"
    result = subprocess.run(
        [sys.executable, str(NEW_WORKTREE), "refs/heads/feature", "--no-skill-refresh"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert worktree_root.is_dir()


def test_remove_worktree_stops_on_locked_directory(tmp_path: Path) -> None:
    """If the worktree directory is locked, the script deregisters it and stops."""
    repo = _make_repo(tmp_path, "locked-repo")
    worktree_root = tmp_path / "_agent-worktrees" / "locked-repo" / "feature"
    result = subprocess.run(
        [sys.executable, str(NEW_WORKTREE), "feature", "--no-skill-refresh"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert worktree_root.is_dir()

    # Lock the directory by starting a process whose cwd is the worktree.
    lock = subprocess.Popen(
        [sys.executable, "-c", "import time; time.sleep(30)"],
        cwd=worktree_root,
    )
    try:
        result = subprocess.run(
            [sys.executable, str(REMOVE_WORKTREE), "feature"],
            cwd=repo,
            env=_stripped_env(),
            capture_output=True,
            text=True,
            timeout=30,
        )
        assert result.returncode != 0
        assert "file is locked for editing; stop" in result.stderr
        assert "Don't continue trying to delete the locked directory" in result.stderr
        assert "Worktree path:" in result.stderr

        # The worktree should be deregistered.
        list_result = subprocess.run(
            ["git", "worktree", "list", "--porcelain"],
            cwd=repo,
            capture_output=True,
            text=True,
        )
        assert list_result.returncode == 0
        assert str(worktree_root) not in list_result.stdout

        # The directory still exists (locked by the other process).
        assert worktree_root.is_dir()
    finally:
        lock.terminate()
        try:
            lock.wait(timeout=5)
        except subprocess.TimeoutExpired:
            lock.kill()
