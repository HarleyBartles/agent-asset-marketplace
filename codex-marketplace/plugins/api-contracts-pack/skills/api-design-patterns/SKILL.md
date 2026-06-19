---
metadata:
  origin: Claude-Cortex
  source_author: NickCrew
  source_license: MIT
  source_repo: https://github.com/NickCrew/Claude-Cortex
  source_path: sources/third_party/codex-cortex/upstream/skills/api-design-patterns/SKILL.md
  content_mode: adapted
  adapted_author: Harley Bartles
---
name: api-design-patterns
description: Contract-first API design patterns for REST and GraphQL services, with versioning, pagination, error handling, generated-client expectations, and validation posture.
keywords:
  - API design
  - API versioning
  - REST API
  - GraphQL
  - contract-first
  - pagination
  - error handling
  - generated clients
  - service contract
  - contract validation
file_patterns:
  - "**/*.http"
  - "**/api/**"
  - "**/contracts/**"
  - "**/schema/**"
confidence: 0.86
---

# API Design Patterns

Use this skill when you are defining or reviewing a service contract that needs
to stay predictable across clients, services, and releases.

## When to Use This Skill

- designing a new REST or GraphQL API;
- refactoring an existing contract for clarity or stability;
- defining versioning rules for an externally or internally consumed service;
- standardizing pagination, filtering, and field selection;
- tightening error formats so clients can recover cleanly;
- validating generated clients or contract tests; or
- reviewing backend/frontend seams where payload shape matters.

## Quick Reference

| Topic | Load reference |
| --- | --- |
| Contract design process and API evolution | `references/design-process.md` |
| Contract quality rubric and validation posture | `validation/rubric.yaml` |

## Core Principles

### 1. Treat the contract as the product

- resource names, field names, and status codes are part of the public API;
- clients should not depend on storage details, service internals, or framework
  defaults;
- every contract change should be judged by its effect on consumers, not just
  the server implementation.

### 2. Keep the surface explicit and stable

- prefer clear resource-oriented paths and predictable request/response shapes;
- avoid hidden behavior that changes based on undocumented server heuristics;
- keep input validation local to the boundary before domain work begins;
- return the same shape for the same kind of error whenever possible.

### 3. Make the lifecycle visible

- use versioning rules that let old clients continue to function while new
  clients adopt the next shape;
- define deprecation, migration, and sunset expectations up front;
- keep generated-client expectations and contract tests aligned with the live
  service shape.

## Resource-Oriented Design

**Use nouns for resources and verbs for state transitions only when a resource
cannot model the action cleanly.**

```text
GET    /users/123
POST   /users
PUT    /users/123
PATCH  /users/123
DELETE /users/123
```

Prefer plural resource collections, nested resources only when they reflect a
real ownership boundary, and sub-resources only when they make the contract
clearer.

## HTTP Status Codes

### Success

- `200 OK`: standard successful response;
- `201 Created`: resource created;
- `202 Accepted`: asynchronous work started;
- `204 No Content`: successful request with no body.

### Client Errors

- `400 Bad Request`: malformed or invalid request;
- `401 Unauthorized`: authentication required or failed;
- `403 Forbidden`: authenticated but not allowed;
- `404 Not Found`: resource absent;
- `409 Conflict`: state or version conflict;
- `422 Unprocessable Entity`: semantic validation failure;
- `429 Too Many Requests`: client exceeded rate limits.

### Server Errors

- `500 Internal Server Error`: unexpected failure;
- `502 Bad Gateway`: upstream service failure;
- `503 Service Unavailable`: temporary outage or maintenance;
- `504 Gateway Timeout`: upstream timeout.

## Versioning and Compatibility

- prefer additive changes inside a version;
- introduce a new version for breaking contract changes;
- document the migration path before the new shape ships;
- keep deprecation headers, successor links, and release notes consistent;
- make the compatibility rules obvious to generated clients and manual clients
  alike.

## Pagination, Filtering, and Field Selection

- use offset pagination when the dataset is small and stable;
- use cursor or keyset pagination when consistency and scale matter;
- include explicit next/previous links or cursors in the response;
- support sparse fieldsets when payload size matters;
- keep filters and sort parameters predictable and documented.

## Errors and Validation

- return a stable error envelope with a machine-readable code;
- include a human-readable message and actionable field detail where relevant;
- distinguish syntax errors from semantic validation errors;
- keep request IDs or correlation IDs in the error payload when possible;
- make generated clients able to branch on error shape without scraping text.

## Authentication, Idempotency, and Caching

- choose the simplest authentication mechanism that fits the trust boundary;
- require idempotency keys for non-safe operations that may be retried;
- use ETags or equivalent validators when the client needs conditional reads;
- set cache rules deliberately instead of inheriting defaults;
- document rate-limit behavior and retry guidance.

## GraphQL Considerations

- keep queries bounded and explicit;
- prefer stable schemas and additive field changes;
- return predictable error details for missing resources or invalid input;
- make pagination and filtering rules obvious in the schema and resolver
  behavior;
- align GraphQL responses with the same contract discipline you would expect
  from a REST surface.

## Contract Testing and Validation

1. define the contract in one place;
2. validate requests at the boundary;
3. test success, validation failure, and version-compatibility cases;
4. exercise generated clients against the contract;
5. verify that breaking changes are blocked before release.

## Best Practices Summary

1. keep the contract readable by humans and stable for machines;
2. document versioning and migration rules before clients depend on them;
3. make errors structured and recoverable;
4. prefer explicit pagination, filtering, and field selection;
5. treat generated clients and contract tests as first-class consumers.

## Anti-Patterns to Avoid

- leaking database or framework internals into the payload shape;
- changing a field type or meaning without a new version;
- returning inconsistent error envelopes across endpoints;
- using ad hoc pagination that breaks under load;
- allowing undocumented client dependence on incidental response order;
- treating generated-client compatibility as optional.

## Resources

- `references/design-process.md`
- `validation/rubric.yaml`
