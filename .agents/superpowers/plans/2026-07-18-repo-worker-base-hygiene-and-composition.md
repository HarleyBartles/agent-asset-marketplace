# Repository Worker Base Hygiene and Superpowers Composition Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Extend `repo-worker-base` with portable hygiene references, stage-guide composition, and an explicit `work-mode-router` handoff, while moving this repository's guide set to `.agents/guides/`.

**Architecture:** Keep `SKILL.md` as a thin router. Put repeatable cross-repository rules in skill-root-relative references; keep repository-specific overlays in `.agents/guides/`; make `work-mode-router` invoke the base skill before the selected Superpowers lane. Generated projections, zips, manifests, maps, and indexes remain tool-owned outputs.

**Tech Stack:** Markdown, `agents/openai.yaml`, Python generators/validators, pytest, Git worktrees, PowerShell.

## Global Constraints

- Resolve the current checkout with `git -C <start-path> rev-parse --show-toplevel`.
- Reject submodules with `git -C <start-path> rev-parse --show-superproject-working-tree`, then resolve the main checkout from the absolute result of `git -C <current-checkout> rev-parse --path-format=absolute --git-common-dir`; use its parent, never current-directory, script-location, or filesystem parent walking.
- Derive external locations as `<main-checkout-root>/../_agent-worktrees/<repo-name>` and `<main-checkout-root>/../_agent-scratch/<repo-name>/<branch-name>`.
- Edit only canonical first-party sources; regenerate projections and packages.
- `work-mode-router` classifies; `repo-worker-base` owns hygiene/composition/publication; Superpowers owns stage technique.
- Repo-backed Superpowers requires base skill + matching baseline reference + local `.agents/guides/` guide.
- Installed skills are agent assets, not runtime dependencies.
- Local validation and commits do not prove completion; require GitHub publication and remote verification.
- MARK-337 remains a separate spike; do not implement it here.

## File map

- Modify `sources/first_party/skills/repo-worker-base/SKILL.md` for thin routing.
- Create ten references under `sources/first_party/skills/repo-worker-base/references/`.
- Modify `sources/first_party/skills/repo-worker-base/agents/openai.yaml` if discovery metadata needs the composition triggers.
- Modify `sources/first_party/skills/work-mode-router/SKILL.md` for the explicit handoff.
- Move the eight files in `.agents/docs/guides/` to `.agents/guides/`; update nearest routers and mesh indexes.
- Create `tests/test_repo_worker_base_contract.py` and `tests/pressure/repo-worker-base/`.
- Regenerate `codex-marketplace/**` projections and `generated/skill-zips/**`; never hand-edit them.

## Task 1: Write the RED contract tests

**Files:** Create `tests/test_repo_worker_base_contract.py`; create `tests/pressure/repo-worker-base/README.md` and the structured `campaign.json` fixture.

- [x] Add tests that assert all ten reference filenames exist, source text contains no `Z:`/ `C:` assumptions, and portable worktree references contain Git-anchored `--show-toplevel`, absolute `--git-common-dir`, `_agent-worktrees`, and `_agent-scratch` behavior.
- [x] Add route-order assertions:

```python
def test_router_requires_base_before_downstream_lane():
    text = ROUTER.read_text(encoding="utf-8")
    assert "repo-worker-base" in text
    assert text.index("repo-worker-base") < text.index("using-superpowers")
```

- [x] Add guide assertions for `.agents/guides/design-guide.md`, `planning-guide.md`, `implementing-guide.md`, and `code-review-guide.md`, while treating the existing `.agents/docs/guides/` location as the expected RED state.
- [x] Run `py -3 -m pytest tests/test_repo_worker_base_contract.py -q`; record the intentional failure.
- [x] Commit: `test: add repo worker base contract baseline`.

## Task 2: Author the base references and routing

**Files:** Modify `sources/first_party/skills/repo-worker-base/SKILL.md` and `agents/openai.yaml`; create:

```text
references/worktree-and-branch-policy.md
references/mutation-script-safety.md
references/script-entrypoint-contract.md
references/repository-layout-and-mesh.md
references/stage-guide-contract.md
references/design-baseline.md
references/planning-baseline.md
references/implementation-baseline.md
references/code-review-baseline.md
references/superpowers-composition.md
```

- [x] Write each reference with one dominant use case. Include doctrine/guides/playbooks-or-runbooks/skills boundaries; local authored-skill custody and installer non-pruning; canonical homes and forbidden legacy homes; one authority per rule; thin routers; README boundaries; doctrine metadata; cleanup survival; generated mesh proof; publication proof; runtime separation; and external scratch custody.
- [x] State the exact portable algorithm:

```text
superproject = git -C <start-path> rev-parse --show-superproject-working-tree
current_checkout = git -C <start-path> rev-parse --show-toplevel
common_git = git -C <current-checkout> rev-parse --path-format=absolute --git-common-dir
checkout_git = git -C <current-checkout> rev-parse --path-format=absolute --git-dir
main_checkout = parent(common_git)
external_worktree_root = main_checkout / ".." / "_agent-worktrees" / repo_name
external_scratch_root = main_checkout / ".." / "_agent-scratch" / repo_name / branch_name
```

