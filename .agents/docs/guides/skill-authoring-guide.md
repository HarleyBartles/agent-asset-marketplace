# Skill Authoring Guide

Use this reference when writing, editing, or testing skills in the agent-asset-marketplace repo. This guide covers skill structure, metadata standards, and testing requirements.

## Before You Begin: Read the Standards

- **[`docs/skill-standards-policy.md`](../../../docs/skill-standards-policy.md)** — first-party skill authoring standards
- **[`docs/overlay-adapter-policy.md`](../../../docs/overlay-adapter-policy.md)** — third-party overlay and adapter triggers
- **[`sources/AGENTS.md`](../../../sources/AGENTS.md)** — first-party skill source format
- **[`../writing-skills`](../../skills/writing-skills)** — skill creation and testing guidance

## Skill Structure

### First-Party Skills

First-party skills live under `sources/first_party/skills/<skill-name>/`:

```
sources/first_party/skills/<skill-name>/
├── SKILL.md              # Skill definition and documentation
├── agents/               # Optional: agent configuration
│   └── openai.yaml       # Codex-facing wrapper metadata
├── references/           # Optional: supporting documentation
└── scripts/              # Optional: helper scripts
```

### SKILL.md Frontmatter

Required frontmatter fields:

```yaml
---
name: skill-name
description: Discoverable, concise description with use when/do not use when triggers
metadata:
  source-id: skill-name
  source-path: sources/first_party/skills/skill-name
  provenance-name: Skill Name first-party skill
  source-category: first_party
  status: active
  owner: Owner Name
  scope: Use when this skill applies
  use_when:
  - Use when condition 1
  - Use when condition 2
  do_not_use_when:
  - Do not use when condition 1
license: MIT
---
```

Keep canonical identity fields stable:
- `source-id`
- `source-path`
- `provenance-name`
- `source-category`
- `status`
- `owner`

Additional fields for routing and provenance:
- `scope`
- `use_when`
- `do_not_use_when`
- `related_skills`
- `notes`

### agents/openai.yaml

Use it for Codex-facing wrapper metadata:

- Keep `interface.display_name`, `interface.short_description`, and `interface.default_prompt` aligned to the canonical skill name and trigger language
- Prefer explicit `use when` phrasing in the short description and default prompt
- Keep `policy.allow_implicit_invocation` explicit
- Add dependencies only when the skill actually needs them

## Skill Testing

### Testing Requirements

Before deploying a skill, verify:

1. **Frontmatter validation** — all required fields are present and correctly formatted
2. **Description quality** — description is discoverable, concise, and includes explicit `use when` and `do not use when` triggers
3. **Metadata completeness** — canonical identity fields are stable and correct
4. **Content review** — skill content is accurate, actionable, and follows repo standards
5. **Installation test** — skill installs correctly via marketplace regeneration
6. **Invocation test** — skill can be invoked and provides expected guidance

### Testing Process

1. Write the skill in `sources/first_party/skills/<skill-name>/`
2. Run marketplace regeneration: `py -3 tools/rebuild_marketplace.py`
3. Verify skill appears in generated marketplace plugins
4. Verify skill installs to `.agents/skills/` via `py -3 tools/install_agent_skills.py`
5. Test skill invocation in a test session
6. Verify skill provides expected guidance

## Skill Updates

### Targeted Skill Updates

For targeted skill updates, use:
```bash
py -3 tools/update_skill_artifacts.py --skill <pack>/<skill>
```

This updates a specific skill without full marketplace regeneration.

### Full Regeneration

For changes that affect multiple skills or marketplace structure:
```bash
py -3 tools/rebuild_marketplace.py
```

This is the canonical completion path for source-changing work.

## Skill Quality Standards

### Description Quality

- **Discoverable** — skill name and description make it clear when to use the skill
- **Concise** — description is brief but includes key triggers
- **Explicit triggers** — includes `use when` and `do not use when` conditions
- **No jargon** — avoids unnecessary technical jargon when plain language works

### Content Quality

- **Actionable** — skill provides clear, specific guidance
- **Accurate** — skill content is technically correct
- **Complete** — skill covers the key aspects of its domain
- **Scoped** — skill stays focused on its specific domain

### Metadata Quality

- **Stable identity** — canonical identity fields don't change unnecessarily
- **Rich routing** — metadata includes routing information (scope, use_when, do_not_use_when)
- **Provenance** — metadata includes provenance information (source, owner, status)

## Common Pitfalls

### Avoid

- Vague descriptions that don't specify when to use the skill
- Overlapping skills that have unclear boundaries
- Skills that are too broad and try to cover too much
- Skills that are too narrow and have no practical use
- Missing or incomplete frontmatter
- Unstable canonical identity fields

### Prefer

- Clear, specific `use when` and `do not use when` conditions
- Well-defined skill boundaries
- Focused skills that cover a specific domain
- Practical skills that solve real problems
- Complete, accurate frontmatter
- Stable canonical identity fields
