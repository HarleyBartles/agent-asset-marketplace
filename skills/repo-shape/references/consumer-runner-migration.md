# Consumer Plugin Migration

The previous consumer workflow vendored the Marketplace source as a submodule and projected selected plugin skills into `.agents/skills/` through `refreshing-installed-skills`. That workflow is retired.

For Codex consumers, adopt the optional `repo-plugin-subscriptions` AOM standard. It scaffolds native repo marketplace and project configuration and validates Git-backed plugin declarations. The Codex Marketplace Upgrade action refreshes the Marketplace snapshot and installed plugin payload. A consumer tracking `ref: main` receives the published update without copying plugin files into its repository or changing the subscription declaration.

The consuming repository owns its `.agents/contracts/operating-standards.json` opt-in and its native plugin configuration. Preserve genuine repo-authored `.agents/skills/` and `repo.local_skills` entries; the plugin subscription standard does not copy, rewrite, or delete local skills.

Codex consumers must register their catalog in `.codex/config.toml` with `[marketplaces.<catalog-name>]`, `source_type = "git"`, and the Git source containing the catalog. Activation keys alone do not register it, and native Upgrade requires a Git-backed marketplace. The scaffold uses the consumer's `origin` and `main` for new configs; publish the catalog there, or temporarily override the catalog ref to the migration branch for field testing.

Perform consumer migrations in the consuming repository using the [repo plugin subscription standard](repo-plugin-subscriptions-standard.md).
