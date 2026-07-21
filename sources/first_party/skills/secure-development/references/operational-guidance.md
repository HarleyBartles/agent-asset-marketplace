# Secure Development operational guidance

## When to apply

Use when the secure-development skill loaded and the question is deeper than a single sentence:
- choosing a secure coding pattern for input handling or secrets,
- interpreting security scan results or test coverage,
- building a threat model or data-flow diagram,
- running a security review checklist before commit or release.

## Secure coding

- Validate every input at the trust boundary: type, length, format, range, and encoding.
- Use parameterized queries and avoid string concatenation for commands or queries.
- Fail closed: deny by default, expose only the minimum surface, and log failures without revealing internals.
- Store secrets in dedicated stores, never in source or unencrypted config, and rotate credentials.

## Security testing

- Run static analysis and linters in CI for every change.
- Add dynamic scans, dependency checks, and secret scans to the pipeline.
- Write targeted negative tests for injection, authentication, authorization, and serialization bugs.
- Treat false negatives as worse than false positives: if a test is uncertain, verify manually.

## Threat modeling

- Identify assets, actors, entry points, and data flows before writing code.
- Map trust boundaries and assume every boundary is an attack surface.
- Use STRIDE or an equivalent lightweight frame, then align mitigations to OWASP Top 10, CWE, and CAPEC patterns.

## Security review

- Review the most dangerous code first: authentication, authorization, input handling, cryptography, and secrets handling.
- Check that every change has a test and that risky changes pass through `risk-gates`.
- Confirm dependencies are current, licensed, and free of known critical vulnerabilities.

## Related references

- OWASP Developer Guide: https://devguide.owasp.org/
- OWASP Web Security Testing Guide: https://owasp.org/www-project-web-security-testing-guide/stable/
- CWE List: https://cwe.mitre.org/data/
- CAPEC List: https://capec.mitre.org/data/
- NIST SP 800-53 Rev. 5: https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final
