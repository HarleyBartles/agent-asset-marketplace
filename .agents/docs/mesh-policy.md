# Mesh Policy

## 1. `AGENTS.md` mesh

`AGENTS.md` files are authored law. In the Devin Local / Devin CLI runtime,
any `AGENTS.md` that is discovered is loaded as an **always-on** rule for the
remainder of the session. It is not scoped by working directory. Do not rely on
sub-directory `AGENTS.md` for scoped rules.

Root `AGENTS.md` should contain only the small set of rules that are genuinely
always on for the whole repository. If a sub-directory `AGENTS.md` exists, it
must be so short and safe that loading it always-on does not overwhelm the
agent. If the law is not appropriate for every session, it does not belong in
an `AGENTS.md`.

`AGENTS.md` should explain rules, boundaries, and source/projection
distinctions, not directory navigation. It is a routing surface, not a content
surface. Do not restate doctrine in `AGENTS.md`. When a rule lives in a doctrine
doc under `docs/` or `.agents/docs/`, the `AGENTS.md` carries only a
MUST READ pointer with the trigger condition and the path to the doctrine
doc. The doctrine doc is the canonical rule surface; `AGENTS.md` is the
routing surface.

## 2. `.devin/rules/` and Devin Rules

For scoped, conditional, or non-always-on rules, use the Devin Rules surface:
`.devin/rules/*.md`. Each rule is a separate Markdown file with a `trigger`
in its frontmatter that controls when the rule is loaded.

Allowed `trigger` values in Devin Local / Devin CLI:

- `always_on` -- loaded in every message.
- `glob` -- loaded only when the agent works with files matching `globs:`.
- `model_decision` -- the model decides when to apply.
- `manual` -- only when invoked.

Example:

```markdown
---
description: "tools and marketplace generation"
trigger: glob
globs: "tools/**"
---
```

Keep each rule under 12,000 characters.

The repo does not support an `.agents/rules/` surface. Do not create it unless
the runtime adds native support.

## 3. `INDEX.md` mesh

`INDEX.md` files are generated navigation and coverage surfaces.
They tell agents and humans what exists in a subtree and where to go next.
They must not carry operative law.
They must not be inserted into skill roots or adapter overlay roots.

## 4. `README.md` and docs-owned guidance

`README.md` files are human-facing explanation only. They may point at agent
law, but they are not the law.

`docs/` files are docs-owned guidance and doctrine surfaces. They may carry
durable guidance, but they are still separate from generated navigation.

## 5. `.agents/` tree

`.agents/` is the tracked repo-resident home for agent-facing doctrine, local
plugin posture, agent work surfaces, and output/evidence conventions.
It is not disposable cache.
It is not the home for ordinary product/source work unless that source is
agent-facing infrastructure.

## 6. Mesh self-healing

If a worker finds stale or misleading authored mesh law (`AGENTS.md`,
`README.md`, or other agent-facing doctrine docs), repair it in scope or return
AMBER with the exact deferred repair.
If a worker finds stale generated `INDEX.md` navigation, repair it by
regenerating the whole index mesh through tooling.
If whole-mesh regeneration does not produce a valid mesh, fix the generator,
exclusion policy, or source inputs.
Do not hand-edit individual generated `INDEX.md` files or regenerate only a
subtree to satisfy CI.
