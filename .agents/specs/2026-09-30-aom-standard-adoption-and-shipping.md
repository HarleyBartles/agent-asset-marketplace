# AOM Standard Adoption and Shipping

> Status: Approved by the human on 2026-09-30; implementation is authorized. Design date: 2026-09-30. Investigated source baseline: `3b39cc051f1fb4241c9ee36a1fca411190f9b1a8`.

## 1. Purpose and scope

Agent Operating Model (AOM) publishes selectable standards for how agents work in repositories. A repository chooses the standards it needs, implements their requirements, and maintains its own certification. AOM supplies definitions, adoption capabilities, and optional starter implementations.

The existing distribution boundary mixes standard definitions, consumer implementation, recurring validators, and one-time scaffolders in `.agents/standards/`. Some checks enforce starter inventories, headings, or unchanged deployed bytes rather than the operating promise. This design replaces that boundary with repository-owned implementation and explicit self-certification against immutable requirements.

This specification defines the shipping model and the outcome each retained standard protects. It covers the original twelve-entry catalog, consolidation and retirement decisions, and two additional standards identified during the audit. It is a design contract for later planning, not a task sequence or authorization to migrate consumers.

The design does not require a marketplace source submodule, copied scaffolders, automatic consumer upgrades, a universal deployment resolver, mandatory starter inventories, or one runtime implementation language. It does not redefine product schemas as agent contracts.

## 2. Ownership and authority

| Surface                 | Owner and responsibility                                                                                             |
| ----------------------- | -------------------------------------------------------------------------------------------------------------------- |
| Standard definition     | AOM owns the requirements, their rationale, and what establishes conformance.                                        |
| Standard skill          | AOM owns the capability to understand, adopt, assess, and explicitly upgrade the standard.                           |
| Deployment machinery    | AOM owns scripts that provision selected assets. One-time scaffolders stay with AOM.                                 |
| Optional starter assets | AOM offers templates, checkers, target implementations, examples, and supporting tests. The repo chooses what helps. |
| Adopted implementation  | The repo owns deployed or independently authored documents, configuration, tools, and targets.                       |
| Compliance chain        | The repo owns its mechanical checks, semantic review, workflow measures, and certification.                          |
| Historical requirements | The source repository and pinned Git commit preserve the definition the repo adopted.                                |

A starter becomes repository-owned when adopted. Its origin does not make it generated output or require byte equality with AOM. The repo may adapt, replace, or omit a starter while satisfying the standard. A particular standard may require the repo to provide a checker or interface, but never requires the AOM starter solely because it was supplied.

Recurring tools can legitimately remain in a consumer. Classify an asset by what it does throughout its lifecycle, rather than by its filename. Generated output is legitimate where the repo owns a generation contract; this is separate from treating adopted starters as permanently vendor-owned.

Portable Python work ships one Python implementation. Shell and PowerShell are appropriate for genuine platform-specific requirements or thin launchers that delegate portable logic. Avoid maintaining equivalent implementations in three languages.

## 3. Plugin packaging

Each selectable standard is represented by a skill in the AOM plugin. The skill bundles its current definition, adoption and assessment guidance, and any deployment scripts, assets, templates, or optional checkers it supplies. A standard can have no deployable starter assets.

The skill is a capability; the definition is the authority governing a subscription. Improving an ambient skill does not change an existing repo pledge. Skill descriptions make the capability discoverable. Full definitions, scripts, and starter assets are loaded when relevant rather than all being injected into context.

A small coordinating entrypoint may help select several standards and explain their interactions. It must preserve each standard's ownership and independent adoption. Concrete filenames and internal skill organization are implementation choices; the roles and boundaries above are required.

Current plugins need not carry historical definitions. A subscription identifies the adopted standard by:

- Stable standard ID.
- Source repository.
- Immutable Git commit.
- Definition path at that commit.
- Reference to the repo's readable certification.

Those commits must remain retrievable. A repo may retain a reference snapshot for offline access without taking a source submodule or deployment machinery. A branch selector is insufficient as the authority of an adopted standard because its meaning can change.

## 4. Subscription and certification

### 4.1 Records

