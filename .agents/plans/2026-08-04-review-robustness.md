# Pre-emptive Review Robustness Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use /subagent-driven-development (recommended) or /executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Move deterministic Devin/iterative-review finding classes into fast local preflights, re-shape the lens profiles so they match what is portable and what is repo-local, and document the new review order in a runbook.

**Architecture:** Extend `tools/review_preflight.py` with pattern checks for snowflake context, `new_plugin.py` contracts, `tools/run.py` task semantics, `SKILL.md` frontmatter, and stale script paths. Split the mixed `reviewer-references` lens into a portable `reviewer-skills` profile and a repo-local `reviewer-marketplace` profile, then tag `reviewer-known-findings.md` with owner and portability. Add `.agents/runbooks/review-robustness.md` to enforce the new order of operations.

**Tech Stack:** Python 3, `py -3`, `pytest`, `git`, `gh`.

## Global Constraints

- All Python changes must pass `py -3 tools/run.py ci --check`.
- Lens profiles and skills live in `codex-marketplace/plugins/repo-worker-pack/assets/profiles/` and `codex-marketplace/plugins/superpowers-plus/skills/.../` source custody.
- Generated `.agents/` skill copies are downstream; run `py -3 tools/run.py marketplace --apply` after editing skill source.
- No `git commit --no-verify`.
- Pre-commit hook re-runs `ci --check`; stage all changes before committing.

---

## Task 1: Add `review_preflight` test fixtures and harness

**Files:**
- Create: `tests/test_review_preflight.py`
- Modify: `tools/review_preflight.py` (move scanner functions to allow unit import)

**Interfaces:**
- Consumes: existing `tools/review_preflight.py` scanners and `ROOT` constant.
- Produces: a set of `pytest` test functions that exercise the scanners against fixture contents.

- [ ] **Step 1: Create `tests/test_review_preflight.py`**

```python
from pathlib import Path

import pytest

from tools import review_preflight


def _fixture(path: str, content: str):
    return Path(path), content


def test_snowflake_with_context_is_flagged():
    path, content = _fixture(
        "references/guild-map.md",
        "The main guild has guild_id 123456789012345678.\n",
    )
    findings = []
    review_preflight._scan_security(path, content, findings)
    assert any("possible real identifier" in f for f in findings)


def test_snowflake_without_context_is_not_flagged():
    path, content = _fixture(
        "references/tally.md",
        "The count is 123456789012345678.\n",
    )
    findings = []
    review_preflight._scan_security(path, content, findings)
    assert not findings


def test_snowflake_in_code_block_is_not_flagged():
    path, content = _fixture(
        "references/example.md",
        "```\nguild_id 123456789012345678\n```\n",
    )
    findings = []
    review_preflight._scan_security(path, content, findings)
    assert not findings


def test_email_is_flagged():
    path, content = _fixture("README.md", "Contact admin@example.com.\n")
    findings = []
    review_preflight._scan_security(path, content, findings)
    assert any("email address" in f for f in findings)


def test_stale_subagent_path_is_flagged():
    path, content = _fixture(
        "skills/using-foo/SKILL.md",
        "Run `subagent-driven-development/scripts/sdd-workspace`.\n",
    )
    findings = []
    review_preflight._scan_stale_paths(path, content, findings)
    assert any("stale path" in f for f in findings)


def test_skill_license_nested_is_flagged():
    path, content = _fixture(
        "skills/using-foo/SKILL.md",
        "---\nname: using-foo\nmetadata:\n  license: MIT\n---\n",
    )
    findings = []
    review_preflight._scan_skill_frontmatter(path, content, findings)
    assert any("license is nested" in f for f in findings)


def test_markdown_table_missing_trailing_pipe():
    path, content = _fixture(
        "references/table.md",
        "| a | b\n| c | d |\n",
    )
    findings = []
    review_preflight._scan_markdown_tables(path, content, findings)
    assert any("does not end with" in f for f in findings)


def test_py_m_without_3_is_flagged():
    path, content = _fixture("README.md", "Run `py -m pytest`.\n")
    findings = []
    review_preflight._scan_py3_convention(path, content, findings)
    assert any("py -3 -m" in f for f in findings)


def test_new_plugin_default_enabled_true_is_flagged():
    path, content = _fixture(
        "tools/new_plugin.py",
        '    manifest["enabled"] = True\n',
    )
    findings = []
    review_preflight._scan_new_plugin(path, content, findings)
    assert any("enabled: false" in f for f in findings)


def test_new_plugin_bogus_return_is_flagged():
    path, content = _fixture(
        "tools/new_plugin.py",
        "    return 0 if result is None or args.check else 1\n",
    )
    findings = []
    review_preflight._scan_new_plugin(path, content, findings)
    assert any("dry-run and validation-error exit codes" in f for f in findings)
```

