## Scope

Document custody and placement across root `docs/`, `.agents/docs/`, active planning homes, and external scratch.

## Placement rules

- `docs/` is the durable record of repository truth needed by maintainers, contributors, or users: accepted decisions, architecture and interface contracts, and current repository or product behavior. A page there must remain accurate and have one clear canonical owner.
- `.agents/docs/` is for durable, agent-facing reference that remains useful across tasks. It may explain how an agent works with this repository, but it does not establish policy that belongs in doctrine, runbooks, playbooks, or contracts, and it must not duplicate those authorities.
- Branch and task scratch under `../_agent-scratch/<repo-name>/<branch>/<plan-basename>/` is for transient work: investigation and audit snapshots, release notes and handoff text, drafts, review packets, and generated working evidence. Scratch is not linked as repository authority and has no retention promise.
- Active plans, approved specifications, and governed checkpoints use their declared `.agents/plans/`, `.agents/specs/`, or roadmap homes and follow the planning-artifact lifecycle. They do not move to either docs tree to avoid retirement.
- Repeated operating rules belong in `.agents/doctrine/`, `.agents/runbooks/`, `.agents/playbooks/`, or `.agents/contracts/`, according to the owning surface. Keep one canonical rule and link to it from docs where useful.

Before creating a tracked document, decide its audience, expected lifetime, and canonical owner. If it records one task's findings or a release's specific revision, put it in scratch. If it states current repository truth for people working on the repository, use `docs/`; if it is stable guidance specifically for agents, use `.agents/docs/`. Split mixed documents when their parts have different lifetimes or owners.

## README and AGENTS overlap

`README.md` is human-facing repository orientation; agents can use it for the same overview without copying it into always-on instructions. When an `AGENTS.md` needs information already stated in the README, link to the README instead of repeating that information. Keep agent-specific routing or instructions that the README does not provide, and route operative policy to its canonical doctrine, contract, runbook, or playbook.

## Review guidelines

- Reject transient reports and dated handoffs from both docs trees, even when they are useful in the current task.
- Reject a document from either tree when its only purpose is to restate an existing canonical policy or source file.
- Keep `.agents/docs/` guidance-oriented, not operative source custody.
- Flag stale cross-references when a canonical document moves or retires.

## Maintenance responsibility

This file is the canonical placement policy. Root and scoped `AGENTS.md` files route contributors to it; scoped pointer files contain only a scope-qualified sentence and links to the applicable doctrine.
