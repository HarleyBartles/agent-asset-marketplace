# AGENTS.md

Scope: `docs/`

This scope covers repo docs, docs-owned discovery surfaces, and docs-local
profile or guidance material.

Defer to the repository root `AGENTS.md` for global doctrine, publication
rules, and upstream-drain policy.

Mesh policy for the repo lives at `../.agents/docs/mesh-policy.md`; docs under
`docs/` should stay guidance-oriented, not operative source custody.

## Routing pointers

- `INDEX.md` for docs-owned navigation
- `skill-standards-policy.md` for first-party skill authoring standards
- `overlay-adapter-policy.md` for third-party overlay and adapter triggers
- `non-repo-locations-policy.md` for worktree and scratch file placement
- `unslop/profile.md` for the canonical repo unslop profile
- `contracts/AGENTS.md` for the contract-doc subtree
- `../.agents/docs/mesh-policy.md` for the repo mesh policy

## Review guidelines

- Treat docs under `docs/` as discovery and guidance surfaces, not canonical
  marketplace source.
- The canonical repo unslop profile lives at `docs/unslop/profile.md`.
- Keep docs-owned profile files stable once they are chosen as canonical
  homes.
- Flag stale cross-references when a canonical docs path moves.

## Maintenance responsibility

This file must stay aligned with the repo's documentation structure. When
canonical docs paths move or new docs-owned surfaces are added, review and
update this file to reflect current expectations. The canonical unslop profile
at `docs/unslop/profile.md` should remain stable once chosen—changes to that
path require updating this file.
