# Agent document checker behavior cases

Use these cases to review mechanical coverage and its limits; do not treat candidate output as certification.

## Case A: mixed agent document formats

The repository stores binding Markdown doctrine and a YAML contract alongside a JSON operating contract. One JSON file is malformed, and another valid JSON contract has no agreed schema.

## Case B: static and runtime routes

One Markdown doctrine document is linked from an `AGENTS.md`. Another is loaded through plugin skill metadata or harness scope and has no Markdown inbound link. A third document is not routed anywhere.

## Expected decisions

- The standard requires agent doctrine in `.agents/doctrine/` and agent contracts in `.agents/contracts/`. Product schemas are outside this standard merely because they are called contracts.
- The checker can ensure both stores exist, validate JSON syntax only, and report broken local Markdown links. It does not parse YAML/TOML schemas or execute commands described by contracts.
- A document without a static inbound Markdown link is an advisory candidate, not automatically unreachable: skill, plugin, harness, and other runtime routes may be invisible. A truly unrouted document is also a candidate for repository review.
- `--route-root` adds Markdown source trees/files that should be scanned, and `--exclude` supports repository boundaries. Neither option proves effective routing or creates a universal schema.
- If CI exists, the repository-owned checker runs there. Semantic review and the route map remain part of self-certification.
