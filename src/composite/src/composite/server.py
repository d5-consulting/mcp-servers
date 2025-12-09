"""MCP Composite Server - Aggregates multiple backend MCP servers into a single endpoint."""

import os

from dotenv import load_dotenv
from fastmcp import FastMCP
from langquery import mcp as langquery_mcp

load_dotenv()

mcp = FastMCP(os.getenv("NAME", "composite"))

# Mount langquery server with "lang" prefix
# Tools will be available as: lang_shell, lang_query, lang_add, etc.
mcp.mount(langquery_mcp, prefix="lang")


def serve():
    """Start MCP server."""
    from starlette.middleware import Middleware
    from starlette.middleware.cors import CORSMiddleware

    cors_middleware = Middleware(
        CORSMiddleware,
        allow_origins=[os.getenv("ALLOW_ORIGIN", "*")],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    transport = os.getenv("TRANSPORT", "stdio")

    if transport == "stdio":
        mcp.run(transport="stdio")
    else:
        mcp.run(
            transport=transport,
            host=os.getenv("HOST", "0.0.0.0"),
            port=int(os.getenv("PORT", 8000)),
            middleware=[cors_middleware],
        )
