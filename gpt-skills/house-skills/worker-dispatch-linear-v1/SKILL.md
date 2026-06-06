# Worker Dispatch Linear v1

Use this skill when the issue contract lives in Linear and the work packet needs a narrow dispatch/control-plane shape.

This skill treats the Linear issue as the durable task contract. Linear comments and attachments are the worker event log, the PR branch is the work packet, and GitHub proves the branch after publication. Legacy YAML fallback exists only as a last resort.

## Core rule

Keep the issue body, comments, attachments, branch, and PR in one durable line of evidence.

## Boundaries

- It does not replace Linear object mechanics.
- It does not own general repo doctrine.
- It does not package or publish skills.
