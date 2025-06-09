"""Bybit MCP Server - Model Context Protocol implementation for Bybit trading API.

This server provides access to Bybit's v5 Market API endpoints through the MCP protocol,
enabling AI assistants to fetch real-time market data, instrument information, and
trading statistics.
"""

import asyncio
import json
import logging
from typing import Any, Dict, List

from mcp.server import Server
from mcp.server.lowlevel import NotificationOptions
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    Resource,
    TextContent,
    Tool,
)
from pydantic import AnyUrl

from .market import (
    get_funding_rate_history,
    get_index_price_kline,
    get_instruments_info,
    get_insurance,
    get_kline,
    get_long_short_ratio,
    get_mark_price_kline,
    get_open_interest,
    get_order_book,
    get_premium_index_price_kline,
    get_recent_trades,
    get_risk_limit,
    get_server_time,
    get_tickers,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("bybit-mcp")

# Create the MCP server instance
server = Server("bybit-mcp")


@server.list_tools()
async def handle_list_tools() -> List[Tool]:
    """List all available Bybit market data tools."""
    return [
        Tool(
            name="get_server_time",
            description="Get the current Bybit server time",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        Tool(
            name="get_tickers",
            description="Get ticker information for trading symbols",
            inputSchema={
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "description": "Product type (linear, inverse, option, spot)",
                        "enum": ["linear", "inverse", "option", "spot"],
                        "default": "linear",
                    },
                    "symbol": {
                        "type": "string",
                        "description": "Symbol name (e.g., BTCUSDT)",
                    },
                    "baseCoin": {
                        "type": "string",
                        "description": "Base coin (for option only)",
                    },
                    "expDate": {
                        "type": "string",
                        "description": "Expiry date (for option only, format: 25DEC21)",
                    },
                },
                "required": [],
            },
        ),
        Tool(
            name="get_order_book",
            description="Get order book depth for a trading symbol",
            inputSchema={
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "description": "Product type",
                        "enum": ["linear", "inverse", "option", "spot"],
                        "default": "linear",
                    },
                    "symbol": {
                        "type": "string",
                        "description": "Symbol name (e.g., BTCUSDT)",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Limit for data size per page (1-500)",
                        "minimum": 1,
                        "maximum": 500,
                        "default": 25,
                    },
                },
                "required": ["symbol"],
            },
        ),
        Tool(
            name="get_recent_trades",
            description="Get recent trades for a symbol",
            inputSchema={
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "description": "Product type",
                        "enum": ["linear", "inverse", "option", "spot"],
                        "default": "linear",
                    },
                    "symbol": {
                        "type": "string",
                        "description": "Symbol name (e.g., BTCUSDT)",
                    },
                    "baseCoin": {
                        "type": "string",
                        "description": "Base coin (for option only)",
                    },
                    "optionType": {
                        "type": "string",
                        "description": "Option type (Call or Put, for option only)",
                        "enum": ["Call", "Put"],
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Limit for data size per page (1-1000)",
                        "minimum": 1,
                        "maximum": 1000,
                        "default": 500,
                    },
                },
                "required": ["symbol"],
            },
        ),
        Tool(
            name="get_kline",
            description="Get candlestick/kline data for a symbol",
            inputSchema={
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "description": "Product type",
                        "enum": ["linear", "inverse", "option", "spot"],
                        "default": "linear",
                    },
                    "symbol": {
                        "type": "string",
                        "description": "Symbol name (e.g., BTCUSDT)",
                    },
                    "interval": {
                        "type": "string",
                        "description": "Kline interval",
                        "enum": ["1", "3", "5", "15", "30", "60", "120", "240", "360", "720", "D", "M", "W"],
                        "default": "D",
                    },
                    "start": {
                        "type": "integer",
                        "description": "Start timestamp (ms)",
                    },
                    "end": {
                        "type": "integer",
                        "description": "End timestamp (ms)",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Limit for data size per page (1-1000)",
                        "minimum": 1,
                        "maximum": 1000,
                        "default": 200,
                    },
                },
                "required": ["symbol"],
            },
        ),
        Tool(
            name="get_mark_price_kline",
            description="Get mark price kline data",
            inputSchema={
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "description": "Product type",
                        "enum": ["linear", "inverse"],
                        "default": "linear",
                    },
                    "symbol": {
                        "type": "string",
                        "description": "Symbol name (e.g., BTCUSDT)",
                    },
                    "interval": {
                        "type": "string",
                        "description": "Kline interval",
                        "enum": ["1", "3", "5", "15", "30", "60", "120", "240", "360", "720", "D", "M", "W"],
                        "default": "D",
                    },
                    "start": {
                        "type": "integer",
                        "description": "Start timestamp (ms)",
                    },
                    "end": {
                        "type": "integer",
                        "description": "End timestamp (ms)",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Limit for data size per page (1-1000)",
                        "minimum": 1,
                        "maximum": 1000,
                        "default": 200,
                    },
                },
                "required": ["symbol"],
            },
        ),
        Tool(
            name="get_index_price_kline",
            description="Get index price kline data",
            inputSchema={
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "description": "Product type",
                        "enum": ["linear", "inverse"],
                        "default": "linear",
                    },
                    "symbol": {
                        "type": "string",
                        "description": "Symbol name (e.g., BTCUSDT)",
                    },
                    "interval": {
                        "type": "string",
                        "description": "Kline interval",
                        "enum": ["1", "3", "5", "15", "30", "60", "120", "240", "360", "720", "D", "M", "W"],
                        "default": "D",
                    },
                    "start": {
                        "type": "integer",
                        "description": "Start timestamp (ms)",
                    },
                    "end": {
                        "type": "integer",
                        "description": "End timestamp (ms)",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Limit for data size per page (1-1000)",
                        "minimum": 1,
                        "maximum": 1000,
                        "default": 200,
                    },
                },
                "required": ["symbol"],
            },
        ),
        Tool(
            name="get_premium_index_price_kline",
            description="Get premium index price kline data",
            inputSchema={
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "description": "Product type",
                        "enum": ["linear"],
                        "default": "linear",
                    },
                    "symbol": {
                        "type": "string",
                        "description": "Symbol name (e.g., BTCUSDT)",
                    },
                    "interval": {
                        "type": "string",
                        "description": "Kline interval",
                        "enum": ["1", "3", "5", "15", "30", "60", "120", "240", "360", "720", "D", "M", "W"],
                        "default": "D",
                    },
                    "start": {
                        "type": "integer",
                        "description": "Start timestamp (ms)",
                    },
                    "end": {
                        "type": "integer",
                        "description": "End timestamp (ms)",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Limit for data size per page (1-1000)",
                        "minimum": 1,
                        "maximum": 1000,
                        "default": 200,
                    },
                },
                "required": ["symbol"],
            },
        ),
        Tool(
            name="get_instruments_info",
            description="Get trading instruments information",
            inputSchema={
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "description": "Product type",
                        "enum": ["linear", "inverse", "option", "spot"],
                        "default": "linear",
                    },
                    "symbol": {
                        "type": "string",
                        "description": "Symbol name (e.g., BTCUSDT)",
                    },
                    "baseCoin": {
                        "type": "string",
                        "description": "Base coin",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Limit for data size per page (1-1000)",
                        "minimum": 1,
                        "maximum": 1000,
                        "default": 500,
                    },
                    "cursor": {
                        "type": "string",
                        "description": "Cursor for pagination",
                    },
                },
                "required": [],
            },
        ),
        Tool(
            name="get_funding_rate_history",
            description="Get funding rate history",
            inputSchema={
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "description": "Product type",
                        "enum": ["linear", "inverse"],
                        "default": "linear",
                    },
                    "symbol": {
                        "type": "string",
                        "description": "Symbol name (e.g., BTCUSDT)",
                    },
                    "startTime": {
                        "type": "integer",
                        "description": "Start timestamp (ms)",
                    },
                    "endTime": {
                        "type": "integer",
                        "description": "End timestamp (ms)",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Limit for data size per page (1-200)",
                        "minimum": 1,
                        "maximum": 200,
                        "default": 200,
                    },
                },
                "required": ["symbol"],
            },
        ),
        Tool(
            name="get_open_interest",
            description="Get open interest data",
            inputSchema={
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "description": "Product type",
                        "enum": ["linear", "inverse"],
                        "default": "linear",
                    },
                    "symbol": {
                        "type": "string",
                        "description": "Symbol name (e.g., BTCUSDT)",
                    },
                    "interval": {
                        "type": "string",
                        "description": "Interval time",
                        "enum": ["5min", "15min", "30min", "1h", "4h", "1d"],
                        "default": "5min",
                    },
                    "startTime": {
                        "type": "integer",
                        "description": "Start timestamp (ms)",
                    },
                    "endTime": {
                        "type": "integer",
                        "description": "End timestamp (ms)",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Limit for data size per page (1-200)",
                        "minimum": 1,
                        "maximum": 200,
                        "default": 50,
                    },
                    "cursor": {
                        "type": "string",
                        "description": "Cursor for pagination",
                    },
                },
                "required": ["symbol"],
            },
        ),
        Tool(
            name="get_insurance",
            description="Get insurance fund data",
            inputSchema={
                "type": "object",
                "properties": {
                    "coin": {
                        "type": "string",
                        "description": "Coin name (e.g., BTC, ETH, USDT)",
                    },
                },
                "required": [],
            },
        ),
        Tool(
            name="get_risk_limit",
            description="Get risk limit information",
            inputSchema={
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "description": "Product type",
                        "enum": ["linear", "inverse"],
                        "default": "linear",
                    },
                    "symbol": {
                        "type": "string",
                        "description": "Symbol name (e.g., BTCUSDT)",
                    },
                },
                "required": [],
            },
        ),
        Tool(
            name="get_long_short_ratio",
            description="Get long/short ratio data",
            inputSchema={
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "description": "Product type",
                        "enum": ["linear", "inverse"],
                        "default": "linear",
                    },
                    "symbol": {
                        "type": "string",
                        "description": "Symbol name (e.g., BTCUSDT)",
                    },
                    "interval": {
                        "type": "string",
                        "description": "Data recording interval",
                        "enum": ["5min", "15min", "30min", "1h", "4h", "1d"],
                        "default": "5min",
                    },
                    "startTime": {
                        "type": "integer",
                        "description": "Start timestamp (ms)",
                    },
                    "endTime": {
                        "type": "integer",
                        "description": "End timestamp (ms)",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Limit for data size per page (1-500)",
                        "minimum": 1,
                        "maximum": 500,
                        "default": 50,
                    },
                },
                "required": ["symbol"],
            },
        ),
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """Handle tool calls for Bybit market data endpoints."""
    try:
        if name == "get_server_time":
            result = get_server_time()
            # Extract time information from the response dict
            time_second = result.get("time", "Unknown")
            return [
                TextContent(
                    type="text",
                    text=f"Bybit Server Time: {time_second}",
                )
            ]

        elif name == "get_tickers":
            result = get_tickers(**arguments)
            return [
                TextContent(
                    type="text",
                    text=f"Ticker data for {result.category}:\n{json.dumps(result.dict(), indent=2)}",
                )
            ]

        elif name == "get_order_book":
            result = get_order_book(**arguments)
            return [
                TextContent(
                    type="text",
                    text=f"Order book for {result.s}:\n{json.dumps(result.dict(), indent=2)}",
                )
            ]

        elif name == "get_recent_trades":
            result = get_recent_trades(**arguments)
            return [
                TextContent(
                    type="text",
                    text=f"Recent trades for {result.category}:\n{json.dumps(result.dict(), indent=2)}",
                )
            ]

        elif name == "get_kline":
            result = get_kline(**arguments)
            return [
                TextContent(
                    type="text",
                    text=f"Kline data for {result.symbol} ({result.category}):\n{json.dumps(result.dict(), indent=2)}",
                )
            ]

        elif name == "get_mark_price_kline":
            result = get_mark_price_kline(**arguments)
            return [
                TextContent(
                    type="text",
                    text=f"Mark price kline data for {result.symbol} ({result.category}):\n{json.dumps(result.dict(), indent=2)}",
                )
            ]

        elif name == "get_index_price_kline":
            result = get_index_price_kline(**arguments)
            return [
                TextContent(
                    type="text",
                    text=f"Index price kline data for {result.symbol} ({result.category}):\n{json.dumps(result.dict(), indent=2)}",
                )
            ]

        elif name == "get_premium_index_price_kline":
            result = get_premium_index_price_kline(**arguments)
            return [
                TextContent(
                    type="text",
                    text=f"Premium index price kline data for {result.symbol} ({result.category}):\n{json.dumps(result.dict(), indent=2)}",
                )
            ]

        elif name == "get_instruments_info":
            result = get_instruments_info(**arguments)
            return [
                TextContent(
                    type="text",
                    text=f"Instruments info for {result.category}:\n{json.dumps(result.dict(), indent=2)}",
                )
            ]

        elif name == "get_funding_rate_history":
            result = get_funding_rate_history(**arguments)
            return [
                TextContent(
                    type="text",
                    text=f"Funding rate history for {result.category}:\n{json.dumps(result.dict(), indent=2)}",
                )
            ]

        elif name == "get_open_interest":
            result = get_open_interest(**arguments)
            return [
                TextContent(
                    type="text",
                    text=f"Open interest data for {result.symbol} ({result.category}):\n{json.dumps(result.dict(), indent=2)}",
                )
            ]

        elif name == "get_insurance":
            result = get_insurance(**arguments)
            return [
                TextContent(
                    type="text",
                    text=f"Insurance fund data (updated: {result.updatedTime}):\n{json.dumps(result.dict(), indent=2)}",
                )
            ]

        elif name == "get_risk_limit":
            result = get_risk_limit(**arguments)
            return [
                TextContent(
                    type="text",
                    text=f"Risk limit data for {result.category}:\n{json.dumps(result.dict(), indent=2)}",
                )
            ]

        elif name == "get_long_short_ratio":
            result = get_long_short_ratio(**arguments)
            return [
                TextContent(
                    type="text",
                    text=f"Long/short ratio data:\n{json.dumps(result.dict(), indent=2)}",
                )
            ]

        else:
            return [
                TextContent(
                    type="text",
                    text=f"Unknown tool: {name}",
                )
            ]

    except Exception as e:
        logger.error(f"Error calling tool {name}: {e}")
        return [
            TextContent(
                type="text",
                text=f"Error calling {name}: {str(e)}",
            )
        ]


