# mcp composite server

a bundled mcp server that aggregates multiple mcp servers into a single endpoint using fastmcp's `mount()` feature.

## features

- **simple composition**: use fastmcp's built-in `mount()` to combine servers
- **tool namespacing**: prefixes prevent naming conflicts (e.g., `lang_query`)
- **no proxy overhead**: direct in-process communication
- **single endpoint**: clients see one url with all tools available

## installation

```bash
cd src/composite
uv sync
```

## usage

### standalone

```bash
# stdio transport (default)
cd src/composite
uv run python -m composite

# sse transport for web clients
TRANSPORT=sse PORT=8000 uv run python -m composite
```

### connect to dify

in dify mcp configuration:
```json
{
  "server_name": {
    "url": "http://host.docker.internal:8000/sse",
    "headers": {},
    "timeout": 50,
    "sse_read_timeout": 50
  }
}
```

## configuration

environment variables:
- `NAME`: server name (default: "composite")
- `TRANSPORT`: "stdio" or "sse" (default: "stdio")
- `HOST`: server host for sse (default: "0.0.0.0")
- `PORT`: server port for sse (default: 8000)
- `ALLOW_ORIGIN`: cors origin (default: "*")

## adding servers

edit `src/composite/server.py` to mount additional servers:

```python
from fastmcp import FastMCP
from langquery import mcp as langquery_mcp
from another_server import mcp as another_mcp

mcp = FastMCP("composite")

# mount servers with prefixes
mcp.mount(langquery_mcp, prefix="lang")
mcp.mount(another_mcp, prefix="another")
```

tools will be available as `lang_*` and `another_*`.

## available tools

currently mounts langquery server with `lang_` prefix:

- `lang_get_langquery_prompt` - get prompt for langquery
- `lang_shell` - execute shell commands
- `lang_query` - query data sources
- `lang_get_query_history` - get query history
- `lang_get_cached_result` - get cached results
- `lang_search_query_history` - search query history
- `lang_clear_query_history` - clear query history
- `lang_add`, `lang_sub`, `lang_mul`, `lang_div` - arithmetic operations

## testing

```bash
cd src/composite
uv run pytest -v
```

## development

key files:
- `src/composite/server.py`: main server with mount configuration
- `composite-config.yaml`: optional backend configuration (for future use)