Use one small machine-readable subscription contract, defaulting to `.agents/contracts/operating-standards.json`. It records the immutable identity and certification reference described above. Selected templates and deployment history are separate from that pledge. No shared deployment-history format is required for compliance.

Readable certification defaults to `.agents/contracts/standards-certification.md`. Start with one document; split when useful. Each standard's certification explains:

- Where its implementation lives.
- What relevant agents must preserve.
- Which checks, review practices, and workflow measures prevent drift.
- Which evidence is mechanical and which assessment requires judgment.

Using `.agents/contracts/` for these records does not subscribe the repo to the broader agent doctrine/contracts standard. Each standard can specify its required artifacts without forcing adoption of the category standard.

Certification is an ongoing account of responsibility and safeguards. A permanent `compliant: true` flag, expiry date, or dated passing check cannot replace it. Passing a checker does not excuse violating a semantic requirement.

### 4.2 Adoption

An adoption task reads the selected definition and its applicable conditional obligations, assesses existing implementation, fills actual gaps, establishes discovery and drift-prevention measures, then records subscription and certification against what exists.

Copying templates alone does not establish adoption. An already conforming repo may need only records and missing routes. AOM deployment support provisions selected assets where useful; the adopting agent reconciles them with repo-owned implementation.

Every AOM adoption requires root `AGENTS.md`. Create a minimal entrypoint if missing or integrate necessary discovery into the existing file. It routes agents to subscriptions and applicable certifications with clear read conditions. This shared requirement does not implicitly subscribe the repo to the full AGENTS routing standard.

Certification means satisfying every applicable requirement of the pinned definition. There is no general exception mechanism or partial-compliance subscription. Unfinished adoption remains pending work and gaps are reported honestly. Repeated evidence that a requirement is inappropriate should inform a revised standard rather than an overstated certification.

Every agent changing an affected surface must preserve its certification. Routing should make those responsibilities available at the relevant work point without requiring every certification on every turn.

Detected drift is a compliance failure against the existing pinned requirements, not an invitation to change the subscription to make the check pass. Report the affected obligations and repair the implementation or correct the certification's claim. A retained subscription reference does not prove the repo is currently compliant.

### 4.3 Upgrades and failure handling

Refreshing the ambient AOM plugin changes available capabilities and assets. It does not alter a repo subscription, create a latest-version failure, produce recurring age alarms, or initiate upgrade work.

An explicitly requested adoption update compares the pinned requirements with the requested revision, adapts the repo-owned implementation, and updates subscription and certification. It must not overwrite modified starters as generated vendor output.

An unavailable pinned definition cannot be replaced silently by the latest one. Report the missing authority and do not claim assessment against requirements that were not retrieved. Failed adoption or upgrade work must not be recorded as completed certification. Preserve the existing authority until the revised implementation and certification are established.

## 5. Discovery and composition

### 5.1 Runtime presentation and effective routing

Applicability text explains scope. It corroborates that an agent reached the intended guidance or helps reject guidance outside the task. Writing a prominent applicability instruction on a document does not cause an agent to find it.

The relevant runtime may present:

| Surface                    | Presentation mechanism and limit                                                                                                  |
| -------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| Project instruction files  | Harness-specific scope injection; Codex and Devin have different discovery timing and supported names.                            |
| Skills                     | Metadata supports selection before full instructions are loaded; selection is not guaranteed.                                     |
| Tools, including MCP tools | Definitions are exposed or searchable through the host; server configuration alone does not prove every tool is in model context. |
| Harness-native rules       | Configured always-on, glob, model-decided, or manual activation, where supported.                                                 |
| Review instruction files   | Particular review products load named files for review; this is not general coding-session discovery.                             |

Unless the relevant harness and task demonstrably present an artifact, provide an effective inbound route from something the agent encounters. Doctrine, contracts, certifications, books, profiles, and supporting skill resources normally require those routes. Filesystem presence and inbound links from otherwise unreachable documents are insufficient.

Availability is separate from intentional workflow use. Even a presented tool can go unused without a skill or router explaining when and how to use it. A runtime tool inventory alone does not satisfy a workflow obligation to use that capability.

Progressive discovery keeps brief orientation available and loads detail when relevant. Avoid all-documents-on-every-turn guidance.

### 5.2 Conditional expressions