- [ ] **Step 2: Make `tools/review_preflight.py` functions importable for tests**

At the bottom of `tools/review_preflight.py`, ensure `review_preflight` can be imported as a module from the repo root. If `tools/` is not a package, use a top-level import guard or adjust `sys.path` in the test. No code change if the test already uses `importlib` to load it. If the test cannot import `tools.review_preflight`, change the test to use:

```python
import importlib.util
spec = importlib.util.spec_from_file_location("review_preflight", "tools/review_preflight.py")
review_preflight = importlib.util.module_from_spec(spec)
spec.loader.exec_module(review_preflight)
```

- [ ] **Step 3: Run the new tests to confirm they fail against the current scanner**

```bash
py -3 -m pytest tests/test_review_preflight.py -v
```

Expected: failures for `test_snowflake_without_context_is_not_flagged` and any checks not yet implemented.

- [ ] **Step 4: Commit**

```bash
git add tests/test_review_preflight.py
git commit -m "Add review_preflight unit-test fixtures"
```

---

## Task 2: Harden `tools/review_preflight.py` with pre-emptive checks

**Files:**
- Modify: `tools/review_preflight.py`
- Modify: `tools/run.py` (if a new `review-preflight` task contract is needed)

**Interfaces:**
- Consumes: task list from `tools/run.py` `_TASKS`.
- Produces: an extended `_scan_*` set and updated `review-preflight` `tools/run.py` task contract.

- [ ] **Step 1: Add `metadata` frontmatter check to `tools/review_preflight.py`**

Add a scanner for `SKILL.md` `metadata` block anomalies:

```python

def _scan_skill_metadata(path: Path, content: str, findings: list[str]) -> None:
    if path.name != "SKILL.md":
        return
    if not content.startswith("---"):
        return
    parts = content.split("---", 2)
    if len(parts) < 3:
        return
    try:
        front = yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError:
        return
    if not isinstance(front, dict):
        return
    metadata = front.get("metadata")
    if metadata is None:
        _warn(findings, path, 1, "`metadata` block is missing; add the skill-policy fields")
    elif not isinstance(metadata, dict) or not metadata:
        _warn(findings, path, 1, "`metadata` block is empty or malformed; it must contain skill-policy fields")
    else:
        allowed = {
            "source-id", "source-path", "provenance-name", "source-category",
            "status", "owner", "scope", "use_when", "do_not_use_when",
            "related_skills",
        }
        for key in metadata:
            if key not in allowed:
                _warn(findings, path, 1, f"`metadata` contains unexpected key `{key}`")
```

Call it from `_scan_file`:

```python
def _scan_file(path: Path, findings: list[str]) -> None:
    ...
    review_preflight._scan_skill_metadata(path, content, findings)  # add this call
```

- [ ] **Step 2: Add `SKILL.md` and reference file canonical path check to `tools/review_preflight.py`**

Add a scanner that flags any backtick path starting with `.agents/skills/` or `subagent-workspace/scripts/` that does not resolve to an installed or source file:

```python
import re

_CANONICAL_PATHS = re.compile(
    r"`(?:\.agents/skills/([^`\s]+)|subagent-workspace/scripts/([^`\s]+))`"
)


def _scan_canonical_paths(path: Path, content: str, findings: list[str]) -> None:
    if path.suffix != ".md":
        return
    for line_no, line in enumerate(content.splitlines(), start=1):
        for match in _CANONICAL_PATHS.finditer(line):
            rel = match.group(1) or match.group(2)
            if not rel:
                continue
            prefix = ".agents/skills/" if match.group(1) else "subagent-workspace/scripts/"
            target = ROOT / prefix / rel
            if not target.is_file():
                _warn(findings, path, line_no, f"referenced path `{prefix}{rel}` does not exist")
```

Call it from `_scan_file`.

