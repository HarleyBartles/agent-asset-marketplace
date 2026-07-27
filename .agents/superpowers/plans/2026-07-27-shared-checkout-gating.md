# Shared-checkout gating implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make `--allow-shared-checkout` an authoritative two-step approval gate across skill scripts and `rebuild_marketplace.py`.

**Architecture:** Introduce a shared `tools/shared_checkout_approval.py` helper that stores script-specific, time-bound, consumed-on-use tokens in `<git-dir>/info/`. Each gated script exposes `--allow-shared-checkout` as an approval-only step and `--apply` as an explicit mutation step. Parent scripts pre-approve child scripts by writing their tokens during the approval step.

**Tech Stack:** Python 3.13, `pathlib`, `datetime`, `subprocess`, `argparse`.

## Global constraints

- Token TTL is 10 minutes.
- Tokens are stored in `<git-dir>/info/devin-shared-checkout-approval-<script-name>` and never committed.
- `--allow-shared-checkout` cannot be combined with `--apply` or `--check`.
- No flags defaults to check/no-op; `--apply` must be explicit.
- Text files are written with `newline="\n"`.
- All changes to skill source require marketplace regeneration and full test run.

---

### Task 1: Implement the shared token helper

**Files:**
- Create: `tools/shared_checkout_approval.py`
- Test: `tests/test_shared_checkout_approval.py` (new)

**Interfaces:**
- Consumes: `git rev-parse --git-dir` to locate the token directory.
- Produces:
  - `approval_path(repo_root: Path, script_name: str) -> Path`
  - `is_valid(repo_root: Path, script_name: str) -> bool`
  - `write(repo_root: Path, script_name: str) -> Path`
  - `consume(repo_root: Path, script_name: str) -> bool`

- [ ] **Step 1: Write the failing test**

```python
from pathlib import Path
from shared_checkout_approval import approval_path, write, is_valid, consume

def test_token_round_trip(tmp_path: Path) -> None:
    # Fake a git dir structure
    git_dir = tmp_path / ".git"
    git_dir.mkdir()
    (git_dir / "info").mkdir()
    # Patch subprocess to return the fake git dir
    import shared_checkout_approval
    original_run = shared_checkout_approval.subprocess.run
    def fake_run(cmd, **kwargs):
        class R:
            stdout = str(git_dir)
            returncode = 0
        return R()
    shared_checkout_approval.subprocess.run = fake_run
    try:
        write(tmp_path, "test-script")
        assert is_valid(tmp_path, "test-script")
        assert consume(tmp_path, "test-script")
        assert not is_valid(tmp_path, "test-script")
    finally:
        shared_checkout_approval.subprocess.run = original_run
```

- [ ] **Step 2: Run test to verify it fails**

Run: `py -3 -m pytest tests/test_shared_checkout_approval.py -v`
Expected: FAIL with module not found or function not defined.

- [ ] **Step 3: Implement the helper**

```python
#!/usr/bin/env python3
"""Shared-checkout approval token helpers."""

from __future__ import annotations

import datetime
import os
import subprocess
from pathlib import Path


APPROVAL_TTL_SECONDS = 600
APPROVAL_FILENAME_PREFIX = "devin-shared-checkout-approval-"


def _stripped_env() -> dict[str, str]:
    env = os.environ.copy()
    env.pop("GIT_DIR", None)
    env.pop("GIT_WORK_TREE", None)
    env.pop("GIT_INDEX_FILE", None)
    return env


def _git_dir(repo_root: Path) -> Path:
    result = subprocess.run(
        ["git", "rev-parse", "--git-dir"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=True,
        env=_stripped_env(),
    )
    return Path(result.stdout.strip()).resolve()


def approval_path(repo_root: Path, script_name: str) -> Path:
    return _git_dir(repo_root) / "info" / f"{APPROVAL_FILENAME_PREFIX}{script_name}"


def _read_timestamp(path: Path) -> datetime.datetime | None:
    try:
        text = path.read_text(encoding="utf-8").strip()
        return datetime.datetime.fromisoformat(text)
    except (OSError, ValueError):
        return None


def is_valid(repo_root: Path, script_name: str) -> bool:
    path = approval_path(repo_root, script_name)
    timestamp = _read_timestamp(path)
    if timestamp is None:
        return False
    age = (datetime.datetime.now(datetime.timezone.utc) - timestamp).total_seconds()
    return age < APPROVAL_TTL_SECONDS


def write(repo_root: Path, script_name: str) -> Path:
    path = approval_path(repo_root, script_name)
    path.parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    with path.open("w", encoding="utf-8", newline="\n") as f:
        f.write(timestamp)
        f.write("\n")
    return path


def consume(repo_root: Path, script_name: str) -> bool:
    path = approval_path(repo_root, script_name)
    if is_valid(repo_root, script_name):
        path.unlink(missing_ok=True)
        return True
    path.unlink(missing_ok=True)
    return False
```

