# Playbook And Runbook Doctrine

This repo uses two reusable workflow doc types:

- `playbook`: higher-level scenario guidance. Use it when an agent needs to
  decide which workflow to run, which branch to take, or which follow-on
  surface to consult.
- `runbook`: a deterministic procedure. Use it when the agent can follow a
  fixed ordered sequence with known entrypoint, validation, and recovery.

These docs are agent-facing guidance, not source custody.

## Canonical homes

- `.agents/playbooks/` for scenario routing, decision trees, and workflow
  coordination.
- `.agents/runbooks/` for concrete operational procedures.

## How to use them

- Keep the executable step sequence in scripts or checked-in tooling.
- Keep the doc concise and action-oriented.
- Put branching logic in playbooks.
- Put the exact command sequence and validation in runbooks.
- If a workflow changes often, keep the runbook short and defer the volatile
  command details to the script entrypoint.

## When to write or update one

- Use a playbook when a workflow has multiple valid paths or depends on
  scenario selection.
- Use a runbook when the task should be repeatable from a single entrypoint
  without guesswork.
- If an adapter or projection can go stale, say so in the runbook and block
  regen until the adapter is updated.

## Pattern references

Read these when you are creating or revising playbooks or runbooks:

- Microsoft Sentinel playbooks:
  https://learn.microsoft.com/en-us/azure/sentinel/automation/create-playbooks
- Azure Automation runbooks:
  https://learn.microsoft.com/en-us/azure/automation/automation-runbook-types
- Azure SRE Agent incident response plans:
  https://learn.microsoft.com/en-us/azure/sre-agent/incident-response-plans
- OpenAI Codex guidance on `AGENTS.md` and skills:
  https://developers.openai.com/codex/codex-manual.md

## Repo integration

- Keep the authoritative repo-specific behavior in `AGENTS.md` and the
  executable scripts.
- Use the playbook or runbook doc for the human- and agent-readable procedure.
- Use `.agents/INDEX.md` to discover the available guidance surfaces.
