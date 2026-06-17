---
name: codex-receipts-superpowers
description: Use when repo-backed work needs the smallest applicable workflow skill, durable plan and implementation-record receipts, and a closeout path that naturally links both artifacts.
metadata:
  source-id: codex-receipts-superpowers
  source-path: sources/first_party/skills/codex-receipts-superpowers/SKILL.md
  provenance-name: MARK-162 Codex Receipts Superpowers compositional skill
license: "MIT"
---
# Codex Receipts Superpowers

Use this skill when non-trivial repo-backed work should leave a durable plan and
matching implementation record instead of a one-off worker transcript.

## Core job

Shape repo-backed work so it publishes:

1. a plan under the repository's local convention, or `docs/superpowers/plans/`
   by default;
2. a matching implementation record under the repository's local convention, or
   `docs/superpowers/records/` by default;
3. a PR body or final worker report that links both durable artifacts.

## Composition

Start with `@using-superpowers` as the workflow-selection entrypoint.

Use `@writing-plans` to make receipt publication part of the route review and
to keep the implementation plan explicit before code changes begin.

Use `@executing-plans` as the outer implementation workflow and do not treat
the work as finished until the matching implementation record is ready for
closeout.

Use `repo-worker-base:codex-repo-receipts` for the exact artifact contract, default paths, and
narrow omission rule.

Use `@unslop-superpowers` when the packet needs repo-specific anti-slop
controls, evidence requirements, or a narrow omission decision.

Use `@connector-safety` only for connector mutations or blocked-write recovery.

Nesting rule:

- pick the smallest specialist workflow that actually fits;
- do not stack extra skills just because they exist;
- treat durable receipt publication as part of the work, not as a retrospective
  note.

## Receipt rules

- Treat non-trivial repo-backed work as incomplete until both durable artifacts
  exist, unless a narrow explicit omission applies.
- Keep the implementation record factual: issue, branch, main SHA,
  implementation commit SHA, receipt/record commit SHA when known, final PR
  head at publication or review when useful, PR URL, changed files, generated
  artifacts, validation, skipped checks, and surprises or follow-ups.
- Do not require the record file to be rewritten solely because later pushes
  move the PR tip.
- After the record commit exists, later PR head movement is publication
  evidence verified from GitHub PR state, not a recursive receipt update.
- A record is stale only if it misstates a durable fact, omits important
  validation or publication evidence, or claims finality that GitHub disproves.
- Keep the PR body or final worker report linked to both the plan and the
  implementation record.
- Do not duplicate repository doctrine into repository `AGENTS.md` files.

## Authority split

This skill shapes workflow selection and receipt publication for repo-backed
work.

It does not replace `repo-worker-base:codex-repo-receipts`, does not own connector mutation
rules, and does not claim publication or closeout by itself.

interface:
  display_name: Codex Receipts Superpowers
  short_description: Shape repo-backed work so plans and implementation records are published together.
  default_prompt: Use $codex-receipts-superpowers for non-trivial repo-backed work so the worker publishes a plan under the repository's local convention, or docs/superpowers/plans/ by default, plus a matching implementation record under the repository's local convention, or docs/superpowers/records/ by default. Start with $using-superpowers, route through $writing-plans, execute with $executing-plans, keep the scope narrow with $unslop-superpowers, and use $codex-repo-receipts for the artifact contract. Link both artifacts in the PR body or final worker report. Omit receipts only for tiny mechanical changes, and only when the omission is explicit and justified.
policy:
  products:
  - chatgpt
  - codex
  - api
  - atlas
  allow_implicit_invocation: true
