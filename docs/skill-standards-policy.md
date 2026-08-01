# Skill Standards Policy

This policy defines the standards for first-party skills in the agent-asset-marketplace repo. It covers authoring, frontmatter, metadata, body structure, and testing.

This policy is stricter than upstream sources where noted; otherwise the upstream sources apply.

- The [agentskills.io specification](https://agentskills.io/specification) defines the base `SKILL.md` frontmatter format.
- The installed `superpowers-plus:writing-skills` projection defines the TDD-based approach to skill creation and discovery optimization.

Use the first-party [`writing-skills`](../../sources/first_party/skills/writing-skills/SKILL.md) skill when creating or reviewing a skill. It owns the authoring lanes, custody-aware scaffolding, authority evidence, scholarly citations, and clean-room boundaries. See `writing-skills/references/local-and-marketplace-custody.md` and `writing-skills/references/source-grounded-authoring.md` for the authoring lanes and `writing-skills/scripts/new_skill.py` for the scaffolder.

For third-party skill adaptation and overlay adapter triggers, see `docs/overlay-adapter-policy.md`.

## External references

- [agentskills.io specification](https://agentskills.io/specification)
- `superpowers-plus:writing-skills`
- `docs/contracts/skill-frontmatter.md`
- `docs/contracts/openai-agent-yaml.md`
- `docs/custody-and-projection-doctrine.md`

## Directory structure

```
sources/first_party/skills/<skill-name>/
├── SKILL.md              # Required: metadata + instructions
├── agents/               # Optional: agent configuration
├── references/           # Optional: supporting documentation
├── scripts/              # Optional: helper scripts
└── assets/               # Optional: templates, authority
```

The skill directory name must match the `name` field in `SKILL.md` frontmatter.

## Local skills

Local `.agents/skills/mark-*` skills are tracked local custody. They require normal local skill frontmatter and are excluded from marketplace provenance. Use `writing-skills` for their authoring method.

## Authority and source custody

Source-backed skills must keep `SKILL.md` body text free of inline citations and record derivation boundaries, attribution, and review in `assets/authority/CITATIONS.md`.

Authority lanes are defined in `assets/authority/authority.yaml`:

- `skills-with-source` — one vendored redistributable source in `assets/authority/reference-source/`.
- `skills-with-mixed-source` — multiple vendored redistributable sources with `authority.yaml` mapping labels to records.
- `skills-with-citation` — clean-room synthesis with no vendored source; `CITATIONS.md` is the only authority evidence.

## SKILL.md frontmatter

See `docs/contracts/skill-frontmatter.md` for the base shape and parsing rules.

This repo adds:

- `metadata` is required for first-party skills and must be a mapping.
- `use_when` and `do_not_use_when` trigger lists are required.
- Canonical identity fields must stay stable: `source-id`, `source-path`, `provenance-name`, `source-category`, `status`, `owner`.
- Optional ordering/composition fields: `use_before`, `use_after`, `use_with`, `use_instead`.
- Optional routing fields: `scope`, `related_skills`, `notes`.
- `license: MIT` for first-party skills.
- `name` and `description` follow the agentskills.io rules; descriptions must be third-person, trigger-focused, and under 500 characters when possible.

## SKILL.md body

- Under 500 words excluding frontmatter; move detail to `references/`.
- Inline code patterns under 50 lines.
- Actionable, accurate, scoped, and free of jargon when plain language works.
- Use "your human partner" when referring to the operator; do not use "user", "Harley", or named individuals.

Move real but non-primary boundary cases to `references/scope-notes.md`. Wire them through `do_not_use_when`, a `SKILL.md` call-out, and `assets/authority/source-map.yaml` `load_when` when the skill has one.

## agents/openai.yaml

Required for skills projected into a Codex marketplace plugin.

- `version: 1` is required.
- `metadata` is required and must be a mapping.
- `interface.display_name`, `interface.short_description`, and `interface.default_prompt` must align to the canonical skill name and trigger language, using "Use when" phrasing.
- `policy.allow_implicit_invocation` must be explicit (boolean).
- Add `dependencies` only when the skill actually needs them.

See `docs/contracts/openai-agent-yaml.md` for the full contract.

## Bundled scripts

Every executable Python script bundled with a first-party skill must support the CLI contract in `.agents/specs/2026-08-04-skill-script-cli-contract-design.md`:

- `--help` prints usage, a one-line description, and the read-only or mutating classification for each flag.
- `--check` is the default mode: report what the script would do and exit `0` when no mutation is needed.
- `--apply` is the explicit mutating mode.
- `mixed` scripts must classify themselves as `mixed` in `--help`.

## Testing

Before deploying a skill, verify:

1. Frontmatter validates against the contract.
2. The description is discoverable with explicit `use_when` and `do_not_use_when` triggers.
3. Canonical identity metadata is stable and correct.
4. The body is under 500 words excluding frontmatter.
5. Content is accurate, actionable, and scoped.
6. The skill installs via `tools/run marketplace --apply`.
7. The skill triggers on the right conditions and provides the expected guidance.

## Compliance status

This policy is the target standard. Use it to audit existing skills, bring them up to standard incrementally, and validate new skills before landing. Hold new skills to the full spec from the start; do not block on full compliance for existing skills.