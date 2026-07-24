# Worktree helpers, refresh skills, and generate mesh — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement the two `refreshing-installed-skills` and `generating-index-mesh` first-party skills, ship bundled `new-worktree`/`remove-worktree` scripts through the `using-git-worktrees` Codex overlay, register the skills in `repo-worker-pack`, and regenerate marketplace surfaces.

**Architecture:** Two small Python cores (`refresh_installed_skills.py`, `generate_index_mesh.py`) discover the repo's existing install/index commands and run them. The `using-git-worktrees` overlay injects `new_worktree.py` and `remove_worktree.py`; `new-worktree` auto-runs `refreshing-installed-skills` after worktree creation. Both skills are registered in `repo-worker-pack` and picked up by `house-skills`.

**Tech stack:** Python 3.12, Bash/PowerShell wrappers, pytest, `tools/rebuild_marketplace.py`, `tools/check_marketplace.py`.

## Global Constraints

- All Python source uses `from __future__ import annotations` and `pathlib.Path`.
- Scripts must run on Windows and Unix. Python wrappers call the core with `py -3` on Windows and `python3` on Unix; the `.ps1`/`.sh` wrappers handle that distinction.
- Do not add third-party dependencies. The source repo has no `requirements.txt`; the consumer repos keep their own.
- Do not hand-edit derived marketplace surfaces (`codex-marketplace/plugins/*`, `generated/skill-zips/*`, `repo-index/*`). Regenerate with `tools/rebuild_marketplace.py`.
- Do not edit third-party source (`sources/third_party/**`). Use the `adapters/codex/superpowers-plus/using-git-worktrees` overlay for `using-git-worktrees` changes.
- First-party skill frontmatter must keep the metadata fields the repo normalizer expects: `name`, `description`, `metadata` (with `source-id`, `source-path`, `provenance-name`, `source-category`, `status`, `owner`, `scope`, `use_when`, `do_not_use_when`, `related_skills`), and `license`.
- Every task that changes code ends with a commit.

---

### Task 1: Remove stale artifacts from the old per-repo plan

**Files:**
- Delete: `.agents/superpowers/plans/2026-07-24-add-worktree-scripts-and-overlay.md` (untracked)
- Delete: `tests/test_worktree_scripts.py` (committed; will be replaced in Task 6)

**Steps:**
- [ ] Run `git status --short` to confirm the old plan is untracked and the stale test is tracked.
- [ ] Delete the stale files:
  ```powershell
  Remove-Item -Path ".agents\superpowers\plans\2026-07-24-add-worktree-scripts-and-overlay.md"
  git rm tests/test_worktree_scripts.py
  ```
- [ ] Commit:
  ```
  git commit -m "chore: remove stale per-repo worktree plan and failing test"
  ```

**Expected interim state:** The untracked old plan and the stale failing test are gone. The remaining `tests/` directory has no `test_worktree_scripts.py` yet.

---

### Task 2: Create the `generating-index-mesh` first-party skill

**Files to create:**
- `sources/first_party/skills/generating-index-mesh/SKILL.md`
- `sources/first_party/skills/generating-index-mesh/agents/openai.yaml`
- `sources/first_party/skills/generating-index-mesh/scripts/generate_index_mesh.py`
- `sources/first_party/skills/generating-index-mesh/scripts/generate-index-mesh.sh`
- `sources/first_party/skills/generating-index-mesh/scripts/generate-index-mesh.ps1`

**Test file:** `tests/test_generate_index_mesh.py`

**Interfaces:**
- Produces: `generate_index_mesh.py` with `main(argv=None) -> int` and helper `find_mesh_command(repo_root: Path) -> list[str] | None`.
- Consumes: repo's existing `tools/generate_index_mesh.py` or `scripts/generate_index_mesh.py`.

**Step 1: Write the failing test**

Create `tests/test_generate_index_mesh.py`:

```python
import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
CORE = REPO_ROOT / "sources" / "first_party" / "skills" / "generating-index-mesh" / "scripts" / "generate_index_mesh.py"


def _make_source_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "source-repo"
    repo.mkdir()
    subprocess.run(["git", "init"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@test"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=repo, check=True, capture_output=True)
    (repo / "tools").mkdir()
    (repo / "tools" / "generate_index_mesh.py").write_text("print('mesh ok')\n", encoding="utf-8")
    return repo


def _make_consumer_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "consumer-repo"
    repo.mkdir()
    subprocess.run(["git", "init"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@test"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=repo, check=True, capture_output=True)
    (repo / "scripts").mkdir()
    (repo / "scripts" / "generate_index_mesh.py").write_text("print('mesh ok')\n", encoding="utf-8")
    return repo


def test_source_layout_finds_tools_command(tmp_path: Path) -> None:
    repo = _make_source_repo(tmp_path)
    env = os.environ.copy()
    env.pop("GIT_DIR", None)
    env.pop("GIT_WORK_TREE", None)
    env.pop("GIT_INDEX_FILE", None)
    result = subprocess.run([sys.executable, str(CORE)], cwd=repo, env=env, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert "mesh ok" in result.stdout


def test_consumer_layout_finds_scripts_command(tmp_path: Path) -> None:
    repo = _make_consumer_repo(tmp_path)
    env = os.environ.copy()
    env.pop("GIT_DIR", None)
    env.pop("GIT_WORK_TREE", None)
    env.pop("GIT_INDEX_FILE", None)
    result = subprocess.run([sys.executable, str(CORE)], cwd=repo, env=env, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert "mesh ok" in result.stdout


def test_missing_command_fails(tmp_path: Path) -> None:
    repo = tmp_path / "empty-repo"
    repo.mkdir()
    subprocess.run(["git", "init"], cwd=repo, check=True, capture_output=True)
    env = os.environ.copy()
    env.pop("GIT_DIR", None)
    env.pop("GIT_WORK_TREE", None)
    env.pop("GIT_INDEX_FILE", None)
    result = subprocess.run([sys.executable, str(CORE)], cwd=repo, env=env, capture_output=True, text=True)
    assert result.returncode != 0
    assert "generate_index_mesh" in result.stderr or "index mesh" in result.stderr
```

