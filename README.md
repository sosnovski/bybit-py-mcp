# Bybit MCP Server

> ⚠️ **TRADING WARNING** ⚠️  
> **This MCP server can execute REAL TRADING OPERATIONS on Bybit when `BYBIT_TRADING_ENABLED=true`.**  
> **Trading operations use REAL MONEY and can result in FINANCIAL LOSSES.**  
> **Always test on testnet first (`BYBIT_TESTNET=true`) and understand the risks before enabling trading.**  
> **Trading is DISABLED by default for safety.**

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

### Trading Operations (Requires `BYBIT_TRADING_ENABLED=true`)
- **Order Management**: Place, amend, and cancel orders
- **Batch Operations**: Execute multiple orders in a single request
- **Order History**: View open/closed orders and trade history
- **Order Types**: Support for Market, Limit, and conditional orders

### Position Management (Requires `BYBIT_TRADING_ENABLED=true`)
- **Position Info**: Query real-time position data
- **Leverage Control**: Set and modify position leverage
- **Margin Management**: Switch between cross/isolated margin modes
- **Trading Stops**: Set take profit, stop loss, and trailing stops
- **Auto Add Margin**: Configure automatic margin addition
- **Position Modes**: Switch between one-way and hedge position modes
- **P&L Tracking**: Access closed profit and loss records

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
BYBIT_TESTNET=false  # Set to true for testnet
BYBIT_TRADING_ENABLED=false  # Set to true to enable trading operations
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
  -e BYBIT_TESTNET=false \  # Set to true for testnet
  -e BYBIT_TRADING_ENABLED=false \  # Set to true to enable trading
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
- `BYBIT_TESTNET`: Set to `true` to use the Bybit testnet (default is `false`)
- `BYBIT_TRADING_ENABLED`: Set to `true` to enable trading operations (default is `false`)

### Safety Controls

The server implements several safety controls for trading operations:

#### Trading Disabled by Default
- All trading and position management tools are **disabled by default**
- Must explicitly set `BYBIT_TRADING_ENABLED=true` to enable trading
- Market data tools are always available regardless of this setting

#### Testnet Support
- Set `BYBIT_TESTNET=true` to use Bybit's testnet environment
- Recommended for development and testing
- Testnet trading uses fake money and won't affect real balances

#### Tool Visibility
- Trading tools only appear in the tool list when `BYBIT_TRADING_ENABLED=true`
- Position management tools require the same flag
- This prevents accidental trading operations

#### API Permissions
Ensure your Bybit API key has the appropriate permissions:
- **Read-only**: For market data (always safe)
- **Trade**: Required for order operations (enable only when needed)
- **Position**: Required for position management
- **Withdraw**: Not required for this server

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
          "BYBIT_API_SECRET": "${input:bybit_api_secret}",
          "BYBIT_TESTNET": "false",
          "BYBIT_TRADING_ENABLED": "false"
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
      },
      {
        "type": "promptString",
        "id": "bybit_testnet",
        "description": "Use Bybit Testnet (true/false)",
        "default": "false"
      },
      {
        "type": "promptString",
        "id": "bybit_trading_enabled",
        "description": "Enable Trading Operations (true/false)",
        "default": "false"
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

### Market Data Tools

All market data tools are always available and do not require special permissions.

#### Core Data
- `get_server_time`: Get current Bybit server time
- `get_tickers`: Get ticker information for symbols
- `get_order_book`: Get order book depth
- `get_recent_trades`: Get recent trade history

#### Kline/Candlestick Data
- `get_kline`: Get standard OHLCV kline data
- `get_mark_price_kline`: Get mark price historical data
- `get_index_price_kline`: Get index price historical data
- `get_premium_index_price_kline`: Get premium index kline data

#### Market Information
- `get_instruments_info`: Get trading instrument details
- `get_funding_rate_history`: Get funding rate history
- `get_open_interest`: Get open interest statistics
- `get_insurance`: Get insurance fund data
- `get_risk_limit`: Get risk limit information
- `get_long_short_ratio`: Get long/short ratio data

### Trading Tools (Requires `BYBIT_TRADING_ENABLED=true`)

These tools are only available when trading is enabled via the `BYBIT_TRADING_ENABLED` environment variable.

#### Order Management
- `place_order`: Place a new order (Market, Limit, etc.)
- `amend_order`: Modify an existing order
- `cancel_order`: Cancel a specific order
- `cancel_all_orders`: Cancel all open orders

#### Batch Operations
- `batch_place_order`: Place multiple orders in one request
- `batch_amend_order`: Amend multiple orders in one request
- `batch_cancel_order`: Cancel multiple orders in one request

#### Order Information
- `get_open_closed_orders`: Get open and closed orders
- `get_order_history`: Get order history
- `get_trade_history`: Get trade execution history

### Position Tools (Requires `BYBIT_TRADING_ENABLED=true`)

Position management tools require trading to be enabled.

#### Position Information
- `get_position_info`: Query real-time position data
- `get_closed_pnl`: Get closed profit and loss records

#### Position Configuration
- `set_leverage`: Set position leverage
- `switch_cross_isolated_margin`: Switch margin mode
- `switch_position_mode`: Switch between one-way/hedge mode
- `set_auto_add_margin`: Configure automatic margin addition

#### Risk Management
- `set_trading_stop`: Set take profit, stop loss, trailing stops
- `modify_position_margin`: Add or reduce position margin

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

**Place Order (Requires Trading Enabled)**
```json
{
  "name": "place_order",
  "arguments": {
    "category": "linear",
    "symbol": "BTCUSDT",
    "side": "Buy",
    "orderType": "Limit",
    "qty": "0.001",
    "price": "50000.00",
    "orderLinkId": "my-order-123"
  }
}
```

**Get Position Info (Requires Trading Enabled)**
```json
{
  "name": "get_position_info",
  "arguments": {
    "category": "linear",
    "symbol": "BTCUSDT"
  }
}
```

**Set Leverage (Requires Trading Enabled)**
```json
{
  "name": "set_leverage",
  "arguments": {
    "category": "linear",
    "symbol": "BTCUSDT",
    "buyLeverage": "10",
    "sellLeverage": "10"
  }
}
```

**Set Trading Stop (Requires Trading Enabled)**
```json
{
  "name": "set_trading_stop",
  "arguments": {
    "category": "linear",
    "symbol": "BTCUSDT",
    "takeProfit": "55000.00",
    "stopLoss": "45000.00",
    "positionIdx": 0
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
│   ├── market.py            # Market data API functions
│   ├── trade.py             # Trading API functions
│   ├── position.py          # Position management functions
│   └── models/
│       ├── market_models.py # Market data Pydantic models
│       ├── trade_models.py  # Trading Pydantic models
│       └── position_models.py # Position Pydantic models
├── tests/
│   ├── test_market.py       # Market data unit tests
│   └── test_trade.py        # Trading unit tests
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

## Support the Project

If you find this MCP server useful for your trading and development needs, consider supporting its continued development:

[![Support on Patreon](https://img.shields.io/badge/Support-Patreon-orange.svg)](https://patreon.com/BrianCusack)

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/W7W31G9CXW)

Your support helps maintain and improve this project, add new features, and ensure compatibility with the latest Bybit API updates. Thank you for considering a contribution!

## Acknowledgments

- Built with the [Model Context Protocol](https://modelcontextprotocol.io/)
- Uses the [Bybit API v5](https://bybit-exchange.github.io/docs/v5/intro)
- Powered by [pybit](https://github.com/bybit-exchange/pybit) library