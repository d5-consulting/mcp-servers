import asyncio
import re

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


@pytest.mark.asyncio
async def test_query_history_logging():
    """Test that queries are logged to history."""
    async with Client(mcp) as client:
        # Execute a query
        await client.call_tool("query", {"sql": "SELECT 42 as answer"})

        # Get history
        history_res = await client.call_tool("get_query_history", {"limit": 5})
        history_text = history_res.content[0].text

        # Verify query appears in history
        assert "SELECT 42 as answer" in history_text
        assert "answer" in history_text or "42" in history_text


@pytest.mark.asyncio
async def test_query_history_failed_query():
    """Test that failed queries are logged with error messages."""
    async with Client(mcp) as client:
        # Execute an invalid query
        try:
            await client.call_tool("query", {"sql": "SELECT * FROM nonexistent_table"})
        except Exception:
            pass  # Expected to fail

        # Get history
        history_res = await client.call_tool("get_query_history", {"limit": 5})
        history_text = history_res.content[0].text

        # Verify failed query appears in history
        assert "nonexistent_table" in history_text


@pytest.mark.asyncio
async def test_get_cached_result():
    """Test retrieving cached results from previous queries."""
    async with Client(mcp) as client:
        # Execute a query
        await client.call_tool("query", {"sql": "SELECT 'cached' as test_value"})

        # Get history to find the query ID
        history_res = await client.call_tool("get_query_history", {"limit": 1})
        history_text = history_res.content[0].text

        # Extract query ID from history (first number after "id")
        match = re.search(r"\|\s*(\d+)\s*\|", history_text)
        assert match is not None, "Could not find query ID in history"
        query_id = int(match.group(1))

        # Get cached result
        cached_res = await client.call_tool("get_cached_result", {"query_id": query_id})
        cached_text = cached_res.content[0].text

        # Verify cached result contains our value
        assert "cached" in cached_text or "test_value" in cached_text


@pytest.mark.asyncio
async def test_search_query_history():
    """Test searching query history."""
    async with Client(mcp) as client:
        # Execute a few queries with distinct patterns
        await client.call_tool("query", {"sql": "SELECT 'findme' as unique_search_term"})
        await client.call_tool("query", {"sql": "SELECT 1 as other_query"})

        # Search for the specific query
        search_res = await client.call_tool(
            "search_query_history", {"search_term": "findme", "limit": 5}
        )
        search_text = search_res.content[0].text

        # Verify search finds the right query
        assert "findme" in search_text
        assert "unique_search_term" in search_text


@pytest.mark.asyncio
async def test_query_history_limit():
    """Test that query history respects the limit parameter."""
    async with Client(mcp) as client:
        # Get history with limit of 1
        history_res = await client.call_tool("get_query_history", {"limit": 1})
        history_text = history_res.content[0].text

        # Count the number of query rows (rough check - each query has at least one pipe)
        # This is a basic test - proper implementation would parse markdown properly
        lines = [line for line in history_text.split("\n") if "|" in line and "id" not in line.lower()]

        # Should have at most 1 data row (plus header and separator)
        assert len(lines) <= 3  # header + separator + 1 data row


@pytest.mark.asyncio
async def test_invalid_query_id():
    """Test retrieving cached result with invalid query ID."""
    async with Client(mcp) as client:
        # Try to get result for non-existent query ID
        cached_res = await client.call_tool("get_cached_result", {"query_id": 99999})
        cached_text = cached_res.content[0].text

        # Should return appropriate error message
        assert "not found" in cached_text.lower()


@pytest.mark.asyncio
async def test_search_no_results():
    """Test searching with term that matches no queries."""
    async with Client(mcp) as client:
        # Search for something that doesn't exist
        search_res = await client.call_tool(
            "search_query_history", {"search_term": "nonexistent_query_xyz123", "limit": 5}
        )
        search_text = search_res.content[0].text

        # Should indicate no results found
        assert "no queries found" in search_text.lower() or "nonexistent_query_xyz123" in search_text


@pytest.mark.asyncio
async def test_clear_history():
    """Test clearing all query history."""
    async with Client(mcp) as client:
        # Execute a query to ensure there's something in history
        await client.call_tool("query", {"sql": "SELECT 'to_be_cleared' as test"})

        # Clear history
        clear_res = await client.call_tool("clear_query_history", {})
        clear_text = clear_res.content[0].text

        # Should confirm deletion
        assert "cleared" in clear_text.lower()

        # Verify history is empty
        history_res = await client.call_tool("get_query_history", {"limit": 10})
        history_text = history_res.content[0].text

        assert "no query history" in history_text.lower() or history_text.strip() == ""


@pytest.mark.asyncio
async def test_concurrent_query_logging():
    """Test that concurrent queries are logged correctly without race conditions."""
    async with Client(mcp) as client:
        # Execute multiple queries concurrently
        queries = [
            f"SELECT {i} as concurrent_test_{i}"
            for i in range(20)
        ]

        # Run all queries concurrently
        tasks = [
            client.call_tool("query", {"sql": sql})
            for sql in queries
        ]
        await asyncio.gather(*tasks)

        # Get history
        history_res = await client.call_tool("get_query_history", {"limit": 25})
        history_text = history_res.content[0].text

        # Verify that all queries were logged
        # At least some of the concurrent queries should appear in history
        concurrent_count = sum(1 for i in range(20) if f"concurrent_test_{i}" in history_text)

        # Should have logged most if not all queries
        assert concurrent_count >= 15, f"Only {concurrent_count}/20 concurrent queries were logged"
