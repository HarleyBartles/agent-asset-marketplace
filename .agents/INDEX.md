# Local Worker Surface

This folder is the repo-local worker surface for `agent-asset-marketplace`.
It is a projection of the repo-local plugin marketplace and worker doctrine, not canonical source.

Start here:

- [Marketplace registry](plugins/marketplace.json)
- [Marketplace worker doctrine](docs/marketplace-worker-doctrine.md)
- [Repo AGENTS](../AGENTS.md)

The canonical durable classifier for worker starts is `work-mode-router`.
Use the repo-local plugin marketplace for installed skills and repo work only
after the durable route has been classified.