**Step 2: Run the failing test**

```powershell
py -3 -m pytest tests/test_generate_index_mesh.py -v
```

Expected: `ModuleNotFoundError` or file not found failures.

**Step 3: Implement the skill**

Create `sources/first_party/skills/generating-index-mesh/scripts/generate_index_mesh.py`:

```python
#!/usr/bin/env python3
"""Find and run the repo's generate_index_mesh.py command."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


def _stripped_env() -> dict[str, str]:
    env = os.environ.copy()
    env.pop("GIT_DIR", None)
    env.pop("GIT_WORK_TREE", None)
    env.pop("GIT_INDEX_FILE", None)
    return env


def _repo_root() -> Path:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
        check=True,
        env=_stripped_env(),
    )
    return Path(result.stdout.strip())


def _reject_submodule() -> None:
    result = subprocess.run(
        ["git", "rev-parse", "--show-superproject-working-tree"],
        capture_output=True,
        text=True,
        env=_stripped_env(),
    )
    if result.returncode == 0 and result.stdout.strip():
        raise RuntimeError("This script must not run inside a git submodule")


def _find_override(repo_root: Path) -> list[str] | None:
    for rel in [
        "scripts/generate-index-mesh.py",
        "scripts/generate-index-mesh.ps1",
        "scripts/generate-index-mesh.sh",
        "tools/generate-index-mesh.py",
        "tools/generate-index-mesh.ps1",
        "tools/generate-index-mesh.sh",
    ]:
        candidate = repo_root / rel
        if candidate.is_file():
            if rel.endswith(".py"):
                return [sys.executable, str(candidate)]
            if sys.platform == "win32" and rel.endswith(".ps1"):
                return ["pwsh", "-File", str(candidate)]
            if shutil.which("bash"):
                return ["bash", str(candidate)]
            raise RuntimeError(f"Found {candidate} but no interpreter available")
    return None


def _find_command(repo_root: Path) -> list[str] | None:
    for rel in ["tools/generate_index_mesh.py", "scripts/generate_index_mesh.py"]:
        candidate = repo_root / rel
        if candidate.is_file():
            return [sys.executable, str(candidate)]
    return None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the repo's index mesh generator")
    parser.add_argument("--check", action="store_true", help="validate without writing")
    args = parser.parse_args(argv)

    repo_root = _repo_root()
    _reject_submodule()

    command = _find_override(repo_root) or _find_command(repo_root)
    if command is None:
        print("error: no generate_index_mesh command found", file=sys.stderr)
        return 1

    if args.check:
        command = [*command, "--check"]

    result = subprocess.run(command, cwd=repo_root, env=_stripped_env())
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
```

Create `sources/first_party/skills/generating-index-mesh/scripts/generate-index-mesh.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "${SCRIPT_DIR}/generate_index_mesh.py" "$@"
```

Create `sources/first_party/skills/generating-index-mesh/scripts/generate-index-mesh.ps1`:

```powershell
$ErrorActionPreference = "Stop"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
& py -3 "$scriptDir\generate_index_mesh.py" @args
```

Create `sources/first_party/skills/generating-index-mesh/agents/openai.yaml`:

```yaml
version: 1
metadata:
  skill_name: generating-index-mesh
  source_category: first_party
interface:
  display_name: Generating Index Mesh
  short_description: Use when the repo-wide INDEX.md mesh is stale or as a CI/pre-commit gate.
  default_prompt: Use generating-index-mesh when the repo-wide INDEX.md mesh is stale or as a CI/pre-commit gate.
policy:
  allow_implicit_invocation: false
```

Create `sources/first_party/skills/generating-index-mesh/SKILL.md`:

```markdown
---
name: generating-index-mesh
description: Use when the repo-wide INDEX.md mesh is stale or as a CI/pre-commit gate.
metadata:
  source-id: generating-index-mesh
  source-path: sources/first_party/skills/generating-index-mesh/SKILL.md
  provenance-name: Generating Index Mesh first-party skill
  source-category: first_party
  status: active
  owner: Harley Bartles
  scope: Run the repository's generate_index_mesh.py command.
  use_when:
  - Use when INDEX.md files are stale after skill, plugin, or source changes.
  - Use as a CI or pre-commit gate to verify the navigation mesh.
  do_not_use_when:
  - Do not use when installing or refreshing skills from the plugin source.
  related_skills:
  - refreshing-installed-skills
license: MIT
---

# Generating Index Mesh

Run the repository's index mesh generator.

## When to Use

- After changing skill, plugin, or source files that affect generated `INDEX.md` navigation.
- In CI or as a pre-commit hook to verify the mesh is current.

## Usage

```bash
py -3 .agents/skills/generating-index-mesh/scripts/generate_index_mesh.py
py -3 .agents/skills/generating-index-mesh/scripts/generate_index_mesh.py --check
```

This skill discovers the repo's `tools/generate_index_mesh.py` (source repo) or `scripts/generate_index_mesh.py` (consumer repo) and runs it. It does not commit; the caller decides whether to commit the regenerated mesh.
```

