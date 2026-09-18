# Runbook and Playbook Contract Implementation Plan

> **Execution lane:** `executing-plans` in the current isolated worktree.

**Goal:** Separate lifecycle-stage runbooks from conditional topical playbooks, make stage runbooks the local composition roots, and validate that every declared playbook is structurally valid and reachable from the normal stage path.

**Architecture:** `.agents/runbooks/` contains lifecycle-stage composition roots entered through stage/workflow skills. `.agents/playbooks/` contains conditional topical compositions selected by runbooks. The only valid orchestration direction is router -> stage skill -> runbook -> playbook -> doctrine/contracts/capability skills. The repo-standards policy maps both artifact families. Markdown headings and relative links are the human-readable structural contract; `repo_standards.py` validates headings, references, reciprocal routing, reachability, and cycles without interpreting free prose.

**Approved terminology:** A **runbook** owns a repository lifecycle stage. A **playbook** owns a conditional class of work or concern. These terms are not aliases.

**Scope:** Canonical `repo-standards` and `using-superpowers-plus` sources, their focused tests, the marketplace repository's own local adoption, generated installed-skill projections, and generated indexes.

**Out of scope:** Editing downstream consumer repositories, inventing a general Markdown schema language, inferring applicability from arbitrary prose, or changing portable capability-skill behavior beyond the local-guide paths they load.

**Publication:** Normal hooked commits, push `codex/runbook-playbook-contract`, open a Draft PR into `main`, and verify the published head.

---

## Task 1: Define the two artifact contracts and routing vocabulary

**Consumes:** Approved runbook/playbook terminology and current repo-standards source.

**Files:**

- Modify: `codex-marketplace/plugins/repo-worker-pack/skills/repo-standards/references/repository-runbook-standard.md`
- Modify: `codex-marketplace/plugins/repo-worker-pack/skills/repo-standards/references/repository-shape-standard.md`
- Modify: `codex-marketplace/plugins/repo-worker-pack/skills/repo-standards/SKILL.md`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/using-superpowers-plus/references/bootstrap-routing.md`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/using-superpowers-plus/references/superpowers-composition.md`

### Steps

1. Update the surface taxonomy so repository lifecycle stages belong to runbooks and conditional change concerns belong to playbooks.
2. Define runbooks as stage roots with the seven common composition sections plus `Playbook routing`.
3. Define playbooks as topical compositions with the seven common sections plus `Invoked by`.
4. State the allowed dependency direction and prohibit playbook-to-runbook orchestration and cycles.
5. Replace the retired-playbooks migration rule with the new flat-runbook-to-runbook/playbook migration.
6. Update Superpowers stage-local-guide paths and bootstrap prose to retain `.agents/runbooks/<stage>.md` as stage entry roots while requiring those roots to route applicable playbooks.
7. Run focused prose/contract assertions in `tests/test_workflow_contracts.py`; initially add failing assertions before changing source text.

**Exit:** The canonical standard and stage router unambiguously distinguish the two artifact families and agree on dependency direction.

## Task 2: Teach scaffolding and policy mapping about playbooks

**Consumes:** Task 1 artifact contracts.

**Files:**

- Modify: `codex-marketplace/plugins/repo-worker-pack/skills/repo-standards/scripts/scaffold_runbooks.py`
- Create: `codex-marketplace/plugins/repo-worker-pack/skills/repo-standards/scripts/scaffold_playbooks.py`
- Create: `codex-marketplace/plugins/repo-worker-pack/skills/repo-standards/scripts/scaffold-playbooks.ps1`
- Create: `codex-marketplace/plugins/repo-worker-pack/skills/repo-standards/scripts/scaffold-playbooks.sh`
- Modify: `codex-marketplace/plugins/repo-worker-pack/skills/repo-standards/scripts/scaffold-all.ps1`
- Modify: `codex-marketplace/plugins/repo-worker-pack/skills/repo-standards/scripts/scaffold-all.sh`
- Modify: `codex-marketplace/plugins/repo-worker-pack/skills/repo-standards/scripts/scaffold_repo_runbook_policy.py`
- Modify: `codex-marketplace/plugins/repo-worker-pack/skills/repo-standards/templates/repo-runbook-policy.md`
- Add or modify focused tests in `tests/test_repo_standards.py`

### Steps

1. Write failing tests proving the runbook scaffolder only owns lifecycle files and emits `Playbook routing`.
2. Write failing tests proving the playbook scaffolder reads the playbook policy table, writes under `.agents/playbooks/`, and emits `Invoked by` plus the seven common sections.
3. Split the standard policy template into `Standard runbooks` and `Standard playbooks` mappings.
4. Implement the smallest scaffolder split that passes the tests while preserving `--check`/`--force` behavior.
5. Add thin PowerShell and shell launchers and include playbook scaffolding in `scaffold-all`.
6. Verify all new and changed script entry points satisfy `--help` and safe `--check` behavior.

**Exit:** New consumers receive correctly typed artifacts in separate directories, and policy mappings provide their canonical paths.

## Task 3: Replace heading-only warnings with graph validation

**Consumes:** Tasks 1-2 contracts and policy format.

**Files:**

- Modify: `codex-marketplace/plugins/repo-worker-pack/skills/repo-standards/scripts/repo_standards.py`
- Modify: `tests/test_repo_standards.py`

### Steps

