# Agent Capability Pack

This ambient bundle makes first-party agent capabilities available across projects. It does not impose a project directory layout, runbook inventory, or operating standard.

## Bundle contents

### Documentation

- provenance and source mapping in `SOURCE.md`
- bundle inventory in `references/bundle-manifest.json`

## Boundary

- The first-party repo worker skills provide general worker capabilities. A consumer may use any available capability without copying or installing this bundle into its repository.
- The bundle stays narrow and first-party. Workflow composition and independently deployable repository standards have separate owners.

## Install shape

The package is installed and updated by the agent harness. Its presence in a harness does not opt a project into any repository standards.
