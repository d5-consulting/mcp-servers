import pytest
from fastmcp import Client

from o3_search import mcp


@pytest.mark.asyncio
async def test_o3_search():
    """Test o3_search tool returns a response."""
    async with Client(mcp) as client:
        result = await client.call_tool("o3_search", {"input": "What is 2 + 2?"})
        assert result.content
        assert len(result.content) > 0
        assert result.content[0].text
        # Should contain some response text
        assert len(result.content[0].text) > 0
