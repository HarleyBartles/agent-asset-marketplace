# Skill seams cleanup implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `/subagent-driven-development` (recommended) or `/executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fix the cross-pack `shared_checkout` import in `using-git-worktrees`, the `install_profiles.py` `added`/`updated` status bug, the duplicated loop-breaker in `reviewer-strong.md`, the duplicated `model:` paragraph in `devin-desktop-profile.md`, inconsistent skill-invocation backtick syntax, and stale scratch-path comments in `task-brief`/`review-package`.

**Architecture:** A set of source-only edits under `codex-marketplace/plugins/<pack>/skills/` with no repo shape changes. Each fix is independent and testable before a final `tools/run.py marketplace --apply` regeneration and `ci --check` gate.

**Tech Stack:** Python 3, bash, Markdown, `tools/run.py`.

## Global Constraints

- Edits are source custody under `codex-marketplace/plugins/`. Do not hand-edit generated `.agents/skills/` or `.agents/INDEX.md` surfaces; regenerate them with `tools/run.py marketplace --apply`.
- `tools/shared_checkout.py` and `repository-shape-manifest.json` are unchanged; `repo-standards` remains the owner of `shared_checkout.py` for `repo-worker-pack`.
- Every file-modifying task ends with a focused commit.
- The final task runs `py -3 tools/run.py marketplace --apply` and `py -3 tools/run.py ci --check` before pushing and opening a draft PR.
- Branch: `fix-skill-seams-2026-08-13`. Worktree: `Z:\_agent-worktrees\agent-asset-marketplace\fix-skill-seams-2026-08-13`.

---

### Task 1: Remove cross-pack `shared_checkout` import from `new_worktree.py`

**Files:**
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/using-git-worktrees/scripts/new_worktree.py`

**Interfaces:**
- Consumes: no `shared_checkout` import.
- Produces: `new_worktree.py` imports only stdlib; `--allow-shared-checkout` is forwarded to `refresh_installed_skills` and `generate_index_mesh` only.

- [ ] **Step 1: Remove the `shared_checkout` bootstrap**

Old:
```python
# Import the shared checkout helper from the repo's tools/ directory. The only
# bundled copy lives inside the repo-standards skill; other skills rely on
# repo-standards having deployed tools/shared_checkout.py.
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

New: delete the block entirely; keep the preceding stdlib imports.

- [ ] **Step 2: Remove the `approve_mutation` call**

Old:
```python
        refresh_script = _find_refresh_script(worktree_root)
        if refresh_script:
            if not shared_checkout.approve_mutation(worktree_root, "new-worktree", allow_shared_checkout):
                return 1
            refresh_args = [str(refresh_script), "--apply", "--allow-shared-checkout"]
```

New:
```python
        refresh_script = _find_refresh_script(worktree_root)
        if refresh_script:
            refresh_args = [str(refresh_script), "--apply", "--allow-shared-checkout"]
```

- [ ] **Step 3: Verify the script CLI contract**

Run: `py -3 .agents/skills/using-git-worktrees/scripts/new_worktree.py --help`
Expected: exits 0 with help text.

Run: `py -3 .agents/skills/using-git-worktrees/scripts/new_worktree.py --check some-test-branch`
Expected: exits 1 (branch does not exist), no `shared_checkout` import error.

- [ ] **Step 4: Commit**

```bash
git add codex-marketplace/plugins/superpowers-plus/skills/using-git-worktrees/scripts/new_worktree.py
git commit -m "fix(using-git-worktrees): remove shared_checkout cross-pack import

new_worktree does not need its own approve_mutation because it always
operates on a new linked worktree; child scripts gate themselves."
```

---

### Task 2: Fix `install_profiles.py` `added`/`updated` status

**Files:**
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/selecting-a-subagent/scripts/install_profiles.py`

**Interfaces:**
- Consumes: `_needs_sync` and `_profile_paths` helpers.
- Produces: `_install` tracks pre-write existence status and reports `added` only for fresh files.

- [ ] **Step 1: Track pre-write `added` status**

Old:
```python
    changes: list[Path] = []
    for source in source_profiles:
        target = target_dir / source.name
        if _needs_sync(source, target):
            changes.append(source)
            if apply:
                target.write_bytes(source.read_bytes())
