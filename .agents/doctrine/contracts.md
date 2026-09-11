
# Contract Custody

All repository-level contracts live under `.agents/contracts/`. A contract
defines an interface, accepted shape, or executable binding that consumers can
validate.

Policy and authority remain under `.agents/doctrine/`. Skill-owned schemas and
contracts remain colocated with their canonical skill when they are not
repository-level contracts. Generated manifests and marketplace configuration
remain with the tools and packages that own them.

Repo-specific anti-slop profiles are behavioral contracts. Repo-wide profiles
live under `.agents/contracts/unslop/`; a justified subsystem overlay lives at
`<scope>/.agents/contracts/unslop/`. The portable `unslop-profiles` skill owns
generic reusable profiles, not consumer-specific contract content.
