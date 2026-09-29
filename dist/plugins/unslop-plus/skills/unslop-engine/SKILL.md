---
name: unslop-engine
description: Use when observed AI output defaults in a domain are repetitive and you need a durable anti-slop profile to counter them.
metadata:
  source-id: unslop-engine
  source-path: skills/unslop-engine/SKILL.md
  provenance-name: Unslop Engine first-party skill
  source-category: first_party
  status: active
  owner: Harley Bartles
  use_when:
    - generating a domain-specific anti-slop profile from samples or observed defaults.
  do_not_use_when:
    - applying an existing anti-slop profile to a task.
  related_skills:
    - unslop-profiles
license: MIT
---

# Unslop Engine

## When to Use

Use this skill when you need to empirically detect repetitive AI output patterns in a domain and generate a reusable anti-slop profile.

Do not use this skill when applying an existing anti-slop profile; use `unslop-profiles` instead.

## Profile Lifecycle

Use this engine to help a consumer maintain operational profiles when repeated evidence reveals a durable opportunity to prevent a recurring failure. Treat one mistake as a signal to inspect, not as authority to rewrite a profile. A proposed profile, revision, or retirement must be reviewable by the consumer; do not edit or publish a consumer profile automatically.

Create or revise guidance only when the evidence supports a recurring pattern and a useful intervention. Distill it into operational guidance: a task trigger and scope, recurring failure pattern, recognition cues, corrective behavior, false-positive and override boundaries, applicable workflow routes, authoritative doctrine or skill references, and an application example. Do not accumulate incident notes or restate doctrine's binding rules. The consumer decides whether to accept the proposal.

Retire a profile when it has no reader or its useful guidance has been absorbed into an authoritative standard, doctrine, skill, or workflow. Explain the evidence and proposed destination so the consumer can review the retirement.

Follow the adopted Unslop standard's profile shape and contract when working in a consumer repository. When the consumer adopts the standard, read its deployed copy at `.agents/standards/unslop/references/unslop-standard.md`. If the consumer has not adopted it, use the operational profile shape described above; do not assume a Marketplace source checkout is present.

## Validation Boundary

The engine's sample analysis identifies repeated wording and structures in the supplied samples. Generated-package validation checks the output package's structure and content constraints. Neither determines whether an agent followed or violated a profile in real work. Assess real work through profile-guided review grounded in concrete output or decisions, unless a specific deterministic check has been defined for the behavior. Report only what the evidence supports.

## Core Pattern

1. Identify the domain and whether you are analyzing text or visual samples.
2. Collect representative samples (inline, fixture files, or a sample directory).
3. Resolve the active installed `unslop-engine` skill directory from the loaded skill path. Run its bundled script by that path; never resolve `scripts/unslop.py` from the consumer repository's working directory. In this Marketplace source checkout, the script is `skills/unslop-engine/scripts/unslop.py`.
   ```bash
   py -3 "<active-unslop-engine-skill-directory>/scripts/unslop.py" --apply --domain "..." [--type visual --count N]
   ```
4. Review the generated artifacts in `unslop-output/` in the consumer repository:
   - `analysis.md` — counted repeated patterns
   - `skill.md` — generated anti-slop profile
5. Return the profile name, the dominant repeated patterns, and how to use the profile.

When the request concerns a consumer profile, use recurring evidence to prepare a reviewable creation, revision, or retirement proposal. Keep raw samples and incident notes outside the profile; the profile should express reusable recognition and corrective guidance.