```

New:
```python
    statuses: dict[str, bool] = {}
    changes: list[Path] = []
    for source in source_profiles:
        target = target_dir / source.name
        statuses[source.name] = not target.exists()
        if _needs_sync(source, target):
            changes.append(source)
            if apply:
                target.write_bytes(source.read_bytes())
```

- [ ] **Step 2: Use tracked status in output**

Old:
```python
    for p in changes:
        status = "added" if not (target_dir / p.name).exists() else "updated"
        print(f"{status}: {target_dir / p.name}")
```

New:
```python
    for p in changes:
        status = "added" if statuses[p.name] else "updated"
        print(f"{status}: {target_dir / p.name}")
```

- [ ] **Step 3: Verify with a temporary target**

Create a temporary directory (e.g. `Z:\_agent-scratch\agent-asset-marketplace\fix-skill-seams-2026-08-13\install-test`) and delete it first.

Run:
```bash
py -3 .agents/skills/selecting-a-subagent/scripts/install_profiles.py --source .agents/skills/selecting-a-subagent/assets --target <temp-dir> --apply
```
Expected: at least one profile reports `added: <target>\<name>.md`.

Run the same command again.
Expected: all profiles report `OK: all shipped profiles are already installed.` (no "updated").

- [ ] **Step 4: Commit**

```bash
git add codex-marketplace/plugins/superpowers-plus/skills/selecting-a-subagent/scripts/install_profiles.py
git commit -m "fix(selecting-a-subagent): report added correctly on first install"
```

---

### Task 3: Remove duplicated loop-breaker in `reviewer-strong.md`

**Files:**
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/selecting-a-subagent/assets/reviewer-strong.md`

**Interfaces:**
- Produces: a single, expanded loop-breaker block.

- [ ] **Step 1: Remove the first, narrower loop-breaker block**

Old:
```markdown
- If you are about to make the same `read` or `grep` call again without a new question it can answer, write the report immediately.
- If the last two tool calls produced no new findings, write the report immediately.
- As a hard backstop, do not exceed 50 total tool calls after loading the inputs.
- If you are about to make the same `read`, `grep`, or `find_file_by_name` call again without a new question it can answer, write the report immediately.
- If the last two tool calls produced no new findings, write the report immediately.
- As a hard backstop, do not exceed 50 total tool calls after loading the inputs.
```

New:
```markdown
- If you are about to make the same `read`, `grep`, or `find_file_by_name` call again without a new question it can answer, write the report immediately.
- If the last two tool calls produced no new findings, write the report immediately.
- As a hard backstop, do not exceed 50 total tool calls after loading the inputs.
```

- [ ] **Step 2: Verify no duplicate remains**

Run: `grep -n "last two tool calls produced no new findings" codex-marketplace/plugins/superpowers-plus/skills/selecting-a-subagent/assets/reviewer-strong.md`
Expected: one line in the `## Stop condition and loop breaker` section.

- [ ] **Step 3: Commit**

```bash
git add codex-marketplace/plugins/superpowers-plus/skills/selecting-a-subagent/assets/reviewer-strong.md
git commit -m "fix(reviewer-strong): remove duplicated loop-breaker block"
```

---

### Task 4: Remove duplicated `model:` paragraph in `devin-desktop-profile.md`

**Files:**
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/selecting-a-subagent/references/devin-desktop-profile.md`

**Interfaces:**
- Produces: single `model:`/allowed-tools section; the CLI/Desktop split remains a documented gap for a follow-up plan.

- [ ] **Step 1: Remove the shorter, first `model:` paragraph**

Old:
```markdown
Custom profiles may declare `model:` in their `.md` profile file. The runtime honors that model when the subagent is launched. Do not pass a `model:` argument to `run_subagent`; the tool has no such parameter.