- [ ] **Step 4: Run test to verify it passes**

Run: `py -3 -m pytest tests/test_shared_checkout_approval.py -v`
Expected: PASS.

- [ ] **Step 5: Add expiry test**

```python
import datetime

def test_expired_token_is_invalid(tmp_path: Path) -> None:
    git_dir = tmp_path / ".git"
    git_dir.mkdir()
    (git_dir / "info").mkdir()
    import shared_checkout_approval
    original_run = shared_checkout_approval.subprocess.run
    def fake_run(cmd, **kwargs):
        class R:
            stdout = str(git_dir)
            returncode = 0
        return R()
    shared_checkout_approval.subprocess.run = fake_run
    try:
        write(tmp_path, "expired")
        path = approval_path(tmp_path, "expired")
        # Backdate the timestamp to 11 minutes ago
        old = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(seconds=661)
        path.write_text(old.isoformat() + "\n", encoding="utf-8", newline="\n")
        assert not is_valid(tmp_path, "expired")
        assert not consume(tmp_path, "expired")
    finally:
        shared_checkout_approval.subprocess.run = original_run
```

Run: `py -3 -m pytest tests/test_shared_checkout_approval.py -v`
Expected: PASS.

---

### Task 2: Gate `repo_standards.py`

**Files:**
- Modify: `sources/first_party/skills/repo-standards/scripts/repo_standards.py`
- Test: `tests/test_repo_standards.py`

**Interfaces:**
- Consumes: `tools/shared_checkout_approval.py` added to `sys.path` and imported at runtime.
- Produces: New `--apply` and `--allow-shared-checkout` behavior.

- [ ] **Step 1: Write failing tests**

Add to `tests/test_repo_standards.py`:

```python
def test_repo_standards_apply_with_allow_shared_checkout_rejected(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    _init_git_repo(repo)
    result = subprocess.run(
        [sys.executable, str(REPO_STANDARDS), "--apply", "--yes", "--allow-shared-checkout"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 1
    combined = result.stdout + result.stderr
    assert "cannot be combined" in combined.lower()


def test_repo_standards_allow_shared_checkout_writes_token(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    _init_git_repo(repo)
    result = subprocess.run(
        [sys.executable, str(REPO_STANDARDS), "--allow-shared-checkout"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    git_dir = subprocess.run(
        ["git", "rev-parse", "--git-dir"], cwd=repo, capture_output=True, text=True
    ).stdout.strip()
    token = Path(git_dir).resolve() / "info" / "devin-shared-checkout-approval-repo-standards"
    assert token.is_file()


def test_repo_standards_apply_in_shared_checkout_requires_token(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    _init_git_repo(repo)
    # Make it a linked worktree to simulate shared checkout
    main = tmp_path / "main"
    shutil.copytree(repo, main, ignore=lambda src, names: [".git"])
    # Use git worktree add to create a linked worktree
    # ... test setup helper ...
    result = subprocess.run(
        [sys.executable, str(REPO_STANDARDS), "--apply", "--yes"],
        cwd=linked,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 1
    assert "run --allow-shared-checkout first" in (result.stdout + result.stderr)
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `py -3 -m pytest tests/test_repo_standards.py::test_repo_standards_apply_with_allow_shared_checkout_rejected tests/test_repo_standards.py::test_repo_standards_allow_shared_checkout_writes_token -v`
Expected: FAIL.

- [ ] **Step 3: Modify `repo_standards.py`**

At the top of `repo_standards.py`, add `tools/` to `sys.path` and import the helper:

```python
import sys

