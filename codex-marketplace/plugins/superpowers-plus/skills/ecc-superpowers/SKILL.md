---
name: ecc-superpowers
description: Use when Superpowers+ work needs to route ECC workflow-shaped tasks to the dedicated superpowers-ecc pack while keeping the Superpowers+ router thin and compositional.
metadata:
  source-id: ecc-superpowers
  source-path: sources/first_party/skills/ecc-superpowers/SKILL.md
  provenance-name: MARK-244 ECC Superpowers compositional routing skill
license: "MIT"
---
# ECC Superpowers

Use this skill when Superpowers+ needs to hand ECC workflow-shaped work to the
dedicated `superpowers-ecc` pack instead of absorbing the ECC doctrine into the
Superpowers+ bundle.

## Core job

Shape boring, worker-send-ready ECC workflow packets so they say:

1. which ECC workflow skill is the smallest applicable fit;
2. why that skill applies;
3. what evidence will prove the workflow was followed.

## Composition

Start with `/using-superpowers` as the workflow-selection entrypoint.

When the work is ECC workflow doctrine, route it to the dedicated
`superpowers-ecc` pack and pick the smallest applicable skill there.

When the packet is plan-shaped and meant for a worker, use `/writing-plans`
for route review and `/executing-plans` as the outer execution workflow, but
keep the actual workflow slice in `superpowers-ecc`.

Use `/verification-before-completion` before claiming fixed, passing, merged,
published, or complete.

Use `/finishing-a-development-branch` when implementation is complete and
branch closeout is the actual task.

Nesting rule:

- pick the smallest specialist workflow that actually fits;
- use TDD, debugging, verification, or closeout skills only when they are the
  smallest applicable specialist workflow;
- do not stack skills just because they are available.

## Routing rules

- Keep Superpowers+ broad and compositional.
- Keep ECC-specific workflow doctrine in `superpowers-ecc`.
- Do not pull branding, social publishing, or unrelated domain-specialist
  skills into the ECC workflow pack.
- Do not treat this wrapper as a replacement for the dedicated pack.

## Authority split

This skill shapes Superpowers+ routing for ECC workflow-shaped work.
It does not implement the ECC pack, prove GitHub state, or claim publication by
itself.
