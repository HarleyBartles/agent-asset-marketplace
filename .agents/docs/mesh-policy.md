# Mesh Policy

## 1. `AGENTS.md` mesh

`AGENTS.md` files are authored scoped law.
The nearest scoped `AGENTS.md` applies naturally to the subtree an agent is
working in, with root law inherited unless a nearer node adds a local delta.
`AGENTS.md` should explain rules, boundaries, and source/projection
distinctions, not directory navigation.

`AGENTS.md` files should stay slim. Their job is to tell agents what to read,
when to read it, and where the next relevant surface lives.

## 2. `INDEX.md` mesh

`INDEX.md` files are generated navigation and coverage surfaces.
They tell agents and humans what exists in a subtree and where to go next.
They must not carry operative law.
They must not be inserted into skill roots or adapter overlay roots.

## 3. `README.md` and docs-owned guidance

`README.md` files are human-facing explanation only. They may point at agent
law, but they are not the law.

`docs/` files are docs-owned guidance and doctrine surfaces. They may carry
durable guidance, but they are still separate from generated navigation.

## 4. `.agents/` tree

`.agents/` is the tracked repo-resident home for agent-facing doctrine, local
plugin posture, agent work surfaces, and output/evidence conventions.
It is not disposable cache.
It is not the home for ordinary product/source work unless that source is
agent-facing infrastructure.

## 5. Mesh self-healing

If a worker finds stale or misleading authored mesh law (`AGENTS.md`,
`README.md`, or other agent-facing doctrine docs), repair it in scope or return
AMBER with the exact deferred repair.
If a worker finds stale generated `INDEX.md` navigation, repair it by
regenerating the whole index mesh through tooling.
If whole-mesh regeneration does not produce a valid mesh, fix the generator,
exclusion policy, or source inputs.
Do not hand-edit individual generated `INDEX.md` files or regenerate only a
subtree to satisfy CI.
