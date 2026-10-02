# Mutation script safety

## Read when

Read before running or changing a script that writes, moves, deletes, regenerates, packages, installs, or publishes repository content.

## Contract

Mutation scripts should make their own mutation boundary explicit, commonly through `--apply`, and provide a read-only `--check` path where meaningful. Do not add a redundant shared-checkout intent flag. Where workspace selection matters, follow the repository's worktree policy. Reject unsafe roots such as submodules when required by the operation.

Run git rev-parse --show-superproject-working-tree before any location decision. Reject a non-empty result unconditionally. Resolve checkouts and external worktree or scratch locations through the portable Git-derived algorithm in [worktree-and-branch-policy.md](worktree-and-branch-policy.md); do not derive repository roots from source-file or working-directory parents.

Keep the script's mutation set deterministic, narrow, and reported. Its runtime owns execution behavior, while a repository-local policy owns repository-specific commands, exceptions, and CI. Verify generated outputs through their generator and validate publication through GitHub evidence.
