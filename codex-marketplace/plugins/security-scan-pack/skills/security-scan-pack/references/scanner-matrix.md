# Scanner Matrix

This pack intentionally keeps the tool integrations thin. The job of the pack is
to orchestrate licensed scanners, preserve receipts, and normalize the results
into a reviewable report.

## Gitleaks

- Use for secrets in git history, directories, or stdin-fed content.
- Prefer `git` when the scope is a repository history.
- Prefer `dir` when the scope is a filesystem tree or a single file.
- Use a baseline only when the user asks to suppress known historical findings.
- Record the report path and any ignore/baseline file in the receipt.

## Trivy

- Use for filesystem, dependency, container, IaC, and license scanning.
- Prefer `fs` for repository trees.
- Prefer `image` for container images.
- Prefer `config` for IaC and configuration files.
- Use `--format json --output <path>` so the report is deterministic and machine-readable.
- Use `--license-full` only when the scan explicitly needs deeper license coverage.

## Grype

- Use for vulnerability matching on images, filesystems, or SBOMs.
- Prefer an SBOM input when the scan already has one.
- Record the output path and any SBOM source in the receipt.
- Keep image digests or filesystem paths explicit in the report.

## Integration rules

- Do not copy scanner output into the report without normalization.
- If two tools cover the same surface, prefer the one that provides the clearest
  evidence for the requested result and keep the other as corroboration.
- If a scanner's CLI changes, update the pack from the official upstream docs.
