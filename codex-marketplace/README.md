# Codex Marketplace

This repo keeps the active Codex plugin bundles under
`codex-marketplace/plugins/`, and the authoritative active-root list lives in
`codex-marketplace/plugin-roots.json`. `superpowers-plus` is the retained mixed
first-party workflow bundle over Superpowers source.

Editable source custody lives under `codex-marketplace/plugins/<plugin>/skills/`.
The marketplace roots under `codex-marketplace/plugins/` are the installable
surfaces.

## Layout

- `plugin-roots.json` — canonical list of active plugin roots
- `plugins/<plugin>/.codex-plugin/plugin.json` — plugin metadata
- `plugins/<plugin>/skills/<skill>/` — canonical skill source trees
- `manifest.json` — generated aggregate marketplace manifest

## Inventory

The marketplace currently offers **17 plugins** with **74 bundled skills**. The
following table is the source-of-truth inventory for what this repo vends.
Skills listed under each plugin come from that plugin's bundle manifest. The
`.agents/skills/` tree in this repo contains installed copies from the plugins
consumed here (currently `repo-worker-pack`, `superpowers-plus`, and
`mcp-usage-pack`); those are not additional vendored assets and must not be
mistaken for duplicate marketplace inventory.

| Plugin | Category | Skill count | Skills |
|---|---|---:|---|
| agentic-evaluation | Coding | 1 | agent-evaluation |
| agentic-workflows | Coding | 1 | agentic-harness |
| api-contracts-pack | Productivity | 1 | api-design |
| architecture-pack | Productivity | 7 | clean-architecture, cqrs, database-design-patterns, ddd, event-driven-systems, event-sourcing, hexagonal-architecture |
| data-platform-pack | Productivity | 1 | database-engines |
| dotnet-pack | Productivity | 1 | dotnet |
| engineering-pack | Coding | 2 | observability, release-engineering |
| feature-sliced-design | Coding | 1 | feature-sliced-design |
| frontend-pack | Productivity | 6 | feature-sliced-design, frontend-ux, playwright-testing, react, wcag, web-styling |
| language-patterns-pack | Productivity | 3 | python, python-frameworks, typescript |
| mcp-usage-pack | Productivity | 5 | using-deepwiki-mcp, using-discord-mcp, using-github-mcp, using-linear-mcp, using-playwright-mcp |
| planning-pack | Productivity | 4 | estimation, mermaid-diagramming, release-engineering, requirements-elicitation |
| repo-worker-pack | Productivity | 13 | asking-clarifying-questions, base-doctrine, cleanup-custody, connector-safety, context-safety, generating-agent-mesh, linear-issue-shaping, refreshing-installed-skills, repo-standards, repo-worker-base, risk-gates, unslop-profiles, writing-with-clarity |
| research-pack | Productivity | 1 | research-ops |
| security-pack | Productivity | 4 | owasp-top-ten, risk-gates, secure-development, web-identity |
| superpowers-plus | Coding | 21 | brainstorming, dispatching-parallel-agents, executing-plans, finishing-a-development-branch, handoff-gates, inspecting-the-environment, iterative-review, publishing-source, receiving-code-review, requesting-code-review, selecting-a-subagent, subagent-driven-development, subagent-workspace, systematic-debugging, test-driven-development, using-git-worktrees, using-superpowers-plus, verification-before-completion, writing-roadmaps, writing-plans, writing-skills |
| unslop-plus | Productivity | 2 | unslop-engine, unslop-profiles |
