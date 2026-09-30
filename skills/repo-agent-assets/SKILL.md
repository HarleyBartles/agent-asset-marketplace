---
name: repo-agent-assets
description: Use when changing repository plugin subscriptions, local skill declarations, provenance, or orphan cleanup.
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

For an explicit adoption or assessment of `repo-plugin-subscriptions`, first inspect the repository's pinned subscription and certification, then use the [standard definition](references/standard.md). Ambient skill availability does not adopt the standard.

Canonical marketplace skills live in their plugin source trees. A repository may opt into repo-scoped plugin subscriptions through the `repo-plugin-subscriptions` operating standard, which uses native harness configuration and does not copy plugin payloads or project plugin skills into `.agents/skills/`.

Repository-authored skills remain owned by the consumer. Keep exact local skill names in `repo.local_skills`, validate their `SKILL.md` frontmatter, and preserve them during Marketplace updates. Plugin availability does not select AOM standards or create repository-local skill ownership.

Marketplace publication remains outside this skill. This skill owns the consumer repository's local-skill declaration and the boundary between local skills and repo-scoped native plugin dependencies.
