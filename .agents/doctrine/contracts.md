
# Contract Custody

All repository-level contracts live under `.agents/contracts/` regardless of
whether they are human-readable or machine-readable. A contract defines an
interface, accepted shape, or executable binding that consumers can validate.

Policy and authority remain under `.agents/doctrine/`. Skill-owned schemas and
contracts remain colocated with their canonical skill when they are not
repository-level contracts. Generated manifests and marketplace configuration
remain with the tools and packages that own them.
