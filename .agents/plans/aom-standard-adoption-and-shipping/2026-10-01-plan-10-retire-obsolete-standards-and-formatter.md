# Retire Obsolete Standards and Markdown Formatter

**Status:** ready

> **For agentic workers:** REQUIRED SUB-SKILL: Use `subagent-driven-development` (recommended) or `executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remove obsolete Markdown-formatting and root-gitignore standards and their old deployment surface, carry the useful Markdown authoring guidance into writing-pack, and retire the formatter wheel and gate integration without weakening repository line-ending normalization or the atomic Windows/Linux CI target.

**Architecture:** Markdown prose authoring guidance belongs in the writing skill, not a separately subscribed formatting standard, consumer contract, custom formatter, or Marketplace wheel. The guidance gives a consistent readable source style without imposing a hard line-length rule or repository checker. Repository line endings remain governed by the active tracked validation hook and `.gitattributes`. Root-gitignore cleanup is no longer a standard or deployment target. Current repository-owned v2 subscriptions remain unchanged.

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
- Obsolete local contracts: `.agents/contracts/markdown-formatting.json`, `.agents/contracts/agent-operating-model.json` (v1 surface exceptions), and `.agents/contracts/unslop.json` (v1 profile roots). Confirm remaining production references before deleting each.
- Obsolete root-gitignore deployment source: the old repo-shape catalog/manifest entry, `scaffold_gitignore.py`, its shell/PowerShell wrappers and scaffold-all calls, templates, tests, and guidance. Keep ordinary root `.gitignore` policy and version-control configuration intact.

______________________________________________________________________

### Task 1: Move useful Markdown source guidance into writing-pack

**Files:**

- Modify: `skills/writing/SKILL.md` and/or add a narrowly routed reference under `skills/writing/references/`
- Modify: `.agents/playbooks/code-style.md`
- Read: current Markdown-formatting skill, formatter contract, local formatting policy, and line-ending validator

**Consumes:** The user-approved boundary that Markdown formatting does not need an AOM standard and belongs as a writing-pack capability.

**Produces:** Concise agent-facing advice for readable, consistent Markdown authoring without a line-length gate.

- [ ] Write the useful source-formatting advice in the existing writing-pack entry point; preserve the human-readable preference for consistent paragraph widths without prescribing an exact number.
- [ ] Route code-style guidance to the writing capability for Markdown authoring; remove the deleted formatter command and claims of machine-enforced wrapping.
- [ ] Preserve authored document semantics, code blocks, tables, and existing paragraph content; do not bulk-reformat unrelated files.
- [ ] Confirm that newline normalization remains separately enforced by the tracked gate and `.gitattributes`.

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

- [ ] Remove the formatter apply/check command vectors from the active repo command binding while preserving both `tools/run.py ci --apply` and `--check` invocations.
- [ ] Remove formatter fallback selection from `tools/new_plugin.py` and `tools/sync_skill_shared_references.py`; preserve their actual plugin-generation and reference-sync responsibilities.
- [ ] Remove the formatter skill from canonical plugin definitions and delete its dedicated source tests and implementation.
- [ ] Remove the safe-link-labels wheel source and generation route; ensure no current build or packaging command attempts to create or validate it.
- [ ] Remove the obsolete Markdown-formatting contract, schema, requirements, scaffolders, and formatter config from current source and consumer-facing docs.
- [ ] Rebuild Marketplace projections from canonical sources and verify the generated AOM plugin no longer includes the formatter skill or wheel.
- [ ] Confirm ordinary Markdown link validation, repository line-ending checks, and all non-formatting CI targets still run.

### Task 3: Retire root-gitignore standard and unused legacy contract records

**Files:**

- Modify: relevant current source under `skills/repo-shape/` and tests, removing the obsolete root-gitignore standard registration and scaffolder.
- Delete only after reference audit: `.agents/contracts/agent-operating-model.json` and `.agents/contracts/unslop.json`
- Preserve: root `.gitignore`, `tools/validate_agents_md.py`, the v2 subscription, and `.agents/unslop/repository.md`

**Consumes:** Plan 8 certification and live-source search for old contract references.

**Produces:** No active root-gitignore standard or stale v1 exception/profile-root contract in this repository's selected implementation.

- [ ] Remove `root-gitignore-hygiene` from the current selectable/deployment source catalog, manifest, scaffolder routes, and tests after verifying the new standard catalog already excludes it.
- [ ] Retain the legitimate root `.gitignore` and ordinary ignore rules; remove only obsolete `.agents/superpowers/sdd` compatibility machinery if it has no current owner or consumer.
- [ ] Search production source for readers of `.agents/contracts/agent-operating-model.json` and `.agents/contracts/unslop.json`; remove these files only when no current implementation relies on them.
- [ ] Keep `.agents/unslop/` as the canonical profile location and preserve the v2 certification entry.
- [ ] Update current repo-shape onboarding text so it no longer tells a current adopter to deploy retired standards; preserve historical plans as historical records.

### Task 4: Whole-slice review and closeout

**Files:**

- Modify: this plan, marking completed tasks
- Modify: `roadmap.md`, recording Plan 10's commit and any bounded carry-forward
- Review: canonical source-to-generated plugin diff and active validation path

**Consumes:** Tasks 1-3 and the regenerated Marketplace projection.

**Produces:** A committed retirement slice with source, generated distribution, and gate records consistent.

- [ ] Regenerate canonical plugin outputs and run repository-owned structural and shipping checks.
- [ ] Inspect the whole diff for hand-edited generated files, remaining formatter/root-gitignore routes, removed safeguards, and unrelated content churn.
- [ ] Verify Windows pre-commit and Linux hosted workflow still call the same complete logical CI target; certify only evidence actually observed.
- [ ] Complete a fresh whole-slice review and resolve all material findings.
- [ ] Update roadmap state and commit the closeout; record exact Linux parity evidence as pending Plan 11 unless the hosted system proves it for the tested commit.
