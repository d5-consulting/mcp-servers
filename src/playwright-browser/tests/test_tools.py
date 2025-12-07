import pytest
from fastmcp import Client

from playwright_browser import mcp


@pytest.mark.asyncio
async def test_browser_tools():
    """Test browser navigation, content extraction, and evaluation."""
    async with Client(mcp) as client:
        # Test navigate
        res = await client.call_tool("navigate", {"url": "https://example.com"})
        assert "Navigated to" in res.content[0].text
        assert "Example Domain" in res.content[0].text

        # Test get_content
        res = await client.call_tool("get_content", {})
        assert "Example Domain" in res.content[0].text

        # Test get_url
        res = await client.call_tool("get_url", {})
        assert "example.com" in res.content[0].text

        # Test get_title
        res = await client.call_tool("get_title", {})
        assert "Example Domain" in res.content[0].text

        # Test evaluate
        res = await client.call_tool("evaluate", {"script": "1 + 1"})
        assert res.content[0].text == "2"

        # Test close_browser
        res = await client.call_tool("close_browser", {})
        assert "Browser closed" in res.content[0].text
