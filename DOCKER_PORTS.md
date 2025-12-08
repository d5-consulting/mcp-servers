# Docker Port Assignments

This document tracks port assignments for all MCP servers to prevent conflicts when running multiple containers.

## Port Allocation Table

| Server       | Port | URL                           | Notes                                    |
|--------------|------|-------------------------------|------------------------------------------|
| pdf          | 8001 | http://localhost:8001/sse     | PDF manipulation and extraction          |
| vectorstore  | 8002 | http://localhost:8002/sse     | Vector database operations               |
| pptx         | 8003 | http://localhost:8003/sse     | PowerPoint operations                    |
| xlsx         | 8004 | http://localhost:8004/sse     | Spreadsheet operations                   |
| docx         | 8005 | http://localhost:8005/sse     | Word document operations                 |
| langquery    | 8006 | http://localhost:8006/sse     | Language query operations                |
| browser      | 8007 | http://localhost:8007/sse     | Browser automation (Playwright)          |
| **composite**| **8000** | **http://localhost:8000/sse** | **Unified server (all servers bundled)** |
| **proxy**    | **8000** | **http://localhost:8000/sse** | **Lightweight proxy (routes to backends)** |

## Usage Notes

### Running Individual Servers

Each server can run independently on its assigned port:

```bash
cd src/<server-name>
docker compose up -d
```

### Running Composite Server

The composite server bundles all MCP servers into one container:

```bash
cd src/composite
docker compose up -d
```

**Use composite when:**
- You want simplest deployment (one container)
- Latency is critical (no network overhead)
- You always need multiple servers together

### Running Proxy Server

The proxy server routes requests to independent backend containers:

```bash
cd src/proxy
docker compose up -d
```

**Use proxy when:**
- You need independent backend scaling
- You want fast builds (proxy is lightweight)
- You only need subset of servers
- You want microservices architecture

### For Dify Integration

**Two Options** - both expose the same URL for Dify:

**Option A: Composite Server** (simpler)
- Edit `src/composite/composite-config.yaml` to enable/disable servers
- Run: `cd src/composite && docker compose up -d`
- Connect Dify to: `http://localhost:8000/sse`

**Option B: Proxy Server** (more flexible)
- Edit `src/proxy/proxy-config.yaml` to enable/disable backends
- Run: `cd src/proxy && docker compose up -d`
- Connect Dify to: `http://localhost:8000/sse`

**Important**: Do NOT run composite AND proxy simultaneously - they both use port 8000.

### Port Conflict Prevention

**Scenario 1**: Running composite + individual servers
- ❌ DON'T: Run `composite` with browser enabled AND `browser` container
- ✓ DO: Disable browser in composite config, run browser container separately

**Scenario 2**: Running multiple individual servers
- ✓ DO: Run any combination of individual servers (no conflicts)
- Example: `browser` (8007) + `pdf` (8001) + `xlsx` (8004)

**Scenario 3**: Testing locally vs Docker
- ✓ DO: Change docker-compose port mappings if running local dev on same port
- Example: Change `"8000:8000"` to `"8010:8000"` to avoid conflict with local port 8000

## Changing Ports

To change a server's external port, edit its `docker-compose.yml`:

```yaml
ports:
  - "9000:8000"  # External:Internal
  # Now accessible at http://localhost:9000/sse
```

The internal port (right side) should not be changed without also updating the Dockerfile ENV variables.
