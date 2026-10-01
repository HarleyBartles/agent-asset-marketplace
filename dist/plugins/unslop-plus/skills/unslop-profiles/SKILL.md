---
name: unslop-profiles
description: Use when a task route or recurring failure cue indicates that operational anti-slop guidance may apply, to find and apply matching profiles and record distinct evidence for an explicitly adopted consumer feedback loop.
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
    - no available profile fits, there is no explicit consumer adoption, and no recurring failure cue needs recording.
    - drafting, revising, consolidating, or retiring profile guards from evidence; follow the adopter's pinned management guide, with unslop-engine as optional proposal support.
  related_skills:
    - unslop-engine
    - writing
license: MIT
---

# Unslop Profiles

Find and apply operational profiles when a workflow route or task trigger indicates that one fits. A profile describes a recurring failure pattern, cues that reveal it, and corrective behavior. It guides judgment; it is not a keyword filter, repository policy, or an automatic requirement for unrelated work.

## Discover the applicable profiles

1. Read the current task and its applicable workflow route. Identify a profile's trigger and scope before deciding it applies.
2. Matching generic profiles can be used without AOM or a consumer subscription. When a repository route points to consumer profiles, or a relevant recurring failure may need repository-specific recording, resolve adoption through the repository's declared route. If AOM's `repo-standards` capability is available, use it to read the explicit subscription, any certification named by that subscription, and the exact immutable definition. Otherwise follow the repository's own declared route. Do not use the current catalog or installed skill version to replace pinned authority.
3. Follow only the pinned definition's consumer resources. The historical v1 definition uses `.agents/contracts/unslop.json` and its declared `profile_roots`; it does not acquire the newer occurrence-recording or certification obligations. The selectable definition introduced at `a537f406b0cb991cbd40cc35d964f1dbf26a1e0f` uses `.agents/unslop/`, durable cross-agent observations, continuing certification, and its standalone management guide. For another pin, inspect its exact definition and follow only the locations, routes, and obligations it defines. Do not infer an upgrade from the installed skill version.
4. Find matching bundled profiles under `references/profiles/` using the task map below, then read each profile that fits. Consumer adoption and Unslop+ are independently optional: use available generic profiles without AOM, and use consumer profiles when the adopted standard routes them even when Writing Pack is unavailable.
5. Apply only profiles whose triggers and scopes fit. Multiple compatible profiles may guide the same task. Preserve each profile's source and scope; do not silently reconcile conflicting guidance. Doctrine, evidence, user intent, and task requirements bound every profile.
6. If no profile fits, skip profile application. Do not force a nearby profile onto the work.

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

## Maintain an adopted repository's feedback loop

When the repository's pinned Unslop definition requires an occurrence feedback loop, and this capability is available for relevant work:

- When a concrete failure or near miss matches an existing or candidate repository pattern, inspect durable observations at the location defined by the pinned standard before adding evidence.
- Record a distinct occurrence in the repository's existing organization at the location defined by the pin, linking the task, work surface, or stable evidence that lets a later agent find it. Note whether a relevant guard was available at the work point, routed, read, followed, and effective when those facts are knowable. Keep unknown facts unknown.
- Do not add a second occurrence for duplicate comments or reports about the same underlying work. Connect distinct incidents across agents and sessions so the repository can assess recurrence later.
- Use the pinned standard's standalone management guide when it provides one to decide whether evidence warrants creating, revising, narrowing, consolidating, or retiring a guard. An available `unslop-engine` can help prepare a proposal; it does not replace the guide or the repository's review process.
- Do not turn an observation into a profile automatically. A profile is reusable corrective guidance, not an incident log or an assertion that an agent violated policy.

If the pinned definition does not require repository-specific occurrence records, do not infer them from a newer ambient skill. If no subscription exists, do not create repository-specific occurrence records or certification duties. Matching bundled generic profiles may still guide the current work without requiring AOM discovery.

## Boundaries

Profiles are operational guidance, not binding doctrine, contracts, or a complete history of past mistakes. They may link to authoritative doctrine and skills but do not replace them. This skill's discovery and application does not certify that work complied with a profile. State adherence only as a profile-guided review judgment grounded in the work; use a deterministic claim only when a separately defined check provides that evidence.
