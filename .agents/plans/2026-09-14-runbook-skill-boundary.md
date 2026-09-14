# Runbook/Skill Boundary and Composition Model Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `subagent-driven-development` (recommended) or `executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship the capability-versus-composition model in `repo-standards`, fix the completed-artifacts duplication chain against `cleanup-custody`, and align this repo's own runbooks and doctrine to the new contract.

**Architecture:** The runbook standard gains a surface taxonomy, four named skill shapes, a composition rule, and a required-section runbook contract. The scaffolder emits the contract skeleton, and `repo_standards.py --check` gains a WARN-level check that each `.agents/runbooks/*.md` declares `## Required skills`. `cleanup-custody` gains the canonical promote-before-removal step; the completed-artifacts template shrinks to doctrine plus an ownership line; local runbooks, root `AGENTS.md`, and `non-repo-locations-policy.md` lose restated portable method.

**Tech Stack:** Markdown doctrine/templates, Python 3 (`repo_standards.py`, `scaffold_runbooks.py`), pytest contract tests in `tests/test_repo_standards.py`, `tools/run.py` task bus.

**Spec:** `.agents/specs/2026-09-14-runbook-composition-model-design.md`

**Execution Strategy:** `executing-plans` - sequential, tightly coupled edits to shared doctrine and validator files. Tasks are small; subagent fan-out adds handoff cost without parallelism to exploit.

## Global Constraints

- Canonical skill/template source lives under `codex-marketplace/plugins/repo-worker-pack/skills/`. Never edit the installed copies under `.agents/skills/` by hand; refresh them via `py -3 tools/run.py installed-skills --apply`.
- `.agents/doctrine/completed-artifacts.md` must remain byte-identical to `codex-marketplace/plugins/repo-worker-pack/skills/repo-standards/templates/completed-artifacts.md` (manifest `check_content`).
- The WARN check prints `WARN:` lines and must never change the exit code or emit `DRIFT:` lines.
- Run commands with `py -3` (Windows). Use `;` not `&&` to chain in PowerShell.
- Match existing documentation voice: no emojis, no em-dashes.
- Validation: contract tests via `py -3 -m pytest tests/test_repo_standards.py -v`; canonical gate `py -3 tools/run.py ci --check --diagnostics` for uncommitted verification only; normal commits go through the tracked pre-commit hook.

---

### Task 1: Runbook standard gains taxonomy, skill shapes, and the composition contract

**Files:**
- Modify: `codex-marketplace/plugins/repo-worker-pack/skills/repo-standards/references/repository-runbook-standard.md`

**Interfaces:**
- Produces: the canonical wording Tasks 2-4 quote (skeleton section names, runbook names). Later tasks must match these section headings exactly: `## Required skills`, `## Evidence contract`, `## Prohibited combinations`.

- [ ] **Step 1: Insert the taxonomy and skill-shape sections** after the "Core runbook set" section (after line ~34, before "Pull request runbook policy"):

```markdown
## Surface taxonomy

Route content by this test:

| Question | Owning surface |
| --- | --- |
| What must remain true? | doctrine (`.agents/doctrine/`) |
| What exact shape must participants exchange? | contract (`.agents/contracts/`) |
| How do I perform one focused judgment or work? | capability skill |
| How does this repo combine capabilities for this class of change? | runbook (`.agents/runbooks/`) |
| Can a machine enforce it cheaply? | code or configuration |

## Skill shapes

- **Router** - bootstrap composition and stage routing (for example
  `using-superpowers-plus`).
- **Stage/workflow skill** - portable orchestration of a generic stage or a
  bounded artifact workflow. It owns a portable stage verb and delegates repo
  specifics to the local runbook.
- **Capability skill** - one focused verb or judgment. It may delegate to a
  narrower prerequisite skill.
- **Doctrine/policy carrier** - portable doctrine shipped in skill packaging;
  it routes to policy references and does not own a workflow verb.

## Composition rule

- Runbooks may compose peer skills.
- Capability skills must not sequence a repository delivery lifecycle.
- Stage/workflow skills orchestrate a portable stage and read the local
  runbook for binding; they never restate repo specifics.
- Doctrine and contracts never orchestrate.
```

