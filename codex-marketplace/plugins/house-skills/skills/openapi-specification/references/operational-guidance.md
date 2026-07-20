# Operational Guidance: OpenAPI Specification

## OpenAPI Document Structure

An OpenAPI contract is a single document rooted at the OpenAPI Object. Populate `info` with title, version, and contact details. Use `servers` to declare base URLs. Define routes under `paths`, each with operations that declare parameters, request bodies, and responses. Place reusable schemas, parameters, responses, examples, and security schemes under `components`. Reference them with `$ref` to keep the contract DRY. Declare `security` globally or per operation.

## Versioning and Compatibility

The `openapi` field declares the specification version of the document, e.g., `3.1.0`. API versioning is a separate concern handled through `info.version`, path design, or server URLs. Prefer additive changes within a minor version. Reserve breaking changes for major version bumps. Document deprecated operations with `deprecated: true` and sunset expectations.

## Schema Patterns and Reusable Components

Model data with JSON Schema under `components/schemas`. Use descriptive names, consistent naming conventions, and explicit required arrays. Reuse parameters, headers, and responses by defining them once and referencing them. Keep component names stable; changing a component name is a breaking change for consumers relying on `$ref`.
