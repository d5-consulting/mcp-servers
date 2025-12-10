import os
from unittest.mock import Mock, patch

import pytest
from fastmcp import Client

from o3_search import mcp


@pytest.mark.asyncio
async def test_o3_search_mock():
    """Test o3_search tool with mocked API."""
    with patch("o3_search.tools.get_client") as mock_get_client:
        mock_response = Mock()
        mock_response.output_text = "Mocked response"
        mock_client = Mock()
        mock_client.responses.create.return_value = mock_response
        mock_get_client.return_value = mock_client

        async with Client(mcp) as client:
            result = await client.call_tool("o3-search", {"query": "test query"})
            assert result.content
            assert "Mocked response" in result.content[0].text


@pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="Requires OPENAI_API_KEY")
@pytest.mark.asyncio
async def test_o3_search_integration():
    """Test o3_search tool with real API call."""
    async with Client(mcp) as client:
        result = await client.call_tool("o3-search", {"query": "What is 2 + 2?"})
        assert result.content
        assert len(result.content) > 0
        assert result.content[0].text
        assert len(result.content[0].text) > 0
