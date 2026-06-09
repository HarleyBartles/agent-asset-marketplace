---
name: "security-scan-pack"
description: "Run clean-room repository security scans with licensed tools, deterministic receipts, threat modeling, candidate discovery, attack-path severity analysis, and final markdown reporting. Trigger when the user explicitly asks for a repo security scan, secret scan, vulnerability scan, IaC scan, validation receipt, or security scan report. Do not trigger for generic code review or non-security work."
---

# Security Scan Pack

Use this skill to turn a repository or scoped path into a repeatable security
scan workflow. It is clean-room work: do not copy or paraphrase the proprietary
`openai/plugins/plugins/codex-security` root.

## Workflow

1. Scope the target.
- Identify the exact repo path or subpath in scope.
- Note whether the scan is advisory, PR-gating, or release-blocking.
- Record any ignored paths, baseline files, or time windows up front.

2. Capture the threat model.
- Identify assets, trust boundaries, entry points, and likely attacker goals.
- Note where secrets, dependencies, container images, or IaC files are expected.
- Capture assumptions before any scanner output is treated as complete.

3. Choose the licensed scanner mix.
- Use `gitleaks` for secrets and git-history exposure.
- Use `trivy` for filesystem, dependency, container, IaC, and license scanning.
- Use `grype` for vulnerability matching on images, filesystems, or SBOMs.

4. Run candidate discovery.
- Scan the narrowest path that still covers the requested surface.
- Keep raw tool output and the exact command line in a receipt.
- Preserve zero-finding receipts; a quiet scan is still evidence.

5. Normalize findings.
- Deduplicate repeated matches across tools or repeated paths.
- Tie each finding to a concrete candidate, tool, and evidence file.
- Separate confirmed issues from advisory leads or unverified candidates.

6. Analyze severity and attack paths.
- Prefer attacker goals that map to exfiltration, privilege escalation,
  integrity compromise, or availability loss.
- Distinguish exposed surface from reachable surface.
- Explain why a finding matters before suggesting a fix.

7. Write the report.
- Use the template in `references/report-template.md`.
- Include the coverage ledger, receipts, residual risks, and open blockers.
- Do not hide the surfaces that were not scanned.

## Deterministic rules

- Use fixed output locations and UTC timestamps when possible.
- Record tool name, version, command, target, exit code, output path, and
  finding count for each candidate.
- Keep per-candidate receipts even when a tool returns no findings.
- Keep raw evidence separate from the human summary.

## Guardrails

- Do not claim equivalence with the blocked proprietary upstream root.
- Do not use semgrep unless its license obligations are explicitly handled.
- If a scanner is unavailable, record the blocker instead of inventing results.
- Use the current official docs when a CLI flag or output format may have drifted.
