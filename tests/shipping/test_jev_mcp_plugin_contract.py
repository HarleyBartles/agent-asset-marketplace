"""Validate the installable Jev MCP connection without making a provider call."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PLUGIN = ROOT / "dist/plugins/jev-mcp"


def test_remote_mcp_uses_documented_endpoint_and_external_key() -> None:
    manifest = json.loads((PLUGIN / "plugin.json").read_text(encoding="utf-8"))
    assert manifest["$schema"] == "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
    assert "mcpServers" not in manifest
    assert not (PLUGIN / ".claude-plugin").exists()

    config = json.loads((PLUGIN / "mcp.json").read_text(encoding="utf-8"))
    assert config["$schema"] == "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json"
    assert config == {
        "$schema": "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json",
        "mcpServers": {
            "jev": {
                "type": "streamable-http",
                "url": "https://www.jevai.org/api/mcp",
                "headers": {"Authorization": "Bearer ${JEV_API_KEY}"},
            }
        },
    }
