---
name: boring-buster
description: 'judge exactly one issue or issue-shaped proposal for boring implementation readiness. use when work is being made ready, too interesting, blocked, red/amber/green, or worker-send-ready; for Linear worker coding issues, require the Linear Worker Issue Shaping Stack with worker-dispatch-linear and writing-plans before any worker-ready GREEN.'
---

# Boring Buster

Use this skill to assess exactly one issue or issue-shaped proposal for predictable implementation readiness. It decides whether the target is boring enough for its selected lane; it does not create issues, delegate workers, verify GitHub, run validation, package skills, or emit worker packets unless the latest user turn separately authorizes that downstream action.

## Core posture after Linear/Codex adoption

Boring is lane-relative. The same proposal can be boring for discussion, not boring for Codex, and boring for later Linear pickup after a Receipt repair.

Normal coding implementation routes through the Linear worker control plane. A boring result for a coding issue means the work is predictable enough for the chosen Linear/worker lane; it does not itself delegate a worker, create a PR, or prove GitHub state.

GPT-native skillwork is not automatically a worker task. If the editable target is an installed ChatGPT skill, use the skill stack here: `skill-creator`, then `skill-validator`, then `skill-packager`, then `skill-handoff` when queue or handoff cadence matters. A repo worker becomes lawful only when the editable skill source is known to live in a worker-accessible repo and the task is explicitly repo-backed.

Legacy chat/YAML dispatch is Plan B only. A target that needs old-style worker packet proof should first pass the Linear worker golden gate as unavailable, unsuitable, or explicitly rejected.

## Linear Worker Issue Shaping Stack

When the target is a Linear issue intended to be worker-send-ready for repo or code execution, compose in this order:

```text
worker-dispatch-linear -> boring-buster -> writing-plans -> worker-dispatch-linear
```

Use `worker-dispatch-linear` for the durable Linear surface, issue state, assignment, label, return evidence, and event-log convention.

Use this skill to decide whether the issue is actually boring enough for the selected lane.

Use `writing-plans` before any worker-ready GREEN to check that the issue gives the next engineer enough implementation shape: one observable goal, likely edit surfaces or exact source seams, small executable steps or intended route, validation commands, no placeholders, and no hidden replanning requirement.

Return to `worker-dispatch-linear` for any authorized Linear write/update after the boring and plan-shape gates are satisfied.

Do not require the full stack for parent trackers, product notes, research/discovery issues, or planning-only issues unless Harley asks to make them worker-send-ready.

## Read before formal runs

Read `references/boring-contract.md` before any formal GREEN/RED/AMBER/BLOCKED run.

Read `references/agent-crew-gates.md` when route, authority, worker suitability, source topology, durable pickup, artifact shape, cleanup/recovery, or in-flight surprise could change whether the target is boring.

For casual shaping, use this entrypoint only. Do not load references unless the user asks for a formal classification or a route/authority gate is material.

## Boring-enough lanes

Choose the lane before judging:

- `right_now`: current actor can complete the work in-session without hidden missing decisions, source gaps, or validation/closeout surprises.
- `linear_worker_next`: a Linear issue can be delegated to a future worker after the golden gate proves the task is repo-executable, environment/setup expectations are adequate, and return evidence can be read from Linear/GitHub.
- `gpt_native_skillwork`: the work should be done through the native skill stack, not a repo worker, unless a repo source target is proven.
- `next_actor`: a later actor can pick up from durable context alone.
- `proposal`: the idea is shaped enough to preserve, but not implementation-authorized.
- `legacy_plan_b`: non-Linear worker handoff is appropriate because Linear/default worker flow is unavailable, unsuitable, or explicitly rejected.

## Gate stack

A boring target needs:

1. One owning issue/proposal and one observable goal.
2. Clear scope, source basis, authority, and closeout condition.
3. No implementation-changing ambiguity.
4. No source-truth, mutation, provenance, safety, publication, validation, or project-law invariant break.
5. Settled architecture seams, or explicit deferral outside the lane.
6. Known validation ladder and issue-goal proof.
7. Route suitability: Linear worker route for normal coding, skill stack for GPT-native skills, GitHub proof only after a GitHub artifact exists, legacy dispatch only as Plan B.
8. Interest extraction: interesting material split, resolved, or deliberately deferred.
9. For Linear worker coding issues, writing-plans gate satisfied before worker-ready GREEN.
10. Golden-gate falsification after local gates appear green.

## Golden gate for route suitability

Before any GREEN that implies implementation readiness, ask:

- What is the editable target?
- Can the chosen actor actually access and change it?
- Where will durable evidence return: Linear, GitHub, package artifact, repo commit, or another source?
- Is this coding implementation, GPT-native skillwork, repo-backed skill source, research, connector/UI setup, side discovery, or planning?
- Is the normal Linear worker route available and suitable?
- Would the result still be boring to use, validate, recover, and verify after the worker returns?
- For Linear worker coding issues, did `writing-plans` prove the issue is executable without guessing?

A route that only looks executable is not boring. The regression to catch is treating every interesting work item as worker-executable without proving the editable target, worker environment, and implementation-plan shape.

## Active repair posture

Repair greenable gates before returning a blocker when the repair is deterministic, lawful, local to the selected lane, and authorized by the current task.

Examples:

- Fetch an available issue or source before blocking on unknown state.
- Write missing context to the correct Linear issue when durable pickup is the only blocker and authority exists.
- Split a too-interesting idea into one boring implementation issue plus parked discovery work.
- Downgrade an implementation route to proposal when authority is absent.
- Change a worker task into GPT-native skillwork when the editable target is not repo-backed.
- Invoke `writing-plans` and repair the issue shape when a Linear worker issue is otherwise green but still underdetermined for implementation.

Do not invent source facts, choose product policy, broaden scope, mutate durable state without authority, or let a validation command substitute for issue-goal proof.

## Output posture

For casual discussion, answer in prose.

For formal runs, include: target, lane, result, terminal state, decisive gate, terminal reason, next move, and preserved context. Use a small markdown table or prose. Do not default to YAML in workspaces where YAML is reserved for dispatches or session busters unless the user explicitly requests YAML.

Terminal states: `GREEN`, `RED`, `AMBER_UNRESOLVED`, `BLOCKED`.

`AMBER_UNRESOLVED` is not success. Preserve context and name the missing decision, source, authority, or route proof.

## Composition and read discipline

Use the smallest controlling skill set. For Linear worker-send-ready coding issues, the smallest controlling set normally includes `worker-dispatch-linear`, this skill, and `writing-plans`.

Do not load adjacent skills merely because they sound related. Stop when this skill owns the readiness decision or when a named unresolved decision belongs to a more specific already-known skill.

Project wrappers add domain constraints only. They should not redefine GPT-wide dispatch after Linear worker adoption.
