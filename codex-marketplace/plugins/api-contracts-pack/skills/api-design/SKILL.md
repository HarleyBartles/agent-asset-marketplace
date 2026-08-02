---
name: api-design
description: Use when designing, reviewing, or versioning an HTTP API contract, choosing
  resource naming, or mapping OpenAPI structures to implementation boundaries.
metadata:
  source-id: api-design
  source-path: codex-marketplace/plugins/api-contracts-pack/skills/api-design/SKILL.md
  provenance-name: Api Design first-party skill
  source-category: first_party
  status: active
  owner: Harley Bartles
  scope: Use when designing, reviewing, or versioning an HTTP API contract, choosing
    resource naming, or mapping OpenAPI structures to implementation boundaries.
  use_when:
  - Use when designing a new API contract.
  - Use when reviewing an existing API contract for consistency and spec compliance.
  - Use when versioning paths, schemas, or security schemes.
  - Use when choosing resource and operation naming conventions.
  do_not_use_when:
  - Do not use when the work is implementation framework-specific.
  - Do not use when the work is code-generation only.
  related_skills:
  - secure-development
license: MIT
---

# API Design

## Overview

Produce and evaluate HTTP API contracts that are clear, stable, and aligned with the OpenAPI Specification. This skill covers contract structure, reusable components, versioning, and design conventions.

## When to Use

- Designing a new API contract from requirements.
- Reviewing a contract for spec compliance and consistency.
- Deciding how to version paths, schemas, or security schemes.
- Choosing resource naming, operation semantics, or error response shapes.

Do not use when another more specific skill owns the task.

## Core Pattern

1. Start with the OpenAPI Object, then fill `info`, `servers`, and `paths`.
2. Define reusable schemas, parameters, responses, and security schemes under `components`.
3. Prefer explicit version declarations; keep breaking changes out of patch releases.
4. Use consistent resource naming and HTTP methods; return structured problem details for errors.
5. Reference reusable components with `$ref` to keep the contract DRY.

## Common Mistakes

- Mixing transport, framework, or generator concerns with the contract itself. → Keep the contract independent of implementation.
- Hard-coding repeated schemas instead of using `components/schemas`. → Extract and reference reusable components.
- Changing path semantics without a version bump. → Treat breaking changes as major-version events.
- Treating optional fields as required or missing security scope definitions. → Declare `required` and `security` explicitly.

For detailed guidance, see `references/operational-guidance.md`.