Every definition distinguishes standalone obligations, conditional obligations triggered by another adopted standard or existing facility, and optional integrations. Express them in clear prose; a dependency language or automatic resolver is not required.

A conditional obligation does not subscribe the repo to another standard. Existing CI triggers AGENTS checker integration even without hook/CI adoption. Optional bus targets can be integrated where a conforming bus exists without requiring AOM's bus starter.

## 6. Selectable standards

Final standard IDs for consolidated and additional entries may be chosen during implementation. The boundaries and pledges below are authoritative design decisions.

### 6.1 Plugin installation

The repo declares plugin Git dependencies under `.agents/plugins/` and binds them through native harness configuration. `.agents/skills/` is reserved for repository-authored skills. No separate `repo.local_skills` inventory is required, and plugin payloads are not copied into that local skill store.

Codex and Devin are the investigated harnesses. Codex uses the repo marketplace catalog plus project activation and marketplace configuration. Devin uses its native repo dependency declarations. Their bindings express the same intended dependencies while retaining each client's installation semantics.

Git dependencies identify repository source, plugin path where needed, and a selector. A floating `ref`, including `main`, is valid and intentionally enables native refresh of published capability updates. An immutable `sha` is also valid. Native marketplace Upgrade or harness CLI refresh provides update levers; AOM does not invent an installer or require a marketplace submodule.

Repo declarations and native bindings enable setup from a fresh clone without relying on one person's ambient plugins. Authentication, trust, and host availability remain real prerequisites; a declaration is not proof installation succeeded. Documentation and assessment must distinguish valid configuration from actual availability. Plugin refresh remains separate from upgrading a pinned standard subscription.

AOM ships the definition and native configuration guidance, with optional starters and configuration checks. Consolidate `marketplace-skill-management` and `repo-plugin-subscriptions` into this one standard.

### 6.2 AGENTS routing

All `AGENTS.md` files in an adopting repo are lightweight, safe context-injection routers. They provide brief orientation and conditional pointers to authoritative guidance rather than carrying doctrine.

Rich root and domain routers support progressive discovery. Thin scoped routers identify the directory-tree scope and relevant read condition, ideally in one sentence. Applicability boundaries must be clear. The root is especially sensitive because some harnesses repeatedly inject it across repository work.

Protect against both per-file sprawl and unnecessary folder-boundary proliferation. Scale by delegating from a compact root to rich routers at natural domain boundaries, rather than growing the root indefinitely or placing a router in every folder.

The repo chooses and documents its appropriate locations, footprint, and size budgets and provides a checker. Numeric limits are not universal. AOM offers an optional checker with the investigated 55-line warning and 100-line error as starter alarms, not proof of semantic compliance. If CI exists, it runs the repo-owned checker. If hook/CI is also adopted, parity carries that check into pre-commit.

### 6.3 Runbook composition

A runbook guides a lifecycle stage of work that occurs in the repo. It explains when that stage applies, how work proceeds, and what stage completion means. It can provide guidance directly or compose relevant capabilities and other operating documents.

Adopters maintain useful stage documents with effective inbound routing and usable references. They self-certify document category and usefulness as well as mechanical integrity. There is no fixed heading list or obligation to invent empty capability, doctrine, contract, or routing sections.

No minimum inventory or particular book is required. Adoption normally arises because there is useful stage guidance to create or organize; allowing an empty inventory limits AOM demands rather than promoting empty adoption. Certification must not imply workflow coverage the repo has not implemented.

AOM offers five optional stage starters: design, planning, implementation, code review, and PR. Repos can select any individually, take the bundle, mix them with their own, or use none. A starter checker and supporting tests are optional. Adoption does not require playbooks or another document store.

### 6.4 Playbook composition

A playbook guides a kind of work or concern that can arise across lifecycle stages. Its trigger is the concern becoming relevant. It provides enough guidance to perform that work directly or within a stage, with effective inbound routing and usable references.

Playbooks compose capabilities, doctrine, contracts, commands, paths, evidence expectations, and related playbooks where relevant. Skills express capabilities rather than being a separate mandatory ingredient. Capability references distinguish:

