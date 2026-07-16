# MARK-293: GitHub Actions-owned generated-output proof implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make GitHub Actions the proof surface for deterministic marketplace outputs by switching PR validation to check-only mode, keeping local preflight aligned, and documenting that generated projections, registries, source maps, provenance maps, and skill zips are output surfaces rather than hand-authored source.

**Architecture:** The repo already has check-capable validators for projections, provenance maps, source maps, skill zips, drift, marketplace state, and repo index. The current gap is the workflow: it still writes generated artifacts in the runner workspace, which is easy to trust incorrectly. This plan changes the CI path to run the same deterministic checks without mutating output surfaces, then documents one exact local preflight sequence that matches the workflow.

**Tech Stack:** GitHub Actions YAML, Python 3 via `python` in CI and `py -3` locally, existing marketplace validators under `tools/`, markdown docs in `README.md`, `codex-marketplace/README.md`, and scoped `AGENTS.md` files.

## Global Constraints

- Keep the change narrow to MARK-293: workflow proof model, worker-facing docs, and any minimal validator messaging fix uncovered during dry run.
- Do not add unsafe auto-commit or bot-write behavior.
- Preserve the current deterministic generators and their explicit full-regeneration modes.
- Do not broaden into unrelated marketplace refactors or new skill content.
- Treat generated projections, generated registries, generated source/provenance maps, and `generated/skill-zips/**` as output surfaces.
- The local preflight sequence must match the CI check sequence in substance, even if the executable differs (`python` in Actions, `py -3` locally).

---

### Task 1: Recast the marketplace validation workflow as check-only proof

**Files:**
- Modify: `.github/workflows/marketplace-validation.yml`

**Interfaces:**
- Consumes: the existing check-capable scripts (`tools/update_skill_artifacts.py --check`, `tools/generate_marketplace.py --check`, `tools/generate_repo_index.py --check`, `tools/materialize_projection.py --check`, `tools/generate_mega_packs.py --check`, `tools/generate_provenance_maps.py --check`, `tools/generate_source_maps.py --check`, `tools/validate_marketplace.py`, `tools/validate_repo_index.py`, `tools/validate_skill_zips.py`).
- Produces: a workflow that proves committed marketplace outputs are current without rewriting them in the runner workspace.

- [ ] **Step 1: Replace the write-mode generator steps with explicit check-mode validation.**

Use a workflow shape like this:

```yaml
- name: Check skill artifacts
  run: python tools/update_skill_artifacts.py --check

- name: Check marketplace manifests
  run: python tools/generate_marketplace.py --check

- name: Check repo index
  run: python tools/generate_repo_index.py --check

- name: Check projection drift
  run: python tools/materialize_projection.py --check

- name: Check mega-pack manifests
  run: python tools/generate_mega_packs.py --check

- name: Check provenance maps
  run: python tools/generate_provenance_maps.py --check

- name: Check source maps
  run: python tools/generate_source_maps.py --check

- name: Validate marketplace
  run: python tools/validate_marketplace.py

- name: Validate repo index
  run: python tools/validate_repo_index.py

- name: Validate skill zips
  run: python tools/validate_skill_zips.py

- name: Check whitespace
  run: git diff --check
```

Keep the existing checkout, Python setup, and dependency install steps. Remove the current `python tools/update_skill_artifacts.py --all --base origin/main`, `python tools/generate_marketplace.py`, and `python tools/generate_repo_index.py` write steps from the PR path.

- [ ] **Step 2: Keep the workflow readable by naming the proof surface in step labels.**

The step names should tell reviewers what is being proven:
- skill artifacts
- marketplace manifests
- repo index
- projection drift
- mega-pack manifests
- provenance maps
- source maps
- skill zip registry
- whitespace safety

- [ ] **Step 3: Confirm the workflow still runs on the intended event surface.**

Preserve the current PR validation trigger for marketplace-facing changes. Do not add an auto-commit job or a hidden mutation path.

### Task 2: Update worker-facing docs to publish the check-only model and exact local preflight sequence

**Files:**
- Modify: `README.md`
- Modify: `codex-marketplace/README.md`
- Modify: `tools/README.md`
- Modify: `repo-index/README.md`
- Modify: `AGENTS.md`
- Modify: `tools/AGENTS.md`
- Modify: `codex-marketplace/AGENTS.md`

**Interfaces:**
- Consumes: the check-only workflow from Task 1 and the existing validator commands.
- Produces: worker-facing guidance that says GitHub Actions are the proof surface and gives one exact local preflight sequence.

- [ ] **Step 1: Update the root README to explain the proof model.**

State plainly that:
- generated marketplace outputs are downstream surfaces;
- CI proves they are current;
- workers normally edit source, adapters, and projection intent, not generated files;
- full regeneration is still explicit and separate from the normal proof path.

- [ ] **Step 2: Update `codex-marketplace/README.md` and `tools/README.md` with the exact local preflight sequence.**

Document the matching local sequence in `py -3` form:

```text
py -3 tools/update_skill_artifacts.py --check
py -3 tools/generate_marketplace.py --check
py -3 tools/generate_repo_index.py --check
py -3 tools/materialize_projection.py --check
py -3 tools/generate_mega_packs.py --check
py -3 tools/generate_provenance_maps.py --check
py -3 tools/generate_source_maps.py --check
py -3 tools/validate_marketplace.py
py -3 tools/validate_repo_index.py
py -3 tools/validate_skill_zips.py
git diff --check
```

The docs should say this is the worker preflight path before pushing, and that the same proof classes run in Actions.

- [ ] **Step 3: Update the scoped AGENTS files to match the new operational contract.**

Make the scoped instructions say:
- generated outputs are output surfaces, not hand-edited source truth;
- GitHub Actions provide durable proof for those surfaces;
- local validation is a preflight, not the only proof source;
- the exact check sequence above is the expected worker path.

Do not introduce a new doctrine surface or broader repo policy change.

### Task 3: Run the check sequence locally, then fix only any surfaced proof-model gaps

**Files:**
- Modify only if needed: the smallest workflow or validator file that produces an ambiguous or stale failure message during the dry run.

**Interfaces:**
- Consumes: the updated workflow intent and worker docs from Tasks 1 and 2.
- Produces: a validated check-only marketplace proof path with source-facing failures.

- [ ] **Step 1: Run the local preflight sequence from Task 2 exactly as written.**

Use the same command order listed in the docs. Expected result: every command passes on the current `main` baseline after the workflow rewrite.

- [ ] **Step 2: If any command fails with a non-source-facing or misleading message, tighten the smallest affected message.**

Prefer the narrowest possible fix:
- adjust the workflow step label if the failure is only confusing in CI;
- otherwise, patch the smallest validator or drift check so the error names the stale source, adapter, manifest, or command that should be fixed.

Do not weaken the validation rule to make the error disappear.

- [ ] **Step 3: Re-run the exact same local preflight sequence and `git diff --check`.**

Expected result: the sequence passes cleanly and there is no unintended workspace churn from check-only execution.

## Self-Review

### Spec coverage

- CI proof model changed from write-mode generation to check-only validation.
- Local worker preflight documented as one exact sequence.
- Worker-facing docs updated at the repo surfaces the issue names.
- No unsafe bot-write or auto-commit path introduced.
- No unrelated marketplace refactor required.

### Placeholder scan

- No TBDs or open-ended file names.
- No vague "handle edge cases" language.
- Any message fixes are explicitly limited to the smallest affected validator or workflow label.

### Type consistency

- `python` is used in GitHub Actions.
- `py -3` is used in local docs.
- The same check commands appear in both places, only the executable differs.
