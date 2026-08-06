# `asking-clarifying-questions` design

## Problem

Asking clarifying questions is currently embedded in `brainstorming`
(design-time questions) and `risk-gates` / `ambiguity-gate` (pre-action
gating). Agents have no standalone, any-time skill for the single ambiguity
that appears mid-plan, mid-execution, or inside another skill and can be
resolved by one human answer.

Without a dedicated skill, agents either guess, over-ask, or inappropriately
invoke a full design session or risk gate for a reversible decision.

## Scope

Add a first-party marketplace skill `asking-clarifying-questions` under
`sources/first_party/skills/asking-clarifying-questions/`. It will be
projected into the `house-skills` mega-pack and, optionally, the
`repo-worker-pack`. The design covers the canonical source files
(`SKILL.md`, `agents/openai.yaml`) and the testing approach.

This change does not modify `brainstorming`, `risk-gates`, `writing-plans`,
`executing-plans`, or `handoff-gates`. It adds composition metadata so those
skills can route to `asking-clarifying-questions` when a single human decision
is the lawful next step.

## Goals

1. Provide a discoverable, any-time skill for single, reversible clarifying
   questions.
2. Reuse the compact `ambiguity-gate` / `risk-gates` interactive queue:
   ambiguity, risk of guessing, recommendation, decision needed.
3. Distinguish clearly from `brainstorming` (design/spec) and `risk-gates`
   (pre-action gate / block).
4. Include composition metadata so agents know when to invoke it from
   `writing-plans`, `executing-plans`, `handoff-gates`, and other mid-flight
   surfaces.
5. Observe the first-party skill source format and
   `.agents/doctrine/skill-standards-policy.md` frontmatter and body rules.
6. Make the skill testable with subagent pressure scenarios.

## Non-goals

- Replacing `brainstorming` or `risk-gates`.
- Handling multi-question design conversations.
- Automatically deciding when to ask; the skill provides the pattern and
  boundaries.
- Source-grounded authority records (no external source to custody).
- Changing marketplace projection tooling beyond adding the skill to the pack
  registry.

## Existing guidance inventory

| Surface | Responsibility | Disposition |
|---|---|---|
| `brainstorming` | Design/spec-time clarifying questions | Retain; `asking-clarifying-questions` is not a substitute |
| `risk-gates` / `ambiguity-gate` | Pre-action risk classification and queue contract | Retain; this skill applies to the `interactive`/`amber` outcome and any-time mid-flight ambiguity |
| `writing-plans` / `executing-plans` | Plan and execution workflows that may hit a clarifying question | Add `asking-clarifying-questions` to `related_skills` / `use_instead` metadata, not a workflow rewrite |
| `handoff-gates` | Stage-boundary readiness | Add `asking-clarifying-questions` to `related_skills`; can be invoked if a handoff surfaces a single unresolved ambiguity |

## Design decisions

### 1. First-party, original lane

`asking-clarifying-questions` is an independently authored technique, not a
source-grounded skill, so it uses the `first_party` lane. No
`assets/authority/` is needed. It is MIT-licensed first-party source.

Implementation will scaffold the canonical source with:

```text
py -3 .agents/skills/mark-skill-authoring/scripts/new_skill.py \
  --name asking-clarifying-questions \
  --custody marketplace \
  --lane first_party
```

### 2. Active-verb name

The skill name is `asking-clarifying-questions` (kebab-case, active gerund,
verb-first), matching the naming convention in `writing-skills` and keeping the
action prominent. `clarifying-ambiguity` was considered but reads more like a
state than an action.

### 3. Queue contract from `risk-gates`

The skill reuses the compact interactive queue from `ambiguity-gate` and
`risk-gates`:

- what is unclear;
- risk of guessing;
- recommendation;
- decision needed.

This keeps it compatible with `risk-gates` and avoids inventing a new
interaction pattern.

### 4. Boundaries are the primary content

The skill's main value is in what **not** to ask:

- Do not ask when the answer is forced by durable source or policy.
- Do not ask when a full design/spec is needed; use `brainstorming`.
- Do not ask when scope, authority, source truth, canon, safety, or
  irreversible mutation is at stake; use `risk-gates` and accept a block if
  needed.
- Do ask only when the ambiguity is material, internally unresolved, and a
  single human answer unblocks the next action.

### 5. Any-time composition

`related_skills` will list `brainstorming`, `risk-gates`, `writing-plans`,
`executing-plans`, and `handoff-gates`. `use_instead` will list
`brainstorming` and `risk-gates` to signal that this skill is broadly
triggered by ambiguity but those skills handle the design and risky cases.
The skill does not own their workflows; it is a safe off-ramp for the
`interactive`/`amber` case and for mid-flight single questions.

### 6. House-skills mega-pack

As a general portable technique it belongs in `house-skills`. It may also be
bundled in `repo-worker-pack` because repo workers frequently hit scope and
authority ambiguities during plan execution. The
`codex-marketplace/custody-pack-registry.json` entries will be updated during
implementation. The projection files under `codex-marketplace/plugins/` are
generated by `tools/rebuild_marketplace.py` and must not be edited directly.