**Step 4: Run the test**

```powershell
py -3 -m pytest tests/test_generate_index_mesh.py -v
```

Expected: all three tests pass.

**Step 5: Commit**

```
git add sources/first_party/skills/generating-index-mesh tests/test_generate_index_mesh.py
git commit -m "feat: add generating-index-mesh skill"
```

---

### Task 3: Create the `refreshing-installed-skills` first-party skill

**Files to create:**
- `sources/first_party/skills/refreshing-installed-skills/SKILL.md`
- `sources/first_party/skills/refreshing-installed-skills/agents/openai.yaml`
- `sources/first_party/skills/refreshing-installed-skills/scripts/refresh_installed_skills.py`
- `sources/first_party/skills/refreshing-installed-skills/scripts/refresh-installed-skills.sh`
- `sources/first_party/skills/refreshing-installed-skills/scripts/refresh-installed-skills.ps1`

**Test file:** `tests/test_refresh_installed_skills.py`

**Interfaces:**
- Produces: `refresh_installed_skills.py` with `main(argv=None) -> int`, helper `find_install_command(repo_root: Path) -> list[str] | None`, and `find_mesh_script(repo_root: Path) -> Path | None`.
- Consumes: repo's existing `tools/install_agent_skills.py` or `scripts/install_agent_skills.py`, and the `generating-index-mesh` skill core.

**Step 1: Write the failing test**

Create `tests/test_refresh_installed_skills.py`:

```python
import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
CORE = REPO_ROOT / "sources" / "first_party" / "skills" / "refreshing-installed-skills" / "scripts" / "refresh_installed_skills.py"


def _make_source_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "source-repo"
    repo.mkdir()
    subprocess.run(["git", "init"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@test"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=repo, check=True, capture_output=True)
    (repo / "codex-marketplace" / "plugins").mkdir(parents=True)
    (repo / "tools").mkdir()
    (repo / "tools" / "install_agent_skills.py").write_text(
        "import sys\nprint('install ok')\n", encoding="utf-8"
    )
    (repo / "tools" / "generate_index_mesh.py").write_text(
        "import sys\nprint('mesh ok')\n", encoding="utf-8"
    )
    (repo / ".agents" / "skills" / "generating-index-mesh" / "scripts" / "generate_index_mesh.py").write_text(
        "import sys\nprint('mesh ok')\n", encoding="utf-8"
    )
    return repo


def _make_consumer_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "consumer-repo"
    repo.mkdir()
    subprocess.run(["git", "init"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@test"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=repo, check=True, capture_output=True)
    (repo / "scripts").mkdir()
    (repo / "scripts" / "install_agent_skills.py").write_text(
        "import sys\nprint('install ok')\n", encoding="utf-8"
    )
    (repo / "scripts" / "generate_index_mesh.py").write_text(
        "import sys\nprint('mesh ok')\n", encoding="utf-8"
    )
    (repo / ".agents" / "skills" / "generating-index-mesh" / "scripts" / "generate_index_mesh.py").write_text(
        "import sys\nprint('mesh ok')\n", encoding="utf-8"
    )
    return repo


def test_source_layout_runs_tools_commands(tmp_path: Path) -> None:
    repo = _make_source_repo(tmp_path)
    env = os.environ.copy()
    env.pop("GIT_DIR", None)
    env.pop("GIT_WORK_TREE", None)
    env.pop("GIT_INDEX_FILE", None)
    result = subprocess.run([sys.executable, str(CORE), "--check"], cwd=repo, env=env, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert "install ok" in result.stdout
    assert "mesh ok" in result.stdout


def test_consumer_layout_runs_scripts_commands(tmp_path: Path) -> None:
    repo = _make_consumer_repo(tmp_path)
    env = os.environ.copy()
    env.pop("GIT_DIR", None)
    env.pop("GIT_WORK_TREE", None)
    env.pop("GIT_INDEX_FILE", None)
    result = subprocess.run([sys.executable, str(CORE), "--check"], cwd=repo, env=env, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert "install ok" in result.stdout
    assert "mesh ok" in result.stdout


def test_missing_install_command_fails(tmp_path: Path) -> None:
    repo = tmp_path / "empty-repo"
    repo.mkdir()
    subprocess.run(["git", "init"], cwd=repo, check=True, capture_output=True)
    env = os.environ.copy()
    env.pop("GIT_DIR", None)
    env.pop("GIT_WORK_TREE", None)
    env.pop("GIT_INDEX_FILE", None)
    result = subprocess.run([sys.executable, str(CORE), "--check"], cwd=repo, env=env, capture_output=True, text=True)
    assert result.returncode != 0
    assert "install_agent_skills" in result.stderr or "install skills" in result.stderr
```

**Step 2: Run the failing test**

```powershell
py -3 -m pytest tests/test_refresh_installed_skills.py -v
```

Expected: `ModuleNotFoundError` or file not found failures.