- [ ] **Step 2: Replace the "Allowed additional runbooks" retention rule** (lines 55-57) with the runbook contract. Keep the allowed-names list; replace the trailing paragraph with:

```markdown
A runbook is the repository's composition manifest for a class of change.
Each runbook carries these sections:

- `When` - the change class or trigger it covers.
- `Required skills` - the skills the composition invokes (the owning stage
  skill for stage runbooks).
- `Composition` - the order or conditions under which the skills apply.
- `Doctrine and contracts` - local truths and shapes that constrain it.
- `Local commands and paths` - repository commands, paths, and exceptions.
- `Evidence contract` - what the combined workflow must prove.
- `Prohibited combinations` - combinations not legitimate here, or `none`.

Runbooks name and sequence owners; they must not repeat portable doctrine or
skill internals.
```

- [ ] **Step 3: Add the completion runbook to the allowed list** (after `code-style.md` in that list):

```markdown
- `completing-plans.md`
```

- [ ] **Step 4: Verify** - `grep -n "Required skills" codex-marketplace/plugins/repo-worker-pack/skills/repo-standards/references/repository-runbook-standard.md` shows both the contract bullet and no other matches; `py -3 tools/run.py repo-standards --check` still passes.

- [ ] **Step 5: Commit** - `git add` the file; commit `docs(repo-standards): add surface taxonomy and runbook composition contract`.

---

### Task 2: Scaffolder emits the composition skeleton and completing-plans title

**Files:**
- Modify: `codex-marketplace/plugins/repo-worker-pack/skills/repo-standards/scripts/scaffold_runbooks.py`
- Test: `tests/test_repo_standards.py`

**Interfaces:**
- Consumes: section names from Task 1 Step 2.
- Produces: `_runbook_content(name)` returns the composition skeleton; `RUNBOOK_TITLES` includes `"completing-plans.md"`.

- [ ] **Step 1: Write the failing test** - append to `tests/test_repo_standards.py`:

```python
def test_scaffold_runbooks_stub_is_composition_manifest(tmp_path: Path) -> None:
    import importlib.util as _ilu
    spec = _ilu.spec_from_file_location(
        "scaffold_runbooks_under_test", SKILL_ROOT / "scaffold_runbooks.py"
    )
    mod = _ilu.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    content = mod._runbook_content("security.md")
    for heading in (
        "## When",
        "## Required skills",
        "## Composition",
        "## Doctrine and contracts",
        "## Local commands and paths",
        "## Evidence contract",
        "## Prohibited combinations",
    ):
        assert heading in content
    assert "completing-plans.md" in mod.RUNBOOK_TITLES
```

- [ ] **Step 2: Run test to verify it fails** - `py -3 -m pytest tests/test_repo_standards.py::test_scaffold_runbooks_stub_is_composition_manifest -v` Expected: FAIL (missing headings).

- [ ] **Step 3: Update the scaffolder** - in `scaffold_runbooks.py`, add `"completing-plans.md": "Completion runbook"` to `RUNBOOK_TITLES` and replace the stub body in `_runbook_content` with:

```python
    return (
        f"# {title}\n\n"
        "## When\n\n"
        "<!-- The class of change or trigger this runbook covers. -->\n\n"
        "## Required skills\n\n"
        "<!-- The skills this composition invokes; the owning stage skill for stage runbooks. -->\n\n"
        "## Composition\n\n"
        "<!-- Order or conditions under which the required skills apply. -->\n\n"
        "## Doctrine and contracts\n\n"
        "<!-- Local truths and shapes that constrain this composition. -->\n\n"
        "## Local commands and paths\n\n"
        "<!-- Repository commands, paths, and exceptions. -->\n\n"
        "## Evidence contract\n\n"
        "<!-- What the combined workflow must prove before it is complete. -->\n\n"
        "## Prohibited combinations\n\n"
        "<!-- Combinations explicitly not legitimate here, or `none`. -->\n"
    )
```

