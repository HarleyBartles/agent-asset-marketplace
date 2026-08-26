import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
CORE = (
    REPO_ROOT
    / "codex-marketplace"
    / "plugins"
    / "repo-worker-pack"
    / "skills"
    / "generating-agent-mesh"
    / "scripts"
    / "validate_agent_mesh.py"
)
GENERATE_CORE = (
    REPO_ROOT
    / "codex-marketplace"
    / "plugins"
    / "repo-worker-pack"
    / "skills"
    / "generating-agent-mesh"
    / "scripts"
    / "generate_index_mesh.py"
)


def _stripped_env():
    env = os.environ.copy()
    env.pop("GIT_DIR", None)
    env.pop("GIT_WORK_TREE", None)
    env.pop("GIT_INDEX_FILE", None)
    return env


def test_source_repo_agent_mesh_passes() -> None:
    """The current checkout's agent mesh is valid."""
    result = subprocess.run(
        [sys.executable, str(CORE), "--check"],
        cwd=REPO_ROOT,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert "OK agent mesh" in result.stdout


def _make_repo(tmp_path: Path, name: str) -> Path:
    repo = tmp_path / name
    repo.mkdir()
    subprocess.run(["git", "init"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@test"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=repo, check=True, capture_output=True)
    return repo


def _commit_file(repo: Path, rel_path: str, content: str = "content\n") -> None:
    path = repo / rel_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")
    subprocess.run(["git", "add", "-A"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", f"add {rel_path}"], cwd=repo, check=True, capture_output=True)


def _hook_ext() -> str:
    return ".ps1" if sys.platform == "win32" else ".sh"


def test_broken_markdown_link_fails(tmp_path: Path) -> None:
    """A repo with a broken local link in an INDEX.md fails validation."""
    repo = tmp_path / "broken-link-repo"
    repo.mkdir()
    subprocess.run(["git", "init"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@test"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=repo, check=True, capture_output=True)

    (repo / "INDEX.md").write_text(
        "# Test\n[broken](./missing.md)\n",
        encoding="utf-8",
        newline="\n",
    )
    subprocess.run(["git", "add", "-A"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "init"], cwd=repo, check=True, capture_output=True)

    result = subprocess.run(
        [sys.executable, str(CORE), "--check"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "broken link" in result.stderr.lower()


def test_validate_agent_mesh_extra_hook_reports_drift(tmp_path: Path) -> None:
    """A repo-specific extra hook can report drift via DRIFT: lines."""
    repo = _make_repo(tmp_path, "agent-mesh-hook-repo")
    _commit_file(repo, "INDEX.md", "# Test\n")
    scripts_path = repo / "scripts"
    scripts_path.mkdir()
    hook = scripts_path / f"validate_agent_mesh_extra{_hook_ext()}"

    if sys.platform == "win32":
        hook.write_text(
            "param([switch]$Check, [string]$ChangedFrom)\n"
            "Write-Output \"DRIFT: custom drift\"\n",
            encoding="utf-8",
        )
    else:
        hook.write_text(
            "#!/usr/bin/env bash\n"
            "if [ \"$1\" = \"--check\" ]; then shift; fi\n"
            'echo "DRIFT: custom drift"\n',
            encoding="utf-8",
        )
        hook.chmod(0o755)

    result = subprocess.run(
        [sys.executable, str(CORE), "--check"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "custom drift" in result.stderr


def test_validate_agent_mesh_extra_hook_failure_fails(tmp_path: Path) -> None:
    """A non-zero exit from the extra hook is reported as a finding."""
    repo = _make_repo(tmp_path, "agent-mesh-fail-hook-repo")
    _commit_file(repo, "INDEX.md", "# Test\n")
    scripts_path = repo / "scripts"
    scripts_path.mkdir()
    hook = scripts_path / f"validate_agent_mesh_extra{_hook_ext()}"

    if sys.platform == "win32":
        hook.write_text(
            "param([switch]$Check, [string]$ChangedFrom)\n"
            "Write-Output 'broken hook'\n"
            "exit 1\n",
            encoding="utf-8",
        )
    else:
        hook.write_text(
            "#!/usr/bin/env bash\n"
            "echo 'broken hook'\n"
            "exit 1\n",
            encoding="utf-8",
        )
        hook.chmod(0o755)

    result = subprocess.run(
        [sys.executable, str(CORE), "--check"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "broken hook" in (result.stdout + result.stderr).lower()


def test_validate_agent_mesh_extra_hook_receives_changed_from(tmp_path: Path) -> None:
    """The extra hook receives --changed-from when the flag is passed."""
    repo = _make_repo(tmp_path, "agent-mesh-changed-from-repo")
    _commit_file(repo, "INDEX.md", "# Test\n")
    _commit_file(repo, "another.md", "# Another\n")
    scripts_path = repo / "scripts"
    scripts_path.mkdir()
    hook = scripts_path / f"validate_agent_mesh_extra{_hook_ext()}"

    if sys.platform == "win32":
        hook.write_text(
            "param([switch]$Check, [string]$ChangedFrom)\n"
            'Write-Output "DRIFT: saw changed-from $ChangedFrom"\n',
            encoding="utf-8",
        )
    else:
        hook.write_text(
            "#!/usr/bin/env bash\n"
            "if [ \"$1\" = \"--check\" ]; then shift; fi\n"
            'if [ "$1" = "--changed-from" ]; then\n'
            '  echo "DRIFT: saw changed-from $2"\n'
            "else\n"
            '  echo "DRIFT: missing changed-from"\n'
            "fi\n",
            encoding="utf-8",
        )
        hook.chmod(0o755)

    result = subprocess.run(
        [sys.executable, str(CORE), "--check", "--changed-from", "HEAD~1"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "saw changed-from" in result.stderr


def test_agent_mesh_passes_for_encoded_ambiguous_links(tmp_path: Path) -> None:
    """Generated links to files with markdown-ambiguous names validate."""
    repo = _make_repo(tmp_path, "encoded-link-repo")
    _commit_file(repo, "2. Choosing an Identity (Handle + Persona Creation).md")
    _commit_file(repo, "Ku - Sample Tweets (Reconstructed).md")
    _commit_file(repo, "Style Guides/overview.md")

    generate = subprocess.run(
        [sys.executable, str(GENERATE_CORE), "--apply", "--allow-shared-checkout"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert generate.returncode == 0, generate.stderr

    result = subprocess.run(
        [sys.executable, str(CORE), "--check"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert "OK agent mesh" in result.stdout
