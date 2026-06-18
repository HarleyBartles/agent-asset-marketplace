# third_party

Retained third-party source custody lives here.

Keep each retained plugin or package in its own root under this directory, with
upstream snapshots, patches, normalized copies, and custody notes separated
from the installable marketplace projections under `codex-marketplace/`.

Current retained roots include `unslop/`, `game-studio/`, `superpowers/`,
`dotnet-claude-kit/`, `codex-cortex/`, `claude-cortex/`, and `ecc/`. The
`codex-cortex/` root retains the MARK-204 `api-design-patterns` custody slice,
the MARK-205 `openapi-specification` companion slice, the MARK-207
`secure-coding-practices`, `owasp-top-10`, and
`security-testing-patterns` custody slices, and the MARK-210
`threat-modeling-techniques` custody slice alongside the earlier Claude-Cortex
imports. The `claude-cortex/` root retains the MARK-214 frontend slice:
`react-performance-optimization`, `accessibility-audit`, `ux-review`,
`interaction-design`, and `webapp-testing`.
The `ecc/` root retains the MARK-235 upstream skill inventory as third-party
source custody under `sources/third_party/ecc/upstream/source-custody.md`.