# repo_standards.py is at .../sources/first_party/skills/repo-standards/scripts/ or
# .../.agents/skills/repo-standards/scripts/; _repo_root() returns the repo root.
REPO_TOOLS = _repo_root() / "tools"
sys.path.insert(0, str(REPO_TOOLS))
import shared_checkout_approval
```

Note: place this after `_repo_root()` is defined.

Add a constant for the script name:

```python
_SCRIPT_NAME = "repo-standards"
_SHARED_CHECKOUT_WARNING = (
    "warning: --allow-shared-checkout is an override and requires current human approval "
    "before applying changes"
)
```

In `_parse_args`, change `--apply` to default False and add `--allow-shared-checkout`:

```python
parser.add_argument("--apply", action="store_true", help="create missing surfaces")
parser.add_argument("--yes", action="store_true", help="skip the interactive approval prompt before applying changes")
parser.add_argument("--force", action="store_true", help="when applying, overwrite existing drifted surfaces")
parser.add_argument("--allow-shared-checkout", action="store_true", help="record approval to apply changes in a shared/git-worktree checkout")
```

Update `main`:

```python
def _record_approval(repo_root: Path) -> int:
    print(_SHARED_CHECKOUT_WARNING, file=sys.stderr)
    if sys.stdin.isatty():
        response = input("Record shared-checkout approval for repo-standards? (y/N) ")
        if response.strip().lower() != "y":
            print("approval not recorded", file=sys.stderr)
            return 1
    shared_checkout_approval.write(repo_root, _SCRIPT_NAME)
    print("shared-checkout approval recorded; run --apply --yes to apply", file=sys.stderr)
    return 0


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    repo_root = _repo_root()

    if _is_submodule(repo_root):
        print("error: repo-standards must not run inside a submodule", file=sys.stderr)
        return 1

    if args.apply and args.allow_shared_checkout:
        print("error: --allow-shared-checkout cannot be combined with --apply; run --allow-shared-checkout first, then --apply --yes", file=sys.stderr)
        return 1

    if args.allow_shared_checkout:
        if args.check:
            print("error: --allow-shared-checkout cannot be combined with --check", file=sys.stderr)
            return 1
        return _record_approval(repo_root)

    manifest = json.loads(_manifest_path().read_text(encoding="utf-8"))
    surfaces = manifest.get("surfaces", [])
    exceptions = _load_exceptions(repo_root)

    findings = []
    for surface in surfaces:
        findings.extend(_check_surface(repo_root, surface, exceptions))
    seen = set()
    unique_findings = [f for f in findings if not (f in seen or seen.add(f))]

    if args.check or not args.apply:
        if unique_findings:
            for f in unique_findings:
                print(f"DRIFT: {f}")
            return 1
        print("OK repo-standards: all surfaces present")
        return 0

    if _is_shared_checkout(repo_root):
        if not shared_checkout_approval.consume(repo_root, _SCRIPT_NAME):
            print("error: shared checkout; run --allow-shared-checkout first", file=sys.stderr)
            return 1

    if not args.yes:
        print(f"Will apply {len(unique_findings)} surfaces with drift: {unique_findings}")
        print("Add --yes to apply. Add --yes --force to overwrite existing drifted surfaces.")
        return 1

    applied = 0
    for surface in surfaces:
        if _check_surface(repo_root, surface, exceptions):
            if _apply_surface(repo_root, surface, exceptions, args.force):
                applied += 1
    print(f"OK repo-standards: applied {applied} surface(s)")
    return 0
```

- [ ] **Step 4: Run tests**

Run: `py -3 -m pytest tests/test_repo_standards.py -v`
Expected: New tests PASS; existing tests may need updates if they relied on default apply.

---

### Task 3: Gate `refresh_installed_skills.py`

**Files:**
- Modify: `sources/first_party/skills/refreshing-installed-skills/scripts/refresh_installed_skills.py`
- Test: `tests/test_refresh_installed_skills.py`

**Interfaces:**
- Consumes: `tools/shared_checkout_approval.py` imported at runtime.
- Produces: New `--apply` and `--allow-shared-checkout` behavior.

- [ ] **Step 1: Write failing tests**

Add tests for `--allow-shared-checkout` rejects `--apply` and `--check`, approval writes token, apply consumes token, missing token fails in shared checkout.

- [ ] **Step 2: Modify `refresh_installed_skills.py`**

Add `tools/` to `sys.path` and import `shared_checkout_approval`. Add `_SCRIPT_NAME = "refresh-installed-skills"` and `_MESH_SCRIPT_NAME = "generate-index-mesh"`.

Update `_parse_args`:

```python
parser.add_argument("--check", action="store_true", help="Check mode: report what would change without making changes")
parser.add_argument("--apply", action="store_true", help="Install/refresh skills")
parser.add_argument("--force", action="store_true", help="Force refresh even when provenance matches")
parser.add_argument("--allow-shared-checkout", action="store_true", help="Record approval to run in a shared/git-worktree checkout")
```

Add a helper to record approval:

```python
def _record_approval(repo_root: Path) -> int:
    print(_SHARED_CHECKOUT_WARNING, file=sys.stderr)
    if sys.stdin.isatty():
        response = input("Record shared-checkout approval for refresh-installed-skills? (y/N) ")
        if response.strip().lower() != "y":
            print("approval not recorded", file=sys.stderr)
            return 1
    shared_checkout_approval.write(repo_root, _SCRIPT_NAME)
    shared_checkout_approval.write(repo_root, _MESH_SCRIPT_NAME)
    print("shared-checkout approval recorded; run --apply to install/refresh", file=sys.stderr)
    return 0
