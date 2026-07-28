# Skill Authoring Guide

Use this guide for repository paths, commands, generated-surface rules, and
publication handoff when authoring skills in the agent-asset-marketplace repo.

## Authoring route

1. Use `writing-skills` for general skill TDD and discovery quality.
2. Use `mark-skill-authoring` when the skill needs lane selection, custody
   placement, source decomposition, scholarly citations, or scaffolding.
3. Use this guide for repository paths, commands, generated-surface rules, and
   publication handoff.

Scaffold a local skill with:

```text
bash .agents/skills/mark-skill-authoring/scripts/new-skill.sh --name mark-example --custody local --lane first_party
```

Scaffold a marketplace-custodied source-backed skill with:

```text
py -3 .agents/skills/mark-skill-authoring/scripts/new_skill.py --name ddd --custody marketplace --lane skills-with-source
```

## Repository paths

- Local skills: `.agents/skills/mark-<skill-name>/`
- Marketplace-custodied sources: `sources/first_party/skills/<skill-name>/`
- Generated marketplace and installed skill surfaces are downstream outputs;
  do not edit them directly.

See [`docs/skill-standards-policy.md`](../../docs/skill-standards-policy.md)
for marketplace standards and projection metadata, and
[`docs/overlay-adapter-policy.md`](../../docs/overlay-adapter-policy.md) for
third-party overlay and adapter triggers.

## Generated-surface commands

For a targeted marketplace skill update, run:

```bash
py -3 tools/update_skill_artifacts.py --skill <pack>/<skill>
```

For marketplace-wide source or structure changes, run:

```bash
tools/run marketplace --apply
```

Install refreshed skills to the local agent surface with:

```bash
tools/run installed-skills --apply
```

Check the resulting marketplace state with:

```bash
tools/run ci --check
```

## Publication handoff

After the relevant checks pass, stage only the intended canonical sources and
their required generated outputs, commit the focused change, push the task
branch, and hand off its GitHub-visible PR or explicitly authorized direct-main
commit as the publication proof.
