# AFPSE next authoritative-source specialist candidates

## Decision matrix

| Proposed skill | Canonical authority | License | Vendoring feasibility | Primary pack home | Overlapping third-party entries to retire | Confidence | Open questions |
|---|---|---|---|---|---|---|---|
| `graphql` | [GraphQL specification](https://spec.graphql.org/) (latest) and [graphql-js](https://github.com/graphql/graphql-js) reference implementation | Specification under Open Web Foundation Final Specification Agreement; reference implementation MIT | High — spec pages are static HTML and the reference implementation is small; suitable for source-backed or citation-backed lane | `api-contracts-pack` | `api-design-patterns` (partial overlap on API contracts) | High | Should the spec be vendored as HTML or should authority rely on the OWF-signed release page? |
| `kubernetes` | [Kubernetes documentation](https://kubernetes.io/docs/) (CNCF / CC BY 4.0) and [upstream repo](https://github.com/kubernetes/website) | Docs CC BY 4.0; source code Apache-2.0 | Medium — documentation tree is large; likely better as citation-backed with targeted vendored snapshots of concept pages | `engineering-pack` | `deployment-patterns` (partial overlap) | Medium | How to draw a clean boundary versus `docker-patterns` and `deployment-patterns`? |
| `rust` | [The Rust Programming Language](https://doc.rust-lang.org/book/) and [The Rust Reference](https://doc.rust-lang.org/reference/) (Rust project; MIT/Apache-2.0) | MIT/Apache-2.0 | High — book source is a well-structured mdBook repository; can be vendored as a tarball or cited | `language-patterns-pack` | None identified | Medium-High | Is there enough distinct guidance beyond `language-patterns-pack` to justify a standalone skill versus a generic `rust-patterns`? |
| `go` | [Go documentation](https://go.dev/doc/) and [Effective Go](https://go.dev/doc/effective_go) (BSD-3-Clause for docs, matching Go source) | BSD-3-Clause | High — documentation is compact HTML; easily vendored or cited | `language-patterns-pack` | None identified | High | Should the skill cover only the language, or also expand to `go-modules` and standard-library patterns? |
| `python-language` | [Python documentation](https://docs.python.org/3/) (PSF license) | PSF license agreement | Medium — documentation is large and version-specific; best as citation-backed with snapshot of the tutorial and language reference | `language-patterns-pack` | `async-python-patterns`, `python-performance-optimization`, `python-testing-patterns` (language fundamentals only; keep ecosystem-specific skills) | Medium | Which Python version should be pinned? 3.12 LTS or `main`? |
| `mobile-platforms` | No single canonical authority; iOS Human Interface Guidelines (Apple), Material Design (Google), and platform SDK docs are fragmented | Apple/Google proprietary terms vary; no unified open license | Low — authority is fragmented, vendor-controlled, and often prohibits redistribution | `frontend-pack` (if pursued) | None | Low | Is there a narrower, licensable slice (e.g., Flutter docs under BSD) that could be a `flutter` skill instead? |
| `api-gateways` | No single canonical spec; practical guidance lives in vendor docs (Kong, NGINX, Envoy, AWS) and the broader API design patterns literature | Mixed proprietary and open | Low — no authoritative, licensable source; overlaps with `api-design-patterns` and `openapi-specification` | `api-contracts-pack` (if pursued) | `api-design-patterns` (overlap) | Low | Should this candidate be dropped in favor of vendoring a specific gateway technology (e.g., `envoy-proxy` under Apache-2.0)? |

## Observed licensing calibrations

- **CC BY 4.0** (Microsoft docs, Kubernetes docs) supports source-backed vendoring with attribution; large trees may require Git LFS or citation-backed treatment.
- **MIT / Apache-2.0 / BSD** (GraphQL reference, Rust book, Go docs, Envoy) supports verbatim vendoring and first-party synthesis.
- **PSF license** (Python docs) permits non-commercial redistribution with attribution; treat as citation-backed to avoid license interpretation risk.
- **Proprietary / vendor-controlled** (Apple, Google, commercial gateway vendors) is generally unsuitable for source custody; prefer citation-only or drop the candidate.

## Recommended sequencing

1. `graphql` — highest confidence, clear authority, compact source, strong pack fit.
2. `go` — compact, permissive license, clear language scope.
3. `rust` — permissive license, structured source, but slightly larger than `go`.
4. `python-language` — valuable but large and version-sensitive; tackle after `go` and `rust`.
5. `kubernetes` — valuable for `engineering-pack` but large; consider citation-backed first.
6. `mobile-platforms` and `api-gateways` — defer pending narrower, licensable authority or a decision to keep as citation-only concept skills.

## Notes

- All candidates assume the same first-party skill shape used in MARK-340 through MARK-351: `SKILL.md`, `agents/openai.yaml`, `assets/authority/authority.yaml`, `assets/authority/source-map.yaml`, `assets/authority/CITATIONS.md`, and optional `assets/authority/reference-source/` for source-backed lanes.
- Pack assignments follow the pattern observed during this enrichment wave: specialist ecosystem skills move to topical packs; mega-pack `house-skills` remains the fallback for cross-cutting first-party skills.
