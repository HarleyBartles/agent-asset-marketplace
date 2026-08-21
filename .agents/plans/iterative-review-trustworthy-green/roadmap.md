# Trustworthy Iterative Review - Epic Roadmap

Source spec: [Trustworthy Iterative Review Design](../../specs/2026-08-21-trustworthy-iterative-review-design.md)

| # | Title | Status | Plan File | Commit | PR | Rating | Notes |
|---|---|---|---|---|---|---|---|
| 1 | Fail-closed evidence kernel and legacy false-green regression suite | ready | [Plan 1](2026-08-21-plan-1-evidence-kernel.md) | - | - | 9/10 | Establish the sole machine state, atomic evidence registry, green predicate, transition policy, and regression tests for every proven version-1 router defect. |
| 2 | Immutable snapshot epochs and authority manifest | pending | - | - | - | - | Bind full base/head/tree identifiers, diff and metadata hashes, repo law, linked issue documents, and drift invalidation to each review epoch. |
| 3 | Impact inventory, coverage planner, and safe reviewer packages | pending | - | - | - | - | Replace heuristic lens selection with changed/affected-surface obligations, derive scope-plus-risk capability floors, require risk-based overlap, and build context packages that cannot hide dependencies. |
| 4 | Structured reviewer execution and attestation validation | pending | - | - | - | - | Dispatch intentionally tiered fast, focused, strong, and orchestrator-equivalent roles; validate the live route, identity, context, completeness, and positive evidence for every assignment. |
| 5 | Finding adjudication, fix impact, and re-review lifecycle | pending | - | - | - | - | Track all severities, independently adjudicate findings, enforce fixed/false-positive proof, publish fixes, and re-ascend every invalidated review tier before final review. |
| 6 | Orchestrator-equivalent blind final, closure audit, exact-SHA seal, and presentation recheck | pending | - | - | - | - | Require fresh-context final and closure roles on the orchestrator's own route, move closeout before final freeze, bind hosted checks to the reviewed head, and re-fetch remote state before handoff. |
| 7 | Frontier-reference benchmark, escape measurement, simplification, migration, and rollout | pending | - | - | - | - | Gate weaker routes against a frontier-stable corpus, measure downstream frontier escapes, cut over to one `reviewctl` path, remove bookkeeping nodes and legacy authorities, and publish consumer-safe guidance. |

## Epic invariants

- No plan may weaken the green predicate in the source spec.
- Each plan uses test-driven development and lands as a reviewable draft pull request before the next plan is written.
- Version-1 state, reports, and metrics may inform migration diagnostics but may not satisfy a version-2 green gate.
- A known `accepted-risk` finding may produce `reviewed-with-exceptions` but never green.
- A stored seal is only a candidate proof; human-facing green requires a fresh remote head, authority, and hosted-check revalidation.
- Review dispatches follow a monotonic scope-to-reasoning ladder: broader aperture or greater consequence raises the minimum capability and reasoning floor; a lower tier may discover findings but may never satisfy a higher-tier obligation.
- The blind final reviewer and closure auditor run in fresh independent contexts on the orchestrator's literal inherited model/reasoning route or an explicitly selected identical route. If route equality and fresh context cannot both be proved, green blocks; no silent downgrade is permitted.
- Cutover requires both deterministic state-soundness tests and 100% per-trial recall of the versioned frontier-reference issue set for every supported weaker-model/profile combination.
- A valid in-scope issue first found by an independent external frontier reviewer after internal green is a frontier escape: the benchmark pass is revoked, the missed tier is classified, and the case becomes a permanent regression fixture.
- Source edits remain under `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/` and `codex-marketplace/plugins/superpowers-plus/skills/selecting-a-subagent/`; `.agents/skills/` remains generated.
- Consumer repositories supply local commands and domain obligations. Portable source must not assume this repository's paths outside explicit repo-local adapters.
- Until Plan 7 cuts over and passes the benchmark plus pressure campaign, the existing skill must be described as review assistance, not proof of reviewed green.

## Plan acceptance boundaries

### Plan 1 - Evidence kernel

- Strict version-2 state, scope/risk floors, parent/child route-selection records, cross-reference validation, content-addressed evidence, chained history, atomic writes, pure ordered tier policy, and transient green evaluation exist behind one CLI.
- Every known version-1 false-green/dead-route defect is a fixture proving legacy state cannot satisfy version 2; only the current baseline routing-test inconsistency is repaired.
- Missing one green predicate, skipped or downgraded review tier, unproved final parent-route equality, stale or changed evidence bytes, persisted green, accepted risk, and malformed remote observation all fail closed.

