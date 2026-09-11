# Completing plans

Use this runbook when the implementation PR has delivered an in-flight plan.
It defines this repository's custody steps; portable workflow method belongs to
the routed completion skill.

## Completion boundary

Keep the in-flight plan committed through implementation and review so the PR
shows planned versus delivered work. Before removing it, promote any decision
that still constrains repository architecture to `adr/`, and any operating rule
to current doctrine or a runbook. Do not use the completed plan as a durable
record of either.

## Off-repo archive

Copy the completed plan to the protected cold store and verify its manifest:

```bash
py -3 .agents/skills/repo-standards/scripts/archive_completed_plans.py --apply
py -3 .agents/skills/repo-standards/scripts/archive_completed_plans.py --check
```

The canonical location is
`<main-checkout>/../_agent-scratch/<repo-name>/archive/completed-plans/`. The
command only copies and verifies; it never deletes the repository source.

After a green check, remove the exact tracked plan path with Git-aware deletion,
regenerate the mesh, and commit the resulting tree in the completing PR. Do not
remove `.agents/specs/completed/` under this runbook: a completed specification
requires its own ADR/durability decision.

## Evidence

The completion PR must state the archived plan count and cold-store path. Git
history is the immutable receipt. The archive manifest proves the convenience
copy matched the plan at removal time; it is not a second source of truth.