Custom profiles may declare `model:` in their `.md` profile file. The runtime honors that model when the subagent is launched, but the tool set is also constrained by the profile `name` and is cached; edits may not take effect until the IDE is restarted. `allowed-tools` describes the expected tool set, but the runtime may expose fewer tools. For example, `reviewer-strong` on `glm-5-2` has `exec`, `grep`, `read`, `find_file_by_name`, and `write`; `reviewer-fixes` on `swe-1-6` has the same tools. To create an off-repo file from a profile that does not expose `write`, use `exec`.
```

New:
```markdown
Custom profiles may declare `model:` in their `.md` profile file. The runtime honors that model when the subagent is launched, but the tool set is also constrained by the profile `name` and is cached; edits may not take effect until the IDE is restarted. `allowed-tools` describes the expected tool set, but the runtime may expose fewer tools. For example, `reviewer-strong` on `glm-5-2` has `exec`, `grep`, `read`, `find_file_by_name`, and `write`; `reviewer-fixes` on `swe-1-6` has the same tools. To create an off-repo file from a profile that does not expose `write`, use `exec`.
```

- [ ] **Step 2: Verify no duplicate remains**

Run: `grep -n "Do not pass a \`model:\` argument to \`run_subagent\`" codex-marketplace/plugins/superpowers-plus/skills/selecting-a-subagent/references/devin-desktop-profile.md`
Expected: no output.

- [ ] **Step 3: Commit**

```bash
git add codex-marketplace/plugins/superpowers-plus/skills/selecting-a-subagent/references/devin-desktop-profile.md
git commit -m "fix(devin-desktop-profile): remove duplicated model paragraph"
```

---

### Task 5: Standardize skill-invocation backtick syntax in authoring skills

**Files:**
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/writing-skills/SKILL.md`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/writing-plans/SKILL.md`

**Interfaces:**
- Produces: skill names in prose are wrapped in backticks (`/name`) so examples and templates are unambiguous.

- [ ] **Step 1: Fix `writing-skills` "Good" examples**

Old:
```markdown
- ✅ Good: `**REQUIRED SUB-SKILL:** Use /test-driven-development`
- ✅ Good: `**REQUIRED BACKGROUND:** You MUST understand /systematic-debugging`
```

New:
```markdown
- ✅ Good: `**REQUIRED SUB-SKILL:** Use `/test-driven-development``
- ✅ Good: `**REQUIRED BACKGROUND:** You MUST understand `/systematic-debugging``
```

- [ ] **Step 2: Fix `writing-plans` plan header template**

Old:
```markdown
> **For agentic workers:** REQUIRED SUB-SKILL: Use /subagent-driven-development (recommended) or /executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.
```

New:
```markdown
> **For agentic workers:** REQUIRED SUB-SKILL: Use `/subagent-driven-development` (recommended) or `/executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.
```

- [ ] **Step 3: Fix `writing-plans` bullet examples**

Old:
```markdown
- **REQUIRED SUB-SKILL:** Use /subagent-driven-development
```
and
```markdown
- **REQUIRED SUB-SKILL:** Use /executing-plans
```

New:
```markdown
- **REQUIRED SUB-SKILL:** Use `/subagent-driven-development`
```
and
```markdown
- **REQUIRED SUB-SKILL:** Use `/executing-plans`
```

- [ ] **Step 4: Verify with `grep`**

Run: `grep -n "Use /[a-z-]" codex-marketplace/plugins/superpowers-plus/skills/writing-skills/SKILL.md codex-marketplace/plugins/superpowers-plus/skills/writing-plans/SKILL.md`
Expected: no matches (all backticked).

- [ ] **Step 5: Commit**

```bash
git add codex-marketplace/plugins/superpowers-plus/skills/writing-skills/SKILL.md codex-marketplace/plugins/superpowers-plus/skills/writing-plans/SKILL.md
git commit -m "fix(writing-skills,writing-plans): backtick-wrap skill invocations"
```

---

