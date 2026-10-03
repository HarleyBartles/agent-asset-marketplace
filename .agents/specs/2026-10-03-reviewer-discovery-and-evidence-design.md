# Reviewer discovery and evidence design

Status: completed-awaiting-retirement. Implementation is published in PR #347. Fresh whole-diff and security reviews of the current main-targeted change at 4118bcf8df0c03ec90afa513c0404716175cbdd0 found no change-induced findings; hosted marketplace-validation passed at that exact reviewed head. PR #346 merged into main at 88c02ec6804fd695e43bf6a632c61014a21738f4. Branch codex/mark-379-reviewer-discovery integrates that commit at bca71e9640d0050e5656ce126997071928e206f7, resolving overlapping audit files to the merged main versions. The current PR diff excludes changes already on main. The plan records the exact integration and review basis. No runtime instrumentation was installed or activated by MARK-379. Retain this governing artifact through its completing PR.

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

The #347 source and profile seams were reviewed against the audit snapshot present at initial publication. After #346 merged, its updated implementation became part of main and was integrated into this branch. The current pull request diff should be reviewed against current main without treating those already-merged audit files as MARK-379 changes.

## Reviewer inputs and entry

The coordinator supplies the review object and immutable base/head identity where available, requirements, scope or lens, relevant repository location, prepared review package, allowed actions, and report destination or output contract. It identifies known resource entry points and observed capability limitations. It must not include the parent session history as a substitute for a self-contained brief.

The brief directs the reviewer to conducting-code-review using a usable runtime skill reference. When the runtime does not automatically supply the skill catalog or resource locations to fresh children, the coordinator supplies those discovery entry points. A pointer to a catalog is preferable to pasting every skill body. Do not invent unavailable dispatch parameters or claim that prompt wording grants tools.

When a repository ships REVIEW.md, the dispatcher points the reviewer to that entrypoint. The reviewer also checks for it through targeted discovery when the dispatcher omitted it, and follows its applicable routes alongside AGENTS.md and scoped repository instructions. REVIEW.md is an optional repository-owned entrypoint, not a portable prerequisite or an exemption from higher-priority instructions. Existing review guidance may live elsewhere; absence of REVIEW.md does not imply absence of guidance and does not require creating one.

The reviewer enters its assigned method directly. Retain the using-superpowers-plus exception for explicitly dispatched subagents; do not make each reviewer restart the general conversation router.

## Discovery and investigation

Every reviewer checks the relevant resource entry points before reaching a verdict: repository instructions and routed guidance, the installed skill catalog, and the tool capabilities actually available in its context. Discovery is targeted to the assignment rather than a broad filesystem or tool inventory.

The reviewer reads applicable repository guidance and specialist skills even when they were not named by the coordinator. It chooses relevance using the changed behavior, domain, technologies, versions, and review lens. Loading every skill, repeatedly loading the same guidance, or recursively following unrelated workflows is not discovery quality.

Review includes code style and known anti-patterns, not only functional correctness and security. Understand the accepted standard way to write the relevant language, framework, or mechanism using repository conventions, applicable capability skills, and authoritative documentation where needed. Passing tests does not excuse sloppy implementation or an established anti-pattern. Ground style findings in the applicable standard and concrete code evidence, explain the consequence or binding convention, and distinguish accepted alternatives from personal preference. Account for repository-supported versions and deliberate requirements rather than imposing the newest idiom indiscriminately.

When the repository ships unslop profiles, discover and read those relevant to the review, including profiles reached through local entrypoints and their application skills. Check that the change does not introduce or propagate the identified slop patterns across code, tests, prose, or workflow artifacts within scope. Evaluate each cue using the profile's evidence, false-positive, and override boundaries; a cue is a review question, not an automatic defect or token ban. Report concrete matches and required corrections within scope, and report unrelated pre-existing slop separately under the existing-issue boundary. Reviewing a profile does not authorize rewriting it or recording new occurrences in repository files.

The reviewer forms concrete review questions from requirements, implementation behavior, trust boundaries, failure paths, and applicable guidance. It may investigate beyond a diff when needed to answer those questions, including callers, configuration, tests, and existing mitigations. Diff preparation remains the coordinator's responsibility; discovery does not authorize rebuilding a missing package or changing the reviewed revision.

