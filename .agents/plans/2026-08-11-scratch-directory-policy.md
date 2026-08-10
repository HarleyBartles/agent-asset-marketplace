# Scratch directory namespacing and cleanup policy

> **For agentic workers:** REQUIRED SUB-SKILL: Use /subagent-driven-development (recommended) or /executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the shared `_agent-scratch` root namespaced by repository, add validation so cross-repo dumping cannot happen again, and provide a cleanup tool to remove orphan scratch directories.

**Architecture:** Update the canonical scratch location algorithm in `repo-worker-base` to include the repository name in the scratch path. Add a portable `repo-standards` validator that checks the `_agent-scratch` root only contains repo-name folders and that each repo's scratch tree only contains branch or task folders. Update `using-git-worktrees` to create and remove the namespaced scratch directory alongside the worktree. Add a `cleanup-custody` helper to classify and delete orphan scratch. Canonical edits live in `codex-marketplace/plugins/...`; installed copies under `.agents/skills/` are regenerated.

**Tech Stack:** Python 3, Markdown, `py -3 tools/run.py ci --check`.

## Global Constraints

- Only edit canonical source in `codex-marketplace/plugins/`; regenerate `.agents/skills/` with `py -3 tools/run.py installed-skills --apply`.
- Every new or changed script must satisfy `--help` and `--check`.
- `py -3 tools/run.py ci --check` must pass before claiming any task complete.
- Do not delete or move in-flight scratch directories. Only `delete_now` when the owning branch is merged, the worktree is gone, and the repo has no active plan referencing the scratch path.
- Do not change the existing worktree root layout (`_agent-worktrees/<repo-name>/<branch>`).

---

### Task 0: Update `repo-worker-base` scratch location algorithm

**Files:**
- Modify: `codex-marketplace/plugins/repo-worker-pack/skills/repo-worker-base/references/worktree-and-branch-policy.md`

**Consumes:**
- (none; this is the first task)

**Produces:**
- The canonical algorithm for `external-scratch-root` becomes `parent(main-checkout) / "_agent-scratch" / repository-name / branch-name`.
- `plan-scoped-scratch` becomes `external-scratch-root / <plan-basename>`.

- [ ] **Step 1: Edit the algorithm block**

Replace the `external-scratch-root` and `plan-scoped-scratch` lines in the algorithm with:

```text
repository-name = basename(main-checkout)
external-worktree-root = parent(main-checkout) / "_agent-worktrees" / repository-name
external-scratch-root = parent(main-checkout) / "_agent-scratch" / repository-name / branch-name
plan-scoped-scratch = external-scratch-root / <plan-basename>
```

- [ ] **Step 2: Update the explanatory paragraph below the algorithm**

Change the text to state that `_agent-scratch` is now per-repo namespaced: the top level of `_agent-scratch` must contain only repo-name folders; each repo-name folder contains branch or task folders; each branch folder contains plan-scoped scratch.

- [ ] **Step 3: Commit**

```bash
git add codex-marketplace/plugins/repo-worker-pack/skills/repo-worker-base/references/worktree-and-branch-policy.md
git commit -m "docs(repo-worker-base): namespace scratch by repository in location algorithm"
```

---

### Task 1: Update the repo doctrine scratch policy

**Files:**
- Modify: `.agents/doctrine/non-repo-locations-policy.md`

**Consumes:**
- The canonical scratch algorithm from Task 0.

**Produces:**
- The doctrine file now shows the new scratch path and the rule that `_agent-scratch` top-level entries must be repo-name folders.

- [ ] **Step 1: Update the Scratch files section**

Replace the current path with:

```markdown
## Scratch files

Scratch files (temporary scripts, commit message temp files, inspection
scripts, debug output) go in `../_agent-scratch/<repo-name>/<branch>/<plan-basename>/`,
not in the repo tree. The scratch directory is a sibling of the repo folder.

Rules:

- The top level of `_agent-scratch` must contain only folders named after
  repositories (`<repo-name>`).
- Inside each repo folder, create subfolders named after the worktree branch
  the scratch belongs to.
- Plan- or task-scoped scratch lives inside the branch folder.
- Scratch contents are not durable. Do not put anything in scratch that needs
  to survive beyond the work it supports.
- Do not commit scratch files into the repo.
- Do not leave scratch files in the repo working tree. If a scratch file ends
  up in the repo tree, remove it before committing.
```

