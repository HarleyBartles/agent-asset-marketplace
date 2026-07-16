# Superpowers Refresh Playbook

Use this playbook when the upstream Superpowers source changes and you need to
decide how the repo should respond.

## Use this when

- A new upstream release is available.
- The retained source snapshot may need to move to a new tag.
- The adapter might need an update before regeneration.
- You need to decide whether the change is a source refresh, an adapter-only
  repair, or a blocked follow-up.

## Decision path

1. Identify the newest upstream tag to retain.
2. Check whether the adapter overlay and adapter metadata already match that
   tag.
3. If the adapter is stale, update it before regeneration.
4. If the source snapshot is changing, hand off to the runbook.
5. If the change cannot be completed in one deterministic pass, open or update
   the follow-on issue before proceeding.

## Related runbook

- `.agents/runbooks/superpowers-source-refresh.md`

## External pattern references

- Playbook/runbook pattern references live in
  `.agents/docs/playbook-runbook-doctrine.md`.
