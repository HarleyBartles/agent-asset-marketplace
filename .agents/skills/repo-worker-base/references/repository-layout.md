# Repository layout

## Read when

Read before initializing or restructuring README, AGENTS.md, doctrine, docs, plans, specifications, or scripts.

## Boundary map

One authority owns each rule. Repository doctrine owns durable policy; repository-local guides own stage-specific paths, commands, exclusions, CI, and exceptions; playbooks or runbooks own repeatable operations; skills own portable decision and technique guidance. Do not duplicate an authority's rules in a router.

Keep AGENTS.md files as thin scoped law routers and README files as human-facing explanation. Doctrine carries stable metadata identifying its owner, scope, status, and canonical home. Canonical homes are declared by the consuming repository; its explicitly retired legacy homes are forbidden for new authored content.

## Custody and proof

Local authored skills remain in their canonical repository source home. Installers, marketplace bundles, and caches are runtime surfaces and must not prune or replace authored custody. Cleanup removes stale disposable or generated surfaces only after proving their source and publication requirements survive.

Publication proof remains a GitHub-visible PR or explicitly authorized direct-main commit, not local files or generator output.

## Removing generated indexes

When a repository retires generated `INDEX.md` or `INDEX.json` files, remove the tracked generated files and their generation and validation commands from local runners, hooks, and hosted CI. Do not add a replacement subscription or generated catalog. Keep direct `AGENTS.md` routes for binding repository guidance, and let authored runbooks, playbooks, and skills remain discoverable through their declared runtime or repository paths.