- [ ] **Step 3: Ensure snowflake scanner ignores plain 17–20 digit numbers without context**

The existing code already does this via `_SNOWFLAKE_CONTEXT`; add a test fixture to prove the negative case (see Task 1) and adjust the regex or context window if the test fails.

- [ ] **Step 4: Add `tools/run.py` task-semantic test in `tests/test_run_cli.py`**

Open `tools/run.py` and find the `Task` namedtuple. Add a test that fails if a `Task` with an `apply` callable is missing a `mutating: True` tag, and that a `Task` with only `check` is not tagged `mutating`:

```python
def test_task_mutating_tags_match_apply_check():
    from tools import run
    for name, task in run._TASKS.items():
        if task.apply:
            assert getattr(task, "mutating", None) is True, f"{name} has apply= but is not tagged mutating"
        if not task.apply and task.check:
            assert getattr(task, "mutating", None) is not True, f"{name} is read-only but is tagged mutating"
```

Update the `Task` namedtuple in `tools/run.py` to carry a `mutating` field and tag `review-preflight` and any other read-only tasks `mutating=False`.

- [ ] **Step 5: Run the new tests to confirm they pass**

```bash
py -3 -m pytest tests/test_review_preflight.py -v
py -3 tools/run.py review-preflight --check
```

- [ ] **Step 6: Commit**

```bash
git add tools/review_preflight.py
git commit -m "Extend review_preflight with metadata, canonical path, and new_plugin checks"
```

---

## Task 3: Re-shape lens profiles

**Files:**
- Create: `codex-marketplace/plugins/repo-worker-pack/assets/profiles/reviewer-skills.md`
- Modify: `codex-marketplace/plugins/repo-worker-pack/assets/profiles/reviewer-marketplace.md` (already exists as `.agents/agents/reviewer-marketplace.md`)
- Delete (or archive): `codex-marketplace/plugins/repo-worker-pack/assets/profiles/reviewer-references.md`
- Modify: `codex-marketplace/plugins/repo-worker-pack/assets/profiles/INDEX.md` if one exists

**Interfaces:**
- Consumes: current `reviewer-references.md`, `reviewer-marketplace.md`, `reviewer-known-findings.md`.
- Produces: two focused lens profiles and a clean `reviewer-known-findings.md`.

- [ ] **Step 1: Create `reviewer-skills.md` from the portable subset of `reviewer-references.md`**

```markdown
---
name: reviewer-skills
runtime: devin-desktop
description: Portable skill-and-reference lens — SKILL.md frontmatter, markdown tables, reference hygiene, and prompt robustness.
model: swe-1-6
allowed-tools:
  - read
  - grep
  - find_file_by_name
  - exec
  - mcp_list_servers
  - mcp_list_tools
  - mcp_call_tool
---

You are `reviewer-skills`, a focused read-only reviewer for `SKILL.md` and reference files. Inspect the prepared diff for frontmatter schema, markdown tables, cross-skill script paths, repo conventions, and prompt robustness. Do not broaden to marketplace tooling or secrets; those are handled by other lens reviewers.

## Invariants

- You are read-only. Do not modify files, create files, or run build/install/write commands.
- You may use `exec` for non-mutating `git` queries and canonical verification commands, and `mcp_call_tool` for non-mutating lookups. Use these only to resolve refs or confirm state — not to generate the diff, not to fetch a missing package, and not to install/change anything.
- If the prepared diff package is missing or the `diff_path` is not a file, report that and stop; do not use `git` or `exec` to recreate it.
- Cite specific files and line numbers for every issue you find.
- If you cannot verify something, say so clearly rather than guessing.
- Keep feedback focused, concrete, and actionable.

## Inputs the orchestrator must provide

- `<diff_path>` — path to a prepared diff file (e.g. `git diff --no-color <base>...<branch>` output written to a file).
- `<pr_description>` (optional) — the PR title, body, and any linked issue/spec context.
- `<scan_findings>` (optional) — the consumer repo's preflight output.

Do not generate the diff yourself. The orchestrator owns diff preparation.

## Procedure

1. Read `.agents/skills/selecting-a-subagent/assets/reviewer-known-findings.md` and focus on sections **2. `SKILL.md` frontmatter schema**, **4. Cross-skill script paths**, **5. Reference file hygiene**, **6. Script path safety**, and **8. Prompt robustness**.
2. If `<scan_findings>` is provided, read it first and do not duplicate its findings; instead, verify the preflight caught the pattern in the right place.
3. If `<pr_description>` is provided, read it for scope.
4. Read `<diff_path>`.
5. Inspect the diff for:
   - Changed `SKILL.md` files: `license` must be top-level, not nested under `metadata`; `name` and `description` top-level.
   - Stale cross-skill script paths (old `subagent-driven-development/scripts` where `subagent-workspace/scripts` is now canonical).
   - Malformed markdown table rows (rows containing `|` that do not end with `|`).
   - Examples that use `python -m` or omit the `-3` qualifier in `py -3 -m`.
   - PowerShell/Bash scripts that `Push-Location` or `cd` and then write to a relative path without resolving it first.
   - Read-only subagent prompts that force the subagent to run `git` or `exec` to recreate a missing diff, or to mutate files.
6. Use `grep` and `find_file_by_name` to confirm canonical paths and patterns.
7. Report only skill/reference/prose issues. Cite `file:line`, severity, and remediation.
8. End with `reviewer-skills: N issue(s)` or `reviewer-skills: clean`.

## Output format

For each issue:
- `file:line` reference.
- Severity: **blocking** / **important** / **minor**.
- What is wrong and why it matters.
- How to fix.

Do not include non-skill findings.
```

