# Optional Standard Adoption Assets Implementation Plan

**Status:** completed-awaiting-retirement. Final reviewed implementation head: `d6f8947f1d0ada29ab604aa2918d19564ea2625d`.

> **For agentic workers:** REQUIRED SUB-SKILL: Use `subagent-driven-development` (recommended) or `executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Give agents self-contained, optional AOM assets that help a repository adopt selected standards while leaving deployed files and compliance policy repository-owned.

**Architecture:** Put each starter or checker beside the standard that owns it. Adoption is an explicit agent task that reads the pinned definition, selects assets, adapts them to the repository, and records certification only after the required behavior exists. Templates and checker scripts are standalone files that repositories can copy and change; no installer, submodule, runtime AOM dependency, or automatic bus registration is introduced.

**Tech Stack:** Markdown standard assets, JSON/TOML examples, standard-library Python checker starters and pytest, existing Marketplace builder.

**Spec:** [Approved AOM design](../../specs/2026-09-30-aom-standard-adoption-and-shipping.md).

**Roadmap:** [AOM adoption and shipping](roadmap.md), Plan 2. Planning baseline is the Plan 1 completion commit `474481835`; source baseline is Plan 1 implementation commit `345e39234`.

**Execution Strategy:** `executing-plans`, following the local [planning runbook](../../runbooks/planning.md), because adoption guidance, reusable assets, and checkers share one evolving asset authority model and must be validated together in isolated installs. Inline continuity makes the distinction between definition, optional asset, and consumer-owned deployment explicit. Obtain a fresh whole-change review at handoff.

## Global Constraints

- AOM availability offers capabilities; only an explicit repository subscription adopts a standard.
- A repository records the standard ID, source repository, immutable commit, definition path, and readable certification reference; the checker validates structure only.
- Every AOM adoption requires a root `AGENTS.md` routing to its subscription and applicable certification; this does not adopt the full AGENTS standard.
- The default readable certification path is `.agents/contracts/standards-certification.md`; using it does not adopt the separate doctrine/contracts standard.
- Assets are optional unless their standard definition marks the behavior itself as required. Selecting a template does not make its original bytes a compliance requirement.
- Do not scaffold automatically, overwrite authored files, require empty headings, impose fixed book inventories, install a bus target, add a source submodule, or revive `repo.local_skills`.
- `.agents/plugins/` holds repo plugin declarations; `.agents/skills/` holds repo-authored skills only.
- Checkers are consumer-owned starting points. They report only configured mechanical facts and cannot certify semantic compliance.
- Keep old v1 runtime and resources intact for current consumers; migration and removal belong to Plan 6.
- Edit canonical skills and `src/plugin-definitions/`, regenerate `dist/`, and commit through the normal hook. Keep Python checkers portable and avoid redundant shell/PowerShell wrappers.

## Review Focus

- A single runbook or playbook subscription must be independently useful without implied companion standards; cover with Task 2 adoption scenarios.
- Existing authored files must survive deployment unchanged unless the agent performs an explicitly requested edit; cover with Task 1 preservation scenarios.
- Checker success must not become a semantic certification claim; cover with checker diagnostics and Task 5 guided adoption cases.
- A starter or script installed from one skill must not depend on the source checkout, another plugin, or ambient plugins; cover with Task 5 isolated-package tests.
- Optional templates must not imply current assets are required or an implementation is complete merely because files exist; cover with skill behavior probes and certification guidance.

## File and Interface Map

Canonical ownership and destination:

| Owner                      | New optional material                                                                                                                                     |
| -------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `repo-standards`           | Editable v2 subscription example, root `AGENTS.md` adoption router example, certification example, adoption workflow and check-before-certifying guidance |
| `runbook-composition`      | Five stage guide starters and a repository-editable mechanical checker starter                                                                            |
| `playbook-composition`     | A small set of concern examples and an independent mechanical checker starter                                                                             |
| `agents-routing`           | Editable AGENTS budget checker starter, default warning at 55 lines and error at 100 lines                                                                |
| `agent-doctrine-contracts` | Editable placement, JSON validity, local-link, and candidate reachability checker starter with explicit scope limits                                      |
| `repo-agent-assets`        | Codex/Devin native Git-dependency examples and declaration checks                                                                                         |
| `review-entrypoint`        | Editable root `REVIEW.md` starter                                                                                                                         |
| `contribution-entrypoint`  | Editable root `CONTRIBUTING.md` starter                                                                                                                   |

New content remains inside these owner skills under `assets/`, `references/`, and `tests/`. Any starter `SKILL.md` route points to its material using links that resolve within the installed AOM package. Deployment is an agent editing the consumer repository; there is no copy command whose successful exit records subscription or certification.

## Task 1: Adoption workflow and common entrypoint assets

**Files:** Modify `skills/repo-standards/SKILL.md` and `references/adoption-and-certification.md`; add `assets/templates/operating-standards-v2.example.json`, `assets/templates/AGENTS.md.example`, and `assets/templates/standards-certification.md.example`; add behavior cases under `tests/behavior/` and evaluator-only expectations under `tests/evaluator-only/`.

**Consumes:** Plan 1 subscription schema, checker, pinned reader, adoption guide, standards catalog.

**Produces:** One discoverable adoption method that uses pinned definitions, selects only requested standards/assets, updates only necessary root routing, and certifies the actual implementation.

- [x] Add fresh-context scenarios before guidance changes: one runbook standard requested in an empty repo; adoption requested with an existing authored root `AGENTS.md`; a partially deployed standard whose required behavior is not yet present; and an update request against a current existing pin.
- [x] Add editable examples for a v2 subscription row, minimal root `AGENTS.md` adoption routing, and readable standards certification. Mark placeholders as instructions to the adopting agent, not content to claim as implemented. Include a condition requiring the agent to fill factual paths and drift controls before writing a certification claim.
- [x] Update `repo-standards` adoption guidance to read source and commit before selecting assets, preserve existing authored content, add only the requested subscription and its mandatory common adoption surfaces, implement that standard's required invariants, and report partial adoption without recording false compliance.
- [x] State explicit upgrade handling: compare the newly requested definition with the existing pinned implementation; preserve the old pin until the reconciliation task updates implementation and certification. Do not issue a stale-version alarm during ordinary Marketplace refresh.
- [x] Probe the cases in fresh implementation-time contexts. Confirm existing content is retained, root AGENTS is initialized if absent, one standard does not activate neighboring standards, and certification waits for implemented obligations. Record results in off-repo task scratch.
- [x] Run `py -3 tools/run.py marketplace --apply`, inspect installed-package links, and commit source, behavior fixtures, examples, and generated AOM projections through the normal hook.

**Exit:** An agent can make a narrow standard adoption concrete without an installer or an unsupported compliance claim.

## Task 2: Independent runbook and playbook starter sets

**Files:** Add `assets/runbooks/{design,planning,implementing,code-review,pr}.md`, `scripts/check_runbooks.py`, and `tests/scripts/test_check_runbooks.py` under `skills/runbook-composition/`; add `assets/playbooks/{testing,security,code-review}.md`, `scripts/check_playbooks.py`, and `tests/scripts/test_check_playbooks.py` under `skills/playbook-composition/`; update both owning `SKILL.md` files and behavior cases under their `tests/`.

**Consumes:** The definitions in `skills/runbook-composition/references/standard.md` and `skills/playbook-composition/references/standard.md`, plus Task 1 adoption workflow.

**Produces:** Selectable lifecycle-stage guide examples and distinct concern guide examples. No template imposes a universal section list.

- [x] Write behavior prompts for runbook-only adoption, playbook-only adoption, and combined adoption. Require a selected runbook to be a lifecycle stage, a selected playbook to own a cross-stage concern, each to stand alone, and combined routes to name only applicable books.
- [x] Create the five stage starters for design, planning, implementation, code review, and PR work. Make each one an editable guide with ordinary stage-specific guidance and completion cues; do not add empty capability/doctrine/contracts headings or repo-specific commands.
- [x] Create a small set of concern examples (testing, security, and code review) that can be used from multiple stages. Keep code review concern guidance distinct from the code-review lifecycle runbook.
- [x] Implement each checker with `--repo-root PATH`, repeatable `--document PATH`, optional repeatable `--route-source PATH`, and read-only `--check`. Paths are repository-relative. Report absent or empty selected files, broken local Markdown links, and selected documents not linked from any supplied Markdown route source. Reject an empty document selection. Do not require fixed headings, counts, directory names, reciprocal edges, or infer category compliance from keywords. Diagnostics state that semantic classification, effectiveness, non-Markdown routing, and usefulness need repository review.
- [x] Add behavior tests showing the runbook checker accepts a minimal valid stage document without prescribed headings and resolves inline/reference links with angle-bracket destinations containing spaces or parentheses, ignores link-shaped text in inline/fenced code, checks reference-style images, permits ordinary bracketed prose and task-list markers, and defaults to read-only check mode without an explicit flag. The playbook checker accepts a standalone concern guide and equivalent links; both reject broken inline/reference links and a document missing from supplied Markdown routes. A combined repo connects one relevant stage to one concern without all-to-all wiring.
- [x] Update the two owner skills to distinguish starter material from required invariants, explain that repositories may take any subset or none, and identify agent-led deployment and repository ownership.
- [x] Run `py -3 -m pytest -q skills/runbook-composition/tests/scripts/test_check_runbooks.py skills/playbook-composition/tests/scripts/test_check_playbooks.py`, then `py -3 tools/run.py marketplace --apply`; inspect the generated links and commit the new assets, tests, guidance, and projections through the normal hook.

**Exit:** Either standard can be adopted alone, optional examples have useful starting content, and no shipped checker invents universal document structure.

## Task 3: AGENTS and doctrine/contracts checker starters

**Files:** Add `assets/check_agents_md.py`, `tests/scripts/test_check_agents_md.py`, and behavior fixtures under `skills/agents-routing/`; add `assets/check_agent_docs.py`, `tests/scripts/test_check_agent_docs.py`, and behavior fixtures under `skills/agent-doctrine-contracts/`; update both owning `SKILL.md` files and definitions only if the current text needs asset details clarified.

**Consumes:** Task 1 adoption workflow; the AGENTS and doctrine/contracts definitions from Plan 1.

**Produces:** Editable examples for each standard's required checker, with honest mechanical limits and no universal repository policy beyond the adopted pledge.

- [x] Add AGENTS checker scenarios for 54/55/56 and 99/100/101 line boundaries, root and nested routers, a repository-selected changed budget, and arbitrarily many routers not failing by count alone.
- [x] Implement `check_agents_md.py --repo-root PATH --check` over in-scope `AGENTS.md` files, including untracked files, with repeatable `--exclude GLOB`, `--warn-lines N`, and `--error-lines N` options. Defaults warn above 55 lines and fail above 100. Do not impose maximum file count or universal placement rules; provide clear `--help`, read-only execution, and diagnostics that report configured thresholds. Keep the script easily editable by the consumer.
- [x] Add doctrine checker scenarios for required store placement, valid JSON, broken inline/reference local links and images, unlinked Markdown and structured agent-governance documents, code examples, and routes the checker cannot observe. Explicitly distinguish JSON syntax checks from schema validation and static Markdown links from harness/skill routing.
- [x] Implement `check_agent_docs.py --repo-root PATH --check` to inspect agent documents under `.agents/doctrine/` and `.agents/contracts/`, parse JSON with the standard library, resolve local Markdown links, and report Markdown and structured-format candidate documents without inbound Markdown links. Accept repeatable `--route-root PATH` and `--exclude GLOB` options for known non-Markdown routes and repository-specific boundaries. The result is an advisory candidate report, not proof of semantic reachability.
- [x] Test both helpers from temporary repositories, including advisory candidates for unlinked Markdown and structured agent contracts. Confirm commands do not write, execute declared contract commands, or pass a semantic certification result. Test customization through explicit CLI options or local editable constants, as appropriate for each starter.
- [x] Update each standard's skill with its starter path, required adaptation step, CI obligation when CI exists, and clear checker limits. Run `py -3 -m pytest -q skills/agents-routing/tests/scripts/test_check_agents_md.py skills/agent-doctrine-contracts/tests/scripts/test_check_agent_docs.py`, regenerate with `py -3 tools/run.py marketplace --apply`, and commit through the normal hook.

**Exit:** Adopting repos can bootstrap their required checker obligation while keeping budgets, locations, routing policy, and semantic review repository-owned.

## Task 4: Plugin, review, and contribution examples

**Files:** Add `assets/examples/marketplace.json.example`, `codex-config.toml.example`, and `devin-config.json.example` plus `assets/check_plugin_subscriptions.py` and its tests under `skills/repo-agent-assets/`; add `assets/REVIEW.md.example` under `skills/review-entrypoint/`; add `assets/CONTRIBUTING.md.example` under `skills/contribution-entrypoint/`; update these owners and their behavior fixtures.

**Consumes:** The three Plan 1 definitions and Task 1 adoption workflow.

**Produces:** Self-contained optional examples for repository Git plugin declarations, a root review entrypoint, and a root contribution entrypoint.

- [x] Add one behavior scenario per standard: a fresh clone resolves declared Git plugin dependencies subject to access; an inline `REVIEW.md` is valid without review books; a useful root `CONTRIBUTING.md` is valid without other adopted standards.
- [x] Add Codex catalog and project activation examples plus a Devin native repository declaration example. Use clearly marked sample repository URLs and plugin paths; demonstrate both a floating `main` ref and immutable SHA as alternatives, never both in one declaration. Do not include marketplace source submodules or installed skill copies.
- [x] Add a standard-library read-only plugin declaration checker starter with `--repo-root PATH --check`. Validate local marketplace/catalog JSON, Codex TOML syntax, Devin JSON syntax, source selectors, the local catalog registration, and activations for that local catalog without requiring activation of available entries, inspecting unrelated marketplace settings, requiring optional Codex marketplace refs, fetching remotes, or claiming authentication/runtime success. Keep host-specific differences visible and report which harness surfaces were checked.
- [x] If the checker uses standard-library `tomllib`, state the Python 3.11 minimum in its help and owner guidance. The optional starter may be replaced by the consumer's native parser or checker.
- [x] Add inline-capable `REVIEW.md` and `CONTRIBUTING.md` starter documents with concise factual prompts and useful routing examples. Do not require additional books, fan-out, or a universal heading layout.
- [x] Add focused tests for valid and malformed native declarations, conflicting local activation, unrelated Codex marketplace coexistence, optional Codex ref omission, internal catalog path validity, and source-selector exclusivity. Probe inline-only review/contribution guidance without requiring section names or routing files. Update owners with optional status and deployment guidance, run `py -3 -m pytest -q skills/repo-agent-assets/tests/scripts/test_check_plugin_subscriptions.py`, regenerate with `py -3 tools/run.py marketplace --apply`, then commit through the normal hook.

**Exit:** The three standards have optional assets that help adoption without creating harness-independent installation claims or extra document obligations.

## Task 5: Package closure and adoption behavior review

**Files:** Add `tests/shipping/test_aom_standard_assets.py`; update only metadata/source inventories needed to include the new assets in the self-contained AOM package; add final fresh-context evaluator notes under owning skills' `tests/evaluator-only/`.

**Consumes:** Tasks 1-4 canonical assets, tests, and generated AOM package.

**Produces:** Isolated proof that optional assets and checker starters are available from the package and can be adopted without a source checkout.

- [x] Copy generated `dist/plugins/agent-operating-model` into a temporary installed directory, then copy each selected checker from the isolated package into the consumer's chosen tool location. Run those consumer-owned copies with the consumer as cwd and no Marketplace `PYTHONPATH`. Assert successful and failing output describes only mechanical results and read-only checks leave the consumer tree unchanged.
- [x] Resolve all internal relative links from the affected skill entrypoints and standard definitions inside the isolated package. Assert checker scripts import only standard-library modules and sibling files included in that package.
- [x] Run fresh-context guided adoption probes for selective book choice, root-file preservation, checker limits, native plugin declaration boundaries, and REVIEW/CONTRIBUTING standalone adoption. Compare agent decisions with the spec, not exact wording. Fix any rationalization that turns optional content into required adoption.
- [x] Confirm AOM plugin inventory and generated manifest include all owning skills and deployed starter assets without adding evaluator-only expectations, local skills inventories, or duplicate platform wrappers. Keep first-party provenance intact.
- [x] Run `py -3 tools/run.py marketplace --apply`, focused checker suites, and `py -3 -m pytest -q tests/shipping/test_aom_standard_assets.py`. The normal commit hook supplies the complete repository gate.
- [x] Stage intended source, tests, package metadata, and generated projections; commit. Confirm the commit is Plan 2 scope and the worktree is clean.
- [x] Obtain fresh whole-change review against this plan and approved spec. Fix Critical and Important findings, regenerate affected outputs, and repeat focused checks. Final fresh review of base `1847f5d9c` through head `d6f8947f1` found no Critical or Important issues; the one Minor CLI finding was fixed, tested, regenerated, and re-reviewed.
- [ ] Mark this plan `completed-awaiting-retirement` after the fully reviewable handoff. Keep the roadmap active and preserve its future plans.

**Exit:** Repositories can select, edit, replace, or omit AOM assets; isolated package behavior supports that workflow, and self-certification remains a repository-owned claim.

## Handoff boundaries

- Plan 2 introduces optional assets. It does not migrate Marketplace's own subscription/runtime, implement the command bus, or change hook/CI behavior; those remain Plans 3 and 6.
- Plan 3 owns portable CLI interfaces, optional bus starter, complete Windows/Linux hook parity, and cross-platform text normalization.
- Legacy v1 resources remain untouched until Plan 6.
- The repository does not receive a fixed runbook or playbook inventory because AOM offers these examples.
