---
name: repo-agent-assets
description: Use when changing repository plugin subscriptions or the custody boundary for repository-authored skills.
metadata:
  source-id: repo-agent-assets
  source-path: skills/repo-agent-assets/SKILL.md
  provenance-name: Repo Agent Assets first-party skill
  source-category: first_party
  status: active
  owner: Harley Bartles
license: MIT
---

# Repo Agent Assets

For explicit adoption or assessment, inspect the repository's pinned subscription and certification through `repo-standards`, then follow the [repo plugin subscriptions definition](references/standard.md). Ambient availability does not adopt the standard.

The standard governs installing plugins into a repository through `.agents/plugins`, declared as Git dependencies using the supported harness configuration. `.agents/skills` is reserved for skills authored and owned by that repository. There is no required `repo.local_skills` inventory. A plugin-qualified skill is available to a fresh clone only when its plugin dependency is installed in the repository.

Canonical marketplace skills remain owned by their plugin source trees. AOM standard definitions and optional deployment assets are separately pinned by subscribing repositories; this skill does not copy marketplace payloads into a local skills folder. Follow a repository's historical v1 authority when its pin identifies the older contract.

Marketplace publication and source release remain outside this skill. The repository owns its selected plugin dependencies and its own authored skills.

AOM offers optional [Codex catalog](assets/examples/marketplace.json.example), [Codex project binding](assets/examples/codex-config.toml.example), and [Devin repository dependency](assets/examples/devin-config.json.example) examples, plus an editable [declaration checker](assets/check_plugin_subscriptions.py). Examples show `ref: main` and a full immutable `sha` on separate dependencies. Select only supported harnesses and adapt every repository URL and plugin path. The checker uses only Python's standard library and requires Python 3.11 or newer for `tomllib`. It checks local syntax, Git source selectors and paths, and matching Codex registration/activation; it never fetches dependencies or proves access, authentication, or runtime availability.
