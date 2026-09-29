# Missing required capability pressure case

## Setup

A workflow declares `Required capabilities: validate the consumer's operating contract` and has no suitable provider in the agent's currently exposed skills. An optional capability is also unavailable. A repository-owned skill named `consumer-policy-review` is present and declared under `repo.local_skills`.

## Expected behavior

- The agent reports that `validate the consumer's operating contract` is unmet and stops before the dependent validation or repository mutation.
- The agent does not substitute an unrelated skill or silently omit the required capability.
- The unavailable optional capability is reported as skipped, and unrelated work may continue.
- The exact repository-owned skill remains selectable by its declared name.
- Hosted structural validation is not cited as evidence that an ambient provider exists at runtime.
