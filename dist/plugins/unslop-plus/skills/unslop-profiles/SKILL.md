---
name: unslop-profiles
description: Use when a task route or recurring failure cue indicates that operational anti-slop guidance may apply, to find, read, and apply matching consumer or generic profiles during work and review.
metadata:
  source-id: unslop-profiles
  source-path: skills/unslop-profiles/SKILL.md
  provenance-name: Unslop Profiles first-party skill
  source-category: first_party
  status: active
  owner: Harley Bartles
  use_when:
    - a repository workflow routes the current task to an operational profile.
    - a software task fits a bundled generic profile and profile guidance would improve the result.
    - a recurring profile failure cue appears in actual work or review.
  do_not_use_when:
    - no available profile's trigger and scope fit the task.
    - proposing or maintaining profile content from recurring evidence; use unslop-engine.
  related_skills:
    - unslop-engine
    - writing
license: MIT
---

# Unslop Profiles

Find and apply operational profiles when a workflow route or task trigger indicates that one fits. A profile describes a recurring failure pattern, cues that reveal it, and corrective behavior. It guides judgment; it is not a keyword filter, repository policy, or an automatic requirement for unrelated work.

## Discover the applicable profiles

1. Read the current task and any applicable workflow route. Identify the profile's declared trigger and scope before deciding it applies.
2. If the consumer explicitly adopts the `unslop` Operating Model standard in `.agents/contracts/operating-standards.json`, read `.agents/contracts/unslop.json` and search only its declared `profile_roots` for Markdown profiles. The default root is `.agents/unslop`. Read each matching consumer profile before using it. Do not infer adoption from a directory or ambient plugin alone.
3. Find matching bundled profiles under `references/profiles/` using the task map below, then read each profile that fits. The consumer standard and Unslop+ are independently optional: use available generic profiles if the consumer standard is absent, and use consumer profiles when exposed by the adopted standard even when Writing Pack is unavailable.
4. Apply only profiles whose triggers and scopes fit. Multiple compatible profiles may guide the same task. Preserve each profile's source and scope; do not silently reconcile conflicting guidance. Doctrine, evidence, user intent, and task requirements bound every profile.
5. If no profile fits, skip profile application. Do not force a nearby profile onto the work.

| Task scope                                           | Bundled profile                               |
| ---------------------------------------------------- | --------------------------------------------- |
| General prose and short user-facing writing          | `references/profiles/writing.md`              |
| Technical documentation and operational explanations | `references/profiles/technical-writing.md`    |
| Implementation plans and coding handoffs             | `references/profiles/implementation-plans.md` |
| Code review                                          | `references/profiles/code-review.md`          |
| Worker returns                                       | `references/profiles/worker-returns.md`       |
| Debugging                                            | `references/profiles/debugging.md`            |
| React frontend work                                  | `references/profiles/frontend-react.md`       |
| Generic UI design                                    | `references/profiles/frontend-ui.md`          |
| API design                                           | `references/profiles/api-design.md`           |
| Architecture decisions                               | `references/profiles/architecture.md`         |
| Test design and review                               | `references/profiles/testing.md`              |
| Security review                                      | `references/profiles/security-review.md`      |
| Repository cleanup and custody                       | `references/profiles/cleanup-custody.md`      |

## Apply during work and review

- Read a profile before relying on its cues or corrective moves. Do not apply a remembered summary in place of the current file.
- Use the cues to inspect actual text, code, tests, or decisions as the task progresses. At completion, review the relevant result against the matching profile.
- Ground each finding in the exact output or decision that exhibits the profile's failure pattern. Explain the mismatch, then make or recommend a proportionate correction.
- Preserve meaning, accuracy, clarity, evidence, and task intent. A cue is not proof by itself. Keep intentional examples, quotations, defined terminology, and precise domain language when the profile's own boundaries or the task context justify them.
- Do not mechanically delete a word, reshape prose, or add ceremony solely to satisfy a profile. A profile correction must improve the actual result.
- When profiles appear to conflict, identify the conflicting guidance and its scope. Follow authoritative doctrine and the user's requirements; surface a material unresolved conflict instead of silently merging the profiles.
- For sustained prose, use the `writing` workflow when that capability is available. The generic writing profile remains available for a narrow review or when no suitable writing provider is available.

## Boundaries

Profiles are operational guidance, not binding doctrine, contracts, or a complete history of past mistakes. They may link to authoritative doctrine and skills but do not replace them. This skill's discovery and application does not certify that work complied with a profile. State adherence only as a profile-guided review judgment grounded in the work; use a deterministic claim only when a separately defined check provides that evidence.
