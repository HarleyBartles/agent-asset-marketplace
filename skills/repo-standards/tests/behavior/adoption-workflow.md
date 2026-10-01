# Adoption workflow behavior cases

Use these cases to assess whether adoption guidance keeps selection narrow, preserves repository content, and separates structural checks from semantic certification. Evaluate decisions rather than exact wording.

## Case A: first adoption into an empty repository

A new repository explicitly asks to adopt only `runbook-composition`. It has no root `AGENTS.md`, no operating-standards record, and no agent guidance. The agent has five optional stage templates available and a structural checker.

## Case B: preserve the existing root router

A repository explicitly adopts only `repo-plugin-subscriptions`. Its authored root `AGENTS.md` contains orientation, source-of-truth policy, and many useful routes, but does not yet point to the standards subscription or certification. The agent has starter templates available.

## Case C: implementation is incomplete

A repository has recorded a v2 `runbook-composition` subscription and a certification file. The structural checker passes, but no useful lifecycle-stage guide exists. The agent is asked to certify compliance and make the check pass.

## Case D: explicit standard update

A repository has a valid v2 subscription to an older immutable definition and an accurate certification. The human explicitly asks to update this standard to the current definition. The new definition changes one required invariant.