```

Update `main`:

```python
def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)

    if _is_submodule(ROOT):
        print("error: this script must not run inside a git submodule", file=sys.stderr)
        return 1

    if args.apply and args.allow_shared_checkout:
        print("error: --allow-shared-checkout cannot be combined with --apply; run --allow-shared-checkout first, then --apply", file=sys.stderr)
        return 1

    if args.allow_shared_checkout:
        if args.check:
            print("error: --allow-shared-checkout cannot be combined with --check", file=sys.stderr)
            return 1
        return _record_approval(ROOT)

    if not args.check and not args.apply:
        # Default to check mode
        args.check = True

    if not args.check and _is_shared_checkout(ROOT):
        if not shared_checkout_approval.consume(ROOT, _SCRIPT_NAME):
            print("error: refusing to modify a shared checkout; run --allow-shared-checkout first", file=sys.stderr)
            return 1

    # ... rest of function unchanged except call generate_index_mesh with approval ...
```

- [ ] **Step 3: Run tests**

Run: `py -3 -m pytest tests/test_refresh_installed_skills.py -v`
Expected: PASS after test updates.

---

### Task 4: Gate `generate_index_mesh.py`

**Files:**
- Modify: `sources/first_party/skills/generating-agent-mesh/scripts/generate_index_mesh.py`
- Test: add tests if they exist

**Interfaces:**
- Consumes: `tools/shared_checkout_approval.py` imported at runtime.
- Produces: New `--apply` and `--allow-shared-checkout` behavior.

- [ ] **Step 1: Inspect `generate_index_mesh.py` entry point and argument parser**

Read the file to find `main()` and argument parser. Add `--apply` and `--allow-shared-checkout` flags. Default no flags to `--check`. In `--apply` mode, check shared checkout and consume `generate-index-mesh` token before writing files. In `--allow-shared-checkout` mode, write the token and exit.

- [ ] **Step 2: Update `rebuild_marketplace.py` and `refresh_installed_skills.py` calls**

`rebuild_marketplace.py` calls `generate_index_mesh.py` without `--check`; update to pass `--apply`.
`refresh_installed_skills.py` calls `generate_index_mesh.py` via subprocess; update to pass `--apply`.

---

### Task 5: Gate `rebuild_marketplace.py`

**Files:**
- Modify: `tools/rebuild_marketplace.py`
- Test: `tests/` (if `rebuild_marketplace.py` has tests)

**Interfaces:**
- Consumes: `tools/shared_checkout_approval.py`.
- Produces: `--apply` and `--allow-shared-checkout` semantics.

- [ ] **Step 1: Add `--apply` and `--allow-shared-checkout` arguments**

Default no flags to `--check`.

- [ ] **Step 2: Implement approval step**

When `--allow-shared-checkout` and not `--check`:
- Write tokens for `rebuild-marketplace`, `refresh-installed-skills`, `generate-index-mesh`.
- Print warning, optionally prompt.
- Exit 0.

- [ ] **Step 3: Implement apply gating**

When `--apply` and not `--check`:
- If shared checkout and no valid `rebuild-marketplace` token, error.
- Consume `rebuild-marketplace` token at start.
- Before calling `refresh_installed_skills.py`, ensure its token exists (written by approval step).
- At end, consume any remaining tokens.

- [ ] **Step 4: Update `refresh_installed_skills.py` invocation**

Remove `--allow-shared-checkout` from `refresh_args`. Ensure `refresh_installed_skills.py` is called with `--apply` (not default apply).

---

### Task 6: Regenerate marketplace and run verification

- [ ] **Step 1: Run `py -3 tools/rebuild_marketplace.py --apply`**
- [ ] **Step 2: Run `py -3 tools/check_marketplace.py`**
- [ ] **Step 3: Run `py -3 -m pytest`**
- [ ] **Step 4: Fix any failures**

---

### Task 7: Commit and push

- [ ] **Step 1: Stage changes and commit**
- [ ] **Step 2: Push branch and create PR**
