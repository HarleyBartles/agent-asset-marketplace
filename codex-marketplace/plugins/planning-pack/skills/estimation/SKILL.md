---
name: estimation
description: Use when estimating effort, risk, and uncertainty for sprints, milestones, or releases.
metadata:
  source-id: estimation
  source-path: sources/first_party/skills/estimation/SKILL.md
  provenance-name: Estimation first-party skill
  source-category: first_party
  status: active
  owner: Harley Bartles
  scope: Use when estimating effort, risk, and uncertainty for sprints, milestones, or releases.
  use_when:
  - Use when planning sprints, milestones, or releases.
  - Use when comparing candidate approaches by effort and risk.
  - Use when communicating confidence and buffer to stakeholders.
  - Use when reviewing estimates against actuals to calibrate.
  do_not_use_when:
  - Do not use when another more specific skill owns the task.
  related_skills:
  - requirements-elicitation
  - risk-gates
  - writing-with-clarity
license: MIT
---

# Estimation

## Overview

Estimation predicts effort, risk, and uncertainty so teams can plan without promising false precision.

## When to Use

- Planning sprints, milestones, or releases.
- Comparing candidate approaches by effort and risk.
- Communicating confidence and buffer to stakeholders.
- Reviewing estimates against actuals to calibrate.

Do not use when another more specific skill owns the task.

## Core Pattern

1. Break work into small, comparable units; prefer historical data over intuition.
2. Estimate in ranges or confidence intervals, not single points.
3. Apply risk buffers for unknowns, dependencies, and integration complexity.
4. Use team-based methods (planning poker, affinity grouping) to reduce individual bias.
5. Document assumptions and compare actuals; update the team's baseline.
6. Separate effort from duration: account for availability, interrupts, and dependencies.

## Common Mistakes

- Padding estimates in secret → make uncertainty explicit with ranges.
- Ignoring risk and integration work → add buffers proportional to unknowns.
- Treating estimates as commitments → communicate probability, not guarantee.

Load `references/operational-guidance.md` for deeper coverage of COCOMO, Agile estimation, and risk buffer sizing.
