import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[4]
NEW_WORKTREE = REPO_ROOT / "skills" / "using-git-worktrees" / "scripts" / "new_worktree.py"
REMOVE_WORKTREE = REPO_ROOT / "skills" / "finishing-a-development-branch" / "scripts" / "remove_worktree.py"


def _make_repo(tmp_path: Path, name: str) -> Path:
    repo = tmp_path / name
    repo.mkdir()
    subprocess.run(["git", "init"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "config", "core.autocrlf", "false"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "config", "core.safecrlf", "false"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@test"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=repo, check=True, capture_output=True)
    (repo / "README.md").write_text("# test\n", encoding="utf-8")
    subprocess.run(["git", "add", "-A"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "init"], cwd=repo, check=True, capture_output=True)
    return repo


def _make_repo_with_bundled_refresh(tmp_path: Path, name: str) -> Path:
    """Compatibility fixture name for repos that now use native repo plugins."""
    return _make_repo(tmp_path, name)


def _make_repo_with_failing_refresh(tmp_path: Path, name: str) -> Path:
    """Compatibility fixture name; worktree setup no longer refreshes plugin skills."""
    return _make_repo(tmp_path, name)


def _make_repo_with_marketplace_source_submodule(tmp_path: Path, name: str) -> Path:
    """Create a repo with a generic pinned submodule for worktree initialization coverage."""
    repo = _make_repo(tmp_path, name)
    submodule_bare = tmp_path / f"{name}-submodule-bare"
    submodule_bare.mkdir()
    subprocess.run(["git", "init", "--bare"], cwd=submodule_bare, check=True, capture_output=True)

    submodule_work = tmp_path / f"{name}-submodule-work"
    subprocess.run(["git", "clone", str(submodule_bare), str(submodule_work)], check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@test"], cwd=submodule_work, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=submodule_work, check=True, capture_output=True)
    (submodule_work / "payload.txt").write_text("consumer-pinned content\\n", encoding="utf-8")
    subprocess.run(["git", "add", "payload.txt"], cwd=submodule_work, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "add payload"], cwd=submodule_work, check=True, capture_output=True)
    subprocess.run(["git", "push", "origin", "HEAD:main"], cwd=submodule_work, check=True, capture_output=True)

    subprocess.run(
        ["git", "submodule", "add", "-b", "main", submodule_bare.as_uri(), "vendor/dependency"],
        cwd=repo,
        check=True,
        capture_output=True,
    )
    subprocess.run(["git", "submodule", "update", "--init"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "add", "-A"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "add pinned dependency"], cwd=repo, check=True, capture_output=True)
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


def test_installed_new_worktree_runs_without_repo_tools(tmp_path: Path) -> None:
    """The installed skill script must be self-contained and not rely on repo tools/."""
    installed_scripts = REPO_ROOT / "skills" / "using-git-worktrees" / "scripts"
    isolated = tmp_path / "installed-skill"
    shutil.copytree(installed_scripts, isolated)
    isolated_script = isolated / "new_worktree.py"
    result = subprocess.run(
        [sys.executable, str(isolated_script), "--help"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
    )
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
        [sys.executable, str(NEW_WORKTREE), "feature", "--apply", "--no-skill-refresh"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert worktree_root.is_dir()

    result = subprocess.run(
        [sys.executable, str(REMOVE_WORKTREE), "feature", "--apply"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert not worktree_root.exists()


def test_remove_worktree_discards_dirty_submodule_without_worktree_force(tmp_path: Path, monkeypatch) -> None:
    gitconfig = tmp_path / "gitconfig"
    gitconfig.write_text('[protocol "file"]\n\tallow = always\n', encoding="utf-8")
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", str(gitconfig))

    repo = _make_repo(tmp_path, "remove-submodule")
    submodule_remote = tmp_path / "remove-submodule-remote"
    submodule_remote.mkdir()
    subprocess.run(["git", "init"], cwd=submodule_remote, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@test"], cwd=submodule_remote, check=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=submodule_remote, check=True)
    (submodule_remote / "README.md").write_text("submodule\n", encoding="utf-8")
    subprocess.run(["git", "add", "README.md"], cwd=submodule_remote, check=True)
    subprocess.run(["git", "commit", "-m", "init submodule"], cwd=submodule_remote, check=True)
    subprocess.run(
        ["git", "submodule", "add", submodule_remote.as_uri(), ".agents/plugins/marketplace-source"],
        cwd=repo,
        env=_stripped_env(),
        check=True,
        capture_output=True,
    )
    subprocess.run(["git", "add", "-A"], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-m", "add submodule"], cwd=repo, check=True)
    worktree_root = tmp_path / "_agent-worktrees" / "remove-submodule" / "feature"
    result = subprocess.run(
        [sys.executable, str(NEW_WORKTREE), "feature", "--apply", "--no-skill-refresh"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    subprocess.run(
        ["git", "submodule", "update", "--init", "--recursive"],
        cwd=worktree_root,
        env=_stripped_env(),
        check=True,
        capture_output=True,
    )
    submodule = worktree_root / ".agents" / "plugins" / "marketplace-source"
    (submodule / "consumer-residue.txt").write_text("discard me\n", encoding="utf-8")

    result = subprocess.run(
        [sys.executable, str(REMOVE_WORKTREE), "feature", "--apply"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    assert not worktree_root.exists()


def test_remove_worktree_preserves_dirty_consumer_files_without_force(tmp_path: Path) -> None:
    repo = _make_repo(tmp_path, "dirty-consumer-repo")
    worktree_root = tmp_path / "_agent-worktrees" / "dirty-consumer-repo" / "feature"
    result = subprocess.run(
        [sys.executable, str(NEW_WORKTREE), "feature", "--apply", "--no-skill-refresh"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    (worktree_root / "consumer-work.txt").write_text("keep me\n", encoding="utf-8")

    result = subprocess.run(
        [sys.executable, str(REMOVE_WORKTREE), "feature", "--apply"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0
    assert worktree_root.is_dir()
    assert (worktree_root / "consumer-work.txt").read_text(encoding="utf-8") == "keep me\n"


def test_new_worktree_base_ref(tmp_path: Path) -> None:
    repo = _make_repo(tmp_path, "base-ref-repo")
    marker = "base-marker.txt"
    (repo / marker).write_text("from-base", encoding="utf-8")
    subprocess.run(["git", "add", "-A"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "base"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "tag", "v1-base"], cwd=repo, check=True, capture_output=True)

    worktree_root = tmp_path / "_agent-worktrees" / "base-ref-repo" / "feature"
    result = subprocess.run(
        [sys.executable, str(NEW_WORKTREE), "feature", "--apply", "--base-ref", "v1-base", "--no-skill-refresh"],
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
        [sys.executable, str(NEW_WORKTREE), "feature", "--apply", "--no-skill-refresh"],
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

    # Ensure the new branch does not silently track origin/main as its upstream.
    tracking = subprocess.run(
        ["git", "config", "--get", "branch.feature.remote"],
        cwd=worktree_root,
        capture_output=True,
    )
    assert tracking.returncode != 0, "new feature branch should not track a remote"


def test_remove_worktree_resolves_by_full_ref_and_directory(tmp_path: Path) -> None:
    repo = _make_repo(tmp_path, "resolve-repo")

    # Full ref match
    worktree_full = tmp_path / "_agent-worktrees" / "resolve-repo" / "feature-full"
    result = subprocess.run(
        [sys.executable, str(NEW_WORKTREE), "feature-full", "--apply", "--no-skill-refresh"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert worktree_full.is_dir()

    result = subprocess.run(
        [sys.executable, str(REMOVE_WORKTREE), "refs/heads/feature-full", "--apply"],
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
        [sys.executable, str(NEW_WORKTREE), "feature-dir", "--apply", "--no-skill-refresh"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert worktree_dir.is_dir()

    result = subprocess.run(
        [sys.executable, str(REMOVE_WORKTREE), "feature-dir", "--apply"],
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
        [sys.executable, str(NEW_WORKTREE), "feature", "--apply", "--no-skill-refresh"],
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
        [sys.executable, str(NEW_WORKTREE), "feature", "--apply", "--no-skill-refresh"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "directory" in result.stderr.lower()


def test_new_worktree_preserves_native_plugin_config_and_local_skills(tmp_path: Path) -> None:
    repo = _make_repo(tmp_path, "repo-plugin-repo")
    marketplace = repo / ".agents/plugins/marketplace.json"
    marketplace.parent.mkdir(parents=True)
    marketplace.write_text(
        json.dumps(
            {
                "name": "repo-plugin-repo",
                "plugins": [
                    {
                        "name": "architecture-pack",
                        "source": {
                            "source": "git-subdir",
                            "url": "https://github.com/example/marketplace.git",
                            "path": "./dist/plugins/architecture-pack",
                            "ref": "main",
                        },
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    codex = repo / ".codex/config.toml"
    codex.parent.mkdir(parents=True)
    codex.write_text('[plugins."architecture-pack@repo-plugin-repo"]\nenabled = true\n', encoding="utf-8")
    local_skill = repo / ".agents/skills/local-domain/SKILL.md"
    local_skill.parent.mkdir(parents=True)
    local_skill.write_text("---\nname: local-domain\ndescription: local\n---\n", encoding="utf-8")
    subprocess.run(["git", "add", "-A"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "declare repo plugin"], cwd=repo, check=True, capture_output=True)

    worktree_root = tmp_path / "_agent-worktrees" / "repo-plugin-repo" / "feature"
    result = subprocess.run(
        [sys.executable, str(NEW_WORKTREE), "feature", "--apply"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    assert (worktree_root / ".agents/plugins/marketplace.json").is_file()
    assert (worktree_root / ".codex/config.toml").is_file()
    assert (worktree_root / ".agents/skills/local-domain/SKILL.md").is_file()
    assert not (worktree_root / ".agents/skills/architecture-pack").exists()


def test_new_worktree_initializes_generic_submodule_without_skill_projection(tmp_path: Path, monkeypatch) -> None:
    gitconfig = tmp_path / "gitconfig"
    gitconfig.write_text('[protocol "file"]\n\tallow = always\n', encoding="utf-8")
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", str(gitconfig))

    repo = _make_repo_with_marketplace_source_submodule(tmp_path, "sub")
    worktree_root = tmp_path / "_agent-worktrees" / "sub" / "feature"
    result = subprocess.run(
        [sys.executable, str(NEW_WORKTREE), "feature", "--apply"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    assert (worktree_root / "vendor/dependency/payload.txt").read_text(encoding="utf-8") == "consumer-pinned content\\n"
    assert not (worktree_root / ".agents/skills").exists()
    assert "Worktree ready" in result.stdout


def test_new_worktree_from_linked_worktree_succeeds_without_flag(tmp_path: Path) -> None:
    """new_worktree can be invoked from a linked worktree without --allow-shared-checkout."""
    repo = _make_repo_with_bundled_refresh(tmp_path, "linked-src-repo")
    linked_root = tmp_path / "_agent-worktrees" / "linked-src-repo" / "linked"
    subprocess.run(
        ["git", "worktree", "add", str(linked_root), "-b", "linked"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        check=True,
    )
    target_root = tmp_path / "_agent-worktrees" / "linked-src-repo" / "target"
    result = subprocess.run(
        [sys.executable, str(NEW_WORKTREE), "target", "--apply"],
        cwd=linked_root,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert target_root.is_dir()
    assert "Worktree ready" in result.stdout


def test_new_worktree_from_main_succeeds_without_flag(tmp_path: Path) -> None:
    """new_worktree does not require --allow-shared-checkout even from the main checkout."""
    repo = _make_repo_with_bundled_refresh(tmp_path, "main-non-tty-repo")
    target_root = tmp_path / "_agent-worktrees" / "main-non-tty-repo" / "feature"
    # stdin is not a TTY because capture_output=True and no stdin is piped.
    result = subprocess.run(
        [sys.executable, str(NEW_WORKTREE), "feature", "--apply"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert target_root.is_dir()
    assert "Worktree ready" in result.stdout


def test_remove_worktree_resolves_branch_namespace(tmp_path: Path) -> None:
    repo = _make_repo(tmp_path, "namespace-repo")

    team_root = tmp_path / "_agent-worktrees" / "namespace-repo" / "team" / "feature"
    result = subprocess.run(
        [sys.executable, str(NEW_WORKTREE), "team/feature", "--apply", "--no-skill-refresh"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert team_root.is_dir()

    personal_root = tmp_path / "_agent-worktrees" / "namespace-repo" / "personal" / "feature"
    result = subprocess.run(
        [sys.executable, str(NEW_WORKTREE), "personal/feature", "--apply", "--no-skill-refresh"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert personal_root.is_dir()

    # Resolve by full ref
    result = subprocess.run(
        [sys.executable, str(REMOVE_WORKTREE), "refs/heads/team/feature", "--apply"],
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
        [sys.executable, str(REMOVE_WORKTREE), "feature", "--apply"],
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
        combined = (result.stdout + result.stderr).lower()
        assert any(word in combined for word in ["canonical", "outside", "invalid branch"]), branch


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
    assert any(word in (result.stdout + result.stderr).lower() for word in ["canonical", "outside", "invalid branch"])


def test_remove_worktree_rejects_ambiguous_leaf(tmp_path: Path) -> None:
    repo = _make_repo(tmp_path, "ambiguous-repo")

    team_root = tmp_path / "_agent-worktrees" / "ambiguous-repo" / "team" / "feature"
    subprocess.run(
        [sys.executable, str(NEW_WORKTREE), "team/feature", "--apply", "--no-skill-refresh"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        check=True,
    )
    assert team_root.is_dir()

    personal_root = tmp_path / "_agent-worktrees" / "ambiguous-repo" / "personal" / "feature"
    subprocess.run(
        [sys.executable, str(NEW_WORKTREE), "personal/feature", "--apply", "--no-skill-refresh"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        check=True,
    )
    assert personal_root.is_dir()

    result = subprocess.run(
        [sys.executable, str(REMOVE_WORKTREE), "feature", "--apply"],
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
        [sys.executable, str(REMOVE_WORKTREE), str(outside), "--apply"],
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
        [sys.executable, str(NEW_WORKTREE), "refs/heads/feature", "--apply", "--no-skill-refresh"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert worktree_root.is_dir()


def _make_repo_with_command_bus(tmp_path: Path, name: str, bus_content: str) -> Path:
    """Create a repo that bundles the worker-pack skills and a custom tools/run.py."""
    repo = _make_repo_with_bundled_refresh(tmp_path, name)
    tools = repo / "tools"
    tools.mkdir(parents=True, exist_ok=True)
    (tools / "run.py").write_text(bus_content, encoding="utf-8")
    subprocess.run(["git", "add", "-A"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "add command bus"], cwd=repo, check=True, capture_output=True)
    return repo


_OK_BUS = """\
import sys
from pathlib import Path

def main():
    if len(sys.argv) < 2:
        print("usage: tools/run.py <capability>", file=sys.stderr)
        return 2
    capability = sys.argv[1]
    markers = {
        "install-deps": "install-deps-bus-marker.txt",
    }
    if capability not in markers:
        print(f"invalid choice: {capability}", file=sys.stderr)
        return 2
    (Path.cwd() / markers[capability]).write_text(f"{capability} called", encoding="utf-8")
    return 0

if __name__ == "__main__":
    sys.exit(main())
"""


def test_new_worktree_dispatches_through_command_bus_when_present(tmp_path: Path) -> None:
    repo = _make_repo_with_command_bus(tmp_path, "bus-repo", _OK_BUS)
    worktree_root = tmp_path / "_agent-worktrees" / "bus-repo" / "feature"
    result = subprocess.run(
        [sys.executable, str(NEW_WORKTREE), "feature", "--apply"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert worktree_root.is_dir()
    assert (worktree_root / "install-deps-bus-marker.txt").is_file()
    assert not (worktree_root / ".agents/skills").exists()


def test_new_worktree_fails_and_keeps_worktree_when_dependency_command_fails(tmp_path: Path) -> None:
    failing_bus = """\
import sys
print("repo-owned install-deps failed", file=sys.stderr)
sys.exit(1)
"""
    repo = _make_repo_with_command_bus(tmp_path, "fail-bus-repo", failing_bus)
    worktree_root = tmp_path / "_agent-worktrees" / "fail-bus-repo" / "feature"
    result = subprocess.run(
        [sys.executable, str(NEW_WORKTREE), "feature", "--apply"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0, result.stdout
    assert worktree_root.is_dir()
    assert "repo-owned install-deps failed" in result.stderr


def test_new_worktree_falls_back_to_bundled_for_unknown_bus_capability(tmp_path: Path) -> None:
    partial_bus = """\
import sys
print(f"invalid choice: {sys.argv[1]}", file=sys.stderr)
sys.exit(2)
"""
    repo = _make_repo_with_command_bus(tmp_path, "partial-bus-repo", partial_bus)
    worktree_root = tmp_path / "_agent-worktrees" / "partial-bus-repo" / "feature"
    result = subprocess.run(
        [sys.executable, str(NEW_WORKTREE), "feature", "--apply"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert worktree_root.is_dir()
    assert "Worktree ready" in result.stdout
    assert not (worktree_root / ".agents/skills").exists()


@pytest.mark.skipif(shutil.which("bash") is None, reason="bash not available")
def test_new_worktree_dispatches_through_bash_shell_wrapper(tmp_path: Path) -> None:
    """A repo that only ships a tools/run bash wrapper can still own capabilities."""
    repo = _make_repo_with_bundled_refresh(tmp_path, "bash-bus-repo")
    tools = repo / "tools"
    tools.mkdir(parents=True, exist_ok=True)
    bus = tools / "run"
    bus.write_text(
        "#!/usr/bin/env bash\n"
        "set -euo pipefail\n"
        'capability="$1"\n'
        'case "$capability" in\n'
        '  install-deps) echo "install-deps called" > install-deps-marker.txt ;;\n'
        '  *) echo "invalid choice: $capability" >&2; exit 2 ;;\n'
        "esac\n",
        encoding="utf-8",
        newline="\n",
    )
    bus.chmod(0o755)
    subprocess.run(["git", "add", "-A"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "add bash bus"], cwd=repo, check=True, capture_output=True)

    worktree_root = tmp_path / "_agent-worktrees" / "bash-bus-repo" / "feature"
    result = subprocess.run(
        [sys.executable, str(NEW_WORKTREE), "feature", "--apply"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert worktree_root.is_dir()
    assert (worktree_root / "install-deps-marker.txt").is_file()
    assert not (worktree_root / ".agents/skills").exists()


def _make_fake_package_manager(bin_dir: Path, name: str) -> None:
    """Create a fake package manager that records its arguments in the cwd."""
    if sys.platform == "win32":
        (bin_dir / f"{name}.cmd").write_text(f"@echo off\necho %* > {name}-calls.txt\n", encoding="utf-8")
    else:
        wrapper = bin_dir / name
        wrapper.write_text(f'#!/bin/sh\necho "$@" > {name}-calls.txt\n', encoding="utf-8")
        wrapper.chmod(0o755)


@pytest.mark.parametrize(
    "manifest, manager, expected",
    [
        ("package-lock.json", "npm", "ci"),
        ("package.json", "npm", "install"),
        ("yarn.lock", "yarn", "install"),
        ("pnpm-lock.yaml", "pnpm", "install"),
    ],
)
def test_new_worktree_installs_dependencies_from_manifest(
    tmp_path: Path,
    manifest: str,
    manager: str,
    expected: str,
) -> None:
    """The bundled default picks the right installer for the manifest it sees."""
    repo = _make_repo_with_bundled_refresh(tmp_path, f"{manager}-repo")
    (repo / manifest).write_text("", encoding="utf-8")
    subprocess.run(["git", "add", "-A"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", f"add {manifest}"], cwd=repo, check=True, capture_output=True)

    # Provide fake package managers on a temporary PATH so the test does not require network.
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    for tool in ("npm", "yarn", "pnpm"):
        _make_fake_package_manager(bin_dir, tool)

    env = _stripped_env()
    env["PATH"] = str(bin_dir) + os.pathsep + env.get("PATH", "")

    worktree_root = tmp_path / "_agent-worktrees" / f"{manager}-repo" / "feature"
    result = subprocess.run(
        [sys.executable, str(NEW_WORKTREE), "feature", "--apply"],
        cwd=repo,
        env=env,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert worktree_root.is_dir()
    assert (worktree_root / f"{manager}-calls.txt").is_file()
    assert expected in (worktree_root / f"{manager}-calls.txt").read_text(encoding="utf-8")


def test_new_worktree_fails_when_manifest_has_no_installer(tmp_path: Path) -> None:
    """A manifest without its required package manager returns failure but keeps the worktree."""
    repo = _make_repo_with_bundled_refresh(tmp_path, "missing-npm-repo")
    (repo / "package-lock.json").write_text('{"lockfileVersion": 1}', encoding="utf-8")
    subprocess.run(["git", "add", "-A"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "add package-lock"], cwd=repo, check=True, capture_output=True)

    # Restrict PATH to git only so npm is not found.
    git_path = shutil.which("git")
    assert git_path is not None
    env = _stripped_env()
    env["PATH"] = str(Path(git_path).parent)

    worktree_root = tmp_path / "_agent-worktrees" / "missing-npm-repo" / "feature"
    result = subprocess.run(
        [sys.executable, str(NEW_WORKTREE), "feature", "--apply"],
        cwd=repo,
        env=env,
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0, result.stdout
    assert worktree_root.is_dir()
    assert "npm is not available" in result.stderr


def test_new_worktree_installs_dependencies_with_no_skill_refresh(tmp_path: Path) -> None:
    """Dependency installation runs even when --no-skill-refresh is passed."""
    repo = _make_repo_with_bundled_refresh(tmp_path, "no-skill-refresh-repo")
    (repo / "package.json").write_text('{"name": "no-skill-refresh-repo"}', encoding="utf-8")
    subprocess.run(["git", "add", "-A"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "add package.json"], cwd=repo, check=True, capture_output=True)

    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    _make_fake_package_manager(bin_dir, "npm")

    env = _stripped_env()
    env["PATH"] = str(bin_dir) + os.pathsep + env.get("PATH", "")

    worktree_root = tmp_path / "_agent-worktrees" / "no-skill-refresh-repo" / "feature"
    result = subprocess.run(
        [sys.executable, str(NEW_WORKTREE), "feature", "--apply", "--no-skill-refresh"],
        cwd=repo,
        env=env,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert worktree_root.is_dir()
    assert (worktree_root / "npm-calls.txt").is_file()
    assert "install" in (worktree_root / "npm-calls.txt").read_text(encoding="utf-8")
    assert "Installed skill" not in result.stdout


def test_new_worktree_installs_node_and_python_dependencies(tmp_path: Path) -> None:
    """Mixed-language worktrees install all recognised dependency sets."""
    repo = _make_repo_with_bundled_refresh(tmp_path, "mixed-repo")
    (repo / "package.json").write_text('{"name": "mixed-repo"}', encoding="utf-8")
    (repo / "requirements.txt").write_text("requests", encoding="utf-8")
    subprocess.run(["git", "add", "-A"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "add manifests"], cwd=repo, check=True, capture_output=True)

    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    for tool in ("npm", "pip"):
        _make_fake_package_manager(bin_dir, tool)

    env = _stripped_env()
    env["PATH"] = str(bin_dir) + os.pathsep + env.get("PATH", "")

    worktree_root = tmp_path / "_agent-worktrees" / "mixed-repo" / "feature"
    result = subprocess.run(
        [sys.executable, str(NEW_WORKTREE), "feature", "--apply"],
        cwd=repo,
        env=env,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert worktree_root.is_dir()
    assert (worktree_root / "npm-calls.txt").is_file()
    assert (worktree_root / "pip-calls.txt").is_file()
    assert "install" in (worktree_root / "npm-calls.txt").read_text(encoding="utf-8")
    assert "install" in (worktree_root / "pip-calls.txt").read_text(encoding="utf-8")


def test_new_worktree_installs_poetry_dependencies(tmp_path: Path) -> None:
    """A Poetry project gets `poetry install` when pyproject.toml is present."""
    repo = _make_repo_with_bundled_refresh(tmp_path, "poetry-repo")
    (repo / "pyproject.toml").write_text(
        "[tool.poetry]\nname = 'poetry-repo'\nversion = '0.0.1'\n",
        encoding="utf-8",
    )
    subprocess.run(["git", "add", "-A"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "add pyproject"], cwd=repo, check=True, capture_output=True)

    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    _make_fake_package_manager(bin_dir, "poetry")

    env = _stripped_env()
    env["PATH"] = str(bin_dir) + os.pathsep + env.get("PATH", "")

    worktree_root = tmp_path / "_agent-worktrees" / "poetry-repo" / "feature"
    result = subprocess.run(
        [sys.executable, str(NEW_WORKTREE), "feature", "--apply"],
        cwd=repo,
        env=env,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert worktree_root.is_dir()
    assert (worktree_root / "poetry-calls.txt").is_file()
    assert "install" in (worktree_root / "poetry-calls.txt").read_text(encoding="utf-8")


def test_new_worktree_keeps_worktree_when_pip_fails(tmp_path: Path) -> None:
    """A pip install failure should not delete the worktree; pip is global and can be blocked."""
    repo = _make_repo_with_bundled_refresh(tmp_path, "pip-warn-repo")
    (repo / "package.json").write_text('{"name": "pip-warn-repo"}', encoding="utf-8")
    (repo / "requirements.txt").write_text("requests", encoding="utf-8")
    subprocess.run(["git", "add", "-A"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "add manifests"], cwd=repo, check=True, capture_output=True)

    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    _make_fake_package_manager(bin_dir, "npm")
    if sys.platform == "win32":
        (bin_dir / "pip.cmd").write_text("@echo off\necho %* > pip-calls.txt\nexit /b 1\n", encoding="utf-8")
    else:
        (bin_dir / "pip").write_text('#!/bin/sh\necho "$@" > pip-calls.txt\nexit 1\n', encoding="utf-8")
        (bin_dir / "pip").chmod(0o755)

    env = _stripped_env()
    env["PATH"] = str(bin_dir) + os.pathsep + env.get("PATH", "")

    worktree_root = tmp_path / "_agent-worktrees" / "pip-warn-repo" / "feature"
    result = subprocess.run(
        [sys.executable, str(NEW_WORKTREE), "feature", "--apply"],
        cwd=repo,
        env=env,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert worktree_root.is_dir()
    assert (worktree_root / "npm-calls.txt").is_file()
    assert (worktree_root / "pip-calls.txt").is_file()
    assert "pip install failed" in result.stderr


def test_new_worktree_keeps_worktree_when_npm_fails(tmp_path: Path) -> None:
    """A failing Node installer keeps the worktree for the agent to inspect."""
    repo = _make_repo_with_bundled_refresh(tmp_path, "npm-fail-repo")
    (repo / "package.json").write_text('{"name": "npm-fail-repo"}', encoding="utf-8")
    subprocess.run(["git", "add", "-A"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "add package.json"], cwd=repo, check=True, capture_output=True)

    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    if sys.platform == "win32":
        (bin_dir / "npm.cmd").write_text("@echo off\necho %* > npm-calls.txt\nexit /b 1\n", encoding="utf-8")
    else:
        (bin_dir / "npm").write_text('#!/bin/sh\necho "$@" > npm-calls.txt\nexit 1\n', encoding="utf-8")
        (bin_dir / "npm").chmod(0o755)

    env = _stripped_env()
    env["PATH"] = str(bin_dir) + os.pathsep + env.get("PATH", "")

    worktree_root = tmp_path / "_agent-worktrees" / "npm-fail-repo" / "feature"
    result = subprocess.run(
        [sys.executable, str(NEW_WORKTREE), "feature", "--apply"],
        cwd=repo,
        env=env,
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0, result.stdout
    assert worktree_root.is_dir()


def test_new_worktree_keeps_worktree_when_pip_is_missing(tmp_path: Path) -> None:
    """A missing pip executable should not delete the worktree."""
    repo = _make_repo_with_bundled_refresh(tmp_path, "missing-pip-repo")
    (repo / "requirements.txt").write_text("requests", encoding="utf-8")
    subprocess.run(["git", "add", "-A"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "add requirements"], cwd=repo, check=True, capture_output=True)

    # Restrict PATH to a git-only directory so pip is not found.
    git_path = shutil.which("git")
    assert git_path is not None
    env = _stripped_env()
    if os.name == "nt":
        env["PATH"] = str(Path(git_path).parent)
    else:
        git_only = tmp_path / "git-only-bin"
        git_only.mkdir()
        git_shim = git_only / "git"
        git_shim.write_text(f'#!/bin/sh\nexec "{git_path}" "$@"\n', encoding="utf-8")
        git_shim.chmod(0o755)
        env["PATH"] = str(git_only)

    worktree_root = tmp_path / "_agent-worktrees" / "missing-pip-repo" / "feature"
    result = subprocess.run(
        [sys.executable, str(NEW_WORKTREE), "feature", "--apply"],
        cwd=repo,
        env=env,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert worktree_root.is_dir()
    assert "pip is not on PATH" in result.stderr


@pytest.mark.skipif(os.name != "nt", reason="process working directories do not lock worktrees on POSIX")
def test_remove_worktree_stops_on_locked_directory(tmp_path: Path) -> None:
    """If the worktree directory is locked, the script deregisters it and stops."""
    repo = _make_repo(tmp_path, "locked-repo")
    worktree_root = tmp_path / "_agent-worktrees" / "locked-repo" / "feature"
    result = subprocess.run(
        [sys.executable, str(NEW_WORKTREE), "feature", "--apply", "--no-skill-refresh"],
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
            [sys.executable, str(REMOVE_WORKTREE), "feature", "--apply"],
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
