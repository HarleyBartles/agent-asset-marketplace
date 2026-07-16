---
name: analogy-buster
description: Use when use this skill before relying on an analogy, metaphor, comparison,
  role model, frame, or project-specific shorthand to answer, plan, dispatch, or make
  a durable decision.
metadata:
  source-id: analogy-buster
  source-path: sources/first_party/skills/analogy-buster/SKILL.md
  provenance-name: Analogy Buster first-party skill
  source-category: first_party
  status: active
  owner: Harley Bartles
  scope: Use when use this skill before relying on an analogy, metaphor, comparison,
    role model, frame, or project-specific shorthand to answer, plan, dispatch, or
    make a durable decision.
  use_when:
  - Use when use this skill before relying on an analogy, metaphor, comparison, role
    model, frame, or project-specific shorthand to answer, plan, dispatch, or make
    a durable decision.
  do_not_use_when:
  - Do not use when another more specific skill owns this task.
license: MIT
---
# Analogy Buster

Use this skill before relying on an analogy, metaphor, comparison, role model, frame, or project-specific shorthand to answer, plan, dispatch, or make a durable decision.

Analogies are useful when they clarify a limited relationship. They are dangerous when they become proof, authority, canon, literal mechanics, or a total explanation.

## Owned decision

Given an analogy and the work it is about to support, return one of the buster-framework-v1 outcomes:

- `green` â€” the analogy clarifies the specific question within stated limits, or is unnecessary and can be safely discarded.
- `amber` â€” the analogy may help, but limits, source basis, or decision authority need clarification.
- `red` â€” the analogy is distorting the work or being used as evidence, canon, or authority.
- `blocked` â€” the source needed to judge the analogy is unavailable.

## Analogy tests

Check whether the analogy:

- clarifies the current question rather than decorating the answer;
- maps the right relationship, not incidental surface details;
- has stated limits;
- preserves the actual source hierarchy;
- does not replace evidence, canon, user direction, validation, or domain expertise;
- does not smuggle in assumptions from the source domain;
- does not overfit a single example into a rule;
- does not hide an unresolved decision behind familiar language.

## Workflow

1. Name the analogy and the decision or explanation it is being used to support.
2. Identify what the analogy clarifies.
3. Identify what the analogy does not prove.
4. Check for distortion, overreach, or source/authority laundering.
5. Keep, limit, revise, or drop the analogy.
6. If the work needs proof, route to the actual source or validation surface.

## Common red flags

- The analogy is doing the work of evidence.
- The analogy turns a project shorthand into a binding rule without source support.
- The analogy imports mechanics, permissions, hierarchy, or constraints from the comparison domain.
- The analogy makes a contested or ambiguous point feel settled.
- The analogy becomes more elaborate than the work it was meant to clarify.

## Output posture

When visible, state:

- the analogy;
- what holds;
- what fails or is out of scope;
- whether the analogy holds for the current use, and whether to keep, limit, revise, or drop it;
- the source route for any real factual or canon claim.

## Boundaries

Do not ban analogies just because they are imperfect. Do not let them become durable truth. Do not preserve project-specific analogy overlays in this generic skill; project overlays must carry their own source and canon boundaries.