### 7. Body under 500 words

`SKILL.md` body will be concise; long rationale stays in this design spec.
`references/` is optional and can be added later if operational examples grow.

## Proposed skill contents

```text
sources/first_party/skills/asking-clarifying-questions/
├── SKILL.md
├── agents
│   └── openai.yaml
└── references
    └── .gitkeep
```

The `references/.gitkeep` is created by the `first_party` scaffold and
reserved for future supporting references.

### `SKILL.md` (proposed)

```yaml
---
name: asking-clarifying-questions
description: Use when an ambiguity remains after safe internal resolution and a single human answer would unblock the next action, without needing a full design session or a pre-action risk gate.
metadata:
  source-id: asking-clarifying-questions
  source-path: sources/first_party/skills/asking-clarifying-questions/SKILL.md
  provenance-name: Asking Clarifying Questions first-party skill
  source-category: first_party
  status: active
  owner: Harley Bartles
  scope: mid-flight ambiguity resolution through a single clarifying question
  use_when:
  - Use when an ambiguity is internally unresolved and a single human decision would unblock the immediate next step.
  - Use when the agent is mid-plan, mid-execution, or inside another skill and a missing fact, term, scope, boundary, or output shape prevents safe progress.
  - Use when the answer is a concrete decision, not a design.
  do_not_use_when:
  - Do not use when the ambiguity needs a full spec or design; use brainstorming.
  - Do not use when the next action could violate scope, authority, source truth, canon, safety, or involve irreversible mutation; use risk-gates.
  - Do not use when the answer is already forced by durable source, policy, or a safe default; resolve internally.
  use_instead:
  - brainstorming
  - risk-gates
  related_skills:
  - brainstorming
  - risk-gates
  - writing-plans
  - executing-plans
  - handoff-gates
license: MIT
---

# Asking Clarifying Questions

Ask one narrow, human-answerable question when a single unresolved ambiguity
blocks the immediate next step.

## Core pattern

1. State the immediate next action that depends on the answer.
2. State the ambiguity concisely (one missing fact, term, scope, boundary, or
   output shape).
3. State the risk of guessing.
4. Give a concrete recommendation and the available options.
5. Ask one question.
6. Record the answer and continue.

## When to use

- Internal resolution is exhausted (rules, source truth, non-goals, safe
  defaults).
- A single missing decision separates the agent from the next action.
- The cost of guessing is wasted motion or reversible rework, not a canon or
  authority mistake.

## When not to use

- The ambiguity needs a full design or spec: use `brainstorming`.
- The ambiguity affects scope, authority, source truth, canon, safety, or
  irreversible mutation: use `risk-gates` and accept a block if needed.
- The answer is already forced or harmless: resolve internally and do not ask.

## Common mistakes

- Asking a vague question instead of a single decision.
- Asking when the answer is already in durable source or policy.
- Treating a clarifying question as a substitute for a missing design or risk
  gate.
- Asking multiple questions in one turn.

## Relation to other skills

- `brainstorming` asks many questions to shape a design.
- `risk-gates` decides whether to proceed, repair, or block when hidden risk is
  present.
- `asking-clarifying-questions` handles the `interactive`/`amber` outcome where
  a single human answer is the lawful next step.
```

### `agents/openai.yaml` (proposed)

```yaml
version: 1
metadata:
  skill_name: asking-clarifying-questions
  source_category: first_party

interface:
  display_name: Asking Clarifying Questions
  short_description: Use when an ambiguity remains after safe internal resolution and a single human answer would unblock the next action, without needing a full design session or a pre-action risk gate.
  default_prompt: Use /asking-clarifying-questions when an ambiguity is internally unresolved and a single human decision would unblock the immediate next step. State the next action, the ambiguity, the risk of guessing, a recommendation with options, and ask one concrete question. Do not use when the ambiguity needs a full design or spec (use brainstorming), when it could violate scope/authority/source/canon/safety/irreversible mutation (use risk-gates), or when the answer is already forced by durable source or policy.
policy:
  products:
  - chatgpt
  - codex
  - api
  - atlas
  allow_implicit_invocation: true
```

## Validation

- **Spec-readiness**: this design will be scored by `handoff-gates`
  spec-readiness lane before planning.
- **Plan validation**: the implementation plan will include subagent pressure
  scenarios:
  - an agent with a reversible single ambiguity asks one question with the
    compact queue;
  - an agent with a canon/authority ambiguity escalates to `risk-gates`
    instead of asking;
  - an agent with a design ambiguity escalates to `brainstorming`;
  - an agent with a forced answer resolves internally and asks nothing.
- **Marketplace validation**: after implementation,
  `py -3 tools/rebuild_marketplace.py` and `bash scripts/ci-preflight.sh --check`
  must pass.
- **Skill body**: `SKILL.md` body will be under 500 words and include all
  required frontmatter fields per `.agents/doctrine/skill-standards-policy.md`.