- Repo-authored skills by name and linked repository source.
- Repo-installed plugin skills by plugin-qualified name, backed by repo dependency declarations.
- Ambient capabilities by capability description, resolved from the agent's environment without pretending a personal IDE plugin is present in every clone.

No fixed inventory or empty headings are required. Optional starter playbooks and checkers become repo-owned when selected. The same no-minimum-inventory rule applies as for runbooks.

Playbooks stand alone without runbook or doctrine/contracts adoption. Where authoritative operating knowledge exists, reference it and explain application. Otherwise a playbook may own that knowledge inline; the repo can establish a store if useful without being forced to invent one.

When both book standards are selected, review stages for relevant concerns and route runbooks to applicable playbooks with clear conditions. Shared topical guidance retains a clear owner. No all-to-all routing or mandatory reciprocal links. Stage guides must not become topical procedure collections, and concern guides must not become lifecycle stage guides.

### 6.5 Agent doctrine and contracts

Agent doctrine describes what must remain true. Agent contracts govern the obligations through which agents make it true. This category concerns agent behavior and repository work, not product schemas or APIs merely because they are called contracts.

Adopters place doctrine in `.agents/doctrine/` and contracts in `.agents/contracts/`. Locations are mandatory; a fixed document inventory is not.

Doctrine must have clear agent-facing force and scope, understandable obligations, and an explicit applicability hierarchy where requirements would otherwise conflict. Ambiguous weak wording must not obscure binding requirements. Guidance must be effectively reachable where an agent needs it.

Contracts may be prose Markdown, JSON, YAML, schemas, executable declarations, or settings. They make applicability, obligations, assessment, and authority understandable directly or through schemas, consuming tools, and references. No mandatory headings or universal wrapper is required. Applicability corroborates scope; inbound routing supplies discovery.

Contracts supplied by another standard retain that standard's schema and meaning; the repo owns its recorded values and commitments. This standard organizes agent governance rather than imposing one schema on all contracts.

Classify mixed documents by governing purpose and allow supporting explanation. Split when distinct obligations need separate ownership or discovery, not merely because a procedural paragraph appears.

The repo supplies a checker for placement, structured validity, broken references, and unreachable documents. Semantic review assesses clarity, applicability, conflicts, and useful discovery. Mechanical reachability checks must disclose their limits, including routes provided by harnesses or non-Markdown references. If CI exists, it runs the checker. An AOM starter is optional.

### 6.6 Hook and CI

The repo maintains a pre-commit hook and hosted CI that execute one complete gate. Agents must not skip the hook. Windows pre-commit and Linux hosted CI have equivalent check coverage and failure criteria, including tests, integration tests, linting, generation validation, and every other required gate check.

Required infrastructure and prerequisites are available in both environments. Missing prerequisites fail explicitly. No reduced platform gate or deferral of local failures to hosted execution. The hook catches failures before paid hosted execution; hosted CI verifies the committed result before merge.

The local gate assesses the candidate that will be committed, rather than relying on unstaged repairs that are absent from it. Hosted CI assesses the committed counterpart. Any hook-side normalization or generation must be included in that candidate and followed by validation. Preserve unrelated unstaged work; the mechanism for materializing and restoring the candidate is repo-owned.

The standard owns cross-platform normalization, including declared line-ending and final-newline conventions, Git attributes/configuration, and consistent generated and formatted text output without platform-driven churn. Genuine platform differences can use adapters while preserving shared gate logic.

The repo owns its hook and canonical validation path. If command bus is adopted, the bus owns its interface. AOM can offer a hook starter, normalization starter, and optional conforming bus target implementation. An adopting agent integrates them; no fixed command JSON or source submodule is inherently required.

Remove the shared-checkout mutation-intent flag guard from the target standard. It is not an obligation of hook/CI or command bus.

### 6.7 Command bus

The repo implements a CLI under `tools/` with discoverable targets. The implementation language and target inventory are repo-owned. AOM offers an optional Python starter; `tools/run.py` is not a mandatory filename.

The interface provides top-level `--help` and target `<target> --help`, with meaningful supported execution modes:

- `--check` assesses the declared condition without correcting maintained repository files. Validation failure or needed changes return non-zero. Tests and builds may create disposable outputs.
- `--apply` performs documented changes. Success does not by itself establish that a corresponding check passed.
- Optional `--dry-run` previews mutation where a meaningful preview can be performed. Proposed changes are not themselves dry-run failure.

