# Source

This bundle packages the upstream standalone Supabase skill family as a
market-facing Codex plugin.

## Upstream basis

- Repo: `jeremylongshore/claude-code-plugins-plus-skills`
- URL:
  <https://github.com/jeremylongshore/claude-code-plugins-plus-skills.git>
- Pinned commit: `e773501f1dfb409fc71fccdaf6ac2898fedf66d6`
- License: MIT

## Source roots inspected

- `plugins/saas-packs/skill-databases/supabase/` candidate inventory and shape check
- `plugins/saas-packs/supabase-pack/skills/` imported functional skill root

## Outcome

- Candidate skills found: `30`
- Imported into this pack: `30`
- Skipped as out of scope: `0`
- Blocked: `0`

## Imported skills

The full import ledger is recorded in
`codex-marketplace/plugins/supabase-platform-pack/references/bundle-manifest.json`.

## Notes

Most imported docs were copied verbatim. `supabase-multi-env-setup` was
intentionally adapted to make the destructive reset example local-only, and the
bundle ledger records that safety change.
