# Contract Custody

All repository-level contracts live under `.agents/contracts/`. A contract defines an interface, accepted shape, or executable binding that consumers can validate.

Policy and authority remain under `.agents/doctrine/`. Skill-owned schemas and contracts remain colocated with their canonical skill when they are not repository-level contracts. Generated manifests and marketplace configuration remain with the tools and packages that own them.

Operational Unslop profiles live under `.agents/unslop/`. The current standard uses that canonical location directly; it has no separate profile-root contract. Profiles guide recognition and correction of recurring failure patterns. They are not contracts or binding policy. Doctrine remains authoritative; profiles may link to it without duplicating its rules. The ambient `unslop-profiles` skill discovers and applies suitable profiles when available. A repository pinned to a historical definition follows only that definition's exact contract and profile roots.
