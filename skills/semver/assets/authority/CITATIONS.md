# Authority Record for semver

## Scholarly citation

- Tom Preston-Werner. "Semantic Versioning 2.0.0." https://semver.org/spec/v2.0.0.html (accessed 2026-10-08). The specification is licensed under CC BY 3.0.

## Derivation boundary

- Derived from the specification: declaring a public API; normal and prerelease syntax; precedence; immutable released contents; major, minor, and patch meanings; initial development; and the relationship between prerelease and stable versions.
- Original AOM additions: exactly one authored product-version source per independently versioned product; explicit build propagation to required identity copies; checks for missing, stale, malformed, conflicting, or separately authored product identities; and truthful self-certification.
- Original joint Gitflow/SemVer additions: one `dev.N` identity per ordinary development merge and per reconciliation into continuing development, no checkpoint on each commit inside a PR, unique checkpoint allocation, `rc.N` progression for changed qualified candidates, and reconciliation behavior that distinguishes the stable baseline from continuing development.
- Independent schema, payload, dependency, and product versions retain their own authorities; the SemVer version of this product does not replace them.
- Outside scope: a required branch model, file format, build tool, command bus, CI provider, tag prefix, artifact host, or shared versioning script.

## Attribution

- Clean-room first-party synthesis under MIT. The normative source is linked above; no specification text is vendored or copied into operational guidance.

## Human review

- The current SemVer 2.0.0 specification and its initial-development, 1.0.0, and tag FAQ sections were opened and reviewed for this change on 2026-10-08.
- Human approval of this implementation and certification of any adopting repository remain pending.

## Authority record integrity

- The `content_sha256` value in `authority.yaml` and the `reconciled_against` values in `authority.yaml` and `source-map.yaml` are the SHA-256 of this `CITATIONS.md` file.
