# Source

This plugin projects the retained Codex Cortex security foundations plus the
selected ECC safety and security-review skills.

## Source custody
### Claude Cortex custody
- `sources/third_party/claude-cortex/upstream/skills/owasp-top-10/`
- `sources/third_party/claude-cortex/upstream/skills/secure-coding-practices/`
- `sources/third_party/claude-cortex/upstream/skills/security-testing-patterns/`
- `sources/third_party/claude-cortex/upstream/skills/threat-modeling-techniques/`

### ECC custody
- `sources/third_party/ecc/upstream/source-custody.md`
- `sources/third_party/ecc/upstream/manifest.json`

## Projection surfaces
- Codex plugin root: `codex-marketplace/plugins/security-pack/`
- Skill root: `codex-marketplace/plugins/security-pack/skills/`
- Skill roots:
  - `codex-marketplace/plugins/security-pack/skills/owasp-top-10/`
  - `codex-marketplace/plugins/security-pack/skills/secure-coding-practices/`
- `codex-marketplace/plugins/security-pack/skills/security-testing-patterns/`
- `codex-marketplace/plugins/security-pack/skills/threat-modeling-techniques/`
- `codex-marketplace/plugins/security-pack/skills/safety-guard/`
- `codex-marketplace/plugins/security-pack/skills/security-review/`

## Generated install units
- `generated/skill-zips/security-pack/owasp-top-10/skill.zip`
- `generated/skill-zips/security-pack/secure-coding-practices/skill.zip`
- `generated/skill-zips/security-pack/security-testing-patterns/skill.zip`
- `generated/skill-zips/security-pack/threat-modeling-techniques/skill.zip`

## Boundary
- The retained security foundations stay projected alongside the complementary
  ECC safety and security-review skills.
- The bundle stays out of generic compliance theatre, repo governance, and
  unrelated implementation domains unless another issue explicitly composes
  them in.
