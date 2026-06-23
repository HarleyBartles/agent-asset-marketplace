# plugins

Marketplace plugin projection shape lives here.

Codex plugin first; generated GPT-safe skill zips second.

The active marketplace roots under this directory are limited to
`house-skills/`, `adventures-pack/`, `unslop/`, `game-studio/`,
`wild-bunch-project-pack/`, `superpowers-plus/`, `repo-worker-base/`,
`dotnet-kit/`, `codex-cortex/`, `api-contracts-pack/`, `architecture-pack/`,
`language-patterns-pack/`, `security-pack/`, and `frontend-pack/`.

Everything else in this tree is support custody or historical source material,
not part of the active marketplace inventory for the normalized root pass.

Canonical installable `skill.zip` artifacts for the active installable skills
are written separately under `generated/skill-zips/<pack-or-plugin>/<skill-name>/`.

These plugin roots are the canonical marketplace install surface. Generated
skill zips are derived GPT exports, and GPT overlays should be used to make the
exports safe without mutating Codex-native plugin behavior.
