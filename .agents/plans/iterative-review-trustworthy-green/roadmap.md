# Trustworthy Iterative Review - Epic Roadmap

Source spec: [Trustworthy Iterative Review Design](../../specs/2026-08-21-trustworthy-iterative-review-design.md)

| # | Title | Status | Plan File | Commit | PR | Rating | Notes |
|---|---|---|---|---|---|---|---|
| 1 | Fail-closed evidence kernel and legacy false-green regression suite | ready | [Plan 1](2026-08-21-plan-1-evidence-kernel.md) | - | - | 9/10 | Establish the sole machine state, atomic evidence registry, green predicate, transition policy, and regression tests for every proven version-1 router defect. |
| 2 | Immutable snapshot epochs and authority manifest | pending | - | - | - | - | Bind full base/head/tree identifiers, diff and metadata hashes, repo law, linked issue documents, and drift invalidation to each review epoch. |
| 3 | Impact inventory, coverage planner, and safe reviewer packages | pending | - | - | - | - | Replace heuristic lens selection with changed/affected-surface obligations, risk-based overlap, generation-aware classification, and context packages that cannot hide dependencies. |
| 4 | Structured reviewer execution and attestation validation | pending | - | - | - | - | Dispatch bounded independent roles, validate identity/context/completeness, redispatch truncated work, and require positive evidence for every assigned obligation. |
| 5 | Finding adjudication, fix impact, and re-review lifecycle | pending | - | - | - | - | Track all severities, independently adjudicate findings, enforce fixed/false-positive proof, keep accepted risk non-green, publish fixes, and invalidate every affected obligation. |
| 6 | Blind final review, closure audit, exact-SHA seal, and presentation recheck | pending | - | - | - | - | Add independent final roles, move closeout before the final snapshot, bind required hosted checks to the remote reviewed head, and re-fetch mutable remote state immediately before human handoff. |
| 7 | Frontier-reference benchmark, skill simplification, migration, and rollout | pending | - | - | - | - | Gate weaker-model profiles against a versioned frontier-stable defect corpus, cut over to one `reviewctl` path, remove bookkeeping nodes and legacy authorities, keep `SKILL.md` under 500 words, regenerate surfaces, and publish consumer-safe guidance. |

## Epic invariants

- No plan may weaken the green predicate in the source spec.
- Each plan uses test-driven development and lands as a reviewable draft pull request before the next plan is written.
- Version-1 state, reports, and metrics may inform migration diagnostics but may not satisfy a version-2 green gate.
- A known `accepted-risk` finding may produce `reviewed-with-exceptions` but never green.
- A stored seal is only a candidate proof; human-facing green requires a fresh remote head, authority, and hosted-check revalidation.
- Cutover requires both deterministic state-soundness tests and 100% per-trial recall of the versioned frontier-reference issue set for every supported weaker-model/profile combination.
- Source edits remain under `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/` and `codex-marketplace/plugins/superpowers-plus/skills/selecting-a-subagent/`; `.agents/skills/` remains generated.
- Consumer repositories supply local commands and domain obligations. Portable source must not assume this repository's paths outside explicit repo-local adapters.
- Until Plan 7 cuts over and passes the benchmark plus pressure campaign, the existing skill must be described as review assistance, not proof of reviewed green.

## Plan acceptance boundaries

### Plan 1 - Evidence kernel

- Strict version-2 state, record vocabularies, cross-reference validation, content-addressed evidence, chained history, atomic writes, pure transition policy, and transient green evaluation exist behind one CLI.
- Every known version-1 false-green/dead-route defect is a fixture proving legacy state cannot satisfy version 2; only the current baseline routing-test inconsistency is repaired.
- Missing one green predicate, stale or changed evidence bytes, persisted green, accepted risk, and malformed remote observation all fail closed.

### Plan 2 - Snapshot and authority

- Remote PR URL, full base/head/tree SHAs, canonical diff bytes, PR metadata, required-check policy, repo law, linked issues/documents, plans/specs, and non-goals are materialized and hashed into one authority manifest.
- Base/head/tree, PR scope, governing authority, new unresolved PR feedback, or required-check-policy drift creates a new epoch and invalidates current evidence according to explicit rules.
- Missing connectors, unavailable linked authority, ambiguous base, shallow history, uncommitted review input, or non-remote head blocks.

### Plan 3 - Impact and coverage

- Independent semantic dependency mapping and contract/data-flow/user-journey mapping produce a union of changed and affected surfaces; a separate challenger attacks omissions.
- Every affected surface receives applicable universal and repo/domain obligations. High-risk obligations get independent overlap; `not-applicable` needs positive proof; zero lens matches blocks.
- Reviewer packages contain the complete patch, authorities, dependency context, generated-source provenance, and read-only repo access. Diff slices are navigation only and cannot hide context.

