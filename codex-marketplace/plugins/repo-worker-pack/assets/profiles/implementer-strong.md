---
name: implementer-strong
description: Vendor-provided subagent profile for implementation that needs more reasoning or broader context.
model: inherit
allowed-tools:
- read
- grep
- glob
- exec
- edit
- write
---

# Implementer Strong

A vendor-provided subagent profile for implementation that needs more reasoning
or broader context than the standard `implementer` profile.

## When to use

Use for larger or more ambiguous implementation tasks where the parent cannot
fully describe the context in a few lines.

## What not to do

- Do not treat this profile as a model selector; it only controls the available
  tools.
