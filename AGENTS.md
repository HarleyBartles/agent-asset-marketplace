# AGENTS.md

## Repository purpose

Use [README.md](README.md) for repository orientation and shared project facts.

## Source-of-truth split

Follow [marketplace worker doctrine](.agents/doctrine/marketplace-worker-doctrine.md) for authority, evidence, and publication boundaries.

## Build and test commands

Use the [testing playbook](.agents/playbooks/testing.md) and [tracked hook contract](.agents/contracts/repo-standards-commands.json).

## Routing pointers

- For source authority, read [marketplace worker doctrine](.agents/doctrine/marketplace-worker-doctrine.md); for marketplace sources and deployable standards, read [custody doctrine](.agents/doctrine/custody-and-marketplace-doctrine.md) and [skill standards policy](.agents/doctrine/skill-standards-policy.md).
- For testing, style, review, publication, and security, use the [test policy](.agents/contracts/skill-tests.md), [code style](.agents/playbooks/code-style.md), [review runbook](.agents/runbooks/code-review.md), [PR runbook](.agents/runbooks/pr.md), and [security playbook](.agents/playbooks/security.md).
- For contribution entry, read [CONTRIBUTING.md](CONTRIBUTING.md); for document and scratch placement, follow [documentation doctrine](.agents/doctrine/docs.md), [artifact custody](.agents/doctrine/completed-artifacts.md), and [worktree/scratch doctrine](.agents/doctrine/non-repo-locations-policy.md).
- For scoped docs, runbooks, or playbooks, read the applicable `AGENTS.md` router; Devin's PR trigger is in [.devin/rules/pr.md](.devin/rules/pr.md).

## Maintenance responsibility

Keep this file as a pointer layer; update the owning doctrine, contract, runbook, or playbook when its policy changes.
