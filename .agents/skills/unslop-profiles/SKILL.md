---
name: unslop-profiles
description: Use when a software development workflow would benefit from anti-slop
  guidance for writing, documentation, implementation plans, code review, worker returns,
  debugging, React work, UI design, API design, architecture, testing, security review,
  or repository cleanup.
metadata:
  source-id: unslop-profiles
  source-path: codex-marketplace/plugins/unslop-plus/skills/unslop-profiles/SKILL.md
  provenance-name: Unslop Profiles first-party skill
  source-category: first_party
  status: active
  owner: Harley Bartles
  scope: Use when a software development workflow would benefit from anti-slop
    guidance for writing, documentation, implementation plans, code review, worker
    returns, debugging, React work, UI design, API design, architecture, testing, security
    review, or repository cleanup.
  use_when:
  - Use when writing general prose.
  - Use when writing or reviewing technical documentation.
  - Use when drafting implementation plans.
  - Use when reviewing code changes.
  - Use when writing worker return reports.
  - Use when debugging software.
  - Use when building React frontends.
  - Use when designing generic UI.
  - Use when designing APIs.
  - Use when reasoning about architecture.
  - Use when writing or reviewing tests.
  - Use when performing security reviews.
  - Use when classifying repository cleanup or custody.
  do_not_use_when:
  - Do not use when generating a new domain-specific profile.
  - Do not use as the primary workflow for sustained prose when $writing is installed.
  related_skills:
  - unslop-engine
  - writing
license: MIT
---

# Unslop Profiles

Do not apply a profile from memory. Pick the profile matching the current task and read the file before applying its avoid/prefer rules.

For sustained prose, route through `$writing` when it is installed; that workflow
composes clarity, authorised voice, fatigue review, and a final clarity gate. The
generic writing profile remains available when `$writing` is not installed or
when a caller explicitly requests the generic profile only.

| Task | Profile file |
|---|---|
| Writing general prose | `references/profiles/writing.md` |
| Technical documentation | `references/profiles/technical-writing.md` |
| Implementation plans | `references/profiles/implementation-plans.md` |
| Code review | `references/profiles/code-review.md` |
| Worker returns | `references/profiles/worker-returns.md` |
| Debugging | `references/profiles/debugging.md` |
| React frontend | `references/profiles/frontend-react.md` |
| Generic UI | `references/profiles/frontend-ui.md` |
| API design | `references/profiles/api-design.md` |
| Architecture | `references/profiles/architecture.md` |
| Testing | `references/profiles/testing.md` |
| Security review | `references/profiles/security-review.md` |
| Repository cleanup | `references/profiles/cleanup-custody.md` |