1. Write failing tests for all seven common headings on runbooks and playbooks.
2. Write failing tests for runbook `Playbook routing` links and playbook `Invoked by` links.
3. Write failing tests for missing targets, wrong-directory targets, non-reciprocal edges, unreachable playbooks, and cycles.
4. Write failing tests showing fenced or commented headings and links do not satisfy the contract.
5. Implement a bounded Markdown section/link parser over live Markdown only.
6. Build the runbook-to-playbook graph from explicit links, validate reciprocal declarations, and prove every mapped playbook is reachable from a mapped runbook.
7. Report structural and graph violations as `DRIFT`, not advisory warnings; keep messages path-specific and actionable.
8. Preserve exclusions for `AGENTS.md` and generated indexes, and reject legacy topical Markdown left directly under `.agents/runbooks/` when it is mapped as a playbook.
9. Run the focused repo-standards tests.

**Exit:** A green repo-standards check proves structural composition and reachability instead of file presence plus one heading.

## Task 4: Provide opinionated stage and topical templates

**Consumes:** Tasks 1-3 schema and validation behavior.

**Files:**

- Modify: `codex-marketplace/plugins/repo-worker-pack/skills/repo-standards/templates/pr.md`
- Create: `codex-marketplace/plugins/repo-worker-pack/skills/repo-standards/templates/code-style.md`
- Create or modify other templates only where a standard artifact needs non-generic routing content.
- Modify: `codex-marketplace/plugins/repo-worker-pack/skills/repo-standards/templates/agents-md.template.md`
- Modify: `codex-marketplace/plugins/repo-worker-pack/skills/repo-standards/templates/contributing-template.md`
- Modify: `codex-marketplace/plugins/repo-worker-pack/skills/repo-standards/templates/REVIEW.md`
- Modify tests in `tests/test_repo_standards.py`

### Steps

1. Write failing scaffold-content tests for the approved code-style teaching contract.
2. Make the code-style playbook state that durable architecture belongs in doctrine, language/framework technique belongs in capability skills, and the playbook binds those owners to local conventions and evidence.
3. Make stage templates demonstrate conditional playbook routing rather than leaving applicability implicit.
4. Update contributor/review/root templates to point to stage runbooks and topical playbooks by their correct roles.
5. Run focused scaffold and template tests.

**Exit:** Generated artifacts teach the intended ownership model rather than presenting a generic documentation bucket.

## Task 5: Migrate this repository to the new layout and routing graph

**Consumes:** Tasks 1-4 standard and tooling.

**Files:**

- Keep under `.agents/runbooks/`: `design.md`, `planning.md`, `implementing.md`, `code-review.md`, `pr.md`, `AGENTS.md`
- Move to `.agents/playbooks/`: `code-style.md`, `testing.md`, `security.md`, `skill-authoring.md`, `marketplace-generation.md`, `completing-plans.md`, `repo-doctrine.md`
- Create: `.agents/playbooks/AGENTS.md`
- Modify: `.agents/doctrine/repo-runbook-policy.md`
- Modify: root `AGENTS.md`, `CONTRIBUTING.md`, `REVIEW.md`, and `.devin/rules/*.md` path pointers as required
- Modify: local runbooks and playbooks to satisfy the new contracts
- Modify: `tools/validate_agents_md.py`, `tools/generate_repo_index.py`, and focused tests where local layout is encoded

### Steps

1. Write failing workflow-contract tests for the new local paths and required stage-to-playbook edges.
2. Move topical files with history-preserving filesystem moves, then edit them through patches.
3. Add explicit routing from implementation to code-style, testing, marketplace-generation, and skill-authoring when their triggers apply.
4. Add explicit review routing to code-style, testing, and security when their triggers apply; route other stage-specific concerns narrowly.
5. Give every playbook reciprocal `Invoked by` links and bind its doctrine, capability skills, commands, and evidence without duplicating portable method.
6. Update repository routers, policies, generated-index configuration, allowed `AGENTS.md` paths, and all current non-historical path references.
7. Do not rewrite the completed 2026-09-14 spec/plan as though the new terminology existed then; preserve historical artifacts unless a live link must remain resolvable.
8. Run focused workflow, repo-index, agent-mesh, and repo-standards tests.

**Exit:** This repository is a valid consumer of the new standard and demonstrates an end-to-end reachable composition graph.

## Task 6: Regenerate projections and prove the complete change

**Consumes:** Tasks 1-5 completed source and local overlays.

**Files:**

- Generated by commands: `.agents/skills/`, marketplace manifests, provenance, `INDEX.md`, and `INDEX.json` surfaces.

### Steps

1. Run `py -3 tools/run.py marketplace --apply` to project canonical plugin-source changes.
2. Run `py -3 tools/run.py mesh --apply` and the repository index apply target required by current tooling.
3. Run focused pytest suites for repo standards and workflow contracts.
4. Inspect the actual diff for source/generated custody, stale paths, accidental historical rewrites, and missing reciprocal edges.
5. Remove this completed plan and its generated index entry only after its durable decisions are represented in the standard and live guidance.
6. Stage the intended tree and commit normally so the tracked pre-commit hook materializes and validates the staged snapshot. Do not run the broad CI check immediately before or after the successful hooked commit.
7. Verify the commit tree, status, and hook evidence; push the branch.
8. Open a Draft PR into `main`, read it back, and verify its head SHA matches the pushed commit.

**Exit:** Canonical source, local adoption, installed projections, and generated indexes agree; the hooked commit passes; a verified Draft PR provides publication proof.
