# Agent document checker behavior cases

Use these cases to review mechanical coverage and its limits; do not treat candidate output as certification.

## Case A: mixed agent document formats

The repository stores binding Markdown doctrine and a YAML contract alongside a JSON operating contract. One JSON file is malformed, and another valid JSON contract has no agreed schema.

## Case B: static and runtime routes

One Markdown doctrine document is linked from an `AGENTS.md`. Another is loaded through plugin skill metadata or harness scope and has no Markdown inbound link. A third document is not routed anywhere.

## Expected decisions

- The standard requires agent doctrine in `.agents/doctrine/` and agent contracts in `.agents/contracts/`. Product schemas are outside this standard merely because they are called contracts.
- The checker can ensure both stores exist, validate JSON syntax only, and report broken local Markdown links from the agent-document stores and explicitly selected route roots. Unrelated Markdown can contribute inbound-link evidence without making its broken links fail this check. It does not parse YAML/TOML schemas or execute commands described by contracts.
- A document without a static inbound Markdown link is an advisory candidate, not automatically unreachable: skill, plugin, harness, and other runtime routes may be invisible. A truly unrouted document is also a candidate for repository review.
- `--route-root` adds Markdown source trees/files whose broken links should fail the check, and `--exclude` supports repository boundaries. Other Markdown files may contribute inbound-link evidence without their unrelated broken links failing the check. Neither option proves effective routing or creates a universal schema.
- If CI exists, the repository-owned checker runs there. Semantic review and the route map remain part of self-certification.
