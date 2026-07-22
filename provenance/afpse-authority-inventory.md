# Authoritative First-Party Skill Enrichment — Authority Inventory

| Issue | Skill | Lane | Primary pack | Replaced third-party entries | Execution branch |
|---|---|---|---|---|---|
| MARK-340 | `ddd` | skills-with-source | `architecture-pack` | retired upstream | `harleydbartles/mark-340-re-custody-ddd-from-the-eric-evans-ddd-reference` |
| MARK-341 | `cqrs` | skills-with-citation | `architecture-pack` | retired upstream | `harleydbartles/mark-341-split-cqrs-and-event-sourcing-into-clean-room-citation` |
| MARK-341 | `event-sourcing` | skills-with-citation | `architecture-pack` | same as `cqrs` | same as `cqrs` |
| MARK-342 | `clean-architecture` | skills-with-citation | `architecture-pack` | retired upstream | `harleydbartles/mark-342-create-clean-architecture-and-hexagonal-architecture-citation-backed` |
| MARK-342 | `hexagonal-architecture` | skills-with-citation | `architecture-pack` | none | same as `clean-architecture` |
| MARK-343 | `owasp-top-ten` | skills-with-source | `security-pack` | retired upstream | `harleydbartles/mark-343-re-custody-owasp-top-ten-and-establish-an-asvs-verification` |
| MARK-344 | `openapi-specification` | skills-with-source | `api-contracts-pack` | retired upstream | `harleydbartles/mark-344-re-custody-the-openapi-specification-specialist-skill` |
| MARK-345 | `wcag` | skills-with-source | `frontend-pack` | retired upstream | `harleydbartles/mark-345-re-custody-the-wcag-accessibility-audit-specialist-skill` |
| MARK-346 | `dotnet` | skills-with-citation | `dotnet-pack` | retired upstream | `harleydbartles/mark-346-create-the-first-party-net-ecosystem-skill-and-migrate` |
| MARK-347 | `typescript` | skills-with-citation | `language-patterns-pack` | retired upstream | `harleydbartles/mark-347-create-the-first-party-typescript-ecosystem-skill` |
| MARK-348 | `react` | skills-with-citation | `frontend-pack` | retired upstream | `harleydbartles/mark-348-create-the-first-party-react-ecosystem-skill` |
| MARK-349 | `web-styling` | skills-with-citation | `frontend-pack` | none | `harleydbartles/mark-349-create-the-cross-framework-web-styling-skill` |
| MARK-350 | `observability` | skills-with-citation | `engineering-pack` | none | `harleydbartles/mark-350-create-the-opentelemetry-observability-skill` |
| MARK-351 | `web-identity` | skills-with-citation | `security-pack` | none | `harleydbartles/mark-351-create-the-cross-stack-web-identity-citation-backed-skill` |

## Notes

- `dotnet`, `typescript`, `react`, `observability`, and `web-styling` were initially planned as `skills-with-source`, but the vendored tarballs were too large to push without Git LFS, so they were converted to `skills-with-citation` with canonical URLs and `CITATIONS.md` retained.
- `ddd`, `owasp-top-ten`, `openapi-specification`, and `wcag` retain vendored `reference-source/` snapshots and remain `skills-with-source`.
