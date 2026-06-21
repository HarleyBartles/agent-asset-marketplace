# sources

Upstream references, snapshots, and source-attribution records live here.

Use this directory for source material that informs an asset, not for derived
deployment output.

## Layout

- `first_party/` holds editable first-party source custody.
- `first_party/skills/<skill-name>/` is the single tree for all first-party
  skills, including generic reusable worker machinery and family-owned or
  bundle-specific roots. Every directory under `skills/` must contain a
  `SKILL.md`.
- `first_party/skills/house-skills/` is the current House Skills source ledger.
- `third_party/` holds retained third-party source custody.
- `third_party/unslop/`, `third_party/game-studio/`, `third_party/dotnet-claude-kit/`,
  and `third_party/codex-cortex/` hold the retained third-party plugin source
  custody for the plugins already carried in the marketplace, including the
  `api-design-patterns` contract-doctrine slice, the narrower
  `openapi-specification` companion slice now projected through
  `api-contracts-pack/`, and the `secure-coding-practices`, `owasp-top-10`,
  `security-testing-patterns`, and `threat-modeling-techniques` slices now
  projected through `security-pack/`.
