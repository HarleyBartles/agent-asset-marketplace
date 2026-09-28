# Jev MCP

This plugin connects the Jev AI Community's remote MCP and provides first-party guidance for its six decision tools. Model routing is the initial use case; the skill also routes other bounded judgments when an owning workflow calls for one.

## Bundle contents

- `skills/using-jev-mcp/` contains the canonical skill and tool references.
- `.mcp.json` declares the remote HTTPS server. Installation needs a personal Bearer key in the local `JEV_API_KEY` environment variable; no credential belongs in this repository.
- `references/bundle-manifest.json` is the generated skill inventory.

## Boundary

The MCP is run by Jev AI Community. The plugin and skill are maintained here; Jev decisions do not override user instructions, repository policy, live tool availability, or approval requirements. The existing `selecting-a-subagent` route remains usable if the service is unavailable.

## Install shape

Install `jev-mcp` from this marketplace after configuring the key. The plugin does not change the user's model or dispatch settings on installation.