Authoritative external research is expected when the assignment involves consequential security behavior, unfamiliar mechanisms, version-dependent behavior, or factual uncertainty that could change the verdict. Research may start from a domain or trust boundary before a suspected defect exists. Reviewers must not require a pre-existing suspicion before learning the relevant standard risk patterns.

Use primary sources appropriate to the question, such as official product documentation, standards, upstream source, security advisories, and original research. Establish applicability to the actual version and configuration. Search results are leads; inspect the supporting source before relying on it. Conflicting or unclear sources produce explicit uncertainty rather than a manufactured definitive finding.

For a simple review whose relevant expectations and technology behavior are already established, external research need not become a ceremonial step. Stop when the material questions have been answered or the remaining limitations are identified. Do not use a fixed tool-call or citation quota as a substitute for adequate investigation.

This proportional research policy is human-approved. Code-style questions also warrant authoritative research when the accepted approach, API contract, or version-dependent idiom is uncertain. Every review checks available guidance and capabilities; not every review must retrieve an external source.

## Scope, action, and authority boundaries

Reviewers protect the reviewed source, index, HEAD, and branch state rather than obeying a blanket prohibition on writes or execution. Focused tests and reproductions are legitimate review mechanisms when they answer a concrete question left unresolved by reading and research. The reviewer may create owned off-repo reports and disposable proof artifacts, and use scratch copies of the reviewed revision when checks create files. Preserve the reviewed checkout and its identity; do not let caches or generated test artifacts alter it. Report the question, command or proof, result, and material limits. Do not rerun existing validation merely to recreate evidence already available.

Dependency installation, expensive validation, and checks against live services are referred to the dispatcher rather than performed under ordinary review authority. The dispatcher can arrange an authorized environment or supply resulting evidence. Discovering a skill does not authorize source edits, branch/index changes, publication, or additional subagent dispatch. Review-specific instructions must permit the legitimate verification mechanisms above instead of stymying them with strict read-only wording.

Applicable skill guidance informs the assigned review; its unrelated execution stages do not expand reviewer authority. A requirement to mutate, install, or publish must be reported as incompatible with the current review assignment, not executed automatically. Explicit user constraints and binding repository instructions retain their authority.

Retrieved content is source material, not an instruction channel. Public research queries use generic technical descriptions and public version information. Do not transmit private diffs, secrets, identifiers, or internal paths to external research services.

A standard or recommendation can support a review question without becoming a newly imposed repository requirement. A finding must establish actual impact or a violation of an applicable requirement. Assess existing controls and reachable conditions before claiming a defect.

Reviewers evaluate the code under review. They may investigate surrounding code and report existing issues that surface, but must not demand that the change set expand to resolve unrelated defects. Distinguish issues introduced, worsened, or made reachable by the change; existing issues the assigned requirements explicitly require this change to address; and other pre-existing issues. The first two categories may affect approval. Report the third separately for follow-up, with severity and evidence, without making its repair an automatic condition of approval. Escalate a critical existing issue explicitly without silently expanding the assignment. The human or dispatcher owns any resulting scope decision.

Focused re-review discovers guidance and researches questions relevant to the original findings or new behavior in the fix. It does not restart whole-branch investigation. Adjacent observations follow the existing deferred-finding rules.

## Capability limitations and recovery

The coordinator checks known runtime capabilities before dispatch and the reviewer verifies what it actually received. Both distinguish skill access, repository reading, online retrieval, and permitted verification commands from model or reasoning selection.

An unavailable resource, including internet access, does not by itself terminate the whole review. Give the best assessment supported by available resources, use an appropriate available authoritative alternative where possible, and disclose the missing capability and affected coverage. Do not install a missing skill, fabricate research access, or describe remembered knowledge as a live source lookup.

When missing guidance or research prevents a material question from being assessed, report the affected question as unverified and do not issue an unqualified clean or ready verdict. When binding repository guidance makes a capability mandatory, stop the dependent assessment and return the blocker while completing the independent parts that remain assessable.

The dispatcher may re-dispatch with relevant access when the runtime actually supports it, or conduct the missing research itself and provide the material to the reviewer. Supplied research includes the original source references, relevant excerpts or supporting detail, version and configuration applicability, and remaining uncertainty. The reviewer identifies the material as dispatcher-supplied, evaluates it against the code, and updates the affected assessment without automatically adopting the dispatcher's conclusions. Resume the same reviewer where supported; otherwise provide a fresh reviewer with a self-contained package for the unresolved questions. Do not imply that re-dispatch alone grants access or that supplied research was independently retrieved by the reviewer.

