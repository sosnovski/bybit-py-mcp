# Use Python 3.13 slim image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install uv for faster Python package management
RUN pip install uv

# Copy all necessary files for the build
COPY . ./

# Install dependencies using uv with the virtual environment
RUN uv sync --frozen

# Set environment variables for the MCP server
ENV PYTHONPATH=/app/src
ENV PYTHONUNBUFFERED=1

# Expose port if needed (though MCP typically uses stdio)
EXPOSE 8000

# Default command to run the MCP server using uv run
CMD ["uv", "run", "python", "-m", "bybit_mcp.main"]
