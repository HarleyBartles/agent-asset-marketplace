# Release Engineering operational guidance

## When to apply

Use when the release-engineering skill loaded and the question is deeper than a single sentence:
- designing CI/CD pipelines,
- containerizing and promoting images,
- choosing deployment patterns,
- planning releases and rollbacks.

## Container images

- Build from minimal, pinned base images; pin digests, not just tags.
- Use multi-stage builds to keep runtime images small.
- Scan images for vulnerabilities before promotion.

## CI/CD pipelines

- Trigger pipelines on pull requests, merges, and release tags.
- Run tests, lint, and security scans in parallel.
- Gate promotions on green builds and required approvals.

## Deployment patterns

- Use rolling deployments for stateless services with backward-compatible changes.
- Use blue/green when you need instant cutover and simple rollback.
- Use canary releases for gradual traffic shifts; automate rollback on SLO breach.

## Rollback

- Keep the previous release artifact and deployment manifest ready.
- Automate rollback to the last known good version.
- Test rollback in staging before it matters.

## Supply-chain security

- Sign container images and release artifacts.
- Use short-lived runner credentials and least-privilege service accounts.
- Audit runner and registry permissions regularly.

## Related references

- Docker docs: https://docs.docker.com/
- Kubernetes docs: https://kubernetes.io/docs/home/
- GitHub Actions docs: https://docs.github.com/en/actions
- SRE book: https://sre.google/sre-book-table-of-contents/
