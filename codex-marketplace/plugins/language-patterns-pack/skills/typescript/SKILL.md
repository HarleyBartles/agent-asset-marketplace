---
name: typescript
description: Use when writing or reviewing TypeScript type design, generics, module
  resolution, or compiler configuration. Do not use when the work is JavaScript runtime
  debugging or framework-specific UI composition.
metadata:
  source-id: typescript
  source-path: codex-marketplace/plugins/language-patterns-pack/skills/typescript/SKILL.md
  provenance-name: Typescript first-party skill
  source-category: first_party
  status: active
  owner: Harley Bartles
  scope: TypeScript type design, generics, module resolution, and compiler configuration.
  use_when:
  - Use when writing or reviewing TypeScript type design.
  - Use when working with generics, mapped types, or conditional types.
  - Use when resolving module paths or configuring tsconfig.json.
  - Use when narrowing types or writing type guards.
  do_not_use_when:
  - Do not use when the work is JavaScript runtime debugging.
  - Do not use when the work is framework-specific UI composition.
license: MIT
---

# TypeScript

## Overview

TypeScript adds a static type system to JavaScript. This skill covers type design, generics, module resolution, and compiler configuration so code stays safe and maintainable.

## When to Use

- Designing interfaces, type aliases, unions, intersections, or literal types.
- Writing or consuming generic functions and types.
- Narrowing types with guards, `typeof`, `instanceof`, or discriminated unions.
- Authoring declaration files or configuring project-wide `tsconfig.json`.
- Choosing module resolution strategy and strictness settings.

Do not use for runtime behavior, build tooling unrelated to types, or framework-specific component composition.

## Core Pattern

1. Model data with `interface` or `type` before writing logic.
2. Use generics only when the function or type must work across multiple concrete types; add constraints.
3. Let inference do the work; add annotations at module boundaries and public APIs.
4. Prefer `unknown` over `any`; narrow with type guards before use.
5. Keep `strict` and `noImplicitAny` enabled; align `module`, `moduleResolution`, and `target` with the runtime.

## Common Mistakes

- Overusing `any` instead of `unknown` or precise unions.
- Declaring generic parameters without constraints, leading to impossible operations.
- Mixing `interface` extension and `type` aliases for the same shape inconsistently.
- Misaligned `tsconfig.json` paths or module resolution causing hidden import errors.
- Disabling strict settings to silence errors instead of fixing the underlying type issue.