- [ ] **Step 2: Commit**

```bash
git add .agents/doctrine/non-repo-locations-policy.md
git commit -m "docs(doctrine): namespace scratch directories by repository"
```

---

### Task 2: Add `repo-standards` scratch policy reference

**Files:**
- Create: `codex-marketplace/plugins/repo-worker-pack/skills/repo-standards/references/scratch-workspace-policy.md`

**Consumes:**
- (none; this is a new portable reference)

**Produces:**
- Portable reference that consumer repos can install under `.agents/skills/repo-standards/references/scratch-workspace-policy.md`.

- [ ] **Step 1: Create the reference file**

```markdown
# Scratch workspace policy

## Scope

This policy covers the off-repo `_agent-scratch` directory used for
plan-scoped, branch-scoped, and task-scoped temporary files.

## Layout

```text
_agent-scratch/
  <repo-name>/
    <branch-name>/
      <plan-or-task-basename>/
        ...
```

The top level of `_agent-scratch` may only contain folders named after the
repositories that use it. Each repo folder may only contain folders named
after in-flight branches or active tasks. Leaf contents are disposable
scratch for that task.

## Naming

- `<repo-name>` is the basename of the repository's main checkout directory.
- `<branch-name>` is the git branch name the scratch belongs to.
- `<plan-or-task-basename>` is the base name of the plan or task file without
  extension.

## Validation

The `repo-standards` validator checks the local `_agent-scratch` root against
this layout. It reports any file or folder that is not a repo-name folder, and
any repo folder that contains entries not matching a branch or task.

## Cleanup

When a branch is merged and its worktree is removed, its scratch directory is
`delete_now` unless another active task or plan still references it.
```

- [ ] **Step 2: Commit**

```bash
git add codex-marketplace/plugins/repo-worker-pack/skills/repo-standards/references/scratch-workspace-policy.md
git commit -m "docs(repo-standards): add portable scratch workspace policy"
```

---

### Task 3: Update `repo-standards` SKILL.md to reference the new policy

**Files:**
- Modify: `codex-marketplace/plugins/repo-worker-pack/skills/repo-standards/SKILL.md`

**Consumes:**
- The `scratch-workspace-policy.md` reference from Task 2.

**Produces:**
- `SKILL.md` lists the new reference and the validator script once it exists.

- [ ] **Step 1: Add a scratch entry to the Read when table**

Append this row to the table in `SKILL.md`:

```markdown
| Scratch workspace layout and cleanup | [references/scratch-workspace-policy.md](references/scratch-workspace-policy.md) |
```

- [ ] **Step 2: Commit**

```bash
git add codex-marketplace/plugins/repo-worker-pack/skills/repo-standards/SKILL.md
git commit -m "docs(repo-standards): route to scratch workspace policy reference"
```

---

### Task 4: Add `repo-standards` scratch validator script

**Files:**
- Create: `codex-marketplace/plugins/repo-worker-pack/skills/repo-standards/scripts/validate_scratch.py`
- Test: `py -3 codex-marketplace/plugins/repo-worker-pack/skills/repo-standards/scripts/validate_scratch.py --check` and `--help`

**Consumes:**
- The `scratch-workspace-policy.md` reference from Task 2.

**Produces:**
- `validate_scratch.py` script with `--help`, `--check`, and `--apply` semantics.
- `--check` exits 0 if the `_agent-scratch` root under the repo's canonical location is clean, 1 otherwise.
- `--apply` removes orphan directories classified as `delete_now`.

- [ ] **Step 1: Create the validator script**