### Plan 4 - Reviewer execution

- Reviewer profiles are role-bounded and portable, with explicit assignment IDs, model/context/profile identity, structured JSON output, inspected surfaces, tested hypotheses, commands, findings, and uncertainties.
- Dispatcher validation rejects wrong snapshot/dispatch/profile, omitted assignments, malformed reports, unsupported clean verdicts, and partial/tool-capped runs. Remaining work is redispatched or blocks.
- Independence means a fresh agent context and distinct dispatch; high-risk overlap uses distinct profiles or hazard framings. Final-review context excludes prior reports/findings by manifest validation. Repeated generic passes without distinct obligations are removed.

### Plan 5 - Findings and fixes

- Every severity follows an immutable lifecycle. Only evidence-backed `fixed` or `false-positive` satisfies green; `accepted-risk` produces `reviewed-with-exceptions`; all other dispositions block.
- Independent adjudication verifies each finding. Fixes use RED/GREEN evidence when applicable, are published, create a new epoch, and trigger impact recomputation plus all invalidated obligation reviewers.
- No cumulative historical count, stale regression link, overwritten origin field, missing round increment, circular resolution artifact, or arbitrary round cap can discard an unresolved issue or authorize green.

### Plan 6 - Independent closure and remote presentation

- Planning/archive/closeout mutations happen before the final freeze. A blind final reviewer and separate closure auditor both produce current valid attestations; disagreement or uncertainty blocks.
- Required hosted checks are discovered from current policy and must succeed on the exact reviewed remote head. Draft-to-ready is an explicit CI-candidate transition, not green.
- A candidate seal is content-bound. `reviewctl present` re-fetches remote head, authority metadata, unresolved feedback, and required checks and emits green only for the exact matching SHA without persisting green.

### Plan 7 - Benchmark and cutover

- A versioned mutation/PR corpus spans every universal category. The reference set contains findings independently reproduced by two blinded frontier runs or confirmed by human adjudication.
- Every supported weaker-model/profile combination achieves 100% reference-finding recall on every one of at least three fresh trials per case, with zero false greens. New frontier-stable misses become permanent fixtures.
- Adversarial pressure tests cover truncation, no matching lens, stale CI, post-final drift, anchoring, premature-green pressure, generated-source omissions, cross-lens fixes, and unavailable tools/context.
- `SKILL.md` becomes a sub-500-word control plane; metrics, encoding normalization, ledger rendering, and summaries are derived CLI views rather than semantic graph nodes; version-1 authorities and parallel routes are removed; generated marketplace surfaces and consumer migration guidance are verified.

## Epic done gate

The epic is done only when all seven plans are merged, canonical staged CI and exact-SHA hosted CI pass, the Plan 7 benchmark passes, the marketplace/generated copies match canonical source, a fresh end-to-end dogfood review produces a presentation proof, and no user-facing path can label version-1 or incomplete version-2 work reviewed green.

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
| No structured coverage attestation, finding proof, or dispatch identity | Plans 1, 4, and 5: strict records, schema validation, all-severity lifecycle and evidence hashes |
| Local checks or old hosted CI can be mistaken for current PR proof | Plans 2 and 6: full snapshot identity, required-check discovery, exact remote SHA, transient presentation observation |
| Accepted or deferred known defects can be called green | Plans 1 and 5: only fixed/false-positive is green; accepted risk has a distinct non-green terminal result |
| Metrics, encoding normalization, ledger rendering, and summaries consume semantic graph nodes | Plan 7: derived views behind the CLI; bookkeeping nodes removed |
| No objective test that weaker agents match frontier-reliable detection | Plan 7: blinded frontier-reference corpus and 100% per-trial recall/zero-false-green release gate |
| Current focused suite is red | Plan 1: preserve the intended lens-triage contract, make the minimal route correction, and require the complete focused suite green |

## Handoff notes

- The earlier `iterative-review-triage-and-selection` roadmap remains historical evidence for completed Plan 1. Its pending generation-aware selection and automated triage work is superseded by Plans 3 and 4 here.
- Plans 2-7 are intentionally written just-in-time after the previous plan lands. Their titles and acceptance boundaries are fixed by this roadmap, but implementation detail must use the then-current source.
- Plan 1 is sequential because its transition policy consumes the model and store produced by earlier tasks. Use `/executing-plans` for Plan 1; later plans may select `/subagent-driven-development` when their tasks are independent.
