import pytest
from fastmcp import Client

from langquery.prompts import mcp


@pytest.mark.asyncio
async def test_langquery():
    async with Client(mcp) as client:
        res = await client.get_prompt(
            "langqquery",
            {
                "input": "test",
                "scratchpad": "",
                "tools": "",
            },
        )
        assert res.messages[0].content.text


@pytest.mark.asyncio
async def test_get_langquery_prompt():
    async with Client(mcp) as client:
        res = await client.call_tool(
            "get_langquery_prompt",
            {
                "input": "test",
                "scratchpad": "",
                "tools": "",
            },
        )
        assert res.content[0].text