```python
#!/usr/bin/env python3
"""Validate and optionally clean the _agent-scratch directory layout."""

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path


def _stripped_env() -> dict[str, str]:
    import os
    env = os.environ.copy()
    env.pop("GIT_DIR", None)
    env.pop("GIT_WORK_TREE", None)
    env.pop("GIT_INDEX_FILE", None)
    return env


def _main_repo_root() -> Path:
    result = subprocess.run(
        ["git", "worktree", "list", "--porcelain"],
        capture_output=True,
        text=True,
        check=True,
        env=_stripped_env(),
    )
    for line in result.stdout.splitlines():
        if line.startswith("worktree "):
            return Path(line.split(" ", 1)[1]).resolve()
    raise RuntimeError("Could not determine the main repository root")


def _scratch_root() -> Path:
    main = _main_repo_root()
    return main.parent / "_agent-scratch"


def _valid_name(name: str) -> bool:
    """Return True if name is a non-empty, path-safe token without separators."""
    return bool(name) and re.fullmatch(r"[A-Za-z0-9_.-]+", name) is not None


def _validate(check: bool, apply: bool) -> int:
    scratch_root = _scratch_root()
    if not scratch_root.exists():
        print(f"OK: {scratch_root} does not exist")
        return 0

    issues = 0
    for entry in scratch_root.iterdir():
        if entry.is_file():
            print(f"FAIL: top-level scratch file {entry.name} is not a repo folder")
            if apply:
                entry.unlink()
                print(f"  removed {entry}")
            issues += 1
            continue
        if not _valid_name(entry.name):
            print(f"FAIL: {entry.name} is not a valid repo-name folder")
            if apply:
                shutil.rmtree(entry, ignore_errors=True)
                print(f"  removed {entry}")
            issues += 1
            continue
        for repo_entry in entry.iterdir():
            if repo_entry.is_file():
                print(f"FAIL: {entry.name} contains a file {repo_entry.name}, expected branch/task folders")
                if apply:
                    repo_entry.unlink()
                    print(f"  removed {repo_entry}")
                issues += 1
                continue
            if not _valid_name(repo_entry.name):
                print(f"FAIL: {entry.name}/{repo_entry.name} is not a valid branch/task folder")
                if apply:
                    shutil.rmtree(repo_entry, ignore_errors=True)
                    print(f"  removed {repo_entry}")
                issues += 1

    if issues:
        print(f"FAIL: {issues} issue(s) found")
        return 0 if apply else 1
    print(f"OK: {scratch_root} is clean and namespaced")
    return 0


def _cli() -> int:
    parser = argparse.ArgumentParser(
        description="Validate the _agent-scratch directory is namespaced by repo."
    )
    parser.add_argument(
        "--check", action="store_true", default=False, help="report drift and exit 1 if found"
    )
    parser.add_argument(
        "--apply", action="store_true", default=False, help="remove orphan entries classified as delete_now"
    )
    args = parser.parse_args()
    if not args.check and not args.apply:
        parser.print_help()
        return 0
    if args.apply:
        return _validate(check=False, apply=True)
    return _validate(check=True, apply=False)


if __name__ == "__main__":
    sys.exit(_cli())
```

- [ ] **Step 2: Verify `--help` and `--check` pass on a fresh checkout**

```bash
py -3 codex-marketplace/plugins/repo-worker-pack/skills/repo-standards/scripts/validate_scratch.py --help
py -3 codex-marketplace/plugins/repo-worker-pack/skills/repo-standards/scripts/validate_scratch.py --check
```

Expected: `--help` prints usage; `--check` reports OK because the scratch root either does not exist or is not initialized.

- [ ] **Step 3: Commit**

```bash
git add codex-marketplace/plugins/repo-worker-pack/skills/repo-standards/scripts/validate_scratch.py
git commit -m "feat(repo-standards): add scratch directory layout validator"
```

---

### Task 5: Update `using-git-worktrees` to create and remove namespaced scratch

**Files:**
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/using-git-worktrees/scripts/new_worktree.py`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/using-git-worktrees/scripts/remove_worktree.py`

**Consumes:**
- The canonical scratch algorithm from Task 0.

**Produces:**
- `new_worktree.py` creates `../_agent-scratch/<repo-name>/<branch>` alongside the worktree.
- `remove_worktree.py` removes that scratch directory when the worktree is removed.

- [ ] **Step 1: Add scratch creation to `new_worktree.py`**

After the worktree is created and before skill refresh, add:

