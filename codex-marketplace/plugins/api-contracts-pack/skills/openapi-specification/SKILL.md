---
name: openapi-specification
description: Use when designing, reviewing, or versioning an OpenAPI contract. Do
  not use when the work is implementation framework-specific or code-generation only.
metadata:
  source-id: openapi-specification
  source-path: sources/first_party/skills/openapi-specification/SKILL.md
  provenance-name: Openapi Specification first-party skill
  source-category: first_party
  status: active
  owner: Harley Bartles
  scope: OpenAPI contract design, review, and versioning guidance grounded in the
    OpenAPI Specification.
  use_when:
  - Use when designing a new OpenAPI contract.
  - Use when reviewing an existing OpenAPI contract for correctness and consistency.
  - Use when versioning or evolving an OpenAPI contract.
  do_not_use_when:
  - Do not use when the work is implementation framework-specific.
  - Do not use when the work is code-generation only.
  related_skills:
  - api-design-patterns
license: MIT
---

# OpenAPI Specification

## Overview
Use this skill to produce and evaluate OpenAPI contracts that match the OpenAPI Specification. It focuses on contract structure, reusable components, and version compatibility.

## When to Use
- Designing a new API contract from requirements.
- Reviewing an existing contract for spec compliance.
- Deciding how to version paths, schemas, or security schemes.
- Refactoring a contract to reduce duplication through components.

## Core Pattern
Start with the OpenAPI Object, then fill `info`, `servers`, and `paths`. Define reusable schemas, parameters, responses, and security schemes under `components`. Prefer explicit version declarations and keep breaking changes out of patch releases.

## Common Mistakes
- Mixing transport, framework, or generator concerns with the contract itself.
- Hard-coding repeated schemas instead of using `components/schemas`.
- Treating optional fields as required or missing security scope definitions.
- Changing path semantics without a version bump.

For detailed guidance, see `references/operational-guidance.md`.