Check-only and apply-only targets are valid. Help explains purpose, supported modes, prerequisites, side effects, and target-specific arguments without running target work.

A selected target needs an explicit mode or help request. Without one, show usage and exit non-zero. Bare bus invocation may show top-level help. Reject unknown targets, conflicting modes, and unsupported modes before work starts; never silently succeed with no operation.

Forward target-specific arguments faithfully. Targets own their meaning and implementation. Preserve target output and exact exit status. Required step failures or skips cannot be reported as success.

An agent adopts a conforming target into the bus. No automatic installation or universal registration protocol is required. Dependency graphs, multiple-target requests, and diagnostic collection are optional repo capabilities.

### 6.8 Review entrypoint

The repo maintains code-review guidance at root `REVIEW.md`. It may carry the guide and invariants inline, route to books or other guidance, or combine both. No fixed headings, document fan-out, other standard adoption, or deeper REVIEW files are required. Scoped review files are a repo choice.

Review-specific runtime loading is documented in particular products. It does not imply all coding agents discover REVIEW during ordinary work or follow its links identically. The AGENTS router-only constraint does not apply to REVIEW.

AOM offers an optional starter. The repo owns guidance and certifies its relevance and effective discovery for its review workflow.

### 6.9 Contribution entrypoint

The repo maintains root `CONTRIBUTING.md` sufficient to direct a contributor through its applicable contribution process. It can provide guidance inline, route to existing documents, or do both. No prescribed headings, fan-out, runbooks, or playbooks are required.

Root placement is AOM's convention; GitHub also recognizes other locations. Some review products consume CONTRIBUTING as instruction context, but its purpose remains usable contribution guidance. AOM supplies an optional starter; the repo owns content and certification.

### 6.10 Completed artifact custody

Adopters require agents to follow next-slice retirement for plans, specs, roadmaps, checkpoints, and similar execution artifacts. Preserve them through the completing PR so canonical Git history retains the completing artifact, then retire them in the first commit of the next substantive slice. Completed artifacts cease to be current authority even while temporarily retained.

Before removal, promote enduring knowledge to its appropriate durable home. Do not retire still-live future work. Completion is semantic: checked plans and evidence that their governed work is done prompt classification even without an exact marker. A marker such as `completed-awaiting-retirement` can record state but cannot be the only discovery mechanism or prerequisite for recognizing completion. Assess the whole artifact scope and repo evidence.

Abandonment is explicit and preserves enduring knowledge before removal; inactivity, rejected scratch candidates, or deletion do not prove abandonment. Remove stale links and indexes when retiring artifacts. If no later substantive slice occurs, retained completed artifacts can remain without becoming current authority.

AOM provides the lifecycle definition and adoption guidance, with optional implementation support. The portable completion capability must recognize semantic completion and follow the repo's adopted policy. Ambient capability availability alone must not impose this subscription on other repos.

### 6.11 Unslop

Agent slop is repeated or recurring agent mistakes in repository work, including coding, tests, architecture, writing, and other relevant concerns. An unslop profile provides durable, actionable guards against encountered slop. Adopters pledge to maintain effective profiles and the feedback loop that keeps them useful.

`.agents/unslop/` is canonical. A small repo can use `.agents/unslop/repo.md` for guards and occurrence records. Larger inventories can split by slop class with observations alongside or linked. No file-per-pattern rule, separate observation database, automatic counters, or telemetry system is required.

Profiles make failure patterns, recognition cues, corrective behavior, applicability, and false-positive boundaries understandable. No eight-heading schema or reciprocal-link ceremony is required. Guards remain subordinate to doctrine and user intent and may explain recurring pitfalls without duplicating binding policy.

Durable occurrence recording is mandatory across agents and sessions. Record enough evidence to connect occurrences to patterns, distinguish recurrence from duplicate reports, and assess whether the guard was reached and effective. Missing routing, ineffective correction, and ignored useful guards must be distinguishable. Candidate observations can precede a warranted profile.

