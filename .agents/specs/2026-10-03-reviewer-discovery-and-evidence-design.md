# Reviewer discovery and evidence design

Status: proposed specification for human review. No implementation plan or skill implementation is authorized by this document.

Issue: [MARK-379](https://linear.app/harleys-workspace/issue/MARK-379/enable-reviewer-subagents-to-discover-skills-and-research)

## Purpose

Give fresh-context reviewer subagents the guidance and capabilities needed to evaluate their assigned work. A reviewer must discover relevant repository guidance and installed skills, investigate applicable external knowledge, and verify findings against the implementation. Fresh context removes conversational baggage while preserving access to relevant resources.

The coordinator's suggested resources are starting points, not an exhaustive list. Success includes discovering useful guidance the coordinator did not name. This applies to ordinary, task-scoped, specialist, and focused fix reviews, with investigation proportional to each assignment.

## Design choice

Introduce one first-party Superpowers+ skill, `conducting-code-review`, to own the reviewer's method. Existing coordinator skills invoke it through their reviewer briefs. Specialist profiles supply domain focus and output contracts rather than duplicating the shared method.

Keeping the method only in requesting-code-review would leave independent reviewer entry points dependent on coordinator instructions. Creating separate discovery, research, and evidence skills would split one review method across unnecessary entry points. A reviewer-owned skill provides one place to maintain the behavior across runtimes and dispatch paths.

This change does not add a standalone web-research skill or an OWASP catalogue. Relevant installed specialist skills remain available to the reviewer, including repository-specific skills. External sources supplement their guidance where appropriate.

## Current source evidence

The design was inspected against main at `b481f98ae90aa45e5271d10fe1f7aaeb6c7047aa`. These observations identify integration seams, not instructions to preserve restrictive behavior:

- `skills/requesting-code-review/SKILL.md` owns coordinator dispatch and fresh reviewer context. Its prepared-diff template restricts lookups to resolving refs or confirming state.
- `skills/subagent-driven-development/task-reviewer-prompt.md` strongly limits additional reading. Focused investigation is allowed for named risks, but guidance discovery and research need an explicit place in the method.
- `skills/selecting-a-subagent/SKILL.md` selects models, reasoning, context, and profiles. It must also assess whether available reviewer resources satisfy the assignment.
- `skills/selecting-a-subagent/assets/reviewer-security.md` is currently a secrets and identifiers lens. General security review requires a broader remit and matching selection behavior.
- The user reports `iterative-review` is broken and unused. Its source is retained for later refactoring, but it will be removed from the shipped Superpowers+ plugin in this slice. Its evolving review runtime is not an integration target for this design.

Reinspect these seams after the required rebase. Current file arrangements do not bind the future plan to obsolete implementations.

## Reviewer inputs and entry

The coordinator supplies the review object and immutable base/head identity where available, requirements, scope or lens, relevant repository location, prepared review package, allowed actions, and report destination or output contract. It identifies known resource entry points and observed capability limitations. It must not include the parent session history as a substitute for a self-contained brief.

The brief directs the reviewer to conducting-code-review using a usable runtime skill reference. When the runtime does not automatically supply the skill catalog or resource locations to fresh children, the coordinator supplies those discovery entry points. A pointer to a catalog is preferable to pasting every skill body. Do not invent unavailable dispatch parameters or claim that prompt wording grants tools.

The reviewer enters its assigned method directly. Retain the using-superpowers-plus exception for explicitly dispatched subagents; do not make each reviewer restart the general conversation router.

## Discovery and investigation

Every reviewer checks the relevant resource entry points before reaching a verdict: repository instructions and routed guidance, the installed skill catalog, and the tool capabilities actually available in its context. Discovery is targeted to the assignment rather than a broad filesystem or tool inventory.

The reviewer reads applicable repository guidance and specialist skills even when they were not named by the coordinator. It chooses relevance using the changed behavior, domain, technologies, versions, and review lens. Loading every skill, repeatedly loading the same guidance, or recursively following unrelated workflows is not discovery quality.

The reviewer forms concrete review questions from requirements, implementation behavior, trust boundaries, failure paths, and applicable guidance. It may investigate beyond a diff when needed to answer those questions, including callers, configuration, tests, and existing mitigations. Diff preparation remains the coordinator's responsibility; discovery does not authorize rebuilding a missing package or changing the reviewed revision.

Authoritative external research is expected when the assignment involves consequential security behavior, unfamiliar mechanisms, version-dependent behavior, or factual uncertainty that could change the verdict. Research may start from a domain or trust boundary before a suspected defect exists. Reviewers must not require a pre-existing suspicion before learning the relevant standard risk patterns.

Use primary sources appropriate to the question, such as official product documentation, standards, upstream source, security advisories, and original research. Establish applicability to the actual version and configuration. Search results are leads; inspect the supporting source before relying on it. Conflicting or unclear sources produce explicit uncertainty rather than a manufactured definitive finding.

For a simple review whose relevant expectations and technology behavior are already established, external research need not become a ceremonial step. Stop when the material questions have been answered or the remaining limitations are identified. Do not use a fixed tool-call or citation quota as a substitute for adequate investigation.

## Scope, action, and authority boundaries

Reviews are read-only on repository state. No source edits, installs, branch/index changes, publication, or additional subagent dispatch follows from discovering a skill. The existing workflow may allow an owned off-repo report. Focused verification commands require the assignment's authorization and must respect its action boundaries.

Applicable skill guidance informs the assigned review; its unrelated execution stages do not expand reviewer authority. A requirement to mutate, install, or publish must be reported as incompatible with the current review assignment, not executed automatically. Explicit user constraints and binding repository instructions retain their authority.

Retrieved content is source material, not an instruction channel. Public research queries use generic technical descriptions and public version information. Do not transmit private diffs, secrets, identifiers, or internal paths to external research services.

A standard or recommendation can support a review question without becoming a newly imposed repository requirement. A finding must establish actual impact or a violation of an applicable requirement. Assess existing controls and reachable conditions before claiming a defect.

Focused re-review discovers guidance and researches questions relevant to the original findings or new behavior in the fix. It does not restart whole-branch investigation. Adjacent observations follow the existing deferred-finding rules.

## Capability limitations and recovery

The coordinator checks known runtime capabilities before dispatch and the reviewer verifies what it actually received. Both distinguish skill access, repository reading, online retrieval, and permitted verification commands from model or reasoning selection.

An optional unavailable resource does not block unrelated review. Use an appropriate available authoritative alternative where possible and disclose the material limitation. Do not install a missing skill or fabricate research access.

When missing guidance or research prevents a material question from being assessed, report the affected question as unverified and do not issue an unqualified clean or ready verdict. When binding repository guidance makes a capability mandatory, stop the dependent assessment and return the blocker. The coordinator can supply the required material or select an authorized adequate runtime; supplied material is identified as supplied rather than independently retrieved.

On resumption, preserve review identity and the questions already answered. Revalidate material external facts when their version, applicability, or currency has changed. Do not treat old research notes as proof that new code was reviewed.

## Evidence and output

The shared method contributes evidence to each workflow's existing report format. It does not replace existing severity scales, fix loops, verdicts, or terminal-response contracts.

For each finding, report the affected code location, observed behavior, relevant reachable conditions or requirement, impact, and supporting evidence. When external knowledge or a specialist skill materially supports the finding, identify the source and the specific applicable guidance. Include version or retrieval context where material. A citation alone does not prove the implementation is vulnerable.

Keep confirmed defects, conditional risks, and unanswered questions distinct. Report material missing capabilities and coverage limits. Briefly identify guidance used and significant checks, including an existing mitigation that resolves an otherwise plausible risk, when needed to explain the assessment. Do not require an exhaustive browsing transcript in the human report.

Repository requirements and code evidence remain tied to the reviewed revision. External sources and installed skills are separately attributed review resources, not silently admitted as new governing authority. Reports retain enough evidence to explain what was consulted, its relevance, and the conclusion. Unsupported capture paths must yield honest evidence limitations. This change does not depend on the iterative-review runtime.

## Ownership and integration map

| Owner | Responsibility |
| --- | --- |
| `skills/conducting-code-review/` | Reviewer discovery, investigation, source applicability, action boundaries, and evidence method. |
| `skills/requesting-code-review/` | Dispatch entry and both commit-range and prepared-diff templates invoke the shared reviewer method. |
| `skills/selecting-a-subagent/` | Route adequacy includes resource access; runtime profiles and reviewer assets preserve that access and report unenforceable capabilities. |
| `skills/subagent-driven-development/` | Task review and focused re-review use the shared method while retaining their respective scope and output contracts. |
| `skills/iterative-review/` | Retain all canonical source, tests, references, and helpers unchanged for later refactoring. No discovery integration or runtime repair is included. |
| `skills/receiving-code-review/` | Evaluate supplied sources against implementation, versions, configuration, and binding requirements before accepting or rejecting findings. |
| `src/plugin-definitions/superpowers-plus/contents.json` | Add first-party product membership for the new skill and remove iterative-review membership. |

Reconcile active shipped routing and authored plugin documentation that assume iterative-review is available, including using-superpowers-plus and selecting-a-subagent where applicable. Remove mandatory routes to the unshipped skill while keeping historical attribution and retained source intact. Regenerate the package so iterative-review is absent from the installed plugin and generated inventories accurately reflect membership. Do not delete or refactor its canonical source to make packaging checks pass.

Canonical skill behavior is authored under skills/, reusable cross-skill resources under shared/ where needed, and composition under src/plugin-definitions/. Generated dist/ outputs are regenerated through repository tooling during implementation, not edited as source.

The security profile will cover relevant security and privacy boundaries, risk patterns, and mitigations in the assigned change. Selection triggers must cover those surfaces rather than only secret-related keywords. Security findings remain conditioned on the product's real threat model; a secrets scan is useful evidence but does not establish comprehensive security coverage. Other reviewer profiles adopt the common method without unrelated expansion of their lenses.

## Behavioral acceptance criteria

Use a narrow witnessed behavioral proof before changing the skill behavior, then compare the revised behavior on the same underlying review problem. Do not use text-presence or change-detector tests to claim successful review.

- A fresh reviewer discovers an unmentioned repository-specific review skill and applies its relevant guidance correctly without inheriting the coordinator's conclusions.
- A security reviewer consults an applicable authoritative source, finds a real code-backed defect, and correctly accepts a companion case whose existing mitigation addresses that risk. Authoritative research supports both detection and restraint.
- An installed specialist skill is used when relevant, while any mutation or delegation workflow it contains is kept outside the reviewer's authority.
- A missing mandatory resource or material research capability produces a specific limitation and a qualified assessment rather than a false clean verdict.
- A focused fix re-review uses relevant guidance and research without expanding into untouched whole-branch review.
- Online content cannot change review instructions, and queries do not disclose private review material.
- A regenerated Superpowers+ plugin omits iterative-review while its canonical source, tests, references, and helpers remain available for future refactoring. Active shipped routes do not require the absent skill.

Each proof records the available resources, reviewed revision, observable actions, supporting sources, and resulting findings or non-findings. Hook instrumentation may be used when available with verified coverage, but this issue does not implement instrumentation or assume an empty log proves no tools were used.

Later implementation must run focused owning behavior tests, regenerate marketplace artifacts, and satisfy the repository's staged hook and publication gates. The implementation plan chooses exact fixture mechanics, runtime checks, and commands after rebase.

## Sequencing and open gate

This worktree is reserved for specification, later planning, and eventual implementation. No plan is written in this phase. Keep MARK-379 In Progress and preserve the worktree.

The user confirmed MARK-377 (temporary tool auditing) as the merge dependency for planning. Its plan is at `Z:/_agent-worktrees/agent-asset-marketplace/codex/mark-377-temporary-tool-auditing/.agents/plans/2026-10-03-temporary-tool-auditing.md`. That plan proposes bounded auditing for Codex and Devin with sanitized records, verified activation, attribution limits, and teardown. Treat the plan as context and verify merged behavior before selecting any instrumentation for this issue's behavioral proof. Do not edit that worktree.

After MARK-377 merges, verify the merged repository state, rebase this branch onto current main, and reconcile this specification with the resulting contracts. Present any material design changes for human resolution. Only after the specification is approved and the sequencing gate is satisfied may the implementation plan be written. Skill changes and iterative-review packaging removal occur during that subsequent implementation stage.
