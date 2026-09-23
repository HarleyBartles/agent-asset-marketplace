"""Validate the installable Jev MCP connection without making a provider call."""

import json
from pathlib import Path


PLUGIN = Path(__file__).resolve().parents[3]


def test_remote_mcp_uses_documented_endpoint_and_external_key() -> None:
    manifest = json.loads((PLUGIN / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
    assert manifest["mcpServers"] == "./.mcp.json"

    config = json.loads((PLUGIN / ".mcp.json").read_text(encoding="utf-8"))
    assert config == {
        "mcpServers": {
            "jev": {
                "type": "http",
                "url": "https://www.jevai.org/api/mcp",
                "bearer_token_env_var": "JEV_API_KEY",
            }
        }
    }