### Plan 2 - Snapshot and authority

- Remote PR URL, full base/head/tree SHAs, canonical diff bytes, PR metadata, required-check policy, repo law, linked issues/documents, plans/specs, and non-goals are materialized and hashed into one authority manifest.
- Base/head/tree, PR scope, governing authority, new unresolved PR feedback, or required-check-policy drift creates a new epoch and invalidates current evidence according to explicit rules.
- Missing connectors, unavailable linked authority, ambiguous base, shallow history, uncommitted review input, or non-remote head blocks.

### Plan 3 - Impact and coverage

- Independent semantic dependency mapping and contract/data-flow/user-journey mapping produce a union of changed and affected surfaces; a separate challenger attacks omissions.
- Every affected surface receives applicable universal and repo/domain obligations. Each obligation records its aperture and the maximum of its scope-derived and risk/consequence-derived capability and reasoning floors. High-risk work is at least `strong` and gets independent overlap; `not-applicable` needs positive proof; zero lens matches blocks.
- Reviewer packages contain the complete patch, authorities, dependency context, generated-source provenance, and read-only repo access. Diff slices are navigation only and cannot hide context.

### Plan 4 - Reviewer execution

- Preserve intentionally different `reviewer-fast`, `reviewer-fixes`, `reviewer`, and `reviewer-strong` roles, but make their policy tiers explicit: hunk/file mechanical review may use `fast`; bounded fixes and surfaces use at least `focused`; cross-file, security, architectural, and high-risk review uses at least `strong`; whole-PR synthesis uses `orchestrator-equivalent`.
- The live route adapter queries the current inventory and budget through `selecting-a-subagent`, records the parent and child model/reasoning/context routes plus selection mode, and rejects any dispatch below its obligation floor. `reviewer-strong` literally inherits the parent route when the runtime can preserve fresh context; otherwise it selects the same model and reasoning explicitly. Unprovable equivalence blocks.
- Reviewer profiles are role-bounded and portable, with explicit assignment IDs, model/context/profile identity, structured JSON output, inspected surfaces, tested hypotheses, commands, findings, and uncertainties. Canonical Devin, Codex, and shared policy surfaces encode the same ladder without assuming provider names, prices, entitlements, or that every parent is the strongest available route.
- Dispatcher validation rejects wrong snapshot/dispatch/profile/route, omitted assignments, malformed reports, unsupported clean verdicts, silent downgrade, and partial/tool-capped runs. Remaining work is redispatched at the required or higher tier or blocks.
- Independence means a fresh agent context and distinct dispatch; high-risk overlap uses distinct profiles or hazard framings. Final-review context excludes prior reports/findings by manifest validation. Repeated generic passes without distinct obligations are removed.

### Plan 5 - Findings and fixes

- Every severity follows an immutable lifecycle. Only evidence-backed `fixed` or `false-positive` satisfies green; `accepted-risk` produces `reviewed-with-exceptions`; all other dispositions block.
- Independent adjudication verifies each finding. Fixes use RED/GREEN evidence when applicable, are published, create a new epoch, and trigger impact recomputation plus all invalidated obligation reviewers. A fix may narrow back to a focused reviewer, but the workflow must then repeat every invalidated broader tier in ascending order; a lower-tier rereview never preserves a stale higher-tier attestation.
- No cumulative historical count, stale regression link, overwritten origin field, missing round increment, circular resolution artifact, or arbitrary round cap can discard an unresolved issue or authorize green.

### Plan 6 - Independent closure and remote presentation

- Planning/archive/closeout mutations happen before the final freeze. A blind final reviewer and separate closure auditor both produce current valid attestations from fresh contexts on the orchestrator's inherited route or an explicitly identical model/reasoning route; disagreement, uncertainty, unavailable equality evidence, or downgrade blocks.
- Required hosted checks are discovered from current policy and must succeed on the exact reviewed remote head. Draft-to-ready is an explicit CI-candidate transition, not green.
- A candidate seal is content-bound. `reviewctl present` re-fetches remote head, authority metadata, unresolved feedback, and required checks and emits green only for the exact matching SHA without persisting green.

### Plan 7 - Benchmark and cutover