**Step 3: Implement the skill**

Create `sources/first_party/skills/refreshing-installed-skills/scripts/refresh_installed_skills.py`:

```python
#!/usr/bin/env python3
"""Refresh installed skills from the plugin source, then regenerate the index mesh."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


def _stripped_env() -> dict[str, str]:
    env = os.environ.copy()
    env.pop("GIT_DIR", None)
    env.pop("GIT_WORK_TREE", None)
    env.pop("GIT_INDEX_FILE", None)
    return env


def _repo_root() -> Path:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
        check=True,
        env=_stripped_env(),
    )
    return Path(result.stdout.strip())


def _reject_submodule() -> None:
    result = subprocess.run(
        ["git", "rev-parse", "--show-superproject-working-tree"],
        capture_output=True,
        text=True,
        env=_stripped_env(),
    )
    if result.returncode == 0 and result.stdout.strip():
        raise RuntimeError("This script must not run inside a git submodule")


def _init_marketplace_source(repo_root: Path) -> None:
    submodule = repo_root / ".agents" / "plugins" / "marketplace-source"
    if not (repo_root / ".gitmodules").is_file():
        return
    if not submodule.exists():
        return
    subprocess.run(
        ["git", "submodule", "update", "--init", "--recursive", str(submodule.relative_to(repo_root))],
        cwd=repo_root,
        env=_stripped_env(),
        check=True,
    )


def _find_override(repo_root: Path) -> list[str] | None:
    for rel in [
        "scripts/refresh-installed-skills.py",
        "scripts/refresh-installed-skills.ps1",
        "scripts/refresh-installed-skills.sh",
        "tools/refresh-installed-skills.py",
        "tools/refresh-installed-skills.ps1",
        "tools/refresh-installed-skills.sh",
    ]:
        candidate = repo_root / rel
        if candidate.is_file():
            if rel.endswith(".py"):
                return [sys.executable, str(candidate)]
            if sys.platform == "win32" and rel.endswith(".ps1"):
                return ["pwsh", "-File", str(candidate)]
            if shutil.which("bash"):
                return ["bash", str(candidate)]
            raise RuntimeError(f"Found {candidate} but no interpreter available")
    return None


def _find_install_command(repo_root: Path) -> list[str] | None:
    if (repo_root / "codex-marketplace" / "plugins").is_dir() and (repo_root / "tools" / "install_agent_skills.py").is_file():
        return [sys.executable, str(repo_root / "tools" / "install_agent_skills.py")]
    _init_marketplace_source(repo_root)
    if (repo_root / "scripts" / "install_agent_skills.py").is_file():
        return [sys.executable, str(repo_root / "scripts" / "install_agent_skills.py")]
    return None


def _find_mesh_script(repo_root: Path) -> Path | None:
    candidates = [
        repo_root / ".agents" / "skills" / "generating-index-mesh" / "scripts" / "generate_index_mesh.py",
    ]
    for pattern in [
        "codex-marketplace/plugins/*/skills/generating-index-mesh/scripts/generate_index_mesh.py",
        ".agents/plugins/marketplace-source/codex-marketplace/plugins/*/skills/generating-index-mesh/scripts/generate_index_mesh.py",
    ]:
        candidates.extend(sorted(repo_root.glob(pattern)))
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    return None


def _git_has_changes(repo_root: Path) -> bool:
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        env=_stripped_env(),
    )
    return bool(result.stdout.strip())


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Refresh installed skills and regenerate the index mesh")
    parser.add_argument("--check", action="store_true", help="validate without writing")
    args = parser.parse_args(argv)

    repo_root = _repo_root()
    _reject_submodule()

    override = _find_override(repo_root)
    if override:
        result = subprocess.run(override, cwd=repo_root, env=_stripped_env())
        return result.returncode

    install_cmd = _find_install_command(repo_root)
    if install_cmd is None:
        print("error: no install_agent_skills.py command found", file=sys.stderr)
        return 1

    install_run = install_cmd + (["--check"] if args.check else [])
    result = subprocess.run(install_run, cwd=repo_root, env=_stripped_env())
    if result.returncode != 0:
        return result.returncode

    mesh_script = _find_mesh_script(repo_root)
    if mesh_script is None:
        print("error: generating-index-mesh skill not found", file=sys.stderr)
        return 1
    mesh_cmd = [sys.executable, str(mesh_script)] + (["--check"] if args.check else [])
    result = subprocess.run(mesh_cmd, cwd=repo_root, env=_stripped_env())
    if result.returncode != 0:
        return result.returncode

    if not args.check and _git_has_changes(repo_root):
        subprocess.run(["git", "add", "-A"], cwd=repo_root, env=_stripped_env(), check=True)
        subprocess.run(
            ["git", "commit", "-m", "chore: refresh installed skills and regenerate index mesh"],
            cwd=repo_root,
            env=_stripped_env(),
            check=True,
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

Create `sources/first_party/skills/refreshing-installed-skills/scripts/refresh-installed-skills.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "${SCRIPT_DIR}/refresh_installed_skills.py" "$@"
```

Create `sources/first_party/skills/refreshing-installed-skills/scripts/refresh-installed-skills.ps1`:

```powershell
$ErrorActionPreference = "Stop"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
& py -3 "$scriptDir\refresh_installed_skills.py" @args
```

Create `sources/first_party/skills/refreshing-installed-skills/agents/openai.yaml`:

```yaml
version: 1
metadata:
  skill_name: refreshing-installed-skills
  source_category: first_party
