# Ops Connectors Pack Provenance

## Summary

The Ops Connectors Pack projects retained ECC operations and infrastructure skills into a Codex marketplace pack.

## Source Custody

### Retained ECC Upstream

- **Upstream root**: `sources/third_party/ecc/upstream/`
- **Retained skill roots**:
  - `sources/third_party/ecc/upstream/skills/terraform-modules/`
  - `sources/third_party/ecc/upstream/skills/kubernetes-deployment/`
  - `sources/third_party/ecc/upstream/skills/docker-compose/`
  - `sources/third_party/ecc/upstream/skills/ci-cd-pipeline/`
  - `sources/third_party/ecc/upstream/skills/infrastructure-as-code/`

### First-Party Ledgers

- **Selection/provenance ledger**: `sources/first_party/skills/ecc/decisions.json`
- **Human-readable ledger**: `sources/first_party/skills/ecc/decisions.md`
- **Intake record**: `sources/first_party/skills/ecc/intake.json`
- **Provenance notes**:
  - `provenance/ecc.md`

## Projection Surfaces

### ECC Projection

- `codex-marketplace/plugins/ops-connectors-pack/skills/terraform-modules/`
- `codex-marketplace/plugins/ops-connectors-pack/skills/kubernetes-deployment/`
- `codex-marketplace/plugins/ops-connectors-pack/skills/docker-compose/`
- `codex-marketplace/plugins/ops-connectors-pack/skills/ci-cd-pipeline/`
- `codex-marketplace/plugins/ops-connectors-pack/skills/infrastructure-as-code/`

- **Ops Connectors Pack source map**: `codex-marketplace/plugins/ops-connectors-pack/references/source-map.md`

## Marketplace Adaptation

- **Status**: `projected`
- **Plugin name**: `ops-connectors-pack`
- **Display name**: `Ops Connectors Pack`
- **Marketplace category**: `Productivity`
- **Content mode**: `verbatim` from ECC custody
- **Adaptation note**: Projected from retained ECC custody with first-party selection ledger

## Rights and Attribution

### ECC Content

- **Upstream source**: ECC (Enterprise Contract Copilot)
- **License**: Per ECC license terms
- **Redistribution rights**: Per upstream license terms with first-party selection provenance
- **Provenance note**: `provenance/ecc.md`

## Boundary

The bundle focuses on operations and infrastructure skills from ECC custody:
- Infrastructure as code (Terraform, Docker Compose)
- Container orchestration (Kubernetes)
- CI/CD pipeline configuration
- Infrastructure deployment and management
