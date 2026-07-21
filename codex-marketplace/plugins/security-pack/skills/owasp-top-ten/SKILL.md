---
name: owasp-top-ten
description: Use when reviewing web application security risks, mapping controls to
  OWASP Top 10, or establishing an ASVS verification route. Do not use when the task
  is pen-testing execution or vendor tool selection.
metadata:
  source-id: owasp-top-ten
  source-path: sources/first_party/skills/owasp-top-ten/SKILL.md
  provenance-name: Owasp Top Ten first-party skill
  source-category: first_party
  status: active
  owner: Harley Bartles
  scope: Review web application security risks, map controls to the OWASP Top 10,
    and establish an ASVS verification route.
  use_when:
  - Use when reviewing web application security risks.
  - Use when mapping controls to OWASP Top 10.
  - Use when establishing an ASVS verification route.
  do_not_use_when:
  - Do not use when the task is pen-testing execution.
  - Do not use when the task is vendor tool selection.
  related_skills:
  - security-review
  - threat-modeling-techniques
  - safety-guard
license: MIT
---

# OWASP Top Ten

Use this skill to review web application security risks, map controls to the OWASP Top 10, and establish an ASVS verification route. The operational guidance lives in `references/operational-guidance.md`.

## When to use

- Use when reviewing web application security risks.
- Use when mapping controls to OWASP Top 10.
- Use when establishing an ASVS verification route.

Do not use for pen-testing execution or vendor tool selection.

## Core pattern

1. Identify the OWASP Top 10 categories that apply to the application or change.
2. Pick prevention controls for each risk from the reference guide: least privilege, input validation, secure defaults, centralized authentication, output encoding, dependency verification, structured logging, and cryptographic hygiene.
3. Map controls to the right ASVS verification level:
   - Level 1 — all applications; verified by design review and automated checks.
   - Level 2 — applications with sensitive data; adds manual testing and positive controls.
   - Level 3 — high-value, high-assurance applications; requires architecture review, threat modeling, and deep verification.
4. Record secure defaults and common misconfigurations to address before verification.

## Common mistakes

- Treating the Top 10 as a flat checklist instead of a risk-prioritization tool.
- Applying ASVS Level 3 to every system regardless of data sensitivity.
- Relying on tools without design or code review.
- Ignoring supply-chain and integrity controls when dependencies are involved.