On resumption, preserve review identity and the questions already answered. Revalidate material external facts when their version, applicability, or currency has changed. Do not treat old research notes as proof that new code was reviewed.

## Evidence and output

The shared method contributes evidence to each workflow's existing report format. It does not replace existing severity scales, fix loops, verdicts, or terminal-response contracts.

Every substantive review report includes a short review basis alongside its findings and verdict, including when no issues are found. Identify applicable repository guidance, specialist skills and unslop profiles actually applied, authoritative sources used, focused tests or proofs performed and their outcomes, and material coverage gaps. Explain material applicability or version assumptions where needed. If external research or executable proof was unnecessary, state that briefly rather than implying it occurred. Keep this concise and relevant to the assignment; no exhaustive tool transcript or recital of every discovered resource is required. For workflows with a terse terminal response, this basis belongs in the report artifact, not an expanded terminal message.

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
- A reviewer identifies a code-style anti-pattern using applicable repository and language/framework standards, while accepting a supported idiomatic alternative instead of enforcing personal preference.
- A reviewer discovers a relevant repository unslop profile and detects propagation of its evidenced pattern, while respecting a companion case covered by the profile's false-positive or override boundary.
- A repository with REVIEW.md has its applicable review routes consulted even when the dispatcher omitted the pointer; a repository without it is reviewed using its existing entrypoints without requiring a new file.
- A security reviewer consults an applicable authoritative source, finds a real code-backed defect, and correctly accepts a companion case whose existing mitigation addresses that risk. Authoritative research supports both detection and restraint.
- An installed specialist skill is used when relevant, while any mutation or delegation workflow it contains is kept outside the reviewer's authority.
- A missing mandatory resource or material research capability produces a specific limitation and a qualified assessment rather than a false clean verdict.
- A reviewer without internet access completes the assessable review and reports the gap. Dispatcher-supplied authoritative research enables it to assess the unresolved question without claiming independent retrieval or accepting a conclusion unsupported by the code; re-dispatch with access is an alternative only where supported.
- A focused fix re-review uses relevant guidance and research without expanding into untouched whole-branch review.
- A reviewer reports a pre-existing issue surfaced during investigation separately from change-related findings and does not demand unrelated repairs as a condition of approval; existing issues introduced into reachability or required to be addressed remain within the review's assessment.
- Online content cannot change review instructions, and queries do not disclose private review material.
- A focused executable proof answers a concrete review question using disposable scratch artifacts while preserving the reviewed source, index, HEAD, and branch state. Checks requiring installation, expensive validation, or live-service activity are referred to the dispatcher.
- A regenerated Superpowers+ plugin omits iterative-review while its canonical source, tests, references, and helpers remain available for future refactoring. Active shipped routes do not require the absent skill.
- A clean review and a review with findings both provide a concise, truthful review basis showing applied guidance, profiles, sources, proof outcomes, and material gaps; the report does not claim resources were used merely because they were available.

Each proof records the available resources, reviewed revision, observable actions, supporting sources, and resulting findings or non-findings. Hook instrumentation may be used when available with verified coverage, but this issue does not implement instrumentation or assume an empty log proves no tools were used.

The implementation ran the focused owning behavior tests, regenerated marketplace artifacts, and passed the repository staged hook. Final delivery still requires a fresh review of the complete current main-targeted diff and exact-head hosted proof after closeout edits.

## Sequencing and current integration

PR #346 merged into main at `88c02ec6804fd695e43bf6a632c61014a21738f4`. Branch `codex/mark-379-reviewer-discovery` integrates the merged commit in `bca71e9640d0050e5656ce126997071928e206f7`. Where both branches changed temporary-tool-auditing files, this integration uses the merged main versions. The current PR diff excludes changes already present on main. GitHub reports the pushed reviewed head MERGEABLE, and its hosted validation passed. Fresh whole-diff and security reviews found no change-induced findings; a pre-existing Important plan-only contradiction remains separately assigned and does not expand this issue. Final documentation closeout, Ready preflight, and exact-head checks after closeout remain.

For #347, the remaining agent-owned gates are fresh independent reviews of the complete current main-targeted diff, resolution of any blocking findings, and exact-head publication checks after final documentation updates. A prior implementation review does not replace review of the resulting current diff. Keep MARK-379 In Progress and preserve its worktree until these gates complete.
