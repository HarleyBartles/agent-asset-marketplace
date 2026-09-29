# Stage guide contract

## Read when

Read when locating, creating, or reviewing the consuming repository's local guide for design, planning, implementation, or code review.

## Contract

Use the consuming repository's declared guidance entrypoint and follow its paths for lifecycle-stage guides and topical workflows. Do not assume a runbook or playbook inventory, a particular directory, or a fixed set of stage files. `.agents/runbooks/` and `.agents/playbooks/` are conventions only when the repository adopts them.

Each runbook supplies repository-specific composition, paths, commands, exclusions, CI, and exceptions. It does not replace, override, reorder, or bypass the matching portable baseline or selected Superpowers lane. Migrate a legacy home through the repository's approved plan and keep a fallback pointer only when that policy explicitly requires it.

If repository policy requires a local guide and none is present at its declared location, report that gap. When no local guide is declared or required, continue with the portable workflow. Do not invent repository-specific commands or paths in this portable skill.