```python
def _canonical_scratch_root(main_repo_root: Path, branch: str) -> Path:
    repo_name = main_repo_root.name
    return main_repo_root.parent / "_agent-scratch" / repo_name / branch

scratch_root = _canonical_scratch_root(main_repo_root, branch)
scratch_root.mkdir(parents=True, exist_ok=True)
print(f"Scratch ready at {scratch_root}")
```

Call it inside the `__main__` flow right after `_init_submodules` and before the refresh/skills step.

- [ ] **Step 2: Add scratch removal to `remove_worktree.py`**

Locate the worktree removal logic and add the scratch removal step:

```python
def _remove_scratch(main_repo_root: Path, branch: str) -> None:
    repo_name = main_repo_root.name
    scratch_root = main_repo_root.parent / "_agent-scratch" / repo_name / branch
    if scratch_root.exists():
        shutil.rmtree(scratch_root, ignore_errors=True)
        print(f"Removed scratch {scratch_root}")
```

Call `_remove_scratch(main_repo_root, branch)` immediately after `git worktree remove` succeeds.

- [ ] **Step 3: Commit each file**

```bash
git add codex-marketplace/plugins/superpowers-plus/skills/using-git-worktrees/scripts/new_worktree.py
git commit -m "feat(using-git-worktrees): create namespaced scratch with new worktree"
git add codex-marketplace/plugins/superpowers-plus/skills/using-git-worktrees/scripts/remove_worktree.py
git commit -m "feat(using-git-worktrees): remove namespaced scratch with worktree"
```

---

### Task 6: Add `cleanup-custody` scratch cleanup helper

**Files:**
- Create: `codex-marketplace/plugins/repo-worker-pack/skills/cleanup-custody/scripts/cleanup_scratch.py`

**Consumes:**
- (none; this is a new helper)

**Produces:**
- `cleanup_scratch.py` script that lists all top-level `_agent-scratch` entries, classifies each against running branches, and can remove `delete_now` entries.

- [ ] **Step 1: Create the script**

```python
#!/usr/bin/env python3
"""Classify and optionally clean orphan _agent-scratch directories."""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def _stripped_env() -> dict[str, str]:
    import os
    env = os.environ.copy()
    env.pop("GIT_DIR", None)
    env.pop("GIT_WORK_TREE", None)
    env.pop("GIT_INDEX_FILE", None)
    return env


def _main_repo_root() -> Path:
    result = subprocess.run(
        ["git", "worktree", "list", "--porcelain"],
        capture_output=True,
        text=True,
        check=True,
        env=_stripped_env(),
    )
    for line in result.stdout.splitlines():
        if line.startswith("worktree "):
            return Path(line.split(" ", 1)[1]).resolve()
    raise RuntimeError("Could not determine the main repository root")


def _active_branches(main_repo_root: Path) -> set[str]:
    result = subprocess.run(
        ["git", "branch", "--format=%(refname:short)"],
        cwd=main_repo_root,
        capture_output=True,
        text=True,
        check=True,
        env=_stripped_env(),
    )
    return {line.strip() for line in result.stdout.splitlines() if line.strip()}


def _classify(scratch_root: Path, repo_name: str, active_branches: set[str]) -> list[tuple[str, Path]]:
    repo_scratch = scratch_root / repo_name
    if not repo_scratch.exists():
        return []
    decisions = []
    for entry in repo_scratch.iterdir():
        if entry.is_dir() and entry.name in active_branches:
            decisions.append(("keep_live", entry))
        elif entry.is_dir():
            decisions.append(("delete_now", entry))
        else:
            decisions.append(("delete_now", entry))
    return decisions


def _main() -> int:
    parser = argparse.ArgumentParser(
        description="Classify or remove orphan _agent-scratch directories."
    )
    parser.add_argument("--repo-name", help="repository name to inspect; defaults to main checkout basename")
    parser.add_argument("--apply", action="store_true", help="remove delete_now entries")
    args = parser.parse_args()

    main_repo_root = _main_repo_root()
    repo_name = args.repo_name or main_repo_root.name
    scratch_root = main_repo_root.parent / "_agent-scratch"
    active = _active_branches(main_repo_root)

    decisions = _classify(scratch_root, repo_name, active)
    if not decisions:
        print(f"No scratch entries for {repo_name}")
        return 0

    for decision, path in decisions:
        print(f"{decision}: {path}")
        if decision == "delete_now" and args.apply:
            if path.is_dir():
                shutil.rmtree(path, ignore_errors=True)
            else:
                path.unlink(missing_ok=True)
            print(f"  removed {path}")

    return 0


if __name__ == "__main__":
    sys.exit(_main())
```

