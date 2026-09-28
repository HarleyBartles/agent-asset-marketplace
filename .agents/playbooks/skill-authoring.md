# Skill Authoring Playbook

## When

Use when creating or changing a marketplace skill.

## Required skills

- `writing-skills`
- `verification-before-completion`

## Composition

Apply the named capability skills under the binding doctrine and local evidence requirements. This playbook does not own a lifecycle stage.

## Doctrine and contracts

- [Skill standards policy](../doctrine/skill-standards-policy.md)

## Local commands and paths

Canonical marketplace skills live under `codex-marketplace/plugins/<plugin>/skills/<skill>/`; repository-local skills use `.agents/skills/<skill>/` and exact `repo.local_skills` registration. Read `writing-skills/references/local-and-marketplace-custody.md` and `source-grounded-authoring.md` when custody or source decomposition matters.

Scaffold through `writing-skills/scripts/new_skill.py`, regenerate marketplace-wide changes with `py -3 tools/run.py marketplace --apply`, and refresh installed skills through the canonical marketplace target. MCP wrapper skills use the `using-<x>-mcp` name, a reference router, `agents/openai.yaml`, an icon, and a tool-surface reference.

For a targeted marketplace skill update, run `py -3 tools/update_skill_artifacts.py --skill <pack>/<skill>`. After adding or moving an MCP-wrapper skill, run `py -3 tools/new_plugin.py --sync mcp-usage-pack` before the marketplace and installed-skill refreshes.

## Evidence contract

Frontmatter, references, scripts, provenance, bundle manifests, installed projections, and focused tests agree.

## Prohibited combinations

Do not edit generated installed skills as source.

## Runbook routing

- [Implementation](../runbooks/implementing.md)
- [Code review](../runbooks/code-review.md)
