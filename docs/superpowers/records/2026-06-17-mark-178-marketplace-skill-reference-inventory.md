# MARK-178 Marketplace Skill Reference Inventory Record

**Issue:** MARK-178
**Branch:** `codex/mark-178-marketplace-skill-reference-inventory`
**Starting main SHA:** `e4777ffa796f7fa9fd181fa7e67a177b7609fef4`
**Status:** Local inventory evidence published; no source rewrites or generated artifact changes were made.

## Source-of-truth checks

- `codex-marketplace/manifest.json` lists the active plugin roots by plugin `name`.
- `codex-marketplace/plugin-roots.json` mirrors the editable active root inventory.
- `codex-marketplace/plugins/*/.codex-plugin/plugin.json` defines plugin `name`.
- Skill frontmatter `name:` in `SKILL.md` files defines skill identity.
- `codex-marketplace/plugins/house-skills/skills/house-skills/references/source-map.md` shows the `codex-repo-receipts` and `wild-bunch-project-doctrine` source/projection split for the House Skills bundle.
- `codex-marketplace/plugins/repo-worker-base/SOURCE.md` confirms `codex-repo-receipts` is projected from the House Skills source tree.

## Search surfaces inspected

- `rg -n "skill reference|skill references|Use the installed|Consult the installed|REQUIRED SUB-SKILL|REQUIRED BACKGROUND|superpowers:[A-Za-z0-9_-]+" codex-marketplace/plugins`
- `rg -n "codex-repo-receipts|codex-receipt-superpowers" codex-marketplace/plugins`
- `rg -n "skill-creator|skill-validator|skill-packager|skill-handoff|skill-installer" codex-marketplace/plugins/house-skills/skills`
- `rg -n "wild-bunch-project-doctrine" codex-marketplace/plugins/house-skills/skills codex-marketplace/plugins/wild-bunch-project-pack/skills`
- `rg -n "superpowers:" codex-marketplace/plugins/superpowers/skills`

## Inventory summary

### Already project-canonical references

These references already use the canonical plugin-qualified shape or point at skill names that are clearly owned by the same plugin root:

- `superpowers:using-git-worktrees`
- `superpowers:subagent-driven-development`
- `superpowers:executing-plans`
- `superpowers:finishing-a-development-branch`
- `superpowers:writing-plans`
- `superpowers:requesting-code-review`
- `superpowers:test-driven-development`
- `superpowers:verification-before-completion`

Representative source paths:

- `codex-marketplace/plugins/superpowers/skills/writing-plans/SKILL.md`
- `codex-marketplace/plugins/superpowers/skills/executing-plans/SKILL.md`
- `codex-marketplace/plugins/superpowers/skills/subagent-driven-development/SKILL.md`
- `codex-marketplace/plugins/superpowers/skills/systematic-debugging/SKILL.md`
- `codex-marketplace/plugins/superpowers/skills/writing-skills/SKILL.md`
- `codex-marketplace/plugins/superpowers/skills/github-superpowers/SKILL.md`

### Same-plugin bare references

These are bare references inside source files whose target skill lives in the same plugin root as the source file:

- `skill-creator`
- `skill-validator`
- `skill-packager`
- `skill-handoff`
- `skill-installer`
- `asset-market`
- `github-operations`
- `linear-superpowers`
- `linear-issue-compactor`
- `boring-loop`
- `tps-reporting`
- `connector-safety`
- `wild-bunch-project-doctrine` in the Wild Bunch bundle sources

Representative source paths:

- `codex-marketplace/plugins/house-skills/skills/asset-market/SKILL.md`
- `codex-marketplace/plugins/house-skills/skills/crew-buster/SKILL.md`
- `codex-marketplace/plugins/house-skills/skills/skill-handoff/SKILL.md`
- `codex-marketplace/plugins/house-skills/skills/skill-installer/SKILL.md`
- `codex-marketplace/plugins/house-skills/skills/skill-validator/SKILL.md`
- `codex-marketplace/plugins/house-skills/skills/skill-packager/SKILL.md`
- `codex-marketplace/plugins/house-skills/skills/bootstrap-router/SKILL.md`
- `codex-marketplace/plugins/house-skills/skills/work-mode-router/SKILL.md`
- `codex-marketplace/plugins/house-skills/skills/boring-loop/SKILL.md`
- `codex-marketplace/plugins/house-skills/skills/wild-bunch-domain-modeling/SKILL.md`
- `codex-marketplace/plugins/house-skills/skills/wild-bunch-dotnet-architecture/SKILL.md`
- `codex-marketplace/plugins/house-skills/skills/wild-bunch-worker-verification/SKILL.md`
- `codex-marketplace/plugins/wild-bunch-project-pack/skills/wild-bunch-domain-modeling/SKILL.md`
- `codex-marketplace/plugins/wild-bunch-project-pack/skills/wild-bunch-dotnet-architecture/SKILL.md`
- `codex-marketplace/plugins/wild-bunch-project-pack/skills/wild-bunch-worker-verification/SKILL.md`

### Cross-plugin bare references

These references are not plugin-qualified in the current text, and the source map/projection split means the target has to be resolved from repo context rather than from the token alone:

- `@codex-repo-receipts` in `codex-marketplace/plugins/house-skills/skills/codex-receipts-superpowers/SKILL.md`
- `@codex-repo-receipts` in `codex-marketplace/plugins/superpowers/skills/codex-receipts-superpowers/SKILL.md`
- bare `wild-bunch-project-doctrine` in the Wild Bunch source files under `house-skills` and `wild-bunch-project-pack`

### GPT overlay/export-only references

These references live in projection-layer prompt data rather than marketplace-source doctrine:

- `$using-superpowers`
- `$writing-plans`
- `$executing-plans`
- `$unslop-superpowers`
- `$codex-repo-receipts`
- `$codex-receipts-superpowers`
- `$skill-packager`
- `$crew-buster`
- `$house-skills`

Representative source paths:

- `codex-marketplace/plugins/house-skills/skills/codex-receipts-superpowers/agents/openai.yaml`
- `codex-marketplace/plugins/superpowers/skills/codex-receipts-superpowers/agents/openai.yaml`
- `codex-marketplace/plugins/house-skills/skills/github-superpowers/agents/openai.yaml`
- `codex-marketplace/plugins/house-skills/skills/unslop-superpowers/agents/openai.yaml`
- `codex-marketplace/plugins/house-skills/skills/skill-packager/agents/openai.yaml`
- `codex-marketplace/plugins/house-skills/skills/crew-buster/agents/openai.yaml`
- `codex-marketplace/plugins/house-skills/skills/house-skills/agents/openai.yaml`

### Ambiguous references

The unresolved ambiguity found in this pass is the `codex-repo-receipts` source/projection split and any bare reference that only resolves after choosing which marketplace surface is authoritative for that skill family.

## Follow-up scope for MARK-179

- Canonicalize marketplace source references to the verified `plugin_name:skill_name` shape.
- Decide how to treat projection-layer prompt data separately from marketplace source doctrine.
- Normalize or flag cross-plugin bare references where the target is not inferable from the current source text alone.

## Validation

- `rg -n "skill reference|skill references|Use the installed|Consult the installed|REQUIRED SUB-SKILL|REQUIRED BACKGROUND|superpowers:[A-Za-z0-9_-]+" codex-marketplace/plugins`
- `rg -n "codex-repo-receipts|codex-receipt-superpowers" codex-marketplace/plugins`
- `git diff --check`

## Publication note

No source files outside this plan and record were changed. No generated skill zips were modified. This record exists to unblock MARK-179 with evidence-backed inventory context.