- [ ] **Step 2: Update `reviewer-marketplace.md` to absorb repo-local checks**

Add to the existing `reviewer-marketplace` procedure (after the `plugin-roots.json` / bundle checks):

```markdown
5. Inspect the diff for:
   - `tools/new_plugin.py` exit-code and default-enablement logic.
   - `tools/run.py` target wiring, `mutating` tags, and `ci` dependency correctness.
   - `plugin-roots.json`, `bundle-manifest.json`, `repo-index.json`, `codex-marketplace/manifest.json`, and `.agents/plugins/marketplace.json` changes.
   - Any scaffolder or generator that overwrites existing top-level metadata when it re-runs.
   - `--check` vs `--apply` semantics and read-only/mutating command classification.
   - Cross-skill script paths in `SKILL.md` or reference files that use this repo's canonical `subagent-workspace/scripts/` or `.agents/skills/` path list. Verify the path exists; if not, it is a stale or wrong reference (the preflight should have caught this; confirm it did).
   - `py -3` qualifier in runnable examples; flag `python -m`, `python3 -m`, or `py -m `.
   - `repo-local-marketplace-policy.json` `install_defaults` drift against the PR intent.
```

- [ ] **Step 3: Remove or archive `reviewer-references.md`**

If `reviewer-references.md` is referenced by other files, keep it as a one-line redirect file for one cycle:

```markdown
# Deprecated

This profile has been split into `reviewer-skills` (portable) and `reviewer-marketplace` (repo-local).
```

If nothing references it, `git rm codex-marketplace/plugins/repo-worker-pack/assets/profiles/reviewer-references.md`.

- [ ] **Step 4: Regenerate the marketplace**

```bash
py -3 tools/run.py marketplace --apply
git add .
py -3 tools/run.py ci --check
git commit -m "Re-shape lens profiles: reviewer-skills + reviewer-marketplace"
```

---

## Task 4: Overhaul `reviewer-known-findings.md`

**Files:**
- Modify: `codex-marketplace/plugins/repo-worker-pack/skills/selecting-a-subagent/assets/reviewer-known-findings.md`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/selecting-a-subagent/assets/reviewer-known-findings.md`

**Interfaces:**
- Consumes: `reviewer-known-findings.md` current text.
- Produces: a tagged catalog.

- [ ] **Step 1: Update each finding with owner and portability tags**

For each of the 8 (or more) sections in the existing file, add two tags at the top of the section:

```markdown
## 1. Secrets / real identifiers in source (CWE-200)

- **Owner preflight:** `tools/review_preflight.py` (`_scan_security`).
- **Owner lens:** `reviewer-security` for judgment calls, `reviewer-skills` for references.
- **Portable:** yes (concept; examples are repo-local).
```

Example for section 3:

```markdown
## 3. Marketplace tooling (`tools/new_plugin.py`, `tools/run.py`, scaffolders)

