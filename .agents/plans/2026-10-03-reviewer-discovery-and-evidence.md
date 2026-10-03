# Reviewer Discovery and Evidence Implementation Plan

**Artifact status:** publication-closeout-pending.

> **For agentic workers:** REQUIRED SUB-SKILL: Use `subagent-driven-development` (recommended) or `executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship one reviewer-owned discovery and evidence method across active Superpowers+ review entrypoints, and stop shipping iterative-review while preserving its source.

**Architecture:** conducting-code-review owns discovery, applicable skills, proportionate research, focused executable proofs, scope, capability recovery, and reporting. Coordinator templates and runtime profiles provide usable entrypoints into that method without duplicating it. Product composition excludes iterative-review; generated outputs follow canonical source.

**Tech Stack:** Markdown/YAML instructions, existing Python marketplace tooling and pytest suites, and fresh-context behavioral evaluations. No new production runtime dependency or general review engine.

**Spec:** [Settled design](../specs/2026-10-03-reviewer-discovery-and-evidence-design.md).

**Execution Strategy:** `executing-plans`. The shared method, coordinator prompts, specialist profiles, and behavioral proofs depend on the same review contract. Inline sequential implementation preserves that context; use a fresh whole-branch reviewer after the complete change. The nearest alternative is subagent-driven-development, which adds fresh implementer/reviewer contexts per task but repeatedly reconstructs the shared contract.

## Execution rulings and current evidence

Implementation is published in PR #347. PR #346 merged into main at `88c02ec6804fd695e43bf6a632c61014a21738f4`. This branch integrates that main commit at `bca71e9640d0050e5656ce126997071928e206f7`; overlapping temporary-tool-auditing files were resolved to the merged main versions. GitHub reported #347 MERGEABLE at final-diff review head `116573bbd053701146a40137e638530ad5c1d090`, and hosted marketplace-validation run 37143134133 passed for that exact head. Fresh whole-diff and security reviews found no implementation or package findings. The final whole-diff reviewer identified a Minor status contradiction in these closeout artifacts; correction and focused re-review remain before handoff. The pre-existing Important plan-only contradiction remains separate and outside this change.

MARK-379 did not install or activate audit instrumentation. The planned child-query capture was unavailable; the cited behavioral reports and parent reproductions do not independently witness each child's retrieval or every public query. These are explicit evidence limits and are not negative findings. No instrumentation, audit logs, or helper copies were created by MARK-379, so this slice has no teardown or purge obligation.

The fixture creates a base/change repository and a separate clone with a third fixed revision, resolving the two-commit/fixed-checkout interface conflict. Evaluator-only expectations stay outside shipped output. Run evidence remains off-repo.

The first fresh reviewer found both seeded defects and accepted the safe boundaries; RED is specifically its missing review-basis reporting. The fresh shared-workflow reviewer then reported applied local/installed guidance and unslop, applicable sources, focused proofs and limits. The parent independently reproduced unsafe/safe rendering and indistinguishable load results, and verified the original revision and only pre-existing cache state remained. Individual child tool calls remain unverified. The task-review baseline also found the defects and reported local guidance despite contradictory diff-only rules; reconcile that instruction conflict without claiming a witnessed discovery failure.

The AOM adoption roadmap, eleven plans and spec were classified complete against their full recorded obligations, durable owners and live merged PR #345, then retired in the first substantive implementation commit. Retain this slice, MARK-377 and uncertain/active predecessor artifacts.

Task 1 delivery: `b2b12dc9cd119e4622bc21dbc6a41935d1756536`, new shared skill/source/generated membership and reusable behavior cases. Fixture custody/revision tests: 3 passed. Complete tracked Windows hook: build 13 passed/1 skipped, repository 114 passed, shipping 10 passed, other checks passed. Narrow report-basis RED/GREEN is recorded off-repo. Baseline and GREEN used the same UTF-8 fixture-produced diff rather than the package helper; the fix case uses the owning helper. Git tracked content/index/revision checks establish custody; individual child tool/query execution remains outside independent coverage.

Task 2 evidence: current-template baseline found defects despite restrictive wording, so the change resolves a contract conflict without claiming a discovery failure. The updated fix template produced ADDRESSED with no new breakage, applied the remaining AGENTS route with REVIEW.md absent, and separated the unchanged loader issue without blocking the fix. The nominated unavailable documentation route failed both in the child report and a dispatcher web-tool verification; other official URLs were usable. The child continued with the best supported review and then attributed dispatcher-supplied research, which corroborated its findings without inventing a gap. This demonstrates failed-resource recovery, not a runtime with all internet access unavailable.

Task 2 delivery: `8b44b8c93f1e9605e5f53e6bc7a55698553a3867`, coordinator/task/fix integration and triage. The complete tracked Windows hook passed with the same build/repository/shipping counts as Task 1.

Task 3 evidence: all eight reviewer profile model fields were compared against Task 3 base `8b44b8c93f1e9605e5f53e6bc7a55698553a3867` and remain unchanged. A fresh Codex V2 gpt-6-sol medium security-lens child used the new method/resource entrypoints and returned the exact `reviewer-security: 2 issue(s)` terminal line after writing its report. Its report identifies applicable HTML-output and loader-failure risks, accepts the safe text-context companion and explicit optional-absence contract, and records supporting sources and focused proofs. The parent verified the original reviewed HEAD and tracked/index state. Devin execution is not exposed here: those assets were inspected for coherent action/report/stop contracts, not live-run or globally installed. Individual child lookup/query attribution remains unverified.

The strong profile's mandatory legacy engine metrics/ledger precondition was removed while aligning its resource contract: ordinary review cannot depend on the workflow being unshipped in Task 4. Prior reports/resolution evidence remain optional claims to verify, and missing prepared packages retain the blocked outcome. This changes active routing, not retained iterative-review source.

Task 3 delivery: `1badd247b0cc15a4bba6a2e411d0a3d064018d48`; the complete tracked Windows hook passed with the same build/repository/shipping counts as Task 1.

Task 4 source-retention baseline is Git tree `05e475f50278ff381c54619e646825fb9e1d62fa` for `47a2f03bec9ebe6bf7928cfdabc2a87b89030358:skills/iterative-review`. The active-route scan after canonical removal leaves only the authored retention note, historical immutable audit-probe attribution and an explicitly legacy scratch name. Retained skill internals and historical tests are unchanged. The assembly suite had no membership-retirement behavior test, so the added generic alpha/beta case verifies preview non-mutation, apply removing only the retired output, and unchanged canonical source/other package. The existing generator already supports it; no fabricated generator RED or production bug-fix claim is made. Assembly/isolated-plugin command: 5 passed, 1 Windows POSIX-bits skip.

Task 4 isolated-package evaluation initially failed for workspace credits, then completed after the human reported restored credits. A fresh gpt-6-sol medium child used the copied 043ab545 package entrypoints, discovered fixture guidance and installed specialist resources, identified both seeded defects, accepted the safe boundaries, assessed the instruction-like resource as data and reported its actual review basis. The parent read the report and verified the original source/index/HEAD and pre-existing cache state. Ordinary review did not require iterative-review. This is copied-package path evidence, not a global installation, filesystem sandbox or independent child-query trace claim. Task 4 is complete; its owning helper recorded completion after the existing assembly evidence, actual report and final link validation were inspected.

Task 4 source/package delivery: f66789823034c87ebc0fc13819298c485e1acf78. Complete tracked Windows hook: build 14 passed/1 skipped, repository 114 passed, shipping 10 passed, other checks passed. The earlier MARK-377 snapshot at 224ac579fa62e5622facc89f2fb4eb8226ac8273 was merged into this branch at 26dd06cc904acce81ff8f906746f8c47b48f7ec0 and is included in the #347 main-targeted diff. Main remains b481f98ae90aa45e5271d10fe1f7aaeb6c7047aa.

Self-inspection found two refinements: fix the review-basis link relative to its reference directory, and preserve actual severity for unrelated observations in the task/fix controller instead of automatically treating them as deferred Minor findings. These reconcile the approved scope contract. The later full main-targeted review found no implementation or package issue; its Minor finding concerns stale completion-status prose later in this record.

Merged dependency and canonical fixture checks: py -3 -m pytest skills/temporary-tool-auditing/tests skills/conducting-code-review/tests/scripts -q reported 211 passed, 2 skipped. The fixture payloads were reformatted at whitespace and logical newline boundaries, with parsed values unchanged; its three behavior tests passed again after that source-only readability refinement.

Initial publication ruling: Publish an explicitly incomplete Draft for inspection. The user then directed #347 to follow #346. After #346 merged, this branch integrated its mainline commit and reviewers assessed the resulting MARK-379 main-targeted diff. Do not reintroduce the superseded audit snapshot or claim that it remains part of the current PR diff.

Independent whole-branch review at 043ab545 found two Important conflicts: the task template still discouraged checking unchanged context, and the selector treated common prepared-diff inputs as lens triggers. Both are accepted within this slice. The focused selection baseline selected seven profiles for a CSS padding edit; corrected fresh behavior selected no specialist for it, and scripts/security for the CLI-derived shell-command case. Both baseline and corrected task reviewers reproduced an unchanged caller's broken CLI behavior, so the targeted-context correction resolves conflicting instructions without claiming a witnessed baseline miss. Reusable pressure prompts live with the selecting-a-subagent and subagent-driven-development owners; run evidence stays off-repo. Fresh gpt-6-luna medium fix re-review at 0bed64de marked both findings ADDRESSED, checked their generated counterparts and found no new Critical/Important breakage. The pre-existing plan-only profile observation remains separately recorded with its actual severity.

Review rulings: independent child lookup/public-query capture and live Devin execution remain explicit coverage limits. Isolated copied-package evaluation is resolved. The temporary-tool-auditing implementation is now present in main and outside the current #347 diff. Fresh whole-diff and security reviews found no implementation or package findings. The final whole-diff review at `116573bbd053701146a40137e638530ad5c1d090` found stale status prose and an unchecked closeout item in this plan/spec; a focused review of their correction is the remaining gate. The reviewer separately confirmed the pre-existing Important plan-only/missing-diff contradiction in `reviewer-plans`; preserve its severity and owner for follow-up without requiring this change to repair that mode or expand the fix loop. Retained iterative-review internals remain out of scope and byte-identical.
Source implementation review is complete at 0bed64de1b7b5f1d2b5822862707602c20d367f4: fresh whole-branch review at 043ab545 plus fresh scoped verification of its correction range. Complete tracked Windows hook at 0bed64de passed build 14/1 skipped, repository 114, shipping 10 and remaining checks. Hosted marketplace-validation run 37127824353 succeeded for that exact published head; GitHub reports MERGEABLE/CLEAN. The final evidence-only plan/spec update changes no shipped source or generated output.

Checklist disposition: Tasks 2-4 and the conducting-code-review authoring, fixture, and report-basis behavior are delivered. The planned hook-capture exercise was not performed because this slice could not establish a positively verified installation, activation, and attribution path. That exercise is optional under the approved specification, so its absence is an explicit evidence limit rather than an unreported acceptance failure. The full main-targeted diff passed review at `116573bbd053701146a40137e638530ad5c1d090`; hosted validation passed, and Ready preflight found zero issues across 82 changed files. One Minor contradiction in the completion-status prose and checklist was reported on that revision and is being corrected. Keep the artifacts open until a fresh focused review verifies the correction and the final Linear/Ready closeout is recorded.
## Global Constraints

- Implement MARK-379 only, in `Z:/_agent-worktrees/agent-asset-marketplace/codex/mark-379-reviewer-discovery` on `codex/mark-379-reviewer-discovery`.
- PR #346 has merged to main at `88c02ec6804fd695e43bf6a632c61014a21738f4`; PR #347 follows it. Review the actual current main-targeted #347 diff after pushing the merge integration.
- Protect reviewed source, index, HEAD, and branch state. Allow legitimate focused tests, reproductions, disposable scratch artifacts, and report writes. Installation, expensive validation, and live-service checks go to the dispatcher.
- Fresh reviewers receive a self-contained brief and usable guidance/capability entrypoints, never the parent's conversation history. Discover relevant resources beyond those the dispatcher names.
- REVIEW.md is an optional repository-owned entrypoint. Discover applicable code-style guidance and unslop profiles; apply evidence and false-positive boundaries rather than personal preference or token bans.
- Expect primary-source research for consequential security behavior, unfamiliar mechanisms, version-dependent behavior, or material uncertainty. Do not impose a universal browsing quota. Do not send private source, secrets, or internal identifiers in public queries.
- Missing access yields the best available review plus explicit gaps. The dispatcher may supply sourced research or re-dispatch with actual access. Supplied research remains attributed and subject to independent code assessment.
- Report unrelated pre-existing issues separately without demanding scope expansion. Issues introduced, worsened, made reachable, or explicitly required to be fixed by this change may affect approval.
- Every substantive report, including a clean report, has a concise review basis. Preserve workflow-specific severity, verdict, and terminal-response contracts.
- Retain `skills/iterative-review/` source, tests, references, and helpers unchanged. Remove its Superpowers+ membership and active shipped dependencies. Do not repair its runtime.
- Canonical edits belong in skills/, shared/ if needed, and src/plugin-definitions/. Never hand-edit generated dist/ files. Keep UTF-8 without BOM, LF, and one physical line per Markdown prose paragraph/list item.
- Use behavior evidence for instruction changes. No phrase-presence, change-detector, or tautological tests. Do not broaden or rerun suites after a passing gate without a new reason.
- Complete source work, a fresh review of the exact final main-targeted diff, plan/spec closeout, and exact-head hosted proof before applying the repository Ready preflight. Do not merge without separate human instruction.

## Sequencing evidence

At initial publication, #347 targeted main `b481f98ae90aa45e5271d10fe1f7aaeb6c7047aa` and included the earlier audit snapshot. The human then merged #346 at `88c02ec6804fd695e43bf6a632c61014a21738f4`. This branch integrates that commit at `bca71e9640d0050e5656ce126997071928e206f7`, resolving overlap in favor of the merged main files. The current main-targeted diff excludes changes already present on main. At `116573bbd053701146a40137e638530ad5c1d090`, GitHub reported MERGEABLE and hosted validation passed; Ready preflight found zero issues across 82 changed files.

## File responsibilities

| Files | Responsibility |
| --- | --- |
| `skills/conducting-code-review/SKILL.md`, `agents/openai.yaml` | Direct reviewer entry, reusable method, scope, output and capability recovery. First-party compositional workflow skill, not a security/style expert catalogue. |
| `skills/conducting-code-review/references/review-basis.md` | Concise report structure and evidence classification; no duplicate severity system. |
| `skills/conducting-code-review/tests/behavior/README.md`, `tests/pressure/prompts/{discovery,limited-access,fix-review}.md`, `tests/pressure/fixtures/review_case.py` | Three focused reusable behavioral cases and an off-repo fixture materializer. |
| `skills/conducting-code-review/tests/evaluator-only/expectations.md` | Blinded evaluator requirements; never supplied to workers or shipped. |
| `skills/requesting-code-review/{SKILL.md,code-reviewer.md,reviewer-prompt.md}` | Coordinator handoff for commit-range and prepared-diff review. |
| `skills/subagent-driven-development/{SKILL.md,task-reviewer-prompt.md,re-review-prompt.md,implementer-prompt.md}` | Task and fix review integration, consistent action boundaries, replacement of the final iterative-review route. |
| `skills/selecting-a-subagent/SKILL.md`, `references/shared-policy.md`, runtime profile references, `assets/reviewer*.md` | Actual capability adequacy, usable shared-skill pointers, consistent lens boundaries and reports. |
| `skills/receiving-code-review/SKILL.md` | Source applicability and version/configuration/code verification during triage. |
| `skills/using-superpowers-plus/SKILL.md`, `skills/subagent-workspace/SKILL.md`, `src/plugin-definitions/superpowers-plus/{contents.json,files/references/codex-marketplace-compatibility.md}` | Active packaging/routing consistency, new membership, and removal of iterative-review membership. |
| `tests/build/test_plugin_assembly.py`, existing shipping suites | Actual assembly and isolated-install behavior, extended only for a genuine uncovered behavior. |

Runtime profile references in scope are `codex-multi-agent-v1-profile.md`, `codex-multi-agent-v2-profile.md`, `devin-desktop-profile.md`, and `generic-free-first-profile.md`. Reviewer assets in scope are reviewer, reviewer-strong, reviewer-fast, reviewer-fixes, reviewer-security, reviewer-skills, reviewer-plans, and reviewer-scripts. Do not change their model choices as part of this work.

## Review Focus

- A fresh child lacks the parent's skill catalog: Task 2 supplies usable discovery entrypoints, and Task 3 checks a real child can resolve them without a consumer `.agents/skills/` projection.
- A supplied source supports a general risk but the actual implementation already mitigates it: Tasks 1 and 3 require code applicability and a safe companion rather than a source-backed false positive.
- A profile still says no tools, read the diff only, or stop after two unproductive calls: Task 3 reconciles those restrictions so necessary discovery and focused proofs can happen without unbounded investigation.
- A fix reviewer notices an unrelated existing issue: Task 2's fix case reports it separately and does not reopen whole-branch approval.
- Hook data is missing or purge is incomplete: record evidence limitations and never infer witnessed behavior from an empty log. MARK-379 created no active instrumentation or owned helper files.

## Task 1: Prove and implement the shared reviewer method

**Files:** Create conducting-code-review files listed above; add its composition entry to `src/plugin-definitions/superpowers-plus/contents.json` in the deliverable commit. Use the scaffold's metadata conventions and existing first-party provenance.

**Interfaces:** `review_case.py` exports `materialize(root: Path) -> dict[str, Path]`; it refuses an existing populated root, creates a disposable two-commit fixture, and returns repo, brief, full_diff, fix_diff, report_dir, and skill_catalog paths. It has no production runtime role. CLI `--check` previews and `--apply --root <absolute scratch path>` materializes the fixture. The worker sees only ordinary review inputs and resource entrypoints, never evaluator-only expectations.

- [x] Use `/writing-skills` first-party authoring and behavior RED/GREEN guidance with `.agents/playbooks/skill-authoring.md`. Keep run evidence off-repo, prepare the fixture and evaluator before authoring, and scaffold the canonical skill only after observing baseline behavior.
- [x] Materialize the integrated fixture where REVIEW.md routes to a repo-owned skill and unslop profile, unsafe rendering contrasts with an escaped companion, a changed failure path swallows an error, an unrelated issue is visible, and an installed specialist resource contains an out-of-scope mutation instruction. Include passing tests that cannot substitute for review behavior.

```python
# Fixture code, not production code.
from html import escape

