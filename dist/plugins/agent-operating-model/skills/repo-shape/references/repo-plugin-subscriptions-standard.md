# Repo Plugin Subscriptions Standard

This optional AOM standard lets a repository declare plugins that its agent harness loads in that repository and its worktrees. The plugin source remains a Git dependency; the consumer does not vendor its payload or copy plugin skills into `.agents/skills/`.

## Opt in

Add `repo-plugin-subscriptions` to `.agents/contracts/operating-standards.json`. The standard scaffolds missing native config files and validates them. The consumer owns and may edit the resulting files. Applying the scaffold never overwrites an existing config.

When creating `.codex/config.toml`, the scaffold registers the consumer catalog using its marketplace name and the consumer repository's Git `origin` URL, tracking `main`. A missing or invalid Git origin must be corrected before scaffolding. Existing configs need the registration below added by the consumer if it is missing.

## Codex

Declare each plugin in `.agents/plugins/marketplace.json` using `source.source: "git-subdir"`, the Git repository `url`, the plugin-relative `path`, and exactly one selector: a floating `ref` such as `main`, or a fixed `sha`. Codex reads repo activation from `.codex/config.toml`; its `[plugins]` entries use the `plugin-name@marketplace-name` key and `enabled = true`. Every activation key must resolve to a declared plugin and marketplace.

Register the catalog in the same `.codex/config.toml` under `[marketplaces.<name>]`, where `<name>` matches the catalog's `name`. For example, a consumer named `wild-bunch` registers its own Git repository, which contains `.agents/plugins/marketplace.json`:

```toml
[marketplaces.wild-bunch]
source_type = "git"
source = "https://github.com/HarleyBartles/wild-bunch.git"
ref = "main"

[plugins."architecture-pack@wild-bunch"]
enabled = true
```

An activation key alone does not register the catalog. A local catalog registration cannot use native Marketplace Upgrade; this standard requires Git registration. The catalog Git source and ref identify the consumer's published catalog, while each catalog entry independently identifies the upstream plugin Git source and selector. Publish the catalog on the registered ref before relying on discovery or Upgrade. To field-test an unpublished consumer branch, temporarily override the catalog ref to that branch.

Codex's native `codex plugin marketplace upgrade <marketplace-name>` refreshes the managed marketplace and installed plugin payload. For a consumer tracking `main`, that refresh picks up new commits without changing the consumer declaration. A fixed `sha` remains pinned until the consumer changes it.

## Devin

`.devin/config.json` is scaffolded as a native repo configuration starting point. Repositories may add Devin-native `requiredPlugins`, `optionalPlugins`, or `forbiddenPlugins` declarations when they choose to use Devin. This standard does not install plugins at user scope and does not invoke Devin's global plugin update command.

## Validation and ownership

`repo-standards --check --standard repo-plugin-subscriptions` validates local config syntax, matching Git marketplace registration, and references without network access. It does not prove the registered remote contains the catalog. Plugin paths must start with `./`, such as `./plugins/game-studio` or `./dist/plugins/architecture-pack`, and contain no parent traversal. After removing `./`, they must remain relative under both Windows and POSIX syntax: absolute paths, drive-qualified paths (including drive-relative paths), rooted paths, and UNC paths are rejected on every host. A plugin name may be declared only once. Existing `.agents/skills/` and the `repo.local_skills` list remain consumer-owned; the standard neither projects plugin skills nor removes local skills.