@server.list_resources()
async def handle_list_resources() -> List[Resource]:
    """List available resources."""
    return [
        Resource(
            uri=AnyUrl("bybit://market/info"),
            name="Bybit Market Information",
            description="General information about Bybit market endpoints and capabilities",
            mimeType="text/plain",
        )
    ]


@server.read_resource()
async def handle_read_resource(uri: AnyUrl) -> str:
    """Read resource content."""
    if str(uri) == "bybit://market/info":
        content = """
# Bybit MCP Server

This MCP server provides access to Bybit's v5 Market API endpoints.

## Available Endpoints:

### Core Market Data
- get_server_time: Get Bybit server time
- get_tickers: Get ticker information for symbols
- get_order_book: Get order book depth
- get_recent_trades: Get recent trade history

### Kline/Candlestick Data
- get_kline: Get standard candlestick data
- get_mark_price_kline: Get mark price klines
- get_index_price_kline: Get index price klines
- get_premium_index_price_kline: Get premium index price klines

### Trading Information
- get_instruments_info: Get trading instrument details
- get_funding_rate_history: Get historical funding rates
- get_open_interest: Get open interest data
- get_risk_limit: Get risk limit information

### Statistics
- get_insurance: Get insurance fund data
- get_long_short_ratio: Get long/short ratio statistics

## Supported Categories:
- linear: USDT perpetual, USDC perpetual, USDC futures
- inverse: Inverse perpetual, Inverse futures
- option: Options
- spot: Spot trading

## Usage:
Each tool accepts parameters specific to the endpoint. Required parameters
are marked in the tool schema. Most tools support optional filtering by
symbol, category, time ranges, and pagination.
        """
        return content.strip()
    else:
        raise ValueError(f"Unknown resource: {uri}")


async def main() -> None:
    """Main entry point for the Bybit MCP server."""
    # Initialize the server
    logger.info("Starting Bybit MCP Server...")

    async with stdio_server() as (read_stream, write_stream):
        logger.info("Server initialized and ready for connections")
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="bybit-mcp",
                server_version="0.1.0",
                capabilities=server.get_capabilities(NotificationOptions(), {}),
            ),
        )


def cli_main() -> None:
    """CLI entry point that wraps the async main function."""
    asyncio.run(main())


if __name__ == "__main__":
    cli_main()
