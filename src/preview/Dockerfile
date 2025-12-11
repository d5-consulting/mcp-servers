FROM python:3.12-slim

WORKDIR /app

# Install uv
RUN pip install uv

# Copy workspace files
COPY ../../pyproject.toml ../../uv.lock ./
COPY ../../src/core ./src/core
COPY . ./src/preview

# Install dependencies
RUN uv sync --package preview

# Expose ports
EXPOSE 8014 3000

# Run the server
CMD ["uv", "run", "python", "-m", "preview"]
