---
name: secure-development
description: Use when designing, writing, reviewing, or testing code and the task
  calls for secure coding, security testing, threat modeling, or security review guidance.
metadata:
  source-id: secure-development
  source-path: codex-marketplace/plugins/security-pack/skills/secure-development/SKILL.md
  provenance-name: Secure Development first-party skill
  source-category: first_party
  status: active
  owner: Harley Bartles
  scope: Use when designing, writing, reviewing, or testing code and the task
    calls for secure coding, security testing, threat modeling, or security review guidance.
  use_when:
  - Use when designing, writing, or reviewing code that handles sensitive data, trust boundaries, or external input.
  - Use when selecting or interpreting security tests, threat models, or review checklists.
  - Use when a task touches OWASP Top 10, CWE, CAPEC, or NIST control categories.
  do_not_use_when:
  - Do not use when the task is purely infrastructure deployment or operations.
  - Do not use when another more specific skill owns the task.
  related_skills:
  - owasp-top-ten
  - risk-gates
license: MIT
---

# Secure Development

Use this skill to build and verify software with security built in: secure coding, testing, threat modeling, and review.

## When to Use

- Designing or reviewing code that processes external input, secrets, or crosses trust boundaries.
- Choosing security tests, interpreting scan results, or building a test plan.
- Modeling threats for a feature, API, or data flow.
- Running a security review or checklist before a commit, merge, or release.

## Core Pattern

1. **Secure by design**: validate all input, fail safely, apply least privilege, and keep secrets out of code.
2. **Map threats**: identify assets, trust boundaries, attack surface, and likely attack paths before building.
3. **Test early and often**: combine static analysis, dynamic scans, dependency checks, and targeted negative tests.
4. **Review before commit**: use a checklist, check against the OWASP Top 10 and relevant CWEs, and route high-risk findings through `risk-gates`.

## Common Mistakes

- Treating security as a final scan instead of a design constraint. → Build it in from the first sketch.
- Trusting input that crossed a boundary. → Validate, sanitize, and parameterize at every boundary.
- Storing secrets in source, logs, or environment variables that leak. → Use a secrets manager and scan for leaks.
- Relying on one test type. → Layer static, dynamic, dependency, and manual review.

Load `references/operational-guidance.md` for deeper coverage of secure coding, testing, threat modeling, and review checklists.
