import os

from openai import OpenAI

from . import mcp

DEFAULT_MODEL = "o3"


def get_client() -> OpenAI:
    """Get OpenAI client instance."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set")
    return OpenAI(api_key=api_key)


@mcp.tool()
def o3_search(input: str) -> str:
    """
    An AI agent with advanced web search capabilities.
    Useful for finding the latest information, troubleshooting errors, and discussing ideas or design challenges.
    Supports natural language queries.

    Args:
        input: Ask questions, search for information, or consult about complex problems in English.

    Returns:
        Response from o3 with web search results and analysis.
    """
    client = get_client()
    model = os.getenv("O3_MODEL", DEFAULT_MODEL)

    try:
        response = client.responses.create(
            model=model,
            tools=[{"type": "web_search_preview"}],
            input=input,
        )
        return response.output_text
    except Exception as e:
        return f"Error: {e}"
