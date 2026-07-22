# plugins

Marketplace plugin projection shape lives here.

Codex plugin first; generated GPT-safe skill zips second.

The active marketplace roots under this directory are limited to
`house-skills/`, `unslop-plus/`, `game-studio/`, `superpowers-plus/`, `repo-worker-pack/`, `dotnet-pack/`, `api-contracts-pack/`, `architecture-pack/`, `language-patterns-pack/`, `security-pack/`, `frontend-pack/`, `data-platform-pack/`, `planning-pack/`, `rooms-project-pack/`, `feature-sliced-design/`, `agentic-workflows/`, `agentic-evaluation/`, `research-pack/`, `engineering-pack/`.

Everything else in this tree is support custody or historical source material,
not part of the active marketplace inventory for the normalized root pass.

Canonical installable `skill.zip` artifacts for the active installable skills
are written separately under `generated/skill-zips/<skill-name>.zip`.

These plugin roots are the canonical marketplace install surface. Generated
skill zips are derived GPT exports, and GPT overlays should be used to make the
exports safe without mutating Codex-native plugin behavior.
