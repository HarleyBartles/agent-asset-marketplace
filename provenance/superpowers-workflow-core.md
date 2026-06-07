# Superpowers Workflow Core Adaptation

This note records how the repo treats the vendor-mirrored Superpowers workflow core and the first-party adaptation that hangs off it.

## Vendor Custody

- Upstream project: `obra/superpowers`
- Upstream URL: <https://github.com/obra/superpowers.git>
- Mirrored tag: `v5.1.0`
- Mirrored commit: `f2cbfbefebbfef77321e4c9abc9e949826bea9d7`
- License: MIT
- Vendor mirror root: `sources/vendor/obra/superpowers/v5.1.0/`

## Why The Mirror Exists

MARK-34 owns vendor custody. This mirror keeps the upstream generic workflow core available as third-party source with license and provenance intact.

The mirror is the provenance anchor for first-party worker habits in this repo. It is not the first-party doctrine itself.

## First-Party Adaptation

The repo’s first-party worker guidance lives in:

- `docs/worker-playbooks.md`
- `README.md`
- `provenance/README.md`

Those surfaces adapt the reusable concepts into repo-local operating habits without relabeling upstream text as Harley-owned doctrine.

## Concepts Adopted

- brainstorming
- writing-plans
- executing-plans
- test-driven-development
- systematic-debugging
- verification-before-completion
- using-git-worktrees
- requesting-code-review
- receiving-code-review
- finishing-a-development-branch

## Concepts Not Adopted Here

- `using-superpowers`
- `dispatching-parallel-agents`
- `subagent-driven-development`

Those remain out of scope for this issue. Multi-agent support is parked with `MARK-36`.

## Related Logs

- `MARK-7 Activity Log`
- `MARK-34 Activity Log`
- `MARK-35 Activity Log`

## Provenance Rule

If a future change copies exact upstream wording, keep the MIT attribution chain intact and point back to this mirror and the upstream source. Prefer fresh conceptual wording whenever possible.