### Task 6: Fix stale scratch-path comments in `task-brief` and `review-package`

**Files:**
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/subagent-workspace/scripts/task-brief`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/subagent-workspace/scripts/review-package`

**Interfaces:**
- Produces: Usage comments match the `<repo-name>/<branch>/<plan-stem>` path that `sdd-workspace` actually returns.

- [ ] **Step 1: Fix `task-brief` comment**

Old:
```bash
# Default OUTFILE: <repo-root>/../_agent-scratch/<branch>/<plan-stem>/task-<N>-brief.md
```

New:
```bash
# Default OUTFILE: <main-checkout>/../_agent-scratch/<repo-name>/<branch>/<plan-stem>/task-<N>-brief.md
```

- [ ] **Step 2: Fix `review-package` comment**

Old:
```bash
# Default OUTFILE: <repo-root>/../_agent-scratch/<branch>/<plan-stem>/review-<base7>..<head7>.diff
```

New:
```bash
# Default OUTFILE: <main-checkout>/../_agent-scratch/<repo-name>/<branch>/<plan-stem>/review-<base7>..<head7>.diff
```

- [ ] **Step 3: Verify by running `sdd-workspace`**

Run: `py -3 .agents/skills/subagent-workspace/scripts/sdd-workspace .agents/plans/2026-08-13-skill-seams-cleanup.md`
Expected: output path contains `_agent-scratch/agent-asset-marketplace/<branch>/2026-08-13-skill-seams-cleanup`.

- [ ] **Step 4: Commit**

```bash
git add codex-marketplace/plugins/superpowers-plus/skills/subagent-workspace/scripts/task-brief codex-marketplace/plugins/superpowers-plus/skills/subagent-workspace/scripts/review-package
git commit -m "fix(subagent-workspace): correct scratch-path usage comments"
```

---

### Task 7: Regenerate installed skills and open a draft PR

**Files:**
- Generated: `.agents/skills/**`, `codex-marketplace/plugins/*/`, `INDEX.md` files.
- Create: PR on GitHub (draft).

**Interfaces:**
- Consumes: all source edits from Tasks 1-6.
- Produces: green `ci --check` and a draft PR into `main`.

- [ ] **Step 1: Regenerate the marketplace**

Run: `py -3 tools/run.py marketplace --apply`
Expected: all generators pass; generated files are updated.

- [ ] **Step 2: Stage regenerated files and source edits**

Run: `git add -A`
Then: `git status --short` to confirm only expected files are staged.

- [ ] **Step 3: Run the preflight**

Run: `py -3 tools/run.py ci --check`
Expected: `[tools/run] all requested targets passed.`

- [ ] **Step 4: Commit regeneration and any remaining changes**

```bash
git commit -m "chore: regenerate installed skills after seam fixes"
```

- [ ] **Step 5: Push and open a draft PR**

```bash
git push -u origin fix-skill-seams-2026-08-13
gh pr create --draft --title "fix: skill seams cleanup" --body "Fixes cross-pack shared_checkout import, install_profiles status, duplicated content, invocation syntax, and stale scratch comments."
```

- [ ] **Step 6: Record publication proof**

Capture the PR URL and the head SHA: `git rev-parse HEAD`.

---

## Plan-readiness assessment

**Execution confidence: 8/10.**

Coverage:
- Task 1-4 and 6 have exact file paths and old/new string blocks.
- Task 5 has exact strings for the primary authoring skills but does not sweep every bare `/name` in other marketplace skill files; the remaining occurrences in `using-superpowers-plus/references/bootstrap-routing.md` and `repo-standards/references/repository-runbook-standard.md` are deliberate follow-up work.
- Task 7 is standard marketplace regeneration and PR flow.

Gaps:
- The CLI versus Desktop distinction in `devin-desktop-profile.md` is not resolved; only the duplicate paragraph is removed. A follow-up plan needs a CLI reference to document the difference.
- Skill-invocation syntax is only standardized in `writing-skills` and `writing-plans`; other skills still mix bare and backticked forms.
