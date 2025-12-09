"""MCP Composite Server - Aggregates multiple backend MCP servers into a single endpoint."""

import asyncio
import logging
import os
from pathlib import Path
from typing import Any

import yaml
from fastmcp import FastMCP
from mcp import ClientSession
from mcp.client.sse import sse_client

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def load_config() -> dict[str, Any]:
    """Load composite configuration from YAML file."""
    config_path = os.getenv("COMPOSITE_CONFIG_PATH")

    if not config_path:
        # Try default locations
        candidates = [
            Path.cwd() / "composite-config.yaml",
            Path(__file__).parent.parent.parent / "composite-config.yaml",
        ]
        for candidate in candidates:
            if candidate.exists():
                config_path = str(candidate)
                break

    if not config_path or not Path(config_path).exists():
        raise FileNotFoundError(
            "No configuration file found. Set COMPOSITE_CONFIG_PATH or create composite-config.yaml"
        )

    with open(config_path) as f:
        return yaml.safe_load(f)


class BackendConnection:
    """Manages a persistent MCP client connection to a backend server using a background task."""

    def __init__(self, name: str, url: str, prefix: str):
        self.name = name
        self.url = url
        self.prefix = prefix
        self._connected = False
        self._task: asyncio.Task | None = None
        self._request_queue: asyncio.Queue | None = None
        self._stop_event: asyncio.Event | None = None

    async def start(self) -> bool:
        """Start the background connection task."""
        self._request_queue = asyncio.Queue()
        self._stop_event = asyncio.Event()
        self._task = asyncio.create_task(self._connection_loop())

        # Wait a bit for connection to establish
        for _ in range(50):  # 5 second timeout
            await asyncio.sleep(0.1)
            if self._connected:
                return True
        return False

    async def _connection_loop(self):
        """Background task that maintains the SSE connection and processes requests."""
        try:
            async with sse_client(self.url) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    self._connected = True
                    logger.info(f"Connected to backend: {self.name} at {self.url}")

                    # Process requests until stopped
                    while not self._stop_event.is_set():
                        try:
                            # Wait for request with timeout to check stop event
                            request = await asyncio.wait_for(
                                self._request_queue.get(), timeout=0.5
                            )
                            method, args, response_future = request

                            try:
                                if method == "list_tools":
                                    result = await session.list_tools()
                                elif method == "call_tool":
                                    result = await session.call_tool(*args)
                                elif method == "list_prompts":
                                    result = await session.list_prompts()
                                elif method == "get_prompt":
                                    result = await session.get_prompt(*args)
                                else:
                                    result = Exception(f"Unknown method: {method}")

                                response_future.set_result(result)
                            except Exception as e:
                                response_future.set_exception(e)
                        except asyncio.TimeoutError:
                            continue
        except Exception as e:
            logger.error(f"Backend {self.name} connection error: {e}")
        finally:
            self._connected = False

    async def _call(self, method: str, *args) -> Any:
        """Make a request to the backend via the background task."""
        if not self._connected or self._request_queue is None:
            raise Exception(f"Backend {self.name} not connected")

        loop = asyncio.get_event_loop()
        response_future = loop.create_future()
        await self._request_queue.put((method, args, response_future))
        return await response_future

    async def list_tools(self):
        return await self._call("list_tools")

    async def call_tool(self, name: str, arguments: dict):
        return await self._call("call_tool", name, arguments)

    async def list_prompts(self):
        return await self._call("list_prompts")

    async def get_prompt(self, name: str, arguments: dict | None):
        return await self._call("get_prompt", name, arguments)

    async def stop(self):
        """Stop the background connection task."""
        if self._stop_event:
            self._stop_event.set()
        if self._task:
            try:
                await asyncio.wait_for(self._task, timeout=5.0)
            except asyncio.TimeoutError:
                self._task.cancel()
        self._connected = False

    @property
    def is_connected(self) -> bool:
        return self._connected


# Global state
backends: dict[str, BackendConnection] = {}
mcp = FastMCP("mcp-composite")
_backends_initialized = False


async def ensure_backends_connected():
    """Lazily connect to backends on first use."""
    global _backends_initialized
    if not _backends_initialized:
        await connect_backends()
        _backends_initialized = True


async def connect_backends():
    """Connect to all configured backends."""
    config = load_config()

    for backend_cfg in config["backends"]:
        if backend_cfg.get("enabled", True):
            name = backend_cfg["name"]
            backends[name] = BackendConnection(
                name=name,
                url=backend_cfg["url"],
                prefix=backend_cfg.get("prefix", name),
            )

    tasks = [backend.start() for backend in backends.values()]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    connected = sum(1 for r in results if r is True)
    logger.info(f"Connected to {connected}/{len(backends)} backends")


@mcp.tool()
async def composite_list_backends() -> str:
    """List all configured backends and their connection status."""
    await ensure_backends_connected()
    result = []
    for name, backend in backends.items():
        status = "connected" if backend.is_connected else "disconnected"
        result.append(f"{name}: {status} ({backend.url})")
    return "\n".join(result) if result else "No backends configured"


@mcp.tool()
async def composite_list_tools() -> str:
    """List all tools available from all connected backends."""
    await ensure_backends_connected()
    all_tools = []
    for backend in backends.values():
        if backend.is_connected:
            try:
                result = await backend.list_tools()
                for tool in result.tools:
                    all_tools.append(f"{backend.prefix}_{tool.name}: {tool.description}")
            except Exception as e:
                all_tools.append(f"{backend.name}: Error listing tools - {e}")
    return "\n".join(all_tools) if all_tools else "No tools available"


@mcp.tool()
async def composite_call_tool(tool_name: str, arguments: dict | None = None) -> str:
    """Call a tool from a backend. Use prefix_toolname format (e.g., 'lang_query')."""
    await ensure_backends_connected()
    arguments = arguments or {}

    for backend in backends.values():
        if tool_name.startswith(f"{backend.prefix}_"):
            if not backend.is_connected:
                return f"Error: Backend {backend.name} not connected"

            original_name = tool_name[len(backend.prefix) + 1:]
            try:
                result = await backend.call_tool(original_name, arguments)
                # Format the result content
                output = []
                for content in result.content:
                    if hasattr(content, 'text'):
                        output.append(content.text)
                    else:
                        output.append(str(content))
                return "\n".join(output)
            except Exception as e:
                return f"Error calling tool: {e}"

    return f"Tool not found: {tool_name}"


def serve():
    """Start MCP server."""
    from starlette.middleware import Middleware
    from starlette.middleware.cors import CORSMiddleware

    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))

    logger.info("Starting MCP Composite Server")

    # Load config to show backends
    config = load_config()
    enabled_backends = [b["name"] for b in config["backends"] if b.get("enabled", True)]
    logger.info(f"Backends: {', '.join(enabled_backends)}")
    logger.info(f"Listening on {host}:{port}/sse")

    cors_middleware = Middleware(
        CORSMiddleware,
        allow_origins=[os.getenv("ALLOW_ORIGIN", "*")],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Use FastMCP's run method
    mcp.run(
        transport="sse",
        host=host,
        port=port,
        middleware=[cors_middleware],
    )
