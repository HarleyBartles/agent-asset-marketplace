# Contract Custody

All repository-level contracts live under `.agents/contracts/`. A contract defines an interface, accepted shape, or executable binding that consumers can validate.

Policy and authority remain under `.agents/doctrine/`. Skill-owned schemas and contracts remain colocated with their canonical skill when they are not repository-level contracts. Generated manifests and marketplace configuration remain with the tools and packages that own them.

Unslop adoption settings belong in `.agents/contracts/unslop.json` when a repository explicitly adopts the optional Unslop standard. Operational profiles live under `.agents/unslop/` by default, with any additional roots declared in that settings contract. Profiles are guidance for recognizing and correcting recurring failure patterns, not contracts or binding policy. Doctrine remains authoritative; profiles may link to it without duplicating its rules. The ambient `unslop-profiles` skill discovers and applies suitable profiles when available.