Create, revise, narrow, consolidate, or retire guards using encountered failures and evidence of effectiveness. Static speculative files and unread inventories do not satisfy adoption. Effective inbound routing is required. Runbooks and playbooks, where implemented, route profiles at relevant stages and concerns; repos without them use another effective route.

AOM ships a standalone guide explaining profiles, their purpose, routing, and especially their management lifecycle. Available ambient Unslop+ or another checked-out capability can assist authoring and maintenance; no particular plugin or skill invocation is mandatory. Optional templates, observation formats, and structural checkers support implementation but do not prove the feedback loop works.

## 7. Catalog and migration boundaries

| Existing catalog entry                        | Target disposition                                                                               |
| --------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| `marketplace-skill-management`                | Consolidate into plugin installation; retire submodule and local-skill declaration requirements. |
| `repo-plugin-subscriptions`                   | Consolidate into plugin installation with native Git dependency bindings.                        |
| `root-agent-router`                           | Retain as AGENTS routing with repo-owned policy and checker.                                     |
| `runbook-composition`                         | Retain; optional starter inventory and semantic stage requirements.                              |
| `playbook-composition`                        | Retain; concern-based composition and independent adoption.                                      |
| `tracked-validation-hook`                     | Retain as complete Windows/Linux hook/CI parity; remove shared-checkout flag obligation.         |
| `markdown-formatting`                         | Retire selectable standard; move useful authoring guidance to writing-pack.                      |
| `review-entrypoint`                           | Retain root guidance pledge with inline or routed content.                                       |
| `contribution-entrypoint`                     | Retain root contribution guidance pledge.                                                        |
| `root-gitignore-hygiene`                      | Retire obsolete SDD cleanup packaged as a standard.                                              |
| `completed-artifact-custody`                  | Retain mandatory two-slice lifecycle with semantic completion discovery.                         |
| `unslop`                                      | Retain active profile maintenance, routing, and durable occurrence evidence.                     |
| Command bus, absent from catalog              | Add independently selectable standard with the agreed CLI interface.                             |
| Agent doctrine/contracts, absent from catalog | Add independently selectable standard with mandatory stores and quality requirements.            |

The old `agent-operating-model.json` exception record is a legacy migration surface rather than a retained standard. Its broadly mandatory shape model retires. The current `operating-standards.json` is the subscription record to evolve; executable implementation commands and generated paths are not part of the new subscription identity.

`repo-standards-commands.json` currently binds the hook to commands. Retain or replace that mechanism according to the repo-owned hook implementation; it is not a universal required record. `markdown-formatting.json` and formatter/wheel machinery need an owner-by-owner retirement assessment so unrelated useful checks are not accidentally discarded.

Current deployed scaffolders and byte-provenance enforcement must be reconciled with consumer ownership. Consumer migration is an explicit adoption task, not an automatic consequence of shipping the new plugin. Retiring a catalog entry does not rewrite old Git-pinned subscriptions. Record migrations honestly and preserve active future plans during artifact cleanup.

The Markdown problem identified is inconsistent prose hard wrapping. Keep concise, optional authoring guidance in writing-pack: favor consistent paragraph widths when starting or substantially revising a document, follow a clear existing convention, and avoid reflowing unrelated text. Do not prescribe one paragraph per source line, a fixed width, a repo adoption standard, or a mandatory formatter system.

## 8. Acceptance criteria for later implementation

These criteria describe required observable outcomes, not tests executed during this design task.

- A repo can select a single standard without receiving unselected books, mandatory document inventories, source submodules, or copied one-time scaffolders.
- Every standard exposes requirements, conditional obligations, optional integrations, self-certification guidance, and any optional starters through its owning skill.
- Subscription authority remains immutable and retrievable after an ambient plugin refresh. No latest-version alarm or implicit upgrade occurs.
- A modified or independently authored implementation can certify against requirements without matching AOM starter bytes.
- Adoption establishes root AGENTS discovery, accurate subscription references, readable certification, and effective routes at relevant work points.
- Partial or failed adoption does not produce a certified compliance claim.
- Runbooks and playbooks stand independently, preserve stage/concern boundaries, and compose conditionally when both are adopted.
- Repo-local, repo-installed plugin, and ambient capability references have distinct availability claims.
- Doctrine/contracts assessment covers semantic quality and routing as well as the required placement and mechanical checks.
- Windows hook and Linux hosted CI run the complete equivalent gate with prerequisites, normalization, and no silent omissions.
- Hook validation proves the candidate committed tree and preserves unrelated work; hosted validation proves its committed counterpart.
- Conforming bus implementations honor explicit modes, help, argument forwarding, output, and exact failure propagation regardless of language.
- Semantic completion discovers unlabeled completed artifacts while preserving active future work and enduring knowledge.
- Successive agents can record recurring slop, discover existing observations and guards, and improve ineffective routing or correction.

