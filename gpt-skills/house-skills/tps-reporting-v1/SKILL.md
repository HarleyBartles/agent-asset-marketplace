# TPS Reporting v1

Use this skill when producing a report, worker return, handoff note, validation summary, closeout memo, or other durable claim surface that another agent, reviewer, project owner, or future session may need to ingest.

TPS is a reporting protocol, not vibes. It does not own every domain-specific report body. It owns the producer-side cover sheet, claim discipline, source partitioning, and falsifiable evidence posture that make the report safe to consume.

## Owned decision

Given a request to report work or findings, produce a TPS-shaped report with a required cover sheet and a domain-owned body.

Return one of:

- `tps_report_ready` — the report includes the required cover sheet, body, evidence, and limits.
- `repair_required` — the report can be fixed now but is missing required TPS structure, evidence, or claim partitioning.
- `blocked` — the report cannot be produced honestly because required source surfaces, validation, or authority are unavailable.

## Producer / consumer split

This is the producer-side skill. It creates reports.

Use `tps-ingress-v1` when consuming, reviewing, validating, falsifying, or routing someone else's report. Do not collapse these jobs. A report that is easy to write is not necessarily safe to ingest.

## Required TPS cover sheet

Every TPS report requires a cover sheet before the body. If the report has no cover sheet, it is not a TPS report.

The cover sheet should be compact, but it must include:

- `report_id` — stable identifier when available, or a short generated identifier.
- `report_type` — worker return, validation summary, closeout, incident note, source assessment, handoff, or other named type.
- `producer` — agent/person/system that produced the report.
- `consumer` — intended reviewer, next agent, project owner, issue, or durable surface.
- `scope` — what the report claims to cover.
- `non_scope` — what the report explicitly does not cover.
- `source_surfaces` — durable surfaces inspected, such as files, commits, PRs, Linear issues, logs, artifacts, screenshots, or commands.
- `claim_status` — `verified`, `partially_verified`, `unverified`, or `blocked`.
- `validation_run` — checks performed and observable results, or why validation was not run.
- `open_risks` — known uncertainty, missing evidence, race conditions, stale assumptions, or follow-up work.
- `handoff_route` — where the consumer should verify, continue, merge, reject, or archive the report.

Use prose or a Markdown table unless the destination explicitly requires JSON/YAML. Do not use dispatch-shaped YAML for an ordinary TPS report.

## Domain-owned body

TPS owns the cover sheet and evidence posture. The reporting domain owns the report body.

Examples:

- Code work body: changed files, implementation notes, tests, PR/commit evidence.
- Validation body: acceptance criteria, observed behavior, commands, failures, reproduction limits.
- Source-intake body: source payload, provenance, license/trust notes, import decisions.
- Design or product body: decision context, options, constraints, accepted/rejected outcomes.

Do not force domain content into a generic TPS template when a domain-specific report format exists. Put the TPS cover sheet first, then let the domain body use the domain's best format.

## Source partitioning rules

Partition report claims before writing the final answer:

- `verified_source` — observed in durable source surfaces during this reporting pass.
- `reported_claim` — claimed by another agent, issue, comment, user, or document but not independently verified.
- `inference` — reasoned from sources; label it as inference.
- `assumption` — necessary but unverified premise; label it and route for confirmation when material.
- `out_of_scope` — relevant-looking material intentionally not assessed.

Generic/base source partitioning folds into TPS unless another specific skill owns the partition for a narrower domain. Passing tests is not equal to issue-goal conformance; tests are evidence inside the report, not the whole report.

## Evidence requirements

A TPS report should make claims falsifiable by pointing to durable evidence surfaces:

- file paths and line ranges when reporting repo content;
- branch, commit, PR, and diff evidence when reporting code work;
- exact commands and results when reporting validation;
- issue identifiers, comment links, or document names when reporting control-plane state;
- artifact paths, screenshots, logs, or manifests when reporting generated outputs.

If a claim cannot be verified, label it as a claim. Worker reports are claims until checked against durable source surfaces.

## Repair triggers

Return `repair_required` instead of a finished report when:

- the cover sheet is missing;
- scope and non-scope are unclear;
- source surfaces are not named;
- validation is summarized as "passed" without commands or observable evidence;
- issue-goal conformance is implied only from passing tests;
- domain body claims are mixed with assumptions;
- the handoff route is missing;
- the report asks the consumer to trust the producer's confidence rather than inspect evidence.

## Block triggers

Return `blocked` when:

- required durable source surfaces are unavailable;
- the producer is asked to report on private hidden context as if it were source truth;
- validation is required for the report's claim but cannot be run or observed;
- the requested report would blur producer and consumer responsibilities;
- the report would present unverified worker claims as verified outcomes.

## Output shape

Use this order:

1. TPS cover sheet.
2. Domain-specific report body.
3. Evidence and validation details, if not already included in the body.
4. Open risks and next actions.

Stop when the report is complete. Do not add unrelated skill imports, future-work speculation, or broad doctrine unless the domain body requires it.
