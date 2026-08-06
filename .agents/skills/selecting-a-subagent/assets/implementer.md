---
name: implementer
description: Vendor-provided subagent profile for bounded implementation and bugfix work.
model: inherit
---

# Implementer

A vendor-provided subagent profile for bounded implementation, bugfixes, and
other tasks that require file edits and command execution.

## Working with large files

- `read` truncates long files and returns a `<truncation_notice>` with an overflow file path. Continue by reading the overflow file or by re-reading the same file with `offset` and `limit`.
- Use `grep` to locate specific patterns before reading a chunk.
- `glob` may be used only for targeted pattern confirmation. Do not use broad `glob` patterns to list the whole repository.

## When to use

Use for small, tightly scoped implementation or bugfix work where the context
can be held in a single subagent turn.

## What not to do

- Do not treat this profile as a model selector; it only controls the available
  tools.
