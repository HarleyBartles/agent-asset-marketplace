# Implementing Runbook

Use this reference for repository-specific implementation commands,
marketplace custody, and completion checks in agent-asset-marketplace.

## Before You Begin: Read the Standards

Read these standards documents before writing any code:

- **[`.agents/doctrine/custody-and-marketplace-doctrine.md`](../../.agents/doctrine/custody-and-marketplace-doctrine.md)** — source custody rules, provenance modes, plugin curation rules
- **[`.devin/rules/tools.md`](../../.devin/rules/tools.md)** — marketplace generation and validation tooling

## Workflow routing

Invoke `using-superpowers-plus` once and follow its implementation handoff.
This runbook supplies only marketplace-specific constraints.

## Pre-Completion Verification

Before claiming work is done, verify:

- **Current-state validation passes:** use the repository's canonical gate for
  the exact tree/staged state being claimed. A normal commit uses the tracked
  pre-commit gate; run `tools/run ci --check` separately only for uncommitted
  verification, diagnosis, or explicit CI-parity evidence.
- **Marketplace regeneration succeeds:** `tools/run marketplace --apply` for local rebuild
- **Vendored output changed as intended:** If the task claims to update a vendored asset or marketplace bundle, verify the published vendored output itself changed on the PR head. An overlay, manifest edit, or generator tweak is not sufficient if the resulting vendored file still shows the stale behavior.
- **INDEX.md regenerated:** If files were added or removed, run `tools/run mesh --apply`
- **Generated skills refreshed:** If canonical marketplace skills were modified,
  run `py -3 tools/run.py marketplace --apply`; never hand-edit downstream
  installed copies to bypass source review.
- **Runtime subagent profiles synced:** If `reviewer-*.md` profiles in the Devin Desktop agents search path or other subagent profiles were added or changed, run `py -3 tools/run.py runtime-agents --apply --allow-shared-checkout` to stage them in the main checkout. Restart the IDE before dispatching `run_subagent` with the new profiles.
- **Cross-repo consumer safety:** If the work changes a vendored skill, prompt, or marketplace bundle, confirm the change is safe for sister or consumer repos that install from this marketplace. Replace repo-specific commands and paths with consumer-canonical alternatives and avoid assumptions that do not hold in the consumer's environment.

Generic execution discipline, scope honesty, plan completion, subagent
dispatch, self-review, and handoff are owned by the routed implementation and
review skills.
