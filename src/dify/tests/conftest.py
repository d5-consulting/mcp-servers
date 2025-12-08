"""Test configuration and fixtures."""

import pytest
import pytest_asyncio
from fastmcp import Context


@pytest_asyncio.fixture(scope="function")
async def mock_context():
    """Create a mock FastMCP context for testing."""

    class MockState:
        def __init__(self):
            from dify.tools import DifyClient

            self.client = DifyClient(
                api_key="test-api-key",
                base_url="https://test.dify.ai/v1",
                console_api_key="test-console-key",
                console_base_url="https://test.dify.ai",
            )

    class MockRequestContext:
        def __init__(self):
            self.state = MockState()

    class MockContext:
        def __init__(self):
            self.request_context = MockRequestContext()

    ctx = MockContext()
    yield ctx
    # Clean up the HTTP client
    await ctx.request_context.state.client.close()
