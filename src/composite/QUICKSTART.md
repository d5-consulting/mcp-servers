# MCP Proxy Server - Quick Start

Get all MCP servers accessible through a single URL using a lightweight proxy architecture.

## What's the Difference?

### Proxy (This Approach)
```
Dify → proxy:8000 → browser:8007
                  → pdf:8001
                  → xlsx:8004
```
- Lightweight proxy container (~200MB, builds in <1 min)
- Backend servers run independently
- Good for: flexible deployment, independent scaling

### Composite (Alternative)
```
Dify → composite:8000 (all servers bundled)
```
- Single large container (~1.5GB, builds in ~10 min)
- Everything in one place
- Good for: simplest deployment, lowest latency

## Prerequisites

- Docker and Docker Compose installed
- API keys for enabled backends (Dify, OpenAI if vectorstore is used)

## Setup (3 Steps)

### 1. Configure Environment Variables

```bash
cd src/proxy
cp .env.example .env
```

Edit `.env` and add your API keys:
```bash
DIFY_API_KEY=sk-your-dify-key-here
DIFY_CONSOLE_API_KEY=your-console-key-here
OPENAI_API_KEY=sk-your-openai-key-here  # if vectorstore enabled
```

### 2. Choose Which Backends to Enable

Edit `proxy-config.yaml` to control which MCP servers are included:

```yaml
backends:
  - name: browser
    enabled: true   # ✓ Include browser automation

  - name: pdf
    enabled: true   # ✓ Include PDF tools

  - name: xlsx
    enabled: false  # ✗ Skip Excel tools
```

**Default configuration**: All backends enabled

### 3. Build and Run

```bash
docker compose up -d
```

The proxy will be available at: **http://localhost:8000/sse**

This command will:
1. Build all enabled backend containers (in parallel)
2. Build the lightweight proxy container
3. Start the proxy and backends
4. Configure networking between containers

## Connect to Dify

In your Dify configuration, add an MCP server connection:

- **URL**: `http://localhost:8000/sse`
- **Transport**: SSE

You'll now have access to all enabled MCP tools through this single endpoint!

## Verify It's Working

Check the logs:
```bash
docker compose logs -f proxy
```

You should see:
```
Starting MCP Proxy Server
Backends: browser, pdf, xlsx, docx
Listening on 0.0.0.0:8000/sse
```

Test a backend directly:
```bash
# Check if browser backend is responding
curl http://localhost:8007/sse
```

## Common Operations

### Stop all services
```bash
docker compose down
```

### View backend logs
```bash
docker compose logs -f browser  # check specific backend
docker compose logs -f          # all services
```

### Restart after config changes
```bash
# After editing proxy-config.yaml
docker compose restart proxy
```

### Rebuild after code changes
```bash
docker compose up -d --build
```

## Enable/Disable Backends

To enable or disable backends, edit `proxy-config.yaml` and restart:

```bash
# 1. Edit proxy-config.yaml (change enabled: true/false)
# 2. Restart only the proxy
docker compose restart proxy

# Or restart backend if you changed its config
docker compose restart browser
```

No rebuild needed for config changes!

## Selective Deployment

Only run the backends you need to save resources:

```yaml
# proxy-config.yaml
backends:
  - name: browser
    enabled: true

  - name: pdf
    enabled: true

  - name: xlsx
    enabled: false  # Won't be queried
```

Then start only enabled services:
```bash
docker compose up -d proxy browser pdf
# Don't need to start xlsx
```

## Performance Tuning

### Build Optimization
Backends build in parallel - use Docker BuildKit:
```bash
DOCKER_BUILDKIT=1 docker compose build
```

### Resource Limits
Add resource limits to docker-compose.yml:
```yaml
services:
  browser:
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 2G
```

### Connection Pooling
The proxy maintains persistent HTTP connections to backends for efficiency.

## Troubleshooting

### Error: connection refused to backend

**Problem**: Proxy can't reach backend service

**Solutions**:
```bash
# 1. Check if backend is running
docker compose ps

# 2. Check backend logs
docker compose logs browser

# 3. Verify backend URL in proxy-config.yaml uses Docker service name
backends:
  - name: browser
    url: http://browser:8007/sse  # ✓ Use service name
    # NOT http://localhost:8007/sse  # ✗ Won't work in Docker
```

### Error: port already in use

**Problem**: Port 8000 is already allocated

**Solutions**:
```bash
# Option 1: Stop conflicting service
docker ps  # find container using port 8000
docker stop <container-id>

# Option 2: Change proxy port in docker-compose.yml
ports:
  - "9000:8000"  # Use external port 9000
```

### Tools not appearing in Dify

**Checklist**:
1. ✓ Backend is enabled in `proxy-config.yaml`
2. ✓ Backend container is running: `docker compose ps`
3. ✓ Backend is healthy: `docker compose logs browser`
4. ✓ Proxy sees the backend: `docker compose logs proxy`

**Debug**:
```bash
# Test backend directly
curl http://localhost:8007/sse

# Check proxy logs for errors
docker compose logs proxy | grep ERROR
```

### Slow response times

**Expected**: Proxy adds ~5-10ms latency per request (network hop)

**If slower**:
- Check if backends are overloaded: `docker stats`
- Ensure all containers on same Docker network
- Consider composite server if latency is critical

## Comparing with Composite

| Feature          | Proxy                  | Composite           |
|------------------|------------------------|---------------------|
| Image size       | ~200MB (proxy only)    | ~1.5GB              |
| Build time       | ~1 min                 | ~10 min             |
| Containers       | N+1 (proxy + backends) | 1                   |
| Latency          | +5-10ms                | none                |
| Scaling          | Independent            | Monolithic          |
| Resource usage   | Higher (multiple)      | Lower (single)      |
| Flexibility      | High                   | Medium              |

**Use proxy when**: You need flexibility, independent scaling, or fast development cycles

**Use composite when**: You want simplest deployment, or latency is critical

## Next Steps

- See [README.md](README.md) for architecture details
- See [../../DOCKER_PORTS.md](../../DOCKER_PORTS.md) for port assignments
- See individual backend docs in `src/*/README.md` for backend-specific features

## Advanced: Kubernetes Deployment

For production Kubernetes deployment:

1. Build and push images to registry:
```bash
docker compose build
docker tag proxy:latest your-registry/proxy:latest
docker push your-registry/proxy:latest
```

2. Create Kubernetes manifests for each service
3. Use Kubernetes services for backend discovery
4. Update proxy-config.yaml with K8s service names

Example backend URL in K8s:
```yaml
backends:
  - name: browser
    url: http://browser-service.default.svc.cluster.local:8007/sse
```
