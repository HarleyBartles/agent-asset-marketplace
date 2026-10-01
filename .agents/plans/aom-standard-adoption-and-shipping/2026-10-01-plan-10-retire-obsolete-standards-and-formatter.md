# Retire Obsolete Standards and Markdown Formatter

**Status:** in progress

> **For agentic workers:** REQUIRED SUB-SKILL: Use `subagent-driven-development` (recommended) or `executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remove obsolete Markdown-formatting and root-gitignore standards and their old deployment surface, carry the useful Markdown authoring guidance into writing-pack, and retire the formatter wheel and gate integration without weakening repository line-ending normalization or the atomic Windows/Linux CI target.

**Architecture:** Markdown prose authoring guidance belongs in the writing skill, not a separately subscribed formatting standard, consumer contract, custom formatter, or Marketplace wheel. The guidance gives a consistent readable source style without imposing a hard line-length rule or repository checker. Repository line endings remain governed by the active tracked validation hook and `.gitattributes`. Root-gitignore cleanup is no longer a standard or deployment target. The entire `repo-shape` skill is an obsolete v1 structural/deployment compatibility layer; its history remains available from the exact source commit recorded by old consumers, while current repository-owned common tools move to `tools/`. Remove the retired shared-checkout mutation-intent flag from current repository tools and agent guidance; explicit `--apply` remains the mutation boundary and the worktree workflow governs checkout selection. Current repository-owned v2 subscriptions remain unchanged.

**Tech Stack:** Python 3, existing writing-pack source, plugin build/generation tools, existing tracked validation hook and command declaration.

**Spec:** [Approved AOM design](../../specs/2026-09-30-aom-standard-adoption-and-shipping.md), especially sections 2, 3, 6, 7, and 8, plus the agreed Markdown-formatting decision recorded during brainstorming: keep only lightweight writing guidance in writing-pack.

**Roadmap:** [Marketplace migration roadmap](2026-10-01-plan-7-marketplace-migration-roadmap.md), Plan 10. Baseline: Plan 9 closeout.

**Execution Strategy:** `executing-plans` - migrate the two live formatter consumers, hook declaration, writing guidance, and package ownership before deleting formatter source and regenerating the published plugin.

## Global Constraints

- Do not change the primary checkout or other repositories.
- Preserve all eight selected v2 standard IDs, immutable pins, and truthful certification.
- Keep `.agents/contracts/repo-standards-commands.json` as the tracked hook binding, but remove Markdown formatting commands from it.
- Preserve complete Windows pre-commit and Linux hosted CI parity. Both continue to run the same full repository gate.
- Preserve LF normalization and tracked-line-ending enforcement; do not treat dropping mdformat as permission for line-ending churn.
- Do not add a fixed markdown column limit, formatter dependency, standard subscription, hook target, or CI target.
- Change canonical source and use existing Marketplace generators for `dist/`; do not edit generated plugin output or manifests by hand.
- Keep writing advice proportionate: avoid mixing visibly inconsistent source wrapping conventions in one document, but do not reflow unrelated Markdown to satisfy a formatter.
- Remove repository-specific obsolete contract files only after verifying no current certification, hook, or source route reads them.
- Historical plan/spec documents may retain accurately labeled historical references; current instructions and active routes must not direct agents to retired commands.

## Review Focus

- The only Markdown obligation retained is a writing practice, not a machine-enforced standard.
- The full CI gate still verifies line endings on Windows and Linux.
- Every package consumer and generator reference to the formatter skill, contract, wheel, and scaffolder is found and resolved.
- The Marketplace-generated plugin inventory remains consistent after rebuilding.
- Old root-gitignore implementation paths do not remain in the current standards catalog or repo-shape onboarding guidance.
- v2 certification and selected pins do not change merely because unrelated old contracts are deleted.

## Known dependency inventory

- Formatter consumers: `.agents/contracts/repo-standards-commands.json`, `tools/new_plugin.py`, `tools/sync_skill_shared_references.py`, `.agents/playbooks/code-style.md`, old repository-shape scaffolding/docs, and the formatter skill itself.
- Formatter source/package: `skills/markdown-formatting/`, `.agents/standards/markdown-formatting/`, `.mdformat.toml`, `src/packages/mdformat-safe-link-labels/`, and generated Marketplace plugin/wheel files.
- Legacy coordinator: `skills/repo-shape/` and the compatibility entrypoint `skills/repo-standards/scripts/repo_standards.py`. Live repository utility functions used by `tools/run.py` are `deploy_vendor_profiles.py` and `validate_skill_scripts.py`; move these two to `tools/` before retiring the old skill.
- Obsolete local contracts: `.agents/contracts/markdown-formatting.json`, `.agents/contracts/agent-operating-model.json` (v1 surface exceptions), and `.agents/contracts/unslop.json` (v1 profile roots). Confirm remaining production references before deleting each.
- Obsolete root-gitignore deployment source: the old repo-shape catalog/manifest entry, `scaffold_gitignore.py`, its shell/PowerShell wrappers and scaffold-all calls, templates, tests, and guidance. Keep ordinary root `.gitignore` policy and version-control configuration intact.
- Retired shared-checkout flag: `tools/shared_checkout.py`, `tools/run.py`, `tools/new_plugin.py`, `tools/sync_runtime_agents.py`, the writing-skills scaffolder, the now-worktree creator's deprecated no-op flag, CLI validation policy, and Repo Worker Pack docs/tests.

______________________________________________________________________

### Task 1: Move useful Markdown source guidance into writing-pack

**Files:**

- Modify: `skills/writing/SKILL.md` and/or add a narrowly routed reference under `skills/writing/references/`
- Modify: `.agents/playbooks/code-style.md`
- Read: current Markdown-formatting skill, formatter contract, local formatting policy, and line-ending validator

**Consumes:** The user-approved boundary that Markdown formatting does not need an AOM standard and belongs as a writing-pack capability.

**Produces:** Concise agent-facing advice for readable, consistent Markdown authoring without a line-length gate.

- [x] Write the useful source-formatting advice in the existing writing-pack entry point; preserve the human-readable preference for consistent paragraph widths without prescribing an exact number.
- [x] Route code-style guidance to the writing capability for Markdown authoring; remove the deleted formatter command and claims of machine-enforced wrapping.
- [x] Preserve authored document semantics, code blocks, tables, and existing paragraph content; do not bulk-reformat unrelated files.
- [x] Confirm that newline normalization remains separately enforced by the tracked gate and `.gitattributes`.

### Task 2: Remove the formatter standard and its wheel from owned source

**Files:**

- Delete: `skills/markdown-formatting/` and `.agents/standards/markdown-formatting/`
- Delete: `src/packages/mdformat-safe-link-labels/`
- Delete: `.mdformat.toml` and the Markdown-formatting contract/config templates and schema owned only by the retired standard
- Modify: `src/plugin-definitions/agent-operating-model/contents.json`
- Modify: `tools/new_plugin.py`, `tools/sync_skill_shared_references.py`, and any generator/build target that references the formatter or wheel
- Modify: `.agents/contracts/repo-standards-commands.json`

**Consumes:** Task 1, the formatter dependency inventory, and the Plan 9 retained formatter subtree.

**Produces:** A Marketplace with no separately installable Markdown-formatting standard, wheel, formatter commands, or local standard deployment copy.

- [x] Remove the formatter apply/check command vectors from the active repo command binding while preserving both `tools/run.py ci --apply` and `--check` invocations.
- [x] Remove formatter fallback selection from `tools/new_plugin.py` and `tools/sync_skill_shared_references.py`; preserve their actual plugin-generation and reference-sync responsibilities.
- [x] Remove the formatter skill from canonical plugin definitions and delete its dedicated source tests and implementation.
- [x] Remove the safe-link-labels wheel source and generation route; ensure no current build or packaging command attempts to create or validate it.
- [x] Remove the obsolete Markdown-formatting contract, schema, requirements, scaffolders, and formatter config from current source and consumer-facing docs.
- [x] Rebuild Marketplace projections from canonical sources and verify the generated AOM plugin no longer includes the formatter skill or wheel.
- [x] Confirm ordinary Markdown link validation, repository line-ending checks, and all non-formatting CI targets still run.

### Task 3: Retire the obsolete v1 compatibility skill and local legacy contracts

**Files:**

- Move: `skills/repo-shape/scripts/deploy_vendor_profiles.py` and `validate_skill_scripts.py` to their current repository tool owners under `tools/`
- Delete: `skills/repo-shape/` and its obsolete tests/fixtures, plus `skills/repo-standards/scripts/repo_standards.py`
- Delete only after reference audit: `.agents/contracts/agent-operating-model.json` and `.agents/contracts/unslop.json`
- Modify: `skills/repo-standards/SKILL.md`, `skills/repo-composition/SKILL.md`, `.agents/docs/distribution.md`, and current plugin README to route old pins to Git history rather than bundling v1 implementation history
- Preserve: root `.gitignore`, `tools/validate_agents_md.py`, the v2 subscription, and `.agents/unslop/repository.md`

**Consumes:** Plan 8 certification and live-source search for old contract references.

**Produces:** No current `repo-shape` compatibility skill, root-gitignore deployment surface, or stale v1 exception/profile-root contract in the v2 implementation. Git history remains the authority for old immutable pins.

- [x] Move the two generic tools used by `tools/run.py` before deleting `skills/repo-shape/`; retain their behavior and wire the runner to the new paths.
- [x] Remove the v1 `repo-shape` skill from the current AOM plugin definition and delete its current source and tests; exact old pins remain retrievable from Git history rather than a current plugin projection.
- [x] Remove the compatibility entrypoint from `skills/repo-standards` and update current docs so v1 authority resolution uses the exact immutable source commit.
- [x] Remove all root-gitignore and markdown-formatting deployment registrations with the v1 skill; verify the new v2 standard catalog already excludes both.
- [x] Retain the legitimate root `.gitignore` and ordinary ignore rules; remove only obsolete `.agents/superpowers/sdd` compatibility machinery if it has no current owner or consumer.
- [x] Search production source for readers of `.agents/contracts/agent-operating-model.json` and `.agents/contracts/unslop.json`; remove these files only when no current implementation relies on them.
- [x] Keep `.agents/unslop/` as the canonical profile location and preserve the v2 certification entry.
- [x] Delete `.agents/contracts/agent-operating-model.json`, `.agents/contracts/markdown-formatting.json`, and `.agents/contracts/unslop.json` only after confirming no active source, certification, or gate reads them.
- [x] Remove the redundant `--allow-shared-checkout` gates from current mutation tools and their wrappers, docs, and behavior tests; keep `--apply` as the explicit write request and preserve submodule rejection and the approved worktree workflow.
- [x] Preserve historical plans as historical records; do not edit past decisions merely to erase references to the retired model.

### Task 4: Whole-slice review and closeout

**Files:**

- Modify: this plan, marking completed tasks
- Modify: `roadmap.md`, recording Plan 10's commit and any bounded carry-forward
- Review: canonical source-to-generated plugin diff and active validation path

**Consumes:** Tasks 1-3 and the regenerated Marketplace projection.

**Produces:** A committed retirement slice with source, generated distribution, and gate records consistent.

- [x] Regenerate canonical plugin outputs and run repository-owned structural and shipping checks.
- [ ] Inspect the whole diff for hand-edited generated files, remaining formatter/root-gitignore routes, removed safeguards, and unrelated content churn.
- [ ] Verify Windows pre-commit and Linux hosted workflow still call the same complete logical CI target; certify only evidence actually observed.
- [ ] Complete a fresh whole-slice review and resolve all material findings.
- [ ] Update roadmap state and commit the closeout; record exact Linux parity evidence as pending Plan 11 unless the hosted system proves it for the tested commit.
