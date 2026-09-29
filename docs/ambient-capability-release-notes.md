# Marketplace release notes: ambient capabilities and selectable standards

This source release separates agent capabilities from consumer repository policy.

- Superpowers+ provides workflow composition; Repo Worker Pack provides general repository-work capabilities; MCP Usage Pack guides use of tools exposed in the current runtime; Unslop+ provides optional writing-quality capabilities; Agent Operating Model publishes independently selectable standards.
- Installing an ambient plugin does not subscribe a repository to it or adopt its standards. A repository declares only the standards it wants, including no marketplace standards.
- Runbooks and playbooks state required and optional capabilities. Agents select suitable skills from those currently exposed. If a required capability is unavailable, dependent work stops and the unmet need is reported. Exact names are reserved for genuine repository-owned skills declared through `repo.local_skills`.
- Hosted structural validation checks authored contracts, declared local-skill custody, and composition graphs. It does not claim ambient skills are installed in CI.
- Generated index mesh files and commands have been retired with no replacement.

Consumers should use the exact merged source commit SHA from the release handoff as their `marketplace-source` revision. Follow the [consumer runner migration guide](../skills/repo-shape/references/consumer-runner-migration.md) before removing copied ambient plugins or changing refresh and mesh calls. In particular, keep old subscriptions until the runner and tracked hook have completed the coherent cutover.

For this release, pin marketplace source revision `b5ba27face374e86ca99fcce9da5b61d04c3ea69` (PR #338).
