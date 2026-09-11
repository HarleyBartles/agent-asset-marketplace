# Testing Runbook

Use this runbook for the test commands and conventions in `agent-asset-marketplace`.

## Before you begin

- Read [`.devin/rules/tools.md`](../../.devin/rules/tools.md) for the canonical validation commands.
- Read [`.agents/runbooks/implementing.md`](./implementing.md) for repository-specific implementation constraints.

## When to use

- Writing new tests.
- Running the test suite before claiming completion.
- Choosing the right validation command for a change.

## Repo-specific guidance

- Start with the focused test or target that proves the changed behavior. Use
  the full `py -3 -m pytest` suite when the touched surface, plan, or final
  gate requires repository-wide regression proof.
- Run a single test file with `py -3 -m pytest tests/<file>.py -v`.
- Contract tests live under `tests/`. Marketplace generation correctness is proven by `tools/run marketplace --apply` and `tools/run ci --check`.
- After changing source custody, adapters, plugin shapes, bundle manifests,
  source maps, provenance maps, or generated zips, run the full marketplace
  rebuild as the green-path proof.

## Workflow routing

Invoke `using-superpowers-plus` once and follow its testing or implementation
handoff. This runbook owns only the repository's test commands and locations.
