# Bybit MCP Server

> ⚠️ **TRADING WARNING** ⚠️  
> **This MCP server can execute REAL TRADING OPERATIONS on Bybit when `BYBIT_TRADING_ENABLED=true`.**  
> **Trading operations use REAL MONEY and can result in FINANCIAL LOSSES.**  
> **Always test on testnet first (`BYBIT_TESTNET=true`) and understand the risks before enabling trading.**  
> **Trading is DISABLED by default for safety.**

A comprehensive Model Context Protocol (MCP) server that provides full access to Bybit's v5 API. This server enables AI assistants to fetch real-time market data, execute trading operations, manage positions, and access account information from the Bybit cryptocurrency exchange.

## 🚀 **Production Ready** 
✅ **Fully Tested** - All endpoints tested and working  
✅ **Docker Support** - Published image available at `falconiun/bybit-mcp`  
✅ **VS Code Integration** - Ready-to-use configurations provided  
✅ **Comprehensive API Coverage** - Market data, trading, positions, and account management

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
- **Order Management**: Place, amend, and cancel orders with full control
- **Advanced Order Types**: Support for Market, Limit, and conditional/trigger orders
- **Batch Operations**: Execute multiple orders in a single request for efficiency
- **Order History**: View comprehensive open/closed orders and trade history
- **Real-time Execution**: Get immediate feedback on order status and fills
- **Trigger Orders**: Conditional orders with price triggers and advanced stop/take profit logic

### Position Management (Requires `BYBIT_TRADING_ENABLED=true`)
- **Position Info**: Query real-time position data with detailed metrics
- **Leverage Control**: Set and modify position leverage dynamically  
- **Margin Management**: Switch between cross/isolated margin modes
- **Trading Stops**: Set take profit, stop loss, and trailing stops
- **Auto Add Margin**: Configure automatic margin addition
- **Position Modes**: Switch between one-way and hedge position modes
- **P&L Tracking**: Access closed profit and loss records

### Account & Wallet Management
- **Wallet Balance**: Get comprehensive wallet balance information
- **Single Coin Balance**: Query specific coin balances
- **Account Information**: Access detailed account information and settings
- **Multiple Account Types**: Support for UNIFIED, CONTRACT, SPOT, INVESTMENT accounts

## 🎯 Key Capabilities

### ✅ Complete API Coverage
- **Market Data**: All Bybit v5 market endpoints (tickers, order book, klines, funding rates, etc.)
- **Trading**: Full order lifecycle management (place, amend, cancel, batch operations)
- **Advanced Orders**: Conditional/trigger orders with sophisticated entry and exit strategies  
- **Positions**: Complete position management (leverage, margin, stops, P&L tracking)
- **Account**: Wallet balances, account info, and multi-account support

### ✅ Agent-Optimized Design
- **Clear Tool Descriptions**: Each tool has detailed, agent-friendly descriptions explaining purpose and usage
- **Rich Parameter Schemas**: Comprehensive JSON schemas with examples, enums, and validation constraints
- **Safety Warnings**: Important trading tools include prominent safety warnings and risk notices
- **Usage Guidance**: Tools include context about when and how to use them effectively
- **Error Prevention**: Schema validation prevents common parameter mistakes before API calls

### ✅ Production Features
- **Safety First**: Trading disabled by default with explicit enablement required
- **Testnet Support**: Full testnet integration for safe development and testing
- **Error Handling**: Comprehensive error handling with detailed error messages
- **Data Validation**: Pydantic models ensure data integrity and type safety
- **Docker Ready**: Published Docker image with proper environment variable handling

### ✅ Developer Experience  
- **VS Code Integration**: Ready-to-use configurations for both local and Docker deployment
- **MCP Protocol**: Full Model Context Protocol compliance for AI assistant integration
- **Type Safety**: Complete TypeScript-style typing with Pydantic models
- **Testing**: Comprehensive test suite with real API integration
- **Documentation**: Extensive documentation with examples and best practices

## Supported Categories

- **Linear**: USDT perpetual, USDC perpetual, USDC futures
- **Inverse**: Inverse perpetual, Inverse futures
- **Option**: Options trading
- **Spot**: Spot trading pairs

## Installation

