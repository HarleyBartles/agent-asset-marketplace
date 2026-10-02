# Optional runbook starter behavior cases

Use these cases to assess adoption decisions and routing quality, not exact wording or heading structure.

## Case A: runbook standard alone

A repository adopts `runbook-composition` and has no playbook standard or doctrine/contracts store. It asks for help making its implementation discoverable. AOM offers five lifecycle-stage examples and a checker.

## Case B: select only one stage guide

A repository already has its own design process but lacks a useful PR-stage guide. It asks to adopt only a PR runbook starter and has a local testing concern guide.

## Case C: runbook and playbook together

A repository adopts both composition standards. Its design, implementation, and PR stages all touch testing, but security only applies to a subset of changes. It asks how to connect its selected guides.

## Expected decisions

- Case A can carry all useful stage guidance inline or link to available repository material; no playbooks, doctrine store, standard inventory, or empty composition headings are implied.
- Case B may adapt only the PR stage example or author its own. The concern guide remains separate and is routed only where it helps.
- Case C keeps stage lifecycle procedure in runbooks and reusable cross-stage concern guidance in playbooks. Route relevant stages to testing and only applicable stages/tasks to security; do not create an all-to-all matrix or imply either starter set is mandatory.
- In every case, checker output covers only supplied file/link facts. Semantic category, usefulness, and non-Markdown reachability remain repository judgment.
