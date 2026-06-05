# Worker Readiness Prep v1

Use this skill to prepare and gate executable worker handoffs before they enter a worker lane. It replaces old broad `dispatch-prep` habits and owns the folded `worker-readiness-gate` behavior.

This skill prepares the handoff and lane choice. It does not own the actual Linear send/control-plane mechanics after readiness passes; use `worker-dispatch-linear-v1` for Linear-based Codex delegation, worker status, PR-gate handling, PR iteration, and merge-readiness routing.

## Core purpose

Make a proposed worker job executable and falsifiable without rediscovery, scope drift, hidden chat-only context, fake GREEN, or a report-only return.

Given a proposed worker task/packet and intended worker lane, return one of:

- `ready`: the worker can execute the task and success can be observed.
- `repair_required`: the job is probably executable after specific shaping repairs.
- `blocked`: the job should not enter a worker lane because the target, authority, surface, or proof route is unavailable or wrong.

## Handoff preference lanes

Prefer lanes in this order:

1. Linear/Codex handoff for coding/repo work. Durable work lives in Linear, Codex receives the executable task through the lawful Linear/Codex route, and the worker produces a branch/PR work packet.
2. Linear durable handoff plus small dispatch when a worker needs a copy/paste nudge, but the real brief remains in Linear. The small dispatch points to the durable handoff and states the immediate execution task.
3. Full copy-paste worker dispatch only when no durable/control-plane route is available. This is an explicit fallback, not the normal coding workflow.

Do not revive chat-YAML dispatch as the normal coding workflow. YAML/copy-paste dispatch is a last fallback lane inside readiness/dispatch taxonomy, not a first-class default.

## PR-shaped work packet rule

For repo/code work, PRs are the normal worker work packet. Workers use a branch, raise or enable a PR through the lawful route, and the PR branch is where review and iteration happen until ready to merge.

A repo worker job should state:

- branch/PR expectations when relevant;
- observable success criteria;
- validation/proof route;
- return evidence requirements;
- protected surfaces and mutation boundaries;
- whether the human PR gate is expected.

Do not frame normal proof as direct mutation on `main` before merge. Main is landed source truth after merge; the PR branch and PR evidence are the normal pre-merge proof surface.

## Readiness shaping checklist

Before gating, shape the handoff so a worker can read it and know:

- target project, repo, issue, branch, artifact, or implementation surface;
- exact goal as observable state;
- in-scope changes;
- out-of-scope and protected surfaces;
- required source inputs and where to find them;
- mutation boundary and ownership;
- expected validation commands or acceptable validation evidence;
- return evidence and final summary contract;
- success criteria and failure criteria;
- lane constraints such as `cloud-codex-ok`, `local-codex-required`, `planning-only`, or `native-gpt-route`.

For Linear issue shaping, ordinary Markdown is sufficient. Use headings such as Problem, Goal, Scope, Guardrails, Validation, Return evidence, and Success criteria only when they clarify execution. Boring means executable, not verbose.

## Internal readiness gate

A proposed worker job is `ready` only when all checks pass:

- the worker can execute the task in its environment;
- required source inputs are accessible to the worker;
- target project/repo/issue/artifact is unambiguous;
- mutation boundary is explicit;
- success condition is observable;
- validation/proof route is specified;
- return contract asks for evidence, not vibes;
- the job is small and boring enough for the lane;
- the packet does not require hidden chat-only context;
- the worker cannot pass by writing a good report instead of producing the requested artifact/change;
- protected, retired, or wrong-surface routes are not smuggled into the packet;
- any required human gate is explicit.

If any check fails, do not delegate yet. Return `repair_required` with the smallest concrete repairs, or `blocked` when the surface, authority, or lane is wrong.

## Gate result language

Use this compact result shape in prose or Markdown:

- `ready`: name the lane and the evidence route.
- `repair_required`: list the missing fields or ambiguity to repair before dispatch.
- `blocked`: name the blocker and the next lawful route.

Useful blocker categories:

- `native_route`: GPT-native skill, connector, UI, research, or planning work rather than repo worker work.
- `unavailable_surface`: the worker cannot access/edit/publish the target.
- `hidden_context`: the job depends on chat-only context not embedded in the durable handoff.
- `scope_too_large`: the work is not small/boring enough for the intended lane.
- `fake_green_risk`: the worker could satisfy the words by reporting rather than producing falsifiable change/evidence.
- `retired_route`: the packet attempts to revive a protected or retired workflow.

## Linear/Codex-specific prep

For Linear/Codex coding work, make the Linear issue the durable task contract. Linear comments and attachments are the worker event log. The issue must identify the repo or implementation surface clearly enough for Codex Cloud to clone, edit, validate, and publish as a PR.

Delegate to Codex only after readiness is `ready` and the latest user turn authorizes execution or dispatch. If readiness passes, route actual dispatch mechanics to `worker-dispatch-linear-v1`.

When PR publication should use the Codex UI, include human-gate wording such as:

`When implementation is complete, return evidence in Linear. If the Codex UI offers Create PR, Harley will use that human gate; do not require shell GitHub credentials or PAT-based publication.`

## Relationship to boring checks

A boring-work buster may judge whether the work itself is small and boring enough for a lane. This skill judges whether the worker packet/job is executable and falsifiable for that lane.

Do not use readiness prep to reopen broad product strategy, architecture, or doctrine debates. If the job is not yet a worker job, route it to planning or doctrine first.

## Stop rule

Once the handoff has been shaped and the gate result is returned, stop. Do not create dispatches, delegate Codex, merge PRs, or close issues from this skill alone. Use the narrow control-plane skill that owns the next action.
