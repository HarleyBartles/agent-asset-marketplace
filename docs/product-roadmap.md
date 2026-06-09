# Product Roadmap And Milestone Scheme

Version: v1
Last updated: 2026-06-09

This document defines a lightweight roadmap layer for Wild Bunch. It groups
issues by broad product horizon without turning milestones into a date plan or a
second issue tracker.

## What Labels Mean Versus What Milestones Mean

Labels answer the immediate shape of the work:

- urgency: `must`, `should`, `could`
- timing: `now`, `next`, `later`
- work type: `feature`, `system`, `tooling`
- readiness or queue posture: `boring`

Milestones answer the broad product/version horizon:

- which product phase an issue belongs to;
- whether the issue is part of the near-term ship path or a later platform
  track;
- how to group related work without pretending dates are fixed.

Do not use milestones as a substitute for `now` / `next` / `later`. Labels own
that axis already.

## Proposed Milestone Vocabulary

Use a small, stable set of horizon buckets:

- `Roadmap / Planning`
- `Core Loop`
- `v1`
- `v2 / Sandbox`
- `DLC / Future Packs`

These names are intentionally broad. They are a grouping tool, not a release
promise.

### Milestone meanings

- `Roadmap / Planning`: meta-work about planning, taxonomy, sequencing, and
  roadmap maintenance itself.
- `Core Loop`: foundational game loop work needed to make the project feel like
  the game, not the shell.
- `v1`: the first shippable baseline. This is for the near-term product shape,
  not for every currently active issue.
- `v2 / Sandbox`: later experimentation, sandbox-capable systems, and
  architecture that should not block the initial product. This is the right
  home for later cockpit/sandbox ideas, including local-only LLM-assisted
  concepts that remain proposal-only.
- `DLC / Future Packs`: optional expansions, post-v1 content, and other
  clearly separable future add-ons.

## When To Assign A Milestone

Assign a milestone when the issue is materially part of one of the horizons
above and the grouping improves navigation, review, or release thinking.

Good candidates for milestones:

- work needed for the baseline product;
- work that clearly belongs to a later version boundary;
- roadmap or planning policy changes that shape the horizon model;
- large features that need a coarse version home so they do not get lost.

Leave the issue unmilestoned when:

- the issue is tiny, tactical, or purely operational;
- the label axis already communicates the important planning signal;
- the work is speculative and not yet ready to be tied to a product horizon;
- the issue is current-track but does not need broader version grouping.

If an issue stays unmilestoned, keep it discoverable with labels and a clear
cross-link to any relevant roadmap or parent planning issue.

## Discoverability Rules For Far-Future Work

Long-running future issues should remain easy to find without being promoted to
current-track work:

- keep the issue labeled with timing and type labels;
- cross-link to the roadmap note or the parent planning issue;
- use `v2 / Sandbox` or `DLC / Future Packs` only when the horizon is stable
  enough to be useful;
- avoid inventing date commitments just to make the queue look organized.

This keeps future concepts visible without making them look urgent.

## Tiny Example Map

- `Roadmap / Planning`: a note that adjusts the planning taxonomy or milestone
  rules.
- `Core Loop`: turn resolution, encounter flow, or another foundational gameplay
  mechanic.
- `v1`: a must-have baseline feature required before the first shippable
  version.
- `v2 / Sandbox`: local-only LLM lawman reasoning or sandbox assistance work
  that is explicitly deferred and architecture-sensitive.
- `DLC / Future Packs`: a post-launch expansion idea or an optional content
  pack.

## Review Guidance

- Prefer a milestone only when it helps explain the issue's product horizon.
- Prefer labels when the important signal is urgency, readiness, work type, or
  near-term queue posture.
- Keep the scheme small. If a new bucket is needed, add it deliberately and
  version this document instead of multiplying milestone names.

## Change Policy

This is the initial version of the scheme. If the roadmap vocabulary changes,
update this document first, then decide whether any broader repo convention
needs to follow.

Do not create, rename, delete, or assign real GitHub or Linear milestones in
response to this document unless a fresh explicit instruction authorizes it.
