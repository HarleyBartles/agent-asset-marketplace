# TPS Ingress v1

Use this skill when consuming, reviewing, validating, falsifying, routing, or deciding whether to trust a TPS report, worker return, handoff note, validation summary, closeout memo, or other durable claim surface produced by someone else.

TPS is a reporting protocol, not vibes. This skill owns consumer-side ingress. It does not rewrite the reporter's domain body unless repair is required, and it does not treat a well-written report as verified source truth.

## Owned decision

Given an incoming report, decide whether it is ingestible and what must happen next.

Return one of:

- `accepted_for_ingress` — the report has a TPS cover sheet, named evidence surfaces, clear scope, and claims that can be consumed with their stated verification status.
- `repair_required` — the producer or current agent must repair report structure, evidence labels, scope, or claim partitioning before the report can drive decisions.
- `falsified` — at least one material claim conflicts with durable source evidence.
- `blocked` — the report cannot be assessed because required source surfaces, authority, or context are unavailable.

## Producer / consumer split

This is the consumer-side skill. It ingests reports.

Use `tps-reporting-v1` to produce a new report. Do not collapse ingestion into report production. Ingress may produce a review note, but that review note is a new TPS report if it needs to become durable.

## Ingress steps

1. Confirm the report has a TPS cover sheet.
2. Identify the report type, producer, intended consumer, scope, non-scope, source surfaces, claim status, validation run, open risks, and handoff route.
3. Separate durable source evidence from producer claims, inferences, assumptions, and out-of-scope material.
4. Check whether the domain-specific body is owned by an appropriate domain skill, repo playbook, issue acceptance criteria, or project doctrine.
5. Verify material claims against durable source surfaces when the decision depends on them.
6. Falsify before trusting: actively look for contradictions, missing files, stale branch/PR state, failed checks, incomplete artifacts, or issue-goal mismatch.
7. Route the report to accept, repair, falsify, block, or continue work.

## Required cover sheet gate

A report without a cover sheet fails TPS ingress by default.

A minimum ingestible cover sheet names:

- report identity and type;
- producer and intended consumer;
- scope and non-scope;
- source surfaces inspected;
- claim verification status;
- validation run or validation omission reason;
- open risks;
- handoff route.

If the missing cover sheet can be reconstructed from adjacent durable source without changing claims, return `repair_required` and state the repair. If reconstruction would require guessing, return `blocked` or ask the producer for repair through the durable control plane.

## Claim partitioning

Treat incoming statements as one of:

- `verified_source` — directly observed by this ingress pass in durable surfaces.
- `producer_claim` — stated by the reporter but not independently verified.
- `inference` — reasoned from evidence; keep the inference label.
- `assumption` — necessary premise that still needs confirmation.
- `falsified_claim` — contradicted by durable evidence.
- `out_of_scope` — explicitly not assessed during this ingress pass.

Worker reports are claims until verified against durable source surfaces. Passing tests is not equal to issue-goal conformance; compare test evidence to the actual goal, acceptance criteria, and changed surfaces.

## Falsification route

Before accepting a report as decision-ready, try to falsify material claims:

- Check that named files, artifacts, branches, commits, PRs, issues, or links exist.
- Check that claimed changes match the actual diff or artifact.
- Check that validation commands and results are plausible and relevant.
- Check that skipped validation has a real blocker, not convenience language.
- Check that the report's scope matches the issue goal and non-goals.
- Check that no unrelated surfaces were silently imported, mutated, or claimed.
- Check that open risks do not undermine the claimed status.

If falsification succeeds, return `falsified` with the contradictory evidence and the safe next route.

## Repair route

Return `repair_required` when the report is probably salvageable but unsafe to use as-is:

- cover sheet fields are missing or ambiguous;
- source surfaces are named too vaguely to inspect;
- producer claims and verified evidence are mixed;
- domain body lacks required domain-owned evidence;
- validation output is summarized without exact commands or observable result;
- issue-goal conformance is not addressed;
- handoff route is missing or points to a wrong control plane.

Repair should be boring and bounded: request the missing field, evidence, or verification route. Do not expand repair into unrelated follow-up work.

## Accept route

Return `accepted_for_ingress` only when the report can safely drive the next decision with its stated verification limits.

Acceptance does not mean every claim is true. It means the report is structured, partitioned, and evidenced well enough that the consumer knows what is verified, what remains a claim, what is risky, and where to continue.

## Block route

Return `blocked` when:

- required source surfaces are inaccessible;
- the report relies on hidden chat-only context;
- the consumer lacks authority to inspect or decide;
- material evidence has expired, disappeared, or cannot be matched to the report;
- repair would require inventing producer knowledge.

## Output shape

For ingress reviews, return:

1. Ingress decision.
2. Cover sheet status.
3. Material claims reviewed.
4. Verification/falsification evidence.
5. Repair or next route.
6. Remaining risks.

Stop after routing the report. Do not import or evaluate unrelated skills merely because the report mentions them.
