# MCP Server Guide

This guide covers common operations for all MCP servers in this monorepo.

## Installation

All servers share the same installation process using `uv`:

```bash
# Install all dependencies
uv sync --dev

# Or install a specific server
uv sync --package <server-name>
```

## Running Servers

### Using uv (Recommended)

```bash
# Run a server with default settings (stdio transport)
uv run python -m <module_name>

# Run with SSE transport
uv run python -m <module_name> --transport sse --port 8000

# Run with environment variables
TRANSPORT=sse PORT=8000 uv run python -m <module_name>
```

### Using Docker (Optional)

```bash
# Build and run with docker-compose
cd src/<server-name>
docker compose up
```

## CLI Arguments

All servers support the following command-line arguments:

| Argument | Default | Description |
|----------|---------|-------------|
| `--transport` | `stdio` | Transport protocol: `stdio`, `sse`, or `streamable-http` |
| `--host` | `0.0.0.0` | Host to bind to |
| `--port` | varies | Port to listen on (server-specific default) |
| `--allow-origin` | `*` | CORS allowed origin |

## Environment Variables

Environment variables can be used instead of CLI arguments:

| Variable | Description |
|----------|-------------|
| `NAME` | Server name (for identification) |
| `TRANSPORT` | Transport protocol |
| `HOST` | Host to bind to |
| `PORT` | Port to listen on |
| `ALLOW_ORIGIN` | CORS allowed origins |

## Testing

```bash
# Run tests for a specific server
cd src/<server-name>
uv run pytest -v

# Run all tests
uv run pytest
```

## Claude Desktop Configuration

To use a server with Claude Desktop, add it to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "<server-name>": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/mcp-servers/src/<server-name>",
        "run",
        "python",
        "-m",
        "<module_name>"
      ],
      "env": {
        "ENV_VAR": "value"
      }
    }
  }
}
```

Replace `<server-name>` and `<module_name>` with the appropriate values from the table below.

## Server Reference

| Server | Module | Port | Description |
|--------|--------|------|-------------|
| browser | `browser` | 8007 | Playwright browser automation |
| composite | `composite` | 8000 | Aggregates multiple MCP servers |
| data-analysis | `data_analysis` | 8006 | DuckDB SQL data analysis |
| dify | `dify` | 8001 | Dify AI workflow integration |
| docx | `docx` | 8005 | Word document operations |
| file-management | `file_management` | 8010 | File read/write operations |
| frontend-design | `frontend_design` | 8009 | Design themes and palettes |
| nano-banana | `nano_banana` | 8013 | AI image generation (Gemini) |
| o3-search | `o3_search` | 8012 | OpenAI o3 web search |
| pdf | `pdf` | 8008 | PDF extraction and manipulation |
| pptx | `pptx_mcp` | 8003 | PowerPoint operations |
| shell | `shell` | 8011 | Shell command execution |
| vectorstore | `vectorstore` | 8002 | ChromaDB vector operations |
| xlsx | `xlsx` | 8004 | Excel spreadsheet operations |
