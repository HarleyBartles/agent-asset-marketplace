# repo-standards pre-commit contract and targeted staging

> **For agentic workers:** REQUIRED SUB-SKILL: Use `/executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Relax `repo-standards` pre-commit validation from a byte-for-byte template match to a contract check, and make the default hook template stage only generated/tracked surfaces instead of all files.

**Architecture:** Add a contract scan to `repo_standards.py` for `kind == "hook"`, replace the template's `git add -A` with targeted `git add` calls, and update the shape standard/manifest to describe the contract. Regenerate the installed `repo-standards` skill copy and open a draft PR.

**Tech Stack:** Python 3, `pathlib`, `git`, `tools/run.py`.

## Global Constraints

- `py -3 tools/run.py ci --check` must pass after every meaningful commit.
- `py -3 tools/run.py marketplace --apply` must refresh installed skill copies correctly.
- The source-of-truth for the skill is under `codex-marketplace/plugins/repo-worker-pack/skills/repo-standards/`; `.agents/skills/repo-standards/` is generated.
- Do not break existing consumer repos that use the current template; the new contract should be a superset of acceptable hook content.

## Task 1: Relax hook validation to a contract check

**Files:**
- Modify: `codex-marketplace/plugins/repo-worker-pack/skills/repo-standards/scripts/repo_standards.py`

**Interfaces:**
- Consumes: `_check_surface`, `_check_surface_content` helpers.
- Produces: `_check_hook_contract(repo_root: Path, hook_path: Path) -> list[str]`.

- [ ] **Step 1: Read the current `kind == "hook"` branch in `_check_surface`**

- [ ] **Step 2: Write `_check_hook_contract`**

```python
def _check_hook_contract(hook_path: Path) -> list[str]:
    findings: list[str] = []
    if not os.access(hook_path, os.X_OK):
        # On Windows this may be permissive, so also accept a shebang/executable marker.
        pass
    text = hook_path.read_text(encoding="utf-8")
    if "set -euo pipefail" not in text and ("set -e" not in text or "set -u" not in text or "set -o pipefail" not in text):
        findings.append("pre-commit hook missing errexit/nounset/pipefail guard")
    ci_apply = "tools/run.py ci --apply" in text
    if not ci_apply:
        # Also accept py -3 / python3 / python forms
        ci_apply = any(f"{cmd} tools/run.py ci --apply" in text for cmd in ("py -3", "python3", "python"))
    if not ci_apply:
        findings.append("pre-commit hook must run 'tools/run.py ci --apply'")
    return findings
```

- [ ] **Step 3: Replace byte comparison in `_check_surface` for `kind == "hook"`**

Replace:
```python
        if template is not None and template.is_file():
            expected = template.read_bytes()
            actual = hook_path.read_bytes()
            if expected != actual:
                findings.append(f"drift: {rel}")
```
with:
```python
        findings.extend(_check_hook_contract(hook_path))
```

- [ ] **Step 4: Run `py -3 tools/run.py ci --check` and commit**

```bash
git add codex-marketplace/plugins/repo-worker-pack/skills/repo-standards/scripts/repo_standards.py
git commit -m "feat: validate pre-commit hook by contract, not byte-for-byte"
```

## Task 2: Tighten the default pre-commit template staging

**Files:**
- Modify: `codex-marketplace/plugins/repo-worker-pack/skills/repo-standards/templates/pre-commit`

**Interfaces:**
- None; shell script.

- [ ] **Step 1: Replace the final `git add -A` with targeted staging**

Keep the `ci --apply` call, then add:

```bash
# Re-stage any tracked files the hook regenerated.
git diff --name-only --diff-filter=M | while IFS= read -r file; do
  git add "$file"
done

# Stage canonical generated surfaces that may not yet be tracked in a fresh repo.
git add INDEX.md || true
find . -name INDEX.md -not -path './.git/*' -exec git add {} + || true
git add INDEX.json || true
git add .agents/skills/.provenance.json || true
git add .provenance.json || true
git add codex-marketplace/plugin-roots.json || true
git add .agents/plugins/marketplace.json || true
git add codex-marketplace/manifest.json || true
```

Use `|| true` so a missing file does not abort the hook.

- [ ] **Step 2: Run `py -3 tools/run.py ci --check` and commit**

```bash
git add codex-marketplace/plugins/repo-worker-pack/skills/repo-standards/templates/pre-commit
git commit -m "feat: stage only generated surfaces in pre-commit template"
```

## Task 3: Update shape standard and manifest

**Files:**
- Modify: `codex-marketplace/plugins/repo-worker-pack/skills/repo-standards/references/repository-shape-standard.md`
- Modify: `codex-marketplace/plugins/repo-worker-pack/skills/repo-standards/references/repository-shape-manifest.json`

**Interfaces:**
- None.

- [ ] **Step 1: Update `repository-shape-standard.md` pre-commit wording**

Change the bullet from `.git/hooks/pre-commit` wired to `tools/run.py ci --apply` (or an equivalent command). Note that the hook is validated by contract, not by content.

- [ ] **Step 2: Update `repository-shape-manifest.json` if needed**

Leave the `pre-commit-hook` surface as `kind: "hook"` with `source: "templates/pre-commit`". The `source` is the scaffold template; the validator now uses a contract check.

- [ ] **Step 3: Run `py -3 tools/run.py ci --check` and commit**

```bash
git add codex-marketplace/plugins/repo-worker-pack/skills/repo-standards/references/
git commit -m "docs: describe pre-commit hook as a contract, not a pinned file"
```

## Task 4: Regenerate installed skill copy and open draft PR

**Files:**
- Generated: `.agents/skills/repo-standards/`

- [ ] **Step 1: Regenerate surfaces**

```bash
py -3 tools/run.py marketplace --apply
py -3 tools/run.py mesh --apply
py -3 tools/run.py ci --check
```

- [ ] **Step 2: Commit generated surfaces**

```bash
git add .agents/skills/repo-standards/ .agents/specs/INDEX.md .agents/plans/INDEX.md .agents/docs/INDEX.md INDEX.md
git commit -m "chore: regenerate installed skill and mesh surfaces"
```

- [ ] **Step 3: Push branch and open draft PR**

```bash
git push -u origin fix/repo-standards-pre-commit
gh pr create --draft --title "repo-standards: pre-commit contract and targeted staging" --body-file pr-body.txt
```

## Self-review / readiness

- [ ] Spec: `2026-08-09-repo-standards-pre-commit-contract-design.md` covers goals, contract, validation.
- [ ] No placeholders in the plan.
- [ ] Every task ends with `ci --check` evidence.
