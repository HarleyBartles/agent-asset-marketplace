# Superpowers Repository Artifact Discovery Implementation Plan

**State:** implementation pending; this plan is the reviewable draft handoff.

> **For agentic workers:** REQUIRED SUB-SKILL: Use `executing-plans` to implement this plan task by task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make Superpowers Plus skills discover and consult applicable repository-resident workflow guidance when it exists, without requiring consumers to use this repository's `.agents/runbooks/` layout.

**Architecture:** Keep portable workflow technique in the canonical Superpowers Plus skill sources and express repository guidance as a conditional overlay. The skills should follow paths and inventories declared by each repository, read only material relevant to the active workflow, and continue with the portable baseline when no applicable local artifact exists. Regenerate installed skill projections from canonical marketplace sources.

**Tech Stack:** Markdown skills and references, marketplace generation, installed skill projections, repository mesh validation.

**Spec:** The approved direction in this task: replace mandatory repository runbook assumptions with guidance to read applicable repository-resident artifacts when they exist.

**Execution Strategy:** `executing-plans`, because the shared discovery contract and its stage-specific applications should be changed and reviewed as one coordinated slice.

## Global Constraints

- Edit canonical sources under `codex-marketplace/plugins/superpowers-plus/skills/`; generated `.agents/skills/` copies are downstream.
- Do not require a particular repository directory, filename, inventory, or runbook convention from marketplace consumers.
- Preserve this repository's own runbook requirements in its local guidance and keep portable skill technique intact.
- Read local artifacts only when the repository declares them and they apply to the active workflow; do not load every local guide speculatively.
- Do not add content-matching tests that merely assert the wording or mirror source strings.
- Keep the implementation scoped to Superpowers Plus repository-artifact discovery and its generated projections.

## Review Focus

- A consumer with workflow guidance in a non-`.agents/` location can follow its declared route without being told to search a fixed path.
- A consumer with no applicable workflow artifacts can proceed using the portable skill baseline without a false missing-runbook failure.
- This repository still consults its applicable runbooks and playbooks through its local declared workflow.
- No unrelated stage technique, routing ownership, or generated skill content changes.

______________________________________________________________________

### Task 1: Define the portable repository-artifact discovery contract

**Files:**

- Modify: `codex-marketplace/plugins/superpowers-plus/skills/using-superpowers-plus/SKILL.md`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/using-superpowers-plus/references/bootstrap-routing.md`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/using-superpowers-plus/references/superpowers-composition.md`

**Interfaces:**

- Consumes: repository-declared agent guidance and any local workflow inventory relevant to the active request.

- Produces: one portable rule for locating and conditionally reading applicable local guidance, including how to proceed when none exists.

- [x] Replace assumptions that `.agents/playbooks/INDEX.md` and `.agents/runbooks/INDEX.md` are universal discovery paths with repository-declared discovery, when available.

- [x] Preserve bounded topical discovery: consult only relevant local artifacts, and do not fan out across all playbooks or guides.

- [x] Remove the composition contract that makes a stage runbook a required composition root for every consumer; retain the relationship as this repository's local convention where applicable.

- [x] State that absent local artifacts do not block portable baseline execution, while surfacing a material assumption or repository-local gap when needed.

### Task 2: Align stage skills with conditional local guidance

**Files:**

- Modify: `codex-marketplace/plugins/superpowers-plus/skills/brainstorming/SKILL.md`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/executing-plans/SKILL.md`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/subagent-driven-development/SKILL.md`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/requesting-code-review/SKILL.md`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/writing-plans/SKILL.md`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/finishing-a-development-branch/SKILL.md`

**Interfaces:**

- Consumes: the portable discovery contract established in Task 1.

- Produces: stage-specific instructions that consult applicable repository-resident workflow guidance when present and retain the skill's baseline when absent.

- [x] Replace mandatory `.agents/runbooks/<stage>.md` instructions with conditional consultation of repository-declared artifacts relevant to that stage.

- [x] Preserve any specific local constraints already required by this repository through its own root guidance and runbook system.

- [x] In `subagent-driven-development`, preserve the controller's responsibility for enforcing implementation and handoff requirements without making a particular runbook the universal source.

- [x] Review all remaining fixed-path runbook requirements within the Superpowers Plus skill tree and either update in-scope workflow assumptions or document why a remaining path is intentionally repo-specific.

### Task 3: Regenerate and verify the skill package

**Files:**

- Regenerate: `.agents/skills/superpowers-plus/` through the owning marketplace and skill projection commands.
- Regenerate: mesh or marketplace indexes only if the owning commands report them stale.
- Modify: `tests/test_workflow_contracts.py` to remove the obsolete exact-path and source-placement assertions.

**Interfaces:**

- Consumes: canonical source changes from Tasks 1 and 2.

- Produces: synchronized generated projections and a reviewable Draft PR with source, projection, and validation evidence.

- [x] Audit the canonical Superpowers Plus skill tree for remaining mandatory `.agents/runbooks/` and `.agents/playbooks/` consumer assumptions; inspect each match in context.

- [x] Regenerate through `py -3 tools/run.py marketplace --apply` and the required mesh command; inspect the generated diff for unrelated changes.

- [x] Confirm canonical sources and installed projections agree using the repository's owning validation commands.

- [x] Do not add tests unless implementation reveals a genuine behavioral validation gap; avoid tautological wording checks. The paired baseline probes completed both tasks without exposing a behavior gap, so no scenario test was retained.

- [ ] Update the existing pressure-repair contract test only to remove obsolete exact-path and source-placement assertions; do not replace them with wording checks.

- [ ] Review the complete diff for portable wording, preserved local policy, source custody, and generated projection scope.

- [ ] Commit normally and let the tracked pre-commit hook run the complete staged gate; push and open or update a Draft PR to `main`, then verify its branch, head, and checks in GitHub.
