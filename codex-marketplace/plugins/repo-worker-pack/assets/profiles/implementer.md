---
name: implementer
description: Vendor-provided subagent profile for bounded implementation and bugfix work.
model: inherit
allowed-tools:
- read
- grep
- glob
- exec
- edit
- write
---

# Implementer

A vendor-provided subagent profile for bounded implementation, bugfixes, and
other tasks that require file edits and command execution.

## When to use

Use for small, tightly scoped implementation or bugfix work where the context
can be held in a single subagent turn.

## What not to do

- Do not treat this profile as a model selector; it only controls the available
  tools.
