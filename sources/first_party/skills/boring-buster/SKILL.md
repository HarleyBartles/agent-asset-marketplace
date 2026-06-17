---
name: boring-buster
description: Use this skill before planning, dispatching, or implementing work when success depends on the work being small, dull, explicit, falsifiable, and ready for ordinary execution.
metadata:
  source-id: boring-buster
  source-path: sources/first_party/skills/boring-buster/SKILL.md
  provenance-name: MARK-19 core generic buster House Skills source slice
license: "MIT"
---
# Boring Buster

Use this skill before planning, dispatching, or implementing work when success depends on the work being small, dull, explicit, falsifiable, and ready for ordinary execution.

Boring is a quality gate. It is not an aesthetic preference. Boring work has bounded inputs, clear mutation surfaces, observable success, known validation, and an uninteresting path to completion.

## Owned decision

Given a proposed issue, plan, worker job, PR slice, or implementation route, return:

- `green` â€” boring enough to execute in the intended lane.
- `amber` â€” close, but needs a named repair before execution.
- `red` â€” too broad, clever, hidden, authority-confused, or unfalsifiable to execute safely.
- `blocked` â€” required source, authority, environment, or dependency is missing.

## Boring contract

A boring work packet or plan should have:

- one clear goal;
- explicit non-goals;
- durable source inputs;
- a known target surface;
- a bounded mutation boundary;
- an observable success condition;
- an explicit validation/proof route;
- small enough scope for the lane;
- no hidden chat-only context required to pass;
- no route where a good report can substitute for the requested artifact or change.

## Risk checks

Check for pressures that make work interesting in the bad way:

- vague verbs such as fix, clean up, improve, normalize, align, harden, or make better without a target and success condition;
- multiple unrelated goals in one packet;
- missing source material or stale source authority;
- protected surfaces hidden inside ordinary-sounding work;
- too many files, domains, repositories, issues, or artifact classes;
- unclear validation or proof;
- dependency on manual judgment not captured in acceptance criteria;
- branch/PR, publication, or closure expectations that do not match the current workflow;
- report-only routes where execution was requested;
- scope creep disguised as opportunistic cleanup.

## Workflow

1. Identify the intended execution lane: GPT-local, Codex/worker, PR/code, metadata-only, documentation-only, source import, validation, or other lane.
2. Compare the proposed work against the boring contract.
3. Repair internally when there is one obvious narrowing or explicit non-goal to add.
4. Split or block work that combines unrelated goals or needs unavailable source.
5. Return the smallest safe packet and the proof route.

## Green requirements

Before green, the next executor should be able to answer:

- What exactly do I change or produce?
- What must I not touch?
- Where is the source truth?
- How do I know I am done?
- What command, artifact, review, or evidence proves the result?
- Where do I return the result?

If any answer is missing and material, the result is amber or blocked.

## Relationship to worker readiness

`boring-buster-v1` judges whether the work itself is boring enough for a lane. Worker-readiness preparation judges whether the handoff packet is executable and falsifiable for a worker. A boring idea can still have an unready worker packet.

## Boundaries

Do not make work boring by deleting essential acceptance criteria, source evidence, validation, authority, or user intent. Do not treat low effort as boring when the outcome is not falsifiable.
