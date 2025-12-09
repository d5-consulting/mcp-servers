import pytest
from fastmcp import Client

from shell.tools import mcp


@pytest.mark.asyncio
async def test_shell():
    async with Client(mcp) as client:
        msg = "test"
        res = await client.call_tool("shell", {"command": f"echo {msg}"})
        assert res.content[0].text == f"{msg}\n"


@pytest.mark.asyncio
async def test_shell_with_stderr():
    async with Client(mcp) as client:
        res = await client.call_tool("shell", {"command": "ls /nonexistent_dir_12345"})
        assert "stderr" in res.content[0].text.lower()


@pytest.mark.asyncio
async def test_shell_multiline():
    async with Client(mcp) as client:
        res = await client.call_tool("shell", {"command": "echo 'line1'; echo 'line2'"})
        text = res.content[0].text
        assert "line1" in text
        assert "line2" in text