- [ ] **Step 4: Run test to verify it passes** - same pytest invocation. Expected: PASS.

- [ ] **Step 5: Commit** - `feat(repo-standards): scaffold runbooks as composition manifests`.

---

### Task 3: WARN-level runbook-composition check in `repo_standards.py`

**Files:**
- Modify: `codex-marketplace/plugins/repo-worker-pack/skills/repo-standards/scripts/repo_standards.py`
- Test: `tests/test_repo_standards.py`

**Interfaces:**
- Produces: `_check_runbook_composition(repo_root: Path) -> list[str]` returning warning strings; `main()` prints each as `WARN: <msg>` in `--check` mode without affecting findings or exit code.

- [ ] **Step 1: Write the failing tests** - append to `tests/test_repo_standards.py`:

```python
def test_runbook_composition_warns_on_missing_required_skills(tmp_path: Path) -> None:
    runbooks = tmp_path / ".agents" / "runbooks"
    runbooks.mkdir(parents=True)
    (runbooks / "testing.md").write_text("# Testing\n\nLocal commands only.\n", encoding="utf-8")
    warnings = repo_standards._check_runbook_composition(tmp_path)
    assert any("testing.md" in w for w in warnings)


def test_runbook_composition_quiet_when_section_present(tmp_path: Path) -> None:
    runbooks = tmp_path / ".agents" / "runbooks"
    runbooks.mkdir(parents=True)
    (runbooks / "testing.md").write_text(
        "# Testing\n\n## Required skills\n\n- `test-driven-development`\n", encoding="utf-8"
    )
    assert repo_standards._check_runbook_composition(tmp_path) == []


def test_runbook_composition_ignores_agents_md_and_absent_dir(tmp_path: Path) -> None:
    assert repo_standards._check_runbook_composition(tmp_path) == []
    runbooks = tmp_path / ".agents" / "runbooks"
    runbooks.mkdir(parents=True)
    (runbooks / "AGENTS.md").write_text("# Router\n", encoding="utf-8")
    assert repo_standards._check_runbook_composition(tmp_path) == []
```

- [ ] **Step 2: Run tests to verify they fail** - `py -3 -m pytest tests/test_repo_standards.py -k runbook_composition -v` Expected: FAIL (`AttributeError`).

- [ ] **Step 3: Implement the check** - add to `repo_standards.py` near `_check_surface`:

```python
def _check_runbook_composition(repo_root: Path) -> list[str]:
    warnings: list[str] = []
    runbooks_dir = repo_root / ".agents" / "runbooks"
    if not runbooks_dir.is_dir():
        return warnings
    for path in sorted(runbooks_dir.glob("*.md")):
        if path.name == "AGENTS.md":
            continue
        text = path.read_text(encoding="utf-8")
        if "## Required skills" not in text:
            warnings.append(
                f"{path.relative_to(repo_root).as_posix()}: missing '## Required skills' composition section"
            )
    return warnings
```

In `main()`, inside the `if args.check or not args.apply:` block before the findings verdict, print warnings:

```python
        for warning in _check_runbook_composition(repo_root):
            print(f"WARN: {warning}")
```

- [ ] **Step 4: Run tests to verify they pass** - same `-k runbook_composition` invocation. Expected: 3 PASS.

- [ ] **Step 5: Verify WARN does not fail the gate** - run `py -3 codex-marketplace/plugins/repo-worker-pack/skills/repo-standards/scripts/repo_standards.py --check` from the worktree root. Expected: `WARN:` lines for this repo's current runbooks (they are fixed in Task 7) plus `OK repo-standards: all surfaces present`, exit 0.

- [ ] **Step 6: Commit** - `feat(repo-standards): warn on runbooks missing a composition section`.

---

### Task 4: Completed-artifacts template becomes doctrine-only with an ownership line

