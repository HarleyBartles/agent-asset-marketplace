# Skill Language Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `subagent-driven-development` (recommended) or `executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Give every vendored skill field a clear linguistic role, repair repository-wide metadata and wrapper language, and prevent mechanical “use when” phrasing from returning.

**Architecture:** Extend the existing skill-frontmatter and OpenAI-agent contracts with a field-semantics table, then make doctrine and writing-skills defer to those contracts. Add structural validation around the distinctions that can be proved mechanically; repair canonical vendored sources, regenerate installed copies, and use an adversarial inventory for semantic cases that cannot safely be reduced to regex.

**Tech Stack:** Markdown, YAML, Python, pytest, repository marketplace and mesh generators.

**Spec:** Human-approved field-language model from the MARK-373 review: standalone descriptions carry trigger language; structured trigger fields answer their keys; relationship fields encode ordering; scope names ownership; wrapper prompts instruct an already-selected skill.

**Execution Strategy:** `manual` — the contract, validators, and repository-wide prose migration share one semantic model and require a single editor to adjudicate wording consistently.

## Global Constraints

- Top-level `description` is a standalone discovery sentence beginning `Use when`; it contains trigger conditions, not workflow instructions.
- `metadata.scope` is an ownership noun phrase, not a copied trigger.
- `use_when` and `do_not_use_when` values answer their field names without repeating `Use when` or `Do not use when` prefixes.
- `use_before`, `use_after`, `use_with`, `use_instead`, and `related_skills` contain skill identifiers and carry only their defined relationship semantics.
- `interface.short_description` is concise human-facing capability language; it is not required to begin `Use when`.
- `interface.default_prompt` directly instructs an already-selected skill and names that skill; it must not be an orphaned conditional/cache of the trigger description.
- Canonical prose uses plain skill identifiers, with namespace qualification only when disambiguation is required; client sigils are not canonical syntax.
- Edit canonical plugin sources first and regenerate `.agents/skills/`; do not hand-edit generated installed copies.
- Preserve deliberate safety and authority constraints by moving them to the owning body or structured relationship field when they do not belong in discovery prose.
- Do not run paid model evaluation. Keep PR #311 Draft.

### Task 1: Establish the field-language contract

**Files:**
- Modify: `.agents/contracts/skill-frontmatter.md`
- Modify: `.agents/contracts/openai-agent-yaml.md`
- Modify: `.agents/doctrine/first-party-skills.md`
- Modify: `.agents/doctrine/skill-standards-policy.md`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/writing-skills/SKILL.md`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/writing-skills/references/skill-authoring-checklist.md`
- Test: `tests/test_workflow_contracts.py`

- [ ] **Step 1: Add RED contract tests.** Assert the contracts define distinct semantics for description, scope, trigger lists, relationship fields, short description, and default prompt; reject doctrine that requires `Use when` in wrapper prompts.
- [ ] **Step 2: Verify RED.** Confirm the focused test fails against the current policy wording.
- [ ] **Step 3: Write the contract.** Add the approved field table, positive examples, prohibited mechanical constructions, and plain-identifier rule.
- [ ] **Step 4: Align doctrine and writing-skills.** Remove the blanket wrapper `Use when` requirement and make authoring guidance route to the canonical contracts.
- [ ] **Step 5: Run focused contract tests.** Confirm the field semantics are explicit and non-duplicative.

### Task 2: Make semantic regressions mechanically visible

**Files:**
- Modify: `tools/skill_validation.py`
- Modify: `tools/review_preflight.py` only if its existing scan is the correct integration seam
- Modify: `tests/test_workflow_contracts.py`
- Modify: focused validator tests selected after inspecting current coverage

- [ ] **Step 1: Add RED validation cases.** Cover repeated field prefixes, malformed `Use when use`, `to use when`, orphaned `default_prompt: Use when`, copied description/scope values, missing skill identity in default prompts, workflow leakage markers in descriptions, and slash/dollar client sigils.
- [ ] **Step 2: Separate hard failures from review findings.** Hard-fail deterministic grammar/schema defects; report workflow-like description clauses for adjudication rather than pretending regex can establish semantics.
- [ ] **Step 3: Implement the smallest shared validator.** Keep parsing and diagnostics deterministic, path-specific, and actionable.
- [ ] **Step 4: Prove RED/GREEN behavior.** Run focused validator tests and inspect every diagnostic category.

### Task 3: Repair canonical vendored skill language

**Files:**
- Modify: affected canonical `SKILL.md` and `agents/openai.yaml` files under `codex-marketplace/plugins/`
- Regenerate: `.agents/skills/`
- Test: `tests/test_workflow_contracts.py` and affected validator tests

- [ ] **Step 1: Inventory canonical roots.** Record all 77 roots/74 unique names and classify exact defects separately from semantic-review candidates.
- [ ] **Step 2: Repair frontmatter field semantics.** Rewrite descriptions, scopes, trigger lists, exclusions, and relationship fields without weakening ownership, authority, or safety conditions.
- [ ] **Step 3: Repair OpenAI wrappers.** Replace `to use when`, orphaned conditionals, circular prompts, misleading cross-routing, duplicated trigger prose, and client sigils with concise capability descriptions and direct prompts.
- [ ] **Step 4: Review workflow-heavy descriptions manually.** Retain genuine trigger conditions; move procedural instructions into bodies or structured relationship metadata.
- [ ] **Step 5: Regenerate installed skills and marketplace surfaces.** Run `py -3 tools/run.py installed-skills --apply` and `py -3 tools/run.py mesh --apply`.
- [ ] **Step 6: Run focused suites and full inventory scans.** Require zero deterministic defects and adjudicate every semantic-review candidate.

### Task 4: Close and publish the sub-slice

**Files:**
- Modify: this plan
- Modify: `.agents/plans/2026-09-06-mark-373-operating-system.checkpoint.md`
- Modify: PR #311 body

- [ ] **Step 1: Review the complete diff adversarially.** Check semantic accuracy, grammar, trigger discovery, relationship direction, safety preservation, generated-source custody, and absence of client syntax.
- [ ] **Step 2: Mark plan and checkpoint truthfully.** Record the focused evidence and any irreducibly manual boundary without producing a duplicate receipt.
- [ ] **Step 3: Commit normally.** Let the tracked pre-commit apply/check gate validate the staged state.
- [ ] **Step 4: Push and update Draft PR #311.** Keep it Draft and describe the language contract and repo-wide migration.
- [ ] **Step 5: Verify publication.** Confirm clean tree, local/remote head equality, base `main`, and Draft state.

## Acceptance evidence

- The contracts state one coherent linguistic role for every routing and wrapper field.
- Canonical vendored sources contain no known malformed trigger phrase, duplicated field prefix, orphaned wrapper condition, or client invocation sigil.
- `scope` values describe ownership rather than repeat descriptions.
- Default prompts identify the selected skill and give a direct, grammatical instruction.
- Deterministic validators fail on mechanically provable defects and avoid claiming to prove semantic quality they cannot establish.
- Generated installed copies match canonical sources.
- Focused tests and the normal hooked gate pass; PR #311 remains Draft.

## Plan-readiness self-review

- The contract precedes validation and migration, so the wording changes have one authority.
- Deterministic and judgment-based findings are separated.
- Canonical and generated custody are explicit.
- The 77-root inventory is finite and every previously reported defect class has a task and acceptance check.
- No consequential language-model evaluation is required.

**Plan-readiness rating:** 9.2/10.
