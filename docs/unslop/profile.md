# Asset Marketplace Unslop Profile

This file is the repo-specific anti-slop guard for `HarleyBartles/agent-asset-marketplace`.

## Truth hierarchy

- Durable repository state beats memory, chat summaries, worker claims, installed GPT state, generated artifacts, and unverified PR text.
- When claims conflict, trust the owning surface: committed files, manifests, validators, published GitHub state, and durable provenance records.

## Marketplace doctrine

- Codex marketplace source is plugin-first.
- Canonical skill identity is `plugin_name:skill_name`.
- `gpt-overlays/` describes projection behavior, not source doctrine.
- Generated `skill.zip` files in `generated/skill-zips/` are repo-resident outputs, not canonical source.
- Regenerate generated zips through tooling. Do not hand-edit them.

## Evidence gates

- Do not close, merge, publish, retire, rename, import, or mark done without durable evidence from the owning surface.
- Separate Linear planning truth, GitHub implementation proof, generated output, and GPT installation/export surfaces.
- Keep issue bodies compact. Put dense plans and evidence in attached Linear docs.
- Inventory issues should return evidence to Linear docs and should not create GitHub branches or PRs unless a later implementation issue explicitly requires repo changes.

## Worker return standard

- A valid worker return must name the files changed, commands run, validation output, generated-artifact impact, and any blockers.
- Reject broad "cleanup", "refactor", or "improve" work unless the packet names source seams, validation, and evidence.
- Use the smallest surface that can prove the claim. If the surface cannot prove it, the claim is unfinished.
