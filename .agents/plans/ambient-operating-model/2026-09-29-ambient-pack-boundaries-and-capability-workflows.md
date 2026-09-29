# Ambient Pack Boundaries and Capability-Based Workflows

**Status:** executing

> **For agentic workers:** REQUIRED SUB-SKILL: Use `subagent-driven-development` (recommended) or `executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make Superpowers+, Repo Worker Pack, MCP Usage Pack, and Unslop+ usable as ambient agent capabilities without imposing consumer subscriptions, layouts, or standards, and let portable runbooks/playbooks require capabilities rather than exact ambient skill names.

**Roadmap:** Plan 3 of [Ambient Operating Model and Selectable Standards](roadmap.md), following the index-mesh retirement and selectable-standards runner bridge.

**Execution Strategy:** `executing-plans` - The pack audit and capability contract share one portable-guidance boundary, but each edit group has focused tests. The same integration context is valuable because skill selection language, repo-owned skill exceptions, and required-capability failure behavior must agree across source, templates, validators, and generated packages. Independent per-task contexts would add interface handoffs without reducing the integration risk.

## Scope and authority

- Use the approved design at `.agents/specs/2026-09-28-ambient-operating-model-and-selectable-standards-design.md` and this roadmap as authority.
- Audit all five intended ambient plugins: Superpowers+, Repo Worker Pack, MCP Usage Pack, Unslop+, and Agent Operating Model. Plan 2 owns the Agent Operating Model catalog redesign; this plan verifies its boundary and focuses changes on the four companion packs.
- Preserve the distinct roles: Superpowers+ routes workflow; Repo Worker Pack provides general worker capabilities; MCP Usage Pack guides use of available MCP tools; Unslop+ provides optional writing-quality/profile capabilities; Agent Operating Model offers independently deployable standards.
- Portable runbooks and playbooks state capabilities they require. At runtime, the agent inspects available skills and selects a suitable provider. A genuinely repository-owned skill may be named exactly. If a required capability has no suitable provider, the agent stops and reports it.
- Keep consumer repositories out of scope. Do not edit Rooms-Mostly or any other consumer checkout.
- Do not restore index mesh, index generators, or generated index files.
- Edit canonical source under `skills/`, `shared/`, and `src/plugin-definitions/`; regenerate `dist/` and `.agents/skills/` through the repository commands.

## Current evidence and file map

Plugin membership is declared in `src/plugin-definitions/<plugin>/contents.json`; canonical first-party skill source is under `skills/<skill-id>/`. Marketplace output under `dist/` and installed `.agents/skills/` are generated.

| Concern                                            | Current source seam                                                                                                                                                                                                                                                                                                              | Planned responsibility                                                                                                                                                                                                                                      |
| -------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Superpowers+ workflow and local-guidance discovery | `skills/using-superpowers-plus/SKILL.md`, `skills/using-superpowers-plus/references/bootstrap-routing.md`, `skills/using-superpowers-plus/references/superpowers-composition.md`; membership in `src/plugin-definitions/superpowers-plus/contents.json`                                                                          | Preserve workflow routing while removing fixed consumer inventory/path assumptions and exact ambient provider requirements from portable contracts. PR #334 is a fixed-case starting point, not the audit result.                                           |
| Repo Worker Pack capabilities                      | `skills/repo-worker-base/`, `skills/base-doctrine/`, `skills/refreshing-installed-skills/`, and the other members listed in `src/plugin-definitions/repo-worker-pack/contents.json`                                                                                                                                              | Separate general worker advice from consumer policy and runner dependencies. Do not reintroduce refresh or mesh subscription requirements.                                                                                                                  |
| MCP guidance                                       | `skills/using-*-mcp/` and `src/plugin-definitions/mcp-usage-pack/contents.json`                                                                                                                                                                                                                                                  | Treat tool availability as runtime state. Instructions must provide a safe missing-tool path and must not require a consumer to configure or subscribe to an MCP integration.                                                                               |
| Unslop+                                            | `skills/unslop-profiles/`, `skills/unslop-engine/`, and `src/plugin-definitions/unslop-plus/contents.json`                                                                                                                                                                                                                       | Keep profile discovery/evaluation available as agent capabilities; do not make the whole pack or its profile engine a consumer standard. Distinguish optional deployment of a profile from ambient skill availability.                                      |
| Agent Operating Model consistency check            | `skills/repo-standards/`, `skills/repo-shape/references/operating-standards-catalog.json`, composition/deployment source and `src/plugin-definitions/agent-operating-model/contents.json`                                                                                                                                        | Confirm that the catalog remains optional, declarations control enforcement, and no companion pack contradicts this boundary. Do not reopen Plan 2's composition design absent a concrete contradiction.                                                    |
| Runbook/playbook capability contract               | `skills/repo-shape/references/repository-runbook-standard.md`, `skills/repo-shape/references/repository-shape-manifest.json`, `skills/repo-shape/templates/`, `skills/repo-shape/scripts/` and tests; semantics owned by `skills/repo-composition/`; current repository examples in `.agents/runbooks/` and `.agents/playbooks/` | Define the portable requirement format, migrate repository examples away from exact ambient requirements, validate repository-owned exact references, retain graph validation, scaffold capability language, and fail clearly on unmet required capability. |
| Shipped products and docs                          | `src/plugin-definitions/*/contents.json`, `docs/decisions/README.md`, `docs/decisions/`, `docs/`                                                                                                                                                                                                                                 | Record source-located assumption findings/dispositions and promote durable role/contract decisions. Regenerate all owned outputs.                                                                                                                           |

Before implementation, inspect the live source and identify each actual instruction with a consumer layout, runbook/playbook, marketplace subscription, ambient exact-name, unavailable-tool, or profile-deployment assumption. Include command examples that invoke a bundled ambient skill through a consumer's `.agents/skills/` projection and stale index-mesh commands. Record source paths and disposition in the audit artifact. The file map is an initial map, not permission to skip other pack members found by inventory.

## Interface decisions

1. **Capability requirement:** runbooks/playbooks describe the needed action or expertise in human-readable terms and mark whether it is required. They do not prescribe which ambient skill supplies it.
2. **Repository-owned exception:** where a consumer genuinely owns a skill that is part of its local contract, the workflow may identify that exact local skill separately from the capability statement. The validator checks the repository-owned declaration against the consumer's declared local-skill custody, not against ambient marketplace plugin names.
3. **Runtime resolution:** the agent inspects the skills actually available in its current harness, selects a suitable provider for each required capability, and invokes that skill. Skill names/descriptions are evidence for selection, not proof of a repository subscription or standard adoption.
4. **Required failure:** when no suitable provider is available for a required capability, the agent stops before performing the dependent step and reports the missing capability. Optional capabilities may be skipped with the omission reported. No unrelated provider may be silently substituted.
5. **No runtime detector:** hosted CI validates the authored composition syntax, local exact-skill declarations, links, and runbook/playbook graph. It does not attempt to inspect a Codex harness or assert that an ambient capability exists at validation time.

Use the smallest contract extension consistent with current Markdown and parser behavior. Do not add a new runtime skill registry, plugin-subscription inference, or requirement that consumers use `.agents/runbooks/` or `.agents/playbooks/` unless they explicitly adopt the applicable standard.

## Task 1: Complete and record the five-plugin assumption audit

**Files:** all source members named by the five plugin `contents.json` files; `docs/ambient-plugin-assumption-audit.md` (new); `docs/decisions/README.md` and a new ADR if durable decisions need promotion.

**Consumes:** approved design, Plans 1 and 2, PR #334 as a known fixed Superpowers+ case.

- [x] **Step 1: Inventory actual plugin membership and consumer-facing assumptions**

Read each plugin membership manifest, then inspect every member skill and bundled reference/template/script for references to consumer directory layouts, runbook/playbook inventories, required marketplace subscriptions, exact ambient skill names, configured MCP tools, and consumer-deployed Unslop profiles. Exclude unrelated occurrences such as example fixture filenames unless behavior depends on them.

- [x] **Step 2: Classify each material finding by owner and effect**

Classify it as valid ambient workflow/capability guidance, deployable Agent Operating Model standard, explicitly repository-owned policy, consumer-specific example, or invalid consumer-layout/subscription/provider assumption. For each finding, capture the exact source path, current effect, disposition, and whether a source change or explicit keep decision is required.

- [x] **Step 3: Add the source-located audit record and durable decisions**

Write `docs/ambient-plugin-assumption-audit.md` with a row for each finding and a coverage statement proving that all plugin members were considered. Record why the five plugin roles remain distinct and why their ambient presence does not imply consumer adoption. Promote lasting architecture or normative policy to an ADR and update `docs/decisions/README.md`; keep file-by-file findings in the audit document.

- [x] **Step 4: Verify audit completeness against manifests**

Compare the audit coverage against all skill names in the five current manifests. Re-run the targeted source searches used for discovery and classify every material hit. Confirm that `docs/ambient-plugin-assumption-audit.md` contains no generated-output paths presented as canonical edit locations.

**Task exit:** A reviewer can trace each material finding to canonical source and see its disposition; all five ambient products are covered, with Agent Operating Model explicitly checked against the optional catalog boundary shipped in Plan 2.

## Task 2: Correct companion-pack role and portability assumptions

**Files:** only source assets identified as actionable in Task 1, expected under `skills/` and `src/plugin-definitions/` for `superpowers-plus`, `repo-worker-pack`, `mcp-usage-pack`, or `unslop-plus`; the corresponding `tests/` beside changed skills.

**Consumes:** completed Task 1 audit.

- [ ] **Step 1: Preserve repository-guidance discovery without fixed layout assumptions**

Review the current PR #334 Superpowers+ correction and every other repo-backed workflow bootstrap and workflow contract in the pack. Keep guidance discovery conditional on repository declarations and follow local entrypoints when present. Remove any remaining claim that consumers must provide a particular inventory or `.agents` path merely to use an ambient workflow. Audit plan/spec destinations and discovery in `writing-plans`, `writing-roadmaps`, `brainstorming`, `linear-issue-shaping`, `selecting-a-subagent`, `requesting-code-review`, and `iterative-review`; respect repository-declared homes, using `.agents/plans/` or `.agents/specs/` only when the repository adopts that convention or has no conflicting declared practice.

- [ ] **Step 2: Keep Repo Worker Pack general-purpose and subscription-independent**

Review every Repo Worker Pack skill that mentions local doctrine, marketplace plugins, installed skills, runbooks/playbooks, or runner commands. State that repository guidance is a relevant overlay only when declared by that repository. Replace the fixed `.agents/runbooks/` and `.agents/playbooks/` prescription in `repo-worker-base/references/stage-guide-contract.md` with discovery of the consumer's declared stage-guide homes. Keep refresh commands in consumer canonical runners on the pinned marketplace-source path from Plan 2. Make worktree setup refresh consumer skills only when that repository declares marketplace-skill configuration; a repository with no such composition must remain lean. Recast the plugin metadata and README as a general ambient worker-capability pack, not a pack for one workspace. Ensure ambient worker capabilities do not require the consumer to subscribe to the pack, copy the pack, or install its projection, and do not claim ownership of Superpowers+ routing or Agent Operating Model standards. Remove stale index-mesh invocation from refresh skill metadata.

- [ ] **Step 3: Make MCP usage conditional on the actual tool surface**

For each MCP wrapper, preserve its owning server/tool guidance while requiring runtime discovery of the actual available connector surface. Keep explicit safe handling when the requested tool is unavailable. Remove instructions that imply a consumer must configure a connector or subscribe to MCP Usage Pack for the agent to use an already available MCP tool. In `using-github-mcp`, discover repository-declared PR policy at its own path; do not hard-code `.agents/runbooks/pr.md` as universal.

- [ ] **Step 4: Separate Unslop+ availability from profile adoption**

Audit profile discovery, evaluation, and deployment instructions. Make clear that an ambient agent can use the quality guidance when suitable, while consumer enforcement or repository-owned profile deployment is an explicit local choice. Keep profile validation scoped to profiles the consumer deliberately owns or deploys.

- [ ] **Step 5: Remove ambient command dependence on consumer skill projections**

Search all canonical source members of the four companion packs for commands or helper logic that resolve bundled scripts/references through `.agents/skills/<skill>/`. Update ambient agent instructions to resolve bundled files relative to the active skill's runtime-provided `SKILL.md` path. For consumer canonical runners, retain only the explicitly pinned marketplace-source invocation where the runner contract requires it. Update `using-git-worktrees/scripts/new_worktree.py` so an unconfigured consumer does not attempt marketplace-skill refresh, while a consumer that declared marketplace skills retains its refresh behavior. Do not rewrite paths owned by an explicitly adopted Agent Operating Model checker or repository policy. Remove stale `generating-agent-mesh` and index-mesh commands from all four packs.

- [ ] **Step 6: Add behavior evidence for each changed assumption**

Add or extend skill tests/pressure cases at the owning skills. Cover a consumer with custom plan/runbook homes, no ambient plugin subscriptions, and only a subset of MCP tools; a consumer-owned exact skill remains selectable; an optional Unslop profile is absent; an agent runs an ambient helper with no consumer `.agents/skills/` projection; and worktree creation skips skill refresh for a repository that declared no marketplace-skill configuration but preserves refresh for configured consumers. Assert the intended workflow decision and failure/reporting behavior, not text presence alone.

- [ ] **Step 7: Run focused source-skill suites**

Run tests only for skills changed in Steps 1-5 using their documented commands and the repository's active Python runtime. Record the test commands and results in the plan as execution proceeds.

**Task exit:** Companion packs remain distinct and usable as ambient guidance without imposing consumer subscriptions or assumed repository layouts; changed behavior has focused evidence at the source skill.

## Task 3: Define and implement capability-based runbook/playbook requirements

**Files:** `skills/repo-composition/SKILL.md`; `skills/repo-shape/SKILL.md`, `references/repository-runbook-standard.md`, `references/repository-shape-manifest.json`, relevant templates and scaffolds under `skills/repo-shape/`; repository-owned examples under `.agents/runbooks/` and `.agents/playbooks/`; their existing tests and any behavior fixtures.

**Consumes:** Task 1 audit and Task 2 role boundaries.

- [ ] **Step 1: Add failing contract behavior cases**

In `skills/repo-shape/tests/`, cover a valid capability requirement with no exact provider name, a separately declared exact repository-owned skill that resolves through `repo.local_skills`, an invalid ambient skill declaration used as if it were repository-owned, and a required capability with no provider that causes the workflow to stop and report the unmet requirement. Include a consumer with a custom layout so the portable contract does not infer `.agents/runbooks/` or `.agents/playbooks/` from ambient guidance.

- [ ] **Step 2: Specify the portable Markdown syntax and semantics**

Update `repository-runbook-standard.md` and the owning `repo-composition` skill. Define how a runbook/playbook states a required or optional capability, how a repository-owned exact skill is distinguished, how agents inspect and choose from the skills currently available, and the required stop/report behavior. Preserve current runbook/playbook composition graph rules and locally chosen paths.

- [ ] **Step 3: Update starter templates and scaffold behavior**

Change applicable templates and scaffold generators so newly created runbooks/playbooks use capability-oriented requirements. Do not place exact Superpowers+, Repo Worker Pack, MCP Usage Pack, or Unslop+ skill names in required ambient slots. Keep exact names only for local skills when the template clearly identifies them as repository-owned declarations.

Migrate this repository's runbooks and playbooks that currently require exact ambient skill names. Keep exact references only where the workflow has evidence that the named skill is genuinely repository-owned under its declared local-skill custody.

- [ ] **Step 4: Update structural validation for the new contract**

Teach the relevant repository-owned validator to check syntax, required/optional designation, exact local-skill custody, and graph integrity. Keep the legacy manifest path behavior intact unless Task 2 implementation evidence shows a deliberate compatibility adjustment is required. Do not use Marketplace plugin subscription membership as evidence that a capability is provided or that a standard is adopted.

- [ ] **Step 5: Prove missing required capability stops dependent work**

Add a behavior/pressure case in the source skill suite showing that absence of a required provider yields a clear stop before the dependent workflow action, with the capability named in the report. Verify optional capability absence is reported as skipped and does not block unrelated workflow steps. Do not represent hosted structural validation as proof of runtime skill availability.

- [ ] **Step 6: Run focused composition and validator suites**

Run the relevant `repo-composition` and `repo-shape` tests, including graph, scaffold, legacy compatibility, and hosted-hook fixtures affected by the changed contract. Fix failures at the canonical source boundary.

**Task exit:** The canonical contract and all newly scaffolded artifacts are capability-based; a required missing capability has an observable stop; exact names remain supported only for genuine repository-owned skills.

## Task 4: Regenerate, review, and publish Plan 3

**Files:** generated `dist/` marketplace products, generated `.agents/skills/`, `docs/ambient-plugin-assumption-audit.md`, decision record, and this plan plus `roadmap.md`.

**Consumes:** Tasks 1-3.

- [ ] **Step 1: Regenerate marketplace and installed skill outputs**

Run `py -3 tools/run.py marketplace --apply` and `py -3 tools/run.py installed-skills --apply`. Do not hand-edit generated output.

- [ ] **Step 2: Check generated products and source ownership**

Run `py -3 tools/run.py marketplace --check` and `py -3 tools/run.py installed-skills --check`. Inspect the generated manifests and built plugin trees to confirm expected membership, no unintended plugin subscription or mesh output, and packaging of changed source/test material.

- [ ] **Step 3: Run focused behavior suites and full source inventory review**

Run all affected skill suites and focused repository/build/shipping tests implicated by modified files. Review all five source manifests against the audit, and inspect the complete diff for accidental consumer-specific policy or generated-source edits.

- [ ] **Step 4: Update roadmap and mark plan complete**

Record the actual commit, PR, local hook evidence, and any hosted-check limitation in the roadmap. Mark this plan `completed-awaiting-retirement` and complete all agent-owned checklist steps before handoff. Do not leave human-owned PR readiness or merge actions as unchecked plan steps.

- [ ] **Step 5: Commit through the canonical hook, push, and verify PR**

Stage the intended files and commit normally. The tracked pre-commit hook runs the canonical apply/check gate; do not run the full CI check immediately before or after a successful hooked commit. Push the existing roadmap branch and verify PR #338 head, draft state, mergeability, and hosted-check status. Keep the PR Draft while later roadmap work remains.

**Task exit:** The PR includes the source audit, capability-based workflow contract, focused behavior evidence, and regenerated product output, all published at a verified PR head.

## Review focus

- The audit enumerates all five plugins by current manifest membership and every material consumer assumption with source path, effect, and disposition.
- Superpowers+ remains workflow composition; Repo Worker Pack remains general agent capability; MCP Usage Pack remains conditional tool-use guidance; Unslop+ remains optional writing/profile capability; Agent Operating Model remains optional deployable standards.
- Runbook/playbook syntax requests capabilities and marks required versus optional. Exact skill names remain supported for genuine repository-owned skills only.
- Runtime discovery failure for a required capability stops the dependent workflow and reports what is missing. No unrelated skill is silently substituted.
- Hosted validators validate authored consumer contracts without claiming ambient plugin availability.
- No consumer repo, index mesh artifact, or generated source surface is changed outside its owner.

## Handoff

- **Selected lane:** Native `executing-plans` in the existing roadmap worktree/PR. The pack and contract edits are coupled through shared runtime-resolution semantics; focused skill tests give task-local review evidence without requiring independent branches.
- **Base and publication:** Continue on the existing `codex/ambient-operating-model-design` branch and Draft PR #338. Before any later successor branch, follow the completing-planning-artifacts ingress rule against refreshed `main`; this plan does not authorize deleting completion-marked plans from a base where they have not yet landed.
- **Repository guidance:** Follow `AGENTS.md`, `.agents/runbooks/implementing.md`, `.agents/playbooks/marketplace-generation.md`, `.agents/playbooks/testing.md`, and the portable `repo-composition`/`repo-shape` contracts.
- **Consumer boundary:** Rooms and other consumer migrations remain out of scope. The marketplace migration guide is the supported handoff for those agents.
