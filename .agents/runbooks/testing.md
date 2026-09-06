# Testing Runbook

Use this runbook for the test commands and conventions in `agent-asset-marketplace`.

## Before you begin

- Read [`.devin/rules/tools.md`](../../.devin/rules/tools.md) for the canonical validation commands.
- Read [`.agents/runbooks/implementing.md`](./implementing.md) for the TDD workflow.

## When to use

- Writing new tests.
- Running the test suite before claiming completion.
- Choosing the right validation command for a change.

## Repo-specific guidance

- Start with the focused test or target that proves the changed behavior. Use
  the full `py -3 -m pytest` suite when the touched surface, plan, or final
  gate requires repository-wide regression proof.
- Run a single test file with `py -3 -m pytest tests/<file>.py -v`.
- This repo uses proportionate test-driven development: write a failing test
  before independent behavior, then make it pass; pure glue can rely on a
  focused contract and transitive caller coverage.
- Contract tests live under `tests/`. Marketplace generation correctness is proven by `tools/run marketplace --apply` and `tools/run ci --check`.
- After changing source custody, adapters, plugin shapes, bundle manifests,
  source maps, provenance maps, or generated zips, run the full marketplace
  rebuild as the green-path proof.

## Routing to skills

- For TDD implementation, invoke `/test-driven-development`.
- For test design and coverage, invoke `/unslop-profiles` with the `testing` profile.
- For repo hygiene and publication, invoke `/repo-worker-base`.
