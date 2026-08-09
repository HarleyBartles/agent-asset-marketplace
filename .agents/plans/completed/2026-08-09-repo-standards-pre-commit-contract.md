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
- Produces: `_check_hook_contract(hook_path: Path) -> list[str]`.

- [x] **Step 1: Read the current `kind == "hook"` branch in `_check_surface`**

- [x] **Step 2: Write `_check_hook_contract`**

```python
def _check_hook_contract(hook_path: Path) -> list[str]:
    findings: list[str] = []
    if not hook_path.is_file():
        findings.append("pre-commit hook is not a regular file")
        return findings

    # Best-effort executability check. On POSIX, an executable bit is
    # required; if it is missing, a shebang is accepted as a fallback.
    # On Windows the executable-bit check is skipped.
    if os.name != "nt" and not os.access(hook_path, os.X_OK):
        try:
            shebang = hook_path.read_bytes()[:2]
            if shebang != b"#!":
                findings.append("pre-commit hook is not executable and has no shebang")
        except OSError as exc:
            findings.append(f"pre-commit hook cannot be read: {exc}")

    try:
        text = hook_path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        findings.append(f"pre-commit hook cannot be read: {exc}")
        return findings

    # Scan non-comment, non-empty lines for the required contract elements.
    non_comment = "\n".join(
        line for line in text.splitlines()
        if line.strip() and not line.strip().startswith("#")
    )

    has_guard = "set -euo pipefail" in non_comment
    if not has_guard:
        has_guard = (
            "set -e" in non_comment and "set -u" in non_comment and "set -o pipefail" in non_comment
        )
    if not has_guard:
        findings.append("pre-commit hook missing errexit/nounset/pipefail guard")

    ci_apply = "tools/run.py ci --apply" in non_comment
    if not ci_apply:
        for prefix in ("py -3", "python3", "python"):
            if f"{prefix} tools/run.py ci --apply" in non_comment:
                ci_apply = True
                break
    if not ci_apply:
        findings.append("pre-commit hook must run 'tools/run.py ci --apply'")
    return findings
```

- [x] **Step 3: Replace byte comparison in `_check_surface` for `kind == "hook"`**

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

- [x] **Step 4: Run `py -3 tools/run.py ci --check` and commit**

```bash
git add codex-marketplace/plugins/repo-worker-pack/skills/repo-standards/scripts/repo_standards.py
git commit -m "feat: validate pre-commit hook by contract, not byte-for-byte"
```

## Task 2: Tighten the default pre-commit template staging

**Files:**
- Modify: `codex-marketplace/plugins/repo-worker-pack/skills/repo-standards/templates/pre-commit`

**Interfaces:**
- None; shell script.

- [x] **Step 1: Replace the final `git add -A` with targeted staging**

Keep the `ci --apply` call, then add:

```bash
# Re-stage any tracked files the hook may have modified.
git diff --name-only --diff-filter=M | while IFS= read -r file; do
  git add "$file" 2>/dev/null || true
done

# Stage canonical generated surfaces. Glob pathspecs avoid scanning the
# working tree with `find` and do not stage arbitrary untracked files.
git add -- ':(glob)**/INDEX.md' 2>/dev/null || true
git add -- ':(glob)**/INDEX.json' 2>/dev/null || true
git add -- ':(glob)**/.provenance.json' 2>/dev/null || true
git add -- ':(glob)codex-marketplace/plugin-roots.json' 2>/dev/null || true
git add -- ':(glob).agents/plugins/marketplace.json' 2>/dev/null || true
git add -- ':(glob)codex-marketplace/manifest.json' 2>/dev/null || true
```

Use `|| true` so a missing file does not abort the hook.

- [x] **Step 2: Run `py -3 tools/run.py ci --check` and commit**

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

- [x] **Step 1: Update `repository-shape-standard.md` pre-commit wording**

Change the bullet from `.git/hooks/pre-commit` wired to `tools/run.py ci --apply` (or an equivalent command). Note that the hook is validated by contract, not by content.

- [x] **Step 2: Update `repository-shape-manifest.json` if needed**

No edit is needed. The `pre-commit-hook` surface remains `kind: "hook"` with `source: "templates/pre-commit"`; these fields already describe the scaffold template correctly, and the validator change is behavioral.

- [x] **Step 3: Run `py -3 tools/run.py ci --check` and commit**

```bash
git add codex-marketplace/plugins/repo-worker-pack/skills/repo-standards/references/
git commit -m "docs: describe pre-commit hook as a contract, not a pinned file"
```

## Task 4: Regenerate installed skill copy and open draft PR

**Files:**
- Generated: `.agents/skills/repo-standards/`

- [x] **Step 1: Regenerate surfaces**

```bash
py -3 tools/run.py marketplace --apply
py -3 tools/run.py mesh --apply
py -3 tools/run.py ci --check
```

- [x] **Step 2: Commit generated surfaces**

```bash
git add .agents/skills/repo-standards/ .agents/specs/INDEX.md .agents/plans/INDEX.md .agents/docs/INDEX.md INDEX.md
git commit -m "chore: regenerate installed skill and mesh surfaces"
```

- [x] **Step 3: Push branch and open draft PR**

```bash
git push -u origin fix/repo-standards-pre-commit
gh pr create --draft --title "repo-standards: pre-commit contract and targeted staging" --body-file pr-body.txt
```

## Self-review / readiness

- [x] Spec: `2026-08-09-repo-standards-pre-commit-contract-design.md` covers goals, contract, validation.
- [x] No placeholders in the plan.
- [x] Every task ends with `ci --check` evidence.