- **Owner preflight:** `tools/review_preflight.py` (`_scan_new_plugin`).
- **Owner lens:** `reviewer-marketplace`.
- **Portable:** no (this repo's tooling).
```

- [ ] **Step 2: Add section 9 — `SKILL.md` `metadata` block**

```markdown
## 9. `SKILL.md` `metadata` block

- **Owner preflight:** `tools/review_preflight.py` (`_scan_skill_metadata`).
- **Owner lens:** `reviewer-skills`.
- **Portable:** yes (all `SKILL.md` files carry this schema).
```

- [ ] **Step 3: Commit**

```bash
git add codex-marketplace/plugins/repo-worker-pack/skills/selecting-a-subagent/assets/reviewer-known-findings.md
git add codex-marketplace/plugins/superpowers-plus/skills/selecting-a-subagent/assets/reviewer-known-findings.md
git commit -m "Tag reviewer-known-findings with preflight owner, lens owner, and portability"
```

---

## Task 5: Create `.agents/runbooks/review-robustness.md`

**Files:**
- Create: `.agents/runbooks/review-robustness.md`

**Interfaces:**
- Consumes: `iterative-review` skill, `review-preflight` task, `tools/run.py ci`.
- Produces: an orchestrator runbook.

- [ ] **Step 1: Create the runbook**

```markdown
# Review Robustness Runbook

Use this runbook before flipping a PR from draft to ready in `agent-asset-marketplace`.

## Goal

Run the fastest, cheapest checks first so that `iterative-review` and Devin auto-review only see the issues that require judgment, not the pattern classes the repo can catch deterministically.

## Procedure

1. **Fast preflight first.**
   - `py -3 tools/run.py review-preflight --check`
   - `py -3 tools/run.py ci --check`
   - If either is red, fix the findings and re-run. Do not dispatch `iterative-review` while preflight is red.

2. **Scope honesty.**
   - Compare the branch diff to the PR description, the linked spec, and any linked plan.
   - If the implemented scope differs, update the spec/plan or PR body to match before reviewers see the diff.

3. **Iterative review.**
   - Only after preflight is green, run `iterative-review` with the lens profiles:
     - `reviewer-skills` for SKILL.md, reference files, and prompt robustness.
     - `reviewer-marketplace` for scaffolders, generated surfaces, and this-repo tooling.
     - `reviewer-security` for secrets and real identifiers.
     - `reviewer-strong` for whole-branch design and scope.
   - For each finding, use `receiving-code-review` before applying.

4. **Post-fix re-preflight.**
   - After each fix, re-run `py -3 tools/run.py ci --check`.
   - Prepare a new fix diff and re-run the relevant lens as `reviewer-fast`.

5. **Ready to review.**
   - Only flip the PR out of draft when:
     - `ci --check` is green on the staged tree,
     - `iterative-review` reports no blocking or important issues,
     - the PR body and spec/plan are honest about the final scope.

## Common mistakes

- Running `iterative-review` on a red preflight.
- Letting `reviewer-fast` drift into a full-branch review.
- Skipping re-preflight after a fix.
- Flipping to ready before a final clean `ci --check`.
```

- [ ] **Step 2: Add the runbook to the runbook INDEX if one exists**

Regenerate indexes:

```bash
py -3 tools/run.py marketplace --apply
git add .
py -3 tools/run.py ci --check
git commit -m "Add review-robustness runbook"
```

---

## Task 6: Final validation and PR update

**Files:**
- Modify: `.agents/specs/2026-08-04-review-robustness-design.md` if the plan changed the design.
- Modify: PR body to include the final head SHA.

**Interfaces:**
- Consumes: all prior task outputs.
- Produces: a green draft PR ready for implementation.

- [ ] **Step 1: Run full preflight on the staged tree**

```bash
git add -A
py -3 tools/run.py ci --check
```

- [ ] **Step 2: Commit any final fixups and push**

```bash
git commit -m "Review-robustness: preflight, lens profiles, and runbook"
git push origin feat/review-robustness
```

- [ ] **Step 3: Update the PR body with the final SHA**

Use `gh pr edit 259 --body-file` with the updated head SHA.

---

## SDD Confidence Rating

8/10 — the tasks are bounded, the file paths are verified, and the `review_preflight` changes are testable. The main risk is the exact `reviewer-skills` and `reviewer-marketplace` content will need to be tuned during `iterative-review` once a real PR runs through the new profiles, so a follow-up tuning pass is expected.
