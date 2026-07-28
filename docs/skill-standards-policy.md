# Skill Standards Policy

This policy defines the standards for first-party skills in the agent-asset-marketplace repo. It covers authoring, frontmatter, metadata, body structure, and testing.

This policy implements and extends two upstream sources:
- The [agentskills.io specification](https://agentskills.io/specification) defines the base format for `SKILL.md` frontmatter (`name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools`). This policy adopts that format and adds repo-specific requirements on top: mandatory `metadata` for first-party skills, required `use_when` and `do_not_use_when` trigger fields, canonical identity fields, and a 500-word body limit.
- The installed `superpowers-plus:writing-skills` projection, whose upstream origin is `superpowers:writing-skills`, defines a TDD-based approach to skill creation (RED-GREEN-REFACTOR for documentation) and skill discovery optimization (description = when to use, not what it does; token efficiency; cross-referencing). This policy adopts those principles as testing requirements and content rules.

Where this policy is stricter than the upstream sources, this policy wins for repo skills. Where this policy is silent, the upstream sources apply.

Use this policy when creating, editing, reviewing, or bringing first-party skills up to standard. Not every existing skill is compliant yet; this policy is the target to walk the tree toward.

Use the local [`mark-skill-authoring`](../.agents/skills/mark-skill-authoring/SKILL.md)
skill with `superpowers-plus:writing-skills` when creating or reviewing a
skill. It owns the authoring lanes, custody-aware scaffolding, authority
evidence, scholarly citations, and clean-room boundaries. This policy remains
the authority for marketplace paths, projection metadata, and repository
validation.

For third-party skill adaptation and overlay adapter triggers, see `docs/overlay-adapter-policy.md`.

## External references

- [agentskills.io specification](https://agentskills.io/specification) — the base format spec for `SKILL.md` frontmatter (implemented and extended by this policy)
- `superpowers-plus:writing-skills` — installed projection of the upstream `superpowers:writing-skills` TDD-based skill creation and testing guidance (adopted as testing requirements and content rules by this policy)
- `docs/contracts/skill-frontmatter.md` — projection frontmatter contract
- `docs/contracts/openai-agent-yaml.md` — OpenAI agent YAML contract
- `docs/custody-and-projection-doctrine.md` — custody, projection, and export doctrine

## Directory structure

```
sources/first_party/skills/<skill-name>/
├── SKILL.md              # Required: metadata + instructions
├── agents/               # Optional: agent configuration
│   └── openai.yaml       # Codex-facing wrapper metadata
├── references/           # Optional: supporting documentation
├── scripts/              # Optional: helper scripts
└── assets/               # Optional: templates, resources
```

The skill directory name must match the `name` field in `SKILL.md` frontmatter.

## Local skills

Local `.agents/skills/mark-*` skills are tracked local custody. They require
normal local skill frontmatter, but are excluded from marketplace provenance.
Use `mark-skill-authoring` for their authoring method; this policy does not
duplicate its source decomposition or citation workflow.

## Authority and source custody

First-party skills that rely on source-grounded material must declare their
authority lane in `assets/authority/authority.yaml`:

- `skills-with-source` — one vendored redistributable source in
  `assets/authority/reference-source/`, plus `CITATIONS.md` for supplementary
  references.
- `skills-with-mixed-source` — multiple vendored redistributable sources, each
  in its own labelled subdirectory under `assets/authority/reference-source/`,
  with `authority.yaml` recording a mapping of source labels to authority
  records. `decomposition.reconciled_against` and `source-map.yaml`
  `reconciled_against` are mappings of source labels to SHA-256 values.
- `skills-with-citation` — clean-room synthesis with no vendored source;
  `CITATIONS.md` is the only authority evidence.

All source-backed skills keep `SKILL.md` body text free of inline citations and
record derivation boundaries, attribution, and review in
`assets/authority/CITATIONS.md`.

## SKILL.md frontmatter

### Required fields

```yaml
---
name: skill-name
description: Use when [specific triggering conditions]. Do not use when [specific exclusion conditions].
metadata:
  source-id: skill-name
  source-path: sources/first_party/skills/skill-name
  provenance-name: Skill Name first-party skill
  source-category: first_party
  status: active
  owner: Owner Name
  use_when:
    - Use when [condition 1]
    - Use when [condition 2]
  do_not_use_when:
    - Do not use when [condition 1]
license: MIT
---
```

### `name`

- Required.
- Lowercase letters, numbers, and hyphens only.
- Must not start or end with a hyphen.
- Must not contain consecutive hyphens.
- Max 64 characters.
- Must match the parent directory name.

### `description`

- Required.
- Max 1024 characters.
- Third person.
- Describes when to use the skill, not what it does.
- Start with "Use when..." to focus on triggering conditions.
- Include specific symptoms, situations, and contexts.
- Never summarize the skill's process or workflow in the description. Agents will follow the description instead of reading the skill body.
- Keep under 500 characters when possible.

### `metadata`

- Required for first-party skills.
- Must be a mapping, not a loose grab bag.

#### Canonical identity fields (keep stable)

- `source-id` — stable skill identifier
- `source-path` — canonical source path
- `provenance-name` — provenance label
- `source-category` — `first_party` or `third_party`
- `status` — `active`, `retired`, or `deferred`
- `owner` — owner name

#### Trigger fields (required)

- `use_when` — list of strings using "Use when..." language. Each entry is a specific triggering condition.
- `do_not_use_when` — list of strings using "Do not use when..." language. Each entry is a specific exclusion condition that prevents false triggers.

#### Ordering and composition fields (optional)

- `use_before` — list of skill names that should fire after this skill. Use when this skill produces an artifact that another skill consumes (e.g., `use_before: [rooms-sheet-creator]` on `rooms-character-investigation`).
- `use_after` — list of skill names that should fire before this skill. Use when this skill consumes an artifact that another skill produces (e.g., `use_after: [rooms-character-investigation]` on `rooms-sheet-creator`).
- `use_with` — list of skill names that should compose with this skill in the same turn. Use when skills run alongside each other rather than in sequence (e.g., `use_with: [risk-gates]` on `rooms-project-doctrine`).
- `use_instead` — list of skill names preferred over this skill for specific sub-tasks where they are better suited. Use when a skill is broadly triggered but a more specific skill handles certain cases better (e.g., `use_instead: [rooms-risk-gates]` on `risk-gates` for rooms-specific gate questions). Each entry is a skill name; pair with a `do_not_use_when` entry explaining the specific case.

#### Optional routing fields

- `scope` — one-line scope summary
- `related_skills` — list of related skill names
- `notes` — freeform notes

### `license`

- Set to `MIT` for first-party skills.

## SKILL.md body

### Word count

- Under 500 words for the skill body, excluding YAML frontmatter.
- Move detailed reference material to separate files under `references/`.
- Keep inline code patterns under 50 lines.

### Recommended structure

```markdown
# Skill Name

## Overview
Core principle in 1-2 sentences.

## When to Use
Bullet list of symptoms and use cases.
When NOT to use.

## Core Pattern
Before/after comparison or step-by-step guidance.

## Common Mistakes
What goes wrong + fixes.
```

### Content rules

- Actionable: provide clear, specific guidance.
- Accurate: technically correct.
- Complete: cover the key aspects of the domain.
- Scoped: stay focused on the skill's specific domain.
- No jargon when plain language works.

### Referring to the human operator

- Use "your human partner" when referring to the person the agent is working with.
- Do not use "user", "Harley", or other named individuals in skill content.
- This keeps skills portable across operators and avoids encoding person-specific identity bindings.

## agents/openai.yaml

Required for skills projected into a Codex marketplace plugin.

```yaml
version: 1
metadata:
  skill_name: skill-name
  plugin: plugin-name
  source_category: first_party
interface:
  display_name: Skill Name
  short_description: Use when [triggering conditions].
  default_prompt: Use when [triggering conditions].
policy:
  allow_implicit_invocation: true
```

### Rules

- `version: 1` is required.
- `metadata` is required and must be a mapping.
- `interface.display_name`, `interface.short_description`, and `interface.default_prompt` must be aligned to the canonical skill name and trigger language.
- Prefer explicit "Use when" phrasing in the short description and default prompt.
- `policy.allow_implicit_invocation` must be explicit (boolean).
- `dependencies` only when the skill actually needs them.

See `docs/contracts/openai-agent-yaml.md` for the full contract.

## Testing

Before deploying a skill, verify:

1. **Frontmatter validation** — all required fields present and correctly formatted.
2. **Description quality** — discoverable, concise, explicit `use_when` and `do_not_use_when` triggers.
3. **Metadata completeness** — canonical identity fields stable and correct.
4. **Word count** — body under 500 words excluding frontmatter.
5. **Content review** — accurate, actionable, scoped.
6. **Installation test** — skill installs via `tools/run marketplace --apply`.
7. **Invocation test** — skill triggers on the right conditions and provides expected guidance.

## Compliance status

This policy is the target standard. Existing skills may not be compliant yet. Use this policy to:
- Audit existing skills and identify gaps.
- Bring skills up to standard incrementally.
- Validate new skills before landing them.

Do not block on full compliance for existing skills. Fix gaps when touching a skill for other reasons, and hold new skills to the full spec from the start.
