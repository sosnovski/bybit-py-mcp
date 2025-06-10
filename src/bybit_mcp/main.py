"""Bybit MCP Server - Model Context Protocol implementation for Bybit trading API.

This server provides access to Bybit's v5 Market API endpoints through the MCP protocol,
enabling AI assistants to fetch real-time market data, instrument information, and
trading statistics.
"""

import asyncio
import json
import logging
from typing import Any, Dict, List

from dotenv import load_dotenv  # Correctly placed
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

# Import market functions
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

# Import trade functions and TRADING_ENABLED flag
from .trade import (
    TRADING_ENABLED,  # Import the flag
    amend_order,
    batch_amend_order,
    batch_cancel_order,
    batch_place_order,
    cancel_all_orders,
    cancel_order,
    get_open_closed_orders,
    get_order_history,
    get_trade_history,
    place_order,
)

# Load environment variables from .env file
load_dotenv()  # Call load_dotenv at the module level

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("bybit-mcp")

# Create the MCP server instance
server = Server("bybit-mcp")


@server.list_tools()
async def handle_list_tools() -> List[Tool]:
    """List all available Bybit market data and trading tools."""
    market_tools = [
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

    active_trade_tools = []
    if TRADING_ENABLED:
        active_trade_tools.extend(
            [
                Tool(
                    name="place_order",
                    description="Place a new order. Trading must be enabled.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "category": {"type": "string", "description": "Product category (linear, spot, option, inverse)"},
                            "symbol": {"type": "string", "description": "Symbol name (e.g., BTCUSDT)"},
                            "side": {"type": "string", "description": "Buy or Sell"},
                            "orderType": {"type": "string", "description": "Market or Limit"},
                            "qty": {"type": "string", "description": "Order quantity"},
                            "price": {"type": "string", "description": "Order price (for Limit orders)"},
                            "isLeverage": {"type": "integer", "description": "Whether to use leverage (spot margin)"},
                            "orderLinkId": {"type": "string", "description": "User-defined order ID"},
                        },
                        "required": ["category", "symbol", "side", "orderType", "qty"],
                    },
                ),
                Tool(
                    name="amend_order",
                    description="Amend an existing order. Trading must be enabled.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "category": {"type": "string", "description": "Product category"},
                            "symbol": {"type": "string", "description": "Symbol name"},
                            "orderId": {"type": "string", "description": "Order ID (either orderId or orderLinkId required)"},
                            "orderLinkId": {"type": "string", "description": "User-defined order ID"},
                            "qty": {"type": "string", "description": "New quantity"},
                            "price": {"type": "string", "description": "New price"},
                            # Add other amendable parameters from trade.py
                        },
                        "required": ["category", "symbol"],
                    },
                ),
                Tool(
                    name="cancel_order",
                    description="Cancel an existing order. Trading must be enabled.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "category": {"type": "string", "description": "Product category"},
                            "symbol": {"type": "string", "description": "Symbol name"},
                            "orderId": {"type": "string", "description": "Order ID (either orderId or orderLinkId required)"},
                            "orderLinkId": {"type": "string", "description": "User-defined order ID"},
                        },
                        "required": ["category", "symbol"],
                    },
                ),
                Tool(
                    name="cancel_all_orders",
                    description="Cancel all open orders for a category/symbol. Trading must be enabled.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "category": {"type": "string", "description": "Product category"},
                            "symbol": {"type": "string", "description": "Symbol name (optional)"},
                            "baseCoin": {"type": "string", "description": "Base coin (optional)"},
                            "settleCoin": {"type": "string", "description": "Settle coin (optional)"},
                            "orderFilter": {"type": "string", "description": "Order filter (e.g., Order, StopOrder) (optional)"},
                        },
                        "required": ["category"],
                    },
                ),
                Tool(
                    name="batch_place_order",
                    description="Place a batch of new orders. Trading must be enabled.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "category": {"type": "string", "description": "Product category"},
                            "request": {
                                "type": "array",
                                "description": "List of order creation requests",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "symbol": {"type": "string"},
                                        "side": {"type": "string"},
                                        "orderType": {"type": "string"},
                                        "qty": {"type": "string"},
                                        "price": {"type": "string"},
                                        "orderLinkId": {"type": "string"},
                                        # Add other relevant batch place order item fields
                                    },
                                    "required": ["symbol", "side", "orderType", "qty"],
                                },
                            },
                        },
                        "required": ["category", "request"],
                    },
                ),
                Tool(
                    name="batch_amend_order",
                    description="Amend a batch of existing orders. Trading must be enabled.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "category": {"type": "string", "description": "Product category"},
                            "request": {
                                "type": "array",
                                "description": "List of order amendment requests",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "symbol": {"type": "string"},
                                        "orderId": {"type": "string"},
                                        "orderLinkId": {"type": "string"},
                                        "qty": {"type": "string"},
                                        "price": {"type": "string"},
                                        # Add other relevant batch amend order item fields
                                    },
                                    "required": ["symbol"],  # orderId or orderLinkId also effectively required per item
                                },
                            },
                        },
                        "required": ["category", "request"],
                    },
                ),
                Tool(
                    name="batch_cancel_order",
                    description="Cancel a batch of existing orders. Trading must be enabled.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "category": {"type": "string", "description": "Product category"},
                            "request": {
                                "type": "array",
                                "description": "List of order cancellation requests",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "symbol": {"type": "string"},
                                        "orderId": {"type": "string"},
                                        "orderLinkId": {"type": "string"},
                                        # Add other relevant batch cancel order item fields
                                    },
                                    "required": ["symbol"],  # orderId or orderLinkId also effectively required per item
                                },
                            },
                        },
                        "required": ["category", "request"],
                    },
                ),
            ]
        )

    # These are read-only and can always be listed
    trade_info_tools = [
        Tool(
            name="get_open_closed_orders",
            description="Get open and closed orders for a category/symbol.",
            inputSchema={
                "type": "object",
                "properties": {
                    "category": {"type": "string", "description": "Product category"},
                    "symbol": {"type": "string", "description": "Symbol name (optional)"},
                    # Add other params like baseCoin, orderId, limit, cursor
                },
                "required": ["category"],
            },
        ),
        Tool(
            name="get_order_history",
            description="Get order history for a category/symbol.",
            inputSchema={
                "type": "object",
                "properties": {
                    "category": {"type": "string", "description": "Product category"},
                    "symbol": {"type": "string", "description": "Symbol name (optional)"},
                    # Add other params like orderStatus, startTime, endTime, limit
                },
                "required": ["category"],
            },
        ),
        Tool(
            name="get_trade_history",
            description="Get trade history (executions) for a category/symbol.",
            inputSchema={
                "type": "object",
                "properties": {
                    "category": {"type": "string", "description": "Product category"},
                    "symbol": {"type": "string", "description": "Symbol name (optional)"},
                    # Add other params like execType, limit, startTime, endTime
                },
                "required": ["category"],
            },
        ),
    ]

    return market_tools + active_trade_tools + trade_info_tools  # Combined active_trade_tools


