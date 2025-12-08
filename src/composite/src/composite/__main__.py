"""Entry point for the MCP composite server."""

import asyncio
from composite.server import main

if __name__ == "__main__":
    asyncio.run(main())
