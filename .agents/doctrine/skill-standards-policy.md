# Skill Standards Policy

This policy defines the standards for first-party skills in the agent-asset-marketplace repo. It covers authoring, frontmatter, metadata, body structure, and testing.

This policy is stricter than upstream sources where noted; otherwise the upstream sources apply.

- The [agentskills.io specification](https://agentskills.io/specification) defines the base `SKILL.md` frontmatter format.
- The installed `superpowers-plus:writing-skills` plugin skill defines the TDD-based approach to skill creation and discovery optimization.

Use the first-party [`writing-skills`](../../codex-marketplace/plugins/superpowers-plus/skills/writing-skills/SKILL.md) skill when creating or reviewing a skill. It owns the authoring lanes, custody-aware scaffolding, authority evidence, scholarly citations, and clean-room boundaries. See `writing-skills/references/local-and-marketplace-custody.md` and `writing-skills/references/source-grounded-authoring.md` for the authoring lanes and `writing-skills/scripts/new_skill.py` for the scaffolder.


## External references

- [agentskills.io specification](https://agentskills.io/specification)
- `superpowers-plus:writing-skills`
- `.agents/docs/contracts/skill-frontmatter.md`
- `.agents/docs/contracts/openai-agent-yaml.md`
- `custody-and-marketplace-doctrine.md`

## Directory structure

```
codex-marketplace/plugins/<plugin-pack>/skills/<skill-name>/
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

See `.agents/docs/contracts/skill-frontmatter.md` for the base shape and parsing rules.

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

Required for skills bundled into a Codex marketplace plugin.

- `version: 1` is required.
- `metadata` is required and must be a mapping.
- `interface.display_name`, `interface.short_description`, and `interface.default_prompt` must align to the canonical skill name and trigger language, using "Use when" phrasing.
- `policy.allow_implicit_invocation` must be explicit (boolean).
- Add `dependencies` only when the skill actually needs them.

See `.agents/docs/contracts/openai-agent-yaml.md` for the full contract.

## Bundled scripts

Every executable Python script bundled with a first-party skill must support the CLI contract in `.agents/specs/completed/2026-08-04-skill-script-cli-contract-design.md`:

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
6. The skill installs via `py -3 tools/run.py marketplace --apply`.
7. The skill triggers on the right conditions and provides the expected guidance.

## Pressure testing

When creating or modifying a skill, consider whether a RED/GREEN pressure test scenario would prove the skill's value.

Pressure tests are **advisory**, not mandatory. They are most valuable when:

- The skill prevents a common failure mode (e.g., truncated tool lists, wrong defaults, unsafe shortcuts).
- The skill routes the agent to a specific, non-obvious action.
- The cost of the agent making the wrong choice is high (rework, token waste, destructive operations).

Pure reference skills (syntax guides, API docs) and skills without a concrete failure mode to avoid usually do not need pressure tests.

### Required artifacts when pressure testing

1. **Scenario file in the skill:** Add `assets/pressure-tests.md` to the skill describing the RED and GREEN paths and the tool or decision under pressure. Keep it short and scenario-focused. The scenario ships with the skill so any consumer can run it.
2. **Recorded RED/GREEN runs:** Run the scenario once without the skill (RED) and once with the skill (GREEN) using subagents. Record the results in `provenance/` or `tests/pressure/<skill-name>/`. These proof records are consumer-specific and do not ship with the skill.
3. **Tool-calling fidelity:** Subagents cannot invoke skills, but they can read the skill files from disk and call available MCP or other tools directly. Do not pre-truncate or fabricate tool-list fixtures; let the subagent call the actual MCP server (e.g., `mcp_list_tools`) and experience the same truncation or discovery cost a real agent would.
4. **Cross-reference:** Link to the scenario from `assets/pressure-tests.md` and, where relevant, from the skill body.

### Policy expectations

- New skills: consider a pressure test during authoring; add it if the failure mode is clear.
- Modified skills: if the change affects routing, decisions, or tool selection, re-examine whether a pressure test is now warranted or needs updating.
- Existing skills: backfill pressure tests opportunistically; do not block current work on full backfill.

See `tests/pressure/README.md` for the generic subagent pressure-test runbook and `codex-marketplace/plugins/superpowers-plus/skills/writing-skills/testing-skills-with-subagents.md` for the RED/GREEN methodology.

## Compliance status

This policy is the target standard. Use it to audit existing skills, bring them up to standard incrementally, and validate new skills before landing. Hold new skills to the full spec from the start; do not block on full compliance for existing skills.
