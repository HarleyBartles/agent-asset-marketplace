---
name: requirements-elicitation
description: Use when eliciting, validating, or documenting requirements, user stories, and acceptance criteria.
metadata:
  source-id: requirements-elicitation
  source-path: codex-marketplace/plugins/planning-pack/skills/requirements-elicitation/SKILL.md
  provenance-name: Requirements Elicitation first-party skill
  source-category: first_party
  status: active
  owner: Harley Bartles
  scope: Use when eliciting, validating, or documenting requirements, user stories, and acceptance criteria.
  use_when:
  - Use when starting a feature, project, or iteration.
  - Use when interviewing stakeholders or domain experts.
  - Use when translating needs into user stories and acceptance criteria.
  - Use when reviewing requirements for ambiguity or missing acceptance criteria.
  do_not_use_when:
  - Do not use when another more specific skill owns the task.
  related_skills:
  - estimation
  - risk-gates
  - writing-with-clarity
license: MIT
---

# Requirements Elicitation

## Overview

Good requirements start with what users need, not what the system will do. Elicit, validate, and document expectations before design.

## When to Use

- Starting a feature, project, or iteration.
- Interviewing stakeholders or domain experts.
- Translating needs into user stories, acceptance criteria, or acceptance tests.
- Reviewing requirements for ambiguity, conflicts, or missing acceptance criteria.

Do not use when another more specific skill owns the task.

## Core Pattern

1. Identify stakeholders and their goals; separate wants from constraints.
2. Ask open-ended questions, then converge with "what does success look like?"
3. Record findings as user stories (As a <role>, I want <goal>, so that <why>).
4. Define acceptance criteria using Given/When/Then or concrete success measures.
5. Validate with stakeholders and prototypes before committing to implementation.
6. Trace changes: keep requirements linked to decisions, tests, and releases.

## Common Mistakes

- Writing solutions instead of needs → describe the problem or outcome, not the UI control.
- Vague acceptance criteria → replace "fast" or "user-friendly" with measurable thresholds.
- Skipping stakeholder review → validate early and update the record as understanding improves.

Load `references/operational-guidance.md` for deeper coverage of interview techniques, story splitting, and acceptance criteria.
