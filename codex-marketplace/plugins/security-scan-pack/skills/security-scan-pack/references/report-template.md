# Report Template

Use this structure for the final markdown report.

## Required sections

1. `Executive Summary`
- What was scanned.
- What mattered most.
- Whether any blockers remained.

2. `Scope`
- Repo or path in scope.
- Paths excluded from the scan.
- Tooling used.

3. `Threat Model`
- Assets.
- Trust boundaries.
- Attacker goals.
- Key assumptions.

4. `Coverage Ledger`
- Per-candidate rows.
- Receipts or output artifacts.
- Explicit blockers for unscanned surfaces.

5. `Findings`
- One finding per numbered item.
- Evidence path or command output.
- Why the finding matters.
- How it was confirmed.

6. `Attack-Path Analysis`
- Short path from exposure to impact.
- Why the issue is reachable.
- Why the severity is set the way it is.

7. `Residual Risk`
- What remains after the scan.
- What should be scanned next.

8. `Appendix`
- Tool versions.
- Commands.
- Receipt paths.

## Reporting rules

- Keep the report deterministic and reviewable.
- Separate confirmed findings from advisory leads.
- Call out zero-finding scans so they count as evidence.
- Do not bury blockers in prose.
