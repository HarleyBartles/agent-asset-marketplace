# Consumer Plugin Migration

The previous consumer workflow vendored the Marketplace source as a submodule and projected selected plugin skills into `.agents/skills/` through `refreshing-installed-skills`. That workflow is retired.

For Codex consumers, adopt the optional `repo-plugin-subscriptions` AOM standard. It scaffolds native repo marketplace and project configuration and validates Git-backed plugin declarations. The Codex Marketplace Upgrade action refreshes the Marketplace snapshot and installed plugin payload. A consumer tracking `ref: main` receives the published update without copying plugin files into its repository or changing the subscription declaration.

The consuming repository owns its `.agents/contracts/operating-standards.json` opt-in and its native plugin configuration. Preserve genuine repo-authored `.agents/skills/` and `repo.local_skills` entries; the plugin subscription standard does not copy, rewrite, or delete local skills.

For Wild Bunch, use the migration handoff in the active multi-harness plugin distribution plan and perform the consumer migration in that repository.
