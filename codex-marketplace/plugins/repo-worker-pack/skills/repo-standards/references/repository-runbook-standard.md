# Repository Runbook and Playbook Standard

This is the portable standard for repository lifecycle routing and conditional topical composition.

## Artifact taxonomy

| Question | Owning surface |
| --- | --- |
| What must remain true? | doctrine (`.agents/doctrine/`) |
| What exact shape must participants exchange? | contract (`.agents/contracts/`) |
| How do I perform one focused judgment or action? | capability skill |
| How does this repository execute a lifecycle stage? | runbook (`.agents/runbooks/`) |
| How does this repository handle a conditional concern? | playbook (`.agents/playbooks/`) |
| Can a machine enforce it cheaply? | code or configuration |

Runbooks and playbooks are different artifacts, not interchangeable names.

## Runbooks

A runbook owns one repository lifecycle stage. It is entered through its stage/workflow skill and is the local composition root for that stage. The standard stage set is `design.md`, `planning.md`, `implementing.md`, `code-review.md`, and `pr.md`.

Every runbook contains these exact second-level sections:

- `When`
- `Required skills`
- `Composition`
- `Doctrine and contracts`
- `Local commands and paths`
- `Evidence contract`
- `Prohibited combinations`
- `Playbook routing`

`Playbook routing` links each applicable `.agents/playbooks/*.md` file and states the condition that activates it. Use `none` only when the stage has no topical composition.

## Playbooks

A playbook owns a conditional class of work or concern selected by one or more runbooks. Common playbooks include `code-style.md`, `testing.md`, `security.md`, `skill-authoring.md`, `marketplace-generation.md`, and `completing-plans.md`.

Every playbook contains the same seven common composition sections as a runbook, followed by `Invoked by`. `Invoked by` links every stage runbook that may select it.

Playbooks name and sequence capability skills, doctrine, contracts, commands, and evidence. Durable architecture and policy belong in doctrine; reusable language or framework technique belongs in capability skills. A playbook binds those owners to repository-specific triggers and proof.

## Dependency direction

The only orchestration direction is:

```text
using-superpowers-plus -> stage skill -> runbook -> playbook -> doctrine/contracts/capability skills
```

- Runbooks may select playbooks.
- Playbooks must declare reciprocal runbook parents but must not orchestrate a lifecycle stage.
- Playbooks must not invoke runbooks or other playbooks.
- Doctrine and contracts never orchestrate.
- Capability skills must not sequence a repository lifecycle.
- Cycles are invalid.

Every declared playbook must be reachable from at least one runbook. References must resolve and reciprocal runbook/playbook declarations must agree.

## Local policy

Each consumer keeps `.agents/doctrine/repo-runbook-policy.md` with separate `Standard runbooks` and `Standard playbooks` tables. The tables map standard names to local paths, state required/optional status, and record explicit exceptions.

## Workflow order

The canonical lifecycle is `design -> planning -> implementing -> review -> pull request`. `using-superpowers-plus` selects the hygiene and stage owner. The stage owner reads its baseline and matching runbook. The runbook selects every applicable playbook before work proceeds.

## Migration

Repositories adopting this version move lifecycle roots to `.agents/runbooks/` and conditional topical compositions to `.agents/playbooks/`. A topical file left in the runbook mapping is structural drift; a playbook present but unreachable from a runbook is also drift.
