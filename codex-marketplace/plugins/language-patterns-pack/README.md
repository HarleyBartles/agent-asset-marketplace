# Language Patterns Pack

This plugin bundle projects the MARK-212 `typescript-advanced-patterns` slice
from the retained Claude-Cortex custody plugin into an installable Codex
marketplace pack.

## Bundle contents

- `typescript-advanced-patterns`
- provenance and source mapping in `SOURCE.md`
- bundle inventory in `references/bundle-manifest.json`
- canonical source mapping in `references/source-map.md`

## Boundary

- `typescript-advanced-patterns` carries TypeScript language and runtime guidance.
- The bundle does not own React, frontend architecture, CQRS, database, security,
  or other non-language doctrine.
- The bundle is a projection over retained source custody, not a new source of
  truth.

## Install shape

The installable skill zip is generated under
`generated/skill-zips/language-patterns-pack/typescript-advanced-patterns/skill.zip`
and can be installed directly from that artifact.
