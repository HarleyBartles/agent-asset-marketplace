# Shared-checkout gating implementation plan

**Goal:** Replace the token-based shared-checkout approval mechanism with a simple runtime `--allow-shared-checkout` flag across skill scripts and `rebuild_marketplace.py`.

**Tech Stack:** Python 3.13, `pathlib`, `subprocess`, `argparse`.

## Global constraints

- `--allow-shared-checkout` is rejected unless `--apply` (or the default mutation mode) is present.
- In a shared checkout, scripts warn and prompt interactively unless `--allow-shared-checkout` is passed.
- Parent scripts forward `--allow-shared-checkout` to any child mutation scripts.
- Text files are written with `newline="\n"`.
- All changes to skill source require marketplace regeneration and full test run.

---

### Task 1: Implement the shared helper

**Files:**
- Add: `tools/shared_checkout.py`
- Add: `tests/test_shared_checkout.py` (rename from `tests/test_shared_checkout_approval.py`)

**Interfaces:**
- `is_shared_checkout(repo_root: Path) -> bool`
- `prompt_for_approval(script_name: str) -> bool`
- `approve_mutation(repo_root: Path, script_name: str, flag_approved: bool) -> bool`

- [x] **Step 1: Write the helper**.
- [x] **Step 2: Write tests**.
- [x] **Step 3: Run `py -3 -m pytest tests/test_shared_checkout.py -v` and ensure PASS.**.

### Task 2: Integrate `shared_checkout` into `repo_standards.py`

- [x] **Step 1: Replace `_is_shared_checkout` and token calls with `shared_checkout.approve_mutation`.**.
- [x] **Step 2: Reject `--allow-shared-checkout` without `--apply` and with `--check`.**.
- [x] **Step 3: Update `tests/test_repo_standards.py` for the new flag semantics.**.
- [x] **Step 4: Run targeted tests and confirm PASS.**.

### Task 3: Integrate `shared_checkout` into `refresh_installed_skills.py`

- [x] **Step 1: Remove token logic and use `shared_checkout.approve_mutation`.**.
- [x] **Step 2: Remove redundant `_regenerate_index_mesh` call from `main`.**.
- [x] **Step 3: Update `tests/test_refresh_installed_skills.py` to patch `shared_checkout.approve_mutation`.**.
- [x] **Step 4: Run targeted tests and confirm PASS.**.

### Task 4: Integrate `shared_checkout` into `generate_index_mesh.py`

- [x] **Step 1: Remove token logic and use `shared_checkout.approve_mutation`.**.
- [x] **Step 2: Update `tests/test_generate_index_mesh.py` if needed.**.
- [x] **Step 3: Run targeted tests and confirm PASS.**.

### Task 5: Integrate `shared_checkout` into `rebuild_marketplace.py`

- [x] **Step 1: Remove `shared_checkout_approval.py` and token orchestration.**.
- [x] **Step 2: Accept and forward `--allow-shared-checkout` to child scripts.**.
- [x] **Step 3: Update `tests/test_rebuild_marketplace_cli.py` if needed.**.
- [x] **Step 4: Run targeted tests and confirm PASS.**.

### Task 6: Integrate `shared_checkout` into `new_worktree.py`

- [x] **Step 1: Add `--allow-shared-checkout` argument and use `shared_checkout.approve_mutation`.**.
- [x] **Step 2: Forward `--allow-shared-checkout` to `refresh_installed_skills.py` and `generate_index_mesh.py` in the new worktree.**.
- [x] **Step 3: Update `tests/test_worktree_scripts.py`.**.
- [x] **Step 4: Run targeted tests and confirm PASS.**.

### Task 7: Remove token artifacts and regenerate

- [x] **Step 1: Delete `tools/shared_checkout_approval.py` and vendored copies.**.
- [x] **Step 2: Add `shared_checkout.py` copies next to each gated skill script so installed/projected skills are self-contained.**.
- [x] **Step 3: Update `tools/AGENTS.md` to document the new `--apply --allow-shared-checkout` usage.**.
- [x] **Step 4: Run `py -3 tools/rebuild_marketplace.py --apply`.**.
- [x] **Step 5: Run `py -3 -m pytest` and confirm all PASS.**.
- [x] **Step 6: Run `py -3 tools/check_marketplace.py` and confirm PASS.**.

### Task 8: Publish

- [ ] **Step 1: Stage all changed files and commit.**
- [ ] **Step 2: Push the branch and open/update the PR.**
