# Operational guidance for OWASP Top Ten

## Top 10 risks

| ID | Risk | Concise description | Prevention controls |
|---|---|---|---|
| A01:2025 | Broken Access Control | Users can act outside intended permissions. | Enforce least privilege, deny by default, server-side access checks, use mature frameworks, log access decisions. |
| A02:2025 | Security Misconfiguration | Unnecessary features, default accounts, verbose errors, missing patches. | Hardened images, minimal install, automated patch and inventory, disable unnecessary features, consistent environment config. |
| A03:2025 | Software Supply Chain Failures | Vulnerable, outdated, or malicious dependencies or build steps. | SBOM, dependency scanning, signed artifacts, private registries, lock files, vendor assessment. |
| A04:2025 | Cryptographic Failures | Sensitive data exposed or weak/inadequate cryptography. | Classify data, encrypt in transit and at rest, use current algorithms and key management, avoid custom crypto. |
| A05:2025 | Injection | Untrusted data sent to interpreters as command or query. | Parameterized queries, input validation, output encoding, limit interpreters, least privilege database accounts. |
| A06:2025 | Insecure Design | Missing or ineffective security controls by design. | Threat modeling, secure design patterns, positive access controls, integrity checks by design. |
| A07:2025 | Authentication Failures | Weak credential management or session handling. | Multi-factor authentication, strong password policy, secure session tokens, rate limiting, use identity providers. |
| A08:2025 | Software or Data Integrity Failures | Insecure deserialization, untrusted CI/CD, unsigned updates. | Sign and verify updates/deserialized data, integrity checks, trusted CI/CD pipelines, avoid unsafe deserialization. |
| A09:2025 | Security Logging and Alerting Failures | Insufficient logging, monitoring, and incident response. | Centralized structured logging, log integrity, alerting, retention, privacy-aware logging, incident playbooks. |
| A10:2025 | Mishandling of Exceptional Conditions | Errors, edge cases, or resource failures leak data or enable crashes. | Safe error handling, fail securely, resource limits, fuzz testing, no sensitive data in error messages. |

## ASVS verification route

ASVS provides three assurance levels. Map each Top 10 risk to the level that matches the application's data sensitivity and assurance target.

- **Level 1** — Baseline for every application. Verify through design review, automated scanning, and basic manual checks. Map Top 10 risks to ASVS requirements for input validation, access control, and logging.
- **Level 2** — Applications that store or process sensitive data or are exposed to significant threats. Add manual verification, positive controls, and targeted testing. Map Broken Access Control, Authentication Failures, Cryptographic Failures, and Injection to ASVS V1–V14 where applicable.
- **Level 3** — High-value, high-assurance applications. Requires architecture review, threat modeling, code review, and deep verification. Map all Top 10 risks through ASVS chapters and validate supply chain, integrity, and incident response controls.

Use the levels as a verification route, not a maturity score. Choose the level before testing and document the justification.

## Common misconfigurations and secure defaults

- Default credentials, sample data, or debug endpoints left enabled in production.
- Verbose error messages and stack traces exposed to users.
- Missing or disabled security headers (HSTS, CSP, X-Content-Type-Options).
- Unpatched dependencies and unreviewed third-party libraries.
- Overly permissive CORS or cross-origin trusts.
- Weak or missing encryption for data in transit and at rest.

Secure defaults to enforce:

- Deny by default for access and network exposure.
- Least-privilege service accounts and database roles.
- Automated dependency updates with SBOM tracking.
- Centralized, tamper-resistant logging.
- Standard cryptographic libraries and key management.
- Consistent hardening across development, staging, and production environments.