- [x] Require unconditional submodule rejection through `git -C <start-path> rev-parse --show-superproject-working-tree`, and require future tooling to consume this algorithm rather than independently walking filesystem parents.
- [x] Add `Use when`/ `Read when` routing for repo work, design, planning, implementation, evidence, review, closeout, publication, mutation scripts, mesh changes, worktrees, scratch, and agent-facing scripts.
- [x] Add the paired contract: `repo-worker-base` -> matching baseline -> local guide -> selected Superpowers lane. Do not add Portfolio's namespace or any absolute path.
- [x] Run `py -3 -m pytest tests/test_repo_worker_base_contract.py -q` and an `rg` sweep for forbidden paths.
- [x] Commit: `feat: add repo worker hygiene references and composition routing`.

## Task 3: Add the router handoff

**Files:** Modify `sources/first_party/skills/work-mode-router/SKILL.md`, its `agents/openai.yaml` only if needed, and the contract test.

- [x] Add explicit text: `work-mode-router -> repo-worker-base -> matching baseline reference and local guide -> Superpowers lane`.
- [x] State that the router owns classification, the base skill owns hygiene/composition/publication boundaries, and Superpowers owns stage technique; prohibit recursive router invocation after classification.
- [x] Cover planning, implementation, source evidence, publication, and review.
- [x] Run `py -3 -m pytest tests/test_repo_worker_base_contract.py -q`.
- [x] Commit: `feat: route repository work through repo worker base`.

## Task 4: Migrate the guide home and mesh

**Files:** Move `.agents/docs/guides/AGENTS.md`, `design-guide.md`, `planning-guide.md`, `implementing-guide.md`, `code-review-guide.md`, `marketplace-generation-guide.md`, `skill-authoring-guide.md`, and `INDEX.md` to `.agents/guides/`. Modify `.agents/AGENTS.md`, `.agents/docs/AGENTS.md`, `tools/AGENTS.md`, router references, and tests.

- [x] Move files with `git mv`; preserve `implementing-guide.md`; leave no retained guide under `.agents/docs/guides/`.
- [x] Replace old guide pointers with `.agents/guides/`; keep local guides thin and repository-specific.
- [x] Run `py -3 tools/generate_index_mesh.py`, then `py -3 tools/generate_index_mesh.py --check`.
- [x] Run `py -3 -m pytest tests/test_repo_worker_base_contract.py -q` and `git diff --check`.
- [x] Commit: `docs: make agents guides a first-class canonical home`.

## Task 5: Regenerate, validate, and publish

**Files:** Generated projections, zips, manifests, source/provenance maps, indexes, and drift surfaces selected by the rebuild; no hand-edits.

- [x] Run `py -3 tools/rebuild_marketplace.py`.
- [x] Run `py -3 tools/check_marketplace.py`, `py -3 tools/generate_marketplace.py --check`, `py -3 tools/generate_repo_index.py --check`, `py -3 tools/generate_pack_manifests.py --check`, `py -3 tools/materialize_projection.py --check`, `py -3 tools/generate_index_mesh.py --check`, and `py -3 tools/validate_generated_drift.py --base origin/main`.
- [x] Run `py -3 -m pytest tests/test_repo_worker_base_contract.py tests/test_validate_marketplace.py tests/test_generator_check_modes.py -q` and `git diff --check`; the focused contract is 20/20 GREEN, while the combined command still exposes two unchanged generator-check test failures already present outside this fix wave.
- [x] Check in a reproducible pressure campaign with separate no-guidance controls and guided prompts, explicit RED/GREEN/REFACTOR evidence fields, three-plus combined-pressure scenarios, five-plus micro-tests, and no unchecked runtime-result claims.
- [x] Confirm both projections and both repo-worker-base zips contain the ten references, `SKILL.md`, and `agents/openai.yaml`; confirm application code/tests do not import installed skill trees or user caches.
- [ ] Commit: `chore: regenerate repo worker base marketplace surfaces`.
- [ ] Push, open a PR into `main`, and record the remote PR URL and full head SHA. Only then treat completion as publishable; Portfolio refresh is a separate downstream authorized action.

## Interim states

- Task 1 is intentionally RED.
- After Tasks 2-4, generated projections may still be stale until Task 5.
- The guide migration test is RED until Task 4.
- No overall GREEN claim is valid before remote publication verification.

## Spec coverage and confidence

The tasks cover capability boundaries, authored-skill custody, guide migration, router composition, Git-derived worktree/scratch resolution, layout/mesh rules, publication proof, runtime separation, pressure scenarios, and generated validation. No MARK-337 implementation is included.

**SDD confidence: 8.4/10.** Current source paths, guide paths, and generator commands were verified. Remaining uncertainty is limited to the exact generated-file set (tool-owned) and fresh-context pressure execution, both of which are explicit validation steps rather than design gaps.
