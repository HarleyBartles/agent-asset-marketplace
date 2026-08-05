---
name: implementer-strong
description: Vendor-provided subagent profile for implementation that needs more reasoning or broader context.
model: inherit
allowed-tools:
- read
- grep
- find_file_by_name
- exec
- edit
---

# Implementer Strong

A vendor-provided subagent profile for implementation that needs more reasoning
or broader context than the standard `implementer` profile.

## Working with large files

- `read` truncates long files and returns a `<truncation_notice>` with an overflow file path. Continue by reading the overflow file or by re-reading the same file with `offset` and `limit`.
- Use `grep` to locate specific patterns before reading a chunk.
- `glob` may be used only for targeted pattern confirmation. Do not use broad `glob` patterns to list the whole repository.

## When to use

Use for larger or more ambiguous implementation tasks where the parent cannot
fully describe the context in a few lines.

## What not to do

- Do not treat this profile as a model selector; it only controls the available
  tools.
