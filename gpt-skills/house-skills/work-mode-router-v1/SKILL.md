# Work Mode Router v1

Use this skill for the first turn of a task when the main question is which House Skills lane should handle it.

This skill is the router. It chooses the right doctrine, the right task skill, or the right repo playbook before deeper work starts. It does not perform the work itself.

## Core rule

Classify the request once, then route to the most specific live capability. Do not rediscover routing that already exists in the repo.

## Boundaries

- It does not mutate repos.
- It does not dispatch workers.
- It does not validate or package skills.
