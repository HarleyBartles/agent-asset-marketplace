# Shared-checkout helper owned by repo-standards

> **For agentic workers:** implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. `py -3 tools/run.py ci --check` must pass before claiming any task is complete.

## Goal

Gate `--allow-shared-checkout` so it only applies when the main shared checkout is on the `main` branch, and make `repo-standards` the single skill that bundles `shared_checkout.py` and deploys it to `tools/shared_checkout.py`. Other skills that need the helper import it from `tools/`. Repo-specific overrides in `tools/shared_checkout.py` are allowed and are not reported as drift.

## Architecture

- `tools/shared_checkout.py::approve_mutation` only requires `--allow-shared-checkout` when the repo is the main shared checkout and `HEAD` is `main`; on any other branch it returns `True`, and linked worktrees are always approved.
- `repo-standards/scripts/shared_checkout.py` remains the bundled source of truth for the consumer deployment.
- `repo-standards` declares `tools/shared_checkout.py` as a surface with `check_content: false` so `--check` only verifies existence.
- `repo-standards --apply` deploys `tools/shared_checkout.py` if it is missing, and no-ops if it exists.
- `repo-standards --apply --force` overwrites `tools/shared_checkout.py` with the bundled copy.
- `generating-agent-mesh`, `refreshing-installed-skills`, and `using-git-worktrees` drop their bundled `shared_checkout.py` copies and import from the repo's `tools/shared_checkout.py`.

## Recommendations

1. **Runtime import for non-owner skills:** walk parent directories from the script location until `tools/shared_checkout.py` is found, then add that directory to `sys.path`. This works both in the marketplace source repo and in a consumer repo's `.agents/skills/...` installed layout.
2. **Force update mechanism:** use the existing `repo-standards --apply --force` flag. It already overwrites drifted surfaces. `ci --apply` does not pass `--force`, so it will not clobber a repo's customized `tools/shared_checkout.py`.

---

### Task 0: Branch-gate `--allow-shared-checkout` to the `main` branch

**Files:**
- Modify: `tools/shared_checkout.py`, `tools/run.py`
- Test: `py -3 tools/run.py ci --check`

**Interfaces:**
- `approve_mutation` returns `True` without the flag on any branch other than `main` in the main checkout.
- Linked worktrees always return `True`.

- [x] **Step 1: Add `_current_branch` helper and branch check in `approve_mutation`**

- [x] **Step 2: Update `tools/run.py` to preserve the user's `--allow-shared-checkout` value and reword help text**

---

### Task 1: Add `check_content: false` support to `repo_standards.py`

**Files:**
- Modify: `codex-marketplace/plugins/repo-worker-pack/skills/repo-standards/scripts/repo_standards.py`
- Test: `py -3 codex-marketplace/plugins/repo-worker-pack/skills/repo-standards/scripts/repo_standards.py --check`

**Interfaces:**
- Consumes: surface `check_content` manifest key.
- Produces: no drift findings for surfaces where `check_content` is `false`.

- [ ] **Step 1: Skip byte comparison when `check_content` is `false`**

In `_check_surface`, after the file is verified to exist, skip `_check_surface_content` if the surface has `check_content: false`.

- [ ] **Step 2: Ensure `--apply` still deploys when missing and `--apply --force` still overwrites**

`_apply_surface` already respects the existing `force` parameter; no change needed.

---

### Task 2: Add `tools/shared_checkout.py` to the repo-standards manifest

**Files:**
- Modify: `codex-marketplace/plugins/repo-worker-pack/skills/repo-standards/references/repository-shape-manifest.json`
- Test: `py -3 codex-marketplace/plugins/repo-worker-pack/skills/repo-standards/scripts/repo_standards.py --check`

**Interfaces:**
- Consumes: bundled `repo-standards/scripts/shared_checkout.py`.
- Produces: new `tools/shared_checkout.py` surface.

- [ ] **Step 1: Add the surface entry**

```json
{
  "id": "tools-shared-checkout",
  "path": "tools/shared_checkout.py",
  "kind": "file",
  "source": "scripts/shared_checkout.py",
  "check_content": false,
  "optional": false
}
```

---

### Task 3: Update non-owner skills to import from `tools/`

**Files:**
- Modify:
  - `codex-marketplace/plugins/repo-worker-pack/skills/generating-agent-mesh/scripts/generate_index_mesh.py`
  - `codex-marketplace/plugins/repo-worker-pack/skills/refreshing-installed-skills/scripts/refresh_installed_skills.py`
  - `codex-marketplace/plugins/superpowers-plus/skills/using-git-worktrees/scripts/new_worktree.py`
- Delete:
  - `codex-marketplace/plugins/repo-worker-pack/skills/generating-agent-mesh/scripts/shared_checkout.py`
  - `codex-marketplace/plugins/repo-worker-pack/skills/refreshing-installed-skills/scripts/shared_checkout.py`
  - `codex-marketplace/plugins/superpowers-plus/skills/using-git-worktrees/scripts/shared_checkout.py`
- Test: `py -3 tools/run.py ci --check`

**Interfaces:**
- Consumes: `tools/shared_checkout.py` being present in the repo.
- Produces: no bundled `shared_checkout.py` in non-repo-standards skills.

- [ ] **Step 1: Remove local-first branch from the import bootstrap**

Replace each skill's top-of-file shared-checkout bootstrap with a `tools/`-only search.

```python
_SCRIPT_DIR = Path(__file__).resolve().parent
_SHARED_CHECKOUT_PATH: Path | None = None
for _parent in _SCRIPT_DIR.parents:
    _candidate = _parent / "tools" / "shared_checkout.py"
    if _candidate.is_file():
        _SHARED_CHECKOUT_PATH = _parent / "tools"
        break
if _SHARED_CHECKOUT_PATH is None:
    raise RuntimeError("tools/shared_checkout.py not found; run repo-standards --apply")
sys.path.insert(0, str(_SHARED_CHECKOUT_PATH))
import shared_checkout  # noqa: E402
```

- [ ] **Step 2: Delete the bundled `shared_checkout.py` files in the non-owner skills**

---

### Task 4: Stage generated marketplace files in the repo-standards pre-commit template

**Files:**
- Modify: `codex-marketplace/plugins/repo-worker-pack/skills/repo-standards/templates/pre-commit`
- Test: `py -3 tools/run.py ci --check`

- [x] **Step 1: Restore `git add` for `codex-marketplace/plugin-roots.json` and `codex-marketplace/manifest.json` in the pre-commit allow-list**

`tools/run.py ci --apply` regenerates these files, so the hook must stage them before the `AFTER_STATUS` check.

---

### Task 5: Regenerate installed skills and verify

**Files:**
- Generated: `.agents/skills/*/scripts/shared_checkout.py`, `.agents/skills/.provenance.json`
- Test: `py -3 tools/run.py ci --check`

- [ ] **Step 1: Run `installed-skills --apply --allow-shared-checkout`**

- [ ] **Step 2: Run `py -3 tools/run.py ci --check`**

---

### Task 5: Commit and push

- [ ] **Step 1: Commit the changes and amend or extend the existing PR #285**

```bash
git add -A
git commit -m "feat: make repo-standards the single owner of shared_checkout.py"
git push
```

- [ ] **Step 2: Verify the PR head and `ci --check` output are recorded in the PR body**
