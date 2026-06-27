---
name: canon-buster
description: Use when use this skill before making, changing, summarizing, publishing,
  dispatching, or relying on a durable canon claim.
metadata:
  source-id: canon-buster
  source-path: sources/first_party/skills/canon-buster/SKILL.md
  provenance-name: Canon Buster first-party skill
  source-category: first_party
  status: active
  owner: Harley Bartles
  scope: Use when use this skill before making, changing, summarizing, publishing,
    dispatching, or relying on a durable canon claim.
  use_when:
  - Use when use this skill before making, changing, summarizing, publishing, dispatching,
    or relying on a durable canon claim.
  do_not_use_when:
  - Do not use when another more specific skill owns this task.
  projection_targets:
  - codex-marketplace/plugins/house-skills/skills/canon-buster
license: MIT
---
# Canon Buster

Use this skill before making, changing, summarizing, publishing, dispatching, or relying on a durable canon claim.

Canon means the authoritative truth set for the relevant domain: project doctrine, world state, character facts, source-of-truth records, schemas, accepted decisions, policy, or other governed truth surfaces. This skill is generic. Rooms-specific canon/world material was provenance for extracting the pattern, not imported as a Rooms overlay here.

## Owned decision

Given a proposed canon-facing claim or mutation, return:

- `green` â€” the claim or action is grounded in the current authoritative canon/source route and does not drift.
- `amber` â€” the claim may be valid, but source basis, authority, wording, or mutation route needs repair.
- `red` â€” the claim contradicts canon, invents canon, collapses ambiguity, or uses the wrong authority.
- `blocked` â€” the authoritative canon/source surface is unavailable or the required authority is missing.

## Canon risks

Check for:

- memory, conversation, report, inference, or analogy being treated as canon;
- old decisions overriding newer accepted source without evidence;
- generic doctrine being mistaken for project-specific canon, or project residue being imported as generic law;
- unresolved ambiguity being flattened into a fact;
- summaries changing the meaning of source material;
- unauthorized mutation of a protected truth surface;
- validation or tests being treated as canon approval when they only prove a narrower condition;
- worker output or assistant reports being accepted without ingress/verification;
- naming, versioning, or metadata drift that changes identity.

## Source ladder

Use the domain's declared source hierarchy when available. If no explicit hierarchy exists, prefer:

1. Current user instruction for the current task, within lawful scope.
2. Tracked source files, manifests, schemas, accepted decisions, or canonical docs.
3. Issue bodies, PRs, comments, reports, and validation logs as evidence surfaces, not automatic canon.
4. Prior conversation or memory only as discovery hints until verified.
5. Analogy or inference only as labeled reasoning, never as canon by itself.

## Workflow

1. Name the canon-facing claim or mutation.
2. Identify the relevant canon domain and authoritative source route.
3. Separate source-backed facts, reported claims, inference, assumptions, and unresolved ambiguity.
4. Check contradiction, drift, authority, and mutation boundary.
5. Repair wording or route internally when one lawful path exists.
6. Surface a decision only when lawful authority must choose among real canon options.
7. Block rather than invent when the canon source or authority is unavailable.

## Generic extraction rule

When this skill is derived from project-specific residue, drain the generic pattern and leave project law behind. Do not import Rooms actor names, Rooms paths, Rooms source hierarchy, or Rooms-only workflow assumptions into this generic skill. Use project overlays later when a project needs its own canon binding.

## Output posture

When visible, report:

- canon domain;
- source route used or missing;
- claim status: source-backed, reported, inferred, assumed, contradicted, or unresolved;
- repair, blocker, or remaining decision;
- next lawful route.

## Boundaries

Do not use canon busting as a broad research workflow. Do not make canon by summarizing. Do not treat a green as publication, validation, merge, or mutation proof unless the owning workflow also provides that evidence.
