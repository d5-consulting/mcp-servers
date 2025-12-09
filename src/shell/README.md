# Shell MCP Server

MCP server for executing shell commands.

## Features

- Execute shell commands
- Capture stdout and stderr
- Return combined output

## Tools

### shell

Execute a shell command and return the output.

**Parameters:**
- `command` (required): Shell command to execute

**Returns:**
- Command output (stdout, and stderr if present)

## Installation

```bash
cd src/shell
uv sync
```

## Running

```bash
# stdio mode (default)
uv run fastmcp run shell

# SSE mode
TRANSPORT=sse PORT=8011 uv run fastmcp run shell
```

## Testing

```bash
cd src/shell
uv run pytest -v
```
