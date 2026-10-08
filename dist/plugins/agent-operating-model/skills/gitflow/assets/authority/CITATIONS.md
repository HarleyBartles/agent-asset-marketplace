# Authority Record for gitflow

## Scholarly citation

- Vincent Driessen. "A successful Git branching model." Published 2010-01-05; author reflection dated 2020-03-05. https://nvie.com/posts/a-successful-git-branching-model/ (accessed 2026-10-08).
- The author reflection narrows applicability and cautions against treating Gitflow as a universal workflow. Its branch-role and routing sections inform this original operational synthesis.

## Derivation boundary

- Derived from the cited feature, release, hotfix, and long-lived-branch model: branch purpose, origins, targets, stabilization, promotion, and reconciliation.
- The branch policy in this AOM standard is an adapted, repository-neutral contract. Conventional names are examples that adopters can map to local branch names.
- Original AOM additions: optional independent adoption; explicit subscription and self-certification; current-ref and hosting-rule verification; preservation of active release fixes; and conditional SemVer `dev.N`/`rc.N` identities with the two reconciliation states.
- Outside scope: a mandatory hosted provider, branch protection configuration, CI implementation, deployment process, branch prefix, or prescribed product version file.

## Attribution

- Clean-room first-party synthesis under MIT. No source prose, diagram, or source code is vendored or reproduced. The linked article is cited as pattern authority, with AOM-specific obligations identified separately.

## Human review

- The article and its dated author reflection were opened and reviewed for this change on 2026-10-08. The reflection's applicability caveat is retained in the standard.
- Human approval of this implementation and certification of any adopting repository remain pending.

## Authority record integrity

- The `content_sha256` value in `authority.yaml` and the `reconciled_against` values in `authority.yaml` and `source-map.yaml` are the SHA-256 of this `CITATIONS.md` file.