interface:
  display_name: Refreshing Installed Skills
  short_description: Use when a worktree is initialized or .agents/skills/ is stale from the plugin source.
  default_prompt: Use refreshing-installed-skills when a worktree is initialized or .agents/skills/ is stale from the plugin source.
policy:
  allow_implicit_invocation: false
```

Create `sources/first_party/skills/refreshing-installed-skills/SKILL.md`:

```markdown
---
name: refreshing-installed-skills
description: Use when a worktree is initialized or .agents/skills/ is stale from the plugin source.
metadata:
  source-id: refreshing-installed-skills
  source-path: sources/first_party/skills/refreshing-installed-skills/SKILL.md
  provenance-name: Refreshing Installed Skills first-party skill
  source-category: first_party
  status: active
  owner: Harley Bartles
  scope: Install or refresh .agents/skills/ from the plugin source and regenerate the index mesh.
  use_when:
  - Use when creating a new worktree.
  - Use after updating the marketplace-source submodule.
  - Use when .agents/skills/ appears stale.
  do_not_use_when:
  - Do not use when only the INDEX.md mesh is stale without any skill changes; use generating-index-mesh instead.
  related_skills:
  - generating-index-mesh
  - using-git-worktrees
license: MIT
---

# Refreshing Installed Skills

Install or refresh `.agents/skills/` from the plugin source, then regenerate the index mesh.

## When to Use

- After creating a new worktree.
- After updating the `marketplace-source` submodule in a consumer repo.
- When `.agents/skills/` appears stale.

## Usage

```bash
py -3 .agents/skills/refreshing-installed-skills/scripts/refresh_installed_skills.py
py -3 .agents/skills/refreshing-installed-skills/scripts/refresh_installed_skills.py --check
```

