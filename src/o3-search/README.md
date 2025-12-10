# O3 Search MCP Server

A thin MCP wrapper around OpenAI's o3 model with web search capabilities for deep research, planning, and problem-solving.

## Features

- Web search powered by OpenAI o3
- Natural language queries for research and planning
- Latest information retrieval
- Error troubleshooting assistance
- Design and architecture consulting

## Tools

### o3-search

An AI agent with advanced web search capabilities.

**Parameters:**
- `query` (required): Ask questions, search for information, or consult about complex problems in English.

**Returns:** Response from o3 with web search results and analysis.

## Requirements

- Python 3.12+
- OpenAI API key with access to o3 model

## Installation

Set the required environment variable:

```bash
export OPENAI_API_KEY=your_api_key_here
```

Optional environment variables:
- `O3_MODEL`: Model to use (default: `o3`)
- `NAME`: Server name (default: `o3-search`)
- `TRANSPORT`: Transport type (`stdio` or `sse`, default: `stdio`)
- `HOST`: Host for SSE transport (default: `0.0.0.0`)
- `PORT`: Port for SSE transport (default: `8012`)

## Usage

Run as a Python module (from repo root):

```bash
uv run python -m o3_search
```

Or with console script:

```bash
uv run o3-search
```

Or with SSE transport:

```bash
TRANSPORT=sse PORT=8012 uv run python -m o3_search
```

## Testing

```bash
cd src/o3-search
uv run pytest -v
```
