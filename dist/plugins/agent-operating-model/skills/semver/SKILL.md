---
name: semver
description: Use when choosing a product version, assessing compatibility or release identity, or tracing conflicting versions across package metadata, runtime, manifests, and artifacts.
metadata:
  source-id: "semver"
  source-path: "skills/semver/SKILL.md"
  provenance-name: Semantic Versioning Standard first-party skill
  source-category: first_party
  status: active
  owner: "Harley Bartles"
  scope: Product compatibility versions, single-source ownership, and release identity decisions.
  use_when:
    - choosing or reviewing a product version, compatibility claim, prerelease, or released tag.
    - tracing duplicate, stale, or separately authored product versions across a build.
    - assessing or certifying an explicit SemVer subscription.
  do_not_use_when:
    - the repository has not adopted SemVer and the human has not requested its assessment or adoption.
    - the version belongs to a dependency or independently versioned data schema rather than a product; assess each independently released product under its own compatibility contract.
license: MIT
---

# SemVer

Use this skill when a repository explicitly adopts or asks to assess the `semver` standard. First read its pinned subscription and certification. Then use the [standard](references/standard.md) for required invariants and the [versioning guide](references/adoption-and-versioning.md) for compatibility, build identity, and release decisions. The source record identifies normative SemVer 2.0.0 and AOM's additional obligations; no standard adoption is implied by ambient skill availability.
