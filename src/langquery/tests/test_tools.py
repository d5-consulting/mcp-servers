import pytest
from fastmcp import Client

from langquery.tools import mcp


@pytest.mark.asyncio
async def test_add():
    async with Client(mcp) as client:
        res = await client.call_tool("add", {"a": 1, "b": 2})
        assert res.content[0].text == "3"


@pytest.mark.asyncio
async def test_sub():
    async with Client(mcp) as client:
        res = await client.call_tool("sub", {"a": 2, "b": 1})
        assert res.content[0].text == "1"


@pytest.mark.asyncio
async def test_mul():
    async with Client(mcp) as client:
        res = await client.call_tool("mul", {"a": 2, "b": 3})
        assert res.content[0].text == "6"


@pytest.mark.asyncio
async def test_div():
    async with Client(mcp) as client:
        res = await client.call_tool("div", {"a": 2, "b": 1})
        assert res.content[0].text == "2.0"


@pytest.mark.asyncio
async def test_shell():
    async with Client(mcp) as client:
        msg = "test"
        res = await client.call_tool("shell", {"command": f"echo {msg}"})
        assert res.content[0].text == f"{msg}\n"


@pytest.mark.asyncio
async def test_query():
    async with Client(mcp) as client:
        res = await client.call_tool("query", {"sql": "SELECT 1 as test"})
        assert "test" in res.content[0].text
