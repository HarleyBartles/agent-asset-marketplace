# Source

This bundle packages the upstream standalone Replit skill family as a
market-facing Codex plugin.

## Upstream basis

- Repo: `jeremylongshore/claude-code-plugins-plus-skills`
- URL:
  <https://github.com/jeremylongshore/claude-code-plugins-plus-skills.git>
- Pinned commit: `e773501f1dfb409fc71fccdaf6ac2898fedf66d6`
- License: MIT

## Source roots inspected

- `plugins/saas-packs/skill-databases/replit/` primary standalone skill root
- `plugins/saas-packs/replit-pack/` cross-check bundle surface

## Outcome

- Candidate skills found: `30`
- Imported into this pack: `28`
- Skipped as out of scope: `2`
- Blocked: `0`

## Imported skills

The full import ledger is recorded in
`codex-marketplace/plugins/testing-skill-pack/references/bundle-manifest.json`.

## Skipped skills

These upstream docs were present in the source root but were not imported into
this proof slice because they are adjacent Replit growth / education skills
rather than testing or operations workflow skills:

- `plugins/saas-packs/skill-databases/replit/replit-bounty-hunting.md`
- `plugins/saas-packs/skill-databases/replit/replit-edu-classroom.md`

## Notes

No behavior changes were made to the imported docs. The wrapper only maps the
upstream skill docs into local plugin paths and attaches provenance evidence.
