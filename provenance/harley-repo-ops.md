# Harley Repo Ops Provenance

## Summary

- Bundle name: `harley-repo-ops`
- Bundle type: curated cross-repo worker bundle
- Canonical source root: `gpt-skills/house-skills`
- License posture: first-party Harley-authored source

## Projected skills

- `connector-safety`
- `gpt-base-doctrine`
- `work-mode-router`
- `worker-dispatch-linear`
- `linear`
- `tps-reporting`
- `tps-ingress`
- `don-logan-boundary`
- `crew`
- `crew-buster`

## Notes

- The bundle is a projection, not a source of truth.
- The shared safety component is included so connector/tool side effects stay
  narrow, auditable, and recoverable.
- Project-specific bundles remain the right place for repo-specific doctrine.
