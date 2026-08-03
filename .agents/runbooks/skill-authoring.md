# Skill Authoring Runbook

Use this runbook for repository paths, commands, generated-surface rules, and
publication handoff when authoring skills in the agent-asset-marketplace repo.

## Authoring route

1. Use `writing-skills` for general skill TDD and discovery quality.
2. Use `writing-skills/references/local-and-marketplace-custody.md` and
   `writing-skills/references/source-grounded-authoring.md` when the skill needs
   lane selection, custody placement, source decomposition, scholarly citations,
   or scaffolding.
3. Use this runbook for repository paths, commands, generated-surface rules, and
   publication handoff.

Scaffold a local skill with:

```text
bash codex-marketplace/plugins/superpowers-plus/skills/writing-skills/scripts/new-skill.sh --name mark-example --custody local --lane first_party
```

Scaffold a marketplace-custodied source-backed skill with:

```text
py -3 codex-marketplace/plugins/superpowers-plus/skills/writing-skills/scripts/new_skill.py --name ddd --custody marketplace --lane superpowers-plus
```

## Repository paths

- Local skills: `.agents/skills/mark-<skill-name>/`
- Marketplace-custodied sources: `codex-marketplace/plugins/<plugin-pack>/skills/<skill-name>/`
- Generated marketplace and installed skill surfaces are downstream outputs;
  do not edit them directly.

See [`docs/skill-standards-policy.md`](../../docs/skill-standards-policy.md)
for marketplace standards and marketplace metadata, and
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

## MCP wrapper skills

MCP-usage skills follow the `using-<x>-mcp` naming convention and live in the `mcp-usage-pack` plugin pack. When adding or moving one:

1. Name the skill `using-<x>-mcp` and place it in `codex-marketplace/plugins/mcp-usage-pack/skills/<name>/`.
2. Provide `SKILL.md` with a router table that maps common intents to `references/*.md` files.
3. Provide `agents/openai.yaml` with `skill_name`, `source_category: first_party`, `display_name`, `short_description`, `default_prompt`, and `allow_implicit_invocation: true`.
4. Provide `assets/icon.svg` and a `references/` directory with `surface-map.md` covering the key MCP tools, use-case files, and `other-playwright-tools.md` for fallback to non-MCP surfaces.
5. After adding or moving skills, regenerate the pack's `references/bundle-manifest.json` with:

```bash
py -3 tools/new_plugin.py --sync mcp-usage-pack
```

6. Apply marketplace and installed-skills changes with `py -3 tools/run.py marketplace --apply`.

## Publication handoff

After the relevant checks pass, stage only the intended canonical sources and
their required generated outputs, commit the focused change, push the task
branch, and hand off its GitHub-visible PR or explicitly authorized direct-main
commit as the publication proof.