def render_label_unsafe(label):
    return f"<p>{label}</p>"

def render_label_safe(label):
    return f"<p>{escape(label)}</p>"

def label_or_empty(load):
    try:
        return load()
    except Exception:
        return ""
```

- [x] Build the unslop profile around swallowed load failures, with an explicit empty-state contract as its false-positive boundary and a companion satisfying that boundary. Treat instruction-like resource text as review data, never assignment authority.
- [x] Prepare fresh-context baseline and GREEN behavior cases without naming hidden resources or expected defects. Baseline and GREEN used fixture-produced UTF-8 diffs; the later fix case used the owning package helper. Preserve reviewed revision, index, and source.
- [x] Assess instrumentation capability before scenario dispatch. No positively verified live hook attribution route was available to MARK-379, so no hooks were installed or activated. Record public-query and child-tool capture as explicit evidence limits; do not infer a no-tool claim from empty logs.
- [x] Scaffold and author conducting-code-review after the baseline, package reusable behavior fixtures, and keep evaluator expectations out of generated output. The implementation covers discovery, style/unslop, research, focused proofs, scope, recovery, and evidence reporting without a new domain catalogue.
- [x] Run discovery and fix cases in fresh contexts. Reports and parent reproductions establish the observed cases; individual child lookup/query traces are not independently captured. Private-query non-disclosure remains an explicit capture limitation.
- [x] Verify no instrumentation, audit logs, or owned helper copies were created by this slice, so it has no teardown or purge work. Regenerate, validate, and commit the shared skill through the tracked hook.

**Exit:** The first-party skill is packaged, the narrow core behavior has witnessed RED/GREEN, and unobserved tool/query capture is reported as an evidence limitation. No live instrumentation lifecycle is claimed.

## Task 2: Integrate coordinator and task-review prompts

**Files:** Modify requesting-code-review and subagent-driven-development files listed in the file map; modify receiving-code-review/SKILL.md. Extend `tests/pressure/prompts/limited-access.md` and `fix-review.md` under conducting-code-review.

**Interfaces:** Dispatch briefs add usable conducting-code-review and resource-catalog entrypoints, reviewed revision/package, scope/lens, proof/scratch boundaries, known capability limits, and report destination. The review basis stays inside each existing report structure. Commit-range, prepared-diff, task, and fix reviewers consume the same method; fix reviews retain per-finding verdicts and out-of-scope observations.

- [x] Run one current task-review dispatch on the fixture to establish whether its diff-only rules exclude required REVIEW.md/skill/profile discovery. Capture the specific behavior, not a regex verdict. Update both requesting-code-review templates and both task/fix reviewer templates to invoke conducting-code-review directly and permit targeted repository reading, source lookup, and focused proofs. Replace contradictory strict read-only and diff-context-is-everything wording; preserve coordinator-owned package generation, missing-package failure, no child delegation, and focused validation discipline.
- [x] Update receiving-code-review so supporting sources are inspected for applicability, supported version, configuration, and code evidence. Sources are not automatic defects; pre-existing observations do not silently expand the change. Keep the dispatcher-research fallback explicit and attribute supplied material.
- [x] Exercise `limited-access.md` using a child runtime that actually lacks network access or returns a controlled unavailable result. Do not describe a textual no-browse request in a capable runtime as missing tool access. The reviewer must give its best review and identify unanswered material questions. The dispatcher then retrieves the official source and supplies supporting detail to the same reviewer where supported, or a self-contained fresh reviewer. Verify it distinguishes supplied research from independent retrieval and does not falsely flag the safe companion. If the harness cannot enforce missing access, report that limitation and use observed access failure; do not invent a capability test result.
- [x] Exercise `fix-review.md`: fixture fix diff replaces unsafe interpolation with html.escape; the brief lists the original encoding finding. Verify the fix assessment, permitted focused proof, concise review basis, and separate existing-issue observation without whole-branch scope expansion. REVIEW.md absence is exercised in this case by removing that optional fixture entrypoint before committing its review revision; the remaining AGENTS.md route is sufficient.
- [x] Regenerate the plugin and commit the coherent template/triage integration through the tracked hook as `feat: connect review dispatch to reviewer discovery`.

**Exit:** All four reviewer entry types preserve the method and scope; missing-access and fix cases demonstrate the approved recovery and scope boundaries.

## Task 3: Align runtime routes and specialist profiles

**Files:** Modify selecting-a-subagent/SKILL.md, shared-policy.md, the four runtime references, and all eight reviewer assets named above. The shared skill and existing behavioral fixtures own the method and proof, avoiding cloned domain guidance.

**Interfaces:** Route adequacy records actual skill/catalog access, repository reading, online retrieval, focused execution, and material limitations separately from model/reasoning/context. Profile injection carries a resolvable skill entrypoint, not an assumed path relative to a globally installed Devin profile. Security-lens triggers cover applicable boundaries as well as credential exposure.

- [x] Inspect each profile's output contract and action/stop restrictions. Resolve differences locally without changing model selection or forcing a new runtime abstraction. A capability cannot be enabled by merely listing it in a prompt; unavailable schema controls are reported as unenforceable.
- [x] Inject the new shared method through usable runtime-provided paths or discovery entrypoints; supply a catalog when fresh children do not automatically receive one. Remove lookups-only and strict no-write restrictions that prohibit relevant research or scratch proofs. Replace call-count/last-two-calls shortcuts where they can terminate material investigation prematurely with stopping on answered questions or explicitly recorded limits.
- [x] Broaden reviewer-security's remit and Applies-to triggers to include authn/authz, untrusted input/output, process/filesystem boundaries, serialization, dependencies, and privacy exposure where the diff makes them relevant. Assess the real product threat model, reachable conditions, and existing mitigations. Keep credentials/PII checks, but do not treat placeholder-looking identifiers, private IPs, or examples as automatic vulnerabilities. Preserve specialist scopes and terse terminal responses across all profiles.
- [x] Use the integrated discovery case to run one actual fresh child with a reviewer-security brief through the live Codex route. Verify usable skill access and authoritative-source applicability. For Devin assets, use its demonstrated runtime when exposed; otherwise inspect/profile-test applicable contracts and report live execution as unverified. Do not invent a Devin session, install global profiles during this plan, or claim cross-runtime live proof from a Codex run.
- [x] Regenerate and stage the intended tree; commit through the tracked hook as `feat: preserve reviewer resources across runtime profiles`.

**Exit:** All shipped reviewer profiles permit legitimate discovery and proof; live capability claims are accurate; security assessment uses the broader scope without source-backed false positives.

## Task 4: Stop shipping iterative-review and reconcile active routes

**Files:** Modify superpowers-plus contents.json and authored compatibility reference, using-superpowers-plus/SKILL.md, selecting-a-subagent/SKILL.md, requesting/receiving-code-review related metadata, subagent-driven-development/implementer-prompt.md, and subagent-workspace/SKILL.md where active text assumes shipped availability. Do not edit `skills/iterative-review/`.

**Interfaces:** Canonical iterative-review remains byte-identical to the integrated base; built Superpowers+ no longer exports that skill. Active review dispatch uses requesting-code-review plus conducting-code-review; historical attribution and legacy scratch naming are not instructions to invoke an unshipped skill.

- [x] Record a source-tree byte digest for skills/iterative-review from the integrated implementation base. Identify shipped active routes with `rg -n iterative-review skills shared src/plugin-definitions --glob '*.md' --glob '*.json'`, classify each hit, and change only routes or current product claims that require availability. Preserve historical records and retained skill internals. Do not rename old scratch directories merely to erase every mention.
- [x] Remove iterative-review's composition entry. Update the compatibility reference to include the compositional conducting-code-review wrapper and omit iterative-review from the active list. Keep the new skill justified as a workflow composition over existing review entrypoints, not a relocated expert skill.
- [x] Regenerate via `py -3 tools/run.py marketplace --apply`. Confirm the actual built plugin omits iterative-review, includes conducting-code-review and its ship-ready tests, excludes evaluator-only expectations, and the retained source digest is unchanged. Inspect its bundle manifest and generated catalog as outputs; do not hand-edit them.
- [x] Use `py -3 -m pytest tests/build/test_plugin_assembly.py tests/shipping/test_isolated_plugin.py -q` for assembly/closure behavior. Add a builder behavior test only if no existing test covers retiring an included skill while retaining canonical source: start from `_source(tmp_path)`, build alpha/beta, remove shared-skill from alpha's contents only, rebuild, and assert alpha's old output is removed while beta's included copy and canonical source remain byte-identical. This exercises assembly behavior, not a hardcoded product-name change detector.
- [x] Perform an isolated installed-plugin review with the retained iterative-review source unavailable to that child. Verify active dispatch reaches conducting-code-review and requesting-code-review without requiring the removed skill. Commit through the tracked hook as `build: unship iterative review while retaining source`.

**Exit:** Installable output and active routes are coherent, retained source is unchanged, and a source checkout is not required for ordinary installed review.

## Task 5: Validate combined delivery, review, and publish

**Files:** Update this plan and its spec for completing-slice status; update only necessary durable method owners if implementation reveals accepted enduring decisions not already carried by the shipped skill.

**Interfaces:** Final evidence names the main base, final reviewed commit, behavioral outcomes, sources/coverage limits, generated closure, and GitHub PR/check state. Report artifacts are scratch; the plan/spec remain tracked through their completing PR.

- [x] Review spec coverage against Tasks 1-4 and the behavioral case results. Ensure each agreed behavior has observed evidence or an explicit unresolved limit. Run any changed fixture helper tests against their canonical owner; do not add fake instruction tests or re-run already-green suites without a new reason. Run `py -3 tools/build_marketplace.py --check` when needed to verify uncommitted generation state; normal commits use the full staged hook as the owner gate.
- [x] Fetch main and inspect current #346 and #347 GitHub states. Integrate #346's merged main commit and verify GitHub mergeability and hosted validation at the published head.
- [x] Prepare the full current main-targeted diff and obtain fresh independent whole-diff and security reviews with discovered repository/installed guidance and authoritative sources where relevant. Both reviews found no change-induced issues. Preserve the separate pre-existing Important plan-only contradiction without expanding this issue.
- [ ] Correct the closeout status prose and checklist to match completed reviews, hosted validation and Ready preflight. Complete a fresh focused review of that correction before setting both artifacts to `completed-awaiting-retirement`.
- [x] Refresh the PR body with the current head, review state and hosted evidence. Preflight found zero issues; GitHub reports MERGEABLE/CLEAN and marketplace-validation passed for the exact head `116573bbd053701146a40137e638530ad5c1d090`.
- [ ] Update MARK-379 after the focused correction review and apply the Ready preflight to the final tree. Retain the worktree while the PR is under review.

**Exit:** A fully reviewable PR to main with a fresh independent review of the actual final main-targeted diff, generated parity, exact-head validation evidence, and an accurate follow-on integration record for #346. This plan does not require #346 to merge first and does not authorize merging #347.

## Research references for the reusable fixture

The fixture uses HTML text output, not arbitrary JavaScript/URL/attribute contexts. Use the Python html.escape documentation to verify its escaping contract and OWASP's HTML-context encoding guidance to judge the unsafe/safe pair. These links are evaluator leads rather than answers pasted into the worker's initial brief; the reviewer discovers and assesses relevant sources itself.

- [Python html utilities](https://docs.python.org/3/library/html.html#html.escape)
- [OWASP XSS prevention guidance](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)

The executing agent chooses the exact observed model/reasoning route with selecting-a-subagent and records it as runtime evidence. Do not persist a handoff readiness score in this plan or claim that planned behavioral evaluations have already run.
