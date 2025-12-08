# mcp proxy server

a lightweight reverse proxy that aggregates multiple mcp backend servers into a single endpoint. unlike the composite server which bundles all dependencies, the proxy routes requests to independently running backend servers.

## features

- **lightweight**: minimal dependencies, fast builds (<1 min vs 10+ min for composite)
- **flexible deployment**: backends can scale independently
- **runtime reconfiguration**: enable/disable backends without rebuilding
- **tool namespacing**: prefixes prevent naming conflicts
- **single endpoint**: dify sees one url, proxy handles routing

## architecture comparison

### proxy approach (this server)
```
dify → proxy:8000 → browser:8007
                  → pdf:8001
                  → xlsx:8004
                  → ...
```

**pros:**
- tiny proxy image (~200mb vs 1.5gb composite)
- fast builds (~1 min proxy, backends build in parallel)
- independent scaling
- selective deployment (only run backends you need)

**cons:**
- requires all backend containers running
- network hop adds latency (~5-10ms)
- more complex orchestration (n+1 containers)

### composite approach (alternative)
```
dify → composite:8000 (all servers bundled)
```

**pros:**
- single container
- no network overhead
- simpler deployment

**cons:**
- large image (~1.5gb)
- slow builds (~10+ min)
- monolithic

## installation

```bash
cd src/proxy
uv sync
```

## quick start with docker

### 1. configure environment variables

```bash
cp .env.example .env
# edit .env with your api keys
```

### 2. configure backends

edit `proxy-config.yaml` to enable/disable backends:

```yaml
backends:
  - name: browser
    url: http://browser:8007/sse
    enabled: true  # set to false to disable

  - name: dify
    url: http://dify:8001/sse
    enabled: true
```

### 3. build and run

```bash
docker compose up -d
```

the proxy will be available at: **http://localhost:8000/sse**

## configuration

### proxy-config.yaml

```yaml
backends:
  - name: browser           # unique identifier
    url: http://browser:8007/sse  # backend sse endpoint
    prefix: browser        # tool name prefix
    enabled: true          # enable/disable
    description: browser automation
```

**configuration fields:**
- `name`: unique backend identifier
- `url`: backend server sse endpoint (use docker service names)
- `prefix`: prepended to tool names (e.g., `browser_navigate`)
- `enabled`: set to false to disable without removing config
- `description`: human-readable description (optional)

### environment variables

**proxy configuration:**
- `PROXY_CONFIG_PATH`: path to yaml config (default: ./proxy-config.yaml)
- `HOST`: server host (default: 0.0.0.0)
- `PORT`: server port (default: 8000)

**backend-specific** (see individual server docs):
- `DIFY_API_KEY`, `DIFY_CONSOLE_API_KEY`: required if dify enabled
- `OPENAI_API_KEY`: required if vectorstore enabled
- `BROWSER_TIMEOUT`, `NAVIGATION_TIMEOUT`: optional browser config

## usage

### standalone (no docker)

```bash
# start backend servers first
cd src/browser && TRANSPORT=sse PORT=8007 uv run python -m browser &
cd src/pdf && TRANSPORT=sse PORT=8001 uv run python -m pdf &
# ...

# start proxy
cd src/proxy
PROXY_CONFIG_PATH=./proxy-config.yaml uv run python -m proxy
```

### docker compose

```bash
# start all services
docker compose up -d

# view logs
docker compose logs -f proxy

# stop services
docker compose down
```

### connect to dify

in dify configuration:
- **url**: `http://localhost:8000/sse`
- **transport**: sse

## port allocation

see [../../DOCKER_PORTS.md](../../DOCKER_PORTS.md) for complete port assignments:

- proxy: 8000
- pdf: 8001
- vectorstore: 8002
- pptx: 8003
- xlsx: 8004
- docx: 8005
- langquery: 8006
- browser: 8007
- dify: 8001

## selective deployment

only run the backends you need:

```yaml
# proxy-config.yaml - enable only browser and pdf
backends:
  - name: browser
    enabled: true

  - name: pdf
    enabled: true

  - name: xlsx
    enabled: false  # disabled

  - name: docx
    enabled: false  # disabled
```

then in docker-compose.yml, comment out unused services or use profiles:

```bash
# only start proxy and enabled backends
docker compose up -d proxy browser pdf
```

## troubleshooting

### error: connection refused to backend

check if backend service is running:
```bash
docker compose ps
docker compose logs browser  # check specific backend
```

ensure backend urls in `proxy-config.yaml` use docker service names (not localhost).

### error: no configuration file found

set `PROXY_CONFIG_PATH` environment variable:
```bash
export PROXY_CONFIG_PATH=/path/to/proxy-config.yaml
```

### tools not appearing in dify

1. check proxy logs: `docker compose logs proxy`
2. verify backend is enabled in config
3. test backend directly: `curl http://localhost:8007/sse` (adjust port)
4. ensure backend has `TRANSPORT=sse` environment variable

### high latency

the proxy adds a network hop (~5-10ms per request). if latency is critical:
- use composite server instead (no proxy overhead)
- ensure all containers on same docker network
- consider deploying on same host

## comparison with composite

| feature | proxy | composite |
|---------|-------|-----------|
| image size | ~200mb | ~1.5gb |
| build time | ~1 min | ~10 min |
| containers | n+1 | 1 |
| latency | +5-10ms | none |
| scaling | independent | monolithic |
| deployment | complex | simple |

**use proxy when:**
- you need independent scaling
- you want fast builds
- you only need subset of servers
- you have multiple clients with different needs

**use composite when:**
- you want simplest deployment
- latency is critical
- you always need all servers
- you're primarily targeting dify

## testing

```bash
uv run pytest
```

## development

the proxy is intentionally minimal (~150 lines). key components:

- `server.py`: main proxy logic
- `proxy-config.yaml`: backend configuration
- `Dockerfile`: lightweight python:3.12-slim base
- `docker-compose.yml`: orchestrates proxy + backends

## architecture notes

**how tool routing works:**

1. client calls `browser_navigate`
2. proxy identifies prefix `browser` → routes to browser backend
3. strips prefix: `navigate`
4. forwards to `http://browser:8007/sse` with method `tools/call` and name `navigate`
5. backend processes request
6. proxy returns result to client

**why sse only:**

backends must expose sse endpoints because:
- dify requires sse transport
- http makes routing simpler than stdio
- containers communicate over network

**connection pooling:**

proxy maintains persistent httpx client for efficient backend communication. connections are reused across requests.
