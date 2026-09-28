# API Design operational guidance

## When to apply

Use this reference when designing a new HTTP API contract, reviewing an existing contract, or resolving versioning and naming questions.

## Core pattern

1. Anchor the contract with the OpenAPI Object (`openapi: 3.1.0`).
2. Populate `info` with a stable title and version; use `servers` for base URLs.
3. Model resources under `paths`; keep operations idempotent where possible and use HTTP methods consistently.
4. Place reusable schemas, parameters, responses, examples, and security schemes under `components`.
5. Reference components with `$ref` to avoid duplication and keep names stable.
6. Declare `security` globally or per operation; define scopes explicitly.

## Versioning and compatibility

The `openapi` field declares the specification version of the document. API versioning is a separate concern handled through `info.version`, path design, or server URLs. Prefer additive changes within a minor version. Reserve breaking changes for major version bumps. Document deprecated operations with `deprecated: true` and sunset expectations.

## Schema patterns and reusable components

Model data with JSON Schema under `components/schemas`. Use descriptive names, consistent naming conventions, and explicit `required` arrays. Reuse parameters, headers, and responses by defining them once and referencing them. Keep component names stable; changing a component name is a breaking change for consumers relying on `$ref`.

## Error responses

Use structured problem details (RFC 7807) when exposing errors to API consumers. Include a `type` URI, a short `title`, an optional `detail`, and `status` aligned with the HTTP status code. Avoid leaking internal implementation details.

## Common mistakes

- Mixing transport, framework, or generator concerns with the contract itself. → Keep the contract independent of implementation.
- Hard-coding repeated schemas instead of using `components/schemas`. → Extract and reference reusable components.
- Changing path semantics without a version bump. → Treat breaking changes as major-version events.
- Treating optional fields as required or missing security scope definitions. → Declare `required` and `security` explicitly.

## Related references

- [OpenAPI Specification 3.1.0](https://spec.openapis.org/oas/v3.1.0)
- [RFC 7807: Problem Details for HTTP APIs](https://www.rfc-editor.org/rfc/rfc7807)
