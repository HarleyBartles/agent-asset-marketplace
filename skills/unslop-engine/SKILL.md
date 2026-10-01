---
name: unslop-engine
description: Use when recurring agent mistakes or repeated output patterns have evidence that may justify creating, revising, consolidating, or retiring an operational anti-slop profile.
metadata:
  source-id: unslop-engine
  source-path: skills/unslop-engine/SKILL.md
  provenance-name: Unslop Engine first-party skill
  source-category: first_party
  status: active
  owner: Harley Bartles
  use_when:
    - an adopted repository needs a reviewable profile lifecycle proposal based on durable evidence from distinct work incidents.
    - repeated text or visual samples may help identify a reusable output pattern and corrective guard.
  do_not_use_when:
    - applying an existing anti-slop profile to a task.
  related_skills:
    - unslop-profiles
license: MIT
---

# Unslop Engine

## When to Use

Use this skill when encountered agent behavior or output samples show a possible recurring failure that a reusable operational profile could prevent.

Do not use this skill when applying an existing anti-slop profile; use `unslop-profiles` instead.

## Profile Lifecycle

Use this engine to help a consumer maintain operational profiles when encountered evidence shows a useful opportunity to prevent recurring failure. Treat one mistake as a reason to inspect candidate evidence when the repository's pinned definition requires that feedback loop, not as authority to rewrite a profile. When required by the pin, compare durable occurrence records across agents and sessions. Separate independent incidents from duplicate reports, and use known routing, reach, reading, following, and outcome evidence to understand what intervention could help. Repeated sample wording alone does not establish repeated repository behavior.

Before proposing a consumer profile change, follow the repository's explicit subscription route to the exact pinned Unslop definition. Use `repo-standards` or the repository's declared pinned-source procedure when available. A v1 adopter remains governed by its historical deployed definition and resources, including its declared profile roots; do not add newer occurrence-recording or certification duties. The selectable definition introduced at `a537f406b0cb991cbd40cc35d964f1dbf26a1e0f` requires `.agents/unslop/`, durable observations, and continuing certification. Any other pin is governed by its exact source commit and definition path. Do not substitute the current ambient definition, assume `.agents/standards/unslop/`, or run a current scaffolder as an upgrade. If the repository has not adopted the standard, do not impose its occurrence-recording or certification requirements.

Create or revise guidance when the evidence supports a reusable correction, not merely because examples share words. Distill only the operational detail this particular guard needs: the applicable task or scope, recognizable failure, corrective behavior, and boundaries that prevent false positives. Add a workflow route, authoritative reference, or example when it helps an agent find or apply the guard. Do not require fixed headings, fill empty categories, accumulate incident notes in the profile, or restate binding doctrine. Where the pinned standard or repository's own process requires durable occurrence evidence, keep it in the repository's chosen record; the consumer decides whether to accept the proposal.

Retire or consolidate a profile when evidence shows it has no reader, no longer applies, overlaps another useful guard, or its guidance has been absorbed into an authoritative standard, doctrine, skill, or workflow. Explain the evidence and proposed destination so the consumer can review the lifecycle decision.

## Validation Boundary

The engine's sample analysis identifies repeated wording and structures in the supplied samples. It does not establish distinct work incidents, profile reach, or a recurring repository behavior without supporting evidence. Generated-package validation checks the output package's structure and content constraints. Neither determines whether an agent followed or violated a profile in real work. Assess real work through profile-guided review grounded in concrete output or decisions, unless a specific deterministic check has been defined for the behavior. Report only what the evidence supports.

## Core Pattern

1. Identify the recurring failure, applicable tasks, and whether the evidence concerns repository work, text samples, visual samples, or a combination.
2. For an adopter, inspect only the resources and obligations in its pinned definition. Where the pin requires occurrence records, connect evidence to distinct incidents, remove duplicate reports from recurrence reasoning, and note when route/reach/read/follow/effect is unknown. Inspect concrete outputs or decisions; a count alone is insufficient.
3. Collect representative text or visual samples when sample analysis would help identify a pattern. Sample analysis is optional support for the evidence-based lifecycle, not a substitute for occurrence records or real-work review.
4. When analyzing samples, resolve the active installed `unslop-engine` skill directory from the loaded skill path. Run its bundled script by that path; never resolve `scripts/unslop.py` from the consumer repository's working directory. In this Marketplace source checkout, the script is `skills/unslop-engine/scripts/unslop.py`.
   ```bash
   py -3 "<active-unslop-engine-skill-directory>/scripts/unslop.py" --apply --domain "..." [--type visual --count N]
   ```
5. Review the generated artifacts in `unslop-output/` in the consumer repository when the sample script was used:
   - `analysis.md` — counted repeated patterns
   - `skill.md` — generated anti-slop profile
6. Prepare a reviewable proposal with only the operational guidance the pattern needs. Explain its evidence, scope, correction, false-positive boundary, and useful route or references. The consumer decides whether to accept it.

When the request concerns a consumer profile, use recurring evidence to prepare a reviewable creation, revision, consolidation, narrowing, or retirement proposal. When the repository records occurrences, keep that evidence and raw samples outside the profile; the profile should express reusable recognition and corrective guidance.
