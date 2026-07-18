# Mutation script safety

## Read when

Read before running or changing a script that writes, moves, deletes,
regenerates, packages, installs, or publishes repository content.

## Contract

Mutation scripts refuse a shared checkout by default. A script may expose
--allow-shared-checkout only as an explicit override that emits a prominent
warning that human approval is required; it never implies approval itself.
Every mutation script provides a read-only --check path where meaningful.

Run git rev-parse --show-superproject-working-tree before any location
decision. Reject a non-empty result unconditionally. Resolve checkouts and
external worktree or scratch locations through the portable Git-derived
algorithm in [worktree-and-branch-policy.md](worktree-and-branch-policy.md);
do not walk filesystem parents independently.

Keep the script's mutation set deterministic, narrow, and reported. Its
runtime owns execution behavior, while a repository-local policy owns
repository-specific commands, exceptions, and CI. Verify generated outputs
through their generator and validate publication through GitHub evidence.