- [ ] **Step 2: Verify `--help` and `--check` equivalent**

```bash
py -3 codex-marketplace/plugins/repo-worker-pack/skills/cleanup-custody/scripts/cleanup_scratch.py --help
py -3 codex-marketplace/plugins/repo-worker-pack/skills/cleanup-custody/scripts/cleanup_scratch.py
```

Expected: `--help` prints usage; no-args run lists each `_agent-scratch/<repo-name>` entry with a classification.

- [ ] **Step 3: Commit**

```bash
git add codex-marketplace/plugins/repo-worker-pack/skills/cleanup-custody/scripts/cleanup_scratch.py
git commit -m "feat(cleanup-custody): add scratch directory cleanup helper"
```

---

### Task 7: Regenerate installed skills and run full CI

**Files:**
- All canonical skill source under `codex-marketplace/plugins/`
- Generated: `.agents/skills/`

**Consumes:**
- Canonical source changes from Tasks 0-6.

**Produces:**
- `.agents/skills/` mirrors canonical source.
- Marketplace indexes are current.

- [ ] **Step 1: Regenerate installed skills and indexes**

```bash
py -3 tools/run.py installed-skills --apply
py -3 tools/run.py marketplace --apply
```

Expected: installed skills and marketplace indexes reflect canonical source.

- [ ] **Step 2: Stage and run CI on the staged tree**

```bash
git add -A
py -3 tools/run.py ci --check
```

Expected: all targets pass on the staged tree.

- [ ] **Step 3: Commit the regenerated copies**

```bash
git commit -m "chore: regenerate installed skills and marketplace for scratch namespace policy"
```

Expected: the pre-commit hook re-runs `ci --apply` and succeeds.

---

### Task 8: Apply one-time cleanup to the current scratch root

**Files:**
- External: `Z:/_agent-scratch/`

**Consumes:**
- Installed `cleanup_scratch.py` from Task 6.
- Installed `validate_scratch.py` from Task 4.

**Produces:**
- The top level of `Z:/_agent-scratch/` contains only repo-name folders.
- Any current in-flight work is preserved under its repo/branch path.

- [ ] **Step 1: Inspect and classify**

Run from the main repo:

```bash
py -3 .agents/skills/cleanup-custody/scripts/cleanup_scratch.py
```

Expected: lists each top-level entry with `keep_live` or `delete_now`.

- [ ] **Step 2: Apply deletion for entries with no active branch or unknown repo**

```bash
py -3 .agents/skills/cleanup-custody/scripts/cleanup_scratch.py --apply
```

Expected: orphan entries removed; any in-flight branches remain.

- [ ] **Step 3: Run the scratch validator**

```bash
py -3 .agents/skills/repo-standards/scripts/validate_scratch.py --check
```

Expected: OK.

- [ ] **Step 4: Do not commit this cleanup**

Scratch is external to the repo. There is no git change to commit. Record the cleanup in the PR body only.

---

### Task 9: Push the branch and open a draft PR

**Files:**
- Branch: `2026-08-11-scratch-policy`
- PR body: brief summary and test command output

**Consumes:**
- All prior tasks completed.

**Produces:**
- Draft PR exists with publication proof.

- [ ] **Step 1: Push the branch**

```bash
git push origin 2026-08-11-scratch-policy
```

- [ ] **Step 2: Open the draft PR**

```bash
gh pr create --draft --title "Scratch directory namespacing and cleanup policy" --body "Implements per-repo scratch namespaces and adds validation/cleanup helpers. See .agents/plans/2026-08-11-scratch-directory-policy.md."
```

- [ ] **Step 3: Report the PR URL**

Expected: a GitHub draft PR URL.
