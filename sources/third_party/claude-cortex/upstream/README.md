# Claude Cortex Retained Snapshot

Selective third-party custody for the NickCrew/Claude-Cortex upstream drain.

Pinned commit: `7892d00e7cb6adf00144a535103b930c772fb2c0`
License: MIT

This snapshot retains the 18 Claude-Cortex skills projected into the
marketplace across MARK-172, MARK-200, MARK-201, MARK-204, MARK-205,
MARK-207, MARK-210, MARK-212, MARK-213, and MARK-214:

- `accessibility-audit`
- `api-design-patterns`
- `async-python-patterns`
- `cqrs-event-sourcing`
- `database-design-patterns`
- `event-driven-architecture`
- `interaction-design`
- `openapi-specification`
- `owasp-top-10`
- `python-performance-optimization`
- `python-testing-patterns`
- `react-performance-optimization`
- `secure-coding-practices`
- `security-testing-patterns`
- `threat-modeling-techniques`
- `typescript-advanced-patterns`
- `ux-review`
- `webapp-testing`

All 18 retained skills are projected into canonical marketplace plugins
(`codex-cortex`, `architecture-pack`, `api-contracts-pack`,
`language-patterns-pack`, `security-pack`, `frontend-pack`). No other
Claude-Cortex upstream skills are retained. Candidates not listed here
were rejected for hard reasons (not in retained custody, duplicate
existing authority, or violate durable-source doctrine) as recorded in
`provenance/codex-cortex.md` under the MARK-279 child coverage map.
