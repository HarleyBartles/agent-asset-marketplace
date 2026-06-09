# Security Scan Pack Source Map

This pack is clean-room work. The sources below informed the workflow shape,
tooling choices, and report posture, but no file from the proprietary
`openai/plugins/plugins/codex-security` root was copied.

## Advisory-only blocked root

- `openai/plugins/plugins/codex-security`
  - License posture recorded by upstream: proprietary
  - Role here: capability-gap evidence only
  - Copied payload: none

## Repo-owned skill files

- `skills/security-scan-pack/SKILL.md`
  - Orchestrates repo or scoped-path security scans, threat modeling, receipts,
    severity analysis, and final reporting.
- `skills/security-scan-pack/references/scanner-matrix.md`
  - Normalizes the licensed scanner families and the scan modes used by the pack.
- `skills/security-scan-pack/references/ledger-and-receipts.md`
  - Defines deterministic coverage ledgers and per-candidate receipt posture.
- `skills/security-scan-pack/references/report-template.md`
  - Defines the final markdown report structure.
- `skills/security-scan-pack/references/threat-model-capture.md`
  - Captures the minimum threat model inputs before a scan is treated as complete.

## Permissive source families consulted

| Candidate | Source | License | Role in the pack |
| --- | --- | --- | --- |
| Gitleaks | https://github.com/gitleaks/gitleaks | MIT | Secret scanning for git history, directories, and stdin-fed content |
| Trivy | https://github.com/aquasecurity/trivy | Apache-2.0 | Vulnerability, secret, IaC, dependency, container, and license scanning |
| Grype | https://github.com/anchore/grype | Apache-2.0 | Vulnerability scanning for images, filesystems, and SBOMs |

## Notes

- The pack uses repo-authored prose, not lightly rewritten upstream plugin text.
- Semgrep was intentionally left out of the default integration set so license
  obligations never become ambiguous.
- If a scanner's CLI or output format changes, refresh the pack from the
  official upstream docs rather than from memory.