- A versioned mutation/PR corpus spans every universal category. The reference set contains findings independently reproduced by two blinded frontier runs or confirmed by human adjudication.
- Every supported weaker-model/profile combination achieves 100% reference-finding recall on every one of at least three fresh trials per case, with zero false greens. New frontier-stable misses become permanent fixtures.
- Benchmark and dogfood PRs receive an additional blinded external frontier audit after internal green. The release target is zero frontier escapes across benchmark trials; production reports escape count per green PR by severity, obligation category, and tier that should have caught it, without presenting zero future escapes as a correctness guarantee.
- Adversarial pressure tests cover truncation, no matching lens, stale CI, post-final drift, anchoring, premature-green pressure, generated-source omissions, cross-lens fixes, and unavailable tools/context.
- `SKILL.md` becomes a sub-500-word control plane; metrics, encoding normalization, ledger rendering, and summaries are derived CLI views rather than semantic graph nodes; version-1 authorities and parallel routes are removed; generated marketplace surfaces and consumer migration guidance are verified.

## Epic done gate

The epic is done only when all seven plans are merged, canonical staged CI and exact-SHA hosted CI pass, the Plan 7 benchmark has 100% per-trial reference recall, zero false greens, and zero frontier escapes, the marketplace/generated copies match canonical source, a fresh end-to-end dogfood review produces a presentation proof, and no user-facing path can label version-1 or incomplete version-2 work reviewed green.

## Assessment traceability

| Proven weakness | Owning plan and closure evidence |
|---|---|
| Router sequences names without proving evidence; final review can be skipped or unvalidated | Plans 1 and 4: pure predicates, dispatch/report matching, remove-one-predicate tests |
| Circular resolution entry, cumulative preflight counts, never-closing regressions, lost normalization origin, missing round advancement | Plans 1 and 5: frozen legacy fixtures, replacement lifecycle tests; no repair investment in the dead graph beyond current baseline CI |
| `blocked` cannot lawfully resume | Plan 1: blocker/resolution evidence and transition-table tests |
| Stale initial diff/head/authority after fixes or closeout mutation | Plans 2, 5, and 6: epochs, fix invalidation, closeout-before-freeze, exact-SHA presentation |
| Heuristic lens selection can produce zero deep review and misses affected dependencies | Plan 3: dual impact maps, universal obligations, non-zero assignment gate, independent scope challenge |
| Diff slicing hides context | Plan 3: complete patch plus dependency/context package and live read-only repo access |
| Reviewer profiles are narrow, speed-biased, anchored, or silently truncated by tool caps | Plans 4 and 7: bounded role profiles, blind context exclusion, incomplete/redispatch semantics, weaker-model pressure trials |
| The graph names strong profiles but does not force increasing reasoning as review aperture widens | Plans 1, 3, 4, 5, and 6: scope/risk floors in state, monotonic tier policy, observed route attestation, post-fix re-ascent, and orchestrator-route final/closure tests |
| No structured coverage attestation, finding proof, or dispatch identity | Plans 1, 4, and 5: strict records, schema validation, all-severity lifecycle and evidence hashes |
| Local checks or old hosted CI can be mistaken for current PR proof | Plans 2 and 6: full snapshot identity, required-check discovery, exact remote SHA, transient presentation observation |
| Accepted or deferred known defects can be called green | Plans 1 and 5: only fixed/false-positive is green; accepted risk has a distinct non-green terminal result |
| Metrics, encoding normalization, ledger rendering, and summaries consume semantic graph nodes | Plan 7: derived views behind the CLI; bookkeeping nodes removed |
| No objective test that weaker agents match frontier-reliable detection | Plan 7: blinded frontier-reference corpus and 100% per-trial recall/zero-false-green release gate |
| Expensive external frontier review can still reject internally green PRs for issues the workflow should have caught | Plan 7: blinded downstream frontier audit, zero-escape benchmark gate, missed-tier classification, and permanent escape fixtures |
| Current focused suite is red | Plan 1: preserve the intended lens-triage contract, make the minimal route correction, and require the complete focused suite green |

## Handoff notes

- The earlier `iterative-review-triage-and-selection` roadmap remains historical evidence for completed Plan 1. Its pending generation-aware selection and automated triage work is superseded by Plans 3 and 4 here.
- Plans 2-7 are intentionally written just-in-time after the previous plan lands. Their titles and acceptance boundaries are fixed by this roadmap, but implementation detail must use the then-current source.
- Plan 1 is sequential because its transition policy consumes the model and store produced by earlier tasks. Use `/executing-plans` for Plan 1; later plans may select `/subagent-driven-development` when their tasks are independent.
