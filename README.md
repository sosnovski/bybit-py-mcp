# Bybit MCP Server

A Model Context Protocol (MCP) server that provides access to Bybit's v5 Market API endpoints. This server enables AI assistants to fetch real-time market data, instrument information, and trading statistics from the Bybit cryptocurrency exchange.

## Features

### Core Market Data
- **Server Time**: Get current Bybit server time
- **Tickers**: Retrieve ticker information for trading symbols
- **Order Book**: Get order book depth for any symbol
- **Recent Trades**: Access recent trade history

### Kline/Candlestick Data
- **Standard Klines**: Get OHLCV candlestick data
- **Mark Price Klines**: Get mark price historical data
- **Index Price Klines**: Get index price historical data
- **Premium Index Klines**: Get premium index price data

### Trading Information
- **Instruments Info**: Get detailed trading instrument information
- **Funding Rate History**: Access historical funding rates
- **Open Interest**: Get open interest statistics
- **Risk Limits**: Retrieve risk limit information

### Market Statistics
- **Insurance Fund**: Get insurance fund data
- **Long/Short Ratio**: Access long/short ratio statistics

## Supported Categories

- **Linear**: USDT perpetual, USDC perpetual, USDC futures
- **Inverse**: Inverse perpetual, Inverse futures
- **Option**: Options trading
- **Spot**: Spot trading pairs

## Installation

### Prerequisites
- Python 3.13+
- [uv](https://docs.astral.sh/uv/) package manager

### Using uv (Recommended)

1. Clone the repository:
```bash
git clone <repository-url>
cd bybit-mcp
```

2. Install dependencies:
```bash
uv sync
```

3. Set up environment variables:
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your Bybit API credentials
BYBIT_API_KEY=your_api_key_here
BYBIT_API_SECRET=your_api_secret_here
```

4. Run the server:
```bash
uv run bybit-mcp
```

### Using pip

```bash
pip install -e .
python -m bybit_mcp.main
```

## Docker Usage

### Build and Run

```bash
# Build the Docker image
docker build -t bybit-mcp .

# Run with environment variables
docker run -i --rm \
  -e BYBIT_API_KEY=your_api_key \
  -e BYBIT_API_SECRET=your_api_secret \
  bybit-mcp
```

### Using Docker Compose

```bash
# Set environment variables in .env file first
docker-compose up
```

## Configuration

### Environment Variables

- `BYBIT_API_KEY`: Your Bybit API key
- `BYBIT_API_SECRET`: Your Bybit API secret

### VS Code MCP Integration

Add to your VS Code settings.json:

```json
{
  "mcp": {
    "servers": {
      "bybit-mcp": {
        "type": "stdio",
        "command": "uv",
        "args": ["run","-i", "bybit-mcp"],
        "env": {
          "BYBIT_API_KEY": "${input:bybit_api_key}",
          "BYBIT_API_SECRET": "${input:bybit_api_secret}"
        }
      }
    },
    "inputs": [
      {
        "type": "promptString",
        "id": "bybit_api_key",
        "description": "Bybit API Key",
        "password": true
      },
      {
        "type": "promptString",
        "id": "bybit_api_secret",
        "description": "Bybit API Secret",
        "password": true
      }
    ]
  }
}
```

## Testing

### MCP Inspector

Test the server using the MCP inspector:

```bash
npx @modelcontextprotocol/inspector uv run bybit-mcp
```

### Unit Tests

```bash
uv run pytest tests/
```

## API Reference

### Tools

All tools support the following common parameters where applicable:

- `category`: Product type (linear, inverse, option, spot)
- `symbol`: Trading symbol (e.g., BTCUSDT)
- `limit`: Data size limit per page
- `start`/`end`: Time range for historical data

#### Example Tool Calls

**Get Server Time**
```json
{
  "name": "get_server_time",
  "arguments": {}
}
```

**Get Ticker Data**
```json
{
  "name": "get_tickers",
  "arguments": {
    "category": "linear",
    "symbol": "BTCUSDT"
  }
}
```

**Get Kline Data**
```json
{
  "name": "get_kline",
  "arguments": {
    "symbol": "BTCUSDT",
    "interval": "1",
    "category": "linear",
    "limit": 100
  }
}
```

### Resources

- `bybit://market/info`: General information about available endpoints and capabilities

## Development

### Project Structure

```
bybit-mcp/
├── src/bybit_mcp/
│   ├── __init__.py
│   ├── main.py              # MCP server implementation
│   ├── market.py            # Bybit API client
│   └── models/
│       └── market_models.py # Pydantic models
├── tests/
│   └── test_market.py       # Unit tests
├── pyproject.toml           # Project configuration
├── Dockerfile               # Docker configuration
└── README.md
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

### Code Quality

The project uses:
- **Ruff**: For linting and formatting
- **Pytest**: For testing
- **Pydantic**: For data validation
- **Type hints**: For better code documentation

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This software is for educational and development purposes. Always test thoroughly before using in production environments. The authors are not responsible for any financial losses incurred through the use of this software.

## Support

For issues and questions:
1. Check the existing [GitHub Issues](../../issues)
2. Create a new issue with detailed information
3. Provide logs and error messages when applicable

## Acknowledgments

- Built with the [Model Context Protocol](https://modelcontextprotocol.io/)
- Uses the [Bybit API v5](https://bybit-exchange.github.io/docs/v5/intro)
- Powered by [pybit](https://github.com/bybit-exchange/pybit) library