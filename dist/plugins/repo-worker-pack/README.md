# Repo Worker Pack

This ambient bundle makes first-party repository-worker capabilities available to agents across repositories. It is not a repository subscription and does not impose a directory layout, runbook inventory, or operating standard.

## Bundle contents

### Documentation

- provenance and source mapping in `SOURCE.md`
- bundle inventory in `references/bundle-manifest.json`

## Boundary

- The first-party repo worker skills provide general worker capabilities. A consumer may use any available capability without copying or installing this bundle into its repository.
- The bundle stays narrow and first-party. Workflow composition and independently deployable repository standards have separate owners.

## Install shape

When a repository deliberately configures marketplace skill installation, the refresh utility projects selected skills from their declared sources. Runtime availability of this ambient bundle does not imply that repository configuration.
