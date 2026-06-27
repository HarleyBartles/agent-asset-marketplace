# Mesh Policy

## 1. `AGENTS.md` mesh

`AGENTS.md` files are authored scoped law.
The nearest scoped `AGENTS.md` applies naturally to the subtree an agent is
working in, with root law inherited unless a nearer node adds a local delta.
`AGENTS.md` should explain rules, boundaries, and source/projection
distinctions, not directory navigation.

## 2. `INDEX.md` mesh

`INDEX.md` files are generated navigation and coverage surfaces.
They tell agents and humans what exists in a subtree and where to go next.
They must not carry operative law.
They must not be inserted into skill roots or adapter overlay roots.

## 3. `.agents/` tree

`.agents/` is the tracked repo-resident home for agent-facing doctrine, local
plugin posture, agent work surfaces, and output/evidence conventions.
It is not disposable cache.
It is not the home for ordinary product/source work unless that source is
agent-facing infrastructure.

## 4. Mesh self-healing

If a worker finds stale or misleading mesh law or navigation while working in
scope, repair it in the same PR.
If the repair is outside scope, return AMBER with the exact deferred mesh
repair.

