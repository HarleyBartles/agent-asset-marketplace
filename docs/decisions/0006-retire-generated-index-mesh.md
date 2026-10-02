# ADR 0006: Retire the generated index mesh

**Status:** Accepted

## Context

The generated Markdown and JSON index mesh produced many files and runner steps for limited navigation value. Repository routers and direct file search provide sufficient access to the authored guidance and skills.

## Decision

Remove the index-mesh skill, its Markdown and JSON generators and validators, their runner and CI integrations, and every tracked generated `INDEX.md` and `INDEX.json` artifact. Do not replace the mesh with another generated index or subscription. Keep product manifests and registries that describe marketplace packages; they are build inputs, not navigation artifacts.

## Consequences

Repository guidance routes directly through `AGENTS.md`, authored runbooks, playbooks, and skill metadata. Consumers remove mesh generation and validation calls and delete generated index files when they migrate to a marketplace revision without the mesh. Existing link validation remains available independently of index generation.

## Current authority

Root and scoped repository routers, authored runbooks and playbooks, and skill metadata define current direct routing. AOM standards are pinned in Git and implemented by the adopting repository; old consumer migration artifacts remain available at their historical commits.