@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """Handle tool calls for Bybit market data and trading endpoints."""
    try:
        # Market Data Tools
        if name == "get_server_time":
            result = get_server_time()
            return [
                TextContent(
                    type="text",
                    text=f"Bybit Server Time: {result.get('timeSecond', 'Unknown')}\nFull Response: {json.dumps(result, indent=2)}",
                )
            ]
        elif name == "get_tickers":
            result = get_tickers(**arguments)
            return [TextContent(type="text", text=f"Ticker data for {result.category}:\n{json.dumps(result.dict(), indent=2)}")]
        elif name == "get_order_book":
            result = get_order_book(**arguments)
            return [TextContent(type="text", text=f"Order book for {result.s}:\n{json.dumps(result.dict(), indent=2)}")]
        elif name == "get_recent_trades":
            result = get_recent_trades(**arguments)
            return [TextContent(type="text", text=f"Recent trades for {result.category}:\n{json.dumps(result.dict(), indent=2)}")]
        elif name == "get_kline":
            result = get_kline(**arguments)
            return [
                TextContent(type="text", text=f"Kline data for {result.symbol} ({result.category}):\n{json.dumps(result.dict(), indent=2)}")
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
            return [TextContent(type="text", text=f"Instruments info for {result.category}:\n{json.dumps(result.dict(), indent=2)}")]
        elif name == "get_funding_rate_history":
            result = get_funding_rate_history(**arguments)
            return [TextContent(type="text", text=f"Funding rate history for {result.category}:\n{json.dumps(result.dict(), indent=2)}")]
        elif name == "get_open_interest":
            result = get_open_interest(**arguments)
            return [
                TextContent(
                    type="text", text=f"Open interest data for {result.symbol} ({result.category}):\n{json.dumps(result.dict(), indent=2)}"
                )
            ]
        elif name == "get_insurance":
            result = get_insurance(**arguments)
            return [
                TextContent(
                    type="text", text=f"Insurance fund data (updated: {result.updatedTime}):\n{json.dumps(result.dict(), indent=2)}"
                )
            ]
        elif name == "get_risk_limit":
            result = get_risk_limit(**arguments)
            return [TextContent(type="text", text=f"Risk limit data for {result.category}:\n{json.dumps(result.dict(), indent=2)}")]
        elif name == "get_long_short_ratio":
            result = get_long_short_ratio(**arguments)
            return [TextContent(type="text", text=f"Long/short ratio data:\n{json.dumps(result.dict(), indent=2)}")]

        # Trading Tools (TRADING_ENABLED check is now primarily within trade.py functions)
        # The tools are only listed if TRADING_ENABLED is true,
        # but the functions in trade.py provide a secondary check.
        elif name == "place_order":
            result = place_order(**arguments)
            return [TextContent(type="text", text=f"Place Order Response:\n{json.dumps(result.dict(), indent=2)}")]
        elif name == "amend_order":
            result = amend_order(**arguments)
            return [TextContent(type="text", text=f"Amend Order Response:\n{json.dumps(result.dict(), indent=2)}")]
        elif name == "cancel_order":
            result = cancel_order(**arguments)
            return [TextContent(type="text", text=f"Cancel Order Response:\n{json.dumps(result.dict(), indent=2)}")]
        elif name == "get_open_closed_orders":  # Read-only
            result = get_open_closed_orders(**arguments)
            return [TextContent(type="text", text=f"Open/Closed Orders:\n{json.dumps(result.dict(), indent=2)}")]
        elif name == "cancel_all_orders":
            result = cancel_all_orders(**arguments)
            return [TextContent(type="text", text=f"Cancel All Orders Response:\n{json.dumps(result.dict(), indent=2)}")]
        elif name == "get_order_history":  # Read-only
            result = get_order_history(**arguments)
            return [TextContent(type="text", text=f"Order History:\n{json.dumps(result.dict(), indent=2)}")]
        elif name == "get_trade_history":  # Read-only
            result = get_trade_history(**arguments)
            return [TextContent(type="text", text=f"Trade History:\n{json.dumps(result.dict(), indent=2)}")]
        elif name == "batch_place_order":
            result = batch_place_order(**arguments)
            return [TextContent(type="text", text=f"Batch Place Order Response:\n{json.dumps(result.dict(), indent=2)}")]
        elif name == "batch_amend_order":
            result = batch_amend_order(**arguments)
            return [TextContent(type="text", text=f"Batch Amend Order Response:\n{json.dumps(result.dict(), indent=2)}")]
        elif name == "batch_cancel_order":
            result = batch_cancel_order(**arguments)
            return [TextContent(type="text", text=f"Batch Cancel Order Response:\n{json.dumps(result.dict(), indent=2)}")]
        # ... (add handlers for get_spot_borrow_quota and set_dcp if implemented) ...

        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]

    except Exception as e:
        logger.error(f"Error calling tool {name} with arguments {arguments}: {e}", exc_info=True)
        return [TextContent(type="text", text=f"Error calling {name}: {str(e)}")]


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
