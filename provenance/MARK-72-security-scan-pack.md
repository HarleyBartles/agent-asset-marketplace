# MARK-72 Security Scan Pack Provenance

Issue: `MARK-72`

## Outcome

Created a repo-owned clean-room security scan pack at
`codex-marketplace/plugins/security-scan-pack`.

## Blocked advisory root

- Upstream root: `openai/plugins/plugins/codex-security`
- Usage posture: advisory only
- License posture: proprietary
- Copied payload: none

## Permitted source families reviewed

- `gitleaks/gitleaks` under MIT
- `aquasecurity/trivy` under Apache-2.0
- `anchore/grype` under Apache-2.0

## Repo-held evidence

- Pack README: `codex-marketplace/plugins/security-scan-pack/README.md`
- Pack source note: `codex-marketplace/plugins/security-scan-pack/SOURCE.md`
- Pack source map: `codex-marketplace/plugins/security-scan-pack/references/source-map.md`
- Pack license notice: `codex-marketplace/plugins/security-scan-pack/LICENSE`

## Notes

- The pack text was authored from first principles.
- The pack integrates licensed scanner families by reference only; no scanner
  source code was vendored into the plugin root.
- Semgrep was intentionally left out of the default integration set so license
  obligations stay explicit.
