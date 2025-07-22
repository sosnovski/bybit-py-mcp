
# Use Python 3.13 slim image
FROM python:3.13-slim@sha256:97fe872832570df2866e64d6e53bd899dcd2e9c974b8aa49eabb2e2cad7944d7

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir uv

# Copy project files
COPY pyproject.toml ./
COPY uv.lock* ./
COPY README.md ./

# Install dependencies
RUN uv sync --frozen --no-dev || uv sync --no-dev

# Copy source code
COPY src/ ./src/

# Set environment variables
ENV PYTHONPATH=/app/src
ENV PYTHONUNBUFFERED=1

# Default command
CMD ["uv", "run", "bybit-mcp"]
