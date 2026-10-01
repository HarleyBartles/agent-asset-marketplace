# Marketplace Adoption Migration Roadmap

**Status:** complete

**Goal:** Decompose the Marketplace's own adoption migration into safe, reviewable plans that replace the old deployment model without losing the repository's actual compliance gates.

**Authority:** [Approved AOM design](../../specs/2026-09-30-aom-standard-adoption-and-shipping.md), especially sections 7-9, and the existing [epic roadmap](roadmap.md).

## Why this is a roadmap

The current enforcement path combines at least five responsibilities: v1 standard dispatch, copies of Marketplace resources under `.agents/standards/`, byte hashes in a generated provenance file, formatter policy and wheel ownership, and repo-specific hook commands. The v2 subscription model makes a different promise: an immutable definition identifies the standard, while the repository owns its implementation, compliance chain, and continuing self-certification. Removing the old runtime before the new repository-owned chain is working would temporarily remove meaningful gates; changing all of these responsibilities in one plan would make failures and ownership changes difficult to review.

## Migration sequence

| Plan | Deliverable                                           | Exit condition                                                                                                                                                                                                                                                                 |
| ---- | ----------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 8    | V2 subscription and repository-owned compliance chain | This repository records only selected standards, pins published definitions, routes agents to truthful certification, and the normal hook/CI invokes repository-owned checks without depending on vendor-byte identity.                                                        |
| 9    | Retire legacy standard deployment machinery           | No active command, hook, skill, or documentation path requires copied marketplace scaffolders, the old exception contract, v1 composition dispatcher, or byte-provenance ledger. Selected standard invariants remain represented in repository-owned checks and certification. |
| 10   | Retire obsolete standards and Markdown formatter      | Obsolete catalog entries and formatter/wheel machinery have no remaining owners; useful Markdown authoring guidance is available through writing-pack.                                                                                                                         |
| 11   | Distribution and adoption closure                     | Isolated packaged-plugin adoption, immutable old-pin resolution, mixed standard selection, generated parity, Windows hook and Linux CI equivalence, and migration documentation have evidence.                                                                                 |

## Boundaries

- The selected set is `root-agent-router`, `runbook-composition`, `playbook-composition`, `tracked-validation-hook`, `review-entrypoint`, `contribution-entrypoint`, `completed-artifact-custody`, and `unslop`.
- Do not select `repo-plugin-subscriptions`: README identifies `.agents/plugins/marketplace.json` as the catalog this repository publishes, and explicitly says the checkout declares no skill subscriptions. A published catalog is not this repository installing plugins for its own use.
- Keep `marketplace-registry` repository-owned. Do not add `command-bus` or `agent-doctrine-contracts` subscriptions merely because the repository has related files or capabilities.
- The `repo-plugin-subscriptions` pledge concerns this repository's `.agents/plugins/` declarations and harness bindings. Do not restore a Marketplace source submodule requirement. `.agents/skills/` is reserved for repository-authored skills.
- Subscription identity records the immutable definition source and certification reference. Do not retain command vectors or generated paths as universal subscription data.
- Certification must report observed state. Do not label a standard certified until its requirements, implementation, evidence, and drift controls have been assessed.
- Preserve the current Windows hook and hosted Linux checks throughout migration. Do not delete a checker solely because it is Marketplace-deployed; map its live invariant to a repository-owned check or semantic certification first.
- Inspect the repository's actual gitlink ownership before removing any submodule. Do not modify other repositories.
- Generated plugin output remains downstream of canonical source. The final plan owns isolated package and cross-platform closure evidence.

## Current evidence and implementation baseline

- Plan 6 is closed at `3d59506db` on `codex/open-runbook-playbook-composition`; the worktree was clean before this roadmap was authored.
- `.agents/contracts/operating-standards.json` is v1 and embeds origin, implementation roots, command vectors, generated paths, and dependency details. It currently selects Markdown formatting and root gitignore hygiene in addition to retained standards.
- `tools/run.py` requires every Marketplace deployment to match `.agents/standards/provenance.json` byte-for-byte before running the legacy generic checker.
- `.agents/standards/_runtime/repo_standards.py` combines generic surface scaffolding, standard-specific dispatch, and runbook/playbook structural checks. Its dependants include tracked hooks and helper scripts, so removal must be reference-driven.
- `.agents/contracts/repo-standards-commands.json` is a repo-specific hook binding. The spec allows retaining or replacing it according to the actual hook; it is not a universal standard subscription field.
- The current Markdown formatter owns requirements, hook commands, generated exclusions, scripts, and a vendored wheel. `tools/new_plugin.py` and `tools/sync_skill_shared_references.py` have live formatter references that must be resolved before removal.
- No `.gitmodules` file exists in this worktree at the baseline, so there is no repository source submodule to remove in this migration. This observation does not authorize changes to another checkout.

## Handoff

Write Plan 8 just in time against `3d59506db`, then execute it inline. Re-plan only if live source inspection shows a meaningful boundary different from the sequence above. Plans 9-11 remain unwritten until their preceding deliverables are reviewed and closed.
