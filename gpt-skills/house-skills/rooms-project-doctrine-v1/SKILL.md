# Rooms Project Doctrine v1

Use this skill as the shared doctrine store for Rooms work that is not owned by a more specific Rooms skill.

This skill keeps the Rooms truth domains, actor boundaries, and repository posture in one place. It does not own dispatch, QA, or publication by itself.

## Core rule

Keep Rooms truth domains first-class and do not flatten them into generic repo language.

## Boundaries

- It does not own source partitioning.
- It does not own issue closure.
- It does not replace more specific Rooms skills.