**Files:**
- Modify: `codex-marketplace/plugins/repo-worker-pack/skills/repo-standards/templates/completed-artifacts.md`
- Modify: `.agents/doctrine/completed-artifacts.md` (must stay byte-identical)

- [ ] **Step 1: Write the new template content** (replace the whole file, both paths):

```markdown
## Scope

Completed planning-artifact custody truth for this repository.

## Doctrine

Completed plans, specifications, roadmaps, checkpoints, and similar execution
artifacts are not retained in the tracked repository. Git history is the
immutable record. A completed artifact is not an authority: do not use it as
a source of canonical command sequences, a template for current
implementation, or an authoritative example of repo conventions. Completion
does not create a durable exception for an artifact type.

When a completed artifact leaves the tracked tree, an optional disposable
convenience copy may live at
`<main-checkout>/../_agent-scratch/<repo-name>/completed/<artifact-type>/`
with no manifest, retention promise, or evidentiary role.

Durable content promotes before removal: enduring architecture decisions
belong in `adr/`; operating rules belong in `.agents/doctrine/` or
`.agents/runbooks/`.

## Ownership

`cleanup-custody` owns the custody classification and the
promotion-before-removal method. The `completing-plans.md` runbook (or the
repo's mapped completion runbook) owns the composition that applies this
doctrine. For current conventions, use `.agents/doctrine/*.md`,
`.agents/runbooks/*.md`, and active plans and specs.
```

- [ ] **Step 2: Verify content parity** - `py -3 codex-marketplace/plugins/repo-worker-pack/skills/repo-standards/scripts/repo_standards.py --check` passes the `completed-artifacts-doctrine` content check.

- [ ] **Step 3: Commit** - `docs(repo-standards): bound completed-artifacts doctrine to cleanup-custody`.

---

### Task 5: `cleanup-custody` gains the canonical promote-before-removal step

**Files:**
- Modify: `codex-marketplace/plugins/repo-worker-pack/skills/cleanup-custody/SKILL.md`
- Regenerate: `.agents/skills/cleanup-custody/` (via installed-skills)

- [ ] **Step 1: Add the section** to `SKILL.md` immediately after the "Custody ladder" block:

```markdown
## Promotion before removal

Before a surface leaves `keep_live` custody, migrate durable content to its
owning surface: enduring architecture decisions to the repo's ADR home,
operating rules to current doctrine or runbooks, and evidence to its declared
proof surface. The repo's local binding names the destinations; this skill
owns the step. A removal that strands durable decisions in deleted or
scratch-only material is not GREEN.
```

- [ ] **Step 2: Refresh the installed copy** - `py -3 tools/run.py installed-skills --apply` (add `--allow-shared-checkout` only if it requests it). Verify `grep -n "Promotion before removal" .agents/skills/cleanup-custody/SKILL.md` matches.

- [ ] **Step 3: Commit** - `feat(cleanup-custody): own the promotion-before-removal step`.

---

### Task 6: Shape standard compresses restated doctrine; policy template maps completion runbook

**Files:**
- Modify: `codex-marketplace/plugins/repo-worker-pack/skills/repo-standards/references/repository-shape-standard.md`
- Modify: `codex-marketplace/plugins/repo-worker-pack/skills/repo-standards/templates/repo-runbook-policy.md`

- [ ] **Step 1: Compress "Completed artifacts"** (lines 91-99) to:

```markdown
## Completed artifacts

The `completed-artifacts-doctrine` surface carries this repo's custody truth
for finished planning artifacts. `cleanup-custody` owns the custody method and
promotion-before-removal step; the mapped completion runbook owns the removal
composition.
```

- [ ] **Step 2: Compress "SDD scratch"** (lines 71-89): keep the `.gitignore` requirements and the `scaffold-gitignore` sentence (shape surfaces); replace the path diagram and "outputs are not repo resident" paragraph with a pointer:

```markdown
## SDD scratch

The off-repo `_agent-scratch` layout, naming, sanitization, and cleanup rules
live in [scratch-workspace-policy.md](scratch-workspace-policy.md).

The root `.gitignore` must not contain a stale in-repo rule such as:

```gitignore
.agents/superpowers/sdd/**
!.agents/superpowers/sdd/.gitignore
```

`scaffold-gitignore` removes the stale rule and any leftover `.agents/superpowers/sdd/.gitignore` directory from older repo layouts.
```

- [ ] **Step 3: Add the completion mapping** to `templates/repo-runbook-policy.md` after the `code-style.md` row:

```markdown
| completing-plans.md | `.agents/runbooks/completing-plans.md` |  |
```

- [ ] **Step 4: Commit** - `docs(repo-standards): point shape standard at owning custody surfaces`.

---

### Task 7: Local runbooks declare their composition

**Files:**
- Modify: `.agents/runbooks/completing-plans.md` (full recast)
- Modify: `.agents/runbooks/marketplace-generation.md` (add `## Required skills` + evidence line)
- Modify: `.agents/runbooks/pr.md` (add `## Required skills`; compress the `ci --check` guidance to a pointer)
- Modify: each remaining `.agents/runbooks/*.md` (`design.md`, `planning.md`, `implementing.md`, `code-review.md`, `security.md`, `testing.md`, `code-style.md`, `skill-authoring.md`, `repo-doctrine.md`) - add a `## Required skills` section naming the owners. Read each file first and name the skills it already invokes; do not invent compositions.

Reference for required-skill content (adjust to what each file actually says):

| Runbook | Required skills |
| --- | --- |
| design.md | `brainstorming` (owning stage), `handoff-gates` (spec readiness) |
| planning.md | `writing-plans` (owning stage), `handoff-gates` (plan readiness) |
| implementing.md | `executing-plans` or `subagent-driven-development` (stage lane), `test-driven-development` |
| code-review.md | `requesting-code-review`, `receiving-code-review`, `unslop-profiles` (lenses) |
| security.md | `unslop-profiles` security profile, `risk-gates` |
| testing.md | `test-driven-development`, `verification-before-completion` |
| code-style.md | `writing-with-clarity` (prose surfaces) or `none - style contract only` |
| skill-authoring.md | `writing-skills`, `repo-standards` (script contract) |
| repo-doctrine.md | `base-doctrine`, `repo-worker-base` |
| pr.md | `publishing-source`, `repo-worker-base`, `verification-before-completion` |
| marketplace-generation.md | `generating-agent-mesh`, `refreshing-installed-skills`, `verification-before-completion` |
| completing-plans.md | `cleanup-custody`, `generating-agent-mesh`, `verification-before-completion` |

- [ ] **Step 1: Recast `completing-plans.md`** as a full composition manifest:

```markdown
# Completing planning artifacts

## When

An implementation PR completes an in-flight plan, specification, roadmap,
checkpoint, or similar planning artifact.

## Required skills

- `cleanup-custody` - custody classification and the promotion-before-removal
  step.
- `generating-agent-mesh` - regenerate the index mesh after removal.
- `verification-before-completion` - completion evidence.

## Composition

1. Invoke `cleanup-custody` and classify each artifact. In-flight artifacts
   stay `keep_live` while they govern implementation and review.
2. Apply promotion-before-removal: enduring architecture decisions to `adr/`,
   operating rules to `.agents/doctrine/` or `.agents/runbooks/`.
3. Remove the exact tracked artifacts with Git-aware deletion.
4. Optionally place a disposable convenience copy under
   `_agent-scratch/<repo-name>/completed/<artifact-type>/`. This centralized
   disposable store is the only scratch custody for finished paperwork; a copy
   is optional and proves nothing.
5. Regenerate the mesh and commit the resulting tree in the completing PR.

## Doctrine and contracts

- `.agents/doctrine/completed-artifacts.md` - completed artifacts are not
  retained, are not authority, and git history is the immutable record.

## Local commands and paths

- `py -3 tools/run.py mesh --apply` regenerates the index mesh.
- `adr/` holds durable architecture decisions.

## Evidence contract

Git history is the immutable record. Completion creates no manifest, count,
archive index, or recurring PR-reporting duty.

## Prohibited combinations

- Do not treat a completed artifact as a source of canonical commands, an
  implementation template, or an example of current conventions.
- Do not retain completed artifacts under a `completed/` directory inside
  `.agents/plans/`, `.agents/specs/`, or `.agents/roadmaps/`.
```

- [ ] **Step 2: Update `marketplace-generation.md`** - add near the top:

```markdown
## Required skills

- `generating-agent-mesh` - index mesh regeneration.
- `refreshing-installed-skills` - installed-skill refresh.
- `verification-before-completion` - regeneration and validation evidence.
```

And add to "Validation Standards": `Evidence contract: regeneration plus `tools/run ci --check` green on the committed tree is the completion proof.`

- [ ] **Step 3: Update `pr.md`** - add `## Required skills` (`publishing-source`, `repo-worker-base`, `verification-before-completion`); replace the three `ci --check` bullets under "Repo-specific guidance" with a pointer: `The portable rule for when to run the complete gate lives in `repo-standards` `references/ci-validation-pipeline.md`; this repo's command is `py -3 tools/run.py ci --check [--diagnostics]`.` Keep the `marketplace --apply` bullet.

- [ ] **Step 4: Add `## Required skills` to the remaining runbooks** per the reference table, placed after the intro/`## When to use` section of each file.

- [ ] **Step 5: Verify zero warnings** - `py -3 codex-marketplace/plugins/repo-worker-pack/skills/repo-standards/scripts/repo_standards.py --check` prints no `WARN:` lines.

- [ ] **Step 6: Commit** - `docs(runbooks): declare required-skill composition per runbook`.

---

### Task 8: Local doctrine trims to binding plus pointers

**Files:**
- Modify: `AGENTS.md`
- Modify: `.agents/doctrine/non-repo-locations-policy.md`

- [ ] **Step 1: Trim `AGENTS.md` "Publication proof for repo work"** - remove the generic invariant paragraph ("Local file changes are not repo completion..."); keep the three valid return forms and "prefer a PR into `main`"; end the section with: `The portable publication method belongs to `publishing-source` and `repo-worker-base`.` Keep the heading and `## Draft PR policy` intact (canonical topics must stay covered).

- [ ] **Step 2: Reduce `non-repo-locations-policy.md`** - keep the canonical location table (worktree and scratch roots as this repo's binding), the subagent-profile runtime staging section (local-only rule), and add a pointer paragraph: `Canonical layout, sanitization, and cleanup rules live in `repo-standards` `references/scratch-workspace-policy.md` and `repo-worker-base` `references/worktree-and-branch-policy.md`; `subagent-workspace` resolves paths inside the layout.` Remove the restated generic rules (top-level-only-repo-folders, branch-folder naming, do-not-commit-scratch) that the portable policies already own.

- [ ] **Step 3: Commit** - `docs(doctrine): trim local restatements to bindings and pointers`.

---

### Task 9: Regenerate derived surfaces and verify the full gate

**Files:**
- Regenerate: `.agents/skills/` installed copies, `INDEX.md` mesh, `INDEX.json` surfaces.

- [ ] **Step 1: Regenerate** - `py -3 tools/run.py marketplace --apply` then `py -3 tools/run.py mesh --apply` (add `--allow-shared-checkout` if requested). Stage any generated changes.

- [ ] **Step 2: Run contract tests** - `py -3 -m pytest tests/test_repo_standards.py -v` Expected: all PASS.

- [ ] **Step 3: Uncommitted full verification** - `py -3 tools/run.py ci --check --diagnostics`. Expected: all targets pass; repo-standards emits zero `WARN:` lines.

- [ ] **Step 4: Final commit** - `docs(repo-standards): regenerate installed skills and mesh` (or fold generated files into their owning task commits if the hook regenerates them there).

- [ ] **Step 5: Push and report** - push the branch; the draft PR carrying this plan is the publication surface. Report WARN-check behavior, template/doctrine parity proof, and the green gate as completion evidence.