This skill discovers the repo's `tools/install_agent_skills.py` (source repo) or `scripts/install_agent_skills.py` (consumer repo), runs it, then runs `generating-index-mesh`. If changes were made, it commits them with the message `chore: refresh installed skills and regenerate index mesh`.
```

**Step 4: Run the test**

```powershell
py -3 -m pytest tests/test_refresh_installed_skills.py -v
```

Expected: all three tests pass.

**Step 5: Commit**

```
git add sources/first_party/skills/refreshing-installed-skills tests/test_refresh_installed_skills.py
git commit -m "feat: add refreshing-installed-skills skill"
```

---

### Task 4: Create `using-git-worktrees` bundled scripts and overlay

**Files to create:**
- `adapters/codex/superpowers-plus/using-git-worktrees/scripts/new_worktree.py`
- `adapters/codex/superpowers-plus/using-git-worktrees/scripts/new-worktree.sh`
- `adapters/codex/superpowers-plus/using-git-worktrees/scripts/new-worktree.ps1`
- `adapters/codex/superpowers-plus/using-git-worktrees/scripts/remove_worktree.py`
- `adapters/codex/superpowers-plus/using-git-worktrees/scripts/remove-worktree.sh`
- `adapters/codex/superpowers-plus/using-git-worktrees/scripts/remove-worktree.ps1`

**Files to modify:**
- `adapters/codex/superpowers-plus/using-git-worktrees/overlay.yaml`

**Test file:** `tests/test_worktree_scripts.py`

**Interfaces:**
- Produces: `new_worktree.py` with `main(argv=None) -> int`, and `remove_worktree.py` with `main(argv=None) -> int`.
- Consumes: `git worktree add/remove/list`, and the `refreshing-installed-skills` skill core.

**Step 1: Write the failing test**

Create `tests/test_worktree_scripts.py`:

```python
import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
NEW_WORKTREE = REPO_ROOT / "adapters" / "codex" / "superpowers-plus" / "using-git-worktrees" / "scripts" / "new_worktree.py"
REMOVE_WORKTREE = REPO_ROOT / "adapters" / "codex" / "superpowers-plus" / "using-git-worktrees" / "scripts" / "remove_worktree.py"


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
    env = os.environ.copy()
    env.pop("GIT_DIR", None)
    env.pop("GIT_WORK_TREE", None)
    env.pop("GIT_INDEX_FILE", None)

    worktree_root = repo.parent / "_agent-worktrees" / "cycle-repo" / "feature"
    result = subprocess.run(
        [sys.executable, str(NEW_WORKTREE), "feature", "--no-skill-refresh"],
        cwd=repo,
        env=env,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert worktree_root.is_dir()

    result = subprocess.run(
        [sys.executable, str(REMOVE_WORKTREE), "feature"],
        cwd=repo,
        env=env,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert not worktree_root.exists()
```

**Step 2: Run the failing test**

```powershell
py -3 -m pytest tests/test_worktree_scripts.py -v
```

Expected: `ModuleNotFoundError` or file not found failures.

**Step 3: Implement the scripts**

Create `adapters/codex/superpowers-plus/using-git-worktrees/scripts/new_worktree.py`:

```python
#!/usr/bin/env python3
"""Create a git worktree at the canonical sibling location and refresh skills."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


def _stripped_env() -> dict[str, str]:
    env = os.environ.copy()
    env.pop("GIT_DIR", None)
    env.pop("GIT_WORK_TREE", None)
    env.pop("GIT_INDEX_FILE", None)
    return env


def _repo_root() -> Path:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
        check=True,
        env=_stripped_env(),
    )
    return Path(result.stdout.strip())


def _reject_submodule() -> None:
    result = subprocess.run(
        ["git", "rev-parse", "--show-superproject-working-tree"],
        capture_output=True,
        text=True,
        env=_stripped_env(),
    )
    if result.returncode == 0 and result.stdout.strip():
        raise RuntimeError("This script must not run inside a git submodule")


def _main_repo_root() -> Path:
    result = subprocess.run(
        ["git", "rev-parse", "--git-common-dir"],
        capture_output=True,
        text=True,
        check=True,
        env=_stripped_env(),
    )
    common = Path(result.stdout.strip())
    if not common.is_absolute():
        common = (_repo_root() / common).resolve()
    else:
        common = common.resolve()
    return common.parent


def _canonical_worktree_root(main_repo_root: Path, branch: str) -> Path:
    repo_name = main_repo_root.name
    return main_repo_root.parent / "_agent-worktrees" / repo_name / branch


def _find_refresh_script(worktree_root: Path) -> Path | None:
    candidates = [
        worktree_root / ".agents" / "skills" / "refreshing-installed-skills" / "scripts" / "refresh_installed_skills.py",
    ]
    for pattern in [
        "codex-marketplace/plugins/*/skills/refreshing-installed-skills/scripts/refresh_installed_skills.py",
        ".agents/plugins/marketplace-source/codex-marketplace/plugins/*/skills/refreshing-installed-skills/scripts/refresh_installed_skills.py",
    ]:
        candidates.extend(sorted(worktree_root.glob(pattern)))
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    return None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Create a git worktree at the canonical sibling location")
    parser.add_argument("branch", help="branch name to create")
    parser.add_argument("--base-ref", default=None, help="base ref for the new branch (default: HEAD)")
    parser.add_argument("--no-skill-refresh", action="store_true", help="skip refreshing installed skills in the new worktree")
    args = parser.parse_args(argv)

    repo_root = _repo_root()
    _reject_submodule()
    main_repo_root = _main_repo_root()

    worktree_root = _canonical_worktree_root(main_repo_root, args.branch)
    if worktree_root.exists():
        print(f"error: worktree path already exists: {worktree_root}", file=sys.stderr)
        return 1

    worktree_root.parent.mkdir(parents=True, exist_ok=True)

    cmd = ["git", "worktree", "add", str(worktree_root), "-b", args.branch]
    if args.base_ref:
        cmd.append(args.base_ref)

    result = subprocess.run(cmd, cwd=repo_root, env=_stripped_env())
    if result.returncode != 0:
        return result.returncode

    if not args.no_skill_refresh:
        refresh_script = _find_refresh_script(worktree_root)
        if refresh_script:
            subprocess.run([sys.executable, str(refresh_script)], cwd=worktree_root, env=_stripped_env())
        else:
            print("warning: refreshing-installed-skills not found; run it manually in the new worktree", file=sys.stderr)

    print(f"Worktree ready at {worktree_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

Create `adapters/codex/superpowers-plus/using-git-worktrees/scripts/remove_worktree.py`:

```python
#!/usr/bin/env python3
"""Remove a git worktree by branch name or path."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


def _stripped_env() -> dict[str, str]:
    env = os.environ.copy()
    env.pop("GIT_DIR", None)
    env.pop("GIT_WORK_TREE", None)
    env.pop("GIT_INDEX_FILE", None)
    return env


def _repo_root() -> Path:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
        check=True,
        env=_stripped_env(),
    )
    return Path(result.stdout.strip())


def _list_worktrees(repo_root: Path) -> dict[str, str]:
    result = subprocess.run(
        ["git", "worktree", "list", "--porcelain"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        env=_stripped_env(),
        check=True,
    )
    worktrees: dict[str, str] = {}
    current_path = ""
    current_branch = ""
    for line in result.stdout.splitlines():
        if line.startswith("worktree "):
            current_path = line.split(" ", 1)[1]
            current_branch = ""
        elif line.startswith("branch "):
            current_branch = line.split(" ", 1)[1]
        elif line == "":
            if current_path and current_branch:
                branch_name = current_branch.split("/")[-1]
                worktrees[branch_name] = current_path
            current_path = ""
            current_branch = ""
    if current_path and current_branch:
        branch_name = current_branch.split("/")[-1]
        worktrees[branch_name] = current_path
    return worktrees


def _resolve_worktree(repo_root: Path, target: str) -> Path:
    candidate = Path(target)
    if candidate.is_absolute() and candidate.is_dir():
        return candidate.resolve()

    worktrees = _list_worktrees(repo_root)
    if target in worktrees:
        return Path(worktrees[target]).resolve()

    for path in worktrees.values():
        resolved = Path(path).resolve()
        if resolved.name == target:
            return resolved

    raise RuntimeError(f"Could not resolve worktree: {target}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Remove a git worktree")
    parser.add_argument("target", help="branch name or absolute path of the worktree to remove")
    parser.add_argument("--force", action="store_true", help="force remove the worktree")
    args = parser.parse_args(argv)

    repo_root = _repo_root()
    worktree = _resolve_worktree(repo_root, args.target)

    if worktree == repo_root.resolve():
        print("error: refusing to remove the main repository checkout", file=sys.stderr)
        return 1

    try:
        subprocess.run(["git", "-C", str(worktree), "submodule", "deinit", "--all", "-f"], check=False, capture_output=True)
    except Exception:
        pass

    cmd = ["git", "worktree", "remove", str(worktree)]
    if args.force:
        cmd.append("--force")

    result = subprocess.run(cmd, cwd=repo_root, env=_stripped_env())
    if result.returncode != 0:
        return result.returncode

    print(f"Removed worktree {worktree}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

Create wrappers:

`new-worktree.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "${SCRIPT_DIR}/new_worktree.py" "$@"
```

`new-worktree.ps1`:

```powershell
$ErrorActionPreference = "Stop"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
& py -3 "$scriptDir\new_worktree.py" @args
```

`remove-worktree.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "${SCRIPT_DIR}/remove_worktree.py" "$@"
```

`remove-worktree.ps1`:

```powershell
$ErrorActionPreference = "Stop"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
& py -3 "$scriptDir\remove_worktree.py" @args
```

**Step 4: Update the overlay**

Read `adapters/codex/superpowers-plus/using-git-worktrees/overlay.yaml` and add the `generated_files` block and three `insert_after` edits.

Add to the top of `overlay.yaml` after the `metadata` block:

```yaml
generated_files:
  - source: adapters/codex/superpowers-plus/using-git-worktrees/scripts/new_worktree.py
    path: scripts/new_worktree.py
  - source: adapters/codex/superpowers-plus/using-git-worktrees/scripts/new-worktree.sh
    path: scripts/new-worktree.sh
  - source: adapters/codex/superpowers-plus/using-git-worktrees/scripts/new-worktree.ps1
    path: scripts/new-worktree.ps1
  - source: adapters/codex/superpowers-plus/using-git-worktrees/scripts/remove_worktree.py
    path: scripts/remove_worktree.py
  - source: adapters/codex/superpowers-plus/using-git-worktrees/scripts/remove-worktree.sh
    path: scripts/remove-worktree.sh
  - source: adapters/codex/superpowers-plus/using-git-worktrees/scripts/remove-worktree.ps1
    path: scripts/remove-worktree.ps1
```

Add an `insert_after` edit to point to the bundled scripts after Step 1a. Use this anchor from the upstream `SKILL.md`:

```yaml
- path: SKILL.md
  op: insert_after
  line: 57
  anchor: "Only proceed to Step 1b if you have no native worktree tool available."
  insert_lines:
    - ""
    - "If the repo provides bundled `new-worktree`/`remove-worktree` scripts (e.g. under `.agents/skills/using-git-worktrees/scripts/` or the `adapters/codex/superpowers-plus/using-git-worktrees/scripts/` source), prefer those helpers. They place the worktree at the canonical sibling-folder root (`../_agent-worktrees/<repo-name>/<branch>`) and automatically refresh installed skills after creation."
```

Add an `insert_after` edit to extend the Quick Reference table. Use the last row as anchor:

```yaml
- path: SKILL.md
  op: insert_after
  line: 157
  anchor: "| No package.json/Cargo.toml | Skip dependency install |"
  insert_lines:
    - "| Bundled `new-worktree` script | Use it instead of `git worktree add` |"
    - "| Bundled `remove-worktree` script | Use it to remove a worktree and deinit submodules |"
    - "| Skills need refresh after creation | `new-worktree` auto-runs `refreshing-installed-skills` |"
```

Add an `insert_after` edit for a new "Remove a worktree" section before Red Flags. Use the blank line before `## Red Flags` as anchor:

```yaml
- path: SKILL.md
  op: insert_after
  line: 184
  anchor: "- **Fix:** Report failures, get explicit permission to proceed"
  insert_lines:
    - ""
    - "## Remove a Worktree"
    - ""
    - "When a feature branch is complete, remove the isolated worktree to avoid stale copies."
    - ""
    - "1. Run the bundled `remove-worktree` script if available:"
    - "   ```bash"
    - "   bash .agents/skills/using-git-worktrees/scripts/remove-worktree.sh <branch-name>"
    - "   # or on Windows:"
    - "   .agents/skills/using-git-worktrees/scripts/remove-worktree.ps1 <branch-name>"
    - "   ```"
    - "   This de-initializes any submodules and removes the worktree directory."
    - ""
    - "2. If no bundled script is available, use `git worktree remove` directly:"
    - "   ```bash"
    - "   git worktree remove <path-to-worktree>"
    - "   ```"
    - "   Then manually deinitialize submodules if the repo uses them."
    - ""
    - "Never remove the main repository checkout with this command."
```

**Step 5: Run the test**

```powershell
py -3 -m pytest tests/test_worktree_scripts.py -v
```

Expected: all four tests pass.

**Step 6: Commit**

```
git add adapters/codex/superpowers-plus/using-git-worktrees tests/test_worktree_scripts.py
git commit -m "feat: bundle new/remove worktree scripts and update using-git-worktrees overlay"
```

---

### Task 5: Register the new skills in `repo-worker-pack`

**Files to modify:**
- `codex-marketplace/custody-pack-registry.json`

**Steps:**
- [ ] Open `codex-marketplace/custody-pack-registry.json`.
- [ ] In the `repo-worker-pack` pack, add two entries to `source_ledger`:
  ```json
  "sources/first_party/skills/refreshing-installed-skills",
  "sources/first_party/skills/generating-index-mesh",
  ```
- [ ] In the `repo-worker-pack` pack `entries` array, add two entry objects (order does not matter):

  ```json
  {
    "canonical_name": "refreshing-installed-skills",
    "source_category": "first_party",
    "content_mode": "verbatim",
    "source_family": "first_party",
    "canonical_source_path": "sources/first_party/skills/refreshing-installed-skills",
    "local_path": "skills/refreshing-installed-skills",
    "lane": "Worker",
    "source_path": "sources/first_party/skills/refreshing-installed-skills/SKILL.md",
    "source_author": "Harley Bartles",
    "source_license": "MIT",
    "source_repo": "https://github.com/HarleyBartles/agent-asset-marketplace",
    "copy_expectation": "byte_identical",
    "provenance_note": "First-party skill projected verbatim into the repo-worker-pack. Refreshes installed skills from the plugin source and regenerates the index mesh."
  },
  {
    "canonical_name": "generating-index-mesh",
    "source_category": "first_party",
    "content_mode": "verbatim",
    "source_family": "first_party",
    "canonical_source_path": "sources/first_party/skills/generating-index-mesh",
    "local_path": "skills/generating-index-mesh",
    "lane": "Worker",
    "source_path": "sources/first_party/skills/generating-index-mesh/SKILL.md",
    "source_author": "Harley Bartles",
    "source_license": "MIT",
    "source_repo": "https://github.com/HarleyBartles/agent-asset-marketplace",
    "copy_expectation": "byte_identical",
    "provenance_note": "First-party skill projected verbatim into the repo-worker-pack. Runs the repo's generate_index_mesh.py command."
  }
  ```
- [ ] Run the marketplace rebuild:
  ```powershell
  py -3 tools/rebuild_marketplace.py
  ```
- [ ] Run the marketplace check:
  ```powershell
  py -3 tools/check_marketplace.py
  ```
- [ ] Commit:
  ```
  git add codex-marketplace/custody-pack-registry.json codex-marketplace/plugins repo-index generated .agents/plugins .agents/skills .agents/INDEX.md
  git commit -m "chore: register refreshing-installed-skills and generating-index-mesh in repo-worker-pack and regenerate marketplace"
  ```

**Expected interim state:** `codex-marketplace/plugins/repo-worker-pack/skills/` now contains `refreshing-installed-skills` and `generating-index-mesh`; `tools/check_marketplace.py` passes.

---

### Task 6: Normalize first-party skill sources

**Files:**
- `sources/first_party/skills/refreshing-installed-skills/SKILL.md`
- `sources/first_party/skills/generating-index-mesh/SKILL.md`
- `sources/first_party/skills/refreshing-installed-skills/agents/openai.yaml`
- `sources/first_party/skills/generating-index-mesh/agents/openai.yaml`

**Steps:**
- [ ] Run the normalizer:
  ```powershell
  py -3 tools/normalize_first_party_skill_sources.py --write
  ```
- [ ] Inspect the diff to ensure frontmatter and `agents/openai.yaml` are still valid.
- [ ] Commit:
  ```
  git add sources/first_party/skills/refreshing-installed-skills sources/first_party/skills/generating-index-mesh
  git commit -m "chore: normalize new first-party skill sources"
  ```

**Expected interim state:** Frontmatter is normalized; `display_name` in `agents/openai.yaml` matches the skill names.

---

### Task 7: Full validation

**Steps:**
- [ ] Run the test suite:
  ```powershell
  py -3 -m pytest tests/test_generate_index_mesh.py tests/test_refresh_installed_skills.py tests/test_worktree_scripts.py -v
  ```
- [ ] Run marketplace rebuild and check:
  ```powershell
  py -3 tools/rebuild_marketplace.py
  py -3 tools/check_marketplace.py
  ```
- [ ] Stage all changes and run the whitespace check:
  ```powershell
  git add -A
  git diff --cached --check
  ```
  If it fails, fix whitespace and re-stage.
- [ ] Commit:
  ```
  git commit -m "chore: regenerate marketplace and validate"
  ```

**Expected interim state:** All tests pass, `check_marketplace.py` exits 0, `git diff --cached --check` exits 0.

---

### Task 8: Push and open PR to `dev`

**Files:** all changed files.

**Steps:**
- [ ] Verify branch target is `dev`:
  ```powershell
  git branch
  ```
  The current branch is `add-worktree-helpers`.
- [ ] Push the branch:
  ```powershell
  git push origin add-worktree-helpers
  ```
- [ ] Create PR against `dev` with the PR template from `.github/PULL_REQUEST_TEMPLATE.md`.
- [ ] Fill every section of the template, including:
  - What changed and why.
  - How to test (the validation commands above).
  - Disclosure of the model/harness/plugins used.
- [ ] Do not merge without human review.

---

## SDD Confidence Rating

9/10

The plan is concrete and each task has exact file targets, code, and validation. Overlay `insert_after` anchors are quoted verbatim from the current upstream `SKILL.md` and `tools/heal_overlays.py` runs during `rebuild_marketplace.py`/`check_marketplace.py`, so line-number drift is auto-healed as long as the anchor text remains unchanged. The only remaining risk is if the upstream `SKILL.md` content changes before execution; the implementer should verify the three anchors in `sources/third_party/superpowers/obra-superpowers/v6.1.0/skills/using-git-worktrees/SKILL.md` before running Task 4 Step 4.
