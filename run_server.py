#!/usr/bin/env python3
"""Entry point for running the GEPA MCP server"""

from src.gepa_mcp.gepa_server import mcp

if __name__ == "__main__":
    mcp.run(transport="stdio")