## 9. Planning handoff

The architectural decisions in this specification are settled for review. Exact subscription serialization, certification reference syntax, package file layout, starter formats, native config integration, migration mechanics, and pinned-source retrieval are implementation choices within these requirements. If a choice would alter a pledge or ownership boundary, return it for a design decision rather than infer authorization.

Implementation planning must trace canonical `skills/`, `skills/repo-shape` catalog and deployment logic, `src/plugin-definitions/`, generated `dist/` projections, current consumer contracts, hook bindings, and the completion/profile capabilities affected by this design. Generated plugin outputs remain downstream of canonical source. This document does not authorize source changes, consumer migrations, publication, or an implementation plan before human review.

## Appendix: investigation evidence

### Repository findings

The investigated catalog has twelve entries and copies flat resource lists, including scaffolders, into consumer `.agents/standards/`. Marketplace's current bus enforces recorded deployment bytes; that behavior illustrates the ownership boundary to replace.

Marketplace, Portfolio, Wild Bunch, Rooms-Mostly, and Adventures of Patch have Python command runners with named targets and apply/check conventions but different registries and orchestration. No common module registration interface was established. Sheg's `sheg-4-gitflow-releases` worktree uses npm scripts instead. This diversity informed the CLI contract and agent-led integration decision.

Marketplace's AGENTS checker warns above 55 root lines and errors above 100. Commit `1500d1a4d` reduced accumulated inline guidance to pointers. Its one-sentence scoped routers demonstrate progressive discovery without establishing universal thresholds.

Sampled doctrine/contracts stores show broad adoption of the canonical locations but mixed document purposes, weak wording, and incomplete static inbound links. The static scan did not prove runtime unreachability. These findings informed quality and effective-routing obligations rather than a filename-only check.

Wild Bunch has Git-subdirectory plugin catalog entries tracking `main` and Codex native bindings. The current completion skill discovers exact markers and blocks retirement without them, illustrating the semantic discovery gap. The old gitignore standard only cleans obsolete in-repo SDD rules and scaffolding.

### Primary documentation

- [OpenAI plugin packaging and Git-backed marketplaces](https://developers.openai.com/plugins/build/plugins) documents repo marketplace catalogs, Git selectors, project activation, and native refresh.
- [Devin plugin documentation](https://docs.devin.ai/cli/extensibility/plugins/overview) documents Git sources, selectors, native repo requirements, installation, and portable package support.
- [Agent Plugins](https://agent-plugins.org/) defines a portable package format while leaving installation and distribution to clients.
- [Codex instruction discovery](https://learn.chatgpt.com/docs/agent-configuration/agents-md) and [Devin rules](https://docs.devin.ai/cli/extensibility/rules) document different scope-loading mechanisms.
- [OpenAI skills](https://developers.openai.com/plugins/concepts/skills) and [Devin skills](https://docs.devin.ai/cli/extensibility/skills/overview) document skill selection and invocation.
- [MCP tool specification](https://modelcontextprotocol.io/specification/2025-06-18/server/tools) documents tool discovery without mandating one host presentation mechanism.
- [Devin Review](https://docs.devin.ai/work-with-devin/devin-review) documents review-context instruction files. [Claude Code review](https://code.claude.com/docs/en/code-review) distinguishes managed review handling from its local command. These are product-specific discovery mechanisms.
- [GitHub contribution guidance](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/setting-guidelines-for-repository-contributors) establishes CONTRIBUTING's contributor-facing purpose and hosting-platform discovery.

These sources explain investigated runtime behavior; this specification's pledges remain the design authority for the proposed AOM changes.
