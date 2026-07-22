# Testing Guide

Use this guide for the test commands and conventions in `agent-asset-marketplace`.

## Before you begin

- Read [`tools/AGENTS.md`](../../tools/AGENTS.md) for the canonical validation commands.
- Read [`.agents/guides/implementing-guide.md`](./implementing-guide.md) for the TDD workflow.

## When to use

- Writing new tests.
- Running the test suite before claiming completion.
- Choosing the right validation command for a change.

## Repo-specific guidance

- Run the full test suite with `py -3 -m pytest` from the repo root.
- Run a single test file with `py -3 -m pytest tests/<file>.py -v`.
- This repo uses test-driven development. Write a failing test before implementation code, then make it pass.
- Contract tests live under `tests/`. Marketplace generation correctness is proven by `py -3 tools/rebuild_marketplace.py` and `py -3 tools/check_marketplace.py`.
- After changing source custody, adapters, projection plugin shapes, bundle manifests, source maps, provenance maps, or generated zips, run the full marketplace rebuild as the green-path proof.

## Routing to skills

- For TDD implementation, invoke `/test-driven-development`.
- For test design and coverage, invoke `/unslop-profiles` with the `testing` profile.
- For repo hygiene and publication, invoke `/repo-worker-base`.