### Prerequisites
- Python 3.13+
- [uv](https://docs.astral.sh/uv/) package manager

### Using uvx (Easiest - No Installation Required)

Run directly from PyPi without cloning or installing:
```bash
uvx bybit-mcp@git+https://github.com/sosnovski/bybit-py-mcp.git
```

### Using uv (Recommended for local Development)

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

## Docker Usage

### Build and Run

```bash
# Build the Docker image
docker build -t bybit-mcp .

# Run with environment variables (correct syntax)
docker run -i --rm --init \
  -e BYBIT_API_KEY=your_api_key \
  -e BYBIT_API_SECRET=your_api_secret \
  -e BYBIT_TESTNET=false \
  -e BYBIT_TRADING_ENABLED=false \
  bybit-mcp
```

### Using Docker Compose

```bash
# Set environment variables in .env file first
docker-compose up
```

### Using Published Image

```bash
# Use the published Docker image
docker run -i --rm --init \
  -e BYBIT_API_KEY=your_api_key \
  -e BYBIT_API_SECRET=your_api_secret \
  -e BYBIT_TESTNET=false \
  -e BYBIT_TRADING_ENABLED=false \
  falconiun/bybit-mcp
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

### MCP Client Integration

#### Claude Desktop

To use the Bybit MCP server with Claude Desktop, add the following configuration to your Claude Desktop MCP settings file:

**Location of Claude Desktop MCP config:**
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

**Option 1: Using Published Docker Image (Recommended)**
```json
{
  "mcpServers": {
    "bybit-mcp": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "--init",
        "-e", "BYBIT_API_KEY=your_api_key_here",
        "-e", "BYBIT_API_SECRET=your_api_secret_here",
        "-e", "BYBIT_TESTNET=false",
        "-e", "BYBIT_TRADING_ENABLED=false",
        "falconiun/bybit-mcp"
      ]
    }
  }
}
```

**Option 2: Using uvx (No Installation Required)**
```json
{
  "mcpServers": {
    "bybit-mcp": {
      "command": "uvx",
      "args": [
        "bybit-mcp@git+https://github.com/sosnovski/bybit-py-mcp.git"
      ],
      "env": {
        "BYBIT_API_KEY": "your_api_key_here",
        "BYBIT_API_SECRET": "your_api_secret_here",
        "BYBIT_TESTNET": "false",
        "BYBIT_TRADING_ENABLED": "false"
      }
    }
  }
}
```

**Option 3: Local Development**
```json
{
  "mcpServers": {
    "bybit-mcp": {
      "command": "uv",
      "args": ["run", "bybit-mcp"],
      "cwd": "path/to/your/bybit-mcp",
      "env": {
        "BYBIT_API_KEY": "your_api_key_here",
        "BYBIT_API_SECRET": "your_api_secret_here",
        "BYBIT_TESTNET": "false",
        "BYBIT_TRADING_ENABLED": "false"
      }
    }
  }
}
```

**Important Claude Desktop Notes:**
- Replace `your_api_key_here` and `your_api_secret_here` with your actual Bybit API credentials
- Set `BYBIT_TESTNET=true` for testing with fake money (recommended for first use)
- Set `BYBIT_TRADING_ENABLED=true` only when you want to enable real trading operations
- Restart Claude Desktop after modifying the configuration file

**Claude Desktop Usage Examples:**

Once configured, you can ask Claude Desktop questions like:
- "What's my USDT balance?"
- "What's the current price of BTCUSDT?"
- "Show me the order book for ETHUSDT"
- "Get me the recent trading history for my account"
- "What positions do I currently have open?"

For trading (when `BYBIT_TRADING_ENABLED=true`):
- "Place a limit buy order for 0.001 BTC at $95,000"
- "Cancel all my open orders"
- "Set leverage to 10x for BTCUSDT"
- "Set a stop loss at $90,000 for my BTC position"

**Security Best Practices:**
- Start with `BYBIT_TESTNET=true` to test functionality safely
- Use API keys with minimal required permissions (read-only for market data, trade permissions only when needed)
- Never share your configuration file containing API keys
- Consider using environment variables for sensitive credentials in production

#### Other MCP Clients

This server works with any MCP-compatible client. The configuration format may vary slightly between clients, but the core setup remains the same:

#### VS Code MCP Integration

#### Option 1: Local Development (Recommended)

Add to your VS Code settings.json:

```json
{
  "mcp": {
    "servers": {
      "bybit-mcp": {
        "type": "stdio",
        "command": "uvx",
        "args": ["bybit-mcp"],
        "env": {
          "BYBIT_API_KEY": "${input:bybit_api_key}",
          "BYBIT_API_SECRET": "${input:bybit_api_secret}",
          "BYBIT_TESTNET": "${input:bybit_testnet}",
          "BYBIT_TRADING_ENABLED": "${input:bybit_trading_enabled}"
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
        "description": "Use Bybit Testnet",
        "default": "false"
      },
      {
        "type": "promptString",
        "id": "bybit_trading_enabled",
        "description": "Enable Bybit Trading",
        "default": "false"
      }
    ]
  }
}
```

#### Option 2: Docker (Production)

For using the published Docker image:

```json
{
  "mcp": {
    "servers": {
      "bybit-mcp": {
        "type": "stdio",
        "command": "docker",
        "args": [
          "run",
          "-i",
          "--rm",
          "--init",
          "-e",
          "DOCKER_CONTAINER",
          "-e",
          "BYBIT_API_KEY",
          "-e",
          "BYBIT_API_SECRET",
          "-e",
          "BYBIT_TRADING_ENABLED",
          "-e",
          "BYBIT_TESTNET",
          "falconiun/bybit-mcp"
        ],
        "env": {
          "DOCKER_CONTAINER": "true",
          "BYBIT_API_KEY": "${input:bybit_api_key}",
          "BYBIT_API_SECRET": "${input:bybit_api_secret}",
          "BYBIT_TRADING_ENABLED": "${input:bybit_trading_enabled}",
          "BYBIT_TESTNET": "${input:bybit_testnet}"
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
        "description": "Use Bybit Testnet",
        "default": "false"
      },
      {
        "type": "promptString",
        "id": "bybit_trading_enabled",
        "description": "Enable Bybit Trading",
        "default": "false"
      }
    ]
  }
}
```

**Important Docker Notes:**
- The `-e` flags are required to pass environment variables to the Docker container
- The `env` section sets the variables in VS Code's environment, which are then passed to Docker
- The `--init` flag helps with proper signal handling in containers

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
- `place_order`: Place standard orders (Market, Limit) for immediate or specified price execution
- `place_trigger_order`: Place conditional/trigger orders with advanced stop-loss, take-profit, and market entry strategies
- `amend_order`: Modify existing pending orders (price, quantity, or trigger conditions)
- `cancel_order`: Cancel a specific pending order
- `cancel_all_orders`: Cancel all open orders for enhanced risk management

#### Batch Operations
- `batch_place_order`: Place multiple orders in one request
- `batch_amend_order`: Amend multiple orders in one request
- `batch_cancel_order`: Cancel multiple orders in one request

#### Order Information
- `get_open_closed_orders`: Get open and closed orders
- `get_order_history`: Get order history
- `get_trade_history`: Get trade execution history

#### Wallet & Account Management
- `get_wallet_balance`: Get comprehensive wallet balance information
- `get_single_coin_balance`: Get balance for a specific cryptocurrency
- `get_account_info`: Get detailed account information and settings

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

**Place Trigger Order (Requires Trading Enabled)**
```json
{
  "name": "place_trigger_order",
  "arguments": {
    "category": "linear",
    "symbol": "BTCUSDT",
    "side": "Buy",
    "orderType": "Market",
    "qty": "0.001",
    "triggerPrice": "48000.00",
    "triggerDirection": 2,
    "triggerBy": "LastPrice",
    "orderLinkId": "trigger-buy-123"
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

**Get Wallet Balance**
```json
{
  "name": "get_wallet_balance",
  "arguments": {
    "accountType": "UNIFIED",
    "coin": "USDT"
  }
}
```

**Get Single Coin Balance**
```json
{
  "name": "get_single_coin_balance",
  "arguments": {
    "accountType": "UNIFIED",
    "coin": "BTC"
  }
}
```

**Get Account Info**
```json
{
  "name": "get_account_info",
  "arguments": {}
}
```

### Resources

- `bybit://market/info`: General information about available endpoints and capabilities

## Troubleshooting

### Common Issues

#### Environment Variables Not Working in Docker
- **Problem**: API keys not being passed to Docker container
- **Solution**: Use the `-e` flag format shown in the Docker configuration above
- **Note**: The `env` section in VS Code MCP settings sets variables in VS Code's environment, which are then passed to Docker via `-e` flags

#### Pydantic Validation Errors
- **Problem**: Data type mismatches (e.g., integers vs strings)
- **Solution**: The server includes automatic type conversion for common API inconsistencies
- **Example**: `seq` field in trade history is automatically converted from int to string

#### Trading Operations Disabled
- **Problem**: Trading tools not appearing or returning disabled errors
- **Solution**: Set `BYBIT_TRADING_ENABLED=true` in your environment variables
- **Safety**: This is intentional - trading is disabled by default for safety

#### API Permission Errors
- **Problem**: 401 Unauthorized or insufficient permissions
- **Solution**: Verify your Bybit API key has the required permissions:
  - Read-only: For market data (always safe)
  - Trade: Required for order operations
  - Position: Required for position management

### Debug Mode

Enable debug logging by setting the log level:
```bash
# Local development
PYTHONPATH=src python -c "import logging; logging.basicConfig(level=logging.DEBUG)" -m bybit_mcp.main

# Docker
docker run -e PYTHONPATH=src -e LOG_LEVEL=DEBUG ...
```

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

### Recent Updates

**v0.1.0 - Production Release**
- ✅ Complete Bybit v5 API coverage (market data, trading, positions, accounts)
- ✅ Docker image published to `falconiun/bybit-mcp`
- ✅ Fixed Pydantic validation issues (seq field type conversion)
- ✅ Comprehensive VS Code MCP integration with working Docker configuration
- ✅ Enhanced error handling and safety controls
- ✅ Full wallet and account management support
- ✅ Testnet support for safe development
- ✅ Production-ready with comprehensive testing

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
